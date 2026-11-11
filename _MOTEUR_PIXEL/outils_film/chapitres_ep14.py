"""Chapitres YouTube du film Moussa (épisode 14) : début de chaque partie dans le film assemblé
(xfade de 1 s entre les parties, comme assemble_film.py). python chapitres_ep14.py  -> liste « 0:00 Titre »."""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
MOTEUR = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
sys.path.insert(0, MOTEUR)
import assemble_film  # noqa: E402

D = os.path.join(MOTEUR, "scenarios", "film", "ep14")
NOIR = 1.0
ACCENTS = {"L'Egypte de Pharaon": "L'Égypte de Pharaon", "Dix ans a Madyan": "Dix ans à Madyan",
           "Le retour en Egypte": "Le retour en Égypte", "Face a Pharaon": "Face à Pharaon",
           "Le jour de la fete": "Le jour de la fête", "Les fleaux": "Les fléaux", "Dans le desert": "Dans le désert"}


def titre(n):
    for ligne in io.open(os.path.join(D, f"p{n:02d}.txt"), encoding="utf-8"):
        if ligne.startswith("TITRE:"):
            return ligne.split(":", 1)[1].strip()
    return None


def parties():
    out = []
    for n in range(1, 25):
        t = titre(n)
        nom = re.sub(r"\s+", " ", re.sub(r"[^\w \-']", "", "".join(
            c for c in __import__("unicodedata").normalize("NFD", t) if not __import__("unicodedata").combining(c)))).strip()
        mp4 = os.path.join(D, nom + ".mp4")
        out.append((n, t, mp4))
    return out


def fmt(s):
    s = int(round(s))
    h, m, x = s // 3600, (s % 3600) // 60, s % 60
    return f"{h}:{m:02d}:{x:02d}" if h else f"{m}:{x:02d}"


if __name__ == "__main__":
    t = 0.0
    lignes = []
    for (n, ti, mp4) in parties():
        if not os.path.exists(mp4):
            print("MANQUE", mp4)
            continue
        d = assemble_film.duree_image(mp4)
        court = ti.split(" - ", 2)[-1]
        court = ACCENTS.get(court, court)
        lignes.append(f"{fmt(t)} {court}")
        t += d - NOIR
    print("\n".join(lignes))
    print("durée totale ≈", fmt(t + NOIR))
