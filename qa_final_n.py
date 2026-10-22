"""Final ν pedagogical acceptance, scoped to school-spelling variants.

Examines real article cards, both variants in six locales, no false miss debt,
and *strict* exclusion before a vowel or where gender/case changes.
All persistence uses a throwaway SQLite DB.
"""
from pathlib import Path
import sqlite3,tempfile
import server
import form_exercises
import final_n_guidance

with tempfile.TemporaryDirectory() as td:
    server.DB=str(Path(td)/'qa.sqlite3');server.init_db()
    variants={'article_001':('στη','στην','Λευκωσία'),
              'article_014':('τη','την','Μαρία'),
              'article_017':('τη','την','λέξη'),
              'article_020':('τη','την','φίλη'),
              'article_023':('τη','την','ζάχαρη')}
    assert {c['id'] for c in form_exercises.ARTICLES if len(c['acceptedForms'])==2}==set(variants)
    for lang in ('ru','en','zh','ar','es','pt'):
      for cid,(expected,retained,noun) in variants.items():
        c=server.BY_ID[cid]
        assert c['correct']==expected and retained in c['acceptedForms']
        assert noun in c['prompt']
        q=server.format_question(c,'fill',lang)
        assert q.get('articleSpellingVariant') is True and 'multipleValid' not in q
        assert set(c['acceptedForms'])<=set(q['choices'])
        assert len(q['choices'])==len(set(q['choices']))==8
        good=server.mark('new-'+lang+'-'+cid,dict(id=cid,direction='fill',lang=lang,selected=retained))
        assert good['correct'] and good['missDebt']==0,good
        assert good['acceptedVariant'] is True
        assert good['preferredAnswer']==expected
        assert good['acceptedAnswers']==[expected,retained]
        assert expected+' '+noun in good['spellingNote']
        assert '-ν' in good['spellingNote']
        valid=server.mark('new-'+lang+'-'+cid,dict(id=cid,direction='fill',lang=lang,selected=expected))
        assert valid['correct'] and valid['missDebt']==0
    # The soft rule is contextual, NOT "always accept τη and την."
    strict={'article_002':('στην','στη'),   # Αθήνα — vowel
            'article_005':('στην','στη'),  # Κύπρο — κ
            'article_015':('την','τη'),   # Άννα — vowel
            'article_022':('την','τη'),   # εφημερίδα — vowel
            'article_013':('τον','το'),   # male accusative
            'article_018':('το','τον'),   # neuter
            'article_016':('τον','την'),  # masculine
            'article_011':('το','τον'),}  # neuter nominative
    for cid,(canonical,wrong) in strict.items():
      card=server.BY_ID[cid]
      assert card['correct']==canonical and card['acceptedForms']==[canonical],cid
      assert server.format_question(card,'fill','ru').get('articleSpellingVariant') is None
      result=server.mark('strict-'+cid,dict(id=cid,direction='fill',lang='ru',selected=wrong))
      assert not result['correct'] and result['missDebt']==2,(cid,result)
      assert result.get('spellingNote') is None and result['acceptedAnswers']==[canonical]
      repeat=server.mark('strict-'+cid,dict(id=cid,direction='fill',lang='ru',selected=canonical))
      assert repeat['correct'] and repeat['missDebt']==1
    # Existing missed answer heals the usual way; accepting variant reduces
    # existing debt instead of adding a new wrong attempt. No historic deletion.
    cid='article_014'
    first=server.mark('existing-user',dict(id=cid,direction='fill',lang='ru',selected='το'))
    assert not first['correct'] and first['missDebt']==2
    second=server.mark('existing-user',dict(id=cid,direction='fill',lang='ru',selected='την'))
    assert second['correct'] and second['missDebt']==1
    third=server.mark('existing-user',dict(id=cid,direction='fill',lang='ru',selected='τη'))
    assert third['correct'] and third['missDebt']==0
    with server.conn() as db:
      assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
      assert db.execute('select count(*) from attempts where user_id=? and correct=0',('new-ru-article_014',)).fetchone()[0]==0
print('PASS 5 scoped feminine variants * 6 locales, accepted as correct with no debt and orthographic note')
print('PASS strict Άννα/Κύπρο/εφημερίδα/masculine/neuter remain wrong, no incorrect equivalences')
print('PASS prior weak debt clears on soft-accepted final -ν without deleting history')
