"use strict";
(() => {
  // Greek Life is a guided adventure. Only one learner-facing preference:
  // the last studied textbook chapter. Scenario order is account-adaptive.
  const $=id=>document.getElementById(id);
  const COPY={
    ru:{
      chapter:"Я дошёл до главы",intro:"Тренируй греческий так, как будто уже живёшь на Кипре.",
      eyebrow:"ТВОЁ СЛЕДУЮЩЕЕ ПРИКЛЮЧЕНИЕ",play:"Продолжить приключение",resume:"Продолжить",
      scene:"Ситуация",mission:"ТВОЯ ЗАДАЧА",guide:"Небольшая подсказка",type:"Напиши по-гречески",
      check:"Ответить",good:"Отлично! Тебя поняли.",bad:"Почти! Попробуй исправить фразу.",
      unsure:"Фраза может быть допустимой. Ошибку не засчитываем.",
      explain:"Почему не подошло?",right:"Так можно сказать",mean:"Что это значит",
      next:"Следующая ситуация",back:"На главную",progress:"Ситуаций освоено",
      fresh:"Новая ситуация",returning:"Повторение знакомого",guided:"С подсказкой",
      independent:"Без подсказок",loading:"Подбираем ситуацию…",
      error:"Не удалось загрузить приключение",round:"Твой путь",
      needsLanguage:"(перевод на английском)",notScored:"Неуверенный вариант не штрафуем — можно продолжить."
    },
    en:{
      chapter:"I've studied through chapter",intro:"Put your Greek to work in everyday situations.",
      eyebrow:"YOUR NEXT ADVENTURE",play:"Continue the adventure",resume:"Continue",
      scene:"Scene",mission:"YOUR MISSION",guide:"A helpful hint",type:"Write in Greek",
      check:"Send reply",good:"Great! They understood you.",bad:"Almost! Try adjusting your phrase.",
      unsure:"That may be valid Greek. No mistake is recorded.",
      explain:"What needs adjusting?",right:"A natural way to say it",mean:"Meaning",
      next:"Next scene",back:"Home",progress:"Scenes mastered",
      fresh:"New scene",returning:"Practice again",guided:"With hints",
      independent:"Without hints",loading:"Finding your next moment…",
      error:"Couldn't open the adventure",round:"Your journey",
      needsLanguage:"(English translation)",notScored:"This unverified answer won't count as a mistake."
    }
  };
  const t=key=>(COPY[$("lang").value]||COPY.en)[key]||COPY.en[key]||key;
  const lang=()=>$("lang").value;
  const text=(tag,value,css)=>{
    const n=document.createElement(tag);n.textContent=String(value??"");
    if(css)n.className=css;
    return n;
  };
  const button=(title,click,css)=>{
    const n=document.createElement("button");n.type="button";
    n.className=css||"primary life-button";n.textContent=title;
    n.addEventListener("click",click);return n;
  };
  const root=()=>$("life-roleplay-content");
  const art=id=>{
    const wrapper=document.createElement("div");wrapper.className="life-illustration";
    if(window.LexiScenes)wrapper.append(window.LexiScenes.illustration(id));
    return wrapper;
  };
  let overview=null,current=null,busy=false,activeMode="hub";
  function notice(value,bad=false){
    const n=$("life-message");n.hidden=!value;n.textContent=value||"";
    n.className="track-message"+(bad?" bad":"");
  }
  async function api(kind,data){
    const url=kind.startsWith("scene:")?"/greek/api/life/scene?id="+encodeURIComponent(kind.slice(6)):
      kind==="life"?"/greek/api/life":"/greek/api/life/scene";
    const params=data?"":"&lang="+encodeURIComponent(lang());
    const final=url+(url.includes("?")?params:"?lang="+encodeURIComponent(lang()));
    const response=await fetch(final,{credentials:"same-origin",cache:"no-store",
      ...(data?{method:"POST",headers:{"Content-Type":"application/json"},
        body:JSON.stringify({...data,lang:lang()})}:{})});
    const body=await response.json().catch(()=>({}));
    if(!response.ok)throw Error(body.error||"HTTP "+response.status);
    return body;
  }
  function onlyHub(){
    activeMode="hub";
    $("life-content").hidden=true;
    root().hidden=false;
    current=null;
  }
  function backgroundScene(){
    const scene=overview.nextAdventure;
    if(!scene)return null;
    return scene;
  }
  function heroHeader(scene){
    const heading=document.createElement("div");heading.className="life-scene-head";
    const label=text("span",t("eyebrow"),"life-quest-eyebrow");
    heading.append(label);
    heading.append(text("span",t(scene.difficulty==="independent"?"independent":"guided"),
      "life-quest-difficulty"));
    return heading;
  }
  function progress(row){
    const box=document.createElement("div");box.className="life-progress";
    const line=document.createElement("div");line.className="life-progress-line";
    line.append(text("span",t("progress"),"life-progress-title"));
    line.append(text("strong",overview.completedExperiences+" / "+overview.totalExperiences,
      "life-progress-count"));
    box.append(line);
    const track=document.createElement("div");track.className="life-progress-track";
    const fill=document.createElement("div");fill.className="life-progress-fill";
    fill.style.width=(overview.totalExperiences?
      Math.round(100*overview.completedExperiences/overview.totalExperiences):0)+"%";
    track.append(fill);box.append(track);
    return box;
  }
  function renderHub(){
    onlyHub();
    const el=root();el.replaceChildren();
    const scene=backgroundScene();
    if(!scene)return;
    const shell=document.createElement("div");shell.className="life-adventure-card";
    shell.append(art(scene.id));
    const bottom=document.createElement("div");bottom.className="life-adventure-info";
    bottom.append(heroHeader(scene));
    bottom.append(text("h3",scene.name,"life-adventure-title"));
    bottom.append(text("p",t(scene.correct?"returning":"fresh")+" · "+
      (lang()==="ru"?"Глава ":"Chapter ")+scene.chapter,"life-adventure-subtitle"));
    bottom.append(button(t("play"),startRecommended,"primary life-continue"));
    shell.append(bottom);el.append(shell);
    el.append(progress(scene));
  }
  function showTask(){
    $("life-content").hidden=true;
    root().hidden=false;
    activeMode="scene";
    const el=root();el.replaceChildren();
    const wrapper=document.createElement("div");wrapper.className="life-task-card";
    wrapper.append(art(current.id));
    const task=document.createElement("div");task.className="life-task-body";
    task.append(text("span",t("scene")+" "+current.chapter,"life-quest-eyebrow"));
    task.append(text("div",t("mission"),"life-mission-label"));
    task.append(text("h3",current.prompt,"life-task-prompt"));
    if(current.promptLang!==lang())task.append(text("p",t("needsLanguage"),"life-muted"));
    if(current.hint)task.append(text("div",t("guide")+": "+current.hint,"life-hint-strip"));
    const form=document.createElement("form");form.className="life-answer-form";
    const input=document.createElement("textarea");input.rows=2;input.maxLength=320;
    input.lang="el";input.dir="ltr";input.autocomplete="off";
    input.placeholder="Γράψε στα ελληνικά…";input.setAttribute("aria-label",t("type"));
    form.append(input);
    const actions=document.createElement("div");actions.className="life-task-actions";
    const submit=document.createElement("button");submit.type="submit";
    submit.className="primary life-continue";submit.textContent=t("check");
    actions.append(submit);
    actions.append(button(t("back"),renderHub,"secondary life-secondary"));
    form.append(actions);
    const feedback=document.createElement("div");feedback.className="life-answer-feedback";
    form.append(feedback);task.append(form);
    wrapper.append(task);el.append(wrapper);
    form.addEventListener("submit",async e=>{
      e.preventDefault();if(busy||!input.value.trim())return;
      busy=true;submit.disabled=true;notice("");
      try{
        const result=await api("scene",{revision:current.revision,id:current.id,answer:input.value});
        current.revision=result.revision;feedback.replaceChildren();
        const success=result.correct;
        const header=text("div",t(success?"good":result.unverified?"unsure":"bad"),
          success?"life-feedback-good":result.unverified?"life-feedback-caution":"life-feedback-bad");
        feedback.append(header);
        if(result.explanation){
          feedback.append(text("strong",t("explain"),"life-feedback-label"));
          feedback.append(text("p",result.explanation,"life-feedback-explanation"));
        }
        if(result.orthographyNote)
          feedback.append(text("p",result.orthographyNote,"life-orthography-note"));
        feedback.append(text("strong",t("right"),"life-feedback-label"));
        const shown=result.closestAnswer||result.answer;
        feedback.append(text("p",shown,"life-feedback-greek"));
        const otherOptions=[result.answer,...(result.alternatives||[])]
          .filter((value,i,all)=>value!==shown&&all.indexOf(value)===i);
        if(otherOptions.length){
          const more=document.createElement("details");
          more.className="life-more-answers";
          const summary=document.createElement("summary");
          summary.textContent=lang()==="ru"?"Другие допустимые формулировки":"Other accepted wordings";
          more.append(summary,text("p",otherOptions.join(" / "),"life-muted"));
          feedback.append(more);
        }
        feedback.append(text("p",t("mean")+": "+result.translation+
          (result.translationLang!==lang()?" (EN)":""),"life-feedback-meaning"));
        if(success){
          submit.hidden=true;input.disabled=true;
          actions.replaceChildren(button(t("next"),nextAdventure,"primary life-continue"));
        }else{
          input.focus();input.select();
          submit.disabled=false;
          if(result.unverified){
            feedback.append(text("p",t("notScored"),"life-muted"));
            feedback.append(button(t("next"),skipUnverified,"secondary life-secondary"));
          }
        }
      }catch(error){
        if(error.message==="stale_track")return await loadScene(current.id);
        notice(t("error")+": "+error.message,true);
      }finally{busy=false;if(!input.disabled)submit.disabled=false;}
    });
    input.focus();
  }
  async function loadScene(id){
    if(busy)return;busy=true;notice("");
    try{current=await api("scene:"+id);showTask();}
    catch(error){notice(t("error")+": "+error.message,true);}
    finally{busy=false;}
  }
  function startRecommended(){
    if(!overview?.nextAdventure||busy)return;
    const scene=overview.nextAdventure;
    if(scene.type==="roleplay")return loadScene(scene.id);
    activeMode="activity";
    root().hidden=true;
    $("life-content").hidden=false;
    window.lexiTracks?.openLife?.(scene.id);
  }
  async function refresh(){
    overview=await api("life");
    const select=$("life-max-chapter");
    select.replaceChildren();
    for(let i=1;i<=overview.printedChapterCount;i++){
      const option=document.createElement("option");option.value=String(i);
      option.textContent=(lang()==="ru"?"Глава ":"Chapter ")+i;
      select.append(option);
    }
    select.value=String(overview.maxChapter);
    $("life-scope-label").textContent=t("chapter");
    $("life-description").textContent=t("intro");
    renderHub();
  }
  async function skipUnverified(){
    if(busy||!current)return;
    busy=true;
    try{
      overview=await api("life",{action:"skip",revision:current.revision,id:current.id});
      renderHub();
    }catch(error){notice(t("error")+": "+error.message,true);}
    finally{busy=false;}
    if(!busy)startRecommended();
  }
  async function nextAdventure(){
    if(busy)return;busy=true;
    try{await refresh();}
    catch(error){notice(t("error")+": "+error.message,true);}
    finally{busy=false;}
    if(!busy)startRecommended();
  }
  async function open(){
    if($("life-view").hidden||busy)return;
    busy=true;notice("");
    try{await refresh();}
    catch(error){notice(t("error")+": "+error.message,true);}
    finally{busy=false;}
  }
  async function changeChapter(value){
    if(!overview||busy)return;
    busy=true;notice("");
    try{
      overview=await api("life",{revision:overview.revision,maxChapter:Number(value)});
      await refresh();
    }catch(error){
      notice(t("error")+": "+error.message,true);
      if(error.message==="stale_track")await refresh();
    }finally{busy=false;}
  }
  $("life-max-chapter").addEventListener("change",e=>changeChapter(e.target.value));
  window.lexiLife={onOpen:open,advanceFromActivity:nextAdventure,
    showSimulation:()=>{activeMode="activity";root().hidden=true;$("life-content").hidden=false;}};
})();
