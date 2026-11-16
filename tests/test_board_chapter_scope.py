#!/usr/bin/env python3
"""Regression tests for board chapter/skill scope (issue #51).

Run: python3 tests/test_board_chapter_scope.py
These fixtures are synthetic, not from the commercial textbook.
"""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import board_course as board


LANGS=("ru","en","zh","ar","es","pt")


def material():
    cards=[]
    words=[]
    for chapter in range(1,9):
        for i in range(18):
            suffix=f"{chapter}_{i}"
            card=dict(id=f"b{suffix}",chapter=chapter,kind="word",source="original",
                      gr=f"λέξη{suffix}",en=f"word{suffix}",
                      ru=f"слово{suffix}",zh=f"词{suffix}",ar=f"كلمة{suffix}",
                      es=f"palabra{suffix}",pt=f"palavra{suffix}")
            cards.append(card)
            words.append({k:card[k] for k in ("gr",)+LANGS} |
                         {"id":f"book_{suffix}","level":"A1"})
        for i in range(8):
            suffix=f"{chapter}_{i}"
            cards.append(dict(id=f"p{suffix}",chapter=chapter,kind="phrase",
                              source="original",gr=f"Καλημέρα {suffix}",
                              en=f"phrase{suffix}",ru=f"фраза{suffix}",
                              zh=f"短语{suffix}",ar=f"عبارة{suffix}",
                              es=f"frase{suffix}",pt=f"frase{suffix}"))
    # A valid-looking independent A1 lexeme from the future must not enter the board.
    words.append(dict(id="atlas_future",level="A1",gr="άγνωστο",
                      ru="неизвестно",en="unknown",zh="未知",ar="مجهول",
                      es="desconocido",pt="desconhecido"))
    return cards,words


def formatter(card,direction,lang):
    return dict(id=card["id"],kind=card["kind"],chapter=card["chapter"],
                direction=direction,lang=lang,prompt=card["gr"],choices=["FUTURE_BAD_DECOY"])


def state(position):
    s=copy.deepcopy(board.DEFAULT)
    s["position"]=position
    s["chapterLimit"]=7
    return s


class BoardChapterScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards,cls.words=material()

    def build(self,chapter,family,lang="ru",s=None,listening_on=False):
        s=s or state((chapter-1)*8+board.FAMILIES.index(family))
        return board._build_lesson(s,"student",lang,self.cards,self.words,
                                   formatter,lambda c:c.get("chapter",99),
                                   listening_on,lambda text:None)

    def test_all_chapters_and_families_do_not_leak_future_words(self):
        for chapter in range(1,8):
            for family in board.FAMILIES:
                for lang in ("ru","en"):
                    with self.subTest(chapter=chapter,family=family,lang=lang):
                        lesson=self.build(chapter,family,lang)
                        self.assertTrue(lesson["items"])
                        self.assertLessEqual(len(lesson["items"]),board.TARGETS[board.FAMILIES.index(family)])
                        self.assertTrue(all(q["chapter"]<=chapter for q in lesson["items"]))
                        self.assertTrue(all(q.get("family")==lesson["family"] for q in lesson["items"]))
                        self.assertTrue(all(q.get("prompt")!="άγνωστο" for q in lesson["items"]))
                        self.assertLessEqual(sum(q.get("review",False) for q in lesson["items"])*5,len(lesson["items"]))
                        allowed=set()
                        for c in self.cards:
                            if c["chapter"]<=chapter:
                                allowed.add(c["gr"]);allowed.add(c[lang])
                        for q in lesson["items"]:
                            if q["type"]=="quiz":
                                self.assertNotIn("FUTURE_BAD_DECOY",q["choices"])
                                self.assertTrue(set(q["choices"])<=allowed)
                            elif q["type"]=="lexicon":
                                self.assertNotIn("неизвестно",q["choices"])
                                self.assertNotIn("unknown",q["choices"])
                                self.assertTrue(set(q["choices"])<=allowed)

    def test_unrelated_family_uses_honest_fallback_name(self):
        lesson=self.build(7,"dialogue")
        self.assertEqual(lesson["name"],"Практика главы")
        self.assertEqual(lesson["family"],"book")
        self.assertTrue(all(q["kind"] in ("word","number","phrase","sentence") for q in lesson["items"]))
        lesson=self.build(2,"listening",listening_on=False)
        self.assertEqual(lesson["name"],"Практика фраз")
        self.assertTrue(all(q["kind"] in ("phrase","sentence") for q in lesson["items"]))

    def test_audio_enabled_uses_listen_direction_and_scoped_options(self):
        import random
        self.assertEqual(board._direction({"kind":"listening"},random.Random(1)),"listen")
        listening=[]
        for i in range(10):
            source=self.cards[i]
            listening.append(dict(source,id="listen_"+source["id"],
                                  kind="listening",chapter=1))
        data=self.cards+listening
        s=state(board.FAMILIES.index("listening"))
        out=board._build_lesson(s,"student","ru",data,self.words,formatter,
                                lambda card:card["chapter"],True,lambda text:None)
        self.assertTrue(out["items"])
        self.assertEqual(out["name"],"Слушаем греческий")
        self.assertTrue(all(q["direction"]=="listen" for q in out["items"]))
        valid={q["ru"] for q in listening}
        self.assertTrue(all(set(q["choices"])<=valid for q in out["items"]))

    def test_current_node_previews_truthful_fallback(self):
        s=state((7-1)*8+board.FAMILIES.index("dialogue"))
        view=board._view(s,0,"ru")
        materials=(self.cards,self.words,formatter,
                   lambda c:c.get("chapter",99),False,lambda text:None)
        view=board._retitle_current(view,"ru",materials)
        current=next(n for n in view["nodes"] if n["state"]=="current")
        self.assertEqual(current["name"],"Практика главы")
        self.assertEqual(current["family"],"book")

    def test_current_chapter_first(self):
        lesson=self.build(4,"book")
        self.assertTrue(all(q["chapter"]==4 for q in lesson["items"]))
        chapter_words={c["gr"] for c in self.cards if c["chapter"]==4 and c["kind"]=="word"}
        words=self.build(4,"lexicon")
        self.assertTrue(all(q["prompt"] in chapter_words for q in words["items"]))

    def test_no_independent_atlas_in_backlog(self):
        s=state(board.FAMILIES.index("lexicon"))
        s["backlog"]={"lexicon:atlas_future":dict(id="atlas_future",kind="lexicon",
            chapter=1,family="lexicon",due=True,errors=9,lastWrong="2026-11-01")}
        lesson=self.build(1,"lexicon",s=s)
        self.assertTrue(all(q["id"]!="atlas_future" for q in lesson["items"]))
        self.assertIn("lexicon:atlas_future",s["backlog"])  # history retained

    def test_six_locales_and_existing_active_session(self):
        for lang in LANGS:
            lesson=self.build(3,"book",lang=lang)
            allowed={c[lang] for c in self.cards if c["chapter"]<=3}
            allowed|={c["gr"] for c in self.cards if c["chapter"]<=3}
            for q in lesson["items"]:
                self.assertTrue(set(q["choices"])<=allowed)
        s=state(0)
        s["active"]=dict(self.build(1,"book"),at=0)
        self.assertEqual(board._view(s,0,"ru")["lesson"]["count"],len(s["active"]["items"]))
        self.assertEqual(board._view(s,0,"ru")["lesson"]["question"],s["active"]["items"][0])

    def test_unanswered_legacy_lesson_refreshes_without_erasing_progress(self):
        old=state(0)
        old["active"]=dict(self.build(1,"book"),at=0)
        old["active"].pop("generatorVersion",None)
        old["backlog"]={"old":dict(due=True,errors=1)}
        with patch.object(board.tracks,"_load",return_value=(old,5)):
            updated,revision,migrated=board._load(None,"student")
        self.assertEqual(revision,5)
        self.assertTrue(migrated)
        self.assertIsNone(updated["active"])
        self.assertIn("old",updated["backlog"])
        partially_answered=state(0)
        partially_answered["active"]=dict(self.build(1,"book"),at=2)
        partially_answered["active"].pop("generatorVersion",None)
        with patch.object(board.tracks,"_load",return_value=(partially_answered,6)):
            preserved,revision,migrated=board._load(None,"student")
        self.assertFalse(migrated)
        self.assertEqual(preserved["active"]["at"],2)

    def test_sparse_chapter_remains_short_and_on_topic(self):
        cards=[c for c in self.cards if c["chapter"]==1 and c["kind"]=="word"][:2]
        out=board._build_lesson(state(0),"s","ru",cards,[],
                                formatter,lambda c:c["chapter"],False,lambda text:None)
        self.assertEqual(len(out["items"]),2)
        self.assertTrue(all(q["chapter"]==1 for q in out["items"]))


if __name__=="__main__":
    unittest.main()
