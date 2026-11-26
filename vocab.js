"use strict";
(() => {
 const $=id=>document.getElementById(id);
 const terms={
  ru:{title:"Словарь A1 / A2",subtitle:"Отдельные тематические уроки: сначала 10 слов с переводом, затем восемь вариантов ответа. Ошибки живут в отдельной очереди.",theme:"Тема",level:"Уровень",new:"Изучить 10 новых слов",review:"Повторить ошибки",preview:"Сначала запомни эти 10 слов",start:"Я запомнил — начать карточки →",next:"Следующее слово →",done:"Урок завершён",again:"Следующие 10 слов →",weak:"Ошибок",learned:"Уже тренировались",remaining:"Осталось новых",correct:"Верно",wrong:"Ошибка. Правильно: ",empty:"В этой теме больше нет новых слов. Можно повторить ошибки или выбрать другую тему.",noWeak:"Ошибок для повторения в выбранной теме пока нет.",error:"Не получилось загрузить урок: ",lesson:"УРОК СЛОВ",back:"Назад к темам",fallback:"Для этого слова ещё нет перевода на выбранный язык — показан английский.",source:"Уровни слов ориентировочные, а не официальный список CEFR. Словоформы не считаются отдельными словами."},
  en:{title:"A1 / A2 vocabulary",subtitle:"An independent vocabulary course: preview ten themed words and then practice eight-choice translation cards. Mistakes have a separate review queue.",theme:"Topic",level:"Level",new:"Learn 10 new words",review:"Review mistakes",preview:"First, remember these 10 words",start:"Ready — start the cards →",next:"Next word →",done:"Lesson completed",again:"Next 10 words →",weak:"Needs review",learned:"Practised",remaining:"New remaining",correct:"Correct",wrong:"Incorrect. Answer: ",empty:"There are no new words left here. Review mistakes or choose another topic.",noWeak:"There are no mistakes to review in this topic yet.",error:"Could not load the lesson: ",lesson:"WORD LESSON",back:"Back to topics",fallback:"A translation in the selected language is not available yet; English is shown.",source:"CEFR levels are editorial estimates, not an official mandatory word list. Inflections are not counted as separate words."},
  zh:{title:"A1 / A2 希腊语词汇",subtitle:"按主题学习：先记住十个新词，再做八选一练习。错题单独复习。",theme:"主题",level:"级别",new:"学习10个新词",review:"复习错题",preview:"先记住这10个词",start:"记住了，开始练习 →",next:"下一个词 →",done:"课程完成",again:"继续学习10个词 →",weak:"待复习",learned:"已练习",remaining:"剩余新词",correct:"正确",wrong:"错误。正确答案：",empty:"此主题已没有新词。可以复习错题或选择其他主题。",noWeak:"此主题没有需要复习的错题。",error:"加载课程失败：",lesson:"词汇课程",back:"返回主题",fallback:"此词暂无中文翻译，显示英语释义。",source:"词汇等级仅供学习参考，并非 CEFR 官方词表；词形变化不重复计数。"},
  es:{title:"Vocabulario A1 / A2",subtitle:"Lecciones por temas: primero memoriza diez palabras y luego practica con ocho opciones. Repasa los errores aparte.",theme:"Tema",level:"Nivel",new:"Aprender 10 palabras nuevas",review:"Repasar errores",preview:"Primero memoriza estas 10 palabras",start:"Ya las sé: empezar →",next:"Siguiente palabra →",done:"Lección terminada",again:"Otras 10 palabras →",weak:"Por repasar",learned:"Practicadas",remaining:"Nuevas pendientes",correct:"Correcto",wrong:"Incorrecto. Respuesta: ",empty:"No quedan palabras nuevas en este tema. Repasa errores o elige otro tema.",noWeak:"No hay errores pendientes en este tema.",error:"No se pudo cargar la lección: ",lesson:"LECCIÓN DE VOCABULARIO",back:"Volver a temas",fallback:"Aún no hay traducción al español; se muestra el inglés.",source:"Los niveles son estimaciones didácticas, no una lista oficial del MCER. Las formas flexionadas no se cuentan aparte."},
  pt:{title:"Vocabulário A1 / A2",subtitle:"Lições por tema: primeiro memoriza dez palavras, depois pratica com oito opções. Revê os erros à parte.",theme:"Tema",level:"Nível",new:"Aprender 10 palavras novas",review:"Rever erros",preview:"Primeiro, memoriza estas 10 palavras",start:"Já memorizei — começar →",next:"Palavra seguinte →",done:"Lição concluída",again:"Mais 10 palavras →",weak:"Por rever",learned:"Praticadas",remaining:"Novas por aprender",correct:"Certo",wrong:"Incorreto. Resposta: ",empty:"Já não há palavras novas neste tema. Revê os erros ou escolhe outro tema.",noWeak:"Não há erros para rever neste tema.",error:"Não foi possível carregar a lição: ",lesson:"LIÇÃO DE VOCABULÁRIO",back:"Voltar aos temas",fallback:"Ainda não existe tradução em português; aparece o inglês.",source:"Os níveis são estimativas didáticas, não uma lista oficial do QECR. As formas flexionadas não contam como palavras diferentes."},
  ar:{title:"مفردات A1 / A2",subtitle:"دروس مستقلة حسب الموضوع: تعلّم عشر كلمات ثم اختبر نفسك بثمانية خيارات. مراجعة الأخطاء منفصلة.",theme:"الموضوع",level:"المستوى",new:"تعلّم ١٠ كلمات جديدة",review:"مراجعة الأخطاء",preview:"احفظ أولاً هذه الكلمات العشر",start:"أنا مستعد — ابدأ البطاقات",next:"الكلمة التالية",done:"اكتمل الدرس",again:"العشر كلمات التالية",weak:"تحتاج مراجعة",learned:"تم التدريب",remaining:"متبقية",correct:"صحيح",wrong:"خطأ. الصحيح: ",empty:"لا توجد كلمات جديدة هنا. راجع الأخطاء أو اختر موضوعاً آخر.",noWeak:"لا توجد أخطاء للمراجعة في هذا الموضوع.",error:"تعذّر تحميل الدرس: ",lesson:"درس المفردات",back:"العودة إلى المواضيع",fallback:"لا تتوفر ترجمة عربية لهذه الكلمة بعد؛ يظهر المعنى بالإنجليزية.",source:"المستويات تقديرية وليست قائمة رسمية من CEFR. التصريفات لا تُحسب كلمات منفصلة."}
 };
 const AUDIO_STRINGS={
  ru:{play:"🔊 Послушать слово",slow:"0,8× Медленно",previewPlay:"Послушать произношение",pocket:"Запись Pocket TTS.",unavailable:"Запись Pocket TTS для этого слова ещё не готова.",errorAudio:"Воспроизведение недоступно.",doneAudio:"Готово.",coverage:"Готовых записей Pocket TTS: {count} из 1700. Для остальных воспроизведение пока недоступно."},
  en:{play:"🔊 Hear word",slow:"0.8× Slower",previewPlay:"Hear pronunciation",pocket:"Offline Pocket TTS recording.",unavailable:"Pocket TTS recording for this word is not ready yet.",errorAudio:"Playback unavailable.",doneAudio:"Finished.",coverage:"Pocket TTS recordings: {count} of 1700. Playback is unavailable for the remaining words."},
  zh:{play:"🔊 听单词",slow:"0.8× 慢速",previewPlay:"聆听发音",pocket:"Pocket TTS 离线录音。",unavailable:"这个词的 Pocket TTS 录音尚未准备好。",errorAudio:"无法播放。",doneAudio:"播放完毕。",coverage:"Pocket TTS 已录制 {count}/1700 个词；其余暂时无法播放。"},
  ar:{play:"🔊 استمع إلى الكلمة",slow:"0.8× ببطء",previewPlay:"سماع النطق",pocket:"تسجيل Pocket TTS محفوظ.",unavailable:"تسجيل Pocket TTS لهذه الكلمة غير جاهز بعد.",errorAudio:"التشغيل غير متاح.",doneAudio:"انتهى التشغيل.",coverage:"تسجيلات Pocket TTS: {count} من 1700؛ تشغيل بقية الكلمات غير متاح مؤقتًا."},
  es:{play:"🔊 Escuchar palabra",slow:"0,8× Lento",previewPlay:"Escuchar pronunciación",pocket:"Grabación Pocket TTS sin conexión.",unavailable:"La grabación Pocket TTS de esta palabra aún no está lista.",errorAudio:"No disponible.",doneAudio:"Listo.",coverage:"Grabaciones Pocket TTS: {count} de 1700. El resto aún no se puede reproducir."},
  pt:{play:"🔊 Ouvir palavra",slow:"0,8× Devagar",previewPlay:"Ouvir pronúncia",pocket:"Gravação Pocket TTS offline.",unavailable:"A gravação Pocket TTS desta palavra ainda não está pronta.",errorAudio:"Reprodução indisponível.",doneAudio:"Terminado.",coverage:"Gravações Pocket TTS: {count} de 1700. As restantes ainda não podem ser reproduzidas."}
 };
 for(const [locale,labels] of Object.entries(AUDIO_STRINGS))Object.assign(terms[locale],labels);
 function statusFromAudio(code){
   return ({pocket:"pocket",unavailable:"unavailable",error:"errorAudio",done:"doneAudio"})[code]||"errorAudio";
 }
 async function playWord(word,{slow=false,statusId="vocab-audio-status"}={}){
   if(!word?.wordAudio || !window.LexiWordAudio)return;
   await window.LexiWordAudio.play(word.wordAudio,{
     slow,onStatus:state=>{
       if((statusId==="vocab-audio-status"&&current===word)||
          (statusId==="vocab-preview-audio-status"&&!$("vocab-word-preview").hidden)){
         set(statusId,tr(statusFromAudio(state)));
       }
     }
   });
 }

 let meta=null,words=[],pos=0,review=false,busy=false,correct=0,wrong=0,current=null,pending=null,receipt=null,selection=null,lessonLang="en",preview=false,loadedOwner=null,ownerGeneration=0;
 const storageKey="lexi-vocab-session-v1";
 const ui=(key,values)=>window.LexiUI.t(key,values);
 const language=()=>$("lang").value;
 const visible=()=>!$("vocab-view").hidden;
 const uuid=()=>window.crypto?.randomUUID?.()||"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,c=>{const r=Math.floor(Math.random()*16);return(c==="x"?r:r&3|8).toString(16);});
 const tr=key=>(terms[language()]||terms.en)[key]||terms.en[key];
 const englishHint=(value,en)=>lessonLang!=="en"&&en&&value.trim().toLocaleLowerCase()!==en.trim().toLocaleLowerCase()?value+" ("+en+")":value;
 const api=async(path,opts)=>{
   const headers=new Headers(opts?.headers),owner=headers.get("X-Lexi-Owner")||window.LexiApp?.accountKey();
   if((opts?.method||"GET").toUpperCase()==="POST"){
     if(!window.LexiApp?.loggedIn()||!owner)throw Error("account_changed");
     if(!headers.has("X-Lexi-Owner"))headers.set("X-Lexi-Owner",owner);
   }
   const response=await fetch("/greek/api/"+path,{credentials:"same-origin",cache:"no-store",...opts,headers});
   const result=await response.json().catch(()=>({}));
   if(owner!==window.LexiApp?.accountKey())throw Error("account_changed");
   if(!response.ok){if(result.error==="account_changed")window.LexiApp?.reconcileAccount?.();const error=Error(result.error||"HTTP "+response.status);error.status=response.status;throw error;}
   return result;
 };
 const set=(id,value)=>{$(id).textContent=value;};
 const show=(id,yes)=>{$(id).hidden=!yes;};
 const node=(tag,value,css)=>{const el=document.createElement(tag);if(value!==undefined)el.textContent=String(value);if(css)el.className=css;return el;};
 const focus=el=>{if(visible()){el.tabIndex=el.tabIndex<0?-1:el.tabIndex;el.focus({preventScroll:true});}};
 function save(){
   try{
     if(words.length)sessionStorage.setItem(storageKey,JSON.stringify({owner:window.LexiApp?.accountKey(),words,pos,review,correct,wrong,pending,receipt,selection,lessonLang,preview}));
     else sessionStorage.removeItem(storageKey);
   }catch{}
 }
 function restore(){
   const owner=window.LexiApp?.accountKey();
   if(loadedOwner===owner)return;
   loadedOwner=owner;words=[];pending=null;receipt=null;current=null;selection=null;pos=0;
   try{
     const stored=JSON.parse(sessionStorage.getItem(storageKey)||"null");
     if(stored?.owner!==owner||!Array.isArray(stored.words))return;
     ({words,pos,review,correct,wrong,pending,receipt,selection,lessonLang,preview}=stored);
     if(pending&&!pending.owner)pending.owner=stored.owner;
     pos=Number(pos)||0;correct=Number(correct)||0;wrong=Number(wrong)||0;
   }catch{}
 }
 function message(value,retry,id="vocab-message"){
   const target=$(id);target.replaceChildren();target.hidden=!value;target.setAttribute("role","status");
   if(value)target.append(node("p",value));
   if(retry){const button=node("button",ui("retry"),"secondary");button.type="button";button.addEventListener("click",retry);target.append(button);}
 }
 function failure(error,retry,id){
   if(error.message==="account_changed")return;
   if(error.status===401||error.message==="login_required"){window.LexiApp?.requireLogin();return;}
   message(ui(pending?"unknown":"network"),retry,id);
 }
 function renderMeta(){
   if(!meta)return;
   set("vocab-title",tr("title"));set("vocab-subtitle",tr("subtitle"));set("vocab-topic-label",tr("theme"));
   set("vocab-level-label",tr("level"));set("vocab-new",tr("new"));set("vocab-review",tr("review"));
   set("vocab-source",tr("source"));set("vocab-back",tr("back"));set("vocab-again",tr("again"));set("vocab-begin",tr("start"));
   const select=$("vocab-topic"),prev=select.value;select.replaceChildren();
   const topicLocales={
     zh:{everyday:"日常",shopping:"购物",road:"交通",home:"居家",food:"食物",family:"家庭",work:"工作",city:"城市",health:"健康",time:"时间",travel:"旅行",leisure:"休闲",nature:"自然"},
     ar:{everyday:"الحياة اليومية",shopping:"التسوق",road:"المواصلات",home:"المنزل",food:"الطعام",family:"العائلة",work:"العمل",city:"المدينة",health:"الصحة",time:"الوقت",travel:"السفر",leisure:"الترفيه",nature:"الطبيعة"},
     es:{everyday:"Vida cotidiana",shopping:"Compras",road:"Transporte",home:"Hogar",food:"Alimentación",family:"Familia",work:"Trabajo",city:"Ciudad",health:"Salud",time:"Tiempo",travel:"Viajes",leisure:"Ocio",nature:"Naturaleza"},
     pt:{everyday:"Dia a dia",shopping:"Compras",road:"Transportes",home:"Casa",food:"Alimentação",family:"Família",work:"Trabalho",city:"Cidade",health:"Saúde",time:"Tempo",travel:"Viagens",leisure:"Lazer",nature:"Natureza"}
   };
   const lang=language(),allTopics={ru:"Все темы",en:"All topics",zh:"所有主题",ar:"كل المواضيع",es:"Todos los temas",pt:"Todos os temas"};
   const any=node("option",allTopics[lang]);any.value="all";select.append(any);
   meta.topics.forEach(topic=>{const option=node("option",(topicLocales[lang]?.[topic.id]||(lang==="ru"?topic.ru:topic.en))+" · "+topic.count);option.value=topic.id;select.append(option);});
   if(Array.from(select.options).some(option=>option.value===prev))select.value=prev;
   set("vocab-total",meta.count+" · A1 "+meta.levels.A1+" / A2 "+meta.levels.A2);
 }
 async function loadMeta(){
   try{meta=await api("vocab/meta");renderMeta();}
   catch(error){failure(error,loadMeta);}
 }
 function renderStats(data){
   set("vocab-progress",tr("learned")+": "+data.learned+" · "+tr("remaining")+": "+data.remaining+" · "+tr("weak")+": "+data.weak);
 }
 function renderPreview(){
   preview=true;show("vocab-controls",false);show("vocab-lesson",true);show("vocab-word-preview",true);show("vocab-card",false);show("vocab-summary",false);
   set("vocab-preview-audio-status","");set("vocab-preview-heading",tr("preview"));set("vocab-begin",tr("start"));
   const list=$("vocab-preview-list");list.replaceChildren();
   words.forEach(word=>{
     const row=node("div",undefined,"topic-study-row"),greek=node("strong",[word.gr,...(word.greekVariants||[])].join(" / "));
     greek.lang="el";greek.dir="ltr";
     const translation=node("span",word.translation);translation.lang=word.untranslated?"en":lessonLang;translation.dir=translation.lang==="ar"?"rtl":"ltr";
     const level=node("small",word.level+(word.untranslated?" · EN":""));
     const sound=node("button","♪","vocab-audio-btn");sound.type="button";const ready=window.LexiWordAudio?.available(word.wordAudio)??false;
     sound.disabled=!ready;sound.title=ready?tr("previewPlay"):ui("audioUnavailable");sound.setAttribute("aria-label",sound.title);
     sound.addEventListener("click",()=>playWord(word,{statusId:"vocab-preview-audio-status"}));
     row.append(greek,translation,level,sound);list.append(row);
   });
   save();focus($("vocab-preview-heading"));
 }
 async function loadLesson(isReview){
   if(busy||pending)return;busy=true;const generation=ownerGeneration;message(ui("loading"));
   for(const id of ["vocab-new","vocab-review"])$(id).disabled=true;
   try{
     if(!meta){meta=await api("vocab/meta");renderMeta();}
     const topic=$("vocab-topic").value||"all",level=$("vocab-level").value||"A1",lang=language();
     const lesson=await api("vocab/lesson?"+new URLSearchParams({topic,level,lang,review:isReview?"1":"0"}));
     renderStats(lesson);words=lesson.words;review=isReview;pos=0;correct=0;wrong=0;current=null;receipt=null;selection=null;lessonLang=lang;
     if(!words.length){message(review?tr("noWeak"):tr("empty"));show("vocab-lesson",false);show("vocab-controls",true);save();return;}
     message("");show("vocab-controls",false);show("vocab-lesson",true);show("vocab-summary",false);
     if(!review)renderPreview();else renderCard();
   }catch(error){failure(error,()=>loadLesson(isReview));}
   finally{if(generation===ownerGeneration){busy=false;for(const id of ["vocab-new","vocab-review"])$(id).disabled=false;}}
 }
 function renderCard(){
   window.LexiWordAudio?.stop();preview=false;current=words[pos];
   if(!current){done();return;}
   show("vocab-controls",false);show("vocab-lesson",true);show("vocab-word-preview",false);show("vocab-summary",false);show("vocab-card",true);
   set("vocab-audio-status","");set("vocab-pronounce",tr("play"));set("vocab-pronounce-slow",tr("slow"));
   const ready=window.LexiWordAudio?.available(current.wordAudio)??false;
   $("vocab-pronounce").disabled=!ready;$("vocab-pronounce-slow").disabled=!ready;
   if(!ready)set("vocab-audio-status",ui("audioUnavailable"));
   show("vocab-feedback",false);show("vocab-next",false);
   set("vocab-question-count",(pos+1)+" / "+words.length);set("vocab-card-heading",tr("lesson"));
   set("vocab-prompt",current.direction==="gr-target"?[current.gr,...(current.greekVariants||[])].join(" / "):englishHint(current.translation,current.english));
   const prompt=$("vocab-prompt");prompt.lang=current.direction==="gr-target"?"el":current.untranslated?"en":lessonLang;prompt.dir=prompt.lang==="ar"?"rtl":"ltr";
   set("vocab-direction",current.direction==="gr-target"?"Ελληνικά → ?":"? → Ελληνικά");
   const choices=$("vocab-choices");choices.replaceChildren();choices.classList.add("vocab-answer-container");
   const form=node("form"),fieldset=node("fieldset",undefined,"lesson-choices");fieldset.append(node("legend",ui("choose"),"sr-only"));
   const submit=node("button",ui("check"),"primary");submit.type="submit";submit.id="vocab-submit";submit.disabled=selection===null||Boolean(pending)||Boolean(receipt);
   current.choices.forEach((choice,index)=>{
     const label=node("label",undefined,"lesson-choice"),radio=node("input");radio.type="radio";radio.name="vocab-answer";radio.value=String(index);radio.checked=selection===index;radio.disabled=Boolean(pending)||Boolean(receipt);
     const copy=node("span",current.direction==="gr-target"?englishHint(choice,current.choicesEn?.[index]):choice);
     copy.lang=current.direction==="gr-target"?current.untranslated?"en":lessonLang:"el";copy.dir=copy.lang==="ar"?"rtl":"ltr";
     radio.addEventListener("change",()=>{selection=index;submit.disabled=false;save();});label.append(radio,copy);fieldset.append(label);
   });
   form.append(fieldset,submit);form.addEventListener("submit",event=>{event.preventDefault();choose();});choices.append(form);
   $("vocab-back").disabled=Boolean(pending);set("vocab-fallback",current.untranslated&&language()!=="en"?tr("fallback"):lessonLang!==language()?ui("translationUnavailable"):"");
   save();focus(prompt);
   if(receipt)renderFeedback(receipt.result);
   else if(pending)message(ui("unknown"),sendPending,"vocab-feedback");
 }
 function renderFeedback(result){
   const panel=$("vocab-feedback");panel.replaceChildren();panel.hidden=false;panel.className="feedback "+(result.correct?"good":"bad");panel.setAttribute("role","status");panel.setAttribute("aria-live","polite");
   const heading=node("h3",ui(result.correct?"correct":result.unverified?"unverified":"wrong"));heading.id="vocab-result-heading";panel.append(heading);
   const at=current.choices.indexOf(result.answer),answer=current.direction==="gr-target"?englishHint(result.answer,current.choicesEn?.[at]):result.answer;
   if(!result.correct){const line=node("p",ui("correction")+": "+answer);line.dir="auto";panel.append(line);}
   for(const key of ["explanation","orthographyNote"]){if(result[key])panel.append(node("p",result[key]));}
   if(result.greekVariants?.length){const line=node("p",ui("alternatives")+": "+result.greekVariants.join(" / "));line.dir="auto";panel.append(line);}
   panel.append(node("p",ui("finalAnswer"),"quiet"));
   $("vocab-choices").querySelectorAll("input,button").forEach(control=>control.disabled=true);
   $("vocab-choices").querySelectorAll(".lesson-choice").forEach((label,index)=>{
     if((result.acceptedAnswers||[result.answer]).includes(current.choices[index]))label.classList.add("is-correct");
     if(index===selection&&!result.correct)label.classList.add("is-wrong");
   });
   set("vocab-next",pos===words.length-1?tr("done"):tr("next"));show("vocab-next",true);
   $("vocab-next").setAttribute("aria-describedby","vocab-result-heading");$("vocab-back").disabled=false;focus($("vocab-next"));
 }
 async function choose(){
   if(busy||!current||receipt)return;
   if(!pending){
     if(selection===null)return;
     pending={owner:window.LexiApp?.accountKey(),body:{id:current.id,lang:lessonLang,direction:current.direction,selected:current.choices[selection],requestId:uuid()},pos};
     save();
   }
   return sendPending();
 }
 async function sendPending(){
   if(busy||!pending)return;busy=true;const generation=ownerGeneration;const submission=pending;
   $("vocab-choices").querySelectorAll("input,button").forEach(control=>control.disabled=true);$("vocab-back").disabled=true;
   message(ui("saving"),null,"vocab-feedback");
   try{
     const result=await api("vocab/answer",{method:"POST",headers:{"Content-Type":"application/json","X-Lexi-Owner":submission.owner},body:JSON.stringify(submission.body)});
     if(!receipt||receipt.requestId!==submission.body.requestId){if(result.correct)correct++;else wrong++;}
     receipt={requestId:submission.body.requestId,result};pending=null;save();
     if(visible())renderFeedback(result);
     document.dispatchEvent(new CustomEvent("lexi:progress"));
   }catch(error){failure(error,sendPending,"vocab-feedback");}
   finally{if(generation===ownerGeneration)busy=false;}
 }
 function done(){
   window.LexiWordAudio?.stop();show("vocab-card",false);show("vocab-word-preview",false);show("vocab-summary",true);show("vocab-controls",false);show("vocab-lesson",true);
   set("vocab-complete",tr("done")+" · "+ui("correct")+": "+correct+" / "+words.length+" · "+ui("errors")+": "+wrong);save();focus($("vocab-complete"));
   document.dispatchEvent(new CustomEvent("lexi:progress"));
 }
 function next(){if(!receipt||busy)return;pos++;receipt=null;selection=null;pending=null;renderCard();}
 function back(){
   if(pending||busy)return;window.LexiWordAudio?.stop();words=[];current=null;receipt=null;selection=null;save();
   show("vocab-lesson",false);show("vocab-controls",true);show("vocab-word-preview",false);show("vocab-card",false);show("vocab-summary",false);loadMeta();focus($("vocab-title"));
 }
 async function onOpen(){
   if(window.LexiApp?.loggedIn()===false)return;restore();
   if(!meta)await loadMeta();else renderMeta();
   if(words.length){if(preview)renderPreview();else renderCard();}
 }
 function onLanguageChange(){
   if(meta)renderMeta();if(words.length&&visible()){if(preview)renderPreview();else renderCard();}
 }
 window.lexiVocab={onOpen,onLanguageChange,onLeave:()=>{window.LexiWordAudio?.stop();save();}};
 document.addEventListener("lexi:logout",()=>{
   ownerGeneration++;busy=false;words=[];pending=null;receipt=null;current=null;loadedOwner=null;meta=null;
   for(const id of ["vocab-new","vocab-review"])$(id).disabled=false;
   $("vocab-progress").replaceChildren();
 });
 document.addEventListener("visibilitychange",()=>{if(document.hidden)window.LexiWordAudio?.stop();});
 $("vocab-new").addEventListener("click",()=>loadLesson(false));
 $("vocab-review").addEventListener("click",()=>loadLesson(true));
 $("vocab-begin").addEventListener("click",renderCard);
 $("vocab-pronounce").addEventListener("click",()=>playWord(current));
 $("vocab-pronounce-slow").addEventListener("click",()=>playWord(current,{slow:true}));
 $("vocab-next").addEventListener("click",next);
 $("vocab-back").addEventListener("click",back);
 $("vocab-again").addEventListener("click",()=>loadLesson(false));
})();
