# SAUVEGARDE DATÉE DU MOTEUR PIXEL + DU SKILL video-pixel (une seule commande, à lancer après chaque grosse
# modification validée et AVANT toute modification risquée) :
#     python sauve_moteur.py <sujet_sans_espace>
# → ..\_MOTEUR\moteur_pixel_<AAAA-MM-JJ>_<sujet>.zip  (code, textes, réglages, sons ; pas les planches ni les vidéos)
import os
import sys
import time
import zipfile

ICI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(os.path.dirname(ICI), "_MOTEUR")
SKILL = os.path.join(os.path.expanduser("~"), ".claude", "skills", "video-pixel")
EXT = (".py", ".txt", ".json", ".md", ".mp3", ".wav", ".ogg", ".ttf", ".otf")
SAUTE = ("__pycache__",)


def _fichiers(racine, images=False):
    for dossier, sous, noms in os.walk(racine):
        sous[:] = [d for d in sous if d not in SAUTE]
        for n in noms:
            chemin = os.path.join(dossier, n)
            bas = n.lower()
            if bas.endswith(EXT):
                yield chemin
            elif images and bas.endswith(".png") and os.path.getsize(chemin) < 400_000 \
                    and "planche" not in bas and "_qa" not in bas:
                yield chemin                                     # petites images utiles au moteur (pas les planches)
            elif images and bas.endswith(".jpg") and os.path.basename(dossier) == "controle_moteur_ref":
                yield chemin                                     # vignettes de référence de controle_moteur.py


def main():
    sujet = "_".join(sys.argv[1:]) or "sauvegarde"
    os.makedirs(DEST, exist_ok=True)
    base = os.path.join(DEST, "moteur_pixel_%s_%s" % (time.strftime("%Y-%m-%d"), sujet))
    cible, n = base + ".zip", 2
    while os.path.exists(cible):                                 # jamais d'écrasement d'une sauvegarde
        cible = "%s_%d.zip" % (base, n)
        n += 1
    nb = 0
    with zipfile.ZipFile(cible, "w", zipfile.ZIP_DEFLATED) as z:
        for f in _fichiers(ICI, images=True):
            z.write(f, os.path.join("_MOTEUR_PIXEL", os.path.relpath(f, ICI)))
            nb += 1
        if os.path.isdir(SKILL):
            for f in _fichiers(SKILL):
                z.write(f, os.path.join("skill_video-pixel", os.path.relpath(f, SKILL)))
                nb += 1
    print("OK : %d fichiers, %.1f Mo -> %s" % (nb, os.path.getsize(cible) / 1e6, cible))


if __name__ == "__main__":
    main()
