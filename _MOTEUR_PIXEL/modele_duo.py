# MODÈLE DE SHORT « DUO » — à copier pour chaque nouvelle vidéo, sur n'importe quelle chaîne.
#  1) Copier ce fichier (ex. ciel01.py), remplir CODE, TITRE, DOSSIER, THEME, les deux personnages et REPLIQUES.
#  2) python ciel01.py sheet          -> planche de contrôle (MAQUETTE sans voix tant que les MP3 n'existent pas)
#  3) python ciel01.py voix           -> textes à générer sur ElevenLabs : un MP3 par personnage, nommé CODE_QUI.mp3
#  4) python ciel01.py asr            -> transcription des voix (asr_CODE.json) ; relancer sheet : tout se cale sur les voix
#  5) python ciel01.py frames 0 4 (… 1 4, 2 4, 3 4 en parallèle), puis python ciel01.py video
# Exemple ci-dessous : une chaîne « science » (thème bleu), un enfant qui demande, une scientifique qui explique.
import kit, pxv

CODE = "EXEMPLE01"
TITRE = "Pourquoi le ciel est bleu"                       # nom du fichier vidéo (jamais d'apostrophe)
DOSSIER = pxv.BASE + "/_MOTEUR_PIXEL/CATALOGUE/"
VOIX = DOSSIER + "voix_exemple/"
MUSIQUE = pxv.BASE + "/_MUSIQUES/FOND/fond_espoir.mp3"
THEME = kit.THEMES["science"]                             # valable, neutre, sketch, info, histoire, mystere, science, argent, podcast
Q, R = "ENFANT", "SCIENTIFIQUE"                           # Q pose les questions (vignette à droite), R explique

REPLIQUES = [
    (Q, "Pourquoi le ciel est bleu ?"),
    (R, "La lumière du soleil contient toutes les couleurs."),
    (Q, "Même le rouge ?"),
    (R, "Oui. Mais en traversant l'air, le bleu est éparpillé beaucoup plus que le rouge."),
    (Q, "Éparpillé où ?"),
    (R, "Partout dans le ciel. Alors, où que tu regardes, du bleu arrive dans tes yeux."),
    (Q, "Et le soir, il devient orange !"),
    (R, "La lumière traverse plus d'air, et le bleu se perd en route. Abonne-toi pour la suite."),
]

D = kit.dialogue(VOIX, CODE, REPLIQUES)
L = D.lines
t = lambda k: L[k]["t0"]
te = lambda k: L[k]["t1"] + 0.06
THEME.cotes = {Q: "right", R: "left"}

plans = [
    kit.accroche(["POURQUOI LE CIEL", "EST BLEU ?"], kit.photo("parc", Q, face="choc"), THEME),
    kit.duo_plan(kit.T_HOOK, te(0), "parc", Q, R, g=dict(pose="question", face="choc"), d=dict(pose="neutre", face="content")),
    kit.tableau_plan(t(1), te(1), kit.ecrit([(80, "LA LUMIÈRE DU SOLEIL", 13, False), (100, "TOUTES LES COULEURS", 14, True)],
                                            [("soleil", 95, 124, 5)], style="craie"), gauche=Q, droite=R),
    kit.gros_plan(t(2), te(2), Q, "parc", face="suspect", bulle="?"),
    kit.duo_plan(t(3), te(3), "labo", Q, R, g=dict(pose="neutre", face="neutre"), d=dict(pose="explique", face="neutre")),
    kit.gros_plan(t(4), te(4), Q, "labo", face="choc", pose="question"),
    kit.tableau_plan(t(5), te(5), kit.ecrit([(80, "LE BLEU S'ÉPARPILLE", 13, True), (100, "DANS TOUT LE CIEL", 13, False)],
                                            [("nuage", 60, 124, 5), ("oeil", 140, 124, 5)], style="craie"), gauche=Q, droite=R),
    kit.gros_plan(t(6), te(6), Q, "parc_soir", face="etoile", pose="pointe"),
    kit.fin(t(7), D.dur, "parc_soir", Q, R, THEME),
]
VID = pxv.Video(D, plans, music=MUSIQUE, music_gain=0.10, theme=THEME)

if __name__ == "__main__":
    kit.rendu(VID, TITRE, DOSSIER, code=CODE, voix=VOIX, repliques=REPLIQUES)
