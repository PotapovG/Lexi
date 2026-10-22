#!/usr/bin/env python3
"""Small six-language UI/API contract for learning upgrade, no student state."""
from pathlib import Path
import re
p=Path(__file__).resolve().parent
ui=(p/'app.js').read_text(encoding='utf-8')
html=(p/'index.html').read_text(encoding='utf-8')
server=(p/'server.py').read_text(encoding='utf-8')
engine=(p/'learning_upgrade.py').read_text(encoding='utf-8')
assert html.count('id="topic-mastery"')==1
assert html.count('id="grammar-mastery"')==1
assert html.count('id="vocab-topic-mastery"')==1
assert 'app.js?v=42' in html
for locale in ('ru','en','zh','ar','es','pt'):
    assert re.search(r'\b'+locale+r':\{topicEvidenceTitle:',ui),locale
    assert re.search(r'\b'+locale+r':\{alphabet:',ui),locale
    assert re.search(r'\b'+locale+r':\{vocabEvidenceTitle:',ui),locale
for tag in ('topic-mastery','grammar-mastery','vocab-topic-mastery',
            'capacityTaskNote','capacityEnough','capacityShort'):
    assert tag in ui,tag
for api in ('vocabTopics','learning_upgrade.knowledge_breakdown',
            'learning_upgrade.capacity_projection','learning_upgrade.selected_explanation'):
    assert api in server,api
assert 'db.execute' in engine and 'WHERE user_id=?' in engine
assert 'INSERT INTO' not in engine and 'UPDATE ' not in engine
print('PASS LEARNING UI CONTRACT: 3 map panels, six language translations, card-aware capacity, account-scoped readonly API')
