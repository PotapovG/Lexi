"use strict";
(() => {
  const $=id=>document.getElementById(id),lang=()=>window.LexiUI.lang(),t=(key,values)=>window.LexiUI.t(key,values);
  const text=(tag,value,css)=>{const n=document.createElement(tag);if(value!==undefined)n.textContent=String(value);if(css)n.className=css;return n;};
  const button=(label,fn,css="primary life-button")=>{const b=text("button",label,css);b.type="button";b.addEventListener("click",fn);return b;};
  const root=()=>$("life-roleplay-content");
  const uuid=()=>window.crypto?.randomUUID?.()||"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,c=>{const r=Math.floor(Math.random()*16);return(c==="x"?r:r&3|8).toString(16);});
  let overview=null,current=null,busy=false,activeMode="hub",pending=null,currentReceipt=null,renderEpoch=0,deferPending=null,ownerGeneration=0;
  const visible=()=>!$("life-view").hidden;
  function remember(){
    try{if(current)sessionStorage.setItem("lexi-life-scene-v1",JSON.stringify({owner:window.LexiApp?.accountKey(),id:current.id,lang:lang()}));
      else sessionStorage.removeItem("lexi-life-scene-v1");
      if(pending)sessionStorage.setItem("lexi-life-pending-v1",JSON.stringify({owner:window.LexiApp?.accountKey(),...pending}));
      else sessionStorage.removeItem("lexi-life-pending-v1");
      if(deferPending)sessionStorage.setItem("lexi-life-defer-v1",JSON.stringify({owner:window.LexiApp?.accountKey(),...deferPending}));
      else sessionStorage.removeItem("lexi-life-defer-v1");}catch{}
  }
  function notice(value,bad=false,retry){
    const n=$("life-message");n.hidden=!value;n.replaceChildren();if(value)n.append(text("span",value));
    n.className="track-message"+(bad?" bad":"");if(retry)n.append(button(t("retry"),retry,"secondary"));
  }
  function failure(error,retry){
    if(error.message==="account_changed")return;
    if(error.status===401||error.message==="login_required"){window.LexiApp?.requireLogin();return;}
    notice(t("network"),true,retry);
  }
  async function api(kind,data,requestedLang,expectedOwner){
    const owner=expectedOwner||window.LexiApp?.accountKey();
    if(data&&(!window.LexiApp?.loggedIn()||!owner))throw Error("account_changed");
    const language=data?.lang||requestedLang||lang();
    const url=kind.startsWith("scene:")?"/greek/api/life/scene?id="+encodeURIComponent(kind.slice(6)):
      kind==="life"?"/greek/api/life":"/greek/api/life/scene";
    const response=await fetch(url+(url.includes("?")?"&":"?")+"lang="+encodeURIComponent(language),{
      credentials:"same-origin",cache:"no-store",...(data?{method:"POST",headers:{"Content-Type":"application/json","X-Lexi-Owner":owner},body:JSON.stringify({...data,lang:language})}:{})});
    const result=await response.json().catch(()=>({}));
    if(owner!==window.LexiApp?.accountKey())throw Error("account_changed");
    if(!response.ok){if(result.error==="account_changed")window.LexiApp?.reconcileAccount?.();const err=Error(result.error||"HTTP "+response.status);err.status=response.status;throw err;}return result;
  }
  function illustration(id){
    const wrap=text("div",undefined,"life-illustration");if(window.LexiScenes)wrap.append(window.LexiScenes.illustration(id));return wrap;
  }
  function renderHub(){
    renderEpoch++;activeMode="hub";$("life-content").hidden=true;root().hidden=false;root().replaceChildren();
    const scene=overview?.nextAdventure;
    if(!scene){root().append(text("p",t("noMaterial"),"life-muted"));return;}
    const shell=text("article",undefined,"life-adventure-card");
    shell.append(illustration(scene.id));const body=text("div",undefined,"life-adventure-info");
    body.append(text("span",t("nextStep"),"life-quest-eyebrow"),text("h3",scene.name,"life-adventure-title"));
    body.append(text("p",t(scene.correct?"reviewAgain":"fresh")+" · "+t("chapter")+" "+scene.chapter,"life-adventure-subtitle"));
    body.append(button(t("resume"),startRecommended,"primary life-continue"));shell.append(body);root().append(shell);
    const progress=text("p",t("sceneProgress")+": "+overview.completedExperiences+" / "+overview.totalExperiences,"life-progress-count");root().append(progress);
  }
  function feedback(result,receipt,selected){
    if(!visible()||activeMode!=="scene")return;
    currentReceipt=receipt;const form=root().querySelector("form"),panel=root().querySelector(".life-answer-feedback");
    form.querySelector("textarea").disabled=true;form.querySelector(".life-task-actions").replaceChildren();panel.replaceChildren();panel.hidden=false;
    const heading=text("h3",t(result.correct?"correct":result.unverified?"unverified":"wrong"),result.correct?"life-feedback-good":result.unverified?"life-feedback-caution":"life-feedback-bad");
    heading.id="life-feedback-title";panel.append(heading);
    if(!result.correct&&selected){const original=text("p",t("yourAnswer")+": "+selected,"life-muted");original.dir="auto";panel.append(original);}
    if(result.explanation)panel.append(text("p",result.explanation,"life-feedback-explanation"));
    if(result.orthographyNote)panel.append(text("p",result.orthographyNote,"life-orthography-note"));
    const canonical=text("p",result.closestAnswer||result.answer,"life-feedback-greek");canonical.lang="el";canonical.dir="ltr";panel.append(text("strong",t("correction")),canonical);
    const alternatives=[result.answer,...result.alternatives||[]].filter((v,i,a)=>v&&v!==(result.closestAnswer||result.answer)&&a.indexOf(v)===i);
    if(alternatives.length){const details=text("details");details.append(text("summary",t("alternatives")));const list=text("p",alternatives.join(" / "));list.lang="el";list.dir="ltr";details.append(list);panel.append(details);}
    if(result.translation){const translation=text("p",t("meaning")+": "+result.translation,"life-feedback-meaning");translation.lang=result.translationLang||lang();translation.dir=translation.lang==="ar"?"rtl":"ltr";panel.append(translation);}
    panel.append(text("p",t("finalAnswer"),"life-muted"));
    const next=button(t("nextScene"),()=>continueAfterFeedback(result,receipt),"primary life-continue");next.setAttribute("aria-describedby","life-feedback-title");panel.append(next);
    notice(t("saved"));queueMicrotask(()=>next.focus({preventScroll:true}));
  }
  function showTask(draft=""){
    renderEpoch++;activeMode="scene";$("life-content").hidden=true;root().hidden=false;root().replaceChildren();
    const wrapper=text("article",undefined,"life-task-card"),body=text("div",undefined,"life-task-body");
    wrapper.append(illustration(current.id));body.append(text("span",t("chapter")+" "+current.chapter,"life-quest-eyebrow"));
    const heading=text("h2",current.prompt,"life-task-prompt");heading.id="life-question-heading";heading.lang=current.promptLang||lang();heading.dir=heading.lang==="ar"?"rtl":"ltr";body.append(heading);
    if(current.promptLang&&current.promptLang!==lang())body.append(text("p",t("translationUnavailable"),"life-muted"));
    if(current.hint){const hint=text("p",t("hint")+": "+current.hint,"life-hint-strip");hint.dir="auto";body.append(hint);}
    const form=text("form",undefined,"life-answer-form"),label=text("label",t("typeGreek"));label.htmlFor="life-answer";
    const input=text("textarea");input.id="life-answer";input.rows=3;input.maxLength=320;input.lang="el";input.dir="ltr";input.autocomplete="off";input.spellcheck=false;input.value=draft;
    const actions=text("div",undefined,"life-task-actions"),submit=text("button",t("check"),"primary life-continue");submit.type="submit";submit.disabled=!draft.trim();
    const error=text("p",undefined,"life-muted");error.setAttribute("role","alert");error.hidden=true;
    input.addEventListener("input",()=>{submit.disabled=!input.value.trim()||busy;error.hidden=true;});
    input.addEventListener("keydown",event=>{if(event.key==="Enter"&&!event.shiftKey&&!event.isComposing){event.preventDefault();form.requestSubmit();}});
    actions.append(submit,button(t("toLessons"),()=>window.LexiApp?.setPage("board"),"secondary life-secondary"));
    const panel=text("section",undefined,"life-answer-feedback");panel.hidden=true;panel.setAttribute("role","status");panel.setAttribute("aria-live","polite");
    form.append(label,input,error,actions,panel);body.append(form);wrapper.append(body);root().append(wrapper);
    form.addEventListener("submit",event=>{event.preventDefault();if(busy||currentReceipt)return;
      if(!input.value.trim()){error.textContent=t("emptyAnswer");error.hidden=false;return;}
      if(!pending)pending={owner:window.LexiApp?.accountKey(),body:{revision:current.revision,id:current.id,answer:input.value.trim(),requestId:uuid(),lang:lang()}};
      remember();submitPending();
    });
    heading.tabIndex=-1;heading.focus({preventScroll:true});remember();
    if(current.lastReceipt)feedback(current.lastReceipt.feedback,current.lastReceipt,current.lastReceipt.selected);
    else if(pending){input.disabled=true;submit.disabled=true;notice(t("unknown"),true,recover);}
  }
  async function submitPending(){
    if(busy||!pending)return;busy=true;const generation=ownerGeneration;notice(t("saving"));
    const epoch=renderEpoch,submission=pending;
    root().querySelectorAll("textarea,button").forEach(el=>el.disabled=true);
    try{
      const result=await api("scene",submission.body,null,submission.owner);current.revision=result.revision;
      const receipt=result.lastReceipt||{requestId:submission.body.requestId,questionId:submission.body.id,selected:submission.body.answer,feedback:result};
      pending=null;remember();currentReceipt=receipt;
      if(epoch===renderEpoch&&visible())feedback(receipt.feedback||result,receipt,submission.body.answer);
      document.dispatchEvent(new CustomEvent("lexi:progress",{detail:{source:"life"}}));
    }catch(error){
      if(error.message==="account_changed")return;
      try{
        const fresh=await api("scene:"+submission.body.id,null,submission.body.lang);current=fresh;
        if(fresh.lastReceipt){pending=null;remember();currentReceipt=fresh.lastReceipt;if(epoch===renderEpoch&&visible())feedback(fresh.lastReceipt.feedback,fresh.lastReceipt,fresh.lastReceipt.selected);}
        else if(fresh.revision!==submission.body.revision){pending=null;remember();if(epoch===renderEpoch&&visible())showTask(submission.body.answer);notice(t("conflict"),true);}
        else notice(t("unknown"),true,recover);
      }catch{notice(t("unknown"),true,recover);}
    }finally{if(generation===ownerGeneration)busy=false;}
  }
  async function recover(){
    if(busy||!pending)return;busy=true;const generation=ownerGeneration;
    try{
      const fresh=await api("scene:"+pending.body.id,null,pending.body.lang);current=fresh;
      if(fresh.lastReceipt){const receipt=fresh.lastReceipt;pending=null;remember();showTask();feedback(receipt.feedback,receipt,receipt.selected);return;}
      if(fresh.revision!==pending.body.revision){const draft=pending.body.answer;pending=null;remember();showTask(draft);notice(t("conflict"),true);return;}
    }catch(error){failure(error,recover);return;}finally{if(generation===ownerGeneration)busy=false;}
    if(pending)submitPending();
  }
  async function loadScene(id){
    if(busy)return;busy=true;const generation=ownerGeneration;notice("");
    try{current=await api("scene:"+id);currentReceipt=null;showTask(pending?.body.id===id?pending.body.answer:"");}
    catch(error){failure(error,()=>loadScene(id));}finally{if(generation===ownerGeneration)busy=false;}
  }
  function startRecommended(){
    if(busy||!overview?.nextAdventure)return;
    const scene=overview.nextAdventure;
    if(scene.type==="roleplay")return loadScene(scene.id);
    current=null;currentReceipt=null;remember();activeMode="activity";root().hidden=true;$("life-content").hidden=false;window.lexiTracks?.openLife?.(scene.id);
  }
  async function refresh(){
    overview=await api("life");const select=$("life-max-chapter");select.replaceChildren();
    for(let i=1;i<=overview.printedChapterCount;i++){const option=text("option",t("chapter")+" "+i);option.value=i;select.append(option);}
    select.value=overview.maxChapter;$("life-scope-label").textContent=t("scope");$("life-description").textContent=t("lifeIntro");renderHub();
  }
  async function continueAfterFeedback(result,receipt){
    if(busy)return;busy=true;const generation=ownerGeneration;notice(t("saving"));
    const finishedId=current?.id||receipt?.questionId;
    try{
      if(receipt?.requestId){const ack=await api("scene",{action:"ack_feedback",id:finishedId,requestId:receipt.requestId});if(ack.revision!=null&&current)current.revision=ack.revision;}
      if(!result.correct){
        if(!deferPending)deferPending={owner:window.LexiApp?.accountKey(),body:{action:"skip",revision:current.revision,id:finishedId,requestId:uuid(),lang:lang()},receiptId:receipt?.requestId};
        remember();overview=await api("life",deferPending.body,null,deferPending.owner);deferPending=null;
      }
      current=null;currentReceipt=null;pending=null;remember();await refresh();notice("");
      document.dispatchEvent(new CustomEvent("lexi:progress"));
    }catch(error){failure(error,()=>continueAfterFeedback(result,receipt));return;}finally{if(generation===ownerGeneration)busy=false;}
    if(overview?.nextAdventure?.id&&overview.nextAdventure.id!==finishedId)startRecommended();
    else notice(t("reviewAgain"));
  }
  async function nextAdventure(){
    if(busy)return;busy=true;const generation=ownerGeneration;
    try{current=null;currentReceipt=null;remember();await refresh();notice("");}
    catch(error){failure(error,nextAdventure);return;}finally{if(generation===ownerGeneration)busy=false;}startRecommended();
  }
  async function open(){
    if(!visible()||busy||window.LexiApp?.loggedIn()===false)return;busy=true;const generation=ownerGeneration;notice(t("loading"));
    let saved=null;try{
      saved=JSON.parse(sessionStorage.getItem("lexi-life-scene-v1")||"null");
      const stored=JSON.parse(sessionStorage.getItem("lexi-life-pending-v1")||"null");
      if(stored?.owner===window.LexiApp?.accountKey())pending=stored;
      const deferred=JSON.parse(sessionStorage.getItem("lexi-life-defer-v1")||"null");
      if(deferred?.owner===window.LexiApp?.accountKey())deferPending=deferred;
      if(saved?.owner!==window.LexiApp?.accountKey()||saved?.lang!==lang())saved=null;
    }catch{}
    try{
      if(deferPending){overview=await api("life",deferPending.body,null,deferPending.owner);deferPending=null;pending=null;saved=null;current=null;remember();}
      await refresh();notice("");if(saved?.id){current=await api("scene:"+saved.id);currentReceipt=null;showTask(pending?.body.id===saved.id?pending.body.answer:"");}
    }
    catch(error){failure(error,open);}finally{if(generation===ownerGeneration)busy=false;}
  }
  async function changeChapter(value,body){
    if(!overview||busy)return;busy=true;const generation=ownerGeneration;
    body=body||{revision:overview.revision,maxChapter:Number(value),requestId:uuid(),lang:lang()};
    try{overview=await api("life",body);current=null;currentReceipt=null;pending=null;remember();await refresh();notice("");}
    catch(error){failure(error,()=>changeChapter(value,body));}finally{if(generation===ownerGeneration)busy=false;}
  }
  document.addEventListener("lexi:logout",()=>{ownerGeneration++;busy=false;renderEpoch++;current=null;pending=null;currentReceipt=null;overview=null;deferPending=null;});
  $("life-max-chapter").addEventListener("change",event=>changeChapter(event.target.value));
  async function changeLanguage(){
    if(!visible()||busy)return;
    if(activeMode==="activity"){window.lexiTracks?.onLanguageChange?.();return;}
    const id=current?.id,draft=root().querySelector("textarea")?.value||"";busy=true;const generation=ownerGeneration;
    try{await refresh();if(id){current=await api("scene:"+id);currentReceipt=null;showTask(draft);}}
    catch(error){failure(error,changeLanguage);}finally{if(generation===ownerGeneration)busy=false;}
  }
  window.lexiLife={onOpen:open,onLanguageChange:changeLanguage,onLeave:()=>{renderEpoch++;window.LexiWordAudio?.stop();remember();},advanceFromActivity:nextAdventure,showSimulation:()=>{activeMode="activity";root().hidden=true;$("life-content").hidden=false;}};
})();
