# DÉMONSTRATIONS EN IMAGE DU 04/11/2026 — pour 3 Shorts duo (la fièvre, l'eau glacée des ablutions, le cauchemar).
# Même principe que les éléments du 03/11 (explique.py : radiographie, orteil, arbre, balance) : le sens propre du
# hadith, montré en grand, avec des mouvements doux (jamais de secousse ni de flash).
#   {fievre PETIT}               gros plan : Petit malade sous sa couverture, le thermomètre monte à 39,5 °C, sueur,
#                                frissons (accroche ; Mouslim 2575 : « pourquoi trembles-tu ? » — « la fièvre »)
#   {forge "TES PETITS PÉCHÉS"}  une forge : le fer, couvert de croûtes noires « PÉCHÉ », est dans les braises ;
#   {soufflet}                   le soufflet du forgeron souffle trois fois : le feu monte, les croûtes partent une à
#                                une, le fer ressort propre et brille (Mouslim 2575 : « comme le soufflet du forgeron
#                                enlève la saleté du fer »)
#   {glace}                      gros plan : l'eau glacée du robinet tombe sur les mains (givre, « BRRR ! ») (accroche)
#   {ablutions PETIT}            les ablutions : {ablutions yeux} le visage, {ablutions mains} les mains,
#                                {ablutions pieds} les pieds ; chaque fois, le voile sombre se défait en gouttes
#                                « PÉCHÉ » qui partent avec l'eau dans la grille (Mouslim 244)
#   {cauchemar PETIT}            la nuit : Petit dort, bulle de cauchemar (il tombe dans le vide), il se réveille en
#                                sursaut (accroche)
#   {gestes PETIT}               Petit assis dans son lit, vu de dos (sa gauche = la gauche de l'écran) :
#                                {gestes souffle} trois petits souffles à sa gauche (1, 2, 3) ; {gestes refuge}
#                                « A'OUDHOU BILLAH… » ×3 ; {gestes tourne} il se recouche de l'autre côté ;
#                                {gestes chut} « À PERSONNE » ; {gestes protege} une lumière douce : « AUCUN MAL »
#                                (Mouslim 2261 · 2262 · Boukhari 7044)
# Ces classes sont branchées dans explique.Schema._ordre (import tardif) et scenario._fin_anim.
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import cast
import objets
import pxv
from px import Px
from pxv import smooth
from explique import Element, _titre, _titres, _fade, _copie, _erode, autocollant, petit_texte, BLANC, JAUNE

OL = (34, 22, 34)
GLACE = (170, 222, 255)


# ---------------------------------------------------------------- petits outils
def _peau(who="PETIT"):
    p = cast.CAST.get(who, {}).get("_peau") or {"b": (224, 166, 124), "s": (186, 128, 94), "d": (146, 96, 72),
                                                 "h": (242, 196, 156)}
    return p


def _sprite(who, pose="neutre", face="neutre", **kw):
    return Image.fromarray(cast.dessine(cast.CAST[who], pose, face, **kw).a, "RGBA")


def _buste(who, face="neutre", **kw):
    """Tête et épaules du perso (même cadrage qu'explique.tete), avec les options du dessin (sueur, joues…)."""
    r = cast.CAST[who]
    a = cast.dessine(r, "neutre", face, **kw).a
    g = cast.geo(r)
    zone = a[max(0, g.y0 - 14):g.y0 + 2, 8:36, 3]
    rows = np.where(zone.max(axis=1) > 0)[0]
    top = min(max(0, g.y0 - 14) + (int(rows[0]) if len(rows) else 14), g.y0 - 1)
    a = a[top: g.y0 + 26, 8:36].copy()
    bouche = (g.hd["mouth"][0] - 8, g.y0 + g.hd["mouth"][1] - top)
    return Image.fromarray(a, "RGBA"), bouche


def _grand(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def _tourne(im, angle, pivot):
    """Tourne une image (degrés, sens inverse des aiguilles d'une montre) autour d'un point ; renvoie (image, décalage)
    tel que le pivot reste au même endroit : coller l'image à (x_pivot - dx, y_pivot - dy)."""
    R = int(math.hypot(im.width, im.height)) + 4
    can = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0))
    can.alpha_composite(im, (int(R - pivot[0]), int(R - pivot[1])))
    if abs(angle) > 0.01:
        can = can.rotate(angle, resample=Image.NEAREST, center=(R, R))
    bb = can.getbbox() or (0, 0, 1, 1)
    return can.crop(bb), (R - bb[0], R - bb[1])


def _goutte(col, k=6, w=5, h=7):
    """Une goutte (pointe en haut) en pixels, agrandie xk."""
    c = Px(w + 2, h + 2, alpha=True)
    cx = (w + 2) / 2
    m = c.mask_ell(cx, h - (w / 2) + 1, w / 2, w / 2) | c.mask_poly([(cx - 0.6, 1), (cx + 0.6, 1), (cx + w / 2, h - w / 2 + 1),
                                                                    (cx - w / 2, h - w / 2 + 1)])
    c.fill(m, col)
    c.edge(m, tuple(int(v * 0.7) for v in col), "bottom", 1)
    c.px(int(cx) - 1, h - 2, tuple(min(255, int(v * 1.5) + 40) for v in col))
    c.outline(m, OL)
    return c.img(k, rgba=True)


def _etiquette_peche():
    return autocollant(petit_texte("PÉCHÉ", (255, 236, 236), (96, 20, 34), size=9, k=4), r=3, ombre=False)


def _brille(d, rng, zone, n, K, al):
    """Petites étoiles en croix (comme l'arbre propre) dans une zone (x0, y0, x1, y1) en pixels d'écran."""
    x0, y0, x1, y1 = zone
    for _ in range(n):
        x, y = int(rng.integers(x0, x1)), int(rng.integers(y0, y1))
        d.rectangle([x - K, y - 3 * K, x + K, y + 3 * K], fill=(255, 255, 230, al))
        d.rectangle([x - 3 * K, y - K, x + 3 * K, y + K], fill=(255, 255, 230, al))


def _frissons(d, cx, cy, ecart, u, K, col=(255, 255, 255)):
    """Traits de frisson de part et d'autre d'un point (ils changent de forme, l'image ne bouge pas)."""
    ph = int(u * 7) % 2
    for sgn in (-1, 1):
        for j, dy in enumerate((-1, 0, 1)):
            x = cx + sgn * (ecart + j % 2 * 2 * K)
            y = cy + dy * 9 * K
            pts = []
            for i in range(4):
                pts.append((x + sgn * i * 2 * K, y + ((i + ph + j) % 2) * 2 * K))
            d.line(pts, fill=(20, 16, 30, 255), width=K + 6)
            d.line(pts, fill=(*col, 255), width=K + 1)


def _carrelage(c, y0, y1):
    """Mur carrelé clair de la salle des ablutions (+ frise verte), dans un dessin Px."""
    W = c.w
    m = c.mask_rect(0, y0, W, y1)
    c.fill(m, (232, 238, 242))
    for x in range(0, W, 12):
        c.fill(m & c.mask_rect(x, y0, x + 1, y1), (204, 214, 222))
    for y in range(y0, y1, 12):
        c.fill(m & c.mask_rect(0, y, W, y + 1), (204, 214, 222))
    fr = c.mask_rect(0, y0 + 46, W, y0 + 54)
    c.fill(fr, (46, 128, 112))
    for x in range(0, W, 6):
        c.fill(fr & c.mask_rect(x + 2, y0 + 48, x + 4, y0 + 52), (230, 236, 228))


def _robinet(c, x, y, givre=False):
    """Robinet chromé fixé au mur : plaque (x, y), bec qui descend ; renvoie le point d'où l'eau tombe."""
    chrome, ombre, clair = (178, 188, 200), (122, 132, 148), (244, 248, 252)
    plaque = c.mask_rrect(x, y, x + 14, y + 10, 2)
    c.shape(plaque, chrome, shade=ombre, light=clair, band=1, olcol=OL)
    tuyau = c.mask_rect(x + 13, y + 3, x + 34, y + 8)
    c.shape(tuyau, chrome, shade=ombre, light=clair, band=1, olcol=OL)
    bec = c.mask_rect(x + 28, y + 6, x + 35, y + 20) | c.mask_rect(x + 27, y + 18, x + 36, y + 21)
    c.shape(bec, chrome, shade=ombre, light=clair, band=1, olcol=OL)
    poignee = c.mask_rect(x + 16, y - 6, x + 19, y + 3) | c.mask_rect(x + 11, y - 8, x + 24, y - 5)
    c.shape(poignee, (60, 120, 210), shade=(40, 84, 160), light=(120, 170, 240), band=1, olcol=OL)
    if givre:                                             # givre sur le dessus, petits glaçons sous le tuyau
        for (gx, gy) in ((x + 2, y), (x + 6, y - 1), (x + 15, y + 2), (x + 22, y + 2), (x + 29, y + 5), (x + 33, y + 5)):
            c.fill(c.mask_rect(gx, gy, gx + 3, gy + 1), (236, 248, 255))
        for gx in (x + 17, x + 23):
            c.fill(c.mask_poly([(gx, y + 8), (gx + 3, y + 8), (gx + 1.5, y + 14)]), (200, 236, 255))
            c.px(gx + 1, y + 9, (255, 255, 255))
    return (x + 31.5, y + 21)


def _mains(c, x, y, peau, rouge=0.0):
    """Les deux mains en coupe, vues de côté (paumes vers le haut, doigts à droite), sous l'eau : (x, y) = le creux de
    la main de devant ; les avant-bras arrivent de la gauche, manches rouges retroussées. rouge > 0 : le froid."""
    def teinte(col, cible):
        return tuple(int(v + (w - v) * rouge) for v, w in zip(col, cible)) if rouge > 0 else col
    b, s_, h, dk = (teinte(peau["b"], (236, 130, 120)), teinte(peau["s"], (200, 96, 92)), peau["h"],
                    teinte(peau["d"], (170, 80, 76)))
    for k, (dx, dy) in enumerate(((5, -4), (0, 0))):     # la main du fond (plus sombre), puis celle de devant
        X, Y = x + dx, y + dy
        cb, cs = (s_, dk) if k == 0 else (b, s_)
        manche = c.mask_poly([(X - 86, Y - 3), (X - 50, Y - 1), (X - 48, Y + 15), (X - 86, Y + 19)])
        c.shape(manche, (200, 50, 50) if k else (160, 38, 42), shade=(150, 34, 40), light=(232, 92, 84), band=1,
                olcol=OL)
        c.fill(manche & c.mask_rect(X - 54, 0, X - 48, c.h), (150, 34, 40) if k else (126, 28, 34))   # le revers
        bras = c.mask_poly([(X - 52, Y + 1), (X - 13, Y + 1), (X - 11, Y + 10), (X - 52, Y + 13)])
        c.shape(bras, cb, shade=cs, light=h if k else None, band=1, olcol=OL)
        paume = c.mask_poly([(X - 15, Y - 1), (X - 11, Y + 8), (X + 3, Y + 11), (X + 12, Y + 8), (X + 18, Y - 1),
                             (X + 16, Y - 6), (X + 11, Y - 5), (X + 8, Y + 1), (X - 2, Y + 3), (X - 12, Y - 2)])
        c.shape(paume, cb, shade=cs, light=h if k else None, band=1, olcol=OL)
        for j in range(3):                               # les doigts repliés vers le haut
            c.fill(c.mask_rect(X + 12 + j, Y - 4 + 2 * j, X + 13 + j, Y - 3 + 2 * j), cs)
        pouce = c.mask_poly([(X - 10, Y), (X - 6, Y - 6), (X, Y - 7), (X + 1, Y - 5), (X - 4, Y + 1)])
        c.shape(pouce, cb, shade=cs, light=h if k else None, band=1, olcol=OL)
        c.fill(c.mask_rect(X - 7, Y + 6, X + 9, Y + 7) & paume, cs)  # le pli de la paume


def _pieds(c, x, y, peau, e=1.0):
    """Deux pieds nus vus de côté (orteils vers la droite), talon du pied de devant en x, sol à y ; bas du jean
    retroussé ; e = échelle."""
    b, s_, h = peau["b"], peau["s"], peau["h"]
    for k, dx in enumerate((10, 0)):                    # le pied du fond, puis celui de devant
        X, Y = x + dx * e, y - 3 * k * e

        def P(a, b_):
            return (X + a * e, Y + b_ * e)
        jambe = c.mask_poly([P(-2, -30), P(8, -30), P(8, -9), P(-2, -9)])
        c.shape(jambe, b if k else s_, shade=s_ if k else peau["d"], light=h, band=1, olcol=OL)
        jean = c.mask_poly([P(-4, -46), P(10, -46), P(10, -27), P(-4, -27)])
        c.shape(jean, (62, 96, 166) if k else (48, 76, 136), shade=(44, 70, 128), light=(96, 132, 200), band=1, olcol=OL)
        c.fill(c.mask_poly([P(-4, -32), P(10, -32), P(10, -28), P(-4, -28)]), (96, 132, 200) if k else (70, 104, 170))
        pied = c.mask_poly([P(-3, 0), P(-4, -6), P(-1, -11), P(8, -11), P(18, -6), P(30, -4), P(33, -1), P(32, 0)])
        c.shape(pied, b if k else s_, shade=s_ if k else peau["d"], light=h, band=1, olcol=OL)
        for j in range(4):                              # les orteils
            ox, oy = P(23 + 3 * j, -3.5 + 0.5 * (j // 2))
            c.fill(c.mask_rect(ox, oy, ox + max(1, e * 0.8), oy + max(1, e)), s_ if k else peau["d"])
        c.fill(c.mask_poly([P(-3, -1), P(32, -1), P(32, 0), P(-3, 0)]), s_)


def _voile(W, H, zones, u, alpha=1.0, seed=3):
    """Voile sombre (les péchés) : des volutes violet foncé autour des zones (cx, cy, rx, ry), qui ondulent doucement."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rng = np.random.default_rng(seed)
    for (cx, cy, rx, ry) in zones:
        for i in range(9):
            a = 2 * math.pi * i / 9 + 0.4 * math.sin(u * 1.3 + i)
            r_ = 0.75 + 0.25 * math.sin(u * 2.1 + i * 1.7)
            x = cx + rx * 0.8 * math.cos(a) * r_
            y = cy + ry * 0.8 * math.sin(a) * r_
            rr = float(rng.uniform(0.32, 0.5)) * min(rx, ry) * 2
            d.ellipse([x - rr, y - rr * 0.8, x + rr, y + rr * 0.8], fill=(46, 30, 64, int(150 * alpha)))
    lay = lay.filter(ImageFilter.GaussianBlur(10))
    return lay


# ---------------------------------------------------------------- {fievre PETIT}
class Fievre(Element):
    """{fievre PETIT} : gros plan sur Petit malade sous sa couverture : le thermomètre (dans sa bouche et en grand à
    côté) monte de 37,0 à 39,5 °C, gouttes de sueur, joues rouges, traits de frisson. Rien ne secoue l'image."""
    plein = True
    negatif = True                       # le mercure monte déjà avant le mot
    K = 6
    PW_, PH_ = 170, 150
    T0, T1 = -0.5, 1.4                   # montée du mercure (secondes autour du mot)
    TMIN, TMAX = 35.0, 41.0
    TBAS, THAUT = 37.0, 39.5

    def __init__(s, cmd, who="PETIT"):
        super().__init__(cmd)
        s.who = who if who in cast.CAST else "PETIT"
        s._cache = {}

    def sons_el(s):
        return [(s.T1 - 0.1, "sa_ting", 0.025, None)]

    def _fond(s):
        if "f" in s._cache:
            return s._cache["f"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        c.vgrad(tout_, 0, H, (196, 204, 226), (160, 170, 200), steps=5)            # mur de la chambre
        for x in range(8, W, 14):
            c.dither(tout_ & c.mask_rect(x, 0, x + 4, H), (184, 192, 216), 0.5)
        tete_lit = c.mask_rrect(6, 30, 118, 120, 10)                              # tête de lit en bois
        c.shape(tete_lit, (150, 100, 62), shade=(116, 76, 46), light=(186, 132, 84), band=2, olcol=OL)
        c.fill(c.mask_rrect(12, 36, 112, 116, 8) & tete_lit, (164, 112, 70))
        oreiller = c.mask_rrect(14, 56, 110, 100, 12)
        c.shape(oreiller, (240, 242, 250), shade=(196, 204, 226), light=(255, 255, 255), band=2, olcol=OL)
        c.fill(c.mask_rect(20, 76, 104, 77) & oreiller, (214, 220, 236))
        tab = c.mask_rect(0, 118, W, H) & tout_                                   # le bas : le matelas
        c.fill(tab, (120, 140, 190))
        s._cache["f"] = c
        return c

    def _couverture(s):
        if "c" in s._cache:
            return s._cache["c"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        m = c.mask_poly([(4, 150), (2, 112), (14, 100), (36, 94), (52, 99), (66, 99), (84, 94), (104, 98), (120, 108),
                         (126, 150)]) & tout_
        c.shape(m, (226, 120, 54), shade=(178, 84, 40), light=(250, 164, 96), band=2, olcol=OL)
        for (x0, y0) in ((10, 112), (40, 104), (72, 104), (100, 112), (24, 130), (58, 126), (92, 130)):
            carre = c.mask_rect(x0, y0, x0 + 14, y0 + 12) & m
            c.fill(carre, (204, 70, 64))
            c.dither(carre, (232, 104, 92), 0.3)
        for x in range(8, 126, 5):                                                # surpiqûres
            c.px(x, 103 + int(3 * math.sin(x / 9)), (250, 196, 140))
        c.outline(m, OL)
        s._cache["c"] = c.img(s.K, rgba=True)
        return s._cache["c"]

    def _thermo_fixe(s):
        """Le grand thermomètre (sans le mercure) : tube, graduations, boule ; en pixels d'écran."""
        if "t" in s._cache:
            return s._cache["t"]
        K = s.K
        c = Px(36, 128, alpha=True)
        tube = c.mask_rrect(10, 2, 26, 108, 8) | c.mask_ell(18, 112, 13, 13)
        c.shape(tube, (236, 244, 252), shade=(186, 200, 220), light=(255, 255, 255), band=2, olcol=OL)
        c.fill(c.mask_rrect(14, 6, 22, 104, 4), (210, 222, 236))
        for i in range(13):                                                       # graduations 35 → 41 °C
            y = int(round(s._y_px(35 + i * 0.5)))
            c.fill(c.mask_rect(3 if i % 2 == 0 else 5, y, 9, y + 1), (60, 60, 80))
        s._cache["t"] = c.img(K, rgba=True)
        return s._cache["t"]

    def _y_px(s, temp):                   # hauteur de la colonne dans le petit dessin du thermomètre (36 x 128)
        return 100 - (temp - s.TMIN) / (s.TMAX - s.TMIN) * 92

    def _temp(s, u):
        return s.TBAS + (s.THAUT - s.TBAS) * smooth((u - s.T0) / (s.T1 - s.T0))

    def image(s, u):
        K = s.K
        W_, H_ = s.PW_ * K, s.PH_ * K
        im = s._fond().img(K, rgba=True)
        face = "enerve" if u >= -0.05 else "triste"
        key = ("b", face)
        if key not in s._cache:
            b, bouche = _buste(s.who, face, sweat=True, blush=True)
            s._cache[key] = (_grand(b, 12), bouche)
        bus, bouche = s._cache[key]
        bx, by = 156, 150
        im.alpha_composite(bus, (bx, by))
        d = ImageDraw.Draw(im)
        mx, my = bx + bouche[0] * 12 + 10, by + bouche[1] * 12 + 4                # thermomètre dans la bouche
        L, ep, ang = 190, 16, math.radians(14)
        ca, sa = math.cos(ang), math.sin(ang)
        pts = [(mx, my - ep / 2), (mx + L * ca, my + L * sa - ep / 2), (mx + L * ca, my + L * sa + ep / 2), (mx, my + ep / 2)]
        d.polygon(pts, fill=(236, 244, 252, 255), outline=(34, 22, 34, 255), width=5)
        niv = (s._temp(u) - s.TMIN) / (s.TMAX - s.TMIN)
        d.line([(mx + 10, my), (mx + 10 + (L - 30) * ca * (0.25 + 0.7 * niv), my + (L - 30) * sa * (0.25 + 0.7 * niv))],
               fill=(222, 40, 40, 255), width=5)
        im.alpha_composite(s._couverture())
        # le grand thermomètre et sa colonne
        th = s._thermo_fixe()
        tx, ty = 790, 60
        im.alpha_composite(th, (tx, ty))
        temp = s._temp(u)
        ytop = ty + s._y_px(temp) * K
        rouge = (226, 40, 40) if temp < 39 else (int(226 + 29 * (0.5 + 0.5 * math.sin(u * 7))), 36, 36)
        d.rounded_rectangle([tx + 15 * K, ytop, tx + 21 * K, ty + 108 * K], 3 * K, fill=(*rouge, 255))
        d.ellipse([tx + 9 * K, ty + 103 * K, tx + 27 * K, ty + 121 * K], fill=(*rouge, 255))
        d.rectangle([tx + 16 * K, ytop + K, tx + 17 * K, ty + 104 * K], fill=(255, 150, 150, 255))
        if temp >= 38.6:                                                          # la boule chauffe : halo rouge doux
            a = int(120 * smooth((temp - 38.6) / 0.7) * (0.75 + 0.25 * math.sin(u * 6)))
            halo = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
            ImageDraw.Draw(halo).ellipse([tx - 30, ty + 90 * K, tx + 36 * K + 30, ty + 128 * K + 30], fill=(255, 60, 40, a))
            im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(18)))
        lab = f"{temp:0.1f}".replace(".", ",") + " °C"
        col = (255, 120, 60) if temp < 39 else (255, 70, 60)
        t_img = s._cache.setdefault(("lab", lab, col), _titre(lab, col, 92, r=4))
        im.alpha_composite(t_img, (int(min(835 - t_img.width, 640 - t_img.width / 2)), int(96 - t_img.height / 2)))
        # gouttes de sueur qui glissent sur le front, frissons autour de la tête
        g_ = s._cache.setdefault("g", _goutte((150, 214, 255), k=5))
        for j, (gx, gy, dec) in enumerate(((bx + 70, by + 110, 0.0), (bx + 250, by + 96, 0.6))):
            v = ((u + 2 + dec) % 1.5) / 1.5
            a = smooth(v / 0.15) * (1 - smooth((v - 0.75) / 0.25))
            im.alpha_composite(_fade(g_, a), (int(gx), int(gy + 90 * v)))
        _frissons(d, bx + 168, by + 150, 230, u, K)
        return im


# ---------------------------------------------------------------- {forge "TES PETITS PÉCHÉS"} {soufflet}
class Forge(Element):
    """{forge "TES PETITS PÉCHÉS"} : une forge ; dans les braises, une barre de fer couverte de croûtes noires (4 marquées
    « PÉCHÉ »). {soufflet} : le soufflet du forgeron souffle trois fois, le feu monte, les croûtes se détachent une à une
    et s'envolent en cendres ; le fer ressort propre et brille (Mouslim 2575)."""
    plein = True
    K = 6
    PW_, PH_ = 170, 140
    P = 0.75                               # durée d'un coup de soufflet
    N_COUPS = 3
    CROUTES = [(92, 0), (99, 1), (106, -1), (113, 1), (120, 0), (127, -1), (134, 1), (141, 0)]
    MARQ = (1, 3, 5, 7)
    DT, VOL = 0.27, 1.3

    def __init__(s, cmd, titre="TES PETITS PÉCHÉS // AVIS MAJORITAIRE"):
        super().__init__(cmd)
        s.titre = titre
        s.t_souffle = None
        s._cache = {}
        rng = np.random.default_rng(7)
        s.formes = [(float(rng.uniform(3.0, 4.4)), float(rng.uniform(3.2, 4.6)), float(rng.uniform(-1, 1))) for _ in s.CROUTES]

    def sons_el(s):
        out = [(0.0, "dv_feu_allumage", 0.03, None)]
        if s.t_souffle is not None:
            out += [(s.t_souffle, "tr_whoosh_vent", 0.05, None), (s.fin() + 0.2, "sa_scintillement", 0.05, None)]
        return out

    def fin(s):
        return None if s.t_souffle is None else s.t_souffle + 0.15 + (len(s.CROUTES) - 1) * s.DT + s.VOL

    def _fond(s):
        if "f" in s._cache:
            return s._cache["f"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        c.vgrad(tout_, 0, H, (70, 52, 48), (40, 30, 30), steps=5)                 # mur de pierre de l'atelier
        for y in range(6, H, 10):
            c.fill(tout_ & c.mask_rect(0, y, W, y + 1), (52, 38, 36))
            dec = 0 if (y // 10) % 2 == 0 else 9
            for x in range(dec, W, 18):
                c.fill(tout_ & c.mask_rect(x, y, x + 1, y + 10), (52, 38, 36))
        hotte = c.mask_poly([(84, 0), (164, 0), (156, 34), (92, 34)])              # la hotte au-dessus du feu
        c.shape(hotte, (84, 66, 60), shade=(60, 46, 42), light=(110, 88, 80), band=2, olcol=OL)
        c.fill(c.mask_rect(90, 30, 158, 34), (66, 50, 46))
        base = c.mask_rect(70, 92, 168, 140) & tout_                               # le foyer en pierre
        c.shape(base, (110, 92, 86), shade=(80, 66, 62), light=(140, 120, 110), band=2, olcol=OL)
        for y in (104, 116, 128):
            c.fill(base & c.mask_rect(70, y, 168, y + 1), (80, 66, 62))
        for (x, y0) in ((86, 92), (112, 104), (138, 92), (98, 116), (128, 116), (90, 128), (150, 128)):
            c.fill(base & c.mask_rect(x, y0, x + 1, y0 + 12), (80, 66, 62))
        dalle = c.mask_rect(66, 86, 168, 93)
        c.shape(dalle, (130, 110, 100), shade=(96, 80, 74), light=(160, 140, 128), band=1, olcol=OL)
        s._cache["f"] = c
        return c

    def _ouverture(s, u):
        """Ouverture du soufflet (1 = ouvert, 0,35 = fermé) : trois coups doux, puis il reste ouvert."""
        if s.t_souffle is None or u < s.t_souffle or u > s.t_souffle + s.N_COUPS * s.P:
            return 1.0
        ph = (u - s.t_souffle) % s.P
        if ph < 0.28:
            return 1.0 - 0.65 * smooth(ph / 0.28)
        return 0.35 + 0.65 * smooth((ph - 0.28) / (s.P - 0.28))

    def _souffle(s, u):
        """Force du feu : monte après chaque coup de soufflet, retombe doucement."""
        if s.t_souffle is None or u < s.t_souffle:
            return 0.0
        f = 0.0
        for i in range(s.N_COUPS):
            t_ = s.t_souffle + i * s.P + 0.18
            if u >= t_:
                f = max(f, math.exp(-(u - t_) / 0.6))
        return f

    def _chaleur(s, u):
        if s.t_souffle is None:
            return 0.0
        fin = s.fin()
        monte = smooth((u - s.t_souffle) / 1.6)
        refroidit = smooth((u - fin + 0.1) / 0.8)
        return monte * (1 - refroidit)

    def image(s, u):
        K = s.K
        c = _copie(s._fond())
        o = s._ouverture(u)
        boost = s._souffle(u)
        # les braises
        braises = c.mask_ell(118, 88, 44, 6) & c.mask_rect(0, 82, c.w, 92)
        c.fill(braises, (60, 24, 20))
        rng = np.random.default_rng(int(u * 8) % 997)
        for _ in range(26):
            x, y = int(rng.integers(76, 160)), int(rng.integers(83, 90))
            if braises[y, x]:
                c.fill(c.mask_rect(x, y, x + 2, y + 1), (255, int(110 + 80 * boost), 30) if rng.random() < 0.6 else (180, 40, 20))
        # les flammes (derrière le fer)
        for j, fx in enumerate((84, 98, 112, 126, 140, 154)):
            h = (12 + 5 * math.sin(u * 7.3 + j * 1.9) + 3 * math.sin(u * 13.1 + j)) * (1 + 1.1 * boost)
            w = 6 + 2 * boost
            fl = c.mask_poly([(fx - w, 88), (fx - w * 0.4, 88 - h * 0.55), (fx + 1.5 * math.sin(u * 9 + j), 88 - h),
                              (fx + w * 0.5, 88 - h * 0.5), (fx + w, 88)])
            c.fill(fl, (238, 110, 34))
            coeur = c.mask_poly([(fx - w * 0.5, 88), (fx, 88 - h * 0.62), (fx + w * 0.5, 88)])
            c.fill(coeur, (255, 206, 80) if boost < 0.5 else (255, 238, 170))
        # le fer : sombre → rouge orangé quand il chauffe → acier propre qui brille
        ch = s._chaleur(u)
        fin = s.fin()
        propre = fin is not None and u >= fin - 0.1
        base_col = np.array((96, 96, 108), float)
        chaud = np.array((255, 140, 56), float)
        acier = np.array((206, 214, 228), float)
        col = base_col + (chaud - base_col) * ch
        if propre:
            col = col + (acier - col) * smooth((u - fin + 0.1) / 0.8)
        col = tuple(int(v) for v in col)
        fer = c.mask_rect(86, 77, 150, 85)
        c.shape(fer, col, shade=tuple(int(v * 0.72) for v in col), light=tuple(min(255, int(v * 1.2) + 20) for v in col),
                band=1, olcol=OL)
        pince = c.mask_rect(150, 79, 169, 83)                                     # la pince qui tient le fer
        c.shape(pince, (70, 70, 80), shade=(46, 46, 54), light=(110, 110, 124), band=1, olcol=OL)
        # les croûtes (la saleté du fer) encore collées
        for i, ((cx, dy), (rx, ry, sk)) in enumerate(zip(s.CROUTES, s.formes)):
            t0 = None if s.t_souffle is None else s.t_souffle + 0.15 + i * s.DT
            if t0 is not None and u >= t0:
                continue
            cr = c.mask_ell(cx + sk, 81 + dy, rx, ry)
            c.fill(cr, (38, 32, 36))
            c.dither(cr & ~_erode(cr, 1), (116, 62, 40), 0.6)
            c.px(cx - 1, 79 + dy, (70, 60, 66))
        # le soufflet (à gauche) : deux planches articulées au bec, le cuir entre elles
        hx, hy = 62, 84
        ang = math.radians(12 + 13 * o)
        L = 50
        haut = (hx - L * math.cos(ang), hy - L * math.sin(ang))
        bas = (hx - L * math.cos(ang), hy + L * math.sin(ang))
        cuir = c.mask_poly([(hx, hy), haut, (haut[0] + 4, (haut[1] + bas[1]) / 2), bas])
        c.shape(cuir, (134, 84, 50), shade=(100, 60, 36), light=(166, 112, 72), band=1, olcol=OL)
        for k_ in range(1, 4):                                                    # les plis du cuir
            fx = hx - L * k_ / 4.2
            ey = (fx - hx) * math.tan(ang)
            c.line(fx, hy + ey + 2, fx, hy - ey - 2, (96, 58, 34))
        for (p_, sgn) in ((haut, -1), (bas, 1)):
            planche = c.mask_poly([(hx, hy + sgn * 1), (p_[0], p_[1]), (p_[0], p_[1] + sgn * 5), (hx, hy + sgn * 4)])
            c.shape(planche, (170, 118, 66), shade=(128, 86, 48), light=(204, 152, 96), band=1, olcol=OL)
        poignee = c.mask_rect(int(haut[0]) - 8, int(haut[1]) - 2, int(haut[0]) + 1, int(haut[1]) + 2)
        c.shape(poignee, (120, 80, 46), shade=(90, 58, 34), band=1, olcol=OL)
        bec = c.mask_poly([(hx - 1, hy - 3), (hx + 12, hy - 1), (hx + 12, hy + 1), (hx - 1, hy + 3)])
        c.shape(bec, (150, 150, 160), shade=(100, 100, 112), light=(200, 200, 210), band=1, olcol=OL)
        im = c.img(K, rgba=True)
        tit = s._cache.setdefault("t", _titres(s.titre, BLANC, 74))
        haut_px = tit.height + 50
        W_, H_ = im.width, im.height + haut_px
        out = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        out.alpha_composite(tit, (int(W_ / 2 - tit.width / 2), 46))
        lueur = Image.new("RGBA", im.size, (0, 0, 0, 0))                          # la lueur du feu sur le mur
        ImageDraw.Draw(lueur).ellipse([60 * K, 30 * K, 176 * K, 120 * K], fill=(255, 140, 50, int(60 + 70 * boost)))
        im2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
        im2.alpha_composite(im)
        im2.alpha_composite(lueur.filter(ImageFilter.GaussianBlur(40)))
        out.alpha_composite(im2, (0, haut_px))
        d = ImageDraw.Draw(out)
        if s.t_souffle is not None and s.t_souffle <= u <= s.t_souffle + s.N_COUPS * s.P:   # l'air du soufflet
            ph = (u - s.t_souffle) % s.P
            if ph < 0.45:
                a = int(220 * (1 - ph / 0.45))
                for j, dy in enumerate((-2, 0, 2)):
                    x0 = (hx + 13) * K + ph * 260
                    d.line([(x0, (hy + dy) * K + haut_px), (x0 + 60 + 20 * j, (hy + dy * 1.6) * K + haut_px)],
                           fill=(255, 255, 255, a), width=K)
        for _ in range(int(4 + 10 * boost)):                                       # étincelles qui montent
            x = int(rng.integers(80, 160)) * K
            y = (88 - rng.integers(4, 40) * (0.5 + boost)) * K + haut_px
            d.rectangle([x, y, x + K - 1, y + K - 1], fill=(255, 220, 120, 230))
        lab = s._cache.setdefault("lab", _etiquette_peche())
        for i, ((cx, dy), (rx, ry, sk)) in enumerate(zip(s.CROUTES, s.formes)):
            t0 = None if s.t_souffle is None else s.t_souffle + 0.15 + i * s.DT
            if t0 is None or u < t0:                                               # encore collée : son étiquette
                if i in s.MARQ:
                    yl = (81 + dy - 7) * K + haut_px - lab.height if i % 4 == 1 else (81 + dy + 7) * K + haut_px
                    out.alpha_composite(lab, (int(cx * K - lab.width / 2), int(yl)))
                continue
            v = (u - t0) / s.VOL                                                   # elle s'envole en cendres
            if v >= 1:
                continue
            x = cx * K + 30 * K * v * (0.3 + 0.7 * (i % 3) / 2) * (1 if i % 2 else -0.4) + 10 * math.sin(v * 7 + i) * K / 6
            y = (81 + dy) * K + haut_px - 52 * K * (v ** 0.8)
            gris = int(38 + 120 * smooth(v / 0.6))
            a = 1 - smooth((v - 0.55) / 0.45)
            r_ = int(rx * K * (1 - 0.4 * v))
            d.ellipse([x - r_, y - r_, x + r_, y + r_], fill=(gris, gris - 4, gris + 2, int(255 * a)))
            if i in s.MARQ:
                out.alpha_composite(_fade(lab, a), (int(x - lab.width / 2), int(y - r_ - lab.height)))
        fin = s.fin()
        if fin is not None and fin - 0.2 <= u < fin + 2.0:                         # le fer propre brille
            v = u - fin + 0.2
            xs = (86 + 64 * smooth(v / 0.7)) * K
            if v < 0.9:
                d.polygon([(xs - 20, 77 * K + haut_px), (xs + 10, 77 * K + haut_px), (xs - 10, 85 * K + haut_px),
                           (xs - 40, 85 * K + haut_px)], fill=(255, 255, 255, int(200 * (1 - smooth((v - 0.6) / 0.3)))))
            al = int(230 * smooth(v / 0.3) * (1 - smooth((v - 1.4) / 0.6)))
            _brille(d, np.random.default_rng(int(u * 6)), (86 * K, 60 * K + haut_px, 150 * K, 95 * K + haut_px), 6, K, al)
        return out


# ---------------------------------------------------------------- {glace}
class Glace(Element):
    """{glace} : gros plan sur le robinet de la salle des ablutions, givré ; les mains arrivent dessous, l'eau glacée
    tombe dedans, elles reculent un peu et rougissent, « BRRR ! », traits de frisson (accroche)."""
    plein = True
    negatif = True
    K = 6
    PW_, PH_ = 170, 150
    T_CHOC = 0.0
    ELAN = 0.45

    def __init__(s, cmd, who="PETIT"):
        super().__init__(cmd)
        s.who = who if who in cast.CAST else "PETIT"
        s._cache = {}

    def sons_el(s):
        return [(-0.3, "dv_eau_jaillit", 0.05, None)]

    def _fond(s):
        if "f" in s._cache:
            return s._cache["f"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        _carrelage(c, 0, H)
        c.al &= tout_
        s.bec = _robinet(c, 96, 34, givre=True)
        bac = c.mask_rect(0, 132, W, H) & tout_                                   # le rebord en pierre
        c.shape(bac, (170, 172, 180), shade=(130, 132, 142), light=(206, 208, 216), band=1, olcol=OL)
        s._cache["f"] = c
        return c

    def image(s, u):
        K = s.K
        c = _copie(s._fond())
        bx, by = s.bec
        e = smooth((u - (s.T_CHOC - s.ELAN)) / s.ELAN)
        v = u - s.T_CHOC
        recul = (-6 * smooth(v / 0.12) + 6 * smooth((v - 0.3) / 0.5)) if v >= 0 else 0.0
        mx = bx - 2 - 40 * (1 - e) + recul
        my = 100
        rouge = 0.55 * smooth((v - 0.1) / 0.8) if v >= 0 else 0.0
        _mains(c, mx, my, _peau(s.who), rouge=rouge)
        im = c.img(K, rgba=True)
        d = ImageDraw.Draw(im)
        y_fin = (my - 2) * K if e > 0.75 else 132 * K                              # le filet d'eau glacée
        x0, x1 = (bx - 2.5) * K, (bx + 2.5) * K
        d.rectangle([x0, by * K, x1, y_fin], fill=(*GLACE, 215))
        dec = (u * 900) % (12 * K)
        y = by * K - 12 * K + dec
        while y < y_fin:
            d.rectangle([x0 + K, y, x0 + 2 * K, min(y_fin, y + 4 * K)], fill=(255, 255, 255, 230))
            y += 12 * K
        if e > 0.75:                                                               # éclaboussures dans les mains
            rng = np.random.default_rng(int(u * 14) % 997)
            for _ in range(10):
                ang = rng.uniform(math.pi * 1.05, math.pi * 1.95)
                rr = rng.uniform(4, 24) * K
                x = bx * K + math.cos(ang) * rr
                yy = (my - 3) * K + math.sin(ang) * rr * 0.6
                d.rectangle([x, yy, x + K, yy + K], fill=(220, 244, 255, 235))
        if v >= 0:                                                                 # « BRRR ! »
            br = s._cache.setdefault("brrr", _titre("BRRR !", (150, 214, 255), 170, r=5))
            a = smooth((v - 0.04) / 0.2)
            k2 = 0.86 + 0.14 * smooth(v / 0.25)
            br2 = br.resize((int(br.width * k2), int(br.height * k2)), Image.LANCZOS)
            im.alpha_composite(_fade(br2, a), (int(300 - br2.width / 2), int(150 - br2.height / 2)))
            _frissons(d, (mx - 8) * K, (my + 3) * K, 34 * K, u, K, col=(200, 236, 255))
        rng = np.random.default_rng(int(u * 3) % 997)                              # le givre scintille
        for _ in range(3):
            gx = int(rng.integers(96, 132)) * K
            gy = int(rng.integers(28, 40)) * K
            d.rectangle([gx - K, gy - 2 * K, gx + K, gy + 2 * K], fill=(255, 255, 255, 200))
            d.rectangle([gx - 2 * K, gy - K, gx + 2 * K, gy + K], fill=(255, 255, 255, 200))
        return im


# ---------------------------------------------------------------- {ablutions PETIT} {ablutions yeux|mains|pieds}
class Ablutions(Element):
    """{ablutions PETIT} : les ablutions, partie par partie (Mouslim 244). Les péchés = un voile sombre (une IMAGE :
    les péchés ne sont pas des corps qui sortent vraiment — an-Nawawi 3/133) autour des yeux, des mains, des pieds,
    marqué « PÉCHÉ ». {ablutions yeux} : l'eau, toujours CLAIRE, coule sur le visage ; le voile se défait en lumière avec
    la dernière goutte. {ablutions mains} : l'eau coule de la main jusqu'au coude ; {ablutions pieds} : sur tout le pied,
    talon compris (Coran 5:6, Boukhari 165). Il ressort propre (étincelles)."""
    plein = True
    K = 6
    PW_, PH_ = 170, 150
    PARTIES = ("yeux", "mains", "pieds")
    LEGENDES = {"yeux": "TES YEUX // CE QU'ILS ONT REGARDÉ", "mains": "TES MAINS // CE QU'ELLES ONT FAIT",
                "pieds": "TES PIEDS // LÀ OÙ ILS ONT MARCHÉ"}
    LAVE = 1.5                                   # durée du lavage d'une partie
    HAUT = 240                                   # bande du haut pour la légende (+ 50 px de marge sous la source)

    def __init__(s, cmd, who="PETIT"):
        super().__init__(cmd)
        s.who = who if who in cast.CAST else "PETIT"
        s.t = {}                                 # partie → instant du lavage (u)
        s._cache = {}

    def sons_el(s):
        out = [(t_, "tr_whoosh_doux", 0.035, None) for t_ in sorted(s.t.values())]
        if "pieds" in s.t:
            out.append((s.t["pieds"] + s.LAVE, "sa_scintillement", 0.05, None))
        return out

    def _partie(s, u):
        """La partie montrée à l'instant u, la précédente (fondu) et l'avancement du fondu."""
        evts = sorted((t_, p_) for p_, t_ in s.t.items())
        cur, prev, t_cur = "yeux", None, None
        for (t_, p_) in evts:
            if u >= t_ - 0.25:
                prev, cur, t_cur = (cur if cur != p_ else prev), p_, t_
        f = 1.0 if t_cur is None else smooth((u - (t_cur - 0.25)) / 0.3)
        return cur, prev, f

    def _fond(s):
        if "f" in s._cache:
            return s._cache["f"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        _carrelage(c, 0, H)
        c.al &= tout_
        bac = c.mask_rect(0, 132, W, H) & tout_
        c.shape(bac, (170, 172, 180), shade=(130, 132, 142), light=(206, 208, 216), band=1, olcol=OL)
        grille = c.mask_rrect(64, 138, 106, 146, 2)                              # la grille d'évacuation
        c.fill(grille, (70, 74, 86))
        for x in range(67, 104, 4):
            c.fill(c.mask_rect(x, 139, x + 2, 145), (34, 36, 44))
        c.outline(grille, OL)
        s._cache["f"] = c
        return c

    def _scene(s, partie, propre):
        """Le dessin fixe d'une partie (sans l'eau), la zone du voile (cx, cy, rx, ry) et la description de l'eau."""
        key = ("s", partie, propre)
        if key in s._cache:
            return s._cache[key]
        K = s.K
        c = _copie(s._fond())
        peau = _peau(s.who)
        if partie == "mains":
            bec = _robinet(c, 96, 26)
            mx, my = bec[0] - 2, 92
            _mains(c, mx, my, peau)
            im = c.img(K, rgba=True)
            zone = ((mx - 26) * K, (my + 3) * K, 40 * K, 13 * K)
            eau = ("bras", bec[0] * K, bec[1] * K, (my - 2) * K, (mx - 50) * K, (mx + 6) * K, (my + 1) * K)
        elif partie == "pieds":
            bec = _robinet(c, 74, 22)
            _pieds(c, 60, 128, peau, e=1.6)
            im = c.img(K, rgba=True)
            zone = (88 * K, 120 * K, 36 * K, 11 * K)
            eau = ("pied", bec[0] * K, bec[1] * K, 114 * K, 56 * K, 114 * K, 121 * K)
        else:                                                                    # le visage, les yeux fermés
            im = c.img(K, rgba=True)
            b, _ = _buste(s.who, "content" if propre else "ferme")
            b = _grand(b.crop((0, 0, b.width, 36)), 20)
            bx, by = int(im.width / 2 - b.width / 2), 20
            im.alpha_composite(b, (bx, by))
            g = cast.geo(cast.CAST[s.who])
            oeil_x = (g.hd["ex"] - 8 + 1.5) * 20 + bx
            oeil_y = by + (b.height / 36) * 12.5
            zone = (oeil_x, oeil_y, 9 * 20, 4.5 * 20)
            eau = ("visage", bx, by, b.width, b.height)
        s._cache[key] = (im, zone, eau)
        return s._cache[key]

    def _calque(s, partie, u):
        K = s.K
        t_ = s.t.get(partie)
        propre = t_ is not None and u >= t_ + s.LAVE * 0.8
        im, zone, eau = s._scene(partie, propre)
        im = im.copy()
        W_, H_ = im.size
        cx, cy, rx, ry = zone
        lab = s._cache.setdefault("lab", _etiquette_peche())
        a_voile = 1.0 if (t_ is None or u < t_ + 0.3) else 1 - smooth((u - t_ - 0.3) / 0.9)
        if a_voile > 0.01:                                                        # le voile sombre (une image)
            im.alpha_composite(_voile(W_, H_, [zone], u, alpha=a_voile))
            for j, (fx, fy) in enumerate(((0.55, -0.9), (-0.75, 0.55))):
                im.alpha_composite(_fade(lab, a_voile), (int(cx + fx * rx - lab.width / 2), int(cy + fy * ry - lab.height / 2)))
        d = ImageDraw.Draw(im)
        if t_ is not None and t_ - 0.1 <= u < t_ + s.LAVE + 0.4:                   # l'eau, toujours claire
            a = smooth((u - t_ + 0.1) / 0.2) * (1 - smooth((u - t_ - s.LAVE) / 0.4))
            if eau[0] == "visage":                                                 # l'eau des mains sur le visage
                _, bx, by, bw, bh = eau
                rng = np.random.default_rng(int(u * 12) % 997)
                for _ in range(16):
                    x = bx + bw * float(rng.uniform(0.25, 1.0))
                    y = by + bh * float(rng.uniform(0.25, 0.95))
                    d.rectangle([x, y, x + K, y + 2 * K], fill=(210, 240, 255, int(235 * a)))
                for j, fx in enumerate((0.55, 0.7, 0.85)):                         # trois rigoles qui coulent
                    x = bx + bw * fx
                    off = (u * 500 + j * 60) % (14 * K)
                    yy = by + bh * 0.3 + off
                    while yy < by + bh:
                        d.rectangle([x, yy, x + K, yy + 5 * K], fill=(190, 232, 255, int(200 * a)))
                        yy += 14 * K
            else:
                _, sx, sy, y_fin, xa, xb, yb = eau
                x0, x1 = sx - 2.5 * K, sx + 2.5 * K                                # le filet du robinet
                d.rectangle([x0, sy, x1, y_fin], fill=(*GLACE, int(215 * a)))
                off = (u * 800) % (12 * K)
                yy = sy - 12 * K + off
                while yy < y_fin:
                    d.rectangle([x0 + K, yy, x0 + 2 * K, min(y_fin, yy + 4 * K)], fill=(255, 255, 255, int(230 * a)))
                    yy += 12 * K
                etale = smooth((u - t_) / 0.6)                                     # l'eau s'étale : jusqu'au coude /
                xg = xb - (xb - xa) * etale                                        # jusqu'au talon
                d.rectangle([xg, yb - 2 * K, xb, yb], fill=(190, 232, 255, int(170 * a)))
                off = (u * 300) % (10 * K)
                xx = xb - off
                while xx > xg:
                    d.rectangle([xx - 3 * K, yb - 2 * K, xx, yb - K], fill=(255, 255, 255, int(200 * a)))
                    xx -= 10 * K
                if etale > 0.95:                                                   # elle goutte au bout
                    v_ = ((u - t_) * 2.2) % 1.0
                    d.rectangle([xa - K, yb + v_ * 14 * K, xa + K, yb + v_ * 14 * K + 2 * K], fill=(190, 232, 255, int(220 * a)))
        if t_ is not None and t_ + 0.3 <= u < t_ + 1.6:                           # le voile part en lumière
            v = (u - t_ - 0.3) / 1.3
            rng = np.random.default_rng(int(u * 10) % 997 + 7)
            al = int(240 * math.sin(math.pi * min(1.0, v)))
            for _ in range(10):
                x = cx + float(rng.uniform(-1, 1)) * rx
                y = cy + float(rng.uniform(-1, 1)) * ry - v * 30 * K
                d.rectangle([x - K, y - K, x + K, y + K], fill=(255, 250, 210, al))
        if propre:                                                                # la partie lavée brille
            v = u - (t_ + s.LAVE * 0.8)
            al = int(230 * smooth(v / 0.3) * (1 - smooth((v - 1.2) / 0.5)))
            if al > 0:
                _brille(d, np.random.default_rng(int(u * 6) + len(partie)),
                        (int(cx - rx), int(cy - ry), int(cx + rx), int(cy + ry)), 4, K, al)
        return im

    def image(s, u):
        cur, prev, f = s._partie(u)
        im = s._calque(cur, u)
        if prev is not None and f < 1:
            im = Image.blend(s._calque(prev, u), im, f)
        H0 = s.HAUT
        out = Image.new("RGBA", (im.width, im.height + H0), (0, 0, 0, 0))
        out.alpha_composite(im, (0, H0))
        for p_, a in ((cur, f), (prev, 1 - f)):
            if p_ is None or a <= 0.01:
                continue
            lg = s._cache.setdefault(("l", p_), _titres(s.LEGENDES[p_], JAUNE, 76))
            out.alpha_composite(_fade(lg, a), (int(out.width / 2 - lg.width / 2), int(50 + (H0 - 50) / 2 - lg.height / 2)))
        return out


# ---------------------------------------------------------------- la chambre de nuit (cauchemar, gestes)
LIT_Y = 118                       # haut du matelas (en pixels du dessin, x6 à l'écran)
HANCHE_SPR = (22, 77)             # les hanches dans le dessin du perso assis (pivot pour se coucher / se redresser)
K_PERSO = 8                       # échelle du perso dans la chambre


def _chambre_nuit(W, H, lit_y=LIT_Y):
    c = Px(W, H, alpha=True)
    tout_ = c.mask_rrect(0, 0, W, H, 6)
    c.vgrad(tout_, 0, H, (40, 42, 92), (24, 24, 58), steps=5)
    fen = c.mask_rrect(104, 8, 156, 60, 3)                                          # la fenêtre, la lune, les étoiles
    c.shape(fen, (34, 40, 96), shade=(26, 30, 76), light=(60, 70, 140), band=1, olcol=OL)
    vitre = c.mask_rect(108, 12, 152, 56)
    c.vgrad(vitre, 12, 56, (20, 28, 74), (44, 52, 120), steps=4)
    c.fill(c.mask_ell(140, 24, 7, 7) & ~c.mask_ell(137, 22, 6, 6), (250, 236, 170))
    for (x, y) in ((114, 18), (124, 32), (148, 44), (118, 48), (132, 16)):
        c.px(x, y, (255, 255, 230))
    c.fill(c.mask_rect(129, 12, 131, 56) | c.mask_rect(108, 33, 152, 35), (34, 40, 96))
    for x0 in (98, 152):                                                            # rideaux
        rid = c.mask_rect(x0, 4, x0 + 8, 68)
        c.shape(rid, (92, 56, 120), shade=(66, 38, 92), light=(120, 80, 150), band=1, olcol=OL)
    rayon = c.mask_poly([(108, 56), (152, 56), (168, lit_y), (76, lit_y)]) & tout_  # clair de lune
    c.tint(rayon, (180, 190, 255), 0.12)
    tete = c.mask_rrect(2, lit_y - 40, 16, lit_y + 18, 4)                            # le lit
    c.shape(tete, (120, 80, 56), shade=(90, 58, 40), light=(150, 104, 72), band=2, olcol=OL)
    mat = c.mask_rect(6, lit_y, 166, lit_y + 10)
    c.shape(mat, (220, 222, 236), shade=(176, 180, 204), light=(255, 255, 255), band=1, olcol=OL)
    cadre = c.mask_rect(4, lit_y + 10, 168, lit_y + 20)
    c.shape(cadre, (120, 80, 56), shade=(90, 58, 40), light=(150, 104, 72), band=1, olcol=OL)
    sol = c.mask_rect(0, lit_y + 20, W, H) & tout_
    c.fill(sol, (52, 44, 80))
    oreiller = c.mask_rrect(10, lit_y - 11, 52, lit_y + 2, 5)
    c.shape(oreiller, (236, 238, 248), shade=(190, 196, 222), light=(255, 255, 255), band=1, olcol=OL)
    return c


def _couverture_nuit(W, H, lit_y, x0, haut, long_=70):
    """La couverture bleue à étoiles, de x0 au pied du lit ; haut = hauteur de la bosse (le corps) au-dessus du
    matelas, sur long_ pixels ; les jambes, plus bas, jusqu'au pied du lit."""
    c = Px(W, H, alpha=True)
    jambes = max(6, min(haut, 12))
    pts = [(x0, lit_y + 12), (x0 + 1, lit_y - haut + 6), (x0 + 6, lit_y - haut + 1), (x0 + 14, lit_y - haut)]
    for i in range(1, 6):                                                           # le haut de la bosse, arrondi
        x = x0 + 14 + (long_ - 14) * i / 5
        pts.append((x, lit_y - haut + (haut - jambes) * (i / 5) ** 2))
    pts += [(150, lit_y - jambes + 1), (164, lit_y - jambes + 3), (167, lit_y + 12)]
    m = c.mask_poly(pts)
    c.shape(m, (60, 96, 190), shade=(42, 70, 150), light=(96, 134, 220), band=2, olcol=OL)
    for (x, y) in ((x0 + 14, lit_y - haut + 8), (x0 + 36, lit_y - haut // 2), (x0 + 60, lit_y - 2), (120, lit_y + 4),
                   (146, lit_y - 2)):
        c.fill(c.mask_rect(x, y, x + 2, y + 2) & _erode(m, 1), (230, 220, 120))
    c.fill(c.mask_poly([(x0 + 1, lit_y - haut + 6), (x0 + 6, lit_y - haut + 1), (x0 + 9, lit_y - haut + 4),
                        (x0 + 3, lit_y - haut + 9)]) & m, (230, 232, 244))        # le drap replié
    return c


def _perso_lit(who, face, back=False, sweat=False):
    sp = _sprite(who, "neutre", face, assis=True, back=back, sweat=sweat)
    return _grand(sp.crop((0, 0, sp.width, 80)), K_PERSO)


def _place_lit(im, corps, angle, hanches):
    """Colle le perso (assis = 0°, couché tête à gauche = 90°) avec ses hanches en `hanches` (pixels d'écran) ;
    renvoie la position du centre de sa tête."""
    piv = (HANCHE_SPR[0] * K_PERSO, HANCHE_SPR[1] * K_PERSO)
    rot, (dx, dy) = _tourne(corps, angle, piv)
    im.alpha_composite(rot, (int(hanches[0] - dx), int(hanches[1] - dy)))
    a = math.radians(angle)
    hx, hy = 0.0 * K_PERSO, -32 * K_PERSO                                         # la tête : 32 rangées au-dessus
    return (hanches[0] + hx * math.cos(a) + hy * math.sin(a), hanches[1] - hx * math.sin(a) + hy * math.cos(a))


# ---------------------------------------------------------------- {cauchemar PETIT}
class Cauchemar(Element):
    """{cauchemar PETIT} : la nuit, Petit dort ; au-dessus de lui, une bulle de cauchemar sombre (il tombe dans le vide).
    Sur le mot, il se redresse d'un mouvement doux (0,35 s), les yeux grands ouverts, en sueur ; la bulle s'efface."""
    plein = True
    negatif = True
    K = 6
    PW_, PH_ = 170, 150
    T_REVEIL = 0.0
    HANCHES = (64 * 6, LIT_Y * 6 + 6)

    def __init__(s, cmd, who="PETIT"):
        super().__init__(cmd)
        s.who = who if who in cast.CAST else "PETIT"
        s._cache = {}

    def sons_el(s):
        return [(s.T_REVEIL, "tr_whoosh_doux", 0.04, None)]

    def _bulle(s, u):
        """La bulle du cauchemar : nuée violette, Petit qui tombe dans le vide (il tourne lentement), traits de vitesse."""
        W, H = 78, 56
        if "nue" not in s._cache:
            c = Px(W, H, alpha=True)
            nue = np.zeros((H, W), bool)
            for (x, y, r) in ((20, 24, 17), (40, 17, 19), (60, 24, 16), (30, 38, 17), (52, 38, 16), (13, 34, 11), (66, 36, 10)):
                nue |= c.mask_ell(x, y, r, r * 0.8)
            c.fill(nue, (34, 18, 52))
            c.fill(nue & ~_erode(nue, 2), (110, 70, 150))
            c.outline(nue, OL)
            dedans = _erode(nue, 3)
            c.vgrad(dedans, 4, 52, (14, 8, 26), (60, 26, 70), steps=4)
            s._cache["nue"] = c.img(s.K, rgba=True)
        im = s._cache["nue"].copy()
        d = ImageDraw.Draw(im)
        for j in range(6):                                                          # traits de chute (vers le haut)
            x = (18 + 9 * j) * s.K
            y = ((u * 260 + j * 37) % (40 * s.K)) + 6 * s.K
            d.line([(x, y), (x, y + 8 * s.K)], fill=(180, 150, 220, 160), width=s.K)
        if "chute" not in s._cache:
            s._cache["chute"] = _grand(_sprite(s.who, "panique", "peur"), 3)
        sp = s._cache["chute"].rotate(18 * math.sin(u * 2.2), resample=Image.NEAREST, expand=True)
        im.alpha_composite(sp, (int(im.width / 2 - sp.width / 2), int(im.height / 2 - sp.height / 2 + 6 * math.sin(u * 3))))
        return im

    def image(s, u):
        K = s.K
        if "f" not in s._cache:
            s._cache["f"] = _chambre_nuit(s.PW_, s.PH_).img(K, rgba=True)
        im = s._cache["f"].copy()
        v = u - s.T_REVEIL
        e = smooth(v / 0.35) if v > 0 else 0.0                                     # 0 = couché, 1 = assis
        face = "dodo" if v < 0.05 else "peur"
        key = ("c", face)
        if key not in s._cache:
            s._cache[key] = _perso_lit(s.who, face, sweat=face != "dodo")
        tete = _place_lit(im, s._cache[key], 90 * (1 - e), (s.HANCHES[0], s.HANCHES[1] - 50 * (1 - e)))
        n_ = int(round(e * 6))                                                    # couché : couverture haute
        cle = ("couv", n_)
        if cle not in s._cache:
            s._cache[cle] = _couverture_nuit(s.PW_, s.PH_, LIT_Y, int(36 + 14 * n_ / 6), int(30 - 18 * n_ / 6)
                                             ).img(K, rgba=True)
        im.alpha_composite(s._cache[cle])
        ab = 1.0 if v < 0.15 else 1 - smooth((v - 0.15) / 0.8)                     # la bulle du cauchemar
        if ab > 0.01:
            b = s._bulle(u)
            im.alpha_composite(_fade(b, ab), (int(30 * K), int(4 * K)))
            d = ImageDraw.Draw(im)
            for j, (x, y, r) in enumerate(((36, 74, 5), (30, 86, 4), (24, 96, 3))):  # petites bulles vers sa tête
                d.ellipse([(x - r) * K, (y - r) * K, (x + r) * K, (y + r) * K], fill=(34, 18, 52, int(255 * ab)),
                          outline=(110, 70, 150, int(255 * ab)), width=K)
        if v >= 0.12:                                                              # « ! » au réveil
            ex = s._cache.setdefault("ex", _titre("!", (255, 220, 90), 170, r=5))
            a = smooth((v - 0.12) / 0.2) * (1 - smooth((v - 1.6) / 0.4))
            im.alpha_composite(_fade(ex, a), (int(tete[0] + 22 * K), int(tete[1] - 34 * K)))
        return im


# ---------------------------------------------------------------- {gestes PETIT} …
class Gestes(Element):
    """{gestes PETIT} : Petit assis dans son lit la nuit, vu de dos (sa gauche = la gauche de l'écran). Sur les mots :
    {gestes souffle} trois petits souffles à sa gauche « 1, 2, 3 » ; {gestes refuge} bulle « A'OUDHOU BILLAHI MINA
    CH-CHAYTANI R-RAJIM » ×3 ; {gestes tourne} il se recouche sur le côté ; {gestes chut} « À PERSONNE » ;
    {gestes protege} une lumière douce l'entoure : « IL NE TE FERA AUCUN MAL » (Mouslim 2261 · 2262, Boukhari 7044)."""
    plein = True
    K = 6
    PW_, PH_ = 170, 150
    ETAPES = ("souffle", "refuge", "tourne", "chut", "protege")
    LEGENDES = {"souffle": "1. SOUFFLE 3 FOIS À GAUCHE", "refuge": "2. DEMANDE LA PROTECTION D'ALLAH",
                "tourne": "3. CHANGE DE CÔTÉ", "chut": "4. NE RACONTE PAS LE RÊVE", "protege": "IL NE TE FERA AUCUN MAL"}
    HANCHES = (78 * 6, LIT_Y * 6 + 6)
    HAUT = 170

    def __init__(s, cmd, who="PETIT"):
        super().__init__(cmd)
        s.who = who if who in cast.CAST else "PETIT"
        s.t = {}
        s._cache = {}

    def sons_el(s):
        out = []
        if "souffle" in s.t:
            out += [(s.t["souffle"] + i * 0.45, "tr_whoosh_doux", 0.025, None) for i in range(3)]
        if "tourne" in s.t:
            out.append((s.t["tourne"], "tr_whoosh_doux", 0.03, None))
        if "protege" in s.t:
            out.append((s.t["protege"], "sa_scintillement", 0.05, None))
        return out

    def _bulle_refuge(s):
        if "bulle" not in s._cache:
            tx = pxv.big_title([("A'OUDHOU BILLAHI", BLANC), ("MINA CH-CHAYTAN", BLANC), ("WA MIN CHARRIHA", BLANC)], size=46)
            pad = 26
            b = Image.new("RGBA", (tx.width + 2 * pad, tx.height + 2 * pad), (0, 0, 0, 0))
            ImageDraw.Draw(b).rounded_rectangle([0, 0, b.width - 1, b.height - 1], 28, fill=(40, 60, 120, 240),
                                                outline=(255, 255, 255, 255), width=6)
            b.alpha_composite(tx, (pad, pad))
            x3 = _titre("×3", JAUNE, 96, r=4)
            out_b = Image.new("RGBA", (b.width + x3.width - 30, b.height + 40), (0, 0, 0, 0))
            out_b.alpha_composite(b, (0, 40))
            out_b.alpha_composite(x3, (b.width - 50, 0))
            s._cache["bulle"] = out_b
        return s._cache["bulle"]

    def _chut(s):
        if "chut" not in s._cache:
            bu = objets.icone("bulle").img(10)
            it = objets.icone("interdit").img(10)
            z = Image.new("RGBA", (max(bu.width, it.width), max(bu.height, it.height)), (0, 0, 0, 0))
            z.alpha_composite(bu, ((z.width - bu.width) // 2, (z.height - bu.height) // 2))
            z.alpha_composite(it, ((z.width - it.width) // 2, (z.height - it.height) // 2))
            s._cache["chut"] = autocollant(z, r=5)
        return s._cache["chut"]

    def image(s, u):
        K = s.K
        if "f" not in s._cache:
            s._cache["f"] = _chambre_nuit(s.PW_, s.PH_).img(K, rgba=True)
        im = s._cache["f"].copy()
        W_, H_ = im.size
        t_tourne = s.t.get("tourne")
        e = smooth((u - t_tourne) / 0.7) if t_tourne is not None and u >= t_tourne else 0.0
        if "dos" not in s._cache:
            s._cache["dos"] = _perso_lit(s.who, "neutre", back=True)
        if "protege" in s.t and u >= s.t["protege"] - 0.1:                         # la lumière douce autour de lui
            v = u - s.t["protege"] + 0.1
            a = smooth(v / 0.6)
            halo = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
            hd = ImageDraw.Draw(halo)
            hx_, hy_ = 64 * K, (LIT_Y - 4) * K
            for j, rr in enumerate((72, 56, 40)):
                hd.ellipse([hx_ - rr * K * 1.3, hy_ - rr * K * 0.75, hx_ + rr * K * 1.3, hy_ + rr * K * 0.45],
                           fill=(255, 226, 150, int((24 + 22 * j) * a)))
            im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(16)))
        tete = _place_lit(im, s._cache["dos"], 90 * e, (s.HANCHES[0], s.HANCHES[1] - 50 * e))
        n_ = int(round(e * 6))                                                    # assis : jusqu'à la taille
        cle = ("couv", n_)
        if cle not in s._cache:
            s._cache[cle] = _couverture_nuit(s.PW_, s.PH_, LIT_Y, int(58 - 8 * n_ / 6), int(12 + 18 * n_ / 6)
                                             ).img(K, rgba=True)
        im.alpha_composite(s._cache[cle])
        d = ImageDraw.Draw(im)
        if "souffle" in s.t:                                                       # 3 petits souffles à sa gauche
            for i in range(3):
                t0 = s.t["souffle"] + i * 0.45
                v = u - t0
                if v < 0:
                    continue
                if v < 0.9:
                    a = smooth(v / 0.12) * (1 - smooth((v - 0.5) / 0.4))
                    x = tete[0] - 13 * K - 30 * K * smooth(v / 0.8)
                    y = tete[1] + 4 * K
                    for j, r in enumerate((5, 4, 3)):
                        rr = r * K * (0.6 + 0.6 * smooth(v / 0.5))
                        xx = x - j * 6 * K
                        d.ellipse([xx - rr, y - rr * 0.7, xx + rr, y + rr * 0.7], fill=(235, 240, 255, int(210 * a)))
                fin_ = s.t.get("refuge", 1e9)
                if u < fin_ + 0.3:                                                  # le numéro reste jusqu'à l'étape 2
                    n_ = s._cache.setdefault(("n", i), _titre(str(i + 1), JAUNE, 100, r=4))
                    a2 = smooth(v / 0.2) * (1 - smooth((u - fin_) / 0.3))
                    im.alpha_composite(_fade(n_, a2), (int(tete[0] - 70 * K + 20 * K * i - n_.width / 2),
                                                       int(tete[1] - 22 * K - n_.height / 2)))
        if "refuge" in s.t:                                                        # « A'OUDHOU BILLAH… » ×3
            v = u - s.t["refuge"]
            fin_ = s.t.get("tourne", 1e9)
            if 0 <= v and u < fin_ + 0.3:
                a = smooth(v / 0.3) * (1 - smooth((u - fin_) / 0.3))
                b = s._bulle_refuge()
                im.alpha_composite(_fade(b, a), (int(max(10, min(W_ - b.width - 10, tete[0] - b.width * 0.6))),
                                                 int(max(8, tete[1] - 30 * K - b.height) + 10 * (1 - smooth(v / 0.3)))))
        if t_tourne is not None and t_tourne <= u < t_tourne + 1.6:                # la flèche qui tourne
            v = u - t_tourne
            a = smooth(v / 0.2) * (1 - smooth((v - 1.2) / 0.4))
            r_ = 30 * K
            ccx, ccy = s.HANCHES[0] - 14 * K, s.HANCHES[1] - 30 * K
            deb, fin_ang = 330, 330 - 150 * smooth(v / 0.7)
            box = [ccx - r_, ccy - r_ * 0.7, ccx + r_, ccy + r_ * 0.7]
            d.arc(box, fin_ang, deb, fill=(20, 16, 30, int(255 * a)), width=4 * K)
            d.arc(box, fin_ang, deb, fill=(255, 214, 70, int(255 * a)), width=2 * K)
            ang = math.radians(fin_ang)
            px_, py_ = ccx + r_ * math.cos(ang), ccy + r_ * 0.7 * math.sin(ang)
            d.polygon([(px_ - 6 * K, py_ - 1 * K), (px_ + 2 * K, py_ - 6 * K), (px_ + 3 * K, py_ + 4 * K)],
                      fill=(255, 214, 70, int(255 * a)), outline=(20, 16, 30, int(255 * a)))
        if "chut" in s.t:                                                          # « À PERSONNE » : bulle barrée
            v = u - s.t["chut"]
            fin_ = s.t.get("protege", 1e9) + 0.6
            if v >= 0 and u < fin_ + 0.3:
                a = smooth(v / 0.3) * (1 - smooth((u - fin_) / 0.3))
                ch = s._chut()
                im.alpha_composite(_fade(ch, a), (int(tete[0] - ch.width / 2 + 4 * K), int(tete[1] - 42 * K - ch.height / 2)))
        if "protege" in s.t and u >= s.t["protege"]:                               # « zzz » paisibles
            v = u - s.t["protege"]
            for j in range(3):
                vv = ((v + j * 0.5) % 1.5) / 1.5
                z_ = s._cache.setdefault(("z", j), _titre("z", (200, 210, 255), 60 + 14 * j, r=3))
                a = smooth(vv / 0.2) * (1 - smooth((vv - 0.7) / 0.3)) * smooth(v / 0.4)
                im.alpha_composite(_fade(z_, a), (int(tete[0] + 20 * K + j * 9 * K), int(tete[1] - 12 * K - vv * 26 * K - j * 6 * K)))
        H0 = s.HAUT
        out = Image.new("RGBA", (im.width, im.height + H0), (0, 0, 0, 0))
        out.alpha_composite(im, (0, H0))
        evts = sorted((t_, p_) for p_, t_ in s.t.items() if u >= t_)                 # la légende de l'étape
        if evts:
            t_, p_ = evts[-1]
            col = JAUNE if p_ == "protege" else BLANC
            lg = s._cache.setdefault(("l", p_), _titre(s.LEGENDES[p_], col, 62 if p_ != "protege" else 68))
            if p_ == "protege":
                st = s._cache.setdefault("ok", autocollant(objets.icone("check").img(5), r=4))
                comb = Image.new("RGBA", (lg.width + st.width - 16, max(lg.height, st.height)), (0, 0, 0, 0))
                comb.alpha_composite(lg, (0, (comb.height - lg.height) // 2))
                comb.alpha_composite(st, (lg.width - 16, (comb.height - st.height) // 2))
                lg = comb
            if lg.width > out.width - 20:
                k_ = (out.width - 20) / lg.width
                lg = lg.resize((int(lg.width * k_), int(lg.height * k_)), Image.LANCZOS)
            a = smooth((u - t_) / 0.3)
            out.alpha_composite(_fade(lg, a), (int(out.width / 2 - lg.width / 2), int(50 + (H0 - 50) / 2 - lg.height / 2)))
        return out


# ---------------------------------------------------------------- branchement dans explique.Schema
CLES = ("fievre", "fièvre", "forge", "soufflet", "glace", "ablutions", "cauchemar", "gestes")


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique.Schema._ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
    import re
    k = mots[0].lower()
    sous = mots[1].lower() if len(mots) > 1 else ""

    def dernier(cls):
        return next((it["el"] for it in reversed(schema._visibles(t + 0.01)) if isinstance(it["el"], cls)), None)

    def u_de(el):
        return t - next(it["t_in"] for it in schema.items if it["el"] is el)

    if k in ("fievre", "fièvre"):
        schema._ajoute(t, Fievre(brut, mots[1].upper() if len(mots) > 1 else "PETIT"))
    elif k == "forge":
        m_ = re.search(r'"(.+)"', reste)
        schema._ajoute(t, Forge(brut, m_.group(1).upper() if m_ else "TES PETITS PÉCHÉS"))
    elif k == "soufflet":
        fo = dernier(Forge)
        if fo is not None:
            fo.t_souffle = u_de(fo)
    elif k == "glace":
        schema._ajoute(t, Glace(brut))
    elif k == "ablutions":
        ab = dernier(Ablutions)
        if sous in Ablutions.PARTIES:
            if ab is None:
                ab = Ablutions(brut, "PETIT")
                schema._ajoute(t, ab)
            ab.t[sous] = u_de(ab)
        else:
            schema._ajoute(t, Ablutions(brut, mots[1].upper() if len(mots) > 1 else "PETIT"))
    elif k == "cauchemar":
        schema._ajoute(t, Cauchemar(brut, mots[1].upper() if len(mots) > 1 else "PETIT"))
    elif k == "gestes":
        ge = dernier(Gestes)
        if sous in Gestes.ETAPES:
            if ge is None:
                ge = Gestes(brut, "PETIT")
                schema._ajoute(t, ge)
            ge.t[sous] = u_de(ge)
        else:
            schema._ajoute(t, Gestes(brut, mots[1].upper() if len(mots) > 1 else "PETIT"))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = pas d'animation à attendre."""
    k = mots[0].lower()
    sous = mots[1].lower() if len(mots) > 1 else ""
    if k == "soufflet":
        return t + 0.15 + 7 * Forge.DT + Forge.VOL + 1.0
    if k == "ablutions" and sous in Ablutions.PARTIES:
        return t + Ablutions.LAVE + (0.9 if sous == "pieds" else 0.2)
    if k == "gestes" and sous:
        return t + (2.0 if sous == "protege" else 1.3)
    if k in ("fievre", "fièvre", "glace"):
        return t + 1.6
    if k == "cauchemar":
        return t + 1.8
    return None
