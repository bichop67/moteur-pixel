"""Grille d'images clés d'un scénario : python stills_grille.py scenario.txt sortie.png t1 t2 t3 …"""
import os
import sys

MOTEUR = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
sys.path.insert(0, MOTEUR)
os.chdir(MOTEUR)
scen, out, ts = sys.argv[1], os.path.abspath(sys.argv[2]), [float(x) for x in sys.argv[3:]]
sys.argv = ["scenario.py"]
import scenario  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

V = scenario.fabrique(scen)[0]
W, H = 960, 540
cols = 2
rows = (len(ts) + cols - 1) // cols
g = Image.new("RGB", (cols * W, rows * H), (0, 0, 0))
f = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 22)
for i, t in enumerate(ts):
    im = V.frame(t).convert("RGB").resize((W, H), Image.LANCZOS)
    ImageDraw.Draw(im).text((10, 6), f"{t:.1f} s", fill=(255, 255, 0), font=f)
    g.paste(im, ((i % cols) * W, (i // cols) * H))
g.save(out)
print("ok", out)
