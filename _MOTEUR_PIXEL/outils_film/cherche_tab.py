"""Cherche des tabulations / retours chariot suspects dans les textes (chemin Windows abîmé : \t -> tabulation, \r -> retour)."""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BS = chr(92)
RACINES = [
    BS.join(["C:", "Users", "abdellah", ".claude", "skills"]),
    BS.join(["C:", "Users", "abdellah", ".claude", "projects", "C--WINDOWS-system32", "memory"]),
    BS.join(["C:", "Users", "abdellah", "Desktop", "VIDEO YOUTUBE", "_MOTEUR_PIXEL"]),
    BS.join(["C:", "Users", "abdellah", "Desktop", "VIDEO YOUTUBE", "FILM", "EPISODE 14"]),
]
EXT = (".md", ".txt", ".py")
# une tabulation collée entre deux lettres ou après un nom de dossier : « scenarios<TAB>est », « ia501<TAB>k »
TAB = re.compile(r"[A-Za-z0-9_)\]]\t[a-z]")
# un retour chariot seul (pas suivi d'un saut de ligne) au milieu d'une ligne
CR = re.compile(r"\r(?!\n)")
# un saut de ligne juste après un morceau de chemin : « …\_MOTEUR_PIXEL\scenarios » coupé en « …PIXEL » + « ouveau »
NL = re.compile(r"[A-Za-z0-9_]" + re.escape(BS) + r"?\n(?:ouveau|otes|ew|om_|ormal|um)")
for r in RACINES:
    for d, sous, fichiers in os.walk(r):
        sous[:] = [x for x in sous if x not in ("__pycache__", ".git")]
        for f in fichiers:
            if not f.lower().endswith(EXT):
                continue
            p = os.path.join(d, f)
            try:
                s = open(p, encoding="utf-8", errors="replace", newline="").read()
            except OSError:
                continue
            if len(s) > 5_000_000:
                continue
            for nom, rx in (("TAB", TAB), ("CR", CR), ("NL", NL)):
                for m in list(rx.finditer(s))[:3]:
                    a = max(0, m.start() - 50)
                    print(f"{nom} {p} : {s[a:m.end() + 30]!r}")
print("fin")
