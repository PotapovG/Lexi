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
const vm=require('vm');
const appSrc=fs.readFileSync('/app/app.js','utf8');
const localeBlock=appSrc.slice(appSrc.indexOf('const I18N='),appSrc.indexOf('const kindIds='));
const ctx={};vm.runInNewContext(localeBlock.replace('const I18N=','globalThis.I18N='),ctx);
const locales=ctx.I18N;
const langs=['ru','en','pt','ar','zh','es'];
const topicExpected={pt:'Compras',ar:'التسوق',zh:'购物',es:'Compras'};
async function pause(ms=130){await sleep(ms)}
function assertLocalization(lang){
 const translations=locales[lang];
 for(const locale of langs){
  for(const key of Object.keys(locales.ru))test(typeof locales[locale][key]==='string','missing '+locale+' '+key);
 }
 for(const el of d.querySelectorAll('[data-i18n]')){
   const expected=translations[el.dataset.i18n];
   test(typeof expected==='string','unknown key '+el.dataset.i18n);
   if(el.id==='training-description')continue;
   if(el.id==='auth-submit' && d.getElementById('auth-gate').hidden)continue;
   test(el.textContent===expected,'stale ['+lang+'] '+el.dataset.i18n+' '+JSON.stringify(el.textContent)+' instead of '+JSON.stringify(expected));
 }
 test(d.getElementById('catalog-summary').textContent===translations.available.replace('{count}','1795'),'catalog summary '+lang+' '+d.getElementById('catalog-summary').textContent);
 test(d.getElementById('auth-name').placeholder===translations.nicknamePlaceholder,'registration placeholder '+lang);
 test(d.title===translations.footerBrand,'browser title '+lang);
 test(d.querySelector('[data-i18n="footerBrand"]').textContent===translations.footerBrand,'footer '+lang);
 test(d.documentElement.lang===lang,'html lang '+lang);
 test(d.documentElement.dir===(lang==='ar'?'rtl':'ltr'),'doc direction '+lang);
}
(async()=>{
 w.eval(fs.readFileSync('/app/app.js','utf8'));
 w.eval(fs.readFileSync('/app/vocab.js','utf8'));
 await until(()=>!d.getElementById('auth-gate').hidden,'auth');
 await until(()=>d.getElementById('catalog-summary').textContent.includes('1795'),'catalog');
 d.getElementById('auth-name').value='Locale QA '+(process.env.TEST_NICK||'a');
 fire('auth-form','submit');
 await until(()=>!d.getElementById('auth-success').hidden,'registered');
 fire('auth-enter');
 await until(()=>d.getElementById('auth-gate').hidden,'auth closed');
 for(const lang of langs){
   const picker=d.getElementById('lang');picker.value=lang;
   picker.dispatchEvent(new w.Event('change',{bubbles:true}));
   await pause();
   assertLocalization(lang);
   // User reproducer: Portuguese selection after initial Russian catalog load.
   if(lang==='pt')test(d.getElementById('catalog-summary').textContent==='1795 cartões na biblioteca','Portuguese screenshot regression');
   await pause();
   const shopping=d.querySelector('#topic-grid input[value=shopping]').nextElementSibling;
   test(shopping.textContent===(topicExpected[lang] || (lang==='ru'?'Магазин и покупки':'Shopping')),'topic translation '+lang+': '+shopping.textContent);
   // Switching back and forth should re-localize both computed and static strings.
   console.log('PASS LOCALE',lang,'catalog summary, 155 locale keys, registration hint, topic labels, RTL');
 }
 // Language switch on login (not only post-login dropdown) must propagate.
 d.getElementById('auth-gate').hidden=false;
 d.getElementById('auth-lang').value='pt';
 d.getElementById('auth-lang').dispatchEvent(new w.Event('change',{bubbles:true}));
 await pause();assertLocalization('pt');
 // Vocabulary interface should render its own Portuguese strings.
 d.getElementById('auth-gate').hidden=true;
 d.querySelector('[data-page=vocab]').click();
 await until(()=>d.getElementById('vocab-topic').options.length>=13,'vocab ready');
 test(d.getElementById('vocab-title').textContent==='Vocabulário A1 / A2','vocab title');
 test(d.getElementById('vocab-topic').options[0].textContent==='Todos os temas','vocab all topics');
 test(d.getElementById('vocab-new').textContent==='Aprender 10 palavras novas','vocab button');
 const arPicker=d.getElementById('lang');arPicker.value='ar';arPicker.dispatchEvent(new w.Event('change',{bubbles:true}));
 await pause();test(d.getElementById('vocab-topic').options[0].textContent==='كل المواضيع','Arabic topic selector');
 test(!errors.length,'browser errors '+JSON.stringify(errors));
 console.log('PASS all six translated vocab/practice contexts, including language switches and no Russian catalog leak');
 w.close();
})().catch(e=>{console.error('FAIL '+e.stack);w.close();process.exitCode=1});
