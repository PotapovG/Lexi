const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({args:['--no-sandbox']});
 try{
 for(const width of [390,1440]){
  const ctx=await browser.newContext({viewport:{width,height:900},ignoreHTTPSErrors:true,isMobile:width===390,hasTouch:width===390});
  const p=await ctx.newPage();p.setDefaultTimeout(15000);
  const errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto('https://localhost:18443/greek/',{waitUntil:'networkidle'});
  await p.locator('#auth-name').fill('PocketCourseQA'+width);
  await p.locator('#auth-submit').click();await p.locator('#auth-enter').click();
  await p.locator('#auth-gate').waitFor({state:'hidden'});
  await p.locator('input[name=scope][value=listening]').evaluate(el=>el.disabled=false); // isolate stage pre-release UI only
  await p.locator('label:has(input[name=scope][value=listening]) span').click();
  const count=await p.locator('#chapter-grid input').count();
  if(count!==20)throw Error('20 printed listening sections expected, got '+count);
  const page17=await p.locator('#chapter-grid .chapter-page').nth(16).textContent();
  if(!page17.includes('232–245'))throw Error('Wrong printed chapter17 page anchor: '+page17);
  const initial=await p.locator('#chapter-grid input:checked').count();
  if(initial!==4)throw Error('Expected initial 4 chapters: '+initial);
  await p.locator('#listening-range').selectOption('pages');
  if(!await p.locator('#page-controls').isVisible() || await p.locator('#chapter-controls').isVisible())throw Error('Page mode visibility');
  await p.locator('#page-from').fill('48');await p.locator('#page-to').fill('56');
  await p.locator('#listening-difficulty input[value=word]').uncheck();
  await p.locator('#listening-difficulty input[value=sentence]').uncheck();
  await p.locator('#listening-range').selectOption('chapters');
  if(!await p.locator('#chapter-controls').isVisible())throw Error('Chapter mode visibility');
  await p.locator('#chapter-grid .only').nth(16).click();
  const checked=await p.locator('#chapter-grid input:checked').count();
  const value=await p.locator('#chapter-grid input:checked').first().inputValue();
  if(checked!==1||value!=='17')throw Error('Select-only printed chapter 17: '+value);
  await p.locator('label:has(input[name=scope][value=chapters]) span').click();
  if(await p.locator('#chapter-grid input').count()!==22)throw Error('Original ordinary textbook chapter grid changed');
  await p.locator('label:has(input[name=scope][value=listening]) span').click();
  if(await p.locator('#chapter-grid input:checked').first().inputValue()!=='17')throw Error('Listening chapter selection not preserved after mode switching');
  const overflow=await p.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
  if(overflow>2)throw Error('Horizontal overflow '+width+': '+overflow);
  if(errors.length)throw Error('JavaScript page error '+errors.join(' | '));
  console.log('PASS',width,'20 printed book chapters, pages 48-56, word/phrase/sentence controls, original 22-unit grid preserved, no overflow');
  await ctx.close();
 }
 }finally{await browser.close()}
})().catch(e=>{console.error('FAIL',e.stack);process.exitCode=1});
