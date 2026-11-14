"""CULT-04: shared UI contract and server payload safety.

Pure stdlib checks; tests contract of the existing app, not an independent
browser/a11y sign-off or human editorial review.
"""
from pathlib import Path
import json
import re
import culture_adapter

ROOT=Path(__file__).parent
html=(ROOT/"index.html").read_text(encoding="utf-8")
js=(ROOT/"app.js").read_text(encoding="utf-8")
css=(ROOT/"styles.css").read_text(encoding="utf-8")

# Exactly one top-level learner-facing Culture mode, no second app/router.
assert html.count('data-page="culture"')==1
assert html.count('id="culture-view"')==1
assert html.count('id="quiz"')==1
assert html.count('id="answers"')==1
assert html.count('id="feedback"')==1

required_ids=("culture-language","culture-topics","culture-start",
              "culture-weak-start","culture-available","culture-practiced",
              "culture-weak-count","culture-message","culture-exam",
              "culture-hint-wrap","culture-hint-button","culture-hint-text")
for identifier in required_ids:
    assert html.count(f'id="{identifier}"')==1, identifier

assert 'id="culture-exam" class="secondary" disabled' in html, "Exam must be gated by #39"
assert 'api("catalog?scope=culture")' in js
assert 'api("stats?scope=culture")' in js
assert 'startQuiz(weak,false,true)' in js
assert 'setPage(culture?"culture":"practice")' in js
assert 'setPage(isCulture()?"culture":"practice")' in js
assert 'cultureAssisted:state.cultureAssisted' in js
assert 'assisted:!!state.cultureAssisted[q.id]' in js
assert 'result.originalChoices' in js and 'result.translationChoices' in js
assert 'id==="practice"&&cultureSession' in js
assert 'q.kind==="culture"?["Α","Β","Γ","Δ"][i]' in js
assert 'show("culture-hint-wrap",q.kind==="culture")' in js
assert '#culture-view' in css and '@media(max-width:600px)' in css

# Client receives a shuffled question but never a source/correct answer.
fixture=json.loads((ROOT/"tests/fixtures/culture/sample_corpus.json").read_text(encoding="utf-8"))
card=culture_adapter.to_card(fixture["questions"][0],fixture["facts"][0])
shown=culture_adapter.format_card(card,"ru",shuffle=lambda choices,k: list(reversed(choices)))
assert len(shown["choices"])==4
assert shown["choices"]==list(reversed(card["options"]))
for private in ("answerIndex","correct_index","originalChoices","translationChoices",
                "translations","explanations","source","correct","answer"):
    assert private not in shown, private

# Only post-grade does the order/translation mapping become possible.
scored=culture_adapter.after_answer(card,"ru",card["options"][1],False,True)
assert scored["originalChoices"]==list(card["options"])
assert len(scored["translationChoices"])==4
assert scored["assisted"] and not scored["independentCorrect"]
mapping=dict(zip(scored["originalChoices"],scored["translationChoices"]))
assert all(mapping[o] for o in shown["choices"])

print("PASS CULT-04: one Culture view, shared quiz flow, assisted state, gated exam, post-answer translations")
