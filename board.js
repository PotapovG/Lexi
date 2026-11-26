"use strict";
(() => {
  const $=id=>document.getElementById(id);
  const ui=()=>window.LexiUI;
  const lang=()=>ui().lang();
  const t=(key,values)=>ui().t(key,values);
  const node=(tag,text,css)=>{const el=document.createElement(tag);if(text!==undefined)el.textContent=String(text);if(css)el.className=css;return el;};
  const button=(text,fn,css="primary lesson-primary")=>{const b=node("button",text,css);b.type="button";b.addEventListener("click",fn);return b;};
  const uuid=()=>window.crypto?.randomUUID?.()||"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,c=>{const r=Math.random()*16|0;return(c==="x"?r:(r&3|8)).toString(16);});
  const fmt=s=>{const n=Math.max(0,Math.floor(s||0));return Math.floor(n/60)+" "+t("minutes")+(n%60?" "+n%60+" "+t("seconds"):"");};
  const familyName=family=>t("family_"+family);
  let data=null,working=false,clip=null,feedbackVisible=false,view="list",pending=null,pauseAfterPending=false,currentQuestion=null,currentLesson=null,draft=null,currentSummary=null,ownerGeneration=0;
  const visible=()=>!$("board-view").hidden;
  function persistPending(){
    try{if(pending)sessionStorage.setItem("lexi-board-pending-v1",JSON.stringify({owner:window.LexiApp?.accountKey(),...pending}));else sessionStorage.removeItem("lexi-board-pending-v1");}catch{}
  }
  function restorePending(){
    try{const value=JSON.parse(sessionStorage.getItem("lexi-board-pending-v1")||"null");
      if(value?.owner===window.LexiApp?.accountKey()&&value?.body?.requestId)pending=value;
      else sessionStorage.removeItem("lexi-board-pending-v1");}catch{}
  }
  const draftKey=(lesson,q)=>[window.LexiApp?.accountKey(),lesson?.runId,lesson?.index,lesson?.at,q?.id,q?.direction].join(":");
  function captureDraft(){
    if(!currentQuestion||feedbackVisible||view!=="lesson")return;
    const form=$("board-play").querySelector(".lesson-answer-form");if(!form)return;
    const field=form.querySelector("#lesson-typed-answer"),radio=form.querySelector('input[type="radio"]:checked');
    draft={key:draftKey(currentLesson,currentQuestion),selected:field?field.value:radio?.value??null,order:Array.from(form.querySelectorAll(".lesson-order-built button")).map(b=>Number(b.dataset.token))};
  }
  async function request(body,keepalive=false,expectedOwner){
    const owner=expectedOwner||window.LexiApp?.accountKey();
    if(body&&(!window.LexiApp?.loggedIn()||!owner))throw Error("account_changed");
    const res=await fetch("/greek/api/board"+(body?"":"?lang="+encodeURIComponent(lang())),{
      credentials:"same-origin",cache:"no-store",keepalive,
      ...(body?{method:"POST",headers:{"Content-Type":"application/json","X-Lexi-Owner":owner},body:JSON.stringify({...body,lang:body.lang||lang()})}:{})});
    const obj=await res.json().catch(()=>({}));
    if(owner!==window.LexiApp?.accountKey())throw Error("account_changed");
    if(!res.ok){if(obj.error==="account_changed")window.LexiApp?.reconcileAccount?.();const err=Error(obj.error||"HTTP "+res.status);err.status=res.status;err.body=obj;throw err;}
    return obj;
  }
  function status(msg,bad=false,retry=null){
    const e=$("board-message");e.hidden=!msg;e.replaceChildren();
    if(msg)e.append(node("span",msg));
    e.classList.toggle("board-error",bad);
    if(retry)e.append(button(t("retry"),retry,"secondary"));
  }
  function errorStatus(error,retry){
    if(error.message==="account_changed")return;
    if(error.status===401||error.message==="login_required"){status(t("loginRequired"),true);window.LexiApp?.requireLogin();return;}
    status(t("network"),true,retry);
  }
  function stopAudio(){
    if(clip){try{clip.pause();clip.removeAttribute("src");clip.load();}catch{}clip=null;}
    window.LexiWordAudio?.stop();
  }
  function setView(next){
    view=next;$("board-map").hidden=next!=="list";$("board-play").hidden=next==="list";
    document.body.classList.toggle("lesson-active",visible()&&next!=="list");
  }
  function focusHeading(el){el.tabIndex=-1;queueMicrotask(()=>{if(visible())el.focus({preventScroll:true});});}
  function sound(parent,q){
    const available=Boolean(q?.audioUrl||window.LexiWordAudio?.available(q?.wordAudio));
    if(!available){if(q?.wordAudio||q?.kind==="listening")parent.append(node("p",t("audioUnavailable"),"lesson-muted"));return;}
    const wrap=node("div",undefined,"lesson-audio-row");
    for(const slow of [false,true])wrap.append(button(t(slow?"slow":"listen"),async()=>{
      stopAudio();
      if(q.audioUrl){
        if(!/^\/greek\/audio\/[a-f0-9]{32}\.wav$/.test(q.audioUrl)){status(t("audioUnavailable"),true);return;}
        clip=new Audio(q.audioUrl);clip.playbackRate=slow?.8:1;
        try{await clip.play();}catch{status(t("audioUnavailable"),true);}
      }else await window.LexiWordAudio.play(q.wordAudio,{slow,onStatus:()=>{}});
    },"secondary lesson-audio-btn"));
    parent.append(wrap);
  }
  function clock(root,q){
    if(q.kind!=="clock")return;
    const ns="http://www.w3.org/2000/svg",svg=document.createElementNS(ns,"svg");
    svg.setAttribute("viewBox","0 0 220 220");svg.setAttribute("role","img");svg.setAttribute("aria-label",t("clock"));svg.classList.add("lesson-clock");
    const add=(name,attrs)=>{const e=document.createElementNS(ns,name);for(const [k,v]of Object.entries(attrs))e.setAttribute(k,String(v));svg.append(e);return e;};
    add("circle",{cx:110,cy:110,r:102,fill:"var(--panel)",stroke:"var(--text)","stroke-width":2});
    for(let n=1;n<=12;n++){const a=n*Math.PI/6;add("text",{x:110+80*Math.sin(a),y:116-80*Math.cos(a),fill:"var(--text)","font-size":15,"text-anchor":"middle"}).textContent=n;}
    const ah=((q.clockHour%12)+q.clockMinute/60)*Math.PI/6,am=q.clockMinute*Math.PI/30;
    add("line",{x1:110,y1:110,x2:110+48*Math.sin(ah),y2:110-48*Math.cos(ah),stroke:"var(--lx-action)","stroke-width":8,"stroke-linecap":"round"});
    add("line",{x1:110,y1:110,x2:110+74*Math.sin(am),y2:110-74*Math.cos(am),stroke:"var(--text)","stroke-width":5,"stroke-linecap":"round"});
    add("circle",{cx:110,cy:110,r:4,fill:"var(--text)"});root.append(svg);
  }
  function dialogue(root,q){
    if(q.kind!=="dialogue"||!q.dialogueLines)return;
    const panel=node("div",undefined,"lesson-dialogue");panel.lang="el";panel.dir="ltr";
    const gap=Number.isInteger(q.activeGap)?q.activeGap:Number((q.direction||"gap0").slice(3))||0;
    const count=q.gapCount||q.gapIndices?.length||q.dialogueLines.join(" ").match(/\[\[\d+\]\]/g)?.length||1;
    const label=node("p",t("gap",{at:gap+1,count}),"lesson-gap-label");label.id="lesson-gap-label";root.append(label);
    for(const value of q.dialogueLines){
      const line=node("p",undefined,"lesson-dialogue-line");const parts=String(value).split(/(\[\[\d+\]\])/);
      for(const part of parts){const match=part.match(/^\[\[(\d+)\]\]$/);if(!match){line.append(document.createTextNode(part));continue;}
        const index=Number(match[1]),filled=q.filledGaps?.[index],isActive=index===gap;
        const blank=node("span",filled||t(isActive?"activeGap":"futureGap"),"lesson-dialogue-gap "+(filled?"filled":isActive?"active":"future"));
        blank.dataset.gap=String(index);blank.lang=filled?"el":lang();blank.dir=filled?"ltr":"auto";
        if(isActive)blank.setAttribute("aria-current","step");line.append(blank);
      }panel.append(line);
    }root.append(panel);
  }
  function scopeControl(parent){
    const details=node("details",undefined,"lesson-scope-settings");details.append(node("summary",t("scopeSettings")));
    const label=node("label",t("scope"),"lesson-scope");const select=node("select");select.id="lesson-chapter-limit";
    for(let i=1;i<=20;i++){const option=node("option",t("chapter")+" "+i);option.value=i;select.append(option);}
    select.value=data.chapterLimit;select.disabled=working;
    select.addEventListener("change",()=>sendAction({action:"scope",revision:data.revision,chapterLimit:Number(select.value)},false));
    label.append(select);details.append(label,node("p",t("scopeNote"),"lesson-muted"));
    if(data.canJump&&data.chapterLimit>1){
      details.append(button(t("jump"),()=>sendAction({action:"jump",revision:data.revision,chapter:data.chapterLimit},false),"secondary"));
      details.append(node("p",t("jumpNote"),"lesson-muted"));
    }parent.append(details);
  }
  function review(parent){
    const stats=data.backlog||{due:0,items:[],byFamily:{}};
    const box=node("section",undefined,"lesson-review");const heading=node("div",undefined,"lesson-section-heading");
    heading.append(node("h3",t("backlog")),node("span",stats.due,"lesson-small"));box.append(heading,node("p",t(stats.due?"backlogNote":"noBacklog"),"lesson-muted"));
    if(stats.due){const list=node("ul",undefined,"lesson-review-list");for(const item of(stats.items||[]).slice(0,5)){
      const row=node("li");row.append(node("span",item.prompt||familyName(item.family)),node("small",t("chapter")+" "+item.chapter));list.append(row);}box.append(list);}
    parent.append(box);
  }
  function statsBox(parent,r,label){
    const box=node("section",undefined,"lesson-stats");if(label)box.append(node("h3",label));
    const grid=node("dl",undefined,"lesson-stats-grid");
    for(const [key,value]of[["activeTime",fmt(r.activeSeconds)],["attempts",r.attempts||0],["errors",r.errors||0],["accuracy",r.accuracy==null?"—":r.accuracy+"%"]]){
      const cell=node("div",undefined,"lesson-stat");cell.append(node("dt",t(key)),node("dd",value));grid.append(cell);}
    box.append(grid);parent.append(box);
  }
  function renderList(){
    if(!data)return;stopAudio();feedbackVisible=false;setView("list");
    const main=$("board-map");main.replaceChildren();
    const head=node("header",undefined,"lesson-header");const intro=node("div");
    intro.append(node("span",t("nextStep"),"board-kicker"),node("h1",t("continueTitle"),"lesson-title"));
    head.append(intro,node("span",t("chapter")+" "+data.round,"lesson-context"));main.append(head);
    const current=data.nodes.find(x=>x.state==="current");
    if(current&&!data.roundReady){
      const resume=node("section",undefined,"lesson-resume");
      const copy=node("div");copy.append(node("span",t("lesson")+" "+current.number+" "+t("of")+" 8","lesson-kicker"),node("h2",current.name));
      if(data.lesson){copy.append(node("p",t("savedPosition"),"lesson-muted"));
        copy.append(node("p",t("remaining",{count:Math.max(0,data.lesson.count-data.lesson.at)}),"lesson-small"));}
      else if(current.goal)copy.append(node("p",current.goal,"lesson-muted"));
      else if(current.questionCount!=null)copy.append(node("p",t("count",{count:current.questionCount}),"lesson-muted"));
      resume.append(copy,button(t(data.lesson?"resume":"start"),startLesson));main.append(resume);
    }
    if(data.roundReady||data.finished){
      const done=node("section",undefined,"lesson-resume");done.append(node("h2",t(data.finished?"allDone":"chapterResult")));
      if(data.roundReady)done.append(button(t("continueChapter"),()=>sendAction({action:"continue_round",revision:data.revision},false)));main.append(done);
    }
    if(data.lastCompletedLesson&&!data.roundStats.lessons?.some(item=>item.runId===data.lastCompletedLesson.runId)){
      main.append(button(t("lastResult"),()=>renderSummary(data.lastCompletedLesson),"text-button lesson-latest-result"));
    }
    const layout=node("div",undefined,"lesson-home-grid"),section=node("section");
    const label=node("div",undefined,"lesson-section-heading");label.append(node("h2",t("inChapter")),node("span",(data.roundStats.lessonsCompleted||0)+" / 8","lesson-small"));section.append(label);
    const list=node("ol",undefined,"lesson-list");
    for(const item of data.nodes){
      const row=node("li",undefined,"lesson-list-item "+item.state),body=node("div",undefined,"lesson-list-copy");
      row.append(node("span",String(item.number).padStart(2,"0"),"lesson-list-number"));
      body.append(node("strong",item.state==="locked"?t("locked"):item.state==="skipped"?t("skipped"):item.name));
      body.append(node("small",item.state==="completed"?t("complete"):item.state==="current"?t("current"):item.state==="skipped"?t("skipped"):t("lockedNote")));
      row.append(body);
      if(item.state==="completed"){
        const saved=data.roundStats.lessons?.find(l=>l.index===item.index)||{...item.stats,index:item.index,name:item.name,chapter:data.round};
        row.append(button(t("lessonResult"),()=>renderSummary(saved),"text-button lesson-result-link"));
      }else if(item.state==="current")row.append(button(t(data.lesson?"resume":"start"),startLesson,"text-button"));
      else row.append(node("span",item.state==="skipped"?"—":"○","lesson-lock"));
      list.append(row);
    }
    section.append(list);layout.append(section);review(layout);main.append(layout);
    const detail=node("details",undefined,"lesson-stat-details");detail.append(node("summary",t("chapterResult")));statsBox(detail,data.roundStats);main.append(detail);
    scopeControl(main);
    if(pending)status(t("unknown"),true,recoverPending);
  }
  async function startLesson(){
    if(working||!data)return;
    view="lesson";
    if(data.lastReceipt){
      if(data.lesson?.paused)await sendAction({action:"lesson_start",revision:data.revision},true);
      else renderReceipt(data.lastReceipt);
      return;
    }
    if(pending){renderLesson(pending.lesson,pending.question);status(t("unknown"),true,recoverPending);return;}
    if(data.lesson&&!data.lesson.paused){renderLesson();return;}
    await sendAction({action:"lesson_start",revision:data.revision},true);
  }
  function renderLesson(lessonOverride,questionOverride){
    const lesson=lessonOverride||data?.lesson,q=questionOverride||lesson?.question;
    if(!lesson||!q){renderList();return;}
    stopAudio();feedbackVisible=false;currentQuestion=q;currentLesson=lesson;setView("lesson");const holder=$("board-play");holder.replaceChildren();
    const bar=node("div",undefined,"lesson-play-top");bar.append(button("← "+t("toLessons"),pauseLesson,"text-button"));
    bar.append(node("span",t("chapter")+" "+lesson.chapter+" · "+t("lesson")+" "+(lesson.index%8+1)+"/8"));holder.append(bar);
    const wrap=node("article",undefined,"lesson-question");wrap.append(node("span",lesson.name||familyName(lesson.family),"lesson-kicker"));
    const at=lesson.cardAt??lesson.at,count=lesson.cardCount??lesson.count;
    const counter=node("p",t("question")+" "+(at+1)+" "+t("of")+" "+count,"lesson-progress-label");wrap.append(counter);
    const track=node("div",undefined,"lesson-progress-track");track.setAttribute("role","progressbar");track.setAttribute("aria-label",t("complete"));
    track.setAttribute("aria-valuemin","0");track.setAttribute("aria-valuemax",String(lesson.count));track.setAttribute("aria-valuenow",String(lesson.at));
    const fill=node("div",undefined,"lesson-progress-fill");fill.style.width=(lesson.count?100*lesson.at/lesson.count:0)+"%";track.append(fill);wrap.append(track);
    const title=node("h2",q.prompt,"lesson-question-prompt");title.id="lesson-question-heading";
    title.lang=q.promptLang||(q.direction==="ru-gr"?q.lang||lang():q.kind==="listening"?lang():"el");title.dir=title.lang==="ar"?"rtl":"ltr";
    if(q.kind==="dialogue"){title.classList.add("lesson-dialogue-instruction");title.lang=q.lang||lang();title.dir="auto";}
    if(String(q.prompt).includes("\n"))title.classList.add("lesson-long-prompt");wrap.append(title);
    if(q.lang&&q.lang!==lang())wrap.append(node("p",t("contentLanguage"),"lesson-muted"));
    if(q.note&&q.kind!=="life"&&q.type!=="life"){const note=node("p",q.note,"lesson-muted lesson-question-note");note.lang=q.lang||lang();note.dir=note.lang==="ar"?"rtl":"ltr";wrap.append(note);}
    if(q.scenarioTitle)wrap.append(node("p",q.scenarioTitle+" · "+q.scenarioStep+"/"+q.scenarioTotal,"lesson-scenario"));
    dialogue(wrap,q);clock(wrap,q);sound(wrap,q);
    const form=node("form",undefined,"lesson-answer-form");form.setAttribute("aria-labelledby","lesson-question-heading");
    const answers=node("div",undefined,"lesson-choices"),feedback=node("section",undefined,"lesson-feedback");
    feedback.id="lesson-feedback";feedback.setAttribute("role","status");feedback.setAttribute("aria-live","polite");feedback.setAttribute("aria-atomic","false");feedback.hidden=true;
    const error=node("p",undefined,"lesson-input-error");error.setAttribute("role","alert");error.hidden=true;
    const restored=draft?.key===draftKey(lesson,q)?draft:null;
    let selected=restored?.selected??null;
    const check=node("button",t("check"),"primary lesson-primary");check.type="submit";check.disabled=true;
    if(q.type==="life"||q.typedAnswer){
      const label=node("label",t("typeGreek"));label.htmlFor="lesson-typed-answer";form.append(label);
      const input=node(q.type==="life"?"textarea":"input",undefined,"lesson-textarea");
      if(input.tagName==="INPUT")input.type="text";else input.rows=3;
      input.id="lesson-typed-answer";input.lang="el";input.dir="ltr";input.autocomplete="off";input.autocapitalize="off";input.spellcheck=false;
      input.maxLength=q.type==="life"?320:80;input.setAttribute("aria-describedby","lesson-answer-hint");
      input.value=String(restored?.selected||"");
      if(pending?.body?.questionId===q.id)input.value=String(pending.body.selected||"");
      input.addEventListener("input",()=>{selected=input.value;check.disabled=!input.value.trim()||working;error.hidden=true;});
      input.addEventListener("keydown",event=>{if(event.key==="Enter"&&!event.shiftKey&&!event.isComposing){event.preventDefault();form.requestSubmit();}});
      answers.append(input);selected=input.value;check.disabled=!selected.trim();
    }else if(q.kind==="order"){
      const chosen=restored?.order?.slice()||[],built=node("div",undefined,"lesson-order-built");built.lang="el";built.dir="ltr";
      const pool=node("div",undefined,"lesson-order-pool");const tokens=q.tokens||[];
      const redraw=()=>{built.replaceChildren();pool.replaceChildren();
        chosen.forEach((index,position)=>{const b=button(tokens[index],()=>{chosen.splice(position,1);redraw();},"secondary");b.dataset.token=index;built.append(b);});
        tokens.forEach((value,index)=>{const b=button(value,()=>{chosen.push(index);redraw();},"secondary");b.disabled=chosen.includes(index);pool.append(b);});
        selected=chosen.map(i=>tokens[i]).join(" ");check.disabled=chosen.length!==tokens.length;};
      answers.append(built,pool);redraw();
    }else{
      const field=node("fieldset");field.append(node("legend",t("choose")));
      const options=node("div",undefined,"lesson-option-grid");
      const items=q.kind==="accent"?q.letters:q.choices||[];
      if(items.some(x=>String(x).length>36))options.classList.add("long-options");
      items.forEach((value,index)=>{
        if(q.kind==="accent"&&!q.accentableIndices?.includes(index))return;
        const label=node("label",undefined,"lesson-option");const input=node("input");input.type="radio";input.name="lesson-answer";input.value=q.kind==="accent"?String(index):String(value);input.checked=String(selected)===input.value;if(input.checked)check.disabled=false;
        const display=q.kind==="accent"?items.map((letter,position)=>String(letter).normalize("NFD").replace(/\u0301/g,"")+(position===index?"\u0301":"")).join("").normalize("NFC"):value;
        const text=node("span",display);text.lang=q.direction==="gr-ru"?q.lang||lang():"el";text.dir=text.lang==="ar"?"rtl":"ltr";
        input.addEventListener("change",()=>{selected=q.kind==="accent"?String(index):value;check.disabled=false;});
        label.append(input,text);options.append(label);
      });
      field.append(options);answers.append(field);
    }
    const actions=node("div",undefined,"lesson-answer-actions"),hint=node("p",t("draft"),"lesson-muted");hint.id="lesson-answer-hint";
    actions.append(hint,check);form.append(answers,error,actions);wrap.append(form,feedback);holder.append(wrap);
    form.addEventListener("submit",event=>{
      event.preventDefault();if(working||feedbackVisible)return;
      if(selected==null||!String(selected).trim()){error.textContent=t("emptyAnswer");error.hidden=false;return;}
      if(typeof selected==="string"&&selected.length>(q.type==="life"?320:80)&&q.typedAnswer){error.textContent=t("longAnswer",{count:80});error.hidden=false;return;}
      submitAnswer(selected,q,lesson);
    });
    if(pending)for(const el of form.querySelectorAll("input,textarea,button"))el.disabled=true;
    focusHeading(title);
  }
  function detailText(parent,label,value,greek=false){
    if(!value)return;const section=node("div",undefined,"lesson-feedback-detail");section.append(node("strong",label));
    const text=node("p",Array.isArray(value)?value.join(" / "):value);
    text.lang=greek?(["gr-ru","gr-target"].includes(currentQuestion?.direction)?currentQuestion.lang||lang():"el"):currentQuestion?.lang||lang();
    text.dir=text.lang==="ar"?"rtl":"ltr";if(greek)text.className="lesson-correct-answer";section.append(text);parent.append(section);
  }
  function renderFeedback(result,selected,receipt){
    if(!visible()){return;}feedbackVisible=true;const form=$("board-play").querySelector(".lesson-answer-form"),panel=$("lesson-feedback");
    if(!panel)return;form.hidden=true;panel.hidden=false;panel.replaceChildren();
    const title=node("h3",t(result.correct?"correct":result.unverified?"unverified":"wrong"),result.correct?"lesson-correct":result.unverified?"lesson-uncertain":"lesson-incorrect");
    title.id="lesson-feedback-title";panel.append(title);
    if(!result.correct&&selected!=null)detailText(panel,t("yourAnswer"),Array.isArray(selected)?selected.map(i=>currentQuestion?.tokens?.[i]||i).join(" "):selected,true);
    detailText(panel,t("correction"),result.closestAnswer||result.answer,true);
    detailText(panel,t("explanation"),result.explanation);
    if(result.orthographyNote)panel.append(node("p",result.orthographyNote,"lesson-orthography"));
    const translation=result.translation||result.clozeTranslation||result.meaning;
    if(translation)detailText(panel,t("meaning"),translation);
    const alternatives=[result.answer,...(result.alternatives||result.acceptedAnswers||[])].filter((x,i,a)=>x&&x!==(result.closestAnswer||result.answer)&&a.indexOf(x)===i);
    if(alternatives.length){const details=node("details");details.append(node("summary",t("alternatives")));detailText(details,"",alternatives,true);panel.append(details);}
    if(result.conjugation?.forms){
      const details=node("details");details.append(node("summary",t("details")));const table=node("table",undefined,"conjugation-table");
      (result.conjugation.persons||["εγώ","εσύ","αυτός / αυτή","εμείς","εσείς","αυτοί / αυτές"]).forEach((person,i)=>{const row=node("tr");row.append(node("th",person),node("td",result.conjugation.forms[i]));table.append(row);});
      table.lang="el";table.dir="ltr";details.append(table);panel.append(details);
    }
    for(const key of["rule","note","syllableExplanation","articleExplanation","encliticExplanation","wordMeaning","phraseTranslation"])
      if(result[key]&&result[key]!==result.explanation)detailText(panel,t("details"),result[key]);
    if(result.dialogueFullTemplate&&result.dialogueFullGlosses){
      const details=node("details");details.append(node("summary",t("meaning")));
      for(const line of result.dialogueFullTemplate)details.append(node("p",String(line).replace(/\[\[(\d+)\]\]/g,(_,n)=>result.dialogueFullGlosses[currentQuestion?.filledGaps?.[n]||result.answer]||"…")));
      panel.append(details);
    }
    if(currentQuestion?.kind==="dialogue"){
      const gap=Number.isInteger(currentQuestion.activeGap)?currentQuestion.activeGap:Number((currentQuestion.direction||"gap0").slice(3));
      const blank=$("board-play").querySelector('[data-gap="'+gap+'"]');if(blank){blank.textContent=result.answer;blank.className="lesson-dialogue-gap filled";blank.lang="el";blank.dir="ltr";blank.removeAttribute("aria-current");}
    }
    panel.append(node("p",t("finalAnswer"),"lesson-muted"));
    const next=button(t(result.lessonComplete?"finish":"next"),()=>acknowledge(receipt,result),"primary lesson-next");next.setAttribute("aria-describedby","lesson-feedback-title");
    panel.append(next);status(t("saved"));queueMicrotask(()=>next.focus({preventScroll:true}));
  }
  function renderReceipt(receipt){
    const lesson=receipt.lesson||pending?.lesson||(data.lesson?{...data.lesson,at:Math.max(0,data.lesson.at-1)}:null)||{index:receipt.lessonIndex||0,chapter:Math.floor((receipt.lessonIndex||0)/8)+1,name:receipt.feedback?.lessonComplete?.name||t("lesson"),at:0,count:1};
    const question=receipt.question||pending?.question||lesson.question;
    if(!question){status(t("network"),true,open);return;}
    renderLesson(lesson,question);renderFeedback(receipt.feedback||data.feedback,receipt.selected,receipt);
  }
  async function acknowledge(receipt,result){
    if(working)return;working=true;const generation=ownerGeneration;status(t("saving"));
    try{if(receipt?.requestId)data=await request({action:"ack_feedback",requestId:receipt.requestId,revision:data.revision});
      feedbackVisible=false;pending=null;persistPending();status("");
      if(result.lessonComplete)renderSummary(result.lessonComplete);
      else {if(data.lesson?.paused)data=await request({action:"lesson_start",revision:data.revision});renderLesson();}
    }catch(error){errorStatus(error,()=>acknowledge(receipt,result));}finally{finishWork(generation);}
  }
  function renderSummary(lesson){
    currentSummary=lesson;stopAudio();setView("summary");feedbackVisible=false;const main=$("board-play");main.replaceChildren();
    const panel=node("article",undefined,"lesson-summary"),title=node("h1",t("done"));
    panel.append(node("span",t("chapter")+" "+(lesson.chapter||Math.floor(lesson.index/8)+1),"lesson-kicker"),title,node("p",t("practised")+": "+(lesson.name||familyName(lesson.family)),"lesson-muted"));
    statsBox(panel,{...lesson,accuracy:lesson.attempts?Math.round(100*(lesson.correct??lesson.attempts-lesson.errors)/lesson.attempts):null},t("lessonResult"));
    if(data.backlog?.due)panel.append(node("p",t("backlogNote"),"lesson-muted"));
    const ai=node("section");ai.id="lesson-summary-ai";panel.append(ai);
    const actions=node("div",undefined,"lesson-summary-actions");
    if(data.roundReady)actions.append(button(t("continueChapter"),()=>sendAction({action:"continue_round",revision:data.revision},false)));
    else if(data.nodes.some(n=>n.state==="current"))actions.append(button(t("resume"),()=>{renderList();startLesson();}));
    actions.append(button(t("toLessons"),renderList,"secondary"));panel.append(actions);main.append(panel);focusHeading(title);
    document.dispatchEvent(new CustomEvent("lexi:lesson-complete",{detail:{lesson,runId:lesson.runId,chapter:lesson.chapter,board:data,lang:lang()}}));
  }
  async function reconcile(){
    const latest=await request();data=latest;
    const receipt=latest.lastReceipt;
    if(receipt){
      if(pending&&receipt.requestId!==pending.body.requestId)status(t("conflict"),true);
      pending=null;persistPending();if(visible()&&view!=="list")renderReceipt(receipt);else if(visible())renderList();return true;
    }
    return false;
  }
  async function submitAnswer(selected,q,lesson){
    if(working||feedbackVisible)return;
    if(!pending){pending={owner:window.LexiApp?.accountKey(),body:{action:"answer",revision:data.revision,lessonIndex:lesson.index,questionId:q.id,selected,requestId:uuid(),lang:lang()},question:q,lesson:{...lesson,question:undefined}};persistPending();}
    await sendPending();
  }
  async function sendPending(){
    if(!pending||working)return;working=true;const generation=ownerGeneration;status(t("saving"));
    for(const el of $("board-play").querySelectorAll(".lesson-answer-form input,.lesson-answer-form textarea,.lesson-answer-form button"))el.disabled=true;
    const submission=pending;
    try{data=await request(submission.body,false,submission.owner);pending=null;persistPending();
      const receipt=data.lastReceipt||{requestId:submission.body.requestId,question:submission.question,lesson:submission.lesson,selected:submission.body.selected,feedback:data.feedback};
      if(visible()&&view!=="list")renderReceipt(receipt);else if(visible())renderList();
      document.dispatchEvent(new CustomEvent("lexi:progress",{detail:{source:"board"}}));
    }catch(error){
      if(error.message==="account_changed")return;
      try{if(!await reconcile()){
        const unchanged=data.lesson?.index===submission.lesson.index&&data.lesson?.at===submission.lesson.at;
        if(!unchanged){pending=null;persistPending();if(visible())renderList();status(t("conflict"),true);}
        else status(t("unknown"),true,recoverPending);
      }}catch{status(t("unknown"),true,recoverPending);}
    }finally{finishWork(generation);}
  }
  async function recoverPending(){
    if(working)return;working=true;const generation=ownerGeneration;status(t("unknown"));
    try{const found=await reconcile();if(found)return;
      if(!pending)return;
      const unchanged=data.lesson?.index===pending.lesson.index&&data.lesson?.at===pending.lesson.at;
      if(!unchanged){pending=null;persistPending();renderList();status(t("conflict"),true);return;}
    }catch(error){errorStatus(error,recoverPending);return;}finally{finishWork(generation);}
    if(pending)await sendPending();
  }
  function finishWork(generation){
    if(generation!==ownerGeneration)return;
    working=false;
    if(pauseAfterPending&&!pending){pauseAfterPending=false;pauseLesson(false);}
  }
  async function pauseLesson(showList=true){
    captureDraft();stopAudio();if(showList){view="list";if(data)renderList();}
    if(working||pending){pauseAfterPending=true;return;}
    if(!data?.lesson||data.lesson.paused)return;
    working=true;const generation=ownerGeneration;
    try{data=await request({action:"pause",revision:data.revision},document.visibilityState==="hidden");if(showList&&visible())renderList();}
    catch(error){if(showList)errorStatus(error,open);}
    finally{finishWork(generation);}
  }
  async function sendAction(body,showQuestion){
    if(working)return;working=true;const generation=ownerGeneration;status(t("loading"));
    try{data=await request(body);status("");if(!visible())return;
      if(showQuestion&&data.lastReceipt)renderReceipt(data.lastReceipt);
      else if(showQuestion&&data.lesson)renderLesson();else renderList();
    }catch(error){
      if(error.message==="stale_track"){try{data=await request();if(visible())renderList();status(t("conflict"),true);}catch(e){errorStatus(e,open);}}
      else errorStatus(error,()=>sendAction({...body,revision:data.revision},showQuestion));
    }finally{finishWork(generation);}
  }
  async function open(){
    if(!visible()||working||window.LexiApp?.loggedIn()===false)return;
    working=true;const generation=ownerGeneration;status(t("loading"));restorePending();
    try{data=await request();status("");if(data.lastReceipt){pending=null;persistPending();renderReceipt(data.lastReceipt);}else renderList();}
    catch(error){errorStatus(error,open);}finally{finishWork(generation);}
  }
  function leave(){
    captureDraft();stopAudio();document.body.classList.remove("lesson-active");
    if(working)pauseAfterPending=true;else if(data?.lesson&&!data.lesson.paused)pauseLesson(false);
  }
  document.addEventListener("visibilitychange",()=>{if(document.hidden&&visible())leave();else if(visible()&&view==="lesson"&&!working)open();});
  window.addEventListener("pagehide",leave);
  document.addEventListener("lexi:logout",()=>{ownerGeneration++;working=false;stopAudio();pending=null;data=null;draft=null;currentQuestion=null;currentLesson=null;view="list";feedbackVisible=false;pauseAfterPending=false;});
  async function changeLanguage(){
    captureDraft();if(!visible())return;const previous=view;
    if(previous==="lesson"&&currentQuestion){
      if(feedbackVisible&&data.lastReceipt)renderReceipt(data.lastReceipt);
      else renderLesson({...currentLesson,name:familyName(currentLesson.family)},currentQuestion);
    }else if(previous==="summary"&&currentSummary)renderSummary(currentSummary);
    else if(data)renderList();
    if(working)return;working=true;const generation=ownerGeneration;
    try{
      data=await request();if(!visible())return;
      if(previous==="summary"&&currentSummary){
        const localized=data.roundStats.lessons?.find(item=>item.runId===currentSummary.runId)||data.lastCompletedLesson;
        renderSummary(localized?.runId===currentSummary.runId?localized:currentSummary);
      }else if(data.lastReceipt)renderReceipt(data.lastReceipt);
      else if(previous==="lesson"&&data.lesson&&!data.lesson.paused)renderLesson();
      else renderList();
    }catch(error){errorStatus(error,changeLanguage);}finally{finishWork(generation);}
  }
  window.lexiBoard={onOpen:open,onLeave:leave,onLanguageChange:changeLanguage,refresh:open};
})();
