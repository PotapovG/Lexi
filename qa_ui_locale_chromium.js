'use strict';
// Cross-locale real-Chromium regression: public app paths, throwaway local HTTPS/DB.
const {chromium}=require('playwright');
const LANGS=['ru','pt','ar','zh','es','en','pt','ru'];
const AVAILABLE={ru:'1795 карточек в библиотеке',pt:'1795 cartões na biblioteca',
 ar:'1795 بطاقة',zh:'题库共有 1795 张卡片',es:'1795 tarjetas en la biblioteca',
 en:'1795 cards in the library'};
const EXPECTED={ru:'Сонный Академик',pt:'Estudante de grego',
 ar:'متعلم اليونانية',zh:'希腊语学习者',es:'Estudiante de griego',en:'Curious Learner'};
async function main(){
 const browser=await chromium.launch({headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const ctx=await browser.newContext({viewport:{width:360,height:780},isMobile:true,hasTouch:true,ignoreHTTPSErrors:true});
  const page=await ctx.newPage();
  page.setDefaultTimeout(8000);
  const jsErrors=[];page.on('pageerror',e=>jsErrors.push(e.message));
  await page.goto('https://localhost:18443/greek/',{waitUntil:'networkidle'});
  await page.locator('#auth-gate:not([hidden])').waitFor();
  await page.locator('#auth-name').fill('UILocalChromium2026');
  await page.locator('#auth-submit').tap();
  await page.locator('#auth-success:not([hidden])').waitFor();
  await page.locator('#auth-enter').tap();
  await page.locator('#auth-gate').waitFor({state:'hidden'});
  for(const lang of LANGS){
    await page.locator('#lang').selectOption(lang);
    await page.waitForTimeout(160);
    const info=await page.evaluate(()=>({lang:document.documentElement.lang,dir:document.documentElement.dir,
       summary:document.getElementById('catalog-summary').textContent,
       title:document.title,placeholder:document.getElementById('auth-name').placeholder,
       footer:document.querySelector('[data-i18n="footerBrand"]').textContent,
       view:document.getElementById('practice-view').textContent.slice(-150)}));
    if(info.summary!==AVAILABLE[lang])throw Error('Wrong catalog summary for '+lang+': '+info.summary);
    if(info.placeholder!==EXPECTED[lang])throw Error('Wrong registration placeholder for '+lang+': '+info.placeholder);
    if(info.lang!==lang||info.dir!==(lang==='ar'?'rtl':'ltr'))throw Error('Wrong document language '+lang);
    if(info.title!==info.footer)throw Error('Wrong browser tab title '+lang);
    if(lang!=='ru' && /карточек в библиотеке/.test(info.view))throw Error('Russian fallback leaked into '+lang);
    console.log('PASS',lang,info.summary,info.dir);
  }
  await page.locator('#lang').selectOption('pt');
  await page.locator('[data-page="vocab"]').tap();
  await page.locator('#vocab-topic option').nth(12).waitFor({state:'attached'});
  if(await page.locator('#vocab-title').textContent()!=='Vocabulário A1 / A2')throw Error('Vocabulary PT UI not translated');
  await page.locator('#lang').selectOption('ar');
  await page.waitForTimeout(120);
  if(await page.locator('#vocab-topic option').first().textContent()!=='كل المواضيع')throw Error('Arabic all topics not translated');
  if(jsErrors.length)throw Error('Browser exceptions '+JSON.stringify(jsErrors));
  console.log('PASS Chromium RU-PT-AR-ZH-ES-EN live language switches and vocabulary locale rerender');
  await ctx.close();
 }finally{await browser.close()}
}
main().catch(e=>{console.error('FAIL '+e.stack);process.exitCode=1});
