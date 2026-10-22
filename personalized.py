"""Per-account learned vocabulary composition. Never exposes unstudied words as questions."""
import vocab_lessons as vocab
import pedagogy_rules as _pedagogy

def progress_summary(db,uid):
    rows=db.execute("SELECT word_id,attempts,correct,miss_debt FROM vocab_progress WHERE user_id=?",(uid,)).fetchall()
    valid={w["id"] for w in vocab.VOCAB}
    learned=[r for r in rows if r["word_id"] in valid and r["correct"]>=1 and r["miss_debt"]==0]
    return {"introduced":sum(r["word_id"] in valid and r["attempts"]>0 for r in rows),
            "learned":len(learned),
            "needsReview":sum(r["word_id"] in valid and r["miss_debt"]>0 for r in rows),
            "available":len(valid)}

def is_learned(db,uid,word_id):
    row=db.execute("SELECT correct,miss_debt FROM vocab_progress WHERE user_id=? AND word_id=?",(uid,word_id)).fetchone()
    return bool(row and row["correct"]>=1 and row["miss_debt"]==0)

def to_card(word):
    # Original course ID is retained in prefix; verified per user before marking.
    return dict(id="personal_"+word["id"],semanticId=_pedagogy.semantic_id(word),
                kind="word",gr=word["gr"],en=word["en"],ru=word["ru"],
                ar=vocab.visible_translation(word,"ar")[0],
                es=vocab.visible_translation(word,"es")[0],
                pt=vocab.visible_translation(word,"pt")[0],
                zh=vocab.visible_translation(word,"zh")[0],
                chapter=-10,unit=-10,page=0,topic=(word.get("topics") or ["everyday"])[0],
                source="personalized",curriculum="personalized")

def learned_cards(db,uid):
    entries=db.execute("SELECT word_id FROM vocab_progress WHERE user_id=? AND correct>=1 AND miss_debt=0",(uid,)).fetchall()
    return [to_card(vocab.VOCAB_BY_ID[row["word_id"]]) for row in entries
            if row["word_id"] in vocab.VOCAB_BY_ID]
