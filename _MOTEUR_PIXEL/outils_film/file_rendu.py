# File de rendu du film (version conte) : une partie à la fois, dans l'ordre de file_rendu_ordre.json.
#  - attend la planche de la partie (planches_conte.py) et qu'elle ait au moins 6 min (le temps de la regarder),
#    sauf si planches/pNN.ok existe ; parties 1 et 15 (déjà validées) : pas d'attente ;
#  - fichier PAUSE dans ce dossier : la file attend avant la partie suivante ;
#  - une partie dont le scénario a changé depuis son rendu est refaite ;
#  - après chaque rendu réussi : dossier d'images temporaires supprimé (4 Go) ;
#  - attend s'il reste moins de 9 Go sur le disque.
import json
import os
import re
import shutil
import subprocess
import sys
import time

MOTEUR = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
SC = os.path.join(MOTEUR, "scenarios", "film", "ep14_conte")
SCR = os.path.dirname(os.path.abspath(__file__))
PL = os.path.join(SCR, "planches")
ETAT = os.path.join(SCR, "file_rendu_etat.json")
LOG = os.path.join(SCR, "file_rendu.log")


def log(m):
    m = time.strftime("%H:%M:%S ") + m
    print(m, flush=True)
    open(LOG, "a", encoding="utf-8").write(m + "\n")


def titre(num):
    for line in open(os.path.join(SC, f"p{num:02d}.txt"), encoding="utf-8"):
        if line.startswith("TITRE:"):
            return line.split(":", 1)[1].strip()


def suivante(etat):
    for num in json.load(open(os.path.join(SCR, "file_rendu_ordre.json"), encoding="utf-8")):
        e = etat.get(str(num))
        if not e or e["mtime"] != os.path.getmtime(os.path.join(SC, f"p{num:02d}.txt")):
            return num
    return None


etat = json.load(open(ETAT, encoding="utf-8")) if os.path.exists(ETAT) else {}
log("file de rendu : début")
while True:
    if os.path.exists(os.path.join(SCR, "PAUSE")):
        time.sleep(30)
        continue
    num = suivante(etat)
    if num is None:
        break
    if num not in (1, 15):
        p = os.path.join(PL, f"p{num:02d}_1.png")
        scen_m = os.path.getmtime(os.path.join(SC, f"p{num:02d}.txt"))
        pret = os.path.exists(p) and os.path.getmtime(p) > scen_m and (
            time.time() - os.path.getmtime(p) > 360 or os.path.exists(os.path.join(PL, f"p{num:02d}.ok")))
        if not pret:
            time.sleep(20)
            continue
    libre = shutil.disk_usage("C:\\").free / 1e9
    if libre < 9:
        log(f"disque : {libre:.1f} Go libres, j'attends")
        time.sleep(300)
        continue
    mtime = os.path.getmtime(os.path.join(SC, f"p{num:02d}.txt"))
    nom = titre(num)
    mp4 = os.path.join(SC, nom + ".mp4")
    t0 = time.time()
    log(f"p{num:02d} : rendu ({nom})")
    r = subprocess.run([sys.executable, "scenario.py", f"scenarios/film/ep14_conte/p{num:02d}.txt", "tout", "3"],
                       cwd=MOTEUR)
    ok = r.returncode == 0 and os.path.exists(mp4) and os.path.getmtime(mp4) > t0
    etat[str(num)] = dict(mtime=mtime, ok=ok, fin=time.strftime("%H:%M"), minutes=round((time.time() - t0) / 60, 1))
    json.dump(etat, open(ETAT, "w", encoding="utf-8"), indent=1)
    if ok:
        w = os.path.join(os.environ["TEMP"], "ia501", nom.replace(" ", "_") + "_frames")
        shutil.rmtree(w, ignore_errors=True)
        log(f"p{num:02d} : OK en {(time.time() - t0) / 60:.1f} min, {os.path.getsize(mp4) / 1e9:.2f} Go ; "
            f"images temporaires supprimées ; {shutil.disk_usage('C:/').free / 1e9:.1f} Go libres")
    else:
        log(f"p{num:02d} : ÉCHEC (code {r.returncode})")
log("file de rendu : terminée")
