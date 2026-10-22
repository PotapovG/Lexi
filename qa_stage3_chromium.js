const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--no-sandbox']});try{
const c=await b.newContext({viewport:{width:320,height:760},isMobile:true,hasTouch:true,ignoreHTTPSErrors:true});const p=await c.newPage();
await p.goto('https://localhost:18443/greek/',{waitUntil:'networkidle'});
await p.locator('#auth-name').fill('StageThreeMobileQA');await p.locator('#auth-submit').tap();
await p.locator('#auth-enter').tap();await p.locator('#auth-gate').waitFor({state:'hidden'});
await p.locator('label:has(input[value="verbs"]) span').tap();
await p.locator('#verb-max-unit').selectOption('2');
await p.waitForFunction(()=>document.querySelector('#verb-stage-summary').textContent.includes('6'));
await p.locator('#estimate-capacity').tap();
await p.waitForFunction(()=>document.querySelector('#capacity-result').textContent.includes('6 уникальных'));
const overflow=await p.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
if(overflow>2)throw Error('overflow '+overflow);
console.log('PASS Chromium mobile 320px: step2 count, capacity shortage and no overflow');await c.close();
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
