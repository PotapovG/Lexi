"""CULT-04 shared UI contract smoke.

This is a static integration guard; browser accessibility and mobile QA still
need real-device checks. It does not approve unpublished Culture questions.
"""
from pathlib import Path

root=Path(__file__).parent
html=(root/"index.html").read_text(encoding="utf-8")
app=(root/"app.js").read_text(encoding="utf-8")
ui=(root/"culture_ui.js").read_text(encoding="utf-8")
css=(root/"styles.css").read_text(encoding="utf-8")
adapter=(root/"culture_adapter.py").read_text(encoding="utf-8")

assert html.count('data-page="culture"')==1, "one navigation entry, not parallel learner modes"
assert html.count('id="culture-view"')==1
assert 'culture_ui.js?v=1' in html
for element in ("culture-start","culture-review","culture-exam","culture-status",
                "culture-topics","culture-duration","culture-lang","culture-srs"):
    assert html.count('id="'+element+'"')==1, element
assert 'id="culture-exam" disabled' in html, "no mock exam before secure session #39"
for marker in (
    'window.lexiCultureBridge=', 'start:options=>startQuiz(',
    'for(const id of ["practice","vocab","weak","stats","leaderboard","tracks","life","board","culture"])',
    'scope:"culture"', 'q.kind==="culture"', 'result.optionTranslations',
    'state.settings?.scope==="culture"', 'state.settings.srsOptIn'
):
    assert marker in app, marker
assert 'bridge.api("catalog?scope=culture")' in ui
assert 'bridge.api("stats?scope=culture")' in ui
assert 'culture-exam").disabled=true' in ui
assert 'if(!meta?.available' not in ui # only verified bank enables start
assert "window.lexiCultureBridge.start" in ui
assert 'card["options"]' in adapter and '"optionTranslations"' in adapter
assert ".culture-topics" in css and "@media(max-width:360px)" in css

# Never add a separate quiz/score implementation in the culture UI script.
for disallowed in ("correctIndex", "correct_index", "answerIndex", "fetch(\"/api/answer\""):
    assert disallowed not in ui, disallowed
print("PASS CULT-04: one Lexi mode, shared quiz bridge, scoped catalog/stats, no mock-exam impersonation")


# CULT-04 assisted wording: question-instruction glosses only, never an answer.
for element in ("culture-wording-wrap", "culture-wording-button", "culture-wording-text"):
    assert html.count('id="'+element+'"')==1, element
for marker in (
    'cultureAssisted:state.cultureAssisted',
    'state.cultureAssisted=(saved.cultureAssisted',
    'state.cultureAssisted[state.current.id]=true',
    'assisted:!!state.cultureAssisted[q.id]',
    'state.settings?.mode!=="exam"',
    'function cultureWordingHint(question)',
    'show("culture-wording-wrap",showHint)',
    'showCultureWording',
):
    assert marker in app, marker
assert ".culture-hint-wrap" in css
assert 'id="culture-exam" disabled' in html
# The full choice translation is still returned only from the server AFTER grading.
assert 'result.optionTranslations' in app
