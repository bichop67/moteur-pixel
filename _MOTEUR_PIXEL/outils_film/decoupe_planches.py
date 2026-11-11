"""Découpe les planches du film en morceaux lisibles + repère les images noires / ratées (magenta)."""
import os
import sys
from PIL import Image, ImageStat

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "planches_film")
os.makedirs(OUT, exist_ok=True)

# 1) enchaînements : 3 colonnes de 320x180, une ligne par passage d'une partie à l'autre
g = Image.open(os.path.join(D, "film_enchainements.png")).convert("RGB")
rows = g.height // 180
for k in range(0, rows, 6):
    g.crop((0, k * 180, 960, min(rows, k + 6) * 180)).save(os.path.join(OUT, f"ench_{k // 6 + 1}.png"))
print("enchaînements :", rows, "lignes")

# 2) une image toutes les 10 s : 10 colonnes ; morceaux de 6 lignes réduits de moitié
g2 = Image.open(os.path.join(D, "film_toutes_10s.png")).convert("RGB")
rows2 = g2.height // 180
for k in range(0, rows2, 6):
    c = g2.crop((0, k * 180, 3200, min(rows2, k + 6) * 180))
    c.resize((c.width // 2, c.height // 2), Image.LANCZOS).save(os.path.join(OUT, f"10s_{k // 6 + 1}.png"))

# 3) contrôle automatique de chaque image (sans le texte jaune du coin)
sombres, ratees = [], []
for r in range(rows2):
    for col in range(10):
        i = r * 10 + col
        cell = g2.crop((col * 320, r * 180 + 30, col * 320 + 320, r * 180 + 180))
        m = ImageStat.Stat(cell).mean
        if m[0] > 240 and m[1] < 15 and m[2] > 240:
            ratees.append(i * 10)
        elif sum(m) / 3 < 6:
            sombres.append(i * 10)
print("images ratées (magenta) :", ratees or "aucune")
print("images presque noires :", sombres or "aucune")
print("morceaux :", sorted(os.listdir(OUT)))
