"""Cherche des caractères de contrôle (BEL, BS, VT, FF) dans les fichiers texte : signe d'un chemin Windows abîmé (\a \b \v \f)."""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BS = chr(92)
RACINES = [
    BS.join(["C:", "Users", "abdellah", ".claude", "skills"]),
    BS.join(["C:", "Users", "abdellah", ".claude", "projects", "C--WINDOWS-system32", "memory"]),
    BS.join(["C:", "Users", "abdellah", "Desktop", "VIDEO YOUTUBE", "_MOTEUR_PIXEL"]),
    BS.join(["C:", "Users", "abdellah", "Desktop", "VIDEO YOUTUBE", "FILM", "EPISODE 14"]),
]
EXT = (".py", ".txt", ".md", ".json")
MAUVAIS = {7: "BEL (\\a)", 8: "BS (\\b)", 11: "VT (\\v)", 12: "FF (\\f)"}
trouves = 0
for r in RACINES:
    for d, sous, fichiers in os.walk(r):
        sous[:] = [x for x in sous if x not in ("__pycache__", ".git", "cache", "_cache")]
        for f in fichiers:
            if not f.lower().endswith(EXT):
                continue
            p = os.path.join(d, f)
            try:
                b = open(p, "rb").read()
            except OSError:
                continue
            if len(b) > 20_000_000:
                continue
            for code, nom in MAUVAIS.items():
                i = b.find(bytes([code]))
                if i >= 0:
                    trouves += 1
                    extrait = b[max(0, i - 40):i + 30].decode("utf-8", "replace").replace(chr(code), "<" + nom + ">")
                    print(f"{p} : {nom} x{b.count(bytes([code]))} … {extrait!r}")
print("fichiers touchés :", trouves)
