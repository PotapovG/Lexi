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
 // Old saved chapter 5 meant transport in the pre-PDF app. Preserve the topic
 // in the new numbering by migrating that selection to printed chapter 6.
 w.localStorage.setItem('lexi-greek-v2',JSON.stringify({
    lang:'ru',scope:'chapters',chapters:[1,2,3,4,5],
    chapterNumberingVersion:1,types:['word','number','phrase','sentence','dialogue'],duration:30
 }));
 w.eval(fs.readFileSync('/app/app.js','utf8'));
 w.eval(fs.readFileSync('/app/vocab.js','utf8'));
 await until(()=>d.querySelectorAll('#chapter-grid input').length===22,'real PDF chapters loaded');
 const options=[...d.querySelectorAll('#chapter-grid .chapter-option')];
 test(options.length===22,'intro + 20 units + appendix');
 const chapter=(number)=>options.find(row=>row.querySelector('input')?.value===String(number));
 for(let i=1;i<=20;i++){
    const expected=[0,14,24,38,48,59,66,80,94,108,122,132,150,166,184,200,212,232,246,262,278][i];
    test(chapter(i).querySelector('.chapter-page').textContent.startsWith(String(expected)+'–'),'chapter start '+i);
    test(chapter(i).querySelector('.chapter-focus').textContent.length>12,'grammar summary '+i);
 }
 for(const ch of [5,10,15,20])test(chapter(ch).textContent.includes('Повторение'),'review chapter '+ch);
 test(chapter(5).textContent.includes('Пάμε')||chapter(5).textContent.includes('Πάμε'),'book section 5 title');
 test(chapter(6).textContent.includes('Πού πάτε'),'book transport is section 6');
 test(chapter(5).querySelector('input').checked===false,'old transport preference is NOT wrongly review 5');
 test(chapter(6).querySelector('input').checked===true,'old transport preference migrated to chapter 6');
 test(chapter(1).querySelector('input').checked,'old introductory chapter selected');
 // Existing login still works after curriculum alignment.
 await until(()=>!d.getElementById('auth-gate').hidden,'login');
 d.getElementById('auth-name').value='Patakis Book QA '+(process.env.TEST_NICK||'A');
 fire('auth-form','submit');
 await until(()=>!d.getElementById('auth-success').hidden,'registered');
 fire('auth-enter');
 await until(()=>d.getElementById('auth-gate').hidden,'login closed');

 d.querySelector('input[name=scope][value=chapters]').click();
 d.querySelectorAll('#kind-options input').forEach(x=>x.checked=['word','number','phrase','sentence','dialogue','accent'].includes(x.value));
 // Select the actual first FIVE printed chapters; review 5 is now included.
 for(const input of d.querySelectorAll('#chapter-grid input'))input.checked=[1,2,3,4,5].includes(Number(input.value));
 fire('start');
 await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.questions?.length===60,'first-five session 60');
 test(lastQuiz.questions.every(x=>x.chapter>=1&&x.chapter<=5),
      'first 5 chapters only 1–4+review, not transport');
 test(!lastQuiz.questions.some(x=>x.chapter===6),'no transport in first five');
 fire('finish-now');
 await until(()=>!d.getElementById('finished').hidden,'finished');
 fire('again');
 d.querySelector('input[name=scope][value=pages]').click();
 d.getElementById('page-from').value='59';d.getElementById('page-to').value='65';
 d.querySelectorAll('#kind-options input').forEach(x=>x.checked=x.value==='word');
 fire('start');
 await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.questions?.length>0,'revision pages quiz');
 test(lastQuiz.questions.every(x=>x.chapter===5),'printed 59–65 is review 5');
 fire('finish-now');
 await until(()=>!d.getElementById('finished').hidden,'review completed');
 test(!errors.length,'no JS errors '+JSON.stringify(errors));
 await sleep(250);
 console.log('PASS DOM: 20 authentic numbered units, 4 review chapters, legacy preferences migrate, first five no transport, page59–65 review');
 w.close();
})().catch(e=>{console.error('FAIL '+e.stack);w.close();process.exitCode=1});
