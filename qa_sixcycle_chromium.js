'use strict';
const {chromium}=require('/qa/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({args:['--no-sandbox','--disable-dev-shm-usage']});
 try {
 for(const width of [320,1440]){
  const context=await browser.newContext({viewport:{width,height:900},
    isMobile:width===320,hasTouch:width===320,ignoreHTTPSErrors:true});
  const page=await context.newPage();page.setDefaultTimeout(16000);
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('https://localhost:18443/greek/',{waitUntil:'networkidle'});
  if(!await page.locator('#adaptive-mode').count()||!await page.locator('#srs-optin').count())
    throw Error('Learning controls missing');
  await page.locator('#auth-name').fill('Sixcycle UI QA '+width);
  await page.locator('#auth-submit').click();
  await page.locator('#auth-enter').click();
  await page.locator('#auth-gate').waitFor({state:'hidden'});
  await page.locator('#adaptive-mode').check();
  await page.locator('#srs-optin').check();
  const cap=page.waitForResponse(r=>r.url().includes('/api/capacity?'));
  await page.locator('#estimate-capacity').click();
  const pace=await (await cap).json();
  if(pace.paceSeconds!==20)throw Error('Pace fallback invalid');
  await page.locator('#start').click();
  await page.locator('#quiz:not([hidden])').waitFor();
  const action=page.waitForResponse(r=>r.url().includes('/api/answer')&&r.request().method()==='POST');
  await page.locator('#answers .answer').first().click();
  const result=await (await action).json();
  if(!result.nextReview)throw Error('SRS answer not recorded');
  if(!result.correct&&!result.explanation)throw Error('Explanation absent on wrong answer');
  await page.locator('#finish-now').click();
  await page.locator('#finished:not([hidden])').waitFor();
  await page.locator('.tab[data-page=stats]').click();
  await page.waitForFunction(()=>document.querySelectorAll('#mastery-heatmap .mastery-chip').length===20);
  const chips=await page.locator('#mastery-heatmap .mastery-chip').count();
  if(chips!==20)throw Error('Expected twenty chapters');
  await page.locator('.tab[data-page=practice]').click();
  await page.locator('#again').click();
  await page.waitForFunction(()=>document.querySelector('#srs-status').textContent.includes('1'));
  await page.locator('#lang').selectOption('ar');
  if(await page.evaluate(()=>document.documentElement.dir)!=='rtl')throw Error('Arabic RTL missing');
  if(await page.locator('#adaptive-mode').isChecked()!==true)throw Error('Adaptive toggle lost');
  if(await page.locator('#srs-optin').isChecked()!==true)throw Error('SRS toggle lost');
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
  if(overflow>2)throw Error('Horizontal overflow '+width+' '+overflow);
  if(errors.length)throw Error('Page errors: '+errors.join(' | '));
  console.log('PASS SIXCYCLE CHROMIUM',width,'opt-in SRS, adaptive, feedback, 20-chapter heatmap, Arabic RTL, no overflow');
  await context.close();
 }
 } finally {await browser.close()}
})().catch(e=>{console.error('FAIL SIXCYCLE CHROMIUM '+e.stack);process.exitCode=1});
