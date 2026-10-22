"use strict";
const {JSDOM}=require('/tmp/qa/node_modules/jsdom');
const fs=require('fs');
const dom=new JSDOM(fs.readFileSync('/app/index.html','utf8'),{url:'https://potapovfamily.com/greek/',runScripts:'outside-only',pretendToBeVisual:true});
const w=dom.window,d=w.document;
w.HTMLElement.prototype.scrollIntoView=function(){};
w.alert=()=>{};w.confirm=()=>true;
let cookie='',lastQuiz=null,lastLesson=null,errors=[];
w.addEventListener('error',event=>errors.push(event.message));
w.addEventListener('unhandledrejection',event=>errors.push(String(event.reason)));
w.fetch=async(url,options={})=>{
 const path=url.replace(/^\/greek\//,'/');
 const headers=new Headers(options.headers||{});
 headers.set('Origin','https://potapovfamily.com');
 if(cookie)headers.set('Cookie',cookie);
 const response=await fetch('http://127.0.0.1:18561'+path,{...options,headers});
 const match=(response.headers.get('set-cookie')||'').match(/greek_session=([a-f0-9]{32})/);
 if(match)cookie='greek_session='+match[1];
 if(path.startsWith('/api/quiz?')){try{lastQuiz=await response.clone().json();}catch{}}
 if(path.startsWith('/api/vocab/lesson?')){try{lastLesson=await response.clone().json();}catch{}}
 return response;
};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function until(test,name){for(let i=0;i<100;i++){if(test())return;await sleep(65);}throw Error('Timeout '+name+' '+d.getElementById('setup-error')?.textContent+' '+JSON.stringify(errors))}
function test(v,message){if(!v)throw Error('ASSERT '+message);}
function fire(id,event='click'){const e=d.getElementById(id);test(e,'missing '+id);e.dispatchEvent(new w.Event(event,{bubbles:true,cancelable:true}));}
async function post(path,data){const response=await w.fetch('/greek/api/'+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});test(response.ok,'POST '+path+' '+response.status);return response.json();}
async function get(path){const response=await w.fetch('/greek/api/'+path);test(response.ok,'GET '+path);return response.json();}
(async()=>{
 w.eval(fs.readFileSync('/app/app.js','utf8'));
 w.eval(fs.readFileSync('/app/vocab.js','utf8'));
 await until(()=>!d.getElementById('auth-gate').hidden,'auth');
 d.getElementById('auth-name').value='Final Nu QA '+(process.env.TEST_NICK||'1');
 fire('auth-form','submit');
 await until(()=>!d.getElementById('auth-success').hidden,'registered');
 fire('auth-enter');await until(()=>d.getElementById('auth-gate').hidden,'login');
 function restrict(p){
  d.querySelector('input[name=scope][value=pages]').click();
  d.querySelectorAll('#kind-options input').forEach(x=>x.checked=x.value==='article');
  d.getElementById('page-from').value=p;
  d.getElementById('page-to').value=p;
 }
 async function qstart(p,id){
  restrict(p);fire('start');
  await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.questions?.[0]?.id===id,'quiz '+id);
  return lastQuiz.questions[0];
 }
 let q=await qstart('52','article_014');
 test(q.choices.includes('τη')&&q.choices.includes('την'),'both article forms selectable');
 test(d.getElementById('question-note').textContent.includes('варианты написания')||
      d.getElementById('question-note').textContent.includes('Варианты написания'),'neutral prior notice');
 const alternative=q.choices.indexOf('την');
 d.querySelectorAll('#answers .answer')[alternative].click();
 await until(()=>!d.getElementById('next').hidden,'retained nu accepted');
 test(d.getElementById('feedback').classList.contains('good'),'retained ν NOT marked wrong');
 test(d.querySelectorAll('#answers .answer.is-correct').length===2,'both valid articles highlighted green');
 test(d.querySelectorAll('#answers .answer.is-wrong').length===0,'no red marking');
 test(d.querySelector('.answer.is-preferred')?.textContent.includes('По учебнику'),'preferred book form subtly labeled');
 const note=d.querySelector('#feedback .spelling-guidance');
 test(note?.textContent.includes('τη Μαρία'),'after-answer note explains spelling context');
 test(note?.textContent.includes('не ошибка в грамматике'),'spelling not a grammar mistake');
 test((await get('stats')).weak===0,'no new weak debt');
 fire('next');await until(()=>!d.getElementById('finished').hidden,'end');
 fire('again');
 q=await qstart('54','article_015');
 test(q.prompt.includes('Άννα'),'strict before vowel');
 const wrong=q.choices.indexOf('τη');
 test(wrong>=0,'shorter vowel form remains distractor');
 d.querySelectorAll('#answers .answer')[wrong].click();
 await until(()=>!d.getElementById('next').hidden,'strict wrong selected');
 test(d.getElementById('feedback').classList.contains('bad'),'short variant before vowel still incorrect');
 test(d.querySelector('#feedback .spelling-guidance')===null,'no optional-final-n note before vowel');
 test((await get('stats')).weak===1,'actual orthographic mistake still due');
 test(!errors.length,'browser errors '+JSON.stringify(errors));
 console.log('PASS DOM retained -ν correctly accepted and explained; shorter -ν before vowel rejected');
 w.close();
})().catch(e=>{console.error('FAIL '+e.stack);w.close();process.exitCode=1});
