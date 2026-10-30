"use strict";
const {chromium}=require("/app/qa_deps/node_modules/playwright");
(async()=>{
 const browser=await chromium.launch({headless:true,args:["--no-sandbox","--disable-dev-shm-usage"]});
 try{
   const ctx=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
   await ctx.addCookies([{name:"greek_session",value:process.env.QA_TOKEN,
      url:"http://127.0.0.1:18632/greek/",httpOnly:true,secure:false,sameSite:"Lax"}]);
   const page=await ctx.newPage();
   const errors=[];page.on("pageerror",err=>errors.push(err.message));
   await page.goto("http://127.0.0.1:18632/greek/",{waitUntil:"networkidle"});
   await page.locator("#auth-gate").waitFor({state:"hidden",timeout:12000});
   const audioRequests=[];
   page.on("request",request=>{
     if(/\/greek\/(?:audio|pronunciation)\/[a-f0-9]{32}\.wav$/.test(new URL(request.url()).pathname))
       audioRequests.push(request.url());
   });
   await page.locator('[data-page="tracks"]').click();
   await page.locator(".track-word-card .track-greek").getByText("το όνομα").waitFor();
   const soundButtons=page.locator(".track-audio-button");
   if(await soundButtons.count()!==2)throw Error("Expected two recorded-audio buttons");
   if(await soundButtons.first().isDisabled())throw Error("Pocket TTS button disabled despite recording");
   await soundButtons.first().click();
   await page.getByText("Воспроизводится Pocket TTS.",{exact:true}).waitFor({timeout:12000});
   await soundButtons.last().click();
   await page.getByText("Воспроизводится Pocket TTS.",{exact:true}).waitFor({timeout:12000});
   if(audioRequests.length<1)throw Error("Pocket WAV request was not made for each playback");
   await page.locator(".track-word-card button.primary").click();
   await page.getByText("2/30",{exact:false}).first().waitFor();
   if(await page.locator(".track-audio-button").count()!==2)throw Error("Next card missing playback");
   await page.locator('[data-page="life"]').click();
   await page.locator(".life-adventure-card").waitFor();
   await page.waitForFunction(()=>document.querySelector("#life-max-chapter").value==="6");
   if(await page.locator("#life-activity-controls").isVisible())throw Error("Category picker exposed");
   if(await page.locator(".life-adventure-card svg").count()!==1)throw Error("Missing scene artwork");
   if(await page.locator(".life-adventure-title").textContent()!=="Знакомство")throw Error("First journey not chosen");
   await page.locator(".life-adventure-card .life-continue").click();
   await page.locator(".life-answer-form textarea").waitFor();
   await page.locator(".life-answer-form textarea").fill("Με λένε Μαρία.");
   await page.locator(".life-answer-form button[type=submit]").click();
   await page.getByText("Отлично! Тебя поняли.",{exact:false}).waitFor();
   await page.locator(".life-task-actions .life-continue").click();
   await page.locator(".life-task-prompt").getByText("Я живу в Никосии",{exact:false}).waitFor();
   await page.locator(".life-answer-form textarea").fill("Μένω στην Λεθκώσια");
   await page.locator(".life-answer-form button[type=submit]").click();
   await page.getByText("опечатка",{exact:false}).first().waitFor();
   const panel=await page.locator(".life-answer-feedback").innerText();
   if(panel.includes("Не хватает формы"))throw Error("False missing-article diagnosis");
   if(!panel.includes("Λεθκώσια")||!panel.includes("Λευκωσία"))
     throw Error("No precise correction of the city name");
   if(await page.locator(".life-feedback-greek").textContent()!=="Μένω στην Λευκωσία.")
     throw Error("Did not show nearest accepted form");
   if(!panel.includes("Я живу в Никосии"))throw Error("Missing Russian translation");
   await page.locator(".life-answer-form textarea").fill("Μένω Λευκωσία");
   await page.locator(".life-answer-form button[type=submit]").click();
   await page.getByText("артикль",{exact:false}).first().waitFor();
   await page.locator(".life-answer-form textarea").fill("Μένω στην Λευκωσία");
   await page.locator(".life-answer-form button[type=submit]").click();
   await page.getByText("Отлично! Тебя поняли.",{exact:false}).waitFor();
   await page.getByText("Другие допустимые формулировки",{exact:true}).waitFor();
   await page.locator(".life-task-actions .life-continue").click();
   await page.locator(".life-task-prompt").getByText("У меня есть",{exact:false}).waitFor();
   const finishTask=async(phrase)=>{
     await page.locator(".life-answer-form textarea").fill(phrase);
     await page.locator(".life-answer-form button[type=submit]").click();
     await page.getByText("Отлично! Тебя поняли.",{exact:false}).waitFor();
     await page.locator(".life-task-actions .life-continue").click();
   };
   await finishTask("Έχω έναν αδελφό.");
   await page.locator(".life-task-prompt").getByText("Я говорю по-гречески",{exact:false}).waitFor();
   await finishTask("Μιλάω ελληνικά.");
   await page.locator(".route-map svg").waitFor();
   if(await page.locator("#life-activity-controls").isVisible())throw Error("Activity picker exposed");
   const fields={
     number:"πενήντα πέντε",origin:"το σχολείο",via1:"το κέντρο",
     via2:"το πανεπιστήμιο",stop:"Σπίτι",destination:"την τράπεζα"
   };
   for(const [key,value] of Object.entries(fields))
     await page.locator('.route-answer-form input[name="'+key+'"]').fill(value);
   await page.locator(".route-answer-form button[type=submit]").click();
   await page.getByText("Маршрут описан правильно!",{exact:false}).waitFor();
   await page.locator(".track-route-feedback button.primary").click();
   await page.locator(".life-task-prompt").getByText("билет до Лимасола",{exact:false}).waitFor();
   await finishTask("Ένα εισιτήριο για τη Λεμεσό.");
   await page.locator(".life-task-prompt").waitFor();

   await page.locator('[data-page="tracks"]').click();
   await page.locator(".track-word-card .track-meaning").waitFor();
   await page.locator('[data-page="life"]').click();
   await page.locator(".life-adventure-card").waitFor();
   await page.locator("#life-max-chapter").selectOption("8");
   await page.waitForFunction(()=>document.querySelector("#life-max-chapter").value==="8");
   await page.locator(".life-adventure-title").getByText("Мой день",{exact:false}).waitFor();
   await page.locator(".life-adventure-card svg").waitFor();
   if(await page.locator("#life-activity-controls").isVisible())throw Error("Categories shown after scope change");
   await page.locator(".life-adventure-card .life-continue").click();
   await page.locator(".life-task-prompt").getByText("завтракаю в восемь",{exact:false}).waitFor();
   await finishTask("Τρώω πρωινό στις οκτώ.");
   await page.locator(".life-task-prompt").getByText("килограмм помидоров",{exact:false}).waitFor();
   await finishTask("Θέλω ένα κιλό ντομάτες, παρακαλώ.");
   await page.locator(".shop-list .shop-item").first().waitFor();
   if(await page.locator(".shop-list .shop-item").count()!==4)throw Error("Marketplace should show four items");
   const purchases={
      apple:"Θέλω ένα μήλο, παρακαλώ.",milk:"Θέλω ένα λίτρο γάλα, παρακαλώ.",
      water:"Θέλω ένα μπουκάλι νερό, παρακαλώ.",bread:"Θέλω ένα ψωμί, παρακαλώ."
   };
   for(const [index,[product,value]] of Object.entries(purchases).entries()){
     const item=page.locator(".shop-list .shop-item").filter({has:page.locator('input')}).first();
     await item.locator("input").fill(value);
     await item.locator("button[type=submit]").click();
     await page.getByText("В корзине: "+(index+1)+"/4",{exact:false}).waitFor();
   }
   await page.getByText("Все четыре покупки собраны!",{exact:false}).waitFor();
   await page.locator("#life-content button.primary.track-button").click();
   await page.locator(".life-task-prompt").waitFor();
   const top=await page.locator(".life-head").boundingBox();
   if(!top||top.width<300)throw Error("Mobile hero too narrow");
   for(const width of [390,360,320,768,1200]){
     await page.setViewportSize({width,height:900});
     await page.waitForTimeout(80);
     const layout=await page.evaluate(()=>({
       extra:document.documentElement.scrollWidth-document.documentElement.clientWidth,
       overflow:document.querySelector("#life-view")?.scrollWidth-
         document.querySelector("#life-view")?.clientWidth
     }));
     if(layout.extra>3||layout.overflow>3)throw Error("Horizontal overflow "+width+" "+JSON.stringify(layout));
   }
   if(errors.length)throw Error("Browser runtime errors: "+JSON.stringify(errors));
   console.log("PASS Anki Pocket WAV normal/slow playback, then Greek Life adaptive journey and 320–1200px");
   await ctx.close();
 }finally{await browser.close();}
})().catch(err=>{console.error("FAIL "+err.stack);process.exitCode=1});
