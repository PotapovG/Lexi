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
 w.HTMLMediaElement.prototype.play=function(){this.playbackRate=this.playbackRate||1;return Promise.resolve();};
 w.HTMLMediaElement.prototype.pause=function(){};
 w.eval(fs.readFileSync('/app/app.js','utf8'));
 w.eval(fs.readFileSync('/app/vocab.js','utf8'));
 await until(()=>!d.getElementById('auth-gate').hidden,'auth gate');
 d.getElementById('auth-name').value='Listening QA '+(process.env.TEST_NICK||'One');
 fire('auth-form','submit');
 await until(()=>!d.getElementById('auth-success').hidden,'registered');
 fire('auth-enter');
 await until(()=>d.getElementById('auth-gate').hidden,'logged in');
 const scope=d.querySelector('input[name=scope][value=listening]');
 test(Boolean(scope),'separate listening mode exists');
 scope.click();
 test(!d.getElementById('chapter-controls').hidden,'chapter picker visible');
 test(d.getElementById('material-config-group').hidden,'unrelated card kinds hidden');
 let chosen=[...d.querySelectorAll('#chapter-grid input:checked')].map(x=>Number(x.value));
 test(chosen.length>=1,'book chapters selected by default');
 d.querySelectorAll('#chapter-grid input').forEach(x=>x.checked=Number(x.value)===1);
 fire('estimate-capacity');
 await until(()=>d.getElementById('capacity-result').textContent.includes('уникальн'),'listen capacity');
 fire('start');
 await until(()=>!d.getElementById('quiz').hidden&&lastQuiz?.questions?.[0]?.kind==='listening','listening quiz');
 const q=lastQuiz.questions[0];
 test(q.audioUrl.includes('/greek/audio/')&&q.audioUrl.endsWith('.wav'),'static audio URL');
 test(!('gr' in q)&&!('transcript' in q),'no Greek leaked before answer');
 test(d.getElementById('listening-reveal').hidden,'transcript hidden');
 test(!d.getElementById('listening-controls').hidden,'play button shown');
 test([...d.querySelectorAll('#answers .answer')].every(b=>b.disabled),'choices disabled before listening');
 test(d.getElementById('question-prompt').textContent==='Что ты услышал?','generic listening prompt');
 fire('listen-slow');
 await until(()=>[...d.querySelectorAll('#answers .answer')].every(b=>!b.disabled),'audio playback unlocked');
 test(d.getElementById('listening-audio').playbackRate===0.8,'slow audio speed');
 fire('listen-play');
 await until(()=>d.getElementById('listening-audio').playbackRate===1,'normal audio speed');
 d.querySelectorAll('#answers .answer')[0].click();
 await until(()=>!d.getElementById('next').hidden,'answer graded');
 test(!d.getElementById('listening-reveal').hidden,'Greek text revealed after grading');
 test(/[α-ωά-ώΑ-ΩΆ-Ώ]/u.test(d.getElementById('listening-reveal').textContent),'genuine Greek transcript');
 test(!errors.length,'no JS error '+JSON.stringify(errors));
 console.log('PASS jsdom: separate listening, chapters/capacity, hidden transcript, playback gates, slower/normal, graded reveal');
 w.close();
})().catch(e=>{console.error('FAIL '+e.stack);w.close();process.exitCode=1});
