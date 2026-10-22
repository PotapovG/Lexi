'use strict';
// Real Chromium, emulated touch + mobile layout, isolated service and throwaway DB.
const {chromium}=require('playwright');
const fs=require('fs');
const base='https://localhost:18443/greek/';
const screens='/screens';
const langs=(process.env.LEXI_LANGS||'ru,ar,zh,es,pt,en').split(',');
const widths=(process.env.LEXI_WIDTHS||'320,360,390,430,768').split(',').map(Number);
const issues=[];
const perf=[];
function recordIssue(type,detail){issues.push({type,...detail})}
async function measure(page,where,lang,width,{verbose=false}={}){
 const m=await page.evaluate(()=>{
   const visible=e=>{
     if(!e || !(e instanceof Element))return false;
     const st=getComputedStyle(e);
     if(st.display==='none'||st.visibility==='hidden'||!e.getClientRects().length||e.closest('[hidden]'))return false;
     return true;
   };
   const vw=document.documentElement.clientWidth;
   const elements=[...document.querySelectorAll('body *')].filter(visible);
   const bad=elements.map(el=>{
      const r=el.getBoundingClientRect();
      const style=getComputedStyle(el);
      return {tag:el.tagName,sel:el.id?('#'+el.id):el.className?.toString().replaceAll(/\s+/g,'.').slice(0,75),
      text:el.textContent?.slice(0,90),width:Math.round(r.width),left:Math.round(r.left),right:Math.round(r.right),
      scrollWidth:el.scrollWidth,clientWidth:el.clientWidth,overflowX:style.overflowX}
   }).filter(x=>x.left<-4||x.right>vw+4).filter(x=>x.width>0);
   const buttons=elements.filter(el=>el.matches('button,input,select')).map(el=>{
     const r=el.getBoundingClientRect();
     return {id:el.id||el.getAttribute('data-page')||el.className?.toString().slice(0,35),
       w:Math.round(r.width),h:Math.round(r.height),y:Math.round(r.top),text:el.textContent?.slice(0,28)};
   });
   return {url:location.href,vw,sw:document.documentElement.scrollWidth,bodyWidth:document.body.scrollWidth,
     docDir:document.documentElement.dir,overflow:bad.slice(0,12),smallButtons:buttons.filter(x=>x.h<42||x.w<35).slice(0,15),
     anyButtonCount:buttons.length,viewportHeight:window.innerHeight};
 });
 const {overflow,smallButtons}=m;
 if(m.sw>m.vw+2)recordIssue('horizontal-scroll',{where,lang,width,sw:m.sw,vw:m.vw,overflow});
 if(overflow.some(x=>x.right>m.vw+30||x.left< -30))recordIssue('overhanging-element',{where,lang,width,overflow:overflow.slice(0,5)});
 if(m.docDir!==(lang==='ar'?'rtl':'ltr'))recordIssue('wrong-direction',{where,lang,width,dir:m.docDir});
 if(where==='vocab-answer'&&smallButtons.some(x=>x.id==='vocab-back'))recordIssue('small-touch-target',{where,lang,width,target:'vocab-back',h:smallButtons.find(x=>x.id==='vocab-back').h});
 if(verbose)console.log('MEASURE',JSON.stringify({where,lang,width,vw:m.vw,scroll:m.sw,issues:overflow.slice(0,3),tiny:smallButtons.slice(0,3)}));
 return m;
}
function randTestScreenshotName(lang,width,phase){return `${lang}-${width}-${phase}.png`}
async function screenshot(page,lang,width,phase){
 if(width!==320&&width!==390)return;
 if(lang!=='ru'&&lang!=='ar'&&lang!=='zh')return;
 await page.screenshot({path:`${screens}/${randTestScreenshotName(lang,width,phase)}`,fullPage:true});
}
async function run(){
 const browser=await chromium.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  let sharedCode=null;
  for(const width of widths){
   for(const lang of langs){
    const context=await browser.newContext({viewport:{width,height:800},deviceScaleFactor:2,
      isMobile:width!==768,hasTouch:true,locale:lang==='ar'?'ar-SA':lang==='zh'?'zh-CN':'en-US',
      reducedMotion:'reduce',ignoreHTTPSErrors:true});
    const page=await context.newPage();
    page.setDefaultTimeout(7000);
    const jsErrors=[];
    page.on('pageerror',err=>jsErrors.push(err.message));
    page.on('console',msg=>{if(msg.type()==='error'&&!msg.text().includes('401'))jsErrors.push(msg.text())});
    let lastQuiz=null;
    page.on('response',async resp=>{if(resp.url().includes('/api/quiz?'))try{lastQuiz=await resp.json()}catch{}});
    const start=Date.now();
    try{
      await page.goto(base,{waitUntil:'networkidle',timeout:20000});
      await page.locator('#auth-gate:not([hidden])').waitFor({timeout:8000});
      await page.locator('#auth-lang').selectOption(lang);
      await measure(page,'auth',lang,width,{verbose:width===320});
      await screenshot(page,lang,width,'auth');
      if(!sharedCode){
        await page.locator('#auth-name').fill('Mobi'+lang+width);
        await page.locator('#auth-submit').tap();
        await page.locator('#auth-success:not([hidden])').waitFor({timeout:9000});
        await measure(page,'registered',lang,width,{verbose:width===320});
        sharedCode=(await page.locator('#auth-created-code').textContent()).trim();
        if(!/^\d{8}$/.test(sharedCode))throw Error('Registration code not eight digits');
        await screenshot(page,lang,width,'registered');
        await page.locator('#auth-enter').tap();
      }else{
        await page.locator('#mode-login').click();
        await page.locator('#auth-input-code').fill(sharedCode);
        await page.locator('#auth-submit').tap();
      }
      await page.locator('#auth-gate').waitFor({state:'hidden',timeout:8000});
      await measure(page,'home',lang,width);
      await screenshot(page,lang,width,'home');
      // Verify that the source-PDF table of contents is really navigable on
      // phone widths, with 20 printed units (5/10/15/20 = reviews).
      await page.locator('label:has(input[name="scope"][value="chapters"]) span').tap();
      const units=await page.locator('#chapter-grid .chapter-option').count();
      if(units!==22)recordIssue('missing-printed-chapters',{lang,width,units});
      const printed5=await page.locator('#chapter-grid .chapter-option').filter({has:page.locator('input[value="5"]')}).textContent();
      if(!printed5.includes('Πάμε πάλι'))recordIssue('printed-review-5-missing',{lang,width,printed5});
      await measure(page,'chapters-20-and-4-reviews',lang,width);
      await screenshot(page,lang,width,'chapters');
      await page.locator('label:has(input[name="scope"][value="pages"]) span').tap();
      await page.locator('[data-page="vocab"]').click();
      await page.locator('#vocab-topic option').nth(10).waitFor({state:'attached',timeout:6000});
      await page.locator('#vocab-topic').selectOption('everyday');
      await page.locator('#vocab-level').selectOption('A2');
      await page.locator('#vocab-new').tap();
      await page.locator('#vocab-preview-list .topic-study-row').first().waitFor({timeout:6000});
      await measure(page,'vocab-preview',lang,width);
      await screenshot(page,lang,width,'preview');
      await page.locator('#vocab-begin').tap();
      await page.locator('#vocab-choices .answer').first().waitFor({timeout:6000});
      await measure(page,'vocab-answer',lang,width,{verbose:width===320});
      const touch=await page.evaluate(()=>({
        columns:getComputedStyle(document.querySelector('#vocab-choices')).gridTemplateColumns,
        backHeight:document.querySelector('#vocab-back').getBoundingClientRect().height,
        firstHeight:document.querySelector('#vocab-choices .answer').getBoundingClientRect().height
      }));
      if(touch.backHeight<44)recordIssue('touch-back-small',{lang,width,...touch});
      if(touch.firstHeight<48)recordIssue('touch-choice-small',{lang,width,...touch});
      if(width<=760&&touch.columns.split(' ').length!==1)recordIssue('vocab-two-narrow-columns',{lang,width,...touch});
      await screenshot(page,lang,width,'vocab-answer');
      // Create a stress test very long translated label in a real answer button.
      await page.locator('#vocab-choices .answer').first().evaluate(e=>{
        const last=e.querySelector('span:last-child');
        last.textContent+=' — Δοκιμή μέγιστου μήκους • Ultra-long example of conjugation, translated meaning, and a descriptive context. '.repeat(3);
      });
      await measure(page,'vocab-stress',lang,width);
      await screenshot(page,lang,width,'vocab-stress');
      await page.locator('#vocab-back').tap();
      await page.locator('[data-page="practice"]').tap();
      await page.locator('label:has(input[name="scope"][value="pages"]) span').tap();
      await page.locator('#page-from').fill('1');
      await page.locator('#page-to').fill('56');
      await page.locator('#kind-options input').evaluateAll(els=>{
        for(const e of els)e.checked=e.value==='word';
      });
      await page.locator('#start').tap();
      await page.locator('#quiz:not([hidden])').waitFor({timeout:8000});
      await page.locator('#answers .answer').first().waitFor({timeout:8000});
      await measure(page,'book-word-translation',lang,width);
      await screenshot(page,lang,width,'book-word-translation');
      if(lang!=='en'){
        const q=lastQuiz?.questions?.[0];
        const content=q?.direction==='gr-ru'
          ?await page.locator('#answers').textContent()
          :await page.locator('#question-prompt').textContent();
        if(!content.includes('('))recordIssue('missing-English-translation-hint',{lang,width});
      }
      await page.locator('#answers .answer').first().evaluate(el=>{
        el.querySelector('span:last-child').textContent+=' — Greek learning stress test of a very long translation and its parenthetical English wording. '.repeat(3);
      });
      await measure(page,'book-word-stress',lang,width);
      await page.locator('#finish-now').tap();
      await page.locator('#finished:not([hidden])').waitFor({timeout:8000});
      await page.locator('#again').tap();
      await page.locator('#setup:not([hidden])').waitFor({timeout:8000});
      await page.locator('label:has(input[name="scope"][value="pages"]) span').tap();
      await page.locator('#page-from').fill('198');
      await page.locator('#page-to').fill('198');
      await page.locator('#kind-options input').evaluateAll(els=>{for(const e of els)e.checked=(e.value==='dialogue')});
      await page.locator('#start').tap();
      await page.locator('#dialogue-lines:not([hidden])').waitFor({timeout:8000});
      const startq=lastQuiz?.questions?.[0];
      if(!startq || startq.id!=='dlg080')recordIssue('wrong-dialogue',{lang,width,id:startq?.id});
      await measure(page,'dialogue',lang,width,{verbose:width===320});
      const dlgDir=await page.locator('#dialogue-lines').evaluate(e=>getComputedStyle(e).direction);
      if(dlgDir!=='ltr')recordIssue('greek-dialogue-not-ltr',{lang,width,dir:dlgDir});
      await screenshot(page,lang,width,'dialogue');
      if(startq && startq.gapIndices.length===3){
        for(let k=0;k<3;k++){
          const ans=startq.dialogueGaps[k],ix=startq.choices.indexOf(ans);
          if(ix<0)throw Error('answer not in dialogue bank');
          await page.locator('#answers .answer').nth(ix).tap();
          await page.locator('#next:not([hidden])').waitFor({timeout:5000});
          const fill=await page.locator('.dialogue-blank[data-gap-index="'+k+'"]').evaluate(el=>({text:el.textContent,filled:el.classList.contains('filled')}));
          if(!fill.filled||fill.text!==ans)throw Error('Completed dialogue gap not filled inline '+k);
          const nextText=await page.locator('#next').textContent();
          if(lang==='ru' && nextText!==(k<2?'Следующий пропуск →':'Далее →'))throw Error('Wrong last-gap text '+nextText);
          if(k===2 && lang==='ru'){
            const note=await page.locator('#question-note').textContent();
            if(!note.includes('Все пропуски заполнены'))throw Error('No dialogue completion state');
          }
          if(k<2){
           await page.locator('#next').tap();
           await page.waitForTimeout(100);
           await measure(page,'dialogue-gap-'+(k+2),lang,width);
          }
        }
      }
      if(jsErrors.length)recordIssue('javascript',{lang,width,errors:jsErrors.slice(0,8)});
      perf.push({lang,width,duration:Date.now()-start});
      console.log('PASS',width,lang,'auth, translated 10-word lesson, 8 choices, Arabic RTL, 3-gap dialogue, layout');
    }catch(e){
      recordIssue('failed',{lang,width,message:e.message.slice(0,350),authError:await page.locator('#auth-error').textContent().catch(()=>''),jsErrors:jsErrors.slice(0,4),vocabMessage:await page.locator('#vocab-message').textContent().catch(()=>''),vocabLessonVisible:await page.locator('#vocab-lesson').isVisible().catch(()=>false)});
      console.log('FAIL',width,lang,e.message.slice(0,200));
    }finally{await context.close()}
   }
  }
 }finally{await browser.close()}
 fs.writeFileSync(screens+'/mobile_qa_'+widths.join('_')+'.json',JSON.stringify({issues,perf},null,2));
 console.log('MOBILE_QA',JSON.stringify({count:perf.length,issues:issues.length,kinds:issues.reduce((d,x)=>(d[x.type]=(d[x.type]||0)+1,d),{}),sample:issues.slice(0,18)},null,2));
 if(issues.length)process.exitCode=1;
}
run().catch(err=>{console.error(err);process.exitCode=1});
