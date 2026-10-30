"""Regression: contextless single/unmarried overlaps are not false errors.

Both genders, Greek<->Russian, English translations, three quiz engines,
in-progress answer acceptance, negative controls and multiple-choice quality.
"""
import tempfile
from pathlib import Path
import server
import vocab_lessons as vocab
import study_tracks as tracks
import lexical_overlap as overlap
import accepted_glosses as glosses
import distractor_quality as distractors

PAIRS=[
    ("ελεύθερος","ανύπαντρος"),
    ("ελεύθερη","ανύπαντρη"),
]
with tempfile.TemporaryDirectory() as directory:
    server.DB=str(Path(directory)/"test.sqlite3")
    server.init_db()
    for gr_a,gr_b in PAIRS:
        a=next(c for c in server.PRACTICE_ALL if c.get("gr")==gr_a and c["kind"]=="word")
        b=next(c for c in server.PRACTICE_ALL if c.get("gr")==gr_b and c["kind"]=="word")
        wa=next(c for c in vocab.VOCAB if c["gr"]==gr_a)
        wb=next(c for c in vocab.VOCAB if c["gr"]==gr_b)
        assert overlap.overlaps(a,b) and overlap.overlaps(b,a)
        assert overlap.overlaps(wa,wb)
        assert not overlap.overlaps(a,{"gr":"διαζευγμένος","kind":"word"})
        assert not overlap.overlaps(a,{"gr":"ανύπαντρος" if gr_a=="ελεύθερη" else "ανύπαντρη","kind":"word"})
        for lang in ("ru","en","zh","ar","es","pt"):
            for src,other in ((a,b),(b,a)):
                translated=src[lang]
                alternate=other[lang]
                assert alternate in glosses.accepted(src,"gr-ru",lang,translated)
                assert other["gr"] in glosses.accepted(src,"ru-gr",lang,src["gr"])
                assert distractors.same_sense_or_variant(src,other)
                # Neither card is present as a wrong distractor.
                choices,_=server.generate_options(src,"gr-ru",translated,lang)
                assert alternate not in choices,(src["gr"],lang,choices)
                choices,_=server.generate_options(src,"ru-gr",src["gr"],lang)
                assert other["gr"] not in choices,(src["gr"],lang,choices)
                assert len(choices)==len(set(choices))==8
                # An already displayed answer before the fix still scores.
                for direction,selected in (("gr-ru",alternate),("ru-gr",other["gr"])):
                    outcome=server.mark("test-user",{
                        "id":src["id"],"direction":direction,"selected":selected,"lang":lang})
                    assert outcome["correct"],(src["gr"],direction,lang)
                    assert selected in outcome["acceptedAnswers"]
                # Standalone A1/A2 course accepts the alternative but doesn't
                # present it as wrong in new generated lessons.
                direction="gr-target"
                with server.conn() as db:
                    result=vocab.answer(db,"vocab-user",{
                        "id":wa["id"] if src["gr"]==gr_a else wb["id"],
                        "direction":direction,"selected":alternate,"lang":lang})
                    assert result["correct"],(src["gr"],lang)
                    assert alternate in result["acceptedAnswers"]
                    result=vocab.answer(db,"vocab-user",{
                        "id":wa["id"] if src["gr"]==gr_a else wb["id"],
                        "direction":"target-gr","selected":other["gr"],"lang":lang})
                    assert result["correct"]
        # Anki: candidate no longer offered, but an already served ambiguous
        # old option is still accepted as correct after a deployment.
        wa=tracks.BY_ID[wa["id"]]
        other=wb
        assert other["ru"] not in tracks._options(wa,"ru",27)
        import json
        from sqlite3 import Row
        with server.conn() as db:
            s={"phase":"quiz","batch":0,"at":0,"mastered":[],"known":[],
               "queue":[wa["id"]],"nextPhase":None,"reviewRound":0,"misses":0}
            db.execute("""INSERT OR REPLACE INTO learning_tracks(user_id,name,lang,revision,data)
                          VALUES (?,?,?,?,?)""",("anki-user","anki","ru",0,json.dumps(s)))
        with server.conn() as db:
            result=tracks.anki_action(db,"anki-user","ru",{
                "revision":0,"action":"answer","cardId":wa["id"],"selected":other["ru"]})
            assert result["feedback"]["correct"] is True
            assert result["misses"]==0
    for other in ("παντρεμένος","διαζευγμένος","ελεύθερη"):
        assert not overlap.overlaps({"kind":"word","gr":"ανύπαντρος"},{"kind":"word","gr":other})
    assert not overlap.overlaps({"kind":"phrase","gr":"ελεύθερος"},{"kind":"phrase","gr":"ανύπαντρος"})
    print("PASS masculine/feminine semantic overlap; six UI languages; 8-choice distractors; legacy answer recovery")
    print("PASS textbook, vocab A1/A2 and Anki grading, no unrelated marital/gender conflation")
