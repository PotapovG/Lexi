# Existing-material learning path

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

| Family | Goal (Russian content) |
| --- | --- |
| book | Понимать слова и фразы изученной главы. |
| lexicon | Вспомнить значения уже изученных слов. |
| verb | Практиковать доступные формы глаголов. |
| grammar | Применять знакомые языковые формы в контексте. |
| listening | Распознавать знакомые слова и фразы на слух. |
| dialogue | Выбирать подходящие реплики в знакомых разговорах. |
| clock | Читать время и понимать знакомые расписания. |
| life | Составлять короткие ответы для знакомых ситуаций. |

## Generated composition

Audio: disabled. No learner data or backlog.

### Chapter 1

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `w035/gr-ru`, `w125/ru-gr`, `w120/ru-gr`, `patk01_002/ru-gr`, `w031/ru-gr`, `w010/ru-gr`, `w015/gr-ru`, `w027/ru-gr`, `w124/ru-gr`, `p004/ru-gr`, `w020/ru-gr`, `w012/ru-gr`, `w003/ru-gr`, `w006/ru-gr` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_2d323da0133ae9/gr-ru`, `book_3f4b6c3757ef11/gr-ru`, `book_2c09822eb18b17/gr-ru`, `book_bf9fcd6fddc9bd/gr-ru`, `book_da46510fcb3f27/gr-ru`, `book_3e367ab30b9ed1/gr-ru`, `book_0c5498eeefaa04/gr-ru`, `book_46fd77da5405fc/gr-ru`, `book_04cca81f677ffa/gr-ru`, `book_9d6e3528137f04/gr-ru`, `book_89e89661d4a820/gr-ru`, `book_98e6975b335b43/gr-ru`, `book_8af023c3a00cd1/gr-ru`, `book_96c0ba34b93dc5/gr-ru` |
| 3 · verb | book | 12 / 12 / 12 | choice | `w120/ru-gr`, `w175/ru-gr`, `w001/ru-gr`, `w021/gr-ru`, `w009/gr-ru`, `w036/gr-ru`, `w013/gr-ru`, `w020/ru-gr`, `w002/ru-gr`, `w118/gr-ru`, `w008/ru-gr`, `w014/gr-ru` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, typed Greek | `g2261021_499/grammar_fill`, `g2261021_500/grammar_fill`, `g2261021_501/grammar_fill`, `g2261021_502/grammar_fill`, `g2261021_503/grammar_fill`, `stress_w016/accent`, `g2261021_424/grammar_fill`, `stress_w028/accent`, `stress_w174/accent`, `stress_w124/accent`, `stress_w030/accent`, `stress_w121/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `p001/gr-ru`, `patk01_006/gr-ru`, `patk01_003/ru-gr`, `p003/ru-gr`, `patk01_005/gr-ru`, `p002/gr-ru`, `p005/ru-gr`, `patk01_004/ru-gr`, `p007/ru-gr`, `patk01_001/ru-gr`, `patk01_002/gr-ru`, `p006/gr-ru` |
| 6 · dialogue | dialogue | 11 / 6 / 12 · short | dialogue gap | `dlg025/gap0`, `dlg102/gap0`, `dlg102/gap1`, `dlg001/gap0`, `dlg001/gap1`, `dlg101/gap0`, `dlg101/gap1`, `dlg021/gap0`, `dlg021/gap1`, `dlg103/gap0`, `dlg103/gap1` |
| 7 · clock | book | 12 / 12 / 12 | choice | `p006/gr-ru`, `p007/ru-gr`, `p003/gr-ru`, `patk01_003/ru-gr`, `p002/gr-ru`, `p004/ru-gr`, `p001/gr-ru`, `patk01_001/ru-gr`, `patk01_005/ru-gr`, `patk01_006/ru-gr`, `patk01_002/ru-gr`, `p005/ru-gr` |
| 8 · life | life | 1 / 1 / 10 · short | typed scene | `meet` |

### Chapter 2

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `w055/ru-gr`, `w037/gr-ru`, `w071/ru-gr`, `p014/gr-ru`, `w190/ru-gr`, `w074/ru-gr`, `p008/ru-gr`, `w054/ru-gr`, `w178/ru-gr`, `w188/ru-gr`, `w179/gr-ru`, `w183/gr-ru`, `w065/gr-ru`, `p016/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_1d4073d37b6285/gr-ru`, `book_f19acafffd325b/gr-ru`, `book_965a456cefc710/gr-ru`, `book_102dc08f17c93e/gr-ru`, `book_1151f7f8216a18/gr-ru`, `book_c035ce36e63f11/gr-ru`, `book_74ea3fe5b47b3f/gr-ru`, `book_d151162e566d1a/gr-ru`, `book_41ccca16fafe26/gr-ru`, `book_192d8a9b09ed13/gr-ru`, `book_805327fa8d2554/gr-ru`, `book_8107d61772f240/gr-ru`, `book_d6ee834ed259b6/gr-ru`, `book_db4ad8dca534a6/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `p011/gr-ru`, `patk02_005/ru-gr`, `p019/gr-ru`, `p008/ru-gr`, `patk02_006/ru-gr`, `patk02_003/ru-gr`, `p017/ru-gr`, `p012/ru-gr`, `p020/gr-ru`, `p016/ru-gr`, `p018/ru-gr`, `p015/gr-ru` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, typed Greek | `g2261021_504/grammar_fill`, `g2261021_505/grammar_fill`, `g2261021_506/grammar_fill`, `g2261021_507/grammar_fill`, `g2261021_508/grammar_fill`, `stress_w193/accent`, `stress_w185/accent`, `article_008/fill`, `stress_w046/accent`, `g2261021_099/grammar_fill`, `g2261021_105/grammar_fill`, `stress_w052/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `p020/gr-ru`, `patk02_005/ru-gr`, `patk02_004/ru-gr`, `p013/gr-ru`, `patk02_006/gr-ru`, `p011/ru-gr`, `patk02_002/gr-ru`, `p008/ru-gr`, `p017/gr-ru`, `patk02_001/gr-ru`, `p010/ru-gr`, `p019/gr-ru` |
| 6 · dialogue | dialogue | 12 / 7 / 12 | dialogue gap | `dlg028/gap0`, `dlg028/gap1`, `dlg029/gap0`, `dlg024_v2/gap0`, `dlg024_v2/gap1`, `dlg107/gap0`, `dlg107/gap1`, `dlg002/gap0`, `dlg002/gap1`, `dlg105/gap0`, `dlg105/gap1`, `dlg026/gap0` |
| 7 · clock | book | 12 / 12 / 12 | choice | `p010/ru-gr`, `p015/gr-ru`, `p018/gr-ru`, `p017/ru-gr`, `p008/ru-gr`, `p014/ru-gr`, `patk02_002/ru-gr`, `patk02_001/ru-gr`, `p013/gr-ru`, `p009/ru-gr`, `p020/gr-ru`, `patk02_005/gr-ru` |
| 8 · life | life | 2 / 2 / 10 · short | typed scene | `home_city`, `meet` |

### Chapter 3

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `w114/ru-gr`, `s008/ru-gr`, `p021/ru-gr`, `s001/ru-gr`, `w112/gr-ru`, `p027/gr-ru`, `p025/ru-gr`, `s006/ru-gr`, `patk03_006/ru-gr`, `w111/ru-gr`, `w107/ru-gr`, `p029/ru-gr`, `w097/gr-ru`, `s014/ru-gr` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_0ed51ad66573ce/gr-ru`, `book_1ab689f0168e62/gr-ru`, `book_c40f649230c36f/gr-ru`, `book_0583faa933ff76/gr-ru`, `book_8c28beeecaf638/gr-ru`, `book_b9af7faf7ba179/gr-ru`, `book_67d8ba867eaf30/gr-ru`, `book_2e2a454f30b54e/gr-ru`, `book_3dd94793c4150b/gr-ru`, `book_76a0f1e7b20178/gr-ru`, `book_7ade48bd10bf6a/gr-ru`, `book_7108255329142c/gr-ru`, `book_218684a55fbd6d/gr-ru`, `book_2d826ea763eea3/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `s006/ru-gr`, `s010/gr-ru`, `p021/gr-ru`, `s014/ru-gr`, `p032/gr-ru`, `p031/gr-ru`, `patk03_005/ru-gr`, `s012/ru-gr`, `p025/gr-ru`, `patk03_002/ru-gr`, `s013/gr-ru`, `s011/ru-gr` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, typed Greek | `g2261021_509/grammar_fill`, `g2261021_510/grammar_fill`, `g2261021_511/grammar_fill`, `g2261021_512/grammar_fill`, `g2261021_513/grammar_fill`, `en261021_112/stress_enclitic`, `stress_w101/accent`, `en261021_132/stress_enclitic`, `sy261021_015/stress_syllable`, `g2261021_095/grammar_fill`, `stress_w113/accent`, `g2261021_067/grammar_fill` |
| 5 · book | book | 12 / 12 / 12 | choice | `p025/gr-ru`, `p032/ru-gr`, `patk03_003/gr-ru`, `s014/gr-ru`, `p027/gr-ru`, `p031/ru-gr`, `s009/gr-ru`, `patk03_002/gr-ru`, `s005/gr-ru`, `p021/ru-gr`, `s008/gr-ru`, `p022/ru-gr` |
| 6 · dialogue | dialogue | 12 / 6 / 12 | dialogue gap | `dlg004/gap0`, `dlg004/gap1`, `dlg034/gap0`, `dlg034/gap1`, `dlg027/gap0`, `dlg027/gap1`, `dlg108/gap0`, `dlg108/gap1`, `dlg033/gap0`, `dlg033/gap1`, `dlg031/gap0`, `dlg031/gap1` |
| 7 · clock | book | 12 / 12 / 12 | choice | `s011/ru-gr`, `p028/ru-gr`, `p025/gr-ru`, `p029/ru-gr`, `s013/gr-ru`, `p027/ru-gr`, `p022/gr-ru`, `s001/gr-ru`, `p026/gr-ru`, `patk03_005/gr-ru`, `patk03_004/gr-ru`, `p030/gr-ru` |
| 8 · life | life | 3 / 3 / 10 · short | typed scene | `family`, `meet`, `home_city` |

### Chapter 4

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `w130/ru-gr`, `w146/ru-gr`, `patk04_006/ru-gr`, `p043/gr-ru`, `patk04_002/gr-ru`, `w152/ru-gr`, `w157/ru-gr`, `w158/gr-ru`, `p034/ru-gr`, `s016/ru-gr`, `w195/gr-ru`, `s015/ru-gr`, `w131/ru-gr`, `w138/ru-gr` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_214db33660796a/gr-ru`, `book_62b469341fcb65/gr-ru`, `book_ddec3570d89bad/gr-ru`, `book_6fa5a48e5d32ca/gr-ru`, `book_8af023c3a00cd1/gr-ru`, `book_6080dc506fda90/gr-ru`, `book_e776ab3eb6629a/gr-ru`, `book_d5ff101d3b46ae/gr-ru`, `book_5b893c8e4737e7/gr-ru`, `book_c1ff2686c943b8/gr-ru`, `book_c8a582dcd2fce1/gr-ru`, `book_648c677172faa6/gr-ru`, `book_59bf21e6922231/gr-ru`, `book_cc12d432a860bf/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `p040/ru-gr`, `patk04_003/ru-gr`, `patk04_004/gr-ru`, `p036/gr-ru`, `s019/gr-ru`, `patk04_001/ru-gr`, `p039/gr-ru`, `p034/gr-ru`, `p038/gr-ru`, `p037/gr-ru`, `patk04_002/gr-ru`, `p043/gr-ru` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, typed Greek | `g2261021_514/grammar_fill`, `g2261021_515/grammar_fill`, `g2261021_516/grammar_fill`, `g2261021_517/grammar_fill`, `g2261021_518/grammar_fill`, `article_020/fill`, `stress_w155/accent`, `g2261021_071/grammar_fill`, `article_017/fill`, `stress_w150/accent`, `g2261021_009/grammar_fill`, `stress_w154/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `p035/ru-gr`, `p037/gr-ru`, `s019/ru-gr`, `patk04_006/ru-gr`, `p042/gr-ru`, `s018/gr-ru`, `patk04_003/ru-gr`, `s015/gr-ru`, `patk04_001/gr-ru`, `p038/gr-ru`, `p039/gr-ru`, `patk04_002/gr-ru` |
| 6 · dialogue | dialogue | 12 / 7 / 12 | dialogue gap | `dlg112/gap0`, `dlg112/gap1`, `dlg030/gap0`, `dlg030/gap1`, `dlg111/gap0`, `dlg111/gap1`, `dlg104/gap0`, `dlg104/gap1`, `dlg035/gap0`, `dlg103/gap0`, `dlg103/gap1`, `dlg029/gap0` |
| 7 · clock | book | 12 / 12 / 12 | choice | `s020/ru-gr`, `p043/gr-ru`, `s017/gr-ru`, `patk04_001/gr-ru`, `patk04_006/gr-ru`, `p035/gr-ru`, `s016/ru-gr`, `p042/gr-ru`, `p040/gr-ru`, `p034/gr-ru`, `s015/gr-ru`, `p038/ru-gr` |
| 8 · life | life | 4 / 4 / 10 · short | typed scene | `languages`, `family`, `meet`, `home_city` |

### Chapter 5

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `v1_002/ru-gr`, `v1_008/ru-gr`, `v1_001/gr-ru`, `v1_013/gr-ru`, `v1_010/gr-ru`, `v1_019/gr-ru`, `v1_012/ru-gr`, `v1_015/gr-ru`, `v1_016/ru-gr`, `v1_018/gr-ru`, `v1_014/gr-ru`, `v1_000/ru-gr`, `v1_011/ru-gr`, `v1_005/ru-gr` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_8c28beeecaf638/gr-ru`, `book_ac633a33098de5/gr-ru`, `book_d5ff101d3b46ae/gr-ru`, `book_85aa5ab80a3699/gr-ru`, `book_04cca81f677ffa/gr-ru`, `book_628209b31b3fdf/gr-ru`, `book_7ade48bd10bf6a/gr-ru`, `book_192d8a9b09ed13/gr-ru`, `book_dbc59b2dd843cc/gr-ru`, `book_f33bfc00c7a90a/gr-ru`, `book_ef735be5c4af1c/gr-ru`, `book_965a456cefc710/gr-ru`, `book_d7d09a78784f2f/gr-ru`, `book_5dabb61cdbb68b/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `v1_014/ru-gr`, `v1_019/gr-ru`, `v1_004/gr-ru`, `patk01_001/ru-gr`, `p001/ru-gr`, `s020/ru-gr`, `p002/ru-gr`, `patk03_001/gr-ru`, `patk04_002/gr-ru`, `patk04_003/ru-gr`, `p030/ru-gr`, `s016/gr-ru` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, typed Greek | `g2261021_514/grammar_fill`, `g2261021_515/grammar_fill`, `g2261021_516/grammar_fill`, `g2261021_517/grammar_fill`, `g2261021_518/grammar_fill`, `stress_v1_009/accent`, `stress_v1_001/accent`, `stress_v1_008/accent`, `stress_v1_013/accent`, `stress_v1_016/accent`, `stress_v1_015/accent`, `stress_v1_006/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `v1_019/gr-ru`, `v1_004/ru-gr`, `v1_014/gr-ru`, `s008/ru-gr`, `p033/ru-gr`, `p012/ru-gr`, `s003/gr-ru`, `patk02_003/ru-gr`, `p010/ru-gr`, `p037/gr-ru`, `s007/ru-gr`, `p038/ru-gr` |
| 6 · dialogue | dialogue | 12 / 7 / 12 | dialogue gap | `dlg004/gap0`, `dlg004/gap1`, `dlg026/gap0`, `dlg001/gap0`, `dlg001/gap1`, `dlg002/gap0`, `dlg002/gap1`, `dlg032/gap0`, `dlg032/gap1`, `dlg108/gap0`, `dlg108/gap1`, `dlg035/gap0` |
| 7 · clock | book | 12 / 12 / 12 | choice | `v1_019/gr-ru`, `v1_004/ru-gr`, `v1_014/ru-gr`, `p023/ru-gr`, `s014/ru-gr`, `s015/ru-gr`, `p041/gr-ru`, `p010/gr-ru`, `s006/gr-ru`, `s009/ru-gr`, `patk01_005/gr-ru`, `p016/ru-gr` |
| 8 · life | life | 4 / 4 / 10 · short | typed scene | `meet`, `home_city`, `languages`, `family` |

### Chapter 6

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `x05w020/gr-ru`, `x05w014/gr-ru`, `x05w022/gr-ru`, `x05w001/ru-gr`, `x05p001/gr-ru`, `x05w023/gr-ru`, `x05w002/gr-ru`, `x05w018/ru-gr`, `x05w015/ru-gr`, `x05p003/gr-ru`, `x05s002/ru-gr`, `x05p004/ru-gr`, `x05p005/ru-gr`, `x05w004/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_05ea689e73ee58/gr-ru`, `book_5c99121a9bec86/gr-ru`, `book_3043b83181c1bd/gr-ru`, `book_70fc2e5b1be96b/gr-ru`, `book_85344ae55f6a28/gr-ru`, `book_cea227bad7f42e/gr-ru`, `book_f745b230644690/gr-ru`, `book_ac62a9426741ab/gr-ru`, `book_f1f9242dea67b1/gr-ru`, `book_d768261149e655/gr-ru`, `book_4ed9ab36b328bf/gr-ru`, `book_0220470f992ac7/gr-ru`, `book_7a8c7d681e3624/gr-ru`, `book_32d21d3a8f5aaf/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `x05p001/ru-gr`, `x05p005/ru-gr`, `x05s002/gr-ru`, `x05p002/ru-gr`, `x05p003/ru-gr`, `x05p004/gr-ru`, `x05s001/ru-gr`, `patk03_004/ru-gr`, `patk04_006/ru-gr`, `s011/ru-gr`, `s014/ru-gr`, `patk03_006/ru-gr` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, token order, typed Greek | `g2261021_519/grammar_fill`, `g2261021_520/grammar_fill`, `g2261021_521/grammar_fill`, `g2261021_522/grammar_fill`, `g2261021_523/grammar_fill`, `stress_x05w018/accent`, `stress_x05w020/accent`, `stress_x05w008/accent`, `sy261021_020/stress_syllable`, `or261021_x05s002/arrange`, `stress_x05w012/accent`, `g2261021_487/grammar_fill` |
| 5 · book | book | 12 / 12 / 12 | choice | `x05p001/ru-gr`, `x05s001/gr-ru`, `x05p003/gr-ru`, `x05s002/ru-gr`, `x05p005/ru-gr`, `x05p004/ru-gr`, `x05p002/gr-ru`, `p025/ru-gr`, `p016/gr-ru`, `p020/gr-ru`, `patk01_006/ru-gr`, `patk04_004/gr-ru` |
| 6 · dialogue | dialogue | 12 / 7 / 12 | dialogue gap | `dlg041/gap0`, `dlg041/gap1`, `dlg011/gap0`, `dlg011/gap1`, `dlg044/gap0`, `dlg044/gap1`, `dlg043/gap0`, `dlg012/gap0`, `dlg012/gap1`, `dlg042/gap0`, `dlg021/gap0`, `dlg021/gap1` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_08_00/read`, `clock_04_35/read`, `clock_02_15/read`, `clock_10_25/read`, `clock_02_45/read`, `clock_07_05/read`, `clock_11_35/read`, `clock_12_30/read`, `clock_11_30/read`, `clock_09_50/read`, `clock_02_35/read`, `clock_11_05/read` |
| 8 · life | life | 5 / 5 / 10 · short | typed scene | `ticket`, `home_city`, `languages`, `meet`, `family` |

### Chapter 7

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `x06s002/ru-gr`, `x06w025/ru-gr`, `x06p004/ru-gr`, `x06w013/gr-ru`, `x06w015/ru-gr`, `x06w006/gr-ru`, `x06w021/ru-gr`, `x06w014/gr-ru`, `x06w009/gr-ru`, `x06w018/ru-gr`, `x06w026/ru-gr`, `x06w008/gr-ru`, `x06w022/gr-ru`, `x06w002/ru-gr` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_31e3673320933d/gr-ru`, `book_a042eb9b8b4ace/gr-ru`, `book_1912c2507f34d0/gr-ru`, `book_1f3a8b1f8041f2/gr-ru`, `book_e1cd7ee7596962/gr-ru`, `book_2bcff8aa01bfa3/gr-ru`, `book_51be4065298ba0/gr-ru`, `book_8c2d2cc8b8586d/gr-ru`, `book_243af97c39c53b/gr-ru`, `book_0c3bea0fe7e339/gr-ru`, `book_51cf7bd80176b9/gr-ru`, `book_353c67d03e5d49/gr-ru`, `book_9aa042d0a76e3e/gr-ru`, `book_71fa690a34352b/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `x06p003/gr-ru`, `x06p001/gr-ru`, `x06p004/gr-ru`, `x06s002/gr-ru`, `x06s001/ru-gr`, `x06p002/gr-ru`, `patk04_006/ru-gr`, `p034/gr-ru`, `patk02_003/ru-gr`, `x05p004/gr-ru`, `p009/ru-gr`, `p039/gr-ru` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, typed Greek | `g2261021_539/grammar_fill`, `g2261021_540/grammar_fill`, `g2261021_541/grammar_fill`, `g2261021_542/grammar_fill`, `g2261021_543/grammar_fill`, `g2261021_294/grammar_fill`, `g2261021_469/grammar_fill`, `g2261021_291/grammar_fill`, `g2261021_385/grammar_fill`, `stress_x06w017/accent`, `g2261021_139/grammar_fill`, `g2261021_404/grammar_fill` |
| 5 · book | book | 12 / 12 / 12 | choice | `x06p001/gr-ru`, `x06s001/ru-gr`, `x06s002/gr-ru`, `x06p004/gr-ru`, `x06p002/ru-gr`, `x06p003/ru-gr`, `x05s001/ru-gr`, `patk03_004/gr-ru`, `p015/gr-ru`, `p030/ru-gr`, `patk01_004/gr-ru`, `p022/gr-ru` |
| 6 · dialogue | dialogue | 12 / 7 / 12 | dialogue gap | `dlg010/gap0`, `dlg010/gap1`, `dlg047/gap0`, `dlg047/gap1`, `dlg022/gap0`, `dlg022/gap1`, `dlg039/gap0`, `dlg039/gap1`, `dlg036/gap0`, `dlg050/gap0`, `dlg049/gap0`, `dlg049/gap1` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_10_35/read`, `clock_10_10/read`, `clock_01_55/read`, `clock_11_40/read`, `clock_02_50/read`, `clock_06_40/read`, `clock_01_10/read`, `clock_01_45/read`, `clock_11_20/read`, `clock_06_30/read`, `clock_10_45/read`, `clock_04_55/read` |
| 8 · life | life | 6 / 6 / 10 · short | typed scene | `daily`, `family`, `home_city`, `meet`, `languages`, `ticket` |

### Chapter 8

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `x08w024/ru-gr`, `x07w016/gr-ru`, `x07s001/gr-ru`, `x08s001/gr-ru`, `x07w004/ru-gr`, `x07s002/ru-gr`, `x08w006/gr-ru`, `x08w010/ru-gr`, `x07w020/ru-gr`, `x08w016/gr-ru`, `x07w013/ru-gr`, `x07w014/ru-gr`, `x08w021/gr-ru`, `x07w009/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_8ae3d1779eaee7/gr-ru`, `book_cce576644c896e/gr-ru`, `book_036af9b78df9c4/gr-ru`, `book_4c842a16248428/gr-ru`, `book_7524f720a32126/gr-ru`, `book_c72a6d12afffb0/gr-ru`, `book_97a23e8e5e1a51/gr-ru`, `book_0c33e50b869e92/gr-ru`, `book_82af5acde7d7d6/gr-ru`, `book_a6e0b4df257a0c/gr-ru`, `book_d5f72ac6136525/gr-ru`, `book_5ebe39f9ff5c05/gr-ru`, `book_f6577fcb71947a/gr-ru`, `book_6f469285603176/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `x07p003/gr-ru`, `x08s001/ru-gr`, `x08s002/gr-ru`, `cm08_0501/gr-ru`, `x07s001/ru-gr`, `cm08_0502/ru-gr`, `x07s002/ru-gr`, `x08p002/gr-ru`, `sx261021_006/ru-gr`, `x07p004/ru-gr`, `cm08_0504/gr-ru`, `x08p004/gr-ru` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, token order, typed Greek | `g2261021_529/grammar_fill`, `g2261021_530/grammar_fill`, `g2261021_531/grammar_fill`, `g2261021_532/grammar_fill`, `g2261021_533/grammar_fill`, `g2261021_171/grammar_fill`, `en261021_122/stress_enclitic`, `stress_x08w020/accent`, `or261021_x08s002/arrange`, `stress_x07w001/accent`, `g2261021_118/grammar_fill`, `stress_x08w013/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `x07p001/ru-gr`, `x08p004/ru-gr`, `x07p002/ru-gr`, `x08s001/gr-ru`, `x08p003/ru-gr`, `cm08_0501/ru-gr`, `sx261021_006/ru-gr`, `x08p002/gr-ru`, `x07s002/gr-ru`, `cm08_0502/ru-gr`, `cm08_0503/gr-ru`, `x07p003/ru-gr` |
| 6 · dialogue | dialogue | 12 / 6 / 12 | dialogue gap | `dlg053/gap0`, `dlg053/gap1`, `dlg052/gap0`, `dlg052/gap1`, `dlg055/gap0`, `dlg055/gap1`, `dlg008/gap0`, `dlg008/gap1`, `dlg001/gap0`, `dlg001/gap1`, `dlg109/gap0`, `dlg109/gap1` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_03_50/read`, `clock_07_25/read`, `clock_02_20/read`, `clock_04_20/read`, `clock_07_20/read`, `clock_08_40/read`, `clock_05_20/read`, `clock_03_40/read`, `clock_08_05/read`, `clock_05_00/read`, `clock_07_35/read`, `clock_12_40/read` |
| 8 · life | life | 7 / 7 / 10 · short | typed scene | `groceries`, `meet`, `home_city`, `ticket`, `family`, `languages`, `daily` |

### Chapter 9

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `patk09_005/ru-gr`, `patk09_010/gr-ru`, `patk09_019/ru-gr`, `sx261021_007/ru-gr`, `patk09_006/ru-gr`, `patk09_013/gr-ru`, `patk09_003/gr-ru`, `patk09_018/ru-gr`, `patk09_008/ru-gr`, `patk09_014/ru-gr`, `patk09_020/gr-ru`, `patk09_004/ru-gr`, `patk09_009/gr-ru`, `patk09_015/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `vx0005/gr-ru`, `vx0008/gr-ru`, `book_ee2a6af2790022/gr-ru`, `vx0007/gr-ru`, `lexi_5c86577527420a0c08c5/gr-ru`, `lexi_48c2892bb6b88ca8c02e/gr-ru`, `book_7c165b8804bccc/gr-ru`, `book_d6ee834ed259b6/gr-ru`, `book_9a2540585c4fd4/gr-ru`, `book_373ae6d7a0e4d8/gr-ru`, `vx3019/gr-ru`, `lexi_55710a77a7feb6a2e346/gr-ru`, `book_9aa042d0a76e3e/gr-ru`, `vx0004/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `sx261021_007/gr-ru`, `patk09_019/gr-ru`, `patk09_020/ru-gr`, `patk09_017/ru-gr`, `patk09_018/ru-gr`, `x08s001/ru-gr`, `p020/ru-gr`, `s008/ru-gr`, `cm02_0601/ru-gr`, `x07p004/ru-gr`, `s010/ru-gr`, `p001/ru-gr` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, token order, typed Greek | `g2261021_529/grammar_fill`, `g2261021_530/grammar_fill`, `g2261021_531/grammar_fill`, `g2261021_532/grammar_fill`, `g2261021_533/grammar_fill`, `g2261021_479/grammar_fill`, `g2261021_464/grammar_fill`, `g2261021_017/grammar_fill`, `g2261021_020/grammar_fill`, `g2261021_011/grammar_fill`, `order_patk09_017/arrange`, `g2261021_018/grammar_fill` |
| 5 · book | book | 12 / 12 / 12 | choice | `patk09_018/gr-ru`, `patk09_020/gr-ru`, `sx261021_007/ru-gr`, `patk09_019/gr-ru`, `patk09_017/ru-gr`, `cm02_0603/gr-ru`, `x08s002/gr-ru`, `patk03_001/ru-gr`, `cm03_0601/gr-ru`, `cm02_0607/ru-gr`, `cm03_0001/gr-ru`, `cm04_0503/ru-gr` |
| 6 · dialogue | dialogue | 12 / 6 / 12 | dialogue gap | `dlg058/gap0`, `dlg058/gap1`, `dlg056/gap0`, `dlg056/gap1`, `dlg102/gap0`, `dlg102/gap1`, `dlg104/gap0`, `dlg104/gap1`, `dlg112/gap0`, `dlg112/gap1`, `dlg041/gap0`, `dlg041/gap1` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_11_30/read`, `clock_12_15/read`, `clock_05_25/read`, `clock_01_15/read`, `clock_04_50/read`, `clock_01_50/read`, `clock_08_45/read`, `clock_10_15/read`, `clock_02_30/read`, `clock_04_55/read`, `clock_11_50/read`, `clock_06_00/read` |
| 8 · life | life | 8 / 8 / 10 · short | typed scene | `clothes`, `home_city`, `ticket`, `groceries`, `languages`, `meet`, `family`, `daily` |

### Chapter 10

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `v2_003/gr-ru`, `v2_006/ru-gr`, `v2_019/ru-gr`, `v2_013/gr-ru`, `v2_001/gr-ru`, `v2_018/ru-gr`, `v2_004/ru-gr`, `v2_000/ru-gr`, `v2_016/gr-ru`, `v2_005/ru-gr`, `v2_017/ru-gr`, `v2_002/ru-gr`, `v2_015/gr-ru`, `v2_012/ru-gr` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_bbf6129a54adc4/gr-ru`, `book_5e9df0cc6d0d97/gr-ru`, `book_85344ae55f6a28/gr-ru`, `book_087ef03de725e5/gr-ru`, `book_8465924678a0f3/gr-ru`, `book_87763a02412bf0/gr-ru`, `book_c23e557f53a4b0/gr-ru`, `book_f1f9242dea67b1/gr-ru`, `book_cb28802cfffc3f/gr-ru`, `book_70fc2e5b1be96b/gr-ru`, `book_733951f8e927b0/gr-ru`, `book_7a8c7d681e3624/gr-ru`, `book_cea227bad7f42e/gr-ru`, `book_1912c2507f34d0/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `sx261021_008/ru-gr`, `v2_019/ru-gr`, `p026/ru-gr`, `s003/ru-gr`, `cm02_0501/ru-gr`, `cm07_0903/ru-gr`, `p001/ru-gr`, `p027/gr-ru`, `x08p003/ru-gr`, `s016/ru-gr`, `cm03_0509/gr-ru`, `p042/ru-gr` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, typed Greek | `g2261021_539/grammar_fill`, `g2261021_540/grammar_fill`, `g2261021_541/grammar_fill`, `g2261021_542/grammar_fill`, `g2261021_543/grammar_fill`, `stress_v2_002/accent`, `stress_v2_008/accent`, `stress_v2_005/accent`, `stress_v2_015/accent`, `stress_v2_012/accent`, `stress_v2_006/accent`, `stress_v2_007/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `v2_019/ru-gr`, `sx261021_008/gr-ru`, `cm03_0602/gr-ru`, `s014/gr-ru`, `cm03_0502/gr-ru`, `v1_014/gr-ru`, `s008/ru-gr`, `x08p002/ru-gr`, `patk02_002/gr-ru`, `cm01_0605/gr-ru`, `patk04_006/gr-ru`, `patk04_002/ru-gr` |
| 6 · dialogue | dialogue | 12 / 7 / 12 | dialogue gap | `dlg029/gap0`, `dlg107/gap0`, `dlg107/gap1`, `dlg052/gap0`, `dlg052/gap1`, `dlg112/gap0`, `dlg112/gap1`, `dlg006/gap0`, `dlg006/gap1`, `dlg030/gap0`, `dlg030/gap1`, `dlg050/gap0` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_03_15/read`, `clock_05_40/read`, `clock_07_40/read`, `clock_10_35/read`, `clock_03_55/read`, `clock_02_05/read`, `clock_07_35/read`, `clock_07_20/read`, `clock_04_25/read`, `clock_02_20/read`, `clock_08_05/read`, `clock_09_05/read` |
| 8 · life | life | 8 / 8 / 10 · short | typed scene | `groceries`, `languages`, `daily`, `meet`, `clothes`, `home_city`, `ticket`, `family` |

### Chapter 11

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `x09w021/ru-gr`, `x09w014/ru-gr`, `patk11_004/ru-gr`, `x09w017/gr-ru`, `x09w005/gr-ru`, `x09w015/ru-gr`, `x09p002/ru-gr`, `sx261021_009/gr-ru`, `x09w019/ru-gr`, `x09w013/gr-ru`, `x09w006/gr-ru`, `x09p004/ru-gr`, `x09w004/ru-gr`, `x09w018/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_e4e21b6d3b3e59/gr-ru`, `book_ab5670f8542ee3/gr-ru`, `book_dc7f86992f7440/gr-ru`, `book_d1b5d8f09d2b8a/gr-ru`, `book_63b14be9d79544/gr-ru`, `book_f8029fbb3c3fa7/gr-ru`, `book_10fa8485959bed/gr-ru`, `book_4687bb50dc650e/gr-ru`, `book_7cc70b8b2dcc1f/gr-ru`, `book_44a98df4641d4e/gr-ru`, `book_f088e7b744877f/gr-ru`, `book_891a1304d626f3/gr-ru`, `book_fdc054dea1484b/gr-ru`, `book_6f8f894df51941/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `patk11_001/gr-ru`, `sx261021_010/ru-gr`, `patk11_004/gr-ru`, `patk11_003/ru-gr`, `x09s002/ru-gr`, `sx261021_009/ru-gr`, `x09p004/ru-gr`, `x09p001/ru-gr`, `x09p003/gr-ru`, `patk11_002/gr-ru`, `x09s001/ru-gr`, `x09p002/ru-gr` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, token order, typed Greek | `g2261021_539/grammar_fill`, `g2261021_540/grammar_fill`, `g2261021_541/grammar_fill`, `g2261021_542/grammar_fill`, `g2261021_543/grammar_fill`, `g2261021_339/grammar_fill`, `or261021_x09s002/arrange`, `g2261021_332/grammar_fill`, `g2261021_024/grammar_fill`, `stress_x09w002/accent`, `g2261021_460/grammar_fill`, `en261021_041/stress_enclitic` |
| 5 · book | book | 12 / 12 / 12 | choice | `patk11_001/gr-ru`, `x09p001/ru-gr`, `x09p003/ru-gr`, `patk11_002/ru-gr`, `sx261021_010/gr-ru`, `x09p004/ru-gr`, `sx261021_009/gr-ru`, `x09p002/gr-ru`, `patk11_004/ru-gr`, `x09s001/ru-gr`, `x09s002/ru-gr`, `patk11_003/ru-gr` |
| 6 · dialogue | dialogue | 12 / 6 / 12 | dialogue gap | `dlg064/gap0`, `dlg064/gap1`, `dlg061/gap0`, `dlg061/gap1`, `dlg020/gap0`, `dlg020/gap1`, `dlg062/gap0`, `dlg062/gap1`, `dlg005/gap0`, `dlg005/gap1`, `dlg009/gap0`, `dlg009/gap1` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_11_30/read`, `clock_10_05/read`, `clock_12_55/read`, `clock_02_00/read`, `clock_02_20/read`, `clock_07_10/read`, `clock_12_15/read`, `clock_07_45/read`, `clock_11_05/read`, `clock_12_45/read`, `clock_12_00/read`, `clock_04_55/read` |
| 8 · life | life | 9 / 9 / 10 · short | typed scene | `directions`, `family`, `languages`, `ticket`, `meet`, `clothes`, `home_city`, `daily`, `groceries` |

### Chapter 12

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `x10w018/ru-gr`, `x10w011/gr-ru`, `x10w012/gr-ru`, `x10w013/gr-ru`, `x10w008/gr-ru`, `x10w019/gr-ru`, `x10w007/ru-gr`, `x10w021/ru-gr`, `x10w016/gr-ru`, `x10w020/gr-ru`, `x10w010/gr-ru`, `x10w004/ru-gr`, `x10w005/ru-gr`, `patk12_002/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_0000251e4f8df9/gr-ru`, `book_52295e93a2f573/gr-ru`, `book_ee1c24c458b9f1/gr-ru`, `book_d144d3bb1f11c6/gr-ru`, `book_a1fbbd3a059b3d/gr-ru`, `book_4f3dcd56c5bdee/gr-ru`, `book_2248f114cdb309/gr-ru`, `book_b580257d71bd84/gr-ru`, `book_226a900c1af5be/gr-ru`, `book_c58be7d33885d9/gr-ru`, `book_019ba7af63d6c7/gr-ru`, `book_96c34eba8bb9db/gr-ru`, `book_163809e27d3f05/gr-ru`, `book_c8faeb53dab37b/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `patk12_001/ru-gr`, `patk12_003/gr-ru`, `sx261021_011/ru-gr`, `patk12_004/gr-ru`, `patk12_002/ru-gr`, `sx261021_012/ru-gr`, `patk03_002/ru-gr`, `v1_019/ru-gr`, `cm03_0002/ru-gr`, `x07s002/gr-ru`, `patk09_017/gr-ru`, `p043/gr-ru` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, token order, typed Greek | `g2261021_539/grammar_fill`, `g2261021_540/grammar_fill`, `g2261021_541/grammar_fill`, `g2261021_542/grammar_fill`, `g2261021_543/grammar_fill`, `g2261021_039/grammar_fill`, `stress_x10w017/accent`, `stress_x10w018/accent`, `stress_x10w021/accent`, `stress_x10w019/accent`, `order_patk12_001/arrange`, `g2261021_040/grammar_fill` |
| 5 · book | book | 12 / 12 / 12 | choice | `patk12_004/gr-ru`, `sx261021_012/gr-ru`, `patk12_001/gr-ru`, `sx261021_011/ru-gr`, `patk12_002/ru-gr`, `patk12_003/gr-ru`, `patk04_002/ru-gr`, `s011/ru-gr`, `p030/ru-gr`, `sx261021_010/gr-ru`, `cm04_0601/gr-ru`, `x08p003/ru-gr` |
| 6 · dialogue | dialogue | 12 / 7 / 12 | dialogue gap | `dlg069/gap0`, `dlg069/gap1`, `dlg068/gap0`, `dlg068/gap1`, `dlg066/gap0`, `dlg066/gap1`, `dlg067/gap0`, `dlg067/gap1`, `dlg025/gap0`, `dlg047/gap0`, `dlg047/gap1`, `dlg035/gap0` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_09_05/read`, `clock_03_40/read`, `clock_04_45/read`, `clock_10_40/read`, `clock_01_10/read`, `clock_02_20/read`, `clock_12_35/read`, `clock_11_10/read`, `clock_09_45/read`, `clock_04_55/read`, `clock_02_10/read`, `clock_12_30/read` |
| 8 · life | life | 9 / 9 / 10 · short | typed scene | `directions`, `languages`, `ticket`, `family`, `meet`, `daily`, `home_city`, `groceries`, `clothes` |

### Chapter 13

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `x11w001/gr-ru`, `x11w018/gr-ru`, `x11p002/ru-gr`, `x11w020/gr-ru`, `x11s001/ru-gr`, `x11w022/gr-ru`, `x11w021/gr-ru`, `x11w019/ru-gr`, `x11p001/gr-ru`, `x11s002/gr-ru`, `x11w013/ru-gr`, `x11w014/gr-ru`, `x11w015/ru-gr`, `x11w004/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_b9fba93e3a2691/gr-ru`, `book_0849dd2a309561/gr-ru`, `book_3088a3f157d8ad/gr-ru`, `book_a13332df0c97d0/gr-ru`, `book_e4735863ac6229/gr-ru`, `book_6f469285603176/gr-ru`, `book_7b9e5d45709608/gr-ru`, `book_71e87d9b5235c2/gr-ru`, `book_77e7d1d6cdde16/gr-ru`, `book_3fd9a07c2f92fb/gr-ru`, `book_42d7954f0bb576/gr-ru`, `book_3451ade35a22cb/gr-ru`, `book_d40e13dbff53e0/gr-ru`, `book_f91465566417bd/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `x11p004/ru-gr`, `x11s002/ru-gr`, `x11p003/ru-gr`, `x11p002/ru-gr`, `x11s001/ru-gr`, `x11p001/ru-gr`, `patk02_001/ru-gr`, `sx261021_006/gr-ru`, `p013/ru-gr`, `patk03_002/ru-gr`, `s002/gr-ru`, `p019/gr-ru` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, token order, typed Greek | `g2261021_539/grammar_fill`, `g2261021_540/grammar_fill`, `g2261021_541/grammar_fill`, `g2261021_542/grammar_fill`, `g2261021_543/grammar_fill`, `g2261021_308/grammar_fill`, `stress_x11w005/accent`, `or261021_x11s002/arrange`, `stress_x11w010/accent`, `g2261021_334/grammar_fill`, `stress_x11w009/accent`, `stress_x11w021/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `x11p003/gr-ru`, `x11s001/gr-ru`, `x11s002/ru-gr`, `x11p001/ru-gr`, `x11p002/gr-ru`, `x11p004/gr-ru`, `p018/ru-gr`, `p029/gr-ru`, `p035/gr-ru`, `sx261021_011/ru-gr`, `cm04_0601/ru-gr`, `cm03_0508/ru-gr` |
| 6 · dialogue | dialogue | 12 / 6 / 12 | dialogue gap | `dlg074/gap0`, `dlg074/gap1`, `dlg071/gap0`, `dlg071/gap1`, `dlg073/gap0`, `dlg073/gap1`, `dlg023/gap0`, `dlg023/gap1`, `dlg075/gap0`, `dlg075/gap1`, `dlg072/gap0`, `dlg072/gap1` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_04_40/read`, `clock_03_45/read`, `clock_11_40/read`, `clock_12_15/read`, `clock_01_40/read`, `clock_05_00/read`, `clock_09_20/read`, `clock_03_20/read`, `clock_12_00/read`, `clock_09_50/read`, `clock_08_00/read`, `clock_08_20/read` |
| 8 · life | life | 9 / 9 / 10 · short | typed scene | `ticket`, `daily`, `meet`, `groceries`, `clothes`, `directions`, `languages`, `home_city`, `family` |

### Chapter 14

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `x12s002/gr-ru`, `patk14_003/gr-ru`, `x12w008/ru-gr`, `x12p003/ru-gr`, `x12w017/ru-gr`, `patk14_002/gr-ru`, `patk14_005/ru-gr`, `x12w015/ru-gr`, `sx261021_013/ru-gr`, `x12p002/ru-gr`, `x12w016/gr-ru`, `x12w013/ru-gr`, `x12w009/ru-gr`, `x12w004/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_b3f26231aad4b8/gr-ru`, `book_12662c1cc98375/gr-ru`, `book_c3dfb182b36ef5/gr-ru`, `book_30e92d1324a5e3/gr-ru`, `book_305b3fc683429f/gr-ru`, `book_7507297ea58f2c/gr-ru`, `book_7e2d93e213f552/gr-ru`, `book_42c503bd0db42d/gr-ru`, `book_6e5c7ae3e5bc7b/gr-ru`, `book_6027c6980430a7/gr-ru`, `book_3b260bf675b082/gr-ru`, `book_8c292dd7eed981/gr-ru`, `book_9223fb579c9256/gr-ru`, `book_aec660128ae571/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `patk14_001/ru-gr`, `x12p001/ru-gr`, `patk14_003/ru-gr`, `patk14_002/ru-gr`, `sx261021_014/gr-ru`, `patk14_004/ru-gr`, `sx261021_013/gr-ru`, `x12p002/ru-gr`, `x12s001/gr-ru`, `x12p003/gr-ru`, `x12s002/gr-ru`, `patk14_006/ru-gr` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, token order, typed Greek | `g2261021_534/grammar_fill`, `g2261021_535/grammar_fill`, `g2261021_536/grammar_fill`, `g2261021_537/grammar_fill`, `g2261021_538/grammar_fill`, `stress_x12w015/accent`, `g2261021_043/grammar_fill`, `or261021_patk14_005/arrange`, `g2261021_042/grammar_fill`, `g2261021_045/grammar_fill`, `stress_x12w012/accent`, `stress_x12w014/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `x12s001/gr-ru`, `x12p002/gr-ru`, `patk14_002/gr-ru`, `x12p003/ru-gr`, `patk14_003/ru-gr`, `patk14_006/ru-gr`, `patk14_005/ru-gr`, `x12p001/gr-ru`, `patk14_001/gr-ru`, `sx261021_014/ru-gr`, `patk14_004/ru-gr`, `x12s002/gr-ru` |
| 6 · dialogue | dialogue | 12 / 7 / 12 | dialogue gap | `dlg080/gap0`, `dlg080/gap1`, `dlg080/gap2`, `dlg007/gap0`, `dlg007/gap1`, `dlg070/gap0`, `dlg070/gap1`, `dlg054/gap0`, `dlg051/gap0`, `dlg013/gap0`, `dlg013/gap1`, `dlg035/gap0` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_10_00/read`, `clock_03_20/read`, `clock_07_25/read`, `clock_08_05/read`, `clock_11_20/read`, `clock_12_00/read`, `clock_05_50/read`, `clock_06_45/read`, `clock_03_55/read`, `clock_08_15/read`, `clock_08_25/read`, `clock_12_20/read` |
| 8 · life | life | 10 / 10 / 10 | typed scene | `cafe`, `family`, `home_city`, `ticket`, `groceries`, `daily`, `directions`, `meet`, `languages`, `clothes` |

### Chapter 15

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `v3_015/gr-ru`, `v3_013/gr-ru`, `v3_009/gr-ru`, `v3_012/ru-gr`, `v3_003/ru-gr`, `v3_014/ru-gr`, `v3_017/ru-gr`, `v3_000/gr-ru`, `v3_016/ru-gr`, `v3_005/ru-gr`, `v3_008/gr-ru`, `v3_019/ru-gr`, `v3_006/gr-ru`, `v3_007/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_f325cd9b465eb8/gr-ru`, `book_c3dfb182b36ef5/gr-ru`, `book_4687bb50dc650e/gr-ru`, `book_44a98df4641d4e/gr-ru`, `book_b580257d71bd84/gr-ru`, `book_ae1687aede451a/gr-ru`, `book_c2a3eed5dfa2c7/gr-ru`, `book_ab5670f8542ee3/gr-ru`, `book_6f469285603176/gr-ru`, `book_c1c3d9542f583e/gr-ru`, `book_66353d9ea3b0ab/gr-ru`, `book_7b9e5d45709608/gr-ru`, `book_7fccb52f207643/gr-ru`, `book_71e87d9b5235c2/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `v3_019/gr-ru`, `p023/ru-gr`, `v1_014/ru-gr`, `v2_019/gr-ru`, `s011/gr-ru`, `x08s002/ru-gr`, `cm08_0503/ru-gr`, `x08p001/gr-ru`, `cm03_0502/ru-gr`, `patk01_004/gr-ru`, `patk03_004/gr-ru`, `sx261021_002/gr-ru` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, typed Greek | `g2261021_539/grammar_fill`, `g2261021_540/grammar_fill`, `g2261021_541/grammar_fill`, `g2261021_542/grammar_fill`, `g2261021_543/grammar_fill`, `stress_v3_018/accent`, `stress_v3_007/accent`, `stress_v3_012/accent`, `stress_v3_000/accent`, `stress_v3_014/accent`, `stress_v3_004/accent`, `stress_v3_009/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `v3_019/ru-gr`, `x09s001/gr-ru`, `cm04_0505/ru-gr`, `p005/ru-gr`, `patk11_002/gr-ru`, `p019/ru-gr`, `patk09_017/gr-ru`, `sx261021_001/ru-gr`, `p021/ru-gr`, `cm03_0512/ru-gr`, `patk03_003/ru-gr`, `x11p004/ru-gr` |
| 6 · dialogue | dialogue | 12 / 7 / 12 | dialogue gap | `dlg064/gap0`, `dlg064/gap1`, `dlg110/gap0`, `dlg110/gap1`, `dlg062/gap0`, `dlg062/gap1`, `dlg009/gap0`, `dlg009/gap1`, `dlg043/gap0`, `dlg025/gap0`, `dlg052/gap0`, `dlg052/gap1` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_11_50/read`, `clock_02_20/read`, `clock_08_10/read`, `clock_10_45/read`, `clock_09_20/read`, `clock_06_15/read`, `clock_04_20/read`, `clock_03_45/read`, `clock_10_30/read`, `clock_03_10/read`, `clock_04_15/read`, `clock_09_45/read` |
| 8 · life | life | 10 / 10 / 10 | typed scene | `daily`, `directions`, `family`, `meet`, `groceries`, `cafe`, `home_city`, `ticket`, `languages`, `clothes` |

### Chapter 16

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `x13w005/ru-gr`, `x13w003/ru-gr`, `patk16_003/gr-ru`, `x13p002/ru-gr`, `patk16_002/gr-ru`, `sx261021_016/ru-gr`, `x13s001/ru-gr`, `x13w014/gr-ru`, `sx261021_015/ru-gr`, `x13w009/ru-gr`, `cm16_0802/ru-gr`, `cm16_0806/gr-ru`, `x13w001/ru-gr`, `x13w011/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_36a64b1623f639/gr-ru`, `book_49289c4fe1a138/gr-ru`, `book_27522d493fb2f9/gr-ru`, `book_749ad12ea2b954/gr-ru`, `book_38930c78317ae5/gr-ru`, `book_4be4dbf0d0e7b4/gr-ru`, `book_7ba7270707969c/gr-ru`, `book_69d7a5515b71a1/gr-ru`, `book_40716f54603275/gr-ru`, `book_92be57241345b7/gr-ru`, `book_7595920966941b/gr-ru`, `book_ee4cf168cba1ae/gr-ru`, `book_ec29bfd043a461/gr-ru`, `book_3578d3aace56e3/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `cm16_0810/ru-gr`, `cm16_0809/ru-gr`, `cm16_0805/ru-gr`, `sx261021_015/ru-gr`, `x13s002/ru-gr`, `x10p001/gr-ru`, `x10s001/ru-gr`, `x12p004/gr-ru`, `patk16_002/gr-ru`, `cm16_0801/gr-ru`, `patk16_001/ru-gr`, `cm16_0804/gr-ru` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, typed Greek | `g2261021_534/grammar_fill`, `g2261021_535/grammar_fill`, `g2261021_536/grammar_fill`, `g2261021_537/grammar_fill`, `g2261021_538/grammar_fill`, `g2261021_201/grammar_fill`, `g2261021_252/grammar_fill`, `g2261021_173/grammar_fill`, `g2261021_182/grammar_fill`, `g2261021_217/grammar_fill`, `g2261021_178/grammar_fill`, `g2261021_185/grammar_fill` |
| 5 · book | book | 12 / 12 / 12 | choice | `x13p002/ru-gr`, `x10p004/ru-gr`, `x13p004/gr-ru`, `cm16_0810/ru-gr`, `patk16_003/ru-gr`, `x12p004/ru-gr`, `x10s001/gr-ru`, `cm16_0804/ru-gr`, `x13p001/gr-ru`, `patk16_001/ru-gr`, `patk16_002/gr-ru`, `x13p003/gr-ru` |
| 6 · dialogue | dialogue | 12 / 6 / 12 | dialogue gap | `dlg017/gap0`, `dlg017/gap1`, `dlg081/gap0`, `dlg081/gap1`, `dlg045/gap0`, `dlg045/gap1`, `dlg045/gap2`, `dlg082/gap0`, `dlg082/gap1`, `dlg078/gap0`, `dlg078/gap1`, `dlg042/gap0` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_05_55/read`, `clock_12_55/read`, `clock_02_35/read`, `clock_12_00/read`, `clock_07_45/read`, `clock_07_30/read`, `clock_10_05/read`, `clock_04_45/read`, `clock_01_10/read`, `clock_02_50/read`, `clock_05_45/read`, `clock_10_45/read` |
| 8 · life | life | 10 / 10 / 10 | typed scene | `plans`, `family`, `directions`, `groceries`, `home_city`, `languages`, `meet`, `ticket`, `cafe`, `clothes` |

### Chapter 17

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `x14w008/gr-ru`, `x14w013/gr-ru`, `x14s001/ru-gr`, `x14w018/gr-ru`, `patk17_004/ru-gr`, `x14w002/gr-ru`, `x14p003/gr-ru`, `x14w010/ru-gr`, `patk17_003/ru-gr`, `x14w003/gr-ru`, `x14w007/ru-gr`, `x14w011/gr-ru`, `x14w001/gr-ru`, `x14w004/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_d7484ecba4655e/gr-ru`, `book_916e083dc85414/gr-ru`, `book_98690cd2454f5f/gr-ru`, `book_755437b5b35891/gr-ru`, `book_4c71efb3c891e8/gr-ru`, `book_73fe696890e737/gr-ru`, `book_cb098593ca1249/gr-ru`, `book_323cf7f968b7d8/gr-ru`, `book_9c3fa810eb338c/gr-ru`, `book_4380d3791263c1/gr-ru`, `book_a769a331bbd32d/gr-ru`, `book_ee0d8accf15146/gr-ru`, `book_f4377d0597a3e7/gr-ru`, `book_0f1e6035fe146f/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `x14s002/ru-gr`, `x14s001/ru-gr`, `x14p002/gr-ru`, `patk17_001/gr-ru`, `x14p003/gr-ru`, `x14p004/gr-ru`, `patk17_004/gr-ru`, `patk17_003/gr-ru`, `patk17_002/gr-ru`, `x14p001/gr-ru`, `cm03_0601/gr-ru`, `patk11_001/ru-gr` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, token order, typed Greek | `g2261021_534/grammar_fill`, `g2261021_535/grammar_fill`, `g2261021_536/grammar_fill`, `g2261021_537/grammar_fill`, `g2261021_538/grammar_fill`, `stress_x14w021/accent`, `en261021_071/stress_enclitic`, `stress_x14w020/accent`, `en261021_072/stress_enclitic`, `or261021_x14s002/arrange`, `stress_x14w008/accent`, `stress_x14w012/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `patk17_004/ru-gr`, `patk17_002/gr-ru`, `patk17_003/gr-ru`, `x14p001/ru-gr`, `x14p002/gr-ru`, `x14s002/gr-ru`, `x14p003/gr-ru`, `x14s001/ru-gr`, `x14p004/gr-ru`, `patk17_001/ru-gr`, `x11p002/ru-gr`, `patk04_006/ru-gr` |
| 6 · dialogue | dialogue | 12 / 6 / 12 | dialogue gap | `dlg088/gap0`, `dlg089/gap0`, `dlg089/gap1`, `dlg090/gap0`, `dlg090/gap1`, `dlg090/gap2`, `dlg018/gap0`, `dlg018/gap1`, `dlg087/gap0`, `dlg087/gap1`, `dlg086/gap0`, `dlg086/gap1` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_10_10/read`, `clock_09_30/read`, `clock_02_20/read`, `clock_12_55/read`, `clock_10_05/read`, `clock_12_05/read`, `clock_01_20/read`, `clock_04_40/read`, `clock_12_50/read`, `clock_09_50/read`, `clock_01_55/read`, `clock_02_25/read` |
| 8 · life | life | 10 / 10 / 10 | typed scene | `clothes`, `home_city`, `daily`, `groceries`, `cafe`, `meet`, `directions`, `languages`, `family`, `plans` |

### Chapter 18

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `x15p001/ru-gr`, `x15w006/ru-gr`, `x15s001/ru-gr`, `sx261021_017/ru-gr`, `x15w009/gr-ru`, `patk18_001/gr-ru`, `sx261021_018/gr-ru`, `x15w001/gr-ru`, `x15p003/ru-gr`, `patk18_004/gr-ru`, `x15w013/ru-gr`, `x15w005/ru-gr`, `x15w020/gr-ru`, `x15w011/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_95d8d4d56e6292/gr-ru`, `book_f0102afd595622/gr-ru`, `book_c2eb67dbbd8df3/gr-ru`, `book_f10a1c9f2f39ba/gr-ru`, `book_f74fd9c2f24dcc/gr-ru`, `book_efba4b5835fb95/gr-ru`, `book_30dbd155473142/gr-ru`, `book_10515044f0da83/gr-ru`, `book_bc56154f6e353c/gr-ru`, `book_c40f649230c36f/gr-ru`, `book_528f3c464df88d/gr-ru`, `book_2bb4bccb829f12/gr-ru`, `book_34841b0bd94b55/gr-ru`, `book_242fb6c58bb731/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `patk18_003/ru-gr`, `x15p001/ru-gr`, `x15p004/gr-ru`, `sx261021_017/ru-gr`, `x15p003/gr-ru`, `patk18_001/gr-ru`, `sx261021_018/ru-gr`, `x15s002/gr-ru`, `x15s001/gr-ru`, `patk18_002/ru-gr`, `x15p002/ru-gr`, `patk18_004/ru-gr` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, typed Greek | `g2261021_529/grammar_fill`, `g2261021_530/grammar_fill`, `g2261021_531/grammar_fill`, `g2261021_532/grammar_fill`, `g2261021_533/grammar_fill`, `stress_x15w014/accent`, `sy261021_029/stress_syllable`, `stress_x15w019/accent`, `stress_x15w016/accent`, `stress_x15w004/accent`, `stress_x15w005/accent`, `stress_x15w007/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `x15s002/gr-ru`, `sx261021_017/gr-ru`, `x15s001/ru-gr`, `x15p003/gr-ru`, `patk18_001/gr-ru`, `x15p004/gr-ru`, `patk18_004/gr-ru`, `x15p002/ru-gr`, `x15p001/gr-ru`, `patk18_002/gr-ru`, `sx261021_018/gr-ru`, `patk18_003/ru-gr` |
| 6 · dialogue | dialogue | 12 / 6 / 12 | dialogue gap | `dlg093/gap0`, `dlg093/gap1`, `dlg015/gap0`, `dlg015/gap1`, `dlg091/gap0`, `dlg091/gap1`, `dlg094/gap0`, `dlg094/gap1`, `dlg094/gap2`, `dlg016/gap0`, `dlg016/gap1`, `dlg095/gap0` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_05_50/read`, `clock_08_50/read`, `clock_10_10/read`, `clock_02_15/read`, `clock_03_50/read`, `clock_11_30/read`, `clock_08_45/read`, `clock_04_45/read`, `clock_03_25/read`, `clock_11_45/read`, `clock_01_15/read`, `clock_09_00/read` |
| 8 · life | life | 10 / 10 / 10 | typed scene | `family`, `languages`, `plans`, `meet`, `groceries`, `directions`, `cafe`, `daily`, `ticket`, `clothes` |

### Chapter 19

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `x16w022/ru-gr`, `x16w009/ru-gr`, `x16w003/gr-ru`, `x16w012/gr-ru`, `x16p004/ru-gr`, `x16w018/gr-ru`, `x16p001/ru-gr`, `x16w013/ru-gr`, `x16w019/gr-ru`, `x16s002/gr-ru`, `patk19_004/ru-gr`, `x16w002/ru-gr`, `x16w005/ru-gr`, `x16w001/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_c784dfa1ef29db/gr-ru`, `book_e2dd8fbd982218/gr-ru`, `book_a45d0e72ff477f/gr-ru`, `book_86395821ab8a52/gr-ru`, `book_2092ff370a842c/gr-ru`, `book_4f5b5bb0b0e98e/gr-ru`, `book_53f9d70537e7ab/gr-ru`, `book_10906f280f5055/gr-ru`, `book_fc7faf00af7c6f/gr-ru`, `book_e4989317e9761c/gr-ru`, `book_2e98027677ab15/gr-ru`, `book_d292b49f921488/gr-ru`, `book_3740a3b0e472dd/gr-ru`, `book_94f6b23c7f64c8/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `x16p002/gr-ru`, `x16s001/gr-ru`, `patk19_004/gr-ru`, `x16p001/ru-gr`, `patk19_003/ru-gr`, `x16s002/gr-ru`, `x16p004/gr-ru`, `patk19_002/ru-gr`, `patk19_001/ru-gr`, `x16p003/gr-ru`, `sx261021_008/gr-ru`, `patk16_002/gr-ru` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, token order, typed Greek | `g2261021_534/grammar_fill`, `g2261021_535/grammar_fill`, `g2261021_536/grammar_fill`, `g2261021_537/grammar_fill`, `g2261021_538/grammar_fill`, `stress_x16w010/accent`, `stress_x16w013/accent`, `stress_x16w011/accent`, `stress_x16w003/accent`, `or261021_x16s001/arrange`, `stress_x16w018/accent`, `stress_x16w008/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `x16s001/gr-ru`, `x16p004/ru-gr`, `x16p002/ru-gr`, `patk19_002/ru-gr`, `patk19_001/gr-ru`, `patk19_003/gr-ru`, `x16p003/gr-ru`, `x16s002/ru-gr`, `patk19_004/ru-gr`, `x16p001/gr-ru`, `x06p004/ru-gr`, `patk16_003/ru-gr` |
| 6 · dialogue | dialogue | 12 / 6 / 12 | dialogue gap | `dlg099/gap0`, `dlg099/gap1`, `dlg098/gap0`, `dlg098/gap1`, `dlg100/gap0`, `dlg100/gap1`, `dlg100/gap2`, `dlg097/gap0`, `dlg097/gap1`, `dlg096/gap0`, `dlg109/gap0`, `dlg109/gap1` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_02_25/read`, `clock_07_45/read`, `clock_01_30/read`, `clock_04_25/read`, `clock_11_05/read`, `clock_12_50/read`, `clock_02_15/read`, `clock_09_00/read`, `clock_06_20/read`, `clock_10_35/read`, `clock_08_05/read`, `clock_07_10/read` |
| 8 · life | life | 10 / 10 / 10 | typed scene | `daily`, `clothes`, `home_city`, `languages`, `groceries`, `family`, `directions`, `cafe`, `plans`, `ticket` |

### Chapter 20

| Slot / actual family | Goal family | Responses / cards / target | Response types | Existing card IDs and directions |
| --- | --- | --- | --- | --- |
| 1 · book | book | 14 / 14 / 14 | choice | `v4_016/gr-ru`, `v4_018/ru-gr`, `v4_003/gr-ru`, `v4_007/gr-ru`, `v4_008/ru-gr`, `v4_013/ru-gr`, `v4_000/ru-gr`, `v4_011/ru-gr`, `v4_006/ru-gr`, `v4_010/ru-gr`, `v4_012/gr-ru`, `v4_009/gr-ru`, `v4_001/gr-ru`, `v4_002/gr-ru` |
| 2 · lexicon | lexicon | 14 / 14 / 14 | choice | `book_3578d3aace56e3/gr-ru`, `book_3a90518ed355b7/gr-ru`, `book_0f1e6035fe146f/gr-ru`, `book_d292b49f921488/gr-ru`, `book_ee0d8accf15146/gr-ru`, `book_2bb4bccb829f12/gr-ru`, `book_2092ff370a842c/gr-ru`, `book_3710e8e7c459ca/gr-ru`, `book_38930c78317ae5/gr-ru`, `book_4be4dbf0d0e7b4/gr-ru`, `book_69d5fbe7bba421/gr-ru`, `book_30dbd155473142/gr-ru`, `book_f4377d0597a3e7/gr-ru`, `book_4380d3791263c1/gr-ru` |
| 3 · book | book | 12 / 12 / 12 | choice | `p031/ru-gr`, `x14p003/gr-ru`, `x10p003/ru-gr`, `x09p003/gr-ru`, `x10p002/gr-ru`, `p003/gr-ru`, `x06p004/ru-gr`, `patk14_006/gr-ru`, `patk14_002/ru-gr`, `patk17_002/ru-gr`, `s014/gr-ru`, `patk14_001/gr-ru` |
| 4 · grammar | grammar | 12 / 12 / 12 | choice, letter index, typed Greek | `g2261021_529/grammar_fill`, `g2261021_530/grammar_fill`, `g2261021_531/grammar_fill`, `g2261021_532/grammar_fill`, `g2261021_533/grammar_fill`, `stress_v4_015/accent`, `stress_v4_004/accent`, `stress_v4_016/accent`, `stress_v4_001/accent`, `stress_v4_003/accent`, `stress_v4_019/accent`, `stress_v4_006/accent` |
| 5 · book | book | 12 / 12 / 12 | choice | `x11p003/ru-gr`, `x14s001/gr-ru`, `p043/gr-ru`, `patk01_002/ru-gr`, `x13p002/ru-gr`, `patk19_002/gr-ru`, `x11s001/ru-gr`, `patk04_001/gr-ru`, `patk16_001/ru-gr`, `cm04_0504/ru-gr`, `sx261021_017/ru-gr`, `p025/ru-gr` |
| 6 · dialogue | dialogue | 12 / 6 / 12 | dialogue gap | `dlg010/gap0`, `dlg010/gap1`, `dlg085/gap0`, `dlg085/gap1`, `dlg085/gap2`, `dlg049/gap0`, `dlg049/gap1`, `dlg101/gap0`, `dlg101/gap1`, `dlg111/gap0`, `dlg111/gap1`, `dlg025/gap0` |
| 7 · clock | clock | 12 / 12 / 12 | choice | `clock_06_10/read`, `clock_08_20/read`, `clock_11_30/read`, `clock_01_45/read`, `clock_06_15/read`, `clock_07_20/read`, `clock_07_35/read`, `clock_10_05/read`, `clock_06_20/read`, `clock_10_15/read`, `clock_03_40/read`, `clock_10_40/read` |
| 8 · life | life | 10 / 10 / 10 | typed scene | `languages`, `meet`, `clothes`, `cafe`, `groceries`, `home_city`, `daily`, `ticket`, `directions`, `family` |

## Editorial volume flags

14 of 160 representative lessons are shorter than their maximum target.
The rows above identify the exact affected chapters and families. This is an
inventory of available scoped practice, not a request to fill gaps with future
vocabulary or artificial repetition.

