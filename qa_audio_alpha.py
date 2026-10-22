from pathlib import Path
import tempfile
import server
if server.LISTENING_ENABLED:
 print("SKIP: old ALPHA rollback regression; listening is now enabled and covered by qa_listening.py")
 raise SystemExit(0)
assert server.LISTENING_ENABLED is False
assert len(server.ALL)==1795 and len(server.vocab.VOCAB)==1700
with tempfile.TemporaryDirectory() as folder:
 server.DB=str(Path(folder)/'app.sqlite3');server.init_db()
 try:server.make_quiz('user',{'scope':['listening'],'chapters':['1,2,3,4']})
 except ValueError as e:assert str(e)=='listening_alpha_disabled'
 else:raise AssertionError('disabled listening quiz still available')
 assert server.estimate_capacity('user',{'scope':['listening'],'chapters':['1,2,3,4']})['uniqueCards']==0
 cid=server.LISTEN_CARDS[0]['id'] if server.LISTEN_CARDS else None
 try:server.mark('user',{'id':cid,'direction':'listen','lang':'ru','selected':'wrong'})
 except ValueError as e:assert str(e) in ('listening_alpha_disabled','invalid answer')
 else:raise AssertionError('disabled listening answers still accepted')
 assert server.stats('user')['attempts']==0
 assert server.make_quiz('user',{'scope':['chapters'],'chapters':['1,2,3,4']})['questions']
print('PASS ALPHA server disabled quiz, capacity, marking and old audio; normal lesson unaffected')
