"""Reviewed present-tense 17 verb × six persons; explicit ES/PT subject/person inflection."""
import json
from pathlib import Path
ROOT=Path(__file__).parent
path=ROOT/'verb_phrase_locales.json'
atlas=json.loads(path.read_text())
es={'γράφω':('escribo,escribes,escribe,escribimos,escribís,escriben','un mensaje'),
'μένω':('vivo,vives,vive,vivimos,vivís,viven','en Nicosia'),
'διαβάζω':('leo,lees,lee,leemos,leéis,leen','un libro'),
'δουλεύω':('trabajo,trabajas,trabaja,trabajamos,trabajáis,trabajan','en la oficina'),
'αγοράζω':('compro,compras,compra,compramos,compráis,compran','pan'),
'παίζω':('juego,juegas,juega,jugamos,jugáis,juegan','en el parque'),
'μαθαίνω':('aprendo,aprendes,aprende,aprendemos,aprendéis,aprenden','griego'),
'μιλάω':('hablo,hablas,habla,hablamos,habláis,hablan','griego'),
'ρωτάω':('pregunto,preguntas,pregunta,preguntamos,preguntáis,preguntan','al profesor'),
'αγαπάω':('amo,amas,ama,amamos,amáis,aman','la música'),
'περπατάω':('camino,caminas,camina,caminamos,camináis,caminan','por la ciudad'),
'απαντάω':('respondo,respondes,responde,respondemos,respondéis,responden','a la pregunta'),
'μπορώ':('puedo,puedes,puede,podemos,podéis,pueden','ayudar'),
'οδηγώ':('conduzco,conduces,conduce,conducimos,conducís,conducen','por la ciudad'),
'τηλεφωνώ':('llamo,llamas,llama,llamamos,llamáis,llaman','a mi amigo'),
'θεωρώ':('creo,crees,cree,creemos,creéis,creen','que está bien'),
'χρησιμοποιώ':('uso,usas,usa,usamos,usáis,usan','el ordenador')}
pt={'γράφω':('escrevo,escreves,escreve,escrevemos,escrevem,escrevem','uma mensagem'),
'μένω':('vivo,vives,vive,vivemos,vivem,vivem','em Nicósia'),
'διαβάζω':('leio,lês,lê,lemos,leem,leem','um livro'),
'δουλεύω':('trabalho,trabalhas,trabalha,trabalhamos,trabalham,trabalham','no escritório'),
'αγοράζω':('compro,compras,compra,compramos,compram,compram','pão'),
'παίζω':('brinco,brincas,brinca,brincamos,brincam,brincam','no parque'),
'μαθαίνω':('aprendo,aprendes,aprende,aprendemos,aprendem,aprendem','grego'),
'μιλάω':('falo,falas,fala,falamos,falam,falam','grego'),
'ρωτάω':('pergunto,perguntas,pergunta,perguntamos,perguntam,perguntam','ao professor'),
'αγαπάω':('adoro,adoras,adora,adoramos,adoram,adoram','música'),
'περπατάω':('caminho,caminhas,caminha,caminhamos,caminham,caminham','pela cidade'),
'απαντάω':('respondo,respondes,responde,respondemos,respondem,respondem','à pergunta'),
'μπορώ':('posso,podes,pode,podemos,podem,podem','ajudar'),
'οδηγώ':('conduzo,conduzes,conduz,conduzimos,conduzem,conduzem','pela cidade'),
'τηλεφωνώ':('telefono,telefonas,telefona,telefonamos,telefonam,telefonam','ao meu amigo'),
'θεωρώ':('acho,achas,acha,achamos,acham,acham','que isso é bom'),
'χρησιμοποιώ':('uso,usas,usa,usamos,usam,usam','o computador')}
zh={'γράφω':('写','一条消息'),'μένω':('住','在尼科西亚'),
'διαβάζω':('读','一本书'),'δουλεύω':('工作','在办公室'),
'αγοράζω':('买','面包'),'παίζω':('玩','在公园'),
'μαθαίνω':('学习','希腊语'),'μιλάω':('说','希腊语'),
'ρωτάω':('问','老师'),'αγαπάω':('喜欢','音乐'),
'περπατάω':('散步','在城里'),'απαντάω':('回答','这个问题'),
'μπορώ':('能','帮忙'),'οδηγώ':('开车','在城里'),
'τηλεφωνώ':('打电话','给我的朋友'),'θεωρώ':('认为','这很好'),
'χρησιμοποιώ':('使用','电脑')}
subj_es=['Yo','Tú','Él/ella','Nosotros','Vosotros','Ellos/ellas']
subj_pt=['Eu','Tu','Ele/ela','Nós','Vocês','Eles/elas']
subj_zh=['我','你','他/她','我们','你们','他们/她们']
for lang,source,subjects in [('es',es,subj_es),('pt',pt,subj_pt)]:
  for lemma,(verbs,complement) in source.items():
    forms=verbs.split(',')
    assert len(forms)==6,(lemma,forms)
    for person in range(6):
      translated=f'{subjects[person]} {forms[person]} {complement}'
      atlas[lang][f'{lemma}:{person}']=translated
for lemma,(verb,obj) in zh.items():
 for person in range(6):
  subject=subj_zh[person]
  if lemma=='μένω':text=f'{subject}{obj.replace("在","住在",1)}'
  elif lemma in ('δουλεύω','παίζω','περπατάω','οδηγώ'):text=f'{subject}{obj}{verb}'
  elif lemma=='τηλεφωνώ':text=f'{subject}{obj}{verb}'
  elif lemma=='θεωρώ':text=f'{subject}{verb}{obj}'
  else:text=f'{subject}{verb}{obj}'
  atlas['zh'][f'{lemma}:{person}']=text
assert all(len(atlas[lang])==102 for lang in ('es','pt','zh'))
path.write_text(json.dumps(atlas,ensure_ascii=False,indent=1)+'\n')
print('Reviewed present tense: 17 verb paradigms × 6 persons × 3 locales = 306 translations')
for lemma in ('διαβάζω','μιλάω','μένω'):
 for lang in ('es','pt','zh'):
  print(lemma,lang,[atlas[lang][f'{lemma}:{p}'] for p in (0,1,4)])
