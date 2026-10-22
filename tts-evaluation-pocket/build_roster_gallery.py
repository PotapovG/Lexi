"""Build static comparative gallery of human-approved/pending Greek TTS voices."""
from pathlib import Path
from html import escape
import json,zipfile,wave
base=Path(__file__).resolve().parent/'long-tests'
text=' '.join([
 'Το πρωί ξυπνάω νωρίς και ανοίγω το παράθυρο.',
 'Στη γειτονιά μου έχει ήλιο και τα παιδιά παίζουν στην αυλή.',
 'Μετά πίνω έναν καφέ και πηγαίνω στο κέντρο της Λευκωσίας.',
 'Στον δρόμο συναντώ τη Μαρία και τη ρωτάω: Πού μένεις; Εκείνη μου απαντάει: Μένω στη Λευκωσία.'
])
groups=[
 ('Женские голоса',[
  ('athina','Афина','Одобрен','pocket'),
  ('eleni','Елени','Одобрен','pocket'),
  ('katerina','Катерина','Одобрен','pocket')]),
 ('Мужские голоса',[
  ('kostas','Костас','Одобрен','pocket'),
  ('spyros','Спирос','Одобрен','pocket'),
  ('nikos','Никос','Одобрен · Pocket TTS','pocket')])
]
variants={'pocket':[('02_clear_phrases','Чётче · по предложениям'),('03_lively_phrases','Живее · по предложениям')],
          'meta':[('04_even','Ровнее · Meta MMS'),('05_expressive','Живее · Meta MMS')]}
files=[];sections=[];persons=[]
for heading,people in groups:
 cards=[]
 for vid,name,status,engine in people:
  players=[]
  for version,label in variants[engine]:
   filename=f'{vid}_{version}.wav'
   p=base/filename
   assert p.exists(),filename
   with wave.open(str(p),'rb') as wav:
    dur=round(wav.getnframes()/wav.getframerate(),1)
    assert wav.getframerate() in (16000,24000) and wav.getnchannels()==1
   files.append(filename)
   players.append(f'<div class="variation"><span>{escape(label)} · {dur:g} с</span><audio controls preload="none" src="{filename}"></audio></div>')
  cards.append(f'<article><h3>{escape(name)}</h3><p class="small">{escape(status)}</p>{"".join(players)}</article>')
  persons.append({'id':vid,'display':name,'status':status,'engine':engine,'samples':[f'{vid}_{version}.wav' for version,_ in variants[engine]]})
 sections.append('<section><h2>'+escape(heading)+'</h2><div class="grid">'+''.join(cards)+'</div></section>')
assert len(files)==12 and len(set(files))==12
(base/'all-voices.zip').unlink(missing_ok=True)
with zipfile.ZipFile(base/'all-voices.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for filename in files:z.write(base/filename,filename)
manifest={'experimental':True,'student_listening_enabled':False,'text':text,'approved_current':['athina','eleni','katerina','kostas','spyros','nikos'],'proposed_female':[],'proposed_male':[],'backup_male':[],'presets':persons}
(base/'ensemble-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
html='''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Λέξη — 3 женских + 3 мужских голоса</title><link rel="stylesheet" href="style.css"></head><body><main>
<p class="eyebrow">ΛΈΞΗ · СРАВНЕНИЕ ГОЛОСОВ</p>
<h1>3 женских и 3 мужских голоса</h1>
<p>Все произносят <b>один и тот же греческий текст</b>. Все шесть голосовых профилей одобрены для дальнейшей подготовки аудиотеки. Два варианта озвучки каждого, одной локальной моделью.</p>
<p class="notice"><b>Аудирование ALPHA пока отключено.</b> Здесь только демонстрации. Нет платных API, дополнительных учётных записей и записи голоса пользователя.</p>
<h2>Один текст для сравнения</h2><blockquote lang="el" dir="ltr">'''+escape(text)+'''</blockquote>
'''+''.join(sections)+'''
<p class="downloads"><a href="all-voices.zip" download>Скачать все 12 записей одним ZIP</a></p>
<footer>Pocket TTS Greek — <a href="https://huggingface.co/myned-ai/pocket-tts-greek">myned-ai</a>, CC BY 4.0. Аудио создано локально, заранее. Шесть разных голосовых профилей одной модели. Голосовые профили Pocket поставляются автором модели и основаны на лицензированных примерах Common Voice. Качество длинных фраз пользователь оценил; качество отдельных коротких слов проверяется отдельно.</footer></main></body></html>'''
(base/'index.html').write_text(html)
css='''*{box-sizing:border-box}body{margin:0;background:#0b1525;color:#ebeff7;font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1130px;margin:auto;padding:30px 20px 60px}.eyebrow{color:#edc87b;font-size:12px;letter-spacing:2px;font-weight:700}h1{color:#f3d38e;line-height:1.2;font-size:clamp(26px,4vw,38px)}h2{font-size:22px;color:#f3d38e;margin:28px 0 13px}h3{font-size:19px;margin:0 0 2px}.notice{padding:12px 16px;border:1px solid #b2964b;border-radius:12px;background:#292532;color:#f3d9a5}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,310px),1fr));gap:14px}.grid article{border:1px solid #3c4c65;background:#17283b;border-radius:14px;padding:18px}.small{font-size:13px;color:#b6c4d6;margin:0 0 12px}blockquote{background:#16263b;border:1px solid #394e63;border-radius:12px;margin:0;padding:20px;color:#f2f5ff;font-size:18px;line-height:1.9}.variation{margin:10px 0 16px}.variation span{font-size:13px;display:block;margin-bottom:5px;color:#c8d5e5}.variation audio{width:100%;height:44px}.downloads{margin:29px 0}a{color:#f3d18b}footer{border-top:1px solid #3c4c65;padding-top:17px;font-size:13px;color:#b4c1d2}@media(max-width:480px){main{padding:20px 14px 40px}blockquote{font-size:16px;padding:14px}}'''
(base/'style.css').write_text(css)
for f in ('index.html','style.css','all-voices.zip','ensemble-manifest.json'):(base/f).chmod(0o644)
print('GALLERY_RENDERED',len(persons),'different voice profiles',len(files),'WAV','ZIP',round((base/'all-voices.zip').stat().st_size/1024/1024,2),'MB')
