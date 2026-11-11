# Attend qu'au moins un scénario du lot du 08/11/2026 porte le marqueur « # TEXTE FIGÉ » (posé par la contre-vérification
# religieuse) et ne soit pas encore dans deja.txt (codes déjà passés aux voix). Affiche les nouveaux puis s'arrête.
# Usage : python attend_figes.py [délai_max_minutes]
import io
import os
import sys
import time

SC = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL/scenarios"
ICI = os.path.dirname(os.path.abspath(__file__))
LOT = {"ISL23": "islam_23_talons.txt", "ISL24": "islam_24_urine.txt", "ISL25": "islam_25_droite.txt",
       "ISL26": "islam_26_imam.txt", "ISL27": "islam_27_asr.txt", "ISL28": "islam_28_medisance.txt",
       "ISL29": "islam_29_ecoute.txt", "ISL30": "islam_30_horoscope.txt", "ISL31": "islam_31_coucher.txt"}
fin = time.time() + 60 * float(sys.argv[1] if len(sys.argv) > 1 else 240)
p_deja = os.path.join(ICI, "deja.txt")


def figes():
    out = []
    for code, f in LOT.items():
        p = os.path.join(SC, f)
        if os.path.exists(p):
            with io.open(p, encoding="utf-8") as fh:
                if fh.readline().startswith("# TEXTE FIGÉ"):
                    out.append(code)
    return out


while True:
    deja = set(io.open(p_deja, encoding="utf-8").read().split()) if os.path.exists(p_deja) else set()
    nouveaux = [c for c in figes() if c not in deja]
    mini = int(sys.argv[2]) if len(sys.argv) > 2 else 1        # nombre minimum de nouveaux figés avant de s'arrêter
    if len(nouveaux) >= mini:
        time.sleep(20)                     # laisse l'agent finir d'écrire
        nouveaux = [c for c in figes() if c not in deja]
        print("FIGÉS :", " ".join(nouveaux), "| déjà faits :", " ".join(sorted(deja)) or "aucun",
              "| en attente :", " ".join(c for c in LOT if c not in deja and c not in nouveaux), flush=True)
        sys.exit(0)
    if time.time() > fin:
        print("délai dépassé ; figés :", " ".join(figes()), flush=True)
        sys.exit(1)
    time.sleep(30)
