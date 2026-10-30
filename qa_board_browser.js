"use strict";
const {chromium}=require("/app/qa_deps/node_modules/playwright");
(async()=>{
 const browser=await chromium.launch({headless:true,args:["--no-sandbox","--disable-dev-shm-usage"]});
 try{
  const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  await context.addCookies([{name:"greek_session",value:process.env.QA_TOKEN,
    url:"http://127.0.0.1:18632/greek/",httpOnly:true,secure:false,sameSite:"Lax"}]);
  const page=await context.newPage();const errors=[];
  page.on("pageerror",e=>errors.push(e.message));
  await page.goto("http://127.0.0.1:18632/greek/",{waitUntil:"networkidle"});
  await page.locator("#auth-gate").waitFor({state:"hidden",timeout:12000});
  await page.locator("#board-view").waitFor({state:"visible",timeout:12000});
  await page.locator(".board-node").first().waitFor();
  if(await page.locator('[data-page="life"]').isVisible())
    throw Error("Advanced categories exposed on primary nav");
  await page.locator("#additional-modes-label").click();
  await page.locator('[data-page="life"]').waitFor({state:"visible"});
  await page.locator('[data-page="life"]').click();
  await page.locator("#life-view").waitFor({state:"visible"});
  await page.locator('[data-page="board"]').click();
  await page.locator(".board-node").first().waitFor();
  if(await page.locator(".board-node").count()!==8)throw Error("Not eight visible game tiles");
  if(await page.locator(".board-node.current").count()!==1)throw Error("No active piece");
  if(await page.locator(".board-node.locked").count()!==7)throw Error("Locked future steps missing");
  if(await page.locator(".board-node.skipped").count())throw Error("Skipped steps at fresh start");
  if((await page.locator(".board-stats").innerText()).includes("1 / 48"))throw Error("Free mastery");
  await page.locator(".board-main-start").click();
  await page.locator(".board-answer-choices .board-choice").first().waitFor();
  if(await page.locator("#board-play").isHidden())throw Error("Game quest did not open");
  const target=process.env.QA_TARGET;
  let hit=null;
  for(const option of await page.locator(".board-choice").all()){
    const label=await option.innerText();
    if(label.endsWith(target)){hit=option;break;}
  }
  if(!hit)throw Error("Correct reviewed option unavailable in board quest");
  await hit.click();
  await page.getByText("Ход пройден!",{exact:false}).waitFor({timeout:4000});
  await page.locator(".board-next").click();
  await page.locator(".board-node.current").waitFor();
  if(await page.locator(".board-node.completed").count()!==1)throw Error("Mastery not stored");
  await page.locator(".board-main-start").click();
  await page.locator(".board-choice").first().waitFor();
  if(await page.locator(".board-audio").count()!==2)throw Error("A1 word missing Greek WAV playback buttons");
  await page.locator(".board-back").click();
  await page.locator('[data-page="practice"]').click();
  await page.locator("#practice-view").waitFor({state:"visible"});
  if(!await page.locator(".legacy-notice").isVisible())throw Error("Deprecated interface not labelled");
  if(!await page.locator("#setup").isVisible())throw Error("Classic configuration missing");
  if(await page.locator("#kind-options input").count()<12)throw Error("Classic filters not preserved");
  if(await page.locator("#duration-options input").count()!==6)throw Error("Classic time options altered");
  await page.locator("#legacy-switch-board").click();
  await page.locator("#board-view").waitFor({state:"visible"});
  await page.locator('[data-page="practice"]').click();
  await page.locator("#setup").waitFor({state:"visible"});
  await page.locator("#start").click();
  await page.locator("#quiz").waitFor({state:"visible"});
  await page.locator("#answers .answer").first().waitFor();
  await page.locator("#answers .answer").first().click();
  await page.locator("#feedback").waitFor({state:"visible"});
  await page.locator('[data-page="board"]').click();
  await page.locator(".board-node.completed").waitFor();
  await page.locator('[data-page="practice"]').click();
  await page.locator("#quiz").waitFor({state:"visible"});
  if(await page.locator("#answers").count()!==1)throw Error("Classic quiz lost");
  await page.locator('[data-page="board"]').click();
  await page.locator("#board-view").waitFor({state:"visible"});
  if(await page.locator(".board-node.completed").count()!==1)throw Error("Board progress reset by classic toggle");
  for(const w of [320,360,390,768,1200]){
    await page.setViewportSize({width:w,height:900});await page.waitForTimeout(70);
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
    if(overflow>3){
      const bad=await page.evaluate(()=>[...document.querySelectorAll("body *")]
        .filter(x=>x.getBoundingClientRect().right>document.documentElement.clientWidth+4)
        .slice(0,15).map(x=>[x.tagName,x.className,x.getBoundingClientRect().right]));
      const sizes=await page.evaluate(()=>({doc:[document.documentElement.clientWidth,document.documentElement.scrollWidth],
        body:[document.body.clientWidth,document.body.scrollWidth],
        viewport:[innerWidth,visualViewport?.width],
        tabs:[document.querySelector(".tabs")?.clientWidth,document.querySelector(".tabs")?.scrollWidth],
        site:[document.querySelector(".site")?.clientWidth,document.querySelector(".site")?.scrollWidth]}));
      throw Error("Horizontal overflow "+w+" "+overflow+" "+JSON.stringify({bad,sizes}));
    }
  }
  if(errors.length)throw Error("Uncaught JS errors "+JSON.stringify(errors));
  console.log("PASS new board 8 tiles, authentic scoring, A1 Pocket audio, classic Deprecated full quiz preserved, mobile 320–1200px");
  await context.close();
 }finally{await browser.close();}
})().catch(err=>{console.error("FAIL "+err.stack);process.exitCode=1});
