/* Open-disclosure visual and keyboard regression against an isolated real server.
 * One synthetic account; no learner APIs are mocked and no answers are submitted.
 * Run: LEXI_BASE_URL=http://localhost:18560 node tests/test_navigation_ui.cjs
 * LEXI_ARTIFACT_DIR saves masked synthetic screenshots and measured geometry/colors.
 * LEXI_NAV_DIAGNOSTIC=1 records old-release visual defects without failing on them.
 */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const {chromium}=require("playwright");
const base=process.env.LEXI_BASE_URL||"http://localhost:18560";
const artifactDir=process.env.LEXI_ARTIFACT_DIR;
const diagnostic=process.env.LEXI_NAV_DIAGNOSTIC==="1";
assert.ok(["localhost","127.0.0.1","[::1]"].includes(new URL(base).hostname),
  "Navigation regression requires a disposable loopback server.");
const failures=[],metrics=[];
function check(ok,label,detail){if(!ok)failures.push(label+(detail===undefined?"":": "+JSON.stringify(detail)));}

// Read the painted colors, including transparent backgrounds inherited from ancestors.
function measureNavigation(){
  const more=document.querySelector("#additional-modes"),menu=more.querySelector(".tab-more-menu");
  const summary=more.querySelector("summary");
  function rgba(value){
    const numbers=value.match(/[\d.]+/g)?.map(Number)||[];
    if(value.startsWith("color(srgb"))return [...numbers.slice(0,3).map(x=>x*255),numbers[3]??1];
    return [numbers[0]||0,numbers[1]||0,numbers[2]||0,numbers[3]??1];
  }
  function over(a,b){
    const alpha=a[3]+b[3]*(1-a[3]);
    return alpha?[...a.slice(0,3).map((x,i)=>(x*a[3]+b[i]*b[3]*(1-a[3]))/alpha),alpha]:[0,0,0,0];
  }
  function background(el){
    const chain=[];for(let node=el;node;node=node.parentElement)chain.unshift(node);
    return chain.reduce((color,node)=>over(rgba(getComputedStyle(node).backgroundColor),color),[255,255,255,1]);
  }
  function luminance(color){
    return color.slice(0,3).map(x=>x/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4)
      .reduce((sum,x,i)=>sum+x*[.2126,.7152,.0722][i],0);
  }
  function contrast(a,b){const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
  function rect(el){const r=el.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height};}
  const focus=getComputedStyle(summary),outside=background(summary.parentElement);
  return {
    width:innerWidth,height:innerHeight,scrollWidth:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth),
    direction:document.documentElement.dir,open:more.open,menu:rect(menu),anchor:rect(more),
    menuScrollHeight:menu.scrollHeight,menuClientHeight:menu.clientHeight,
    focus:{visible:summary.matches(":focus-visible"),width:parseFloat(focus.outlineWidth)||0,
      contrast:contrast(over(rgba(focus.outlineColor),outside),outside),color:focus.outlineColor},
    rows:[...menu.querySelectorAll(".tab")].filter(el=>el.getClientRects().length).map(el=>{
      const style=getComputedStyle(el),bg=background(el),fg=over(rgba(style.color),bg);
      return {page:el.dataset.page,active:el.classList.contains("active"),rect:rect(el),
        contrast:contrast(fg,bg),color:style.color,background:bg.slice(0,3)};
    })
  };
}
(async()=>{
  const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
  const context=await browser.newContext({viewport:{width:1280,height:900},locale:"ru",colorScheme:"light",reducedMotion:"reduce"});
  const page=await context.newPage(),errors=[];
  page.setDefaultTimeout(15000);
  page.on("pageerror",error=>errors.push(error.message));
  const more=page.locator("#additional-modes"),summary=more.locator(":scope > summary");
  const account=page.locator("#account-menu");
  async function isOpen(locator){return locator.evaluate(el=>el.open);}
  async function shot(name){
    if(!artifactDir)return;
    fs.mkdirSync(artifactDir,{recursive:true});
    await page.screenshot({path:path.join(artifactDir,name+".png"),
      mask:[page.locator("#auth-created-code:visible,#account-code:visible,#auth-input-code:visible")]});
  }
  async function closeMore(){if(await isOpen(more))await summary.click();}
  async function openMore(){
    await closeMore();
    await summary.focus();await page.keyboard.press("Enter");
    await page.waitForFunction(()=>document.querySelector("#additional-modes").open);
    // A newly opened native details subtree needs a completed paint before style measurements.
    await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
  }
  async function configure({locale,theme,width,height}){
    await closeMore();
    if(await isOpen(account))await account.locator(":scope > summary").click();
    await page.setViewportSize({width,height});
    await page.locator("#lang").selectOption(locale);
    await page.waitForFunction(locale=>document.documentElement.lang===locale,locale);
    await account.locator(":scope > summary").click();
    await page.locator("#theme-select").selectOption(theme);
    await account.locator(":scope > summary").click();
    await page.locator('.tabs > .tab[data-page="vocab"]').click();
    await page.locator("#vocab-view").waitFor({state:"visible"});
    await page.locator("#vocab-topic option").first().waitFor({state:"attached"});
    await page.evaluate(()=>window.scrollTo(0,0));
    await page.mouse.move(0,0);
  }
  function verify(label,value){
    check(value.open,label+" disclosure is open");
    check(value.scrollWidth<=value.width+1,label+" document has no horizontal overflow",value.scrollWidth);
    check(value.menu.left>=-1&&value.menu.right<=value.width+1,label+" popup fits viewport horizontally",value.menu);
    check(value.menu.top>=-1&&value.menu.bottom<=value.height+1,label+" popup fits viewport vertically",value.menu);
    const edge=value.direction==="rtl"?"left":"right";
    check(Math.abs(value.menu[edge]-value.anchor[edge])<=1.5,label+" popup follows logical end anchor",{menu:value.menu[edge],anchor:value.anchor[edge]});
    check(value.focus.visible&&value.focus.width>=2,label+" keyboard focus ring is visible",value.focus);
    check(value.focus.contrast>=3,label+" focus ring contrast >= 3",value.focus);
    check(value.rows.length>=6,label+" existing menu destinations remain available",value.rows.length);
    for(const row of value.rows){
      check(row.contrast>=4.5,label+" "+row.page+" text contrast >= 4.5",row);
      check(row.rect.height>=44-.5,label+" "+row.page+" target remains at least 44px",row.rect.height);
      check(row.rect.left>=value.menu.left-1&&row.rect.right<=value.menu.right+1,label+" "+row.page+" fits popup width",row.rect);
    }
  }
  try{
    await page.goto(base+"/greek/");
    await page.locator("#auth-gate").waitFor({state:"visible"});
    await page.locator("#auth-lang").selectOption("ru");
    await page.locator("#auth-name").fill("Navigation QA "+Date.now().toString(36));
    await page.locator("#auth-submit").click();
    await page.locator("#auth-success").waitFor({state:"visible"});
    await page.locator("#auth-enter").click();
    await page.locator(".lesson-resume").waitFor();
    await page.waitForFunction(()=>window.LexiApp?.loggedIn()&&!document.querySelector(".site").inert);

    const cases=[];
    for(const locale of ["ru","ar"])for(const theme of ["light","dark"])
      for(const width of [320,360,768,1280])cases.push({locale,theme,width,height:width>=768?900:780});
    cases.push({locale:"es",theme:"light",width:320,height:780},{locale:"pt",theme:"dark",width:360,height:780},
      {locale:"ru",theme:"light",width:480,height:320},{locale:"ar",theme:"dark",width:480,height:320});
    for(const config of cases){
      const label=[config.locale,config.theme,config.width,config.height].join("-");
      await configure(config);await openMore();
      const value=await page.evaluate(measureNavigation);metrics.push({label,...value});verify(label,value);
      if((config.locale==="ru"&&config.width===1280&&config.theme==="light")||
         (config.locale==="ru"&&config.width===360)||
         (config.locale==="ar"&&config.width===360&&config.theme==="light"))
        await shot("navigation-"+label);
      if(!diagnostic){
        // Every destination must remain reachable inside a short scrolling popup.
        const rows=more.locator(".tab:visible");
        for(const row of await rows.all()){
          await row.scrollIntoViewIfNeeded();
          const geometry=await row.evaluate(el=>{
            const row=el.getBoundingClientRect(),menu=el.closest(".tab-more-menu").getBoundingClientRect();
            return {page:el.dataset.page,top:row.top,bottom:row.bottom,menuTop:menu.top,menuBottom:menu.bottom,height:innerHeight};
          });
          check(geometry.top>=Math.max(0,geometry.menuTop)-1&&geometry.bottom<=Math.min(geometry.height,geometry.menuBottom)+1,
            label+" destination is fully reachable",geometry);
        }
        await rows.first().scrollIntoViewIfNeeded();await rows.first().hover();
        const hovered=(await page.evaluate(measureNavigation)).rows[0];
        check(hovered.contrast>=4.5,label+" hover text contrast >= 4.5",hovered);
      }
      await closeMore();
    }

    if(!diagnostic){
      await configure({locale:"ru",theme:"light",width:1280,height:900});
      await openMore();await page.keyboard.press("Tab");
      check(await more.evaluate(el=>el.querySelector(".tab-more-menu").contains(document.activeElement)),
        "Tab enters an open disclosure");
      await page.keyboard.press("Escape");
      check(!await isOpen(more),"Escape closes More");
      check(await summary.evaluate(el=>el===document.activeElement),"Escape restores focus to More summary");

      await openMore();await page.locator("#vocab-topic").click();
      check(!await isOpen(more),"Outside click closes More");
      check(await page.locator("#vocab-topic").evaluate(el=>el===document.activeElement),
        "Outside click retains destination focus");
      await page.keyboard.press("Escape"); // Dismiss a native select popup if the browser opened it.
      // A deliberate Tab departure dismisses the menu without redirecting the user's focus.
      await openMore();await more.locator(".tab:visible").last().focus();
      await page.keyboard.press("Tab");
      await page.waitForFunction(()=>!document.querySelector("#additional-modes").open);
      check(!await more.evaluate(el=>el.contains(document.activeElement)),
        "Tab departure keeps focus outside More");

      await openMore();await account.locator(":scope > summary").click();
      await page.waitForFunction(()=>document.querySelector("#account-menu").open&&!document.querySelector("#additional-modes").open);
      check(!await isOpen(more),"Opening Account closes More");

      // Delayed content rendering can focus a background heading; that is not a user dismissal.
      await page.locator("#vocab-title").evaluate(el=>{el.tabIndex=-1;el.focus();});
      await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
      check(await page.locator("#vocab-title").evaluate(el=>el===document.activeElement),
        "Regression probe really moved focus to the background heading");
      check(await isOpen(account),"Background content focus does not close Account");
      check(await page.locator("#account-logout").isVisible(),"Logout remains visible after background focus");
      await page.locator("#account-logout").click({trial:true}); // Check actionability without logging out.
      await account.locator(":scope > summary").focus();await page.keyboard.press("Escape");
      await page.waitForFunction(()=>!document.querySelector("#account-menu").open);
      check(await account.locator(":scope > summary").evaluate(el=>el===document.activeElement),
        "Account Escape returns focus to its summary");

      await account.locator(":scope > summary").click();
      await page.waitForFunction(()=>document.querySelector("#account-menu").open);
      // The account popover can cover navigation; ordinary focus + Enter opens More explicitly.
      await summary.focus();await page.keyboard.press("Enter");
      await page.waitForFunction(()=>document.querySelector("#additional-modes").open&&!document.querySelector("#account-menu").open);
      check(!await isOpen(account),"Opening More closes Account");

      await more.locator('.tab[data-page="stats"]').click();
      await page.locator("#stats-view").waitFor({state:"visible"});
      check(!await isOpen(more),"Selecting a destination closes More");
      check(!await page.locator("#vocab-view").isVisible(),"Selecting Statistics leaves Vocabulary");
      await openMore();
      const selected=(await page.evaluate(measureNavigation)).rows.find(row=>row.page==="stats");
      check(selected?.active&&selected.contrast>=4.5,"Current destination is selected and readable",selected);
      check(await more.locator('.tab[data-page="stats"]').getAttribute("aria-current")==="page",
        "Current destination is exposed to assistive technology");
      await page.keyboard.press("Escape");
      check(!await isOpen(more),"Selected menu can be dismissed");
    }
    check(errors.length===0,"Navigation causes no uncaught browser errors",errors);
    if(artifactDir){
      fs.mkdirSync(artifactDir,{recursive:true});
      fs.writeFileSync(path.join(artifactDir,"navigation-metrics.json"),JSON.stringify({diagnostic,metrics,failures,errors},null,2)+"\n");
    }
    if(diagnostic)console.log("DIAGNOSTIC navigation: "+cases.length+" layouts, "+failures.length+" visual failures; metrics retained.");
    else{
      assert.deepEqual(failures,[],"Open navigation regression: "+failures.join("\n"));
      console.log("PASS navigation: "+cases.length+" open-menu layouts; light/dark contrast, logical anchors, 44px targets, scrolling, focus, Escape/outside dismissal, selection and exclusive disclosures.");
    }
  }catch(error){
    if(artifactDir){
      fs.mkdirSync(artifactDir,{recursive:true});
      fs.writeFileSync(path.join(artifactDir,"navigation-metrics.json"),
        JSON.stringify({diagnostic,metrics,failures,errors,error:error.message},null,2)+"\n");
    }
    await shot("navigation-failure").catch(()=>{});
    throw error;
  }finally{
    await context.close();await browser.close();
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
