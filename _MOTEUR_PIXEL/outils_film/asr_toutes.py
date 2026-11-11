"""Transcrit (mots horodatés) les voix des parties 3 à 24 du film Moussa : asr_E14Pn.json dans le dossier voix."""
import io
import json
import os
import sys

MOTEUR = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
sys.path.insert(0, MOTEUR)
import voix  # noqa: E402

D = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\FILM\EPISODE 14\voix"
blocs = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "blocs_e14.json"), encoding="utf-8"))
parts = {}
for b in blocs:
    code = b["fichier"].split("_")[0]
    qui = b["fichier"][len(code) + 1:-4]
    parts.setdefault(code, []).append(qui)
for code, qui in parts.items():
    n = int(code[4:])
    if n < 3 or os.path.exists(os.path.join(D, f"asr_{code}.json")):
        continue
    print("==", code, qui, flush=True)
    voix.transcrire(D, code, qui)
print("fini", flush=True)
