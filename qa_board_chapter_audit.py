#!/usr/bin/env python3
"""Read-only audit of the *real, independently authored* chapter catalogs.

No paid textbook contents are needed. This checks internal syllabus gating,
not an assertion that every word appears verbatim in the publisher's edition.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
import server
import board_course as board

cards=server.PRACTICE_ALL+server.LISTEN_CARDS
seen_counts=Counter()
for chapter in range(1,8):
    for family_index,family in enumerate(board.FAMILIES):
        s=dict(board.DEFAULT,position=(chapter-1)*8+family_index,chapterLimit=7,
               lessons=[],backlog={},active=None)
        lesson=board._build_lesson(s,"qa_user","ru",cards,server.vocab.VOCAB,
            server.format_question,server._grammar_guard.milestone,
            True,lambda gr:None)  # Force full audio-enabled path, even in CI without WAV assets
        assert lesson["items"],(chapter,family,"empty")
        assert all(1<=q["chapter"]<=chapter for q in lesson["items"]),(chapter,family,"future chapter")
        assert len(lesson["items"])<=board.TARGETS[family_index]
        assert all(q.get("family")==lesson["family"] for q in lesson["items"])
        assert sum(q.get("review",False) for q in lesson["items"])*5<=len(lesson["items"])
        primary={"Глаголы в действии":{"verb"},
                 "Грамматика":{"grammar","article"},
                 "Слушаем греческий":{"listening"},
                 "Разговоры":{"dialogue"},
                 "Часы и расписание":{"clock"},
                 "Реальная жизнь":{"life"},
                 "Практика фраз":{"phrase","sentence"},
                 "Повторение слов":{"word","number","lexicon"},
                 "Слова главы":{"word","number","lexicon"}}
        if lesson["name"] in primary:
            assert all(q["kind"] in primary[lesson["name"]] for q in lesson["items"]),(
                chapter,family,lesson["name"],[q["kind"] for q in lesson["items"]])
        base=board._book_base(chapter,cards,server._grammar_guard.milestone)
        for q in lesson["items"]:
            if q["kind"] not in ("word","number","phrase","sentence","listening"):
                continue
            scope={"word","number"} if q["kind"] in ("word","number") else (
                {"listening"} if q["kind"]=="listening" else {"phrase","sentence"})
            known={(c["ru"] if q["direction"]=="gr-ru" else c["gr"])
                   for c in base if c["kind"] in scope}
            if q["kind"]=="listening":
                known={c["ru"] for c in server.LISTEN_CARDS if c["chapter"]<=chapter}
            assert set(q["choices"])<=known,(
                chapter,family,q["id"],set(q["choices"])-known)
        seen_counts[(chapter,lesson["family"])]+=len(lesson["items"])
print("PASS real catalog: chapters 1–7 / all 8 board families; no future chapter, mislabeled type, or unseen textbook-path distractors")
print("Card counts:",dict(sorted(seen_counts.items())))
