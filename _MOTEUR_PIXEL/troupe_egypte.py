# PERSONNAGES DE L'ÉGYPTE ANCIENNE ET DE MADYAN (film « L'histoire du prophète Moussa », épisode 14).
# Ici, uniquement des gens ordinaires. Les prophètes et les figures vénérées (Moussa, Haroun, sa mère, sa sœur, Asiya,
# le vieil homme de Madyan et ses filles…) ne sont JAMAIS dessinés : ce sont des orbes (film.py).
# S'utilisent dans les scénarios comme les autres persos (PHARAON place 600, SOLDAT entre à gauche, tient la lance…).
from cast import nouveau

LIN = (236, 228, 206)             # lin blanc d'Égypte
LIN2 = (222, 210, 180)            # lin plus ordinaire
TERRE = (150, 118, 82)            # habits de travail (Israélites, bergers)

# ---------------------------------------------------------------- le palais
nouveau("PHARAON", taille="grand", peau="halee", cheveux="rase", barbe="postiche", couleur_barbe=(40, 30, 36),
        haut="robe_longue", couleur=LIN, couleur2="or", chapeau="nemes", acc=["collier", "ceinture", "devanteau"],
        couleurs_acc=dict(ceinture="or"), chaussures="sandales", cadre=(226, 182, 70),
        description="Pharaon : coiffe royale rayée or et bleu, grand collier, barbe postiche (objet='crosse')")
nouveau("HAMAN", taille="grand", peau="halee", cheveux="rase", haut="robe_longue", couleur=(44, 56, 96), couleur2="or",
        chapeau="khat", couleur_chapeau=(30, 36, 60), acc=["collier", "ceinture"],
        couleurs_acc=dict(collier=(200, 160, 70), ceinture="or"), chaussures="sandales", corpulence="mince",
        cadre=(90, 110, 190), description="Haman, le ministre de Pharaon : robe bleu nuit, coiffe sombre")
nouveau("CONSEILLER", taille="adulte", peau="mate", age="vieux", cheveux="rase", barbe="courte", couleur_barbe="gris",
        haut="robe_longue", couleur=(120, 60, 50), couleur2="or", chapeau="khat", couleur_chapeau=LIN, acc=["collier"],
        couleurs_acc=dict(collier=(190, 150, 70)), chaussures="sandales", corpulence="fort", cadre=(170, 90, 70),
        description="Notable du conseil de Pharaon, robe brique")
nouveau("CONSEILLER2", taille="grand", peau="halee", cheveux="rase", haut="robe_longue", couleur=(56, 100, 90),
        couleur2="or", chapeau="khat", couleur_chapeau=(214, 200, 160), acc=["collier"],
        couleurs_acc=dict(collier=(190, 150, 70)), chaussures="sandales", cadre=(70, 150, 130),
        description="Notable du conseil de Pharaon, robe vert sombre")
nouveau("DEVIN", taille="adulte", peau="halee", age="vieux", cheveux="vieux", couleur_cheveux="blanc", barbe="longue",
        couleur_barbe="blanc", haut="robe_longue", couleur=(70, 40, 70), couleur2=(150, 110, 60), acc=["collier"],
        couleurs_acc=dict(collier=(150, 110, 60)), chaussures="sandales", cadre=(150, 90, 160),
        description="Le devin de Pharaon (vieil homme, robe prune)")
nouveau("HERAUT", taille="grand", peau="mate", cheveux="court", haut="tunique", couleur=LIN, bas="jupe",
        chapeau="khat", couleur_chapeau=(170, 50, 50), acc=["collier"], couleurs_acc=dict(collier=(190, 150, 70)),
        chaussures="sandales", cadre=(200, 70, 60), description="Le crieur de Pharaon")
nouveau("SOLDAT", taille="grand", peau="halee", cheveux="court", haut="tunique", couleur=LIN, bas="jupe",
        chapeau="khat", couleur_chapeau=(196, 160, 96), rayures=True, couleur_rayures=(236, 228, 206), acc=["collier"], couleurs_acc=dict(collier=(150, 110, 60)),
        chaussures="sandales", corpulence="fort", cadre=(190, 140, 70), description="Soldat de Pharaon (objet='lance')")
nouveau("SOLDAT2", taille="grand", peau="mate", cheveux="court", haut="tunique", couleur=LIN2, bas="jupe",
        chapeau="khat", couleur_chapeau=(60, 80, 130), rayures=True, couleur_rayures=(236, 228, 206), acc=["collier"], couleurs_acc=dict(collier=(150, 110, 60)),
        chaussures="sandales", cadre=(80, 110, 170), description="Soldat de Pharaon, coiffe bleue (objet='lance')")
nouveau("GARDE", taille="grand", peau="foncee", cheveux="rase", haut="tunique", couleur=LIN, bas="jupe",
        chapeau="khat", couleur_chapeau=(40, 40, 50), acc=["collier"], couleurs_acc=dict(collier=(190, 150, 70)),
        chaussures="sandales", corpulence="fort", cadre=(120, 120, 140), description="Garde du palais (objet='lance')")
nouveau("CONTREMAITRE", taille="grand", peau="halee", cheveux="rase", barbe="3j", haut="tunique", couleur=LIN2, bas="jupe",
        chapeau="khat", couleur_chapeau=(130, 60, 40), chaussures="sandales", corpulence="fort", cadre=(160, 80, 50),
        description="Contremaître égyptien du chantier de briques (objet='fouet')")
nouveau("MAGICIEN", taille="grand", peau="mate", cheveux="rase", barbe="bouc", couleur_barbe="noir", haut="robe_longue",
        couleur=(40, 30, 50), couleur2=(140, 60, 160), acc=["collier", "ceinture"],
        couleurs_acc=dict(collier=(150, 110, 60), ceinture=(140, 60, 160)), chaussures="sandales", cadre=(140, 60, 160),
        description="Magicien de Pharaon, robe noire et violette")
nouveau("MAGICIEN2", taille="adulte", peau="halee", age="vieux", cheveux="rase", barbe="longue", couleur_barbe="gris",
        haut="robe_longue", couleur=(30, 34, 50), couleur2=(60, 130, 140), acc=["collier"],
        couleurs_acc=dict(collier=(60, 130, 140)), chaussures="sandales", cadre=(60, 130, 140),
        description="Magicien de Pharaon (âgé), robe sombre, collier turquoise")
nouveau("MAGICIEN3", taille="grand", peau="foncee", cheveux="rase", haut="robe_longue", couleur=(60, 24, 30),
        couleur2=(200, 150, 60), acc=["collier", "ceinture"], couleurs_acc=dict(collier=(200, 150, 60), ceinture=(200, 150, 60)),
        chaussures="sandales", corpulence="fort", cadre=(180, 70, 60), description="Magicien de Pharaon, robe grenat")
nouveau("SERVANTE", genre="f", peau="halee", haut="robe_longue", couleur=LIN, couleur2=(60, 130, 140), chapeau="hijab",
        couleur_chapeau=LIN2, acc=["collier"], couleurs_acc=dict(collier=(60, 130, 140)), chaussures="sandales",
        cadre=(60, 150, 150), description="Servante du palais, voile et robe de lin")
nouveau("SERVANTE2", genre="f", peau="mate", haut="robe_longue", couleur=(214, 196, 160), couleur2=(170, 60, 60),
        chapeau="hijab", couleur_chapeau=(196, 150, 110), chaussures="sandales", cadre=(190, 100, 90),
        description="Servante du palais (2), voile ocre")
nouveau("CROYANT", taille="grand", peau="halee", age="vieux", cheveux="vieux", couleur_cheveux="gris", barbe="courte",
        couleur_barbe="gris", haut="robe_longue", couleur=LIN, couleur2=(60, 120, 90), chapeau="khat", couleur_chapeau=LIN,
        acc=["collier"], couleurs_acc=dict(collier=(60, 120, 90)), chaussures="sandales", cadre=(80, 160, 110),
        description="L'homme croyant de la famille de Pharaon (40:28), digne, robe blanche")

# ---------------------------------------------------------------- la ville et le chantier
nouveau("EGYPTIEN", taille="grand", peau="halee", cheveux="court", haut="tunique", couleur=LIN, bas="jupe",
        acc=["collier"], couleurs_acc=dict(collier=(150, 110, 60)), chaussures="sandales", corpulence="fort",
        cadre=(200, 150, 80), description="Un Égyptien (celui de la bagarre, 28:15)")
nouveau("EGYPTIEN2", taille="adulte", peau="mate", cheveux="rase", haut="tunique", couleur=LIN2, bas="jupe",
        chaussures="sandales", cadre=(170, 140, 100), description="Passant égyptien")
nouveau("EGYPTIENNE", genre="f", peau="halee", haut="robe_longue", couleur=LIN2, couleur2=(40, 84, 170), chapeau="hijab",
        couleur_chapeau=(160, 120, 90), chaussures="sandales", cadre=(150, 120, 90), description="Passante égyptienne voilée")
nouveau("NOURRICE", genre="f", peau="mate", haut="robe_longue", couleur=(226, 214, 186), couleur2=(150, 90, 50),
        chapeau="hijab", couleur_chapeau=(120, 70, 50), acc=["collier"], couleurs_acc=dict(collier=(190, 140, 60)),
        chaussures="sandales", corpulence="fort", cadre=(170, 110, 70), description="Nourrice égyptienne, voile brun")
nouveau("NOURRICE2", genre="f", peau="foncee", haut="robe_longue", couleur=(236, 226, 200), couleur2=(60, 110, 150),
        chapeau="hijab", couleur_chapeau=(70, 110, 140), chaussures="sandales", cadre=(80, 130, 170),
        description="Nourrice égyptienne, voile bleu")
nouveau("NOURRICE3", genre="f", peau="halee", age="vieux", haut="robe_longue", couleur=(200, 186, 160), couleur2=(120, 120, 80),
        chapeau="hijab", couleur_chapeau=(150, 150, 110), chaussures="sandales", cadre=(140, 140, 100),
        description="Vieille nourrice égyptienne, voile vert-gris")
nouveau("ISRAELITE", taille="adulte", peau="doree", cheveux="court", couleur_cheveux="brun", barbe="courte",
        couleur_barbe="brun", haut="tunique", couleur=TERRE, bas="jupe", chaussures="sandales", cadre=(160, 130, 90),
        description="Un Israélite (celui qui appelle à l'aide, 28:15 et 28:18)")
nouveau("ISRAELITE2", taille="adulte", peau="halee", age="vieux", cheveux="vieux", couleur_cheveux="gris", barbe="longue",
        couleur_barbe="gris", haut="tunique", couleur=(120, 100, 80), bas="jupe", chaussures="sandales",
        cadre=(140, 120, 100), description="Vieil Israélite")
nouveau("ISRAELITE3", taille="ado", peau="doree", cheveux="boucle", couleur_cheveux="brun", haut="tunique",
        couleur=(170, 140, 100), bas="jupe", chaussures="nus", cadre=(170, 140, 100), description="Jeune Israélite")
nouveau("ISRAELITE4", taille="grand", peau="mate", cheveux="court", barbe="courte", haut="tunique", couleur=(110, 90, 70),
        bas="jupe", chapeau="turban", bijou=False, couleur_chapeau=(200, 180, 140), chaussures="sandales", corpulence="fort",
        cadre=(130, 110, 80), description="Israélite au turban de toile")
nouveau("ISRAELITE_F", genre="f", peau="doree", haut="robe_longue", couleur=(150, 120, 90), couleur2=(110, 80, 60),
        chapeau="hijab", couleur_chapeau=(120, 90, 70), chaussures="sandales", cadre=(150, 110, 80),
        description="Femme israélite, voile brun")
nouveau("MESSAGER", taille="adulte", peau="halee", cheveux="court", barbe="3j", haut="tunique", couleur=LIN2, bas="jupe",
        chaussures="sandales", corpulence="mince", cadre=(120, 170, 200),
        description="L'homme qui arrive en courant du bout de la ville (28:20)")

# ---------------------------------------------------------------- Madyan
nouveau("BERGER", taille="grand", peau="mate", cheveux="court", barbe="courte", haut="djellaba", couleur=(120, 96, 70),
        couleur2=(200, 180, 140), chapeau="keffieh", couleur_chapeau=(170, 60, 50), chaussures="sandales",
        corpulence="fort", cadre=(170, 110, 70), description="Berger de Madyan (objet='baton')")
nouveau("BERGER2", taille="adulte", peau="halee", cheveux="court", barbe="bouc", haut="djellaba", couleur=(90, 80, 70),
        couleur2=(180, 160, 120), chapeau="turban", bijou=False, couleur_chapeau=(220, 210, 180), chaussures="sandales",
        cadre=(140, 120, 100), description="Berger de Madyan (2)")
nouveau("BERGER3", taille="ado", peau="doree", cheveux="court", haut="djellaba", couleur=(150, 120, 90),
        couleur2=(200, 180, 140), chaussures="sandales", cadre=(160, 130, 100), description="Jeune berger de Madyan")

# ---------------------------------------------------------------- le peuple dans le désert, Samiri, Qaroun
nouveau("FILS_D_ISRAEL", taille="adulte", peau="doree", cheveux="court", barbe="courte", haut="djellaba",
        couleur=(140, 110, 80), couleur2=(200, 180, 140), chapeau="turban", bijou=False, couleur_chapeau=(210, 196, 160),
        chaussures="sandales", cadre=(170, 140, 100), description="Un homme du peuple d'Israël (désert)")
nouveau("SAMIRI", taille="grand", peau="halee", cheveux="long", couleur_cheveux="noir", barbe="bouc", couleur_barbe="noir",
        haut="djellaba", couleur=(50, 44, 50), couleur2=(110, 30, 40), acc=["cape"], couleurs_acc=dict(cape=(70, 24, 30)),
        chaussures="sandales", corpulence="mince", cadre=(120, 40, 50), description="As-Samiri, cape sombre")
nouveau("QAROUN", taille="grand", peau="halee", cheveux="court", barbe="courte", haut="robe_longue", couleur=(130, 30, 50),
        couleur2="or", chapeau="turban", couleur_chapeau=(240, 220, 160), acc=["cape", "ceinture", "chaine"],
        couleurs_acc=dict(cape=(200, 150, 50), ceinture="or", chaine="or"), chaussures="sandales", corpulence="fort",
        cadre=(226, 182, 70), description="Qaroun, l'homme le plus riche : robe pourpre, or partout")
nouveau("SAGE_ISRAEL", taille="adulte", peau="halee", age="vieux", cheveux="vieux", couleur_cheveux="blanc", barbe="longue",
        couleur_barbe="blanc", haut="djellaba", couleur=(220, 214, 196), couleur2=(120, 100, 70), chapeau="turban", bijou=False,
        couleur_chapeau="blanc", chaussures="sandales", cadre=(214, 192, 152),
        description="Un sage du peuple (ceux qui avaient reçu le savoir, 28:80)")
nouveau("HOMME_PIEUX", taille="grand", peau="doree", cheveux="court", barbe="courte", haut="djellaba", couleur=(200, 190, 160),
        couleur2=(90, 120, 80), chapeau="turban", bijou=False, couleur_chapeau=(230, 222, 200), chaussures="sandales",
        cadre=(110, 150, 100), description="Un des deux hommes qui craignaient Allah (5:23)")

# ---------------------------------------------------------------- voix du script = un corps à l'écran
# Les voix de groupe (CONSEILLERS, MAGICIENS…) parlent par la bouche d'un représentant ; les autres membres du groupe
# se placent en figurants (CONSEILLER2, MAGICIEN2, MAGICIEN3…).
import cast as _cast  # noqa: E402


def alias(nom, modele, **changements):
    r = dict(_cast.CAST[modele])
    r.update(changements)
    _cast.CAST[nom] = r
    return r


alias("CONSEILLERS", "CONSEILLER", description="Les notables du conseil (voix de groupe)")
alias("MAGICIENS", "MAGICIEN", description="Les magiciens (voix de groupe, par la bouche du premier)")
alias("SAGES", "SAGE_ISRAEL", description="Ceux qui avaient reçu le savoir (28:80)")
alias("DEUX_HOMMES", "HOMME_PIEUX", description="Les deux hommes qui craignaient Allah (5:23)")
nouveau("HOMME_PIEUX2", taille="adulte", peau="halee", cheveux="court", barbe="longue", couleur_barbe="gris",
        haut="djellaba", couleur=(170, 160, 130), couleur2=(80, 110, 70), chapeau="turban", bijou=False,
        couleur_chapeau=(220, 214, 196), chaussures="sandales", cadre=(110, 150, 100),
        description="Le second des deux hommes qui craignaient Allah")
nouveau("VIEILLARD", taille="adulte", peau="doree", age="vieux", cheveux="vieux", couleur_cheveux="blanc", barbe="longue",
        couleur_barbe="blanc", haut="tunique", couleur=(130, 104, 78), bas="jupe", chaussures="sandales",
        cadre=(200, 190, 170), description="Le vieil homme des fils d'Israël (la promesse faite à Ibrahim)")
nouveau("DELATEUR", taille="adulte", peau="halee", cheveux="rase", barbe="moustache", couleur_barbe="noir",
        haut="tunique", couleur=LIN, bas="jupe", acc=["ceinture"], couleurs_acc=dict(ceinture=(170, 50, 40)),
        chaussures="sandales", corpulence="mince", cadre=(190, 70, 60),
        description="L'Égyptien qui court dénoncer Moussa (28:19)")
nouveau("GENS", taille="adulte", peau="doree", cheveux="court", barbe="courte", haut="djellaba", couleur=(160, 130, 96),
        couleur2=(210, 190, 150), chapeau="turban", bijou=False, couleur_chapeau=(200, 186, 150), chaussures="sandales",
        cadre=(170, 140, 100), description="Des gens du peuple (Qaroun)")
nouveau("RICHE_ISRAEL", taille="adulte", peau="doree", age="vieux", cheveux="vieux", couleur_cheveux="gris",
        barbe="longue", couleur_barbe="gris", haut="djellaba", couleur=(104, 66, 112), couleur2=(220, 180, 70),
        acc=["ceinture"], couleurs_acc=dict(ceinture=(220, 180, 70)), chaussures="sandales", cadre=(150, 100, 150),
        description="Le vieil homme riche retrouvé mort (2:72)")
nouveau("NEVEU", taille="adulte", peau="doree", cheveux="court", couleur_cheveux="noir", barbe="courte",
        couleur_barbe="noir", haut="tunique", couleur=(86, 104, 124), bas="jupe", chaussures="sandales",
        corpulence="mince", cadre=(90, 110, 140), description="Son neveu, qui l'avait tué (Ibn Kathir, 2:73)")
# Al-Khidr (18:65-82) : les enfants du chemin, les parents croyants, les orphelins du mur, les pêcheurs
nouveau("ENFANT_A", taille="enfant", peau="doree", cheveux="court", couleur_cheveux="noir", haut="tunique",
        couleur=(200, 180, 140), bas="jupe", chaussures="sandales", cadre=(200, 170, 110), description="Un enfant qui joue")
nouveau("ENFANT_B", taille="enfant", peau="halee", cheveux="boucle", couleur_cheveux="brun", haut="tunique",
        couleur=(150, 110, 80), bas="jupe", chaussures="sandales", cadre=(160, 120, 90), description="Un autre enfant")
nouveau("GARCON", taille="enfant", peau="doree", cheveux="boucle", couleur_cheveux="noir", haut="tunique",
        couleur=(120, 140, 110), bas="jupe", chaussures="sandales", cadre=(120, 150, 110),
        description="Le garçon (18:74) — jamais montré au moment où il est tué")
nouveau("FILLETTE_A", taille="enfant", genre="f", peau="doree", cheveux="long", couleur_cheveux="noir",
        haut="robe_longue", couleur=(190, 120, 110), couleur2=(150, 90, 80), chaussures="sandales",
        cadre=(200, 130, 120), description="L'enfant que reçoivent les parents (18:81)")
nouveau("ORPHELIN", taille="enfant", peau="doree", cheveux="court", couleur_cheveux="brun", haut="tunique",
        couleur=(170, 150, 120), bas="jupe", chaussures="sandales", cadre=(170, 150, 120), description="Orphelin (18:82)")
nouveau("ORPHELIN2", taille="ado", peau="doree", cheveux="court", couleur_cheveux="noir", haut="tunique",
        couleur=(130, 120, 100), bas="jupe", chaussures="sandales", cadre=(130, 120, 100), description="Son frère (18:82)")
nouveau("PERE_CROYANT", taille="adulte", peau="doree", cheveux="court", barbe="courte", haut="djellaba",
        couleur=(170, 150, 120), couleur2=(200, 180, 140), chapeau="turban", bijou=False, couleur_chapeau=(220, 210, 180),
        chaussures="sandales", cadre=(170, 150, 120), description="Le père croyant (18:80)")
nouveau("MERE_CROYANTE", genre="f", peau="doree", haut="robe_longue", couleur=(120, 130, 150), couleur2=(90, 100, 120),
        chaussures="sandales", cadre=(120, 130, 150), description="La mère croyante (18:80)")
nouveau("PECHEUR", taille="adulte", peau="mate", cheveux="court", barbe="courte", haut="tunique", couleur=(150, 130, 100),
        bas="jupe", chaussures="sandales", corpulence="mince", cadre=(150, 130, 100), description="Pêcheur pauvre (18:79)")
nouveau("PECHEUR2", taille="adulte", peau="halee", cheveux="court", couleur_cheveux="gris", barbe="longue",
        couleur_barbe="gris", haut="tunique", couleur=(120, 110, 90), bas="jupe", chaussures="sandales",
        cadre=(120, 110, 90), description="Vieux pêcheur (18:79)")
# Qaroun (28:76) : les hommes forts qui portent les clés de ses trésors
nouveau("PORTEUR", taille="grand", peau="mate", cheveux="rase", haut="tunique", couleur=(200, 190, 160), bas="jupe",
        chaussures="sandales", corpulence="fort", cadre=(200, 190, 160), description="Porteur (les clés de Qaroun)")
nouveau("PORTEUR2", taille="grand", peau="halee", cheveux="court", barbe="courte", haut="tunique", couleur=(180, 160, 130),
        bas="jupe", chaussures="sandales", corpulence="fort", cadre=(180, 160, 130), description="Porteur (2)")
nouveau("PORTEUR3", taille="adulte", peau="doree", cheveux="rase", barbe="moustache", haut="tunique",
        couleur=(210, 200, 176), bas="jupe", chaussures="sandales", corpulence="fort", cadre=(210, 200, 176),
        description="Porteur (3)")
