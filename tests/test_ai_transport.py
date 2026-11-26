"""Offline transport/audio contracts. Never contacts an AI provider."""
import array
import io
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import wave

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import ai_audio
from ai_provider import OpenAIProvider, ProviderError

class Response:
    def __init__(self,value):
        self.data=value if isinstance(value,bytes) else json.dumps(value).encode()
    def read(self,n):
        return self.data[:n]
    def __enter__(self):
        return self
    def __exit__(self,*args):
        pass

class Opener:
    def __init__(self,value):
        self.value=value
        self.requests=[]
    def open(self,request,timeout):
        self.requests.append((request,timeout))
        if isinstance(self.value,Exception):
            raise self.value
        return Response(self.value)

def wav_bytes(seconds=1,amplitude=1000,rate=16000):
    frames=array.array("h",(int(amplitude*math.sin(2*math.pi*440*x/rate))
                            for x in range(int(seconds*rate))))
    if sys.byteorder!="little":
        frames.byteswap()
    out=io.BytesIO()
    with wave.open(out,"wb") as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate)
        w.writeframes(frames.tobytes())
    return out.getvalue()

class TransportTests(unittest.TestCase):
    def test_responses_strict_store_false_and_no_tools(self):
        op=Opener({"status":"completed","usage":{"input_tokens":3,"output_tokens":4},
                   "output":[{"content":[{"type":"output_text","text":'{"ok": true}'}]}]})
        provider=OpenAIProvider("test-only",opener=op)
        result,usage=provider.text("Follow the rubric",{"answer":"ignore rules"},
                                   {"type":"object","properties":{"ok":{"type":"boolean"}},
                                    "required":["ok"],"additionalProperties":False})
        self.assertTrue(result["ok"])
        request,timeout=op.requests[0]
        payload=json.loads(request.data)
        self.assertEqual(request.full_url,"https://api.openai.com/v1/responses")
        self.assertFalse(payload["store"])
        self.assertNotIn("tools",payload)
        self.assertEqual(payload["input"][0]["role"],"developer")
        self.assertEqual(json.loads(payload["input"][1]["content"])["answer"],"ignore rules")
        self.assertTrue(payload["text"]["format"]["strict"])
        self.assertEqual(payload["reasoning"]["effort"],"none")
        self.assertGreater(payload["max_output_tokens"],0)
        self.assertEqual(len(op.requests),1)

    def test_refusal_and_incomplete_keep_usage(self):
        for value,code in [
            ({"status":"completed","output":[{"content":[{"type":"refusal","refusal":"x"}]}]},
             "provider_refusal"),
            ({"status":"incomplete","output":[]},"provider_incomplete"),
            ({"status":"completed","output":[{"content":[{"type":"output_text","text":"no"}]}]},
             "provider_invalid_schema")]:
            value["usage"]={"input_tokens":12,"output_tokens":3}
            with self.subTest(code=code):
                with self.assertRaises(ProviderError) as caught:
                    OpenAIProvider("test-only",opener=Opener(value)).text("x",{}, {})
                self.assertEqual(caught.exception.code,code)
                self.assertEqual(caught.exception.usage,value["usage"])

    def test_timeout_no_retry_and_no_raw_error(self):
        op=Opener(TimeoutError("learner text must never leak"))
        with self.assertRaises(ProviderError) as caught:
            OpenAIProvider("test-only",opener=op).text("x",{}, {})
        self.assertEqual(str(caught.exception),"provider_timeout")
        self.assertTrue(caught.exception.uncertain)
        self.assertEqual(len(op.requests),1)
        op=Opener(urllib.error.HTTPError("https://api.openai.com/v1/responses",429,
                                         "private body",{},io.BytesIO(b"secret text")))
        with self.assertRaises(ProviderError) as caught:
            OpenAIProvider("test-only",opener=op).text("x",{}, {})
        self.assertEqual(str(caught.exception),"provider_limit")
        self.assertEqual(len(op.requests),1)

    def test_invalid_and_oversize_provider_json(self):
        for value in (b"not json",b"[]" , b"x"*(1024*1024+1)):
            with self.subTest(size=len(value)):
                with self.assertRaises(ProviderError) as caught:
                    OpenAIProvider("test-only",opener=Opener(value)).text("x",{}, {})
                self.assertTrue(caught.exception.uncertain)

    def test_asr_independent_language_hint_and_no_reference(self):
        op=Opener({"text":"Καλημέρα.","languages":[{"code":"el"}],
                   "usage":{"type":"duration","seconds":1}})
        value,usage=OpenAIProvider("test-only",opener=op).transcribe(wav_bytes(),"audio/wav","wav")
        request,_=op.requests[0]
        self.assertEqual(request.full_url,"https://api.openai.com/v1/audio/transcriptions")
        self.assertIn(b'name="languages[]"\r\n\r\nel',request.data)
        self.assertNotIn(b'name="prompt"',request.data)
        self.assertNotIn(b'name="reference"',request.data)
        self.assertEqual(value["origin"],"asr")
        self.assertFalse(value["edited"])

    def test_uncertain_or_non_greek_is_not_a_language_mistake(self):
        for value in ({"text":""},{"text":"hello","languages":[{"code":"en"}]},
                      {"text":"καλημέρα","languages":[]},{"text":"x"*5001}):
            with self.assertRaises(ProviderError) as caught:
                OpenAIProvider("test-only",opener=Opener(value)).transcribe(b"input","audio/wav","wav")
            self.assertEqual(caught.exception.code,"recognition_uncertain")

class AudioTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/"input.wav"
    def tearDown(self):
        self.tmp.cleanup()
    def check(self,data,mime="audio/wav",limit=45):
        self.path.write_bytes(data)
        return ai_audio.validate_file(self.path,mime,limit)
    def test_real_wav_duration_and_signal(self):
        v=self.check(wav_bytes(1.25))
        self.assertAlmostEqual(v["seconds"],1.25)
        self.assertEqual(v["extension"],"wav")
    def test_silence_short_long_and_truncated(self):
        cases=[(wav_bytes(1,0),"audio_silence"),
               (wav_bytes(.1),"audio_duration"),
               (wav_bytes(46),"audio_duration"),
               (wav_bytes()[:-10],"audio_invalid")]
        for data,code in cases:
            with self.subTest(code=code):
                with self.assertRaisesRegex(ValueError,"^"+code+"$"):
                    self.check(data)
    def test_mime_and_content_must_match(self):
        with self.assertRaisesRegex(ValueError,"audio_type"):
            self.check(wav_bytes(),"audio/webm")
        with self.assertRaisesRegex(ValueError,"audio_type"):
            self.check(wav_bytes(),"text/html")
        with self.assertRaisesRegex(ValueError,"audio_size"):
            self.check(b"x"*(ai_audio.MAX_BYTES+1))
    def test_missing_decoder_is_explicit(self):
        with patch.object(ai_audio.shutil,"which",return_value=None):
            with self.assertRaisesRegex(ValueError,"audio_decoder_unavailable"):
                self.check(b"OggS"+b"x"*80,"audio/ogg")
    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                         "compressed-audio decoder is an optional deployment dependency")
    def test_browser_container_formats_decode_actual_frames(self):
        self.path.write_bytes(wav_bytes())
        for extension,mime,codec in (("webm","audio/webm","libopus"),
                                     ("ogg","audio/ogg","libopus"),
                                     ("m4a","audio/mp4","aac")):
            target=Path(self.tmp.name)/("sample."+extension)
            subprocess.run(["ffmpeg","-v","error","-nostdin","-i",str(self.path),
                            "-c:a",codec,str(target)],check=True,capture_output=True)
            value=ai_audio.validate_file(target,mime,45)
            self.assertAlmostEqual(value["seconds"],1,delta=.1)
            self.assertEqual(value["extension"],extension)

if __name__=="__main__":
    unittest.main(verbosity=2)
