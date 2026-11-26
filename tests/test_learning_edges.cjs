/* Focused browser acceptance for #70, #73 and #83.
 * Uses a disposable real Lexi server and one synthetic account. API transport
 * faults are injected after real commits; saved questions/results are not mocked.
 * Run: LEXI_BASE_URL=http://localhost:18560 node tests/test_learning_edges.cjs
 */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const {chromium}=require("playwright");
const base=process.env.LEXI_BASE_URL||"http://localhost:18560";
const artifactDir=process.env.LEXI_ARTIFACT_DIR;
const SESSION_KEY="greek-active-session-v2";
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
function deferred(){
  let resolve;const promise=new Promise(done=>{resolve=done;});return {promise,resolve};
}
async function bounded(promise,label,ms=15000){
  let timer;
  try{return await Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(new Error("Timed out: "+label)),ms);})]);}
  finally{clearTimeout(timer);}
}
async function eventually(read,accept,label){
  const deadline=Date.now()+15000;let last;
  while(Date.now()<deadline){
    last=await read();if(accept(last))return last;await delay(100);
  }
  assert.fail(label+": "+JSON.stringify(last));
}
const snapshot=page=>page.evaluate(key=>JSON.parse(localStorage.getItem(key)||"null"),SESSION_KEY);
function lessonIdentity(value){
  return {sessionId:value?.sessionId,deadline:value?.deadline,index:value?.index,
    questionId:value?.questions?.[value.index]?.id,count:value?.count,answered:!!value?.answered,
    orderIndices:value?.orderIndices||[]};
}
async function api(page,endpoint){
  return page.evaluate(async endpoint=>{
    const response=await fetch("/greek/api/"+endpoint,{credentials:"same-origin",cache:"no-store"});
    return {status:response.status,data:await response.json()};
  },endpoint);
}
async function serverSession(page){
  const result=await api(page,"session");assert.equal(result.status,200);return result.data;
}
async function focusBody(page){
  await page.evaluate(()=>{document.activeElement?.blur();document.body.tabIndex=-1;document.body.focus();});
  assert.equal(await page.evaluate(()=>document.activeElement===document.body),true);
}
async function nav(page,destination){
  const tab=page.locator('.tab[data-page="'+destination+'"]');
  if(!await tab.isVisible())await page.locator("#additional-modes > summary").click();
  await tab.click();await page.locator("#"+destination+"-view").waitFor({state:"visible"});
}
async function register(page,nickname){
  await page.goto(base+"/greek/");
  await page.locator("#auth-gate").waitFor({state:"visible"});
  await page.locator("#auth-lang").selectOption("en");
  await page.locator("#auth-name").fill(nickname);
  await page.locator("#auth-submit").click();await page.locator("#auth-success").waitFor({state:"visible"});
  const code=(await page.locator("#auth-created-code").textContent()).trim();
  assert.match(code,/^[0-9]{8}$/);
  await page.locator("#auth-enter").click();
  await page.waitForFunction(()=>window.LexiApp?.loggedIn()&&/^[a-f0-9]{32}$/.test(window.LexiApp.accountKey()||""));
  await page.locator(".lesson-resume").waitFor();
  return {code,owner:await page.evaluate(()=>window.LexiApp.accountKey())};
}
async function login(page,code){
  await page.locator("#auth-gate").waitFor({state:"visible"});
  await page.locator("#auth-lang").selectOption("en");
  await page.locator("#mode-login").click();
  await page.locator("#auth-input-code").fill(code);
  await page.locator("#auth-submit").click();
  await page.waitForFunction(()=>window.LexiApp?.loggedIn()&&window.LexiApp.accountKey());
}
async function startClassic(page,kind){
  await nav(page,"practice");await page.locator("#setup").waitFor({state:"visible"});
  await page.locator('input[name="scope"][value="pages"]').check();
  await page.locator("#page-from").fill("1");await page.locator("#page-to").fill("312");
  for(const item of await page.locator("#kind-options input").all())
    await item.setChecked((await item.inputValue())===kind);
  await page.locator("#listen-mix").uncheck();
  await page.locator('#duration-options label:has(input[value="60"])').click();
  await page.locator("#start").click();
  await page.locator("#quiz").waitFor({state:"visible"});
  await page.locator("#answers button").first().waitFor();
  await page.waitForFunction(({key,kind})=>{
    const saved=JSON.parse(localStorage.getItem(key)||"null");return saved?.questions?.[saved.index]?.kind===kind;
  },{key:SESSION_KEY,kind});
  return snapshot(page);
}
async function assertRestored(page,expected,owner,label){
  await page.waitForFunction(owner=>window.LexiApp?.loggedIn()&&window.LexiApp.accountKey()===owner&&!document.querySelector(".site").inert,owner);
  await page.locator("#quiz").waitFor({state:"visible"});
  assert.deepEqual(lessonIdentity(await snapshot(page)),lessonIdentity(expected),label);
  assert.equal(await page.locator("#auth-gate").isVisible(),false,label+": no false auth gate");
}
async function assertBlockedStartup(page,retry,label){
  assert.equal(await page.evaluate(()=>document.querySelector(".site").inert),true,label+": shell is inert");
  assert.equal(await page.locator("#app-state").isVisible(),true,label+": loading/error state");
  assert.equal(await page.locator("#app-state button").isVisible(),retry,label+": appropriate retry");
  assert.equal(await page.locator("#auth-gate").isVisible(),false,label+": no false sign-up");
  const visible=await page.locator("section[id$='-view']:visible").count();
  assert.equal(visible,0,label+": no premature learner view");
}
(async()=>{
  const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
  const contexts=[],pages=[],errors=[],release=[];
  const makePage=async context=>{
    const page=await context.newPage();pages.push(page);page.setDefaultTimeout(15000);
    page.on("pageerror",error=>errors.push(error.stack||error.message));return page;
  };
  try{
    const contextA=await browser.newContext({viewport:{width:1280,height:900},locale:"en"});contexts.push(contextA);
    const pageA=await makePage(contextA);
    const account=await register(pageA,"UI edges "+Date.now().toString(36));
    const answers=[];
    pageA.on("request",request=>{
      if(new URL(request.url()).pathname==="/greek/api/answer"&&request.method()==="POST")answers.push(request.postDataJSON());
    });
    await startClassic(pageA,"word");
    const untouched=lessonIdentity(await snapshot(pageA));
    const destinations=["board","stats","life","vocab","culture"];
    for(const destination of destinations){
      await nav(pageA,destination);await focusBody(pageA);
      for(const key of ["1","Enter","ArrowLeft","ArrowRight"])await pageA.keyboard.press(key);
      await delay(100);
      assert.equal(answers.length,0,destination+": hidden unanswered Classic made no grading request");
      await nav(pageA,"practice");
      assert.deepEqual(lessonIdentity(await snapshot(pageA)),untouched,destination+": same unanswered question and deadline");
    }
    await focusBody(pageA);
    const answered=pageA.waitForResponse(response=>new URL(response.url()).pathname==="/greek/api/answer"&&response.request().method()==="POST");
    await pageA.keyboard.press("1");assert.equal((await answered).status(),200);
    await pageA.locator("#next").waitFor({state:"visible"});
    const graded=lessonIdentity(await snapshot(pageA));
    assert.equal(graded.count,1);assert.equal(graded.answered,true);assert.equal(answers.length,1);
    for(const destination of destinations){
      await nav(pageA,destination);await focusBody(pageA);
      for(const key of ["Enter","1","ArrowRight","ArrowLeft"])await pageA.keyboard.press(key);
      await delay(100);await nav(pageA,"practice");
      assert.equal(answers.length,1,destination+": hidden answered Classic made no grading request");
      assert.deepEqual(lessonIdentity(await snapshot(pageA)),graded,destination+": hidden Enter did not advance");
    }
    await focusBody(pageA);await pageA.keyboard.press("Enter");
    await pageA.waitForFunction(({key,index})=>JSON.parse(localStorage.getItem(key)).index===index+1,{key:SESSION_KEY,index:graded.index});
    assert.equal((await snapshot(pageA)).count,1,"visible Enter advances without grading");
    const stats=(await api(pageA,"stats")).data;assert.equal(stats.attempts,1,"exactly one real attempt was recorded");
    console.log("PASS #70: Classic hidden in Board, Stats, Life, Vocab and Culture; digits/Enter/arrows do not grade or advance; returning keyboard works; exactly one real attempt.");
    await pageA.locator("#finish-now").click();await pageA.locator("#finished").waitFor({state:"visible"});
    await eventually(()=>serverSession(pageA),value=>!value.exists,"completed Classic session is cleared");
    await pageA.locator("#again").click();

    await startClassic(pageA,"order");
    const initial=await snapshot(pageA);
    assert.ok(initial.questions[initial.index].tokens.length>=2,"authored order fixture supports a partial draft");
    const savedStart=await eventually(()=>serverSession(pageA),value=>value.exists&&value.snapshot.sessionId===initial.sessionId,"initial order snapshot commits");
    const firstCommit=deferred(),releaseLost=deferred(),retried=deferred();release.push(releaseLost.resolve);
    let lostBody=null,lostRevision=null,retryBody=null,retryReply=null,retryStatus=null,committedOnce=false;
    await pageA.route("**/greek/api/session",async route=>{
      const request=route.request(),body=request.method()==="POST"?request.postDataJSON():null;
      if(body?.op==="save"&&!committedOnce){
        committedOnce=true;lostBody=request.postData();
        const response=await route.fetch();assert.equal(response.status(),200);
        const reply=await response.json();lostRevision=reply.revision;firstCommit.resolve();
        await releaseLost.promise;return route.abort("failed");
      }
      if(lostBody&&body?.requestId===JSON.parse(lostBody).requestId){
        retryBody=request.postData();const response=await route.fetch();
        retryStatus=response.status();retryReply=await response.json();
        await route.fulfill({response});retried.resolve();return;
      }
      return route.continue();
    });
    await pageA.locator("#answers .order-word:not(:disabled)").first().click();
    await bounded(firstCommit.promise,"real autosave commit");
    const once=await snapshot(pageA);
    assert.equal(once.orderIndices.length,1);assert.equal(once.deadline,initial.deadline);
    // Edit while the first committed save's response is still in flight.
    await pageA.locator("#answers .order-word:not(:disabled)").first().click();
    const latestDraft=await snapshot(pageA);assert.equal(latestDraft.orderIndices.length,2);
    releaseLost.resolve();await bounded(retried.promise,"same-operation automatic retry");
    assert.equal(retryBody===lostBody,true,"lost response retry body changed: original indices "+JSON.stringify(JSON.parse(lostBody).snapshot.orderIndices)+"; retry indices "+JSON.stringify(JSON.parse(retryBody).snapshot.orderIndices));
    assert.equal(retryStatus,200,"same operation retry is accepted: "+JSON.stringify(retryReply));
    assert.equal(retryReply.replayed,true,"real server returned the committed receipt");
    assert.equal(retryReply.revision,lostRevision,"replay does not increment revision");
    assert.equal(lostRevision,savedStart.revision+1);
    const savedDraft=await eventually(()=>serverSession(pageA),value=>value.exists&&value.snapshot.orderIndices?.length===2,"newer local draft commits after replay");
    assert.equal(savedDraft.revision,lostRevision+1,"newer draft is one later save");
    assert.deepEqual(lessonIdentity(savedDraft.snapshot),lessonIdentity(latestDraft),"older response cannot roll back the newer draft");
    assert.equal(await pageA.locator("#quiz").isVisible(),true);
    assert.equal(await pageA.locator("#setup-error").isVisible(),false,"lost own response is not a takeover");
    assert.equal((await snapshot(pageA)).deadline,initial.deadline,"timer deadline survives transport loss");
    await pageA.unroute("**/greek/api/session");

    const contextB=await browser.newContext({viewport:{width:1280,height:900},locale:"en"});contexts.push(contextB);
    const pageB=await makePage(contextB),dialogs=[];
    pageB.on("dialog",async dialog=>{dialogs.push(dialog.message());await dialog.accept();});
    await pageB.goto(base+"/greek/");await login(pageB,account.code);
    await assertRestored(pageB,latestDraft,account.owner,"second device restores real snapshot");
    assert.equal(dialogs.length,1,"takeover requires the real existing-session prompt");
    const deviceB=await pageB.evaluate(()=>localStorage.getItem("greek-student-device-v1"));
    const transferred=await eventually(()=>serverSession(pageB),value=>value.ownerDevice===deviceB,"second device owns session");
    assert.equal(transferred.sessionId,initial.sessionId,"takeover preserves existing stable session ID");
    // The former owner makes its next save only after the real takeover.
    await pageA.locator("#order-undo").click();
    await pageA.locator("#setup-error").waitFor({state:"visible"});
    assert.match(await pageA.locator("#setup-error").textContent(),/moved to another device/i);
    assert.equal(await pageA.locator("#quiz").isVisible(),false,"genuine takeover stops former owner");
    assert.equal(answers.length,1,"takeover and draft edits never create a scored answer");
    await assertRestored(pageB,latestDraft,account.owner,"new owner remains active after old-owner save is rejected");
    await pageB.locator("#order-undo").click();
    const resumable=await snapshot(pageB);
    assert.equal(resumable.orderIndices.length,1);
    await eventually(()=>serverSession(pageB),value=>value.ownerDevice===deviceB&&value.snapshot.orderIndices?.length===1,"new owner can continue saving");
    console.log("PASS #73: real autosave commit then lost response; exact-body UUID receipt replay; newer in-flight draft preserved; original deadline and session ID; real UI takeover between saves stops only the old owner.");

    const profileSeen=deferred(),releaseProfile=deferred();release.push(releaseProfile.resolve);
    const authenticatedPaths=new Set(["board","quiz","stats","session","life","life/scene","vocab/lesson","culture/exam","srs/status","personalized/status"]);
    const premature=[];
    let heldProfile=true;
    const watch=request=>{
      const endpoint=new URL(request.url()).pathname.replace("/greek/api/","");
      if(heldProfile&&authenticatedPaths.has(endpoint))premature.push(endpoint);
    };
    pageB.on("request",watch);
    await pageB.route("**/greek/api/profile",async route=>{
      const response=await route.fetch();assert.equal(response.status(),200);
      profileSeen.resolve();await releaseProfile.promise;return route.fulfill({response});
    });
    await pageB.reload({waitUntil:"domcontentloaded"});
    await bounded(profileSeen.promise,"held real profile response");
    await assertBlockedStartup(pageB,false,"slow profile");
    assert.deepEqual(premature,[],"authenticated learner fetches wait for the profile");
    heldProfile=false;releaseProfile.resolve();
    await assertRestored(pageB,resumable,account.owner,"slow profile restores existing activity");
    await pageB.unroute("**/greek/api/profile");pageB.off("request",watch);

    for(const condition of ["offline","503"]){
      const pattern=condition==="offline"?"**/greek/api/**":"**/greek/api/profile";
      await pageB.route(pattern,route=>condition==="offline"
        ?route.abort("internetdisconnected")
        :route.fulfill({status:503,contentType:"application/json",body:JSON.stringify({error:"temporarily_unavailable"})}));
      await pageB.reload({waitUntil:"domcontentloaded"});
      await pageB.locator("#app-state button").waitFor({state:"visible"});
      await assertBlockedStartup(pageB,true,condition);
      assert.deepEqual(lessonIdentity(await snapshot(pageB)),lessonIdentity(resumable),condition+": local draft retained");
      assert.equal(await pageB.evaluate(()=>window.LexiApp.loggedIn()),false,condition+": identity not assumed");
      await pageB.unroute(pattern);await pageB.locator("#app-state button").click();
      await assertRestored(pageB,resumable,account.owner,condition+": retry restores same owner, question, draft and deadline");
    }

    // Expire the browser's real HttpOnly credential, leaving local lesson data.
    const cookie=(await contextB.cookies(base+"/greek/")).find(item=>item.httpOnly&&item.path==="/greek/");
    assert.ok(cookie,"authenticated cookie exists");
    await contextB.addCookies([{...cookie,expires:Math.floor(Date.now()/1000)-60}]);
    assert.equal((await contextB.cookies(base+"/greek/")).some(item=>item.name===cookie.name),false);
    await pageB.reload({waitUntil:"domcontentloaded"});
    await pageB.locator("#auth-gate").waitFor({state:"visible"});
    assert.equal(await pageB.locator("#app-state").isVisible(),false,"expired identity is auth, not transient error");
    assert.equal(await pageB.evaluate(()=>window.LexiApp.loggedIn()),false);
    assert.equal(await pageB.evaluate(()=>window.LexiApp.accountKey()),null);
    assert.equal(await pageB.evaluate(()=>document.querySelector(".site").inert),true);
    assert.equal(await pageB.locator("section[id$='-view']:visible").count(),0);
    assert.deepEqual(lessonIdentity(await snapshot(pageB)),lessonIdentity(resumable),"expired login preserves local session");
    assert.ok(!(await pageB.locator("#auth-gate").innerText()).includes("login_required"));
    await login(pageB,account.code);
    await assertRestored(pageB,resumable,account.owner,"re-login resumes same saved lesson");
    assert.equal((await api(pageB,"stats")).data.attempts,1,"startup failure and retry preserve real progress");
    console.log("PASS #83: held real profile has inert loading and no premature authenticated requests; API-offline and 503 show retry; retry restores same lesson; expired actual browser cookie shows auth; re-login preserves draft, deadline and progress.");
    assert.deepEqual(errors,[],"no uncaught browser exceptions");
  }catch(error){
    if(artifactDir){
      fs.mkdirSync(artifactDir,{recursive:true});
      for(let i=0;i<pages.length;i++)if(!pages[i].isClosed())
        await pages[i].screenshot({path:path.join(artifactDir,"edges-failure-"+i+".png"),fullPage:true}).catch(()=>{});
    }
    throw error;
  }finally{
    for(const unblock of release)unblock();
    for(const context of contexts)await context.close().catch(()=>{});
    await browser.close();
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
