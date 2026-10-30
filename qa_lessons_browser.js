"use strict";
const {chromium}=require("/app/qa_deps/node_modules/playwright");
(async()=>{
 const browser=await chromium.launch({headless:true,args:["--no-sandbox","--disable-dev-shm-usage"]});
 try{
  const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  await context.addCookies([{name:"greek_session",value:process.env.QA_TOKEN,
    url:"http://127.0.0.1:18632/greek/",httpOnly:true,secure:false,sameSite:"Lax"}]);
  const page=await context.newPage(),errors=[];
  page.on("pageerror",e=>errors.push(e.message));
  await page.goto("http://127.0.0.1:18632/greek/",{waitUntil:"networkidle"});
  await page.locator("#auth-gate").waitFor({state:"hidden",timeout:12000});
  await page.locator("#board-view").waitFor({state:"visible"});
  await page.locator(".lesson-list-item").first().waitFor();
  if(await page.locator(".board-road").count())throw Error("Old map is still in UI");
  if(await page.locator(".lesson-list-item").count()!==8)throw Error("Expected eight lessons");
  if(await page.locator(".lesson-list-item.current").count()!==1)throw Error("Missing next lesson");
  if(await page.locator(".lesson-list-item.locked").count()!==7)throw Error("Locked lessons exposed");
  if((await page.locator(".lesson-list-item.locked").allInnerTexts()).some(x=>!x.includes("Неизвестный урок")))
    throw Error("Future lesson names leaked");
  await page.locator(".lesson-list-item.current .lesson-inline-start").click();
  await page.locator("#board-play").waitFor({state:"visible"});
  await page.locator(".lesson-option").first().waitFor();
  if(!/(12|14)/.test(await page.locator(".lesson-progress-label").innerText()))throw Error("One-question lesson");
  const choices=page.locator(".lesson-option");
  const target=process.env.QA_TARGET;
  const labels=await choices.allInnerTexts();
  const correct=labels.findIndex(x=>x.endsWith(target));
  if(correct<0)throw Error("Correct option missing");
  const wrong=labels.findIndex((x,i)=>i!==correct);
  await choices.nth(wrong).click();
  await page.getByText("Есть ошибка. Попробуй исправить.",{exact:false}).waitFor();
  if(!(await page.locator(".lesson-progress-label").innerText()).includes("Задание 1"))
    throw Error("Wrong answer advanced lesson");
  await choices.nth(correct).click();
  await page.getByText("Верно!",{exact:true}).waitFor();
  await page.locator(".lesson-feedback .lesson-primary").click();
  await page.locator(".lesson-progress-label").getByText("Задание 2",{exact:false}).waitFor();
  await page.locator(".lesson-play-top button").click();
  await page.locator(".lesson-list-item.current").waitFor();
  if(!await page.locator(".lesson-review-count").isVisible())throw Error("Backlog counter missing");
  if(!(await page.locator(".lesson-review-count").innerText()).includes("1"))
    throw Error("Missed question not in learning backlog");
  await page.locator(".lesson-list-item.current .lesson-inline-start").click();
  await page.locator(".lesson-progress-label").getByText("Задание 2",{exact:false}).waitFor();
  await page.locator(".lesson-play-top button").click();
  await page.locator('[data-page="practice"]').click();
  await page.locator("#practice-view").waitFor({state:"visible"});
  if(!await page.locator(".legacy-notice").isVisible())throw Error("Classic deprecation warning missing");
  if(await page.locator("#kind-options input").count()<12)throw Error("Classic filter set changed");
  await page.locator("#start").click();
  await page.locator("#quiz").waitFor({state:"visible"});
  await page.locator("#answers .answer").first().click();
  await page.locator("#feedback").waitFor({state:"visible"});
  await page.locator('[data-page="board"]').click();
  await page.locator(".lesson-review-count").waitFor();
  await page.locator(".lesson-list-item.current .lesson-inline-start").click();
  await page.locator(".lesson-progress-label").getByText("Задание 2",{exact:false}).waitFor();
  await page.locator(".lesson-play-top button").click();
  for(const width of [320,360,390,768,1200]){
    await page.setViewportSize({width,height:900});
    await page.waitForTimeout(70);
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
    if(overflow>3)throw Error("Horizontal overflow "+width+" "+overflow);
  }
  if(errors.length)throw Error("Browser JavaScript errors "+JSON.stringify(errors));
  console.log("PASS eight locked lessons, 14-question progress, mistake backlog, resume, Classic intact, mobile 320–1200px");
  await context.close();
 }finally{await browser.close();}
})().catch(e=>{console.error("FAIL "+e.stack);process.exitCode=1});
