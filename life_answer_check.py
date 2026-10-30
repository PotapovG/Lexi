"""High-confidence diagnostics for Greek Life free-typed answers.

Greedy token membership checks are wrong: "στη" and "στην" both occur in
accepted textbook variants, and a typo in "Λευκωσία" is not a missing article.
Only diagnose a mistake when structure is unambiguous. Unrecognized
grammatical alternatives are never scored as errors.
"""
from __future__ import annotations

from difflib import SequenceMatcher
import unicodedata

from study_tracks import _normalized

# Functional words whose differences can be explained specifically.
_ARTICLES = {
    "ο", "η", "το", "οι", "τα", "τον", "τη", "την", "του", "της",
    "στο", "στη", "στην", "στον", "τους", "τις", "ενα", "εναν",
    "μια", "μιαν", "ενας",
}
_PARTICLES = {"να": ("частица να", "the particle να"),
              "δεν": ("отрицание δεν", "negative δεν")}


def _plain_tokens(value: str) -> list[str]:
    return _normalized(value).split()


def _raw_words(value: str) -> list[str]:
    # Preserve original Greek tonos for showing the exact misspelled word.
    clean = "".join(ch if ch.isalpha() or ch.isspace() else " " for ch in value)
    return clean.split()


def _nearest(text: str, candidates: tuple[str, ...]) -> str:
    """Choose the accepted sentence structurally closest to the answer."""
    a = _plain_tokens(text)
    return max(candidates, key=lambda item: (
        SequenceMatcher(None, a, _plain_tokens(item), autojunk=False).ratio(),
        SequenceMatcher(None, " ".join(a), " ".join(_plain_tokens(item)), autojunk=False).ratio()
    ))


def evaluate(answer: str, accepted: tuple[str, ...], lang: str = "ru") -> dict:
    if not accepted:
        raise ValueError("no_reviewed_answers")
    ru = lang == "ru"
    selected = _plain_tokens(answer)
    correct_variant = next((s for s in accepted if selected == _plain_tokens(s)), None)
    if correct_variant is not None:
        # Punctuation and capitals are insignificant. Tonos omission is
        # accepted but highlighted without counting as a mistake.
        given_words = _raw_words(answer)
        expected_words = _raw_words(correct_variant)
        notes = None
        if len(given_words) == len(expected_words) and all(
            _normalized(a) == _normalized(b) for a, b in zip(given_words, expected_words)
        ) and any(
            unicodedata.normalize("NFC",a).casefold() !=
            unicodedata.normalize("NFC",b).casefold()
            for a, b in zip(given_words, expected_words)
        ):
            notes = (("Ответ засчитан. Обрати внимание на ударения: " if ru else
                      "Accepted. Note the accent marks: ") + correct_variant)
        return {"correct": True, "unverified": False, "explanation": None,
                "orthographyNote": notes, "closest": correct_variant}

    best = _nearest(answer, accepted)
    expected = _plain_tokens(best)
    written = _raw_words(answer)
    exemplar = _raw_words(best)
    if not selected:
        return _unknown(best, lang)

    # Equal-length, one-token discrepancy: recognize wrong word or near typo
    # before checking for 'missing' words. A correct word already *exists*
    # at the expected slot, so claiming it is missing is misleading.
    if len(selected) == len(expected):
        changed = [i for i, (a, b) in enumerate(zip(selected, expected)) if a != b]
        if len(changed) == 1:
            i = changed[0]
            actual, wanted = selected[i], expected[i]
            display_actual = written[i] if i < len(written) else actual
            display_wanted = exemplar[i] if i < len(exemplar) else wanted
            if actual in _ARTICLES or wanted in _ARTICLES:
                return _known(
                    (f"Здесь нужна форма «{display_wanted}», а не «{display_actual}». Проверь предлог, род или падеж."
                     if ru else f"Use «{display_wanted}» rather than «{display_actual}». Check the preposition, gender or case."),
                    best
                )
            if actual == "αρεσει" and wanted == "αρεσουν":
                return _known("С несколькими предметами употребляется «αρέσουν»." if ru else
                              "Use «αρέσουν» for plural things.", best)
            if actual == "αρεσουν" and wanted == "αρεσει":
                return _known("С одним предметом употребляется «αρέσει»." if ru else
                              "Use «αρέσει» for singular things.", best)
            ratio = SequenceMatcher(None, actual, wanted).ratio()
            if ratio >= 0.62 and len(wanted) >= 4:
                return _known(
                    (f"Похоже, опечатка в слове «{display_actual}». Проверь написание: «{display_wanted}»."
                     if ru else f"Likely a typo in «{display_actual}». Check the spelling: «{display_wanted}»."),
                    best
                )
            # An entirely different noun/verb may be a grammatical synonym;
            # leave its judgment open rather than producing a false rule.
            return _unknown(best, lang)

    # True missing particles: compare with the nearest reviewed variant,
    # and accept only if all other words align after removing that token.
    for particle in ("να", "δεν"):
        if particle in expected and particle not in selected:
            remaining = list(expected)
            remaining.remove(particle)
            if remaining == selected:
                if particle == "να":
                    return _known("Пропущена частица «να» перед глаголом." if ru else
                                  "The particle «να» is missing before the verb.", best)
                return _known("Пропущено отрицание «δεν», и смысл стал противоположным." if ru else
                              "Missing «δεν» changes the sentence into an affirmative.", best)

    if "δεν" in selected and "δεν" not in expected:
        remaining = list(selected)
        remaining.remove("δεν")
        if remaining == expected:
            return _known("Лишнее отрицание «δεν» меняет смысл фразы." if ru else
                          "Extra «δεν» changes the sentence's meaning.", best)

    # A missing article or preposition must be an actual *insertion*, not a
    # substituted form (στην is not 'missing στη') or a nearby spelling error.
    if len(expected) == len(selected) + 1:
        for i, token in enumerate(expected):
            if token in _ARTICLES and expected[:i] + expected[i+1:] == selected:
                display = exemplar[i] if i < len(exemplar) else token
                return _known(
                    (f"Перед этим словом нужна форма «{display}» — проверь предлог и артикль."
                     if ru else f"The form «{display}» is needed here. Check preposition and article."),
                    best)

    return _unknown(best, lang)


def _known(explanation: str, closest: str) -> dict:
    return {"correct": False, "unverified": False, "explanation": explanation,
            "orthographyNote": None, "closest": closest}


def _unknown(closest: str, lang: str) -> dict:
    return {"correct": False, "unverified": True,
            "explanation": (
                "Этот вариант отличается от проверенных. Возможно, он допустим — не буду считать его грамматической ошибкой. Сравни с примером ниже."
                if lang == "ru" else
                "This wording differs from reviewed options. It might be valid; no grammar mistake will be recorded. Compare the example below."
            ),
            "orthographyNote": None, "closest": closest}
