from pathlib import Path
p=Path('index.html');s=p.read_text()
def once(a,b):
 global s
 assert s.count(a)==1,(a[:100],s.count(a))
 s=s.replace(a,b)
once('app.js?v=29','app.js?v=30')
once('styles.css?v=26','styles.css?v=27')
once('       <p class="quiet"><span data-i18n="mixedDirections">Направление: греческий ↔ перевод (автоматически)</span></p>',
'''       <div class="learning-engine-options">
        <label><input type="checkbox" id="adaptive-mode"><span data-i18n="adaptiveMode">Адаптивная сложность</span></label>
        <label><input type="checkbox" id="srs-optin"><span data-i18n="srsOptIn">Включить интервальные повторы новых ответов</span></label>
        <p class="quiet" data-i18n="srsNotice">Новая функция включается по желанию; старые ответы остаются без изменений.</p>
        <button type="button" class="secondary compact" id="srs-due-start" disabled data-i18n="srsStart">Карточки по расписанию</button>
        <p class="quiet" id="srs-status" aria-live="polite"></p>
       </div>
       <p class="quiet"><span data-i18n="mixedDirections">Направление: греческий ↔ перевод (автоматически)</span></p>''')
once('   <div class="panel stat-panel"><span class="eyebrow" data-i18n="last14">ПОСЛЕДНИЕ 14 ДНЕЙ</span>',
'''   <div class="panel stat-panel"><span class="eyebrow" data-i18n="masteryTitle">КАРТА ОСВОЕНИЯ</span><h2 data-i18n="masteryHeading">Главы</h2><p class="quiet" data-i18n="masteryNotice">Цвет зависит от правильности ответов. Меньше 8 ответов — предварительная оценка.</p><div class="mastery-heatmap" id="mastery-heatmap"></div></div>
   <div class="panel stat-panel"><span class="eyebrow" data-i18n="last14">ПОСЛЕДНИЕ 14 ДНЕЙ</span>''')
p.write_text(s)

p=Path('app.js');s=p.read_text()
def once(a,b):
 global s
 assert s.count(a)==1,(a[:100],s.count(a))
 s=s.replace(a,b)
once('  const kindIds=["word",',
'''  const ENGINE_I18N={
    ru:{adaptiveMode:"Адаптивная сложность по моим ответам",srsOptIn:"Включить интервальные повторения новых ответов",srsNotice:"Расписание включается добровольно; прежняя история не изменяется.",srsStart:"Повторить по расписанию",srsStatus:"К повторению: {due}; в расписании: {total}",srsSession:"ИНТЕРВАЛЬНЫЕ ПОВТОРЫ",srsEmpty:"Нет карточек к повторению.",masteryTitle:"КАРТА ОСВОЕНИЯ ГЛАВ",masteryHeading:"Прогресс по главам",masteryNotice:"20 глав; цвет отражает точность, менее 8 ответов — предварительные данные. Страницы ориентировочны.",masteryTip:"Глава {chapter}: {pct}% из {count} ответов",masteryUnseen:"Глава {chapter}: пока без ответов",explanationTitle:"Пояснение",paceKind:"Твой темп: около {pace} сек./задание.",paceDefault:"Примерный темп: {pace} сек./задание."},
    en:{adaptiveMode:"Adaptive difficulty based on my answers",srsOptIn:"Enable spaced repetition for new answers",srsNotice:"Opt-in only; earlier results stay unchanged.",srsStart:"Review scheduled cards",srsStatus:"Due: {due}; scheduled: {total}",srsSession:"SPACED REVIEW",srsEmpty:"No cards due for review.",masteryTitle:"CHAPTER MASTERY MAP",masteryHeading:"Progress by chapter",masteryNotice:"20 chapters, colour indicates accuracy; under 8 answers is provisional. Page tags are approximate.",masteryTip:"Chapter {chapter}: {pct}% of {count} answers",masteryUnseen:"Chapter {chapter}: no answers yet",explanationTitle:"Explanation",paceKind:"Your pace: around {pace} sec/item.",paceDefault:"Estimated pace: {pace} sec/item."},
    zh:{adaptiveMode:"按答题情况调整难度",srsOptIn:"对新答案开启间隔复习",srsNotice:"自愿启用，不更改以往进度。",srsStart:"复习到期卡片",srsStatus:"待复习：{due}；已安排：{total}",srsSession:"间隔复习",srsEmpty:"暂无到期卡片。",masteryTitle:"章节掌握地图",masteryHeading:"各章进度",masteryNotice:"共20章；颜色代表正确率，少于8次作答仅供参考。页码近似。",masteryTip:"第{chapter}章：{count}次，{pct}%正确",masteryUnseen:"第{chapter}章：尚无答题",explanationTitle:"说明",paceKind:"你的速度：约每题{pace}秒。",paceDefault:"估计每题{pace}秒。"},
    ar:{adaptiveMode:"صعوبة متكيفة مع إجاباتي",srsOptIn:"تفعيل المراجعة المتباعدة للإجابات الجديدة",srsNotice:"تُفعّل اختياريًا ولا تغيّر النتائج السابقة.",srsStart:"مراجعة البطاقات المستحقة",srsStatus:"مستحقة: {due}؛ مجدولة: {total}",srsSession:"مراجعة متباعدة",srsEmpty:"لا توجد بطاقات للمراجعة الآن.",masteryTitle:"خريطة إتقان الوحدات",masteryHeading:"التقدم حسب الوحدة",masteryNotice:"20 وحدة؛ اللون يوضح الدقة، وأقل من 8 إجابات تقدير أولي. الصفحات تقريبية.",masteryTip:"الوحدة {chapter}: دقة {pct}% من {count} إجابات",masteryUnseen:"الوحدة {chapter}: دون إجابات",explanationTitle:"التفسير",paceKind:"سرعتك: نحو {pace} ثانية للسؤال.",paceDefault:"السرعة المقدرة: {pace} ثانية للسؤال."},
    es:{adaptiveMode:"Dificultad adaptativa según mis respuestas",srsOptIn:"Activar repetición espaciada para respuestas nuevas",srsNotice:"Opcional; no modifica tu historial.",srsStart:"Repasar tarjetas programadas",srsStatus:"Pendientes: {due}; programadas: {total}",srsSession:"REPASO ESPACIADO",srsEmpty:"No hay tarjetas pendientes.",masteryTitle:"MAPA DE DOMINIO POR UNIDAD",masteryHeading:"Progreso por unidad",masteryNotice:"20 unidades; color según precisión, menos de 8 respuestas es provisional. Páginas aproximadas.",masteryTip:"Unidad {chapter}: {pct}% en {count} respuestas",masteryUnseen:"Unidad {chapter}: sin respuestas",explanationTitle:"Explicación",paceKind:"Tu ritmo: unos {pace} s/pregunta.",paceDefault:"Ritmo estimado: {pace} s/pregunta."},
    pt:{adaptiveMode:"Dificuldade adaptativa segundo as respostas",srsOptIn:"Ativar repetição espaçada para novas respostas",srsNotice:"É opcional e não altera o histórico.",srsStart:"Rever cartões agendados",srsStatus:"Pendentes: {due}; agendados: {total}",srsSession:"REVISÃO ESPAÇADA",srsEmpty:"Não há cartões pendentes.",masteryTitle:"MAPA DE DOMÍNIO POR UNIDADE",masteryHeading:"Progresso por unidade",masteryNotice:"20 unidades; cor pela precisão, menos de 8 respostas é provisório. Páginas aproximadas.",masteryTip:"Unidade {chapter}: {pct}% em {count} respostas",masteryUnseen:"Unidade {chapter}: sem respostas",explanationTitle:"Explicação",paceKind:"O teu ritmo: cerca de {pace} s/cartão.",paceDefault:"Ritmo estimado: {pace} s/cartão."}
  };
  for(const [loc,labels] of Object.entries(ENGINE_I18N))Object.assign(I18N[loc],labels);
  const kindIds=["word",''')
once('       listeningRange:listeningRange(),listeningKinds:selectedListeningKinds()',
'''       listeningRange:listeningRange(),listeningKinds:selectedListeningKinds(),
       adaptive:$("adaptive-mode").checked,srsOptIn:$("srs-optin").checked''')
once('    if(Array.isArray(o.listeningKinds))',
'''    $("adaptive-mode").checked=o.adaptive===true;
    $("srs-optin").checked=o.srsOptIn===true;
    if(Array.isArray(o.listeningKinds))''')
once('    return cfg;\n  }\n  async function estimateCapacity()',
'''    if($("adaptive-mode").checked)cfg.adaptive="1";
    return cfg;
  }
  async function estimateCapacity()''')
once('        +" "+t("capacityDisclaimer"));',
'''        +" "+t(r.personalizedPace?"paceKind":"paceDefault").replace("{pace}",r.paceSeconds)
        +" "+t("capacityDisclaimer"));''')
once('  async function startQuiz(weak){','  async function startQuiz(weak,due=false){')
once('    try{state.settings=weak?{mode:"weak_all",lang:$("lang").value,count:"60"}:config(false);show("setup-error",false);}',
'''    try{state.settings=due?{mode:"srs_due",lang:$("lang").value,count:"60"}:
      (weak?{mode:"weak_all",lang:$("lang").value,count:"60"}:config(false));
      show("setup-error",false);}''')
once('    state.mode=weak?"weak":"all";','    state.mode=due?"due":weak?"weak":"all";')
once('        if(weak){txt("weak-empty",t("weakNoAvailable"));setPage("weak");}\n        else {txt("setup-error",t("noCards"));show("setup-error",true);}',
'''        if(weak){txt("weak-empty",t("weakNoAvailable"));setPage("weak");}
        else {txt("setup-error",t(due?"srsEmpty":"noCards"));show("setup-error",true);}''')
once('    txt("quiz-mode",state.mode==="weak"?t("weakSession"):t("session"));',
'''    txt("quiz-mode",state.mode==="due"?t("srsSession"):
      state.mode==="weak"?t("weakSession"):t("session"));''')
once('        body:JSON.stringify({id:q.id,direction:actualDirection,lang:q.lang||state.settings.lang,selected})});',
'''        body:JSON.stringify({id:q.id,direction:actualDirection,lang:q.lang||state.settings.lang,selected,
          srsOptIn:$("srs-optin").checked||state.mode==="due"})});''')
once('      state.seen.push(state.mode==="weak"\n',
     '      state.seen.push((state.mode==="weak"||state.mode==="due")\n')
once('      if(result.spellingNote){',
'''      if(result.explanation){
        const note=document.createElement("p");note.className="spelling-guidance";
        const heading=document.createElement("strong");heading.textContent=t("explanationTitle")+": ";
        note.append(heading,document.createTextNode(result.explanation));$("feedback").append(note);
      }
      if(result.spellingNote){''')
once('  function drawDaily(rows){',
'''  function drawMastery(rows){
    const el=$("mastery-heatmap");el.replaceChildren();
    for(const m of rows||[]){
      const cell=document.createElement("span");cell.className="mastery-chip "+m.status;
      cell.textContent=String(m.chapter);
      cell.title=m.attempts?t("masteryTip").replace("{chapter}",m.chapter)
        .replace("{pct}",m.accuracy).replace("{count}",m.attempts):
        t("masteryUnseen").replace("{chapter}",m.chapter);
      cell.setAttribute("aria-label",cell.title);el.append(cell);
    }
  }
  function drawDaily(rows){''')
once('      drawDaily(s.daily);',
'''      drawDaily(s.daily);drawMastery(s.mastery);
      const due=s.srs?.due||0;
      txt("srs-status",t("srsStatus").replace("{due}",due).replace("{total}",s.srs?.scheduled||0));
      $("srs-due-start").disabled=due===0;''')
once('    $("duration-options").addEventListener("change",saveSettings);',
'''    $("duration-options").addEventListener("change",saveSettings);
    $("adaptive-mode").addEventListener("change",saveSettings);
    $("srs-optin").addEventListener("change",saveSettings);
    $("srs-due-start").addEventListener("click",()=>startQuiz(false,true));''')
p.write_text(s)

p=Path('styles.css');s=p.read_text()
s+='''

.learning-engine-options{display:flex;flex-direction:column;gap:.5rem;margin:1rem 0}
.learning-engine-options>label{display:flex;align-items:flex-start;gap:.6rem;line-height:1.5}
.learning-engine-options input{flex:0 0 auto;margin-top:.25rem}
.learning-engine-options .quiet{margin:.15rem 0}
.mastery-heatmap{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:.5rem}
.mastery-chip{display:grid;place-items:center;min-height:2.3rem;border-radius:.55rem;font-weight:700;background:#344053;color:#fff;border:1px solid #617087}
.mastery-chip.early{background:#54476c}
.mastery-chip.review{background:#884b4b}
.mastery-chip.developing{background:#79652b}
.mastery-chip.strong{background:#235c50}
@media(max-width:500px){.mastery-heatmap{grid-template-columns:repeat(5,minmax(0,1fr))}}
'''
p.write_text(s)
print('FRONTEND_PATCHED',len(s))
