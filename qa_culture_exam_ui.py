"""CULT-06 mock exam UI integration smoke.

Static contract only. Real mobile/accessibility QA remains in #41.
"""
from pathlib import Path

root=Path(__file__).parent
app=(root/"app.js").read_text(encoding="utf-8")
html=(root/"index.html").read_text(encoding="utf-8")
css=(root/"styles.css").read_text(encoding="utf-8")
ui=(root/"culture_ui.js").read_text(encoding="utf-8")
exam=(root/"culture_exam.py").read_text(encoding="utf-8")

for item in ("culture-exam-navigation","culture-exam-prev","culture-exam-next",
             "culture-exam-flag","culture-exam-review"):
    assert html.count('id="'+item+'"')==1,item
assert html.count('id="quiz"')==1, "must reuse existing Lexi quiz card"
assert html.count('id="answers"')==1, "must reuse existing answer choices"
assert html.count('id="finished"')==1, "must reuse existing finish panel"
assert 'id="culture-exam" disabled' in html, "initially fail closed until review gate"
assert 'culture_ui.js?v=2' in html
assert 'app.js?v=48' in html

for symbol in (
    "function enterCultureExam(", "function renderCultureExam(",
    "function changeCultureExamAnswer(", "function flagCultureExamQuestion(",
    "function navigateCultureExam(", "function finishCultureExam(",
    "function restoreCultureExam(", "async function startCultureExam(",
    "culture/exam?sessionId=", "scope:\"culture\",mode:\"exam\"",
    'startExam:()=>startCultureExam()', "const examRestored=await restoreCultureExam()",
    'state.exam?.status==="active"',
    "state.examSkew", "state.examIndex",
    'show("culture-wording-wrap",false)',
    'show("culture-exam-navigation",true)',
    'show("culture-exam-review",true)',
    "q.optionTranslations", "q.correctIndex", "q.source",
):
    assert symbol in app,symbol

# No answer keys or translations in the exam's pre-finish payload.
# These are only used by the existing #finished review renderer.
assert 'const result=expired?' in app
assert 'const result=await examRequest({action:"start"' in app
assert 'window.lexiCultureBridge.startExam()' in ui
assert '(stats?.availableFacts||0)>=25' in ui
assert 'culture-exam").disabled=working||!examReady' in ui
assert 'def _safe_view(row,now):' in exam
assert 'if finished:' in exam

assert ".culture-exam-navigation" in css
assert ".culture-exam-review" in css
assert ".exam-selected" in css
assert "@media(max-width:360px)" in css
print("PASS CULT-06 exam UI: existing Lexi question/finish DOM, server session profile, review gate")
