"""Finite curator-reviewed semantic-preserving Greek sentence-order alternatives.

Do not grade arbitrary anagrams as Greek grammar. Case/punctuation ignored
only when comparing a complete sentence against this explicit allowlist;
diacritics and word forms remain significant.
"""
import collections
import re
import unicodedata

VARIANTS={
 'order_patk02_001':['Η Μαρία στην οδό Κύπρου μένει και ο Αντρέας μένει στην οδό Αθηνάς.'],
 'order_patk02_003':['Εγώ μένω στη Λευκωσία, αλλά στην Πάφο μένει η φίλη μου.'],
 'order_patk02_005':['Η Άννα και ο Νίκος στην Αθήνα μένουν και έχουν κινητά.'],
 'order_patk02_006':['Η Άννα έχει τηλέφωνο, αλλά δεν έχω εγώ.'],
 'order_patk03_001':['Αυτή είναι η οικογένειά μου: η μητέρα μου, ο πατέρας μου και η αδελφή μου.'],
 'order_patk03_003':['Ο Γιώργος είναι οδηγός και η γυναίκα του δασκάλα είναι.'],
 'order_patk03_005':['Ο φίλος μου έχει δύο παιδιά, μία κόρη και έναν γιο.'],
 'order_patk03_006':['Ο αδελφός μου δουλεύει σε σχολείο και μένει στην Ελλάδα.'],
 'order_patk04_001':['Ο φίλος μου μιλάει καλά ελληνικά, αλλά είναι Γερμανός.'],
 'order_patk04_003':['Η Άννα μιλάει γαλλικά και ελληνικά, αλλά δεν μιλάει ρωσικά.'],
 'order_patk04_005':['Ο αδελφός μου μιλάει μόνο αγγλικά, αλλά καταλαβαίνει ελληνικά.'],
 'order_patk09_017':['Αυτό το φόρεμα είναι ακριβό, αλλά είναι φτηνό εκείνο.'],
 'order_patk12_001':['Χθες με το τρένο πήγαμε στην Πάτρα.'],
 'order_patk14_004':['Αύριο με δύο φίλους θα πάμε στην ταβέρνα.'],
 'or261021_x05s002':['Κοντά στην πλατεία είναι ο σταθμός, αλλά το σχολείο είναι μακριά.'],
 'or261021_x06s001':['Το πρωί τη Δευτέρα δουλεύω, αλλά την Κυριακή κοιμάμαι πολύ.'],
 'or261021_x06s002':['Κάθε βράδυ η Μαρία διαβάζει και το Σάββατο πηγαίνει στο κέντρο.'],
 'or261021_x07s001':['Δέκα ευρώ κάνει το βιβλίο και τρία ευρώ κάνει το τετράδιο.'],
 'or261021_x08s001':['Από το σούπερ μάρκετ σήμερα αγοράζω ψωμί, τυρί και ντομάτες.'],
 'or261021_x10s001':['Αύριο με το αεροπλάνο ταξιδεύω στην Αθήνα και μένω σε ξενοδοχείο.'],
 'or261021_x11s001':['Στη Λευκωσία γεννήθηκα, αλλά στην Αθήνα έζησα πολλά χρόνια.'],
 'or261021_x14s001':['Σε μια εταιρεία δουλεύω, γράφω μηνύματα και μιλάω με τους πελάτες.'],
 'or261021_sx261021_002':['Γιατρός είναι ο αδελφός μου και η αδελφή μου είναι δασκάλα.'],
 'or261021_sx261021_005':['Το πρωί τη Δευτέρα δουλεύω, αλλά την Τρίτη έχω μάθημα ελληνικών.'],
 'or261021_sx261021_007':['Ένα παράθυρο και δύο καρέκλες έχει το μικρό δωμάτιο.'],
 'or261021_sx261021_011':['Χθες στο μουσείο πήγα και μετά ήπια καφέ με έναν φίλο μου.'],
 'or261021_sx261021_017':['Αν έχεις πονοκέφαλο, με τον γιατρό πρέπει να μιλήσεις.'],
 'or261021_patk12_002':['Έναν παλιό φίλο είδα την περασμένη εβδομάδα.'],
 'or261021_patk12_004':['Προχτές αργά ξύπνησα και έφυγα το μεσημέρι.'],
 'or261021_patk14_005':['Πρώτα θα φάμε σαλάτα και μετά ψάρι.'],
 'or261021_patk18_001':['Πήγαινε στον γιατρό αν έχεις πυρετό.'],
 'or261021_patk18_003':['Πάρε τηλέφωνο τον γιατρό αν νιώθεις χειρότερα.'],
 'or261021_patk16_002':['Σήμερα προτιμώ να μείνω στο σπίτι και να διαβάσω.'],
}
def words(s):
    return re.findall(r'[\w\u0370-\u03ff\u1f00-\u1fff]+',unicodedata.normalize('NFC',s.casefold()),re.UNICODE)
def normalized(s):
    return ' '.join(words(s))

# The learner selects words, not typographical variants of the same word.
# Punctuation belongs to the finished sentence; apostrophes inside a word
# are retained. Existing card.tokens and user progress keys remain untouched.
CHOICE_EDGE_PUNCT = '.,!?;:··…«»“”()'
def choice_token(token):
    return token.strip(CHOICE_EDGE_PUNCT)

def formatted(card, selected):
    # For a completed grammatical variant, restore that variant's punctuation,
    # not necessarily the original author's word order.
    normal = normalized(selected)
    for text in all_valid(card):
        if normalized(text) == normal:
            return text
    return card['gr']

def matches(card,selected):
    if normalized(selected)==normalized(card['gr']):
        return True
    return normalized(selected) in {normalized(v) for v in VARIANTS.get(card['id'],())}
def all_valid(card):
    return [card['gr']]+VARIANTS.get(card['id'],[])
def validate(by_id):
    for cid,variants in VARIANTS.items():
        card=by_id[cid]
        assert card['kind']=='order'
        originals=collections.Counter(words(card['gr']))
        assert len(variants)==len({normalized(v) for v in variants}),cid
        for variant in variants:
            assert collections.Counter(words(variant))==originals,(cid,variant)
            assert normalized(variant)!=normalized(card['gr'])
    return len(VARIANTS)
