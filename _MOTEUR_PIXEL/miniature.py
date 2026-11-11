# MINIATURES AUTOMATIQUES : miniature YouTube 1280x720 + couverture de Short 1080x1920, dans le style des vidéos.
#   python miniature.py scenarios\le_passeport_de_papi.txt        tout est déduit du scénario (décor, persos, émotions)
#   (en-têtes facultatifs du scénario : MINIATURE: IL A MIS SON PASSEPORT / OÙ ?!     ICONE: question)
# Ou depuis Python :
#   import miniature
#   miniature.youtube("aeroport", [("PAPI", dict(face="peur", sweat=True)), ("ADA", dict(face="choc"))],
#                     ["IL A MIS SON PASSEPORT", "OÙ ?!"], icone_nom="question", sortie="mini.jpg")
#   miniature.short(…mêmes réglages…, sortie="couverture.jpg")
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont
import pxv, duo, sets, lieux, objets, cast

JAUNE, BLANC = (255, 214, 60), (255, 255, 255)


# ---------------------------------------------------------------- briques
def _fond(bg, large, y0=None, flou=2.5, sombre=0.78):
    """Le décor agrandi x4, un peu flou et assombri (les persos et le titre ressortent)."""
    if large:
        px, fg = lieux.decor_large(bg)
        y0 = 110 if y0 is None else y0
        im = px.img(1).convert("RGB")
        if fg is not None:
            im = im.convert("RGBA"); im.alpha_composite(fg.img(1, rgba=True)); im = im.convert("RGB")
        im = im.crop((0, y0, 480, y0 + 270)).resize((1920, 1080), Image.NEAREST)
    else:
        px, fg = sets.DECORS[bg]()
        im = px.img(1).convert("RGB")
        if fg is not None:
            im = im.convert("RGBA"); im.alpha_composite(fg.img(1, rgba=True)); im = im.convert("RGB")
        im = im.resize((1080, 1920), Image.NEAREST)
    im = im.filter(ImageFilter.GaussianBlur(flou))
    im = ImageEnhance.Color(im).enhance(1.2)
    return ImageEnhance.Brightness(im).enhance(sombre).convert("RGBA")


def _halo(img, x, y, rx, ry, col, force=0.55):
    """Lumière colorée derrière les persos."""
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = ((xx - x) / rx) ** 2 + ((yy - y) / ry) ** 2
    a = np.clip(1 - d, 0, 1) ** 1.6 * force
    lay = np.zeros((h, w, 4), np.uint8)
    lay[..., :3] = col
    lay[..., 3] = (a * 255).astype(np.uint8)
    img.alpha_composite(Image.fromarray(lay, "RGBA"))


def _vignette(img, k=0.55):
    w, h = img.size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a = np.clip((d - 0.55) / 0.9, 0, 1) * k
    lay = np.zeros((h, w, 4), np.uint8)
    lay[..., 3] = (a * 255).astype(np.uint8)
    img.alpha_composite(Image.fromarray(lay, "RGBA"))


def _contour(im, epais, col=(255, 255, 255)):
    """Contour épais autour d'un sprite (le perso se détache du fond, comme sur les vraies miniatures)."""
    a = np.array(im)[..., 3] > 0
    e = a.copy()
    r = epais
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                e |= np.roll(np.roll(a, dy, 0), dx, 1)
    out = np.zeros(np.array(im).shape, np.uint8)
    out[e] = (*col, 255)
    o = Image.fromarray(out, "RGBA")
    o.alpha_composite(im)
    return o


def perso(who, k, miroir=False, **st):
    """Le perso en grand (pixels nets), avec contour blanc et ombre douce. Renvoie (image, haut_de_tête_en_px)."""
    st = dict(st)
    spr = duo.sprite(who, **st)
    a = np.array(spr)
    ys, xs = np.where(a[..., 3] > 0)
    top = int(ys.min()) if len(ys) else 0
    pad = 3
    big = Image.new("RGBA", (spr.width + 2 * pad, spr.height + 2 * pad), (0, 0, 0, 0))
    big.alpha_composite(spr, (pad, pad))
    if miroir:
        big = big.transpose(Image.FLIP_LEFT_RIGHT)
    big = big.resize((big.width * k, big.height * k), Image.NEAREST)
    out = _contour(big, max(4, k // 2))
    ombre = Image.new("RGBA", out.size, (0, 0, 0, 0))
    m = (np.array(out)[..., 3] > 0).astype(np.uint8) * 150
    ombre.putalpha(Image.fromarray(m))
    ombre = ombre.filter(ImageFilter.GaussianBlur(k * 1.2))
    fin = Image.new("RGBA", (out.width + 4 * k, out.height + 4 * k), (0, 0, 0, 0))
    fin.alpha_composite(ombre, (3 * k, 3 * k))
    fin.alpha_composite(out, (0, 0))
    return fin, (top + pad) * k


def titre(lignes, largeur_max, taille=150, couleurs=(BLANC, JAUNE)):
    """Titre en lettres pleines (même police que les accroches des vidéos), réduit jusqu'à tenir dans largeur_max."""
    t = taille
    while True:
        im = pxv.big_title([(l, couleurs[min(i, len(couleurs) - 1)]) for i, l in enumerate(lignes)], size=t)
        if im.width <= largeur_max or t <= 40:
            return im
        t -= 6


def icone_img(nom, k=12):
    ic = objets.icone(nom).img(k)
    return _contour(ic, max(3, k // 3))


def fleche(img, x0, y0, x1, y1, col=(235, 40, 40), ep=34):
    """Grosse flèche rouge (style miniature) de (x0, y0) vers (x1, y1)."""
    d = ImageDraw.Draw(img)
    ang = math.atan2(y1 - y0, x1 - x0)
    L = math.hypot(x1 - x0, y1 - y0)
    tete = min(110, L * 0.45)
    xb, yb = x1 - tete * math.cos(ang), y1 - tete * math.sin(ang)
    nx, ny = -math.sin(ang), math.cos(ang)
    for c, e in (((20, 10, 14), ep + 14), (col, ep)):
        d.line([(x0, y0), (xb, yb)], fill=(*c, 255), width=int(e))
        w2 = e * 1.6
        d.polygon([(x1 + (e - ep) * math.cos(ang) * 0.6, y1 + (e - ep) * math.sin(ang) * 0.6),
                   (xb + nx * w2, yb + ny * w2), (xb - nx * w2, yb - ny * w2)], fill=(*c, 255))


def cercle(img, x, y, r, col=(235, 40, 40), ep=16):
    d = ImageDraw.Draw(img)
    for c, e in (((20, 10, 14), ep + 10), (col, ep)):
        d.ellipse([x - r, y - r, x + r, y + r], outline=(*c, 255), width=int(e))


def _tampon(txt, col=(235, 40, 40)):
    a = pxv.pixel_text(txt, BLANC, (90, 10, 20), size=11, k=6, ol2=(30, 6, 10))
    box = Image.new("RGBA", (a.width + 40, a.height + 24), (*col, 235))
    ImageDraw.Draw(box).rectangle([0, 0, box.width - 1, box.height - 1], outline=(30, 6, 10, 255), width=6)
    box.alpha_composite(a, (20, 12))
    return box.rotate(6, resample=Image.NEAREST, expand=True)


# ---------------------------------------------------------------- les deux formats
def youtube(bg, persos, lignes, icone_nom=None, sortie="miniature.jpg", halo=(255, 190, 80), tampon=None,
            fleche_vers=None, y0=None):
    """Miniature YouTube 16:9 (fabriquée en 1920x1080, enregistrée en 1280x720) : titre à gauche, persos à droite."""
    img = _fond(bg, True, y0)
    n = len(persos)
    k = 18 if n == 1 else 15                      # gros plan : visages en grand, corps coupé par le bas
    xs = [1440] if n == 1 else [1250, 1690]
    _halo(img, sum(xs) / len(xs), 520, 560 if n > 1 else 420, 560, halo)
    tetes = []
    for i, (who, st) in enumerate(persos):
        st = dict(st)
        mir = st.pop("miroir", i == 1 and n > 1)
        im, top = perso(who, k, miroir=mir, **st)
        x = xs[i] - im.width // 2 + 2 * k
        y = 80 - top
        img.alpha_composite(im, (x, y))
        tetes.append((xs[i], 80 + 12 * k))
    _vignette(img)
    t = titre(lignes, 860)
    tx, ty = 70, max(60, 540 - t.height // 2 - (60 if icone_nom else 0))
    img.alpha_composite(t, (tx, ty))
    if icone_nom:
        ic = icone_img(icone_nom, k=13)
        ix, iy = tx + t.width // 2 - ic.width // 2, min(1080 - ic.height - 40, ty + t.height + 10)
        _halo(img, ix + ic.width / 2, iy + ic.height / 2, 190, 190, (255, 240, 200), 0.5)
        img.alpha_composite(ic, (ix, iy))
    if tampon:
        tp = _tampon(tampon)
        img.alpha_composite(tp, (1920 - tp.width - 40, 1080 - tp.height - 40))
    if fleche_vers is not None and tetes:
        hx, hy = tetes[min(fleche_vers, len(tetes) - 1)]
        fleche(img, tx + t.width - 40, ty + t.height - 20, hx - 150, hy + 40)
    out = img.convert("RGB").resize((1280, 720), Image.LANCZOS)
    out.save(sortie, quality=93)
    return out


def short(bg, persos, lignes, icone_nom=None, sortie="couverture.jpg", halo=(255, 190, 80), tampon=None):
    """Couverture de Short 1080x1920 : titre en haut, persos en bas (zone sûre : rien d'important tout en bas)."""
    img = _fond(bg, False)
    n = len(persos)
    k = 16 if n == 1 else 13
    xs = [540] if n == 1 else [290, 800]
    _halo(img, 540, 1250, 640, 660, halo)
    for i, (who, st) in enumerate(persos):
        st = dict(st)
        mir = st.pop("miroir", i == 1 and n > 1)
        im, top = perso(who, k, miroir=mir, **st)
        x = xs[i] - im.width // 2 + 2 * k
        y = 720 - top
        img.alpha_composite(im, (x, y))
    _vignette(img, 0.5)
    t = titre(lignes, 990, taille=130)
    img.alpha_composite(t, (540 - t.width // 2, 190))
    if icone_nom:
        ic = icone_img(icone_nom, k=12)
        ix, iy = 540 - ic.width // 2, 190 + t.height + 10
        if iy + ic.height < 730:
            _halo(img, 540, iy + ic.height / 2, 170, 170, (255, 240, 200), 0.5)
            img.alpha_composite(ic, (ix, iy))
    if tampon:
        tp = _tampon(tampon)
        img.alpha_composite(tp, (1080 - tp.width - 40, 130))
    out = img.convert("RGB")
    out.save(sortie, quality=93)
    return out


# ---------------------------------------------------------------- tout seul depuis un scénario
ORDRE = ("choc", "peur", "cri", "enerve", "pleure", "triste", "suspect", "degoute", "gene", "malin", "rire", "fier",
         "content", "neutre")


def depuis_scenario(path, dossier=None):
    import scenario
    head, blocs = scenario.lire(path)
    titre_ = head.get("MINIATURE") or head.get("TITRE", os.path.splitext(os.path.basename(path))[0])
    if "/" in titre_:
        lignes = [x.strip().upper() for x in titre_.split("/") if x.strip()]
    else:
        mots = titre_.upper().split()
        coupe = max(1, min(len(mots) - 1, round(len(mots) / 2))) if len(mots) > 1 else 1
        lignes = [" ".join(mots[:coupe]), " ".join(mots[coupe:])] if len(mots) > 2 else [titre_.upper()]
    bg = blocs[0]["decor"]
    persos = [p.strip().upper() for p in head.get("PERSONNAGES", "").split(",") if p.strip()]
    qui = []
    for b in blocs:
        for it in b["items"]:
            if it["type"] in ("ligne", "action") and it["qui"] not in qui:
                qui.append(it["qui"])
    persos = ([p for p in persos if p in qui] + [p for p in qui if p not in persos])[:2]
    choix = []
    for w in persos:
        best, st = len(ORDRE), dict(face="choc")
        for b in blocs:
            for it in b["items"]:
                if it["type"] == "ligne" and it["qui"] == w:
                    a = it["act"]
                    f = a["face"] or "neutre"
                    r = ORDRE.index(f) if f in ORDRE else len(ORDRE) - 1
                    if r < best:
                        best = r
                        st = dict(face=f)
                        if a["pose"] and a["pose"] not in ("tient", "telephone"):
                            st["pose"] = a["pose"]
                        if "goutte" in a["effets"]:
                            st["sweat"] = True
                        if "larmes" in a["effets"]:
                            st["larmes"] = True
        choix.append((w, st))
    ic = head.get("ICONE")
    if not ic:
        ic = next((it["act"]["pensee"] for b in blocs for it in b["items"]
                   if it["type"] in ("ligne", "action") and it["act"]["pensee"] in objets.ICONES), None)
    if not ic and lignes[-1].rstrip().endswith("?"):
        ic = "question"
    dossier = dossier or os.path.dirname(os.path.abspath(path))
    nom = os.path.splitext(os.path.basename(path))[0]
    nom = head.get("TITRE", nom)
    a = os.path.join(dossier, nom + " - miniature.jpg")
    b = os.path.join(dossier, nom + " - couverture short.jpg")
    youtube(bg if bg in sets.DECORS else "rue", choix, lignes, icone_nom=ic, sortie=a)
    short(bg if bg in sets.DECORS else "rue", choix, lignes, icone_nom=ic, sortie=b)
    return a, b


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("python miniature.py mon_scenario.txt")
    for p in depuis_scenario(sys.argv[1]):
        print("miniature :", p)
