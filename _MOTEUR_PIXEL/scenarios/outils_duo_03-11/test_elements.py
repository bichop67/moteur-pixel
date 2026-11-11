# Planche de test des 4 nouveaux éléments (radiographie, orteil, arbre, balance), sur fond sombre.
import os
import sys

sys.path.insert(0, "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL")
from PIL import Image, ImageDraw
import explique as ex

SCR = os.path.dirname(os.path.abspath(__file__))

rad = ex.Radio("radio PETIT", "PETIT")
rad.plus = [(1.0, "SUBHAN ALLAH"), (1.8, "ALHAMDOULILLAH"), (2.6, "ALLAHOU AKBAR")]
rad.t_tout, rad.lab_tout = 4.0, "2 RAKATS DE DUHA"
ort = ex.Orteil("orteil")
arb = ex.Arbre("arbre", "TES PÉCHÉS")
arb.t_chute = 1.0
bal = ex.Balance("balance", "LE MONDE ENTIER", "2 RAKATS")
bal.ajouts = [(2.4, "manette")]
bal.t_pese = 3.4

lignes = [(rad, [0.0, 1.3, 2.9, 4.4, 5.5]), (ort, [0.0, 0.3, 0.5, 0.8, 1.6]), (arb, [0.5, 1.6, 2.4, 3.4, 5.0]),
          (bal, [0.0, 1.0, 2.8, 4.0, 5.2])]
TW, TH = 520, 500
planche = Image.new("RGB", (TW * 5, TH * 4), (34, 30, 44))
d = ImageDraw.Draw(planche)
for j, (el, us) in enumerate(lignes):
    for i, u in enumerate(us):
        im = el.image(u)
        k = min((TW - 10) / im.width, (TH - 30) / im.height)
        im2 = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        fond = Image.new("RGBA", (TW, TH), (52, 46, 64, 255))
        fond.alpha_composite(im2, (int((TW - im2.width) / 2), 24))
        planche.paste(fond.convert("RGB"), (i * TW, j * TH))
        d.text((i * TW + 8, j * TH + 4), f"{type(el).__name__} u={u}", fill=(255, 255, 0))
planche.save(os.path.join(SCR, "test_elements.png"))
print("ok", planche.size)
for el in (rad, ort, arb, bal):
    print(type(el).__name__, el.image(1.0).size, el.sons_el())
