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
  if(await page.locator(".lesson-option").count()!==0)
    throw Error("Incorrect answer options remained available after revealing solution");
  if(await page.locator(".lesson-feedback button").count()!==1)
    throw Error("Answer not finalized to a single navigation button");
  if((await page.locator(".lesson-feedback button").innerText())!=="Дальше")
    throw Error("Expected only Next after wrong answer");
  if(await page.locator(".lesson-play-top button").isVisible())
    throw Error("Back button still available while answer correction visible");
  if(!await page.locator(".lesson-correct-answer").isVisible())
    throw Error("Missing solution after wrong response");
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
  await context.close();

  // Last question failed: one Finish lesson control, not a leaked retry
  // despite the server having finalized the lesson on that response.
  const lastContext=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  await lastContext.addCookies([{name:"greek_session",value:process.env.QA_LAST_TOKEN,
    url:"http://127.0.0.1:18632/greek/",httpOnly:true,secure:false,sameSite:"Lax"}]);
  const lastPage=await lastContext.newPage();
  await lastPage.goto("http://127.0.0.1:18632/greek/",{waitUntil:"networkidle"});
  await lastPage.locator("#auth-gate").waitFor({state:"hidden",timeout:12000});
  await lastPage.locator(".lesson-list-item.current .lesson-inline-start").click();
  await lastPage.locator(".lesson-progress-label").getByText("Задание 14",{exact:false}).waitFor();
  const lastOptions=lastPage.locator(".lesson-option");
  const finalLabels=await lastOptions.allInnerTexts();
  const lastWrongIndex=finalLabels.findIndex(x=>!x.endsWith(process.env.QA_LAST_CORRECT));
  if(lastWrongIndex<0)throw Error("No wrong last answer offered");
  await lastOptions.nth(lastWrongIndex).click();
  await lastPage.getByText("Есть ошибка. Попробуй исправить.",{exact:false}).waitFor();
  if(await lastPage.locator(".lesson-option").count())
    throw Error("Last question remained answerable after wrong response");
  if(await lastPage.locator(".lesson-feedback button").count()!==1)
    throw Error("Expected exactly one lesson completion button");
  if((await lastPage.locator(".lesson-feedback button").innerText())!=="Завершить урок")
    throw Error("Expected Finish lesson after wrong FINAL answer");
  if(!await lastPage.getByText("Ошибки: 1",{exact:false}).isVisible())
    throw Error("Final wrong answer not counted");
  await lastPage.locator(".lesson-feedback button").click();
  await lastPage.locator(".lesson-list-item.completed").first().waitFor();
  if(await lastPage.locator(".lesson-review-count").innerText()!=="1")
    throw Error("Final wrong question not in later-review backlog");
  await lastContext.close();
  console.log("PASS wrong first/final answers immediately finalized with single Next/Finish, backlog, Classic intact, mobile 320–1200px");
 }finally{await browser.close();}
})().catch(e=>{console.error("FAIL "+e.stack);process.exitCode=1});
