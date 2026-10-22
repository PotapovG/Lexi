"""Pedagogical soft acceptance for written final ν in selected feminine articles.

School standard typically drops final -ν before μ/λ/φ/ζ; many speakers and
writers nevertheless retain it. In a case/gender *selection* exercise the
retained feminine accusative is accepted (without miss debt), while the
orthographically preferred textbook form is always explained.

This is not blanket equivalence: e.g. τη Άννα remains wrong (vowel), as do
different case/gender options such as η and τον. Masculine τον is unchanged.
"""
from html import escape

_DESCRIPTIONS = {
 'ru': 'По школьному орфографическому правилу перед «{letter}» конечное -ν обычно опускают: {preferred}. Вариант с -ν здесь тоже засчитывается: род и падеж правильные. Это подсказка о написании, а не ошибка в грамматике.',
 'en': 'School spelling normally drops final -ν before “{letter}”: {preferred}. Keeping -ν is also accepted here: the gender and case are correct. This is a spelling note, not a grammar mistake.',
 'zh': '按照学校正字法，遇到“{letter}”前通常省略词尾 -ν：{preferred}。此处保留 -ν 也算正确，因为性和格并没有错误；这是拼写提示。',
 'ar': 'وفق قاعدة الكتابة المدرسية يُحذف حرف -ν عادة قبل «{letter}»: {preferred}. تُقبل هنا أيضًا الصيغة التي تحتفظ بـ -ν لأن الجنس والحالة الإعرابية صحيحان؛ هذه ملاحظة إملائية وليست خطأً نحويًا.',
 'es': 'La ortografía escolar suele omitir la -ν final ante «{letter}»: {preferred}. También se acepta aquí conservarla: el género y el caso son correctos. Es una nota ortográfica, no un error gramatical.',
 'pt': 'A ortografia escolar costuma omitir o -ν final antes de «{letter}»: {preferred}. Aqui também se aceita mantê-lo: o género e o caso estão corretos. É uma nota ortográfica, não um erro gramatical.',
}
def explanation(card,lang):
    forms=card.get('acceptedForms') or []
    if len(forms)<2:return None
    context=card['prompt'].split('___',1)[1].strip()
    letter=context[0].casefold()
    assert letter in {'μ','λ','φ','ζ'}
    preferred=card['correct']+' '+context
    return _DESCRIPTIONS.get(lang,_DESCRIPTIONS['en']).format(letter=letter,preferred=preferred)
