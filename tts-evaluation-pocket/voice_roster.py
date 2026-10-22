"""Approved no-cost Greek listening voice roster, 2026-10-20.

One local CPU TTS engine only. No Meta MMS, microphone, speech scoring,
public runtime inference or billed service. Synthetic voices require
short-card quality validation before ALPHA listening can be re-enabled.
"""
VOICE_IDS=("athina","eleni","katerina","kostas","spyros","nikos")
FEMALE=VOICE_IDS[:3]
MALE=VOICE_IDS[3:]
STYLE_PRESETS={
    "clear":dict(temperature=.3,sampler_decode_steps=5,pause_between_sentences_s=.22),
    "lively":dict(temperature=.6,sampler_decode_steps=5,pause_between_sentences_s=.22),
}
assert len(VOICE_IDS)==len(set(VOICE_IDS))==6
