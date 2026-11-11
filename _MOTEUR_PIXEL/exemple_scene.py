# EXEMPLE DE VRAIE SCÈNE : « Rentré trop tard » (sketch de 40 s, en maquette : sous-titres sans voix).
# Montre comment on enchaîne : plan d'ensemble sous la pluie → la porte s'ouvre → la mère attend, assise, en colère
# → l'écran des SMS → l'ado se justifie (pensée) → il lui tend le pain → elle craque (cœurs) → fin.
# python exemple_scene.py sheet planche.png | frames i n | video      (avec de vraies voix : voir modele_duo.py)
import os
import kit, pxv, scene
from scene import Scene

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CATALOGUE")
MUSIC = pxv.BASE + "/_MUSIQUES/FOND/fond_espoir.mp3"
THEME = pxv.Theme(bandeau=None, grain=4.0, cotes={"ADO": "right", "MAMAN": "left"})
A, M = "ADO", "MAMAN"

REPLIQUES = [
    (M, "Il est quelle heure, là ?"),
    (A, "Euh… un peu tard ?"),
    (M, "Je t'ai envoyé quatre messages !"),
    (A, "J'avais plus de batterie, je te jure !"),
    (M, "Et pourquoi t'es trempé ?"),
    (A, "Je suis allé te chercher ton pain préféré."),
    (M, "… Bon. Va te sécher. Et charge ton téléphone !"),
    (A, "Oui chef !"),
]
# silences voulus : 7,6 s avant la 1re réplique (plan d'ensemble + entrée), 3,2 s avant la 4e (écran des SMS)
D = kit.dialogue(OUT + "/voix_exemple_scene/", "SCENE01", REPLIQUES, avant={0: 7.6, 3: 3.2})
kit.allonge(D, 1.8)                                        # le dernier plan dure un peu plus (abonne-toi)
L = D.lines
t = lambda k: L[k]["t0"]
te = lambda k: L[k]["t1"] + 0.08
plans = []

# 1. plan d'ensemble : la rue sous la pluie, la caméra s'approche d'une fenêtre allumée ; « 23 H 47 »
T1 = 3.6
sc = scene.etablissement(0.0, T1, "rue_nuit", cible=(300, 640), zoom=1.3)
sc.pluie(); sc.voitures(phares=True, periode=9.0); sc.ambiance("amb_pluie", 0.7)
heure = pxv.big_title([("23 H 47", (255, 255, 255))], size=80)
sc.texte(lambda img, u: img.alpha_composite(scene._fade(heure, scene._env(u, T1, 0.5, 0.5)), (int(540 - heure.width / 2), 1500)))
plans.append(sc.plan(band=False))

# 2. l'entrée : la porte s'ouvre, il entre tout mouillé, traverse et sort à droite
T2 = 3.6
sc = Scene(T1, T1 + T2, "entree_nuit")
sc.porte(410, 1272, t_ouvre=0.3, t_ferme=2.2)
ado = sc.role(A, x=410, y=1272, face="gene")
ado.cache(); ado.apparait(0.6, 1.0); ado.marche(1.0, 3.5, 1200, 1340)
sc.effet(ado, 1.0, 3.4, "goutte"); sc.ambiance("amb_pluie", 0.25)          # la pluie s'entend encore, dehors
plans.append(sc.plan(band=False))

# 3. la cuisine : maman assise, bras croisés ; il entre par la gauche ; répliques 0 à 2 ; la caméra suit qui parle
t3 = T1 + T2
sc = Scene(t3, te(2), "cuisine_nuit")
sc.meuble("chaise", 780, regard="gauche"); sc.meuble("table", 780, regard="gauche")
maman = sc.role(M, x=780, regard="gauche", assis=True, pose="bras_croises", face="enerve")
ado = sc.role(A, x=320, face="gene")
ado.entre(0.0, 1.4, depuis="gauche")
sc.effet(maman, 0.6, te(0) - t3, "colere")
ado.a(t(1) - t3, pose="question", face="gene"); sc.effet(ado, t(1) - t3, te(1) - t3, "goutte")
maman.a(t(2) - t3, pose="index", face="enerve")
sc.suit(D, A, M, zoom=1.08, ecart=90)
plans.append(sc.plan(band=False))

# 4. l'écran du téléphone : les 4 messages de maman (pendant le silence avant la réplique 3)
plans.append(scene.sms(te(2), t(3), "MAMAN", [(0.3, "lui", "T'es où ?"), (0.9, "lui", "Réponds !"),
                                              (1.5, "lui", "Je m'inquiète…"), (2.1, "lui", "Appelle-moi.")],
                       bg="cuisine_nuit", heure="23:48", avatar=M))

# 5. gros plan : il se justifie (pensée : batterie vide)
plans.append(kit.gros_plan(t(3), te(3), A, "cuisine_nuit", face="gene", pose="haussement", pensee="batterie"))

# 6. retour au plan large : elle se lève ; il lui tend le pain ; elle craque
t6 = te(3)
sc = Scene(t6, te(6), "cuisine_nuit")
sc.meuble("chaise", 780, regard="gauche"); sc.meuble("table", 780, regard="gauche")
maman = sc.role(M, x=780, regard="gauche", assis=True, pose="bras_croises", face="enerve")
ado = sc.role(A, x=320, pose="tient", objet="sac_courses", face="gene")
maman.leve(t(4) - t6 - 0.2); maman.a(t(4) - t6 - 0.2, pose="hanches", face="suspect")
ado.marche(t(5) - t6, t(5) - t6 + 1.0, 470)
sc.donne(t(5) - t6 + 1.3, t(5) - t6 + 2.0, ado, maman, "sac_courses")
ado.a(t(5) - t6 + 2.1, face="content")
maman.a(t(6) - t6, face="content"); sc.effet(maman, t(6) - t6, te(6) - t6, "coeurs")
sc.suit(D, A, M, zoom=1.08, ecart=90)
plans.append(sc.plan(band=False))

# 7. fin : « Oui chef ! », ils rient, abonne-toi
t7 = te(6)
sc = Scene(t7, D.dur, "cuisine_nuit")
sc.meuble("chaise", 780, regard="gauche"); sc.meuble("table", 780, regard="gauche")
maman = sc.role(M, x=780, regard="gauche", pose="tient", objet="sac_courses", face="content")
ado = sc.role(A, x=470, pose="salut", face="content")
ado.rit(0.8, D.dur - t7); maman.rit(1.0, D.dur - t7)
sc.texte(kit.cta(THEME))
sc.camera([(0.0, 1.06, (560, 1080)), (D.dur - t7, 1.1, (580, 1070))])
plans.append(sc.plan(band=False))

VID = pxv.Video(D, plans, music=MUSIC, music_gain=0.06, theme=THEME)

if __name__ == "__main__":
    kit.rendu(VID, "Exemple - scene complete", OUT, code="SCENE01", voix=OUT + "/voix_exemple_scene/", repliques=REPLIQUES)
