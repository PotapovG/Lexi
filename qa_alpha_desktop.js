const {chromium}=require('playwright');
(async()=>{const browser=await chromium.launch({args:['--no-sandbox']});try{
const ctx=await browser.newContext({viewport:{width:1440,height:900},ignoreHTTPSErrors:true});
const page=await ctx.newPage();
await page.goto('https://localhost:18443/greek/',{waitUntil:'networkidle'});
await page.evaluate(()=>{const c=document.querySelector('input[name=scope][value=chapters]');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}));});
for(const width of [1440,1200,1024,900,760,390]){
 await page.setViewportSize({width,height:900});
 const data=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,
   alpha:document.querySelector('input[name=scope][value=listening]').disabled,
   boxes:[...document.querySelectorAll('#chapter-grid .chapter-option')].slice(0,5).map(row=>{
    const r=x=>x.getBoundingClientRect();const n=r(row.querySelector('.chapter-name'));
    const f=r(row.querySelector('.chapter-focus'));const pg=r(row.querySelector('.chapter-page'));
    return {labelW:Math.round(n.width),focusW:Math.round(f.width),focusH:Math.round(f.height),cardH:Math.round(r(row).height),overlap:f.bottom>pg.top+2};})}));
 if(!data.alpha||data.overflow>2)throw Error('Alpha/overflow '+width+' '+JSON.stringify(data));
 if(width>=1024&&data.boxes.some(x=>x.labelW<140||x.focusW<140||x.focusH>80||x.cardH>200||x.overlap))throw Error('Bad desktop layout '+width+' '+JSON.stringify(data));
 if(width===1440)await page.locator('#chapter-grid').screenshot({path:'/tmp/qa/greek-chapters-desktop-after.png'});
 console.log('PASS chapter-grid',width,JSON.stringify(data.boxes[2]));
}
await ctx.close();}finally{await browser.close()}})().catch(e=>{console.error('FAIL '+e.stack);process.exitCode=1});
