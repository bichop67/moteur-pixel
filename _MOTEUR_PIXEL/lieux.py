# NOUVEAUX DÉCORS pixel art (270x480 pixels, agrandis x4), pour toutes les chaînes. Même style que sets.py.
# Chaque décor renvoie (fond RGB, avant-plan RGBA ou None) ; beaucoup existent en version jour / soir / nuit.
# Ils s'ajoutent automatiquement à sets.DECORS : Shot(t0, t1, "rue_nuit", ...) marche comme "salon".
# SPOTS[nom] = placements conseillés des personnages (x, y des pieds en pixels écran 1080x1920, échelle, réglages).
import math, random
import numpy as np
from px import Px, OUT, INK, BAYER, TAHOMA
from px import Px as _PxBase
import sets
from sets import books, planks, star_light, lantern, chandelier

R = random.Random


def dk(c, k=0.72):
    return tuple(int(v * k) for v in c)


def lt(c, k=0.25):
    return tuple(int(v + (255 - v) * k) for v in c)


def mix(a, b, k):
    return tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))


def pose_calque(img, lay):
    """Pose sur l'image un calque dessiné en petits pixels (agrandi sans lissage). Résultat identique au pixel près à
    img.alpha_composite(lay.resize(img.size, NEAREST)), mais seule la zone réellement dessinée est agrandie et posée
    (11/11/2026 : une animation qui ne touche qu'un coin de l'image coûtait autant qu'une image entière)."""
    from PIL import Image
    k = img.width // max(1, lay.width)
    if k < 1 or (lay.width * k, lay.height * k) != img.size:
        img.alpha_composite(lay.resize(img.size, Image.NEAREST))
        return
    bb = lay.getbbox()
    if bb is None:                                  # rien de dessiné
        return
    if bb != (0, 0, lay.width, lay.height):
        lay = lay.crop(bb)
    img.alpha_composite(lay.resize((lay.width * k, lay.height * k), Image.NEAREST), (bb[0] * k, bb[1] * k))


# =================================================================== ciel, lumière, heures
SKY = dict(jour=((92, 164, 234), (190, 224, 250)), soir=((74, 58, 128), (250, 156, 96)), nuit=((10, 14, 40), (42, 40, 98)))


def nuage(c, x, y, w, col=(250, 250, 252), sh=(206, 218, 238), m=None):
    blob = c.mask_ell(x, y, w * 0.32, w * 0.16) | c.mask_ell(x - w * 0.22, y + w * 0.05, w * 0.22, w * 0.12) | \
        c.mask_ell(x + w * 0.24, y + w * 0.04, w * 0.24, w * 0.12) | c.mask_rect(x - w * 0.42, y + w * 0.04, x + w * 0.46, y + w * 0.15)
    if m is not None:
        blob &= m
    c.fill(blob, col)
    c.fill(blob & c.mask_rect(0, y + w * 0.08, 270, y + w * 0.2), sh)


def ciel(c, m, y0, y1, heure="jour", seed=1, astre=None, nuages=True):
    top, bot = SKY[heure]
    c.vgrad(m, y0, y1, top, bot, steps=7)
    rnd = R(seed)
    ox = getattr(c, "ox", 0)
    if heure == "nuit":
        for _ in range(max(6, int(m.sum() / 240))):
            x, y = rnd.randrange(c.w) - ox, rnd.randrange(max(0, y0), min(c.h, y1))
            if m[y, x + ox]:
                c.px(x, y, (232, 232, 255) if rnd.random() < 0.4 else (150, 150, 210))
        if astre:
            ax, ay = astre
            moon = c.mask_ell(ax, ay, 9, 9) & ~c.mask_ell(ax + 4, ay - 3, 8, 8) & m
            c.fill(moon, (252, 240, 200))
            c.glow(ax, ay, 26, (200, 200, 255), 0.18, m=m)
    elif heure == "soir":
        if astre:
            ax, ay = astre
            c.glow(ax, ay, 60, (255, 200, 120), 0.35, m=m)
            c.fill(c.mask_ell(ax, ay, 11, 11) & m, (255, 222, 150))
        if nuages:
            for k in range(3):
                nuage(c, rnd.randint(20, 250), rnd.randint(y0 + 10, max(y0 + 12, y1 - 30)), rnd.randint(40, 70),
                      (250, 170, 150), (196, 110, 120), m)
    else:
        if astre:
            ax, ay = astre
            c.glow(ax, ay, 40, (255, 250, 210), 0.35, m=m)
            c.fill(c.mask_ell(ax, ay, 9, 9) & m, (255, 246, 196))
        if nuages:
            for k in range(3):
                nuage(c, rnd.randint(10, 260), rnd.randint(y0 + 8, max(y0 + 10, y1 - 30)), rnd.randint(40, 80), m=m)


def intact(c, snap, m):
    """Pixels du masque qui n'ont pas changé depuis la photo snap (= le ciel encore visible)."""
    return m & np.all(c.a == snap, axis=2)


def relief(c, snap, m):
    """Pour le relief (parallaxe) : le ciel lointain devient une couche à part, qui bouge moins vite que la scène."""
    c.lointain = snap.copy()
    c.ciel_m = intact(c, snap, m)
    return c


def teinte(c, heure, m=None, interieur=False):
    """Ambiance de l'heure : le soir chauffe, la nuit bleuit et assombrit (à faire avant d'allumer les lampes).
    interieur=True : nuit chaude (pièce éclairée par des lampes) au lieu du bleu de la rue."""
    if heure == "jour":
        return
    if heure == "soir":
        mul, add = (1.0, 0.84, 0.74), (14, 4, 0)
    elif interieur:
        mul, add = (0.68, 0.60, 0.66), (8, 4, 12)
    else:
        mul, add = (0.46, 0.52, 0.80), (4, 6, 22)
    mul, add = np.array(mul, np.float32), np.array(add, np.float32)
    sel = np.ones((c.h, c.w), bool) if m is None else m
    a = c.a.astype(np.float32)
    a[sel] = np.clip(a[sel] * mul + add, 0, 255)
    c.a = a.astype(np.uint8)


def skyline(c, y_base, heure="jour", seed=3, x0=0, x1=270, hmin=30, hmax=110, m=None, far=False):
    rnd = R(seed)
    ox = getattr(c, "ox", 0)
    if ox and x0 == 0 and x1 == 270:                      # toile élargie (16:9) : la ville continue sur les côtés
        x0, x1 = -ox, 270 + ox
    x = x0 - rnd.randint(0, 10)
    day = [(150, 170, 200), (170, 186, 214), (136, 156, 190)] if not far else [(176, 196, 222), (188, 206, 230)]
    night = [(26, 26, 54), (34, 32, 66), (22, 22, 46)]
    dusk = [(110, 80, 120), (126, 92, 130), (96, 70, 110)]
    pal = dict(jour=day, soir=dusk, nuit=night)[heure]
    while x < x1:
        w = rnd.randint(14, 30); h = rnd.randint(hmin, hmax)
        b = c.mask_rect(x, y_base - h, x + w, y_base)
        if m is not None:
            b &= m
        colr = rnd.choice(pal)
        c.fill(b, colr)
        c.fill(b & c.mask_rect(x, y_base - h, x + 2, y_base), dk(colr, 0.85))
        if rnd.random() < 0.3:                                             # antenne
            c.fill(c.mask_rect(x + w // 2, y_base - h - 6, x + w // 2 + 1, y_base - h) & (m if m is not None else True), colr)
        for yy in range(y_base - h + 4, y_base - 2, 5):
            for xx in range(x + 3, x + w - 2, 4):
                on = rnd.random()
                if heure == "nuit" and on < 0.42:
                    c.px(xx, yy, (250, 214, 110) if on < 0.3 else (200, 170, 100))
                elif heure != "nuit" and on < 0.5:
                    c.px(xx, yy, lt(colr, 0.35) if heure == "jour" else (250, 190, 120))
        x += w + rnd.randint(0, 3)


def sol_carreaux(c, y0, y1, horizon, c1, c2, grout, cell=0.7, cx=135):
    yy, xx = c.yy, c.xx
    floor = c.mask_rect(0, y0, 270, y1)
    c.fill(floor, c1)
    dz = np.maximum(yy - horizon, 1).astype(float); z = 420.0 / dz; xw = (xx - cx) * z / 105.0
    chk = ((np.floor(xw / cell) + np.floor(z / cell)) % 2 == 0) & floor
    c.fill(chk, c2)
    g = ((((xw / cell) - np.floor(xw / cell)) < 0.05) | (((z / cell) - np.floor(z / cell)) < 0.05)) & floor
    c.fill(g, grout)
    return floor


def carrelage_mur(c, m, size, c1, grout, c2=None, seed=1):
    rnd = R(seed)
    c.fill(m, c1)
    if c2 is not None:
        for ty in range(0, c.h, size):
            for tx in range(0, c.w, size):
                if rnd.random() < 0.18:
                    c.fill(m & c.mask_rect(tx, ty, tx + size, ty + size), c2)
    c.fill(m & (((c.xx % size) == 0) | ((c.yy % size) == 0)), grout)


def plante(c, x, y_base, h=30, pot=(186, 96, 60), leaf=(54, 130, 64), seed=9, n=14):
    p = c.mask_poly([(x - 12, y_base - 20), (x + 12, y_base - 20), (x + 9, y_base), (x - 9, y_base)])
    c.shape(p, pot, dk(pot, 0.75), lt(pot, 0.2), band=2)
    rnd = R(seed)
    for _ in range(n):
        a = rnd.uniform(-2.7, -0.45); L = rnd.randint(int(h * 0.5), h)
        x2, y2 = x + math.cos(a) * L, y_base - 20 + math.sin(a) * L
        lf = c.mask_ell((x + x2) / 2, (y_base - 20 + y2) / 2, 3.5, L / 2.2)
        c.shape(lf, leaf, dk(leaf, 0.7), lt(leaf, 0.25), band=1)


def lampadaire(c, x, y_base, h=180, on=False, col=(44, 56, 60)):
    c.shape(c.mask_rect(x - 2, y_base - h, x + 2, y_base), col, dk(col, 0.7), lt(col, 0.3), band=1)
    c.shape(c.mask_rect(x - 4, y_base - 8, x + 4, y_base), col, dk(col, 0.7), band=1)
    arm = c.mask_rect(x, y_base - h, x + 16, y_base - h + 3)
    c.shape(arm, col, dk(col, 0.7), band=1)
    head = c.mask_poly([(x + 10, y_base - h + 2), (x + 26, y_base - h + 2), (x + 23, y_base - h + 8), (x + 13, y_base - h + 8)])
    c.shape(head, col, dk(col, 0.7), band=1)
    c.fill(c.mask_rect(x + 14, y_base - h + 8, x + 23, y_base - h + 10), (255, 236, 170) if on else (200, 204, 196))
    if on:
        c.glow(x + 18, y_base - h + 12, 60, (255, 220, 140), 0.45)
        cone = c.mask_poly([(x + 13, y_base - h + 10), (x + 23, y_base - h + 10), (x + 48, y_base), (x - 12, y_base)])
        c.tint(cone, (255, 226, 150), 0.10)


def arbre(c, cx, y_base, r=26, trunk=40, col=(70, 140, 70), seed=5, m=None):
    tr = c.mask_rect(cx - 4, y_base - trunk, cx + 4, y_base)
    c.shape(tr, (110, 76, 50), (78, 52, 34), (140, 100, 66), band=2)
    rnd = R(seed)
    cy = y_base - trunk - r * 0.6
    canopy = np.zeros((c.h, c.w), bool)
    for _ in range(9):
        canopy |= c.mask_ell(cx + rnd.uniform(-r * 0.6, r * 0.6), cy + rnd.uniform(-r * 0.5, r * 0.4),
                             r * rnd.uniform(0.45, 0.65), r * rnd.uniform(0.4, 0.55))
    if m is not None:
        canopy &= m
    c.fill(canopy, col)
    c.fill(canopy & c.mask_rect(0, cy + r * 0.2, 270, 480), dk(col, 0.78))
    for _ in range(7):
        hx, hy = cx + rnd.uniform(-r * 0.6, r * 0.3), cy + rnd.uniform(-r * 0.6, 0)
        c.fill(canopy & c.mask_ell(hx, hy, r * 0.22, r * 0.14), lt(col, 0.22))
    c.dither(canopy & c.mask_rect(0, cy + r * 0.05, 270, cy + r * 0.25), dk(col, 0.78), 0.5)
    c.outline(canopy, dk(col, 0.45))


def voiture(c, x, y_base, col=(200, 60, 60), sens=1, phares=False):
    """Voiture vue de côté (environ 96 x 34 pixels), x = centre, y_base = sol."""
    def P(pts):
        return c.mask_poly([(x + sens * px_, y_base - py_) for px_, py_ in pts])
    body = P([(-48, 6), (48, 6), (49, 16), (44, 20), (22, 22), (12, 33), (-24, 33), (-36, 22), (-48, 19)])
    c.shape(body, col, dk(col, 0.7), lt(col, 0.3), band=2, sdir="bottom")
    win = P([(10, 22), (-1, 31), (-22, 31), (-31, 22)])
    c.fill(win, (150, 200, 230)); c.fill(win & P([(-6, 22), (-1, 31), (-4, 31), (-10, 22)]), (220, 240, 252))
    c.fill(P([(-12, 22), (-11, 31), (-13, 31), (-14, 22)]), dk(col, 0.6))
    c.outline(win, dk(col, 0.45))
    c.fill(P([(-30, 13), (-26, 13), (-26, 12), (-30, 12)]), dk(col, 0.5))
    c.fill(P([(4, 13), (8, 13), (8, 12), (4, 12)]), dk(col, 0.5))
    c.fill(P([(44, 15), (48, 15), (48, 11), (44, 11)]), (255, 240, 180) if phares else (240, 236, 210))
    c.fill(P([(-48, 15), (-45, 15), (-45, 11), (-48, 11)]), (220, 40, 40))
    for wx in (-30, 30):
        wc = x + sens * wx
        t = c.mask_ell(wc, y_base - 6, 7, 7)
        c.shape(t, (36, 34, 40), (20, 20, 24), band=1)
        c.shape(c.mask_ell(wc, y_base - 6, 3.4, 3.4), (190, 194, 204), (130, 134, 146), band=1)
    if phares:
        c.glow(x + sens * 50, y_base - 13, 40, (255, 240, 180), 0.35)


def banc(c, x0, x1, y_seat, col=(150, 100, 60), iron=(50, 56, 60)):
    for x in (x0 + 4, x1 - 6):
        c.shape(c.mask_rect(x, y_seat, x + 3, y_seat + 18), iron, dk(iron, 0.7), band=1)
    c.shape(c.mask_rect(x0, y_seat - 3, x1, y_seat + 2), col, dk(col, 0.72), lt(col, 0.25), band=1, sdir="bottom")
    for y in (y_seat - 18, y_seat - 11):
        c.shape(c.mask_rect(x0, y, x1, y + 4), col, dk(col, 0.72), lt(col, 0.25), band=1, sdir="bottom")
    for x in (x0 + 4, x1 - 6):
        c.fill(c.mask_rect(x, y_seat - 20, x + 3, y_seat), iron)


def ecran(c, x0, y0, x1, y1, scr=(40, 120, 200), kind="jeu", seed=1, glow=True):
    c.shape(c.mask_rect(x0, y0, x1, y1), (30, 30, 36), (18, 18, 22), band=1)
    s = c.mask_rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2)
    c.vgrad(s, y0, y1, lt(scr, 0.15), dk(scr, 0.6), steps=4)
    rnd = R(seed)
    if kind == "jeu":
        c.fill(s & c.mask_rect(x0 + 2, y1 - 8, x1 - 2, y1 - 2), (60, 150, 80))
        for k in range(3):
            bx = rnd.randint(x0 + 4, x1 - 8)
            c.fill(c.mask_rect(bx, y1 - 12, bx + 4, y1 - 8), (240, 200, 70))
        c.fill(c.mask_rect(x0 + 6, y1 - 14, x0 + 9, y1 - 8), (230, 60, 70))
    elif kind == "code":
        for yy in range(y0 + 4, y1 - 3, 3):
            w = rnd.randint(4, max(5, x1 - x0 - 8))
            c.fill(c.mask_rect(x0 + 4 + rnd.randint(0, 4), yy, min(x1 - 3, x0 + 4 + w), yy + 1),
                   rnd.choice([(120, 220, 140), (240, 200, 90), (150, 190, 250), (230, 120, 170)]))
    elif kind == "graph":
        pts = [(x0 + 4 + i * (x1 - x0 - 8) / 6, y1 - 6 - rnd.randint(0, y1 - y0 - 12)) for i in range(7)]
        for a, b in zip(pts, pts[1:]):
            c.line(a[0], a[1], b[0], b[1], (120, 240, 160))
    elif kind == "carte":
        for _ in range(5):
            c.fill(c.mask_ell(rnd.randint(x0 + 6, x1 - 6), rnd.randint(y0 + 5, y1 - 5), rnd.randint(3, 8), rnd.randint(2, 5)) & s, (90, 190, 120))
    if glow:
        c.glow((x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0) * 1.1, scr, 0.18)


def produits(c, x0, x1, y_base, h=14, seed=1, pal=None, magasin=False):
    """Rangée de produits sur une étagère. magasin=True : rayon de supermarché (paquets larges, conserves, pots,
    bouteilles, groupés par 3 à 5 identiques comme en vrai)."""
    rnd = R(seed)
    pal = pal or [(220, 60, 60), (240, 200, 70), (60, 150, 220), (90, 180, 90), (240, 140, 60), (250, 250, 250), (160, 80, 170)]
    x = x0
    if not magasin:
        while x < x1 - 4:
            kind = rnd.random()
            colr = rnd.choice(pal)
            if kind < 0.4:                                              # boîte
                w = rnd.randint(6, 9); hh = rnd.randint(h - 4, h)
                m = c.mask_rect(x, y_base - hh, x + w, y_base)
                c.shape(m, colr, dk(colr, 0.75), lt(colr, 0.3), band=1)
                c.fill(c.mask_rect(x + 1, y_base - hh + 3, x + w - 1, y_base - hh + 5), (250, 250, 250))
            elif kind < 0.75:                                           # bouteille
                w = 5; hh = rnd.randint(h - 2, h + 3)
                m = c.mask_rect(x, y_base - hh + 4, x + w, y_base) | c.mask_rect(x + 1, y_base - hh, x + w - 1, y_base - hh + 4)
                c.shape(m, colr, dk(colr, 0.75), lt(colr, 0.35), band=1)
                c.fill(c.mask_rect(x + 1, y_base - hh + 7, x + w - 1, y_base - hh + 10), (250, 246, 230))
            else:                                                       # canette
                w = 4; hh = 7
                m = c.mask_rect(x, y_base - hh, x + w, y_base)
                c.shape(m, colr, dk(colr, 0.75), lt(colr, 0.4), band=1)
            x += w + 1
        return
    while x < x1 - 8:
        kind = rnd.choice(["paquet", "paquet", "conserve", "bocal", "bouteille", "brique"])
        colr = rnd.choice(pal)
        n = rnd.randint(2, 4)
        for _ in range(n):
            if x > x1 - 8:
                break
            if kind == "paquet":                                        # céréales, biscuits : large, logo rond
                w, hh = 11, h
                m = c.mask_rect(x, y_base - hh, x + w, y_base)
                c.shape(m, colr, dk(colr, 0.72), lt(colr, 0.3), band=1)
                c.fill(c.mask_ell(x + 5.5, y_base - hh * 0.55, 3.2, 3.2), (252, 248, 236))
                c.fill(c.mask_rect(x + 2, y_base - hh + 2, x + w - 2, y_base - hh + 4), lt(colr, 0.5))
            elif kind == "conserve":                                    # boîtes de conserve empilées
                w, hh = 8, 8
                for j in range(2):
                    m = c.mask_rect(x, y_base - hh * (j + 1), x + w, y_base - hh * j)
                    c.shape(m, (196, 200, 210), (150, 154, 166), band=1)
                    c.fill(c.mask_rect(x, y_base - hh * (j + 1) + 2, x + w, y_base - hh * j - 2), colr)
            elif kind == "bocal":
                w, hh = 8, 12
                m = c.mask_rect(x, y_base - hh + 3, x + w, y_base) | c.mask_rect(x + 1, y_base - hh, x + w - 1, y_base - hh + 3)
                c.shape(m, (226, 160, 60) if colr != (250, 250, 250) else (230, 210, 170), (180, 110, 40), band=1)
                c.fill(c.mask_rect(x + 1, y_base - hh, x + w - 1, y_base - hh + 2), colr)
                c.fill(c.mask_rect(x + 1, y_base - hh + 5, x + w - 1, y_base - hh + 8), (252, 248, 236))
            elif kind == "bouteille":
                w, hh = 6, h + 2
                m = c.mask_rect(x, y_base - hh + 6, x + w, y_base) | c.mask_rect(x + 2, y_base - hh, x + w - 2, y_base - hh + 6)
                c.shape(m, colr, dk(colr, 0.75), lt(colr, 0.35), band=1)
                c.fill(c.mask_rect(x + 1, y_base - hh + 10, x + w - 1, y_base - hh + 14), (250, 246, 230))
            else:                                                       # brique de lait / jus
                w, hh = 7, h - 4
                m = c.mask_rect(x, y_base - hh, x + w, y_base) | c.mask_poly([(x, y_base - hh), (x + w, y_base - hh), (x + w // 2, y_base - hh - 3)])
                c.shape(m, (250, 250, 248), (210, 210, 214), band=1)
                c.fill(c.mask_rect(x, y_base - hh + 4, x + w, y_base - 3), colr)
            x += w + 1
        x += 2


def neon_texte(c, xy, txt, col, size=9, glow=True):
    m = c.text(xy, txt, lt(col, 0.55), size=size, anchor="ma", ol=col)
    if glow:
        ys, xs = np.where(m)
        if len(xs):
            c.glow(xs.mean(), ys.mean(), max(14, (xs.max() - xs.min()) * 0.75), col, 0.28)


# =================================================================== CUISINE
def cuisine(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 320)
    c.vgrad(wall, 0, 320, (234, 218, 186), (248, 236, 210), steps=6)
    c.shape(c.mask_rect(0, 0, 270, 8), (214, 196, 166), (186, 168, 140), band=2, sdir="bottom")
    # fenêtre au-dessus de l'évier
    win = c.mask_rect(160, 52, 246, 148)
    ciel(c, win, 52, 148, heure, seed=4, astre=(228, 76))
    arbre(c, 182, 160, r=24, trunk=30, col=(76, 150, 80) if heure != "nuit" else (40, 70, 60), seed=3, m=win)
    snap = c.a.copy()
    c.shape(c.mask_rect(154, 46, 252, 52), (250, 250, 250), (210, 210, 216), band=1)
    c.shape(c.mask_rect(154, 46, 160, 154), (250, 250, 250), (210, 210, 216), band=1)
    c.shape(c.mask_rect(246, 46, 252, 154), (250, 250, 250), (210, 210, 216), band=1)
    c.fill(c.mask_rect(202, 52, 204, 148), (246, 246, 248)); c.fill(c.mask_rect(160, 99, 246, 101), (246, 246, 248))
    c.shape(c.mask_rect(150, 148, 256, 155), (240, 240, 244), (200, 200, 206), band=1, sdir="bottom")
    cur = c.mask_rect(160, 106, 246, 128)                                 # rideau bistrot
    c.fill(cur, (246, 246, 246))
    c.fill(cur & ((((c.xx // 3) + (c.yy // 3)) % 2) == 0), (210, 60, 60))
    for x in range(160, 246, 6):
        c.fill(c.mask_ell(x + 3, 128, 3, 2), (246, 246, 246))
    c.fill(c.mask_rect(158, 104, 248, 106), (180, 140, 90))
    for px_ in (172, 232):                                               # pots d'herbes aromatiques
        p = c.mask_poly([(px_ - 6, 148), (px_ + 6, 148), (px_ + 5, 138), (px_ - 5, 138)])
        c.shape(p, (196, 104, 66), (150, 74, 44), band=1)
        for k in range(5):
            c.fill(c.mask_ell(px_ - 4 + k * 2, 134 - (k % 2) * 3, 2, 4), (70, 150, 70))
    # placards hauts + hotte
    for x0 in (66, 104):
        d = c.mask_rect(x0, 26, x0 + 36, 112)
        c.shape(d, (196, 150, 104), (156, 112, 74), (220, 180, 132), band=2)
        c.shape(c.mask_rect(x0 + 4, 32, x0 + 32, 106), (206, 162, 116), (170, 126, 86), band=1, ol=False)
        c.fill(c.mask_rect(x0 + 28, 96, x0 + 30, 104), (90, 90, 96))
    hood = c.mask_poly([(68, 122), (138, 122), (132, 112), (74, 112)]) | c.mask_rect(92, 26, 114, 112)
    c.shape(hood, (190, 196, 206), (146, 152, 166), (226, 230, 238), band=2)
    c.fill(c.mask_rect(70, 120, 136, 124), (120, 124, 136))
    # crédence carrelée
    cred = c.mask_rect(62, 124, 270, 232) & ~c.mask_rect(150, 46, 256, 156)
    carrelage_mur(c, cred, 8, (236, 244, 244), (190, 200, 204), c2=(120, 190, 190), seed=6)
    # ustensiles suspendus
    c.fill(c.mask_rect(140, 162, 150, 164), (110, 110, 120))
    for i, (ux, ln) in enumerate(((142, 18), (146, 22), (150, 16))):
        c.fill(c.mask_rect(ux, 164, ux + 1, 164 + ln), (120, 80, 50))
        c.shape(c.mask_ell(ux, 166 + ln, 2.5, 3.5), (170, 176, 188), (120, 126, 140), band=1)
    # frigo
    fr = c.mask_rrect(6, 98, 62, 318, 5)
    c.shape(fr, (236, 238, 242), (196, 200, 210), (250, 251, 253), band=3)
    c.fill(c.mask_rect(8, 170, 60, 172), (176, 180, 192))
    c.fill(c.mask_rect(52, 112, 55, 160), (160, 164, 176)); c.fill(c.mask_rect(52, 182, 55, 240), (160, 164, 176))
    dr = c.mask_rect(14, 112, 38, 140)                                   # dessin d'enfant
    c.fill(dr, (252, 252, 246)); c.outline(dr, (200, 200, 190))
    c.fill(c.mask_ell(26, 132, 7, 4) & dr, (90, 170, 90)); c.fill(c.mask_ell(31, 118, 3, 3), (250, 200, 60))
    c.fill(c.mask_rect(20, 122, 26, 131), (220, 70, 60)); c.fill(c.mask_poly([(18, 123), (28, 123), (23, 117)]), (150, 70, 50))
    for mx_, my_, mc in ((16, 188, (230, 60, 60)), (30, 200, (60, 140, 230)), (22, 214, (250, 200, 60)), (40, 194, (90, 190, 90))):
        c.shape(c.mask_ell(mx_, my_, 3, 3), mc, dk(mc, 0.7), band=1)
    c.shape(c.mask_rect(18, 222, 40, 236), (252, 250, 236), (220, 216, 196), band=1)
    for yy in (226, 229, 232):
        c.fill(c.mask_rect(21, yy, 36, yy + 1), (150, 150, 170))
    # plan de travail + meubles bas
    top = c.mask_rect(62, 228, 270, 238)
    c.shape(top, (120, 110, 104), (84, 76, 72), (160, 152, 146), band=2, sdir="bottom")
    low = c.mask_rect(62, 238, 270, 318)
    c.fill(low, (196, 150, 104))
    for x0 in (64, 140, 176, 212, 240):
        d = c.mask_rect(x0 + 2, 242, x0 + (34 if x0 < 240 else 28), 312)
        c.shape(d, (206, 160, 112), (166, 122, 82), (226, 186, 136), band=2)
        c.fill(c.mask_rect(x0 + 6, 248, x0 + 18, 250), (90, 90, 96))
    oven = c.mask_rect(66, 240, 136, 314)                                  # four
    c.shape(oven, (60, 62, 70), (40, 42, 48), (90, 92, 104), band=2)
    ow = c.mask_rect(74, 262, 128, 300)
    c.fill(ow, (30, 26, 30))
    if heure == "nuit" or True:
        c.fill(c.mask_rect(78, 270, 124, 296), (120, 60, 30)); c.glow(101, 284, 26, (255, 150, 60), 0.35, m=ow)
    c.fill(c.mask_rect(72, 248, 130, 252), (170, 174, 186))
    for kx in (80, 92, 104, 116):
        c.fill(c.mask_ell(kx, 244, 2, 2), (200, 204, 214))
    for hx in (82, 118):                                                   # plaques + casserole
        c.fill(c.mask_ell(hx, 228, 11, 2), (40, 40, 44))
    pot = c.mask_rect(70, 208, 96, 228)
    c.shape(pot, (196, 60, 54), (150, 36, 36), (230, 110, 96), band=2)
    c.shape(c.mask_rect(68, 204, 98, 209), (210, 70, 64), (160, 44, 40), band=1)
    c.fill(c.mask_rect(96, 214, 106, 216), (60, 60, 64))
    for k in range(3):                                                    # vapeur
        for j in range(4):
            c.px(76 + k * 7 + (j % 2), 198 - j * 4, (250, 250, 250))
            c.px(77 + k * 7 + ((j + 1) % 2), 196 - j * 4, (236, 236, 240))
    sink = c.mask_rect(172, 226, 234, 230)                                # évier + robinet
    c.fill(sink, (150, 156, 168))
    fau = c.mask_rect(201, 200, 205, 228) | c.mask_rect(201, 198, 216, 202) | c.mask_rect(213, 198, 217, 206)
    c.shape(fau, (200, 206, 216), (140, 146, 160), (240, 244, 250), band=1)
    board = c.mask_rect(110, 222, 144, 228)                               # planche + tomates
    c.shape(board, (200, 160, 110), (160, 120, 76), band=1)
    for tx in (118, 128):
        c.shape(c.mask_ell(tx, 219, 4, 4), (220, 50, 46), (160, 30, 30), (250, 120, 100), band=1)
        c.px(tx, 214, (70, 150, 70))
    jar = c.mask_rect(244, 204, 258, 228)
    c.shape(jar, (200, 230, 236), (160, 196, 204), band=1)
    c.fill(c.mask_rect(246, 214, 256, 228), (236, 200, 120))
    c.shape(c.mask_rect(243, 200, 259, 205), (196, 60, 54), (150, 36, 36), band=1)
    clock = c.mask_ell(34, 62, 12, 12)                                    # horloge
    c.shape(clock, (250, 250, 248), (210, 206, 196), band=1)
    c.outline(c.mask_ell(34, 62, 14, 14) & ~clock, (196, 60, 54))
    c.line(34, 62, 34, 54, INK); c.line(34, 62, 40, 65, INK)
    sol_carreaux(c, 318, 480, horizon=250, c1=(230, 218, 196), c2=(184, 98, 74), grout=(150, 140, 124))
    c.shape(c.mask_rect(0, 314, 270, 320), (176, 136, 96), (136, 100, 70), band=1, sdir="bottom")
    teinte(c, heure, m=~intact(c, snap, win), interieur=True)
    if heure == "nuit":
        c.line(135, 0, 135, 30, (60, 50, 50))
        sh = c.mask_poly([(124, 30), (146, 30), (152, 40), (118, 40)])
        c.shape(sh, (60, 110, 100), (40, 80, 70), band=1)
        c.fill(c.mask_ell(135, 41, 4, 2), (255, 240, 190))
        c.glow(135, 50, 190, (255, 200, 130), 0.34)
        c.glow(135, 300, 150, (255, 196, 120), 0.10)
        c.glow(101, 284, 30, (255, 150, 60), 0.3)
    elif heure == "jour":
        ray = c.mask_poly([(160, 148), (246, 148), (236, 480), (110, 480)])
        c.tint(ray & c.mask_rect(0, 150, 270, 480), (255, 250, 220), 0.10)
    return c, None


# =================================================================== RUE (cité)
def rue(heure="jour"):
    c = Px()
    sky = c.mask_rect(0, 0, 270, 300)
    ciel(c, sky, 0, 200, heure, seed=12, astre=(214, 40))
    skyline(c, 240, heure, seed=4, hmin=70, hmax=150, far=True)
    snap = c.a.copy()
    rnd = R(21)
    lits = []                                                             # fenêtres allumées (rallumées après la teinte de nuit)
    # immeuble gauche (HLM beige)
    b1 = c.mask_rect(-2, 34, 118, 300)
    c.shape(b1, (222, 200, 164), (186, 162, 128), (240, 224, 194), band=3)
    for fy in range(46, 230, 30):
        bal = c.mask_rect(4, fy + 18, 112, fy + 24)
        c.shape(bal, (200, 176, 140), (160, 138, 106), band=1, sdir="bottom")
        for wx in range(10, 108, 24):
            w = c.mask_rect(wx, fy, wx + 14, fy + 17)
            lit = heure == "nuit" and rnd.random() < 0.5
            c.fill(w, (250, 210, 120) if lit else ((120, 160, 200) if heure != "soir" else (200, 140, 120)))
            c.fill(w & c.mask_rect(wx, fy, wx + 14, fy + 3), (180, 120, 80) if not lit else (230, 180, 100))
            c.outline(w, (150, 130, 104))
            c.fill(c.mask_rect(wx + 6, fy, wx + 7, fy + 17), (150, 130, 104))
            if lit:
                lits.append((w & ~c.mask_rect(wx + 6, fy, wx + 7, fy + 17), wx + 7, fy + 9))
        for bx in range(6, 112, 6):
            c.fill(c.mask_rect(bx, fy + 19, bx + 1, fy + 23), (160, 138, 106))
        if fy in (76, 136):                                                # paraboles
            c.shape(c.mask_ell(24 + (fy % 50), fy + 12, 4, 5), (236, 236, 236), (190, 190, 196), band=1)
    door = c.mask_rect(40, 244, 74, 300)                                   # hall d'entrée
    c.shape(door, (70, 90, 110), (50, 64, 80), band=2)
    c.fill(c.mask_rect(44, 248, 56, 296), (150, 190, 220) if heure != "nuit" else (250, 214, 130))
    c.fill(c.mask_rect(58, 248, 70, 296), (150, 190, 220) if heure != "nuit" else (250, 214, 130))
    c.fill(c.mask_rect(80, 262, 86, 272), (60, 60, 66)); c.px(83, 265, (120, 220, 120))
    c.shape(c.mask_rect(34, 238, 80, 244), (190, 168, 134), (150, 130, 100), band=1, sdir="bottom")
    c.text((57, 230), "B", (60, 70, 90), size=8, anchor="ma")
    for k, (gx, gc) in enumerate(((8, (220, 70, 120)), (92, (60, 160, 220)))):  # tags (formes abstraites)
        for j in range(6):
            c.line(gx + j * 3, 286 - (j % 2) * 4, gx + j * 3 + 3, 282 + (j % 3) * 2, gc)
    # immeuble droit (ocre) + snack
    b2 = c.mask_rect(124, 70, 272, 300)
    c.shape(b2, (214, 150, 110), (176, 116, 82), (232, 178, 138), band=3, sdir="right")
    for fy in range(82, 220, 28):
        for wx in range(134, 266, 26):
            w = c.mask_rect(wx, fy, wx + 16, fy + 18)
            lit = heure == "nuit" and rnd.random() < 0.45
            c.fill(w, (250, 214, 120) if lit else ((118, 156, 196) if heure != "soir" else (190, 130, 120)))
            c.outline(w, (150, 96, 70))
            sh = c.mask_rect(wx - 4, fy, wx, fy + 18)
            c.shape(sh, (90, 120, 90), (60, 86, 60), band=1)
            if lit:
                lits.append((w, wx + 8, fy + 9))
    shop = c.mask_rect(126, 228, 270, 300)
    c.shape(shop, (60, 52, 56), (40, 34, 38), band=2)
    glass = c.mask_rect(134, 250, 220, 298)
    c.fill(glass, (90, 120, 120) if heure != "nuit" else (250, 220, 150))
    c.fill(glass & c.mask_poly([(150, 250), (160, 250), (140, 298), (134, 298)]), (150, 190, 190) if heure != "nuit" else (255, 240, 200))
    c.outline(glass, (30, 26, 30))
    for k in range(3):                                                     # menu dans la vitrine
        c.fill(c.mask_rect(172 + k * 14, 258, 182 + k * 14, 270), (250, 246, 230)); c.outline(c.mask_rect(172 + k * 14, 258, 182 + k * 14, 270))
    sd = c.mask_rect(226, 250, 262, 300)
    c.shape(sd, (120, 40, 40), (90, 26, 30), band=1); c.fill(c.mask_rect(230, 254, 258, 292), (90, 120, 120) if heure != "nuit" else (250, 214, 140))
    aw = c.mask_poly([(128, 232), (270, 232), (270, 246), (124, 246)])       # store rayé
    c.fill(aw, (240, 240, 240))
    c.fill(aw & (((c.xx // 9) % 2) == 0), (210, 50, 50))
    for x in range(124, 270, 9):
        c.fill(c.mask_ell(x + 4.5, 246, 4.5, 2.5), (210, 50, 50) if (x // 9) % 2 == 0 else (240, 240, 240))
    c.outline(aw)
    sign = c.mask_rect(150, 210, 250, 228)
    c.shape(sign, (34, 30, 40), (20, 18, 24), band=1)
    if heure == "nuit" or heure == "soir":
        neon_texte(c, (200, 213), "SNACK", (255, 90, 120), size=11)
    else:
        c.text((200, 213), "SNACK", (250, 210, 80), size=11, anchor="ma")
    # trottoir + route
    walk = c.mask_rect(0, 300, 270, 352)
    c.fill(walk, (176, 174, 170))
    for y in (312, 328):
        c.fill(walk & c.mask_rect(0, y, 270, y + 1), (150, 148, 146))
    for x in range(0, 270, 30):
        c.fill(walk & c.mask_rect(x, 300, x + 1, 352), (150, 148, 146))
    c.shape(c.mask_rect(0, 352, 270, 358), (200, 198, 194), (150, 148, 146), band=2, sdir="bottom")
    road = c.mask_rect(0, 358, 270, 480)
    c.vgrad(road, 358, 480, (74, 74, 80), (96, 96, 102), steps=4)
    c.dither(road, (110, 110, 116), 0.12)
    for y0_, w_ in ((392, 3), (436, 5)):
        for x in range(-20, 120, 70):
            c.fill(c.mask_rect(x + (y0_ % 40), y0_, x + (y0_ % 40) + 30, y0_ + w_), (236, 236, 230))
    for k in range(6):                                                    # passage piéton
        xa, xb = 150 + k * 20, 162 + k * 20
        c.fill(c.mask_poly([(xa + 4, 362), (xb + 3, 362), (xb + (xb - 135) * 0.25, 480), (xa + (xa - 135) * 0.25, 480)]), (232, 232, 226))
    voiture(c, 74, 444, col=(70, 110, 190), sens=1, phares=heure == "nuit")
    lampadaire(c, 248, 352, h=200, on=heure != "jour")
    # poubelle + plot
    bin_ = c.mask_rect(10, 318, 26, 344)
    c.shape(bin_, (60, 120, 90), (40, 86, 62), (90, 150, 116), band=2)
    c.shape(c.mask_rect(8, 314, 28, 319), (70, 136, 100), (40, 86, 62), band=1)
    teinte(c, heure, m=~intact(c, snap, sky))
    if heure == "nuit":
        for w, gx, gy in lits:
            c.fill(w, (250, 212, 122))
            c.fill(w & c.mask_rect(0, gy - 9, 270, gy - 6), (226, 176, 98))
            c.glow(gx, gy, 18, (255, 206, 120), 0.22)
        for gm in (c.mask_rect(44, 248, 56, 296), c.mask_rect(58, 248, 70, 296), c.mask_rect(230, 254, 258, 292)):
            c.fill(gm, (250, 220, 150))
        c.fill(glass, (250, 224, 160))
        c.fill(glass & c.mask_poly([(150, 250), (160, 250), (140, 298), (134, 298)]), (255, 242, 210))
        for k in range(3):
            c.fill(c.mask_rect(172 + k * 14, 258, 182 + k * 14, 270), (250, 246, 230)); c.outline(c.mask_rect(172 + k * 14, 258, 182 + k * 14, 270))
        neon_texte(c, (200, 213), "SNACK", (255, 90, 120), size=11)
        lampadaire(c, 248, 352, h=200, on=True)
        c.glow(178, 274, 70, (255, 220, 150), 0.22)
        c.glow(57, 272, 40, (255, 220, 150), 0.18)
        c.glow(124, 438, 40, (255, 240, 180), 0.3)
    return relief(c, snap, sky), None


def rue_proche(heure="jour"):
    """La rue À L'ÉCHELLE DES PERSOS (01/11/2026 : dans « rue », l'utilisateur trouvait les persos « disproportionnés »
    — ils faisaient trois étages de haut). Ici on est tout près des façades : rez-de-chaussée grand (portes un peu plus
    hautes qu'un perso, vitrine, grande enseigne), seulement le 1er étage au-dessus, pas de petite voiture au premier plan."""
    c = Px()
    sky = c.mask_rect(0, 0, 270, 40)
    ciel(c, sky, 0, 40, heure, seed=12, astre=(196, 14))
    snap = c.a.copy()
    rnd = R(23)
    lits = []
    vitre = (120, 160, 200) if heure != "soir" else (200, 140, 120)
    # ---- immeuble gauche (HLM beige) : 1er étage + hall d'entrée
    c.shape(c.mask_rect(-2, 14, 124, 300), (222, 200, 164), (186, 162, 128), (240, 224, 194), band=3)
    c.shape(c.mask_rect(-2, 10, 126, 16), (200, 176, 140), (160, 138, 106), band=1, sdir="bottom")
    for wx in (12, 68):
        w = c.mask_rect(wx, 40, wx + 40, 106)
        lit = heure == "nuit" and rnd.random() < 0.6
        c.fill(w, (250, 210, 120) if lit else vitre)
        c.fill(w & c.mask_rect(wx, 40, wx + 40, 47), (180, 120, 80) if not lit else (230, 180, 100))
        c.outline(w, (150, 130, 104))
        c.fill(c.mask_rect(wx + 19, 40, wx + 21, 106), (150, 130, 104))
        if lit:
            lits.append((w, wx + 20, 74))
        c.shape(c.mask_rect(wx - 5, 104, wx + 45, 111), (200, 176, 140), (160, 138, 106), band=1, sdir="bottom")
        for bx in range(wx - 3, wx + 45, 5):
            c.fill(c.mask_rect(bx, 111, bx + 1, 124), (160, 138, 106))
        c.fill(c.mask_rect(wx - 5, 122, wx + 45, 125), (170, 148, 116))
    c.shape(c.mask_rect(-2, 150, 126, 158), (200, 176, 140), (160, 138, 106), band=1, sdir="bottom")
    c.shape(c.mask_rect(26, 186, 100, 300), (70, 90, 110), (50, 64, 80), band=2)           # porte vitrée double
    for gx0, gx1 in ((31, 61), (65, 95)):
        g = c.mask_rect(gx0, 192, gx1, 298)
        c.fill(g, (150, 190, 220) if heure != "nuit" else (250, 214, 130))
        c.fill(g & c.mask_poly([(gx0 + 6, 192), (gx0 + 13, 192), (gx0 + 3, 244), (gx0, 244)]),
               (190, 220, 240) if heure != "nuit" else (255, 236, 180))
        c.outline(g, (40, 52, 66))
        c.fill(c.mask_rect(gx1 - 5, 238, gx1 - 3, 254), (200, 200, 206))
    c.shape(c.mask_rect(20, 176, 106, 186), (190, 168, 134), (150, 130, 100), band=1, sdir="bottom")
    c.text((63, 163), "HALL B", (60, 70, 90), size=8, anchor="ma")
    c.fill(c.mask_rect(106, 226, 116, 246), (60, 60, 66)); c.px(111, 231, (120, 220, 120))   # interphone
    for gx, gc in ((4, (220, 70, 120)), (108, (60, 160, 220))):                                # tags
        for j in range(5):
            c.line(gx + j * 3, 292 - (j % 2) * 5, gx + j * 3 + 3, 287 + (j % 3) * 2, gc)
    # ---- immeuble droit (ocre) : 1er étage + snack
    c.shape(c.mask_rect(126, 0, 272, 300), (214, 150, 110), (176, 116, 82), (232, 178, 138), band=3, sdir="right")
    for wx in (146, 214):
        w = c.mask_rect(wx, 26, wx + 34, 96)
        lit = heure == "nuit" and rnd.random() < 0.5
        c.fill(w, (250, 214, 120) if lit else ((118, 156, 196) if heure != "soir" else (190, 130, 120)))
        c.outline(w, (150, 96, 70))
        c.fill(c.mask_rect(wx + 16, 26, wx + 18, 96), (150, 96, 70))
        for sx in (wx - 9, wx + 35):                                                     # volets
            c.shape(c.mask_rect(sx, 26, sx + 8, 96), (90, 120, 90), (60, 86, 60), band=1)
            for yy in range(30, 94, 6):
                c.fill(c.mask_rect(sx + 1, yy, sx + 7, yy + 1), (70, 100, 72))
        c.shape(c.mask_rect(wx - 4, 96, wx + 38, 102), (200, 140, 104), (160, 104, 74), band=1, sdir="bottom")
        if lit:
            lits.append((w, wx + 17, 60))
    sign = c.mask_rect(136, 140, 264, 164)                                               # grande enseigne (sous « ABONNE-TOI »)
    c.shape(sign, (34, 30, 40), (20, 18, 24), band=1)
    if heure in ("nuit", "soir"):
        neon_texte(c, (200, 143), "SNACK", (255, 90, 120), size=15)
    else:
        c.text((200, 143), "SNACK", (250, 210, 80), size=15, anchor="ma")
    aw = c.mask_poly([(130, 166), (270, 166), (270, 180), (124, 180)])                    # store rayé
    c.fill(aw, (240, 240, 240))
    c.fill(aw & (((c.xx // 10) % 2) == 0), (210, 50, 50))
    for x in range(124, 270, 10):
        c.fill(c.mask_ell(x + 5, 180, 5, 3), (210, 50, 50) if (x // 10) % 2 == 0 else (240, 240, 240))
    c.outline(aw)
    c.shape(c.mask_rect(128, 183, 270, 300), (60, 52, 56), (40, 34, 38), band=2)
    glass = c.mask_rect(134, 188, 212, 298)                                               # vitrine
    c.fill(glass, (90, 120, 120) if heure != "nuit" else (250, 220, 150))
    c.fill(glass & c.mask_poly([(152, 188), (164, 188), (140, 298), (134, 298)]),
           (150, 190, 190) if heure != "nuit" else (255, 240, 200))
    c.outline(glass, (30, 26, 30))
    for k in range(3):                                                                     # menu
        m_ = c.mask_rect(160 + k * 16, 200, 172 + k * 16, 216)
        c.fill(m_, (250, 246, 230)); c.outline(m_)
        c.fill(c.mask_rect(162 + k * 16, 204, 170 + k * 16, 205), (200, 80, 60))
        c.fill(c.mask_rect(162 + k * 16, 208, 168 + k * 16, 209), (120, 110, 100))
    c.fill(c.mask_rect(136, 262, 210, 266), (120, 100, 90))                               # comptoir
    sd = c.mask_rect(220, 186, 264, 300)                                                   # porte du snack
    c.shape(sd, (120, 40, 40), (90, 26, 30), band=1)
    c.fill(c.mask_rect(225, 192, 259, 292), (90, 120, 120) if heure != "nuit" else (250, 214, 140))
    c.fill(c.mask_rect(250, 238, 254, 252), (220, 210, 190))
    # ---- trottoir + route (sans voiture : une voiture au premier plan devrait être plus grande que les persos)
    walk = c.mask_rect(0, 300, 270, 352)
    c.fill(walk, (176, 174, 170))
    for y in (314, 332):
        c.fill(walk & c.mask_rect(0, y, 270, y + 1), (150, 148, 146))
    for x in range(0, 270, 36):
        c.fill(walk & c.mask_rect(x, 300, x + 1, 352), (150, 148, 146))
    c.shape(c.mask_rect(0, 352, 270, 358), (200, 198, 194), (150, 148, 146), band=2, sdir="bottom")
    road = c.mask_rect(0, 358, 270, 480)
    c.vgrad(road, 358, 480, (74, 74, 80), (96, 96, 102), steps=4)
    c.dither(road, (110, 110, 116), 0.12)
    for k in range(6):                                                                     # passage piéton
        xa, xb = 150 + k * 20, 162 + k * 20
        c.fill(c.mask_poly([(xa + 4, 362), (xb + 3, 362), (xb + (xb - 135) * 0.25, 480), (xa + (xa - 135) * 0.25, 480)]),
               (232, 232, 226))
    for x in range(-20, 120, 70):
        c.fill(c.mask_rect(x + 12, 420, x + 42, 424), (236, 236, 230))
    lampadaire(c, 121, 352, h=250, on=heure != "jour")
    c.shape(c.mask_rect(4, 304, 28, 346), (60, 120, 90), (40, 86, 62), (90, 150, 116), band=2)   # poubelle
    c.shape(c.mask_rect(2, 299, 30, 305), (70, 136, 100), (40, 86, 62), band=1)
    teinte(c, heure, m=~intact(c, snap, sky))
    if heure == "nuit":
        for w, gx, gy in lits:
            c.fill(w, (250, 212, 122))
            c.glow(gx, gy, 26, (255, 206, 120), 0.22)
        for gm in (c.mask_rect(31, 192, 61, 298), c.mask_rect(65, 192, 95, 298), c.mask_rect(225, 192, 259, 292)):
            c.fill(gm, (250, 220, 150))
        c.fill(glass, (250, 224, 160))
        neon_texte(c, (200, 143), "SNACK", (255, 90, 120), size=15)
        lampadaire(c, 121, 352, h=250, on=True)
        c.glow(174, 244, 80, (255, 220, 150), 0.22)
        c.glow(63, 244, 50, (255, 220, 150), 0.18)
    return relief(c, snap, sky), None


# =================================================================== PARC
def parc(heure="jour"):
    c = Px()
    sky = c.mask_rect(0, 0, 270, 230)
    ciel(c, sky, 0, 230, heure, seed=8, astre=(60, 60))
    skyline(c, 200, heure, seed=9, hmin=20, hmax=70, far=True)
    snap = c.a.copy()
    gr = c.mask_rect(0, 196, 270, 480)
    gc = dict(jour=((110, 176, 84), (88, 150, 70)), soir=((140, 150, 80), (110, 120, 66)), nuit=((50, 80, 60), (40, 64, 52)))[heure]
    c.vgrad(gr, 196, 480, gc[1], gc[0], steps=5)
    rnd = R(5)
    for _ in range(900):                                                  # brins d'herbe
        x, y = rnd.randrange(270), rnd.randrange(200, 480)
        c.px(x, y, lt(gc[0], 0.2) if rnd.random() < 0.5 else dk(gc[0], 0.8))
    for k, (tx, ty, r_) in enumerate(((20, 220, 30), (80, 206, 22), (196, 210, 26), (250, 224, 32), (140, 200, 16))):
        arbre(c, tx, ty, r=r_, trunk=int(r_ * 1.1), col=dict(jour=(64, 140, 70), soir=(110, 120, 60), nuit=(34, 70, 56))[heure], seed=k + 2)
    # allée
    path = c.mask_poly([(118, 236), (152, 236), (230, 480), (40, 480)])
    c.fill(path, (214, 196, 156) if heure != "nuit" else (120, 116, 110))
    c.dither(path, (190, 172, 132) if heure != "nuit" else (100, 96, 92), 0.25)
    for side in (-1, 1):
        edge = c.mask_poly([(135 + side * 17, 236), (135 + side * 19, 236), (135 + side * 98, 480), (135 + side * 94, 480)])
        c.fill(edge, (176, 170, 160) if heure != "nuit" else (90, 90, 90))
    # fleurs
    for _ in range(70):
        x, y = rnd.randrange(270), rnd.randrange(250, 470)
        if not path[y, x]:
            fc = rnd.choice([(250, 90, 110), (250, 220, 80), (250, 250, 250), (180, 110, 240)])
            c.px(x, y, fc); c.px(x + 1, y, fc); c.px(x, y - 1, (60, 120, 60))
    banc(c, 186, 250, 300)
    banc(c, 14, 70, 296)
    lampadaire(c, 104, 300, h=150, on=heure == "nuit")
    # étang
    pond = c.mask_ell(230, 380, 46, 14)
    c.fill(pond, (90, 160, 210) if heure != "nuit" else (30, 50, 90))
    c.fill(pond & c.mask_rect(0, 372, 270, 376), (160, 210, 240) if heure != "nuit" else (80, 90, 140))
    c.outline(pond, (120, 110, 90))
    for dx in (-10, 12):                                                   # canards
        d = c.mask_ell(226 + dx, 378, 4, 2.5)
        c.fill(d, (250, 250, 246)); c.fill(c.mask_ell(229 + dx, 375, 2, 2), (250, 250, 246)); c.px(231 + dx, 375, (250, 170, 40))
    teinte(c, heure, m=~intact(c, snap, sky))
    if heure == "nuit":
        lampadaire(c, 104, 300, h=150, on=True)
    return relief(c, snap, sky), None


# =================================================================== CHAMBRE D'ADO (gameur, nuit)
def chambre_ado(heure="nuit"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 312)
    c.vgrad(wall, 0, 312, (40, 34, 74), (70, 54, 110), steps=6)
    # bande LED au plafond
    for x in range(0, 270):
        k = x / 270
        colr = mix((255, 60, 200), (60, 220, 255), k)
        c.px(x, 6, colr); c.px(x, 7, colr)
    c.glow(135, 8, 200, (200, 100, 255), 0.18)
    # fenêtre (ville la nuit) avec store
    win = c.mask_rect(18, 50, 96, 146)
    ciel(c, win, 50, 146, "nuit", seed=2, astre=(80, 68))
    skyline(c, 146, "nuit", seed=7, x0=18, x1=96, hmin=20, hmax=60, m=win)
    for y in range(52, 84, 4):
        c.fill(c.mask_rect(18, y, 96, y + 2), (200, 196, 210))
    c.outline(win, (20, 16, 30)); c.shape(c.mask_rect(14, 146, 100, 151), (90, 80, 110), (60, 54, 80), band=1)
    # posters
    p1 = c.mask_rect(112, 40, 150, 92)
    c.vgrad(p1, 40, 92, (250, 120, 80), (130, 40, 120), steps=5)
    c.fill(c.mask_ell(131, 58, 9, 9), (255, 220, 120)); c.fill(c.mask_rect(116, 76, 146, 79), (30, 20, 40))
    c.fill(c.mask_poly([(116, 92), (124, 70), (132, 92)]), (60, 30, 80)); c.fill(c.mask_poly([(126, 92), (138, 66), (148, 92)]), (40, 20, 60))
    c.outline(p1, (20, 16, 30))
    p2 = c.mask_rect(158, 50, 190, 96)
    c.fill(p2, (30, 40, 70))
    c.fill(c.mask_ell(174, 66, 10, 10), (90, 200, 240)); c.fill(c.mask_ell(174, 66, 10, 3) & ~c.mask_ell(174, 66, 7, 2), (250, 200, 100))
    for k in range(6):
        c.px(162 + k * 5, 84 + (k % 2) * 4, (250, 250, 250))
    c.outline(p2, (20, 16, 30))
    # étagère + figurines
    c.shape(c.mask_rect(200, 100, 262, 104), (120, 90, 130), (80, 60, 90), band=1)
    for k, (fx, fc) in enumerate(((208, (230, 60, 70)), (222, (250, 200, 60)), (236, (80, 200, 120)), (250, (90, 150, 250)))):
        f = c.mask_rect(fx, 88, fx + 6, 100) | c.mask_ell(fx + 3, 86, 3.5, 3.5)
        c.shape(f, fc, dk(fc, 0.7), lt(fc, 0.3), band=1)
    # lit (gauche)
    bed = c.mask_rect(0, 236, 100, 316)
    c.shape(bed, (60, 50, 80), (40, 34, 56), band=2)
    duvet = c.mask_poly([(0, 244), (98, 236), (104, 300), (0, 306)])
    c.shape(duvet, (50, 70, 130), (36, 50, 100), (80, 100, 170), band=3)
    for y in (258, 276):
        c.line(0, y, 100, y - 6, (40, 56, 110))
    c.shape(c.mask_rrect(4, 224, 46, 244, 6), (200, 200, 220), (160, 160, 186), band=2)
    # bureau gameur (droite) : 2 écrans, clavier lumineux, chaise
    desk = c.mask_rect(140, 226, 266, 234)
    c.shape(desk, (36, 30, 44), (20, 18, 26), (70, 60, 86), band=1)
    for lx in (146, 258):
        c.fill(c.mask_rect(lx, 234, lx + 4, 312), (30, 26, 36))
    ecran(c, 150, 162, 206, 204, scr=(110, 60, 220), kind="jeu", seed=3)
    ecran(c, 210, 166, 262, 204, scr=(40, 160, 220), kind="code", seed=5)
    for sx in (176, 234):
        c.fill(c.mask_rect(sx, 204, sx + 4, 222), (30, 30, 36)); c.fill(c.mask_rect(sx - 8, 220, sx + 12, 226), (30, 30, 36))
    kb = c.mask_rect(170, 218, 222, 225)
    c.fill(kb, (30, 30, 36))
    for x in range(172, 220, 2):
        c.px(x, 220, mix((255, 60, 200), (60, 220, 255), (x - 170) / 52)); c.px(x + 1, 222, mix((60, 220, 255), (255, 60, 200), (x - 170) / 52))
    c.shape(c.mask_ell(232, 222, 4, 2.5), (40, 40, 50), band=1)
    c.shape(c.mask_rect(240, 210, 248, 226), (230, 60, 70), (170, 30, 40), band=1)       # canette
    # sol
    planks(c, 312, 480, horizon=240, col=(70, 56, 70), dark=(50, 40, 54), light=(92, 76, 92))
    c.shape(c.mask_rect(0, 308, 270, 314), (50, 40, 70), (30, 26, 44), band=1, sdir="bottom")
    rug = c.mask_ell(135, 410, 100, 40)
    c.fill(rug, (90, 60, 140)); c.fill(rug & ~c.mask_ell(135, 410, 90, 34), (130, 90, 190))
    c.dither(rug & c.mask_ell(135, 410, 70, 24), (110, 76, 166), 0.4)
    c.glow(178, 186, 120, (140, 90, 255), 0.22)
    c.glow(236, 186, 90, (60, 200, 255), 0.18)
    c.glow(57, 100, 60, (120, 120, 220), 0.15)
    return c, None


# =================================================================== SALLE DE CLASSE
def classe(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 316)
    c.vgrad(wall, 0, 316, (214, 226, 200), (234, 238, 218), steps=6)
    c.shape(c.mask_rect(0, 0, 270, 10), (236, 236, 230), (200, 200, 192), band=2, sdir="bottom")
    for x in (40, 140, 240):                                              # néons
        c.shape(c.mask_rect(x - 22, 10, x + 22, 15), (250, 250, 246), (210, 210, 206), band=1)
    # fenêtres (gauche)
    for wy in (40, 150):
        win = c.mask_rect(4, wy, 54, wy + 96)
        ciel(c, win, wy, wy + 96, heure if heure != "nuit" else "nuit", seed=wy, astre=None)
        arbre(c, 30, wy + 120, r=30, trunk=26, col=(70, 150, 80), seed=wy, m=win)
        c.fill(c.mask_rect(28, wy, 30, wy + 96), (240, 240, 236)); c.fill(c.mask_rect(4, wy + 46, 54, wy + 48), (240, 240, 236))
        c.outline(win, (120, 120, 120))
        c.shape(c.mask_rect(0, wy + 96, 60, wy + 101), (236, 236, 232), (196, 196, 192), band=1)
    wins = c.mask_rect(4, 40, 54, 136) | c.mask_rect(4, 150, 54, 246)
    snap = c.a.copy()
    # tableau blanc + feutres
    wb = c.mask_rect(74, 54, 236, 170)
    c.shape(c.mask_rect(70, 50, 240, 174), (180, 186, 196), (140, 146, 160), band=2)
    c.fill(wb, (248, 250, 252))
    rnd = R(14)
    c.text((90, 62), "2x + 3 = 11", (40, 60, 160), size=9)
    c.text((90, 80), "x = 4", (200, 40, 50), size=9)
    for k in range(4):
        y = 104 + k * 14
        c.line(90, y, 90 + rnd.randint(40, 120), y + rnd.randint(-1, 1), (60, 70, 90))
    c.outline(c.mask_ell(210, 92, 14, 14) & ~c.mask_ell(210, 92, 13, 13), (40, 140, 70))
    c.line(196, 92, 224, 92, (40, 140, 70)); c.line(210, 78, 210, 106, (40, 140, 70))
    c.shape(c.mask_rect(70, 174, 240, 179), (170, 176, 186), (130, 136, 150), band=1)
    for fx, fc in ((90, (40, 60, 160)), (100, (200, 40, 50)), (110, (40, 140, 70))):
        c.fill(c.mask_rect(fx, 171, fx + 7, 174), fc)
    clk = c.mask_ell(155, 30, 11, 11)
    c.shape(clk, (250, 250, 248), (210, 206, 196), band=1); c.outline(c.mask_ell(155, 30, 13, 13) & ~clk, (40, 40, 50))
    c.line(155, 30, 155, 22, INK); c.line(155, 30, 161, 33, INK)
    # affiches
    m1 = c.mask_rect(244, 40, 268, 100)
    c.fill(m1, (250, 246, 230)); c.outline(m1, (150, 140, 120))
    for k in range(5):
        c.fill(c.mask_rect(248, 46 + k * 10, 248 + 6 + (k * 3) % 12, 50 + k * 10), [(220, 60, 60), (60, 120, 220), (70, 170, 80), (240, 180, 50), (160, 80, 180)][k])
    m2 = c.mask_rect(244, 110, 268, 150)
    c.fill(m2, (170, 210, 240)); c.fill(c.mask_ell(252, 126, 6, 9) & m2, (110, 180, 100)); c.fill(c.mask_ell(262, 138, 5, 6) & m2, (110, 180, 100))
    c.outline(m2, (150, 140, 120))
    # bureau du prof + globe + pommes + livres
    desk = c.mask_rect(186, 248, 266, 256)
    c.shape(desk, (170, 120, 76), (130, 88, 54), (200, 150, 100), band=1)
    c.shape(c.mask_rect(190, 256, 262, 312), (150, 104, 66), (112, 76, 46), band=2)
    c.fill(c.mask_rect(196, 266, 256, 268), (112, 76, 46))
    gl = c.mask_ell(246, 232, 10, 10)
    c.fill(gl, (70, 140, 220)); c.fill(gl & c.mask_ell(242, 228, 5, 4), (100, 180, 100)); c.fill(gl & c.mask_ell(250, 238, 4, 3), (100, 180, 100))
    c.outline(gl); c.fill(c.mask_rect(244, 242, 248, 248), (120, 90, 50))
    books(c, 196, 226, 248, 8, 12, seed=4)
    c.shape(c.mask_ell(232, 244, 4, 4), (220, 40, 40), (150, 20, 30), (250, 120, 110), band=1); c.px(232, 239, (80, 150, 60))
    # sol lino
    floor = c.mask_rect(0, 316, 270, 480)
    c.vgrad(floor, 316, 480, (186, 196, 186), (206, 214, 204), steps=4)
    for y in range(320, 480, 16):
        c.fill(floor & c.mask_rect(0, y, 270, y + 1), (170, 180, 170))
    c.shape(c.mask_rect(0, 312, 270, 318), (120, 130, 120), (90, 100, 90), band=1, sdir="bottom")
    # pupitres d'élèves (premier plan, sur les côtés)
    for x0, y0 in ((-6, 364), (202, 364)):
        top = c.mask_poly([(x0, y0), (x0 + 74, y0), (x0 + 80, y0 + 12), (x0 - 6, y0 + 12)])
        c.shape(top, (200, 170, 120), (160, 130, 86), (226, 200, 150), band=2, sdir="bottom")
        c.shape(c.mask_rect(x0 - 4, y0 + 12, x0 + 78, y0 + 22), (110, 116, 126), (80, 86, 96), band=1)
        for lx in (x0 + 4, x0 + 70):
            c.fill(c.mask_rect(lx, y0 + 22, lx + 3, y0 + 76), (110, 116, 126))
        c.shape(c.mask_rect(x0 + 14, y0 - 4, x0 + 40, y0 + 1), (246, 246, 240), (210, 210, 200), band=1)
        c.fill(c.mask_rect(x0 + 44, y0 - 2, x0 + 58, y0), (60, 90, 190))
    bag = c.mask_rrect(120, 434, 150, 470, 5)
    c.shape(bag, (60, 100, 170), (40, 70, 130), (90, 130, 200), band=2)
    c.fill(c.mask_rect(126, 446, 144, 456), (40, 70, 130))
    teinte(c, heure, m=~intact(c, snap, wins), interieur=True)
    if heure == "jour":
        for wy in (40, 150):
            ray = c.mask_poly([(54, wy), (54, wy + 96), (200, wy + 330), (200, wy + 150)])
            c.tint(ray & c.mask_rect(54, 0, 270, 480), (255, 250, 220), 0.08)
    return c, None


# =================================================================== OPEN SPACE (bureau)
def bureau(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 300)
    c.fill(wall, (226, 228, 232))
    c.shape(c.mask_rect(0, 0, 270, 14), (240, 240, 242), (206, 208, 214), band=2, sdir="bottom")
    for x in range(10, 270, 64):                                          # dalles lumineuses
        c.fill(c.mask_rect(x, 4, x + 40, 9), (252, 252, 246))
    # grande baie vitrée sur la ville
    win = c.mask_rect(0, 22, 270, 214)
    ciel(c, win, 22, 214, heure, seed=6, astre=(230, 60))
    skyline(c, 214, heure, seed=11, hmin=60, hmax=170, m=win)
    snap = c.a.copy()
    for x in range(0, 271, 54):
        c.shape(c.mask_rect(x - 2, 22, x + 2, 214), (70, 76, 86), (50, 54, 62), band=1)
    c.shape(c.mask_rect(0, 116, 270, 119), (70, 76, 86), (50, 54, 62), band=1)
    c.shape(c.mask_rect(0, 212, 270, 220), (90, 96, 106), (64, 68, 78), band=1, sdir="bottom")
    if heure == "jour":
        for x in range(0, 270, 54):
            c.tint(c.mask_poly([(x + 10, 22), (x + 22, 22), (x + 6, 214), (x - 6, 214)]) & win, (255, 255, 255), 0.18)
    # rangée de bureaux au fond
    for k, x0 in enumerate((10, 96, 182)):
        d = c.mask_rect(x0, 252, x0 + 78, 258)
        c.shape(d, (236, 236, 240), (196, 198, 206), band=1)
        for lx in (x0 + 4, x0 + 72):
            c.fill(c.mask_rect(lx, 258, lx + 3, 300), (120, 124, 134))
        ecran(c, x0 + 22, 222, x0 + 56, 246, scr=[(60, 140, 220), (70, 180, 140), (200, 120, 70)][k], kind=["graph", "code", "carte"][k], seed=k, glow=False)
        c.fill(c.mask_rect(x0 + 37, 246, x0 + 41, 252), (60, 60, 66))
        c.fill(c.mask_rect(x0 + 8, 248, x0 + 18, 252), (250, 250, 250))
        cup = c.mask_rect(x0 + 62, 244, x0 + 68, 252); c.shape(cup, (220, 70, 60), (160, 40, 40), band=1)
        ch = c.mask_rrect(x0 + 26, 262, x0 + 52, 290, 4)                   # dossiers de chaises
        c.shape(ch, (50, 54, 64), (32, 34, 42), (80, 84, 96), band=2)
    plante(c, 92, 300, h=44, pot=(240, 240, 240), seed=3)
    plante(c, 178, 300, h=36, pot=(60, 60, 66), seed=8)
    # fontaine à eau
    wc = c.mask_rect(250, 230, 268, 300)
    c.shape(wc, (236, 238, 242), (196, 200, 210), band=2)
    c.shape(c.mask_rrect(250, 200, 268, 230, 4), (150, 210, 240), (110, 170, 210), (200, 236, 250), band=2)
    # sol moquette
    floor = c.mask_rect(0, 300, 270, 480)
    c.vgrad(floor, 300, 480, (110, 120, 140), (130, 140, 158), steps=4)
    yy, xx = c.yy, c.xx
    dz = np.maximum(yy - 240, 1).astype(float); z = 420.0 / dz; xw = (xx - 135) * z / 105.0
    c.fill(floor & ((((xw / 0.9) - np.floor(xw / 0.9)) < 0.04) | (((z / 0.9) - np.floor(z / 0.9)) < 0.04)), (100, 108, 126))
    c.dither(floor, (120, 130, 150), 0.15)
    c.shape(c.mask_rect(0, 298, 270, 302), (90, 96, 106), (64, 68, 78), band=1)
    teinte(c, heure, m=~intact(c, snap, win), interieur=True)
    if heure == "nuit":
        for x in range(10, 270, 64):
            c.glow(x + 20, 8, 70, (255, 246, 220), 0.25)
        for k, x0 in enumerate((10, 96, 182)):
            c.glow(x0 + 39, 234, 40, [(60, 140, 220), (70, 180, 140), (200, 120, 70)][k], 0.3)
    return c, None


# =================================================================== SNACK (fast-food)
def snack(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 300)
    carrelage_mur(c, wall, 10, (246, 246, 244), (210, 210, 210), seed=3)
    c.fill(c.mask_rect(0, 150, 270, 160), (210, 50, 50))
    c.fill(c.mask_rect(0, 152, 270, 153), (250, 200, 70))
    # menu lumineux
    for k, (x0, title) in enumerate(((60, "BURGER"), (122, "TACOS"), (184, "BOISSONS"))):
        p = c.mask_rect(x0, 22, x0 + 58, 96)
        c.shape(p, (30, 28, 36), (20, 18, 24), band=1)
        inner = c.mask_rect(x0 + 3, 25, x0 + 55, 93)
        c.vgrad(inner, 25, 93, (60, 50, 60), (40, 34, 44), steps=3)
        c.text((x0 + 29, 28), title, (250, 210, 80), size=7, anchor="ma")
        if k == 0:
            c.shape(c.mask_ell(x0 + 29, 52, 14, 6) & c.mask_rect(0, 0, 270, 52), (230, 160, 70), (190, 120, 50), band=1)
            c.fill(c.mask_rect(x0 + 15, 52, x0 + 43, 55), (90, 170, 60)); c.fill(c.mask_rect(x0 + 15, 55, x0 + 43, 58), (120, 60, 40))
            c.shape(c.mask_rect(x0 + 15, 58, x0 + 43, 62), (230, 160, 70), (190, 120, 50), band=1)
        elif k == 1:
            tac = c.mask_ell(x0 + 29, 58, 16, 9) & c.mask_rect(0, 0, 270, 58)
            c.shape(tac, (240, 200, 110), (200, 160, 80), band=1)
            c.fill(c.mask_ell(x0 + 29, 56, 12, 5) & c.mask_rect(0, 0, 270, 56), (90, 170, 60))
        else:
            for j, cc in enumerate(((220, 40, 40), (60, 150, 230), (250, 200, 60))):
                c.shape(c.mask_rect(x0 + 12 + j * 12, 44, x0 + 20 + j * 12, 62), cc, dk(cc, 0.7), lt(cc, 0.3), band=1)
        for j in range(3):
            c.fill(c.mask_rect(x0 + 8, 70 + j * 7, x0 + 34, 71 + j * 7), (200, 200, 200))
            c.text((x0 + 48, 67 + j * 7), str(5 + j + k * 2) + "€", (250, 210, 80), size=6, anchor="ma")
        c.glow(x0 + 29, 58, 46, (255, 230, 170), 0.12)
    # broche à kebab
    c.fill(c.mask_rect(24, 40, 27, 150), (180, 184, 196))
    meat = c.mask_poly([(14, 60), (38, 60), (34, 140), (18, 140)])
    c.shape(meat, (170, 100, 60), (130, 70, 40), (200, 136, 80), band=2)
    for y in range(64, 140, 6):
        c.fill(meat & c.mask_rect(0, y, 270, y + 1), (140, 80, 46))
    heater = c.mask_rect(40, 56, 50, 144)
    c.shape(heater, (90, 90, 100), (60, 60, 70), band=1)
    c.fill(c.mask_rect(42, 60, 48, 140), (240, 110, 50)); c.glow(45, 100, 40, (255, 130, 50), 0.35)
    # frigo à boissons
    fr = c.mask_rect(234, 40, 268, 230)
    c.shape(fr, (200, 40, 40), (150, 26, 30), (230, 90, 80), band=2)
    gl = c.mask_rect(238, 50, 264, 214)
    c.fill(gl, (190, 220, 236))
    for k, y in enumerate(range(80, 214, 32)):
        c.fill(c.mask_rect(238, y, 264, y + 2), (150, 170, 184))
        produits(c, 239, 263, y - 1, h=9, seed=10 + k)
    c.tint(gl & c.mask_poly([(240, 50), (248, 50), (240, 120)]), (255, 255, 255), 0.4)
    c.glow(251, 130, 40, (220, 240, 255), 0.2)
    # comptoir
    counter = c.mask_rect(0, 222, 230, 300)
    c.shape(counter, (200, 50, 50), (150, 30, 34), (230, 90, 84), band=3)
    c.fill(c.mask_rect(0, 222, 230, 232), (196, 202, 212)); c.fill(c.mask_rect(0, 230, 230, 232), (140, 146, 160))
    for x in range(0, 230, 40):
        c.fill(c.mask_rect(x, 240, x + 1, 300), (160, 34, 38))
    c.fill(c.mask_rect(0, 262, 230, 266), (250, 200, 70))
    reg = c.mask_rect(150, 198, 186, 222)                                  # caisse
    c.shape(reg, (60, 62, 70), (40, 42, 48), band=1)
    c.fill(c.mask_rect(154, 202, 182, 210), (90, 220, 140))
    c.shape(c.mask_rect(158, 190, 178, 199), (60, 62, 70), (40, 42, 48), band=1)
    for k, (bx, bc) in enumerate(((70, (230, 40, 40)), (80, (250, 210, 60)), (90, (250, 250, 240)))):   # sauces
        c.shape(c.mask_rect(bx, 204, bx + 7, 222), bc, dk(bc, 0.7), lt(bc, 0.3), band=1)
        c.fill(c.mask_rect(bx + 2, 199, bx + 5, 204), bc)
    c.shape(c.mask_rect(110, 210, 130, 222), (200, 204, 214), (150, 156, 170), band=1)
    c.fill(c.mask_rect(113, 205, 127, 211), (250, 250, 250))
    # sol en damier
    sol_carreaux(c, 300, 480, horizon=240, c1=(240, 236, 228), c2=(200, 50, 50), grout=(170, 160, 150), cell=0.8)
    c.shape(c.mask_rect(0, 298, 270, 302), (60, 50, 50), (40, 34, 34), band=1)
    teinte(c, heure, interieur=True)
    neon_texte(c, (135, 108), "OUVERT", (80, 230, 140) if heure == "jour" else (255, 80, 140), size=10)
    return c, None


# =================================================================== VOITURE (vue de face, à travers le pare-brise)
GLASS = [(30, 76), (240, 76), (262, 306), (8, 306)]


def voiture_int(heure="jour"):
    c = Px()
    rnd = R(4)
    # dehors (vu par la lunette arrière)
    out = c.mask_rect(0, 0, 270, 480)
    ciel(c, out, 0, 220, heure, seed=3, astre=None, nuages=heure == "jour")
    skyline(c, 216, heure, seed=13, hmin=40, hmax=110)
    # habitacle
    roof = c.mask_rect(0, 76, 270, 128)
    c.vgrad(roof, 76, 128, (150, 146, 150), (184, 180, 182), steps=4)
    rear = c.mask_rrect(56, 124, 214, 204, 10)
    snap_rear = c.a.copy()
    c.outline(rear, (40, 38, 44))
    side = c.mask_rect(0, 124, 56, 330) | c.mask_rect(214, 124, 270, 330)
    c.vgrad(side, 124, 330, (120, 116, 122), (90, 88, 96), steps=4)
    c.fill(c.mask_rect(0, 124, 270, 128), (110, 106, 112))
    for x0 in (56, 210):                                                   # montants arrière
        c.fill(c.mask_rect(x0 - 4, 124, x0 + 4, 210), (100, 96, 104))
    bench = c.mask_rect(40, 196, 230, 330)                                 # banquette arrière
    c.shape(bench, (70, 70, 84), (50, 50, 62), (96, 96, 110), band=2)
    for x in range(60, 220, 30):
        c.fill(bench & c.mask_rect(x, 200, x + 1, 260), (56, 56, 68))
    for sx in (82, 188):                                                   # sièges avant (appuie-tête derrière la tête)
        seat = c.mask_rrect(sx - 46, 214, sx + 46, 340, 10)
        c.shape(seat, (52, 52, 64), (36, 36, 46), (78, 78, 92), band=3)
        c.fill(seat & c.mask_rect(sx - 30, 226, sx + 30, 334), (64, 64, 78))
        for y in range(238, 330, 12):
            c.fill(seat & c.mask_rect(sx - 30, y, sx + 30, y + 1), (52, 52, 64))
        hr = c.mask_rrect(sx - 22, 180, sx + 22, 212, 8)
        c.shape(hr, (58, 58, 70), (40, 40, 50), (84, 84, 98), band=2)
        c.fill(c.mask_rect(sx - 10, 210, sx - 7, 216) | c.mask_rect(sx + 7, 210, sx + 10, 216), (150, 154, 164))
    c.fill(c.mask_rect(116, 80, 154, 84), (210, 206, 196))                 # plafonnier
    teinte(c, heure, m=~intact(c, snap_rear, rear), interieur=True)
    # ---- avant-plan : carrosserie autour du pare-brise, planche de bord, volant (le verre reste transparent)
    f = Px(alpha=True)
    glass = f.mask_poly(GLASS)
    outside = ~glass
    ciel(f, outside & f.mask_rect(0, 0, 270, 130), 0, 130, heure, seed=9, astre=(222, 14), nuages=False)
    skyline(f, 70, heure, seed=21, hmin=20, hmax=60, m=outside & f.mask_rect(0, 0, 270, 70))
    paint = dict(jour=(200, 56, 60), soir=(190, 60, 64), nuit=(150, 44, 54))[heure]
    roof = f.mask_poly([(14, 30), (256, 30), (270, 74), (270, 480), (0, 480), (0, 74)]) & outside
    f.fill(roof, paint)
    f.fill(f.mask_poly([(14, 30), (256, 30), (262, 40), (8, 40)]), lt(paint, 0.25))
    f.fill(f.mask_poly([(8, 40), (262, 40), (266, 48), (4, 48)]), lt(paint, 0.1))
    dil = glass.copy()                                                     # montants (bord épais autour du verre)
    for _ in range(7):
        dil = dil | np.roll(dil, 1, 0) | np.roll(dil, -1, 0) | np.roll(dil, 1, 1) | np.roll(dil, -1, 1)
    f.fill(dil & ~glass & f.mask_rect(0, 60, 270, 306), dk(paint, 0.6))
    f.fill(dil & ~glass & f.mask_rect(0, 60, 270, 306) & ~np.roll(dil & ~glass, 2, 1) & f.mask_rect(0, 0, 135, 480), dk(paint, 0.45))
    hood = f.mask_rect(0, 306, 270, 480)
    f.vgrad(hood, 306, 480, dk(paint, 0.82), lt(paint, 0.10), steps=5)
    f.fill(f.mask_poly([(44, 334), (226, 334), (244, 480), (26, 480)]), lt(paint, 0.04))
    f.line(44, 334, 26, 480, dk(paint, 0.72)); f.line(226, 334, 244, 480, dk(paint, 0.72))
    f.fill(f.mask_rect(0, 306, 270, 310), dk(paint, 0.5))
    dash = f.mask_poly([(10, 262), (260, 262), (262, 306), (8, 306)])
    wheel = f.mask_ell(84, 270, 36, 24) & ~f.mask_ell(84, 270, 30, 19) & f.mask_rect(0, 0, 270, 263)
    f.shape(wheel, (30, 30, 36), (20, 20, 24), (70, 70, 80), band=1)
    f.shape(dash, (56, 56, 64), (36, 36, 42), (90, 90, 100), band=2, sdir="bottom", ldir="top")
    f.fill(f.mask_rect(12, 262, 258, 265), (86, 86, 96))
    f.fill(f.mask_rect(150, 272, 182, 284), (24, 24, 28))                  # écran central
    f.fill(f.mask_rect(152, 274, 180, 282), (60, 140, 200) if heure != "jour" else (90, 120, 150))
    for wx0, wx1 in ((30, 120), (140, 236)):                               # essuie-glaces
        f.fill(f.mask_poly([(wx0, 312), (wx1, 300), (wx1, 303), (wx0, 315)]), (30, 30, 34))
    mirror = f.mask_rrect(112, 84, 158, 98, 4)
    f.shape(mirror, (40, 40, 46), (26, 26, 30), band=1)
    f.fill(f.mask_rect(116, 87, 154, 95), (150, 170, 190))
    f.fill(f.mask_rect(133, 76, 137, 84), (40, 40, 46))
    f.line(135, 98, 135, 110, (60, 60, 60))                                # désodorisant
    tree = f.mask_poly([(135, 110), (141, 122), (137, 122), (142, 130), (128, 130), (133, 122), (129, 122)])
    f.shape(tree, (60, 170, 90), (40, 120, 60), band=1)
    rnd = R(6)
    for k in range(4):                                                     # reflets sur la vitre (pointillés)
        x0 = rnd.randint(30, 220)
        for j in range(22):
            if (j + k) % 3:
                f.px(x0 + j + k * 3, 92 + j * 2, (236, 244, 252))
    if heure == "nuit":
        f.glow(166, 278, 40, (80, 160, 255), 0.4, m=f.al)
    return c, f


# =================================================================== MÉTRO (intérieur)
def metro(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 330)
    c.vgrad(wall, 0, 330, (214, 216, 210), (236, 236, 230), steps=5)
    c.shape(c.mask_rect(0, 0, 270, 18), (240, 240, 236), (206, 206, 200), band=2, sdir="bottom")
    for x in range(10, 270, 60):
        c.fill(c.mask_rect(x, 6, x + 40, 12), (252, 252, 240))
    c.fill(c.mask_rect(0, 40, 270, 44), (190, 194, 204))                   # barre de maintien
    for x in range(20, 270, 34):                                         # poignées
        c.line(x, 44, x, 54, (150, 150, 160))
        c.outline(c.mask_ell(x, 58, 4, 4) & ~c.mask_ell(x, 58, 3, 3), (60, 60, 70))
    strip = c.mask_rect(10, 66, 260, 82)                                   # plan de ligne
    c.fill(strip, (250, 250, 246)); c.outline(strip, (150, 150, 160))
    c.fill(c.mask_rect(18, 73, 252, 75), (240, 190, 40))
    for k, x in enumerate(range(22, 252, 26)):
        c.fill(c.mask_ell(x, 74, 2.5, 2.5), (250, 250, 250)); c.outline(c.mask_ell(x, 74, 2.5, 2.5), (40, 40, 50))
        if k == 4:
            c.fill(c.mask_ell(x, 74, 3.5, 3.5), (220, 50, 50))
    for k, x0 in enumerate((0, 92, 184)):                                 # fenêtres (tunnel)
        w = c.mask_rrect(x0 + 8, 92, x0 + 84, 186, 8)
        c.vgrad(w, 92, 186, (30, 30, 40), (50, 48, 60), steps=3)
        for j in range(4):
            y = 110 + j * 20
            c.fill(w & c.mask_rect(x0 + 8, y, x0 + 84, y + 2), (250, 220, 150) if j % 2 == 0 else (120, 120, 150))
        c.tint(w & c.mask_poly([(x0 + 20, 92), (x0 + 34, 92), (x0 + 18, 186), (x0 + 4, 186)]), (255, 255, 255), 0.12)
        c.outline(w, (120, 124, 134))
        c.shape(c.mask_rect(x0 + 6, 186, x0 + 86, 192), (190, 194, 204), (150, 154, 166), band=1)
    for k, x0 in enumerate((14, 108, 200)):                               # pubs
        ad = c.mask_rect(x0, 196, x0 + 56, 226)
        colr = [(240, 120, 60), (60, 140, 220), (110, 190, 100)][k]
        c.fill(ad, colr); c.fill(c.mask_rect(x0 + 4, 200, x0 + 30, 206), (250, 250, 250))
        c.fill(c.mask_ell(x0 + 44, 214, 8, 8), lt(colr, 0.4)); c.outline(ad, (100, 100, 110))
    # banquettes
    seat = c.mask_rect(0, 236, 270, 302)
    c.fill(seat, (50, 80, 150))
    pat = seat & (((c.xx // 4 + c.yy // 4) % 3) == 0)
    c.fill(pat, (220, 70, 80))
    c.fill(seat & (((c.xx // 4 + c.yy // 4) % 5) == 1), (240, 190, 60))
    for x in range(0, 270, 45):
        c.fill(c.mask_rect(x, 236, x + 2, 302), (36, 56, 110))
    c.shape(c.mask_rect(0, 266, 270, 270), (36, 56, 110), (26, 40, 80), band=1)
    c.shape(c.mask_rect(0, 302, 270, 330), (150, 154, 166), (110, 114, 126), band=2, sdir="bottom")
    # sol
    floor = c.mask_rect(0, 330, 270, 480)
    c.vgrad(floor, 330, 480, (110, 112, 120), (140, 142, 148), steps=4)
    rnd = R(3)
    for _ in range(500):
        c.px(rnd.randrange(270), rnd.randrange(330, 480), rnd.choice([(90, 92, 100), (160, 162, 168), (200, 120, 80)]))
    c.fill(c.mask_rect(0, 330, 270, 334), (230, 200, 60))
    for x in (60, 210):                                                    # barres verticales
        pole = c.mask_rect(x - 2, 44, x + 2, 470)
        c.shape(pole, (210, 214, 224), (150, 156, 170), (250, 252, 255), band=1)
    c.fill(c.mask_rect(56, 466, 64, 472), (150, 156, 170)); c.fill(c.mask_rect(206, 466, 214, 472), (150, 156, 170))
    teinte(c, heure, interieur=True)
    return c, None


# =================================================================== SUPERMARCHÉ (rayon de face)
def supermarche(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 320)
    c.fill(wall, (232, 234, 236))
    for x in range(0, 270, 54):
        c.fill(c.mask_rect(x + 8, 6, x + 46, 12), (252, 252, 246))
    c.fill(c.mask_rect(0, 28, 270, 44), (40, 130, 70))
    c.text((135, 30), "ÉPICERIE", (250, 250, 240), size=9, anchor="ma")
    unit = c.mask_rect(4, 50, 266, 312)                                    # rayonnage
    c.shape(unit, (200, 204, 212), (160, 164, 174), band=2)
    c.fill(c.mask_rect(8, 54, 262, 308), (120, 124, 132))
    rnd = R(17)
    for k, yb in enumerate((96, 142, 188, 234, 280)):
        produits(c, 10, 260, yb - 1, h=22, seed=30 + k, magasin=True)
        c.shape(c.mask_rect(6, yb, 264, yb + 6), (230, 232, 236), (190, 194, 202), band=1, sdir="bottom")
        for x in range(14, 256, 28):                                       # étiquettes de prix
            tg = c.mask_rect(x, yb + 1, x + 12, yb + 5)
            c.fill(tg, (250, 230, 70) if rnd.random() < 0.35 else (252, 252, 252))
            c.fill(c.mask_rect(x + 2, yb + 2, x + 8, yb + 3), (200, 40, 40))
    promo = c.mask_poly([(196, 56), (250, 56), (250, 80), (196, 80)])          # pancarte promo
    c.line(210, 44, 210, 56, (80, 80, 80)); c.line(236, 44, 236, 56, (80, 80, 80))
    c.shape(promo, (250, 210, 40), (210, 160, 20), band=1)
    c.text((223, 62), "PROMO", (210, 30, 40), size=8, anchor="ma")
    # chariot
    cart = c.mask_poly([(14, 300), (64, 300), (60, 330), (20, 330)])
    c.fill(cart & (((c.xx % 4) == 0) | ((c.yy % 4) == 0)), (180, 184, 196))
    c.outline(cart, (120, 124, 136))
    c.fill(c.mask_rect(10, 296, 68, 299), (60, 130, 220))
    produits(c, 22, 58, 312, h=12, seed=4)
    for wx in (24, 54):
        c.shape(c.mask_ell(wx, 336, 3, 3), (40, 40, 46), band=1)
    # sol brillant
    floor = c.mask_rect(0, 320, 270, 480)
    c.vgrad(floor, 320, 480, (206, 206, 200), (226, 226, 220), steps=4)
    yy, xx = c.yy, c.xx
    dz = np.maximum(yy - 250, 1).astype(float); z = 420.0 / dz; xw = (xx - 135) * z / 105.0
    c.fill(floor & ((((xw / 1.2) - np.floor(xw / 1.2)) < 0.03) | (((z / 1.2) - np.floor(z / 1.2)) < 0.03)), (186, 186, 180))
    refl = floor & c.mask_rect(0, 320, 270, 360)
    c.dither(refl, (236, 236, 232), 0.3)
    teinte(c, heure, interieur=True)
    return c, None


# =================================================================== SALLE DE SPORT
def salle_sport(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 316)
    c.vgrad(wall, 0, 316, (60, 62, 70), (84, 86, 94), steps=5)
    c.fill(c.mask_rect(0, 228, 270, 236), (240, 196, 40))
    for x in range(10, 270, 60):
        c.fill(c.mask_rect(x, 6, x + 44, 12), (240, 240, 230)); c.glow(x + 22, 12, 40, (255, 250, 230), 0.15)
    mir = c.mask_rect(62, 40, 252, 220)                                     # grand miroir (reflète la salle)
    c.vgrad(mir, 40, 220, (150, 176, 192), (118, 144, 162), steps=4)
    for x in range(70, 250, 40):                                            # reflet : fenêtres du mur d'en face
        c.fill(mir & c.mask_rect(x, 64, x + 26, 120), (196, 220, 236))
        c.fill(mir & c.mask_rect(x + 12, 64, x + 14, 120), (150, 176, 192))
    for k, x in enumerate(range(70, 250, 34)):                              # reflet : machines (silhouettes claires)
        c.fill(mir & c.mask_rect(x, 160, x + 18, 214), (132, 158, 176))
        c.fill(mir & c.mask_rect(x + 4, 150, x + 14, 160), (132, 158, 176))
    c.fill(mir & c.mask_rect(62, 200, 252, 220), (128, 152, 170))
    for k in range(4):
        c.tint(mir & c.mask_poly([(80 + k * 50, 40), (96 + k * 50, 40), (70 + k * 50, 220), (54 + k * 50, 220)]), (255, 255, 255), 0.14)
    c.outline(mir, (40, 40, 46))
    c.text((157, 46), "NO PAIN NO GAIN", (250, 210, 60), size=10, anchor="ma", ol=(30, 30, 36))
    c.line(32, 14, 32, 60, (90, 90, 96))                                    # sac de frappe
    bag = c.mask_rrect(18, 60, 46, 200, 10)
    c.shape(bag, (200, 40, 46), (150, 24, 34), (232, 90, 90), band=3)
    for y in (90, 170):
        c.fill(bag & c.mask_rect(0, y, 270, y + 4), (40, 40, 46))
    c.fill(c.mask_rect(28, 56, 36, 62), (90, 90, 96))
    rack = c.mask_rect(20, 250, 250, 300)                                   # râtelier d'haltères
    c.shape(rack, (40, 40, 46), (26, 26, 30), band=1)
    for row, y in enumerate((262, 286)):
        c.fill(c.mask_rect(24, y + 6, 246, y + 9), (90, 90, 100))
        for k, x in enumerate(range(30, 240, 22)):
            col_ = [(220, 50, 50), (60, 120, 220), (240, 200, 50), (60, 170, 90)][(k + row) % 4]
            for dx in (0, 12):
                c.shape(c.mask_rect(x + dx, y, x + dx + 5, y + 12), col_, dk(col_, 0.7), lt(col_, 0.3), band=1)
            c.fill(c.mask_rect(x + 5, y + 5, x + 12, y + 7), (180, 184, 196))
    bench = c.mask_rect(196, 306, 262, 314)                                # banc de musculation
    c.shape(bench, (40, 40, 46), (26, 26, 30), (70, 70, 80), band=1)
    c.fill(c.mask_rect(206, 314, 210, 336), (150, 154, 166)); c.fill(c.mask_rect(250, 314, 254, 336), (150, 154, 166))
    for kx in (14, 40):                                                    # kettlebells
        kb = c.mask_ell(kx, 326, 9, 8)
        c.shape(kb, (40, 40, 46), (26, 26, 30), (80, 80, 92), band=1)
        c.outline(c.mask_ell(kx, 314, 6, 6) & ~c.mask_ell(kx, 314, 4, 4) & c.mask_rect(0, 300, 270, 318), (40, 40, 46))
    floor = c.mask_rect(0, 316, 270, 480)
    c.vgrad(floor, 316, 480, (40, 42, 48), (56, 58, 64), steps=4)
    rnd = R(8)
    for _ in range(700):
        c.px(rnd.randrange(270), rnd.randrange(316, 480), rnd.choice([(70, 72, 80), (30, 30, 36), (110, 60, 60)]))
    for y in range(340, 480, 40):
        c.fill(floor & c.mask_rect(0, y, 270, y + 1), (30, 30, 36))
    teinte(c, heure, interieur=True)
    return c, None


# =================================================================== CHAMBRE D'HÔPITAL
def hopital(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 316)
    c.vgrad(wall, 0, 316, (196, 222, 210), (220, 236, 226), steps=5)
    c.shape(c.mask_rect(0, 0, 270, 10), (236, 240, 236), (200, 206, 200), band=2, sdir="bottom")
    win = c.mask_rect(150, 40, 250, 150)
    ciel(c, win, 40, 150, heure, seed=5, astre=(230, 64))
    skyline(c, 150, heure, seed=2, x0=150, x1=250, hmin=20, hmax=60, m=win)
    snap = c.a.copy()
    for y in range(42, 96, 4):                                             # store vénitien
        c.fill(c.mask_rect(150, y, 250, y + 2), (236, 236, 230))
    c.outline(win, (150, 160, 156))
    c.shape(c.mask_rect(144, 150, 256, 156), (236, 240, 236), (200, 206, 200), band=1)
    c.fill(c.mask_rect(0, 26, 140, 29), (170, 176, 186))                   # rideau
    cur = c.mask_rect(4, 29, 60, 300)
    c.fill(cur, (170, 210, 236))
    for x in range(6, 60, 6):
        c.fill(cur & c.mask_rect(x, 29, x + 2, 300), (140, 186, 220))
    for x in range(6, 60, 7):
        c.fill(c.mask_ell(x, 29, 2, 2), (150, 154, 166))
    mon = c.mask_rect(90, 90, 136, 126)                                    # moniteur
    c.shape(mon, (60, 64, 72), (40, 42, 48), band=1)
    sc = c.mask_rect(93, 93, 133, 123)
    c.fill(sc, (14, 30, 24))
    pts = [(93, 110), (104, 110), (107, 102), (110, 118), (113, 106), (116, 110), (133, 110)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1], (80, 250, 140))
    c.text((126, 94), "72", (80, 250, 140), size=6, anchor="ma")
    c.glow(113, 108, 30, (80, 250, 140), 0.2)
    c.fill(c.mask_rect(110, 126, 116, 180), (150, 154, 166))
    c.fill(c.mask_rect(250, 60, 252, 240), (190, 194, 204))               # perfusion
    c.shape(c.mask_rrect(240, 70, 262, 100, 4), (220, 236, 246), (180, 200, 214), band=1)
    c.line(251, 100, 230, 200, (220, 236, 246))
    bed = c.mask_rect(140, 200, 270, 290)                                  # lit
    c.shape(c.mask_rect(256, 150, 266, 300), (200, 204, 214), (160, 164, 176), band=1)
    c.shape(bed, (246, 248, 250), (210, 214, 222), band=2)
    blanket = c.mask_poly([(176, 214), (270, 210), (270, 290), (170, 290)])
    c.shape(blanket, (110, 160, 210), (80, 126, 176), (150, 196, 236), band=2)
    c.shape(c.mask_rrect(146, 200, 186, 218, 5), (252, 252, 252), (214, 216, 224), band=1)
    c.fill(c.mask_rect(140, 290, 270, 296), (160, 164, 176))
    for wx in (150, 256):
        c.fill(c.mask_rect(wx, 296, wx + 4, 316), (150, 154, 166))
    cab = c.mask_rect(70, 230, 116, 300)                                    # chevet + fleurs
    c.shape(cab, (230, 226, 216), (196, 192, 182), band=2)
    c.fill(c.mask_rect(88, 250, 98, 252), (150, 150, 150))
    vase = c.mask_rect(84, 210, 98, 230)
    c.shape(vase, (150, 200, 230), (110, 160, 200), band=1)
    for fx, fy, fc in ((84, 200, (250, 90, 110)), (92, 196, (250, 200, 60)), (99, 202, (250, 130, 170))):
        c.line(fx + 2, fy + 4, 91, 210, (70, 140, 70))
        c.fill(c.mask_ell(fx, fy, 3.5, 3.5), fc)
    floor = c.mask_rect(0, 316, 270, 480)
    sol_carreaux(c, 316, 480, horizon=250, c1=(220, 224, 222), c2=(206, 212, 210), grout=(190, 194, 192), cell=0.9)
    c.shape(c.mask_rect(0, 312, 270, 318), (140, 170, 160), (110, 140, 130), band=1)
    teinte(c, heure, m=~intact(c, snap, win), interieur=True)
    return c, None


# =================================================================== CAFÉ
def cafe(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 312)
    c.fill(wall, (170, 92, 70))                                            # briques
    for y in range(0, 312, 6):
        off = 0 if (y // 6) % 2 == 0 else 7
        c.fill(c.mask_rect(0, y, 270, y + 1), (130, 70, 56))
        for x in range(off, 270, 14):
            c.fill(c.mask_rect(x, y, x + 1, y + 6), (130, 70, 56))
    rnd = R(2)
    for _ in range(40):
        x, y = rnd.randrange(270), rnd.randrange(312)
        c.fill(c.mask_rect(x, y, x + 6, y + 4) & wall, (186, 104, 80))
    win = c.mask_rect(170, 40, 262, 190)                                    # vitrine sur la rue
    ciel(c, win, 40, 190, heure, seed=6, astre=None)
    skyline(c, 190, heure, seed=3, x0=170, x1=262, hmin=40, hmax=110, m=win)
    snap = c.a.copy()
    c.shape(c.mask_rect(166, 36, 266, 42), (60, 40, 30), (40, 26, 20), band=1)
    c.fill(c.mask_rect(214, 40, 217, 190), (60, 40, 30))
    c.outline(win, (40, 26, 20))
    c.text((216, 112), "CAFÉ", (250, 214, 110), size=10, anchor="ma", ol=(60, 40, 30))
    bd = c.mask_rect(14, 30, 120, 120)                                      # menu à la craie
    c.shape(c.mask_rect(10, 26, 124, 124), (110, 76, 46), (80, 54, 32), band=2)
    c.fill(bd, (40, 46, 44))
    for k, (txt, pr) in enumerate((("CAFÉ", "2€"), ("THÉ", "2€"), ("CHOCOLAT", "3€"), ("CROISSANT", "1€"))):
        c.text((20, 38 + k * 19), txt, (236, 236, 226), size=8)
        c.text((112, 38 + k * 19), pr, (250, 214, 110), size=8, anchor="ra")
    for x in range(30, 110, 6):
        c.px(x, 112, (180, 190, 186))
    for k, lx in enumerate((60, 135, 210)):                                # suspensions
        c.line(lx, 0, lx, 22, (40, 30, 30))
        sh = c.mask_poly([(lx - 9, 22), (lx + 9, 22), (lx + 13, 32), (lx - 13, 32)])
        c.shape(sh, (40, 40, 44), (26, 26, 30), band=1)
        c.fill(c.mask_ell(lx, 32, 5, 2), (255, 236, 170))
    sh = c.mask_rect(130, 70, 162, 74)                                      # étagère à tasses
    c.shape(sh, (110, 76, 46), (80, 54, 32), band=1)
    for k, x in enumerate(range(132, 160, 9)):
        mug = c.mask_rect(x, 62, x + 6, 70)
        c.shape(mug, [(250, 250, 246), (60, 140, 120), (230, 180, 60)][k % 3], (180, 180, 180), band=1)
    plante(c, 146, 160, h=24, pot=(240, 240, 236), seed=2, n=10)
    # comptoir + machine à espresso + vitrine à viennoiseries
    counter = c.mask_rect(0, 222, 270, 312)
    c.shape(counter, (120, 80, 52), (90, 58, 36), (150, 104, 70), band=3)
    for x in range(0, 270, 16):
        c.fill(counter & c.mask_rect(x, 232, x + 1, 312), (96, 62, 40))
    c.shape(c.mask_rect(0, 218, 270, 226), (60, 52, 50), (40, 34, 32), (90, 82, 80), band=1, sdir="bottom")
    mach = c.mask_rect(18, 170, 78, 218)
    c.shape(mach, (196, 200, 210), (150, 156, 170), (236, 240, 248), band=2)
    c.fill(c.mask_rect(24, 176, 72, 184), (60, 60, 66))
    for gx in (32, 58):
        c.fill(c.mask_rect(gx - 4, 190, gx + 4, 196), (40, 40, 46))
        c.shape(c.mask_rect(gx - 3, 204, gx + 3, 218), (250, 250, 246), (210, 210, 206), band=1)
        for j in range(3):
            c.px(gx - 1 + (j % 2), 200 - j * 3, (250, 250, 250))
    case = c.mask_rect(100, 186, 164, 218)
    c.fill(case, (210, 230, 236)); c.outline(case, (90, 90, 96))
    for k, x in enumerate(range(106, 160, 14)):
        cr = c.mask_ell(x + 5, 208, 6, 4) & c.mask_rect(0, 0, 270, 211)
        c.shape(cr, (226, 160, 70), (180, 110, 40), (246, 200, 120), band=1)
    c.tint(case & c.mask_poly([(104, 186), (112, 186), (104, 210)]), (255, 255, 255), 0.4)
    floor = c.mask_rect(0, 312, 270, 480)
    planks(c, 312, 480, horizon=240, col=(150, 104, 66), dark=(116, 78, 48), light=(176, 128, 86))
    teinte(c, heure, m=~intact(c, snap, win), interieur=True)
    for lx in (60, 135, 210):
        c.glow(lx, 36, 70, (255, 214, 140), 0.32)
    return c, None


# =================================================================== STUDIO PODCAST (bureau au premier plan)
def studio(heure="nuit"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 330)
    c.fill(wall, (40, 40, 50))
    ox = getattr(c, "ox", 0)
    for ty in range(20, 300, 24):                                          # mousse acoustique
        for tx in range(-((ox + 23) // 24) * 24, 270 + ox, 24):
            tile = c.mask_rect(tx + 1, ty + 1, tx + 23, ty + 23)
            alt = ((tx // 24) + (ty // 24)) % 2
            base = (56, 56, 70) if alt else (48, 48, 62)
            c.fill(tile, base)
            for k in range(0, 22, 4):
                c.fill(tile & c.mask_rect(tx + 1, ty + 1 + k, tx + 23, ty + 2 + k) if alt else tile & c.mask_rect(tx + 1 + k, ty + 1, tx + 2 + k, ty + 23), dk(base, 0.78))
    c.fill(c.mask_rect(0, 0, 270, 20), (26, 26, 34))
    neon = c.mask_rect(70, 52, 200, 54)
    for x in range(70, 200):                                               # néon en vague
        y = int(70 + 8 * math.sin((x - 70) / 130 * 2 * math.pi))
        c.px(x, y, (255, 120, 210)); c.px(x, y + 1, (255, 200, 240))
    c.glow(135, 70, 110, (255, 80, 200), 0.22)
    c.text((135, 92), "LE PODCAST", (120, 230, 255), size=11, anchor="ma", ol=(30, 90, 140))
    c.glow(135, 98, 80, (80, 200, 255), 0.18)
    oa = c.mask_rrect(208, 130, 256, 150, 3)                                # ON AIR
    c.fill(oa, (200, 30, 40)); c.outline(oa, (20, 16, 20))
    c.text((232, 135), "ON AIR", (255, 230, 230), size=7, anchor="ma")
    c.glow(232, 140, 40, (255, 60, 60), 0.35)
    c.shape(c.mask_rect(14, 150, 70, 154), (90, 70, 60), (60, 46, 40), band=1)     # étagère vinyles
    for k, x in enumerate(range(16, 66, 5)):
        c.fill(c.mask_rect(x, 130, x + 4, 150), [(220, 60, 60), (240, 200, 60), (60, 140, 220), (240, 240, 240), (60, 170, 100)][k % 5])
    plante(c, 238, 330, h=50, pot=(40, 40, 46), seed=4)
    for x in range(0, 270):
        c.px(x, 318, mix((255, 60, 200), (60, 220, 255), x / 270))
    c.glow(135, 320, 160, (180, 100, 255), 0.15)
    floor = c.mask_rect(0, 330, 270, 480)
    c.vgrad(floor, 330, 480, (34, 32, 42), (48, 46, 58), steps=3)
    # ---- avant-plan : bureau, micros, casques, tasses
    f = Px(alpha=True)
    desk = f.mask_poly([(0, 300), (270, 300), (270, 480), (0, 480)])
    f.shape(f.mask_rect(0, 300, 270, 312), (150, 106, 70), (110, 76, 48), (186, 140, 96), band=2, sdir="bottom", ldir="top")
    front = f.mask_rect(0, 312, 270, 480)
    f.vgrad(front, 312, 480, (44, 40, 52), (30, 28, 38), steps=3)
    for x in range(0, 270):
        f.px(x, 316, mix((60, 220, 255), (255, 60, 200), x / 270))
    f.text((135, 340), "EP. 12", (200, 200, 220), size=9, anchor="ma")
    for (bx, mx, my) in ((14, 96, 262), (256, 174, 262)):                   # bras + micros
        f.line(bx, 300, bx + (mx - bx) * 0.4, 230, (40, 40, 46))
        f.line(bx + 1, 300, bx + (mx - bx) * 0.4 + 1, 230, (70, 70, 80))
        f.line(bx + (mx - bx) * 0.4, 230, mx, my - 8, (40, 40, 46))
        f.line(bx + (mx - bx) * 0.4 + 1, 230, mx + 1, my - 8, (70, 70, 80))
        mic = f.mask_rrect(mx - 6, my - 12, mx + 6, my + 14, 5)
        f.shape(mic, (50, 50, 58), (30, 30, 36), (100, 100, 114), band=1)
        f.fill(mic & (((f.xx + f.yy) % 2) == 0) & f.mask_rect(0, my - 10, 270, my + 6), (80, 80, 92))
        f.fill(f.mask_rect(mx - 6, my + 6, mx + 6, my + 8), (220, 60, 80))
    hp = f.mask_ell(135, 296, 16, 7) & ~f.mask_ell(135, 296, 12, 4) & f.mask_rect(0, 0, 270, 296)
    f.fill(hp, (30, 30, 36))
    for cx_ in (121, 149):
        f.shape(f.mask_ell(cx_, 297, 4, 3), (230, 60, 80), (170, 30, 50), band=1)
    for mx_, mc in ((48, (250, 250, 246)), (220, (240, 190, 60))):
        mug = f.mask_rect(mx_, 286, mx_ + 10, 300)
        f.shape(mug, mc, dk(mc, 0.8), band=1)
        f.outline(f.mask_ell(mx_ + 12, 293, 3, 4) & ~f.mask_ell(mx_ + 12, 293, 1.5, 2.5), dk(mc, 0.7))
    return c, f


# =================================================================== PLATEAU DU JT (bureau au premier plan)
def plateau_tv(heure="nuit"):
    c = Px()
    bg = c.mask_rect(0, 0, 270, 330)
    c.vgrad(bg, 0, 330, (10, 20, 50), (30, 50, 110), steps=6)
    for k in range(12):                                                     # faisceaux lumineux
        x = 10 + k * 24
        c.tint(c.mask_poly([(x, 0), (x + 6, 0), (x + 30, 330), (x + 18, 330)]), (120, 160, 255), 0.06)
    scr = c.mask_rect(40, 40, 230, 200)                                     # mur d'images : carte du monde
    c.shape(c.mask_rect(36, 36, 234, 204), (30, 34, 46), (20, 22, 30), band=2)
    c.vgrad(scr, 40, 200, (30, 80, 170), (20, 50, 120), steps=4)
    for (ex, ey, erx, ery) in ((84, 92, 22, 20), (96, 138, 12, 22), (138, 84, 14, 12), (146, 120, 16, 24), (186, 96, 30, 18), (204, 150, 12, 9)):
        cont = c.mask_ell(ex, ey, erx, ery) & scr
        c.fill(cont, (80, 150, 230))
        c.fill(cont & (((c.xx + c.yy) % 3) == 0), (110, 180, 250))
    for x in range(40, 230, 16):
        c.fill(scr & c.mask_rect(x, 40, x + 1, 200), (40, 90, 180))
    for y in range(40, 200, 16):
        c.fill(scr & c.mask_rect(40, y, 230, y + 1), (40, 90, 180))
    c.fill(c.mask_ell(146, 118, 3, 3), (255, 80, 80)); c.glow(146, 118, 18, (255, 80, 80), 0.4)
    band_ = c.mask_rect(40, 178, 230, 200)
    c.fill(band_, (200, 30, 50))
    c.text((80, 183), "INFO", (255, 255, 255), size=9, anchor="ma")
    c.fill(c.mask_rect(110, 182, 226, 196), (250, 250, 250))
    c.fill(c.mask_rect(116, 186, 200, 188), (60, 60, 70)); c.fill(c.mask_rect(116, 191, 180, 193), (60, 60, 70))
    for sx in (4, 238):                                                     # écrans latéraux : ville la nuit
        s = c.mask_rect(sx, 60, sx + 28, 220)
        c.fill(s, (16, 18, 40))
        skyline(c, 220, "nuit", seed=sx, x0=sx, x1=sx + 28, hmin=40, hmax=120, m=s)
        c.outline(s, (60, 70, 100))
    c.glow(135, 120, 170, (80, 140, 255), 0.18)
    floor = c.mask_rect(0, 330, 270, 480)
    c.vgrad(floor, 330, 480, (20, 26, 50), (40, 50, 90), steps=4)
    c.dither(floor & c.mask_rect(0, 330, 270, 380), (60, 90, 170), 0.2)
    # ---- avant-plan : bureau du présentateur
    f = Px(alpha=True)
    top = f.mask_poly([(0, 296), (270, 296), (270, 310), (0, 310)])
    f.shape(top, (220, 226, 236), (170, 176, 190), (250, 252, 255), band=2, sdir="bottom", ldir="top")
    front = f.mask_poly([(0, 310), (270, 310), (270, 480), (0, 480)])
    f.vgrad(front, 310, 480, (30, 50, 110), (16, 26, 60), steps=4)
    stripe = f.mask_rect(0, 330, 270, 352)
    f.fill(stripe, (200, 30, 50))
    f.text((135, 334), "LE JOURNAL", (255, 255, 255), size=11, anchor="ma")
    f.fill(f.mask_rect(0, 352, 270, 355), (250, 250, 250))
    for x in range(0, 270, 3):
        f.px(x, 313, (90, 140, 240))
    f.fill(f.mask_rect(196, 286, 236, 296), (250, 250, 246)); f.outline(f.mask_rect(196, 286, 236, 296), (170, 170, 170))
    lap = f.mask_poly([(40, 276), (78, 276), (82, 296), (36, 296)])
    f.shape(lap, (60, 64, 72), (40, 42, 48), band=1)
    f.fill(f.mask_rect(44, 279, 74, 292), (120, 170, 230))
    return c, f


# =================================================================== outils « histoire / nature »
def palmier(c, x, y_base, h=110, lean=14, seed=1, col=(60, 140, 70), trunk=(140, 100, 60)):
    rnd = R(seed)
    pts = [(x + lean * (t ** 1.6), y_base - h * t) for t in np.linspace(0, 1, 26)]
    for i, (px_, py_) in enumerate(pts):
        r = 5.5 - 2.2 * i / len(pts)
        seg = c.mask_ell(px_, py_, r, 2.6)
        c.fill(seg, trunk if i % 2 else dk(trunk, 0.82))
        c.fill(seg & c.mask_rect(px_ + r * 0.3, 0, 270, 480), dk(trunk, 0.7))
    tx, ty = pts[-1]
    for k in range(8):
        a = -math.pi + k * math.pi / 7 + rnd.uniform(-0.15, 0.15)
        L = rnd.randint(30, 44)
        frond = [(tx + math.cos(a) * L * s, ty + math.sin(a) * L * s * 0.6 + (L * s) ** 1.5 * 0.05) for s in np.linspace(0, 1, 10)]
        for j, (fx, fy) in enumerate(frond):
            w = 4.2 * (1 - j / 10) + 0.8
            lf = c.mask_ell(fx, fy, w, w * 0.7)
            c.fill(lf, col if j % 2 else lt(col, 0.18))
            c.fill(lf & c.mask_rect(0, fy + 1, 270, 480), dk(col, 0.72))
    for dx in (-3, 2):
        c.shape(c.mask_ell(tx + dx, ty + 4, 3, 3), (110, 76, 40), (80, 52, 28), band=1)


def dune(c, y_base, amp, wl, phase, col, y1=480, m=None):
    yy, xx = c.yy, c.xx
    top = y_base + amp * np.sin(xx / wl * 2 * math.pi + phase)
    mk = (yy >= top) & (yy < y1)
    if m is not None:
        mk &= m
    c.fill(mk, col)
    slope = np.cos(xx / wl * 2 * math.pi + phase)
    c.fill(mk & (slope > 0.25) & (yy < top + 30), dk(col, 0.86))
    c.fill(mk & (yy < top + 2), lt(col, 0.18))
    return mk


def colonne(c, x, y_top, y_bot, w=14, col=(236, 228, 210), gold=None):
    body = c.mask_rect(x - w // 2, y_top + 8, x + w // 2, y_bot - 6)
    c.shape(body, col, dk(col, 0.8), lt(col, 0.3), band=2)
    for fx in range(x - w // 2 + 3, x + w // 2 - 1, 3):
        c.fill(body & c.mask_rect(fx, y_top + 8, fx + 1, y_bot - 6), dk(col, 0.88))
    cap = c.mask_rect(x - w // 2 - 4, y_top, x + w // 2 + 4, y_top + 8)
    c.shape(cap, gold or col, dk(gold or col, 0.75), lt(gold or col, 0.3), band=1, sdir="bottom")
    base = c.mask_rect(x - w // 2 - 4, y_bot - 6, x + w // 2 + 4, y_bot)
    c.shape(base, col, dk(col, 0.78), band=1)


def torche(c, x, y, on=True):
    c.shape(c.mask_poly([(x - 3, y), (x + 3, y), (x + 1, y + 14), (x - 1, y + 14)]), (110, 76, 46), (80, 52, 30), band=1)
    c.shape(c.mask_rect(x - 5, y - 2, x + 5, y + 2), (150, 120, 60), (110, 86, 40), band=1)
    if on:
        fl = c.mask_ell(x, y - 7, 4, 7)
        c.fill(fl, (250, 140, 40)); c.fill(c.mask_ell(x, y - 5, 2, 4), (255, 230, 130))
        c.glow(x, y - 6, 46, (255, 170, 80), 0.4)


def pavés(c, y0, y1, horizon, col=(150, 140, 130), joint=(110, 100, 94), cx=135):
    yy, xx = c.yy, c.xx
    m = c.mask_rect(0, y0, 270, y1)
    dz = np.maximum(yy - horizon, 1).astype(float); z = 420.0 / dz; xw = (xx - cx) * z / 105.0
    row = np.floor(z / 0.45)
    off = (row % 2) * 0.3
    img = np.zeros((c.h, c.w, 3)); img[:] = col
    c.a[m] = img[m].astype(np.uint8)
    rnd = np.random.default_rng(3)
    shade = rnd.uniform(-14, 14, (300, 300))
    ri = np.clip(row.astype(int) % 300, 0, 299)
    ci = np.clip(np.floor((xw + off) / 0.6).astype(int) % 300, 0, 299)
    var = shade[ri, ci]
    a = c.a.astype(float)
    a[m] = np.clip(a[m] + var[m][:, None], 0, 255)
    c.a = a.astype(np.uint8)
    joints = m & (((z / 0.45) - row < 0.09) | ((((xw + off) / 0.6) - np.floor((xw + off) / 0.6)) < 0.07))
    c.fill(joints, joint)


# =================================================================== DÉSERT (jour / nuit)
def desert(heure="jour"):
    c = Px()
    sky = c.mask_rect(0, 0, 270, 300)
    ciel(c, sky, 0, 260, heure, seed=2, astre=(206, 70), nuages=False)
    if heure == "nuit":
        c.fill(c.mask_ell(206, 70, 16, 16), (250, 244, 214)); c.glow(206, 70, 60, (220, 220, 255), 0.2)
    snap = c.a.copy()
    sand = dict(jour=[(232, 196, 136), (222, 180, 120), (214, 168, 106), (236, 204, 146)],
                soir=[(220, 150, 110), (206, 130, 96), (196, 120, 86), (230, 166, 120)],
                nuit=[(70, 70, 110), (62, 60, 98), (54, 54, 88), (80, 78, 120)])[heure]
    dune(c, 196, 10, 180, 0.4, sand[0])
    dune(c, 222, 14, 240, 2.2, sand[1])
    for k, x in enumerate((40, 70)):                                       # chameaux au loin
        cam = c.mask_ell(x, 214, 7, 3) | c.mask_ell(x - 1, 210, 3, 3) | c.mask_poly([(x + 5, 214), (x + 9, 205), (x + 11, 206), (x + 8, 215)])
        cam |= c.mask_rect(x - 5, 215, x - 4, 222) | c.mask_rect(x + 3, 215, x + 4, 222)
        c.fill(cam, dk(sand[1], 0.55))
    # oasis : palmiers + eau
    pond = c.mask_ell(60, 268, 50, 9)
    c.fill(pond, (80, 150, 200) if heure != "nuit" else (40, 60, 110))
    c.fill(pond & c.mask_rect(0, 262, 270, 265), (150, 200, 230) if heure != "nuit" else (90, 100, 160))
    pc = (60, 140, 70) if heure != "nuit" else (30, 50, 60)
    palmier(c, 36, 270, h=120, lean=10, seed=1, col=pc)
    palmier(c, 78, 266, h=96, lean=-16, seed=2, col=pc)
    # tentes
    for tx, tw, tc in ((176, 52, (120, 70, 50)), (230, 40, (150, 90, 60))):
        tent = c.mask_poly([(tx - tw // 2, 270), (tx + tw // 2, 270), (tx + tw // 2 - 6, 236), (tx, 226), (tx - tw // 2 + 6, 236)])
        tcol = tc if heure != "nuit" else dk(tc, 0.5)
        c.shape(tent, tcol, dk(tcol, 0.7), lt(tcol, 0.25), band=2)
        for k in range(3):
            c.fill(tent & c.mask_rect(0, 240 + k * 9, 270, 242 + k * 9), (220, 180, 120) if heure != "nuit" else (90, 80, 90))
        c.fill(c.mask_poly([(tx - 5, 270), (tx + 5, 270), (tx, 246)]), (40, 26, 20))
    dune(c, 262, 8, 300, 1.0, sand[2])
    ground = dune(c, 292, 6, 360, 3.0, sand[3])
    rnd = R(4)
    for k in range(18):                                                      # rides du sable
        y = rnd.randint(320, 470); x = rnd.randint(-20, 250)
        for j in range(30):
            c.px(x + j, y + int(2 * math.sin(j / 5)), dk(sand[3], 0.88))
    if heure == "nuit":
        fx, fy = 135, 378                                                    # feu de camp (devant les personnages)
        for a in (-0.4, 0.4):
            c.fill(c.mask_poly([(fx - 14, fy + 4 + a * 6), (fx + 14, fy + 4 - a * 6), (fx + 14, fy + 8 - a * 6), (fx - 14, fy + 8 + a * 6)]), (90, 60, 40))
        c.fill(c.mask_ell(fx, fy - 6, 7, 11), (250, 130, 40)); c.fill(c.mask_ell(fx, fy - 3, 4, 7), (255, 220, 120))
        c.glow(fx, fy - 4, 120, (255, 160, 70), 0.35)
    return relief(c, snap, sky), None


# =================================================================== PALAIS (salle du trône)
def palais(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 320)
    c.vgrad(wall, 0, 320, (120, 40, 50), (160, 70, 70), steps=5)
    for x in range(0, 270, 18):                                             # tenture à motif
        c.fill(wall & c.mask_rect(x + 8, 0, x + 9, 300), (140, 56, 60))
    for y in range(20, 300, 30):
        for x in range(9, 270, 18):
            c.fill(c.mask_poly([(x, y - 3), (x + 3, y), (x, y + 3), (x - 3, y)]), (200, 150, 70))
    # arche dorée + trône
    arch = c.mask_arch(70, 200, 40, 320)
    c.shape(arch, (90, 30, 40), (60, 20, 30), band=2)
    c.fill(c.mask_arch(70, 200, 40, 320) & ~c.mask_arch(76, 194, 46, 321), (220, 176, 80))
    win = c.mask_arch(110, 160, 60, 160)
    c.vgrad(win, 60, 160, (170, 210, 250), (240, 220, 180), steps=4)
    c.fill(win & c.mask_rect(134, 60, 136, 160), (200, 160, 70)); c.fill(win & c.mask_rect(110, 110, 160, 112), (200, 160, 70))
    c.outline(win, (200, 160, 70))
    c.glow(135, 110, 70, (255, 240, 200), 0.25)
    dais = c.mask_rect(80, 286, 190, 300) | c.mask_rect(70, 300, 200, 312)
    c.shape(dais, (210, 200, 186), (170, 160, 146), (236, 230, 220), band=2, sdir="bottom")
    throne = c.mask_poly([(108, 286), (162, 286), (162, 216), (150, 200), (135, 186), (120, 200), (108, 216)])
    c.shape(throne, (220, 176, 70), (170, 124, 40), (250, 220, 130), band=3)
    seat = c.mask_rect(116, 214, 154, 286)
    c.shape(seat, (170, 30, 50), (120, 20, 36), (210, 70, 80), band=2)
    c.fill(c.mask_ell(135, 200, 5, 5), (60, 120, 220)); c.outline(c.mask_ell(135, 200, 5, 5), (170, 124, 40))
    for x0 in (100, 162):
        arm = c.mask_rect(x0, 250, x0 + 8, 286)
        c.shape(arm, (220, 176, 70), (170, 124, 40), band=1)
    # bannières
    for bx in (34, 236):
        c.fill(c.mask_rect(bx - 16, 30, bx + 16, 33), (200, 160, 70))
        ban = c.mask_poly([(bx - 14, 33), (bx + 14, 33), (bx + 14, 130), (bx, 116), (bx - 14, 130)])
        c.shape(ban, (40, 60, 130), (26, 40, 90), (70, 90, 170), band=2)
        c.fill(c.mask_poly([(bx, 56), (bx + 8, 72), (bx, 88), (bx - 8, 72)]), (226, 186, 80))
        c.fill(c.mask_poly([(bx, 64), (bx + 4, 72), (bx, 80), (bx - 4, 72)]), (40, 60, 130))
    # colonnes au premier plan
    for x in (16, 254):
        colonne(c, x, 150, 330, w=20, col=(236, 228, 212), gold=(220, 176, 80))
    for x in (40, 230):
        torche(c, x, 176)
    # sol de marbre + tapis rouge
    sol_carreaux(c, 320, 480, horizon=240, c1=(226, 220, 206), c2=(170, 160, 150), grout=(200, 190, 176), cell=0.9)
    carpet = c.mask_poly([(108, 312), (162, 312), (214, 480), (56, 480)])
    c.fill(carpet, (180, 30, 50))
    c.fill(carpet & ~c.mask_poly([(112, 312), (158, 312), (206, 480), (64, 480)]), (220, 176, 80))
    c.dither(carpet & c.mask_poly([(118, 312), (152, 312), (190, 480), (80, 480)]), (160, 24, 44), 0.25)
    c.glow(135, 120, 240, (255, 210, 150), 0.12)
    return c, None


# =================================================================== BIBLIOTHÈQUE ANCIENNE
def bibliotheque(heure="soir"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 320)
    c.vgrad(wall, 0, 320, (70, 44, 34), (110, 74, 52), steps=5)
    win = c.mask_arch(100, 170, 30, 170)                                    # fenêtre ronde
    c.vgrad(win, 30, 170, (230, 200, 150) if heure != "nuit" else (30, 40, 90), (250, 230, 190) if heure != "nuit" else (60, 60, 120), steps=4)
    for x in range(100, 170, 12):
        c.fill(win & c.mask_rect(x, 30, x + 1, 170), (80, 50, 34))
    for y in range(40, 170, 14):
        c.fill(win & c.mask_rect(100, y, 170, y + 1), (80, 50, 34))
    c.outline(win, (60, 36, 26))
    if heure != "nuit":
        ray = c.mask_poly([(100, 170), (170, 170), (200, 480), (60, 480)])
        c.tint(ray, (255, 236, 190), 0.10)
    for x0, x1 in ((0, 92), (178, 270)):                                    # grandes bibliothèques
        sh = c.mask_rect(x0, 10, x1, 316)
        c.shape(sh, (100, 62, 38), (72, 42, 26), (130, 86, 56), band=3)
        c.fill(c.mask_rect(x0 + 4, 14, x1 - 4, 312), (52, 32, 22))
        for k, yb in enumerate(range(50, 316, 40)):
            books(c, x0 + 5, x1 - 5, yb - 1, 24, 34, seed=x0 + k)
            c.shape(c.mask_rect(x0 + 2, yb - 1, x1 - 2, yb + 3), (120, 78, 48), (90, 56, 34), (150, 104, 66), band=1, sdir="bottom")
    lad = c.mask_rect(196, 40, 200, 320) | c.mask_rect(220, 40, 224, 320)    # échelle
    c.fill(lad, (150, 100, 60))
    for y in range(52, 320, 16):
        c.fill(c.mask_rect(196, y, 224, y + 2), (150, 100, 60))
    c.outline(lad, (60, 36, 26))
    c.fill(c.mask_rect(92, 8, 178, 12), (120, 78, 48))
    planks(c, 316, 480, horizon=240, col=(120, 78, 50), dark=(90, 56, 34), light=(146, 100, 66))
    rug = c.mask_poly([(60, 340), (210, 340), (250, 480), (20, 480)])
    c.fill(rug, (120, 30, 40)); c.fill(rug & ~c.mask_poly([(66, 344), (204, 344), (240, 480), (30, 480)]), (200, 160, 80))
    # table de lecture + bougie + livre ouvert + globe
    tbl = c.mask_rect(96, 270, 176, 278)
    c.shape(tbl, (140, 90, 54), (100, 62, 36), (170, 120, 76), band=1)
    for lx in (100, 168):
        c.fill(c.mask_rect(lx, 278, lx + 5, 320), (100, 62, 36))
    bk = c.mask_poly([(112, 268), (134, 264), (136, 270), (112, 270)]) | c.mask_poly([(136, 264), (158, 268), (158, 270), (136, 270)])
    c.fill(bk, (240, 230, 200)); c.outline(bk, (120, 100, 80))
    c.fill(c.mask_rect(164, 252, 168, 270), (240, 236, 220)); c.fill(c.mask_ell(166, 248, 2, 3), (255, 200, 90))
    c.glow(166, 250, 60, (255, 200, 110), 0.4)
    gl = c.mask_ell(104, 254, 8, 8)
    c.fill(gl, (200, 170, 110)); c.fill(gl & c.mask_ell(101, 251, 4, 3), (110, 140, 90)); c.outline(gl, (90, 60, 30))
    c.fill(c.mask_rect(103, 262, 106, 270), (120, 80, 40))
    chandelier(c, 135, 40, chain_y=12, rx=28, ry=6)
    teinte(c, heure, interieur=True) if heure == "nuit" else None
    return c, None


# =================================================================== LABORATOIRE
def labo(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 300)
    carrelage_mur(c, wall, 12, (226, 234, 236), (196, 206, 210), seed=2)
    bd = c.mask_rect(20, 30, 150, 120)                                       # tableau de formules
    c.shape(c.mask_rect(16, 26, 154, 124), (120, 86, 56), (90, 62, 40), band=2)
    c.fill(bd, (40, 60, 52))
    c.text((30, 38), "E = mc²", (240, 240, 230), size=11)
    c.text((30, 62), "H2O", (240, 220, 140), size=9)
    c.line(30, 84, 80, 84, (200, 210, 200)); c.line(80, 84, 90, 76, (200, 210, 200)); c.line(90, 76, 110, 96, (200, 210, 200))
    c.outline(c.mask_ell(126, 62, 10, 10) & ~c.mask_ell(126, 62, 9, 9), (200, 210, 200))
    for a in range(3):
        ang = a * 2.1
        c.outline(c.mask_ell(126, 62, 14, 5) & ~c.mask_ell(126, 62, 13, 4), (150, 200, 240)) if a == 0 else None
    c.fill(c.mask_ell(126, 62, 2, 2), (240, 120, 120))
    sh = c.mask_rect(170, 40, 262, 44)                                       # étagère à bocaux
    for yb in (80, 130):
        c.shape(c.mask_rect(170, yb, 262, yb + 4), (150, 156, 168), (110, 116, 130), band=1)
        for k, x in enumerate(range(174, 258, 14)):
            j = c.mask_rect(x, yb - 16, x + 10, yb) | c.mask_rect(x + 2, yb - 19, x + 8, yb - 16)
            c.fill(j, (210, 236, 246)); c.outline(j, (120, 140, 150))
            c.fill(c.mask_rect(x + 1, yb - 9, x + 9, yb - 1), [(120, 220, 120), (240, 120, 200), (120, 180, 250), (250, 210, 90)][k % 4])
    bench = c.mask_rect(0, 226, 270, 236)                                   # paillasse
    c.shape(bench, (40, 44, 50), (26, 28, 32), (70, 74, 84), band=1, sdir="bottom")
    c.shape(c.mask_rect(0, 236, 270, 306), (220, 222, 226), (180, 184, 190), band=2)
    for x in range(0, 270, 54):
        c.fill(c.mask_rect(x + 4, 240, x + 50, 302), (206, 208, 214)); c.fill(c.mask_rect(x + 24, 260, x + 30, 262), (120, 124, 134))
    flasks = [(30, (120, 230, 140)), (60, (240, 110, 200)), (210, (110, 180, 250)), (240, (250, 200, 80))]
    for fx, fc in flasks:                                                     # erlenmeyers bouillonnants
        fl = c.mask_poly([(fx - 9, 226), (fx + 9, 226), (fx + 3, 206), (fx + 3, 196), (fx - 3, 196), (fx - 3, 206)])
        c.fill(fl, (220, 240, 248)); c.outline(fl, (120, 140, 150))
        liq = fl & c.mask_rect(0, 212, 270, 226)
        c.fill(liq, fc)
        for b in range(3):
            c.px(fx - 2 + b * 2, 208 - b * 3, lt(fc, 0.5))
        c.glow(fx, 218, 24, fc, 0.3)
    mic = c.mask_rect(96, 200, 104, 226) | c.mask_rect(90, 222, 116, 226) | c.mask_poly([(100, 196), (112, 186), (116, 190), (104, 200)])
    c.shape(mic, (60, 64, 72), (40, 42, 48), (100, 104, 116), band=1)      # microscope
    c.fill(c.mask_rect(110, 182, 118, 188), (60, 64, 72))
    coil = c.mask_rect(150, 150, 166, 226)                                    # bobine électrique
    c.shape(coil, (190, 120, 60), (140, 80, 36), (226, 170, 100), band=1)
    for y in range(152, 226, 3):
        c.fill(c.mask_rect(150, y, 166, y + 1), (150, 90, 40))
    c.shape(c.mask_ell(158, 146, 12, 6), (196, 200, 210), (140, 146, 160), band=1)
    rnd = R(9)
    for k in range(5):
        x, y = 158, 142
        for j in range(8):
            x2, y2 = x + rnd.randint(-5, 5), y - rnd.randint(2, 5)
            c.line(x, y, x2, y2, (220, 180, 255)); x, y = x2, y2
    c.glow(158, 130, 50, (180, 120, 255), 0.35)
    sol_carreaux(c, 306, 480, horizon=250, c1=(214, 218, 220), c2=(190, 196, 200), grout=(170, 176, 180), cell=0.9)
    teinte(c, heure, interieur=True)
    return c, None


# =================================================================== VILLAGE D'AUTREFOIS
def maison(c, x0, x1, y_base, h, wall=(236, 226, 200), beam=(100, 66, 40), roof=(170, 70, 50), side=1, seed=1):
    rnd = R(seed)
    body = c.mask_rect(x0, y_base - h, x1, y_base)
    c.shape(body, wall, dk(wall, 0.85), band=2, sdir="right" if side > 0 else "left")
    for x in range(x0, x1, 14):
        c.fill(body & c.mask_rect(x, y_base - h, x + 2, y_base), beam)
    for y in (y_base - h, y_base - h // 2):
        c.fill(body & c.mask_rect(x0, y, x1, y + 2), beam)
    for k in range((x1 - x0) // 22):
        x = x0 + 4 + k * 22
        c.fill(body & c.mask_poly([(x, y_base - h + 2), (x + 12, y_base - h // 2), (x + 10, y_base - h // 2), (x - 2, y_base - h + 2)]), beam)
    for k in range((x1 - x0) // 30):
        wx = x0 + 10 + k * 30
        w = c.mask_rect(wx, y_base - h + 10, wx + 12, y_base - h + 24)
        c.fill(w, (90, 120, 150)); c.fill(c.mask_rect(wx + 5, y_base - h + 10, wx + 6, y_base - h + 24), beam); c.outline(w, beam)
    rf = c.mask_poly([(x0 - 6, y_base - h), (x1 + 6, y_base - h), ((x0 + x1) / 2, y_base - h - (x1 - x0) * 0.45)])
    c.shape(rf, roof, dk(roof, 0.7), lt(roof, 0.2), band=2)
    for y in range(int(y_base - h - (x1 - x0) * 0.45) + 4, y_base - h, 4):
        c.fill(rf & c.mask_rect(0, y, 270, y + 1), dk(roof, 0.82))
    door = c.mask_arch((x0 + x1) // 2 - 7, (x0 + x1) // 2 + 7, y_base - 26, y_base)
    c.shape(door, (110, 70, 40), (80, 50, 28), band=1)


def village(heure="jour"):
    c = Px()
    sky = c.mask_rect(0, 0, 270, 260)
    ciel(c, sky, 0, 220, heure, seed=5, astre=(220, 40))
    hill = c.mask_ell(150, 250, 160, 70)
    c.fill(hill & c.mask_rect(0, 0, 270, 260), (110, 160, 90) if heure == "jour" else (120, 120, 80))
    cast_ = c.mask_rect(120, 150, 180, 196)                                  # château au loin
    stone = (170, 166, 176) if heure == "jour" else (160, 120, 120)
    c.shape(cast_, stone, dk(stone, 0.8), band=1)
    for tx in (116, 176):
        t = c.mask_rect(tx - 7, 130, tx + 7, 196)
        c.shape(t, stone, dk(stone, 0.8), band=1)
        c.fill(c.mask_poly([(tx - 9, 130), (tx + 9, 130), (tx, 112)]), (60, 70, 130))
    for x in range(120, 180, 6):
        c.fill(c.mask_rect(x, 146, x + 3, 150), stone)
    c.fill(c.mask_arch(143, 157, 176, 196), (60, 50, 50))
    c.line(116, 112, 116, 104, (60, 50, 50)); c.fill(c.mask_rect(117, 104, 124, 108), (200, 40, 40))
    snap = c.a.copy()
    maison(c, -10, 70, 304, 120, seed=1)
    maison(c, 60, 104, 296, 76, wall=(226, 214, 180), roof=(150, 90, 60), seed=2)
    maison(c, 196, 280, 306, 130, wall=(240, 230, 210), roof=(130, 60, 50), side=-1, seed=3)
    maison(c, 160, 204, 296, 80, wall=(220, 206, 170), roof=(170, 100, 60), side=-1, seed=4)
    well = c.mask_rect(116, 280, 154, 306)                                    # puits
    c.shape(well, (150, 144, 136), (110, 104, 98), band=2)
    for y in (286, 294):
        c.fill(well & c.mask_rect(0, y, 270, y + 1), (110, 104, 98))
    for x in (118, 150):
        c.fill(c.mask_rect(x, 254, x + 3, 280), (100, 66, 40))
    c.shape(c.mask_poly([(112, 256), (158, 256), (135, 242)]), (150, 70, 50), (110, 50, 34), band=1)
    stall = c.mask_rect(76, 300, 112, 316)                                    # étal de fruits
    c.shape(stall, (130, 90, 56), (96, 64, 38), band=1)
    for k, x in enumerate(range(79, 110, 6)):
        c.fill(c.mask_ell(x, 298, 3, 3), [(220, 50, 40), (240, 180, 40), (120, 180, 60)][k % 3])
    pavés(c, 304, 480, horizon=230)
    teinte(c, heure, m=~intact(c, snap, sky) & ~c.mask_rect(0, 0, 270, 110))
    return relief(c, snap, sky), None


# =================================================================== TEMPLE ANTIQUE
def temple(heure="jour"):
    c = Px()
    sky = c.mask_rect(0, 0, 270, 320)
    ciel(c, sky, 0, 260, heure, seed=7, astre=(40, 50))
    snap = c.a.copy()
    stone = (236, 226, 204) if heure == "jour" else (240, 196, 160)
    ped = c.mask_poly([(40, 112), (230, 112), (135, 60)])                     # fronton
    c.shape(ped, stone, dk(stone, 0.82), lt(stone, 0.3), band=2)
    c.fill(c.mask_poly([(60, 108), (210, 108), (135, 70)]), dk(stone, 0.9))
    c.shape(c.mask_rect(34, 112, 236, 126), stone, dk(stone, 0.8), band=2, sdir="bottom")
    for x in range(40, 232, 8):
        c.fill(c.mask_rect(x, 118, x + 4, 122), dk(stone, 0.85))
    c.fill(c.mask_rect(40, 126, 230, 270), dk(stone, 0.62))                   # intérieur sombre
    for x in (54, 88, 122, 148, 182, 216):
        colonne(c, x, 126, 270, w=16, col=stone)
    for k in range(3):                                                         # marches
        st = c.mask_rect(26 - k * 10, 270 + k * 10, 244 + k * 10, 280 + k * 10)
        c.shape(st, stone, dk(stone, 0.8), lt(stone, 0.2), band=2, sdir="bottom", ldir="top")
    for x, h in ((8, 120), (262, 90)):                                         # colonnes en ruine
        colonne(c, x, 300 - h, 300, w=14, col=dk(stone, 0.95))
    for tx in (20, 250):
        c.fill(c.mask_rect(tx - 2, 250, tx + 2, 300), (110, 90, 60))
        for k in range(6):
            c.fill(c.mask_ell(tx + (k - 3) * 6, 236 + (k % 2) * 6, 9, 6), (120, 140, 90) if heure == "jour" else (140, 120, 80))
    floor = c.mask_rect(0, 300, 270, 480)
    sol_carreaux(c, 300, 480, horizon=230, c1=lt(stone, 0.1), c2=dk(stone, 0.9), grout=dk(stone, 0.78), cell=1.1)
    teinte(c, heure, m=~intact(c, snap, sky))
    return relief(c, snap, sky), None


# =================================================================== TOIT (nuit)
def toit(heure="nuit"):
    c = Px()
    sky = c.mask_rect(0, 0, 270, 330)
    ciel(c, sky, 0, 300, heure, seed=11, astre=(60, 60), nuages=heure == "soir")
    skyline(c, 270, heure, seed=22, hmin=50, hmax=190)
    skyline(c, 300, heure, seed=23, hmin=30, hmax=120)
    snap = c.a.copy()
    tank = c.mask_rect(204, 150, 250, 230)                                    # château d'eau
    c.shape(tank, (100, 70, 60), (70, 50, 44), (130, 96, 80), band=2)
    for y in range(156, 230, 8):
        c.fill(tank & c.mask_rect(0, y, 270, y + 1), (80, 56, 48))
    c.fill(c.mask_poly([(200, 150), (254, 150), (227, 132)]), (70, 50, 44))
    for x in (208, 244):
        c.fill(c.mask_rect(x, 230, x + 3, 300), (60, 50, 50))
    c.line(30, 300, 30, 200, (90, 90, 100)); c.line(22, 220, 38, 220, (90, 90, 100)); c.line(25, 236, 35, 236, (90, 90, 100))
    wall = c.mask_rect(0, 300, 270, 330)                                      # parapet
    c.shape(wall, (120, 110, 110), (90, 82, 84), (150, 140, 140), band=2, sdir="bottom", ldir="top")
    for x in range(0, 270, 20):
        c.fill(wall & c.mask_rect(x, 300, x + 1, 330), (96, 88, 90))
    floor = c.mask_rect(0, 330, 270, 480)
    c.vgrad(floor, 330, 480, (90, 86, 92), (110, 106, 112), steps=4)
    rnd = R(5)
    for _ in range(700):
        c.px(rnd.randrange(270), rnd.randrange(330, 480), rnd.choice([(70, 66, 72), (130, 126, 132)]))
    teinte(c, heure, m=~intact(c, snap, sky))
    for k in range(22):                                                       # guirlande d'ampoules
        x = k * 13
        y = int(100 + 22 * math.sin((x / 270) * math.pi))
        c.px(x, y - 2, (60, 50, 50))
        if k:
            c.line(x - 13, int(100 + 22 * math.sin(((x - 13) / 270) * math.pi)), x, y, (50, 44, 44))
        c.fill(c.mask_ell(x, y + 2, 2, 2.5), (255, 226, 150))
        c.glow(x, y + 2, 12, (255, 210, 120), 0.4)
    return relief(c, snap, sky), None


# =================================================================== FORÊT (nuit + feu de camp)
def foret(heure="nuit"):
    c = Px()
    sky = c.mask_rect(0, 0, 270, 300)
    ciel(c, sky, 0, 260, heure, seed=3, astre=(200, 50), nuages=heure == "jour")
    snap = c.a.copy()
    rnd = R(6)
    pal = dict(nuit=[(30, 50, 70), (24, 40, 56), (18, 30, 42)], jour=[(110, 160, 120), (70, 130, 80), (40, 96, 60)],
               soir=[(110, 90, 100), (80, 70, 80), (56, 50, 60)])[heure]
    ox = getattr(c, "ox", 0)
    for layer, (yb, n, hmin, hmax) in enumerate(((240, 14, 70, 120), (270, 10, 90, 150), (300, 7, 120, 190))):
        col_ = pal[layer]
        for k in range(int(n * (270 + 2 * ox) / 270)):
            x = rnd.randint(-10 - ox, 280 + ox); h = rnd.randint(hmin, hmax)
            tri = np.zeros((c.h, c.w), bool)
            for j in range(4):                                                 # sapin en étages
                y0 = yb - h + j * h * 0.22
                w = (j + 1) * h * 0.09
                tri |= c.mask_poly([(x - w, y0 + h * 0.3), (x + w, y0 + h * 0.3), (x, y0)])
            c.fill(tri, col_)
            c.fill(tri & c.mask_rect(x, 0, 270, 480), dk(col_, 0.82))
            c.fill(c.mask_rect(x - 2, yb - h * 0.12, x + 2, yb), dk(col_, 0.7))
    ground = c.mask_rect(0, 290, 270, 480)
    c.vgrad(ground, 290, 480, dict(nuit=(26, 40, 40), jour=(90, 130, 70), soir=(80, 70, 60))[heure],
            dict(nuit=(40, 54, 50), jour=(110, 150, 84), soir=(100, 86, 70))[heure], steps=4)
    for _ in range(500):
        c.px(rnd.randrange(270), rnd.randrange(292, 480), lt(pal[0], 0.15) if rnd.random() < 0.5 else dk(pal[0], 0.8))
    if heure == "nuit":
        for y0_, k_ in ((262, 0.08), (272, 0.14), (282, 0.2)):                # brume légère au pied des arbres
            c.dither(c.mask_rect(0, y0_, 270, y0_ + 10), (70, 92, 110), k_)
        for _ in range(16):                                                      # lucioles
            x, y = rnd.randint(10, 260), rnd.randint(150, 300)
            c.px(x, y, (220, 255, 140)); c.glow(x, y, 6, (200, 255, 120), 0.5)
    for lx, ly, a in ((40, 330, 0.2), (210, 338, -0.15)):                     # rondins pour s'asseoir
        log = c.mask_poly([(lx - 28, ly - 6 + a * 20), (lx + 28, ly - 6 - a * 20), (lx + 28, ly + 6 - a * 20), (lx - 28, ly + 6 + a * 20)])
        c.shape(log, (110, 74, 46), (80, 52, 32), (140, 100, 64), band=2)
        c.fill(c.mask_ell(lx + 28, ly - a * 20, 4, 6), (190, 150, 100))
    fx, fy = 135, 372                                                        # feu de camp
    for k in range(8):
        a = k / 8 * 2 * math.pi
        c.shape(c.mask_ell(fx + math.cos(a) * 18, fy + math.sin(a) * 6, 5, 3.5), (120, 116, 112), (86, 84, 82), band=1)
    for a in (-0.5, 0.5):
        c.fill(c.mask_poly([(fx - 16, fy + a * 6), (fx + 16, fy - a * 6), (fx + 16, fy + 4 - a * 6), (fx - 16, fy + 4 + a * 6)]), (100, 64, 40))
    if heure != "jour":
        c.fill(c.mask_ell(fx, fy - 12, 9, 15), (250, 120, 40))
        c.fill(c.mask_ell(fx, fy - 9, 6, 10), (255, 190, 80)); c.fill(c.mask_ell(fx, fy - 6, 3, 6), (255, 244, 180))
        for k in range(6):
            c.px(fx + rnd.randint(-10, 10), fy - 30 - rnd.randint(0, 30), (255, 200, 100))
        c.glow(fx, fy - 10, 170, (255, 150, 70), 0.38)
    teinte(c, heure, m=~intact(c, snap, sky) & c.mask_rect(0, 0, 270, 250)) if heure == "soir" else None
    return relief(c, snap, sky), None


# =================================================================== STATION SPATIALE
def espace(heure="nuit"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 320)
    c.vgrad(wall, 0, 320, (60, 70, 90), (90, 100, 120), steps=5)
    for x in range(0, 270, 45):                                              # panneaux + rivets
        for y in range(0, 320, 60):
            p = c.mask_rect(x + 2, y + 2, x + 43, y + 58)
            c.fill(p, (74, 84, 104)); c.outline(p, (44, 50, 64))
            for (rx, ry) in ((x + 5, y + 5), (x + 39, y + 5), (x + 5, y + 54), (x + 39, y + 54)):
                c.px(rx, ry, (140, 150, 170))
    port = c.mask_ell(135, 130, 76, 76)                                      # hublot : la Terre
    c.fill(port, (4, 6, 20))
    rnd = R(12)
    for _ in range(80):
        x, y = rnd.randint(60, 210), rnd.randint(54, 206)
        if port[y, x]:
            c.px(x, y, (230, 230, 255) if rnd.random() < 0.5 else (140, 140, 200))
    earth = c.mask_ell(160, 230, 110, 110) & port
    c.rgrad(earth, 140, 200, 120, (80, 150, 240), (20, 60, 150), steps=5)
    for (ex, ey, erx, ery) in ((120, 160, 26, 12), (170, 180, 30, 16), (140, 196, 16, 8), (200, 160, 18, 10)):
        c.fill(c.mask_ell(ex, ey, erx, ery) & earth, (80, 170, 100))
    for (cx_, cy_, w_) in ((100, 150, 40), (180, 140, 36), (150, 176, 30)):
        c.dither(c.mask_ell(cx_, cy_, w_ * 0.5, 4) & earth, (250, 250, 255), 0.6)
    c.glow(160, 230, 120, (100, 180, 255), 0.2, m=port & ~earth)
    ring = c.mask_ell(135, 130, 84, 84) & ~port
    c.shape(ring, (150, 160, 180), (100, 110, 130), (200, 210, 226), band=3)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        c.fill(c.mask_ell(135 + math.cos(a) * 80, 130 + math.sin(a) * 80, 2, 2), (90, 100, 120))
    for x0 in (8, 214):                                                       # consoles
        con = c.mask_rect(x0, 220, x0 + 48, 300)
        c.shape(con, (50, 56, 70), (34, 38, 48), (80, 88, 106), band=2)
        c.fill(c.mask_rect(x0 + 6, 228, x0 + 42, 250), (20, 40, 60))
        for k in range(8):
            c.fill(c.mask_rect(x0 + 8 + (k % 4) * 9, 258 + (k // 4) * 10, x0 + 13 + (k % 4) * 9, 262 + (k // 4) * 10),
                   rnd.choice([(250, 80, 80), (80, 250, 140), (250, 210, 80), (90, 170, 250)]))
        c.line(x0 + 8, 244, x0 + 40, 234, (90, 220, 250))
    floor = c.mask_rect(0, 300, 270, 480)
    c.vgrad(floor, 300, 480, (50, 56, 70), (70, 78, 94), steps=4)
    c.fill(floor & ((((c.xx + c.yy) % 8) == 0) | (((c.xx - c.yy) % 8) == 0)), (40, 44, 56))
    c.fill(c.mask_rect(0, 300, 270, 304), (250, 200, 60))
    for x in range(0, 270, 12):
        c.fill(c.mask_rect(x, 300, x + 6, 304), (40, 40, 46))
    c.glow(135, 130, 150, (120, 170, 255), 0.12)
    return c, None


# =================================================================== PLAGE
def plage(heure="jour"):
    c = Px()
    sky = c.mask_rect(0, 0, 270, 200)
    ciel(c, sky, 0, 200, heure, seed=4, astre=(210, 150) if heure == "soir" else (60, 50))
    snap = c.a.copy()
    sea = c.mask_rect(0, 196, 270, 290)
    sc = dict(jour=((40, 120, 200), (90, 180, 220)), soir=((90, 70, 130), (220, 130, 110)), nuit=((14, 20, 50), (30, 40, 80)))[heure]
    c.vgrad(sea, 196, 290, sc[0], sc[1], steps=5)
    rnd = R(3)
    for k in range(60):
        x, y = rnd.randint(0, 260), rnd.randint(200, 286)
        c.fill(c.mask_rect(x, y, x + rnd.randint(4, 12), y + 1), lt(sc[1], 0.4))
    if heure == "soir":
        c.fill(sea & c.mask_rect(196, 196, 224, 290) & (((c.yy // 3) % 2) == 0), (255, 200, 130))
    boat = c.mask_poly([(40, 206), (64, 206), (60, 212), (44, 212)])
    c.fill(boat, (250, 250, 250)); c.fill(c.mask_poly([(52, 206), (52, 188), (62, 204)]), (250, 250, 250))
    for gx, gy in ((150, 90), (166, 100), (120, 70)):                         # mouettes
        c.line(gx - 4, gy - 2, gx, gy, (60, 60, 70)); c.line(gx, gy, gx + 4, gy - 2, (60, 60, 70))
    foam = c.mask_rect(0, 286, 270, 296)
    c.fill(foam, (240, 248, 250))
    for x in range(0, 270, 10):
        c.fill(c.mask_ell(x + 5, 296, 5, 2), (240, 248, 250))
    sand = c.mask_rect(0, 296, 270, 480)
    scol = dict(jour=((240, 214, 160), (226, 196, 140)), soir=((230, 176, 130), (214, 156, 116)), nuit=((80, 80, 110), (70, 70, 100)))[heure]
    c.vgrad(sand, 296, 480, scol[1], scol[0], steps=4)
    c.dither(sand, dk(scol[0], 0.9), 0.15)
    c.line(214, 330, 236, 230, (120, 90, 60)); c.line(215, 330, 237, 230, (120, 90, 60))   # parasol
    um = c.mask_ell(236, 230, 46, 16) & c.mask_rect(0, 0, 270, 231)
    c.fill(um, (240, 240, 240))
    for k in range(-4, 5):
        c.fill(um & c.mask_poly([(236, 214), (236 + k * 12, 231), (236 + k * 12 + 6, 231)]), (220, 50, 50))
    c.outline(um, (120, 40, 40))
    towel = c.mask_poly([(176, 360), (240, 352), (252, 392), (186, 400)])
    c.fill(towel, (60, 140, 220)); c.fill(towel & (((c.xx + c.yy) // 6 % 2) == 0), (250, 250, 250)); c.outline(towel, (40, 90, 150))
    ball = c.mask_ell(60, 410, 12, 12)                                         # ballon de plage
    c.fill(ball, (250, 250, 250))
    for k, cc in enumerate(((230, 50, 50), (60, 120, 230), (250, 200, 50))):
        a = k * 2.1
        c.fill(ball & c.mask_poly([(60, 410), (60 + math.cos(a) * 16, 410 + math.sin(a) * 16), (60 + math.cos(a + 0.9) * 16, 410 + math.sin(a + 0.9) * 16)]), cc)
    c.outline(ball, (90, 90, 100))
    for _ in range(8):
        x, y = rnd.randint(10, 260), rnd.randint(320, 470)
        c.fill(c.mask_ell(x, y, 2.5, 1.5), (250, 236, 220))
    return relief(c, snap, sky), None


# =================================================================== TRIBUNAL
def tribunal(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 320)
    c.vgrad(wall, 0, 320, (120, 80, 52), (150, 104, 70), steps=5)
    for x in range(0, 270, 30):                                               # lambris
        p = c.mask_rect(x + 3, 150, x + 27, 300)
        c.shape(p, (140, 96, 62), (110, 72, 44), (166, 120, 80), band=2)
    for wx in (40, 230):                                                       # hautes fenêtres
        w = c.mask_arch(wx - 16, wx + 16, 26, 120)
        c.vgrad(w, 26, 120, (200, 226, 246), (230, 240, 250), steps=4)
        c.fill(w & c.mask_rect(wx - 1, 26, wx + 1, 120), (100, 66, 40)); c.outline(w, (90, 60, 36))
        c.glow(wx, 70, 40, (255, 250, 230), 0.2)
    em = c.mask_ell(135, 60, 30, 30)                                           # emblème : la balance
    c.shape(em, (60, 40, 30), (40, 26, 20), band=1)
    g = (226, 186, 80)
    c.fill(c.mask_rect(134, 42, 136, 78), g); c.fill(c.mask_rect(116, 48, 154, 50), g)
    c.fill(c.mask_rect(126, 76, 144, 79), g)
    for sx in (118, 152):
        c.line(sx, 50, sx - 6, 64, g); c.line(sx, 50, sx + 6, 64, g)
        c.fill(c.mask_ell(sx, 64, 7, 2) & c.mask_rect(0, 64, 270, 480), g)
    bench = c.mask_rect(54, 170, 216, 300)                                     # estrade du juge
    c.shape(bench, (100, 62, 36), (72, 42, 24), (130, 86, 54), band=3)
    c.shape(c.mask_rect(48, 162, 222, 172), (120, 78, 46), (90, 56, 32), (150, 104, 66), band=1, sdir="bottom")
    for x in range(70, 210, 36):
        c.shape(c.mask_rect(x, 186, x + 24, 290), (110, 70, 42), (84, 52, 30), band=2)
    c.shape(c.mask_rrect(116, 120, 154, 162, 6), (60, 30, 30), (40, 20, 20), band=2)          # dossier du fauteuil
    gv = c.mask_rect(178, 154, 196, 160) | c.mask_rect(186, 150, 190, 162)                       # marteau
    c.shape(gv, (110, 70, 40), (80, 50, 28), band=1)
    c.fill(c.mask_rect(82, 152, 112, 162), (250, 250, 246))
    for x0, x1 in ((0, 40), (230, 270)):                                      # barre des témoins / bancs
        c.shape(c.mask_rect(x0, 236, x1, 300), (110, 70, 42), (84, 52, 30), (140, 96, 60), band=2)
        c.shape(c.mask_rect(x0, 230, x1, 238), (130, 86, 54), (96, 60, 36), band=1)
    planks(c, 300, 480, horizon=240, col=(140, 96, 62), dark=(110, 72, 44), light=(166, 120, 80))
    teinte(c, heure, interieur=True)
    return c, None


# =================================================================== ENTRÉE D'APPARTEMENT (mur libre pour une porte animée : scene.Scene.porte(410, 1272))
def entree(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 318)
    c.vgrad(wall, 0, 318, (226, 206, 176), (240, 226, 200), steps=6)
    c.shape(c.mask_rect(0, 0, 270, 8), (210, 190, 160), (180, 160, 130), band=2, sdir="bottom")
    low = c.mask_rect(0, 236, 270, 318)                                       # soubassement en bois
    c.shape(low, (176, 130, 86), (140, 100, 64), (200, 156, 108), band=2)
    for x in range(0, 270, 22):
        c.fill(low & c.mask_rect(x, 240, x + 1, 316), (150, 108, 70))
    c.fill(c.mask_rect(0, 234, 270, 237), (150, 108, 70))
    c.fill(c.mask_rect(68, 200, 136, 318), (226, 206, 176))                    # mur nu derrière la porte
    c.fill(c.mask_rect(144, 214, 150, 224), (250, 250, 246)); c.outline(c.mask_rect(144, 214, 150, 224), (150, 140, 120))
    c.px(147, 219, (180, 180, 180))                                            # interrupteur
    mir = c.mask_ell(186, 120, 18, 26)                                         # miroir
    c.shape(c.mask_ell(186, 120, 21, 29), (190, 150, 80), (150, 110, 50), band=2)
    c.vgrad(mir, 94, 146, (200, 220, 230), (160, 186, 200), steps=4)
    c.tint(mir & c.mask_poly([(176, 96), (184, 96), (172, 140), (166, 140)]), (255, 255, 255), 0.3)
    c.shape(c.mask_rect(214, 96, 262, 102), (120, 80, 50), (90, 58, 34), band=1)    # portemanteau
    for k, (hx, jc) in enumerate(((222, (60, 90, 150)), (238, (180, 60, 60)), (254, (90, 130, 80)))):
        c.fill(c.mask_rect(hx, 102, hx + 1, 108), (60, 60, 66))
        coat = c.mask_poly([(hx - 7, 108), (hx + 8, 108), (hx + 10, 168 - k * 8), (hx - 9, 168 - k * 8)])
        c.shape(coat, jc, dk(jc, 0.72), lt(jc, 0.2), band=2)
    c.fill(c.mask_rect(228, 104, 248, 112), (60, 60, 66))
    rack = c.mask_rect(206, 280, 266, 312)                                     # meuble à chaussures
    c.shape(rack, (120, 80, 50), (90, 58, 34), (150, 104, 66), band=2)
    for k, (sx, sc_) in enumerate(((212, (250, 250, 250)), (230, (40, 40, 48)), (248, (200, 60, 60)))):
        c.shape(c.mask_rect(sx, 272, sx + 12, 280), sc_, dk(sc_, 0.72), band=1)
    plante(c, 30, 318, h=40, pot=(190, 96, 60), seed=6)
    c.line(135, 0, 135, 16, (60, 50, 50))
    lamp = c.mask_ell(135, 20, 9, 5)
    c.shape(lamp, (240, 230, 200), (210, 196, 160), band=1)
    sol_carreaux(c, 318, 480, horizon=250, c1=(214, 204, 190), c2=(186, 172, 156), grout=(160, 150, 140), cell=0.8)
    mat = c.mask_poly([(68, 322), (136, 322), (142, 340), (62, 340)])          # paillasson
    c.fill(mat, (150, 110, 60)); c.dither(mat, (120, 86, 46), 0.5); c.outline(mat, (90, 64, 36))
    teinte(c, heure, interieur=True)
    if heure == "nuit":
        c.glow(135, 24, 170, (255, 214, 150), 0.32)
    return c, None


# =================================================================== TABLEAUX (zone d'écriture identique à « tableau » : x 22-248, y 68-252)
def tableau_blanc(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 318)
    c.vgrad(wall, 0, 318, (206, 214, 224), (226, 232, 238), steps=5)
    c.shape(c.mask_rect(14, 60, 256, 262), (190, 196, 206), (150, 156, 168), (226, 230, 238), band=3)
    bd = c.mask_rect(22, 68, 248, 252)
    c.fill(bd, (250, 251, 252))
    rnd = R(5)
    for _ in range(5):
        x, y = rnd.randint(40, 220), rnd.randint(90, 230)
        c.dither(c.mask_ell(x, y, rnd.randint(14, 30), rnd.randint(4, 7)) & bd, (230, 234, 240), 0.35)
    tray = c.mask_rect(18, 252, 252, 258)
    c.shape(tray, (170, 176, 188), (130, 136, 150), band=1, sdir="bottom")
    for x, colr in ((60, (40, 60, 160)), (72, (210, 40, 50)), (84, (40, 140, 70))):
        c.fill(c.mask_rect(x, 249, x + 9, 252), colr); c.outline(c.mask_rect(x, 249, x + 9, 252))
    c.shape(c.mask_rect(200, 247, 218, 252), (60, 60, 80), (40, 40, 56), band=1)
    for k, (nx, ny, nc) in enumerate(((228, 30, (250, 220, 90)), (240, 40, (250, 150, 180)), (20, 28, (140, 220, 250)))):
        n = c.mask_rect(nx - 8, ny - 8, nx + 8, ny + 8)
        c.shape(n, nc, dk(nc, 0.85), band=1)
    c.shape(c.mask_rect(0, 296, 270, 320), (150, 156, 168), (110, 116, 128), band=2, sdir="bottom")
    floor = c.mask_rect(0, 320, 270, 480)
    c.vgrad(floor, 320, 480, (110, 120, 140), (130, 140, 158), steps=4)
    c.dither(floor, (120, 130, 150), 0.15)
    return c, None


def ecran_info(heure="nuit"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 318)
    c.vgrad(wall, 0, 318, (14, 20, 44), (30, 40, 80), steps=5)
    for k in range(10):
        x = 10 + k * 28
        c.tint(c.mask_poly([(x, 0), (x + 5, 0), (x + 26, 318), (x + 16, 318)]), (120, 160, 255), 0.05)
    c.shape(c.mask_rect(14, 60, 256, 262), (24, 26, 34), (14, 16, 20), (60, 64, 80), band=3)
    bd = c.mask_rect(22, 68, 248, 252)
    c.vgrad(bd, 68, 252, (24, 50, 110), (12, 24, 60), steps=5)
    c.fill(bd & ((c.yy % 3) == 0), (20, 42, 96))
    c.fill(c.mask_rect(22, 68, 70, 78), (200, 30, 50)); c.text((46, 69), "INFO", (255, 255, 255), size=7, anchor="ma")
    c.fill(c.mask_rect(226, 72, 232, 76), (255, 60, 60))
    c.glow(135, 160, 160, (80, 140, 255), 0.18)
    c.fill(c.mask_rect(120, 262, 150, 280), (24, 26, 34)); c.fill(c.mask_rect(100, 280, 170, 286), (24, 26, 34))
    floor = c.mask_rect(0, 318, 270, 480)
    c.vgrad(floor, 318, 480, (20, 26, 50), (40, 50, 90), steps=4)
    c.dither(floor & c.mask_rect(0, 318, 270, 360), (60, 90, 170), 0.2)
    return c, None


def tableau_parchemin(heure="soir"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 320)
    c.fill(wall, (120, 112, 104))
    for y in range(0, 320, 12):                                              # pierres
        off = 0 if (y // 12) % 2 == 0 else 14
        c.fill(c.mask_rect(0, y, 270, y + 1), (90, 84, 78))
        for x in range(off, 270, 28):
            c.fill(c.mask_rect(x, y, x + 1, y + 12), (90, 84, 78))
    rnd = R(3)
    for _ in range(60):
        x, y = rnd.randrange(270), rnd.randrange(320)
        c.fill(c.mask_rect(x, y, x + 8, y + 5) & wall, rnd.choice([(132, 124, 116), (110, 102, 96)]))
    paper = c.mask_rect(20, 64, 250, 256)
    c.fill(paper, (236, 220, 176))
    c.dither(paper & ~c.mask_rect(30, 74, 240, 246), (210, 186, 140), 0.5)
    for x0, x1 in ((12, 258),):
        for y0 in (54, 252):
            roll = c.mask_rrect(x0, y0, x1, y0 + 12, 6)
            c.shape(roll, (214, 190, 140), (170, 146, 100), (240, 222, 180), band=2)
            c.fill(c.mask_ell(x0 + 2, y0 + 6, 4, 6), (140, 100, 60)); c.fill(c.mask_ell(x1 - 2, y0 + 6, 4, 6), (140, 100, 60))
    c.outline(paper, (150, 120, 80))
    for x in (6, 264):
        torche(c, x, 150)
    floor = c.mask_rect(0, 320, 270, 480)
    pavés(c, 320, 480, horizon=240, col=(130, 120, 110), joint=(96, 88, 80))
    c.glow(135, 160, 180, (255, 200, 130), 0.12)
    return c, None


# =================================================================== AÉROPORT (hall)
def avion_ext(c, x, y, s=1.0, col=(246, 246, 250), queue=(200, 40, 60)):
    body = c.mask_rrect(x - 60 * s, y - 7 * s, x + 56 * s, y + 7 * s, int(6 * s))
    c.shape(body, col, (196, 200, 212), (255, 255, 255), band=1)
    c.fill(c.mask_poly([(x + 54 * s, y - 6 * s), (x + 66 * s, y), (x + 54 * s, y + 6 * s)]), col)
    c.fill(c.mask_poly([(x - 56 * s, y - 6 * s), (x - 66 * s, y - 26 * s), (x - 52 * s, y - 26 * s), (x - 40 * s, y - 6 * s)]), queue)
    c.fill(c.mask_poly([(x - 10 * s, y + 2 * s), (x + 14 * s, y + 2 * s), (x - 18 * s, y + 18 * s), (x - 30 * s, y + 18 * s)]), (210, 214, 224))
    for k in range(12):
        c.px(x - 40 * s + k * 7 * s, y - 2 * s, (90, 130, 180))
    c.fill(c.mask_rect(x + 46 * s, y - 4 * s, x + 54 * s, y - 1 * s), (90, 130, 180))


def aeroport(heure="jour"):
    c = Px()
    sky = c.mask_rect(0, 30, 270, 230)
    ciel(c, sky, 30, 230, heure, seed=2, astre=(220, 70))
    snap = c.a.copy()
    c.fill(c.mask_rect(0, 196, 270, 230), (120, 124, 130) if heure != "nuit" else (40, 44, 56))      # piste
    for x in range(0, 270, 30):
        c.fill(c.mask_rect(x, 212, x + 14, 214), (240, 240, 230))
    avion_ext(c, 150, 186, 1.0)
    for x in range(0, 271, 45):                                              # montants de la baie vitrée
        c.shape(c.mask_rect(x - 3, 30, x + 3, 232), (70, 76, 90), (50, 54, 64), band=1)
    c.shape(c.mask_rect(0, 22, 270, 32), (90, 96, 110), (60, 64, 76), band=1, sdir="bottom")
    c.shape(c.mask_rect(0, 228, 270, 236), (90, 96, 110), (60, 64, 76), band=1, sdir="bottom")
    c.fill(c.mask_rect(0, 0, 270, 22), (210, 212, 216))
    for x in range(10, 270, 50):
        c.fill(c.mask_rect(x, 6, x + 30, 10), (252, 252, 246))
    board = c.mask_rect(60, 40, 210, 116)                                    # tableau des départs
    c.shape(board, (26, 26, 32), (16, 16, 20), band=2)
    c.text((135, 44), "DÉPARTS", (250, 210, 60), size=9, anchor="ma")
    for k, (dest, hh, porte) in enumerate((("PARIS", "14:05", "A12"), ("DUBAI", "15:30", "B04"), ("ALGER", "16:10", "A07"),
                                            ("LONDRES", "17:45", "C21"))):
        y = 60 + k * 13
        c.text((68, y), dest, (250, 220, 120), size=7)
        c.text((150, y), hh, (250, 220, 120), size=7)
        c.text((182, y), porte, (120, 230, 140), size=7)
    c.line(90, 22, 90, 40, (60, 60, 66)); c.line(180, 22, 180, 40, (60, 60, 66))
    wall = c.mask_rect(0, 236, 270, 306)
    c.vgrad(wall, 236, 306, (214, 218, 224), (196, 200, 208), steps=4)
    desk = c.mask_rect(10, 262, 110, 306)                                     # comptoirs d'enregistrement
    c.shape(desk, (60, 110, 190), (40, 80, 150), (90, 140, 220), band=2)
    c.fill(c.mask_rect(10, 260, 110, 264), (230, 232, 238))
    for x in (30, 80):
        ecran(c, x - 10, 246, x + 10, 260, scr=(60, 140, 220), kind="code", seed=x, glow=False)
    sign = c.mask_rect(150, 244, 250, 262)
    c.shape(sign, (250, 200, 40), (210, 160, 20), band=1)
    c.text((200, 248), "PORTE A12  →", (30, 30, 40), size=8, anchor="ma") if False else c.text((200, 248), "PORTE A12", (30, 30, 40), size=8, anchor="ma")
    for k, x in enumerate(range(130, 266, 22)):                               # rangée de sièges
        seat = c.mask_rrect(x, 280, x + 18, 300, 3)
        c.shape(seat, (40, 90, 170), (28, 64, 130), (70, 120, 210), band=1)
        c.fill(c.mask_rect(x + 2, 300, x + 4, 306), (120, 124, 134))
    floor = c.mask_rect(0, 306, 270, 480)
    sol_carreaux(c, 306, 480, horizon=240, c1=(226, 228, 232), c2=(210, 212, 218), grout=(190, 192, 198), cell=1.2)
    c.dither(floor & c.mask_rect(0, 306, 270, 360), (240, 242, 246), 0.25)
    val = c.mask_rrect(222, 330, 250, 372, 3)                                   # valise
    c.shape(val, (200, 60, 60), (150, 40, 40), (230, 100, 100), band=2)
    c.fill(c.mask_rect(234, 318, 238, 330), (60, 60, 66)); c.fill(c.mask_rect(230, 316, 242, 318), (60, 60, 66))
    for wx in (226, 246):
        c.fill(c.mask_ell(wx, 374, 2, 2), (30, 30, 36))
    teinte(c, heure, m=~intact(c, snap, sky), interieur=True)
    return relief(c, snap, sky), None


# =================================================================== CABINE D'AVION (deux sièges au premier rang)
def avion(heure="jour"):
    c = Px()
    c.fill(c.mask_rect(0, 0, 270, 480), (224, 226, 230))
    ceil = c.mask_poly([(0, 0), (270, 0), (270, 36), (162, 104), (108, 104), (0, 36)])         # plafond en perspective
    c.vgrad(ceil, 0, 104, (244, 244, 248), (214, 216, 222), steps=4)
    for k in range(6):                                                         # rampe de lumières vers le fond
        z = 1 - k * 0.16
        c.fill(c.mask_rect(135 - 22 * z, 10 + k * 15, 135 + 22 * z, 12 + k * 15), (255, 250, 230))
    for side in (-1, 1):                                                       # coffres à bagages (fermés)
        xo = 0 if side < 0 else 270
        xi = 135 + side * 27
        b = c.mask_poly([(xo, 36), (xi, 104), (xi, 128), (xo, 112)])
        c.shape(b, (240, 240, 244), (206, 208, 216), (252, 252, 254), band=2)
        for t in (0.25, 0.5, 0.75):                                            # séparations des portes
            x = xo + (xi - xo) * t
            y_top = 36 + (104 - 36) * t
            y_bot = 112 + (128 - 112) * t
            c.line(x, y_top, x, y_bot, (196, 198, 206))
            c.fill(c.mask_rect(x - side * 6 - 2, y_bot - 5, x - side * 6 + 2, y_bot - 4), (150, 154, 166))
        c.line(xo, 112, xi, 128, (186, 188, 198))
    for k, (x, y, s_) in enumerate(((22, 168, 1.0), (248, 168, 1.0), (62, 150, 0.6), (208, 150, 0.6))):   # hublots
        w = c.mask_ell(x, y, 10 * s_, 15 * s_)
        c.vgrad(w, y - 15, y + 15, (110, 170, 236) if heure != "nuit" else (20, 24, 60), (200, 230, 250) if heure != "nuit" else (40, 44, 90), steps=3)
        if heure != "nuit":
            nuage(c, x, y + 4 * s_, 18 * s_, m=w)
        c.outline(w, (150, 152, 160))
    for k in range(5):                                                         # rangées de sièges vers le fond
        z = 1 - k * 0.17
        for side in (-1, 1):
            cx_ = 135 + side * (40 + 50 * z)
            seat = c.mask_rrect(cx_ - 34 * z, 200 - 40 * z - k * 8, cx_ + 34 * z, 300 - k * 22, int(5 * z))
            c.shape(seat, (40, 70, 140), (28, 50, 104), (70, 100, 180), band=2)
            c.fill(c.mask_rect(cx_ - 26 * z, 200 - 40 * z - k * 8, cx_ + 26 * z, 200 - 30 * z - k * 8), (240, 240, 244))
    aisle = c.mask_poly([(110, 480), (160, 480), (145, 250), (125, 250)])
    c.fill(aisle, (90, 60, 70)); c.dither(aisle, (110, 76, 86), 0.3)
    for sx in (82, 188):                                                       # nos deux sièges, au premier plan
        seat = c.mask_rrect(sx - 50, 196, sx + 50, 344, 12)
        c.shape(seat, (40, 70, 140), (28, 50, 104), (70, 100, 180), band=3)
        c.fill(c.mask_rect(sx - 34, 200, sx + 34, 226), (240, 240, 244))
    c.shape(c.mask_rect(126, 290, 144, 300), (120, 124, 134), (90, 94, 104), band=1)
    floor = c.mask_rect(0, 344, 270, 480)
    c.fill(floor, (110, 80, 90)); c.dither(floor, (96, 68, 78), 0.3)
    teinte(c, heure, interieur=True)
    return c, None


# =================================================================== STADE
def stade(heure="jour"):
    c = Px()
    sky = c.mask_rect(0, 0, 270, 120)
    ciel(c, sky, 0, 120, heure, seed=7, astre=None, nuages=heure == "jour")
    snap = c.a.copy()
    stands = c.mask_poly([(0, 60), (270, 60), (270, 250), (0, 250)])
    c.vgrad(stands, 60, 250, (70, 76, 90), (110, 116, 130), steps=4)
    rnd = R(5)
    for y in range(66, 248, 6):                                               # le public (points colorés)
        c.fill(c.mask_rect(0, y, 270, y + 1), (60, 64, 78))
        for x in range(rnd.randint(0, 3), 270, 4):
            col_ = rnd.choice([(230, 60, 60), (250, 250, 250), (60, 120, 230), (250, 210, 60), (240, 180, 140), (120, 80, 60), (40, 40, 50)])
            c.px(x, y + 3, col_); c.px(x, y + 2, (220, 180, 150) if rnd.random() < 0.6 else (110, 76, 56))
    c.fill(c.mask_rect(0, 160, 270, 166), (200, 30, 50)); c.text((135, 160), "ALLEZ !", (255, 255, 255), size=6, anchor="ma")
    for fx in (16, 254):                                                      # projecteurs
        c.fill(c.mask_rect(fx - 1, 10, fx + 1, 60), (80, 84, 96))
        c.shape(c.mask_rect(fx - 10, 0, fx + 10, 12), (60, 64, 76), (40, 44, 54), band=1)
        for k in range(4):
            c.fill(c.mask_rect(fx - 8 + k * 4, 3, fx - 6 + k * 4, 9), (255, 250, 220))
    c.shape(c.mask_rect(0, 248, 270, 262), (40, 120, 70), (30, 90, 54), band=1)    # panneaux publicitaires
    for k, x in enumerate(range(0, 270, 54)):
        c.fill(c.mask_rect(x + 2, 250, x + 52, 260), [(220, 60, 60), (60, 120, 230), (250, 200, 50), (60, 170, 90), (240, 240, 240)][k % 5])
    pitch = c.mask_rect(0, 262, 270, 480)
    yy, xx = c.yy, c.xx
    dz = np.maximum(yy - 200, 1).astype(float); z = 420.0 / dz
    stripes = (np.floor(z / 0.8) % 2 == 0)
    c.fill(pitch, (60, 150, 70)); c.fill(pitch & stripes, (74, 168, 82))
    for y_ in (300,):
        c.fill(c.mask_rect(0, y_, 270, y_ + 2), (240, 240, 236))
    c.fill(c.mask_rect(0, 268, 270, 270), (240, 240, 236))
    circ = c.mask_ell(135, 400, 70, 22) & ~c.mask_ell(135, 400, 68, 20)
    c.fill(circ, (240, 240, 236))
    goal = c.mask_rect(20, 226, 70, 268)                                      # but
    c.fill(goal & ((((c.xx + c.yy) % 3) == 0)), (230, 230, 230))
    c.fill(c.mask_rect(20, 226, 70, 228) | c.mask_rect(20, 226, 22, 268) | c.mask_rect(68, 226, 70, 268), (250, 250, 250))
    teinte(c, heure, m=~intact(c, snap, sky))
    if heure == "nuit":
        for fx in (16, 254):
            c.glow(fx, 8, 120, (255, 252, 230), 0.5)
            ray = c.mask_poly([(fx - 10, 10), (fx + 10, 10), (135 + (fx - 135) * 0.2 + 60, 480), (135 + (fx - 135) * 0.2 - 60, 480)])
            c.tint(ray, (255, 255, 230), 0.08)
    return relief(c, snap, sky), None


# =================================================================== MARCHÉ
def marche(heure="jour"):
    c = Px()
    sky = c.mask_rect(0, 0, 270, 200)
    ciel(c, sky, 0, 200, heure, seed=9, astre=(200, 40))
    snap = c.a.copy()
    for k, (x0, x1, h, wc) in enumerate(((-10, 90, 150, (226, 200, 160)), (88, 180, 130, (214, 170, 130)), (178, 280, 160, (200, 190, 170)))):
        b = c.mask_rect(x0, 200 - h + 60, x1, 236)                           # façades au fond
        c.shape(b, wc, dk(wc, 0.85), band=2)
        for wx in range(x0 + 10, x1 - 10, 22):
            for wy in range(200 - h + 72, 220, 26):
                w = c.mask_rect(wx, wy, wx + 12, wy + 16)
                c.fill(w, (90, 110, 130) if heure != "soir" else (250, 200, 120)); c.outline(w, dk(wc, 0.7))
    rnd = R(3)
    for k, (x0, x1, aw) in enumerate(((0, 92, ((230, 60, 60), (250, 250, 250))), (92, 182, ((50, 150, 80), (250, 250, 250))),
                                      (182, 270, ((240, 170, 40), (250, 250, 250))))):
        stall = c.mask_rect(x0 + 4, 262, x1 - 4, 312)                         # étals
        c.shape(stall, (150, 104, 66), (110, 74, 46), (176, 128, 86), band=2)
        for px_ in (x0 + 6, x1 - 8):
            c.fill(c.mask_rect(px_, 214, px_ + 2, 262), (110, 74, 46))
        roof = c.mask_poly([(x0, 214), (x1, 214), (x1 + 4, 232), (x0 - 4, 232)])
        c.fill(roof, aw[1]); c.fill(roof & (((c.xx // 8) % 2) == 0), aw[0]); c.outline(roof)
        for x in range(x0, x1, 8):
            c.fill(c.mask_ell(x + 4, 232, 4, 2.5), aw[0] if (x // 8) % 2 == 0 else aw[1])
        for j in range(3):                                                    # cagettes de fruits
            cx0 = x0 + 10 + j * 26
            crate = c.mask_rect(cx0, 250, cx0 + 22, 262)
            c.shape(crate, (190, 150, 100), (150, 110, 70), band=1)
            fc = rnd.choice([(230, 60, 40), (250, 180, 40), (120, 180, 60), (250, 220, 80), (150, 60, 120)])
            for fx_ in range(cx0 + 2, cx0 + 21, 4):
                c.fill(c.mask_ell(fx_, 249, 2.4, 2.2), fc)
                c.px(fx_ - 1, 248, lt(fc, 0.5))
    pavés(c, 312, 480, horizon=230, col=(160, 150, 140), joint=(120, 112, 104))
    teinte(c, heure, m=~intact(c, snap, sky))
    if heure == "soir":
        for k in range(20):                                                   # guirlande
            x = k * 14
            y = int(204 + 8 * math.sin(x / 270 * math.pi))
            c.fill(c.mask_ell(x, y, 1.8, 2.2), (255, 226, 150)); c.glow(x, y, 10, (255, 210, 120), 0.4)
    return relief(c, snap, sky), None


# =================================================================== PRISON (cellule ; « prison_barreaux » = vue à travers les barreaux)
def prison(heure="jour", barreaux=False):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 320)
    c.fill(wall, (120, 122, 128))
    for y in range(0, 320, 10):
        off = 0 if (y // 10) % 2 == 0 else 12
        c.fill(c.mask_rect(0, y, 270, y + 1), (96, 98, 104))
        for x in range(off, 270, 24):
            c.fill(c.mask_rect(x, y, x + 1, y + 10), (96, 98, 104))
    rnd = R(4)
    for _ in range(50):
        x, y = rnd.randrange(270), rnd.randrange(320)
        c.fill(c.mask_rect(x, y, x + 6, y + 4) & wall, rnd.choice([(132, 134, 140), (108, 110, 116)]))
    win = c.mask_rect(170, 50, 220, 90)                                         # petite fenêtre à barreaux
    ciel(c, win, 50, 90, "jour" if heure == "jour" else "nuit", seed=1, nuages=False)
    for x in range(176, 220, 9):
        c.fill(c.mask_rect(x, 50, x + 2, 90), (60, 62, 70))
    c.outline(win, (60, 62, 70))
    ray = c.mask_poly([(170, 90), (220, 90), (180, 330), (90, 330)])
    c.tint(ray, (240, 246, 255), 0.10 if heure == "jour" else 0.03)
    bunk = c.mask_rect(10, 230, 120, 260)                                      # lit superposé
    c.shape(bunk, (90, 94, 104), (60, 62, 70), band=1)
    c.shape(c.mask_rect(14, 220, 116, 232), (200, 200, 190), (160, 160, 150), band=1)
    c.shape(c.mask_rect(10, 150, 120, 176), (90, 94, 104), (60, 62, 70), band=1)
    c.shape(c.mask_rect(14, 140, 116, 152), (200, 200, 190), (160, 160, 150), band=1)
    for x in (12, 116):
        c.fill(c.mask_rect(x, 140, x + 3, 300), (70, 72, 80))
    for k in range(8):                                                          # traits comptés au mur
        c.fill(c.mask_rect(140 + k * 4, 140, 141 + k * 4, 156), (70, 70, 74))
    c.line(138, 150, 172, 144, (70, 70, 74))
    floor = c.mask_rect(0, 320, 270, 480)
    c.vgrad(floor, 320, 480, (100, 102, 108), (120, 122, 128), steps=4)
    for y in range(330, 480, 22):
        c.fill(floor & c.mask_rect(0, y, 270, y + 1), (86, 88, 94))
    teinte(c, heure, interieur=True)
    f = None
    if barreaux:                                                                # barreaux au premier plan
        f = Px(alpha=True)
        for x in range(10, 270, 34):
            bar = f.mask_rect(x, 0, x + 6, 480)
            f.shape(bar, (70, 74, 84), (44, 46, 54), (120, 124, 136), band=1)
        for y in (80, 400):
            f.shape(f.mask_rect(0, y, 270, y + 8), (70, 74, 84), (44, 46, 54), (120, 124, 136), band=1, sdir="bottom")
    return c, f


# =================================================================== COULOIR D'ÉCOLE
def couloir_ecole(heure="jour"):
    c = Px()
    wall = c.mask_rect(0, 0, 270, 318)
    c.vgrad(wall, 0, 318, (230, 226, 204), (242, 238, 220), steps=5)
    c.shape(c.mask_rect(0, 0, 270, 10), (236, 236, 230), (200, 200, 192), band=2, sdir="bottom")
    for x in (40, 135, 230):
        c.shape(c.mask_rect(x - 24, 10, x + 24, 15), (250, 250, 246), (210, 210, 206), band=1)
    for k, x0 in enumerate(range(0, 150, 15)):                                  # casiers
        col_ = (60, 110, 190) if k % 2 == 0 else (200, 70, 70)
        lk = c.mask_rect(x0 + 1, 170, x0 + 14, 300)
        c.shape(lk, col_, dk(col_, 0.75), lt(col_, 0.2), band=1)
        for y in (180, 184, 188):
            c.fill(c.mask_rect(x0 + 4, y, x0 + 11, y + 1), dk(col_, 0.6))
        c.fill(c.mask_rect(x0 + 10, 232, x0 + 12, 240), (200, 204, 214))
    door = c.mask_rect(170, 150, 226, 300)                                       # porte de classe
    c.shape(door, (150, 104, 66), (110, 74, 46), (176, 128, 86), band=2)
    dw = c.mask_rect(180, 166, 216, 200)
    c.fill(dw, (190, 220, 236) if heure != "nuit" else (40, 50, 80)); c.outline(dw, (110, 74, 46))
    c.fill(c.mask_rect(218, 228, 222, 232), (220, 190, 90))
    c.text((198, 140), "SALLE 12", (60, 60, 70), size=7, anchor="ma")
    bb = c.mask_rect(234, 160, 266, 220)                                         # panneau d'affichage
    c.fill(bb, (186, 140, 90)); c.outline(bb, (120, 84, 50))
    for k, (px_, py_, pc) in enumerate(((238, 164, (250, 250, 240)), (252, 168, (250, 220, 120)), (240, 190, (160, 220, 250)), (254, 196, (250, 160, 180)))):
        c.fill(c.mask_rect(px_, py_, px_ + 10, py_ + 14), pc); c.px(px_ + 5, py_, (220, 40, 40))
    c.text((80, 120), "BIENVENUE !", (60, 110, 190), size=10, anchor="ma")
    c.shape(c.mask_rect(0, 300, 270, 318), (150, 160, 150), (120, 130, 120), band=1, sdir="bottom")
    sol_carreaux(c, 318, 480, horizon=250, c1=(214, 220, 214), c2=(196, 204, 198), grout=(176, 184, 178), cell=0.9)
    c.dither(c.mask_rect(0, 318, 270, 360), (236, 240, 236), 0.2)
    teinte(c, heure, interieur=True)
    return c, None


# =================================================================== LUMIÈRE DES DÉCORS (ambiance + sources, en pixels écran portrait)
NUIT, SOIR, JOUR = (0.66, 0.70, 0.92), (1.0, 0.88, 0.80), (1.0, 1.0, 1.0)
LUMIERES = {
    "rue_nuit": (NUIT, [(1064, 660, 720, (255, 214, 140), 0.8), (800, 900, 520, (255, 90, 140), 0.35)]),
    "parc_nuit": (NUIT, [(488, 660, 680, (255, 214, 140), 0.8)]),
    "cuisine_nuit": ((0.88, 0.82, 0.86), [(540, 190, 900, (255, 206, 140), 0.5), (404, 1136, 380, (255, 140, 60), 0.4)]),
    "entree_nuit": ((0.86, 0.82, 0.86), [(540, 96, 900, (255, 214, 150), 0.55)]),
    "chambre_ado": ((0.82, 0.78, 0.94), [(712, 744, 620, (160, 100, 255), 0.6), (944, 744, 540, (80, 200, 255), 0.5)]),
    "studio": ((0.88, 0.84, 0.94), [(540, 280, 900, (255, 90, 210), 0.35), (928, 560, 400, (255, 60, 60), 0.3)]),
    "plateau_tv": ((0.84, 0.88, 1.0), [(540, 480, 1000, (90, 150, 255), 0.45)]),
    "ecran_info": ((0.84, 0.88, 1.0), [(540, 640, 900, (80, 140, 255), 0.35)]),
    "foret": ((0.62, 0.68, 0.90), [(540, 1450, 780, (255, 140, 50), 0.95)]),
    "desert_nuit": (NUIT, [(540, 1500, 780, (255, 140, 50), 0.9)]),
    "toit": ((0.72, 0.74, 0.90), [(540, 420, 900, (255, 210, 120), 0.45)]),
    "bibliotheque": ((0.96, 0.90, 0.82), [(664, 1000, 520, (255, 190, 100), 0.6), (540, 240, 900, (255, 214, 140), 0.3)]),
    "bibliotheque_nuit": ((0.78, 0.74, 0.82), [(664, 1000, 620, (255, 190, 100), 0.85)]),
    "palais": ((1.0, 0.96, 0.92), [(160, 680, 520, (255, 170, 80), 0.5), (920, 680, 520, (255, 170, 80), 0.5)]),
    "tableau_parchemin": ((0.95, 0.90, 0.84), [(24, 560, 500, (255, 170, 80), 0.5), (1056, 560, 500, (255, 170, 80), 0.5)]),
    "salon": ((0.97, 0.93, 0.90), [(600, 200, 900, (255, 200, 120), 0.35)]),
    "espace": ((0.88, 0.92, 1.0), [(540, 520, 900, (120, 170, 255), 0.35)]),
    "hopital_nuit": ((0.80, 0.82, 0.92), [(452, 432, 500, (80, 250, 140), 0.3)]),
    "voiture_nuit": ((0.72, 0.74, 0.92), [(664, 1110, 420, (80, 160, 255), 0.45)]),
    "stade_nuit": ((0.84, 0.86, 0.96), [(64, 40, 1400, (255, 252, 230), 0.35), (1016, 40, 1400, (255, 252, 230), 0.35)]),
    "marche_soir": (SOIR, [(540, 816, 900, (255, 200, 120), 0.3)]),
    "prison": ((0.88, 0.90, 0.96), [(780, 280, 700, (230, 240, 255), 0.35)]),
    "prison_barreaux": ((0.88, 0.90, 0.96), [(780, 280, 700, (230, 240, 255), 0.35)]),
    "prison_nuit": ((0.66, 0.70, 0.90), []),
    "cafe_soir": (SOIR, [(240, 144, 500, (255, 214, 140), 0.4), (840, 144, 500, (255, 214, 140), 0.4)]),
    "cafe": ((1.0, 0.97, 0.94), [(540, 144, 600, (255, 214, 140), 0.25)]),
}


def lumiere_de(nom, W=1080, H=1920, fmt="portrait"):
    amb, src = LUMIERES.get(nom, (None, []))
    if amb is None:
        amb = NUIT if nom.endswith("_nuit") else (SOIR if nom.endswith("_soir") else JOUR)
    if fmt == "paysage":
        src = [(x + 420, y, r, c, f) for (x, y, r, c, f) in src]
    return amb, src


# =================================================================== FORMAT HORIZONTAL (16:9) : bande de 270 lignes + bords prolongés en miroir
CADRAGE = dict(tableau=40, tableau_blanc=40, ecran_info=40, tableau_parchemin=40, carte=110, voiture=120, avion=130,
               studio=150, plateau_tv=150, stade=110, aeroport=110, espace=60, toit=120, desert=110, temple=60,
               village=80, palais=90, bibliotheque=110, foret=130, plage=110, parc=110, rue=110, marche=100)


def cadrage(nom):
    if nom in CADRAGE:
        return CADRAGE[nom]
    base = nom.rsplit("_", 1)[0]
    return CADRAGE.get(base, CADRAGE.get(nom.split("_")[0], 150))


class PxLarge(_PxBase):
    """Toile ÉLARGIE pour le format 16:9 : le décor est dessiné avec ses coordonnées habituelles (0-270), décalé au centre
    d'une toile de 480 ; tout ce qui touche un bord (murs, sols, ciel, bandes) se prolonge jusqu'au bord de la toile."""
    OX = 105

    def __init__(s, w=270, h=480, bg=(0, 0, 0), alpha=False):
        super().__init__(w + 2 * s.OX, h, bg, alpha)
        s.ox = s.OX
        s.xx = s.xx - s.ox

    def _bx(s, x):                                        # un bord du décor (0 ou 270, à quelques pixels près) → bord de la toile
        return -s.ox if -12 <= x <= 0 else (270 + s.ox if 270 <= x <= 282 else x)

    def mask_rect(s, x0, y0, x1, y1):
        return _PxBase.mask_rect(s, s._bx(x0) + s.ox, y0, s._bx(x1) + s.ox, y1)

    def mask_poly(s, pts):
        return _PxBase.mask_poly(s, [(s._bx(x) + s.ox, y) for x, y in pts])

    def px(s, x, y, col):
        _PxBase.px(s, x + s.ox, y, col)

    def text(s, xy, txt, col, size=10, font=TAHOMA, anchor="la", ol=None):
        return _PxBase.text(s, (xy[0] + s.ox, xy[1]), txt, col, size=size, font=font, anchor=anchor, ol=ol)

    def sprite(s, rows, pal, x0, y0, mirror=False):
        _PxBase.sprite(s, rows, pal, x0 + s.ox, y0, mirror)

    def paste(s, img_rgba, x0, y0):
        _PxBase.paste(s, img_rgba, x0 + s.ox, y0)


def decor_large(nom):
    """Dessine le décor sur une toile élargie (format 16:9), sans doublon ni miroir."""
    g = globals()
    old_l, old_s = g["Px"], sets.Px
    g["Px"] = PxLarge
    sets.Px = PxLarge
    try:
        return sets.DECORS[nom]()
    finally:
        g["Px"] = old_l
        sets.Px = old_s


def vers_paysage(bg, fg, nom):
    """Format horizontal : le décor (270 de large) est prolongé de 105 pixels de chaque côté (en miroir) → 480 de large.
    La vidéo 16:9 est une fenêtre dans cette scène élargie : les positions des persos restent celles du format vertical."""
    def conv(a):
        pad = ((0, 0), (105, 105)) + (((0, 0),) if a.ndim == 3 else ())
        return np.pad(a, pad, mode="symmetric")
    nb = Px(480, 480)
    nb.a, nb.al = conv(bg.a), conv(bg.al)
    if getattr(bg, "lointain", None) is not None:
        nb.lointain, nb.ciel_m = conv(bg.lointain), conv(bg.ciel_m)
    nf = None
    if fg is not None:
        nf = Px(480, 480, alpha=True)
        nf.a, nf.al = conv(fg.a), conv(fg.al)
    return nb, nf


def spot(nom, fmt="portrait"):
    """Places conseillées des persos (pieds en pixels écran, coordonnées du format vertical, valables aussi en 16:9)."""
    return dict(SPOTS.get(nom, dict(gauche=(300, 1340), droite=(780, 1340), k=7, opts={})))


# =================================================================== registre
DECORS = dict(cuisine=cuisine, cuisine_nuit=lambda: cuisine("nuit"), cuisine_soir=lambda: cuisine("soir"),
              rue=rue, rue_soir=lambda: rue("soir"), rue_nuit=lambda: rue("nuit"),
              rue_proche=rue_proche, rue_proche_soir=lambda: rue_proche("soir"),
              rue_proche_nuit=lambda: rue_proche("nuit"),
              parc=parc, parc_soir=lambda: parc("soir"), parc_nuit=lambda: parc("nuit"),
              chambre_ado=chambre_ado, classe=classe, classe_soir=lambda: classe("soir"),
              bureau=bureau, bureau_soir=lambda: bureau("soir"), bureau_nuit=lambda: bureau("nuit"),
              snack=snack, snack_nuit=lambda: snack("nuit"),
              voiture=voiture_int, voiture_soir=lambda: voiture_int("soir"), voiture_nuit=lambda: voiture_int("nuit"),
              metro=metro, supermarche=supermarche, salle_sport=salle_sport,
              hopital=hopital, hopital_nuit=lambda: hopital("nuit"), cafe=cafe, cafe_soir=lambda: cafe("soir"),
              studio=studio, plateau_tv=plateau_tv,
              desert=desert, desert_soir=lambda: desert("soir"), desert_nuit=lambda: desert("nuit"),
              palais=palais, bibliotheque=bibliotheque, bibliotheque_nuit=lambda: bibliotheque("nuit"), labo=labo,
              village=village, village_soir=lambda: village("soir"), temple=temple, temple_soir=lambda: temple("soir"),
              toit=toit, toit_soir=lambda: toit("soir"), foret=foret, foret_jour=lambda: foret("jour"), espace=espace,
              plage=plage, plage_soir=lambda: plage("soir"), tribunal=tribunal,
              tableau_blanc=tableau_blanc, ecran_info=ecran_info, tableau_parchemin=tableau_parchemin,
              carte_rouge=lambda: sets.carte_titre((150, 30, 44), (110, 20, 32)),
              carte_bleue=lambda: sets.carte_titre((30, 64, 136), (20, 44, 100)),
              carte_violette=lambda: sets.carte_titre((70, 40, 110), (50, 26, 80)),
              carte_sepia=lambda: sets.carte_titre((124, 86, 50), (92, 62, 34)),
              carte_verte=lambda: sets.carte_titre((30, 110, 62), (20, 80, 44)),
              carte_noire=lambda: sets.carte_titre((36, 36, 44), (22, 22, 28)),
              noir=lambda: (Px(bg=(10, 10, 16)), None),
              entree=entree, entree_nuit=lambda: entree("nuit"),
              aeroport=aeroport, aeroport_nuit=lambda: aeroport("nuit"), avion=avion, avion_nuit=lambda: avion("nuit"),
              stade=stade, stade_nuit=lambda: stade("nuit"), marche=marche, marche_soir=lambda: marche("soir"),
              prison=prison, prison_nuit=lambda: prison("nuit"), prison_barreaux=lambda: prison("jour", True),
              couloir_ecole=couloir_ecole)

# placements conseillés (pieds en pixels écran 1080x1920) : gauche, droite ; échelle 7 ; options de pose
SPOTS = {name: dict(gauche=(300, 1340), droite=(780, 1340), k=7, opts={}) for name in DECORS}
for _n in ("voiture", "voiture_soir", "voiture_nuit"):
    SPOTS[_n] = dict(gauche=(330, 1268), droite=(756, 1268), k=8, opts=dict(assis=True))
SPOTS["studio"] = dict(gauche=(300, 1384), droite=(780, 1384), k=8, opts=dict(assis=True))
for _n in ("avion", "avion_nuit"):
    SPOTS[_n] = dict(gauche=(330, 1360), droite=(756, 1360), k=8, opts=dict(assis=True))
SPOTS["plateau_tv"] = dict(gauche=(300, 1368), droite=(780, 1368), k=8, opts=dict(assis=True))

sets.DECORS.update(DECORS)
