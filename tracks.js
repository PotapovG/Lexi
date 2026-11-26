"use strict";
(() => {
  const $=id=>document.getElementById(id);
  const COPY={
  "title": [
    "Карточки слов",
    "Word flashcards",
    "单词卡片",
    "بطاقات الكلمات",
    "Tarjetas de palabras",
    "Cartões de palavras"
  ],
  "desc": [
    "Повторяйте слова блоками по 30. Прогресс сохраняется в аккаунте.",
    "Practise words in batches of 30. Your account keeps your progress.",
    "每组练习30个词，进度保存在账户中。",
    "تدرّب على مجموعات من 30 كلمة. يُحفظ تقدمك في حسابك.",
    "Practica en grupos de 30 palabras. El progreso se guarda en tu cuenta.",
    "Pratica grupos de 30 palavras. O progresso fica guardado na tua conta."
  ],
  "anki": [
    "30 слов",
    "30 words",
    "30个词",
    "30 كلمة",
    "30 palabras",
    "30 palavras"
  ],
  "route": [
    "Маршруты",
    "Routes",
    "路线",
    "المسارات",
    "Rutas",
    "Percursos"
  ],
  "likes": [
    "Нравится / не нравится",
    "Like / dislike",
    "喜欢 / 不喜欢",
    "أحب / لا أحب",
    "Gustos y preferencias",
    "Gostos e preferências"
  ],
  "periptero": [
    "Покупки",
    "Shopping",
    "购物",
    "التسوق",
    "Compras",
    "Compras"
  ],
  "preview": [
    "Знакомство со словом",
    "Study the word",
    "学习单词",
    "تعلّم الكلمة",
    "Estudia la palabra",
    "Estuda a palavra"
  ],
  "next": [
    "Следующая карточка",
    "Next card",
    "下一张卡片",
    "البطاقة التالية",
    "Siguiente tarjeta",
    "Cartão seguinte"
  ],
  "study": [
    "Запомните слово и значение",
    "Remember the word and meaning",
    "记住单词和词义",
    "احفظ الكلمة ومعناها",
    "Recuerda la palabra y su significado",
    "Memoriza a palavra e o significado"
  ],
  "test": [
    "Выберите перевод",
    "Choose the translation",
    "选择译文",
    "اختر الترجمة",
    "Elige la traducción",
    "Escolhe a tradução"
  ],
  "known": [
    "Слов закреплено в этом упражнении",
    "Words completed in this activity",
    "本练习已完成词数",
    "الكلمات المكتملة في هذا النشاط",
    "Palabras completadas en esta actividad",
    "Palavras concluídas nesta atividade"
  ],
  "retry": [
    "Ответов с ошибками",
    "Incorrect answers",
    "答错次数",
    "الإجابات غير الصحيحة",
    "Respuestas incorrectas",
    "Respostas incorretas"
  ],
  "milestone": [
    "Блок завершён",
    "Batch completed",
    "本组已完成",
    "اكتملت المجموعة",
    "Grupo completado",
    "Grupo concluído"
  ],
  "continue": [
    "Продолжить",
    "Continue",
    "继续",
    "متابعة",
    "Continuar",
    "Continuar"
  ],
  "correct": [
    "Верно",
    "Correct",
    "正确",
    "صحيح",
    "Correcto",
    "Certo"
  ],
  "wrong": [
    "Ошибка. Правильный ответ:",
    "Incorrect. Answer:",
    "错误。正确答案：",
    "خطأ. الإجابة الصحيحة:",
    "Incorrecto. Respuesta:",
    "Incorreto. Resposta:"
  ],
  "review": [
    "Проверка памяти",
    "Recall practice",
    "回忆练习",
    "تدريب التذكر",
    "Práctica de memoria",
    "Prática de memória"
  ],
  "done": [
    "Пройдено слов",
    "Words completed",
    "已完成单词",
    "الكلمات المكتملة",
    "Palabras completadas",
    "Palavras concluídas"
  ],
  "finished": [
    "Все доступные слова пройдены",
    "All available words completed",
    "已完成所有可用单词",
    "اكتملت كل الكلمات المتاحة",
    "Has completado todas las palabras disponibles",
    "Concluíste todas as palavras disponíveis"
  ],
  "routeTitle": [
    "Опишите маршрут по-гречески",
    "Describe a route in Greek",
    "用希腊语描述路线",
    "صِف مساراً باليونانية",
    "Describe una ruta en griego",
    "Descreve um percurso em grego"
  ],
  "routeHelp": [
    "Введите ответы по-гречески. Названия мест есть на карте; выберите нужные предлоги и формы.",
    "Type in Greek. Places are on the map; choose the articles and prepositions.",
    "用希腊语输入。地图已给出地名；请选用合适的冠词和介词。",
    "اكتب باليونانية. تظهر الأماكن على الخريطة؛ اختر أدوات التعريف وحروف الجر.",
    "Escribe en griego. Los lugares están en el mapa; elige artículos y preposiciones.",
    "Escreve em grego. Os locais estão no mapa; escolhe os artigos e as preposições."
  ],
  "routeComplete": [
    "Маршрут описан верно",
    "Route described correctly",
    "路线描述正确",
    "وُصف المسار بشكل صحيح",
    "Ruta descrita correctamente",
    "Percurso descrito corretamente"
  ],
  "routeWrong": [
    "Проверьте отмеченные поля",
    "Check the highlighted fields",
    "检查标出的内容",
    "راجع الحقول المحددة",
    "Revisa los campos señalados",
    "Revê os campos assinalados"
  ],
  "check": [
    "Проверить маршрут",
    "Check route",
    "检查路线",
    "تحقق من المسار",
    "Comprobar ruta",
    "Verificar percurso"
  ],
  "nextRoute": [
    "Следующий маршрут",
    "Next route",
    "下一条路线",
    "المسار التالي",
    "Siguiente ruta",
    "Percurso seguinte"
  ],
  "routeLesson": [
    "Глава 6 · Передвижение",
    "Chapter 6 · Getting around",
    "第6章 · 出行",
    "الفصل 6 · التنقل",
    "Capítulo 6 · Desplazamientos",
    "Capítulo 6 · Deslocações"
  ],
  "number": [
    "Номер автобуса словами",
    "Bus number in words",
    "用单词写出公交车号",
    "رقم الحافلة بالكلمات",
    "Número de autobús en palabras",
    "Número do autocarro por extenso"
  ],
  "origin": [
    "Откуда отправляется?",
    "Where does it start?",
    "从哪里出发？",
    "من أين تنطلق؟",
    "¿De dónde sale?",
    "De onde parte?"
  ],
  "via1": [
    "Что проезжает сначала?",
    "First landmark passed",
    "先经过哪里？",
    "ما أول معلم تمر به؟",
    "Primer lugar por el que pasa",
    "Primeiro local por onde passa"
  ],
  "via2": [
    "Что проезжает затем?",
    "Next landmark passed",
    "然后经过哪里？",
    "ما المعلم التالي؟",
    "Siguiente lugar por el que pasa",
    "Local seguinte por onde passa"
  ],
  "stop": [
    "Где останавливается?",
    "Where does it stop?",
    "在哪里停靠？",
    "أين تتوقف؟",
    "¿Dónde para?",
    "Onde para?"
  ],
  "destination": [
    "Куда направляется?",
    "Where does it go?",
    "开往哪里？",
    "إلى أين تتجه؟",
    "¿Adónde va?",
    "Para onde vai?"
  ],
  "answer": [
    "Правильный вариант",
    "Correct wording",
    "正确表达",
    "الصياغة الصحيحة",
    "Forma correcta",
    "Forma correta"
  ],
  "likeTitle": [
    "Нравится / не нравится",
    "Like / dislike",
    "喜欢 / 不喜欢",
    "أحب / لا أحب",
    "Gustos y preferencias",
    "Gostos e preferências"
  ],
  "likeHelp": [
    "Напишите полную греческую фразу с нужной формой αρέσει и глагола.",
    "Write the complete Greek phrase with the appropriate form of αρέσει and the verb.",
    "用合适的 αρέσει 及动词形式写出完整希腊语句子。",
    "اكتب العبارة اليونانية كاملة باستخدام الصيغة المناسبة من αρέσει والفعل.",
    "Escribe la frase completa en griego con las formas adecuadas de αρέσει y del verbo.",
    "Escreve a frase completa em grego com as formas adequadas de αρέσει e do verbo."
  ],
  "likeAction": [
    "Проверить фразу",
    "Check phrase",
    "检查句子",
    "تحقق من العبارة",
    "Comprobar frase",
    "Verificar frase"
  ],
  "shopTitle": [
    "Περίπτερο · покупки",
    "Περίπτερο · shopping",
    "Περίπτερο · 购物",
    "Περίπτερο · التسوق",
    "Περίπτερο · compras",
    "Περίπτερο · compras"
  ],
  "shopHelp": [
    "Попросите товар с нужным количеством по-гречески (Θα ήθελα…, Μπορώ να έχω…).",
    "Ask for the item and quantity in Greek (Θα ήθελα…, Μπορώ να έχω…).",
    "用希腊语说出商品及数量（Θα ήθελα…, Μπορώ να έχω…）。",
    "اطلب السلعة والكمية باليونانية (Θα ήθελα…, Μπορώ να έχω…).",
    "Pide el producto y la cantidad en griego (Θα ήθελα…, Μπορώ να έχω…).",
    "Pede o produto e a quantidade em grego (Θα ήθελα…, Μπορώ να έχω…)."
  ],
  "shopEarlyHelp": [
    "Попросите товар и количество с изученной формой «Θέλω…».",
    "Request the item and quantity with the studied form «Θέλω…».",
    "使用学过的 «Θέλω…» 说出所需商品和数量。",
    "اطلب السلعة والكمية باستخدام الصيغة التي تعلمتها «Θέλω…».",
    "Pide el producto y la cantidad con la forma estudiada «Θέλω…».",
    "Pede o produto e a quantidade com a forma estudada «Θέλω…»."
  ],
  "buy": [
    "Добавить в корзину",
    "Add to basket",
    "放入购物篮",
    "أضف إلى السلة",
    "Añadir a la cesta",
    "Adicionar ao cesto"
  ],
  "basket": [
    "В корзине",
    "In the basket",
    "购物篮",
    "في السلة",
    "En la cesta",
    "No cesto"
  ],
  "nextBasket": [
    "Следующий список",
    "Next shopping list",
    "下一个购物清单",
    "قائمة التسوق التالية",
    "Siguiente lista",
    "Lista seguinte"
  ],
  "shopComplete": [
    "Все четыре покупки собраны",
    "All four items collected",
    "已买齐四件商品",
    "جُمعت السلع الأربع",
    "Has conseguido los cuatro productos",
    "Conseguiste os quatro produtos"
  ],
  "shopPlaceholder": [
    "Θέλω …, παρακαλώ.",
    "Θέλω …, παρακαλώ.",
    "Θέλω …, παρακαλώ.",
    "Θέλω …, παρακαλώ.",
    "Θέλω …, παρακαλώ.",
    "Θέλω …, παρακαλώ."
  ],
  "shopLabel": [
    "Как попросите этот товар?",
    "How would you ask for this item?",
    "你会如何购买这件商品？",
    "كيف تطلب هذه السلعة؟",
    "¿Cómo pedirías este producto?",
    "Como pedirias este produto?"
  ],
  "network": [
    "Не удалось загрузить занятие",
    "Could not load the activity",
    "无法加载练习",
    "تعذّر تحميل النشاط",
    "No se pudo cargar la actividad",
    "Não foi possível carregar a atividade"
  ],
  "saved": [
    "Прогресс сохраняется в аккаунте.",
    "Progress is saved to your account.",
    "进度保存在账户中。",
    "يُحفظ التقدم في حسابك.",
    "El progreso se guarda en tu cuenta.",
    "O progresso fica guardado na tua conta."
  ],
  "verb": [
    "Глагол",
    "Verb",
    "动词",
    "الفعل",
    "Verbo",
    "Verbo"
  ]
};
  const UI=Object.fromEntries(["ru","en","zh","ar","es","pt"].map((locale,index)=>[locale,Object.fromEntries(Object.entries(COPY).map(([key,row])=>[key,row[index]]))]));
  const AUDIO={
    ru:{play:"🔊 Послушать",slow:"0,8× Медленно",unavailable:"Запись для этого слова ещё не готова.",pocket:"Воспроизводится Pocket TTS.",done:"Прослушано.",error:"Не удалось воспроизвести запись."},
    en:{play:"🔊 Listen",slow:"0.8× Slower",unavailable:"This word has no recording yet.",pocket:"Playing Pocket TTS recording.",done:"Finished.",error:"Could not play the audio."},
    zh:{play:"🔊 听发音",slow:"0.8× 慢速",unavailable:"该词还没有录音。",pocket:"正在播放 Pocket TTS 录音。",done:"播放结束。",error:"无法播放录音。"},
    ar:{play:"🔊 استمع",slow:"0.8× ببطء",unavailable:"لا يتوفر تسجيل لهذه الكلمة بعد.",pocket:"تشغيل تسجيل Pocket TTS.",done:"انتهى.",error:"تعذّر تشغيل التسجيل."},
    es:{play:"🔊 Escuchar",slow:"0,8× Más lento",unavailable:"Aún no hay grabación de esta palabra.",pocket:"Reproduciendo Pocket TTS.",done:"Finalizado.",error:"No se pudo reproducir."},
    pt:{play:"🔊 Ouvir",slow:"0,8× Devagar",unavailable:"Ainda não há gravação desta palavra.",pocket:"A reproduzir Pocket TTS.",done:"Terminou.",error:"Não foi possível reproduzir."}
  };
  const audioText=key=>(AUDIO[lang()]||AUDIO.en)[key]||AUDIO.en[key]||key;
  function renderAnkiAudio(panel,card){
    const meta=card?.wordAudio;
    const status=text("p","","track-audio-status");
    status.setAttribute("role","status");
    status.setAttribute("aria-live","polite");
    const controls=document.createElement("div");
    controls.className="track-audio-controls";
    const available=window.LexiWordAudio?.available(meta)===true;
    if(!available){
      status.textContent=audioText("unavailable");
    }else{
      for(const slow of [false,true]){
        const b=control(audioText(slow?"slow":"play"),async()=>{
          if(anki?.card?.id!==card.id)return;
          await window.LexiWordAudio.play(meta,{slow,onStatus:state=>{
            if(anki?.card?.id===card.id&&$("tracks-view")&&!$("tracks-view").hidden)
              status.textContent=audioText(state);
          }});
        },"secondary");
        b.classList.add("track-audio-button");
        b.setAttribute("aria-label",(slow?audioText("slow"):audioText("play"))+" · "+card.gr);
        controls.append(b);
      }
    }
    const wrap=document.createElement("div");
    wrap.className="track-audio-block";
    wrap.append(controls,status);
    panel.append(wrap);
  }
  const labels={number:"Το λεωφορείο",origin:"Ξεκινάει από",via1:"Περνάει από",via2:"Μετά περνάει από",
    stop:"Σταματάει στη στάση",destination:"Πηγαίνει προς"};
  let mode="anki",anki=null,route=null,likes=null,shop=null,busy=false,language=null,ownerGeneration=0;
  const lang=()=>$("lang")?.value||"ru";
  const t=key=>(UI[lang()]||UI.en)[key]||UI.en[key]||key;
  const text=(tag,value,cls)=>{
    const n=document.createElement(tag);if(cls)n.className=cls;
    n.textContent=String(value);return n;
  };
  const control=(title,callback,variant="secondary")=>{
    const b=document.createElement("button");
    b.type="button";b.className=variant+" track-button";b.textContent=title;
    b.addEventListener("click",callback);return b;
  };
  async function request(part,body){
    const owner=window.LexiApp?.accountKey();
    if(body&&(!window.LexiApp?.loggedIn()||!owner))throw Error("account_changed");
    const response=await fetch("/greek/api/tracks/"+part+(body?"":"?lang="+encodeURIComponent(lang())),{
      method:body?"POST":"GET",credentials:"same-origin",cache:"no-store",
      ...(body?{headers:{"Content-Type":"application/json","X-Lexi-Owner":owner},body:JSON.stringify({...body,lang:lang()})}:{})});
    const data=await response.json().catch(()=>({}));
    if(owner!==window.LexiApp?.accountKey())throw Error("account_changed");
    if(!response.ok){if(data.error==="account_changed")window.LexiApp?.reconcileAccount?.();throw new Error(data.error||String(response.status));}
    return data;
  }
  function message(msg,bad=false){
    const el=$(mode==="anki"?"track-message":"life-message");if(!el)return;
    el.hidden=!msg;el.textContent=msg||"";el.className="track-message"+(bad?" bad":"");
  }
  async function reload(){
    if(!$(mode==="anki"?"tracks-view":"life-view")||$(mode==="anki"?"tracks-view":"life-view").hidden)return;
    if(busy)return;
    const content=$(mode==="anki"?"track-content":"life-content");
    const drafts=language&&language!==lang()?Array.from(content.querySelectorAll('input[type="text"],textarea')).map(el=>el.value):null;
    language=lang();
    $("track-title").textContent=t("title");
    $("track-description").textContent=t("desc");
    $("track-anki-mode").textContent=t("anki");
    $("track-route-mode").textContent=t("route");
    $("track-likes-mode").textContent=t("likes");
    $("track-periptero-mode").textContent=t("periptero");
    for(const name of ("anki route likes periptero").split(" "))
      $("track-"+name+"-mode").classList.toggle("active",mode===name);
    message("");
    busy=true;const generation=ownerGeneration;
    try{
      if(mode==="anki"){anki=await request("anki");renderAnki();}
      else if(mode==="route"){route=await request("route");renderRoute();}
      else if(mode==="likes"){likes=await request("likes");renderLikes();}
      else {shop=await request("periptero");renderShop();}
      if(drafts)Array.from(content.querySelectorAll('input[type="text"],textarea')).forEach((el,index)=>{if(drafts[index]!==undefined)el.value=drafts[index];});
    }catch(err){if(generation===ownerGeneration&&err.message!=="account_changed")message(t("network")+": "+err.message,true);}
    finally{if(generation===ownerGeneration)busy=false;}
  }
  async function action(part,body,callback){
    if(busy)return;
    busy=true;const generation=ownerGeneration;message("");
    try{
      const response=await request(part,body);
      callback(response);
    }catch(err){
      if(err.message==="account_changed")return;
      if(err.message==="stale_track"){
        message(t("saved"));
        busy=false;await reload();return;
      }
      message(t("network")+": "+err.message,true);
    }finally{if(generation===ownerGeneration)busy=false;}
  }
  function ankiHeader(root){
    const summary=text("div",anki.phase==="review"?t("review"):anki.phase==="preview"?t("study"):t("test"),"track-eyebrow");
    root.append(summary);
    root.append(text("p",t("known")+": "+anki.learned+" · "+t("retry")+": "+anki.misses,"track-meta"));
  }
  function renderAnki(){
    window.LexiWordAudio?.stop();
    const root=$("track-content");root.replaceChildren();ankiHeader(root);
    const panel=document.createElement("div");panel.className="track-word-card";root.append(panel);
    if(anki.phase==="preview"){
      panel.append(text("div",t("preview")+" · "+anki.at+"/"+anki.cohortSize,"track-small"));
      panel.append(text("h3",anki.card.gr,"track-greek"));
      renderAnkiAudio(panel,anki.card);
      panel.append(text("p",anki.card.translation,"track-meaning"));
      panel.append(text("p",t("study"),"track-small"));
      panel.append(control(t("next"),()=>action("anki",{action:"advance",revision:anki.revision},
        data=>{anki=data;renderAnki();}),"primary"));
    }else if(anki.phase==="quiz"||anki.phase==="review"){
      panel.append(text("div",(anki.phase==="review"?t("review"):t("test"))+" · "+anki.done+"/"+anki.target,"track-small"));
      panel.append(text("h3",anki.card.gr,"track-greek"));
      renderAnkiAudio(panel,anki.card);
      const options=document.createElement("div");options.className="track-choices";panel.append(options);
      const form=document.createElement("form"),fieldset=document.createElement("fieldset");
      fieldset.className="lesson-option-grid";const legend=text("legend",t("test"),"sr-only");fieldset.append(legend);let selected=null;
      const check=control(window.LexiUI.t("check"),()=>{},"primary");check.type="submit";check.disabled=true;
      anki.options.forEach(value=>{
        const label=document.createElement("label");label.className="lesson-option";
        const input=document.createElement("input");input.type="radio";input.name="track-answer";
        const copy=text("span",value);copy.dir=lang()==="ar"?"rtl":"ltr";
        input.addEventListener("change",()=>{selected=value;check.disabled=false;});label.append(input,copy);fieldset.append(label);
      });
      form.append(fieldset,check);options.append(form);
      form.addEventListener("submit",event=>{
        event.preventDefault();if(busy||selected===null)return;check.disabled=true;
        action("anki",{action:"answer",revision:anki.revision,cardId:anki.card.id,selected},data=>{
          anki=data;form.querySelectorAll("input,button").forEach(el=>el.disabled=true);
          const feedback=text("p",data.feedback.correct?t("correct"):t("wrong")+" "+data.feedback.translation,data.feedback.correct?"track-success":"track-error");
          feedback.id="track-result";feedback.setAttribute("role","status");panel.append(feedback);
          const next=control(t("continue"),()=>renderAnki(),"primary");next.setAttribute("aria-describedby","track-result");panel.append(next);next.focus({preventScroll:true});
          document.dispatchEvent(new CustomEvent("lexi:progress"));
        }).finally(()=>{if(!busy&&form.isConnected&&!form.querySelector("input").disabled)check.disabled=false;});
      });
    }else if(anki.phase==="milestone"){
      panel.append(text("h3",t("milestone"),"track-greek"));
      panel.append(text("p",t("done")+": "+anki.learned,"track-meaning"));
      panel.append(control(t("continue"),()=>action("anki",{action:"continue",revision:anki.revision},
        data=>{anki=data;renderAnki();}),"primary"));
    }else{
      panel.append(text("h3",t("finished"),"track-greek"));
      panel.append(text("p",t("done")+": "+anki.learned,"track-meaning"));
    }
    root.append(text("p",t("saved"),"track-small"));
    const heading=root.querySelector("h3");if(heading){heading.lang=anki.card?"el":lang();heading.dir=heading.lang==="ar"?"rtl":"ltr";heading.tabIndex=-1;heading.focus({preventScroll:true});}
  }
  function routeSVG(scene){
    const host=document.createElement("div");host.className="route-map";
    const NS="http://www.w3.org/2000/svg",el=(tag,attrs)=>{
      const n=document.createElementNS(NS,tag);
      for(const [key,value] of Object.entries(attrs))n.setAttribute(key,String(value));
      return n;
    };
    const svg=el("svg",{viewBox:"0 0 610 185",width:"610",height:"185",role:"img",
      "aria-label":t("route")+" "+scene.bus});
    const path=el("path",{d:"M50 84 H558",stroke:"#78b5db","stroke-width":"7",
      "stroke-linecap":"round",fill:"none"});
    svg.append(path);
    const arrow=el("path",{d:"M550 72 L568 84 L550 96",stroke:"#e4bc71",
      "stroke-width":"4",fill:"none","stroke-linecap":"round"});svg.append(arrow);
    scene.stops.forEach((stop,i)=>{
      const x=51+i*124;
      const circle=el("circle",{cx:x,cy:84,r:i===3?13:10,fill:"#12273b",
        stroke:i===3?"#e4bc71":"#99cde9","stroke-width":i===3?4:3});
      svg.append(circle);
      const title=el("text",{x,y:53,"text-anchor":"middle",
        "font-size":stop.name.length>13?11:13,"font-weight":"600",fill:"#f1f3f8"});
      title.textContent=stop.name;svg.append(title);
      const gloss=el("text",{x,y:121,"text-anchor":"middle","font-size":11,fill:"#a3b7c9"});
      gloss.textContent=lang()==="ru"?stop.ru:stop.en;svg.append(gloss);
      const number=el("text",{x,y:151,"text-anchor":"middle","font-size":10,fill:"#7f95ac"});
      number.textContent=String(i+1);svg.append(number);
    });
    host.append(svg);return host;
  }
  function renderRoute(){
    const root=$("life-content");root.replaceChildren();
    if(window.LexiScenes){const scene=document.createElement("div");scene.className="life-activity-art";
      scene.append(window.LexiScenes.illustration("route"));root.append(scene);}
    root.append(text("div",t("routeLesson"),"track-eyebrow"));
    root.append(text("h3",t("routeTitle"),"track-subtitle"));
    if(!["ru","en"].includes(lang()))root.append(text("p",window.LexiUI.t("translationUnavailable"),"track-small"));
    root.append(text("p",t("routeHelp"),"track-small"));
    const badge=text("strong",route.bus,"route-bus");
    const bus=document.createElement("div");bus.className="route-bus-wrap";
    bus.append(text("span","🚌"),badge);root.append(bus);
    root.append(routeSVG(route));
    const form=document.createElement("form");form.className="route-answer-form";root.append(form);
    for(const key of route.fields){
      const field=document.createElement("label");field.className="route-field";
      field.append(text("span",t(key),"track-small"));
      const prefix=text("strong",labels[key],"route-prefix");prefix.lang="el";field.append(prefix);
      const input=document.createElement("input");input.type="text";input.name=key;
      input.lang="el";input.dir="ltr";input.autocomplete="off";input.maxLength=160;
      input.placeholder=key==="number"?"αριθμός με λέξεις":"...";
      field.append(input);form.append(field);
    }
    const feedback=document.createElement("div");feedback.className="track-route-feedback";feedback.setAttribute("role","status");feedback.setAttribute("aria-live","polite");
    const submit=document.createElement("button");
    submit.type="submit";submit.className="primary track-button";
    submit.textContent=t("check");form.append(submit);form.append(feedback);
    form.addEventListener("submit",event=>{
      event.preventDefault();if(busy)return;
      const answers=Object.fromEntries(route.fields.map(k=>[k,form.elements.namedItem(k).value]));
      submit.disabled=true;
      action("route",{revision:route.revision,answers},data=>{
        route=data;feedback.replaceChildren();
        const result=data.feedback;
        feedback.append(text("p",result.correct?t("routeComplete"):t("routeWrong"),
          result.correct?"track-success":"track-error"));
        for(const key of Object.keys(result.fields)){
          const input=form.elements.namedItem(key);
          input.classList.toggle("track-invalid",!result.fields[key]);
          if(!result.fields[key])
            feedback.append(text("p",t(key)+": "+result.expected[key]+
              (result.explanations?.[key]?" — "+result.explanations[key]:""),"track-error"));
        }
        feedback.append(text("p",result.greek,"track-greek-summary"));
        feedback.append(text("p",result.translation,"track-small"));
        if(result.correct){
          submit.hidden=true;
          feedback.append(control(t("continue"),()=>window.lexiLife?.advanceFromActivity?.(),"primary"));
        }else{
          submit.disabled=false;
        }
      });
      if(!busy)submit.disabled=false;
    });
  }

  function renderLikes(){
    const root=$("life-content");root.replaceChildren();
    if(window.LexiScenes){const scene=document.createElement("div");scene.className="life-activity-art";
      scene.append(window.LexiScenes.illustration("likes"));root.append(scene);}
    root.append(text("div","Γραμματική · A1/A2","track-eyebrow"));
    root.append(text("h3",t("likeTitle"),"track-subtitle"));
    root.append(text("p",t("likeHelp"),"track-small"));
    if(likes.completed){
      root.append(text("p",t("milestone")+" · "+likes.total+"/"+likes.total,"track-meaning"));
      root.append(control(t("continue"),()=>action("likes",{
        action:"restart",revision:likes.revision
      },data=>{likes=data;renderLikes();}),"primary"));return;
    }
    const box=document.createElement("div");box.className="track-word-card";root.append(box);
    box.append(text("div",likes.step+"/"+likes.total+" · "+t("retry")+": "+likes.misses,"track-small"));
    box.append(text("h3",likes.prompt,"track-meaning"));
    if(likes.promptLang!==lang())box.append(text("p",window.LexiUI.t("translationUnavailable"),"track-small"));
    box.append(text("p",t("verb")+": "+likes.lemma,"track-small"));
    const form=document.createElement("form");form.className="track-like-form";box.append(form);
    const input=document.createElement("input");input.type="text";input.lang="el";
    input.dir="ltr";input.maxLength=180;input.autocomplete="off";
    input.setAttribute("aria-label",window.LexiUI.t("typeGreek"));input.required=true;
    input.placeholder=likes.requiresNa?"… μου αρέσει να …":"… μου αρέσει …";
    form.append(input);
    const submit=document.createElement("button");
    submit.type="submit";submit.className="primary track-button";
    submit.textContent=t("likeAction");form.append(submit);
    const result=document.createElement("div");result.setAttribute("role","status");result.setAttribute("aria-live","polite");form.append(result);
    form.addEventListener("submit",event=>{
      event.preventDefault();if(busy)return;
      const answer=input.value;
      submit.disabled=true;
      action("likes",{action:"submit",revision:likes.revision,answer},data=>{
        likes=data;
        result.replaceChildren();
        result.append(text("p",data.feedback.correct?t("correct"):t("wrong"),
          data.feedback.correct?"track-success":"track-error"));
        if(data.feedback.explanation)result.append(text("p",data.feedback.explanation,"track-error"));
        result.append(text("p",data.feedback.expected,"track-greek-summary"));
        if(data.feedback.correct){
          input.disabled=true;submit.hidden=true;
          result.append(control(t("continue"),()=>window.lexiLife?.advanceFromActivity?.(),"primary"));
        }else submit.disabled=false;
      }).finally(()=>{if(!busy)submit.disabled=false;});
    });
  }
  function renderShop(){
    const root=$("life-content");root.replaceChildren();
    if(window.LexiScenes){const scene=document.createElement("div");scene.className="life-activity-art";
      scene.append(window.LexiScenes.illustration("periptero"));root.append(scene);}
    root.append(text("div","Περίπτερο · Μίνι μάρκετ","track-eyebrow"));
    root.append(text("h3",t("shopTitle")+" · "+shop.round,"track-subtitle"));
    const help=(shop.requestPrefix==="θέλω"
      ?t("shopEarlyHelp")
      :t("shopHelp"));
    root.append(text("p",help,"track-small"));
    if(!["ru","en"].includes(lang()))root.append(text("p",window.LexiUI.t("translationUnavailable"),"track-small"));
    const summary=text("p",t("basket")+": "+shop.bought.length+"/4","track-meta");
    root.append(summary);
    const list=document.createElement("div");list.className="shop-list";root.append(list);
    for(const item of shop.items){
      const row=document.createElement("div");row.className="shop-item";
      const already=shop.bought.includes(item.id);
      row.append(text("span",(already?"✓ ":item.icon+" ")+item.name,"track-item-title"));
      if(already){list.append(row);continue;}
      const form=document.createElement("form");form.className="shop-form";row.append(form);
      const input=document.createElement("input");input.type="text";input.lang="el";
      input.dir="ltr";input.maxLength=250;input.autocomplete="off";
      input.placeholder=(shop.requestPrefix||"Θέλω")+" …, παρακαλώ.";input.setAttribute("aria-label",t("shopLabel")+" "+item.name);
      form.append(input);
      const btn=document.createElement("button");
      btn.type="submit";btn.className="secondary track-button";
      btn.textContent=t("buy");form.append(btn);
      const note=document.createElement("div");note.setAttribute("role","status");note.setAttribute("aria-live","polite");form.append(note);
      form.addEventListener("submit",event=>{
        event.preventDefault();if(busy)return;btn.disabled=true;
        action("periptero",{action:"buy",revision:shop.revision,
          productId:item.id,phrase:input.value},data=>{
          shop=data;
          if(data.feedback.correct){renderShop();}
          else{
            note.replaceChildren();
            note.append(text("p",t("wrong")+" "+data.feedback.expected,"track-error"));
            if(data.feedback.explanation)note.append(text("p",data.feedback.explanation,"track-small"));
            btn.disabled=false;
          }
        }).finally(()=>{if(!busy)btn.disabled=false;});
      });
      list.append(row);
    }
    if(shop.stage==="complete"){
      root.append(text("p",t("shopComplete"),"track-success"));
      root.append(control(t("continue"),()=>action("periptero",{
        action:"next",revision:shop.revision
      },data=>{shop=data;window.lexiLife?.advanceFromActivity?.();}),"primary"));
    }
  }

  function switchMode(next){
    if(busy)return;
    mode=next;window.lexiLife?.showSimulation?.();reload();
  }
  $("track-anki-mode")?.addEventListener("click",()=>switchMode("anki"));
  $("track-route-mode")?.addEventListener("click",()=>switchMode("route"));
  $("track-likes-mode")?.addEventListener("click",()=>switchMode("likes"));
  $("track-periptero-mode")?.addEventListener("click",()=>switchMode("periptero"));
  document.addEventListener("lexi:logout",()=>{ownerGeneration++;busy=false;anki=null;route=null;likes=null;shop=null;language=null;});
  window.lexiTracks={
    onOpen:()=>{mode="anki";reload();},
    openLife:(selected)=>{mode=selected;reload();},
    onLanguageChange:reload,
    onLeave:()=>window.LexiWordAudio?.stop()
  };
})();
