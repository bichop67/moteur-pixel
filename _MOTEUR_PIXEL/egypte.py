# DÉCORS DE L'ÉGYPTE ANCIENNE ET DE MADYAN (film « L'histoire du prophète Moussa ») — format 16:9 avant tout.
# Dessinés comme les décors de lieux.py (pixels du dessin x4 à l'écran) mais composés en LARGE : en 16:9 la toile va
# de x = -105 à x = 375 ; la fenêtre visible va de y = CADRAGE à CADRAGE + 270. Les persos gardent leurs places
# habituelles (pieds vers y = 1340 en pixels écran, soit 335 dans le dessin).
#   nil (+ _aube, _soir, _nuit) : le Nil, la maison de briques au bord de l'eau, roseaux et papyrus, palais au loin
import math

import numpy as np

import lieux
import sets
from lieux import dk, lt, mix, R, palmier, relief


class PxFilm(lieux.PxLarge):
    """Toile 16:9 des décors du film : dessinés directement en large (x = -105 … 375), donc SANS la règle des décors
    verticaux qui étire jusqu'au bord de l'image tout ce qui touche x = 0 ou x = 270 (elle créait des bandes parasites)."""

    def _bx(s, x):
        return x

    def mask_rect(s, x0, y0, x1, y1):
        """Bornes INCLUSES (comme les sprites des persos) : mask_rect(x, y, x, y) = 1 pixel, une ligne fine se voit."""
        return lieux._PxBase.mask_rect(s, x0 + s.ox, y0, x1 + s.ox + 1, y1 + 1)


def _Px(*a, **k):
    cls = lieux.Px                    # Px ou PxLarge (16:9) selon le moment (lieux.decor_large échange la classe)
    return (PxFilm if cls is lieux.PxLarge else cls)(*a, **k)


CIELS = dict(aube=((96, 112, 168), (250, 190, 150)), jour=((104, 168, 232), (206, 228, 246)),
             soir=((84, 66, 128), (250, 160, 104)), nuit=((10, 14, 38), (36, 44, 88)))


def _ciel(c, heure, y1, soleil=None, seed=3):
    sky = c.mask_rect(-105, 0, 375, y1)
    top, bot = CIELS[heure]
    c.vgrad(sky, 0, y1, top, bot, steps=8)
    rnd = R(seed)
    if heure == "nuit":
        for _ in range(140):
            x, y = rnd.randint(-105, 374), rnd.randint(0, y1 - 8)
            c.px(x, y, (232, 232, 255) if rnd.random() < 0.35 else (140, 146, 206))
        if soleil:
            ax, ay = soleil
            moon = c.mask_ell(ax, ay, 8, 8) & ~c.mask_ell(ax + 4, ay - 3, 7, 7)
            c.fill(moon, (252, 240, 204))
            c.glow(ax, ay, 30, (190, 196, 255), 0.18, m=sky)
    elif soleil:
        ax, ay = soleil
        col = dict(aube=(255, 210, 160), jour=(255, 248, 214), soir=(255, 196, 120))[heure]
        c.glow(ax, ay, 70 if heure != "jour" else 46, col, 0.4, m=sky)
        c.fill(c.mask_ell(ax, ay, 10, 10) & sky, lt(col, 0.3))
    return sky


def _papyrus(c, x, y_base, h, col, seed=1, n=7):
    """Touffe de papyrus : tiges fines + ombelles en éventail."""
    rnd = R(seed)
    for i in range(n):
        dx = rnd.uniform(-8, 8)
        hh = h * rnd.uniform(0.7, 1.05)
        lean = rnd.uniform(-6, 6)
        x0, x1 = x + dx, x + dx + lean
        for t in np.linspace(0, 1, int(hh)):
            c.px(int(round(x0 + (x1 - x0) * t)), int(round(y_base - hh * t)), dk(col, 0.82) if i % 2 else col)
        tx, ty = x1, y_base - hh
        for k in range(9):                                       # ombelle
            a = -math.pi / 2 + (k - 4) * 0.32
            for r in range(1, 7):
                c.px(int(round(tx + math.cos(a) * r)), int(round(ty + math.sin(a) * r * 0.8)), lt(col, 0.12) if r > 4 else col)


def _roseaux(c, x0, x1, y_base, h, col, seed=2):
    rnd = R(seed)
    for x in range(int(x0), int(x1)):
        if rnd.random() < 0.55:
            hh = int(h * rnd.uniform(0.4, 1.0))
            lean = rnd.choice((-1, 0, 0, 1))
            for j in range(hh):
                c.px(x + (lean if j > hh * 0.6 else 0), y_base - j, col if j < hh - 2 else lt(col, 0.2))


def nil(heure="jour"):
    """Le Nil : la maison de briques de la mère de Moussa à gauche, l'escalier qui descend à l'eau et le piquet de la
    corde, le fleuve large, roseaux et papyrus ; sur l'autre rive, des palmiers et, au loin à droite, le palais."""
    c = _Px()
    nuit = heure == "nuit"
    soleil = dict(aube=(300, 214), jour=(220, 60), soir=(40, 206), nuit=(250, 70))[heure]
    sky = _ciel(c, heure, 232, soleil)
    snap = c.a.copy()
    amb = dict(aube=(0.92, 0.84, 0.86), jour=(1.0, 1.0, 1.0), soir=(1.0, 0.82, 0.72), nuit=(0.42, 0.46, 0.72))[heure]

    def T(col):
        return tuple(int(min(255, v * a)) for v, a in zip(col, amb))
    # rive d'en face : bande de terre, palmiers, palais au loin
    c.fill(c.mask_rect(-105, 220, 375, 233), T((176, 156, 112)))
    c.fill(c.mask_rect(-105, 228, 375, 233), T((120, 110, 80)))
    loin = mix(T((64, 110, 70)), CIELS[heure][1], 0.55)                     # perspective : le lointain pâlit
    rr = R(21)
    for i in range(16):                                                  # rangée lointaine, petite et pâle
        x = -100 + i * 24 + rr.randint(-6, 6)
        palmier(c, x, 222, h=rr.randint(12, 20), lean=rr.randint(-5, 5), seed=40 + i, col=loin,
                trunk=mix(T((120, 92, 60)), CIELS[heure][1], 0.5))
    for x0, w in ((-30, 22), (120, 30), (196, 18)):                     # petites maisons sur l'autre rive
        mm = mix(T((200, 176, 130)), CIELS[heure][1], 0.35)
        c.fill(c.mask_rect(x0, 214, x0 + w, 226), mm)
        c.fill(c.mask_rect(x0 + 3, 218, x0 + 6, 223), dk(mm, 0.6))
    for i, x in enumerate((-92, -70, -24, 30, 58, 104, 160, 214)):
        palmier(c, x + rr.randint(-4, 4), 228, h=24 + rr.randint(0, 18), lean=rr.randint(-8, 8), seed=10 + i,
                col=T((64, 110, 70)), trunk=T((120, 92, 60)))
    pal = T((214, 196, 160))                                             # le palais de Pharaon, au loin
    for x0, x1, y0 in ((250, 262, 186), (338, 350, 186)):              # deux pylônes
        c.shape(c.mask_poly([(x0, 228), (x1, 228), (x1 - 2, y0), (x0 + 2, y0)]), pal, dk(pal, 0.82), band=1)
    c.shape(c.mask_rect(262, 200, 338, 228), dk(pal, 0.94), dk(pal, 0.78), band=1)
    for x in range(266, 338, 8):                                         # colonnade
        c.fill(c.mask_rect(x, 203, x + 3, 226), lt(pal, 0.14))
    c.fill(c.mask_rect(262, 198, 338, 201), dk(pal, 0.7))
    if not nuit:
        c.fill(c.mask_rect(296, 214, 304, 228), dk(pal, 0.5))           # porte
    else:
        for x in (272, 296, 320):
            c.fill(c.mask_rect(x, 208, x + 3, 212), (255, 200, 110))
            c.glow(x + 1, 210, 8, (255, 180, 90), 0.25)
    # le fleuve : dégradé + reflets en bandes
    river = c.mask_rect(-105, 233, 375, 304)
    eau = dict(aube=((96, 120, 150), (70, 100, 130)), jour=((70, 140, 170), (40, 104, 140)),
               soir=((150, 110, 110), (90, 80, 110)), nuit=((24, 34, 70), (14, 22, 50)))[heure]
    c.vgrad(river, 233, 304, eau[0], eau[1], steps=6)
    rnd = R(7)
    for _ in range(90):
        x, y = rnd.randint(-105, 360), rnd.randint(236, 300)
        L = rnd.randint(4, 14)
        c.fill(c.mask_rect(x, y, x + L, y + 1) & river, lt(mix(eau[0], eau[1], (y - 233) / 70), 0.2))
    sx = soleil[0]                                                       # reflet du soleil / de la lune
    for y in range(234, 300, 3):
        w = max(1, int(10 - (y - 234) / 9))
        c.fill(c.mask_rect(sx - w + rnd.randint(-2, 2), y, sx + w + rnd.randint(-2, 2), y + 1) & river,
               (255, 236, 190) if not nuit else (200, 206, 250))
    _roseaux(c, -105, 375, 236, 6, T((90, 120, 70)), seed=3)              # roseaux de l'autre rive (dans l'eau)
    if heure in ("aube", "soir"):                                        # nappes de brume sur le fleuve
        for y0, k in ((236, 0.38), (250, 0.22), (268, 0.14)):
            band = c.mask_rect(-105, y0, 375, y0 + 6)
            c.tint(band, (250, 236, 226), k)
    # la rive où l'on est : terre, herbe, escalier, piquet
    bank = c.mask_poly([(-105, 300), (40, 296), (120, 302), (220, 298), (375, 304), (375, 480), (-105, 480)])
    terre = T((150, 118, 80))
    c.vgrad(bank, 296, 420, lt(terre, 0.12), dk(terre, 0.8), steps=6)
    c.fill(bank & c.mask_rect(-105, 296, 375, 301), T((96, 130, 70)))
    for k in range(70):
        x, y = rnd.randint(-105, 370), rnd.randint(304, 420)
        c.px(x, y, dk(terre, 0.82)); c.px(x + 1, y, dk(terre, 0.82))
    for x in (34, 44, 54):                                               # marches vers l'eau
        y = 300 + (x - 34) // 3
        c.shape(c.mask_rect(x, y, x + 12, y + 4), T((170, 150, 120)), T((120, 100, 80)), band=1)
    c.shape(c.mask_rect(70, 290, 73, 310), T((110, 80, 50)), T((80, 56, 34)), band=1)    # piquet
    c.fill(c.mask_ell(71, 306, 4, 2), T((190, 170, 120)))                                 # corde enroulée
    # la maison de briques crues, à gauche
    mur = T((196, 160, 110))
    house = c.mask_rect(-104, 236, 22, 318)
    c.shape(house, mur, dk(mur, 0.8), lt(mur, 0.12), band=2)
    for y in range(240, 318, 6):                                         # lits de briques
        c.fill(house & c.mask_rect(-104, y, 22, y), dk(mur, 0.9))
        off = 0 if (y // 6) % 2 else 5
        for x in range(-104 + off, 22, 10):
            c.px(x, y + 3, dk(mur, 0.88))
    c.shape(c.mask_rect(-106, 230, 26, 237), lt(mur, 0.1), dk(mur, 0.75), band=1)          # toit plat
    door = c.mask_rect(2, 276, 18, 318)
    c.fill(door, T((70, 44, 30)) if not nuit else (60, 40, 30))
    c.fill(c.mask_rect(2, 274, 18, 276), dk(mur, 0.7))
    win = c.mask_rect(-60, 262, -44, 276)
    if nuit:
        c.fill(win, (255, 196, 110)); c.glow(-52, 269, 26, (255, 170, 90), 0.3)
    else:
        c.fill(win, T((60, 40, 30)))
    c.outline(win, dk(mur, 0.6))
    if nuit:
        c.glow(10, 300, 30, (255, 170, 90), 0.12)
    for jx, jy, jc in ((-30, 318, (176, 110, 70)), (-20, 320, (150, 92, 60)), (-80, 322, (190, 130, 80))):   # jarres
        jar = c.mask_ell(jx, jy - 6, 5, 7) | c.mask_rect(jx - 2, jy - 15, jx + 2, jy - 11)
        c.shape(jar, T(jc), dk(T(jc), 0.72), lt(T(jc), 0.2), band=1)
    mat = c.mask_poly([(-60, 322), (-36, 322), (-40, 330), (-66, 330)])                         # natte de roseaux
    c.fill(mat, T((190, 160, 100)))
    for x in range(-64, -38, 3):
        c.fill(mat & c.mask_rect(x, 322, x, 330), T((160, 130, 80)))
    palmier(c, 30, 312, h=78, lean=12, seed=31, col=T((60, 120, 66)), trunk=T((130, 98, 62)))
    for k in range(40):                                                  # touffes d'herbe sur la rive
        x, y = rnd.randint(-100, 370), rnd.randint(306, 400)
        for j in range(rnd.randint(2, 5)):
            c.px(x + j - 1, y - (j % 3), T((92, 126, 64)) if j % 2 else T((120, 150, 80)))
    for k in range(18):                                                  # cailloux
        x, y = rnd.randint(-100, 370), rnd.randint(310, 410)
        c.fill(c.mask_ell(x, y, 2, 1), T((176, 160, 136)))
    for y0, k in ((392, 0.10), (404, 0.18), (414, 0.26)):                  # premier plan plus sombre (profondeur)
        c.tint(c.mask_rect(-105, y0, 375, 480), (40, 24, 20), k)
    _roseaux(c, 86, 150, 302, 14, T((84, 120, 60)), seed=5)               # roseaux au bord, derrière les persos
    _roseaux(c, 236, 300, 303, 16, T((84, 120, 60)), seed=6)
    _papyrus(c, 118, 304, 30, T((70, 120, 60)), seed=8, n=6)
    _papyrus(c, 300, 306, 34, T((70, 120, 60)), seed=9, n=7)
    # premier plan : grands papyrus dans les coins (devant les persos)
    fg = _Px(alpha=True)
    _papyrus(fg, -88, 430, 96, T((54, 96, 52)), seed=11, n=9)
    _papyrus(fg, 360, 430, 104, T((54, 96, 52)), seed=12, n=9)
    return relief(c, snap, sky), fg



def _colonne_lotus(c, x, y_top, y_bot, w, pierre, peint=True):
    """Colonne égyptienne : fût en papyrus (cannelures), bandes peintes, chapiteau en fleur de lotus ouverte."""
    fut = c.mask_rect(x - w // 2, y_top + 14, x + w // 2, y_bot - 6)
    c.shape(fut, pierre, dk(pierre, 0.74), lt(pierre, 0.14), band=2)
    for fx in range(x - w // 2 + 3, x + w // 2 - 1, 4):
        c.fill(fut & c.mask_rect(fx, y_top + 14, fx, y_bot - 6), dk(pierre, 0.9))
    if peint:
        for k, col in enumerate(((40, 90, 160), (190, 60, 40), (220, 170, 60))):
            yb = y_bot - 26 - k * 4
            c.fill(fut & c.mask_rect(x - w // 2, yb, x + w // 2, yb + 2), col)
        for k, col in enumerate(((220, 170, 60), (40, 90, 160))):
            yb = y_top + 16 + k * 4
            c.fill(fut & c.mask_rect(x - w // 2, yb, x + w // 2, yb + 2), col)
    cap = c.mask_poly([(x - w // 2, y_top + 14), (x + w // 2, y_top + 14), (x + w // 2 + 8, y_top + 2),
                       (x + w // 2 + 9, y_top - 4), (x - w // 2 - 9, y_top - 4), (x - w // 2 - 8, y_top + 2)])
    c.shape(cap, (60, 130, 110), (36, 90, 80), (110, 180, 150), band=1)
    for k in range(-2, 3):                                               # pétales
        c.fill(cap & c.mask_rect(x + k * (w // 4) - 1, y_top - 4, x + k * (w // 4), y_top + 13), (220, 170, 60))
    c.shape(c.mask_rect(x - w // 2 - 10, y_top - 9, x + w // 2 + 10, y_top - 4), pierre, dk(pierre, 0.7), band=1)
    c.shape(c.mask_rect(x - w // 2 - 3, y_bot - 6, x + w // 2 + 3, y_bot), dk(pierre, 0.9), dk(pierre, 0.7), band=1)


def _brasero(c, x, y_base, nuit=False):
    c.shape(c.mask_rect(x - 1, y_base - 30, x + 1, y_base), (120, 90, 50), (80, 60, 30), band=1)
    for dx in (-8, 8):
        c.line(x, y_base - 22, x + dx, y_base, (110, 80, 44))
    bol = c.mask_ell(x, y_base - 32, 9, 4) | c.mask_rect(x - 9, y_base - 34, x + 9, y_base - 31)
    c.shape(bol, (190, 140, 60), (130, 90, 40), (240, 200, 110), band=1)
    c.fill(c.mask_ell(x, y_base - 40, 6, 8), (250, 130, 40))
    c.fill(c.mask_ell(x, y_base - 38, 3, 5), (255, 226, 130))
    c.glow(x, y_base - 40, 70 if nuit else 46, (255, 170, 80), 0.45 if nuit else 0.3)


def palais_egypte(heure="jour"):
    """Salle du trône de Pharaon : colonnes en fleur de lotus, murs peints (frises, sans écriture), estrade à trois
    marches et trône d'or, braseros, long tapis bleu, rais de lumière des fenêtres hautes."""
    c = _Px()
    nuit = heure == "nuit"
    pierre = (214, 190, 150) if not nuit else (120, 108, 120)
    mur = c.mask_rect(-105, 0, 375, 310)
    c.vgrad(mur, 0, 310, dk(pierre, 0.62), dk(pierre, 0.92), steps=6)
    for y0, col in ((40, (40, 90, 160)), (44, (220, 170, 60)), (48, (190, 60, 40))):        # frise haute
        c.fill(c.mask_rect(-105, y0, 375, y0 + 2), col if not nuit else dk(col, 0.6))
    for x in range(-104, 375, 12):                                       # zigzag peint
        c.fill(c.mask_poly([(x, 58), (x + 6, 52), (x + 12, 58), (x + 6, 54)]), (60, 130, 110) if not nuit else (40, 70, 70))
    for x0 in (-70, 200, 300):                                            # grands panneaux peints (lotus)
        pan = c.mask_rect(x0, 90, x0 + 60, 250)
        c.fill(pan, dk(pierre, 0.84))
        c.outline(pan, (220, 170, 60) if not nuit else (130, 100, 50))
        for k in range(4):
            cx, cy = x0 + 15 + (k % 2) * 30, 120 + (k // 2) * 70
            c.fill(c.mask_poly([(cx, cy + 22), (cx - 9, cy), (cx, cy + 6), (cx + 9, cy)]), (60, 130, 110) if not nuit else (40, 70, 70))
            c.fill(c.mask_ell(cx, cy + 24, 2, 2), (190, 60, 40))
    for k, (x0, x1, y0) in enumerate(((60, 210, 300), (72, 198, 290), (84, 186, 280))):    # estrade
        c.shape(c.mask_rect(x0, y0, x1, y0 + 10), lt(pierre, 0.08 * (2 - k)), dk(pierre, 0.7), band=2, sdir="bottom")
    # baldaquin derrière l'estrade : grand panneau bleu bordé d'or, corniche rayée, deux mâts dorés
    bleu, orr = ((36, 64, 130), (220, 176, 70)) if not nuit else ((24, 36, 76), (130, 100, 50))
    pan = c.mask_rect(98, 150, 172, 280)
    c.fill(pan, bleu)
    c.outline(pan, orr)
    for yy in range(160, 276, 12):                                       # semis de rosettes dorées
        for xx in range(106 + (6 if (yy // 12) % 2 else 0), 168, 12):
            c.fill(c.mask_ell(xx, yy, 1.6, 1.6), orr)
    cor = c.mask_rect(92, 138, 178, 150)                                 # corniche
    c.shape(cor, orr, dk(orr, 0.7), lt(orr, 0.3), band=1)
    for xx in range(94, 178, 4):
        c.fill(cor & c.mask_rect(xx, 140, xx + 1, 147), (40, 90, 160) if not nuit else (30, 50, 90))
    for xa in (90, 176):                                                 # mâts
        c.shape(c.mask_rect(xa, 138, xa + 4, 282), orr, dk(orr, 0.7), lt(orr, 0.3), band=1)
    for x in (30, 240):                                                  # colonnes du fond
        _colonne_lotus(c, x, 70, 300, 20, dk(pierre, 0.9))
    sol = c.mask_rect(-105, 300, 375, 480)
    c.vgrad(sol, 300, 480, dk(pierre, 0.86), dk(pierre, 0.58), steps=6)
    for y in range(306, 480, 14):                                        # dalles
        c.fill(sol & c.mask_rect(-105, y, 375, y), dk(pierre, 0.5))
    tapis = c.mask_poly([(108, 330), (162, 330), (230, 480), (40, 480)])
    c.fill(tapis, (36, 64, 130) if not nuit else (24, 36, 76))
    c.fill(tapis & ~c.mask_poly([(112, 330), (158, 330), (222, 480), (48, 480)]), (220, 170, 60) if not nuit else (130, 100, 50))
    for x in (-40, 310):
        _brasero(c, x, 300, nuit)
    if not nuit:                                                          # rais de lumière
        for x0 in (-60, 60, 180):
            c.tint(c.mask_poly([(x0, 0), (x0 + 22, 0), (x0 + 120, 310), (x0 + 80, 310)]), (255, 236, 190), 0.12)
    fg = _Px(alpha=True)                                                  # grandes colonnes du premier plan
    for x in (-86, 356):
        _colonne_lotus(fg, x, 40, 420, 34, pierre)
    if nuit:
        c.tint(c.mask_rect(-105, 0, 375, 480), (20, 16, 40), 0.25)
    return c, fg


def _eau(c, m, y0, y1, heure, sx=None, seed=7, n=90):
    """Surface d'eau dans le masque m : dégradé, reflets en bandes, scintillement du soleil (colonne sx)."""
    eau = dict(aube=((110, 130, 158), (64, 92, 124)), jour=((76, 146, 176), (36, 96, 132)),
               soir=((156, 116, 112), (84, 74, 104)), nuit=((24, 34, 70), (12, 20, 46)))[heure]
    c.vgrad(m, y0, y1, eau[0], eau[1], steps=7)
    rnd = R(seed)
    for _ in range(n):
        x, y = rnd.randint(-105, 370), rnd.randint(y0 + 2, y1 - 2)
        L = rnd.randint(4, 16)
        c.fill(c.mask_rect(x, y, x + L, y + 1) & m, lt(mix(eau[0], eau[1], (y - y0) / max(1, y1 - y0)), 0.18))
    if sx is not None:                                       # scintillement : éclats épars, plus fins au loin
        for y in range(y0 + 1, y1, 2):
            if rnd.random() < 0.45:
                w = max(1, int(8 - (y - y0) / 14) + rnd.randint(-2, 1))
                xo = sx + rnd.randint(-6, 6)
                c.fill(c.mask_rect(xo - w, y, xo + w, y) & m, (255, 236, 190) if heure != "nuit" else (200, 206, 250))
    return eau


def quai_palais(heure="jour"):
    """Le palais de Pharaon au bord du Nil : grand pylône à droite (porte, mâts à oriflammes), portique à colonnes
    lotus et terrasse plantée de palmiers, quai de pierre dont les marches descendent dans l'eau (à gauche) ;
    le fleuve vient de l'horizon et passe au premier plan. Persos debout sur le quai (pieds y = 318) ;
    le coffre flotte dans l'eau, près des marches (ex. COFFRE place 60 1400)."""
    c = _Px()
    nuit = heure == "nuit"
    soleil = dict(aube=(-40, 170), jour=(40, 70), soir=(-60, 180), nuit=(10, 80))[heure]
    sky = _ciel(c, heure, 226, soleil, seed=5)
    snap = c.a.copy()
    amb = dict(aube=(1.0, 0.9, 0.82), jour=(1.0, 1.0, 1.0), soir=(1.0, 0.82, 0.72), nuit=(0.4, 0.44, 0.7))[heure]

    def T(col):
        return tuple(int(min(255, v * a)) for v, a in zip(col, amb))
    # rive d'en face (à gauche, au loin) et palmiers pâles
    c.fill(c.mask_rect(-105, 214, 140, 228), mix(T((150, 140, 100)), CIELS[heure][1], 0.4))
    rr = R(8)
    for i in range(9):
        palmier(c, -100 + i * 26 + rr.randint(-5, 5), 218, h=rr.randint(12, 22), lean=rr.randint(-5, 5), seed=60 + i,
                col=mix(T((64, 110, 70)), CIELS[heure][1], 0.5), trunk=mix(T((120, 92, 60)), CIELS[heure][1], 0.45))
    # le fleuve : de l'horizon jusqu'au premier plan
    riv = c.mask_rect(-105, 226, 375, 480)
    _eau(c, riv, 226, 480, heure, sx=soleil[0] if heure != "jour" else None, seed=11, n=160)
    pierre = T((222, 196, 150))
    ombre = dk(pierre, 0.62)
    # terrasse haute et palmiers sur la terrasse (derrière le portique)
    c.shape(c.mask_rect(96, 162, 252, 184), dk(pierre, 0.92), dk(pierre, 0.74), lt(pierre, 0.1), band=1)
    for x in range(100, 250, 8):                                         # balustrade
        c.fill(c.mask_rect(x, 156, x + 3, 162), lt(pierre, 0.06))
    c.fill(c.mask_rect(96, 154, 252, 156), dk(pierre, 0.8))
    for i, x in enumerate((112, 150, 196, 236)):
        palmier(c, x, 158, h=26 + (i % 2) * 8, lean=(-6, 4, -3, 7)[i], seed=70 + i, col=T((58, 116, 64)), trunk=T((130, 98, 62)))
    # portique : toit à corniche, intérieur dans l'ombre, colonnes lotus
    c.fill(c.mask_rect(96, 192, 258, 262), dk(ombre, 0.62 if not nuit else 0.5))
    cor = c.mask_rect(92, 182, 256, 194)
    c.shape(cor, lt(pierre, 0.06), dk(pierre, 0.7), band=1)
    for x in range(94, 256, 4):
        c.fill(cor & c.mask_rect(x, 184, x + 1, 190), T((40, 90, 160)) if x % 8 else T((200, 150, 60)))
    for x in range(110, 246, 26):
        _colonne_lotus(c, x, 200, 264, 10, pierre)
    if nuit:                                                             # lampes sous le portique
        for x in (123, 175, 227):
            c.fill(c.mask_ell(x, 236, 2, 3), (255, 200, 110)); c.glow(x, 236, 18, (255, 170, 90), 0.35)
    # grand pylône (à droite) : deux tours trapézoïdales, porte au milieu, corniche, mâts à oriflammes
    for x0, x1 in ((252, 306), (322, 376)):
        tour = c.mask_poly([(x0, 266), (x1, 266), (x1 - 5, 122), (x0 + 5, 122)])
        c.shape(tour, pierre, dk(pierre, 0.78), lt(pierre, 0.12), band=2)
        for y in range(142, 260, 22):                                    # bandes de lits de pierre
            c.fill(tour & c.mask_rect(x0, y, x1, y), dk(pierre, 0.9))
        cc = c.mask_rect(x0 + 3, 114, x1 - 3, 124)
        c.shape(cc, lt(pierre, 0.08), dk(pierre, 0.7), band=1)
        for x in range(x0 + 4, x1 - 3, 3):
            c.fill(cc & c.mask_rect(x, 116, x, 121), T((40, 90, 160)))
        pan = c.mask_rect(x0 + 12, 152, x1 - 12, 228)                   # grand panneau peint (motifs, sans figures)
        c.fill(pan, dk(pierre, 0.9))
        c.outline(pan, T((200, 150, 60)))
        for yy in range(160, 224, 14):
            c.fill(pan & c.mask_rect(x0 + 16, yy, x1 - 16, yy + 2), T((40, 90, 160)) if (yy // 14) % 2 else T((190, 70, 50)))
    porte = c.mask_rect(306, 186, 322, 266)
    c.fill(porte, dk(pierre, 0.84))
    c.fill(c.mask_rect(309, 196, 319, 266), T((70, 46, 30)) if not nuit else (255, 196, 110))
    c.shape(c.mask_rect(302, 178, 326, 188), lt(pierre, 0.1), dk(pierre, 0.7), band=1)
    if nuit:
        c.glow(314, 236, 30, (255, 170, 90), 0.35)
    for x in (258, 300, 328, 370):                                       # mâts et oriflammes
        c.fill(c.mask_rect(x, 84, x + 1, 266), T((150, 110, 60)))
        fl = c.mask_poly([(x + 2, 86), (x + 14, 90), (x + 2, 96)])
        c.fill(fl, T((200, 50, 50)) if x % 3 else T((40, 90, 170)))
    for gx in (296, 332):                                                # deux gardes immobiles, en silhouette
        c.fill(c.mask_rect(gx - 1, 248, gx + 2, 264) | c.mask_ell(gx, 245, 2, 3), dk(ombre, 0.5))
        c.fill(c.mask_rect(gx + 4, 228, gx + 4, 264), dk(ombre, 0.6))
    # le quai : dalle claire (persos debout à y = 318), face avant qui plonge dans l'eau, marches à gauche
    quai = c.mask_poly([(58, 264), (376, 264), (376, 320), (70, 320)])
    c.vgrad(quai, 264, 320, lt(pierre, 0.06), dk(pierre, 0.86), steps=5)
    for y in (276, 290, 306):
        c.fill(quai & c.mask_rect(-105, y, 375, y), dk(pierre, 0.78))
    for x in range(80, 376, 22):
        c.fill(quai & c.mask_rect(x, 264, x, 320), dk(pierre, 0.84))
    face = c.mask_rect(70, 320, 376, 332)
    c.shape(face, dk(pierre, 0.7), dk(pierre, 0.5), band=1)
    c.fill(c.mask_rect(70, 330, 376, 332), dk(pierre, 0.42))
    for k in range(6):                                                   # marches qui descendent dans l'eau
        x0, y0 = 58 - k * 9, 300 + k * 6
        st = c.mask_rect(x0, y0, x0 + 14, y0 + 6) & ~quai
        c.shape(st, lt(pierre, 0.04), dk(pierre, 0.7), band=1, sdir="bottom")
    for x in (110, 200, 300):                                            # bornes d'amarrage
        c.shape(c.mask_rect(x, 308, x + 5, 320), dk(pierre, 0.84), dk(pierre, 0.6), band=1)
        c.fill(c.mask_rect(x - 1, 306, x + 6, 308), dk(pierre, 0.7))
    for jx in (150, 160, 250):                                           # jarres posées sur le quai
        jar = c.mask_ell(jx, 300, 4, 5) | c.mask_rect(jx - 2, 292, jx + 2, 295)
        c.shape(jar, T((180, 110, 70)), dk(T((180, 110, 70)), 0.7), lt(T((180, 110, 70)), 0.2), band=1)
    # reflets du quai dans l'eau (bande sombre ondulée sous la face)
    rr = R(4)
    for y in range(333, 350, 2):
        for x in range(70, 376, 6):
            if rr.random() < 0.6:
                c.fill(c.mask_rect(x, y, x + rr.randint(2, 5), y) & riv, dk(pierre, 0.55))
    _roseaux(c, -40, 2, 334, 9, T((84, 120, 60)), seed=14)
    if heure in ("aube", "soir"):
        for y0, k in ((228, 0.32), (240, 0.18)):
            c.tint(c.mask_rect(-105, y0, 140, y0 + 6), (250, 236, 226), k)
        c.tint(c.mask_rect(-105, 0, 375, 480), (255, 190, 120), 0.08)
    fg = _Px(alpha=True)                                                 # papyrus du premier plan, à gauche
    _papyrus(fg, -90, 470, 110, T((54, 96, 52)), seed=15, n=10)
    _papyrus(fg, -50, 476, 80, T((60, 104, 56)), seed=16, n=6)
    if nuit:
        c.tint(c.mask_rect(-105, 0, 375, 480), (16, 14, 40), 0.2)
    return relief(c, snap, sky), fg


# ---------------------------------------------------------------- cache disque des décors du film
# Un décor du film met 10 à 20 s à se dessiner ; chaque processus de rendu le redessinait. Il est maintenant dessiné une
# seule fois et gardé dans %TEMP%\ia501\decors_film (clé = nom + format + empreinte du code de dessin).
import hashlib as _hashlib
import os as _os
import pickle as _pickle
import tempfile as _tempfile

CACHE_DIR = _os.path.join(_tempfile.gettempdir(), "ia501", "decors_film")
_EMPREINTE = []
_MEM = {}
DECORS_FILM = set()


def _empreinte():
    if not _EMPREINTE:
        h = _hashlib.sha1()
        ici = _os.path.dirname(_os.path.abspath(__file__))
        # (11/11/2026) tous les fichiers decors_*.py comptent, sans liste à tenir à jour : un nouveau fichier de décors
        # oublié dans l'ancienne liste faisait ressortir du cache d'anciennes images après une retouche
        for fn in sorted(f for f in _os.listdir(ici)
                         if f in ("egypte.py", "lieux.py", "px.py", "sets.py", "madyan.py", "desert.py")
                         or (f.startswith("decors_") and f.endswith(".py"))):
            h.update(open(_os.path.join(ici, fn), "rb").read())
        _EMPREINTE.append(h.hexdigest()[:12])
    return _EMPREINTE[0]


def _avec_cache(nom, f):
    def g(*a, **k):
        large = lieux.Px is getattr(lieux, "PxLarge", None)
        cle = f"{nom}_{'L' if large else 'P'}_{_empreinte()}"
        data = _MEM.get(cle)
        if data is None:
            p = _os.path.join(CACHE_DIR, cle + ".pkl")
            try:
                if _os.path.exists(p):
                    data = open(p, "rb").read()
            except OSError:
                data = None
            if data is None:
                res = f(*a, **k)
                try:
                    data = _pickle.dumps(res, protocol=_pickle.HIGHEST_PROTOCOL)
                    _os.makedirs(CACHE_DIR, exist_ok=True)
                    tmp = p + f".{_os.getpid()}.tmp"
                    with open(tmp, "wb") as fo:
                        fo.write(data)
                    _os.replace(tmp, p)
                except Exception:                                 # noqa: BLE001 (pas de cache : on rend quand même)
                    return res
            _MEM[cle] = data
        return _pickle.loads(data)
    g.__name__ = getattr(f, "__name__", nom)
    return g


# ---------------------------------------------------------------- registre (décors, cadrage 16:9, lumières, places)
_DEC = dict(nil=nil, nil_aube=lambda: nil("aube"), nil_soir=lambda: nil("soir"), nil_nuit=lambda: nil("nuit"),
            palais_egypte=palais_egypte, palais_egypte_nuit=lambda: palais_egypte("nuit"),
            quai_palais=quai_palais, quai_palais_aube=lambda: quai_palais("aube"),
            quai_palais_soir=lambda: quai_palais("soir"), quai_palais_nuit=lambda: quai_palais("nuit"))
# FILM : persos à l'échelle du décor (k = 4 : même taille de pixel que le dessin, x4 à l'écran) ;
# SOL = ligne des pieds (pixels du dessin) ; HAUT = haut de la fenêtre du plan large (pixels du dessin) ;
# places nommées en plus de gauche / droite (ex. « PHARAON place trone » dans un scénario).
SOL_HAUT = dict(nil=(335, 130), palais_egypte=(318, 100), quai_palais=(318, 94))
PLACES = dict(palais_egypte=dict(trone=(540, 1144)))


def _places(nom):
    base = nom if nom in SOL_HAUT else nom.rsplit("_", 1)[0]
    sol, haut = SOL_HAUT.get(base, (335, 130))
    d = dict(gauche=(300, sol * 4), droite=(780, sol * 4), k=4, cy=(haut + 135) * 4, opts={})
    d.update(PLACES.get(base, {}))
    return d


def enregistre(decors, sol_haut=None, places=None):
    """Ajoute des décors du film (dict nom -> fonction) ; sol_haut / places : réglages par décor de base."""
    SOL_HAUT.update(sol_haut or {})
    PLACES.update(places or {})
    for _n, _f in decors.items():
        _g = _avec_cache(_n, _f)
        DECORS_FILM.add(_n)
        sets.DECORS[_n] = _g
        lieux.DECORS[_n] = _g
        lieux.CADRAGE[_n] = 150
        lieux.SPOTS[_n] = _places(_n)


enregistre(_DEC)
lieux.LUMIERES["palais_egypte"] = (lieux.JOUR, [(-160, 1040, 320, (255, 170, 80), 0.4), (1240, 1040, 320, (255, 170, 80), 0.4)])
lieux.LUMIERES["palais_egypte_nuit"] = (lieux.NUIT, [(-160, 1040, 420, (255, 170, 80), 0.7), (1240, 1040, 420, (255, 170, 80), 0.7)])
lieux.LUMIERES["nil_nuit"] = (lieux.NUIT, [(-210, 1076, 300, (255, 170, 90), 0.5)])
