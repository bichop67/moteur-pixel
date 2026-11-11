# ÉCRIRE UNE SCÈNE COMME UN SCÉNARIO → la vidéo se fabrique toute seule (plans, gros plans, caméra, regards, sons).
#   python scenario.py mon_sketch.txt sheet        planche de contrôle (maquette sans voix tant que les voix n'existent pas)
#   python scenario.py mon_sketch.txt voix         textes à générer sur ElevenLabs (une génération par personnage)
#   python scenario.py mon_sketch.txt asr          transcription des voix (une fois les MP3 posés dans le dossier VOIX)
#   python scenario.py mon_sketch.txt tout         fabrique la vidéo (plusieurs cœurs, priorité basse)
#   python scenario.py mon_sketch.txt brouillon    APERÇU RAPIDE qui bouge, avec le son : 10 images/s, demi-taille,
#                                                  sans grain, marqué BROUILLON → « <titre> (brouillon).mp4 » (≈ 3 fois plus vite)
#   python scenario.py mon_sketch.txt still 4.5 image.png      une image à 4,5 s
#
# FORMAT DU FICHIER (exemple complet : scenarios/le_passeport_de_papi.txt) — une ligne = une chose :
#   TITRE: Le passeport de Papi           THEME: sketch (valable, info, histoire, mystere, science, argent, podcast)
#   FORMAT: vertical (ou horizontal)      MUSIQUE: fond_espoir     PERSONNAGES: ADA, PAPI (le 1er à gauche, le 2e à droite)
#   == aeroport, passants, 1.5s           un DÉCOR. Options : pluie, neige, feuilles, lucioles, voitures, passants,
#                                         oiseaux, feu, 2s (plan muet au début), ensemble (540, 700) (la caméra
#                                         s'approche de ce point), texte "23 H 47", serre (plan à deux, serré)
#   ADA entre à gauche, téléphone         une ACTION (à ce moment-là du récit)
#   ADA (choc, bulle !) : Comment ?!      une RÉPLIQUE ; entre parenthèses : ce qu'il fait EN la disant
#   PAPI (gros plan, peur, goutte) : …    « gros plan » = plan serré sur lui pendant sa réplique
#   SMS MAMAN : Ça va ? / > Oui           écran de téléphone (« > » = message envoyé par moi)
#   NOTIF MAMAN : Tu rentres quand ?      notification en haut pendant la réplique suivante
#   CARTON : LE LENDEMAIN / 8 H 00        carton de temps plein écran
#   LEGENDE : CHAMP / CONTRE-CHAMP / …    légende de démonstration en haut (jusqu'à la fin du décor)
#   FIN                                   les persos rient + « abonne-toi » (2,6 s)
#   # une ligne qui commence par # est un commentaire
# Mots compris entre parenthèses (accents et majuscules sans importance) : voir FACES, POSES, EFFETS ci-dessous,
# + entre (à gauche / à droite / par la porte), sort (à gauche / à droite), s'approche, se retourne, apparaît,
# assis, se lève, sautille, rit, tient le livre, donne le passeport à ADA, pense à batterie (icône), bulle ! / ? / …
import math, os, re, sys, unicodedata
import numpy as np
from PIL import Image, ImageDraw
import kit, pxv, scene, duo, objets, lieux, sets, explique
import film, egypte                     # films : orbes, voix sans corps, décors de l'Égypte ancienne
import pov                               # Shorts « … tu fais quoi ? » : plans en vue subjective ({pov …}, décors *_pov)
import troupe_egypte                     # films : Pharaon, Haman, soldats, magiciens, Israélites, bergers de Madyan…
import decors_film                       # films : quartier, chantier, chambre de Pharaon, vision du rêve…
import decors_film2                      # films : maison au bord du Nil, ruelle, couloir, chambre d'Asiya, désert…
import decors_madyan                     # films : Madyan (puits, maison, collines), la montagne, l'arbre où flambe le feu
import decors_film3                      # films : porte du palais, esplanade de la fête, tour de Haman, cour au soleil
import decors_film4                      # films : champs, grenier, Nil de sang, terrasse, la mer, le camp, la montagne
import decors_film5                      # films : confluent, village au mur, Qaroun, dune rouge, les cieux, tableaux
import decors_gog                        # film hors-série « Gog et Magog » (10/11/2026) : barrage, sortie, lac, oiseaux…
import decors_mer                        # films : la mer qui s'ouvre (refaite le 02/11/2026) : rivage, face, douze chemins…

HERE = os.path.dirname(os.path.abspath(__file__))
W_MONDE = 1080
MUSIQUES = pxv.BASE + "/_MUSIQUES/FOND/"                           # (pxv.BASE : le dossier « VIDEO YOUTUBE »)
EMOTIONS = dict(a=pxv.BASE + "/_MUSIQUES/emotion_nasheed_A_mercy_in_the_stillness.mp3",
                b=pxv.BASE + "/_MUSIQUES/emotion_nasheed_B_heartsong_in_the_quiet.mp3")


def norm(x):
    x = unicodedata.normalize("NFD", x.lower().strip())
    return "".join(ch for ch in x if not unicodedata.combining(ch)).replace("’", "'")


# ---------------------------------------------------------------- vocabulaire des didascalies (mots → réglages)
FACES = {"neutre": "neutre", "content": "content", "contente": "content", "sourit": "content", "souriant": "content",
         "souriante": "content", "rit": "rire", "rire": "rire", "choc": "choc", "choque": "choc", "choquee": "choc",
         "surpris": "choc", "surprise": "choc", "gene": "gene", "genee": "gene", "malin": "malin", "maligne": "malin",
         "blase": "blase", "blasee": "blase", "enerve": "enerve", "enervee": "enerve", "en colere": "enerve",
         "crie": "cri", "hurle": "cri", "triste": "triste", "pleure": "pleure", "peur": "peur", "a peur": "peur",
         "suspect": "suspect", "soupconneux": "suspect", "soupconneuse": "suspect", "degoute": "degoute",
         "degoutee": "degoute", "clin d'oeil": "clin", "amoureux": "coeur", "amoureuse": "coeur", "emerveille": "etoile",
         "emerveillee": "etoile", "dort": "dodo", "endormi": "dodo", "endormie": "dodo", "fier": "fier", "fiere": "fier",
         "calme": "calme", "regarde en bas": "bas", "honteux": "bas", "honteuse": "bas"}
POSES = {"explique": "explique", "pointe": "pointe", "montre du doigt": "pointe", "index": "index", "question": "question",
         "panique": "panique", "bras croises": "bras_croises", "salut": "salut", "salue": "salut", "fait coucou": "salut",
         "pouce": "pouce", "hanches": "hanches", "mains sur les hanches": "hanches", "facepalm": "facepalm",
         "main sur le visage": "facepalm", "menton": "menton", "reflechit": "menton", "haussement": "haussement",
         "hausse les epaules": "haussement", "victoire": "victoire", "bras leves": "victoire", "tient": "tient",
         "au telephone": "appel", "appelle": "appel", "micro": "micro", "tape": "clavier", "clavier": "clavier",
         "stop": "arret", "arret": "arret", "presente": "montre", "doua": "doua", "invoque": "doua", "prie": "priere",
         "boit": "the", "the": "the", "bras le long du corps": "neutre",
         # orbes (film.py) : lumière faible (peur, chagrin, faim) ou forte (joie, révélation)
         "pale": "pale", "palit": "pale", "faible": "pale", "intense": "intense", "rayonne": "intense",
         "ouvert": "ouvert", "s'ouvre": "ouvert", "vide": "vide", "ferme le couvercle": "ferme", "ferme": "ferme",
         "pose au sol": "ferme", "porte": "porte", "porte a bout de bras": "porte",
         "corde": "corde", "corde detachee": "corde", "prise": "prise", "braise prise": "prise",
         "allonge": "allonge", "etendu au sol": "allonge", "etendu": "allonge", "a terre": "allonge", "au sol": "allonge",
         "prosterne": "prosterne", "se prosterne": "prosterne", "prosternes": "prosterne", "front au sol": "prosterne",
         "sol": "sol", "par terre": "sol", "debout": "neutre", "se releve": "neutre", "neutre": "neutre",
         "porte_vide": "porte_vide", "porte vide": "porte_vide", "breche": "breche"}
EFFETS = {"coeurs": "coeurs", "colere": "colere", "fumee": "colere", "idee": "idee", "zzz": "zzz", "larmes": "larmes",
          "goutte": "goutte", "transpire": "goutte", "etoiles": "etoiles", "notes": "notes", "chante": "notes",
          "points": "points", "brille": "brille"}
OBJETS = set(["telephone", "tasse", "verre_the", "micro", "livre", "parchemin", "ballon", "manette", "billets", "stylo",
              "epee", "canne", "torche", "loupe", "fiole", "sac_courses", "passeport", "valise", "coran",
              "lance", "baton", "fouet", "crosse", "briques", "panier", "jarre"])
BULLES = {"!": "!", "?": "?", "...": "...", "…": "...", "?!": "?!", "!?": "?!"}
A_BOUT_DE_BRAS = ("valise", "sac_courses")              # portés bras le long du corps


def repos(objet):
    """Pose de repos selon ce que le perso a en main."""
    if objet in (None, "aucun") or objet in A_BOUT_DE_BRAS:
        return "neutre"
    if objet in ("lance", "baton"):                         # tenus le long du corps (pas devant le visage)
        return "lance"
    return "telephone" if objet == "telephone" else "tient"


GESTES = ("explique", "pointe", "index", "question", "panique", "salut", "pouce", "facepalm", "haussement", "victoire",
          "arret", "montre")                       # gestes d'un instant : après la réplique, le perso revient au repos


def lire_didascalies(txt):
    """'gêné, bras croisés, colère, pense à batterie' → dict de jeu."""
    act = dict(traverse=False, place=None, cadre=None, off=False, pose=None, face=None, effets=[], gros_plan=False, plan=None, pensee=None, bulle=None, entre=None,
               sort=None, assis=None, siege=None, objet=None, donne=None, tourne=False, rit=False, sautille=False, approche=False,
               apparait=False, nouveau=False, inconnus=[])
    for brut in [p for p in re.split(r"[,;]", txt) if p.strip()]:
        p = re.sub(r"\s+", " ", norm(brut))
        if p in ("gros plan", "plan serre", "zoom"):
            act["gros_plan"] = True; continue
        if p in ("nouveau schema", "nouveau plan", "autre schema", "nouveau tableau"):
            act["nouveau"] = True; continue                  # ce schéma ne prolonge pas le précédent (retour sur la scène entre les deux)
        if p in ("plan moyen", "plan rapproche", "rapproche", "on se rapproche"):
            act["plan"] = "proche"; continue
        if p in ("plan large", "large"):
            act["plan"] = "large"; continue
        if p in ("schema", "explication", "tableau"):
            act["plan"] = "schema"; continue
        if p in ("voix off", "off", "hors champ", "hors-champ"):
            act["off"] = True; continue
        if p in ("epaule", "par-dessus l'epaule", "plan epaule", "champ", "contre-champ", "champ contre-champ",
                 "champ / contre-champ"):
            act["plan"] = "epaule"; continue
        m = re.match(r"pense(?:e)?(?:\s+a(?:u|ux)?)?\s+(?:la |le |l'|les )?(\w+)", p)
        if m:
            act["pensee"] = m.group(1); continue
        m = re.match(r"bulle\s*(\S+)", p)
        if m:
            act["bulle"] = BULLES.get(m.group(1), "!"); continue
        m = re.match(r"entre(?:\s+(?:a|par)(?:\s+la)?\s+(gauche|droite|porte))?$", p)
        if m:
            act["entre"] = m.group(1) or "auto"; continue
        m = re.match(r"(?:sort|part|s'en va)(?:\s+(?:a|par)(?:\s+la)?\s+(gauche|droite))?$", p)
        if m:
            act["sort"] = m.group(1) or "auto"; continue
        if p in ("assis", "assise", "s'assoit", "s'assied", "sur une chaise", "assis sur une chaise"):
            act["assis"] = True; continue
        if p in ("sur le trone", "sur son trone", "assis sur le trone", "assis sur son trone", "sur le trone royal"):
            act["assis"] = True; act["siege"] = "trone"; continue
        if p in ("sur le lit", "assis sur le lit", "sur son lit", "assis au bord du lit"):    # le lit est dans le décor
            act["assis"] = True; act["siege"] = "aucun"; continue
        if p in ("assis par terre", "assise par terre", "assis au sol", "assis sur le sol"):   # sans meuble
            act["assis"] = True; act["siege"] = "aucun"; continue
        if p in ("sur un tabouret", "assis sur un tabouret", "sur le tabouret"):
            act["assis"] = True; act["siege"] = "tabouret"; continue
        if p in ("se leve", "debout"):
            act["assis"] = False; continue
        if p in ("se retourne", "se tourne"):
            act["tourne"] = True; continue
        if p in ("s'approche", "approche", "avance"):
            act["approche"] = True; continue
        if p in ("apparait", "arrive"):
            act["apparait"] = True; continue
        if p in ("sautille", "saute", "danse"):
            act["sautille"] = True; continue
        if p in ("traverse", "passe", "traverse la rue"):
            act["traverse"] = True; continue
        m = re.match(r"place\s+(-?\d+)(?:\s+(-?\d+))?$", p)
        if m:
            act["place"] = int(m.group(1)) if m.group(2) is None else (int(m.group(1)), int(m.group(2))); continue
        m = re.match(r"place\s+([a-z_]+)$", p)                        # place nommée du décor (ex. « place trone »)
        if m:
            act["place"] = m.group(1); continue
        m = re.match(r"donne\s+(?:le |la |les |l'|un |une |son |sa |ses )?(\w+)(?:\s+a\s+(\w+))?", p)
        if m:
            act["donne"] = (m.group(1), (m.group(2) or "").upper()); continue
        m = re.match(r"(?:tient|a|avec)\s+(?:le |la |l'|un |une |son |sa )?(\w+)$", p)
        if m and m.group(1) in OBJETS:
            act["objet"] = m.group(1); act["pose"] = act["pose"] or repos(m.group(1)); continue
        if p in OBJETS:
            act["objet"] = p
            act["pose"] = act["pose"] or repos(p); continue
        if p in ("range", "les mains vides", "range son telephone", "range le telephone"):
            act["objet"] = "aucun"; continue
        if p in EFFETS:
            act["effets"].append(EFFETS[p])
            if p == "colere":
                act["face"] = act["face"] or "enerve"
            continue
        if p in FACES:
            act["face"] = FACES[p]
            if FACES[p] == "rire":
                act["rit"] = True
            if FACES[p] == "pleure":
                act["effets"].append("larmes")
            continue
        if p in POSES:
            act["pose"] = POSES[p]; continue
        m = re.match(r"(?:sur|cadre|camera sur)\s+([a-z_0-9]+)$", p)   # film : la caméra va sur ce perso (plan moyen)
        if m:
            act["cadre"] = m.group(1).upper(); continue
        act["inconnus"].append(brut.strip())
    return act


# ---------------------------------------------------------------- lecture du fichier
ENTETES = ("TITRE", "THEME", "FORMAT", "MUSIQUE", "VOIX", "PERSONNAGES", "CODE", "MINIATURE", "ICONE", "DEMO", "ACCROCHE",
           "DUREE_FIN", "QUEUE", "ACCROCHE_DUREE", "CAMERA", "BATON_MOUSSA",
           "FILM", "CHAPITRE")           # FILM: titre du film entier ; CHAPITRE: titre du chapitre (fais_film.py)


def sans_balises_voix(txt):
    """Retire les balises d'émotion d'ElevenLabs ([dark], [pause], [softly]…) : elles servent à la voix, pas aux
    sous-titres ni au calage. Les {…} du moteur restent."""
    return re.sub(r"\s+", " ", re.sub(r"\[[^\]{}]*\]", " ", txt)).strip()


def _anim_noir(u0, fondu=0.4, fin=None):
    """Fondu au noir de l'image (pas des sous-titres) à partir de u0, jusqu'à la fin du plan ; {noir 3s} : jusqu'à
    u0 + 3 s, puis l'image revient en 0,7 s ; {noir 5} : fondu lent de 5 s."""
    def f(img, u):
        if u <= u0:
            return
        a = min(1.0, (u - u0) / fondu)
        if fin is not None and u > fin:
            a = a * max(0.0, 1 - (u - fin) / 0.7)
        if a <= 0:
            return
        img.alpha_composite(Image.new("RGBA", img.size, (0, 0, 0, int(255 * a))))
    return f


def duree_muette(options):
    for o in options:
        m = re.match(r"^(\d+(?:[.,]\d+)?)\s*s$", o.strip())
        if m:
            return float(m.group(1).replace(",", "."))
    return None


def duree_sms(n):
    return 1.4 + 1.1 * n


def lire(path):
    head, blocs, cur = {}, [], None
    for n, raw in enumerate(open(path, encoding="utf-8-sig"), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-ZÉÈ_]+)\s*:\s*(.*)$", line)                 # « _ » : DUREE_FIN
        cle = m.group(1).replace("É", "E").replace("È", "E") if m else None
        if cle in ENTETES:
            head[cle] = m.group(2).strip(); continue
        if line.startswith("=="):
            parts = [p.strip() for p in re.split(r",(?![^(]*\))(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", line[2:]) if p.strip()]
            if not parts or parts[0] not in sets.DECORS:
                raise SystemExit(f"ligne {n} : décor inconnu « {parts[0] if parts else ''} ». Décors : "
                                 + ", ".join(sorted(sets.DECORS)))
            cur = dict(decor=parts[0], options=parts[1:], items=[], ligne=n)
            blocs.append(cur); continue
        if cur is None:
            raise SystemExit(f"ligne {n} : il faut d'abord un décor (« == nom_du_decor »)")
        if line.upper() == "FIN":
            cur["items"].append(dict(type="fin")); continue
        m = re.match(r"^SMS\s+([\wÉÈ]+)\s*:\s*(.+)$", line)
        if m:
            msgs = [x.strip() for x in m.group(2).split("/") if x.strip()]
            cur["items"].append(dict(type="sms", qui=m.group(1).upper(), msgs=msgs)); continue
        m = re.match(r"^NOTIF\s+([\wÉÈ]+)\s*:\s*(.+)$", line)
        if m:
            cur["items"].append(dict(type="notif", qui=m.group(1).upper(), texte=m.group(2).strip())); continue
        m = re.match(r"^L[EÉ]GENDE\s*:\s*(.+)$", line)
        if m:
            t = [x.strip() for x in m.group(1).rsplit("/", 1)]          # le dernier « / » sépare le titre du texte
            cur["items"].append(dict(type="legende", titre=t[0], code=t[1] if len(t) > 1 else None)); continue
        m = re.match(r"^CARTON\s*:\s*(.+)$", line)
        if m:
            t = [x.strip() for x in m.group(1).split("/")]
            cur["items"].append(dict(type="carton", texte=t[0], sous=t[1] if len(t) > 1 else None)); continue
        m = re.match(r"^([A-Z_0-9]+)\s*(?:\(([^)]*)\))?\s*:\s*(.+)$", line)
        if m:
            act = lire_didascalies(m.group(2) or "")
            for x in act["inconnus"]:
                print(f"(ligne {n} : je ne connais pas « {x} », ignoré)")
            brut = m.group(3).strip()
            voix_txt = re.sub(r"\s+", " ", explique.balises(brut)[0]).strip()     # pour ElevenLabs : balises [dark]… gardées
            txt, vis = explique.balises(sans_balises_voix(brut))    # {miroir ADA} … : schémas calés sur les mots
            cur["items"].append(dict(type="ligne", qui=m.group(1), act=act, texte=txt, texte_voix=voix_txt, visuels=vis, n=n))
            continue
        m = re.match(r"^([A-Z_0-9]+)\s+(.+)$", line)
        if m:
            act = lire_didascalies(m.group(2))
            for x in act["inconnus"]:
                print(f"(ligne {n} : je ne connais pas « {x} », ignoré)")
            cur["items"].append(dict(type="action", qui=m.group(1), act=act, n=n))
            continue
        print(f"(ligne {n} ignorée : {line})")
    for b in blocs:                        # plan muet du décor : après les actions du début, avant le reste
        d = duree_muette(b["options"])
        if d:
            i = next((j for j, it in enumerate(b["items"]) if it["type"] != "action"), len(b["items"]))
            b["items"].insert(i, dict(type="muet", d=d))
    return head, blocs


# ---------------------------------------------------------------- fabrication
ANNOT = ("etiquette", "étiquette", "mesure", "projecteur", "loupe", "pensees", "pensées", "repousse",
         "pousse", "barre", "coche", "va", "regarde", "peches", "péchés", "lumiere", "lumière", "geste",
         "son", "derive", "dérive", "cadre", "large", "gros", "feu_reve", "devient", "apparait", "apparaît",
         "disparait", "disparaît", "noir", "court", "souvenir", "serpent", "main_blanche", "duel", "fleau", "fléau",
         "vagues", "poussiere", "poussière", "sources", "manne", "nuage", "cendres", "danse", "foudre", "cailles", "poisson", "mur", "engloutit", "lueur", "echelle",
         "tableau", "mer_fend", "mer_referme") + tuple(decors_gog.ANNOTATIONS)     # posées sur la scène (pas un schéma)
COULEURS = dict(rouge=(240, 80, 80), vert=(110, 220, 120), bleu=(120, 180, 255), blanc=(255, 255, 255),
                jaune=(255, 214, 70), orange=(255, 160, 60))
GLOBAL = ("etape", "étape")                                                # bandeau de titre {etape "LE MIROIR"} (jamais de « 1/2 »)
def fabrique(path):
    head, blocs = lire(path)
    if not blocs:
        raise SystemExit("aucun décor dans le scénario")
    titre = head.get("TITRE", os.path.splitext(os.path.basename(path))[0])
    nom = "".join(ch for ch in unicodedata.normalize("NFD", titre) if not unicodedata.combining(ch))
    nom = re.sub(r"\s+", " ", re.sub(r"[^\w \-']", "", nom)).strip()
    persos = [p.strip().upper() for p in head.get("PERSONNAGES", "").split(",") if p.strip()]
    fmt = "paysage" if norm(head.get("FORMAT", "vertical")) in ("horizontal", "paysage", "16:9", "16/9") else "portrait"
    base = kit.THEMES.get(norm(head.get("THEME", "sketch")), kit.THEMES["sketch"])
    theme = pxv.Theme(**{k: getattr(base, k) for k in ("bandeau", "bandeau_fond", "bandeau_accent", "bandeau_texte",
                                                      "bandeau_contour", "grain", "chaleur", "vignette", "lignes",
                                                      "cta", "cta_couleurs", "etiquette", "carte",
                                                      "film", "st_maxc", "st_largeur", "vignette_st", "src_droite",
                                                      "cinema")}, format=fmt)
    FILM["actif"], FILM["bande"] = bool(getattr(theme, "film", False)), getattr(theme, "cinema", 0)
    FILM["calme"] = norm(head.get("CAMERA", "")) in ("calme", "posee", "posée", "fixe")   # caméra de film posée
    FILM["baton"] = norm(head.get("BATON_MOUSSA", "")) in ("oui", "yes", "1", "vrai")   # Moussa garde son bâton de berger
    FILM["accroche_fin"] = (float(head.get("ACCROCHE_DUREE", "2.6").replace(",", ".")) if head.get("ACCROCHE") else 0.0)
    pxv.RELIEF_PROLONGE = FILM["actif"]                          # films : plus de ligne noire sous l'horizon
    for b in blocs:
        for it in b["items"]:
            if it["type"] in ("ligne", "action") and not duo.anime(it["qui"]):
                raise SystemExit(f"ligne {it['n']} : personnage inconnu « {it['qui']} »")
    # répliques + silences voulus (plans muets, SMS, cartons) avant chacune
    repliques, repliques_voix, avant, pending = [], [], {}, 0.0      # repliques_voix : avec les balises [dark]… (ElevenLabs)
    for b in blocs:
        for it in b["items"]:
            if it["type"] == "ligne":
                if pending:
                    avant[len(repliques)] = avant.get(len(repliques), 0) + pending
                    pending = 0.0
                it["k"] = len(repliques)
                repliques.append((it["qui"], it["texte"]))
                repliques_voix.append((it["qui"], it.get("texte_voix", it["texte"])))
            elif it["type"] == "sms":
                it["d"] = duree_sms(len(it["msgs"]))
                pending += it["d"]
            elif it["type"] == "carton":
                it["d"] = 2.4
                pending += it["d"]
            elif it["type"] == "muet":
                pending += it["d"]
    if not repliques:
        raise SystemExit("aucune réplique dans le scénario")
    code = head.get("CODE") or (re.sub(r"\W", "", nom.upper())[:10] or "SCENE")
    voix = head.get("VOIX") or os.path.join(os.path.dirname(os.path.abspath(path)), "voix_" + code.lower())
    if head.get("VOIX") and not os.path.isabs(voix):               # « VOIX: FILM/<film>/voix » : à partir du dossier qui
        voix = os.path.join(pxv.BASE, voix)                        # contient _MOTEUR_PIXEL (marche sur un autre ordinateur)
    import estime                                                  # maquette : durées mesurées sur les vraies voix
    durees = [estime.duree(q_, t_, tv_) for (q_, t_), (_, tv_) in zip(repliques, repliques_voix)]
    D = kit.dialogue(voix, code, repliques, avant=avant, serre=True,    # pas de respiration ni de seconde morte
                     durees=durees)
    fin = any(it["type"] == "fin" for b in blocs for it in b["items"])
    duree_fin = float(head.get("DUREE_FIN", "2.0").replace(",", "."))   # fin courte : meilleur taux de visionnage complet
    queue = float(head.get("QUEUE", "0.5").replace(",", "."))      # QUEUE: 6 -> 6 s d'image après la dernière réplique
    kit.allonge(D, (duree_fin if fin else queue) + pending)
    L = D.lines
    for b in blocs:                                                # instant de chaque schéma (le mot où il est écrit)
        for it in b["items"]:
            if it["type"] == "ligne":
                tout_ = [(explique.temps(D, it["k"], idx), cmd) for (idx, cmd) in it.get("visuels", [])]
                tout_ = [(t, _lettres_calees(D, it["k"], t, c) if c.split()[0].lower() == "lettres" else c)
                         for (t, c) in tout_]
                it["annot"] = [(t, c) for (t, c) in tout_ if c.split()[0].lower() in ANNOT]
                it["global"] = [(t, c) for (t, c) in tout_ if c.split()[0].lower() in GLOBAL]
                it["ordres"] = [(t, c) for (t, c) in tout_ if c.split()[0].lower() not in ANNOT + GLOBAL]
                if it["ordres"] and all(c.split()[0].lower() in ("source", "texte") for (_, c) in it["ordres"]) \
                        and it["act"]["plan"] != "schema":                # texte / source seuls : sur la scène
                    it["src_scene"] = [(t, c) for (t, c) in it["ordres"] if c.split()[0].lower() == "source"]
                    it["txt_scene"] = [(t, c) for (t, c) in it["ordres"] if c.split()[0].lower() == "texte"]
                    it["ordres"] = []
    demo = norm(head.get("DEMO", "non")) in ("oui", "1", "vrai")
    # minutage de chaque élément du récit
    tous = [(b, it) for b in blocs for it in b["items"]]
    curt = 0.0
    for i, (b, it) in enumerate(tous):
        ty = it["type"]
        if ty == "ligne":
            it["t0"], it["t1"] = L[it["k"]]["t0"], L[it["k"]]["t1"] + 0.08
            curt = max(curt, it["t1"])
        elif ty in ("action", "notif", "legende"):
            it["t0"] = it["t1"] = curt
        elif ty == "fin":
            it["t0"], it["t1"] = curt, D.dur
            curt = D.dur
        else:                                                      # muet, sms, carton
            it["t0"] = curt
            suiv = tous[i + 1][1] if i + 1 < len(tous) else None
            if suiv is None:
                it["t1"] = D.dur
            elif suiv["type"] == "ligne":
                it["t1"] = max(curt + 0.3, L[suiv["k"]]["t0"])
            else:
                it["t1"] = curt + it["d"]
            curt = it["t1"]
    for b in blocs:                                                # bornes de chaque décor
        b["t0"] = min((it["t0"] for it in b["items"]), default=0.0)
    blocs[0]["t0"] = 0.0
    for i, b in enumerate(blocs):
        b["t1"] = blocs[i + 1]["t0"] if i + 1 < len(blocs) else D.dur
    lignes_ = [it for b in blocs for it in b["items"] if it["type"] == "ligne"]
    etapes = [(t, c) for it in lignes_ for (t, c) in it.get("global", [])]
    citations = [t for it in lignes_ for (t, _) in it.get("txt_scene", [])]
    ETAPES = bandeaux_etapes(etapes, coupe=citations) if etapes else None
    plans = []
    for b in blocs:
        if b["t1"] - b["t0"] > 0.04:
            plans += plans_du_bloc(b, D, persos, theme, demo, etapes=ETAPES)
    music = head.get("MUSIQUE", "fond_espoir")
    if music and norm(music) not in ("aucune", "non", "sans"):
        music = music if os.path.isabs(music) else MUSIQUES + music + ("" if music.endswith(".mp3") else ".mp3")
        music = music if os.path.exists(music) else None
    else:
        music = None
    VID = pxv.Video(D, plans, music=music, music_gain=0.06, theme=theme)
    emos = []                                                   # musique d'émotion (option de bloc « emotion » / « emotion b »)
    for b in blocs:
        for o in b["options"]:
            m_e = re.match(r"emotion(?:\s+([ab]))?$", norm(o))
            if m_e and b["t1"] - b["t0"] > 0.04:
                piste = EMOTIONS[m_e.group(1) or "a"]
                if emos and b["t0"] - emos[-1][1] < 0.6 and emos[-1][2] == piste:
                    emos[-1] = (emos[-1][0], b["t1"], piste)
                else:
                    emos.append((b["t0"], b["t1"], piste))
    VID.emotions = emos
    # GARDER L'ATTENTION : texte d'accroche des premières secondes + bandeaux-titres d'étapes (sans numéro)
    if head.get("ACCROCHE"):
        premier = next((it for b in blocs for it in b["items"] if it["type"] == "ligne"), None)
        a_gauche = premier is not None and any(c.split()[0].lower() in ("selfie", "photographe")
                                               for (_, c) in premier.get("ordres", []))
        VID.globaux.append(accroche([x.strip() for x in head["ACCROCHE"].split("/") if x.strip()], a_gauche,
                                    duree=float(head.get("ACCROCHE_DUREE", "2.6").replace(",", "."))))
    if ETAPES is not None:
        VID.globaux.append(ETAPES)
        VID.sons += [(t, "tr_whoosh_doux", 0.04, None) for (t, _) in etapes]
    if not FILM["actif"]:                                          # Shorts à scénario (11/11/2026 ; ni films ni VOP) :
        VID.encodage_rapide = True                                 # encodage 4 fois plus rapide, même qualité mesurée
        VID.volume_exact = True                                    # volume ramené à la cible à 0,5 LUFS près
    return VID, nom, os.path.dirname(os.path.abspath(path)), code, voix, repliques_voix


def plans_du_bloc(b, D, persos, theme, demo=False, etapes=None):
    bg, t0, t1 = b["decor"], b["t0"], b["t1"]
    sc = scene.Scene(t0, t1, bg)
    opts = [norm(o) for o in b["options"]]
    cam_fixee = serre = False
    for o, brut in zip(opts, b["options"]):
        if o == "pluie":
            sc.pluie(); sc.ambiance("amb_pluie", 0.6)
        elif o == "neige":
            sc.neige()
        elif o == "feuilles":
            sc.feuilles()
        elif o == "lucioles":
            sc.lucioles()
        elif o == "voitures":
            sc.voitures(phares=bg.endswith("_nuit"))
        elif o == "passants":
            sc.passants(n=3)
        elif o == "foule":
            sc.passants(n=6, seed=4)
        elif o == "oiseaux":
            sc.oiseaux(y=420)
        elif o == "feu":
            sc.feu(540, lieux.spot(bg)["gauche"][1] + 150)
        m_ra = re.match(r"rassemblement(?:\s+([\d.]+))?(?:\s+([\d.]+))?$", o)    # rassemblement 0.5 6 : sur la carte
        if m_ra:
            sc.anims.append(decors_film3.anim_rassemblement(float(m_ra.group(1) or 0.5), float(m_ra.group(2) or 6)))
        m_fl = re.match(r"(sauterelles|betes|grenouilles)(?:\s+([\d.]+))?$", o)    # fléaux : sauterelles 0.5 …
        if m_fl:
            f_ = dict(sauterelles=decors_film4.anim_sauterelles, betes=decors_film4.anim_betes,
                      grenouilles=decors_film4.anim_grenouilles)[m_fl.group(1)]
            (sc.avant if m_fl.group(1) == "sauterelles" else sc.anims).append(f_(float(m_fl.group(2) or 0.3)))
        decors_gog.option(sc, o, bg)                                             # options du film Gog et Magog
        m_ar = re.match(r"armee(?:\s+([\d.]+))?$", o)                             # armee 0.5 : la poussière de l'armée, au loin
        if m_ar:
            sc.anims.append(decors_film4.anim_poussiere_armee(float(m_ar.group(1) or 0.3)))
        if o == "mer_vie":                                                      # la mer qui vit (decors_mer)
            if bg.startswith("mer_couloir"):
                sc.anims.append(decors_mer.anim_vie_couloir())
            elif bg.startswith("mer_rivage"):
                sc.anims.append(decors_mer.anim_vie_rivage())
            elif bg == "mer_face":
                sc.anims.append(decors_mer.anim_vie_rivage(ligne_face=True))
            elif bg == "sous_la_mer":
                sc.anims.append(decors_mer.anim_sous_mer())
        if o == "tribus":                                                       # les tribus dans les douze chemins
            sc.anims.append(decors_mer.anim_tribus())
        m_cd = re.match(r"cendres(?:\s+([\d.]+))?(?:\s+([\d.]+))?(?:\s+(-?\d+)\s+(-?\d+))?$", o)   # cendres 0.4 4.5 [x y]
        if m_cd:                                                                # les cendres du veau d'or vers la mer
            sc.avant.append(decors_film4.anim_cendres(float(m_cd.group(1) or 0.4), duree=float(m_cd.group(2) or 4.5),
                                                      x0=int(m_cd.group(3)) / 4 if m_cd.group(3) else 130,
                                                      y0=int(m_cd.group(4)) / 4 if m_cd.group(4) else 280))
        m_nr = re.match(r"noir\s+([\d.]+)(?:\s+([\d.]+))?$", o)                 # noir 1 5 : fondu au noir lent (fin)
        if m_nr:
            sc.avant.append(_anim_noir(float(m_nr.group(1)), fondu=float(m_nr.group(2) or 0.4)))
        m_et = re.match(r"etoiles(?:\s+([\d.]+))?$", o)                          # etoiles 0.08 : les nuits qui passent
        if m_et:
            sc.anims.append(decors_film4.anim_etoiles_tournent(0.0, float(m_et.group(1) or 0.06)))
        if o in ("mur", "mur_droit"):                                           # le mur du village (penché / droit)
            if not hasattr(sc, "_mur"):
                sc._mur = [] if o == "mur" else [(-10.0, "redresse")]
                sc.anims.append(decors_film5.anim_mur(sc._mur))
        if o == "demeure":                                                      # la demeure de Qaroun (sur palais_qaroun_vide)
            if not hasattr(sc, "_engl"):
                sc._engl = []
                sc.anims.append(decors_film5.anim_engloutit(sc._engl))
        m_lu = re.match(r"lueur(?:\s+(-?\d+))?(?:\s+(-?\d+))?$", o)            # lueur 680 1048 : la tombe (déjà là)
        if m_lu:
            sc.anims.append(decors_film5.anim_lueur(-10.0, x=int(m_lu.group(1) or 680) / 4, y=int(m_lu.group(2) or 1048) / 4))
        if o == "echelle":                                                      # l'échelle de lumière (déjà là)
            sc.anims.append(decors_film5.anim_echelle(-10.0))
        if o == "arbre_feu":                                                    # le feu qui flambe dans l'arbre (Touwa)
            sc.anims.append(decors_madyan.anim_arbre_feu())
        if o == "voiles":                                                       # voiles qui ondulent (chambre d'Asiya)
            sc.anims.append(decors_film2.anim_voiles(nuit=bg.endswith("_nuit")))
        if o == "petales":                                                      # pétales qui tombent (fête, cadeaux)
            sc.avant.append(decors_film2.anim_petales())
        m_cr = re.match(r"chemin_retour(?:\s+([\d.]+))?(?:\s+([\d.]+))?$", o)   # chemin_retour 0.5 6 : de Madyan vers le Mont
        if m_cr:
            sc.anims.append(decors_film2.anim_carte(float(m_cr.group(1) or 0.5), float(m_cr.group(2) or 6), nuits=0,
                                                    chemin=decors_film2.CHEMIN_RETOUR))
        m_ch = re.match(r"chemin(?:\s+([\d.]+))?(?:\s+([\d.]+))?$", o)          # chemin 0.5 14 : vers Madyan, sur la carte
        if m_ch:
            sc.anims.append(decors_film2.anim_carte(float(m_ch.group(1) or 0.5), float(m_ch.group(2) or 14)))
        if o == "patrouille":                                                   # torches qui passent à la fenêtre
            sc.anims.append(decors_film.anim_patrouille())
        m_ps = re.match(r"porte_salon(?:\s+(-?\d+))?$", o)                      # porte_salon 410 : porte du salon fermée,
        if m_ps:                                                                # lumière dessous (entree_nuit, ISL29 08/11)
            import explique_0811_ecoute
            explique_0811_ecoute.porte_salon(sc, int(m_ps.group(1) or 410))
        m_lum = re.match(r"lumiere_monte(?:\s+([\d.]+))?$", o)                     # une lumière dorée se lève
        if m_lum:
            sc.avant.append(decors_film.anim_lumiere_monte(float(m_lum.group(1) or 0.5)))
        m_amb = re.match(r"ambiance\s+(\w+)(?:\s+([\d.]+))?$", o)                 # ambiance amb_fleuve 0.5
        if m_amb:
            sc.ambiance(m_amb.group(1), float(m_amb.group(2) or 0.5))
        m_obj = re.match(r"objet\s+(\w+)\s*\(\s*(\d+)\s*(?:,\s*(\d+))?\s*\)", o)       # objet rocher (640, 1185)
        if m_obj:
            sc.accessoire(m_obj.group(1), int(m_obj.group(2)), int(m_obj.group(3)) if m_obj.group(3) else None)
            if m_obj.group(1) == "rocher":
                sc._x_rocher = int(m_obj.group(2))                    # le même rocher dans le gros plan sur l'écume
        # ORBES de lumière (prophète, Compagnons : jamais dessinés) : orbe "LE PROPHÈTE" (760, 1060) dore grand
        #                                                          orbes "DES COMPAGNONS" 3 (300, 1100) pensees
        m_orb = re.match(r'orbes?\s+"(.+?)"\s*(\d+)?\s*\(\s*(\d+)\s*(?:,\s*(\d+))?\s*\)\s*(.*)$', brut.strip(), re.I)
        if m_orb:
            o_ = norm(m_orb.group(5) or "").split()
            t_ch = next((t for it in b["items"] if it["type"] == "ligne" for (t, _) in it.get("txt_scene", [])), None)
            m_at = re.search(r"@(\S+)", m_orb.group(5) or "")             # « @Prophète » : apparaît sur ce mot
            t_app = None
            if m_at:
                for it in b["items"]:
                    if it["type"] == "ligne" and any(m_at.group(1).lower() in w["t"].lower() for w in D.lines[it["k"]]["words"]):
                        t_app = D.at(it["k"], m_at.group(1))
                        break
            sc.orbes(int(m_orb.group(3)), int(m_orb.group(4)) if m_orb.group(4) else lieux.spot(bg)["gauche"][1] - 260,
                     m_orb.group(1).upper(), n=int(m_orb.group(2) or 1), grand="grand" in o_,
                     dore="dore" in o_ or "doré" in o_, pensees="pensees" in o_,
                     t_chasse=(t_ch - t0) if t_ch is not None else None,   # la réponse (citation) chasse leurs nuages
                     t_in=max(0.0, t_app - t0 - 0.2) if t_app is not None else 0.0)
        if o in ("serre", "plan serre", "a deux", "deux"):              # plan à deux, serré : on voit les deux visages
            ys = lieux.spot(bg)["gauche"][1]
            sc.camera([(0.0, 1.32, (540, ys - 330)), (t1 - t0, 1.38, (540, ys - 340))])
            cam_fixee = serre = True
        m = re.match(r"ensemble\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)", o)
        if m:
            sc.camera([(0.0, 1.0, (540, 960)), (t1 - t0, 1.3, (int(m.group(1)), int(m.group(2))))])
            cam_fixee = True
        m = re.match(r'texte\s+"(.+)"', brut.strip(), re.I)
        if m:
            big = pxv.big_title([(m.group(1), (255, 255, 255))], size=80)
            d_ = min(t1 - t0, 3.0)
            sc.texte(lambda img, u, big=big, d_=d_: img.alpha_composite(
                scene._fade(big, scene._env(u, d_, 0.5, 0.5)), (int(img.width / 2 - big.width / 2), int(img.height * 0.2)))
                if u < d_ else None)
    # qui joue dans ce décor (le 1er de PERSONNAGES à gauche, le 2e à droite, le 3e au milieu)
    qui = []
    for it in b["items"]:                                         # (un perso en voix off n'est pas dans le décor)
        if it["type"] in ("ligne", "action") and it["qui"] not in qui and not it["act"].get("off"):
            qui.append(it["qui"])
    ordre = [p for p in persos if p in qui] + [p for p in qui if p not in persos]
    sp = lieux.spot(bg)
    places = [sp["gauche"], sp["droite"], (sp["droite"][0] + 170, sp["droite"][1] - 12)]   # le 3e rejoint le 2e
    roles = {}
    for i, w in enumerate(ordre):
        x, y = places[min(i, 2)]
        roles[w] = sc.role(w, x=x, y=y)
    # FILM, en-tête BATON_MOUSSA: oui (02/11/2026, « mets le bâton à Moussa tout le temps à partir du moment où il est
    # berger ») : dans chaque décor où est l'orbe de Moussa, son bâton est à côté de lui et le suit partout.
    # Option de décor « sans_baton » : pas de bâton (ex. les cieux) ; {apparait BATON} : caché jusqu'à ce mot.
    if FILM.get("baton") and "MOUSSA" in roles and not {"sans_baton", "sans baton"} & set(opts):
        if "BATON" not in roles:
            roles["BATON"] = sc.role("BATON", x=roles["MOUSSA"].x0 + 90, y=roles["MOUSSA"].y0 - 4)
        _baton_suit(roles["BATON"], roles["MOUSSA"], roles)

    def autre(w):
        return next((r for k, r in roles.items() if k != w), None)

    gestes = []                                                   # gestes d'une réplique : on revient au repos après

    def appliquer(w, act, u, u1=None):
        r = roles.get(w)
        if r is None:
            return
        st = {}
        if act["pose"]:
            st["pose"] = act["pose"]
            if u1 is not None and act["pose"] in GESTES:
                gestes.append((r, u, u1))
        if act["face"]:
            st["face"] = act["face"]
        if act["objet"]:
            st["objet"] = act["objet"]
        if act.get("place") is not None and u < 0.1 and not r.moves:   # placement au début du décor (avant le siège)
            pl = act["place"]
            if isinstance(pl, str):
                xy = lieux.spot(bg).get(pl)
                if xy is None:
                    print(f"(place inconnue dans {bg} : {pl})")
                else:
                    r.x0, r.y0 = xy
            elif isinstance(pl, tuple):
                r.x0, r.y0 = pl
            else:
                r.x0 = pl
        if act["assis"] is not None:
            st["assis"] = act["assis"]
            if act["assis"] and not getattr(r, "_chaise", False):
                if act.get("siege") != "aucun":                    # « sur le lit » : le siège fait partie du décor
                    sc.meuble(act.get("siege") or "chaise", r.pos(u)[0], r.pos(u)[1], regard="gauche" if r.miroir(u) else "droite")
                r._chaise = True
        if st:
            r.a(max(0.0, u), **st)
        if act.get("traverse"):                                     # passe d'un bord à l'autre, devant les autres
            depuis_droite = r.x0 > 540
            r.x0 = W_MONDE + 170 if depuis_droite else -170
            r.y0 += 45
            fin_autres = max([m[1] for r2 in roles.values() if r2 is not r for m in r2.moves] + [0.0])
            u_t = max(u, fin_autres + 0.1)                          # attend que les autres aient fini de bouger
            r.marche(u_t, u_t + 3.4, -190 if depuis_droite else W_MONDE + 190)
        if act["entre"]:
            if act["entre"] == "porte":
                r.cache(); r.apparait(u + 0.2, u + 0.7)
            else:
                cote = act["entre"] if act["entre"] in ("gauche", "droite") else ("gauche" if r.x0 < 540 else "droite")
                r.entre(u, u + 1.5, depuis=cote)
        if act["sort"]:
            vers = act["sort"] if act["sort"] in ("gauche", "droite") else ("droite" if r.pos(u)[0] > 540 else "gauche")
            r.sort(u, u + 1.7, vers=vers)
        if act["tourne"]:
            r.tourne(u)
        if act["approche"]:
            o = autre(w)
            if o is not None:
                ox_, _ = o.pos(u)
                mx, _ = r.pos(u)
                r.marche(u, u + 1.0, mx + (ox_ - mx) * 0.35)
        if act["apparait"]:
            r.cache(); r.apparait(u, u + 0.5)
        fin_u = u1 if u1 is not None else u + 2.0
        for e in act["effets"]:
            sc.effet(r, u + 0.1, fin_u, e)
        if act["rit"]:
            r.rit(u + 0.15, fin_u)
        if act["sautille"]:
            r.sautille(u, fin_u)
        if act["bulle"]:
            sc.bulle(r, u + 0.05, min(fin_u, u + 1.8), act["bulle"])
        if act["pensee"]:
            sc.pensee(r, u + 0.1, fin_u, act["pensee"] if act["pensee"] in objets.ICONES else "ampoule")
        if act["donne"]:
            obj, cible = act["donne"]
            c_ = roles.get(cible) or autre(w)
            if c_ is not None:
                sc.donne(u + 0.5, u + 1.3, r, c_, obj)

    pending_notif, coupes, serres = None, [], []
    fin_u = next((it["t0"] - t0 for it in b["items"] if it["type"] == "fin"), None)
    for it in b["items"]:
        u = it["t0"] - t0
        if it["type"] == "action":
            appliquer(it["qui"], it["act"], u)
        elif it["type"] == "notif":
            pending_notif = it
        elif it["type"] == "legende":
            sc.texte(_depuis(u, scene.legende(it["titre"], it["code"]), fin=fin_u))   # s'efface avant « abonne-toi »
        elif it["type"] == "ligne":
            u1 = it["t1"] - t0
            appliquer(it["qui"], it["act"], u, u1)
            if pending_notif:
                sc.notification(u, min(u1 + 0.8, t1 - t0), pending_notif["qui"], pending_notif["texte"])
                pending_notif = None
            if it["act"]["gros_plan"] and it["qui"] in roles and not getattr(theme, "film", False):
                serres.append((it, u))
        elif it["type"] == "sms":
            msgs = [(0.5 + 1.1 * i, "moi" if m.startswith(">") else "lui", m.lstrip(">").strip())
                    for i, m in enumerate(it["msgs"])]
            coupes.append((it["t0"], it["t1"], scene.sms(it["t0"], it["t1"], it["qui"], msgs, bg=bg,
                                                          avatar=it["qui"] if duo.is_char(it["qui"]) else None)))
        elif it["type"] == "carton":
            coupes.append((it["t0"], it["t1"], scene.carton(it["t0"], it["t1"], it["texte"], sous=it["sous"])))
        elif it["type"] == "fin":
            for r in roles.values():
                r.a(u + 0.3, pose="neutre", objet="aucun")
                r.rit(u + 0.4, t1 - t0)
            sc.texte(_cta_depuis(u, theme))
    for (r, u, u1) in gestes:                                     # fin du geste : retour au repos (sauf nouveau geste)
        if not any("pose" in d and u < t <= u1 + 0.6 for (t, d) in r.etats):
            r.a(u1 + 0.15, pose=repos(r.etat(u1).get("objet")))
    affiches = []                                                 # sources sur la scène : [début, fin, texte]
    for it in b["items"]:
        srcs = it.get("src_scene", []) if it["type"] == "ligne" else []
        for j, (t, c) in enumerate(srcs):                         # la source reste pendant TOUTE sa réplique, pas après
            m_ = re.search(r'"(.+)"', c)
            txt_ = m_.group(1) if m_ else c.split(None, 1)[1]
            a_ = (it["t0"] + 0.1) if j == 0 else t
            b_ = (srcs[j + 1][0] - 0.45) if j + 1 < len(srcs) else (it["t1"] - 0.3)
            if affiches and affiches[-1][2] == txt_ and a_ - affiches[-1][1] < 0.9:
                affiches[-1][1] = b_                              # même source à la réplique suivante : elle reste
            else:
                affiches.append([a_, b_, txt_])
    for (a_, b_, txt_) in affiches:
        sc.texte(_depuis(a_ - t0, _tag_source(txt_, etapes, a_), fin=max(a_ + 0.5, b_) - t0))
    for it in b["items"]:                                         # citations affichées sur la scène
        for (t, c) in it.get("txt_scene", []) if it["type"] == "ligne" else []:
            m_ = re.search(r'"(.+)"', c)
            fin_c = it["t1"] + 1.0 - t0
            if fin_u is not None and fin_u > t - t0:                   # jamais par-dessus « abonne-toi »
                fin_c = min(fin_c, fin_u - 0.05)
            sc.texte(_depuis(t - t0, _citation(m_.group(1) if m_ else c.split(None, 1)[1]), fin=fin_c))
            sc.son(t - t0, "sa_ting", 0.03)
    for it in b["items"]:                                         # MONTRER dans la scène : étiquette, règle…
        if it["type"] != "ligne" or not it.get("annot") or it.get("ordres"):
            continue
        fin_a = it["t1"] + 1.2 - t0
        for (t, c) in it["annot"]:
            mots = c.split()
            k_ = mots[0].lower()
            if k_ in ("ecume", "écume"):                           # l'écume de la mer (pas de perso)
                m_ = re.search(r'"(.+)"', c)
                sc.ecume(t - t0, m_.group(1).upper() if m_ else "TES PÉCHÉS")
                if demo:
                    sc.texte(_depuis(t - t0, _code_demo(c), fin=t - t0 + 1.6, fondu=0.3))
                continue
            if k_ == "repousse":                                    # géré avec « pensees »
                continue
            if k_ in ("cadre", "large", "gros"):                    # film : la caméra (camera_film) s'en occupe
                continue
            if k_ == "devient" and len(mots) > 1:                   # {devient ruelle_nuit_eteinte 1.5} : le décor change
                d_ = next((float(m_.rstrip("s").replace(",", ".")) for m_ in mots[2:]
                           if re.match(r"^\d+([.,]\d+)?s?$", m_)), 1.2)
                sc.lumiere(t - t0, mots[1], d_)
                continue
            if k_ in ("fleau", "fléau") and len(mots) > 1:           # {fleau sauterelles|betes|grenouilles} … {fleau stop X}
                if not hasattr(sc, "_fleaux"):
                    sc._fleaux = {}
                if mots[1].lower() == "stop" and len(mots) > 2:
                    if mots[2].lower() in sc._fleaux:
                        sc._fleaux[mots[2].lower()]["fin"] = t - t0
                elif mots[1].lower() in ("sauterelles", "betes", "grenouilles"):
                    h_ = {"fin": None}
                    sc._fleaux[mots[1].lower()] = h_
                    f_ = dict(sauterelles=decors_film4.anim_sauterelles, betes=decors_film4.anim_betes,
                              grenouilles=decors_film4.anim_grenouilles)[mots[1].lower()](t - t0)

                    def g_(img, u, f_=f_, h_=h_):
                        fin_ = h_["fin"]
                        if fin_ is None or u <= fin_:
                            f_(img, u)
                        elif u < fin_ + 1.0:                         # s'efface en 1 s
                            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
                            f_(lay, u)
                            al = np.array(lay.getchannel("A"), np.float32) * (1.0 - (u - fin_))
                            lay.putalpha(Image.fromarray(al.astype(np.uint8)))
                            img.alpha_composite(lay)
                    (sc.avant if mots[1].lower() == "sauterelles" else sc.anims).append(g_)
                continue
            if k_ == "duel" and len(mots) > 1:                       # {duel cordes|jette|happe|fin} : le jour de la fête
                if not hasattr(sc, "_duel"):
                    sc._duel = []
                    sc.anims.append(decors_film3.anim_duel(sc._duel))
                sc._duel.append((t - t0, mots[1].lower()))
                continue
            if k_ == "serpent" and len(mots) > 1:                    # {serpent depart|avale|engloutit|revient|fin}
                if not hasattr(sc, "_serpent"):
                    sc._serpent = []
                    sc.anims.append(decors_madyan.anim_serpent(sc._serpent))
                x_s = int(mots[2]) / 4 if len(mots) > 2 and mots[2].lstrip("-").isdigit() else None   # x du monde (option)
                sc._serpent.append((t - t0, mots[1].lower(), x_s))
                continue
            if k_ in decors_gog.ANNOTATIONS:                         # film Gog et Magog : {barrage_tombe 13} {lac_bu 9}…
                decors_gog.annotation(sc, k_, mots, t - t0, bg)
                continue
            if k_ in ("sources", "manne", "nuage"):                  # {sources [x]} {manne} {nuage} : les bienfaits du désert
                if k_ == "sources":                                  # {sources x [y]} (coordonnées de la scène)
                    xs_ = int(mots[1]) / 4 if len(mots) > 1 and mots[1].lstrip("-").isdigit() else 135
                    ys_ = int(mots[2]) / 4 if len(mots) > 2 and mots[2].lstrip("-").isdigit() else 300
                    sc.anims.append(decors_film4.anim_sources(t - t0, x=xs_, y=ys_))
                elif k_ == "manne":
                    sc.anims.append(decors_film4.anim_manne(t - t0))
                else:
                    sc.avant.append(decors_film4.anim_nuage(t - t0))
                continue
            nb5 = [int(m_) for m_ in mots[1:] if m_.lstrip("-").isdigit()]
            d5 = next((float(m_[:-1].replace(",", ".")) for m_ in mots[1:] if re.match(r"^\d+([.,]\d+)?s$", m_)), None)
            if k_ == "poisson":                                      # {poisson [x0 y0 x1 y1]} : le poisson file dans la mer
                kw_ = dict(zip(("x0", "y0", "x1", "y1"), [v_ / 4 for v_ in nb5[:4]]))
                sc.anims.append(decors_film5.anim_poisson(t - t0, **kw_))
                continue
            if k_ == "mur":                                          # {mur redresse} : le mur penché se redresse
                if not hasattr(sc, "_mur"):
                    sc._mur = []
                    sc.anims.append(decors_film5.anim_mur(sc._mur))
                sc._mur.append((t - t0, mots[1].lower() if len(mots) > 1 else "redresse"))
                continue
            if k_ == "engloutit":                                    # {engloutit} : la terre engloutit la demeure
                if not hasattr(sc, "_engl"):
                    sc._engl = []
                    sc.anims.append(decors_film5.anim_engloutit(sc._engl, duree=d5 or 5.0))
                sc._engl.append(t - t0)
                continue
            if k_ == "lueur":                                        # {lueur [x y]} : la lumière douce de la tombe
                kw_ = dict(zip(("x", "y"), [v_ / 4 for v_ in nb5[:2]]))
                sc.anims.append(decors_film5.anim_lueur(t - t0, **kw_))
                continue
            if k_ == "echelle":                                      # {echelle [x]} : l'échelle de lumière (les cieux)
                kw_ = dict(zip(("x",), [v_ / 4 for v_ in nb5[:1]]))
                sc.anims.append(decors_film5.anim_echelle(t - t0, **kw_))
                continue
            if k_ == "tableau" and len(mots) > 1:                    # {tableau bateau_roi 7s} : un tableau à l'écran
                sc.texte(decors_film5.anim_tableau(mots[1], t - t0, duree=d5 or 6.0))
                continue
            if k_ == "cailles":                                      # {cailles} : des cailles se posent par dizaines
                sc.anims.append(decors_film4.anim_cailles(t - t0))
                continue
            if k_ == "foudre":                                       # {foudre [x]} : la foudre, une lumière pâle (douce)
                xf_ = int(mots[1]) / 4 if len(mots) > 1 and mots[1].lstrip("-").isdigit() else 200
                sc.avant.append(decors_film4.anim_foudre(t - t0, cx=xf_))
                continue
            if k_ == "cendres":                                      # {cendres [x] [y]} : cendres emportées vers la mer
                nb_ = [int(m_) for m_ in mots[1:3] if m_.lstrip("-").isdigit()]
                sc.avant.append(decors_film4.anim_cendres(t - t0, x0=nb_[0] / 4 if nb_ else 170,
                                                          y0=nb_[1] / 4 if len(nb_) > 1 else 284))
                continue
            if k_ in ("poussiere", "poussière"):                     # {poussiere} : le mont pulvérisé, nuage de poussière
                sc.avant.append(decors_film4.anim_poussiere_mont(t - t0))
                continue
            if k_ in ("mer_fend", "mer_referme"):                    # {mer_fend 6} : la mer se fend (sur mer_face) ;
                d_m = next((float(m_.rstrip("s").replace(",", ".")) for m_ in mots[1:]   # {mer_referme 3.4} : elle se
                            if re.match(r"^\d+([.,]\d+)?s?$", m_)), None)                  # referme (devant les persos)
                if k_ == "mer_fend":
                    sc.anims.append(decors_mer.anim_mer_fend(t - t0, duree=d_m or 6.0))
                else:
                    sc.avant.append(decors_mer.anim_mer_referme(t - t0, duree=d_m or 3.4))
                continue
            if k_ == "vagues":                                       # {vagues 300} : les flots montent devant les persos
                niv_ = int(mots[1]) if len(mots) > 1 and mots[1].isdigit() else 300
                sc.avant.append(decors_film4.anim_vagues(t - t0, niveau=niv_))
                continue
            if k_ == "noir":                                         # {noir} : l'image passe au noir jusqu'à la fin du bloc
                d_n = next((float(m_[:-1].replace(",", ".")) for m_ in mots[1:] if re.match(r"^\d+([.,]\d+)?s$", m_)), None)
                lent = next((float(m_.replace(",", ".")) for m_ in mots[1:] if re.match(r"^\d+([.,]\d+)?$", m_)), None)
                sc.avant.append(_anim_noir(t - t0, fondu=lent or 0.4, fin=(t - t0 + d_n) if d_n else None))
                continue
            if k_ == "feu_reve":                                     # {feu_reve} : le feu du rêve part sur ce mot
                sc.anims.append(decors_film.anim_feu_reve(t - t0))
                continue
            if k_ == "son" and len(mots) > 1:                       # {son dv_porte_bois 0.12} : bruitage pile sur ce mot
                g_ = next((float(m_) for m_ in mots[2:] if re.match(r"^\d*\.?\d+$", m_)), 0.12)
                sc.son(t - t0, mots[1], g_)
                continue
            ra = roles.get(mots[1].upper()) if len(mots) > 1 else None
            if ra is None:
                print(f"(annotation ignorée : {c})")
                continue
            u_ = t - t0
            if k_ in ("etiquette", "étiquette"):
                m_ = re.search(r'"(.+)"\s*(\w+)?', c)
                coul = COULEURS.get(norm(m_.group(2)) if m_ and m_.group(2) else "", (255, 214, 70))
                sc.etiquette(ra, u_, fin_a, (m_.group(1) if m_ else " ".join(mots[2:])).upper(), couleur=coul)
            elif k_ in ("pensees", "pensées"):
                rep_ = next((tt for b2 in [b] for it2 in b2["items"] if it2["type"] == "ligne"
                             for (tt, cc) in it2.get("annot", []) if cc.lower().startswith("repousse")
                             and len(cc.split()) > 1 and cc.split()[1].upper() == ra.who and tt > t), None)
                fin_p = (rep_ - t0 + 1.0) if rep_ is not None else fin_a
                sc.pensees(ra, u_, fin_p, t_repousse=(rep_ - t0) if rep_ is not None else None)
            elif k_ == "va" and len(mots) > 2 and mots[2].lstrip("-").isdigit():   # il marche jusqu'à x (calme)
                x_ = int(mots[2])
                dur = max(1.2, abs(x_ - ra.pos(u_)[0]) / 150)
                d_va = next((float(m_[:-1].replace(",", ".")) for m_ in mots[3:] if re.match(r"^\d+([.,]\d+)?s$", m_)), None)
                if d_va:                                                    # {va X 900 6s} : il y met n secondes
                    dur = d_va
                devant = "devant" in [m_.lower() for m_ in mots[3:]]       # {va MAMIE 520 devant} : passe devant les autres
                ra.marche(u_, u_ + dur, x_, y=(ra.y0 + 45) if devant else None)
            elif k_ == "souvenir" and len(mots) > 2:                # {souvenir MOUSSA palais_egypte [dx] [dy] [3s]}
                xr, yr = ra.pos(u_)
                nb = [float(m_) for m_ in mots[3:] if re.match(r"^-?\d+(\.\d+)?$", m_)]
                du = next((float(m_[:-1]) for m_ in mots[3:] if re.match(r"^\d+(\.\d+)?s$", m_)), 2.8)
                sc.avant.append(decors_madyan.anim_souvenir(mots[2], u_, duree=du, cx=xr / 4 + (nb[0] if nb else 0),
                                                             cy=yr / 4 - 80 + (nb[1] if len(nb) > 1 else 0)))
            elif k_ == "danse":                                      # {danse FOULE [6s]} : il sautille (fête) n secondes
                d_ = next((float(m_[:-1].replace(",", ".")) for m_ in mots[2:] if re.match(r"^\d+([.,]\d+)?s$", m_)), 4.0)
                ra.sautille(u_, u_ + d_, amp=10)
            elif k_ == "main_blanche":                               # {main_blanche MOUSSA} : la main blanche (28:32)
                sc.main_blanche(ra, u_)
            elif k_ == "court" and len(mots) > 2 and mots[2].lstrip("-").isdigit():   # {court MESSAGER 600} : il court
                x_ = int(mots[2])
                ra.court(u_, u_ + max(0.8, abs(x_ - ra.pos(u_)[0]) / 330), x_)
            elif k_ in ("derive", "dérive") and len(mots) > 2 and mots[2].lstrip("-").isdigit():
                # {derive COFFRE 900 [1180] [8s]} : glisse lentement (sans pas) jusqu'à x (et y), en n secondes
                x_ = int(mots[2])
                y_ = int(mots[3]) if len(mots) > 3 and mots[3].lstrip("-").isdigit() else None
                d_ = next((float(m_[:-1].replace(",", ".")) for m_ in mots[3:] if re.match(r"^\d+([.,]\d+)?s$", m_)), None)
                xa_, ya_ = ra.pos(u_)
                dist = math.hypot(x_ - xa_, (y_ if y_ is not None else ya_) - ya_)
                ra.glisse(u_, u_ + (d_ or max(2.0, dist / 45.0)), x_, y_)
            elif k_ == "regarde" and len(mots) > 2:               # {regarde X bas|gauche|droite}
                if mots[2].lower() == "bas":
                    ra.a(u_, face="bas")
                else:
                    ra.regarde(u_, mots[2].lower())
            elif k_ == "barre":                                    # son étiquette (celle du moment) est barrée à ce mot
                ra._barres = getattr(ra, "_barres", []) + [u_]
                w_ = getattr(ra, "_etiq_last", None)              # elle reste le temps qu'on voie la barre
                if w_ is not None and w_["t0"] <= u_ <= w_["t1"] + 2.5:
                    w_["t1"] = max(w_["t1"], u_ + 1.3)
                sc.son(u_, "imp_tampon", 0.04)
            elif k_ == "coche":                                    # son étiquette (celle du moment) est cochée à ce mot
                ra._coches = getattr(ra, "_coches", []) + [u_]
                w_ = getattr(ra, "_etiq_last", None)
                if w_ is not None and w_["t0"] <= u_ <= w_["t1"] + 2.5:
                    w_["t1"] = max(w_["t1"], u_ + 1.3)
                sc.son(u_, "sa_ting", 0.04)
            elif k_ in ("peches", "péchés"):                       # ses péchés : écume sale autour de lui
                sc.pensees(ra, u_, fin_a, style="peches")
            elif k_ in ("lumiere", "lumière"):                     # une lumière douce descend sur lui
                sc.rayon(ra, u_, fin_a)
            elif k_ in ("apparait", "apparaît"):                   # {apparait MARYAM} : apparaît en fondu, pile sur ce mot
                if not any(a1_ == 0.0 and t0_ <= u_ for (t0_, t1_, a0_, a1_) in ra.alphas):
                    ra.cache()                                     # (sauf s'il vient de disparaître : il revient)
                d_a = next((float(m_[:-1].replace(",", ".")) for m_ in mots[2:] if re.match(r"^\d+([.,]\d+)?s$", m_)), 0.8)
                ra.apparait(u_, u_ + d_a)
            elif k_ in ("disparait", "disparaît"):                 # {disparait X [3s]} : s'efface en fondu, pile sur ce mot
                d_a = next((float(m_[:-1].replace(",", ".")) for m_ in mots[2:] if re.match(r"^\d+([.,]\d+)?s$", m_)), 0.8)
                ra.disparait(u_, u_ + d_a)
            elif k_ == "geste" and len(mots) > 2:                  # {geste PETIT invoque} : un geste / un visage pile sur ce mot
                mot_ = norm(" ".join(mots[2:]))
                if mot_ in POSES:
                    ra.a(u_, pose=POSES[mot_])
                elif mot_ in FACES:
                    ra.a(u_, face=FACES[mot_])
            elif k_ == "pousse" and len(mots) > 2:
                vers_ = next((int(m_) for m_ in mots[3:] if m_.lstrip("-").isdigit()), None)   # {pousse PETIT trottinette 1250}
                if "mur" in [m_.lower() for m_ in mots[3:]]:                # {pousse PETIT trottinette mur} : rangé contre le mur
                    vers_ = "mur"
                sc.pousse(ra, u_, mots[2].lower(), vers=vers_,
                          apres=next((m_ for m_ in mots[3:] if m_.lower() in ("revient", "continue", "reste")),
                                     "revient").lower())
            elif k_ == "mesure" and len(mots) > 2 and mots[2].upper() in roles:
                sc.mesure(ra, roles[mots[2].upper()], u_, fin_a)
            elif k_ == "projecteur":
                sc.projecteur(ra, u_, fin_a)
            elif k_ == "loupe":
                sc.loupe(ra, u_, fin_a)
            if demo:
                sc.texte(_depuis(u_, _code_demo(c), fin=u_ + 1.6, fondu=0.3))
    # EXPLICATIONS EN IMAGES : répliques avec des {…} (ou « schéma ») qui se suivent = un plan de schéma
    def genre(it):                                                # quel plan cette réplique demande
        cs = [c.split()[0].lower() for (_, c) in it.get("ordres", []) if c.split()]
        if "pov" in cs:                                           # vue subjective (pov.py)
            return "pov"
        if "reflet" in cs:
            return "reflet"
        if any(c in ("ecume", "écume", "vague", "propre", "rocher") for c in cs):
            return "ecume"
        if "selfie" in cs:
            return "selfie"
        if "photographe" in cs:
            return "photo"
        if any(c in ("recule", "avance") for c in cs):
            return "photo+"
        if any(c not in ("texte", "source", "check", "croix", "chiffre", "efface") for c in cs):
            return "schema"
        return None
    segs, cur_seg, cur_genre = [], None, None
    for it in b["items"]:
        if it["type"] != "ligne":
            continue
        if it.get("ordres") or it["act"]["plan"] == "schema":
            g_ = genre(it)
            suite = cur_seg is not None and not it["act"].get("nouveau") and (
                g_ is None or g_ == cur_genre or (g_ == "photo+" and cur_genre == "photo"))
            if not suite:                                         # un nouveau genre de plan : nouveau plan
                cur_seg, cur_genre = [], (g_ if g_ not in (None, "photo+") else "schema")
                segs.append(cur_seg)
            cur_seg.append(it)
        else:
            cur_seg, cur_genre = None, None
    en_schema = set()
    for seg in segs:
        ordres = [o for it in seg for o in it.get("ordres", [])]
        fond = next((c.split()[1] for (_, c) in ordres if c.lower().startswith("fond ") and len(c.split()) > 1), None)
        ordres = [(t, c) for (t, c) in ordres if not c.lower().startswith("fond ")]
        debut = seg[0]["t0"]
        if ordres:
            debut = max(debut - 0.05, min(min(t for t, _ in ordres) - 0.3, seg[0]["t1"] - 0.3))
        if debut - t0 < 0.6:                                      # tout au début du décor : on ouvre directement dessus
            debut = t0
        fin_s = seg[-1]["t1"]
        if ordres:                                                # le dernier élément reste visible au moins 1,1 s
            fin_s = min(max(fin_s, max(t for t, _ in ordres) + 1.1), seg[-1]["t1"] + 0.6, t1)
        debut_ligne = {(t, c): it_["t0"] for it_ in seg for (t, c) in it_.get("ordres", [])}
        ordres = [((max(debut + 0.15, min(t, debut_ligne.get((t, c), t) + 0.1)) if c.split()[0].lower() == "source" else t), c)
                  for (t, c) in ordres]                           # une source s'affiche dès le début de SA réplique
        a_src = seg[0]["t0"] + 0.1                                # la réplique commence sur la scène avant son schéma :
        src0 = next((c for (_, c) in seg[0].get("ordres", []) if c.split()[0].lower() == "source"), None)
        if src0 is not None and a_src < debut - 0.3:              # sa source est déjà là (puis passe sur le schéma)
            m2 = re.search(r'"(.+)"', src0)
            sc.texte(_depuis(a_src - t0, _tag_source(m2.group(1) if m2 else src0.split(None, 1)[1], etapes, a_src),
                             fin=debut - 0.3 - t0))
        anim_ = [_fin_anim(t, c) for (t, c) in ordres if c.lower().split()[0] in ("chrono", "compteur", "lettres", "chiffre",
                                                                                  "radio", "feuilles", "balance", "orteil")
                 or (c.lower().split()[0] in explique.CLES_0411 and _fin_anim(t, c) is not None)
                 or (c.lower().split()[0] in explique.CLES_0411B and _fin_anim(t, c) is not None)
                 or (c.lower().split()[0] in explique.CLES_0611 and _fin_anim(t, c) is not None)
                 or (c.lower().split()[0] in explique.CLES_0811 and _fin_anim(t, c) is not None)
                 or (c.lower().split()[0] in explique.CLES_BRIQUES and _fin_anim(t, c) is not None)]
        if anim_:                                                 # chrono, compteur, lettres, chiffre : le temps de finir + de lire
            fin_s = min(max(fin_s, max(anim_)), seg[-1]["t1"] + 1.4, t1)
        bouge = [t for (t, c) in ordres if c.lower().split()[0] in ("recule", "avance")]
        if bouge:                                                 # démo photo : on laisse le temps de voir l'avant / après
            fin_s = min(max(fin_s, max(bouge) + 3.4), seg[-1]["t1"] + 2.2, t1)
        photo = next(((t, c.split()) for (t, c) in ordres if c.lower().startswith("photographe")), None)
        reflet = next(((t, c.split()) for (t, c) in ordres if c.lower().startswith("reflet")), None)
        selfie = next(((t, c.split()) for (t, c) in ordres if c.lower().startswith("selfie")), None)
        ecu = next(((t, c) for (t, c) in ordres if c.lower().split()[0] in ("ecume", "écume")), None)
        pov_ = any(c.lower().split()[0] == "pov" for (t, c) in ordres)
        if pov_:
            # VUE SUBJECTIVE (Shorts « … tu fais quoi ? ») : le spectateur est à la place de celui qui vit la scène.
            # Le plan va jusqu'à la fin du décor (pas de retour au décor immobile entre deux répliques).
            fin_s = t1
            sh_ = pov.plan(sc, debut, fin_s, [(t - debut, c) for (t, c) in ordres], band=bool(theme.bandeau))
            fins_ = {(t, c): it_["t1"] for it_ in seg for (t, c) in it_.get("ordres", [])}
            srcs_ = sorted((t, c) for (t, c) in ordres if c.lower().split()[0] == "source")
            dern_ = None
            for i_, (t, c) in enumerate(srcs_):                    # une source à la fois (la suivante la remplace) ;
                if c == dern_:                                     # la même source qui revient reste affichée
                    continue
                dern_ = c
                nxt_ = [t2 for (t2, c2) in srcs_[i_ + 1:] if c2 != c]
                m2 = re.search(r'"(.+)"', c)
                sh_.ecran.append(_depuis(t - debut, _tag_source(m2.group(1) if m2 else c.split(None, 1)[1], etapes, t),
                                         fin=(nxt_[0] - debut - 0.25) if nxt_ else None, fondu=0.25))
            for (t, c) in ordres:
                w0 = c.lower().split()[0]
                m2 = re.search(r'"(.+)"', c)
                if w0 == "texte":                                  # citation sur la scène, le temps de sa réplique
                    sh_.ecran.append(_depuis(t - debut, _citation(m2.group(1) if m2 else c.split(None, 1)[1]),
                                             fin=fins_.get((t, c), fin_s) - debut))
            coupes.append((debut, fin_s, sh_))
        elif ecu is not None:
            # L'ÉCUME DE LA MER : {ecume "TES PÉCHÉS"} — plan rapproché sur le rivage, la vague emporte tout
            # {ecume "TES PÉCHÉS" sale} … {vague} … {propre "PETITS PÉCHÉS : EFFACÉS"} … {rocher "GRANDS PÉCHÉS"} …
            # {rocher "IL FAUT SE REPENTIR"} : chaque paquet d'écume sale = un petit péché, lavé un par un par les vagues
            m_ = re.search(r'"(.+)"', ecu[1])
            sale_ = "sale" in norm(ecu[1].split('"')[-1] if '"' in ecu[1] else ecu[1]).split()
            vague_ = next((t for (t, c) in ordres if c.lower().split()[0] == "vague"), None)
            tv_ = (vague_ - debut) if vague_ is not None else min(fin_s - debut - 1.0, max(1.6, ecu[0] - debut + 1.4))
            propre_ = next(((t - debut, re.search(r'"(.+)"', c).group(1).upper()) for (t, c) in ordres
                            if c.lower().split()[0] == "propre" and '"' in c), None)
            rocher_ = [(t - debut, re.search(r'"(.+)"', c).group(1).upper()) for (t, c) in ordres
                       if c.lower().split()[0] == "rocher" and '"' in c]
            sh_ = sc.plan_ecume(debut, fin_s, (m_.group(1) if m_ else "TES PÉCHÉS").upper(), t_vague=tv_, sale=sale_,
                                propre=propre_, rocher=rocher_, band=bool(theme.bandeau))
            for (t, c) in ordres:                                  # sources du même passage
                if c.lower().startswith("source"):
                    m2 = re.search(r'"(.+)"', c)
                    sh_.ecran.append(_depuis(t - debut, _tag_source(m2.group(1) if m2 else c.split(None, 1)[1], etapes, t)))
            coupes.append((debut, fin_s, sh_))
        elif selfie is not None and len(selfie[1]) >= 2 and selfie[1][1].upper() in roles:
            # SELFIE : {selfie ADA} — bras tendu, l'écran du téléphone montre le selfie
            coupes.append((debut, fin_s, sc.plan_selfie(debut, fin_s, roles[selfie[1][1].upper()],
                                                        [(t, c) for (t, c) in ordres] if demo else [],
                                                        demo=demo, paysage=theme.format == "paysage",
                                                        band=bool(theme.bandeau))))
        elif reflet is not None and len(reflet[1]) >= 2 and reflet[1][1].upper() in roles:
            # MIROIR : {reflet ADA} — le perso de dos, son reflet dans un grand miroir
            extras = [(t, c) for (t, c) in ordres if not c.lower().startswith("reflet")]
            coupes.append((debut, fin_s, sc.plan_reflet(debut, fin_s, roles[reflet[1][1].upper()],
                                                        extras + ([(reflet[0], " ".join(reflet[1]))] if demo else []),
                                                        demo=demo, D=D, paysage=theme.format == "paysage",
                                                        face=next((m_ for m_ in reflet[1][2:] if m_ in explique.cast_faces()),
                                                                  None),
                                                        band=bool(theme.bandeau))))
        elif photo is not None and len(photo[1]) >= 3 and photo[1][1].upper() in roles and photo[1][2].upper() in roles:
            # DÉMONSTRATION JOUÉE : {photographe ETUDIANT ADA 30 cm} … {recule 1,5 m} … {avance 30 cm}
            mots = photo[1]
            etapes = [(photo[0], explique._metres(" ".join(mots[3:]) or "30 cm"))]
            etapes += [(t, explique._metres(c.split(None, 1)[1] if len(c.split()) > 1 else "1,5 m"))
                       for (t, c) in ordres if c.lower().split()[0] in ("recule", "avance")]
            extras = [(t, c) for (t, c) in ordres if c.lower().split()[0] not in ("photographe", "recule", "avance")]
            coupes.append((debut, fin_s, sc.plan_photo(debut, fin_s, roles[mots[2].upper()], roles[mots[1].upper()],
                                                       etapes, extras + ([(photo[0], " ".join(mots))] if demo else [])
                                                       + [(t, c) for (t, c) in ordres if demo and
                                                          c.lower().split()[0] in ("recule", "avance")],
                                                       demo=demo, paysage=theme.format == "paysage",
                                                       band=bool(theme.bandeau))))
        else:
            sh_ = sc.plan_schema(debut, fin_s, ordres, fond=fond if fond in sets.DECORS else None,
                                 demo=demo, etapes=etapes, band=bool(theme.bandeau))
            if FILM.get("accroche_fin", 0.0) > debut + 0.3:              # texte d'accroche en haut : le grand schéma
                sh_.ecran[0].decale = (FILM["accroche_fin"] - debut, 110)   # descend un peu, puis remonte doucement
                if debut <= 0.05 and sh_.ecran[0].items and sh_.ecran[0].items[0]["t_in"] < 0.9:
                    sh_.ecran[0].items[0]["t_vis"] = 0.0                    # 1re image du Short : le sujet est déjà là
            coupes.append((debut, fin_s, sh_))
        en_schema |= {id(it) for it in seg}
    serres = [(it, u) for (it, u) in serres if id(it) not in en_schema]
    for (it, u) in serres:                                        # gros plans (après les retours au repos)
        st = {k: v for k, v in roles[it["qui"]].etat(u + 0.3).items() if k in ("face", "pose", "objet")}
        if "goutte" in it["act"]["effets"]:
            st["sweat"] = True
        if "larmes" in it["act"]["effets"]:
            st["larmes"] = True
        pz = it["act"]["pensee"]
        coupes.append((it["t0"], it["t1"], kit.gros_plan(
            it["t0"], it["t1"], it["qui"], bg, bulle=it["act"]["bulle"],
            pensee=(pz if pz in objets.ICONES else "ampoule") if pz else None, **st)))
    if len(roles) >= 2:
        sc.regard_parleur(D)
        sc.reactions(D, sobre=getattr(theme, "film", False))      # celui qui écoute réagit (hoche la tête, sourcils…)
    # CHAMP / CONTRE-CHAMP automatique : les répliques qui se répondent, filmées par-dessus l'épaule de celui qui écoute
    lignes = [it for it in b["items"] if it["type"] == "ligne"]
    fin_ = any(it["type"] == "fin" for it in b["items"])
    forcer = {it["k"] for it in lignes if it["act"]["plan"] == "epaule"}
    interdits = {it["k"] for it in lignes if it["act"]["gros_plan"] or it["act"]["plan"] in ("large", "proche", "schema")
                 or it.get("ordres") or it.get("annot")
                 or it["act"]["entre"] or it["act"]["sort"] or it["act"]["approche"] or it["act"]["apparait"]
                 or it["act"]["assis"] or it["act"]["donne"]}
    if fin_ and lignes:
        interdits.add(lignes[-1]["k"])                            # la chute : plan large qui se rapproche
    for i, it in enumerate(b["items"]):                           # après un SMS ou un carton : on revoit la scène en large
        if it["type"] in ("sms", "carton", "muet"):
            nxt = next((x for x in b["items"][i + 1:] if x["type"] == "ligne"), None)
            if nxt is not None:
                interdits.add(nxt["k"])
    if serre:
        interdits |= {it["k"] for it in lignes}
    if getattr(theme, "film", False):                             # film : plans de cinéma (caméra_film), pas d'épaule auto
        interdits |= {it["k"] for it in lignes if it["k"] not in forcer}
    champs = sc.champs(D, max_suite=2, forcer=forcer, interdits=interdits) if len(roles) >= 2 else []
    for (a, b_, f, d) in champs:
        coupes.append((a, b_, sc.plan_epaule(a, b_, f, d, band=bool(theme.bandeau))))
    if getattr(theme, "film", False) and not cam_fixee:
        camera_film(sc, b, roles, t0)
        cam_fixee = True
    if roles and not cam_fixee and not any(it["type"] == "ligne" and it["qui"] in roles for it in b["items"]):
        ysol = lieux.spot(bg)["gauche"][1]
        xs = [r.pos(2.0)[0] for r in roles.values() if 0 < r.pos(2.0)[0] < 1080] + [o["x0"] for o in getattr(sc, "accessoires", [])]
        cx = (sum(xs) / len(xs) + 60) if xs else 540
        sc.camera([(0.0, 1.08, (540, ysol - 320)), (t1 - t0, 1.24, (cx, ysol - 300))])
        cam_fixee = True
    if roles and not cam_fixee:
        camera_auto(sc, b, roles, t0, epaule={round(a, 3) for (a, _, _, _) in champs})
    return sc.decoupe(coupes, band=bool(theme.bandeau))


FORTS = ("choc", "cri", "peur", "pleure", "enerve", "triste")


def camera_auto(sc, b, roles, t0, epaule=()):
    """CHOIX AUTOMATIQUE DES PLANS (toujours par glissements doux, jamais de secousse) :
    - début du décor : plan d'ensemble qui se resserre doucement pendant le plan muet ;
    - à chaque réplique, la caméra glisse un peu vers celui qui parle ;
    - réplique forte (choc, cri, peur, colère, larmes, bulle « ! ») et la chute avant FIN : elle se rapproche de lui ;
    - « plan moyen » / « plan large » entre parenthèses pour choisir soi-même ; FIN : on recule pour voir tout le monde."""
    ysol = lieux.spot(sc.bg)["gauche"][1]
    LARGE = (1.06, 540, ysol - 280)
    items = b["items"]
    lignes = [it for it in items if it["type"] == "ligne" and it["qui"] in roles]
    if not lignes:
        return
    muet = next((it for it in items if it["type"] == "muet"), None)
    debut = (1.0, 540, ysol - 380) if muet is not None and muet["t0"] - t0 < 0.1 else LARGE
    keys = [(0.0, debut)]
    fin_it = next((it for it in items if it["type"] == "fin"), None)
    chute = lignes[-1] if fin_it is not None else None

    def pose_cle(t, cadre):
        t = max(t, keys[-1][0] + 0.02)
        keys.append((t, cadre))

    for it in lignes:
        u = it["t0"] - t0
        r = roles[it["qui"]]
        cible = next((roles[c.split()[1].upper()] for (_, c) in it.get("annot", [])
                      if len(c.split()) > 1 and c.split()[1].upper() in roles), None)
        if cible is not None and cible is not r and act_large(it):   # l'action se passe sur un autre perso :
            xs = cible.pos(u + 0.3)[0]                               # la caméra glisse vers lui (pas de plan figé)
            pose_cle(u - 0.05, keys[-1][1])
            pose_cle(u + 1.6, (1.18, xs, ysol - 360))
            continue
        xs = r.pos(u + 0.3)[0]
        act = it["act"]
        proche = act["plan"] == "proche" or (act["plan"] != "large" and round(it["t0"], 3) not in epaule and (
            act["face"] in FORTS or act["bulle"] in ("!", "?!") or it is chute))
        if proche:
            cadre = (1.3, xs, ysol - 390)
            pose_cle(u - 0.05, keys[-1][1])
            pose_cle(u + 0.85, cadre)
        else:
            cadre = (LARGE[0], 540 + max(-70, min(70, (xs - 540) * 0.3)), LARGE[2])
            pose_cle(u - 0.05, keys[-1][1])
            pose_cle(u + 1.2, cadre)
    if fin_it is not None:
        u = fin_it["t0"] - t0
        pose_cle(u, keys[-1][1])
        pose_cle(u + 1.1, (1.04, 540, ysol - 300))
    sc.camera([(t, z, (x, y)) for (t, (z, x, y)) in keys])


def _baton_suit(baton, porteur, roles, dx=90, dy=-4):
    """Le bâton de berger reste debout à côté de l'orbe de Moussa et le suit dans tous ses déplacements, sauf quand le
    scénario le déplace lui-même ({derive BATON …} : le rocher frappé, les deux frères qui avancent au palais).
    Côté : à droite de l'orbe, ou à gauche si quelqu'un se tient trop près à droite (positions du début du décor)."""
    propre = baton.pos

    def cote():
        x0 = porteur.pos(0.3)[0]
        autres = [r.pos(0.3)[0] for r in roles.values() if r is not porteur and r is not baton]
        droite = min([x - x0 for x in autres if x > x0] + [999])
        gauche = min([x0 - x for x in autres if x <= x0] + [999])
        return dx if droite >= 170 or droite >= gauche else -dx

    def pos(u):
        if baton.moves:
            return propre(u)
        xm, ym = porteur.pos(u)
        return xm + cote(), ym + dy
    baton.pos = pos


def camera_film(sc, b, roles, t0):
    """FILM : caméra de cinéma, toujours en glissements lents (jamais de secousse ni de coupe).
    - début du décor : plan large qui dérive doucement (on découvre le lieu) ;
    - narration (voix off) : le plan continue de respirer (lente avancée + lent panoramique, sens alterné) ;
    - « sur X » entre parenthèses (même pour NARRATEUR ou CORAN) : plan moyen sur X ; « gros plan » : plus serré ;
      « plan large » : on recule pour voir tout le lieu ;
    - un perso qui parle : plan moyen sur lui, un peu vers celui qui l'écoute (plus serré si la réplique est forte) ;
    - si le perso cadré marche, la caméra l'accompagne."""
    sp = lieux.spot(sc.bg)
    ysol, k = sp["gauche"][1], sp.get("k", 7)
    cy_l = sp.get("cy", ysol - 280)
    calme = FILM.get("calme", False)                              # CAMERA: calme (02/11/2026, « trop de zooms inutiles »)
    Z_L, Z_M, Z_G = (1.04, 1.3, 1.5) if calme else (1.08, 1.7, 2.25)
    dur = b["t1"] - b["t0"]

    def hauteur(r, u, serre):
        if r.who in film.OBJETS_FILM:                             # le coffre : on vise l'objet lui-même
            return 9 * k
        o = film.ORBES.get(r.who)
        if o is not None:
            return o["hauteur"] * k
        assis = r.etat(u).get("assis")
        return (44 if serre else 38) * k if assis else (56 if serre else 46) * k

    def vise(r, u, z):
        x, y = r.pos(u)
        cx = x
        autres = [o.pos(u)[0] for o in roles.values() if o is not r and o.who != "BATON" and abs(o.pos(u)[0] - x) < 560]
        if autres and z < Z_G:                                    # un peu vers celui qui écoute
            xo = min(autres, key=lambda v: abs(v - x))
            cx = x + (xo - x) * 0.28
        return (z, cx, y - hauteur(r, u, z >= Z_G))

    segs = [(0.0, ("large",))]
    cible = ("large",)
    evts = []
    for it in [i for i in b["items"] if i["type"] == "ligne"]:
        evts.append((it["t0"], 0, it))
        for (ta, ca) in it.get("annot", []):
            mo = ca.split()
            if mo and mo[0].lower() in ("cadre", "large", "gros"):
                evts.append((ta, 1, mo))
    for (te, kind, it) in sorted(evts, key=lambda e: (e[0], e[1])):
        if kind == 1:                                            # {cadre X} {gros X} {large}, pile sur le mot
            mo = it
            if mo[0].lower() == "large":
                nv = ("large",)
            elif len(mo) > 1 and mo[1].upper() in roles:
                nv = ("sur", roles[mo[1].upper()], Z_G if mo[0].lower() == "gros" else Z_M)
            else:
                continue
            if nv != cible:
                segs.append((max(0.0, te - t0 - 0.1), nv))
                cible = nv
            continue
        act, qui = it["act"], it["qui"]
        u = it["t0"] - t0
        fort = act["gros_plan"] or act["face"] in FORTS or act["bulle"] in ("!", "?!")
        if act["plan"] == "large":
            nv = ("large",)
        elif act.get("cadre") in roles:
            nv = ("sur", roles[act["cadre"]], Z_G if act["gros_plan"] else Z_M)
        elif qui in roles:
            if calme and it["t1"] - it["t0"] < 2.5:               # caméra calme : pas de mouvement pour une réplique courte
                nv = cible
            else:
                nv = ("sur", roles[qui], Z_M if calme else (Z_G if fort else Z_M))
        elif act["gros_plan"] and cible[0] == "sur":
            nv = ("sur", cible[1], Z_G)
        elif act["plan"] == "proche" and cible[0] == "sur":
            nv = ("sur", cible[1], Z_M)
        else:
            nv = cible
        if nv != cible:
            segs.append((max(0.0, u - 0.15), nv))
            cible = nv
    if calme and len(segs) > 1:                                  # caméra calme : jamais deux mouvements en moins de 7 s
        garde = [segs[0]]
        for (ua_, cib_) in segs[1:]:
            if cib_ != garde[-1][1] and ua_ - garde[-1][0] >= 7.0:
                garde.append((ua_, cib_))
        segs = garde
    keys = []

    def cle(t, z, x, y):
        t = max(t, keys[-1][0] + 0.05) if keys else t
        keys.append((t, z, (x, y)))

    sens = 1
    for i, (ua, cib) in enumerate(segs):
        ub = segs[i + 1][0] if i + 1 < len(segs) else dur
        tr = 0.0 if i == 0 else ((2.6 if cib[0] == "large" else 2.2) if calme else (1.6 if cib[0] == "large" else 1.2))
        if cib[0] == "large":
            amp = 28 if calme else 45
            x0, x1 = 540 - amp * sens, 540 + amp * sens
            if i == 0:
                cle(ua, Z_L, x0, cy_l)
            else:
                cle(ua, keys[-1][1], keys[-1][2][0], keys[-1][2][1])
                cle(ua + tr, Z_L, x0, cy_l)
            cle(max(ub, ua + tr + 0.1), Z_L + (min(0.03, 0.002 * (ub - ua)) if calme else min(0.06, 0.004 * (ub - ua))),
                x1, cy_l - (4 if calme else 8))
        else:
            r, z = cib[1], cib[2]
            if i > 0:
                cle(ua, keys[-1][1], keys[-1][2][0], keys[-1][2][1])
            z0, x0, y0 = vise(r, ua + tr, z)
            cle(ua + tr, z0, x0 + (8 if calme else 18) * sens, y0)
            arrets = sorted({tm for m in r.moves for tm in (m[0], m[1]) if ua + tr < tm < ub})   # il marche : on l'accompagne
            for ta in arrets:
                za, xa, ya = vise(r, ta, z)
                cle(ta, za, xa, ya)
            z1, x1, y1 = vise(r, ub, z)
            cle(max(ub, ua + tr + 0.1), z1 + (min(0.03, 0.002 * (ub - ua)) if calme else min(0.08, 0.005 * (ub - ua))),
                x1 - (8 if calme else 18) * sens, y1)
        sens = -sens
    sc.camera(keys)


def act_large(it):
    """Réplique où l'on peut laisser la caméra aller vers le perso concerné par une annotation (pas un plan imposé)."""
    return it["act"]["plan"] not in ("large", "proche") and not it["act"]["gros_plan"]


def _cta_depuis(u0, theme):
    return _depuis(u0, kit.cta(theme))


def accroche(lignes, a_gauche=False, duree=2.6):
    """Le texte d'accroche des premières secondes (visible dès la 1re image, puis il s'efface en douceur).
    a_gauche : on le met à gauche (quand l'encart d'un selfie ou d'une photo occupe la droite)."""
    cache = {}

    def f(img, t):
        if t >= duree:
            return
        W_, H_ = img.size
        if W_ not in cache:
            larg = W_ * (0.60 if a_gauche else 0.90)
            taille = 96
            while True:
                im = pxv.big_title([(l, (255, 255, 255) if i == 0 else (255, 214, 70)) for i, l in enumerate(lignes)],
                                   size=taille)
                if im.width <= larg or taille <= 40:
                    break
                taille -= 6
            cache[W_] = im
        im = cache[W_]
        a = 1 - scene.smooth((t - (duree - 0.45)) / 0.45)
        x = 30 if a_gauche else int(W_ / 2 - im.width / 2)
        y = int(H_ * (0.13 if H_ > W_ else 0.08))
        img.alpha_composite(explique._fade(im, a), (x, y))
    return f


def bandeaux_etapes(etapes, duree=2.4, coupe=()):
    """{etape "LE MIROIR"} : un bandeau-titre en haut au début de chaque étape (relance l'attention au milieu), sans numéro.
    coupe = instants où une citation arrive en haut de l'écran : le bandeau s'efface juste avant (jamais de chevauchement).
    f.bas(t, W, H) = (bas du bandeau visible, opacité) : la source d'une réplique se glisse dessous en douceur."""
    items = []
    for (t, c) in sorted(etapes):
        # JAMAIS de numérotation à l'écran (« 1/2 », « PARTIE 2/2 ») : l'utilisateur la refuse (01/11/2026, « ça n'a
        # aucun sens »). Seul le titre entre guillemets s'affiche : {etape "LE MIROIR"} ; sans titre, pas de bandeau.
        m = re.search(r'"(.+)"', c)
        txt = m.group(1).upper() if m else ""
        if not txt:
            continue
        fin = t + duree
        for tc in coupe:
            if t + 0.8 < tc < fin:
                fin = tc - 0.05
        items.append((t, "", txt, fin))
    cache = {}

    def image(num, txt, W_):
        if (num, txt) not in cache and not num:                     # titre seul, dans un cadre jaune
            b_ = pxv.pixel_text(txt, (255, 255, 255), (30, 24, 40), size=10, k=5, ol2=(12, 10, 16))
            im = Image.new("RGBA", (b_.width + 60, b_.height + 24), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], 18, fill=(18, 14, 28, 225), outline=(255, 214, 70, 255), width=5)
            im.alpha_composite(b_, (30, (im.height - b_.height) // 2))
            cache[(num, txt)] = im
        if (num, txt) not in cache:
            a_ = pxv.pixel_text(num, (22, 18, 30), (255, 214, 70), size=10, k=5)
            b_ = pxv.pixel_text(txt, (255, 255, 255), (30, 24, 40), size=10, k=5, ol2=(12, 10, 16)) if txt else None
            w_ = a_.width + 40 + (b_.width + 30 if b_ else 0)
            h_ = max(a_.height, b_.height if b_ else 0) + 24
            im = Image.new("RGBA", (w_, h_), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            d.rounded_rectangle([0, 0, w_ - 1, h_ - 1], 18, fill=(18, 14, 28, 225), outline=(255, 214, 70, 255), width=5)
            pastille = Image.new("RGBA", (a_.width + 20, h_ - 16), (255, 214, 70, 255))
            im.alpha_composite(pastille, (8, 8))
            im.alpha_composite(a_, (18, (h_ - a_.height) // 2))
            if b_:
                im.alpha_composite(b_, (a_.width + 50, (h_ - b_.height) // 2))
            cache[(num, txt)] = im
        im = cache[(num, txt)]
        if im.width > W_ - 60:                                     # trop long : réduit pour rester dans l'image
            im = im.resize((W_ - 60, int(im.height * (W_ - 60) / im.width)), Image.LANCZOS)
        return im

    def opacite(t0, fin, t):
        return scene.smooth((t - t0) / 0.3) * (1 - scene.smooth((t - (fin - 0.4)) / 0.4))

    def bas(t, W_, H_):
        best = (0, 0.0)
        for (t0, num, txt, fin) in items:
            if t0 <= t < fin:
                a = opacite(t0, fin, t)
                if a > best[1]:
                    best = (int(H_ * (0.115 if H_ > W_ else 0.06)) + image(num, txt, W_).height, a)
        return best

    def f(img, t):
        W_, H_ = img.size
        for (t0, num, txt, fin) in items:
            if not (t0 <= t < fin):
                continue
            im = image(num, txt, W_)
            u = t - t0
            a = opacite(t0, fin, t)
            y = int(H_ * (0.115 if H_ > W_ else 0.06)) - int((1 - scene.smooth(u / 0.3)) * 20)
            img.alpha_composite(explique._fade(im, a), (int(W_ / 2 - im.width / 2), y))
    f.bas = bas
    return f


def _citation(txt):
    """Une phrase forte sur la scène (citation, idée clé) : grosses lettres sur un bandeau sombre doux, en haut.
    « texte // sous-texte » : le sous-texte s'ajoute dessous, plus petit, en jaune (explication, sans voix)."""
    principal, _, sous = txt.partition("//")
    lignes = explique.coupe(principal.strip(), 26)
    lignes_sous = explique.coupe(sous.strip(), 32) if sous.strip() else []
    cache = {}

    def f(img, u):
        if img.size not in cache:
            t_ = pxv.big_title([(l_, (255, 255, 255)) for l_ in lignes], size=64 if len(lignes) < 3 else 56)
            if lignes_sous:
                s_ = pxv.big_title([(l_, (255, 214, 70)) for l_ in lignes_sous], size=42)
                t2 = Image.new("RGBA", (max(t_.width, s_.width), t_.height + s_.height - 6), (0, 0, 0, 0))
                t2.alpha_composite(t_, ((t2.width - t_.width) // 2, 0))
                t2.alpha_composite(s_, ((t2.width - s_.width) // 2, t_.height - 6))
                t_ = t2
            if t_.width > img.width - 60:
                t_ = t_.resize((img.width - 60, int(t_.height * (img.width - 60) / t_.width)), Image.LANCZOS)
            bande = Image.new("RGBA", (img.width, t_.height + 60), (0, 0, 0, 0))
            d = ImageDraw.Draw(bande)
            for i in range(bande.height):                         # bandeau sombre aux bords doux
                al = int(150 * min(1, min(i, bande.height - i) / 24))
                d.line([(0, i), (bande.width, i)], fill=(10, 8, 18, al))
            bande.alpha_composite(t_, ((bande.width - t_.width) // 2, 30))
            cache[img.size] = bande
        im = cache[img.size]
        a = scene.smooth(u / 0.35)
        y = int(img.height * (0.15 if img.height > img.width else 0.10)) + int((1 - a) * 18)
        img.alpha_composite(explique._fade(im, a), (0, y))
    return f


FILM = dict(actif=False, bande=0, calme=False, baton=False)   # thème « film » : référence en petit, en haut à droite, dans la bande noire


def _tag_source(txt, etapes=None, t_abs=0.0):
    """La source en petit, en haut à gauche (sous la barre de TikTok), comme dans les schémas.
    etapes (bandeaux d'étape) + t_abs (instant où la source commence) : si un bandeau est là, elle glisse dessous.
    Film : petite référence sans cadre, en haut à droite (dans la bande noire du haut)."""
    if FILM["actif"]:
        imf = pxv.pixel_text(txt.upper(), (236, 226, 204), (20, 16, 22), size=8, k=3)

        def ff(img, u):
            y = max(14, (FILM["bande"] - imf.height) // 2) if FILM["bande"] else 30
            img.alpha_composite(explique._fade(imf, scene.smooth(u / 0.35)), (img.width - 40 - imf.width, y))
        return ff
    im = pxv.tag_img("SRC " + txt.upper())
    # 08/11/2026 (ISL29) : la source est au même endroit que le texte d'ACCROCHE ; si elle commence pendant l'accroche,
    # elle attend sa fin (jamais de chevauchement), puis apparaît en fondu comme d'habitude.
    att = max(0.0, FILM.get("accroche_fin", 0.0) - t_abs) if t_abs > 0 else 0.0

    def f(img, u):
        y = int(img.height * (0.12 if img.width > img.height else 0.125))
        if etapes is not None:
            bas, al = etapes.bas(u + t_abs, img.width, img.height)
            if al > 0:
                y = int(y + scene.smooth(al) * max(0, bas + 12 - y))
        img.alpha_composite(explique._fade(im, scene.smooth((u - att) / 0.35)), (40, y))
    return f


def _code_demo(c):
    """En mode DEMO : le code d'une annotation, en haut de l'écran."""
    im = explique.petit_texte("{" + c + "}", explique.JAUNE, (60, 40, 10), size=9, k=5)

    def f(img, u):
        img.alpha_composite(explique._fade(im, scene.smooth(u / 0.2)), (int(img.width / 2 - im.width / 2), int(img.height * 0.03)))
    return f


NOMS_LETTRES = {"alif", "hamza", "ba", "ta", "tha", "jim", "ha", "kha", "dal", "dhal", "ra", "zay", "zayn", "sin", "shin",
                "chin", "sad", "dad", "za", "ayn", "ain", "ghayn", "fa", "qaf", "kaf", "lam", "mim", "nun", "noun", "waw",
                "ya"}


def _lettres_calees(D, k, t, c):
    """{lettres ا ل م} : chaque lettre apparaît pile quand on entend son nom (« Alif… Lam… Mim… ») après la balise.
    On ajoute « @0,1.56,2.90 » (instants depuis la balise) ; si on ne trouve pas tous les noms, rythme fixe."""
    mots = c.split()
    if any(m_.startswith("@") for m_ in mots):
        return c
    n = len([m_ for m_ in mots[1:] if m_.strip()])
    ts = [w["s"] for w in D.lines[k]["words"]
          if w["s"] >= t - 0.05 and re.sub(r"[^a-z]", "", norm(w["t"])) in NOMS_LETTRES]
    if n < 1 or len(ts) < n:
        return c
    return c + " @" + ",".join(f"{max(0.0, x - t):.2f}" for x in ts[:n])


def _fin_anim(t, c):
    """Fin d'un chrono / compteur / lettres / chiffre + le temps de lire le résultat."""
    mots = c.split()
    if mots[0].lower() == "chiffre":                              # il monte en 0,9 s, puis 1 s pour le lire
        return t + 1.9
    if mots[0].lower() == "feuilles":                             # les feuilles tombent une à une (≈ 3,5 s)
        return t + 4.0
    if mots[0].lower() == "orteil":
        return t + 1.6
    if mots[0].lower() in explique.CLES_0411:                    # éléments du 04/11 (explique_0411.fin_anim)
        import explique_0411
        return explique_0411.fin_anim(t, mots)
    if mots[0].lower() in explique.CLES_0411B:                   # éléments du 04/11 soir (explique_0411b.fin_anim)
        import explique_0411b
        return explique_0411b.fin_anim(t, mots)
    if mots[0].lower() in explique.CLES_0611:                    # éléments du 07/11 (explique_0611.fin_anim)
        import explique_0611
        return explique_0611.fin_anim(t, mots)
    if mots[0].lower() in explique.CLES_0811:                    # éléments du 08/11 (explique_0811.fin_anim)
        import explique_0811
        return explique_0811.fin_anim(t, mots)
    if mots[0].lower() in explique.CLES_BRIQUES:                 # briques réutilisables du 09/11 (briques.fin_anim)
        import briques
        return briques.fin_anim(t, mots)
    if mots[0].lower() == "radio" and len(mots) > 1 and mots[1].lower() == "tout":   # balayage 0,9 s + coche + note
        return t + 2.0
    if mots[0].lower() == "lettres" and mots[-1].startswith("@"):
        try:
            return t + float(mots[-1][1:].split(",")[-1]) + 1.9
        except ValueError:
            pass
    return t + 2.4


def _depuis(u0, f, fin=None, fondu=0.4):
    """Un dessin d'écran qui commence à l'instant u0 du plan (et s'efface en fondu à l'instant fin)."""
    from PIL import Image

    def g(img, u):
        if u < u0 or (fin is not None and u >= fin + fondu):
            return
        if fin is not None and u > fin:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            f(lay, u - u0)
            a = 1 - (u - fin) / fondu
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
            img.alpha_composite(lay)
            return
        f(img, u - u0)
    return g


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("python scenario.py mon_sketch.txt sheet | voix | asr | tout | still 4.5 image.png")
    path = os.path.abspath(sys.argv[1])
    real = os.path.abspath(__file__)
    sys.argv = [real] + sys.argv[2:]
    VID, nom, dossier, code, voix, repliques = fabrique(path)
    if sys.argv[1:] and sys.argv[1] == "tout":                    # les sous-processus relancent ce script avec le fichier
        import subprocess
        pxv.priorite_basse()
        n = int(sys.argv[2]) if len(sys.argv) > 2 else max(2, min(8, (os.cpu_count() or 4) - 4))
        work = os.path.join(os.environ.get("TEMP", "."), "ia501", nom.replace(" ", "_") + "_frames")
        kit.vide_images(work)                                     # jamais d'images d'un ancien rendu
        a_preparer = {getattr(sh_, "bg", None) for sh_ in VID.shots}
        a_preparer |= {sh_.fond2[0] for sh_ in VID.shots if getattr(sh_, "fond2", None)}
        for bg_ in sorted(a_preparer & egypte.DECORS_FILM):
            lieux.decor_large(bg_) if VID.fmt == "paysage" else sets.DECORS[bg_]()   # décors du film : cache préparé
        procs = [subprocess.Popen([sys.executable, real, path, "frames", str(i), str(n)]) for i in range(n)]
        if any(p.wait() for p in procs):
            raise SystemExit("une partie du rendu a échoué")
        VID.encode(os.path.join(dossier, nom + ".mp4"), work)
        print("vidéo :", os.path.join(dossier, nom + ".mp4"))
    elif sys.argv[1:] and sys.argv[1] == "brouillon":             # APERÇU RAPIDE : 10 images/s, demi-taille, avec le son
        import subprocess                                         #   python scenario.py x.txt brouillon [processus]
        pxv.priorite_basse()
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        work = os.path.join(os.environ.get("TEMP", "."), "ia501", nom.replace(" ", "_") + "_brouillon")
        kit.vide_images(work, "b*.jpg")
        procs = [subprocess.Popen([sys.executable, real, path, "brouillon_images", str(i), str(n)]) for i in range(n)]
        if any(p.wait() for p in procs):
            raise SystemExit("une partie du brouillon a échoué")
        VID.encode_brouillon(os.path.join(dossier, nom + " (brouillon).mp4"), work)
        kit.vide_images(work, "b*.jpg")
        print("brouillon :", os.path.join(dossier, nom + " (brouillon).mp4"))
    else:
        kit.rendu(VID, nom, dossier, code=code, voix=voix, repliques=repliques)
