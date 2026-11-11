"""Une image au milieu de chaque bloc d'un scénario (planche 2 colonnes) — charge aussi les décors en test.
python stills_blocs.py scenario.txt sortie.png [module_decors ...]"""
import importlib
import os
import sys

MOTEUR = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
sys.path.insert(0, MOTEUR)
os.chdir(MOTEUR)
scen, out, mods = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3:]
sys.argv = ["scenario.py"]
import scenario  # noqa: E402
for m in mods:
    importlib.import_module(m)
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

V = scenario.fabrique(scen)[0]
ts = []
for sh in V.shots:
    ts.append(((sh.t0 + sh.t1) * 0.5, sh.bg if isinstance(sh.bg, str) else "?"))
if not ts:
    print("pas de plans ?", [type(s).__name__ for s in V.shots][:5])
W, H = 960, 540
cols = 2
rows = (len(ts) + cols - 1) // cols
g = Image.new("RGB", (cols * W, rows * H), (0, 0, 0))
f = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 22)
for i, (t, nom) in enumerate(ts):
    im = V.frame(t).convert("RGB").resize((W, H), Image.LANCZOS)
    ImageDraw.Draw(im).text((10, 6), f"{t:.1f} s  {nom}", fill=(255, 255, 0), font=f)
    g.paste(im, ((i % cols) * W, (i // cols) * H))
g.save(out)
print("ok", out, len(ts))
