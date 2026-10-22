from pathlib import Path
from html import escape
import json,zipfile
root=Path(__file__).resolve().parent/'short-tests'
data=json.loads((root/'manifest.json').read_text())
assert len(data['samples'])==36
voices={'athina':'Афина · женский','eleni':'Елени · женский','katerina':'Катерина · женский','kostas':'Костас · мужской','spyros':'Спирос · мужской','nikos':'Никос · мужской'}
styles={'clear':'Чётче','lively':'Живее'}
kinds={'word':'Отдельное слово','phrase':'Короткая фраза','sentence':'Предложение'}
items={r['file']:r for r in data['samples']}
sections=[]
for voice,display in voices.items():
 grid=[]
 for kind,label in kinds.items():
  players=[]
  for style,style_title in styles.items():
   file=f'{voice}_{style}_{kind}.wav'
   assert file in items and (root/file).is_file()
   players.append(f'<div class="variant"><span>{style_title} · {items[file]["duration"]} c</span><audio controls preload="none" src="{file}"></audio></div>')
  grid.append(f'<article><h3>{label}</h3>{"".join(players)}</article>')
 sections.append(f'<section><h2>{display}</h2><div class="grid">{"".join(grid)}</div></section>')
html='''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Λέξη — короткие слова и фразы · Pocket TTS</title><link rel="stylesheet" href="style.css"></head><body><main><p class="eyebrow">ΛΈΞΗ · ПРОВЕРКА ЧЁТКОСТИ</p><h1>Шесть голосов на коротких карточках</h1><p>Важная контрольная проверка после удачных длинных абзацев. Для каждого из одобренных голосов есть слово, короткая фраза и предложение — в режимах «Чётче» и «Живее». Тест нужен, чтобы увидеть, не проглатывает ли модель короткие слова.</p><p class="notice">Аудирование ALPHA отключено. Учебные результаты не изменены; данные здесь только для оценки голосов.</p><h2>Одинаковые тексты</h2><blockquote lang="el" dir="ltr">ελεύθερη<br>Η μητέρα μου είναι δασκάλα.<br>Ο φίλος μου έχει δύο παιδιά, έναν γιο και μία κόρη.</blockquote>'''+''.join(sections)+'''<p><a href="short-samples.zip" download>Скачать все 36 WAV одним ZIP</a></p><footer>Генерация локальная, движок <a href="https://huggingface.co/myned-ai/pocket-tts-greek">Pocket TTS Greek</a> (CC BY 4.0), шесть готовых голосовых профилей. Ни микрофонов, ни платных API.</footer></main></body></html>'''
css='''*{box-sizing:border-box}body{background:#0d1728;color:#e5ecf7;font:16px/1.55 system-ui,Arial,sans-serif;margin:0}main{max-width:1060px;padding:26px 18px 70px;margin:auto}.eyebrow{color:#e9cb8a;letter-spacing:2px;font-size:12px;font-weight:700}h1{color:#f4d18c;font-size:clamp(25px,4vw,38px);line-height:1.2}.notice{padding:13px 17px;border-radius:12px;border:1px solid #8b7a4e;background:#272437;color:#f5d6a0}blockquote{margin:10px 0 22px;border-radius:14px;background:#18293c;border:1px solid #40576d;color:#e9eff8;padding:19px;font-size:18px;line-height:1.9}h2{margin:28px 0 12px;color:#f5d18d}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,285px),1fr));gap:13px}.grid article{padding:17px;border:1px solid #354b64;border-radius:13px;background:#15273c}.grid h3{margin:0 0 11px;font-size:17px}.variant{margin-bottom:11px}.variant span{display:block;color:#b8cada;font-size:13px}.variant audio{display:block;width:100%;height:45px;margin-top:4px}a{color:#f4d18b}footer{border-top:1px solid #354b64;color:#bac8d6;padding-top:17px;margin-top:28px;font-size:13px}'''
(root/'index.html').write_text(html,encoding='utf-8');(root/'style.css').write_text(css,encoding='utf-8')
with zipfile.ZipFile(root/'short-samples.zip','w',compression=zipfile.ZIP_DEFLATED) as archive:
 for f in items: archive.write(root/f,f)
for file in ('index.html','style.css','short-samples.zip'):(root/file).chmod(0o644)
root.chmod(0o755)
print('SHORT PREVIEW READY',len(items),'clips')
