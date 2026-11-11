# DÉMO 3 « LES NOUVEAUTÉS » : chaque amélioration du moteur, avec son nom et la commande à l'écran (sans voix).
# python demo_nouveautes.py sheet | tout | still 12.5 image.png
import os
import kit, pxv, scene
from scene import Scene, legende
from pxv import Theme

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CATALOGUE")
MUSIC = pxv.BASE + "/_MUSIQUES/FOND/fond_espoir.mp3"
THEME = Theme(bandeau="NOUVEAUTÉS", bandeau_fond=(44, 40, 70), bandeau_accent=(120, 230, 255), bandeau_contour=(20, 16, 40))
plans, repl = [], []
t = 0.0


def ajoute(sh, d):
    global t
    plans.append(sh)
    t += d


def dit(who, txt, u, d=None):
    """Réplique muette (sous-titre + bouche qui suit les lettres) à l'instant t + u."""
    repl.append((who, txt, t + u, d))


# 0. titre
ajoute(scene.carton(t, t + 2.6, "NOUVEAUTÉS", sous="DU MOTEUR PIXEL"), 2.6)

# 1. ombres + feu qui éclaire
D = 4.8; sc = Scene(t, t + D, "foret")
det = sc.role("DETECTIVE", x=300, face="suspect"); cap = sc.role("CAPUCHE", x=790, face="peur")
sc.feu(540, 1490); sc.lucioles(); sc.ambiance("amb_feu_camp", 0.5)
sc.camera([(0.0, 1.0, (540, 1000)), (D, 1.14, (540, 1120))])
sc.legende("OMBRES + LUMIÈRE DU FEU", "automatique (Theme : ombres, lumiere)")
ajoute(sc.plan(), D)

# 2. lampadaires : la lumière change quand on marche
D = 5.0; sc = Scene(t, t + D, "rue_nuit")
ada = sc.role("ADA", x=120, pose="telephone", objet="telephone", face="bas")
ada.marche(0.2, 4.6, 960)
sc.voitures(phares=True)
sc.camera([(0.0, 1.18, (330, 1080)), (4.6, 1.18, (760, 1080))])
sc.legende("LA LUMIÈRE SUIT LA MARCHE", "lampadaire + néon du décor (automatique)")
ajoute(sc.plan(), D)

# 3. gestes en douceur
D = 5.6; sc = Scene(t, t + D, "classe")
prof = sc.role("PROF", x=540, regard="droite", face="content")
for u, p in ((0.8, "explique"), (1.8, "pointe"), (2.8, "bras_croises"), (3.8, "menton"), (4.7, "victoire")):
    prof.a(u, pose=p)
dit("PROF", "Alors… regardez bien… voilà… hmm… parfait !", 0.7, 4.6)
sc.camera([(0.0, 1.85, (540, 1010)), (D, 1.9, (540, 1010))])
sc.legende("GESTES EN DOUCEUR", 'prof.a(1.8, pose="pointe")   (images intermédiaires)')
ajoute(sc.plan(), D)

# 4. marche en 8 images
D = 4.8; sc = Scene(t, t + D, "rue")
liv = sc.role("LIVREUR", x=-150, pose="tient", objet="sac_courses")
liv.marche(0.1, 4.7, 1230)
sc.camera([(0.0, 1.6, (240, 1060)), (4.7, 1.6, (840, 1060))])
sc.oiseaux(y=360)
sc.legende("MARCHE EN 8 IMAGES + OMBRE", "livreur.marche(0.1, 4.7, 1230)")
ajoute(sc.plan(), D)

# 5. la bouche suit les sons, sourcils sur « ! » et « ? », petit hochement
D = 6.4; sc = Scene(t, t + D, "salon")
ada = sc.role("ADA", x=330, face="content"); papa = sc.role("PAPA", x=760, face="neutre")
dit("ADA", "Papa ! Tu as vu MA photo ?!", 0.4, 2.4)
dit("PAPA", "Mmm… oui. Bof… et alors ?", 3.2, 2.6)
ada.a(0.4, pose="explique"); ada.a(2.9, pose="neutre", face="suspect"); papa.a(3.2, pose="haussement", face="blase")
sc.camera([(0.0, 1.9, (330, 1000)), (2.7, 1.9, (330, 1000)), (3.5, 1.9, (760, 1000)), (D, 1.9, (760, 1000))])
sc.legende("LA BOUCHE SUIT LES SONS", "A, O, E, M, F + sourcils sur « ! » et « ? »")
ajoute(sc.plan(), D)

# 6. ils regardent celui qui parle
D = 6.6; sc = Scene(t, t + D, "cuisine")
ado = sc.role("ADO", x=220); maman = sc.role("MAMAN", x=540, y=1360, regard="droite", pose="hanches", face="suspect")
tata = sc.role("TATA", x=860)
dit("ADO", "C'est pas moi !", 0.5, 1.4)
dit("TATA", "Ah bon ? Et ça, c'est qui ?", 2.3, 1.9)
dit("ADO", "…Le chat ?", 4.6, 1.3)
ado.a(0.5, pose="panique", face="peur"); tata.a(2.3, pose="pointe", face="malin"); ado.a(4.6, pose="haussement", face="gene")
sc.legende("ILS REGARDENT CELUI QUI PARLE", "sc.regard_parleur(dialogue)", y=1680)
_sc_regard = sc
ajoute(sc.plan(), D)

# 7. relief : le ciel lointain bouge moins que la scène
D = 5.0; sc = Scene(t, t + D, "toit_soir")
sc.role("GAMER", x=330, face="calme"); sc.role("ETUDIANT", x=760, face="content")
sc.camera([(0.0, 1.4, (330, 1000)), (D, 1.4, (760, 1000))])
sc.oiseaux(y=300)
sc.legende("RELIEF : LE LOINTAIN BOUGE MOINS", "automatique (Theme : parallaxe)")
ajoute(sc.plan(), D)

# 8. animaux (1)
D = 5.6; sc = Scene(t, t + D, "parc")
enf = sc.role("ENFANT", x=200, face="rire"); chien = sc.role("CHIEN", x=-120)
chat = sc.role("CHAT", x=830, pose="assis"); sc.role("PIGEON", x=640, y=1350)
chien.marche(0.2, 2.6, 470); chien.a(2.7, pose="assis"); enf.sautille(2.8, 5.2)
chat.a(3.4, pose="couche")
sc.oiseaux(y=380)
sc.legende("ANIMAUX", 'sc.role("CHIEN", x=…)   chien.marche(…)   pose="assis"')
ajoute(sc.plan(), D)

# 9. animaux (2)
D = 5.0; sc = Scene(t, t + D, "desert_soir")
cha = sc.role("CHAMEAU", x=1250, k=6); voy = sc.role("VOYAGEUR", x=1350)
cha.marche(0.2, 4.6, 640); voy.marche(0.2, 4.6, 830)
sc.ambiance("amb_vent_desert", 0.35); sc.son(1.0, "an_cloches_chameau", 0.12, 3.0)
sc.legende("ANIMAUX (2)", "chameau, cheval, âne, mouton, chèvre, chat, chien, pigeon")
ajoute(sc.plan(), D)

D = 4.4; sc = Scene(t, t + D, "village")
sc.role("MOUTON", x=230, pose="mange"); sc.role("CHEVRE", x=420); m2 = sc.role("MOUTON", x=650, pose="debout")
sc.role("CHEVAL", x=900, k=6); sc.role("PAYSAN", x=540, y=1300, face="content")
m2.marche(1.0, 3.8, 560); sc.son(0.8, "an_mouton", 0.12); sc.son(2.6, "an_chevre", 0.10)
sc.legende("ANIMAUX (3)", 'pose : "debout", "assis", "couche", "mange"')
ajoute(sc.plan(), D)

# 10. nouveaux décors
for bg, nom in (("aeroport", "AÉROPORT"), ("avion_nuit", "AVION (NUIT)"), ("stade_nuit", "STADE (NUIT)"),
                ("marche_soir", "MARCHÉ (SOIR)"), ("prison_barreaux", "PRISON (BARREAUX)"), ("couloir_ecole", "COULOIR D'ÉCOLE")):
    D = 2.2; sc = Scene(t, t + D, bg)
    if bg == "avion_nuit":
        sc.role("PAPI", place="gauche", face="dodo"); sc.role("ADA", place="droite", pose="telephone", objet="telephone")
    elif bg == "prison_barreaux":
        sc.role("FOURBE", x=540, pose="bras_croises", face="blase")
    elif bg == "stade_nuit":
        sc.role("FOOTEUX", x=420, pose="victoire", face="rire"); sc.role("COACH", x=760, pose="pouce", face="content")
    elif bg == "marche_soir":
        sc.role("VENDEUSE", x=330, pose="tient", objet="sac_courses", face="content"); sc.role("MAMIE", x=760, face="content")
    elif bg == "couloir_ecole":
        sc.role("ETUDIANTE", x=330, pose="tient", objet="livre"); sc.role("ADO", x=760, face="malin")
    else:
        sc.passants(n=3)
    sc.camera([(0.0, 1.0, (540, 960)), (D, 1.06, (540, 1000))])
    sc.legende("NOUVEAUX DÉCORS", nom)
    ajoute(sc.plan(), D)

# 11. scénario texte, 16:9, miniatures
ajoute(scene.carton(t, t + 3.2, "ÉCRIS TON SCÉNARIO", sous="LA VIDÉO SE FAIT TOUTE SEULE"), 3.2)
ajoute(scene.carton(t, t + 3.0, "AUSSI EN 16:9", sous="+ MINIATURES AUTOMATIQUES"), 3.0)

D_TOT = t + 0.3
DLG = kit.Calee(repl, D_TOT)
_sc_regard.regard_parleur(DLG)
for i, sh in enumerate(plans):                      # le plan « regard » doit être refait avec les regards ajoutés
    if sh.bg == "cuisine":
        plans[i] = _sc_regard.plan()
plans[-1].t1 = D_TOT
VID = pxv.Video(DLG, plans, music=MUSIC, music_gain=0.06, theme=THEME)

if __name__ == "__main__":
    kit.rendu(VID, "Demo 3 - nouveautes", OUT)
