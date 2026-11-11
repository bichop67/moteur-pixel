# Planche des 5 premières secondes (une image toutes les 0,5 s) des 3 Shorts duo, avec les vraies voix.
import os
import sys

ENGINE = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL"
sys.path.insert(0, ENGINE)
os.chdir(ENGINE)
from PIL import Image, ImageDraw
import scenario

SCR = os.path.dirname(os.path.abspath(__file__))
noms = sys.argv[1:] or ["islam_05_aumones", "islam_06_orteil", "islam_07_monde"]
TW, TH = 216, 384
for nom in noms:
    V = scenario.fabrique(f"scenarios/{nom}.txt")[0]
    ts = [i * 0.5 for i in range(10)]
    pl = Image.new("RGB", (TW * 10, TH + 22), (20, 20, 26))
    d = ImageDraw.Draw(pl)
    for i, t in enumerate(ts):
        im = V.frame(t).convert("RGB").resize((TW, TH), Image.LANCZOS)
        pl.paste(im, (i * TW, 22))
        d.text((i * TW + 6, 4), f"{t:.1f} s", fill=(255, 230, 0))
    out = os.path.join(SCR, f"5s_{nom}.png")
    pl.save(out)
    print(out)
