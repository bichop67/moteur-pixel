# Planche de test d'éléments de schéma (_MOTEUR_PIXEL) : une ligne par élément, une case par instant u.
# Usage : python planche_el.py <module> <spec.json> <sortie.png>
# spec.json = liste de lignes : {"nom": "...", "classe": "NomDeClasse", "args": ["cmd", "mode"...],
#                               "t": {"etape": secondes, ...}, "u": [-0.3, 0.2, 1.0, ...]}
# Chaque case montre l'image de l'élément à l'instant u (secondes depuis son apparition) sur un fond gris-bleu,
# réduite pour tenir dans 400 x 400, avec le temps de calcul. La console affiche aussi sons_el() de chaque élément.
import importlib
import json
import os
import sys
import time
import traceback

sys.path.insert(0, "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL")
from PIL import Image, ImageDraw

mod = importlib.import_module(sys.argv[1])
spec = json.load(open(sys.argv[2], encoding="utf-8"))
out = sys.argv[3]

TW, TH = 400, 400
ncol = max(len(l["u"]) for l in spec)
planche = Image.new("RGB", (TW * ncol, TH * len(spec)), (34, 30, 44))
d = ImageDraw.Draw(planche)
for j, l in enumerate(spec):
    el = getattr(mod, l["classe"])(*l.get("args", [l["nom"]]))
    el.t = dict(l.get("t", {}))
    for i, u in enumerate(l["u"]):
        t0 = time.time()
        try:
            im = el.image(u)
        except Exception:
            traceback.print_exc()
            im = Image.new("RGBA", (300, 300), (255, 0, 0, 255))
        dt = time.time() - t0
        k = min((TW - 10) / im.width, (TH - 30) / im.height)
        im2 = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        fond = Image.new("RGBA", (TW, TH), (60, 66, 84, 255))
        fond.alpha_composite(im2, (int((TW - im2.width) / 2), 24))
        planche.paste(fond.convert("RGB"), (i * TW, j * TH))
        d.text((i * TW + 8, j * TH + 4), f"{l['nom']} u={u} ({im.width}x{im.height}, {dt * 1000:.0f} ms)",
               fill=(255, 255, 0))
    try:
        print(l["nom"], "sons_el :", el.sons_el())
    except Exception as e:
        print(l["nom"], "sons_el : ERREUR", e)
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
planche.save(out)
print("planche :", out)
