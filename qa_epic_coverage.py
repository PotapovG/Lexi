"""Read-only source-based acceptance gates for epic #3.

Do not conflate full GitHub content, a green CI run and production state.
This QA checks catalog identity/locales/semantics WITHOUT touching live
accounts or a purchased book/PDF. Live GitOps and real-phone QA are external.
"""
from collections import Counter
from pathlib import Path

import server
import grammar2_cards as grammar
import mixed_review_cards as mixed
import phonetics_foundations as vowels
import consonant_patterns_cards as consonants
import advanced_syllables

ROOT=Path(__file__).resolve().parent
GROUP_COUNTS={
    "case":10,"agreement":10,"comparison":10,"past":10,"future":8,
    "subjunctive":8,"gender":20,"possessive":35,"verb_A":36,"verb_B1":36,
    "verb_B2":40,"likes":36,"schedule":42,"duration":38,"weather":30,
    "verb_core":48,"phonetic":40,"consonant":36,"review_scenario":50
}
BASE_GROUPS={"case","agreement","comparison","past","future","subjunctive"}
assert Counter(c["group"] for c in grammar.CARDS)==GROUP_COUNTS
assert len(grammar.CARDS)==543==len(server.GRAMMAR2_ALL)
assert sum(GROUP_COUNTS[g] for g in BASE_GROUPS)==56
assert sum(v for k,v in GROUP_COUNTS.items() if k not in BASE_GROUPS)==487
assert [c["id"] for c in grammar.CARDS]==[
    f"g2261021_{i:03d}" for i in range(1,544)
]
assert len(set(c["id"] for c in server.PRACTICE_ALL))==len(server.PRACTICE_ALL)
assert len(server.vocab.VOCAB)==1700
assert len(server.SYLLABLE_ALL)==35==len(advanced_syllables.CARDS)
assert server.CLOCK_COUNT==144
assert len([x for x in server.ALL if x["kind"]=="dialogue"])==112
assert not any(c["kind"] in ("review_scenario","consonant","phonetic")
               for c in server.PRACTICE_ALL)
assert len(mixed.SCENARIOS)==10 and len(mixed.CARDS)==50
assert len(vowels.CARDS)==40 and len(consonants.CARDS)==36
assert "grammar" in server.KINDS

# Six non-fallback authored target meanings and teaching hints are present
# for all cards from these groups. Locale presence != native proofreading.
LOCALES=("ru","en","zh","ar","es","pt")
NEW_TRANSLATED={
    "possessive","verb_A","verb_B1","verb_B2","likes","schedule",
    "duration","weather","verb_core","phonetic","consonant","review_scenario"
}
expanded=[c for c in grammar.CARDS if c["group"] in NEW_TRANSLATED]
assert len(expanded)==467,len(expanded)
for c in expanded:
    assert set(c["fullTranslations"])==set(LOCALES),c["id"]
    assert all(isinstance(c["fullTranslations"][l],str)
               and c["fullTranslations"][l].strip() for l in LOCALES),c["id"]
    assert all(isinstance(c[l],str) and c[l].strip() for l in LOCALES),c["id"]
    assert c["source"].startswith("independent_") and not c.get("book_page_verified"),c["id"]
    assert c["curriculum_ready_unit"]<=c["chapter"],c["id"]

# Existing Quick and Greek Life are different client surfaces: the new
# five-step review belongs to existing grammar_fill, never a new kind.
assert all(c["kind"]=="grammar" and c["group"]=="review_scenario"
           and c["chapter"]<=7 for c in mixed.CARDS)
assert all([c["scenarioStep"] for c in seq]==[1,2,3,4,5]
           for seq in mixed.SCENARIOS.values())
assert all(c["typedAnswer"] == bool(c.get("acceptedForms"))
           for c in mixed.CARDS)

# A real-device test cannot be inferred from responsive stylesheet metadata.
app=(ROOT/"app.js").read_text(encoding="utf-8")
html=(ROOT/"index.html").read_text(encoding="utf-8")
styles=(ROOT/"styles.css").read_text(encoding="utf-8")
selection=(ROOT/"mixed_review_selection.py").read_text(encoding="utf-8")
assert 'id="finish-skills"' in html
assert "sessionSkills:state.sessionSkills" in app and "renderSessionSkills();" in app
assert "@media (max-width: 360px)" in styles
assert 'if count<5:return [],ordinary' in selection
assert 'if not candidates:return [],ordinary' in selection
assert 'if row[0].get("group")!="review_scenario"' in (ROOT/"server.py").read_text(encoding="utf-8")

report=(ROOT/"docs/A1_1_7_ACCEPTANCE_20261113.md").read_text(encoding="utf-8")
assert "supplementalGrammar=56" in report
assert "543" in report and "1,700" in report
assert "SKIP: main is not protected" in report
assert "should remain OPEN" in report
assert "real-device" in report.lower() or "real 320px" in report.lower()

print("PASS epic #3: 56 baseline +487 additive =543 grammar cards, 35 old stress, 112 dialogues, 144 clocks")
print("PASS epic #3: 467 independently authored grammar forms have all six localized meanings/notes and gated curriculum")
print("PASS epic #3: 10 complete 5-step scenes, 320px CSS contract, strict partial-scene exclusion")
print("NOTE: CI does not assert native editorial review, a physical 320px device, actual Pocket WAV or production deployment")
