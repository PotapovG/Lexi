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
 await until(()=>!d.getElementById('auth-gate').hidden,'gate');
 d.getElementById('auth-name').value='Form QA '+(process.env.TEST_NICK||'G');
 fire('auth-form','submit');await until(()=>!d.getElementById('auth-success').hidden,'registration');
 fire('auth-enter');await until(()=>d.getElementById('auth-gate').hidden,'entered');
 test(d.querySelector('#kind-options input[value=article]')?.parentElement.textContent.includes('Артикли'),'articles selectable');
 test(d.querySelector('#kind-options input[value=order]')?.parentElement.textContent.includes('Собрать'),'order selectable');
 d.querySelector('input[name=scope][value=pages]').click();
 function restrict(kind,from,to){
  d.querySelectorAll('#kind-options input').forEach(x=>x.checked=x.value===kind);
  d.getElementById('page-from').value=from;
  d.getElementById('page-to').value=to;
 }
 restrict('article',29,29);fire('start');
 await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.questions?.[0]?.kind==='article','article page 29');
 let q=lastQuiz.questions[0];
 test(q.choices.length===8 && q.prompt.includes('___'),'article 8 Greek choices');
 test(!d.getElementById('order-builder').hidden===false,'order composer hidden on article');
 const i=q.choices.indexOf('στη');test(i>=0,'preposition στη available');
 d.querySelectorAll('#answers .answer')[i].click();
 await until(()=>!d.getElementById('next').hidden,'article response');
 test(d.getElementById('feedback').className.includes('good'),'correct Greek preposition');
 fire('next');await until(()=>!d.getElementById('finished').hidden,'article finishes');
 fire('again');
 restrict('order',17,17);fire('start');
 await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.questions?.[0]?.kind==='order','order page17');
 q=lastQuiz.questions[0];
 test(q.tokens.length>=5 && d.querySelectorAll('.answer.order-word').length===q.tokens.length,'word pieces rendered');
 test(!d.getElementById('order-builder').hidden && !d.getElementById('order-tools').hidden,'Greek composition controls visible');
 test(d.getElementById('order-check').disabled,'cannot check incomplete sentence');
 const tapByText=(word)=>{
  const buttons=Array.from(d.querySelectorAll('.answer.order-word'));
  const b=buttons.find(x=>x.textContent===word&&!x.disabled);
  test(Boolean(b),'unused token exists '+word);b.click();
 };
 tapByText('Γεια');
 test(d.getElementById('order-draft').textContent==='Γεια','draft updates on click');
 fire('order-undo');test(d.getElementById('order-draft').textContent==='…','undo clears last token');
 tapByText('Γεια');tapByText('σου');
 fire('order-reset');test(d.getElementById('order-draft').textContent==='…','reset clears draft');
 const model=q.id==='order_patk01_001'?'Γεια σου, είμαι ο Μάριος και αυτή είναι η Λένα.':null;
 test(Boolean(model),'known first original sentence');
 const plain=model.split(' ').map(x=>x.replace(/[.,;:!?]+$/g,'')).join(' ');
 for(const word of plain.split(' '))tapByText(word);
 test(d.getElementById('order-check').disabled===false,'check enabled only on full sentence');
 test(d.getElementById('order-draft').textContent===plain,'reconstructed words before punctuation');
 fire('order-check');
 await until(()=>!d.getElementById('next').hidden,'word-order scored');
 test(d.getElementById('feedback').className.includes('good'),'complete order accepted');
 test(d.getElementById('order-draft').textContent===model,'punctuation restored automatically on correct answer');
 test(d.getElementById('order-check').disabled,'cannot submit twice');
 fire('next');await until(()=>!d.getElementById('finished').hidden,'order completes');
 fire('again');
 restrict('phrase',14,14);fire('start');
 await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.questions?.[0]?.id==='p001','curated multiple answer');
 test(!d.getElementById('answers').classList.contains('order-tokens'),'word order styling cleared for normal multiple choice');
 q=lastQuiz.questions[0];
 const synonym=q.choices.indexOf('Как тебя зовут');
 test(synonym>=0,'reviewed alternate translated answer visible');
 d.querySelectorAll('#answers .answer')[synonym].click();
 await until(()=>!d.getElementById('next').hidden,'alias graded');
 test(d.getElementById('feedback').className.includes('good'),'alternative valid translation accepted');
 test(d.querySelectorAll('#answers .answer.is-correct').length>=2,'all curated valid options highlighted');
 test(!errors.length,'browser JS errors '+JSON.stringify(errors));
 console.log('PASS article 8 choices, reconstructed tapped Greek sentence with undo/reset, alias correct twice');
 w.close();
})().catch(e=>{console.error('FAIL '+e.stack);w.close();process.exitCode=1});
