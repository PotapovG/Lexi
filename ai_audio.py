"""Bounded audio validation before paid transcription; no permanent recordings."""
from __future__ import annotations
import array
import io
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import wave

MAX_BYTES = 10 * 1024 * 1024
MIMES = {"audio/webm": ("webm", "matroska"), "audio/ogg": ("ogg", "ogg"),
         "audio/mp4": ("m4a", "mov"), "audio/x-m4a": ("m4a", "mov"),
         "audio/wav": ("wav", "wav"), "audio/x-wav": ("wav", "wav")}

def validate_file(path, mime, limit_seconds):
    mime = mime.split(";", 1)[0].strip().lower()
    if mime not in MIMES:
        raise ValueError("audio_type")
    data = Path(path).read_bytes()
    if not 44 <= len(data) <= MAX_BYTES:
        raise ValueError("audio_size")
    extension, demuxer = MIMES[mime]
    signatures = {"wav": data[:4] == b"RIFF" and data[8:12] == b"WAVE",
                  "webm": data[:4] == b"\x1aE\xdf\xa3",
                  "ogg": data[:4] == b"OggS",
                  "m4a": data[4:8] == b"ftyp"}
    if not signatures[extension]:
        raise ValueError("audio_type")
    if extension == "wav":
        try:
            with wave.open(io.BytesIO(data)) as audio:
                rate, channels, width = audio.getframerate(), audio.getnchannels(), audio.getsampwidth()
                if not 8000 <= rate <= 96000 or not 1 <= channels <= 2 or width != 2:
                    raise ValueError("audio_format")
                duration = audio.getnframes() / rate
                if not .25 <= duration <= limit_seconds:
                    raise ValueError("audio_duration")
                pcm = audio.readframes(audio.getnframes())
                if len(pcm) != audio.getnframes() * channels * width:
                    raise ValueError("audio_invalid")
        except (wave.Error, EOFError):
            raise ValueError("audio_invalid") from None
    else:
        if not shutil.which("ffprobe") or not shutil.which("ffmpeg"):
            raise ValueError("audio_decoder_unavailable")
        try:
            common = ["-v", "error", "-protocol_whitelist", "file,pipe",
                      "-format_whitelist", demuxer, "-f", demuxer, "-i", str(path)]
            probe = subprocess.run(["ffprobe", *common, "-show_entries",
                                    "format=duration:stream=codec_type",
                                    "-of", "json"], capture_output=True, timeout=8, check=True)
            info = json.loads(probe.stdout)
            streams = info.get("streams", [])
            if not streams or any(x.get("codec_type") != "audio" for x in streams):
                raise ValueError("audio_streams")
            duration = float(info.get("format", {}).get("duration", "nan"))
            # Browser WebM may omit duration. Decode at a bounded ceiling and
            # measure actual PCM samples; never trust the client timer.
            if math.isfinite(duration) and not .25 <= duration <= limit_seconds:
                raise ValueError("audio_duration")
            decoded = subprocess.run(
                ["ffmpeg", "-nostdin", "-threads", "1", *common, "-vn", "-ac", "1",
                 "-ar", "16000", "-t", str(limit_seconds + 1), "-f", "s16le", "pipe:1"],
                capture_output=True, timeout=12, check=True)
            pcm = decoded.stdout
            duration = len(pcm) / 32000
            if not .25 <= duration <= limit_seconds:
                raise ValueError("audio_duration")
        except (subprocess.SubprocessError, ValueError, KeyError, TypeError) as error:
            if isinstance(error, ValueError) and str(error).startswith("audio_"):
                raise
            raise ValueError("audio_invalid") from None
    samples = array.array("h")
    samples.frombytes(pcm)
    if sys.byteorder != "little":
        samples.byteswap()
    rms = math.sqrt(sum(x*x for x in samples) / max(1, len(samples)))
    if rms < 30:
        raise ValueError("audio_silence")
    return {"seconds": duration, "mime": mime, "extension": extension,
            "bytes": len(data)}

def available():
    return bool(shutil.which("ffprobe") and shutil.which("ffmpeg"))
