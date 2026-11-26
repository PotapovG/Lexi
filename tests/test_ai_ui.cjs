/* AI UI browser regression against a local synthetic page and mocked AI endpoints.
 * No real account, audio service, paid inference or production server.
 * Run with Playwright 1.56.1: NODE_PATH=/tmp/pw/node_modules node tests/test_ai_ui.cjs
 */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const http=require("node:http");
const {chromium}=require("playwright");
const root=path.resolve(__dirname,"..");
const runId="a".repeat(32);
const copy=value=>JSON.parse(JSON.stringify(value));
const caps={enabled:true,features:{summary:true,reading:true,dialogue:true},pronunciation:false,audioDecoder:true,
  limits:{uploadBytes:8*1024*1024,readingSeconds:90,dialogueSeconds:45,dialogueTurns:[4,5]},textRetentionDays:30,audioRetentionHours:1};
const reading={id:"dlg001",chapter:1,text:"Καλημέρα. Με λένε Μαρία.",sourceId:"dlg001",sourceVersion:"v1"};
const summaryResult={kind:"summary",observation:{text:"You completed the saved practice.",evidenceIds:["e1"],example:"Καλημέρα"},
  improvements:[{text:"Try the saved article form again.",evidenceIds:["e2"],example:"τη"}],
  nextStep:"Review familiar words.",targetCardId:"w001",evidenceComplete:true,advisory:true};
function fixture(){
  window.__loggedIn=true;window.__account="synthetic-learner";window.__reviewCalls=[];window.__accountReconciles=0;
  window.LexiApp={loggedIn:()=>window.__loggedIn,accountKey:()=>window.__account,currentLang:()=>document.getElementById("lang").value,
    routeToExistingReview:id=>window.__reviewCalls.push(id),
    reconcileAccount:async()=>{window.__accountReconciles++;window.__loggedIn=false;window.__account=null;document.dispatchEvent(new Event("lexi:logout"));},
    api:async(endpoint,options)=>{
      const response=await fetch("/greek/api/"+endpoint,{credentials:"same-origin",...options});
      if(!response.ok){const body=await response.json();const error=new Error(body.error);error.status=response.status;error.body=body;throw error;}
      return response.json();
    }};
  window.__mediaMode="ok";window.__support=true;window.__tracks=[];window.__urls=new Set();window.__timeOffset=0;
  const now=Date.now;Date.now=()=>now()+window.__timeOffset;
  const create=URL.createObjectURL.bind(URL),revoke=URL.revokeObjectURL.bind(URL);
  URL.createObjectURL=blob=>{const url=create(blob);window.__urls.add(url);return url;};
  URL.revokeObjectURL=url=>{window.__urls.delete(url);revoke(url);};
  const stream=()=>{
    const track={readyState:"live",stop(){this.readyState="ended";}};window.__tracks.push(track);
    return {getTracks:()=>[track]};
  };
  Object.defineProperty(navigator,"mediaDevices",{configurable:true,value:{getUserMedia:async()=>{
    if(window.__mediaMode==="denied"){const e=new Error("denied");e.name="NotAllowedError";throw e;}
    if(window.__mediaMode==="deferred")return await new Promise(resolve=>{window.__grant=()=>resolve(stream());});
    return stream();
  }}});
  window.MediaRecorder=class extends EventTarget{
    static isTypeSupported(){return window.__support;}
    constructor(value,options){super();this.stream=value;this.mimeType=options.mimeType;this.state="inactive";}
    start(){this.state="recording";}
    stop(){
      if(this.state==="inactive")return;this.state="inactive";
      setTimeout(()=>{
        const event=new Event("dataavailable");Object.defineProperty(event,"data",{value:new Blob(["synthetic-audio"],{type:this.mimeType})});
        this.dispatchEvent(event);this.dispatchEvent(new Event("stop"));
      },0);
    }
  };
}
const html=["<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>",
  "<style>:root{--bg:#f6f4ed;--panel:#fffdf7;--line:#c7d2cf;--text:#20383f;--muted:#52656a;--accent:#24555b;--accent-text:#fff;--bad:#9b3330}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.55 sans-serif}main{max-width:720px;padding:16px;margin:auto}[hidden]{display:none!important}button,select,textarea{font:inherit}</style>",
  "<link rel='stylesheet' href='/ai_ui.css'></head><body><main id='board-view'><h1>Lesson result</h1>",
  "<label for='lang'>Interface language</label><select id='lang'>",
  ["ru","en","zh","ar","es","pt"].map(x=>"<option value='"+x+"'>"+x+"</option>").join(""),
  "</select><section id='lesson-summary-ai'></section><button id='continue-course'>Continue course</button></main>",
  "<script>("+fixture.toString()+")()</script><script src='/ai_ui.js'></script></body></html>"].join("");
const server=http.createServer((req,res)=>{
  if(req.url==="/ai_ui.js"||req.url==="/ai_ui.css"){
    res.writeHead(200,{"Content-Type":req.url.endsWith(".js")?"application/javascript; charset=utf-8":"text/css; charset=utf-8"});
    res.end(fs.readFileSync(path.join(root,req.url.slice(1))));return;
  }
  res.writeHead(200,{"Content-Type":"text/html; charset=utf-8"});res.end(html);
});
(async()=>{
  await new Promise(resolve=>server.listen(0,"127.0.0.1",resolve));
  const base="http://127.0.0.1:"+server.address().port;
  const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
  const allErrors=[],contexts=[];
  async function fresh(config={}){
    const context=await browser.newContext({viewport:{width:360,height:780},locale:"en"});
    contexts.push(context);
    const page=await context.newPage();page.setDefaultTimeout(6500);
    page.on("pageerror",error=>allErrors.push(error.message));
    if(config.fastPoll)await page.addInitScript(()=>{
      const timer=window.setTimeout;window.setTimeout=(fn,delay,...rest)=>timer(fn,delay===2000?1:delay,...rest);
    });
    const state={caps:copy(caps),jobs:new Map(),ops:new Map(),conversations:new Map(),readingJobs:new Map(),summary:null,
      calls:[],count:0,pendingAlways:false,dropAfterCommit:false,dropBeforeCommit:false,uncertainNext:false,erased:false,...config};
    if(config.disabled)state.caps.enabled=false;
    if(config.cached){
      state.summary={id:"cached-summary",kind:"summary",runId,status:"succeeded",result:copy(summaryResult),reported:false};
      state.jobs.set(state.summary.id,state.summary);
    }
    function job(kind,fields={}){
      const result={id:"job"+(++state.count),kind,runId,status:"queued",result:null,reported:false,usageState:"reserved",...fields};
      state.jobs.set(result.id,result);return result;
    }
    function settle(value){
      if(!["queued","running"].includes(value.status)||state.pendingAlways)return;
      value.status="succeeded";value.usageState="known";
      if(value.kind==="summary")value.result=copy(summaryResult);
      else if(value.kind==="reading")value.result={kind:"reading",readingId:"dlg001",reference:reading.text,transcript:"Καλησπέρα. Με λένε Μαρία.",
        origin:"asr",edited:false,comparison:[{type:"replace",expected:"Καλημέρα",recognized:"Καλησπέρα"}],matchingContent:false,hasMoreDifferences:false,pronunciationAssessed:false,languageErrors:null,revision:0};
      else{
        const c=state.conversations.get(value.conversationId);c.pendingJob=null;
        if(state.uncertainNext){state.uncertainNext=false;value.result={kind:"dialogue",status:"recognition_uncertain",transcript:"δοκιμή",origin:"asr",languageErrors:null};return;}
        const ordinal=c.turnCount+1;
        const entry={ordinal,question:copy(c.question),transcript:value.transcript||"Με λένε Μαρία.",originalTranscript:value.transcript||"Με λένε Μαρία.",
          origin:value.origin||"typed",edited:false,reply:"Καλημέρα.",correction:"",explanation:"",finalNote:ordinal===c.targetTurns?"Practice completed.":"",
          nextQuestion:ordinal<c.targetTurns?{id:"q"+ordinal,text:"Πού μένεις;"}:null,jobId:value.id,revision:0};
        c.history.push(entry);c.turnCount=ordinal;c.revision++;c.question=entry.nextQuestion;
        if(ordinal===c.targetTurns)c.status="completed";
        value.result={kind:"dialogue",status:"evaluated",turn:copy(entry),turnCount:ordinal,targetTurns:c.targetTurns,complete:c.status==="completed",conversationRevision:c.revision,pronunciationAssessed:false};
      }
    }
    await page.route("**/greek/api/**",async route=>{
      const req=route.request(),url=new URL(req.url()),endpoint=url.pathname.replace("/greek/api/",""),method=req.method();
      let body={};if(method==="POST"&&!endpoint.startsWith("ai/audio"))try{body=req.postDataJSON();}catch{}
      state.calls.push({method,endpoint,query:Object.fromEntries(url.searchParams),body,headers:req.headers()});
      const send=(value,status=200)=>route.fulfill({status,contentType:"application/json",body:JSON.stringify(copy(value))});
      if(method==="POST"){
        assert.equal(req.headers()["x-lexi-owner"],"synthetic-learner","every AI mutation carries the captured expected owner");
        if(state.expectedOwner&&state.expectedOwner!==req.headers()["x-lexi-owner"])return send({error:"account_changed"},409);
      }
      if(method==="GET"&&endpoint==="ai/capabilities")return send(state.caps);
      if(method==="GET"&&endpoint==="ai/options"){
        if(state.erased)return send({error:"lesson_evidence_unavailable"},404);
        return send({runId,chapter:3,readings:[reading],dialogues:[{id:"dlg001",firstQuestion:"Πώς σε λένε;"}],dialogueTurns:[4,5],
          existingSummary:state.summary,readingJobs:[...state.readingJobs.entries()].map(([readingId,value])=>({...value,readingId})),conversations:[...state.conversations.values()]});
      }
      if(method==="GET"&&endpoint.startsWith("ai/operations/")){
        const value=state.ops.get(endpoint.split("/").at(-1));return value?send(value):send({error:"operation_not_found"},404);
      }
      if(method==="GET"&&endpoint.startsWith("ai/jobs/")){
        const value=state.jobs.get(endpoint.split("/").at(-1));if(!value)return send({error:"job_not_found"},404);
        settle(value);
        if(state.holdNextJob){
          state.holdNextJob=false;const snapshot=copy(value);
          await new Promise(resolve=>{state.releaseJob=resolve;});return send(snapshot);
        }
        return send(value);
      }
      if(method==="GET"&&endpoint.startsWith("ai/conversations/")){
        const value=state.conversations.get(endpoint.split("/").at(-1));return value?send(value):send({error:"conversation_not_found"},404);
      }
      if(method==="POST"&&endpoint==="ai/audio"&&state.preparationBusy){state.preparationBusy=false;return send({error:"ai_preparation_busy"},429);}
      if(method==="POST"&&state.dropBeforeCommit){state.dropBeforeCommit=false;return route.abort("connectionfailed");}
      let result;
      if(endpoint==="ai/summary"&&method==="POST"){
        result=state.summary||job("summary");state.summary=result;state.ops.set(body.operationId,result);
      }else if(endpoint==="ai/conversations"&&method==="POST"){
        result={id:"conversation"+(++state.count),runId,status:"active",revision:0,pendingJob:null,targetTurns:body.turns,history:[],question:{id:"q0",text:"Πώς σε λένε;"},turnCount:0,scopeVersion:"v1"};
        state.conversations.set(result.id,result);state.ops.set(body.operationId,result);
      }else if(endpoint==="ai/audio"&&method==="POST"){
        const kind=url.searchParams.get("kind"),conversationId=url.searchParams.get("conversationId");
        result=job(kind,{conversationId,origin:"asr"});
        if(kind==="reading")state.readingJobs.set(url.searchParams.get("readingId"),result);
        else state.conversations.get(conversationId).pendingJob=result.id;
        state.ops.set(url.searchParams.get("operationId"),result);
      }else if(endpoint.endsWith("/text")&&method==="POST"){
        const conversationId=endpoint.split("/")[2];
        result=job("dialogue",{conversationId,origin:"typed",transcript:body.transcript});state.conversations.get(conversationId).pendingJob=result.id;state.ops.set(body.operationId,result);
      }else if(endpoint.endsWith("/transcript")&&method==="POST"){
        result=state.jobs.get(endpoint.split("/")[2]);
        assert.equal(result.kind,"reading","fixture edits only reading");
        result.result={...result.result,originalTranscript:result.result.originalTranscript||result.result.transcript,transcript:body.transcript,edited:true,origin:"edited_transcript",revision:result.result.revision+1,comparison:[],matchingContent:true};
        state.ops.set(body.operationId,result);
      }else if(endpoint.endsWith("/cancel")&&method==="POST"){
        result=state.jobs.get(endpoint.split("/")[2]);result.status="cancelled";
        if(result.conversationId)state.conversations.get(result.conversationId).pendingJob=null;
      }else if(endpoint.endsWith("/finish")&&method==="POST"){
        result=state.conversations.get(endpoint.split("/")[2]);result.status="partial";result.revision++;result.question=null;
        if(result.pendingJob)state.jobs.get(result.pendingJob).status="cancelled";result.pendingJob=null;
      }else if(endpoint.endsWith("/report")&&method==="POST"){
        state.jobs.get(endpoint.split("/")[2]).reported=true;result={reported:true};
      }else if(endpoint==="ai/erase"&&method==="POST"){
        assert.equal(body.confirm,true);state.erased=true;state.summary=null;state.readingJobs.clear();state.conversations.clear();state.jobs.clear();result={deleted:true,ordinaryProgressPreserved:true};
      }else return send({error:"unexpected_test_endpoint"},500);
      if(state.dropAfterCommit){state.dropAfterCommit=false;return route.abort("connectionfailed");}
      return send(result);
    });
    await page.goto(base);
    await page.locator("#lang").selectOption(config.lang||"en");
    const open=()=>page.evaluate(run=>document.dispatchEvent(new CustomEvent("lexi:lesson-complete",{detail:{runId:run,lesson:{runId:run,chapter:3},chapter:3,lang:document.getElementById("lang").value,board:{}}})),runId);
    await open();
    if(!config.disabled)await page.locator("[data-ai-focus='choose-reading']").waitFor();
    return {page,state,open,close:()=>context.close()};
  }
  const click=(page,key)=>page.locator("[data-ai-focus='"+key+"']").click();
  async function confirm(page){await page.locator(".lexi-ai-dialog").waitFor();await click(page,"dialog-confirm");}
  async function noOverflow(page,label){
    const layout=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));
    assert.ok(layout.scroll<=layout.width+1,label+": "+JSON.stringify(layout));
  }
  try{
    {
      const {page,state,close}=await fresh({disabled:true});
      await page.waitForTimeout(100);
      assert.equal(await page.locator("#lesson-summary-ai").isVisible(),false);
      assert.deepEqual(state.calls.map(x=>x.endpoint),["ai/capabilities"]);await close();
      console.log("PASS disabled AI silently hides without options or paid requests");
    }
    {
      const {page,state,close}=await fresh();
      assert.equal(state.calls.filter(x=>x.method==="POST").length,0);
      await click(page,"create-summary");assert.equal(state.calls.filter(x=>x.method==="POST").length,0);
      assert.ok((await page.locator(".lexi-ai-dialog").innerText()).includes("OpenAI"));
      for(let i=0;i<8;i++){await page.keyboard.press("Tab");assert.equal(await page.evaluate(()=>document.querySelector("dialog").contains(document.activeElement)),true);}
      state.dropAfterCommit=true;await confirm(page);
      await page.locator("[data-ai-focus='recover-operation']").waitFor();
      assert.equal(state.calls.filter(x=>x.endpoint==="ai/summary"&&x.method==="POST").length,1);
      await click(page,"recover-operation");await page.locator(".lexi-ai-claim").first().waitFor();
      assert.equal(state.calls.filter(x=>x.endpoint==="ai/summary"&&x.method==="POST").length,1);
      await click(page,"existing-review");assert.deepEqual(await page.evaluate(()=>window.__reviewCalls),["w001"]);
      await close();console.log("PASS explicit summary consent, native focus, lost-response operation recovery, existing review");
    }
    {
      const {page,state,close}=await fresh();state.dropBeforeCommit=true;
      await click(page,"create-summary");await confirm(page);
      await page.locator("[data-ai-focus='recover-operation']").waitFor();
      const original=state.calls.find(x=>x.endpoint==="ai/summary").body.operationId;
      await click(page,"recover-operation");await page.locator("[data-ai-focus='retry-operation']").waitFor();
      assert.equal(state.calls.filter(x=>x.endpoint==="ai/summary").length,1);
      await click(page,"retry-operation");await page.locator(".lexi-ai-claim").first().waitFor();
      const posts=state.calls.filter(x=>x.endpoint==="ai/summary");
      assert.equal(posts.length,2);assert.ok(posts.every(x=>x.body.operationId===original));
      assert.equal(state.calls.filter(x=>x.endpoint==="ai/operations/"+original).length,2);
      await close();console.log("PASS manual resend checks operation again and retains the same identity");
    }
    {
      const titles=[];const expectedTitles={ru:"Практика с ИИ",en:"Practice with AI",zh:"AI 练习",ar:"تدريب بالذكاء الاصطناعي",es:"Práctica con IA",pt:"Prática com IA"};
      for(const language of ["ru","en","zh","ar","es","pt"]){
        const {page,state,open,close}=await fresh({lang:language,cached:true});
        state.summary.result.observation.text="<img src=x onerror=alert(1)> "+ "Καλημέρα".repeat(30);
        await open();await page.locator(".lexi-ai-claim").first().waitFor();
        titles.push(await page.locator("#lexi-ai-title").innerText());assert.equal(titles.at(-1),expectedTitles[language]);
        assert.equal(await page.locator(".lexi-ai img").count(),0);
        await page.setViewportSize({width:320,height:780});await noOverflow(page,language);
        assert.equal(await page.locator("#lesson-summary-ai").getAttribute("dir"),language==="ar"?"rtl":"ltr");
        await click(page,"choose-reading");
        assert.equal(await page.locator(".lexi-ai-greek").first().getAttribute("dir"),"ltr");
        await noOverflow(page,language+" reading");
        assert.equal(state.calls.filter(x=>x.method==="POST").length,0);await close();
      }
      assert.equal(new Set(titles).size,6);console.log("PASS six locale flows at320px, Arabic/Greek direction, cached reuse and model-text escaping");
    }
    {
      const {page,state,close}=await fresh();
      await click(page,"choose-reading");await click(page,"record-reading");
      await page.locator("[data-ai-focus='stop-recording']").waitFor();await click(page,"stop-recording");
      await page.locator("audio").waitFor();assert.equal(state.calls.filter(x=>x.endpoint==="ai/audio").length,0);
      assert.equal(await page.evaluate(()=>window.__tracks.every(x=>x.readyState==="ended")),true);
      assert.equal(await page.evaluate(()=>window.__urls.size),1);
      await click(page,"rerecord");await page.locator("[data-ai-focus='stop-recording']").waitFor();await click(page,"stop-recording");await page.locator("audio").waitFor();
      assert.equal(await page.evaluate(()=>window.__urls.size),1);
      await click(page,"send-audio");await confirm(page);
      await page.locator("[data-ai-focus='edit-reading']").waitFor();
      const upload=state.calls.find(x=>x.endpoint==="ai/audio");
      assert.equal(upload.query.readingId,"dlg001");assert.equal(upload.query.kind,"reading");assert.equal(upload.headers["content-type"],"audio/webm");
      assert.equal(await page.evaluate(()=>window.__urls.size),0);
      await click(page,"edit-reading");await page.locator("#ai-transcript-edit").fill(reading.text);await click(page,"save-transcript");
      await page.waitForFunction(()=>!document.getElementById("ai-transcript-edit"));
      assert.ok((await page.locator(".lexi-ai-feedback").innerText()).includes("Text was edited by hand"));
      assert.ok((await page.locator(".lexi-ai-feedback").innerText()).includes("Original recognition"));
      const edits=state.calls.filter(x=>x.endpoint.endsWith("/transcript"));assert.equal(edits.length,1);assert.ok(edits[0].body.operationId);
      await close();console.log("PASS local recording preview/re-record, explicit upload, released resources and honest transcript edits");
    }
    {
      const {page,state,close}=await fresh();
      await click(page,"choose-reading");await page.evaluate(()=>window.__mediaMode="deferred");await click(page,"record-reading");
      await page.locator("[data-ai-focus='cancel-permission']").waitFor();
      await page.evaluate(()=>document.dispatchEvent(new CustomEvent("lexi:page-leave",{detail:{page:"board",nextPage:"stats"}})));
      await page.evaluate(()=>window.__grant());await page.waitForTimeout(100);
      assert.equal(await page.evaluate(()=>window.__tracks.every(x=>x.readyState==="ended")),true);
      assert.equal(await page.evaluate(()=>window.__urls.size),0);
      assert.equal(state.calls.filter(x=>x.endpoint==="ai/audio").length,0);
      await close();console.log("PASS late microphone permission after leaving cannot restart capture");
    }
    {
      const {page,close}=await fresh();
      await click(page,"choose-reading");await click(page,"record-reading");await page.locator("[data-ai-focus='stop-recording']").waitFor();
      await page.evaluate(()=>window.__timeOffset=91000);await page.locator("audio").waitFor();
      assert.equal(await page.evaluate(()=>window.__tracks.every(x=>x.readyState==="ended")),true);
      await page.evaluate(()=>{Object.defineProperty(document,"hidden",{configurable:true,value:true});document.dispatchEvent(new Event("visibilitychange"));});
      assert.equal(await page.evaluate(()=>window.__urls.size),0);
      await close();console.log("PASS90-second capture cap and hidden-page local recording disposal");
    }
    {
      const {page,state,close}=await fresh();
      await click(page,"choose-dialogue");await page.locator("#ai-turns").selectOption("4");await click(page,"start-dialogue");
      await page.locator("[data-ai-focus='record-dialogue']").waitFor();
      await page.evaluate(()=>window.__mediaMode="denied");await click(page,"record-dialogue");await page.locator("#ai-typed-answer").waitFor();
      await page.locator("#ai-typed-answer").fill("Με λένε Μαρία.");
      await page.locator("#lang").selectOption("ar");
      assert.equal(await page.locator("#ai-typed-answer").inputValue(),"Με λένε Μαρία.");
      assert.equal(await page.locator("#ai-typed-answer").getAttribute("dir"),"ltr");
      await page.locator("#lang").selectOption("en");
      for(let turn=0;turn<4;turn++){
        await page.locator("#ai-typed-answer").fill("Με λένε Μαρία.");
        await click(page,"send-text");if(turn===0)await confirm(page);
        await page.waitForFunction(count=>document.querySelectorAll(".lexi-ai-turn").length===count,turn+1);
      }
      assert.equal([...state.conversations.values()][0].turnCount,4);
      assert.equal([...state.conversations.values()][0].status,"completed");
      assert.equal(await page.locator("#ai-typed-answer").count(),0);
      assert.equal(state.calls.filter(x=>x.endpoint.endsWith("/text")).length,4);
      assert.ok((await page.locator(".lexi-ai-section").innerText()).includes("Typed answer: meaning only"));
      await close();console.log("PASS denied mic fallback, language-switch draft, exact4-turn dialogue and typed evidence labels");
    }
    {
      const {page,state,close}=await fresh();await click(page,"choose-dialogue");await click(page,"start-dialogue");
      await page.locator("[data-ai-focus='typed-mode']").waitFor();await click(page,"typed-mode");await page.locator("#ai-typed-answer").fill("Δοκιμή");
      state.uncertainNext=true;await click(page,"send-text");await confirm(page);
      await page.waitForFunction(()=>document.querySelector(".lexi-ai-notice")?.textContent.includes("could not be understood")||document.body.textContent.includes("could not be understood"));
      const c=[...state.conversations.values()][0];assert.equal(c.turnCount,0);assert.equal(c.question.id,"q0");
      await click(page,"finish-dialogue");await page.waitForFunction(()=>!document.getElementById("ai-typed-answer"));
      assert.equal(c.status,"partial");assert.equal(c.turnCount,0);
      await close();console.log("PASS uncertain recognition keeps the same question, manual partial finish grants no mastery");
    }
    {
      const {page,state,close}=await fresh({fastPoll:true,pendingAlways:true});
      await click(page,"create-summary");await confirm(page);
      await page.locator("[data-ai-focus^='check-job']").waitFor();
      const reads=state.calls.filter(x=>x.endpoint.startsWith("ai/jobs/")&&x.method==="GET").length;
      assert.equal(reads,30);await page.waitForTimeout(150);
      assert.equal(state.calls.filter(x=>x.endpoint.startsWith("ai/jobs/")&&x.method==="GET").length,30);
      await page.locator("[data-ai-focus^='cancel-job']").click();
      assert.equal(state.summary.status,"cancelled");await close();console.log("PASS bounded job polling and explicit cancellation");
    }
    {
      const {page,state,close}=await fresh({cached:true});
      await page.locator("[data-ai-focus^='report-']").click();await page.locator(".lexi-ai-dialog select").selectOption("incorrect");await confirm(page);
      await page.waitForFunction(()=>document.querySelector(".lexi-ai-report")?.textContent.includes("Report saved"));
      assert.equal(state.calls.filter(x=>x.endpoint.endsWith("/report")).length,1);
      await page.locator(".lexi-ai-privacy summary").click();await click(page,"erase-ai");
      assert.equal(state.calls.filter(x=>x.endpoint==="ai/erase").length,0);await confirm(page);
      await page.waitForFunction(()=>document.getElementById("lesson-summary-ai").textContent.includes("AI data erased"));
      assert.equal(state.calls.filter(x=>x.endpoint==="ai/erase").length,1);
      assert.equal(await page.locator(".lexi-ai-claim").count(),0);
      await page.evaluate(()=>{window.__loggedIn=false;document.dispatchEvent(new Event("lexi:logout"));});
      assert.equal(await page.evaluate(()=>sessionStorage.getItem("lexi-ai-pending-v1")),null);
      assert.equal(await page.evaluate(()=>window.__urls.size),0);
      await close();console.log("PASS issue report and confirmed erase preserve ordinary course, logout clears local metadata");
    }
    {
      const {page,state,open,close}=await fresh({fastPoll:true});
      state.dropAfterCommit=true;await click(page,"create-summary");await confirm(page);
      await page.locator("[data-ai-focus='recover-operation']").waitFor();
      const op=state.calls.find(x=>x.endpoint==="ai/summary").body.operationId;
      await page.reload();await page.locator("#lang").selectOption("en");await open();
      await page.locator(".lexi-ai-claim").first().waitFor();
      assert.equal(state.calls.filter(x=>x.endpoint==="ai/summary").length,1);
      assert.ok(state.calls.some(x=>x.endpoint==="ai/operations/"+op));
      await close();console.log("PASS reload recovers an unacknowledged operation without another paid request");
    }
    {
      const {page,state,open,close}=await fresh({fastPoll:true});
      await click(page,"choose-reading");await click(page,"record-reading");await page.locator("[data-ai-focus='stop-recording']").waitFor();await click(page,"stop-recording");await page.locator("audio").waitFor();
      state.preparationBusy=true;await click(page,"send-audio");await confirm(page);
      await page.locator("[data-ai-focus='retry-operation']").waitFor();
      const original=state.calls.find(x=>x.endpoint==="ai/audio").query.operationId;
      assert.equal(await page.evaluate(()=>window.__urls.size),1);
      await click(page,"retry-operation");await page.locator("[data-ai-focus='edit-reading']").waitFor();
      const uploads=state.calls.filter(x=>x.endpoint==="ai/audio");assert.equal(uploads.length,2);assert.ok(uploads.every(x=>x.query.operationId===original));
      await page.reload();await page.locator("#lang").selectOption("en");await open();await page.locator("[data-ai-focus='choose-reading']").waitFor();await click(page,"choose-reading");
      await page.locator("[data-ai-focus='edit-reading']").waitFor();
      assert.equal(state.calls.filter(x=>x.endpoint==="ai/audio").length,2);
      if(process.env.LEXI_ARTIFACT_DIR)await page.screenshot({path:path.join(process.env.LEXI_ARTIFACT_DIR,"ai_reading_en_360.png"),fullPage:true});
      await close();console.log("PASS admission-busy keeps clip and operation identity; reading result resumes after reload");
    }
    {
      const {page,state,close}=await fresh({fastPoll:true});
      await click(page,"choose-dialogue");await page.locator("#ai-turns").selectOption("5");await click(page,"start-dialogue");
      for(let turn=0;turn<5;turn++){
        await page.locator("[data-ai-focus='record-dialogue']").waitFor();await click(page,"record-dialogue");
        await page.locator("[data-ai-focus='stop-recording']").waitFor();await click(page,"stop-recording");await page.locator("audio").waitFor();
        await click(page,"send-audio");if(turn===0)await confirm(page);
        await page.waitForFunction(count=>document.querySelectorAll(".lexi-ai-turn").length===count,turn+1);
      }
      const c=[...state.conversations.values()][0];assert.equal(c.turnCount,5);assert.equal(c.status,"completed");
      assert.equal(state.calls.filter(x=>x.endpoint==="ai/audio").length,5);
      assert.equal(await page.locator("[data-ai-focus='record-dialogue']").count(),0);
      assert.equal(await page.evaluate(()=>window.__tracks.every(x=>x.readyState==="ended")&&window.__urls.size===0),true);
      await page.locator("#lang").selectOption("ar");await noOverflow(page,"Arabic completed5turn");
      if(process.env.LEXI_ARTIFACT_DIR)await page.screenshot({path:path.join(process.env.LEXI_ARTIFACT_DIR,"ai_dialogue_ar_360.png"),fullPage:false});
      await close();console.log("PASS exact5voice-turn dialogue, no sixth answer and no retained recording resources");
    }
    {
      const {page,state,close}=await fresh({pendingAlways:true});
      await click(page,"choose-dialogue");await click(page,"start-dialogue");
      await page.locator("[data-ai-focus='typed-mode']").waitFor();
      const a=[...state.conversations.values()][0].id;
      await click(page,"back-options");await click(page,"choose-dialogue");await click(page,"start-dialogue");
      await page.locator("[data-ai-focus='typed-mode']").waitFor();
      const b=[...state.conversations.values()].find(value=>value.id!==a).id;
      await click(page,"back-options");await click(page,"choose-dialogue");await click(page,"saved-"+a);
      await click(page,"typed-mode");await page.locator("#ai-typed-answer").fill("Απάντηση Α.");
      state.holdNextJob=true;await click(page,"send-text");await confirm(page);
      await page.locator("[data-ai-focus^='cancel-job']").waitFor();
      await click(page,"back-options");await click(page,"choose-dialogue");
      assert.equal(await page.locator("[data-ai-focus='start-dialogue']").count(),0);
      assert.equal(await page.locator("[data-ai-focus='saved-"+b+"']").count(),0);
      assert.equal(state.calls.filter(x=>x.endpoint==="ai/conversations"&&x.method==="POST").length,2);
      const deadline=Date.now()+5000;
      while(!state.releaseJob&&Date.now()<deadline)await page.waitForTimeout(20);
      assert.equal(typeof state.releaseJob,"function","poll A is held in flight");
      await click(page,"finish-dialogue");await page.waitForFunction(()=>document.body.textContent.includes("Dialogue ended"));
      await click(page,"back-options");await click(page,"choose-dialogue");await click(page,"saved-"+b);
      await page.locator("#ai-typed-answer").fill("Προσχέδιο Β που πρέπει να μείνει.");
      state.releaseJob();await page.waitForTimeout(2300);
      assert.equal(await page.locator("#ai-typed-answer").inputValue(),"Προσχέδιο Β που πρέπει να μείνει.");
      assert.equal(await page.locator("[data-ai-focus='send-text']").isEnabled(),true);
      assert.equal(state.conversations.get(b).turnCount,0);
      assert.equal(state.calls.filter(x=>x.endpoint.endsWith("/text")).length,1);
      assert.ok(state.calls.filter(x=>x.endpoint.startsWith("ai/jobs/")&&x.method==="GET").length>=2);
      await close();console.log("PASS pending A cannot be switched/cleared; late A poll after finish preserves B identity and typed draft");
    }
    {
      const {page,state,close}=await fresh({cached:true});
      await page.locator(".lexi-ai-privacy summary").click();await click(page,"erase-ai");
      state.expectedOwner="different-account";await confirm(page);
      await page.waitForFunction(()=>window.__accountReconciles===1);
      assert.equal(state.erased,false);
      assert.equal(state.calls.filter(x=>x.endpoint==="ai/erase").length,1);
      assert.equal(await page.locator("#lesson-summary-ai").isVisible(),false);
      assert.equal(await page.evaluate(()=>sessionStorage.getItem("lexi-ai-pending-v1")),null);
      await close();
      const next=await fresh();
      await click(next.page,"choose-reading");await click(next.page,"record-reading");
      await next.page.locator("[data-ai-focus='stop-recording']").waitFor();await click(next.page,"stop-recording");await next.page.locator("audio").waitFor();
      await click(next.page,"send-audio");next.state.expectedOwner="different-account";await confirm(next.page);
      await next.page.waitForFunction(()=>window.__accountReconciles===1);
      assert.equal(next.state.calls.filter(x=>x.endpoint==="ai/audio").length,1);
      assert.equal(next.state.jobs.size,0);
      assert.equal(await next.page.evaluate(()=>window.__urls.size===0&&window.__tracks.every(x=>x.readyState==="ended")),true);
      assert.equal(await next.page.evaluate(()=>sessionStorage.getItem("lexi-ai-pending-v1")),null);
      await next.close();console.log("PASS stale owner headers block JSON erase and raw audio; dispose resources, reconcile account, never retry");
    }
    assert.deepEqual(allErrors,[]);console.log("PASS no uncaught browser errors; all API/provider work mocked");
  }finally{
    for(const context of contexts)await context.close().catch(()=>{});
    await browser.close();await new Promise(resolve=>server.close(resolve));
  }
})().catch(error=>{console.error(error.stack||error);process.exitCode=1;server.close();});
