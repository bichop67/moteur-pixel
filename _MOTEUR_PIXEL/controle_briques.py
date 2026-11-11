# CONTRÔLE DES BRIQUES (à lancer après toute modification de briques.py, AVANT un rendu) :
#     python controle_briques.py              chaque brique est dessinée à 30 images / s pendant 8 s : aucune ne doit
#                                             planter (une seule image qui plante fait échouer tout un rendu)
#     python controle_briques.py planche x.png    + une planche de 3 instants par brique, à regarder
# Leçon du 09/11/2026 : un essai à 10 images / s avait laissé passer une jauge qui plantait pendant 2 images.
import os
import sys
import traceback

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
os.chdir(ICI)
from PIL import Image, ImageDraw  # noqa: E402
import explique  # noqa: E402

ESSAIS = [
    ("liste", [(0.0, 'liste titre "TU JURES SUR…" "TON PÈRE" "TA MÈRE" "PAR ALLAH"'), (1.2, "liste barre 1 2"),
               (2.2, "liste or 3"), (3.0, 'liste + "TA VIE"'), (3.6, "liste barre 4"),
               (4.2, 'liste note "… OU TU TE TAIS"'), (4.4, 'source "ABOU DAWOUD 3248"')], (1.0, 2.9, 5.6)),
    ("liste nuit", [(0.0, 'liste nuit "CE QUI EST EFFACÉ" "TES PETITS PÉCHÉS" "TES GRANDS PÉCHÉS // IL FAUT SE REPENTIR" "TA DETTE"'),
                    (1.0, "liste coche 2"), (1.8, "liste efface 3"), (2.4, "liste or 4")], (0.8, 1.6, 3.4)),
    ("citation", [(0.0, 'citation "LE PROPHÈTE ﷺ A DIT :" "« MALHEUR AUX TALONS… À CAUSE DU FEU ! »"'),
                  (2.0, "citation lueur rouge"), (3.0, 'citation note "= LAVE TOUT LE PIED"'),
                  (0.2, 'source "BOUKHARI 163 · MOUSLIM 241"')], (0.5, 2.6, 4.5)),
    ("jauge", [(0.0, 'jauge "COLÈRE" 100 -> 35 PETIT %'), (2.6, "jauge -> 0"), (3.9, 'jauge fin "CALME"')],
     (0.4, 1.6, 5.0)),
    ("jauge seule", [(0.0, 'jauge "TA FOI" 20 inverse'), (1.0, "jauge -> 90"), (2.4, 'jauge fin "ELLE REMONTE"')],
     (0.6, 1.7, 3.4)),
    ("focus", [(0.0, 'focus telephone "TON TÉLÉPHONE"'), (1.2, 'focus entoure haut "FENDU"'),
               (2.6, 'focus ok "DIS : INNA LILLAHI"'), (3.2, "focus lueur or")], (0.6, 2.0, 4.4)),
    ("focus perso", [(0.0, 'focus PETIT triste "TOI, CE MATIN"'), (1.0, 'focus entoure 50 30 "LES YEUX"'),
                     (2.0, 'focus non "NE FAIS PAS ÇA"'), (2.4, "focus lueur rouge")], (0.6, 1.6, 3.4)),
    ("versus", [(0.0, 'versus titre "TU MANGES AVEC…" pouce_bas "LA MAIN GAUCHE" pouce "LA MAIN DROITE"'),
                (1.4, "versus non"), (2.4, "versus oui")], (0.9, 1.9, 3.4)),
    ("bulles", [(0.2, 'bulles PETIT "AL-HAMDOU LILLAH"'), (1.4, 'bulles GRAND content "YARHAMOUKA ALLAH"'),
                (2.6, 'bulles PETIT or "YAHDIKOUMOU ALLAH"'), (3.8, "bulles GRAND vide")], (1.0, 2.2, 4.6)),
    ("trajet", [(0.0, 'trajet titre "LE VOYAGE" "SA VILLE" -> "LE BON PAYS" PETIT'), (0.8, "trajet avance 45"),
                (1.4, 'trajet etape 45 "MI-CHEMIN"'), (2.6, 'trajet stop "IL S\'ARRÊTE ICI"'), (4.0, "trajet arrive"),
                (4.2, "trajet lueur or")], (1.3, 3.2, 6.0)),
    ("grille 40", [(0.0, 'grille 40 "JOURS" "TA PRIÈRE"'), (1.0, "grille barre 40"), (3.2, "grille vide"),
                   (3.8, "grille coche 12")], (0.6, 2.9, 5.4)),
    ("grille 5", [(0.0, 'grille 5 "PRIÈRES"'), (0.8, "grille coche 3")], (0.5, 1.5, 2.4)),
]


def main():
    planche = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "planche" else None
    mauvais, tuiles = 0, []
    for nom, ordres, instants in ESSAIS:
        try:
            sch = explique.Schema(ordres)
            for it in sch.items:
                for i in range(240):
                    it["el"].image(i / 30.0)
            print("%-12s OK" % nom)
            if planche:
                for u in instants:
                    img = Image.new("RGBA", (1080, 1920), (30, 26, 44, 255))
                    sch(img, u)
                    t = img.crop((0, 200, 1080, 1330)).resize((360, 377), Image.LANCZOS)
                    ImageDraw.Draw(t).text((4, 3), "%s  %.1f s" % (nom, u), fill=(255, 255, 0, 255))
                    tuiles.append(t)
        except Exception:
            mauvais += 1
            print("%-12s ERREUR : %s" % (nom, " | ".join(traceback.format_exc().strip().splitlines()[-3:])))
    if planche and tuiles:
        pl = Image.new("RGBA", (360 * 6, 377 * ((len(tuiles) + 5) // 6)), (0, 0, 0, 255))
        for i, t in enumerate(tuiles):
            pl.alpha_composite(t, (360 * (i % 6), 377 * (i // 6)))
        pl.convert("RGB").save(planche)
        print("planche :", planche)
    print("VERDICT :", "OK, les briques se dessinent toutes" if not mauvais else "%d brique(s) à corriger" % mauvais)


if __name__ == "__main__":
    main()
