"use strict";
(() => {
  const $=id=>document.getElementById(id);
  const i18n={
    ru:{title:"Путешествие по Греции",sub:"Каждый ход — немного языка. Слова, глаголы, грамматика, слух и жизненные ситуации.",
      scope:"Изучено до главы",round:"Глава",path:"Твой путь",continue:"Следующий ход",
      go:"Играть",complete:"Ход пройден!",bad:"Есть ошибка — попробуй ещё раз",
      noFail:"Вариант пока не подтверждён — без штрафа.",
      again:"Попробовать снова",next:"Следующий ход",back:"Вернуться на поле",
      jump:"Я уже знаю первые главы — начать с выбранной",jumpExplain:"Предыдущие клетки будут пропущены, но не отмечены как изученные.",
      quest:"Задание",you:"Твой ответ",listen:"▶ Слушать",slow:"0,8× Медленно",wait:"Загружаю приключение…",
      error:"Не удалось продолжить: ",done:"Этот участок пути пройден!",more:"Можешь выбрать следующую главу.",
      correct:"Верный вариант",reason:"Разбор",meaning:"Перевод",
      board:"Игровое поле",legacy:"Классическая версия · Deprecated",
      note:"Классический режим остаётся доступен со всеми прежними настройками. Новые задания развиваются на игровом поле.",
      cap:"Доступно до главы",skip:"Пропустить без штрафа",
      book:"Учебник",lexicon:"Словарь A1",verb:"Глаголы",grammar:"Грамматика",
      listening:"Аудирование",dialogue:"Диалоги",clock:"Часы",life:"Ситуация",
      audioErr:"Не удалось воспроизвести аудио.",audioMissing:"Запись для задания недоступна."
    },
    en:{title:"Your Greek adventure",sub:"Every step builds a skill: vocabulary, verbs, grammar, listening and daily life.",
      scope:"Studied through chapter",round:"Chapter",path:"Your path",continue:"Next move",
      go:"Play",complete:"Quest completed!",bad:"Not quite — try again",noFail:"Unverified wording, no penalty.",
      again:"Try again",next:"Next move",back:"Back to map",
      jump:"I know the early chapters — start at the selected one",jumpExplain:"Earlier tiles are skipped, not marked as mastered.",
      quest:"Quest",you:"Your answer",listen:"▶ Listen",slow:"0.8× Slower",wait:"Preparing your adventure…",
      error:"Could not continue: ",done:"You've finished this stretch!",more:"Choose another chapter to continue.",
      correct:"Correct answer",reason:"Explanation",meaning:"Meaning",
      board:"Game board",legacy:"Classic version · Deprecated",note:"Classic training keeps every existing setting. Future features belong on the board.",
      cap:"Up to chapter",skip:"Skip without penalty",
      book:"Textbook",lexicon:"A1 words",verb:"Verbs",grammar:"Grammar",
      listening:"Listening",dialogue:"Dialogues",clock:"Clock",life:"Real life",audioErr:"Playback failed.",audioMissing:"No available recording."
    }
  };
  const lang=()=>$("lang")?.value||"ru";
  const tr=k=>(i18n[lang()]||i18n.en)[k]||i18n.en[k]||k;
  const el=(tag,text,cls)=>{
    const x=document.createElement(tag);if(text!==undefined)x.textContent=String(text);
    if(cls)x.className=cls;return x;
  };
  const button=(name,click,cls="primary board-button")=>{
    const x=el("button",name,cls);x.type="button";x.addEventListener("click",click);return x;
  };
  let data=null,working=false,clip=null,displayingAnswer=false;
  async function api(body){
    const url="/greek/api/board"+(body?"":"?lang="+encodeURIComponent(lang()));
    const res=await fetch(url,{credentials:"same-origin",cache:"no-store",
      ...(body?{method:"POST",headers:{"Content-Type":"application/json"},
         body:JSON.stringify({...body,lang:lang()})}:{})});
    const result=await res.json().catch(()=>({}));
    if(!res.ok)throw Error(result.error||"HTTP "+res.status);
    return result;
  }
  const status=(value,isError=false)=>{
    const node=$("board-message");node.hidden=!value;
    node.textContent=value||"";node.classList.toggle("board-error",isError);
  };
  function stopAudio(){
    if(clip){try{clip.pause();clip.removeAttribute("src");clip.load();}catch{}clip=null;}
    window.LexiWordAudio?.stop();
  }
  function playAudio(q,slow){
    const source=q?.audioUrl;
    if(typeof source!=="string"||!/^\/greek\/audio\/[a-f0-9]{32}\.wav$/.test(source)){
      status(tr("audioMissing"),true);return;
    }
    stopAudio();clip=new Audio(source);clip.playbackRate=slow?.8:1;
    clip.play().catch(()=>status(tr("audioErr"),true));
  }
  function sound(root,q){
    if(q?.audioUrl){
      const area=el("div",undefined,"board-audio-row");
      area.append(button(tr("listen"),()=>playAudio(q,false),"secondary board-audio"),
        button(tr("slow"),()=>playAudio(q,true),"secondary board-audio"));
      root.append(area);
    }else if(q?.wordAudio&&window.LexiWordAudio?.available(q.wordAudio)){
      const area=el("div",undefined,"board-audio-row");
      for(const slow of [false,true])
        area.append(button(tr(slow?"slow":"listen"),()=>
          window.LexiWordAudio.play(q.wordAudio,{slow,onStatus:()=>{}}),"secondary board-audio"));
      root.append(area);
    }
  }
  function road(nodes,chapter){
    const wrap=el("div",undefined,"board-road");
    const ns="http://www.w3.org/2000/svg";
    const svg=document.createElementNS(ns,"svg");svg.setAttribute("viewBox","0 0 700 340");
    svg.classList.add("board-road-lines");svg.setAttribute("aria-hidden","true");
    const defs=document.createElementNS(ns,"defs");
    const path=document.createElementNS(ns,"path");
    path.setAttribute("d","M85 265Q125 225 210 221T336 265Q420 270 490 221T581 150Q550 93 455 105T294 61Q190 48 140 95");
    path.setAttribute("stroke","#e6c591");path.setAttribute("stroke-width","9");
    path.setAttribute("stroke-dasharray","18 10");path.setAttribute("stroke-linecap","round");
    path.setAttribute("fill","none");svg.append(path);
    wrap.append(svg);
    const coords=[[12,79],[30,65],[48,79],[70,65],[83,44],[65,32],[42,18],[20,28]];
    for(let i=0;i<8;i++){
      const item=nodes[i];
      const node=button(i+1,()=>{if(item.state==="current")launch();},
        "board-node "+item.state);
      node.style.left=coords[i][0]+"%";node.style.top=coords[i][1]+"%";
      node.disabled=item.state!=="current";
      node.setAttribute("aria-label",item.name+" · "+(i+1)+" · "+item.state);
      const ico=["📖","🧠","✍️","🧩","🎧","💬","🕘","🏛️"][i];
      node.replaceChildren(el("span",ico,"board-node-icon"),el("small",String(i+1),"board-node-step"));
      if(item.state==="current"){
        const here=el("span",lang()==="ru"?"Твой ход":"Your turn","board-your-turn");
        node.append(here);
      }
      wrap.append(node);
    }
    return wrap;
  }
  function showMap(){
    stopAudio();displayingAnswer=false;
    $("board-play").hidden=true;$("board-map").hidden=false;
    const place=$("board-map");place.replaceChildren();
    const active=Math.min(data.position,Math.max(0,data.total-1));
    const shownChapter=Math.floor(active/8)+1;
    const currentNodes=data.nodes.filter(x=>x.chapter===shownChapter);
    const hero=el("div",undefined,"board-header");
    const info=el("div",undefined,"board-heading");
    info.append(el("span","ΛΕΞΗ · "+tr("board"),"board-kicker"),
      el("h2",tr("title"),"board-title"),
      el("p",tr("sub"),"board-subtitle"));
    const selection=el("label",tr("scope"),"board-scope");
    const select=el("select",undefined,"board-chapter-select");
    for(let i=1;i<=20;i++){const o=el("option",(lang()==="ru"?"Глава ":"Chapter ")+i);o.value=String(i);select.append(o);}
    select.value=String(data.chapterLimit);
    select.addEventListener("change",()=>act({action:"scope",revision:data.revision,chapterLimit:Number(select.value)},false));
    selection.append(select);hero.append(info,selection);place.append(hero);
    const progress=el("div",undefined,"board-stats");
    progress.append(el("span","✨ "+data.wins+" "+(lang()==="ru"?"успешных ходов":"wins")),
        el("span","🎲 "+data.completed+" / "+data.total),
        el("span","📍 "+tr("round")+" "+shownChapter));
    place.append(progress);
    const card=el("section",undefined,"board-map-card");
    card.append(el("div",tr("path")+" · "+tr("round")+" "+shownChapter,"board-map-label"));
    if(data.finished){
      card.append(el("h3",tr("done"),"board-over"),el("p",tr("more"),"board-subtitle"));
    }else{
      card.append(road(currentNodes,shownChapter));
      card.append(button(tr("continue"),launch,"primary board-main-start"));
    }
    place.append(card);
    if(!data.hasStarted&&data.chapterLimit>1&&data.position===0){
      const choice=el("div",undefined,"board-jump");
      choice.append(button(tr("jump"),()=>act({
         action:"jump",revision:data.revision,chapter:data.chapterLimit},false),
         "secondary board-jump-button"));
      choice.append(el("p",tr("jumpExplain"),"board-muted"));
      place.append(choice);
    }
    const note=el("p",tr("note"),"board-muted");place.append(note);
  }
  function extraQuestionVisual(card,q){
    if(q.kind==="dialogue"&&Array.isArray(q.dialogueLines)){
      const box=el("div",undefined,"board-dialogue");
      box.append(el("span",lang()==="ru"?"Выбери подходящую реплику для первого пропуска":"Choose a response for the first gap","board-muted"));
      for(const line of q.dialogueLines){
        box.append(el("p",String(line).replace(/\[\[\d+\]\]/g,"________"),"board-dialogue-line"));
      }
      card.append(box);
    }
    if(q.kind==="clock"&&Number.isFinite(q.clockHour)&&Number.isFinite(q.clockMinute)){
      const ns="http://www.w3.org/2000/svg";
      const svg=document.createElementNS(ns,"svg");
      svg.setAttribute("viewBox","0 0 220 220");svg.classList.add("board-clock");
      svg.setAttribute("role","img");svg.setAttribute("aria-label","Analog clock");
      const add=(tag,attrs)=>{
        const node=document.createElementNS(ns,tag);
        for(const [key,value] of Object.entries(attrs))node.setAttribute(key,String(value));
        svg.append(node);return node;
      };
      add("circle",{cx:110,cy:110,r:102,fill:"#15354c",stroke:"#e4c88c","stroke-width":4});
      for(let n=1;n<=12;n++){
        const angle=n*Math.PI/6;
        const txt=add("text",{x:110+80*Math.sin(angle),y:116-80*Math.cos(angle),
          "text-anchor":"middle","font-size":15,fill:"#f8efde"});
        txt.textContent=String(n);
      }
      const angleH=((q.clockHour%12)+q.clockMinute/60)*Math.PI/6;
      const angleM=q.clockMinute*Math.PI/30;
      add("line",{x1:110,y1:110,x2:110+49*Math.sin(angleH),y2:110-49*Math.cos(angleH),
        stroke:"#efd091","stroke-width":8,"stroke-linecap":"round"});
      add("line",{x1:110,y1:110,x2:110+75*Math.sin(angleM),y2:110-75*Math.cos(angleM),
        stroke:"#f5f6ec","stroke-width":5,"stroke-linecap":"round"});
      add("circle",{cx:110,cy:110,r:5,fill:"#f5ecdb"});
      card.append(svg);
    }
  }

  function launch(){
    if(working||!data?.quest||data.finished)return;
    displayingAnswer=false;stopAudio();
    $("board-map").hidden=true;$("board-play").hidden=false;
    const root=$("board-play");root.replaceChildren();
    const quest=data.quest,q=quest.question;
    const back=button("← "+tr("back"),()=>showMap(),"secondary board-back");
    root.append(back);
    const card=el("article",undefined,"board-question-card");
    const header=el("div",undefined,"board-question-header");
    header.append(el("span",tr("quest")+" "+(data.position+1),"board-kicker"),
      el("span",(lang()==="ru"?"Глава ":"Chapter ")+quest.chapter,"board-tile"));
    card.append(header);
    const names=quest.kind==="life"?tr("you"):tr(quest.title);
    card.append(el("h2",names,"board-quest-type"));
    const prompt=el("p",q.prompt,"board-quest-prompt");
    prompt.lang=(q.kind==="life"?(q.promptLang||lang()):(q.direction==="ru-gr"?lang():"el"));
    card.append(prompt);
    extraQuestionVisual(card,q);
    if(q.note&&q.kind!=="life")card.append(el("p",q.note,"board-subtitle"));
    sound(card,q);
    const response=el("div",undefined,"board-answer-choices");
    const feedback=el("div",undefined,"board-response");
    let selectedInput=null;
    if(quest.type==="life"){
      selectedInput=el("textarea",undefined,"board-life-input");
      selectedInput.lang="el";selectedInput.rows=3;selectedInput.placeholder="Γράψε στα ελληνικά…";
      response.append(selectedInput);
      response.append(button(tr("check"),()=>send(selectedInput.value,card,response,feedback),"primary board-submit"));
    }else{
      const choices=q.choices||[];
      choices.forEach((choice,i)=>{
        const b=button((i+1)+". "+choice,()=>send(choice,card,response,feedback),
          "board-choice");
        response.append(b);
      });
    }
    card.append(response,feedback);root.append(card);
    if(selectedInput)selectedInput.focus();
  }
  async function send(selected,card,options,feedback){
    if(working||displayingAnswer||!selected?.trim())return;
    working=true;status("");
    try{
      const next=await api({action:"answer",revision:data.revision,
        questId:data.quest.question.id,selected});
      const result=next.feedback;
      data=next;feedback.replaceChildren();
      if(result.correct){
        displayingAnswer=true;
        feedback.append(el("strong",tr("complete"),"board-success"));
      }else{
        feedback.append(el("strong",tr(result.unverified?"noFail":"bad"),
          result.unverified?"board-warn":"board-error-text"));
      }
      if(result.explanation)feedback.append(el("p",result.explanation,"board-feedback-explanation"));
      if(result.answer){
        feedback.append(el("span",tr("correct"),"board-feedback-caption"));
        feedback.append(el("p",result.answer,"board-feedback-correct"));
      }
      if(result.clozeTranslation||result.translation)
        feedback.append(el("p",tr("meaning")+": "+(result.clozeTranslation||result.translation),"board-muted"));
      if(result.correct){
        options.replaceChildren();
        feedback.append(button(tr("next"),()=>open(),"primary board-next"));
      }else if(result.unverified){
        feedback.append(button(tr("skip"),()=>act({action:"skip",revision:data.revision,
          questId:data.quest.question.id},true),"secondary board-skip"));
      }
    }catch(err){status(tr("error")+err.message,true);}
    finally{working=false;}
  }
  async function act(body,goNext){
    if(working)return;working=true;
    try{
      const next=await api(body);
      data=next;status("");
    }catch(e){status(tr("error")+e.message,true);}
    finally{working=false;}
    await open();
    if(goNext&&!data.finished)launch();
  }
  async function open(){
    if($("board-view").hidden||working)return;
    const boardTab=document.querySelector('.tab[data-page="board"]');
    if(boardTab)boardTab.textContent=lang()==="ru"?"🎲 Путь обучения":"🎲 "+tr("board");
    const oldTab=$("legacy-practice-tab");
    if(oldTab)oldTab.textContent=tr("legacy");
    const oldNote=document.querySelector(".legacy-notice p");
    if(oldNote&&lang()!=="ru"){
      // Keep the link node intact: changing the whole paragraph would
      // discard the working event listener attached by Classic.
      if(oldNote.firstChild)oldNote.firstChild.textContent=tr("note")+" ";
    }
    working=true;status(tr("wait"));stopAudio();
    try{data=await api();status("");showMap();}
    catch(e){status(tr("error")+e.message,true);}
    finally{working=false;}
  }
  window.lexiBoard={onOpen:open};
})();
