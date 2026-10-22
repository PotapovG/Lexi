"use strict";
const assert=require("assert");
const fs=require("fs");
const vm=require("vm");
const src=fs.readFileSync("/app/greek_word_audio.js","utf8");
assert(!/\bspeechSynthesis\b|\bSpeechSynthesisUtterance\b|\bgetUserMedia\b|\bMediaRecorder\b/.test(src),
  "Pocket-only code must not access device TTS, mic or browser voice");
function harness(fail=false){
  const requests=[];
  let calls=0;
  class AudioMock{
    constructor(url){this.url=url;this.playbackRate=1;requests.push(this);}
    play(){calls++;return fail?Promise.reject(Error("missing WAV")):Promise.resolve();}
    pause(){}removeAttribute(){}load(){}
  }
  const window={
    speechSynthesis:{getVoices(){throw Error("device voice accessed")}},
    SpeechSynthesisUtterance:class{constructor(){throw Error("device TTS invoked")}}
  };
  const ctx={window,Audio:AudioMock};
  vm.runInNewContext(src,ctx);
  return {player:window.LexiWordAudio,requests,invocations:()=>calls};
}
(async()=>{
  const yes=harness(),states=[],file="/greek/pronunciation/"+"a".repeat(32)+".wav";
  assert(yes.player.available({audioSource:"pocket",audioUrl:file}));
  assert(await yes.player.play({audioSource:"pocket",speechText:"σπίτι",audioUrl:file},
   {slow:true,onStatus:s=>states.push(s)}));
  assert.deepStrictEqual(states,["pocket"]);
  assert(yes.requests.length===1&&yes.requests[0].playbackRate===0.78);
  const missing=harness(),missingStates=[];
  assert(!missing.player.available({audioSource:"unavailable",audioUrl:null}));
  assert(!await missing.player.play({audioSource:"unavailable",speechText:"μήλο",audioUrl:null},
    {onStatus:s=>missingStates.push(s)}));
  assert.deepStrictEqual(missingStates,["unavailable"]);
  assert(missing.invocations()===0);
  const failed=harness(true),failStates=[];
  assert(!await failed.player.play({audioSource:"pocket",speechText:"ευχαριστώ",audioUrl:file},
    {onStatus:s=>failStates.push(s)}));
  assert.deepStrictEqual(failStates,["error"]);
  assert(failed.invocations()===1);
  for(const unsafe of [
    "https://evil.example/test.wav","/greek/pronunciation/../../foo.wav",
    "/greek/audio/cat.mp3","/greek/pronunciation/"+"g".repeat(32)+".wav"
  ])assert(!yes.player.available({audioSource:"pocket",audioUrl:unsafe}));
  const harmless=harness();
  assert(!harmless.player.available({audioSource:"device",audioUrl:file}));
  assert(harmless.invocations()===0);
  console.log("PASS POCKET ONLY: valid WAV, 0.78x, missing unavailable, failed WAV no fallback, strict hashed media URL; even installed device TTS never invoked");
})().catch(e=>{console.error(e);process.exitCode=1;});
