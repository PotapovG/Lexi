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
    await page.locator("#track-route-mode").click();
    await page.locator(".route-map svg").waitFor();
    if(await page.locator(".route-map svg circle").count()!==5)throw Error("Not five stops");
    if(await page.locator(".route-bus").textContent()!=="55")throw Error("Bus number not shown");
    const route={number:"πενήντα πέντε",origin:"το σχολείο",via1:"το πάρκο",
       via2:"το νοσοκομείο",stop:"Κέντρο",destination:"το μουσείο"};
    for(const [name,value] of Object.entries(route)){
      await page.locator('input[name="'+name+'"]').fill(value);
    }
    await page.locator(".route-answer-form button[type=submit]").click();
    await page.getByText("Маршрут описан правильно!",{exact:false}).waitFor();
    await page.getByText("Следующий маршрут",{exact:false}).click();
    await page.locator(".route-bus").waitFor();
    if(await page.locator(".route-bus").textContent()==="55")throw Error("New route not loaded");
    await page.locator("#track-likes-mode").click();
    await page.locator(".track-like-form input").waitFor();
    await page.locator(".track-like-form input").fill("μου αρέσει να διαβάζω");
    await page.locator(".track-like-form button[type=submit]").click();
    await page.getByText("✓ Верно",{exact:false}).waitFor();
    await page.locator(".track-like-form button").last().click();
    await page.getByText("Мне не нравится читать.",{exact:false}).waitFor();
    await page.locator("#track-periptero-mode").click();
    await page.locator(".shop-list .shop-item").first().waitFor();
    if(await page.locator(".shop-list .shop-item").count()!==4)throw Error("Shopping list not four items");
    const input=page.locator(".shop-list .shop-item").first().locator("input");
    await input.fill("Θα ήθελα ένα μήλο, παρακαλώ.");
    await page.locator(".shop-list .shop-item").first().locator("button[type=submit]").click();
    await page.getByText("В корзине: 1/4",{exact:false}).waitFor();
    await page.locator("#track-anki-mode").click();
    await page.locator(".track-word-card").waitFor();
    await page.locator("#track-periptero-mode").click();
    await page.getByText("В корзине: 1/4",{exact:false}).waitFor();
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
    if(overflow>2)throw Error("Mobile page horizontal overflow "+overflow);
    if(errors.length)throw Error("Browser JS errors: "+JSON.stringify(errors));
    console.log("PASS actual Chromium mobile: 30-card preview persisted, route typing, likes, Periptero basket and cross-mode resume");
    await context.close();
  }finally{await browser.close();}
})().catch(e=>{console.error("FAIL "+e.stack);process.exitCode=1});
