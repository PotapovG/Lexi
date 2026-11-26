"""Validate AI grounding and curriculum gates with the real existing catalog."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import server
import ai_curriculum as curriculum

class CurriculumTests(unittest.TestCase):
    def setUp(self):
        self.card=next(c for c in server.ALL if c["kind"]=="word" and c["chapter"]==1)
        self.snapshot={"runId":"synthetic-run","chapter":1,"sourceVersion":"source-fixture",
                       "rubricVersion":"rubric-fixture","evidenceComplete":True,
                       "evidence":[{"ordinal":0,"cardId":self.card["id"],"printedChapter":1,
                                    "skill":"word","question":{"prompt":self.card["gr"]},
                                    "selected":"synthetic wrong answer",
                                    "result":{"answer":self.card["en"],"correct":False},
                                    "assisted":None,"hintUsageKnown":False}]}
        self.context=curriculum.build(server,self.snapshot,"en")
    def value(self):
        return {"observation":{"text":"You practised a word.","evidenceIds":["e0"],"example":self.card["gr"]},
                "improvements":[{"text":"Review the shown meaning.","evidenceIds":["e0"],"example":self.card["en"]}],
                "nextStep":"Open existing review.","targetCardId":self.card["id"]}
    def test_examples_and_target_must_be_real_evidence(self):
        self.assertEqual(curriculum.validate_summary(self.value(),self.context)["targetCardId"],self.card["id"])
        cases=[("missing evidence",lambda v:v["observation"].update(evidenceIds=["invented"])),
               ("invented example",lambda v:v["observation"].update(example="not present in any answer")),
               ("unknown target",lambda v:v.update(targetCardId="new-ai-card")),
               ("third improvement",lambda v:v.update(improvements=v["improvements"]*3)),
               ("long advice",lambda v:v.update(nextStep="x"*401))]
        for name,mutate in cases:
            with self.subTest(name=name):
                value=self.value();mutate(value)
                with self.assertRaises(ValueError):curriculum.validate_summary(value,self.context)
    def test_correct_skipped_unverified_are_not_negative_evidence(self):
        for flag in ("correct","skipped","unverified"):
            context=copy.deepcopy(self.context);context["evidence"][0][flag]=True
            with self.subTest(flag=flag):
                with self.assertRaisesRegex(ValueError,"unsupported_correction"):
                    curriculum.validate_summary(self.value(),context)
    def test_changed_answers_change_context_and_unknown_hints_stay_unknown(self):
        second=copy.deepcopy(self.snapshot);second["evidence"][0]["selected"]="another answer"
        different=curriculum.build(server,second,"en")
        self.assertNotEqual(self.context["hash"],different["hash"])
        self.assertIsNone(self.context["evidence"][0]["assisted"])
        self.assertFalse(self.context["evidence"][0]["hintUsageKnown"])
        second["evidenceComplete"]=False
        self.assertFalse(curriculum.build(server,second,"en")["evidenceComplete"])
    def test_real_pilot_materials_never_exceed_chapter_or_grammar_gate(self):
        for chapter in (1,2,3,4,5,7,20):
            snapshot=dict(self.snapshot,chapter=chapter)
            context=curriculum.build(server,snapshot,"ru")
            for material in context["readings"]:
                card=server.book_or_audio_card(material["sourceId"])
                self.assertLessEqual(card["chapter"],chapter)
                self.assertLessEqual(server._grammar_guard.milestone(card),chapter)
                self.assertNotIn("[[",material["text"])
                self.assertTrue(material["sourceVersion"])
                if chapter==5:self.assertLessEqual(card["chapter"],4)
            self.assertFalse(context["claims"]["pronunciationValidated"])
            self.assertFalse(context["claims"]["textbookVocabularyFullyVerified"])
    def test_model_cannot_supply_future_question_or_sixth_turn(self):
        context=curriculum.build(server,dict(self.snapshot,chapter=7),"en")
        remaining={q["id"]:q for q in context["questions"]}
        self.assertGreaterEqual(len(remaining),5)
        valid={"understood":True,"reply":"Ευχαριστώ.","correction":"","explanation":"",
               "nextQuestionId":next(iter(remaining)),"finalNote":""}
        with self.assertRaisesRegex(ValueError,"invalid_next_question"):
            curriculum.validate_dialogue(dict(valid,nextQuestionId="outside-scope"),context,remaining)
        with self.assertRaisesRegex(ValueError,"extra_turn"):
            curriculum.validate_dialogue(valid,context,remaining,True)
        answer=curriculum.validate_dialogue(dict(valid,nextQuestionId="",reply="Πώς σε λένε;"),context,remaining,True)
        self.assertNotIn(";",answer["reply"])
    def test_unsupported_model_greek_is_removed_without_penalizing_learner(self):
        context=self.context
        value={"understood":True,"reply":"Θα εξερευνήσουμε το σύμπαν.",
               "correction":"Θα πάω αύριο.","explanation":"Unsupported future tense.",
               "nextQuestionId":"","finalNote":""}
        result=curriculum.validate_dialogue(value,context,{},True)
        self.assertTrue(result["understood"])
        self.assertEqual(result["correction"],"")
        self.assertEqual(result["explanation"],"")
        self.assertEqual(result["reply"],curriculum.SAFE_REPLIES[0])
    def test_locale_validation_and_schema_enums(self):
        for lang in ("ru","en","zh","ar","es","pt"):
            context=curriculum.build(server,self.snapshot,lang)
            self.assertEqual(context["interfaceLanguage"],lang)
        with self.assertRaises(ValueError):curriculum.build(server,self.snapshot,"de")
        schema=curriculum.summary_schema(self.context)
        self.assertEqual(schema["properties"]["observation"]["properties"]["evidenceIds"]["items"]["enum"],["e0"])
        self.assertIn(self.card["id"],schema["properties"]["targetCardId"]["enum"])

if __name__=="__main__":
    unittest.main(verbosity=2)
