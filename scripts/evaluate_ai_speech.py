#!/usr/bin/env python3
"""Aggregate a PRIVATE consented Greek speech evaluation; never calls a provider.

Input remains outside Git. Output contains counts/rates/cost only, no speaker
IDs, audio paths, transcripts or individual remarks. This cannot certify
pronunciation quality or replace an independent Greek-speaking reviewer.
"""
import argparse
import collections
import json
import math
from pathlib import Path
import re
import statistics
import unicodedata

CATEGORIES={"correct","reading_error","stress_shift","accepted_variant",
            "self_correction","silence","noise","cut_off"}
DEVICES={"ios_safari","android_chrome","desktop"}

def words(text):
    plain="".join(c for c in unicodedata.normalize("NFD",text.casefold())
                  if not unicodedata.combining(c))
    return re.findall(r"[^\W\d_]+",plain,re.UNICODE)

def distance(reference,recognized):
    before=list(range(len(recognized)+1))
    for i,left in enumerate(reference,1):
        after=[i]
        for j,right in enumerate(recognized,1):
            after.append(min(after[-1]+1,before[j]+1,before[j-1]+(left!=right)))
        before=after
    return before[-1]

def number(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value) and value>=0

def evaluate(manifest):
    if manifest.get("schema")!=1 or not isinstance(manifest.get("samples"),list):
        raise ValueError("Expected schema 1 and samples array")
    samples=manifest["samples"]
    if not samples:
        return {"schema":1,"sampleCount":0,"status":"awaiting_real_recordings",
                "decisions":{"A":"pending","B":"pending","C":"disabled_unvalidated"},
                "blocking":["No consented human recordings evaluated"],"containsLearnerText":False}
    seen=set()
    for sample in samples:
        if not isinstance(sample,dict):
            raise ValueError("Every sample must be an object")
        sid=sample.get("id")
        if not isinstance(sid,str) or sid in seen:
            raise ValueError("Sample IDs must be unique strings")
        seen.add(sid)
        for field in ("speaker","device","split","category","spoken","recognized","origin"):
            if not isinstance(sample.get(field),str):
                raise ValueError("Missing string field: "+field)
        if sample["device"] not in DEVICES or sample["category"] not in CATEGORIES:
            raise ValueError("Unknown device/category")
        if sample["split"] not in ("tuning","control"):
            raise ValueError("Split must be tuning or control")
        for field in ("consent","referenceReviewed","falseCorrection","abstained"):
            if not isinstance(sample.get(field),bool):
                raise ValueError("Missing boolean field: "+field)
        for field in ("latencySeconds","costUsd"):
            if sample.get(field) is not None and not number(sample[field]):
                raise ValueError("Invalid numeric field: "+field)
    control=[s for s in samples if s["split"]=="control"]
    correct=[s for s in control if s["category"] in ("correct","accepted_variant")]
    unclear=[s for s in control if s["category"] in ("silence","noise","cut_off")]
    categories=collections.Counter(s["category"] for s in samples)
    devices=collections.Counter(s["device"] for s in samples)
    blocking=[]
    if len(samples)<40:
        blocking.append("At least 40 real recordings are required")
    if len(control)<20:
        blocking.append("At least 20 held-out control recordings are required")
    if len(correct)<10:
        blocking.append("At least 10 correct/accepted-variant control recordings are required")
    if len({s["speaker"] for s in samples})<3:
        blocking.append("At least three consenting speakers are required")
    if not all(s["origin"]=="human" and s["consent"] and s["referenceReviewed"] for s in samples):
        blocking.append("Every recording needs human origin, consent and independently reviewed reference")
    if not CATEGORIES<=set(categories):
        blocking.append("Required speech/error/uncertain-audio categories are missing")
    if not {"ios_safari","android_chrome"}<=set(devices):
        blocking.append("Both mobile browser families need real recordings")
    if not manifest.get("modelSnapshot") or not manifest.get("rubricVersion"):
        blocking.append("Actual model identifier and rubric version must be recorded")
    false_rate=sum(s["falseCorrection"] for s in correct)/len(correct) if correct else None
    if false_rate is None or false_rate>.05:
        blocking.append("False-correction target on correct control speech is not met")
    if not unclear or not all(s["abstained"] for s in unclear):
        blocking.append("Uncertain-audio abstention requires human review")
    references=sum(len(words(s["spoken"])) for s in control)
    errors=sum(distance(words(s["spoken"]),words(s["recognized"])) for s in control)
    latencies=sorted(s["latencySeconds"] for s in samples if number(s.get("latencySeconds")))
    costs=[s["costUsd"] for s in samples if number(s.get("costUsd"))]
    return {
        "schema":1,"sampleCount":len(samples),"controlCount":len(control),
        "categoryCounts":dict(sorted(categories.items())),"deviceCounts":dict(sorted(devices.items())),
        "normalizedWordErrorRate":errors/references if references else None,
        "wordErrorRateIsPronunciationScore":False,
        "correctControlCount":len(correct),"falseCorrectionRate":false_rate,
        "uncertainControlCount":len(unclear),
        "uncertainAbstentionRate":sum(s["abstained"] for s in unclear)/len(unclear) if unclear else None,
        "latencyP50Seconds":statistics.median(latencies) if latencies else None,
        "latencyP95Seconds":latencies[max(0,math.ceil(len(latencies)*.95)-1)] if latencies else None,
        "knownCostUsd":round(sum(costs),6),"unknownCostCount":len(samples)-len(costs),
        "status":"blocked" if blocking else "ready_for_independent_A_B_decision",
        "decisions":{"A":"pending","B":"pending","C":"disabled_unvalidated"},
        "blocking":blocking,"containsLearnerText":False,
        "limitations":["Small pilot, not validation for all accents or learners",
                       "A/B require separate signed human decisions; this script never enables a feature",
                       "No acoustic pronunciation assessment is implemented"]
    }

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest",type=Path)
    args=parser.parse_args()
    print(json.dumps(evaluate(json.loads(args.manifest.read_text(encoding="utf-8"))),
                     ensure_ascii=False,indent=2))
