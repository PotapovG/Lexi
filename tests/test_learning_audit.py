#!/usr/bin/env python3
"""Learning audit regressions using disposable synthetic accounts and real authored cards.

Run: python3 -B tests/test_learning_audit.py
No production learner records, external services or commercial textbook fixtures.
"""
from __future__ import annotations

import copy
import datetime as dt
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import server
import board_course as board
import greek_life as life
import greek_variants
import learning_engine as engine
import learning_locales as locales
import life_answer_check as checker
import study_tracks as tracks


LANGS=("ru","en","zh","ar","es","pt")
CARDS=server.PRACTICE_ALL+server.LISTEN_CARDS
MATERIALS=(CARDS,server.vocab.VOCAB,server.format_question,
           server._grammar_guard.milestone,server.LISTENING_ENABLED,lambda text:None)


def state(chapter=1,family="book"):
    value=copy.deepcopy(board.DEFAULT)
    value.update(position=(chapter-1)*8+board.FAMILIES.index(family),chapterLimit=20)
    return value


def build(value,uid="learner",lang="ru",cards=None):
    materials=MATERIALS if cards is None else (cards,)+MATERIALS[1:]
    return board._build_lesson(value,uid,lang,*materials)


def answer_for(q):
    if q["type"]=="life":return life.BY_ID[q["id"]]["accepted"][0]
    if q["type"]=="lexicon":return server.vocab.VOCAB_BY_ID[q["id"]][q["lang"]]
    card=server.book_or_audio_card(q["id"])
    if q["kind"]=="accent":return str(card["accent_index"])
    return server.shape(card,q["direction"],q["lang"])[1]


class LearningAudit(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.old_db=server.DB
        self.old_secret=server.auth.SECRET_FILE
        server.DB=str(Path(self.temp.name)/"learning.sqlite3")
        server.auth.SECRET_FILE=Path(self.temp.name)/"synthetic-pepper"
        server.init_db()

    def tearDown(self):
        server.DB=self.old_db
        server.auth.SECRET_FILE=self.old_secret
        self.temp.cleanup()

    def get(self,uid="learner",lang="ru"):
        with server.conn() as db:return board.board_get(db,uid,lang)

    def seed(self,value,uid="learner"):
        with server.conn() as db:tracks._save(db,uid,"board","shared",value,0)
        return self.get(uid)

    def submit(self,view,selected,uid="learner",lang="ru"):
        lesson=view["lesson"];q=lesson["question"]
        with server.conn() as db:
            return board.board_action(db,uid,lang,dict(action="answer",
                revision=view["revision"],lessonIndex=lesson["index"],
                questionId=q["id"],selected=selected),server.mark,MATERIALS)

    def insert_attempts(self,uid,cid,kind,count=6,unit=-100):
        with server.conn() as db:
            db.executemany("""INSERT INTO attempts
                (user_id,card_key,kind,unit,correct,created_at) VALUES(?,?,?,?,?,?)""",
                [(uid,cid+":gr-ru",kind,unit,1,"2026-11-01T10:00:00+00:00")]*count)

    def assert_readiness(self,uid,sid,expected):
        with server.conn() as db:
            listing=life.current_settings(db,uid,"ru")
            opened=life.scene_get(db,uid,"ru",sid)
        item=next(x for x in listing["available"] if x["id"]==sid)
        self.assertEqual(item["difficulty"],expected)
        self.assertEqual(opened["difficulty"],expected)
        self.assertEqual(item["readinessReason"],opened["readinessReason"])
        self.assertEqual(opened["hint"] is not None,expected=="guided")
        return listing

    def test_new_account_state_is_independent(self):
        with server.conn() as db:
            first,_,_=board._load(db,"first")
            first["lessons"].append({"index":0})
            first["backlog"]["private-card"]={"due":True}
            first["roundSeen"].append(1)
            tracks._save(db,"first","board","shared",first,0)
        second=self.get("second")
        self.assertEqual(second["totals"]["lessons"],0)
        self.assertEqual(second["backlog"]["due"],0)
        self.assertEqual(second["position"],0)
        with server.conn() as db:
            second_state,_,_=board._load(db,"second")
        self.assertEqual(second_state["roundSeen"],[])
        self.assertEqual(board.DEFAULT["lessons"],[])
        self.assertEqual(board.DEFAULT["backlog"],{})
        self.assertEqual(board.DEFAULT["roundSeen"],[])

    def test_full_lesson_reserves_due_slots_and_preserves_grade_history(self):
        value=state()
        eligible=[c for c in board._book_base(1,CARDS,MATERIALS[3])
                  if c["kind"]=="word"][:2]
        self.assertEqual(len(eligible),2)
        for c in eligible:
            value["backlog"]["word:"+c["id"]]=dict(id=c["id"],kind="word",
                chapter=1,family="book",due=True,errors=3,lastWrong="2026-11-01")
        lesson=build(value)
        reviews=[q for q in lesson["items"] if q.get("review")]
        self.assertEqual(len(lesson["items"]),board.TARGETS[0])
        self.assertEqual(len(reviews),2)
        self.assertLessEqual(len(reviews)*5,len(lesson["items"]))
        self.assertEqual({q["id"] for q in reviews},{c["id"] for c in eligible})
        for q in reviews:
            self.assertEqual(sum(x["id"]==q["id"] for x in lesson["items"]),1)
        first=reviews[0];key=first["kind"]+":"+first["id"]
        board._review_success(value,dict(first,review=False))
        self.assertTrue(value["backlog"][key]["due"])
        board._review_success(value,first)
        self.assertFalse(value["backlog"][key]["due"])
        self.assertEqual(value["backlog"][key]["errors"],3)
        board._record_error(value,first,1)
        self.assertTrue(value["backlog"][key]["due"])
        self.assertEqual(value["backlog"][key]["errors"],4)

    def test_dialogue_all_gaps_score_once_and_resume_without_future_keys(self):
        card=server.BY_ID["dlg001"]
        value=state(1,"dialogue")
        value["active"]=build(value,cards=[card])
        view=self.seed(value)
        first=view["lesson"]["question"]
        self.assertEqual((view["lesson"]["count"],view["lesson"]["cardCount"]),(2,1))
        self.assertEqual(first["activeGap"],0)
        self.assertEqual(first["gapCount"],2)
        self.assertNotIn("dialogueGaps",first)
        wrong=next(x for x in first["choices"] if x!=card["gaps"][0])
        result=self.submit(view,wrong)
        self.assertFalse(result["feedback"]["correct"])
        self.assertNotIn("dialogueFullTemplate",result["feedback"])
        self.assertNotIn("dialogueFullGlosses",result["feedback"])
        current=result["lesson"]["question"]
        self.assertEqual(current["id"],"dlg001")
        self.assertEqual(current["direction"],"gap1")
        self.assertEqual(current["filledGaps"],{"0":card["gaps"][0]})
        self.assertNotIn(card["gaps"][0],current["choices"])
        self.assertEqual(result["lesson"]["at"],1)
        self.assertEqual(result["lesson"]["cardAt"],0)
        self.assertEqual(self.get()["lesson"],result["lesson"])
        with self.assertRaisesRegex(ValueError,"stale_track"):
            self.submit(view,card["gaps"][0])
        finished=self.submit(result,card["gaps"][1])
        report=finished["feedback"]["lessonComplete"]
        self.assertEqual((report["attempts"],report["errors"],report["correct"]),(2,1,1))
        self.assertEqual(report["cardCount"],1)
        self.assertEqual(report["runId"],value["active"]["runId"])
        with server.conn() as db:
            rows=db.execute("SELECT card_key,attempts FROM progress WHERE user_id=? ORDER BY card_key",
                            ("learner",)).fetchall()
        self.assertEqual([(r["card_key"],r["attempts"]) for r in rows],
                         [("dlg001:gap0",1),("dlg001:gap1",1)])

    def test_repeatable_dialogue_preserves_accepted_alternatives(self):
        card=server.BY_ID["dlg033"]
        value=state(card["chapter"],"dialogue")
        value["active"]=build(value,cards=[card])
        view=self.seed(value)
        repeated=card["acceptedByGap"]["gap0"][1]
        result=self.submit(view,repeated)
        self.assertTrue(result["feedback"]["correct"])
        self.assertTrue(result["feedback"]["acceptedVariant"])
        self.assertEqual(result["lesson"]["question"]["filledGaps"],{"0":repeated})
        self.assertIn(repeated,result["lesson"]["question"]["choices"])
        finished=self.submit(result,repeated)
        self.assertTrue(finished["feedback"]["correct"])
        self.assertEqual(finished["feedback"]["lessonComplete"]["correct"],2)

    def test_dialogue_debt_tracks_exact_failed_slots(self):
        value=state(3,"dialogue")
        for direction in ("gap0","gap1"):
            q=dict(id="dlg033",kind="dialogue",family="dialogue",
                   direction=direction,prompt="authored scene")
            board._record_error(value,q,3)
        row=value["backlog"]["dialogue:dlg033"]
        self.assertEqual(row["dueDirections"],["gap0","gap1"])
        board._review_success(value,dict(q,review=True,direction="gap0"))
        self.assertTrue(row["due"])
        self.assertEqual(row["dueDirections"],["gap1"])
        board._review_success(value,dict(q,review=True,direction="gap1"))
        self.assertFalse(row["due"])
        self.assertEqual(row["errors"],2)

    def test_existing_scenarios_stay_complete_and_ordered(self):
        for chapter in range(1,8):
            with self.subTest(chapter=chapter):
                lesson=build(state(chapter,"grammar"),uid="scenario")
                linked=[(i,q) for i,q in enumerate(lesson["items"]) if q.get("scenarioId")]
                self.assertEqual(len(linked),5)
                self.assertEqual([q["scenarioStep"] for _,q in linked],[1,2,3,4,5])
                self.assertEqual(len({q["scenarioId"] for _,q in linked}),1)
                self.assertEqual([i for i,_ in linked],list(range(linked[0][0],linked[0][0]+5)))
                self.assertTrue(all(q["chapter"]<=chapter for _,q in linked))
                self.assertLessEqual(len(lesson["items"]),12)

    def test_partial_scenario_never_enters_ordinary_pool(self):
        eligible=board._candidates("grammar",1,CARDS,MATERIALS[3],False)
        scenario=next(c["scenarioId"] for c in eligible if c.get("group")=="review_scenario")
        partial=[c for c in eligible if c.get("scenarioId")==scenario][:4]
        others=[c for c in eligible if c.get("group")!="review_scenario"][:10]
        lesson=build(state(1,"grammar"),cards=partial+others)
        self.assertTrue(lesson["items"])
        self.assertTrue(all(not q.get("scenarioId") for q in lesson["items"]))

    def test_new_typed_and_phonetic_controls_use_authoritative_scorer(self):
        eligible=board._candidates("grammar",1,CARDS,MATERIALS[3],False)
        selected={}
        for card in eligible:
            if card["kind"] in ("accent","syllable","order"):selected.setdefault(card["kind"],card)
            if card.get("typedAnswer") and card.get("group")!="review_scenario":selected.setdefault("typed",card)
        self.assertEqual(set(selected),{"accent","syllable","order","typed"})
        for n,(kind,card) in enumerate(selected.items()):
            with self.subTest(kind=kind):
                value=state(1,"grammar")
                value["active"]=build(value,uid="control"+str(n),cards=[card])
                view=self.seed(value,uid="control"+str(n))
                q=view["lesson"]["question"]
                if kind=="typed":
                    self.assertTrue(q["typedAnswer"])
                    self.assertEqual(q["choices"],[])
                result=self.submit(view,answer_for(q),uid="control"+str(n))
                self.assertTrue(result["feedback"]["correct"])

    def test_early_fallback_goals_describe_actual_material(self):
        for chapter,family in ((1,"verb"),(1,"clock"),(5,"clock")):
            value=state(chapter,family)
            value["active"]=build(value)
            expected=locales.text("ru","goal_book")
            self.assertEqual(value["active"]["goal"],expected)
            self.assertEqual(board._view(value,0,"ru")["lesson"]["goal"],expected)
        value=state(1,"listening")
        preview=board._retitle_current(board._view(value,0,"ru"),"ru",
                                      MATERIALS[:4]+(False,MATERIALS[5]))
        node=next(n for n in preview["nodes"] if n["state"]=="current")
        self.assertEqual(node["goal"],locales.text("ru","goal_book"))

    def test_known_variants_work_without_changing_canonical_text(self):
        before=copy.deepcopy(life.SCENES)
        daily=life.BY_ID["daily"]["accepted"]
        for lang in LANGS:
            for accepted in daily:
                for form in greek_variants.accepted(accepted):
                    result=checker.evaluate(form,daily,lang)
                    self.assertTrue(result["correct"],(lang,form,result))
                    self.assertFalse(result["unverified"])
            self.assertFalse(checker.evaluate("Τρώω πρωινό οχτώ.",daily,lang)["correct"])
        self.assertEqual(life.SCENES,before)
        self.assertEqual(daily[0],"Τρώω πρωινό στις οκτώ.")

    def test_readiness_excludes_culture_supplemental_unknown_and_archived(self):
        supplemental=next(c for c in server.ALL if c.get("chapter",0)<=0)
        for uid,cid,kind in (("culture","cyq_001","culture"),
                             ("unknown","missing_card","word"),
                             ("supplemental",supplemental["id"],supplemental["kind"]),
                             ("archived","dlg024","dialogue")):
            self.insert_attempts(uid,cid,kind,count=12)
            listing=self.assert_readiness(uid,"meet","guided")
            self.assertEqual(listing["observations"],0)

    def test_readiness_normalizes_legacy_chapter_and_matches_list(self):
        c=next(c for c in server.ALL if c["kind"]=="word" and c["chapter"]==1
               and c.get("source")=="original")
        self.insert_attempts("legacy",c["id"],c["kind"],unit=-5)
        listing=self.assert_readiness("legacy","meet","independent")
        self.assertEqual(listing["observations"],6)
        self.assert_readiness("legacy","home_city","guided")
        with server.conn() as db:
            self.assertEqual(db.execute("SELECT MIN(unit) FROM attempts").fetchone()[0],-5)

    def test_scene_success_and_skip_do_not_fabricate_mastery(self):
        with server.conn() as db:
            q=life.scene_get(db,"speaker","ru","home_city")
            result=life.scene_answer(db,"speaker","ru",dict(id="home_city",
                revision=q["revision"],answer="Μένω Λευκωσία"))
        self.assertFalse(result["correct"])
        with server.conn() as db:
            life.skip_scene(db,"speaker","ru",dict(id="home_city",revision=result["revision"]))
        self.assert_readiness("speaker","home_city","guided")
        with server.conn() as db:
            q=life.scene_get(db,"speaker","ru","home_city")
            result=life.scene_answer(db,"speaker","ru",dict(id="home_city",
                revision=q["revision"],answer="Μένω στη Λευκωσία."))
        self.assertTrue(result["correct"])
        self.assert_readiness("speaker","home_city","independent")

    def test_six_locales_cover_names_prompts_diagnostics_and_feedback(self):
        for lang in LANGS:
            with self.subTest(lang=lang):
                value=state(1,"life")
                value["active"]=build(value,uid=lang,lang=lang)
                view=self.seed(value,uid=lang)
                q=view["lesson"]["question"]
                self.assertEqual(q["lang"],lang)
                self.assertEqual(q["prompt"],locales.scene_text(life.BY_ID["meet"],"prompt",lang))
                answer=life.BY_ID["meet"]["accepted"][0]
                result=self.submit(view,answer,uid=lang,lang=lang)
                feedback=result["feedback"]
                self.assertEqual(feedback["translationLang"],lang)
                self.assertEqual(feedback["closestAnswer"],answer)
                self.assertIn("alternatives",feedback)
                for scene in life.SCENES:
                    for field in ("name","prompt","translation"):
                        actual=locales.scene_text(scene,field,lang)
                        self.assertTrue(actual)
                        if lang not in ("ru","en"):
                            self.assertNotEqual(actual,locales.scene_text(scene,field,"en"))
                explanation=checker.evaluate("Μένω Λευκωσία",life.BY_ID["home_city"]["accepted"],lang)["explanation"]
                self.assertTrue(explanation)
                if lang!="en":
                    self.assertNotEqual(explanation,checker.evaluate("Μένω Λευκωσία",
                                        life.BY_ID["home_city"]["accepted"],"en")["explanation"])

    def test_active_totals_are_scoped_and_reads_do_not_duplicate_attempts(self):
        value=state();value["active"]=build(value)
        started=self.seed(value)
        view=self.submit(started,answer_for(started["lesson"]["question"]))
        self.assertEqual(view["totals"]["scope"],"guided_lessons")
        self.assertEqual(view["totals"]["answerUnit"],"graded_responses")
        self.assertEqual(view["totals"]["answers"],1)
        self.assertEqual(view["totals"]["lessons"],0)
        self.assertTrue(view["totals"]["includesActiveLesson"])
        self.assertEqual(view["roundStats"]["attempts"],0)
        self.assertFalse(view["roundStats"]["includesActiveLesson"])
        self.assertEqual(self.get()["totals"],view["totals"])
        self.assertEqual(self.get()["totals"],view["totals"])

    def test_legacy_run_identity_is_stable_and_outer_transaction_works(self):
        value=state();value["active"]=build(value)
        value["active"].pop("runId")
        value["active"]["at"]=1
        value["active"]["generatorVersion"]=3
        with server.conn() as db:tracks._save(db,"legacy-run","board","shared",value,0)
        with server.conn() as db:
            a,_,migrate=board._load(db,"legacy-run")
            b,_,_=board._load(db,"legacy-run")
            self.assertTrue(migrate)
            self.assertEqual(a["active"]["runId"],b["active"]["runId"])
            db.execute("BEGIN IMMEDIATE")
            view=board.board_get(db,"legacy-run","ru")
            self.assertEqual(view["lesson"]["at"],1)
            result=board.board_action(db,"legacy-run","ru",dict(action="pause",
                revision=view["revision"]),server.mark,MATERIALS)
            self.assertTrue(result["lesson"]["paused"])

    def test_paused_time_is_excluded_and_active_time_is_bounded(self):
        active=build(state())
        active.update(lastAt="2026-11-01T00:00:00+00:00",activeSeconds=0,paused=True)
        with patch.object(board,"_stamp",return_value="2026-11-01T12:00:00+00:00"):
            board._update_time(active)
        self.assertEqual(active["activeSeconds"],0)
        active["paused"]=False
        with patch.object(board,"_stamp",return_value="2026-11-02T12:00:00+00:00"):
            board._update_time(active)
        self.assertEqual(active["activeSeconds"],120)

    def test_srs_scope_filters_before_limit_and_streams_beyond_unavailable_rows(self):
        with server.conn() as db:
            rows=[("review",f"cyq_shadow{i:04}:culture","2020-01-01","2020-01-01") for i in range(700)]
            rows += [("review",f"missing{i:04}:gr-ru","2020-01-02","2020-01-01") for i in range(600)]
            rows += [("review","w001:gr-ru","2020-01-03","2020-01-01")]
            db.executemany("INSERT INTO srs_schedule(user_id,card_key,due_at,updated_at) VALUES(?,?,?,?)",rows)
            book=list(engine.iter_due_entries(db,"review",scope="book",batch_size=11))
            culture=list(engine.iter_due_entries(db,"review",scope="culture",batch_size=17))
            self.assertEqual(len(book),601)
            self.assertEqual(len(culture),700)
            usable=[r["card_key"] for r in book if r["card_key"].split(":")[0] in server.BY_ID]
            self.assertEqual(usable,["w001:gr-ru"])
            first=engine.due_entries(db,"review",scope="book",limit=2)
            self.assertTrue(all(not r["card_key"].startswith("cyq_") for r in first))
            self.assertEqual(engine.status(db,"review",scope="book")["due"],601)

    def test_srs_locale_keeps_historical_key_semantics(self):
        for lang in LANGS:
            for kind in engine.NEUTRAL_KEY_KINDS-{"culture"}:
                self.assertEqual(engine.review_language({"id":"x","kind":kind},"x:direction",lang),lang)
                self.assertIsNone(engine.review_language({"id":"x","kind":kind},"x:direction:en",lang))
        word={"id":"w","kind":"word"}
        self.assertEqual(engine.review_language(word,"w:gr-ru","zh"),"ru")
        self.assertEqual(engine.review_language(word,"w:gr-ru:es","zh"),"es")
        self.assertIsNone(engine.review_language(word,"w:gr-ru:unknown","ru"))
        culture={"id":"cyq_a","kind":"culture"}
        self.assertEqual(engine.review_language(culture,"cyq_a:culture","en"),"en")
        self.assertIsNone(engine.review_language(culture,"cyq_a:culture","zh"))


if __name__=="__main__":
    unittest.main()
