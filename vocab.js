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
 let meta=null,words=[],pos=0,review=false,busy=false,correct=0,wrong=0,current=null;
 const englishHint=(value,en)=>$("lang").value!=="en"&&en&&value.trim().toLocaleLowerCase()!==en.trim().toLocaleLowerCase()?value+" ("+en+")":value;
 const tr=key=>(terms[$("lang").value]||terms.en)[key]||terms.en[key];
 const api=async(path,opts)=>{const res=await fetch("/greek/api/"+path,{credentials:"same-origin",cache:"no-store",...opts});if(!res.ok)throw Error("HTTP "+res.status);return res.json();};
 const set=(id,s)=>{$(id).textContent=s;};
 const show=(id,yes)=>{$(id).hidden=!yes;};
 function renderMeta(){
   if(!meta)return;
   set("vocab-title",tr("title"));set("vocab-subtitle",tr("subtitle"));set("vocab-topic-label",tr("theme"));
   set("vocab-level-label",tr("level"));set("vocab-new",tr("new"));set("vocab-review",tr("review"));
   set("vocab-source",tr("source")+" "+tr("coverage").replace("{count}",meta.offlineAudioWords??0));set("vocab-back",tr("back"));set("vocab-again",tr("again"));set("vocab-begin",tr("start"));
   const select=$("vocab-topic"),prev=select.value;
   select.replaceChildren();
   const topicLocales={
     zh:{everyday:"日常",shopping:"购物",road:"交通",home:"居家",food:"食物",family:"家庭",work:"工作",city:"城市",health:"健康",time:"时间",travel:"旅行",leisure:"休闲",nature:"自然"},
     ar:{everyday:"الحياة اليومية",shopping:"التسوق",road:"المواصلات",home:"المنزل",food:"الطعام",family:"العائلة",work:"العمل",city:"المدينة",health:"الصحة",time:"الوقت",travel:"السفر",leisure:"الترفيه",nature:"الطبيعة"},
     es:{everyday:"Vida cotidiana",shopping:"Compras",road:"Transporte",home:"Hogar",food:"Alimentación",family:"Familia",work:"Trabajo",city:"Ciudad",health:"Salud",time:"Tiempo",travel:"Viajes",leisure:"Ocio",nature:"Naturaleza"},
     pt:{everyday:"Dia a dia",shopping:"Compras",road:"Transportes",home:"Casa",food:"Alimentação",family:"Família",work:"Trabalho",city:"Cidade",health:"Saúde",time:"Tempo",travel:"Viagens",leisure:"Lazer",nature:"Natureza"}
   };
   const lang=$("lang").value;
   const allTopics={ru:"Все темы",en:"All topics",zh:"所有主题",ar:"كل المواضيع",es:"Todos los temas",pt:"Todos os temas"};
   const any=document.createElement("option");any.value="all";any.textContent=allTopics[lang]||allTopics.en;select.append(any);
   meta.topics.forEach(t=>{const o=document.createElement("option");o.value=t.id;o.textContent=(topicLocales[lang]?.[t.id]||(lang==="ru"?t.ru:t.en))+" · "+t.count;select.append(o);});
   if(Array.from(select.options).some(o=>o.value===prev))select.value=prev;
   set("vocab-total",meta.count+" · A1 "+meta.levels.A1+" / A2 "+meta.levels.A2);
 }
 async function loadMeta(){
   try{meta=await api("vocab/meta");renderMeta();}
   catch(err){set("vocab-message",tr("error")+err.message);}
 }
 function renderStats(data){
   set("vocab-progress",tr("learned")+": "+data.learned+"  ·  "+tr("remaining")+": "+data.remaining+"  ·  "+tr("weak")+": "+data.weak);
 }
 async function loadLesson(isReview){
   if(!meta)await loadMeta();
   review=isReview;show("vocab-message",false);
   const topic=$("vocab-topic").value||"all",level=$("vocab-level").value||"A1",lang=$("lang").value;
   for(const id of ["vocab-new","vocab-review"])$(id).disabled=true;
   try{
     const lesson=await api("vocab/lesson?"+new URLSearchParams({topic,level,lang,review:review?"1":"0"}));
     renderStats(lesson);words=lesson.words;pos=0;correct=0;wrong=0;
     if(!words.length){set("vocab-message",review?tr("noWeak"):tr("empty"));show("vocab-message",true);show("vocab-lesson",false);return;}
     show("vocab-controls",false);show("vocab-lesson",true);show("vocab-word-preview",!review);
     show("vocab-card",review);show("vocab-summary",false);
     if(!review){
       set("vocab-preview-audio-status","");
       set("vocab-preview-heading",tr("preview"));
       const list=$("vocab-preview-list");list.replaceChildren();
       words.forEach(w=>{
         const row=document.createElement("div");row.className="topic-study-row";
         const gr=document.createElement("strong");gr.lang="el";gr.dir="ltr";
         gr.textContent=[w.gr,...(w.greekVariants||[])].join(" / ");
         const ar=document.createElement("span");ar.textContent=w.translation;
         if(lang==="ar")ar.dir=w.untranslated?"ltr":"rtl";
         const meta=document.createElement("small");meta.textContent=w.level+(w.untranslated?" · EN":"");
         const sound=document.createElement("button");sound.type="button";sound.className="vocab-audio-btn";
         const ready=window.LexiWordAudio?.available(w.wordAudio)??false;
         sound.disabled=!ready;
         sound.textContent=ready?"🔊":"🔇";
         sound.title=ready?tr("previewPlay"):tr("unavailable");
         sound.setAttribute("aria-label",sound.title);
         sound.addEventListener("click",()=>playWord(w,{statusId:"vocab-preview-audio-status"}));
         row.append(gr,ar,meta,sound);list.append(row);
       });
       set("vocab-begin",tr("start"));
     }else renderCard();
   }catch(err){set("vocab-message",tr("error")+err.message);show("vocab-message",true);}
   finally{for(const id of ["vocab-new","vocab-review"])$(id).disabled=false;}
 }
 function button(choice,index){
   const b=document.createElement("button");b.type="button";b.className="answer";
   const n=document.createElement("span");n.className="key";n.textContent=String(index+1);
   const label=document.createElement("span");
   label.textContent=current.direction==="gr-target"?englishHint(choice,current.choicesEn?.[index]):choice;
   if($("lang").value==="ar"&&current.direction==="gr-target")label.dir=current.untranslated?"ltr":"rtl";
   b.append(n,label);b.addEventListener("click",()=>choose(index));return b;
 }
 function renderCard(){
   window.LexiWordAudio?.stop();
   current=words[pos];busy=false;
   set("vocab-audio-status","");
   set("vocab-pronounce",tr("play"));
   set("vocab-pronounce-slow",tr("slow"));
   const ready=window.LexiWordAudio?.available(current?.wordAudio)??false;
   $("vocab-pronounce").disabled=!ready;
   $("vocab-pronounce-slow").disabled=!ready;
   if(!current){done();return;}
   if(!ready)set("vocab-audio-status",tr("unavailable"));
   show("vocab-word-preview",false);show("vocab-card",true);
   show("vocab-feedback",false);show("vocab-next",false);
   set("vocab-question-count",(pos+1)+" / "+words.length);set("vocab-card-heading",tr("lesson"));
   set("vocab-prompt",current.direction==="gr-target"
     ?[current.gr,...(current.greekVariants||[])].join(" / ")
     :englishHint(current.translation,current.english));
   $("vocab-prompt").lang=current.direction==="gr-target"?"el":$("lang").value;
   $("vocab-prompt").dir=current.direction==="gr-target"?"ltr":$("lang").value==="ar"&&!current.untranslated?"rtl":"ltr";
   set("vocab-direction",current.direction==="gr-target"?"Ελληνικά → ?":"? → Ελληνικά");
   const choices=$("vocab-choices");choices.replaceChildren();
   current.choices.forEach((answer,i)=>choices.append(button(answer,i)));
   choices.classList.toggle("wide-choices",current.choices.some(x=>x.length>35));
   set("vocab-fallback",current.untranslated&&$("lang").value!=="en"?tr("fallback"):"");
 }
 async function choose(i){
   if(busy||!current)return;
   busy=true;
   const buttons=Array.from($("vocab-choices").children);buttons.forEach(b=>b.disabled=true);
   const selected=current.choices[i];
   try{
    const result=await api("vocab/answer",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({id:current.id,lang:$("lang").value,direction:current.direction,selected})});
    if(result.correct)correct++;else wrong++;
    buttons.forEach((b,j)=>{if((result.acceptedAnswers||[result.answer]).includes(current.choices[j]))b.classList.add("is-correct");if(j===i&&!result.correct)b.classList.add("is-wrong");});
    $("vocab-feedback").className="feedback "+(result.correct?"good":"bad");
    const at=current.choices.indexOf(result.answer);
    const display=current.direction==="gr-target"?englishHint(result.answer,current.choicesEn?.[at]):result.answer;
    const variantLabel={ru:"Также употребляют",en:"Also used",zh:"另一种常见形式",
      ar:"تُستعمل أيضاً",es:"También se utiliza",pt:"Também se usa"}[$("lang").value]||"Also used";
    const variantText=result.greekVariants?.length?" · "+variantLabel+": "+result.greekVariants.join(" / "):"";
    set("vocab-feedback",(result.correct?tr("correct"):tr("wrong")+display)+variantText);
    show("vocab-feedback",true);set("vocab-next",pos===words.length-1?tr("done"):tr("next"));show("vocab-next",true);
   }catch(err){set("vocab-feedback",tr("error")+err.message);show("vocab-feedback",true);buttons.forEach(b=>b.disabled=false);busy=false;}
 }
 function done(){
   window.LexiWordAudio?.stop();
   show("vocab-card",false);show("vocab-summary",true);
   set("vocab-complete",tr("done")+" · "+correct+"/"+words.length+"  ✓  "+wrong+"  ✕");
 }
 function next(){pos++;renderCard();}
 function back(){
   window.LexiWordAudio?.stop();
   show("vocab-lesson",false);show("vocab-controls",true);show("vocab-word-preview",false);show("vocab-card",false);
   show("vocab-summary",false);loadMeta();
 }
 async function onOpen(){
   if(!meta)await loadMeta();
   else renderMeta();
 }
 function onLanguageChange(){if(meta)renderMeta();if(words.length&&!$("vocab-lesson").hidden){words=[];back();}}
 window.lexiVocab={onOpen,onLanguageChange};
 $("vocab-new").addEventListener("click",()=>loadLesson(false));
 $("vocab-review").addEventListener("click",()=>loadLesson(true));
 $("vocab-begin").addEventListener("click",renderCard);
 $("vocab-pronounce").addEventListener("click",()=>playWord(current));
 $("vocab-pronounce-slow").addEventListener("click",()=>playWord(current,{slow:true}));
 $("vocab-next").addEventListener("click",next);
 $("vocab-back").addEventListener("click",back);
 $("vocab-again").addEventListener("click",()=>loadLesson(false));
})();
