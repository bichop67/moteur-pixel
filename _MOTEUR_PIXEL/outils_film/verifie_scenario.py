"""Vérifie qu'un scénario pNN.txt contient, pour chaque voix, exactement les répliques du fichier voix (blocs_e14.json),
dans le même ordre et mot pour mot (balises v4, *mots en jaune* et {annotations} ignorés) :
python verifie_scenario.py p03.txt"""
import io
import json
import os
import re
import sys
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))
SCEN = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL\scenarios\film\ep14"


def propre(t):
    t = re.sub(r"\{[^}]*\}", " ", t)
    t = re.sub(r"\[[^\]]*\]", " ", t)
    t = t.replace("*", "").replace("ﷺ", ", que la paix et le salut d'Allah soient sur lui,")
    t = re.sub(r"\s*([,;:!?.…«»])\s*", r" ", t)
    t = re.sub(r"(\s,)+", " ,", t)
    t = unicodedata.normalize("NFC", t)
    return re.sub(r"\s+", " ", t).strip()


fn = sys.argv[1]
path = fn if os.path.isabs(fn) else os.path.join(SCEN, fn)
code = None
lignes = {}
for raw in io.open(path, encoding="utf-8-sig"):
    s = raw.strip()
    if s.startswith("CODE:"):
        code = s.split(":", 1)[1].strip()
    m = re.match(r"^([A-Z_0-9]+)\s*(\([^)]*\))?\s*:\s*(.+)$", s)
    if m and m.group(1) not in ("TITRE", "CODE", "THEME", "FORMAT", "MUSIQUE", "VOIX", "PERSONNAGES", "QUEUE", "DUREE_FIN"):
        lignes.setdefault(m.group(1), []).append(propre(m.group(3)))
blocs = json.load(io.open(os.path.join(ICI, "blocs_e14.json"), encoding="utf-8"))
ok = True
for b in blocs:
    if not b["fichier"].startswith(code + "_"):
        continue
    qui = b["fichier"][len(code) + 1:-4]
    attendu = [propre(x) for x in b["texte"].split("\n\n") if x.strip()]
    trouve = lignes.get(qui, [])
    if len(attendu) != len(trouve):
        ok = False
        print(f"{qui} : {len(trouve)} réplique(s) dans le scénario, {len(attendu)} dans la voix")
    for i, (a, t) in enumerate(zip(attendu, trouve)):
        if a != t:
            ok = False
            print(f"{qui} n°{i + 1} différente :\n  voix     : {a}\n  scénario : {t}")
for qui in lignes:
    if not any(b["fichier"] == f"{code}_{qui}.mp3" for b in blocs):
        ok = False
        print(f"{qui} : aucune voix {code}_{qui}.mp3")
print("OK : répliques identiques aux voix" if ok else "À CORRIGER")
