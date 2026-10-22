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
 d.getElementById('auth-name').value='Two Gap QA '+(process.env.TEST_NICK||'A');
 fire('auth-form','submit');
 await until(()=>!d.getElementById('auth-success').hidden,'registered');
 fire('auth-enter');
 await until(()=>d.getElementById('auth-gate').hidden,'auth closes');
 d.querySelector('input[name=scope][value=pages]').click();
 d.querySelectorAll('#kind-options input').forEach(x=>x.checked=x.value==='dialogue');
 d.getElementById('page-from').value='16';d.getElementById('page-to').value='16';
 fire('start');
 await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.questions?.[0]?.id==='dlg001','2-gap dialogue');
 const q=lastQuiz.questions[0];
 test(q.gapIndices.join(',')==='0,1','normal two gaps');
 const expected=(i)=>q.dialogueGaps[i];
 const choose=(i)=>{const slot=q.choices.indexOf(expected(i));test(slot>=0,'answer bank contains Greek answer');d.querySelectorAll('#answers .answer')[slot].click();};
 choose(0);
 await until(()=>!d.getElementById('next').hidden,'first answer');
 test(d.getElementById('next').textContent==='Следующий пропуск →','first step next gap');
 test(d.querySelector('.dialogue-blank[data-gap-index="0"]').textContent===expected(0),'first answer appears inline');
 fire('next');
 await until(()=>d.getElementById('question-note').textContent.includes('2 из 2'),'2nd gap displayed');
 test(d.getElementById('next').textContent==='Следующая →','stale next gap label cleared');
 choose(1);
 await until(()=>!d.getElementById('next').hidden,'second answer');
 test(d.getElementById('next').textContent==='Далее →','no ghost third gap');
 test(d.querySelector('.dialogue-blank[data-gap-index="1"]').textContent===expected(1),'second Greek answer appears inline');
 test(d.querySelectorAll('.dialogue-blank.filled').length===2,'both Greek blanks filled');
 test(d.querySelectorAll('.dialogue-blank.current').length===0,'none left active');
 test(d.getElementById('question-note').textContent.includes('Все пропуски заполнены'),'completion shown');
 console.log('PASS normal 2-gap: answered last gap inline, no phantom next gap label');
 test(d.getElementById('finish-now').textContent==='Завершить тренировку',
    'Early exit explicitly says it ends the entire practice session');
 fire('next');
 await until(()=>!d.getElementById('finished').hidden,'normal session auto-finishes after the only dialogue');
 test(d.getElementById('finished').textContent.includes('2'),'finish results reflect two completed gaps');
 fire('again');
 // Weak repeat: only second gap is due, despite first being already correct.
 await post('answer',{id:'dlg001',direction:'gap1',lang:'ru',selected:'incorrect deliberately'});
 const stats=await get('stats');test(stats.weak===1,'only gap1 due');
 d.querySelector('[data-page=weak]').click();
 await until(()=>d.getElementById('weak-count').textContent==='1','weak count');
 fire('weak-start');
 await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.mode==='weak_all','global review');
 test(lastQuiz.questions.length===1&&lastQuiz.questions[0].gapIndices.join(',')==='1','single due final gap');
 for(let pass=0;pass<2;pass++){
  await until(()=>d.getElementById('question-note').textContent.includes('1 из 1'),'weak gap shown '+pass);
  test(d.querySelector('.dialogue-blank[data-gap-index="0"]').textContent===expected(0),'first gap already filled in weak');
  const idx=lastQuiz.questions[0].choices.indexOf(expected(1));
  test(idx>=0,'correct weak answer available');
  d.querySelectorAll('#answers .answer')[idx].click();
  await until(()=>!d.getElementById('next').hidden,'weak answer '+pass);
  test(d.getElementById('next').textContent==='Далее →','last weak gap continue (not phantom gap)');
  test(d.querySelectorAll('.dialogue-blank.filled').length===2,'both weak blanks filled');
  fire('next');
  if(pass===0){await until(()=>!d.getElementById('quiz').hidden&&d.getElementById('next').hidden,'due second review');}
  else {await until(()=>!d.getElementById('finished').hidden,'finish after two correct reviews');}
 }
 test((await get('stats')).weak===0,'weak debt cleared after 2 correct reviews');
 test(!errors.length,'no JS errors: '+JSON.stringify(errors));
 console.log('PASS weak single-due second gap: after last answer Continue finishes review, no nonexistent gap');
 w.close();
})().catch(e=>{console.error('FAIL '+e.stack);w.close();process.exitCode=1});
