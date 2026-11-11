# LA TROUPE : personnages prêts à l'emploi (toutes chaînes). Chaque nom s'utilise comme "P" ou "G" dans les plans.
# Pour en créer un nouveau, copier une ligne et changer les réglages (voir cast.py : tailles, coiffures, hauts, chapeaux…).
from cast import nouveau

# ---------------------------------------------------------------- vie de tous les jours / sketchs
nouveau("ADO", taille="ado", peau="mate", cheveux="degrade", haut="sweat", couleur=(70, 110, 190), couleur2="blanc",
        bas="jogging", couleur_bas="anthracite", couleur_chaussures="bleu", cadre=(90, 130, 230),
        description="Ado, sweat bleu, jogging, coupe dégradée")
nouveau("ADA", taille="ado", genre="f", peau="doree", cheveux="queue", couleur_cheveux="brun", haut="sweat",
        couleur="rose_pale", couleur2="blanc", bas="jean", couleur_bas="jean_clair", couleur_chaussures="rose",
        acc=["boucles"], cadre=(240, 120, 160), description="Ado (fille), sweat rose, queue de cheval")
nouveau("ENFANT", taille="enfant", peau="claire", cheveux="court", couleur_cheveux="chatain", haut="tshirt",
        couleur="jaune", couleur2="orange", motif="etoile", bas="short", couleur_bas="bleu", couleur_chaussures="vert",
        corpulence="mince", cadre=(240, 170, 50), description="Petit garçon, t-shirt étoile, short")
nouveau("FILLETTE", taille="enfant", genre="f", peau="brune", cheveux="tresses", couleur_cheveux="noir", haut="robe",
        couleur="turquoise", couleur2="jaune", bas="jupe", couleur_chaussures="rose", corpulence="mince",
        couleur_acc_cheveux="jaune", cadre=(40, 190, 190), description="Petite fille, robe turquoise, tresses")
nouveau("MERE", genre="f", peau="mate", haut="abaya", couleur=(110, 70, 110), chapeau="hijab",
        couleur_chapeau=(206, 150, 120), chaussures="ville", couleur_chaussures="marron", cadre=(190, 90, 200),
        description="Mère, hijab et abaya")
nouveau("MAMAN", genre="f", peau="rosee", cheveux="chignon", couleur_cheveux="chatain", haut="pull", couleur="moutarde",
        bas="jean", couleur_bas="jean", chaussures="ville", couleur_chaussures="marron", acc=["boucles"],
        cadre=(240, 170, 50), description="Maman, pull moutarde, chignon")
nouveau("PAPA", taille="grand", peau="halee", cheveux="court", barbe="courte", haut="chemise", couleur=(120, 160, 210),
        bas="pantalon", couleur_bas="anthracite", chaussures="ville", couleur_chaussures="noir", corpulence="fort",
        cadre=(90, 130, 230), description="Papa, chemise bleue, barbe courte")
nouveau("PAPI", taille="adulte", peau="halee", age="vieux", cheveux="vieux", couleur_cheveux="gris", barbe="courte",
        couleur_barbe="blanc", haut="pull", couleur="bordeaux", bas="pantalon", couleur_bas="beige", chaussures="ville",
        couleur_chaussures="marron", lunettes="lunettes", cadre=(200, 200, 210), description="Grand-père, pull bordeaux, lunettes")
nouveau("MAMIE", genre="f", age="vieux", peau="claire", cheveux="chignon", couleur_cheveux="blanc", haut="robe_longue",
        couleur=(90, 120, 170), couleur2="creme", acc=["echarpe"], couleurs_acc=dict(echarpe="lilas"), lunettes="lunettes",
        chaussures="ville", couleur_chaussures="noir", cadre=(176, 150, 214), description="Grand-mère, robe bleue, chignon blanc")
nouveau("TATA", genre="f", peau="noire", cheveux="afro", couleur_cheveux="noir", haut="robe", couleur="orange",
        couleur2="jaune", bas="jupe", chaussures="talons", couleur_chaussures="bordeaux", acc=["boucles"],
        cadre=(234, 128, 48), description="Tata, robe orange, afro")
nouveau("TONTON", taille="grand", peau="foncee", cheveux="rase", barbe="bouc", haut="polo", couleur="vert_fonce",
        bas="pantalon", couleur_bas="beige", chaussures="ville", couleur_chaussures="marron", corpulence="fort",
        cadre=(90, 190, 90), description="Tonton, polo vert, bouc")
nouveau("ETUDIANT", taille="adulte", peau="claire", cheveux="meche", couleur_cheveux="blond", haut="chemise_ouverte",
        couleur=(170, 60, 60), couleur2="anthracite", bas="jean", lunettes="lunettes", acc=["sac"],
        couleurs_acc=dict(sac="kaki"), corpulence="mince", cadre=(226, 62, 62), description="Étudiant, chemise ouverte, sac à dos")
nouveau("ETUDIANTE", genre="f", peau="mate", chapeau="hijab", couleur_chapeau="marine", haut="blazer", couleur="beige",
        couleur2="blanc", bas="pantalon", couleur_bas="marine", chaussures="baskets", couleur_chaussures="beige",
        acc=["sac"], couleurs_acc=dict(sac="marron"), cadre=(90, 130, 230), description="Étudiante, hijab, blazer beige")
nouveau("GAMER", taille="ado", peau="brune", cheveux="boucle", haut="tshirt", couleur="noir", couleur2=(120, 220, 255),
        motif="eclair", bas="jogging", couleur_bas="anthracite", chapeau="casque_audio", couleur_chapeau=(120, 220, 255),
        couleur_chaussures="noir", cadre=(120, 220, 255), description="Gameur, casque, t-shirt éclair")
nouveau("LIVREUR", taille="adulte", peau="foncee", cheveux="rase", barbe="3j", haut="doudoune", couleur="vert",
        bas="jogging", couleur_bas="noir", chapeau="casquette", couleur_chapeau="noir", acc=["sac"],
        couleurs_acc=dict(sac=(60, 190, 120)), couleur_chaussures="vert", cadre=(60, 190, 120),
        description="Livreur, doudoune verte, sac de livraison")
nouveau("FOURBE", taille="adulte", peau="halee", cheveux="degrade", barbe="bouc", haut="cuir", couleur="noir",
        couleur2="blanc", bas="jean", couleur_bas="jean_noir", lunettes="soleil", acc=["chaine"], couleur_chaussures="noir",
        cadre=(160, 60, 200), description="Le fourbe : veste en cuir, chaîne, lunettes noires")
nouveau("CAPUCHE", taille="ado", peau="doree", cheveux="court", haut="sweat", couleur="anthracite", couleur2="gris",
        bas="jogging", couleur_bas="noir", chapeau="capuche", couleur_chapeau="anthracite", couleur_chaussures="noir",
        cadre=(120, 120, 140), description="Inconnu en capuche (mystère)")
nouveau("VOISIN", taille="grand", peau="rosee", age="vieux", cheveux="vieux", couleur_cheveux="gris", barbe="moustache",
        couleur_barbe="gris", haut="chemise", couleur="beige", bas="pantalon", couleur_bas="marron", chaussures="ville",
        couleur_chaussures="marron", corpulence="fort", acc=["gilet"], couleurs_acc=dict(gilet="marron", liseré="marron"),
        cadre=(184, 134, 76), description="Le voisin râleur, gilet et moustache")
nouveau("EPICIER", taille="adulte", peau="halee", cheveux="court", barbe="moustache", haut="tablier", couleur="vert_fonce",
        couleur2="blanc", bas="pantalon", couleur_bas="anthracite", chaussures="ville", couleur_chaussures="noir",
        corpulence="fort", cadre=(60, 150, 80), description="Épicier, tablier vert, moustache")
nouveau("CUISINIER", taille="grand", peau="doree", cheveux="court", barbe="moustache", haut="tablier", couleur="blanc",
        couleur2="blanc", bas="pantalon", couleur_bas="noir", chapeau="toque", chaussures="ville", couleur_chaussures="noir",
        corpulence="fort", cadre=(200, 200, 210), description="Cuisinier, toque et tablier")
nouveau("COACH", taille="grand", peau="noire", cheveux="rase", barbe="courte", haut="survet", couleur="rouge",
        couleur2="blanc", bas="jogging", couleur_bas="rouge", chapeau="bandeau", couleur_chapeau="blanc",
        couleur_chaussures="noir", cadre=(226, 62, 62), description="Coach sportif, survêtement rouge")
nouveau("FOOTEUX", taille="ado", peau="foncee", cheveux="herisse", haut="maillot", couleur="bleu", couleur2="blanc",
        numero=10, bas="short", couleur_bas="blanc", couleur_chaussures="jaune", corpulence="mince",
        cadre=(56, 110, 200), description="Footballeur, maillot n°10")

# ---------------------------------------------------------------- métiers
nouveau("PROF", taille="adulte", peau="rosee", cheveux="court", couleur_cheveux="chatain", barbe="3j", haut="blazer",
        couleur="marron", couleur2="creme", bas="pantalon", couleur_bas="beige", chaussures="ville", couleur_chaussures="marron",
        lunettes="lunettes", cadre=(184, 134, 76), description="Professeur, blazer marron, lunettes")
nouveau("PROFE", genre="f", peau="claire", cheveux="carre", couleur_cheveux="roux", haut="pull", couleur="vert",
        bas="jupe", couleur_bas="anthracite", collant=(50, 46, 60), chaussures="ville", couleur_chaussures="noir",
        lunettes="lunettes", cadre=(90, 190, 90), description="Professeure, carré roux, pull vert")
nouveau("MEDECIN", genre="f", peau="brune", cheveux="queue", couleur_cheveux="noir", haut="blouse", couleur="blanc",
        couleur2=(120, 180, 230), bas="pantalon", couleur_bas="marine", chaussures="baskets", couleur_chaussures="blanc",
        acc=["stethoscope", "badge"], cadre=(124, 182, 236), description="Médecin, blouse et stéthoscope")
nouveau("POLICIER", taille="grand", peau="claire", cheveux="degrade", couleur_cheveux="brun", haut="police", couleur="marine",
        bas="pantalon", couleur_bas="marine", chaussures="ville", couleur_chaussures="noir", chapeau="casquette_police",
        cadre=(56, 110, 200), description="Policier en uniforme")
nouveau("PATRON", taille="grand", peau="claire", cheveux="court", couleur_cheveux="gris", haut="costume", couleur="noir",
        couleurs_acc=dict(cravate="rouge"), chaussures="ville", couleur_chaussures="noir", corpulence="fort",
        cadre=(226, 182, 70), description="Le patron, costume noir, cravate rouge")
nouveau("VENDEUSE", genre="f", peau="doree", cheveux="long", couleur_cheveux="brun", haut="polo", couleur="rouge",
        bas="pantalon", couleur_bas="noir", chaussures="baskets", couleur_chaussures="blanc", acc=["badge"],
        couleurs_acc=dict(badge="rouge"), cadre=(226, 62, 62), description="Vendeuse, polo rouge, badge")

# ---------------------------------------------------------------- info / podcast
nouveau("PRESENTATEUR", taille="grand", peau="halee", cheveux="meche", couleur_cheveux="noir", haut="costume",
        couleur="marine", couleurs_acc=dict(cravate=(60, 140, 220)), chaussures="ville", couleur_chaussures="noir",
        cadre=(60, 140, 220), description="Présentateur du JT, costume marine")
nouveau("JOURNALISTE", genre="f", peau="mate", cheveux="carre", couleur_cheveux="noir", haut="blazer", couleur="rouge",
        couleur2="noir", bas="pantalon", couleur_bas="noir", chaussures="talons", couleur_chaussures="noir", acc=["boucles"],
        couleurs_acc=dict(micro="rouge"), cadre=(226, 62, 62), description="Journaliste, blazer rouge (avec micro : pose micro)")
nouveau("EXPERT", taille="adulte", peau="claire", age="vieux", cheveux="vieux", couleur_cheveux="gris", barbe="courte",
        couleur_barbe="gris", haut="pull", couleur="noir", col_roule=True, bas="pantalon", couleur_bas="anthracite",
        chaussures="ville", couleur_chaussures="noir", lunettes="lunettes", cadre=(200, 200, 210),
        description="L'expert, col roulé noir, barbe grise")
nouveau("PODCASTEUR", taille="adulte", peau="doree", cheveux="boucle", couleur_cheveux="brun", barbe="courte",
        couleur_barbe="brun", haut="tshirt", couleur="blanc", couleur2="noir", motif="logo", bas="jean", couleur_bas="jean_noir",
        chapeau="casque_audio", couleur_chapeau=(250, 200, 60), couleur_chaussures="noir", cadre=(250, 200, 60),
        description="Podcasteur, casque audio, t-shirt blanc")

# ---------------------------------------------------------------- histoire / biographies (personnages génériques)
nouveau("ROI", taille="grand", peau="claire", cheveux="court", couleur_cheveux="brun", barbe="longue", couleur_barbe="brun",
        haut="robe_longue", couleur=(110, 50, 140), couleur2="or", chapeau="couronne", acc=["cape", "ceinture"],
        couleurs_acc=dict(cape="rouge", ceinture="or"), chaussures="bottes", couleur_chaussures="marron",
        cadre=(226, 182, 70), description="Roi, couronne, cape rouge")
nouveau("REINE", genre="f", peau="rosee", cheveux="long", couleur_cheveux="blond", haut="robe_longue", couleur=(60, 90, 170),
        couleur2="or", chapeau="couronne", acc=["cape"], couleurs_acc=dict(cape="bordeaux"), chaussures="talons",
        couleur_chaussures="or", cadre=(90, 130, 230), description="Reine, robe bleue, couronne")
nouveau("SULTAN", taille="grand", peau="halee", barbe="courte", haut="robe_longue", couleur="bordeaux", couleur2="or",
        chapeau="turban", couleur_chapeau="blanc", acc=["cape", "ceinture"], couleurs_acc=dict(cape=(30, 80, 70), ceinture="or"),
        chaussures="bottes", couleur_chaussures="or", cadre=(226, 182, 70), description="Souverain d'Orient, turban, cape")
nouveau("SAVANT", taille="adulte", peau="rosee", age="vieux", cheveux="vieux", couleur_cheveux="blanc", barbe="moustache",
        couleur_barbe="blanc", haut="redingote", couleur=(50, 50, 60), couleur2="bordeaux", bas="pantalon",
        couleur_bas="anthracite", chaussures="ville", couleur_chaussures="noir", cadre=(200, 200, 210),
        description="Savant du XIXe siècle, redingote, moustache blanche")
nouveau("SCIENTIFIQUE", genre="f", peau="claire", cheveux="chignon", couleur_cheveux="brun", haut="blouse", couleur="blanc",
        couleur2=(120, 120, 140), bas="pantalon", couleur_bas="anthracite", chaussures="ville", couleur_chaussures="noir",
        lunettes="lunettes", cadre=(124, 182, 236), description="Scientifique, blouse, lunettes")
nouveau("CHEVALIER", taille="grand", peau="rosee", cheveux="court", couleur_cheveux="chatain", barbe="3j",
        couleur_barbe="chatain", haut="armure", couleur2=(40, 70, 150), bas="armure", chaussures="bottes",
        couleur_chaussures=(110, 116, 128), cadre=(176, 184, 196), description="Chevalier en armure (objet='epee')")
nouveau("ROMAIN", taille="adulte", peau="halee", cheveux="court", couleur_cheveux="brun", haut="toge", couleur="blanc",
        couleur2="bordeaux", chapeau="laurier", chaussures="sandales", cadre=(128, 30, 44), description="Romain, toge et laurier")
nouveau("PAYSAN", taille="adulte", peau="halee", cheveux="court", couleur_cheveux="brun", barbe="courte",
        couleur_barbe="brun", haut="tunique", couleur=(150, 120, 80), bas="pantalon", couleur_bas=(110, 90, 60),
        chaussures="bottes", couleur_chaussures="marron", chapeau="chapeau", couleur_chapeau=(214, 184, 110),
        couleur_ruban=(150, 110, 60), cadre=(184, 134, 76), description="Paysan d'autrefois, tunique, chapeau de paille")
nouveau("EXPLORATEUR", taille="grand", peau="halee", cheveux="court", couleur_cheveux="chatain", barbe="3j",
        couleur_barbe="chatain", haut="chemise", couleur="kaki", bas="cargo", couleur_bas="beige", chaussures="bottes",
        couleur_chaussures="marron", chapeau="chapeau", couleur_chapeau="camel", acc=["sac"], couleurs_acc=dict(sac="marron"),
        cadre=(122, 120, 74), description="Explorateur, chemise kaki, chapeau")
nouveau("VOYAGEUR", taille="adulte", peau="halee", barbe="courte", haut="djellaba", couleur=(150, 110, 70), couleur2="creme",
        chapeau="turban", couleur_chapeau="creme", chaussures="sandales", cadre=(184, 134, 76),
        description="Voyageur d'autrefois, djellaba, turban")
nouveau("SAGE", taille="grand", peau="halee", age="vieux", barbe="longue", couleur_barbe="blanc", cheveux="vieux",
        couleur_cheveux="blanc", haut="djellaba", couleur="creme", couleur2=(150, 110, 70), chapeau="kufi",
        couleur_chapeau="blanc", chaussures="sandales", cadre=(214, 192, 152), description="Vieux sage, djellaba, barbe blanche")

# ---------------------------------------------------------------- mystère / enquête
nouveau("DETECTIVE", taille="grand", peau="rosee", cheveux="court", couleur_cheveux="brun", barbe="3j", couleur_barbe="brun",
        haut="redingote", couleur="camel", couleur2=(70, 60, 56), bas="pantalon", couleur_bas="anthracite", chaussures="ville",
        couleur_chaussures="marron", chapeau="chapeau", couleur_chapeau="marron", cadre=(184, 134, 76),
        description="Détective, trench et chapeau (objet='loupe')")
nouveau("OUVRIER", taille="grand", peau="brune", cheveux="court", barbe="courte", haut="combinaison", couleur="orange",
        couleur2="argent", chapeau="casque_chantier", couleur_chapeau="jaune", chaussures="bottes", couleur_chaussures="noir",
        corpulence="fort", cadre=(234, 128, 48), description="Ouvrier, combinaison orange, casque de chantier")

# ---------------------------------------------------------------- IslamArcade : le duo « VALABLE OU PAS ? » en version troupe
# (mêmes têtes que P et G des VOP, mais avec toutes les nouveautés : champ / contre-champ, réactions, démonstrations…)
nouveau("PETIT", taille="ado", peau="mate", cheveux="court", couleur_cheveux="noir", haut="sweat", couleur=(200, 50, 50),
        couleur2="blanc", bas="jean", couleur_bas="jean", chapeau="casquette", couleur_chapeau=(40, 50, 90),
        couleur_chaussures="blanc", cadre=(220, 70, 70), cote="droite", description="Petit frère (IslamArcade), sweat rouge")
nouveau("GRAND", taille="grand", peau="mate", cheveux="court", couleur_cheveux="noir", barbe="courte", haut="qamis",
        couleur=(236, 230, 214), bas="pantalon", couleur_bas=(236, 230, 214), chapeau="kufi", couleur_chapeau="blanc",
        acc=["gilet"], couleurs_acc=dict(gilet="vert_fonce"), chaussures="sandales", cadre=(60, 160, 90), cote="gauche",
        description="Grand frère (IslamArcade), qamis et gilet vert")
