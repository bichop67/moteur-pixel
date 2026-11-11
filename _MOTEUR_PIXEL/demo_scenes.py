# DÉMO « MISE EN SCÈNE » : un chapitre par fonction, avec le nom de la commande à l'écran (sans voix).
# python demo_scenes.py sheet planche.png | still 12.5 image.png | frames i n | video
import os
import kit, pxv, scene
from scene import Scene, legende
from pxv import Silence, Theme

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CATALOGUE")
MUSIC = pxv.BASE + "/_MUSIQUES/FOND/fond_espoir.mp3"
THEME = Theme(bandeau="MISE EN SCÈNE", bandeau_fond=(44, 40, 70), bandeau_accent=(120, 230, 255), bandeau_contour=(20, 16, 40))
plans, parle = [], []
t = 0.0


def ajoute(sh, d):
    global t
    plans.append(sh)
    t += d


# 0. titre
ajoute(scene.carton(t, t + 2.6, "MISE EN SCÈNE", sous="COMMENT ÇA MARCHE"), 2.6)

# 1. entrer en marchant
D = 4.4; sc = Scene(t, t + D, "rue")
papi = sc.role("PAPI", x=780); ado = sc.role("ADO", x=320)
ado.entre(0.3, 2.3, depuis="gauche"); ado.a(2.5, pose="salut", face="content"); papi.a(2.7, pose="salut", face="content")
ado.parle(2.6, 3.4); papi.parle(3.5, 4.2)
sc.passants(n=3, y=1300, k=5); sc.ambiance("amb_foule_murmure", 0.25)
sc.legende("ENTRER EN MARCHANT", 'ado.entre(0.3, 2.3)   ado.a(2.5, pose="salut")')
ajoute(sc.plan(), D)

# 2. se retourner, sortir
D = 4.4; sc = Scene(t, t + D, "parc")
ada = sc.role("ADA", x=540); mamie = sc.role("MAMIE", x=840)
ada.a(0.2, face="content"); ada.tourne(1.0); ada.a(1.0, face="clin"); ada.sort(1.6, 4.2, vers="gauche")
mamie.a(1.2, pose="salut", face="content"); sc.oiseaux(y=420)
sc.legende("SE RETOURNER, SORTIR", 'ada.tourne(1.0)   ada.sort(1.6, 4.2, vers="gauche")')
ajoute(sc.plan(), D)

# 3. s'asseoir
D = 4.8; sc = Scene(t, t + D, "cuisine")
sc.meuble("chaise", 700, regard="gauche"); sc.meuble("table", 700, regard="gauche")
maman = sc.role("MAMAN", x=930, regard="gauche"); enfant = sc.role("ENFANT", x=300)
maman.marche(0.2, 1.5, 700); maman.assoit(1.6); maman.a(1.7, pose="bras_croises", face="suspect")
enfant.a(2.1, pose="question", face="gene"); enfant.parle(2.2, 3.4)
sc.vapeur(332, 816)
sc.legende("S'ASSEOIR (CHAISE + TABLE)", 'sc.meuble("chaise", 700)   maman.assoit(1.6)')
ajoute(sc.plan(), D)

# 4. donner un objet
D = 4.6; sc = Scene(t, t + D, "snack")
epicier = sc.role("EPICIER", x=780, pose="tient", objet="sac_courses"); ado = sc.role("ADO", x=320)
sc.donne(1.3, 2.1, epicier, ado, "sac_courses")
ado.a(2.2, face="content"); epicier.a(2.4, pose="pouce", face="rire")
sc.effet(ado, 2.3, 4.4, "brille")
sc.legende("DONNER UN OBJET", 'sc.donne(1.3, 2.1, epicier, ado, "sac_courses")')
ajoute(sc.plan(), D)

# 5-7. réactions
for (bg, a_, b_, fa, fb, ea, eb, titre, code) in (
        ("salon", "TATA", "TONTON", dict(face="coeur"), dict(face="enerve", pose="bras_croises"), "coeurs", "colere",
         "RÉACTIONS", 'sc.effet(tata, 0.3, 3.6, "coeurs")   "colere"'),
        ("chambre_ado", "GAMER", "ENFANT", dict(face="etoile", pose="index"), dict(face="dodo"), "idee", "zzz",
         "RÉACTIONS (2)", '"idee"   "zzz"'),
        ("classe", "ETUDIANT", "PROF", dict(face="pleure"), dict(face="gene", pose="facepalm"), "larmes", "points",
         "RÉACTIONS (3)", '"larmes"   "points"   (+ goutte, etoiles, notes, brille)')):
    D = 3.8; sc = Scene(t, t + D, bg)
    ra = sc.role(a_, x=300, **fa); rb = sc.role(b_, x=780, **fb)
    sc.effet(ra, 0.3, D - 0.2, ea); sc.effet(rb, 0.3, D - 0.2, eb)
    sc.legende(titre, code)
    ajoute(sc.plan(), D)

# 8. une porte qui s'ouvre
D = 5.0; sc = Scene(t, t + D, "entree_nuit")
sc.porte(410, 1272, t_ouvre=0.4, t_ferme=2.7)
ado = sc.role("ADO", x=410, y=1272); maman = sc.role("MAMAN", x=800, pose="hanches", face="suspect")
ado.cache(); ado.apparait(0.8, 1.2); ado.marche(1.2, 2.6, 300, 1340); ado.regarde(2.7, "droite"); ado.a(2.7, face="gene")
sc.effet(ado, 2.8, 4.8, "goutte"); maman.parle(3.0, 4.4)
sc.legende("UNE PORTE QUI S'OUVRE", 'sc.porte(410, 1272, t_ouvre=0.4)   ado.apparait(0.8)')
ajoute(sc.plan(), D)

# 9. pluie, voitures, passants
D = 4.6; sc = Scene(t, t + D, "rue_nuit")
sc.role("CAPUCHE", x=320, face="blase"); sc.role("ADA", x=780, pose="telephone", face="bas")
sc.passants(n=3, y=1300, k=5, seed=4); sc.voitures(phares=True); sc.pluie(); sc.ambiance("amb_pluie", 0.6)
sc.legende("PLUIE, VOITURES, PASSANTS", "sc.pluie()   sc.voitures()   sc.passants()")
ajoute(sc.plan(), D)

# 10. neige
D = 4.0; sc = Scene(t, t + D, "parc_nuit")
enf = sc.role("ENFANT", x=320, face="rire"); sc.role("PAPI", x=780, face="content")
enf.sautille(0.4, 3.6); sc.neige()
sc.legende("NEIGE", "sc.neige()   enfant.sautille(0.4, 3.6)")
ajoute(sc.plan(), D)

# 11. feuilles et oiseaux
D = 4.0; sc = Scene(t, t + D, "parc_soir")
sc.role("ADA", x=320, face="content"); m = sc.role("MAMIE", x=820, face="calme")
m.marche(0.4, 3.4, 700); sc.feuilles(); sc.oiseaux(y=360)
sc.legende("FEUILLES, OISEAUX", "sc.feuilles()   sc.oiseaux()")
ajoute(sc.plan(), D)

# 12. feu de camp, lucioles
D = 4.6; sc = Scene(t, t + D, "foret")
sc.role("DETECTIVE", x=300, face="suspect"); sc.role("CAPUCHE", x=790, face="peur")
sc.feu(540, 1490); sc.lucioles(); sc.ambiance("amb_feu_camp", 0.6)
sc.legende("FEU QUI DANSE, LUCIOLES", "sc.feu(540, 1490)   sc.lucioles()")
ajoute(sc.plan(), D)

# 13. la lumière change
D = 5.0; sc = Scene(t, t + D, "cuisine")
mm = sc.role("MAMAN", x=300, pose="tient", objet="tasse", face="content"); pp = sc.role("PAPA", x=780)
sc.vapeur(332, 816); sc.lumiere(2.0, "cuisine_nuit", 1.6); pp.a(2.2, pose="index", face="malin"); pp.parle(2.3, 3.6)
sc.legende("LA LUMIÈRE CHANGE", 'sc.lumiere(2.0, "cuisine_nuit")   sc.vapeur(332, 816)')
ajoute(sc.plan(), D)

# 14. meubles
D = 4.6; sc = Scene(t, t + D, "salon")
sc.meuble("plante", 110); sc.meuble("tele", 330); sc.ecran(190, 1076, 410, 1205); sc.meuble("lampe", 990)
pa = sc.role("PAPI", x=780, meuble="fauteuil", face="dodo"); sc.effet(pa, 0.4, 4.4, "zzz")
sc.legende("MEUBLES : FAUTEUIL, TÉLÉ, LAMPE", 'sc.meuble("tele", 330)   role(..., meuble="fauteuil")')
ajoute(sc.plan(), D)

# 15. SMS à l'écran
D = 6.4
sh = scene.sms(t, t + D, "MAMAN", [(0.7, "lui", "T'es où ?"), (1.9, "lui", "Réponds stp"), (3.2, "moi", "J'arrive dans 5 min"),
                                   (4.6, "lui", "Ok. Fais attention.")], bg="chambre_ado", avatar="MAMAN")
sh.ecran.append(legende("SMS À L'ÉCRAN", 'scene.sms(t0, t1, "MAMAN", [(0.7, "lui", "T\'es où ?"), …])', y=1790))
ajoute(sh, D)

# 16. notification
D = 4.4; sc = Scene(t, t + D, "bureau")
sc.role("ETUDIANTE", x=300, pose="telephone", face="bas"); sc.role("PATRON", x=780, pose="bras_croises", face="suspect")
sc.notification(0.8, 3.8, "MAMAN", "Tu rentres à quelle heure ?")
sc.legende("NOTIFICATION", 'sc.notification(0.8, 3.8, "MAMAN", "Tu rentres…")', y=1790)
ajoute(sc.plan(), D)

# 17. la caméra suit celui qui parle
D = 6.6; sc = Scene(t, t + D, "studio")
pod = sc.role("PODCASTEUR", place="gauche"); jou = sc.role("JOURNALISTE", place="droite")
pod.a(0.3, pose="explique"); pod.parle(0.3, 2.3); jou.a(2.6, pose="explique"); jou.parle(2.6, 4.6); pod.parle(4.9, 6.2)
sc.camera([(0.0, 1.1, (540, 1060)), (0.9, 1.16, (420, 1040)), (3.0, 1.16, (660, 1040)), (5.3, 1.16, (420, 1040)), (6.6, 1.12, (540, 1050))])
sc.legende("LA CAMÉRA SUIT CELUI QUI PARLE", "sc.camera([(0, 1.1, (540, 1060)), (0.9, 1.16, (420, 1040)), …])")
ajoute(sc.plan(), D)

# 18. par-dessus l'épaule
D = 4.6
sh = scene.epaule(t, t + D, "rue", "ADO", "PAPI", st_face=dict(pose="explique", face="content"))
parle.append(("PAPI", t + 0.4, t + 3.9))
sh.ecran.append(legende("PLAN PAR-DESSUS L'ÉPAULE", 'scene.epaule(t0, t1, "rue", "ADO", "PAPI")'))
ajoute(sh, D)

# 19. plan d'ensemble
D = 4.4
sc = scene.etablissement(t, t + D, "rue_nuit", cible=(800, 880), zoom=1.3)
sc.pluie(); sc.ambiance("amb_pluie", 0.5)
sc.legende("PLAN D'ENSEMBLE", 'scene.etablissement(t0, t1, "rue_nuit", cible=(800, 880))')
ajoute(sc.plan(), D)

# 20. carton de temps
D = 3.2
sh = scene.carton(t, t + D, "LE LENDEMAIN…", sous="8 H 00")
sh.ecran.append(legende("CARTON DE TEMPS", 'scene.carton(t0, t1, "LE LENDEMAIN…", sous="8 H 00")', y=1790))
ajoute(sh, D)

# 21. fin
ajoute(scene.carton(t, t + 3.0, "À TOI DE JOUER", sous="TOUT EST DANS LISEZMOI_MOTEUR.TXT"), 3.0)

VID = pxv.Video(Silence(t, parle), plans, music=MUSIC, music_gain=0.06, theme=THEME)

if __name__ == "__main__":
    kit.rendu(VID, "Demo 2 - mise en scene", OUT)
