# CONTRÔLE APRÈS UNE MODIFICATION DU MOTEUR : d'anciens Shorts doivent sortir IDENTIQUES au pixel près.
#     python sauve_moteur.py avant_<sujet>        (AVANT de modifier)
#     … modifications …
#     python controle_avant_apres.py              compare le moteur actuel à la sauvegarde la plus récente
#     python controle_avant_apres.py "..\_MOTEUR\moteur_pixel_….zip"     ou à une sauvegarde précise
# « avant » = le moteur de la sauvegarde (décompressé dans le dossier temporaire) ; « après » = le moteur actuel.
# Remplace controle_vop.py tant que le dossier des voix VOP n'est plus sur le Bureau (constaté le 09/11/2026).
import glob
import hashlib
import os
import subprocess
import sys
import zipfile

from PIL import Image

MOTEUR = os.path.dirname(os.path.abspath(__file__))
SAUVEGARDES = os.path.join(os.path.dirname(MOTEUR), "_MOTEUR")
CAS = [("islam_13_telephone.txt", (1.0, 12.0)), ("islam_17_jurer.txt", (1.0, 9.0, 20.0)),
       ("islam_23_talons.txt", (1.0, 8.0, 19.0))]


def main():
    zips = [a for a in sys.argv[1:] if a.lower().endswith(".zip")]
    z_path = os.path.abspath(zips[0]) if zips else max(glob.glob(os.path.join(SAUVEGARDES, "moteur_pixel_*.zip")),
                                                       key=os.path.getmtime)
    avant = os.path.join(os.environ.get("TEMP", "."), "ia501", "avant", os.path.splitext(os.path.basename(z_path))[0])
    print("avant =", os.path.basename(z_path))
    if not os.path.isdir(os.path.join(avant, "_MOTEUR_PIXEL")):
        with zipfile.ZipFile(z_path) as z:
            z.extractall(avant, [n for n in z.namelist() if n.startswith("_MOTEUR_PIXEL/")])
        for dossier, _, noms in os.walk(MOTEUR):                  # les images absentes de la sauvegarde
            if "__pycache__" in dossier:
                continue
            for n in noms:
                if n.lower().endswith((".png", ".jpg", ".npy", ".npz", ".pkl")) and "planche" not in n \
                        and "_qa" not in n and "controle" not in n:
                    src = os.path.join(dossier, n)
                    dst = os.path.join(avant, "_MOTEUR_PIXEL", os.path.relpath(src, MOTEUR))
                    if not os.path.exists(dst):
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        with open(src, "rb") as a, open(dst, "wb") as b:
                            b.write(a.read())
    mauvais = 0
    for sc, instants in CAS:
        for t in instants:
            h = {}
            for nom, dossier in (("avant", os.path.join(avant, "_MOTEUR_PIXEL")), ("apres", MOTEUR)):
                out = os.path.join(avant, "cmp_%s.png" % nom)
                r = subprocess.run([sys.executable, "scenario.py", os.path.join("scenarios", sc), "still", str(t), out],
                                   cwd=dossier, capture_output=True, text=True, errors="ignore")
                if r.returncode or not os.path.exists(out):
                    h[nom] = "ERREUR : " + (r.stderr.strip().splitlines() or ["?"])[-1][:160]
                else:
                    h[nom] = hashlib.md5(Image.open(out).convert("RGB").tobytes()).hexdigest()
                    os.remove(out)
            ok = h["avant"] == h["apres"] and not h["avant"].startswith("ERREUR")
            mauvais += 0 if ok else 1
            print("%-26s %5.1f s : %s" % (sc, t, "identique" if ok else "DIFFÉRENT  avant=%s  après=%s"
                                          % (h["avant"], h["apres"])))
    print("VERDICT :", "OK : les anciens Shorts sont identiques" if not mauvais else "%d image(s) à regarder" % mauvais)


if __name__ == "__main__":
    main()
