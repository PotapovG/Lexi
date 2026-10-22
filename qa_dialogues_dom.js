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
 d.getElementById('auth-name').value='Three Gaps QA '+(process.env.TEST_NICK||'A');
 fire('auth-form','submit');
 await until(()=>!d.getElementById('auth-success').hidden,'registered');
 fire('auth-enter');
 await until(()=>d.getElementById('auth-gate').hidden,'gate close');
 d.querySelector('input[name=training][value=textbook]').click();
 d.querySelector('input[name=scope][value=pages]').click();
 const inputs=d.querySelectorAll('#kind-options input');
 inputs.forEach(x=>x.checked=x.value==='dialogue');
 d.getElementById('page-from').value='198';
 d.getElementById('page-to').value='198';
 fire('start');
 await until(()=>!d.getElementById('quiz').hidden&&!d.getElementById('dialogue-lines').hidden,'3-gap quiz');
 let q=lastQuiz.questions[0];
 test(q.id==='dlg080'&&q.gapIndices.length===3,'3-gap dialogue selected '+JSON.stringify(q));
 test(d.querySelectorAll('.dialogue-blank').length===3,'three Greek placeholders visible');
 test(d.querySelectorAll('#answers .answer').length===8,'eight Greek bank choices');
 for(let index=0;index<3;index++){
   test(d.querySelectorAll('.dialogue-blank.current').length===1,'current blank '+index);
   const opt=q.choices.indexOf(q.dialogueGaps[index]);
   test(opt>=0,'correct option '+index);
   d.querySelectorAll('#answers .answer')[opt].click();
   await until(()=>!d.getElementById('next').hidden,'answer '+index);
   const justAnswered=d.querySelector('.dialogue-blank[data-gap-index="'+index+'"]');
   test(justAnswered?.classList.contains('filled') && !justAnswered?.classList.contains('current'),
     'answered blank is immediately visibly filled and not current '+index);
   test(justAnswered.textContent===q.dialogueGaps[index],'completed dialogue line shows correct Greek answer '+index);
   test(d.getElementById('next').textContent===(index<2?'Следующий пропуск →':'Далее →'),
     'accurate next-button label at gap '+index+': '+d.getElementById('next').textContent);
   if(index===2)test(d.getElementById('question-note').textContent.includes('Все пропуски заполнены'),
       'completion instruction after last blank');
   if(index<2){
     fire('next');
     await until(()=>d.getElementById('dialogue-lines').textContent.includes(q.dialogueGaps[index])&&
       d.getElementById('question-note').textContent.includes(String(index+2)),'render following gap '+index);
     test(d.querySelectorAll('.dialogue-blank.filled').length===index+1,'previous filled '+index);
     test(d.getElementById('next').textContent==='Следующая →','stale next gap label reset for upcoming blank');
   }
 }
 const stats=await get('stats');
 test(stats.categories.dialogue.attempts>=3,'3 separately persisted answers');
 test(!errors.length,'no JS errors '+JSON.stringify(errors));
 fire('finish-now');
 await until(()=>!d.getElementById('finished').hidden,'finished');
 fire('again');
 d.getElementById('page-from').value='23';
 d.getElementById('page-to').value='23';
 inputs.forEach(x=>x.checked=x.value==='dialogue');
 fire('start');
 await until(()=>!d.getElementById('quiz').hidden&&lastQuiz.questions?.[0]?.id==='dlg025','single gap quiz');
 q=lastQuiz.questions[0];
 test(q.gapIndices.length===1,'single gap');
 test(d.querySelectorAll('.dialogue-blank').length===1,'one Greek placeholder');
 test(d.querySelectorAll('#answers .answer').length===8,'eight distractor choices single gap');
 d.querySelectorAll('#answers .answer')[q.choices.indexOf(q.dialogueGaps[0])].click();
 await until(()=>!d.getElementById('next').hidden,'single-gap answer');
 test(d.getElementById('next').textContent==='Далее →','single last-gap button says continue');
 test(d.querySelectorAll('.dialogue-blank.filled').length===1,'single-gap completion immediately shown');
 test(d.getElementById('question-note').textContent.includes('Все пропуски заполнены'),
    'single-gap ending is explicitly marked complete');
 console.log('PASS DOM: 3 sequential Greek-only blanks + 8 options, earlier choices disabled, and 1-gap dialogue');
 w.close();
})().catch(e=>{console.error('FAIL DOM '+e.stack);w.close();process.exitCode=1});
