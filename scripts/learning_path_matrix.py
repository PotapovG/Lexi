#!/usr/bin/env python3
"""Reproduce the guided-course matrix from the current authored catalog.

Read-only: no learner database, network, answer submission or future UI preview.
Default matrix uses a synthetic fixed account, Russian content and audio disabled.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import board_course as board
import learning_locales
import server


def response_type(question):
    if question["type"]=="life":return "typed scene"
    if question.get("typedAnswer"):return "typed Greek"
    if question["kind"]=="accent":return "letter index"
    if question["kind"]=="order":return "token order"
    if question["kind"]=="dialogue":return "dialogue gap"
    return "choice"


def matrix(listening=False):
    result=[]
    for chapter in range(1,board.MAX_CHAPTER+1):
        for slot,expected_family in enumerate(board.FAMILIES):
            state=copy.deepcopy(board.DEFAULT)
            state.update(chapterLimit=20,position=(chapter-1)*8+slot)
            lesson=board._build_lesson(state,"learning-path-matrix","ru",
                server.PRACTICE_ALL+server.LISTEN_CARDS,server.vocab.VOCAB,
                server.format_question,server._grammar_guard.milestone,
                listening,lambda text:None)
            questions=lesson["items"]
            assert questions and all(1<=q["chapter"]<=chapter for q in questions)
            assert len(questions)<=board.TARGETS[slot]
            scenario=[q for q in questions if q.get("scenarioId") and not q.get("review")]
            if scenario:
                assert [q["scenarioStep"] for q in scenario]==[1,2,3,4,5]
                assert len({q["scenarioId"] for q in scenario})==1
            groups={}
            for q in questions:
                if q["kind"]=="dialogue":
                    groups.setdefault(q["dialogueGroup"],[]).append(q)
            for group in groups.values():
                assert [q["activeGap"] for q in group]==list(range(group[0]["gapCount"]))
            result.append(dict(chapter=chapter,slot=slot+1,plannedFamily=expected_family,
                family=lesson["family"],title=lesson["name"],goal=lesson["goal"],
                goalFamily=board._goal_key(lesson["family"],chapter).removeprefix("goal_"),
                target=board.TARGETS[slot],responses=len(questions),
                cards=len({q["cardIndex"] for q in questions}),
                responseTypes=sorted({response_type(q) for q in questions}),
                selected=[dict(id=q["id"],direction=q.get("direction"),
                    type=response_type(q),review=bool(q.get("review")),
                    cardIndex=q["cardIndex"]) for q in questions]))
    return result


INTRO="""# Existing-material learning path

This document describes guided lesson composition version 4. It maps the existing
authored catalog to a reproducible representative lesson in each chapter and
family. It does not certify correspondence to an exact commercial-book page or
independent linguistic review. IDs, canonical Greek text and historical grades
are unchanged.

## Learning and progress contract

Eight existing lesson slots remain in each chapter. A lesson draws only from
eligible chapter/readiness material. Short lessons are intentional when the
current catalog cannot fill a target. Audio-disabled listening slots become
phrase practice; other unavailable families use chapter practice with an honest
title. Early grammar slots now use eligible existing phonetics, sentence order
and complete authored scenarios.

A new ordinary dialogue contains every gap, in order. The lesson.at/count fields
count response slots; cardAt/cardCount count logical cards. The public question
names only activeGap and previous filledGaps; no future gap answer key is returned.
The allowRepeatChoices and authored acceptedByGap rules still govern valid choices.
Full-dialogue explanatory material appears only after the final slot.

A new ordinary five-step scenario is selected as a whole, in authored order.
An incomplete eligible block is excluded. Weak review may repeat an individual
self-contained scenario card.

Up to two eligible delayed-review responses are reserved before normal material.
They belong to the current actual family and chapter scope and occupy no more
than 20% of actual response slots. A correct assigned review clears its due debt;
an ordinary coincidental correct appearance does not. Every original incorrect
grade remains incorrect. Dialogue debt records the specific failed directions.
A sparse lesson may have no review slot when a single review would exceed 20%.

The totals payload covers guided lessons only, includes finalized graded responses
in an active lesson and counts completed lessons separately. The roundStats
payload covers completed lessons in the displayed chapter. Unverified Life
alternatives and skips grant no mastery. Guided backlog, Classic mistakes and
opt-in SRS remain separate queues; their overlapping quiz records must never be
summed as distinct attempts. Culture remains a separate learning space.

Greek Life list and scene support share one readiness rule: a recorded success
in that scene, or at least six correct eligible book responses in its current
catalog chapter. Stored legacy attempts.unit is not treated as the current
chapter. Unknown, archived, non-book and Culture evidence cannot remove support.
The payload identifies readinessReason; this is practice evidence, not a
certified proficiency level.

Active time is approximate server event time, capped at 120 seconds per event.
Paused intervals are excluded. The browser lifecycle should pause on leaving
the lesson and stop its audio; a lost final request cannot prove exact time.

## Compatibility and review

New lesson runs have a stable random runId; legacy started runs receive a
deterministic identity. Saved partially answered lessons retain their existing
items and grades. An unanswered older generated lesson may rebuild under version
4. Completion records preserve the run ID, content language and logical count.

The six course locales have explicit backend titles, goals, scene prompts,
translations and deterministic correction messages. Lesson content language is
fixed after creation; changing interface language does not rewrite graded work.
Independent linguistic/editorial review and six-locale browser acceptance remain
required. Structural tests do not certify translation quality.

## Regenerate the matrix

Run python3 -B scripts/learning_path_matrix.py in the documented disposable
Python test environment. The --json flag returns the same detailed rows as data.
The --listening flag uses existing enabled audio cards; no speech synthesis or
download is performed.

The committed matrix below uses synthetic account learning-path-matrix,
Russian content, audio disabled and an empty backlog. It is a deterministic
representative composition, not an exhaustive list of every eligible card or a
promise of identical card choices for all users. A different account or backlog
can change chosen IDs. Empty backlog means the displayed rows contain no assigned
reviews; the review rule above applies to every row.

In each row, **responses/cards/target** distinguishes assessed gaps from logical
cards and maximum target. **short** flags material volume for editorial attention.
All named IDs already exist. A suffix after / is the existing scoring direction.
Repeated dialogue IDs are intentional: each direction is assessed separately.

## Family goals

"""

def markdown(rows,listening=False):
    lines=[INTRO.rstrip(),"","| Family | Goal (Russian content) |","| --- | --- |"]
    for family in board.FAMILIES:
        lines.append("| "+family+" | "+learning_locales.text("ru","goal_"+family)+" |")
    lines.extend(["","## Generated composition","",
                  "Audio: "+("enabled" if listening else "disabled")+". No learner data or backlog.",
                  ""])
    for chapter in range(1,21):
        lines.extend(["### Chapter "+str(chapter),"",
            "| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |",
            "| --- | --- | --- | --- | --- |"])
        for row in (r for r in rows if r["chapter"]==chapter):
            volume=f'{row["responses"]} / {row["cards"]} / {row["target"]}'
            if row["responses"]<row["target"]:volume+=" · short"
            ids=", ".join(chr(96)+q["id"]+("/"+q["direction"] if q["direction"] else "")+chr(96)
                          for q in row["selected"])
            lines.append(f'| {row["slot"]} · {row["family"]} | {row["goalFamily"]} | {volume} | '
                         +", ".join(row["responseTypes"])+" | "+ids+" |")
        lines.append("")
    short=[r for r in rows if r["responses"]<r["target"]]
    lines.extend(["## Editorial volume flags","",
                  f'{len(short)} of {len(rows)} representative lessons are shorter than their maximum target.',
                  "The rows above identify the exact affected chapters and families. This is an",
                  "inventory of available scoped practice, not a request to fill gaps with future",
                  "vocabulary or artificial repetition.",""])
    return "\n".join(lines)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--json",action="store_true")
    parser.add_argument("--listening",action="store_true")
    args=parser.parse_args()
    rows=matrix(args.listening)
    print(json.dumps(rows,ensure_ascii=False,indent=2) if args.json else markdown(rows,args.listening))
