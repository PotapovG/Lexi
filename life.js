"use strict";
(() => {
  const $=id=>document.getElementById(id);
  const messages={
    ru:{
      scope:"Изучено до главы включительно",desc:"Применяй знакомые слова в реальных ситуациях. Доступные задания зависят от глав и твоего прогресса.",
      recommended:"Подойдёт сейчас",guided:"С подсказкой",independent:"Самостоятельно",
      start:"Попробовать ситуацию",answer:"Напиши ответ по-гречески",check:"Проверить",
      right:"Верно! Фраза засчитана.",wrong:"Нужно исправить ответ.",
      unverified:"Не уверен, что этот вариант неверен. Ошибка не засчитана.",
      retry:"Попробуй ещё раз",back:"Выбрать другую ситуацию",correct:"Пример правильного ответа",
      why:"Почему ответ не подошёл",meaning:"Перевод",progress:"Практика по аккаунту",
      errors:"ошибок",completed:"правильных",need:"Доступно после главы",
      all:"Сценарии по пройденным главам",later:"Необязательная подсказка",
      unsupported:"Для этого варианта ответ не подтверждён. Сравни с проверенными фразами.",
      noActivity:"Это задание откроется на более позднем этапе."
    },
    en:{
      scope:"Studied up to chapter",desc:"Apply familiar words in everyday situations. Scenes are bounded by your chosen chapters and learning history.",
      recommended:"Recommended for you",guided:"With a hint",independent:"Independent",
      start:"Try this situation",answer:"Write the Greek answer",check:"Check",
      right:"Correct! Your answer is accepted.",wrong:"Correct the answer to continue.",
      unverified:"This alternative is not verified; no mistake is recorded.",
      retry:"Try again",back:"Choose another scene",correct:"Reviewed correct answer",
      why:"Why this answer did not fit",meaning:"Meaning",progress:"Your progress",
      errors:"mistakes",completed:"correct",need:"Available after chapter",
      all:"Situations from studied chapters",later:"Optional hint",
      unsupported:"This alternative is not verified. Compare with the reviewed answers.",
      noActivity:"This situation unlocks at a later learning stage."
    }
  };
  const lang=()=>$("lang").value;
  const text=(tag,value,css)=>{
    const el=document.createElement(tag);el.textContent=String(value||"");
    if(css)el.className=css;return el;
  };
  const button=(caption,action,css="secondary")=>{
    const el=document.createElement("button");el.type="button";
    el.className=css+" track-button";el.textContent=caption;
    el.addEventListener("click",action);return el;
  };
  const t=key=>(messages[lang()]||messages.en)[key]||messages.en[key]||key;
  let overview=null,current=null,shownLang=null,busy=false;
  const root=()=>$("life-roleplay-content");
  function notice(message,bad=false){
    const node=$("life-message");node.hidden=!message;node.textContent=message||"";
    node.className="track-message"+(bad?" bad":"");
  }
  async function api(name,payload=null){
    const query=payload?"":"?lang="+encodeURIComponent(lang())+(name.startsWith("scene:")?"&id="+encodeURIComponent(name.slice(6)):"");
    const route=name.startsWith("scene:")?"scene":name;
    const path=name==="life"?"/greek/api/life":"/greek/api/life/"+route;
    const res=await fetch(path+query,{credentials:"same-origin",cache:"no-store",
      ...(payload?{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({...payload,lang:lang()})}:{})});
    const body=await res.json().catch(()=>({}));
    if(!res.ok)throw Error(body.error||"HTTP "+res.status);
    return body;
  }
  function status(){
    $("life-description").textContent=t("desc");
    $("life-scope-label").textContent=t("scope");
    $("life-max-chapter").value=String(overview.maxChapter);
    $("life-progress-note").textContent=t("progress")+": "+overview.observations+
      " · "+overview.masteredWords+" mastered words";
    for(const [id,chapter] of [["route",6],["periptero",8],["likes",16]]){
      const node=$("track-"+id+"-mode");node.hidden=overview.maxChapter<chapter;
    }
  }
  function showRoleplay(){
    $("life-content").hidden=true;
    root().hidden=false;
    $("life-roleplay-mode").classList.add("active");
    ["route","periptero","likes"].forEach(x=>$("track-"+x+"-mode").classList.remove("active"));
  }
  function showSimulation(){
    $("life-content").hidden=false;
    root().hidden=true;
    $("life-roleplay-mode").classList.remove("active");
    current=null;
    notice("");
  }
  function renderMenu(){
    showRoleplay();
    const el=root();el.replaceChildren();
    const available=overview.available.filter(x=>x.type==="roleplay");
    el.append(text("h3",t("all"),"track-subtitle"));
    const recommended=available.find(x=>x.id===overview.recommended);
    if(recommended)el.append(text("p",t("recommended")+": "+recommended.name,"track-meta"));
    const grid=document.createElement("div");grid.className="life-scenes";
    available.forEach(scene=>{
      const card=document.createElement("div");card.className="life-scene";
      const title=text("strong",scene.name);card.append(title);
      card.append(text("p",(lang()==="ru"?"Глава ":"Chapter ")+scene.chapter+
         " · "+t(scene.difficulty)+" · "+scene.attempts+" "+t("progress"),"track-small"));
      card.append(text("p",scene.errors+" "+t("errors")+" · "+scene.attempts+" attempts","track-small"));
      card.append(button(t("start"),()=>loadScene(scene.id),"secondary"));
      grid.append(card);
    });
    el.append(grid);
  }
  async function loadScene(id){
    if(busy)return;busy=true;notice("");
    try{current=await api("scene:"+id);renderScene();}
    catch(e){notice(e.message,true);}
    finally{busy=false;}
  }
  function renderScene(){
    showRoleplay();
    const host=root();host.replaceChildren();
    host.append(button(t("back"),renderMenu));
    host.append(text("div",current.title+" · "+current.chapter,"track-eyebrow"));
    host.append(text("h3",current.prompt,"life-prompt"));
    if(current.promptLang!==lang())host.append(text("p","(EN)","track-small"));
    if(current.hint)host.append(text("p",t("later")+": "+current.hint,"life-hint"));
    const form=document.createElement("form");form.className="life-form";host.append(form);
    const input=document.createElement("textarea");input.rows=2;input.maxLength=320;
    input.dir="ltr";input.lang="el";input.autocomplete="off";
    input.placeholder="Γράψε στα ελληνικά…";
    input.setAttribute("aria-label",t("answer"));form.append(input);
    const submit=document.createElement("button");submit.type="submit";
    submit.className="primary track-button";submit.textContent=t("check");
    form.append(submit);
    const feedback=document.createElement("div");feedback.className="life-feedback";form.append(feedback);
    form.addEventListener("submit",async event=>{
      event.preventDefault();if(busy||!input.value.trim())return;
      busy=true;submit.disabled=true;notice("");
      try{
        const result=await api("scene",{revision:current.revision,id:current.id,answer:input.value});
        current.revision=result.revision;
        feedback.replaceChildren();
        feedback.append(text("p",t(result.correct?"right":result.unverified?"unverified":"wrong"),
          result.correct?"track-success":result.unverified?"track-meta":"track-error"));
        if(result.explanation){
          feedback.append(text("strong",t("why"),"life-feedback-heading"));
          feedback.append(text("p",result.explanation,"track-error"));
        }
        feedback.append(text("strong",t("correct"),"life-feedback-heading"));
        feedback.append(text("p",result.answer,"track-greek-summary"));
        if(result.alternatives?.length)
          feedback.append(text("p",result.alternatives.join(" / "),"track-small"));
        feedback.append(text("p",t("meaning")+": "+result.translation+
          (result.translationLang!==lang()?" (EN)":""),"track-meta"));
        if(result.correct){
          input.disabled=true;submit.hidden=true;
          feedback.append(button(t("back"),renderMenu,"primary"));
        }else{
          feedback.append(text("p",t("retry"),"track-small"));
          submit.disabled=false;
        }
      }catch(e){
        notice(e.message,true);
        if(e.message==="stale_track"){await loadScene(current.id);}
      }finally{busy=false;if(!input.disabled)submit.disabled=false;}
    });
    input.focus();
  }
  async function open(){
    if($("life-view").hidden||busy)return;
    shownLang=lang();busy=true;notice("");
    try{
      overview=await api("life");
      const select=$("life-max-chapter");select.replaceChildren();
      for(let n=1;n<=overview.printedChapterCount;n++){
        const option=document.createElement("option");option.value=String(n);
        option.textContent=(lang()==="ru"?"Главы 1–":"Chapters 1–")+n;
        select.append(option);
      }
      status();renderMenu();
    }catch(e){notice(e.message,true);}
    finally{busy=false;}
  }
  async function changeScope(value){
    if(busy||!overview)return;
    busy=true;notice("");
    try{
      overview=await api("life",{revision:overview.revision,maxChapter:Number(value)});
      status();renderMenu();
    }catch(e){notice(e.message,true);if(e.message==="stale_track"){busy=false;await open();}}
    finally{busy=false;}
  }
  $("life-max-chapter").addEventListener("change",e=>changeScope(e.target.value));
  $("life-roleplay-mode").addEventListener("click",()=>{if(overview)renderMenu();});
  window.lexiLife={onOpen:open,showSimulation};
})();
