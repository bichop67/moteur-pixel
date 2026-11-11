# Planches catalogue : tout ce que le moteur sait dessiner (personnages, poses, expressions, coiffures, décors, icônes).
# python catalogue.py troupe|poses|visages|options|decors|objets|tout  [dossier de sortie]
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cast, duo

OUTD = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "CATALOGUE")
FONT = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 22)
FONT_S = ImageFont.truetype("C:/Windows/Fonts/tahoma.ttf", 17)
BG = (96, 88, 84)


def grid(items, cols, cell, title=None, bg=BG, label_h=56):
    """items = [(image, nom, sous-titre)] ; une case par élément, nom en dessous."""
    cw, ch = cell
    rows = (len(items) + cols - 1) // cols
    top = 70 if title else 0
    sheet = Image.new("RGB", (cols * cw, top + rows * (ch + label_h)), bg)
    d = ImageDraw.Draw(sheet)
    if title:
        d.text((20, 18), title, fill=(255, 236, 170), font=FONT)
    for i, (im, name, sub) in enumerate(items):
        x, y = (i % cols) * cw, top + (i // cols) * (ch + label_h)
        if im is not None:
            sheet.paste(im, (x + (cw - im.width) // 2, y + ch - im.height), im if im.mode == "RGBA" else None)
        d.text((x + cw // 2, y + ch + 6), name, fill=(255, 255, 255), font=FONT, anchor="ma")
        if sub:
            d.text((x + cw // 2, y + ch + 32), sub[:34], fill=(220, 214, 200), font=FONT_S, anchor="ma")
    return sheet


def spr(who, k=5, **kw):
    im = duo.sprite(who, **kw)
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def troupe():
    items = [(spr(n), n, cast.CAST[n]["description"]) for n in cast.CAST]
    return grid(items, 8, (300, 500), "LA TROUPE  (nom à utiliser dans les plans)")


def poses(who="ADO"):
    items = [(spr(who, pose=p), p, "") for p in cast.POSES]
    items += [(spr(who, assis=True), "assis=True", ""), (spr(who, back=True), "back=True", ""),
              (spr(who, step=1), "step=1 (marche)", ""), (spr(who, step=3), "step=3", "")]
    return grid(items, 8, (300, 500), f"POSES  (pose=…)  — exemple : {who}")


def visages(whos=("ADO", "MAMAN", "PAPA", "TATA")):
    faces = ["neutre", "content", "rire", "choc", "gene", "malin", "blase", "enerve", "cri", "triste", "pleure", "peur",
             "suspect", "degoute", "clin", "coeur", "etoile", "dodo", "fier", "bas"]
    items = []
    for f in faces:
        for w in whos:
            r = cast.CAST[w]
            g = cast.geo(r)
            im = duo.sprite(w, face=f)
            crop = im.crop((6, g.y0 - 6, 40, g.y0 + 24))
            items.append((crop.resize((crop.width * 6, crop.height * 6), Image.NEAREST), f if w == whos[0] else "", w))
    return grid(items, len(whos) * 2, (230, 190), "EXPRESSIONS  (face=…)", label_h=52)


def options():
    base = dict(taille="adulte", peau="doree", haut="tshirt", couleur="gris_clair", bas="jean")
    items = []
    for st in ("court", "degrade", "rase", "meche", "herisse", "boucle", "afro", "long", "carre", "frange", "queue",
               "chignon", "tresses", "vieux", "chauve"):
        cast.nouveau("_T", **dict(base, cheveux=st, couleur_cheveux="brun", genre="f" if st in ("long", "carre", "frange", "chignon") else "h"))
        duo._CACHE.clear()
        items.append((spr("_T"), st, "cheveux"))
    for b in ("courte", "longue", "bouc", "moustache", "3j"):
        cast.nouveau("_T", **dict(base, barbe=b))
        duo._CACHE.clear(); items.append((spr("_T"), b, "barbe"))
    for h in ("casquette", "casquette_arriere", "bonnet", "chapeau", "haut_de_forme", "couronne", "kufi", "turban", "keffieh",
              "hijab", "capuche", "casque_chantier", "toque", "casquette_police", "bandeau", "casque_audio", "laurier", "beret", "bob"):
        cast.nouveau("_T", **dict(base, chapeau=h, couleur_chapeau="bordeaux", genre="f" if h == "hijab" else "h"))
        duo._CACHE.clear(); items.append((spr("_T"), h, "chapeau"))
    for l in ("lunettes", "soleil"):
        cast.nouveau("_T", **dict(base, lunettes=l))
        duo._CACHE.clear(); items.append((spr("_T"), l, "lunettes"))
    del cast.CAST["_T"]
    duo._CACHE.clear()
    return grid(items, 9, (260, 500), "COIFFURES, BARBES, CHAPEAUX, LUNETTES", label_h=60)


def habits():
    items = []
    for h in ("tshirt", "polo", "pull", "sweat", "chemise", "chemise_ouverte", "costume", "blazer", "blouse", "police", "cuir",
              "doudoune", "survet", "maillot", "tablier", "combinaison", "qamis", "djellaba", "abaya", "robe", "robe_longue",
              "toge", "tunique", "armure", "redingote"):
        genre = "f" if h in ("abaya", "robe", "robe_longue") else "h"
        cast.nouveau("_T", taille="adulte", genre=genre, haut=h, couleur="bleu" if h not in ("blouse", "qamis", "toge") else "blanc",
                     couleur2="jaune", bas="jupe" if h == "robe" else "pantalon", couleur_bas="anthracite",
                     cheveux="carre" if genre == "f" else "court")
        duo._CACHE.clear(); items.append((spr("_T"), h, "haut"))
    for b in ("jean", "pantalon", "jogging", "cargo", "short", "jupe"):
        cast.nouveau("_T", taille="adulte", haut="tshirt", couleur="gris_clair", bas=b, couleur_bas="marine" if b != "jean" else "jean",
                     genre="f" if b == "jupe" else "h", cheveux="carre" if b == "jupe" else "court")
        duo._CACHE.clear(); items.append((spr("_T"), b, "bas"))
    for c in ("baskets", "ville", "bottes", "sandales", "talons"):
        cast.nouveau("_T", taille="adulte", haut="tshirt", couleur="gris_clair", bas="short", couleur_bas="marine", chaussures=c,
                     couleur_chaussures="marron" if c != "baskets" else "rouge")
        duo._CACHE.clear(); items.append((spr("_T"), c, "chaussures"))
    for a in ("gilet", "cravate", "noeud", "chaine", "stethoscope", "badge", "medaille", "echarpe", "sac", "cape", "ceinture"):
        cast.nouveau("_T", taille="adulte", haut="chemise", couleur="blanc", bas="pantalon", couleur_bas="anthracite", acc=[a])
        duo._CACHE.clear(); items.append((spr("_T"), a, "acc"))
    for o in ("telephone", "tasse", "verre_the", "micro", "livre", "parchemin", "ballon", "manette", "billets", "stylo",
              "epee", "canne", "torche", "loupe", "fiole", "sac_courses"):
        cast.nouveau("_T", taille="adulte", haut="tshirt", couleur="gris_clair", bas="jean")
        duo._CACHE.clear()
        pose = {"telephone": "telephone", "micro": "micro", "canne": "neutre", "sac_courses": "neutre"}.get(o, "tient")
        items.append((spr("_T", pose=pose, objet=o), o, "objet"))
    del cast.CAST["_T"]
    duo._CACHE.clear()
    return grid(items, 9, (260, 500), "VÊTEMENTS, ACCESSOIRES, OBJETS EN MAIN", label_h=60)


def icones():
    import objets
    items = [(objets.icone(n).img(8), n, "") for n in objets.ICONES]
    return grid(items, 10, (200, 150), "ICÔNES  (objets.icone(\"nom\") / tableau / bulle de pensée)", label_h=44)


def animaux():
    import animaux as an
    items = []
    for n in an.ANIMAUX:
        vus = set()
        for pose, step in (("debout", None), ("debout", 1), ("assis", None), ("couche", None), ("mange", None)) +                 ((("vole", None),) if n == "PIGEON" else ()):
            im = an.image(n, pose=pose, step=step)
            cle = im.tobytes()
            if cle in vus:                      # pose que cet animal n'a pas : on ne l'affiche pas
                continue
            vus.add(cle)
            k = 6 if im.height < 40 else 4
            items.append((im.resize((im.width * k, im.height * k), Image.NEAREST), n if pose == "debout" and step is None else "",
                          pose + (" (marche)" if step is not None else "")))
    return grid(items, 6, (300, 260), "ANIMAUX  (sc.role(\"CHIEN\", x=…) ; pose=debout, assis, couche, mange ; marche)", label_h=60)


def apercu(name, a="ADO", b="MAMAN", k=7, persos=True):
    """Décor en 1080x1920 avec deux personnages aux places conseillées (comme dans un plan large)."""
    import sets, lieux
    bg, fg = sets.DECORS[name]()
    img = bg.img(4).convert("RGBA")
    sp = lieux.SPOTS.get(name, dict(gauche=(300, 1340), droite=(780, 1340), k=7, opts={}))
    if persos:
        for who, (x, y), mir in ((a, sp["gauche"], False), (b, sp["droite"], True)):
            im = duo.sprite(who, **sp.get("opts", {}))
            foot = im.info.get("foot", duo.FOOT)
            kk = sp.get("k", k)
            im = im.resize((im.width * kk, im.height * kk), Image.NEAREST)
            if mir:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            img.alpha_composite(im, (int(x - im.width / 2), int(y - foot * kk)))
    if fg is not None:
        img.alpha_composite(fg.img(4, rgba=True))
    return img.convert("RGB")


def decors(names=None, cols=5, scale=0.5, persos=True):
    import sets, lieux
    names = names or list(sets.DECORS)
    duos = [("ADO", "MAMAN"), ("PAPA", "ADA"), ("ETUDIANT", "MEDECIN"), ("GAMER", "TATA"), ("PROF", "ENFANT"),
            ("PATRON", "LIVREUR"), ("JOURNALISTE", "EXPERT")]
    items = []
    for i, n in enumerate(names):
        a, b = duos[i % len(duos)]
        if n in ("carte",):
            continue
        im = apercu(n, a, b, persos=persos).resize((int(1080 * scale), int(1920 * scale)), Image.NEAREST)
        items.append((im, n, ""))
    return grid(items, cols, (int(1080 * scale) + 8, int(1920 * scale)), "DÉCORS  (Shot(…, \"nom\", …))", label_h=40)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "tout"
    os.makedirs(OUTD, exist_ok=True)
    jobs = dict(troupe=troupe, poses=poses, visages=visages, options=options, habits=habits, icones=icones,
                animaux=animaux)
    if what == "decors":
        names = sys.argv[3:] if len(sys.argv) > 3 else None
        im = decors(names)
        p = os.path.join(OUTD, "decors.png" if not names else "decors_" + "_".join(names)[:60] + ".png")
        im.save(p); print(p, im.size)
    if what in ("decors_pages", "tout"):
        import sets, lieux
        allnames = [n for n in sets.DECORS if not n.startswith("carte")]
        for k in range(0, len(allnames), 15):
            im = decors(allnames[k:k + 15], scale=0.4)
            p = os.path.join(OUTD, f"decors_{k // 15 + 1}.png")
            im.save(p); print(p, im.size)
    for name, fn in jobs.items():
        if what in (name, "tout"):
            im = fn()
            p = os.path.join(OUTD, f"{name}.png")
            im.save(p)
            print(p, im.size)
