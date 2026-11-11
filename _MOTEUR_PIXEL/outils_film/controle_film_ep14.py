"""Contrôle du film assemblé (épisode 14) : durée, volume, trous de son, et une planche des enchaînements
(une image 1,5 s avant / au noir / 1,5 s après chaque passage d'une partie à l'autre) + 1 image toutes les 10 s.
python controle_film_ep14.py film.mp4 dossier_sortie"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
MOTEUR = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
sys.path.insert(0, MOTEUR)
import controle_video as CV  # noqa: E402
from pxv import FF  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chapitres_ep14 as CH  # noqa: E402
import assemble_film  # noqa: E402

vid, out = sys.argv[1], sys.argv[2]
d, (w, h), lufs, pic = CV.infos(vid)
t = CV.trous(vid, d)
print(f"{os.path.basename(vid)} : {d:.1f} s ({d / 60:.1f} min), {w}x{h}, {lufs} LUFS, crête {pic} dBFS, "
      + (f"{len(t)} tranche(s) silencieuse(s) : {t[:20]}" if t else "aucun trou de son"))

# instants des enchaînements (comme assemble_film : 1 s de noir croisé)
debuts, tt = [], 0.0
for (n, ti, mp4) in CH.parties():
    debuts.append(tt)
    tt += assemble_film.duree_image(mp4) - CH.NOIR
f = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 18)


def image(t_):
    r = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-ss", f"{t_:.2f}", "-i", vid, "-frames:v", "1",
                        "-vf", "scale=320:180", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    if len(r.stdout) < 320 * 180 * 3:
        return Image.new("RGB", (320, 180), (255, 0, 255))
    im = Image.frombytes("RGB", (320, 180), r.stdout[:320 * 180 * 3])
    ImageDraw.Draw(im).text((6, 4), f"{t_:.1f}", fill=(255, 255, 0), font=f)
    return im


lignes = []
for i, b in enumerate(debuts[1:], 1):                                          # chaque enchaînement : avant / pendant / après
    lignes.append([image(b - 1.5), image(b - 0.5), image(b + 1.5)])
g = Image.new("RGB", (3 * 320, len(lignes) * 180), (0, 0, 0))
for j, row in enumerate(lignes):
    for i, im in enumerate(row):
        g.paste(im, (i * 320, j * 180))
p1 = os.path.join(out, "film_enchainements.png")
g.save(p1)
ts = [x * 10.0 for x in range(int(d // 10) + 1)]                              # une image toutes les 10 s
cols = 10
rows = (len(ts) + cols - 1) // cols
g2 = Image.new("RGB", (cols * 320, rows * 180), (0, 0, 0))
for k, t_ in enumerate(ts):
    g2.paste(image(min(t_, d - 0.5)), ((k % cols) * 320, (k // cols) * 180))
p2 = os.path.join(out, "film_toutes_10s.png")
g2.save(p2)
print("planches :", p1, p2)
