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
 await until(()=>!d.getElementById('auth-gate').hidden,'auth gate');
 d.getElementById('auth-name').value='Weak Global QA '+(process.env.TEST_NICK||'A');
 fire('auth-form','submit');
 await until(()=>!d.getElementById('auth-success').hidden,'registration');
 fire('auth-enter');
 await until(()=>d.getElementById('auth-gate').hidden,'auth closed');
 const answers={};
 // Four real saved errors: three Spanish translations, one Greek-only dialogue.
 for(const x of [
  {id:'w158',direction:'gr-ru',lang:'es',selected:'INVALID-SPANISH'},
  {id:'w167',direction:'gr-ru',lang:'es',selected:'INVALID-SPANISH'},
  {id:'w192',direction:'ru-gr',lang:'es',selected:'INVALID-GREEK'},
  {id:'dlg006',direction:'gap0',lang:'ru',selected:'INVALID-DIALOGUE'}
 ]){ const result=await post('answer',x);answers[x.id]=result.answer; }
 const s=await get('stats');
 test(s.weak===4&&s.weakUnavailable===0,'four actionable mistakes');
 // Intentionally incompatible selected filters and different current language.
 d.querySelector('input[name=scope][value=pages]').click();
 d.getElementById('page-from').value='300';
 d.getElementById('page-to').value='300';
 d.querySelectorAll('#kind-options input').forEach(x=>x.checked=x.value==='sentence');
 const langPicker=d.getElementById('lang');langPicker.value='ru';
 langPicker.dispatchEvent(new w.Event('change',{bubbles:true}));
 d.querySelector('[data-page=weak]').click();
 await until(()=>d.getElementById('weak-count').textContent==='4','weak count four');
 test(d.getElementById('weak-start').disabled===false,'button enabled');
 fire('weak-start');
 await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.mode==='weak_all','all-language review started');
 test(lastQuiz.questions.length===4,'all four cards returned despite filters');
 test(lastQuiz.questions.filter(q=>q.lang==='es').length===3,'three Spanish errors preserved');
 test(lastQuiz.questions.some(q=>q.kind==='dialogue'),'Greek dialogue preserved');
 // One pass leaves debt 1, second pass closes all four keys.
 const startStats=await get('stats'),attempts=startStats.attempts;
 for(let index=0;index<8;index++){
   const q=lastQuiz.questions[index%4];
   const key=answers[q.id];
   const option=q.choices.indexOf(key);
   test(option>=0,'correct answer in bank '+q.id+' '+q.direction);
   d.querySelectorAll('#answers .answer')[option].click();
   await until(()=>!d.getElementById('next').hidden,'saved '+index);
   test(d.getElementById('feedback').className.includes('good'),'answer correct '+index);
   fire('next');
   await until(()=>index===7?!d.getElementById('finished').hidden:
       (!d.getElementById('quiz').hidden && d.getElementById('next').hidden),
       'next question '+index);
 }
 const end=await get('stats');
 test(end.weak===0,'all four mistakes cleared after two correct reviews');
 test(end.attempts>=attempts+8,'persisted eight review answers');
 test(!errors.length,'no browser JS errors: '+JSON.stringify(errors));
 console.log('PASS DOM: 4 real mistakes across Spanish and Greek-only dialogue accessible from RU with incompatible filters, 2 rounds clear all four');
 w.close();
})().catch(e=>{console.error('FAIL '+e.stack);w.close();process.exitCode=1});
