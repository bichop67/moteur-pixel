"""Miniatures de l'épisode 14 (Moussa, le film) : deux variantes pour le test A/B de YouTube.
A : la mer ouverte, l'orbe de Moussa qui brille, Pharaon dans les flots du côté droit — « MOUSSA / LE FILM COMPLET »
B : le palais, Pharaon sur son trône, l'orbe de Moussa face à lui — « MOUSSA / FACE À PHARAON »"""
import os
import sys

MOTEUR = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
sys.path.insert(0, MOTEUR)
os.chdir(MOTEUR)
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
import miniature as M  # noqa: E402
import film  # noqa: E402
import troupe_egypte  # noqa: E402,F401
import scenario  # noqa: E402,F401  (charge tous les décors du film)

OUT = sys.argv[1]


def orbe(img, x, y, k=13, pose="intense"):
    spr = film.image("MOUSSA", pose=pose)
    big = spr.resize((spr.width * k, spr.height * k), Image.NEAREST)
    M._halo(img, x, y, 330, 330, (255, 214, 120), 0.6)
    cy = spr.info.get("cy", spr.height // 2) * k
    img.alpha_composite(big, (int(x - big.width / 2), int(y - cy)))


def variante(nom, bg, y0, persos, lignes, xo, yo):
    img = M._fond(bg, True, y0, flou=1.5, sombre=0.85)
    orbe(img, xo, yo)
    for (who, st, x, k) in persos:
        st = dict(st)
        mir = st.pop("miroir", False)
        im, top = M.perso(who, k, miroir=mir, **st)
        img.alpha_composite(im, (int(x - im.width / 2 + 2 * k), 120 - top))
    M._vignette(img)
    t = M.titre(lignes, 1040, taille=210)
    img.alpha_composite(t, (60, max(60, 520 - t.height // 2)))
    out = img.convert("RGB").resize((1280, 720), Image.LANCZOS)
    p = os.path.join(OUT, nom)
    out.save(p, quality=93)
    print("ok", p)


variante("Moussa - miniature A (la mer).jpg", "mer_ouverte", 96, [("PHARAON", dict(face="peur", miroir=True), 1690, 13)],
         ["MOUSSA", "LE FILM"], 1300, 470)
variante("Moussa - miniature B (Pharaon).jpg", "palais_egypte", 100,
         [("PHARAON", dict(face="enerve", pose="pointe", miroir=True), 1660, 14)], ["MOUSSA", "FACE À", "PHARAON"], 1260, 470)
