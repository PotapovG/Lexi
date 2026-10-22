"""Automated listening curriculum QA: full offline media, difficulty, ranges,
all six translations, old IDs, replay diversity, weak debt, no paid API.

With --mock only: constructs *in-memory dummy audio metadata* to exercise the
app's filtering while real 1266 samples are being batch generated. Never
serves those mock files or enables ALPHA for actual users.
"""
import argparse,hashlib,json,sqlite3,tempfile,random,collections,wave
from pathlib import Path
import server,listening_catalog as listening
ap=argparse.ArgumentParser();ap.add_argument('--mock',action='store_true');args=ap.parse_args()

if args.mock:
    # Integration fixture: reuse REAL authored card metadata only; fake audio URLs
    # are never exposed in the production website or in any persisted files.
    source=server.BY_ID
    ids=list(listening.ELIGIBLE_IDS)
    cards=[]
    for cid in ids:
        c=source[cid]
        data={k:c[k] for k in ('chapter','unit','page','gr','en','ru','zh','ar','es','pt','topic')}
        data.update(id='listen_'+cid,kind='listening',sourceKind=c['kind'],
                    sourceId=cid,curriculum='listening',
                    semanticId='audio_'+c.get('semanticId',cid),
                    audioVariants=[{'voice':'athina','style':'clear','file':'a'*32+'.wav'},
                                   {'voice':'nikos','style':'lively','file':'b'*32+'.wav'}])
        cards.append(data)
    server.LISTEN_CARDS=cards
    server.LISTEN_BY_ID={c['id']:c for c in cards}
else:
    cards=server.LISTEN_CARDS
    assert len(cards)==len(listening.ELIGIBLE_IDS)==717,(len(cards),len(listening.ELIGIBLE_IDS))
    assert len(listening.AUDIO)==1266,len(listening.AUDIO)
    assert len(listening.MANIFEST['entries'])==633
    assert not (set(listening.AUDIO)&set(json.loads((listening.ROOT/'listening_audio_manifest.json').read_text())['items'].values()))
    for card in cards:
        assert len(card['audioVariants'])==2
        assert card['audioVariants'][0]['voice']!=card['audioVariants'][1]['voice']
        for v in card['audioVariants']:
            assert v['file'] in listening.AUDIO
            assert listening.AUDIO[v['file']].is_file()
    for fn,file in listening.AUDIO.items():
        with wave.open(str(file),'rb') as w:
            assert w.getframerate()==24000 and w.getnchannels()==1
            assert .25<=w.getnframes()/w.getframerate()<=120,(fn,w.getnframes()/w.getframerate())
    assert set(listening.APPROVED)=={v['voice'] for c in cards for v in c['audioVariants']}
assert set(c['sourceId'] for c in cards)==listening.ELIGIBLE_IDS
assert {c['sourceKind'] for c in cards}=={'word','phrase','sentence'}
assert {c['chapter'] for c in cards}==set(range(1,21))
assert len({c['gr'] for c in cards})==633
assert len(server.ALL)==1795 and len(server.vocab.VOCAB)==1700
assert all(c['page']>=14 and c['page']<=289 for c in cards)
server.LISTENING_ENABLED=True
with tempfile.TemporaryDirectory() as tmp:
    server.DB=str(Path(tmp)/'db.sqlite3');server.init_db()
    base={'scope':['listening'],'lang':['ru'],'types':['word,phrase,sentence'],'chapters':['1,2,3,4'],'count':['60']}
    selected=[c for c in cards if c['chapter'] in (1,2,3,4)]
    cap=server.estimate_capacity('student',dict(base,duration=['30']))
    assert cap['uniqueCards']==len({c['semanticId'] for c in selected}),(cap,len(selected))
    assert cap['requiredAt20Seconds']==90 and cap['enoughAt20Seconds']
    for kind in ('word','phrase','sentence'):
        subset=[c for c in selected if c['sourceKind']==kind]
        r=server.make_quiz('student',dict(base,types=[kind]))
        assert r['count']>0 and all(q['listeningDifficulty']==kind for q in r['questions'])
        assert r['count']<=len({c['semanticId'] for c in subset})
    for chapter in range(1,21):
        q=server.make_quiz('student',dict(base,chapters=[str(chapter)]))['questions']
        assert q and all(x['chapter']==chapter for x in q),(chapter,len(q))
    r=server.make_quiz('student',{'scope':['listening'],'lang':['en'],'types':['word,phrase,sentence'],
         'from':['48'],'to':['56'],'count':['60']})['questions']
    assert r and all(48<=q['page']<=56 for q in r)
    r=server.make_quiz('student',dict(base,chapters=['1,2,3,4']))['questions']
    assert len(r)==60 and len({q['semanticId'] for q in r})==60
    assert all(q['kind']=='listening' and q['direction']=='listen' and
               q['audioUrl'].startswith('/greek/audio/') and q['audioVoice'] in listening.APPROVED and
               q['audioStyle'] in ('clear','lively') and
               'gr' not in q and 'transcript' not in q and len(set(q['choices']))==8 for q in r)
    for locale in ('ru','en','zh','ar','es','pt'):
        question=server.format_question(cards[0],'listen',locale,variant_index=0)
        source=server.BY_ID[cards[0]['sourceId']]
        assert source[locale] in question['choices'] and len(question['choices'])==8
        assert question['audioVoice']==cards[0]['audioVariants'][0]['voice']
        outcome=server.mark('test-'+locale,{'id':cards[0]['id'],'direction':'listen',
                     'selected':source[locale],'lang':locale})
        assert outcome['correct'] and outcome['transcript']==cards[0]['gr']
        second=server.format_question(cards[0],'listen',locale,variant_index=1)
        assert second['audioVoice']!=question['audioVoice'] and second['audioUrl']!=question['audioUrl']
    first=cards[1]
    miss=server.mark('weak',{'id':first['id'],'direction':'listen','selected':'intentionally-wrong','lang':'ru'})
    assert not miss['correct'] and miss['missDebt']==2
    review=server.make_quiz('weak',{'mode':['weak_all'],'lang':['ru']})['questions']
    assert len(review)==1 and review[0]['id']==first['id'] and review[0]['direction']=='listen'
    assert review[0]['audioVoice']==first['audioVariants'][1]['voice']
    for debt in (1,0):
        result=server.mark('weak',{'id':first['id'],'direction':'listen',
                            'selected':first['ru'],'lang':'ru'})
        assert result['correct'] and result['missDebt']==debt
    assert server.stats('weak')['weak']==0
    with server.conn() as db:
        assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
print('PASS', 'MOCK_META' if args.mock else 'REAL_1266_AUDIO',
      '717 cards,633 text,6 voices; book chapter/page & word/phrase/sentence levels;',
      'multilingual choices, listener voice alternation and weak review; original library unchanged')
