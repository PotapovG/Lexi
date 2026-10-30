"use strict";
(() => {
  // New course experience: eight real lessons per round, no board/map artwork.
  // Server owns ordering, correctness, timing and weakness backlog.
  const $=id=>document.getElementById(id);
  const dict={
    ru:{title:"Твой путь в греческом",sub:"Восемь уроков на круг. Следующий откроется после предыдущего.",
      chapter:"Изучено до главы",round:"Круг",lesson:"Урок",locked:"Неизвестный урок",
      complete:"Пройден",now:"Текущий урок",start:"Начать урок",resume:"Продолжить урок",
      next:"Дальше",finishLesson:"Завершить урок",yourAnswer:"Твой ответ",toLessons:"К списку уроков",done:"Урок завершён!",
      summary:"Итоги круга",continueRound:"Начать следующий круг",allDone:"Доступные главы пройдены",
      question:"Задание",listen:"▶ Слушать",slow:"0,8× Медленнее",check:"Ответить",
      correct:"Верно!",wrong:"Есть ошибка. Попробуй исправить.",uncertain:"Вариант не подтверждён — без штрафа.",
      correction:"Правильный вариант",explanation:"Разбор ошибки",translation:"Перевод",
      skip:"Пропустить без штрафа",time:"Активное время",elapsed:"С начала круга",
      attempts:"Ответы",errors:"Ошибки",accuracy:"Точность",completed:"Пройдено",
      backlog:"Что стоит повторить",noBacklog:"Ошибок для повторения пока нет.",
      backlogNote:"Ошибочные задания появятся в следующих уроках для закрепления.",
      minutes:"мин",estimate:"Обычно 5–10 минут",paused:"Занятие сохранено",
      jump:"Начать с выбранной главы",jumpNote:"Пропущенные главы не считаются освоенными.",
      wait:"Открываю урок…",fail:"Ошибка: ",board:"Уроки",legacy:"Классика · Deprecated",
      audioUnavailable:"Нет готовой записи",finish:"Готово",stats:"Статистика круга",
      questionOf:"из",roundReport:"Круг завершён. Вот что получилось.",
      all:"Всего",never:"Ещё закрыто"},
    en:{title:"Your Greek lessons",sub:"Eight lessons in each round. The next stays hidden until you finish the current one.",
      chapter:"Studied through chapter",round:"Round",lesson:"Lesson",locked:"Unknown lesson",
      complete:"Complete",now:"Current lesson",start:"Start lesson",resume:"Continue lesson",
      next:"Next",finishLesson:"Finish lesson",yourAnswer:"Your answer",toLessons:"Back to lessons",done:"Lesson completed!",
      summary:"Round results",continueRound:"Start next round",allDone:"All available chapters complete",
      question:"Question",listen:"▶ Listen",slow:"0.8× Slower",check:"Submit",
      correct:"Correct!",wrong:"Not quite. Try again.",uncertain:"Unverified alternative — no penalty.",
      correction:"Correct answer",explanation:"Explanation",translation:"Meaning",
      skip:"Skip without penalty",time:"Active time",elapsed:"Elapsed since round start",
      attempts:"Answers",errors:"Mistakes",accuracy:"Accuracy",completed:"Completed",
      backlog:"Learning backlog",noBacklog:"No items need review yet.",
      backlogNote:"Missed questions return in future lessons.",
      minutes:"min",estimate:"Usually 5–10 minutes",paused:"Lesson saved",
      jump:"Start at selected chapter",jumpNote:"Skipped chapters are not marked mastered.",
      wait:"Loading lesson…",fail:"Error: ",board:"Lessons",legacy:"Classic · Deprecated",
      audioUnavailable:"No available recording",finish:"Finished",stats:"Round statistics",
      questionOf:"of",roundReport:"Round finished. Here's your result.",
      all:"Total",never:"Not available yet"}
  };
  const lang=()=>$("lang")?.value||"ru";
  const t=key=>(dict[lang()]||dict.en)[key]||dict.en[key]||key;
  const node=(tag,text,css)=>{
    const el=document.createElement(tag);if(text!==undefined)el.textContent=String(text);
    if(css)el.className=css;return el;
  };
  const button=(text,fn,css="primary lesson-primary")=>{
    const b=node("button",text,css);b.type="button";b.addEventListener("click",fn);return b;
  };
  const fmt=s=>{
    const secs=Math.max(0,Math.floor(s||0));
    return Math.floor(secs/60)+" "+t("minutes")+(secs%60? " "+String(secs%60).padStart(2,"0")+" с":"");
  };
  const labels={book:"📖",lexicon:"🧠",verb:"✍️",grammar:"🧩",
    listening:"🎧",dialogue:"💬",clock:"🕘",life:"🏛️"};
  let data=null,working=false,clip=null,feedbackVisible=false;
  async function request(body){
    const path="/greek/api/board"+(body?"":"?lang="+encodeURIComponent(lang()));
    const res=await fetch(path,{credentials:"same-origin",cache:"no-store",
      ...(body?{method:"POST",headers:{"Content-Type":"application/json"},
         body:JSON.stringify({...body,lang:lang()})}:{})});
    const obj=await res.json().catch(()=>({}));
    if(!res.ok)throw Error(obj.error||"HTTP "+res.status);
    return obj;
  }
  function status(msg,bad=false){
    const e=$("board-message");e.hidden=!msg;e.textContent=msg||"";
    e.classList.toggle("board-error",bad);
  }
  function stopAudio(){
    if(clip){try{clip.pause();clip.removeAttribute("src");clip.load();}catch{}clip=null;}
    window.LexiWordAudio?.stop();
  }
  function sound(parent,q){
    if(!q?.audioUrl&&!window.LexiWordAudio?.available(q?.wordAudio))return;
    const wrap=node("div",undefined,"lesson-audio-row");
    for(const slow of [false,true]){
      wrap.append(button(t(slow?"slow":"listen"),async()=>{
        stopAudio();
        if(q.audioUrl){
          if(!/^\/greek\/audio\/[a-f0-9]{32}\.wav$/.test(q.audioUrl)){
            status(t("audioUnavailable"),true);return;
          }
          clip=new Audio(q.audioUrl);clip.playbackRate=slow?.8:1;
          try{await clip.play();}catch{status(t("audioUnavailable"),true);}
        }else if(q.wordAudio){
          await window.LexiWordAudio.play(q.wordAudio,{slow,onStatus:()=>{}});
        }
      },"secondary lesson-audio-btn"));
    }
    parent.append(wrap);
  }
  function clock(root,q){
    if(q.kind!=="clock")return;
    const ns="http://www.w3.org/2000/svg";
    const svg=document.createElementNS(ns,"svg");svg.setAttribute("viewBox","0 0 220 220");
    svg.setAttribute("role","img");svg.setAttribute("aria-label","Analog clock");
    svg.classList.add("lesson-clock");
    const add=(name,attrs)=>{
      const e=document.createElementNS(ns,name);
      for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));svg.append(e);return e;
    };
    add("circle",{cx:110,cy:110,r:102,fill:"#142c41",stroke:"#e8c68d","stroke-width":3});
    for(let n=1;n<=12;n++){
      const a=n*Math.PI/6;
      add("text",{x:110+80*Math.sin(a),y:116-80*Math.cos(a),fill:"#f3eada","font-size":15,"text-anchor":"middle"}).textContent=String(n);
    }
    const ah=((q.clockHour%12)+q.clockMinute/60)*Math.PI/6;
    const am=q.clockMinute*Math.PI/30;
    add("line",{x1:110,y1:110,x2:110+48*Math.sin(ah),y2:110-48*Math.cos(ah),
      stroke:"#edd39a","stroke-width":8,"stroke-linecap":"round"});
    add("line",{x1:110,y1:110,x2:110+74*Math.sin(am),y2:110-74*Math.cos(am),
      stroke:"#f3f6e9","stroke-width":5,"stroke-linecap":"round"});
    add("circle",{cx:110,cy:110,r:4,fill:"#f3f6e9"});root.append(svg);
  }
  function dialogue(root,q){
    if(q.kind!=="dialogue"||!q.dialogueLines)return;
    const el=node("div",undefined,"lesson-dialogue");
    for(const line of q.dialogueLines)
      el.append(node("p",String(line).replace(/\[\[\d+\]\]/g,"________"),"lesson-dialogue-line"));
    root.append(el);
  }
  function header(root){
    const h=node("div",undefined,"lesson-header");
    const intro=node("div",undefined,"lesson-intro");
    intro.append(node("span","ΛΕΞΗ · "+t("board"),"board-kicker"),
      node("h2",t("title"),"lesson-title"),node("p",t("sub"),"lesson-subtitle"));
    const control=node("label",t("chapter"),"lesson-scope");
    const select=node("select",undefined,"lesson-scope-select");
    for(let i=1;i<=20;i++){const e=node("option",(lang()==="ru"?"Глава ":"Chapter ")+i);e.value=String(i);select.append(e);}
    select.value=String(data.chapterLimit);
    select.addEventListener("change",()=>sendAction({action:"scope",revision:data.revision,chapterLimit:Number(select.value)},false));
    control.append(select);h.append(intro,control);root.append(h);
  }
  function review(parent){
    const stats=data.backlog;
    const box=node("section",undefined,"lesson-review");
    const head=node("div",undefined,"lesson-review-head");
    head.append(node("h3",t("backlog"),"lesson-card-title"),
      node("strong",String(stats.due),"lesson-review-count"));
    box.append(head,node("p",stats.due?t("backlogNote"):t("noBacklog"),"lesson-muted"));
    if(stats.due){
      const list=node("ul",undefined,"lesson-review-list");
      for(const task of stats.items.slice(0,6)){
        const item=node("li",undefined,"lesson-review-item");
        item.append(node("span",task.prompt||task.id),
          node("small","×"+task.errors+" · "+(lang()==="ru"?"Глава ":"Ch. ")+task.chapter));
        list.append(item);
      }
      box.append(list);
      const kinds=node("div",undefined,"lesson-review-tags");
      for(const [family,count] of Object.entries(stats.byFamily))
        kinds.append(node("span",family+" · "+count,"lesson-topic-tag"));
      box.append(kinds);
    }
    parent.append(box);
  }
  function statsBox(parent,summary=false){
    const r=data.roundStats;
    const box=node("section",undefined,"lesson-stats");
    if(summary)box.append(node("h3",t("summary")+" · "+t("round")+" "+r.chapter,"lesson-card-title"));
    const grid=node("div",undefined,"lesson-stats-grid");
    const items=[
      [t("time"),fmt(r.activeSeconds)],
      [t("attempts"),r.attempts],
      [t("errors"),r.errors],
      [t("accuracy"),r.accuracy===null?"—":r.accuracy+"%"]];
    for(const [label,value] of items){
      const cell=node("div",undefined,"lesson-stat");
      cell.append(node("strong",value),node("span",label));grid.append(cell);
    }
    box.append(grid);
    if(summary&&r.elapsedSeconds)
      box.append(node("p",t("elapsed")+": "+fmt(r.elapsedSeconds),"lesson-muted"));
    parent.append(box);
  }
  function renderList(){
    stopAudio();feedbackVisible=false;
    $("board-play").hidden=true;$("board-map").hidden=false;
    const main=$("board-map");main.replaceChildren();
    header(main);
    const round=data.roundStats;
    const list=node("section",undefined,"lesson-list");
    list.append(node("div",t("round")+" "+data.round+" · "+round.lessonsCompleted+"/8 "+t("completed"),"lesson-round-label"));
    const next=data.nodes.find(x=>x.state==="current");
    for(const item of data.nodes){
      const row=node("div",undefined,"lesson-list-item "+item.state);
      const number=node("div",String(item.number).padStart(2,"0"),"lesson-list-number");
      const body=node("div",undefined,"lesson-list-copy");
      const title=item.state==="locked"?t("locked"):
        item.state==="skipped"?"—":item.name;
      body.append(node("strong",title));
      const details=(item.state==="completed"?
        t("complete")+" · "+fmt(item.stats.activeSeconds)+" · "+item.stats.errors+" "+t("errors"):
        item.state==="current"?
          t("estimate"):(item.state==="skipped"?"Пропущено":"🔒 "+t("never")));
      body.append(node("small",details));
      row.append(number,body);
      if(item.state==="completed")row.append(node("span","✓","lesson-check"));
      if(item.state==="current")
        row.append(button(data.lesson?t("resume"):t("start"),
          ()=>startLesson(),"primary lesson-inline-start"));
      if(item.state==="locked")row.append(node("span","🔒","lesson-lock"));
      list.append(row);
    }
    main.append(list);
    if(round.finished&&(data.roundReady||data.finished)){
      const report=node("section",undefined,"lesson-report");
      report.append(node("h3",t("roundReport"),"lesson-card-title"));
      statsBox(report,true);
      if(data.roundReady)
        report.append(button(t("continueRound"),
          ()=>sendAction({action:"continue_round",revision:data.revision},false),"primary lesson-primary"));
      else report.append(node("p",t("allDone"),"lesson-muted"));
      main.prepend(report);
    }else statsBox(main);
    if(data.canJump&&data.chapterLimit>1){
      const jump=node("div",undefined,"lesson-jump");
      jump.append(button(t("jump"),()=>sendAction({
        action:"jump",revision:data.revision,chapter:data.chapterLimit},false),"secondary lesson-secondary"));
      jump.append(node("p",t("jumpNote"),"lesson-muted"));main.append(jump);
    }
    review(main);
  }
  async function startLesson(){
    if(working||data.finished||data.roundReady)return;
    if(data.lesson&&!data.lesson.paused){renderLesson();return;}
    await sendAction({action:"lesson_start",revision:data.revision},true);
  }
  function renderLesson(){
    if(!data.lesson){renderList();return;}
    stopAudio();feedbackVisible=false;
    $("board-map").hidden=true;$("board-play").hidden=false;
    const holder=$("board-play");holder.replaceChildren();
    const lesson=data.lesson,q=lesson.question;
    const bar=node("div",undefined,"lesson-play-top");
    bar.append(button("← "+t("toLessons"),()=>pauseLesson(),"secondary lesson-secondary"));
    bar.append(node("span",t("lesson")+" "+(lesson.index%8+1)+" / 8","lesson-play-counter"));
    holder.append(bar);
    const wrap=node("article",undefined,"lesson-question");
    wrap.append(node("div",lesson.name+" · "+t("round")+" "+lesson.chapter,"lesson-kicker"));
    const count=node("div",undefined,"lesson-progress-label");
    count.append(node("span",t("question")+" "+(lesson.at+1)+" "+t("questionOf")+" "+lesson.count),
      node("span",fmt(lesson.activeSeconds)));
    wrap.append(count);
    const track=node("div",undefined,"lesson-progress-track");
    const fill=node("div",undefined,"lesson-progress-fill");fill.style.width=(100*lesson.at/lesson.count)+"%";
    track.append(fill);wrap.append(track);
    if(q){
      const prompt=node("h3",q.prompt,"lesson-question-prompt");
      prompt.lang=q.type==="life"?(q.promptLang||lang()):q.direction==="ru-gr"?q.lang:"el";
      wrap.append(prompt);
      if(q.note&&q.kind!=="life")wrap.append(node("p",q.note,"lesson-muted"));
      dialogue(wrap,q);clock(wrap,q);sound(wrap,q);
      const choices=node("div",undefined,"lesson-choices");
      const feedback=node("div",undefined,"lesson-feedback");
      if(q.type==="life"){
        const input=node("textarea",undefined,"lesson-textarea");
        input.lang="el";input.rows=3;input.placeholder="Γράψε στα ελληνικά…";
        choices.append(input);
        choices.append(button(t("check"),()=>submitAnswer(input.value,choices,feedback),"primary lesson-primary"));
      }else{
        for(let i=0;i<q.choices.length;i++){
          const option=q.choices[i];
          choices.append(button((i+1)+". "+option,()=>submitAnswer(option,choices,feedback),"lesson-option"));
        }
      }
      wrap.append(choices,feedback);
    }
    holder.append(wrap);
  }
  function finishFeedback(parent,result,choices,selected){
    // A submitted response is final regardless of correctness. Remove every
    // option / text input immediately; only Next or Finish lesson remains.
    feedbackVisible=true;choices.replaceChildren();parent.replaceChildren();
    // Once the answer is revealed, the learner cannot change it or use
    // another control to resubmit. The only action is Next / Finish lesson.
    const play=$("board-play");
    for(const element of play.querySelectorAll(".lesson-play-top button, .lesson-audio-row"))
      element.hidden=true;
    parent.append(node("strong",result.correct?t("correct"):result.unverified?t("uncertain"):t("wrong"),
      result.correct?"lesson-correct":result.unverified?"lesson-uncertain":"lesson-incorrect"));
    if(!result.correct&&selected)
      parent.append(node("p",t("yourAnswer")+": "+selected,"lesson-muted"));
    if(result.explanation)parent.append(node("p",t("explanation")+": "+result.explanation,"lesson-explanation"));
    if(result.answer)parent.append(node("p",t("correction")+": "+result.answer,"lesson-correct-answer"));
    if(result.translation||result.clozeTranslation)
      parent.append(node("p",t("translation")+": "+(result.translation||result.clozeTranslation),"lesson-muted"));
    if(result.lessonComplete){
      const l=result.lessonComplete;
      parent.append(node("h3",t("done"),"lesson-card-title"));
      parent.append(node("p",t("time")+": "+fmt(l.activeSeconds)+" · "+t("attempts")+": "+l.attempts+
        " · "+t("errors")+": "+l.errors,"lesson-lesson-total"));
      parent.append(button(t("finishLesson"),renderList,"primary lesson-primary"));
    }else{
      parent.append(button(t("next"),renderLesson,"primary lesson-primary"));
    }
  }
  async function submitAnswer(selected,choices,feedback){
    if(working||feedbackVisible||!selected||!String(selected).trim())return;
    working=true;
    status("");
    const lesson=data.lesson,q=lesson.question;
    try{
      const response=await request({action:"answer",revision:data.revision,
        lessonIndex:lesson.index,questionId:q.id,selected});
      data=response;
      finishFeedback(feedback,response.feedback,choices,selected);
    }catch(e){
      status(t("fail")+e.message,true);
    }finally{working=false;}
  }
  async function pauseLesson(){
    if(working||!data.lesson)return renderList();
    await sendAction({action:"pause",revision:data.revision},false);
  }
  async function sendAction(body,showQuestion){
    if(working)return;
    working=true;status(t("wait"));
    try{
      data=await request(body);status("");
      if(showQuestion&&data.lesson)renderLesson();
      else renderList();
    }catch(e){
      status(t("fail")+e.message,true);
      if(e.message==="stale_track"){
        try{data=await request();renderList();}catch{}
      }
    }finally{working=false;}
  }
  async function open(){
    if($("board-view").hidden||working)return;
    const tab=document.querySelector('.tab[data-page="board"]');
    if(tab)tab.textContent=lang()==="ru"?"📚 Уроки":"📚 Lessons";
    const legacy=$("legacy-practice-tab");
    if(legacy)legacy.textContent=t("legacy");
    working=true;status(t("wait"));
    try{data=await request();status("");renderList();}
    catch(e){status(t("fail")+e.message,true);}
    finally{working=false;}
  }
  window.lexiBoard={onOpen:open,onLeave:()=>{stopAudio();}};
})();
