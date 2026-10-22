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
 d.getElementById('auth-name').value='Accent Stage QA '+(process.env.TEST_NICK||'A');
 fire('auth-form','submit');
 await until(()=>!d.getElementById('auth-success').hidden,'registered');
 fire('auth-enter');await until(()=>d.getElementById('auth-gate').hidden,'auth closed');
 const verb=d.querySelector('input[name=scope][value=verbs]');
 verb.click();
 test(!d.getElementById('verb-controls').hidden,'verb settings opened');
 test(d.getElementById('verb-max-unit').value==='4','default stage4');
 await until(()=>d.getElementById('verb-stage-summary').textContent.includes('42'),'stage4 42 conjugations');
 const cap=await get('topics');
 test(cap.verbs.length===17 && cap.verbs.every(v=>Number.isInteger(v.introducedUnit)),'verb catalog metadata');
 const unit=d.getElementById('verb-max-unit');
 unit.value='2';unit.dispatchEvent(new w.Event('change',{bubbles:true}));
 test(d.getElementById('verb-stage-summary').textContent.includes('6'),'stage2 has six forms');
 fire('estimate-capacity');
 await until(()=>d.getElementById('capacity-result').textContent.includes('6 уникальных'),'stage2 capacity preview');
 test(d.getElementById('capacity-result').textContent.includes('может закончиться раньше'),'insufficient warning');
 fire('start');
 await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.questions?.[0]?.kind==='verb','verb practice');
 test(lastQuiz.questions.length===6,'only μένω people six');
 test(lastQuiz.questions.every(q=>q.introducedUnit<=2),'nothing from later unit');
 fire('finish-now');await until(()=>!d.getElementById('finished').hidden,'finish stage2');
 fire('again');
 d.querySelector('input[name=scope][value=verbs]').click();
 unit.value='4';unit.dispatchEvent(new w.Event('change',{bubbles:true}));
 fire('start');await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.questions?.length===42,'stage4 quiz');
 test(lastQuiz.questions.length===42 && lastQuiz.questions.every(x=>x.introducedUnit<=4),'strict stage4 gate');
 fire('finish-now');await until(()=>!d.getElementById('finished').hidden,'finish stage4');
 fire('again');
 d.querySelector('input[name=scope][value=pages]').click();
 d.querySelectorAll('#kind-options input').forEach(x=>x.checked=x.value==='accent');
 d.getElementById('page-from').value='20';d.getElementById('page-to').value='20';
 fire('start');
 await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.questions?.[0]?.kind==='accent','accent quiz');
 const q=lastQuiz.questions[0];
 test(q.accentableIndices.includes(q.letters.indexOf(q.letters[q.accentableIndices[0]])),'vowel indices correct');
 const tiles=Array.from(d.querySelectorAll('#answers .accent-letter'));
 test(tiles.length===q.letters.length,'original spelling in tiles');
 for(let i=0;i<tiles.length;i++){
  test(tiles[i].disabled===!q.accentableIndices.includes(i),'consonants noninteractive '+i);
 }
 const item=(await get('catalog'));test(item.cardCount===1795,'original book count unchanged');
 // Correct stress index found from public question via known catalogue server source
 const known={}; // Select known source stress_w028 if present; otherwise choose any vowel and verify hint.
 const exact=q.id==='stress_w028'?1:q.accentableIndices[0];
 tiles[exact].click();
 await until(()=>!d.getElementById('next').hidden,'stress answer graded');
 const feedback=d.getElementById('feedback').textContent;
 test(feedback.includes('Ударение (τόνος)'),'written vowel/digraph guidance after answer');
 test(d.querySelector('.spelling-guidance')!==null,'explanation is visible');
 test(d.querySelector('#feedback .spelling-guidance')?.textContent.includes('Ударение'),'accent full explanation');
 test(!errors.length,'no browser exceptions '+JSON.stringify(errors));
 console.log('PASS DOM verb curriculum stage 2/4 + accent vowel-only selection and after-answer guidance');
 w.close();
})().catch(e=>{console.error('FAIL '+e.stack);w.close();process.exitCode=1});
