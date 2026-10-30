"""Greek Life semantic/text normalization and non-misleading post-answer feedback."""
import random
import tempfile
import unicodedata
from pathlib import Path

import life_answer_check as check
import greek_life as life
import server

assert life.validate()==11
home=life.BY_ID["home_city"]["accepted"]
for form in home:
    for lang in ("ru","en","zh","ar","es","pt"):
        evaluated=check.evaluate(form,home,lang)
        assert evaluated["correct"] and not evaluated["unverified"],(form,lang,evaluated)
        assert evaluated["explanation"] is None and evaluated["closest"]==form
        unaccented="".join(c for c in unicodedata.normalize("NFD",form)
                            if not unicodedata.combining(c))
        evaluated=check.evaluate(unaccented,home,lang)
        assert evaluated["correct"] and evaluated["orthographyNote"],(form,lang,evaluated)
        assert evaluated["closest"]==form

cases=(
    ("Μένω στην Λεθκώσια","опечатка",False),
    ("Μένω στη Λεθκώσια","опечатка",False),
    ("Μένω στην Λευκοσία","опечатка",False),
    ("Μένω Λευκωσία","нужна форма",False),
    ("Μένω στο Λευκωσία","нужна форма",False),
    ("Μένω στη Λευκωσία",None,True),
    ("Μένω στην Λευκωσία",None,True),
    ("Μενω στην Λευκωσια",None,True),
)
for actual,hint,correct in cases:
    scored=check.evaluate(actual,home,"ru")
    assert scored["correct"]==correct,(actual,scored)
    if hint:
        assert hint in scored["explanation"].lower(),(actual,scored)
        if "Лεθ" in actual or "Лεв" in actual:
            assert "Не хватает формы" not in scored["explanation"]
    assert scored["closest"] in home
    if not correct:
        assert scored["closest"].endswith("Λευκωσία.")

typo=check.evaluate("Μένω στην Λεθκώσια",home,"ru")
assert typo["closest"]=="Μένω στην Λευκωσία."
assert "Λεθκώσια" in typo["explanation"] and "Λευκωσία" in typo["explanation"]
assert "αρтикλ" not in typo["explanation"].casefold()
assert not typo["unverified"]

missing=check.evaluate("Μου αρέσει περπατάω",life.BY_ID["plans"]["accepted"],"ru")
assert not missing["correct"] and not missing["unverified"]
assert "να" in missing["explanation"]
unknown=check.evaluate("Ονομάζομαι Μαρία",life.BY_ID["meet"]["accepted"],"ru")
assert not unknown["correct"] and unknown["unverified"]
assert "не буду считать" in unknown["explanation"]

for scene in life.SCENES:
    for correct_text in scene["accepted"]:
        for lang in ("ru","en","zh","ar","es","pt"):
            evaluated=check.evaluate(correct_text,scene["accepted"],lang)
            assert evaluated["correct"] and not evaluated["unverified"],(scene["id"],lang,evaluated)
        # Removing tonos is acceptable but is noted to avoid teaching the
        # reader that stress marks are optional in written Greek.
        no_accent="".join(x for x in unicodedata.normalize("NFD",correct_text)
                          if not unicodedata.combining(x))
        assert check.evaluate(no_accent,scene["accepted"],"ru")["correct"],scene["id"]

with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/"test.sqlite3")
    server.init_db()
    def answer(txt,uid="user"):
        with server.conn() as db:
            q=life.scene_get(db,uid,"ru","home_city")
            assert not any(k in q for k in ("answer","closestAnswer","alternatives"))
            return life.scene_answer(db,uid,"ru",dict(
                id="home_city",revision=q["revision"],answer=txt))
    response=answer("Μένω στην Λεθκώσια")
    assert not response["correct"] and not response["unverified"]
    assert response["closestAnswer"]=="Μένω στην Λευκωσία."
    assert "опечатка" in response["explanation"].lower()
    assert response["translation"]=="Я живу в Никосии."
    response=answer("Μένω στην Λευκωσία")
    assert response["correct"] and response["explanation"] is None
    assert response["closestAnswer"]=="Μένω στην Λευκωσία."
    response=answer("Μενω στη Λευκωσια")
    assert response["correct"] and response["orthographyNote"]
    with server.conn() as db:
        row=db.execute("SELECT data FROM learning_tracks WHERE name='life' AND user_id='user'").fetchone()
        import json
        data=json.loads(row["data"])["results"]["home_city"]
        assert data["errors"]==1 and data["correct"]==2
        assert db.execute("pragma quick_check").fetchone()[0]=="ok"

js=Path(__file__).with_name("life.js").read_text()
assert "const shown=result.closestAnswer||result.answer" in js
assert "Другие допустимые формулировки" in js
assert "life-orthography-note" in js
assert "life-more-answers" in js
print("PASS screenshot regression: valid στην, typo Λεθκώσια, nearest accepted wording")
print("PASS all scenes x six locales, missing preposition/particle, accent hints, no false penalties")
print("PASS after-score-only feedback, translation and optional labelled alternatives")
