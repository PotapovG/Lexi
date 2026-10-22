"use strict";
(() => {
  // Strict offline Pocket TTS playback. Never uses a device TTS voice,
  // browser/device speech engines, microphone, or remote synthesis APIs.
  const WAV=/^\/greek\/(?:audio|pronunciation)\/[a-f0-9]{32}\.wav$/;
  let audio=null,revision=0;
  function stop(){
    revision++;
    if(audio){
      try{audio.pause();audio.removeAttribute("src");audio.load();}catch{}
      audio=null;
    }
  }
  function available(meta){
    return !!(meta && meta.audioSource==="pocket" &&
      typeof meta.audioUrl==="string" && WAV.test(meta.audioUrl));
  }
  async function play(meta,{slow=false,onStatus=()=>{}}={}){
    stop();
    if(!available(meta)){onStatus("unavailable");return false;}
    const current=revision;
    const clip=new Audio(meta.audioUrl);
    audio=clip;
    clip.preload="auto";
    clip.playbackRate=slow?0.78:1;
    clip.onended=()=>{if(revision===current)onStatus("done");};
    clip.onerror=()=>{if(revision===current)onStatus("error");};
    try{
      await clip.play();
      if(revision!==current){clip.pause();return false;}
      onStatus("pocket");
      return true;
    }catch{
      if(revision===current){
        audio=null;
        onStatus("error");
      }
      return false;
    }
  }
  window.LexiWordAudio={play,stop,available};
})();
