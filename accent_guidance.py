"""Accurate accent placement pedagogy for existing derived word cards.

Stress is denoted by tonos on the written vowel (incl. 2nd letter of an
accented digraph). Curated minimal pairs are semantic facts, not generated
nonsense alternatives; show only when the same unaccented base matches.
"""
import unicodedata
PAIR_GLOSSES={
 'ποτε':{'πότε':('when','когда'),'ποτέ':('never / ever','никогда / когда-либо')},
 'ποσο':{'πόσο':('how much','сколько'),'ποσό':('amount','сумма')},
 'μετρο':{'μέτρο':('measure / metre','мера / метр'),'μετρό':('metro','метро')},
 'αλλα':{'άλλα':('other things','другие (ср. р., мн. ч.)'),'αλλά':('but','но')},
}
HINTS={
 'ru':('Ударение (τόνος) ставится над гласной ударного слога. В сочетаниях ει, οι, αι, ου оно пишется над второй буквой.','Сравни: {pairs}. Место ударения может менять значение.'),
 'en':('A tonos marks the vowel of the stressed syllable. In ει, οι, αι, ου, the accent is written over the second letter.','Compare: {pairs}. Stress can change meaning.'),
 'zh':('τόνος 标在重读音节的元音上。在 ει、οι、αι、ου 组合中，重音写在第二个字母上。','比较：{pairs}。重音位置可能改变词义。'),
 'ar':('توضع علامة النبرة فوق حرف العلة في المقطع المشدد. في ει وοι وαι وου تُكتب فوق الحرف الثاني.','قارن: {pairs}. قد يغيّر موضع النبرة المعنى.'),
 'es':('El acento (τόνος) marca la vocal de la sílaba tónica. En ει, οι, αι y ου se escribe sobre la segunda letra.','Compara: {pairs}. La posición del acento puede cambiar el significado.'),
 'pt':('O acento (τόνος) marca a vogal da sílaba tónica. Em ει, οι, αι e ου escreve-se sobre a segunda letra.','Compara: {pairs}. A posição do acento pode alterar o significado.')
}
def _unaccent(word):
 return ''.join(c for c in unicodedata.normalize('NFD',word) if c!='\u0301')
def accents(card,lang):
 if card['kind']!='accent':return None
 generic,contrast=HINTS.get(lang,HINTS['en'])
 items=PAIR_GLOSSES.get(_unaccent(card['accented']))
 if items and card['accented'] in items:
  k=1 if lang=='ru' else 0
  pairs=' / '.join(word+' — '+labels[k] for word,labels in items.items())
  return generic+' '+contrast.format(pairs=pairs)
 return generic
