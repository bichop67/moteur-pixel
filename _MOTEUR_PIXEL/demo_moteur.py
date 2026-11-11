# Vidéo de démonstration du moteur (sans voix) : un passage par décor, avec des duos différents.
# python demo_moteur.py sheet planche.png | frames i n | video
import os, sys
import pxv, kit
from pxv import Shot, Silence, Theme

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CATALOGUE")
MUSIC = pxv.BASE + "/_MUSIQUES/FOND/fond_espoir.mp3"
THEME = Theme(bandeau="DÉMO DU MOTEUR", bandeau_fond=(44, 40, 70), bandeau_accent=(120, 230, 255), bandeau_contour=(20, 16, 40),
              carte="carte_bleue")

# (décor, gauche, droite, réglages gauche, réglages droite)
SCENES = [
    ("rue", "ADO", "PAPI", dict(pose="question", face="choc"), dict(pose="explique", face="content")),
    ("cuisine_nuit", "MAMAN", "ENFANT", dict(pose="hanches", face="suspect"), dict(pose="neutre", face="gene", objet="ballon", sweat=True)),
    ("voiture_nuit", "PAPA", "ADA", dict(pose="neutre", face="blase"), dict(pose="telephone", face="bas")),
    ("studio", "PODCASTEUR", "JOURNALISTE", dict(pose="explique", face="rire"), dict(pose="neutre", face="content")),
    ("plateau_tv", "PRESENTATEUR", "EXPERT", dict(pose="neutre", face="neutre"), dict(pose="explique", face="malin")),
    ("classe", "PROF", "ENFANT", dict(pose="pointe", face="enerve"), dict(pose="neutre", face="pleure")),
    ("snack", "LIVREUR", "EPICIER", dict(pose="tient", face="content", objet="sac_courses"), dict(pose="pouce", face="rire")),
    ("hopital", "MEDECIN", "PAPI", dict(pose="explique", face="calme"), dict(pose="neutre", face="peur", objet="canne")),
    ("metro", "GAMER", "CAPUCHE", dict(pose="telephone", face="choc"), dict(pose="bras_croises", face="suspect")),
    ("salle_sport", "COACH", "ADO", dict(pose="victoire", face="cri"), dict(pose="facepalm", face="gene", sweat=True)),
    ("palais", "ROI", "REINE", dict(pose="arret", face="enerve"), dict(pose="neutre", face="choc")),
    ("desert_nuit", "VOYAGEUR", "SAGE", dict(pose="question", face="neutre"), dict(pose="doua", face="calme")),
    ("bibliotheque", "SAVANT", "SCIENTIFIQUE", dict(pose="menton", face="suspect"), dict(pose="tient", face="etoile", objet="livre")),
    ("labo", "SCIENTIFIQUE", "ETUDIANT", dict(pose="tient", face="rire", objet="fiole"), dict(pose="panique", face="choc")),
    ("village", "PAYSAN", "CHEVALIER", dict(pose="haussement", face="gene"), dict(pose="tient", face="fier", objet="epee")),
    ("temple", "ROMAIN", "SULTAN", dict(pose="salut", face="content"), dict(pose="explique", face="neutre")),
    ("foret", "DETECTIVE", "CAPUCHE", dict(pose="tient", face="suspect", objet="loupe"), dict(pose="neutre", face="peur")),
    ("espace", "EXPLORATEUR", "SCIENTIFIQUE", dict(pose="montre", face="etoile"), dict(pose="neutre", face="choc")),
    ("plage_soir", "TATA", "TONTON", dict(pose="hanches", face="enerve"), dict(pose="haussement", face="gene")),
    ("tribunal", "POLICIER", "FOURBE", dict(pose="pointe", face="enerve"), dict(pose="bras_croises", face="malin")),
    ("toit", "ETUDIANTE", "ETUDIANT", dict(pose="neutre", face="coeur"), dict(pose="neutre", face="content")),
    ("parc_soir", "ADA", "MAMIE", dict(pose="salut", face="rire"), dict(pose="neutre", face="content")),
]
D_SC = 1.25
t = kit.T_HOOK
plans = [kit.accroche(["NOUVEAU MOTEUR", "DUO PIXEL"], kit.photo("rue", "ADO", face="content"), THEME)]
parle = []
for k, (bg, a, b, ga, gb) in enumerate(SCENES):
    t0, t1 = t, t + D_SC
    parle += [(a, t0 + 0.1, t0 + D_SC * 0.48), (b, t0 + D_SC * 0.52, t1 - 0.05)]
    sh = kit.duo_plan(t0, t1, bg, a, b, g=ga, d=gb)
    sh.tags = [(bg, 0, 99)]
    plans.append(sh)
    t = t1
    if bg == "classe":                                   # un gros plan avec bulle
        plans.append(kit.gros_plan(t, t + 1.2, "ENFANT", "classe", face="choc", bulle="!", pose="panique"))
        plans[-1].tags = [("gros_plan + bulle", 0, 99)]
        t += 1.2
    if bg == "snack":                                    # une marche
        plans.append(kit.marche(t, t + 1.6, "ADA", "rue_soir", 200, 860, face="content"))
        plans[-1].tags = [("marche (rue_soir)", 0, 99)]
        t += 1.6
    if bg == "salle_sport":                              # un tableau avec icônes
        dessin = kit.ecrit([(80, "ARGENT FACILE ?", 15, True), (196, "VRAI OU FAUX", 12, False)],
                           [("argent", 40, 104, 5), ("fleche_haut", 110, 104, 5), ("croix", 180, 104, 5)], style="ecran")
        plans.append(kit.tableau_plan(t, t + 1.6, dessin, bg="ecran_info", gauche="JOURNALISTE", droite="EXPERT",
                                      g=dict(pose="question"), d=dict(pose="pointe")))
        plans[-1].tags = [("tableau : ecran_info", 0, 99)]
        t += 1.6
    if bg == "foret":                                    # un gros plan avec pensée
        plans.append(kit.gros_plan(t, t + 1.3, "DETECTIVE", "foret", face="suspect", pensee="crane"))
        plans[-1].tags = [("bulle de pensée", 0, 99)]
        t += 1.3
plans.append(kit.fin(t, t + 2.2, "parc", "ADO", "PAPI", THEME))
DUR = t + 2.2
VID = pxv.Video(Silence(DUR, parle), plans, music=MUSIC, music_gain=0.10, theme=THEME)

if __name__ == "__main__":
    kit.rendu(VID, "Demo moteur duo", OUT)
