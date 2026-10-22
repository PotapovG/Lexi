"use strict";
const {JSDOM}=require('/tmp/qa/node_modules/jsdom');
const fs=require('fs');
const httpUrl='http://127.0.0.1:18561';
const html=fs.readFileSync('/app/index.html','utf8');
const dom=new JSDOM(html,{url:'https://potapovfamily.com/greek/',runScripts:'outside-only',pretendToBeVisual:true});
const w=dom.window,d=w.document;
let cookie='';
let failures=[];
w.HTMLElement.prototype.scrollIntoView=function(){};
w.alert=msg=>{console.log("ALERT",msg)};
w.confirm=()=>true;
w.fetch=async (url,opts={})=>{
  const path=url.replace(/^\/greek\//,'/');
  const headers=new Headers(opts.headers||{});
  headers.set('Origin','https://potapovfamily.com');
  if(cookie)headers.set('Cookie',cookie);
  const res=await fetch(httpUrl+path,{...opts,headers});
  const set=res.headers.get('set-cookie')||'';
  const match=set.match(/greek_session=([a-f0-9]{32})/);
  if(match)cookie='greek_session='+match[1];
  return res;
};
w.addEventListener('error',e=>failures.push('window error: '+e.message));
w.addEventListener('unhandledrejection',e=>failures.push('rejection: '+String(e.reason)));
const delay=n=>new Promise(r=>setTimeout(r,n));
async function until(check,description){
  for(let i=0;i<80;i++){
    if(check())return;
    await delay(80);
  }
  throw Error("timeout: "+description+"; body "+d.body.textContent.slice(-350));
}
function assert(check,msg){if(!check)throw Error("ASSERT "+msg);}
function fire(id,event='click'){let el=d.getElementById(id);assert(el,'missing '+id);el.dispatchEvent(new w.Event(event,{bubbles:true,cancelable:true}));}
(async()=>{
  w.eval(fs.readFileSync('/app/app.js','utf8'));
  w.eval(fs.readFileSync('/app/vocab.js','utf8'));
  await until(()=>d.getElementById('auth-gate').hidden===false,'auth opens');
  assert(d.getElementById('auth-lang').options.length===6,'six login languages');
  const language=d.getElementById('auth-lang');language.value='ar';language.dispatchEvent(new w.Event('change',{bubbles:true}));
  assert(d.documentElement.lang==='ar'&&d.documentElement.dir==='rtl','Arabic selected on login');
  d.getElementById('auth-name').value='Browser QA '+(process.env.TEST_NICK||'Default');
  fire('auth-form','submit');
  await until(()=>d.getElementById('auth-success').hidden===false,'registration success');
  assert(/^\d{8}$/.test(d.getElementById('auth-created-code').textContent),'8-digit code created');
  fire('auth-enter');
  assert(d.getElementById('auth-gate').hidden===true,'auth overlay closes');
  d.querySelector('[data-page="vocab"]').click();
  await until(()=>d.getElementById('vocab-topic').options.length>=14,'vocab topics fetched');
  d.getElementById('vocab-topic').value='food';d.getElementById('vocab-level').value='A1';
  fire('vocab-new');
  await until(()=>d.querySelectorAll('#vocab-preview-list .topic-study-row').length===10,'ten-word preview');
  fire('vocab-begin');
  await until(()=>d.querySelectorAll('#vocab-choices .answer').length===8,'eight answer choices');
  d.querySelector('#vocab-choices .answer').click();
  await until(()=>d.getElementById('vocab-next').hidden===false,'vocab answer saved');
  fire('vocab-next');
  assert(d.getElementById('vocab-question-count').textContent==='2 / 10','second word rendered');
  fire('vocab-back');
  d.querySelector('[data-page="practice"]').click();
  const verbs=d.querySelector('input[name="scope"][value="verbs"]');verbs.checked=true;verbs.dispatchEvent(new w.Event('change',{bubbles:true}));
  fire('start');
  await until(()=>d.getElementById('quiz').hidden===false,'verb quiz opened');
  try {
    await until(()=>d.getElementById('question-prompt').textContent.includes('____') && d.querySelectorAll('#answers .answer').length===8,'verb prompt and options');
  }catch(err){
    console.error('VERB DEBUG',JSON.stringify({scope:d.querySelector('input[name=scope]:checked')?.value,prompt:d.getElementById('question-prompt').textContent,note:d.getElementById('question-note').textContent,answers:d.querySelectorAll('#answers .answer').length,setupError:d.getElementById('setup-error').textContent,quiz:d.getElementById('quiz').hidden,failed:failures}));
    throw err;
  }
  assert(d.querySelectorAll('#answers .answer').length===8,'verb options');
  d.querySelector('#answers .answer').click();
  await until(()=>d.getElementById('next').hidden===false,'first verb stage recorded');
  fire('next');
  assert(d.getElementById('question-note').textContent.includes('المرحلة الثانية'),'second stage Arabic instructions');
  assert(d.getElementById('question-prompt').textContent.length>12,'Greek phrase');
  assert(d.querySelectorAll('#answers .answer').length===8,'phrase translation choices');
  d.querySelector('#answers .answer').click();
  await until(()=>d.getElementById('next').hidden===false,'phrase answer saved');
  assert(!failures.length,failures.join(';'));
  console.log("PASS DOM: Arabic login, 8-digit register, vocab 10-word preview, 8-choice cards, next word, pronoun→conjugation→sentence translation");
  w.close();
})().catch(e=>{console.error("FAIL DOM",e.stack||e);console.error('additional JS errors',failures);w.close();process.exitCode=1;});
