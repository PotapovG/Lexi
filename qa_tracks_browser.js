"use strict";
const {chromium}=require("/app/qa_deps/node_modules/playwright");
(async()=>{
  const browser=await chromium.launch({headless:true,args:["--no-sandbox","--disable-dev-shm-usage"]});
  try{
    const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
    await context.addCookies([{name:"greek_session",value:process.env.QA_TOKEN,
       url:"http://127.0.0.1:18632/greek/",httpOnly:true,secure:false,sameSite:"Lax"}]);
    const page=await context.newPage();
    const errors=[];page.on("pageerror",e=>errors.push(e.message));
    await page.goto("http://127.0.0.1:18632/greek/",{waitUntil:"networkidle"});
    await page.locator("#auth-gate").waitFor({state:"hidden",timeout:10000});
    await page.locator('[data-page="tracks"]').click();
    await page.locator("#tracks-view").waitFor({state:"visible"});
    await page.locator(".track-word-card .track-meaning").waitFor();
    const first=await page.locator(".track-word-card .track-greek").textContent();
    if(!first)throw Error("Missing Greek preview word");
    await page.locator(".track-word-card button.primary").click();
    await page.getByText("2/30",{exact:false}).first().waitFor();
    await page.locator('[data-page="life"]').click();
    await page.locator("#life-view").waitFor({state:"visible"});
    await page.waitForFunction(()=>document.querySelector("#life-max-chapter").value==="6",{timeout:10000});
    if(await page.locator("#life-max-chapter").inputValue()!=="6")
      throw Error("Greek Life initial stage not chapter 6");
    if(!await page.locator("#track-periptero-mode").isHidden())
      throw Error("Shopping shown before chapter 8");
    await page.locator("#life-max-chapter").selectOption("16");
    await page.locator("#track-periptero-mode").waitFor({state:"visible"});
    await page.locator("#track-likes-mode").waitFor({state:"visible"});
    await page.locator(".life-scene").filter({hasText:"Где ты живёшь?"}).locator("button").click();
    await page.locator(".life-form textarea").fill("Μένω Λευκωσία");
    await page.locator(".life-form button[type=submit]").click();
    await page.getByText("артикль",{exact:false}).first().waitFor();
    await page.locator(".life-form textarea").fill("Μένω στη Λευκωσία");
    await page.locator(".life-form button[type=submit]").click();
    await page.getByText("Верно! Фраза засчитана.",{exact:false}).waitFor();
    await page.locator(".life-form .primary.track-button").last().click();
    await page.locator(".life-scene").first().waitFor();
    await page.locator("#track-route-mode").click();
    await page.locator(".route-map svg").waitFor();
    if(await page.locator(".route-map svg circle").count()!==5)
      throw Error("Not five stops");
    if(await page.locator(".route-bus").textContent()!=="55")
      throw Error("Bus number not shown");
    const route={number:"πενήντα πέντε",origin:"το σχολείο",
       via1:"το κέντρο",via2:"το πανεπιστήμιο",stop:"Σπίτι",destination:"την τράπεζα"};
    for(const [name,value] of Object.entries(route))
      await page.locator('input[name="'+name+'"]').fill(value);
    await page.locator(".route-answer-form button[type=submit]").click();
    await page.getByText("Маршрут описан правильно!",{exact:false}).waitFor();
    await page.getByText("Следующий маршрут",{exact:false}).click();
    await page.locator(".route-bus").waitFor();
    if(await page.locator(".route-bus").textContent()==="55")
      throw Error("New route not loaded");
    await page.locator("#track-likes-mode").click();
    await page.locator(".track-like-form input").waitFor();
    await page.locator(".track-like-form input").fill("μου αρέσει να διαβάζω");
    await page.locator(".track-like-form button[type=submit]").click();
    await page.getByText("✓ Верно",{exact:false}).waitFor();
    await page.locator(".track-like-form button").last().click();
    await page.getByText("Мне не нравится читать.",{exact:false}).waitFor();
    await page.locator("#track-periptero-mode").click();
    await page.locator(".shop-list .shop-item").first().waitFor();
    if(await page.locator(".shop-list .shop-item").count()!==4)
      throw Error("Shopping list not four items");
    const input=page.locator(".shop-list .shop-item").first().locator("input");
    await input.fill("Θα ήθελα ένα μήλο, παρακαλώ.");
    await page.locator(".shop-list .shop-item").first().locator("button[type=submit]").click();
    await page.getByText("В корзине: 1/4",{exact:false}).waitFor();
    await page.locator('[data-page="tracks"]').click();
    await page.locator(".track-word-card").waitFor();
    await page.locator('[data-page="life"]').click();
    await page.locator("#track-periptero-mode").click();
    await page.getByText("В корзине: 1/4",{exact:false}).waitFor();
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
    if(overflow>2)throw Error("Mobile page horizontal overflow "+overflow);
    if(errors.length)throw Error("Browser JS errors: "+JSON.stringify(errors));
    console.log("PASS mobile Greek Life chapter scope, roleplay error explanations, routes, likes, store and Anki resume");
    await context.close();
  }finally{await browser.close();}
})().catch(e=>{console.error("FAIL "+e.stack);process.exitCode=1});
