"use strict";
// Culture is one Lexi section. Questions, grading, progress and quiz UI stay
// in existing app.js/server.py. No separate learning backend or exam engine.
(() => {
  const $ = id => document.getElementById(id);
  const ui = {
    ru: {
      title:"Культура Кипра", intro:"14 тем о государстве, истории, географии и жизни Кипра. Вопросы на греческом, объяснения на русском.",
      unofficial:"Независимый учебный тренажёр — не официальный государственный экзамен.",
      available:"Опубликовано вопросов",mastered:"Освоено фактов",weak:"Мои ошибки",
      language:"Язык перевода",duration:"Тренировка",srs:"Интервальное повторение (SRS)",
      topics:"Темы экзамена",start:"Начать тренировку",review:"Повторить ошибки",
      exam:"Пробный экзамен · скоро",
      examInfo:"Экзамен 25 вопросов / 45 минут станет доступен после реализации защищённой экзаменационной сессии и редакторской проверки банка.",
      empty:"Пока нет вопросов, прошедших независимую редакторскую проверку. Черновики не выдаются пользователям как проверенный материал.",
      noWeak:"Ошибок для повторения пока нет.",loading:"Загружаю темы и прогресс…",
      failed:"Не удалось загрузить Culture: ",noSelection:"Выбери хотя бы одну доступную тему.",
      started:"Открываю тренировку…",disabled:"Нет доступных вопросов для этой выборки.",
      langNotice:"Для Culture переводы пока доступны только на русском и английском.",
      topicCount:n=>n+" вопросов",allTopics:"Все доступные темы"
    },
    en: {
      title:"Cyprus Culture", intro:"14 topics on Cypriot government, history, geography and daily life. Greek questions with English explanations.",
      unofficial:"Independent study tool — not an official government examination.",
      available:"Published questions",mastered:"Facts mastered",weak:"Mistakes",
      language:"Translation language",duration:"Study session",srs:"Spaced repetition (SRS)",
      topics:"Exam topics",start:"Start practice",review:"Review mistakes",
      exam:"Mock exam · coming soon",
      examInfo:"The 25-question, 45-minute mock exam will be enabled after the secure exam session and independent editorial review are complete.",
      empty:"No questions have passed independent editorial review yet. Draft questions are not shown as verified material.",
      noWeak:"No mistakes to review yet.",loading:"Loading topics and progress…",
      failed:"Could not load Culture: ",noSelection:"Select at least one available topic.",
      started:"Starting practice…",disabled:"No questions available for this selection.",
      langNotice:"Culture translations are currently available only in Russian and English.",
      topicCount:n=>n+" questions",allTopics:"All available topics"
    }
  };
  let meta=null,stats=null,loaded=false,working=false;
  const locale=()=>($("lang").value==="ru"?"ru":"en");
  const t=key=>ui[locale()][key];
  const err=message=>{$("culture-status").textContent=message;};
  const topicName=(topic,lang)=>topic?.[lang==="ru"?"ru":"en"]||topic?.en||topic?.code||"";
  function save(){
    try{localStorage.setItem("lexi-culture-settings",JSON.stringify({
      lang:$("culture-lang").value,duration:$("culture-duration").value,srs:$("culture-srs").checked,
      topics:[...$("culture-topics").querySelectorAll("input:checked")].map(x=>x.value)
    }));}catch{}
  }
  function previous(){
    try{return JSON.parse(localStorage.getItem("lexi-culture-settings")||"null")||{};}catch{return {};}
  }
  function render(){
    const data=ui[locale()];
    for(const [id,key] of [
      ["culture-title","title"],["culture-intro","intro"],["culture-unofficial","unofficial"],
      ["culture-available-label","available"],["culture-mastered-label","mastered"],
      ["culture-weak-label","weak"],["culture-lang-label","language"],
      ["culture-duration-label","duration"],["culture-srs-label","srs"],
      ["culture-topics-title","topics"],["culture-start","start"],
      ["culture-review","review"],["culture-exam","exam"],["culture-exam-status","examInfo"]
    ]){const target=$(id);if(id==="culture-lang-label"||id==="culture-duration-label"){
      // Keep the native <select> child when changing the translated label.
      target.firstChild.textContent=data[key]+" ";
    }else target.textContent=data[key];}
    $("culture-available").textContent=String(meta?.available||0);
    $("culture-mastered").textContent=String(stats?.masteredFacts||0);
    $("culture-weak-count").textContent=String(stats?.weak||0);
    const host=$("culture-topics");
    const previously=[...host.querySelectorAll("input:checked")].map(x=>x.value);
    const selected=host.children.length?previously:previous().topics;
    host.replaceChildren();
    for(const topic of meta?.topics||[]){
      const row=document.createElement("label");row.className="culture-topic";
      const checkbox=document.createElement("input");
      checkbox.type="checkbox";checkbox.value=topic.code;checkbox.disabled=!topic.count;
      checkbox.checked=topic.count>0&&(!Array.isArray(selected)||selected.includes(topic.code));
      checkbox.addEventListener("change",save);
      const name=document.createElement("span");name.textContent=topicName(topic,locale());
      const count=document.createElement("small");count.textContent=String(topic.count||0);
      row.append(checkbox,name,count);host.append(row);
    }
    const hasItems=(meta?.available||0)>0;
    $("culture-start").disabled=working||!hasItems;
    $("culture-review").disabled=working||!hasItems||!(stats?.weak>0);
    $("culture-exam").disabled=true; // #39 requires a trusted server-side session.
    if(loaded&&!hasItems)err(t("empty"));
    else if(loaded&&!stats?.weak&&hasItems)err(t("noWeak"));
    if(!["ru","en"].includes($("lang").value)&&loaded&&hasItems){
      err(t("langNotice"));
    }
  }
  async function open(){
    err(t("loading"));
    try{
      const bridge=window.lexiCultureBridge;
      if(!bridge?.loggedIn()){err(t("loading"));return;}
      // Reuse existing app endpoints; no new Culture API or account.
      const [catalog,summary]=await Promise.all([
        bridge.api("catalog?scope=culture"),bridge.api("stats?scope=culture")
      ]);
      meta=catalog;stats=summary;loaded=true;
      render();
    }catch(error){err(t("failed")+String(error.message||error));}
  }
  async function practice(mode){
    if(working||!meta?.available)return;
    const selected=[...$("culture-topics").querySelectorAll("input:checked")].map(x=>x.value);
    if(!selected.length){err(t("noSelection"));return;}
    working=true;render();err(t("started"));
    try{
      const ok=await window.lexiCultureBridge.start({
        scope:"culture",mode,topics:selected.join(","),lang:$("culture-lang").value,
        duration:Number($("culture-duration").value),count:25,
        srsOptIn:$("culture-srs").checked
      });
      if(!ok)err(t("disabled"));
    }catch(error){err(t("failed")+String(error.message||error));}
    finally{working=false;render();}
  }
  function onLanguageChange(){
    if(!$("culture-view").hidden)render();
  }
  function onSessionFinished(){
    // The next open reads the authoritative SQLite stats instead of
    // independently updating local counters on the client.
    loaded=false;
  }
  const preference=previous();
  if(["ru","en"].includes(preference.lang))$("culture-lang").value=preference.lang;
  else $("culture-lang").value=$("lang").value==="ru"?"ru":"en";
  if(["10","20","30","45"].includes(String(preference.duration)))$("culture-duration").value=String(preference.duration);
  $("culture-srs").checked=preference.srs===true;
  for(const id of ["culture-lang","culture-duration","culture-srs"])
    $(id).addEventListener("change",save);
  $("culture-start").addEventListener("click",()=>practice("all"));
  $("culture-review").addEventListener("click",()=>practice("weak"));
  window.lexiCulture={onOpen:open,onLanguageChange,onSessionFinished,
    topicLabel:(code,lang)=>topicName(meta?.topics?.find(x=>x.code===code),lang||$("culture-lang").value)};
})();
