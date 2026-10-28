'use strict';
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
 const ctx=await browser.newContext({viewport:{width:320,height:740},isMobile:true,hasTouch:true,ignoreHTTPSErrors:true});
 const page=await ctx.newPage();page.setDefaultTimeout(8000);
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const captured=[];page.on('response',async r=>{if(r.url().includes('/api/quiz?'))try{captured.push(await r.json())}catch{}});
 await page.goto('https://localhost:18443/greek/',{waitUntil:'networkidle'});
 await page.locator('#auth-gate:not([hidden])').waitFor();
 await page.locator('#auth-name').fill('Actual Mobile Forms QA');
 await page.locator('#auth-submit').tap();
 await page.locator('#auth-success:not([hidden])').waitFor();
 await page.locator('#auth-enter').tap();
 await page.locator('#auth-gate').waitFor({state:'hidden'});
 async function start(kind,pageNo){
  await page.locator('label:has(input[name="scope"][value="pages"]) span').tap();
  await page.locator('#page-from').fill(String(pageNo));await page.locator('#page-to').fill(String(pageNo));
  await page.locator('#kind-options input').evaluateAll((xs,target)=>xs.forEach(x=>x.checked=x.value===target),kind);
  const response=page.waitForResponse(r=>r.url().includes('/api/quiz?'));
  await page.locator('#start').tap();
  const q=(await (await response).json()).questions[0];
  await page.locator('#quiz:not([hidden])').waitFor();
  if(q.kind!==kind)throw Error('Expected '+kind+', got '+q.kind);
  return q;
 }
 async function done(){await page.locator('#next').tap();await page.locator('#finished:not([hidden])').waitFor();await page.locator('#again').tap();}
 const a=await start('article',29);
 if(a.choices.length!==8||a.prompt!=='Μένω ___ Λευκωσία.')throw Error('Article source unit2 wrong');
 await page.locator('#answers .answer').nth(a.choices.indexOf('στην')).tap();
 await page.locator('#next:not([hidden])').waitFor();
 if(!(await page.locator('#feedback').getAttribute('class')).includes('good'))throw Error('Article answer rejected');
 if(!(await page.locator('#feedback .spelling-guidance').textContent()).includes('στη Λευκωσία'))throw Error('Missing textbook spelling guidance');
 if(await page.locator('#answers .answer.is-correct').count()!==2)throw Error('Both correct feminine variants must highlight green');
 if(await page.locator('#answers .answer.is-wrong').count())throw Error('Acceptable longer nu form is wrongly red');

 await done();
 const q=await start('order',17);
 if(!await page.locator('#order-builder').isVisible())throw Error('Order composer invisible');
 const tokens='Γεια σου, είμαι ο Μάριος και αυτή είναι η Λένα.'.split(' ').map(w=>w.replace(/[.,;:!?]+$/g,''));
 const displayed=await page.locator('#answers .answer.order-word').allTextContents();
 if(displayed.some(t=>/[.,;:!?]$/.test(t)))throw Error('Punctuation must not appear as word choices');
 let indices=[];
 for(const word of tokens){const index=q.choiceTokens.findIndex((w,i)=>w===word&&!indices.includes(i));if(index<0)throw Error('Missing word '+word);indices.push(index);}
 await page.locator('#answers .answer.order-word').nth(indices[0]).tap();
 await page.locator('#order-undo').tap();
 if(await page.locator('#order-draft').textContent()!=='…')throw Error('Undo did not clear');
 for(const i of indices)await page.locator('#answers .answer.order-word').nth(i).tap();
 if(await page.locator('#order-check').isDisabled())throw Error('Full answer not enabled');
 await page.locator('#order-check').tap();
 await page.locator('#next:not([hidden])').waitFor();
 if(!(await page.locator('#feedback').getAttribute('class')).includes('good'))throw Error('Composed Greek rejected');
 if(await page.locator('#order-draft').textContent()!=='Γεια σου, είμαι ο Μάριος και αυτή είναι η Λένα.')throw Error('Automatic punctuation missing');
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
 if(overflow>2)throw Error('Horizontal scroll '+overflow);
 await done();
 await page.locator('#lang').selectOption('ar');
 const ar=await start('article',29);
 if(await page.evaluate(()=>document.documentElement.dir)!=='rtl')throw Error('Arabic RTL lost');
 if(!(await page.locator('#question-note').textContent()).includes('اليونانية'))throw Error('Arabic grammar instructions missing');
 await page.locator('#answers .answer').nth(ar.choices.indexOf('στη')).tap();
 await page.locator('#next:not([hidden])').waitFor();
 if(!(await page.locator('#feedback').getAttribute('class')).includes('good'))throw Error('Arabic correct answer invalid');
 if(errors.length)throw Error('Browser JS errors '+errors.join(', '));
 console.log('PASS real Chromium 320px: tap article, order/undo/reassemble Greek, responsive layout, Arabic RTL article');
 await ctx.close();
 }finally{await browser.close()}
})().catch(e=>{console.error('FAIL '+e.stack);process.exitCode=1});
