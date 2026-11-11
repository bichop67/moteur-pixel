# DÉCORS DU FILM « L'HISTOIRE DU PROPHÈTE MOUSSA » (suite d'egypte.py) — 16:9, toile x = -105 … 375, y = 0 … 480.
# Chaque décor est enregistré avec egypte.enregistre(…) : cache disque, échelle k = 4, sol (pieds) et haut du plan large.
#   quartier (+ _soir, _nuit)      le quartier des fils d'Israël : rue de maisons de briques crues, toits plats
#   chantier (+ _nuit)            le chantier de briques : mur géant en construction, rampes, briques qui sèchent
#   route_egypte_souvenir          souvenir : la caravane de Yaqoub entre en Égypte au coucher du soleil (teinte passée)
#   reve_feu                       vision du rêve de Pharaon : le pays vu d'en haut (le feu s'anime : option « feu_reve »)
#   chambre_pharaon                la chambre de Pharaon la nuit : grand lit bas à pattes de lion, lampe, rideaux
#   maison_israelite               une pièce de maison des fils d'Israël le soir : lampe à huile, nattes, fenêtre sur la rue
import math

import numpy as np

import lieux
import egypte
from lieux import dk, lt, mix, R, palmier, relief
from egypte import _Px, _ciel, CIELS, _papyrus, _roseaux, _brasero, _colonne_lotus

BRIQUE = ((196, 160, 110), (182, 144, 98), (206, 174, 124), (174, 136, 92))


def _amb(heure):
    return dict(aube=(1.0, 0.9, 0.84), jour=(1.0, 1.0, 1.0), soir=(1.0, 0.82, 0.70), nuit=(0.40, 0.45, 0.72))[heure]


def _T(heure):
    a = _amb(heure)
    return lambda col: tuple(int(min(255, v * k)) for v, k in zip(col, a))


def _briques(c, m, mur, pas_y=6, pas_x=10, seed=1):
    """Lits de briques crues dans le masque m (joints sombres, quelques briques plus claires)."""
    ys, xs = np.where(m)
    if len(ys) == 0:
        return
    ox = getattr(c, "ox", 0)                                      # indices du tableau -> coordonnées du dessin
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min() - ox, xs.max() - ox
    rnd = R(seed)
    for y in range(int(y0) + 2, int(y1), pas_y):
        c.fill(m & c.mask_rect(int(x0), y, int(x1), y), dk(mur, 0.88))
        off = 0 if (y // pas_y) % 2 else pas_x // 2
        for x in range(int(x0) + off, int(x1), pas_x):
            c.fill(m & c.mask_rect(x, y + 1, x, y + pas_y - 1), dk(mur, 0.9))
            if rnd.random() < 0.12:
                c.fill(m & c.mask_rect(x + 1, y + 1, x + pas_x - 1, y + pas_y - 1), lt(mur, 0.06))


def _porte(c, x0, x1, y_top, y_bot, nuit, bois=(92, 60, 38), ouverte=False, arc=True):
    m = c.mask_arch(x0, x1, y_top, y_bot) if arc else c.mask_rect(x0, y_top, x1, y_bot)
    if ouverte:
        c.fill(m, (255, 206, 130) if nuit else (40, 28, 24))
        if nuit:
            c.glow((x0 + x1) // 2, (y_top + y_bot) // 2, 26, (255, 180, 100), 0.3)
    else:
        c.shape(m, bois if not nuit else dk(bois, 0.6), dk(bois, 0.7), band=1)
        for x in range(x0 + 3, x1 - 1, 4):
            c.fill(m & c.mask_rect(x, y_top, x, y_bot), dk(bois, 0.78 if not nuit else 0.5))
    c.outline(m, (60, 40, 30))
    return m


def _fenetre(c, x0, y0, w, h, nuit, lampe=True):
    m = c.mask_rect(x0, y0, x0 + w, y0 + h)
    if nuit and lampe:
        c.fill(m, (255, 196, 110))
        c.glow(x0 + w // 2, y0 + h // 2, 22, (255, 170, 90), 0.3)
    else:
        c.fill(m, (40, 30, 30) if not nuit else (20, 18, 30))
    c.fill(c.mask_rect(x0 + w // 2, y0, x0 + w // 2, y0 + h), (90, 60, 40) if not nuit else (60, 40, 30))
    c.outline(m, (70, 50, 40))


def _jarre(c, x, y, col, h=7):
    m = c.mask_ell(x, y - h * 0.6, h * 0.62, h * 0.75) | c.mask_rect(x - 1, y - int(h * 1.45), x + 1, y - int(h * 1.15))
    c.shape(m, col, dk(col, 0.72), lt(col, 0.2), band=1)


# ================================================================ le quartier des fils d'Israël
def quartier(heure="jour"):
    """Une rue du quartier des fils d'Israël : maisons de briques crues à toits plats (escaliers, auvents de roseaux,
    jarres, four à pain), une seconde rangée de toits derrière, un palmier ; rue de terre battue où l'on marche
    (pieds y = 330). Nuit : fenêtres éclairées par les lampes à huile."""
    c = _Px()
    nuit = heure == "nuit"
    T = _T(heure)
    soleil = dict(aube=(320, 150), jour=(60, 50), soir=(-60, 150), nuit=(300, 60))[heure]
    sky = _ciel(c, heure, 200, soleil, seed=11)
    snap = c.a.copy()
    rr = R(5)
    # rangée lointaine de toits (pâle) et palmiers
    loin = mix(T((190, 160, 120)), CIELS[heure][1], 0.42)
    x = -105
    while x < 375:
        w = rr.randint(28, 52)
        top = rr.randint(150, 172)
        c.fill(c.mask_rect(x, top, x + w, 205), loin)
        c.fill(c.mask_rect(x, top - 2, x + w, top), lt(loin, 0.08))
        x += w + rr.randint(-4, 2)
    for i, px_ in enumerate((-80, 40, 150, 260, 350)):
        palmier(c, px_ + rr.randint(-8, 8), 172, h=rr.randint(24, 36), lean=rr.randint(-8, 8), seed=200 + i,
                col=mix(T((60, 116, 66)), CIELS[heure][1], 0.35), trunk=mix(T((126, 94, 60)), CIELS[heure][1], 0.3))
    # rangée principale des maisons (façades)
    x = -110
    k = 0
    portes = []
    while x < 380:
        w = rr.randint(46, 78)
        top = rr.randint(176, 214)
        mur = T(BRIQUE[k % 4])
        if nuit:
            mur = dk(mur, 0.95)
        m = c.mask_rect(x, top, x + w, 304)
        c.shape(m, mur, dk(mur, 0.82), lt(mur, 0.1), band=2)
        _briques(c, m, mur, seed=30 + k)
        c.shape(c.mask_rect(x - 1, top - 4, x + w + 1, top), lt(mur, 0.08), dk(mur, 0.7), band=1)       # parapet
        for xx in range(x + 4, x + w - 2, 9):                                                           # gargouilles
            c.fill(c.mask_rect(xx, top + 1, xx + 2, top + 2), dk(mur, 0.6))
        if k % 3 == 1:                                                                                   # escalier extérieur
            for s_ in range(7):
                c.shape(c.mask_rect(x + w - 16 + s_ * 2, 300 - s_ * 9, x + w - 2, 304 - s_ * 9), lt(mur, 0.04), dk(mur, 0.74), band=1)
        dx0 = x + w // 2 - 6 + rr.randint(-6, 6)
        ouverte = (k % 4 == 2) and not nuit
        portes.append(_porte(c, dx0, dx0 + 12, 276, 304, nuit, ouverte=ouverte))
        _fenetre(c, x + 6, top + 18, 8, 7, nuit, lampe=(k % 2 == 0))
        if w > 60:
            _fenetre(c, x + w - 16, top + 22, 7, 6, nuit, lampe=(k % 3 == 0))
        if k % 3 == 0:                                                                                   # auvent de roseaux
            aw = c.mask_poly([(dx0 - 10, 270), (dx0 + 22, 270), (dx0 + 26, 276), (dx0 - 14, 276)])
            c.shape(aw, T((190, 160, 100)), T((150, 120, 70)), band=1)
            for xx in range(dx0 - 12, dx0 + 25, 3):
                c.fill(aw & c.mask_rect(xx, 270, xx, 276), T((160, 130, 80)))
            for px_ in (dx0 - 12, dx0 + 24):
                c.fill(c.mask_rect(px_, 276, px_ + 1, 304), T((120, 90, 56)))
        x += w + rr.randint(0, 3)
        k += 1
    # linge entre les toits
    for (xa, xb, y) in ((-60, 10, 186), (150, 230, 192)):
        for t in np.linspace(0, 1, 60):
            c.px(int(xa + (xb - xa) * t), int(y + 6 * math.sin(math.pi * t)), T((80, 70, 60)))
        for i in range(4):
            tx = xa + 10 + i * (xb - xa - 20) // 3
            ty = int(y + 6 * math.sin(math.pi * (tx - xa) / (xb - xa)))
            c.fill(c.mask_rect(tx - 3, ty + 1, tx + 3, ty + 8), T(((220, 210, 190), (160, 60, 50), (60, 90, 150), (210, 190, 120))[i]))
    # la rue : terre battue, ornières, cailloux
    rue = c.mask_rect(-105, 304, 375, 480)
    terre = T((170, 140, 100))
    c.vgrad(rue, 304, 480, lt(terre, 0.08), dk(terre, 0.72), steps=6)
    c.fill(c.mask_rect(-105, 304, 375, 306), dk(terre, 0.75))
    for y in (338, 352, 372):
        for x in range(-105, 375, 2):
            if rr.random() < 0.35:
                c.px(x, y + rr.randint(-1, 1), dk(terre, 0.86))
    for _ in range(60):
        x, y = rr.randint(-100, 370), rr.randint(310, 470)
        c.fill(c.mask_ell(x, y, 1.6, 1), lt(terre, 0.12))
    # accessoires : jarres, four à pain, paniers
    for (jx, col) in ((-62, (176, 110, 70)), (-52, (150, 92, 60)), (118, (190, 130, 80)), (246, (170, 104, 66)), (330, (150, 96, 64))):
        _jarre(c, jx, 312, T(col))
    four = c.mask_ell(30, 306, 10, 9) & c.mask_rect(0, 290, 60, 306)
    c.shape(four, T((176, 130, 90)), T((130, 90, 60)), band=1)
    c.fill(c.mask_ell(30, 304, 3, 3), (40, 26, 20) if not nuit else (255, 150, 60))
    for (bx, col) in ((186, (190, 150, 90)), (196, (170, 130, 80))):
        b = c.mask_rect(bx - 4, 304, bx + 4, 311)
        c.shape(b, T(col), dk(T(col), 0.7), band=1)
        for xx in range(bx - 3, bx + 4, 2):
            c.fill(b & c.mask_rect(xx, 304, xx, 311), dk(T(col), 0.85))
    for y0, kk in ((420, 0.10), (440, 0.18), (460, 0.26)):
        c.tint(c.mask_rect(-105, y0, 375, 480), (40, 24, 20), kk)
    if nuit:
        for x in (60, 300):                                                     # lueurs des lampes sur la rue
            c.glow(x, 300, 40, (255, 170, 90), 0.12)
    fg = _Px(alpha=True)
    palmier(fg, 366, 470, h=150, lean=-16, seed=77, col=T((50, 104, 56)), trunk=T((110, 80, 52)))
    return relief(c, snap, sky), fg


# ================================================================ le chantier de briques
def chantier(heure="jour"):
    """Le chantier : un mur géant en construction (rampe de terre, échafaudages, ouvriers minuscules au loin), des
    rangées de briques qui sèchent au soleil, des fosses de boue, de la paille, des jarres. Pieds y = 330.
    Nuit : torches plantées le long du chantier, ciel sombre ; on travaille encore."""
    c = _Px()
    nuit = heure == "nuit"
    T = _T(heure)
    soleil = dict(aube=(300, 150), jour=(220, 40), soir=(-50, 140), nuit=(40, 60))[heure]
    sky = _ciel(c, heure, 190, soleil, seed=21)
    if heure == "jour":                                                         # brume de chaleur, ciel blanchi
        c.tint(sky, (255, 246, 220), 0.22)
    snap = c.a.copy()
    rr = R(9)
    # au loin : le désert et la vallée, dans la brume
    loin = mix(T((200, 170, 120)), CIELS[heure][1], 0.5)
    c.fill(c.mask_rect(-105, 186, 375, 292), loin)
    for i in range(12):
        palmier(c, -100 + i * 42 + rr.randint(-8, 8), 206, h=rr.randint(12, 20), lean=rr.randint(-5, 5), seed=400 + i,
                col=mix(T((70, 110, 64)), CIELS[heure][1], 0.5), trunk=mix(T((120, 90, 60)), CIELS[heure][1], 0.45))
    # l'édifice géant en construction : trois gradins de briques crues, crêtes inachevées, échafaudages
    mur = T((190, 152, 106))
    for (x0, x1, y0, y1, k_) in ((-80, 250, 232, 292, 0), (-50, 214, 190, 232, 1), (-14, 170, 156, 190, 2)):
        g = c.mask_rect(x0, y0, x1, y1)
        col = lt(mur, 0.04 * k_)
        c.shape(g, col, dk(col, 0.78), lt(col, 0.1), band=2)
        _briques(c, g, col, pas_y=5, pas_x=9, seed=4 + k_)
        c.fill(c.mask_rect(x0, y1 - 3, x1, y1), dk(col, 0.7))                       # ombre au pied du gradin
        for x in range(x0, x1, 9):                                                   # crête inachevée
            h_ = rr.randint(0, 5)
            if h_ > 1:
                c.shape(c.mask_rect(x, y0 - h_, x + 8, y0), lt(col, 0.06), dk(col, 0.74), band=1)
    rampe = c.mask_poly([(150, 292), (330, 292), (214, 190), (196, 190)])        # rampe de terre jusqu'au 2e gradin
    c.shape(rampe, T((164, 126, 86)), T((124, 92, 62)), band=2)
    for i in range(10):                                                          # traces sur la rampe
        t = i / 9
        c.fill(c.mask_rect(int(205 + 70 * t), int(194 + 96 * t), int(212 + 70 * t), int(194 + 96 * t)), T((140, 106, 72)))
    for x in range(-74, 246, 30):                                                # échafaudages de bois
        c.fill(c.mask_rect(x, 160 if -14 < x < 170 else 196, x + 1, 292), T((112, 80, 50)))
        for y in (200, 240, 270):
            if rr.random() < 0.6:
                c.fill(c.mask_rect(x, y, x + 22, y + 1), T((124, 88, 54)))
    for i in range(16):                                                          # ouvriers minuscules sur la rampe
        t = i / 15
        x = int(200 + 118 * t); y = int(192 + 98 * t)
        c.fill(c.mask_rect(x, y - 6, x + 1, y), T((96, 72, 54)))
        c.fill(c.mask_rect(x - 1, y - 9, x + 2, y - 7), T((210, 180, 130)))             # le panier de terre
    for i in range(14):                                                          # et sur les gradins
        x = rr.randint(-70, 200); y = rr.choice((156, 190, 232))
        c.fill(c.mask_rect(x, y - 6, x + 1, y), T((96, 72, 54)))
    # le sol du chantier : boue sèche, fosses, briques qui sèchent
    sol = c.mask_rect(-105, 290, 375, 480)
    terre = T((176, 144, 102))
    c.vgrad(sol, 290, 480, lt(terre, 0.06), dk(terre, 0.7), steps=6)
    c.fill(c.mask_rect(-105, 290, 375, 292), dk(terre, 0.7))
    for (fx, fy, rx, ry) in ((-40, 312, 30, 6), (310, 318, 34, 7)):            # fosses de boue
        f = c.mask_ell(fx, fy, rx, ry)
        c.fill(f, T((110, 80, 56)))
        c.fill(f & c.mask_ell(fx - 4, fy - 1, rx * 0.6, ry * 0.4), T((140, 104, 72)))
    for row, y in enumerate(range(340, 420, 14)):                               # rangées de briques qui sèchent
        for x in range(-100 + (row % 2) * 6, 370, 13):
            if -60 < x < 330 or rr.random() < 0.5:
                b = c.mask_rect(x, y, x + 9, y + 4)
                c.shape(b, T((184, 140, 96)), T((140, 104, 70)), lt(T((184, 140, 96)), 0.12), band=1)
    for (px_, py_) in ((40, 300), (240, 302)):                                  # tas de paille
        p = c.mask_ell(px_, py_, 16, 6) & c.mask_rect(px_ - 20, py_ - 8, px_ + 20, py_ + 2)
        c.fill(p, T((220, 190, 110)))
        for _ in range(30):
            xx = rr.randint(px_ - 14, px_ + 14); yy = rr.randint(py_ - 5, py_)
            c.px(xx, yy, T((180, 150, 80)))
    for jx in (90, 104, 196):
        _jarre(c, jx, 318, T((170, 110, 70)), h=8)
    for y0, kk in ((430, 0.10), (450, 0.18), (466, 0.26)):
        c.tint(c.mask_rect(-105, y0, 375, 480), (40, 24, 20), kk)
    if nuit:
        c.tint(c.mask_rect(-105, 0, 375, 480), (12, 10, 34), 0.18)
        for x in (-70, 70, 200, 330):                                           # torches plantées
            lieux.torche(c, x, 276)
    else:
        c.tint(c.mask_rect(-105, 120, 375, 300), (255, 236, 200), 0.10)       # poussière dorée
    return relief(c, snap, sky), None


# ================================================================ souvenir : la caravane entre en Égypte
def route_egypte(heure="soir", souvenir=True):
    """Souvenir du temps de Youssouf : la route du désert au coucher du soleil, la vallée verte du Nil et une ville au
    loin ; teinte chaude passée et vignettage fort (souvenir). Les chameaux et les orbes sont des persos (pieds y = 335)."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 230, (60, 200), seed=31)
    snap = c.a.copy()
    rr = R(12)
    loin = mix(T((90, 120, 70)), CIELS[heure][1], 0.5)
    c.fill(c.mask_rect(-105, 214, 375, 232), loin)                                         # vallée verte
    for i in range(22):
        palmier(c, -100 + i * 22 + rr.randint(-5, 5), 220, h=rr.randint(10, 18), lean=rr.randint(-4, 4), seed=300 + i,
                col=mix(T((60, 110, 60)), CIELS[heure][1], 0.45), trunk=mix(T((120, 90, 60)), CIELS[heure][1], 0.4))
    ville = mix(T((210, 186, 140)), CIELS[heure][1], 0.4)                                  # ville au loin
    for x0, w, h in ((150, 20, 18), (172, 14, 26), (188, 30, 14), (220, 12, 22), (234, 26, 16)):
        c.fill(c.mask_rect(x0, 214 - h, x0 + w, 216), ville)
        c.fill(c.mask_rect(x0, 214 - h, x0 + w, 214 - h + 1), lt(ville, 0.1))
    dunes = [(-105, 300, 240, 0.0), (-40, 330, 252, 1.3), (60, 360, 246, 2.1)]
    sable = T((214, 170, 110))
    c.fill(c.mask_rect(-105, 228, 375, 480), mix(sable, CIELS[heure][1], 0.3))           # sol lointain (sous les dunes)
    for (x0, x1, ytop, ph) in dunes:
        m = c.yy >= ytop + 10 * np.sin((c.xx - x0) / 60.0 + ph)
        c.vgrad(m, int(ytop - 10), 480, lt(sable, 0.06), dk(sable, 0.78), steps=6)
    route = c.mask_poly([(-105, 350), (375, 320), (375, 336), (-105, 372)])
    c.fill(route, dk(sable, 0.9))
    for _ in range(80):
        x = rr.randint(-100, 370); y = rr.randint(330, 470)
        c.px(x, y, lt(sable, 0.1))
    if souvenir:                                                                           # le souvenir : teinte passée
        a = c.a.astype(np.float32)
        g = a.mean(axis=2, keepdims=True)
        sep = np.concatenate([g * 1.08 + 18, g * 0.94 + 8, g * 0.74], axis=2)
        c.a = np.clip(a * 0.35 + sep * 0.65, 0, 255).astype(np.uint8)
    return relief(c, snap, sky), None


# ================================================================ vision du rêve de Pharaon
# Points (dessin) : la ville au loin d'où sort le feu, le chemin du feu, les maisons des Égyptiens (qui s'enflamment)
# et celles des fils d'Israël (qui restent sombres). L'animation « feu_reve » les utilise.
REVE_SOURCE = (318, 150)
REVE_CHEMIN = [(318, 150), (290, 176), (250, 190), (206, 210), (160, 232), (118, 256), (80, 280)]
REVE_EGYPTIENS = [(60, 284), (96, 300), (40, 310), (122, 318), (74, 326), (148, 300), (20, 290), (112, 342)]
REVE_ISRAELITES = [(180, 330), (200, 342), (166, 350), (214, 322)]


def reve_feu():
    """Vision : le pays vu de très haut, teinte rouge et sombre, bords flous ; au loin (en haut à droite) la ville d'où
    sort le feu ; en bas à gauche, l'Égypte et le Nil ; un quartier à part (les fils d'Israël)."""
    c = _Px()
    fond = c.mask_rect(-105, 0, 375, 480)
    c.vgrad(fond, 0, 480, (40, 12, 16), (90, 40, 24), steps=8)
    rr = R(41)
    for _ in range(260):                                                       # relief du désert (taches)
        x = rr.randint(-100, 370); y = rr.randint(100, 470)
        c.fill(c.mask_ell(x, y, rr.randint(3, 9), rr.randint(1, 3)), (110, 52, 30) if rr.random() < 0.5 else (74, 30, 22))
    for t in np.linspace(0, 1, 400):                                           # le Nil (ruban sombre)
        x = int(-40 + 160 * t + 14 * math.sin(t * 9))
        y = int(470 - 220 * t)
        c.fill(c.mask_ell(x, y, 4, 2), (40, 30, 60))
    x0, y0 = REVE_SOURCE                                                       # la ville d'où sort le feu
    for dx, dy, w, h in ((-14, -6, 8, 8), (-4, -10, 10, 12), (8, -4, 8, 6), (-8, 2, 16, 4)):
        c.fill(c.mask_rect(x0 + dx, y0 + dy, x0 + dx + w, y0 + dy + h), (130, 90, 70))
    c.outline(c.mask_rect(x0 - 18, y0 - 12, x0 + 18, y0 + 8), (60, 30, 24))
    for (x, y) in REVE_EGYPTIENS + REVE_ISRAELITES:                             # les maisons
        m = c.mask_rect(x - 4, y - 3, x + 4, y + 3)
        c.shape(m, (150, 104, 80), (100, 64, 50), band=1)
        c.fill(c.mask_rect(x - 1, y - 1, x + 1, y + 1), (40, 20, 18))
    yy, xx = c.yy, c.xx                                                        # bords flous et sombres (vision)
    d = np.hypot((xx - 135) / 260.0, (yy - 260) / 200.0)
    a = c.a.astype(np.float32)
    k = np.clip((d - 0.6) / 0.6, 0, 1)[..., None]
    c.a = (a * (1 - 0.8 * k)).astype(np.uint8)
    return c, None


# ================================================================ la chambre de Pharaon
def chambre_pharaon(heure="nuit"):
    """La chambre de Pharaon la nuit : murs sombres à frises d'or, grand lit bas à pattes de lion et appui-tête, deux
    colonnes, rideaux, une lampe sur pied (sa flamme vacille : option « feu »), fenêtre sur la nuit. Pharaon s'assoit au
    bord du lit (« PHARAON place lit, sur le lit »). Pieds y = 330."""
    c = _Px()
    mur = (62, 48, 72)
    m = c.mask_rect(-105, 0, 375, 304)
    c.vgrad(m, 0, 304, dk(mur, 0.7), mur, steps=6)
    for y0, col in ((60, (150, 116, 50)), (64, (40, 70, 120)), (68, (150, 116, 50))):
        c.fill(c.mask_rect(-105, y0, 375, y0 + 2), col)
    fen = c.mask_rect(-60, 110, -10, 200)                                      # fenêtre : la nuit, la lune
    c.fill(fen, (16, 20, 46))
    re_ = R(3)
    for _ in range(18):
        c.px(re_.randint(-58, -12), re_.randint(112, 198), (200, 200, 240))
    c.fill(c.mask_ell(-26, 132, 6, 6) & ~c.mask_ell(-23, 130, 5, 5), (240, 232, 200))
    c.outline(fen, (120, 96, 50))
    c.fill(c.mask_rect(-36, 110, -35, 200), (80, 64, 40))
    for x in (90, 300):                                                        # deux colonnes
        _colonne_lotus(c, x, 60, 304, 18, (130, 116, 120))
    for x0, x1 in ((40, 70), (320, 350)):                                      # rideaux
        r = c.mask_poly([(x0, 70), (x1, 70), (x1 + 6, 304), (x0 - 4, 304)])
        c.shape(r, (110, 40, 50), (70, 24, 34), (150, 70, 80), band=2)
        for x in range(x0, x1, 5):
            c.fill(r & c.mask_rect(x, 70, x, 304), (84, 30, 40))
    sol = c.mask_rect(-105, 304, 375, 480)
    c.vgrad(sol, 304, 480, (70, 56, 60), (36, 28, 34), steps=6)
    for y in range(312, 480, 14):
        c.fill(sol & c.mask_rect(-105, y, 375, y), (52, 40, 46))
    tapis = c.mask_poly([(120, 330), (290, 330), (320, 380), (90, 380)])
    c.fill(tapis, (40, 60, 110))
    c.fill(tapis & ~c.mask_poly([(124, 333), (286, 333), (314, 377), (96, 377)]), (170, 130, 60))
    # le lit : cadre d'or, pattes de lion, matelas blanc, appui-tête (Pharaon s'assoit à x = 150 environ)
    orr, orr_s = (200, 150, 60), (140, 100, 40)
    c.shape(c.mask_rect(132, 318, 286, 322), orr, orr_s, band=1)                   # cadre (lit bas)
    for x in (134, 280):
        p = c.mask_rect(x, 322, x + 5, 328) | c.mask_rect(x - 1, 327, x + 6, 330)
        c.shape(p, orr, orr_s, band=1)
    c.shape(c.mask_rect(134, 311, 284, 318), (230, 224, 210), (190, 184, 170), band=1)  # matelas
    c.fill(c.mask_rect(134, 311, 284, 312), (250, 248, 240))
    tete = c.mask_poly([(268, 311), (282, 311), (284, 295), (280, 293), (276, 303), (272, 303), (268, 293), (264, 295)])
    c.shape(tete, orr, orr_s, band=1)
    for x in (128, 292):                                                       # montants de baldaquin
        c.shape(c.mask_rect(x, 210, x + 3, 322), orr, orr_s, band=1)
    voile = c.mask_poly([(128, 210), (295, 210), (300, 230), (124, 230)])
    c.tint(voile, (230, 220, 210), 0.5)
    lp = c.mask_rect(340, 250, 342, 318) | c.mask_rect(334, 316, 348, 318)    # lampe sur pied
    c.shape(lp, orr, orr_s, band=1)
    c.shape(c.mask_ell(341, 248, 6, 3), orr, orr_s, band=1)
    c.fill(c.mask_ell(341, 242, 2, 4), (255, 200, 110))
    c.glow(341, 240, 60, (255, 170, 90), 0.4)
    c.glow(341, 240, 120, (255, 150, 80), 0.12)
    c.tint(c.mask_rect(-105, 0, 375, 480), (20, 16, 50), 0.15)
    return c, None


# ================================================================ une pièce de maison des fils d'Israël
def maison_israelite(heure="nuit"):
    """Une pièce pauvre aux murs de briques crues, des nattes au sol, une lampe à huile posée par terre au milieu (les
    visages sont éclairés par en dessous), des jarres, une niche, une petite fenêtre sur la rue (les torches d'une
    patrouille y passent : option « patrouille »). On s'assoit par terre (« assis par terre »). Pieds y = 330."""
    c = _Px()
    nuit = heure == "nuit"
    mur = (150, 116, 84) if nuit else (190, 150, 106)
    m = c.mask_rect(-105, 0, 375, 306)
    c.vgrad(m, 0, 306, dk(mur, 0.55), mur, steps=6)
    _briques(c, m, mur, pas_y=7, pas_x=12, seed=8)
    for x0, x1 in ((-105, -90), (360, 375)):                                       # poutres d'angle
        c.fill(c.mask_rect(x0, 0, x1, 306), dk(mur, 0.7))
    c.shape(c.mask_rect(-105, 40, 375, 46), (100, 70, 44), (70, 48, 30), band=1)  # poutre du plafond
    fen = c.mask_rect(250, 150, 290, 190)                                          # petite fenêtre sur la rue
    c.fill(fen, (18, 22, 46) if nuit else (170, 200, 230))
    c.outline(fen, (80, 56, 36))
    c.fill(c.mask_rect(270, 150, 271, 190), (80, 56, 36))
    niche = c.mask_arch(40, 64, 170, 206)
    c.fill(niche, dk(mur, 0.6))
    _jarre(c, 52, 205, (170, 110, 70), h=6)
    eta = c.mask_rect(-60, 200, 20, 204)                                            # étagère : bols et cruches
    c.shape(eta, (110, 76, 46), (80, 54, 32), band=1)
    for i, x in enumerate(range(-54, 16, 12)):
        if i % 2:
            _jarre(c, x, 199, (160, 104, 66), h=5)
        else:
            c.shape(c.mask_ell(x, 197, 4, 2) & c.mask_rect(x - 5, 196, x + 5, 199), (190, 150, 100), (140, 100, 70), band=1)
    for i in range(5):                                                              # herbes séchées pendues
        x = 180 + i * 7
        c.fill(c.mask_rect(x, 46, x, 70), (80, 60, 40))
        c.fill(c.mask_ell(x, 74, 2.5, 5), (110, 130, 70) if i % 2 else (140, 120, 60))
    for (nx, ny) in ((300, 296), (316, 298)):                                       # nattes roulées contre le mur
        n_ = c.mask_ell(nx, ny, 7, 4)
        c.shape(n_, (190, 160, 100), (150, 120, 70), band=1)
        c.fill(c.mask_ell(nx - 5, ny, 1.5, 3), (140, 110, 60))
    met = c.mask_rect(-30, 230, -27, 306) | c.mask_rect(0, 230, 3, 306) | c.mask_rect(-30, 230, 3, 233)   # métier à tisser
    c.shape(met, (120, 84, 50), (90, 60, 36), band=1)
    for x in range(-26, 0, 2):
        c.fill(c.mask_rect(x, 234, x, 296), (200, 180, 140) if x % 4 else (150, 60, 50))
    pan = c.mask_ell(230, 312, 8, 5) & c.mask_rect(220, 306, 240, 316)               # panier de pain
    c.shape(pan, (170, 130, 70), (130, 96, 50), band=1)
    c.fill(c.mask_ell(228, 307, 3, 2), (210, 170, 100)); c.fill(c.mask_ell(234, 308, 3, 2), (200, 160, 90))
    sol = c.mask_rect(-105, 306, 375, 480)
    c.vgrad(sol, 306, 480, (130, 100, 72), (70, 52, 40), steps=6)
    for (x0, x1, y0, y1, col) in ((-40, 110, 318, 360, (190, 160, 100)), (160, 320, 322, 368, (176, 146, 92))):
        nat = c.mask_poly([(x0, y0), (x1, y0), (x1 + 10, y1), (x0 - 10, y1)])
        c.fill(nat, col)
        for x in range(x0 - 8, x1 + 10, 4):
            c.fill(nat & c.mask_rect(x, y0, x, y1), dk(col, 0.86))
    for (jx, col) in ((-70, (170, 104, 66)), (-56, (150, 92, 60)), (330, (176, 120, 76))):
        _jarre(c, jx, 312, col, h=9)
    lx, ly = 135, 336                                                              # la lampe à huile, au milieu
    lampe = c.mask_ell(lx, ly, 6, 2.5) | c.mask_poly([(lx + 4, ly - 1), (lx + 9, ly - 3), (lx + 9, ly - 1)])
    c.shape(lampe, (170, 110, 70), (120, 76, 50), band=1)
    c.fill(c.mask_ell(lx + 9, ly - 6, 1.6, 3), (255, 210, 120))
    if nuit:
        c.tint(c.mask_rect(-105, 0, 375, 480), (10, 8, 30), 0.42)
        c.glow(lx + 9, ly - 8, 110, (255, 170, 90), 0.42)
        c.glow(lx + 9, ly - 8, 40, (255, 210, 140), 0.35)
    return c, None


# ================================================================ registre
egypte.enregistre(
    dict(quartier=quartier, quartier_soir=lambda: quartier("soir"), quartier_nuit=lambda: quartier("nuit"),
         quartier_aube=lambda: quartier("aube"),
         chantier=chantier, chantier_nuit=lambda: chantier("nuit"), chantier_soir=lambda: chantier("soir"),
         route_egypte_souvenir=lambda: route_egypte("soir", True),
         reve_feu=reve_feu, chambre_pharaon=chambre_pharaon,
         maison_israelite=maison_israelite, maison_israelite_jour=lambda: maison_israelite("jour")),
    sol_haut=dict(quartier=(330, 116), chantier=(330, 110), route_egypte=(322, 100), reve_feu=(330, 96),
                  chambre_pharaon=(330, 100), maison_israelite=(330, 100)),
    places=dict(chambre_pharaon=dict(lit=(620, 1320))))
lieux.LUMIERES["quartier_nuit"] = (lieux.NUIT, [(240, 1200, 200, (255, 170, 90), 0.4)])
lieux.LUMIERES["chantier_nuit"] = (lieux.NUIT, [(-280, 1080, 260, (255, 170, 80), 0.5), (280, 1080, 260, (255, 170, 80), 0.5),
                                                (800, 1080, 260, (255, 170, 80), 0.5), (1320, 1080, 260, (255, 170, 80), 0.5)])
lieux.LUMIERES["chambre_pharaon"] = (lieux.NUIT, [(1364, 960, 420, (255, 170, 90), 0.7)])
lieux.LUMIERES["maison_israelite"] = (lieux.NUIT, [(576, 1312, 520, (255, 170, 90), 0.85)])


# ================================================================ animations de décor (film)
def _vers_toile(x, y):
    """Coordonnées du dessin (x = -105 … 375) -> pixels de la toile 16:9 du moteur (1920 x 1920)."""
    return int((x + 105) * 4), int(y * 4)


def anim_feu_reve(t_debut=0.0, duree=4.5, t_maisons=None, pas_maisons=0.35):
    """Le rêve de Pharaon : le feu sort de la ville lointaine (REVE_SOURCE), suit REVE_CHEMIN en `duree` secondes, puis
    entre dans les maisons des Égyptiens une à une ; celles des fils d'Israël restent sombres. Dessiné en pixels du
    décor (agrandis x4), pour rester dans le style. À poser avec {feu_reve} sur le mot voulu."""
    from PIL import Image, ImageDraw
    pts = REVE_CHEMIN
    L = [0.0]
    for a, b in zip(pts, pts[1:]):
        L.append(L[-1] + math.dist(a, b))
    tot = L[-1]
    tm = t_maisons if t_maisons is not None else t_debut + duree

    def point(dd):
        for i in range(len(pts) - 1):
            if L[i + 1] >= dd:
                e = (dd - L[i]) / max(1e-6, L[i + 1] - L[i])
                return pts[i][0] + (pts[i + 1][0] - pts[i][0]) * e, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * e
        return pts[-1]

    def flamme(d, x, y, u, s, graine):
        X, Y = x + 105, y
        f_ = 0.65 + 0.35 * math.sin(u * 8.0 + graine * 1.7)
        r = s * (0.8 + 0.4 * f_)
        d.ellipse([X - r * 2.2, Y - r * 2.6, X + r * 2.2, Y + r * 0.9], fill=(255, 80, 30, 70))
        d.ellipse([X - r * 1.3, Y - r * 2.0, X + r * 1.3, Y + r * 0.6], fill=(255, 140, 40, 170))
        d.ellipse([X - r * 0.6, Y - r * 1.2, X + r * 0.6, Y + r * 0.3], fill=(255, 230, 140, 235))

    def f(img, u):
        if u < t_debut:
            return
        p = min(1.0, (u - t_debut) / max(0.1, duree))
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        n = int(26 * p) + 1
        for i in range(n):
            x, y = point(tot * p * i / max(1, n - 1))
            flamme(d, x, y, u, 1.7, i)
        if u >= tm:
            k = min(len(REVE_EGYPTIENS), int((u - tm) / pas_maisons) + 1)
            for j, (x, y) in enumerate(REVE_EGYPTIENS[:k]):
                flamme(d, x, y - 2, u, 2.4, 40 + j)
        lieux.pose_calque(img, lay)
    return f


def anim_patrouille(fenetre=(250, 150, 290, 190), periode=7.0, decalage=0.0):
    """Par la fenêtre (rectangle du dessin), les torches d'une patrouille passent dans la rue, de gauche à droite."""
    from PIL import Image, ImageDraw
    x0, y0, x1, y1 = fenetre

    def f(img, u):
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for j, dt in enumerate((0.0, 1.1)):
            ph = ((u + decalage - dt) % periode) / periode
            x = x0 - 12 + (x1 - x0 + 24) * ph + 105
            y = y0 + (y1 - y0) * 0.55
            fl = 0.7 + 0.3 * math.sin(u * 11 + j)
            d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(255, 150, 60, int(60 * fl)))
            d.ellipse([x - 2, y - 5 * fl, x + 2, y + 1], fill=(255, 210, 110, 230))
            d.rectangle([x - 1, y + 1, x, y + 10], fill=(60, 40, 30, 255))
        a = np.array(lay)
        cadre = np.zeros(a.shape[:2], bool)
        cadre[y0:y1 + 1, x0 + 105:x1 + 106] = True
        a[~cadre] = 0
        lieux.pose_calque(img, Image.fromarray(a, "RGBA"))
    return f


def anim_lumiere_monte(t_debut=0.0, duree=4.0, force=0.32, couleur=(255, 214, 130)):
    """Une lumière dorée se lève lentement sur toute la scène (plus forte en haut, comme un soleil qui se lève)."""
    from PIL import Image
    cache = {}

    def f(img, u):
        k = max(0.0, min(1.0, (u - t_debut) / max(0.1, duree)))
        if k <= 0:
            return
        if img.size not in cache:
            h = img.height
            g = np.zeros((h, 1, 4), np.uint8)
            g[..., 0], g[..., 1], g[..., 2] = couleur
            g[:, 0, 3] = (255 * np.linspace(1.0, 0.25, h)).astype(np.uint8)
            cache[img.size] = Image.fromarray(g, "RGBA").resize(img.size, Image.NEAREST)
        lay = cache[img.size].copy()
        al = np.array(lay.getchannel("A"), np.float32) * (force * (k * k * (3 - 2 * k)))
        lay.putalpha(Image.fromarray(al.astype(np.uint8)))
        img.alpha_composite(lay)
    return f
