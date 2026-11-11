"""Chapitres YouTube du film Moussa, version « conte » (épisode 14) : début de chaque partie dans le film assemblé
(fondu enchaîné de 1 s entre les parties, comme assemble_conte.py). python chapitres_conte.py -> « 0:00 Titre »."""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
MOTEUR = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
sys.path.insert(0, MOTEUR)
import assemble_film  # noqa: E402

D = os.path.join(MOTEUR, "scenarios", "film", "ep14_conte")
FONDU = 1.0
ACCENTS = {"L'Egypte de Pharaon": "L'Égypte de Pharaon", "Dix ans a Madyan": "Dix ans à Madyan",
           "Le retour en Egypte": "Le retour en Égypte", "Face a Pharaon": "Face à Pharaon",
           "Le jour de la fete": "Le jour de la fête", "Les fleaux": "Les fléaux", "Dans le desert": "Dans le désert"}


def titre(n):
    for ligne in io.open(os.path.join(D, f"p{n:02d}.txt"), encoding="utf-8"):
        if ligne.startswith("TITRE:"):
            return ligne.split(":", 1)[1].strip()
    return None


def fmt(s):
    s = int(s)                                   # YouTube : le chapitre commence à la seconde entamée
    h, m, x = s // 3600, (s % 3600) // 60, s % 60
    return f"{h}:{m:02d}:{x:02d}" if h else f"{m}:{x:02d}"


if __name__ == "__main__":
    t, lignes = 0.0, []
    for n in range(1, 25):
        ti = titre(n)
        mp4 = os.path.join(D, ti + ".mp4")
        if not os.path.exists(mp4):
            print("MANQUE", mp4)
            continue
        d = assemble_film.duree_image(mp4)
        court = ti.split(" - ", 2)[-1]
        lignes.append(f"{fmt(t)} {ACCENTS.get(court, court)}")
        t += d - FONDU
    print("\n".join(lignes))
    print("durée totale ≈", fmt(t + FONDU))
