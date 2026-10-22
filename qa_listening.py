"""Offline listening full release regression: Pocket 6-voice only.

Older Piper-specific QA is retained as qa_listening_legacy_piper.py for
historical debugging but must not be run against the new course.
"""
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
for script in ("qa_pocket_media_audit.py","qa_pocket_curriculum.py"):
 subprocess.run([sys.executable,str(root/script)],check=True,timeout=90)
print("PASS current Pocket listening suite (not deprecated Piper)")
