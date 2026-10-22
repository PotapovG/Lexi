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
 d.getElementById('auth-name').value='New Feature QA '+(process.env.TEST_NICK||'A');
 fire('auth-form','submit');
 await until(()=>!d.getElementById('auth-success').hidden,'registered');
 fire('auth-enter');
 await until(()=>d.getElementById('auth-gate').hidden,'auth gate close');

 // Start with no course words: personalized mode includes book only.
 test((await get('personalized/status')).learned===0,'new user learned zero');
 const radios=d.querySelectorAll('input[name=training]');
 test(radios.length===2,'two training modes');
 d.querySelector('input[name=training][value=personalized]').click();
 await until(()=>d.getElementById('personalized-status').textContent.includes('0'),'personalized status visible');
 test(!d.getElementById('personalized-status').hidden,'personal stats panel shown');
 const select=d.querySelector('input[name=scope][value=pages]');select.click();
 test(d.getElementById('training-description').textContent.length>20,'personalized mode explanation');

 // Learn one word through the vocabulary course.
 d.querySelector('[data-page=vocab]').click();
 await until(()=>d.getElementById('vocab-topic').options.length>=14,'vocab course opens');
 d.getElementById('vocab-topic').value='food';d.getElementById('vocab-level').value='A1';
 fire('vocab-new');
 await until(()=>d.querySelectorAll('#vocab-preview-list .topic-study-row').length===10,'ten-word preview');
 const first=lastLesson.words[0];
 fire('vocab-begin');
 const expected=first.direction==='gr-target'?first.translation:first.gr;
 const index=first.choices.indexOf(expected);
 test(index>=0,'correct vocabulary option');
 test(d.querySelectorAll('#vocab-choices .answer').length===8,'vocab 8 choices');
 d.querySelectorAll('#vocab-choices .answer')[index].click();
 await until(()=>!d.getElementById('vocab-next').hidden,'course answer');
 const status=await get('personalized/status');
 test(status.learned===1,'course word is learned '+JSON.stringify(status));
 // Validate bilingual preview vs test behavior: preview stays unmodified (no parentheses).
 test(!d.querySelector('#vocab-preview-list')?.textContent.includes(' (the '), 'preview is not bilingual added');

 // Personalized course composition scoped by book page.
 const personal=await get('quiz?study=personalized&scope=pages&from=1&to=56&types=word&lang=ru&count=40');
 test(personal.questions.some(q=>q.id.startsWith('personal_')),'personalized generated learned word');
 const book=await get('quiz?study=textbook&scope=pages&from=1&to=56&types=word&lang=ru&count=40');
 test(book.questions.every(q=>!q.id.startsWith('personal_')),'book mode excludes vocabulary lessons');
 test(personal.questions.filter(q=>q.id.startsWith('personal_')).length===1,'only mastered word included');

 // Book-mode bilingual options and prompts.
 d.querySelector('[data-page=practice]').click();
 d.querySelector('input[name=training][value=textbook]').click();
 const inputs=d.querySelectorAll('#kind-options input');
 inputs.forEach(x=>x.checked=x.value==='word');
 fire('start');
 await until(()=>!d.getElementById('quiz').hidden&&d.querySelectorAll('#answers .answer').length===8,'book translation quiz');
 let q=lastQuiz.questions[0];
 test(q.direction==='gr-ru' && q.choicesEn.length===8,'Greek→target metadata');
 const rawChoices=q.choices;
 const displayed=Array.from(d.querySelectorAll('#answers .answer')).map(b=>b.textContent);
 test(displayed.some((v,i)=>v.includes('('+q.choicesEn[i]+')') && rawChoices[i]!==q.choicesEn[i]),'English included in target-language choices');
 test(d.getElementById('question-note').textContent.indexOf('(English)')===-1,'instructions unchanged');
 d.querySelectorAll('#answers .answer')[0].click();
 await until(()=>!d.getElementById('next').hidden,'book answer');
 fire('next');
 await until(()=>lastQuiz.questions[1]&&d.getElementById('question-prompt').textContent.includes('('),'target→Greek bilingual prompt');
 q=lastQuiz.questions[1];
 test(q.direction==='ru-gr' && d.getElementById('question-prompt').textContent.includes(q.promptEn),'English hint in translation prompt');
 fire('finish-now');
 await until(()=>!d.getElementById('finished').hidden,'book finished');
 fire('again');

 // Greek dialogue workflow: eight Greek options, any 1–3 gaps,
 // each answer independently graded; render remaining gaps sequentially.
 inputs.forEach(x=>x.checked=x.value==='dialogue');
 fire('start');
 await until(()=>!d.getElementById('quiz').hidden&& !d.getElementById('dialogue-lines').hidden,'dialogue visible');
 q=lastQuiz.questions[0];
 test(q.kind==='dialogue'&&q.gapIndices.length>=1&&q.gapIndices.length<=3,'dialogue shape');
 test(d.querySelectorAll('#answers .answer').length===8,'eight Greek responses');
 test(!d.getElementById('question-prompt').textContent.includes('English'),'no English question');
 test(!/English|Русский|translated|перевод/.test(d.getElementById('dialogue-lines').textContent),'Greek-only dialogue');
 for(let j=0;j<q.gapIndices.length;j++){
   const slot=q.gapIndices[j],right=q.dialogueGaps[slot];
   const option=q.choices.indexOf(right);
   test(option>=0,'correct dialogue option '+j);
   d.querySelectorAll('#answers .answer')[option].click();
   await until(()=>!d.getElementById('next').hidden,'gap '+j+' graded');
   if(j<q.gapIndices.length-1){
     fire('next');
     await until(()=>d.getElementById('question-note').textContent.includes(String(j+2)),'next gap '+j);
     test(d.getElementById('dialogue-lines').textContent.includes(right),'previous Greek line filled');
   }
 }
 const stats=await get('stats');
 test(stats.categories.dialogue.attempts>=q.gapIndices.length,'dialogue answers persisted independently');
 test(!errors.length,'browser exceptions '+JSON.stringify(errors));
 console.log('PASS browser: two practice modes; 1 learned personalized word; book bilingual question/options; Greek-only variable-gap dialogue and stats');
 w.close();
})().catch(e=>{console.error('FAIL browser '+e.stack);w.close();process.exitCode=1});
