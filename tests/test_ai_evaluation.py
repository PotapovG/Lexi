"""The evaluator must not turn synthetic or incomplete data into a go decision."""
import importlib.util
from pathlib import Path
import unittest

p=Path(__file__).resolve().parents[1]/"scripts/evaluate_ai_speech.py"
spec=importlib.util.spec_from_file_location("speech_eval",p)
ev=importlib.util.module_from_spec(spec);spec.loader.exec_module(ev)

class EvaluationTests(unittest.TestCase):
    def test_empty_manifest_is_pending(self):
        v=ev.evaluate({"schema":1,"samples":[]})
        self.assertEqual(v["status"],"awaiting_real_recordings")
        self.assertEqual(v["decisions"],{"A":"pending","B":"pending","C":"disabled_unvalidated"})
    def test_word_edit_distance_is_not_acoustic(self):
        self.assertEqual(ev.distance(ev.words("Πώς σε λένε;"),ev.words("πως σε λενε")),0)
        self.assertEqual(ev.distance(ev.words("Πώς σε λένε;"),ev.words("Πώς λένε;")),1)
    def test_synthetic_samples_cannot_satisfy_human_gate(self):
        samples=[]
        cats=sorted(ev.CATEGORIES)
        for i in range(48):
            samples.append({"id":str(i),"speaker":"speaker"+str(i%3),
                            "device":"ios_safari" if i%2 else "android_chrome",
                            "split":"control","category":cats[i%len(cats)],
                            "spoken":"καλημέρα","recognized":"καλημέρα",
                            "origin":"synthetic","consent":True,"referenceReviewed":True,
                            "falseCorrection":False,"abstained":True,
                            "latencySeconds":1,"costUsd":None})
        v=ev.evaluate({"schema":1,"modelSnapshot":"test","rubricVersion":"test","samples":samples})
        self.assertEqual(v["status"],"blocked")
        self.assertEqual(v["decisions"]["A"],"pending")
        self.assertEqual(v["unknownCostCount"],48)
        self.assertNotIn("καλημέρα",str(v))
        self.assertNotIn("speaker0",str(v))
    def test_reused_sample_cannot_inflate_coverage(self):
        sample={"id":"same"}
        with self.assertRaises(ValueError):
            ev.evaluate({"schema":1,"samples":[sample,sample]})

if __name__=="__main__":
    unittest.main(verbosity=2)
