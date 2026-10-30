"use strict";
(() => {
  const $=id=>document.getElementById(id);
  const K={
    ru:{title:"Новые режимы Lexi",desc:"Изучение блоками по 30 и практические маршруты. Прогресс сохраняется в аккаунте.",
      anki:"Карточки · 30 слов",route:"Автобусные маршруты",likes:"Μου αρέσει να",periptero:"Περίπτερο",preview:"Изучение слова",next:"Следующая карточка",
      study:"Запомни слово и перевод",test:"Выбери перевод",known:"Закреплено",retry:"Ошибки возвращаются в очередь",
      milestone:"Блок освоен!",continue:"Продолжить",correct:"✓ Верно",wrong:"✗ Ошибка. Правильный ответ:",
      review:"Проверка памяти",done:"Слова освоены",finished:"Все доступные слова изучены",
      routeTitle:"Опиши маршрут по-гречески",routeHelp:"Впиши ответы греческими буквами. Названия мест видны на карте, но предлоги и формы нужно выбрать самостоятельно.",
      routeComplete:"Маршрут описан правильно!",routeWrong:"Проверь отмеченные поля и попробуй снова.",
      check:"Проверить маршрут",nextRoute:"Следующий маршрут",routeLesson:"Глава 6 · Передвижение",
      number:"Номер автобуса словами",origin:"Откуда отправляется?",via1:"Что проезжает сначала?",via2:"Что проезжает затем?",
      stop:"На какой остановке останавливается?",destination:"Куда направляется?",answer:"Правильный вариант",
      likeTitle:"Нравится / не нравится",likeHelp:"Напиши греческую фразу целиком: δεν, μου/σου/του/της/μας/σας/τους, αρέσει να и нужная форма глагола.",
      likeAction:"Проверить конструкцию",shopTitle:"Περίπτερο · покупки",shopHelp:"Список на сегодня. Попроси нужный товар с количеством по-гречески (Θα ήθελα…, Μπορώ να έχω…).",
      buy:"Добавить в корзину",basket:"В корзине",nextBasket:"Следующий список",shopComplete:"Все четыре покупки собраны!",
      shopPlaceholder:"Θα ήθελα …, παρακαλώ.",shopLabel:"Как попросишь этот товар?",
      network:"Не удалось загрузить занятие",saved:"Продолжение доступно с другого устройства через тот же аккаунт."},
    en:{title:"New Lexi learning modes",desc:"Master 30-word batches and practise bus routes. Progress is tied to your account.",
      anki:"Flashcards · 30 words",route:"Bus routes",likes:"I like to · Greek patterns",periptero:"Mini-market",preview:"Study the word",next:"Next card",
      study:"Memorize the word and meaning",test:"Choose the translation",known:"Mastered",retry:"Missed words return until mastered",
      milestone:"Batch mastered!",continue:"Continue",correct:"✓ Correct",wrong:"✗ Incorrect. Correct answer:",
      review:"Memory challenge",done:"Words mastered",finished:"All available words studied",
      routeTitle:"Describe a route in Greek",routeHelp:"Type in Greek. Stops are on the map; choose your own articles and prepositions.",
      routeComplete:"Route described correctly!",routeWrong:"Check the highlighted fields and try again.",
      check:"Check route",nextRoute:"Next route",routeLesson:"Chapter 6 · Getting around",
      number:"Bus number in Greek words",origin:"Starting point",via1:"First landmark passed",via2:"Next landmark",
      stop:"Stop where the bus halts",destination:"Final destination",answer:"Correct wording",
      likeTitle:"Like / dislike",likeHelp:"Type the complete Greek phrase using δεν, μου/σου/του/της/μας/σας/τους, αρέσει να and the verb form.",
      likeAction:"Check the phrase",shopTitle:"Περίπτερο · shopping",shopHelp:"Your shopping list. Request the item and quantity in Greek (Θα ήθελα…, Μπορώ να έχω…).",
      buy:"Add to basket",basket:"In basket",nextBasket:"Next shopping list",shopComplete:"All four items purchased!",
      shopPlaceholder:"Θα ήθελα …, παρακαλώ.",shopLabel:"How would you ask for this?",
      network:"Could not load lesson",saved:"Resume from any device by signing into the same account."}
  };
  const UI={
    zh:{title:"希腊语训练模式",anki:"30词卡片",route:"公交路线",likes:"喜欢/不喜欢",periptero:"迷你市场",
      likeTitle:"喜欢 / 不喜欢",likeAction:"检查希腊语句子",peripteroTitle:"购物",buy:"放入购物篮",basket:"购物篮",
      nextBasket:"下一个购物清单"},
    ar:{title:"أنماط تدريب اليونانية",anki:"بطاقات 30 كلمة",route:"مسارات الحافلات",likes:"أحب / لا أحب",
      periptero:"متجر صغير",likeTitle:"أحب / لا أحب",likeAction:"تحقق من الجملة",
      buy:"أضف إلى السلة",basket:"في السلة",nextBasket:"قائمة جديدة"},
    es:{title:"Modos de aprendizaje",anki:"30 tarjetas",route:"Rutas de autobús",likes:"Me gusta / No me gusta",
      periptero:"Minimercado",likeTitle:"Gustos y preferencias",likeAction:"Comprobar frase",
      buy:"Añadir a la cesta",basket:"En la cesta",nextBasket:"Lista siguiente"},
    pt:{title:"Modos de aprendizagem",anki:"30 cartões",route:"Percursos de autocarro",likes:"Gosto / Não gosto",
      periptero:"Minimercado",likeTitle:"Gostos e preferências",likeAction:"Verificar frase",
      buy:"Adicionar ao cesto",basket:"No cesto",nextBasket:"Lista seguinte"}
  };
  const labels={number:"Το λεωφορείο",origin:"Ξεκινάει από",via1:"Περνάει από",via2:"Μετά περνάει από",
    stop:"Σταματάει στη στάση",destination:"Πηγαίνει προς"};
  let mode="anki",anki=null,route=null,likes=null,shop=null,busy=false,language=null;
  const lang=()=>$("lang")?.value||"ru";
  const t=key=>(UI[lang()]||{})[key]||(K[lang()]||K.en)[key]||K.en[key]||key;
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
    const response=await fetch("/greek/api/tracks/"+part+(body?"":"?lang="+encodeURIComponent(lang())),{
      method:body?"POST":"GET",credentials:"same-origin",cache:"no-store",
      ...(body?{headers:{"Content-Type":"application/json"},body:JSON.stringify({...body,lang:lang()})}:{})});
    const data=await response.json().catch(()=>({}));
    if(!response.ok)throw new Error(data.error||String(response.status));
    return data;
  }
  function message(msg,bad=false){
    const el=$(mode==="anki"?"track-message":"life-message");if(!el)return;
    el.hidden=!msg;el.textContent=msg||"";el.className="track-message"+(bad?" bad":"");
  }
  async function reload(){
    if(!$(mode==="anki"?"tracks-view":"life-view")||$(mode==="anki"?"tracks-view":"life-view").hidden)return;
    if(busy)return;
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
    busy=true;
    try{
      if(mode==="anki"){anki=await request("anki");renderAnki();}
      else if(mode==="route"){route=await request("route");renderRoute();}
      else if(mode==="likes"){likes=await request("likes");renderLikes();}
      else {shop=await request("periptero");renderShop();}
    }catch(err){message(t("network")+": "+err.message,true);}
    finally{busy=false;}
  }
  async function action(part,body,callback){
    if(busy)return;
    busy=true;message("");
    try{
      const response=await request(part,body);
      callback(response);
    }catch(err){
      if(err.message==="stale_track"){
        message(t("saved"));
        busy=false;await reload();return;
      }
      message(t("network")+": "+err.message,true);
    }finally{busy=false;}
  }
  function ankiHeader(root){
    const summary=text("div",anki.phase==="review"?t("review"):anki.phase==="preview"?t("study"):t("test"),"track-eyebrow");
    root.append(summary);
    root.append(text("p",t("known")+": "+anki.learned+" · "+t("retry")+": "+anki.misses,"track-meta"));
  }
  function renderAnki(){
    const root=$("track-content");root.replaceChildren();ankiHeader(root);
    const panel=document.createElement("div");panel.className="track-word-card";root.append(panel);
    if(anki.phase==="preview"){
      panel.append(text("div",t("preview")+" · "+anki.at+"/"+anki.cohortSize,"track-small"));
      panel.append(text("h3",anki.card.gr,"track-greek"));
      panel.append(text("p",anki.card.translation,"track-meaning"));
      panel.append(text("p",t("study"),"track-small"));
      panel.append(control(t("next"),()=>action("anki",{action:"advance",revision:anki.revision},
        data=>{anki=data;renderAnki();}),"primary"));
    }else if(anki.phase==="quiz"||anki.phase==="review"){
      panel.append(text("div",(anki.phase==="review"?t("review"):t("test"))+" · "+anki.done+"/"+anki.target,"track-small"));
      panel.append(text("h3",anki.card.gr,"track-greek"));
      const options=document.createElement("div");options.className="track-choices";panel.append(options);
      anki.options.forEach((value,i)=>{
        const b=control((i+1)+". "+value,()=>action("anki",{
          action:"answer",revision:anki.revision,cardId:anki.card.id,selected:value
        },data=>{
          anki=data;
          options.replaceChildren();
          panel.append(text("p",data.feedback.correct?t("correct"):t("wrong")+" "+data.feedback.translation,
            data.feedback.correct?"track-success":"track-error"));
          panel.append(control(t("continue"),()=>renderAnki(),"primary"));
        }));
        options.append(b);
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
  }
  function routeSVG(scene){
    const host=document.createElement("div");host.className="route-map";
    const NS="http://www.w3.org/2000/svg",el=(tag,attrs)=>{
      const n=document.createElementNS(NS,tag);
      for(const [key,value] of Object.entries(attrs))n.setAttribute(key,String(value));
      return n;
    };
    const svg=el("svg",{viewBox:"0 0 610 185",width:"610",height:"185",role:"img",
      "aria-label":"Route "+scene.bus});
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
    root.append(text("div",t("routeLesson"),"track-eyebrow"));
    root.append(text("h3",t("routeTitle"),"track-subtitle"));
    if(!["ru","en"].includes(lang()))root.append(text("p","Stops: EN translation","track-small"));
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
    const feedback=document.createElement("div");feedback.className="track-route-feedback";
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
          feedback.append(control(t("nextRoute"),()=>renderRoute(),"primary"));
        }else{
          submit.disabled=false;
        }
      });
      if(!busy)submit.disabled=false;
    });
  }

  function renderLikes(){
    const root=$("life-content");root.replaceChildren();
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
    if(likes.promptLang!==lang())box.append(text("p","(EN)","track-small"));
    box.append(text("p","Ρήμα: "+likes.lemma,"track-small"));
    const form=document.createElement("form");form.className="track-like-form";box.append(form);
    const input=document.createElement("input");input.type="text";input.lang="el";
    input.dir="ltr";input.maxLength=180;input.autocomplete="off";
    input.placeholder=likes.requiresNa?"… μου αρέσει να …":"… μου αρέσει …";
    form.append(input);
    const submit=document.createElement("button");
    submit.type="submit";submit.className="primary track-button";
    submit.textContent=t("likeAction");form.append(submit);
    const result=document.createElement("div");form.append(result);
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
          result.append(control(t("continue"),()=>renderLikes(),"primary"));
        }else submit.disabled=false;
      }).finally(()=>{if(!busy)submit.disabled=false;});
    });
  }
  function renderShop(){
    const root=$("life-content");root.replaceChildren();
    root.append(text("div","Περίπτερο · Μίνι μάρκετ","track-eyebrow"));
    root.append(text("h3",t("shopTitle")+" · "+shop.round,"track-subtitle"));
    root.append(text("p",t("shopHelp"),"track-small"));
    if(!["ru","en"].includes(lang()))root.append(text("p","Shopping list: EN translation","track-small"));
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
      const note=document.createElement("div");form.append(note);
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
      root.append(control(t("nextBasket"),()=>action("periptero",{
        action:"next",revision:shop.revision
      },data=>{shop=data;renderShop();}),"primary"));
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
  window.lexiTracks={
    onOpen:()=>{mode="anki";reload();},
    openLife:(selected)=>{mode=selected;reload();}
  };
})();
