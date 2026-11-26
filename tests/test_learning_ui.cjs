/* Browser integration checks against a disposable Lexi server and synthetic account.
 * No mocked learner API: the lost-response case commits at the real server.
 * Run: LEXI_BASE_URL=http://localhost:18560 node tests/test_learning_ui.cjs
 * Optional LEXI_ARTIFACT_DIR saves synthetic screenshots outside the checkout.
 */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const {spawnSync}=require("node:child_process");
const { chromium } = require("playwright");
const base = process.env.LEXI_BASE_URL || "http://localhost:18560";
const artifactDir = process.env.LEXI_ARTIFACT_DIR;
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function testAccountSwitch(browser){
  const errors=[],writes=[],stamp=Date.now().toString(36);
  const created=[];
  let releaseProfiles=()=>{},releaseOldAnswer=()=>{};
  const collect=page=>page.on("pageerror",error=>errors.push(error.stack||error.message));
  async function register(page,nickname){
    collect(page);await page.goto(base+"/greek/");
    await page.locator("#auth-gate").waitFor({state:"visible"});
    await page.locator("#auth-lang").selectOption("en");
    await page.locator("#auth-name").fill(nickname);await page.locator("#auth-submit").click();
    await page.locator("#auth-success").waitFor({state:"visible"});
    const code=(await page.locator("#auth-created-code").textContent()).trim();
    await page.locator("#auth-enter").click();
    await page.waitForFunction(()=>window.LexiApp?.loggedIn()&&/^[a-f0-9]{32}$/.test(window.LexiApp.accountKey()||""));
    await page.locator(".lesson-resume").waitFor();
    return {code,owner:await page.evaluate(()=>window.LexiApp.accountKey())};
  }
  try{
    const prepared=await browser.newContext();created.push(prepared);
    const accountB=await register(await prepared.newPage(),"Auth B "+stamp);
    await prepared.close();
    const shared=await browser.newContext();created.push(shared);
    const tabA=await shared.newPage();
    const accountA=await register(tabA,"Auth A "+stamp);
    assert.notEqual(accountA.owner,accountB.owner);
    await tabA.evaluate(()=>{
      window.accountTransitions=[];
      document.addEventListener("lexi:logout",()=>window.accountTransitions.push({owner:window.LexiApp.accountKey(),loggedIn:window.LexiApp.loggedIn()}));
    });
    tabA.on("request",request=>{
      if(request.method()==="POST"&&!new URL(request.url()).pathname.includes("/auth/"))
        writes.push({path:new URL(request.url()).pathname,owner:request.headers()["x-lexi-owner"]});
    });
    await tabA.locator(".lesson-resume button").click();
    await tabA.locator('.lesson-answer-form input[type="radio"]').first().check();
    let committed;
    const committedAnswer=new Promise(resolve=>{committed=resolve;});
    const oldAnswerGate=new Promise(resolve=>{releaseOldAnswer=resolve;});
    let heldAnswer=false;
    await tabA.route("**/greek/api/board",async route=>{
      const request=route.request(),body=request.method()==="POST"?request.postDataJSON():null;
      if(body?.action==="answer"&&!heldAnswer){
        heldAnswer=true;const response=await route.fetch();assert.equal(response.status(),200);
        committed();await oldAnswerGate;return route.fulfill({response});
      }
      return route.continue();
    });
    await tabA.locator('.lesson-answer-form button[type="submit"]').click();await committedAnswer;
    let profileCaptured;
    const capturedProfile=new Promise(resolve=>{profileCaptured=resolve;});
    const profileGate=new Promise(resolve=>{releaseProfiles=resolve;});
    let firstProfile=true;
    await tabA.route("**/greek/api/profile",async route=>{
      const response=await route.fetch();
      if(firstProfile){firstProfile=false;assert.equal((await response.json()).accountKey,accountA.owner);profileCaptured();}
      await profileGate;return route.fulfill({response});
    });
    await tabA.evaluate(()=>window.dispatchEvent(new Event("focus")));await capturedProfile;

    const tabB=await shared.newPage();collect(tabB);tabB.on("dialog",dialog=>dialog.accept());
    await tabB.goto(base+"/greek/");
    await tabB.waitForFunction(owner=>window.LexiApp?.accountKey()===owner,accountA.owner);
    await tabB.locator("#account-menu summary").click();await tabB.locator("#account-logout").click();
    await tabB.locator("#auth-gate").waitFor({state:"visible"});
    await tabA.waitForFunction(()=>!window.LexiApp.loggedIn()&&window.LexiApp.accountKey()===null&&document.querySelector(".site").inert);
    assert.equal(await tabA.locator(".lesson-answer-form").count(),0,"old account question is removed synchronously");
    await tabB.locator("#mode-login").click();await tabB.locator("#auth-input-code").fill(accountB.code);await tabB.locator("#auth-submit").click();
    await tabB.waitForFunction(owner=>window.LexiApp.accountKey()===owner&&window.LexiApp.loggedIn(),accountB.owner);
    await tabA.waitForFunction(()=>window.accountTransitions.length>=2);
    const countBefore=writes.length;
    const blocked=await tabA.evaluate(async owner=>{
      try{await window.LexiApp.api("ai/erase",{method:"POST",headers:{"Content-Type":"application/json","X-Lexi-Owner":owner},body:JSON.stringify({confirm:true})});return {};}
      catch(error){return {status:error.status,error:error.message};}
    },accountA.owner);
    assert.deepEqual(blocked,{status:409,error:"account_changed"});
    assert.equal(writes.length,countBefore,"stale tab cannot write while owner confirmation is pending");
    assert.equal(await tabA.evaluate(()=>window.accountTransitions.every(event=>event.owner===null&&!event.loggedIn)),true,"identity is invalidated before lifecycle callbacks");

    releaseProfiles();
    await tabA.waitForFunction(owner=>window.LexiApp.accountKey()===owner&&window.LexiApp.loggedIn()&&!document.querySelector(".site").inert,accountB.owner);
    await tabA.locator(".lesson-resume button").waitFor();
    assert.equal(await tabA.locator("#student-nickname").textContent(),"Auth B "+stamp);
    // B must load before the still-pending A request is allowed to settle.
    const oldDelivered=tabA.waitForResponse(response=>new URL(response.url()).pathname==="/greek/api/board"&&response.request().method()==="POST"&&response.request().postDataJSON().action==="answer");
    releaseOldAnswer();await oldDelivered;await sleep(100);
    assert.equal(await tabA.evaluate(()=>window.LexiApp.accountKey()),accountB.owner);
    assert.equal(await tabA.locator(".lesson-resume").isVisible(),true,"late A finally does not leave B blank or reopen A");
    assert.equal(await tabA.locator("#lesson-feedback").count(),0,"late A feedback cannot paint into B");
    await tabA.unroute("**/greek/api/profile");await tabA.unroute("**/greek/api/board");

    // Explicit owner supplied by an old immutable context must survive api's header merge.
    const guarded=await tabA.evaluate(async owner=>{
      try{await window.LexiApp.api("ai/erase",{method:"POST",headers:{"Content-Type":"application/json","X-Lexi-Owner":owner},body:JSON.stringify({confirm:true})});return {};}
      catch(error){return {status:error.status,error:error.message};}
    },accountA.owner);
    assert.deepEqual(guarded,{status:409,error:"account_changed"});
    assert.equal(writes.filter(item=>item.path.endsWith("/ai/erase")).at(-1).owner,accountA.owner);
    assert.equal(await tabA.evaluate(()=>window.LexiApp.accountKey()),accountB.owner);
    await tabA.locator(".lesson-resume button").click();
    await tabA.locator('.lesson-answer-form input[type="radio"]').first().check();
    assert.equal(writes.filter(item=>item.path.endsWith("/board")).at(-1).owner,accountB.owner,"new ordinary writes carry B owner");
    const selected=await tabA.locator('.lesson-answer-form input:checked').inputValue();
    const prompt=await tabA.locator(".lesson-question-prompt").textContent();
    const transitions=await tabA.evaluate(()=>window.accountTransitions.length);
    const sameOwnerProbe=tabA.waitForResponse(response=>new URL(response.url()).pathname==="/greek/api/profile");
    await tabA.evaluate(()=>window.dispatchEvent(new Event("focus")));await sameOwnerProbe;await sleep(30);
    assert.equal(await tabA.locator('.lesson-answer-form input:checked').inputValue(),selected);
    assert.equal(await tabA.locator(".lesson-question-prompt").textContent(),prompt);
    assert.equal(await tabA.evaluate(()=>window.accountTransitions.length),transitions,"same-owner focus preserves the draft and session");

    // A cookie change without a storage event is reconciled on focus as well.
    const login=await tabB.evaluate(async code=>{
      const response=await fetch("/greek/api/auth/login",{method:"POST",credentials:"same-origin",headers:{"Content-Type":"application/json"},body:JSON.stringify({code})});
      return response.status;
    },accountA.code);
    assert.equal(login,200);
    await tabA.evaluate(()=>window.dispatchEvent(new Event("focus")));
    await tabA.waitForFunction(owner=>window.LexiApp.accountKey()===owner&&window.LexiApp.loggedIn(),accountA.owner);
    assert.equal(await tabA.locator("#student-nickname").textContent(),"Auth A "+stamp);
    const staleLogout=await tabB.evaluate(async()=>{
      try{await window.LexiApp.api("auth/logout",{method:"POST",headers:{"Content-Type":"application/json"},body:"{}"});return {};}
      catch(error){return {status:error.status,error:error.message};}
    });
    assert.deepEqual(staleLogout,{status:409,error:"account_changed"},"stale B cannot log out current A");
    assert.deepEqual(errors,[],"two-tab owner transition has no uncaught exceptions");
    console.log("PASS: real two-tab account switch; immediate inert invalidation; stale profile/answer generation guards; immutable AI/core owner headers; same-owner focus preserves draft; cookie-only focus refresh; stale logout rejected.");
  }finally{
    releaseProfiles();releaseOldAnswer();
    for(const context of created)await context.close().catch(()=>{});
  }
}

(async () => {
  const browser = await chromium.launch({headless:true,args:["--no-sandbox"]});
  const context = await browser.newContext({viewport:{width:1280,height:900},locale:"en",colorScheme:"light"});
  const page = await context.newPage();
  const errors = [];
  const nickname="UI check "+Date.now().toString(36);
  page.on("pageerror", error => errors.push(error.stack||error.message));
  page.setDefaultTimeout(15000);
  const api = (endpoint,body) => page.evaluate(async ({endpoint,body}) => {
    const response = await fetch("/greek/api/"+endpoint,{credentials:"same-origin",cache:"no-store",...(body?{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)}:{})});
    return {status:response.status,data:await response.json()};
  },{endpoint,body});
  const board = async () => {const response=await api("board?lang="+await page.locator("#lang").inputValue());assert.equal(response.status,200);return response.data;};
  const noOverflow = async label => {
    const layout = await page.evaluate(() => ({width:innerWidth,body:document.documentElement.scrollWidth}));
    assert.ok(layout.body<=layout.width+1,label+": horizontal overflow "+JSON.stringify(layout));
  };
  const shot = async name => {
    if(!artifactDir)return;
    fs.mkdirSync(artifactDir,{recursive:true});
    await page.screenshot({path:path.join(artifactDir,name+".png"),fullPage:true});
  };
  async function chooseVisible(waitForFeedback=true) {
    const form=page.locator(".lesson-answer-form");
    const typed=form.locator("#lesson-typed-answer");
    if(await typed.count()){
      await typed.fill("δοκιμή");
    }else if(await form.locator(".lesson-order-pool").count()){
      while(await form.locator(".lesson-order-pool button:not(:disabled)").count())await form.locator(".lesson-order-pool button:not(:disabled)").first().click();
    }else{
      await form.locator('input[type="radio"]').first().check();
    }
    await form.locator('button[type="submit"]').click();
    if(waitForFeedback)await page.locator("#lesson-feedback").waitFor({state:"visible"});
  }
  async function advanceFeedback(){
    const old=await page.locator("#lesson-feedback").textContent();
    await page.locator("#lesson-feedback button.primary").click();
    await page.waitForFunction(previous=>{
      const summary=document.querySelector(".lesson-summary");
      return Boolean(summary)||document.querySelector("#lesson-feedback")?.hidden===true||document.querySelector("#lesson-feedback")?.textContent!==previous;
    },old);
  }
  try{
    if(process.env.LEXI_UI_CASE==="account-switch"){await testAccountSwitch(browser);return;}
    await page.goto(base+"/greek/");
    await page.locator("#auth-gate").waitFor({state:"visible"});
    assert.equal(await page.locator(".site").evaluate(el=>el.inert),true);
    for(let index=0;index<18;index++){
      await page.keyboard.press(index%4===0?"Shift+Tab":"Tab");
      assert.equal(await page.evaluate(()=>document.querySelector("#auth-gate").contains(document.activeElement)),true,"auth focus stays inside");
    }
    await page.locator("#auth-lang").selectOption("en");
    await page.locator("#mode-login").click();
    assert.equal(await page.evaluate(()=>document.activeElement.id),"auth-input-code");
    await page.locator("#mode-register").click();
    assert.equal(await page.evaluate(()=>document.activeElement.id),"auth-name");
    await page.locator("#auth-name").fill(nickname);
    await page.locator("#auth-submit").click();
    await page.locator("#auth-success").waitFor({state:"visible"});
    assert.equal(await page.evaluate(()=>document.activeElement.id),"auth-enter");
    await page.locator("#auth-enter").click();
    await page.locator(".lesson-resume").waitFor();
    assert.equal(await page.locator(".site").evaluate(el=>el.inert),false);
    assert.equal(await page.locator("#practice-view").isVisible(),false);
    assert.equal(await page.locator("#account-code").textContent(),"••••••••");
    assert.equal(await page.locator("body").innerText().then(text=>text.includes("v>")),false);
    await noOverflow("desktop home");await shot("home-desktop");
    await page.setViewportSize({width:360,height:780});await noOverflow("360px home");await shot("home-360");
    await page.locator("#account-menu summary").click();
    await page.locator("#theme-select").selectOption("dark");
    await page.locator("#account-menu summary").click();
    await noOverflow("dark home");await shot("home-dark-360");
    await page.locator("#account-menu summary").click();
    await page.locator("#theme-select").selectOption("light");
    await page.locator("#account-menu summary").click();

    await page.locator(".lesson-resume button").click();
    await page.locator(".lesson-answer-form").waitFor();
    const initial = await board();
    assert.equal(initial.lesson.at,0);
    const radios=page.locator('.lesson-answer-form input[type="radio"]');
    if(await radios.count()){
      assert.equal(await radios.filter({visible:true}).count()>0,true);
      assert.equal(await page.locator('.lesson-answer-form input:checked').count(),0);
      await radios.first().check();
      assert.equal((await board()).lesson.at,0,"selection is an unsubmitted draft");
    }
    await noOverflow("360px lesson");await shot("lesson-360");
    await page.setViewportSize({width:1280,height:900});await shot("lesson-desktop");
    let dropped=false,answerPosts=0;
    const dropAnswer=async route=>{
      const request=route.request(),body=request.method()==="POST"?request.postDataJSON():null;
      if(body?.action==="answer"){
        answerPosts++;
        if(!dropped){dropped=true;const response=await route.fetch();assert.equal(response.status(),200);return route.abort("failed");}
      }
      return route.continue();
    };
    await page.route("**/greek/api/board",dropAnswer);
    await chooseVisible();
    const committed=await board();
    assert.ok(committed.lastReceipt,"receipt recovered after real server commit and lost response");
    assert.equal(committed.lastReceipt.questionAt,0);
    assert.equal(answerPosts,1,"recovery fetch does not score another answer");
    assert.equal(await page.locator(".lesson-answer-form").isVisible(),false,"committed feedback cannot submit a replacement");
    assert.equal(await page.evaluate(()=>document.querySelector("#lesson-feedback").contains(document.activeElement)),true,"focus follows the assessed result");
    await shot("feedback-desktop");
    await page.unroute("**/greek/api/board",dropAnswer);
    await advanceFeedback();

    // Leave while a real answer is committed but its response is still in flight.
    let delayed=false;
    const delayAnswer=async route=>{
      const body=route.request().method()==="POST"?route.request().postDataJSON():null;
      if(body?.action==="answer"&&!delayed){delayed=true;const response=await route.fetch();await sleep(350);return route.fulfill({response});}
      return route.continue();
    };
    await page.route("**/greek/api/board",delayAnswer);
    await chooseVisible(false);await page.locator(".lesson-play-top button").click();
    await page.locator(".lesson-resume button").waitFor();
    await page.waitForFunction(()=>!document.querySelector("#board-map").hidden);
    await sleep(450);
    let away=await board();assert.ok(away.lastReceipt);assert.equal(away.lesson.paused,true);
    assert.equal(await page.locator("#board-play").isVisible(),false,"late receipt does not reopen a dismissed lesson");
    await page.locator(".lesson-resume button").click();
    await page.locator("#lesson-feedback").waitFor({state:"visible"});
    await advanceFeedback();
    assert.equal((await board()).lesson.paused,false,"receipt recovery resumes the next question before scoring");
    await page.unroute("**/greek/api/board",delayAnswer);

    let seenTyped=false,seenDialogue=false,seenOrder=false,completed=0,steps=0;
    while(completed<6&&steps++<120){
      if(await page.locator(".lesson-summary").count()){
        completed++;
        assert.ok(await page.locator("#lesson-summary-ai").count());
        if(completed===1){
          await noOverflow("desktop result");await shot("result-desktop");
          await page.setViewportSize({width:360,height:780});await noOverflow("360px result");await shot("result-360");
        }
        if(completed>=6)break;
        await page.locator(".lesson-summary-actions .primary").first().click();
        await page.locator(".lesson-answer-form").waitFor();
      }
      const state=await board(),q=state.lesson?.question;
      if(!q)throw Error("Missing active question before answer");
      if(q.typedAnswer||q.type==="life"){
        seenTyped=true;
        await page.locator("#lesson-typed-answer").fill("δοκιμή");
        await page.locator("#lang").selectOption("ar");
        await page.waitForFunction(()=>document.documentElement.dir==="rtl"&&document.querySelector("#lesson-typed-answer")?.value==="δοκιμή"&&document.querySelector('.lesson-answer-form button[type="submit"]')?.textContent===window.LexiUI.t("check")&&document.querySelector('label[for="lesson-typed-answer"]')?.textContent===window.LexiUI.t("typeGreek"));
        assert.equal(await page.locator('.lesson-answer-form button[type="submit"]').textContent(),"تحقّق");
        assert.ok((await page.locator(".lesson-play-top button").textContent()).includes("العودة"));
        assert.equal(await page.locator("#lesson-typed-answer").getAttribute("dir"),"ltr");
        await noOverflow("RTL typed draft");
        await shot("typed-rtl-360");
        await page.locator("#lang").selectOption("en");
        await page.waitForFunction(()=>document.querySelector("#lesson-typed-answer")?.value==="δοκιμή");
      }
      if(q.kind==="order")seenOrder=true;
      if(q.kind==="dialogue"){
        seenDialogue=true;
        assert.equal(q.dialogueGaps,undefined,"future answers are not sent to the learner");
        assert.ok(q.gapCount>=1);
        assert.equal(await page.locator(".lesson-dialogue-gap.active").count(),1);
        await noOverflow("dialogue");await shot("dialogue-360");
      }
      await chooseVisible();
      await advanceFeedback();
    }
    assert.equal(completed,6,"complete six real lesson families");
    assert.ok(seenDialogue,"real multi-slot dialogue rendered");
    console.log(JSON.stringify({completed,steps,seenTyped,seenDialogue,seenOrder}));

    await page.evaluate(()=>window.LexiApp.setPage("board"));
    await page.locator(".lesson-list").waitFor();
    for(const locale of ["ru","en","zh","ar","es","pt"]){
      await page.locator("#lang").selectOption(locale);
      await page.waitForFunction(expected=>document.documentElement.lang===expected&&document.querySelector(".lesson-title")?.textContent===window.LexiUI.t("continueTitle"),locale);
      await page.setViewportSize({width:320,height:780});
      await noOverflow(locale+" 320px home");
      assert.equal(await page.evaluate(()=>window.LexiUI.keys.every(key=>typeof window.LexiUI.t(key)==="string"&&window.LexiUI.t(key).length>0)),true,"all shared locale keys are filled");
    }
    await page.locator("#lang").selectOption("en");
    await page.setViewportSize({width:360,height:780});
    await page.evaluate(()=>window.LexiApp.setPage("vocab"));
    await page.locator("#vocab-new").click();
    await page.locator("#vocab-begin").waitFor({state:"visible"});
    await page.locator("#vocab-begin").click();
    await page.locator('#vocab-choices input[type="radio"]').first().check();
    let vocabDropped=false,vocabRequests=[];
    const dropVocab=async route=>{
      if(route.request().method()!=="POST")return route.continue();
      vocabRequests.push(route.request().postDataJSON());
      if(!vocabDropped){vocabDropped=true;const response=await route.fetch();assert.equal(response.status(),200);return route.abort("failed");}
      return route.continue();
    };
    await page.route("**/greek/api/vocab/answer",dropVocab);
    await page.locator("#vocab-submit").click();
    await page.locator("#vocab-feedback button").waitFor();
    assert.equal(await page.locator('#vocab-choices input:not(:disabled)').count(),0);
    await page.locator("#vocab-feedback button").click();
    await page.locator("#vocab-next").waitFor({state:"visible"});
    assert.equal(vocabRequests.length,2);assert.deepEqual(vocabRequests[0],vocabRequests[1],"exact idempotent vocabulary retry");
    await page.unroute("**/greek/api/vocab/answer",dropVocab);
    await noOverflow("vocabulary feedback");

    await page.evaluate(()=>window.LexiApp.setPage("life"));
    await page.locator(".life-adventure-card .life-continue").waitFor();
    await page.locator(".life-adventure-card .life-continue").click();
    await page.locator("#life-answer").waitFor();
    const lifeBefore=(await api("stats")).data.progressScopes.life.attempts;
    const sceneId=(await page.evaluate(()=>JSON.parse(sessionStorage.getItem("lexi-life-scene-v1")).id));
    let lifeDropped=false,lifePosts=0;
    const dropLife=async route=>{
      const request=route.request(),body=request.method()==="POST"?request.postDataJSON():null;
      if(body?.answer){lifePosts++;if(!lifeDropped){lifeDropped=true;const response=await route.fetch();assert.equal(response.status(),200);return route.abort("failed");}}
      return route.continue();
    };
    await page.route("**/greek/api/life/scene?*",dropLife);
    await page.locator("#life-answer").fill("δοκιμή");
    await page.locator(".life-answer-form button[type=submit]").click();
    await page.locator(".life-answer-feedback .life-continue").waitFor();
    assert.equal(lifePosts,1);
    assert.equal(await page.locator("#life-answer").isDisabled(),true,"revealed Life answer is final");
    assert.equal((await api("stats")).data.progressScopes.life.attempts,lifeBefore+1);
    await page.locator(".life-answer-feedback .life-continue").click();
    await page.waitForFunction(oldId=>{
      const pending=document.querySelector(".life-answer-feedback:not([hidden])");
      const saved=JSON.parse(sessionStorage.getItem("lexi-life-scene-v1")||"null");
      return !pending&&(!saved||saved.id!==oldId);
    },sceneId);
    assert.equal((await api("stats")).data.progressScopes.life.attempts,lifeBefore+1,"deferral cannot grade again");
    await page.unroute("**/greek/api/life/scene?*",dropLife);
    await noOverflow("Life receipt and deferral");

    await page.evaluate(()=>window.LexiApp.setPage("practice"));
    await page.locator("#start").click();
    await page.locator("#quiz").waitFor({state:"visible"});
    let hiddenAnswerCalls=0;
    const countAnswers=request=>{if(new URL(request.url()).pathname==="/greek/api/answer"&&request.method()==="POST")hiddenAnswerCalls++;};
    page.on("request",countAnswers);
    await page.evaluate(()=>window.LexiApp.setPage("stats"));
    await page.locator("#stats-view").waitFor({state:"visible"});
    await page.locator("body").click({position:{x:3,y:3}});
    await page.keyboard.press("1");await page.keyboard.press("Enter");await page.keyboard.press("Space");
    await sleep(200);assert.equal(hiddenAnswerCalls,0,"hidden Classic ignores answer shortcuts");
    await page.locator("#progress-scopes .progress-scope").first().waitFor();await noOverflow("scoped stats");

    const failProfile=route=>route.fulfill({status:503,contentType:"application/json",body:JSON.stringify({error:"temporary_unavailable"})});
    await page.route("**/greek/api/profile",failProfile);
    await page.reload();
    await page.locator("#app-state button").waitFor({state:"visible"});
    assert.equal(await page.locator("#auth-gate").isVisible(),false,"server outage is not signed-out");
    assert.equal(await page.locator("#practice-view").isVisible(),false,"no Classic flash before profile recovery");
    await page.unroute("**/greek/api/profile",failProfile);
    await page.locator("#app-state button").click();
    await page.locator("#app-state").waitFor({state:"hidden"});
    assert.equal(await page.locator("#auth-gate").isVisible(),false);
    // Optional deterministic authored-card fixtures. Only this synthetic account,
    // and only an explicitly enabled temporary SQLite database, may be seeded.
    if(process.env.LEXI_UI_FIXTURES==="1"){
      function seed(kind){
        const source=[
          "import os,sys,copy,pathlib",
          "import server,board_course as board,study_tracks as tracks",
          "dbpath=pathlib.Path(server.DB).resolve()",
          "assert dbpath.is_relative_to('/tmp'), 'fixtures require temporary DB'",
          "kind,nickname=sys.argv[1:]; assert nickname.startswith('UI check ')",
          "cards=server.PRACTICE_ALL+server.LISTEN_CARDS",
          "if kind=='agenda': chosen=next(c for c in cards if c['id']=='g2261021_281'); chapter=20",
          "else: chosen=next(c for c in board._candidates('grammar',1,cards,server._grammar_guard.milestone,False) if c['kind']==kind); chapter=1",
          "materials=(cards,server.vocab.VOCAB,server.format_question,server._grammar_guard.milestone,server.LISTENING_ENABLED,lambda text:None)",
          "value=copy.deepcopy(board.DEFAULT); value.update(position=(chapter-1)*8+board.FAMILIES.index('grammar'),chapterLimit=20)",
          "with server.conn() as db:",
          " uid=db.execute('SELECT user_id FROM accounts WHERE nickname=?',(nickname,)).fetchone()['user_id']",
          " active=board._build_lesson(value,uid,'en',[chosen],*materials[1:])",
          " matches=[q for q in active['items'] if q['id']==chosen['id']]",
          " assert matches, 'authored fixture missing from generated lesson'",
          " active['items']=matches[:1]; active['at']=0; value['active']=active",
          " old=db.execute(\"SELECT revision FROM learning_tracks WHERE user_id=? AND name='board' AND lang='shared'\",(uid,)).fetchone()",
          " tracks._save(db,uid,'board','shared',value,old['revision'] if old else 0)"
        ].join("\n");
        const result=spawnSync("python3",["-c",source,kind,nickname],{encoding:"utf8"});
        assert.equal(result.status,0,result.stderr);
      }
      for(const kind of ["order","accent","agenda"]){
        seed(kind);await page.evaluate(()=>window.LexiApp.setPage("board"));
        await page.locator(".lesson-resume button").waitFor();await page.locator(".lesson-resume button").click();
        await page.locator(".lesson-answer-form").waitFor();
        const q=(await board()).lesson.question;
        if(kind==="agenda"){
          assert.equal(q.id,"g2261021_281");assert.ok(q.prompt.includes("\n"));
          for(const locale of ["ru","en","zh","ar","es","pt"]){
            await page.locator("#lang").selectOption(locale);
            await page.waitForFunction(()=>document.querySelector('.lesson-answer-form button[type=submit]')?.textContent===window.LexiUI.t("check"));
            await page.setViewportSize({width:320,height:780});await noOverflow("real agenda "+locale);
            assert.equal(await page.evaluate(()=>getComputedStyle(document.querySelector(".lesson-question-prompt")).whiteSpace),"pre-line");
          }
          await shot("agenda-320");
        }else{
          if(kind==="accent"){
            const labels=await page.locator(".lesson-option span").allTextContents();
            assert.equal(new Set(labels).size,labels.length,"accent choices identify different full-word stress positions");
          }
          let submitted=null;
          const observe=request=>{if(new URL(request.url()).pathname==="/greek/api/board"&&request.method()==="POST"&&request.postDataJSON().action==="answer")submitted=request.postDataJSON();};
          page.on("request",observe);await chooseVisible();page.off("request",observe);
          assert.equal(typeof submitted.selected,"string",kind+" answer uses canonical string contract");
          await advanceFeedback();
        }
      }
      console.log("PASS: real authored order/accent scorer controls and agenda g2261021_281 in six locales at 320px.");
    }
    await testAccountSwitch(browser);
    assert.deepEqual(errors,[],"no uncaught frontend exceptions");
    console.log("PASS: auth focus, responsive/theme shell, six real lessons, receipt recovery, six locales/RTL, vocabulary exact retry, hidden Classic, profile retry.");
  }catch(error){
    if(artifactDir)await shot("failure");
    console.error(error);console.error("Page errors:",errors);
    process.exitCode=1;
  }finally{
    await context.close();await browser.close();
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
