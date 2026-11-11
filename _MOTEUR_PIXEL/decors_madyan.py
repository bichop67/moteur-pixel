# DÉCORS DU FILM « MOUSSA » — Madyan et la montagne (parties 7 à 10) — 16:9, toile x = -105 … 375, y = 0 … 480.
# Plan large : on voit environ x = -87 … 357 et y = 100 … 350 ; les pieds sont à y = 330.
#   puits_madyan (+ _jour _soir)     la plaine de Madyan : le puits de pierre (cadre de bois, poulie), l'abreuvoir, le grand
#                                    acacia à droite (son ombre), montagnes au loin ; la PIERRE du puits est un objet (film.py)
#   maison_madyan (+ _jour _nuit)    la maison du vieil homme : murs de pierre, tente en poil de chèvre, enclos des moutons
#   maison_madyan_int (+ _jour)      l'intérieur, la nuit : lampe dans une niche, tapis tissés, métier à tisser, outres
#   collines_madyan (+ _ete _pluie _soir _nuit)   les collines où Moussa garde les moutons, au fil des saisons
#   montagne_nuit (+ _feu)           la nuit entre les montagnes, le rocher-abri ; _feu : un feu au loin sur le flanc
#   vallee_tuwa (+ _aube)            le pied de la montagne, la vallée ; l'arbre vert où flambe le feu (anim_arbre_feu :
#                                    option « arbre_feu », lueur douce et régulière, JAMAIS calée sur la voix)
import math

import numpy as np

import lieux
import egypte
from lieux import dk, lt, mix, R, palmier, relief
from egypte import _Px, _ciel, CIELS
from decors_film import _T, _jarre
from decors_film2 import _clip, _assombrit


# ================================================================ outils
def _montagnes(c, heure, base=228, seed=1, couches=((0.62, 178, 32), (0.44, 194, 24), (0.26, 208, 16))):
    """Chaînes de montagnes au loin (plusieurs plans, de plus en plus pâles avec la distance)."""
    T = _T(heure)
    rr = R(seed)
    roche = T((132, 100, 96))
    for k, (pale, haut, amp) in enumerate(couches):
        col = mix(roche, CIELS[heure][1], pale)
        ph = [rr.uniform(0, 6.28) for _ in range(3)]
        top = haut + amp * 0.0
        h = (top - amp * (0.55 * np.sin(c.xx / 47.0 + ph[0]) + 0.3 * np.sin(c.xx / 23.0 + ph[1])
                          + 0.15 * np.sin(c.xx / 9.0 + ph[2])))
        m = (c.yy >= h) & (c.yy <= base)
        c.vgrad(m, int(top - amp), base, lt(col, 0.05), dk(col, 0.9), steps=4)
        c.fill(m & ~np.roll(m, 1, axis=0), lt(col, 0.14))


def _sol_plaine(c, heure, y0, terre, seed=3, buissons=40):
    T = _T(heure)
    rr = R(seed)
    sol = c.mask_rect(-105, y0, 375, 480)
    c.vgrad(sol, y0, 480, lt(terre, 0.06), dk(terre, 0.68), steps=6)
    for _ in range(90):
        x, y = rr.randint(-100, 370), rr.randint(y0 + 4, 470)
        c.fill(c.mask_ell(x, y, rr.randint(1, 3), 1), lt(terre, 0.1) if rr.random() < 0.5 else dk(terre, 0.88))
    for _ in range(buissons):                                           # touffes sèches
        x, y = rr.randint(-100, 370), rr.randint(y0 + 6, 460)
        s = 2 + (y - y0) // 60
        c.fill(c.mask_ell(x, y - s // 2, s + 1, s * 0.7), T((132, 120, 70)))
        c.fill(c.mask_ell(x - 1, y - s, s * 0.6, s * 0.4), T((160, 146, 84)))
    for y0_, kk in ((420, 0.10), (440, 0.18), (460, 0.26)):
        c.tint(c.mask_rect(-105, y0_, 375, 480), (40, 24, 20), kk)


def _acacia(c, x, y, heure, larg=56, h=74, seed=1):
    """Grand acacia du désert : tronc qui se divise, couronne large et plate (en étages), ombre au sol."""
    T = _T(heure)
    tronc = T((92, 66, 46))
    c.fill(c.mask_ell(x - 6, y + 2, larg * 0.9, 7), dk(T((170, 140, 96)), 0.72))       # ombre au sol
    c.shape(c.mask_poly([(x - 3, y), (x + 3, y), (x + 2, y - h * 0.45), (x - 2, y - h * 0.45)]), tronc, dk(tronc, 0.7), band=1)
    for (dx, dy) in ((-larg * 0.45, -h * 0.82), (larg * 0.4, -h * 0.86), (-larg * 0.1, -h * 0.95), (larg * 0.1, -h * 0.7)):
        c.line(x, y - h * 0.45, x + dx * 0.8, y + dy, tronc)
        c.line(x + 1, y - h * 0.45, x + dx * 0.8 + 1, y + dy, tronc)
    feuille = T((92, 124, 70))
    rr = R(seed)
    for (cx, cy, rx, ry) in ((0, -h * 0.92, larg, 9), (-larg * 0.35, -h * 0.8, larg * 0.55, 6), (larg * 0.38, -h * 0.84, larg * 0.5, 6)):
        m = c.mask_ell(x + cx, y + cy, rx, ry)
        c.fill(m, feuille)
        c.fill(m & c.mask_ell(x + cx - 3, y + cy - 3, rx * 0.85, ry * 0.55), lt(feuille, 0.12))
        c.fill(m & ~c.mask_ell(x + cx, y + cy - 2, rx, ry), dk(feuille, 0.75))
        for _ in range(int(rx)):
            px_, py_ = x + cx + rr.uniform(-rx, rx), y + cy + rr.uniform(-ry, ry)
            if ((px_ - x - cx) / rx) ** 2 + ((py_ - y - cy) / ry) ** 2 <= 1:
                c.px(px_, py_, dk(feuille, 0.82))


def _pierres(c, m, base, seed=2, pas=7):
    """Appareil de pierres sèches (joints sombres irréguliers) dans le masque m."""
    ys, xs = np.where(m)
    if len(ys) == 0:
        return
    ox = getattr(c, "ox", 0)
    rr = R(seed)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min() - ox, xs.max() - ox
    for y in range(int(y0), int(y1) + 1, pas):
        c.fill(m & c.mask_rect(int(x0), y, int(x1), y), dk(base, 0.7))
        x = int(x0) + rr.randint(0, 6)
        while x < x1:
            w = rr.randint(6, 12)
            c.fill(m & c.mask_rect(x, y + 1, x, y + pas - 1), dk(base, 0.72))
            if rr.random() < 0.3:
                c.fill(m & c.mask_rect(x + 1, y + 1, x + w - 1, y + pas - 1), lt(base, 0.07) if rr.random() < 0.5 else dk(base, 0.92))
            x += w


# ================================================================ le puits de Madyan
def puits_madyan(heure="aube"):
    """La plaine de Madyan : montagnes au loin, le puits de pierre au centre-gauche (margelle ronde, cadre de bois et
    poulie, la corde), l'abreuvoir de pierre à sa droite, le grand acacia isolé à droite (Moussa s'y repose), poussière
    dorée. La PIERRE qui ferme le puits est un objet : PIERRE place 440 1188 (sur la bouche) / {derive PIERRE …}.
    Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 228, dict(aube=(300, 190), jour=(70, 46), soir=(-30, 190), nuit=(300, 60))[heure], seed=101)
    snap = c.a.copy()
    _montagnes(c, heure, base=232, seed=11)
    terre = T((206, 170, 116))
    _sol_plaine(c, heure, 228, terre, seed=13, buissons=36)
    loin = mix(T((190, 160, 120)), CIELS[heure][1], 0.35)                 # la ville de Madyan, au loin
    for (x0_, w_, h_) in ((-96, 10, 7), (-84, 14, 9), (-68, 9, 6), (-58, 12, 8), (-44, 10, 6)):
        c.fill(c.mask_rect(x0_, 229 - h_, x0_ + w_, 229), loin)
        c.fill(c.mask_rect(x0_, 229 - h_, x0_ + w_, 229 - h_), lt(loin, 0.1))
    for x_ in (-100, -76, -50, -30):
        palmier(c, x_, 230, h=14, lean=2, seed=200 + x_, col=mix(T((60, 110, 60)), CIELS[heure][1], 0.35),
                trunk=mix(T((120, 90, 60)), CIELS[heure][1], 0.35))
    c.fill(c.mask_poly([(-105, 342), (40, 318), (230, 318), (375, 330), (375, 340), (230, 326), (40, 326), (-105, 352)]),
           dk(terre, 0.9))                                               # piste battue par les troupeaux
    # le puits : margelle ronde de pierres, bouche sombre
    px_, py_ = 110, 300
    pierre = T((168, 150, 128))
    corps = c.mask_ell(px_, py_, 30, 8) | c.mask_rect(px_ - 30, py_, px_ + 30, py_ + 14)
    corps |= c.mask_ell(px_, py_ + 14, 30, 8)
    c.fill(corps, pierre)
    _pierres(c, corps & c.mask_rect(px_ - 30, py_, px_ + 30, py_ + 22), pierre, seed=4, pas=6)
    c.outline(corps, dk(pierre, 0.45))
    c.fill(c.mask_ell(px_, py_, 30, 8), lt(pierre, 0.08))
    c.fill(c.mask_ell(px_, py_ + 1, 22, 5), (34, 28, 30))
    c.fill(c.mask_ell(px_, py_ + 3, 20, 3), (20, 18, 24))
    bois = T((118, 84, 52))
    for x in (px_ - 24, px_ + 22):                                      # cadre de bois et poulie
        c.shape(c.mask_rect(x, 252, x + 2, py_ + 4), bois, dk(bois, 0.7), band=1)
    c.shape(c.mask_rect(px_ - 27, 248, px_ + 27, 252), bois, dk(bois, 0.7), band=1)
    c.shape(c.mask_ell(px_, 255, 4, 4), T((150, 112, 70)), dk(bois, 0.7), band=1)
    c.line(px_ + 3, 256, px_ + 3, 296, T((190, 164, 110)))
    # l'abreuvoir de pierre, avec de l'eau
    ab = c.mask_rect(158, 304, 236, 318)
    c.shape(ab, pierre, dk(pierre, 0.72), lt(pierre, 0.08), band=2)
    c.fill(c.mask_rect(162, 305, 232, 307), T((100, 150, 176)))
    c.fill(c.mask_rect(170, 305, 182, 305), T((180, 214, 230)))
    # le grand acacia (à droite) et quelques rochers
    _acacia(c, 290, 306, heure, larg=56, h=80, seed=7)
    for (rx_, ry_, w, h) in ((-80, 306, 16, 9), (262, 312, 9, 5), (-30, 300, 8, 5)):
        r_ = c.mask_ell(rx_, ry_, w, h) & c.mask_rect(rx_ - w, ry_ - h, rx_ + w, ry_ + 2)
        c.shape(r_, T((150, 128, 104)), T((104, 88, 72)), T((186, 166, 140)), band=2)
    if heure in ("aube", "soir"):                                        # poussière dorée près du sol
        for y0_, k in ((250, 0.10), (270, 0.14), (290, 0.10)):
            c.tint(c.mask_rect(-105, y0_, 375, y0_ + 20), (255, 210, 150), k)
    return relief(c, snap, sky), None


# ================================================================ la maison du vieil homme (extérieur)
def maison_madyan(heure="soir"):
    """La maison du vieil homme au bord de la plaine : murs de pierres sèches, toit plat à parapet, porte fermée d'un
    rideau rayé ; à droite une tente en poil de chèvre (rayée noir et brun) sur ses perches, des tapis dessous ; un enclos
    de pierres pour les moutons ; un palmier, des jarres. Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 228, dict(aube=(320, 190), jour=(60, 46), soir=(330, 196), nuit=(300, 60))[heure], seed=103)
    snap = c.a.copy()
    _montagnes(c, heure, base=232, seed=21)
    terre = T((200, 166, 114))
    _sol_plaine(c, heure, 228, terre, seed=23, buissons=26)
    palmier(c, -86, 300, h=86, lean=-8, seed=31, col=T((64, 120, 66)), trunk=T((126, 94, 60)))
    pierre = T((176, 156, 130))
    mm = c.mask_rect(-60, 206, 118, 306)
    c.shape(mm, pierre, dk(pierre, 0.8), lt(pierre, 0.06), band=2)
    _pierres(c, mm, pierre, seed=5, pas=7)
    c.shape(c.mask_rect(-63, 198, 121, 206), lt(pierre, 0.06), dk(pierre, 0.7), band=1)
    for x in range(-58, 118, 14):
        c.fill(c.mask_rect(x, 194, x + 7, 198), dk(pierre, 0.86))
    porte = c.mask_rect(14, 240, 46, 306)
    c.fill(porte, (40, 30, 30))
    rideau = c.mask_rect(15, 241, 45, 296)
    for j, x in enumerate(range(15, 46, 5)):
        c.fill(rideau & c.mask_rect(x, 241, x + 4, 296), T(((170, 60, 50), (226, 200, 150), (60, 80, 120))[j % 3]))
    c.shape(c.mask_rect(10, 234, 50, 240), T((110, 80, 50)), T((80, 56, 34)), band=1)
    c.fill(c.mask_rect(74, 236, 90, 248), (40, 30, 30) if heure != "nuit" else (255, 196, 110))
    c.outline(c.mask_rect(74, 236, 90, 248), dk(pierre, 0.6))
    # la tente en poil de chèvre : paroi du fond à bandes, toit rayé tendu sur des perches, franges ; tapis à l'ombre
    poil, poil2 = T((58, 44, 40)), T((110, 84, 60))
    fond = c.mask_rect(120, 228, 238, 306)
    for j, x in enumerate(range(120, 239, 6)):
        c.fill(fond & c.mask_rect(x, 228, x + 5, 306), poil if j % 2 else poil2)
    c.tint(fond, (0, 0, 0), 0.38)
    toit = c.mask_poly([(116, 212), (242, 226), (246, 238), (116, 226)])
    c.fill(toit, poil)
    for x in range(116, 246, 8):
        c.fill(toit & c.mask_rect(x, 200, x + 3, 240), poil2)
    c.outline(toit, (30, 24, 22))
    for x in range(118, 246, 3):
        c.px(x, 239 + (x * 7 % 3 == 0) + (x - 116) * 0 // 1, poil2)
    for x in (122, 182, 240):
        c.shape(c.mask_rect(x, 214 + (x - 116) * 14 // 126, x + 1, 306), T((120, 90, 56)), T((84, 62, 38)), band=1)
    for (cx, col) in ((140, (150, 60, 50)), (214, (60, 90, 130))):
        c.shape(c.mask_ell(cx, 298, 8, 4), T(col), dk(T(col), 0.72), band=1)
    tapis = c.mask_poly([(126, 300), (230, 300), (236, 310), (120, 310)])
    c.fill(tapis, T((150, 50, 50)))
    for x in range(124, 234, 10):
        c.fill(tapis & c.mask_poly([(x, 305), (x + 5, 301), (x + 10, 305), (x + 5, 309)]), T((226, 186, 90)))
    # l'enclos de pierres
    enclos = c.mask_poly([(246, 296), (372, 296), (375, 316), (244, 316)])
    c.shape(enclos & ~c.mask_rect(250, 300, 368, 312), pierre, dk(pierre, 0.72), band=1)
    _pierres(c, enclos & ~c.mask_rect(250, 300, 368, 312), pierre, seed=8, pas=4)
    c.fill(c.mask_rect(250, 300, 368, 312), dk(terre, 0.8))
    for (jx, col) in ((-40, (170, 104, 66)), (-26, (150, 92, 60)), (102, (176, 120, 76))):
        _jarre(c, jx, 312, T(col), h=8)
    if heure == "nuit":
        c.glow(82, 242, 30, (255, 170, 90), 0.4)
    return relief(c, snap, sky), None


# ================================================================ la maison du vieil homme (intérieur)
def maison_madyan_int(heure="nuit"):
    """L'intérieur de la maison du vieil homme : murs enduits clairs, tapis tissés pendus au mur, une niche avec la lampe,
    un métier à tisser, des outres de peau, un coffre, des coussins et un plateau bas avec du pain et des dattes ; à droite
    la porte au rideau relevé, la nuit dehors. Pieds y = 330."""
    c = _Px()
    nuit = heure == "nuit"
    mur = (214, 190, 156)
    c.vgrad(c.mask_rect(-105, 0, 375, 306), 100, 306, dk(mur, 0.82), mur, steps=6)
    rr = R(41)
    for _ in range(60):
        x, y = rr.randint(-100, 370), rr.randint(112, 296)
        c.fill(c.mask_ell(x, y, rr.randint(4, 12), rr.randint(2, 4)), lt(mur, 0.05) if rr.random() < 0.5 else dk(mur, 0.94))
    c.fill(c.mask_rect(-105, 0, 375, 104), (96, 74, 52))                    # plafond de poutres et de branchages
    for x in range(-105, 375, 4):
        c.fill(c.mask_rect(x, 0, x + 1, 104), (110, 86, 60))
    c.shape(c.mask_rect(-105, 104, 375, 110), (84, 60, 40), (60, 42, 28), band=1)
    c.fill(c.mask_rect(-105, 290, 375, 306), dk(mur, 0.86))
    # tapis tissés pendus au mur (motifs géométriques)
    for (x0, x1, y0, y1, cols) in ((-80, -20, 130, 214, ((150, 50, 50), (226, 186, 90), (40, 70, 110))),
                                   (150, 214, 126, 200, ((60, 90, 130), (226, 200, 150), (150, 60, 50)))):
        k = c.mask_rect(x0, y0, x1, y1)
        c.fill(k, cols[0])
        c.fill(k & ~c.mask_rect(x0 + 3, y0 + 3, x1 - 3, y1 - 3), cols[1])
        for j, y in enumerate(range(y0 + 10, y1 - 6, 14)):
            cx = (x0 + x1) // 2
            c.fill(c.mask_poly([(cx, y - 5), (cx + 12, y + 2), (cx, y + 9), (cx - 12, y + 2)]), cols[(j % 2) + 1])
        for x in range(x0 + 1, x1, 3):
            c.fill(c.mask_rect(x, y1 + 1, x, y1 + 4), cols[1])
        c.fill(c.mask_rect(x0 - 2, y0 - 3, x1 + 2, y0 - 1), (110, 80, 50))
    # niche et lampe
    c.fill(c.mask_arch(40, 70, 196, 236), dk(mur, 0.6))
    lx, ly = 55, 234
    c.shape(c.mask_ell(lx, ly - 2, 6, 2.5) | c.mask_poly([(lx + 4, ly - 3), (lx + 9, ly - 5), (lx + 9, ly - 3)]),
            (172, 112, 72), (122, 78, 52), band=1)
    # métier à tisser (gauche)
    bois = (120, 86, 54)
    for x in (-96, -40):
        c.shape(c.mask_rect(x, 230, x + 3, 306), bois, dk(bois, 0.7), band=1)
    c.shape(c.mask_rect(-98, 228, -36, 232), bois, dk(bois, 0.7), band=1)
    c.shape(c.mask_rect(-98, 288, -36, 292), bois, dk(bois, 0.7), band=1)
    for x in range(-92, -40, 2):
        c.fill(c.mask_rect(x, 232, x, 288), (226, 214, 186))
    c.fill(c.mask_rect(-92, 262, -42, 288), (150, 50, 50))
    for x in range(-92, -42, 6):
        c.fill(c.mask_poly([(x, 270), (x + 3, 266), (x + 6, 270), (x + 3, 274)]), (226, 186, 90))
    # outres de peau pendues, coffre
    for (ox_, oy_) in ((112, 150), (128, 156)):
        c.line(ox_, 110, ox_, oy_ - 10, (100, 76, 50))
        c.shape(c.mask_ell(ox_, oy_, 7, 11), (140, 104, 70), (100, 72, 46), band=1)
    c.shape(c.mask_rect(220, 276, 262, 306), (130, 92, 56), (92, 64, 38), (160, 120, 76), band=2)
    c.fill(c.mask_rect(220, 286, 262, 287), (92, 64, 38))
    # la porte : rideau relevé, la nuit dehors
    porte = c.mask_rect(290, 196, 344, 306)
    c.fill(c.mask_rect(286, 192, 348, 306), dk(mur, 0.7))
    if nuit:
        c.vgrad(porte, 196, 306, (12, 14, 36), (30, 34, 64), steps=4)
        for (sx, sy) in ((300, 206), (322, 214), (336, 204), (310, 226), (330, 236)):
            c.px(sx, sy, (220, 220, 250))
        c.fill(c.mask_rect(290, 276, 344, 306), (24, 22, 30))
    else:
        c.vgrad(porte, 196, 306, (130, 180, 226), (220, 200, 160), steps=4)
        c.fill(c.mask_rect(290, 270, 344, 306), (206, 170, 116))
    c.fill(c.mask_poly([(290, 196), (344, 196), (344, 214), (330, 230), (290, 208)]), (150, 60, 50))      # rideau relevé
    for x in range(292, 344, 6):
        c.fill(c.mask_poly([(x, 196), (x + 3, 196), (x + 3, 214), (x, 212)]) & c.mask_poly([(290, 196), (344, 196), (344, 214), (330, 230), (290, 208)]),
               (226, 200, 150))
    # sol : tapis, coussins, plateau bas (pain et dattes)
    sol = c.mask_rect(-105, 306, 375, 480)
    c.vgrad(sol, 306, 480, (170, 140, 104), (90, 70, 52), steps=6)
    tapis = c.mask_poly([(-20, 316), (270, 316), (290, 370), (-40, 370)])
    c.fill(tapis, (120, 40, 44))
    c.fill(tapis & ~c.mask_poly([(-16, 319), (266, 319), (285, 367), (-35, 367)]), (226, 186, 90))
    for x in range(10, 260, 28):
        c.fill(c.mask_poly([(x, 334), (x + 10, 342), (x, 350), (x - 10, 342)]), (60, 90, 130))
    for (cx, col) in ((-60, (60, 90, 130)), (-44, (150, 60, 50)), (300, (226, 186, 90)), (318, (60, 120, 90))):
        c.shape(c.mask_ell(cx, 314, 9, 5), col, dk(col, 0.72), lt(col, 0.15), band=1)
    c.shape(c.mask_ell(140, 316, 16, 4), (190, 150, 70), (140, 104, 50), band=1)
    for (fx, col) in ((132, (200, 160, 100)), (140, (200, 160, 100)), (148, (110, 50, 30)), (152, (110, 50, 30))):
        c.fill(c.mask_ell(fx, 313, 2.5, 1.5), col)
    if nuit:
        _assombrit(c, ~porte, (0.40, 0.38, 0.50), (6, 4, 12))
        fl = (lx + 9, ly - 8)
        c.fill(c.mask_ell(fl[0], fl[1], 1.6, 3), (255, 214, 130))
        c.px(fl[0], fl[1] - 3, (255, 240, 200))
        c.glow(fl[0], fl[1], 140, (255, 166, 86), 0.42)
        c.glow(fl[0], fl[1], 50, (255, 210, 140), 0.32)
    return c, None


# ================================================================ les collines de Madyan, au fil des saisons
SAISONS = dict(printemps=((112, 156, 74), (150, 190, 96)), ete=((196, 170, 98), (220, 196, 120)),
               pluie=((92, 120, 80), (120, 146, 96)))


def collines_madyan(heure="jour", saison="printemps"):
    """Les collines où Moussa garde les moutons : collines en plans successifs (vertes au printemps, dorées l'été,
    grises sous la pluie), arbres isolés, rochers, fleurs au printemps, un sentier ; montagnes au loin. Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 226, dict(aube=(320, 190), jour=(80, 44), soir=(-30, 190), nuit=(300, 60))[heure], seed=107)
    if saison == "pluie":
        c.tint(sky, (120, 124, 136), 0.55)
    snap = c.a.copy()
    _montagnes(c, heure, base=236, seed=31, couches=((0.6, 180, 30), (0.4, 196, 22)))   # 236 : sous le creux de la 1re
    herbe, clair = (T(SAISONS[saison][0]), T(SAISONS[saison][1]))                      # colline (230), sinon trait noir
    rr = R(51)
    for (ytop, amp, per, ph, k) in ((220, 10, 64, 0.4, 0.42), (244, 12, 52, 2.1, 0.24), (272, 14, 76, 4.0, 0.10)):
        m = c.yy >= ytop + amp * np.sin(c.xx / per + ph)
        col = mix(herbe, CIELS[heure][1], k)
        c.vgrad(m, ytop - amp, 480, lt(col, 0.06), dk(col, 0.82), steps=5)
        c.fill(m & ~np.roll(m, 1, axis=0), lt(col, 0.16))
    for (tx, ty, s) in ((-60, 252, 0.5), (40, 236, 0.35), (200, 246, 0.45), (300, 258, 0.6)):   # arbres au loin
        tr = c.mask_rect(tx - 1, ty - int(18 * s), tx + 1, ty)
        c.fill(tr, T((90, 70, 50)))
        c.fill(c.mask_ell(tx, ty - 22 * s, 14 * s + 2, 9 * s + 2), mix(dk(herbe, 0.7), CIELS[heure][1], 0.2))
    c.fill(c.mask_poly([(-105, 350), (60, 322), (180, 318), (375, 326), (375, 334), (180, 326), (60, 330), (-105, 360)]),
           dk(herbe, 0.86))                                                # le sentier
    for _ in range(140):                                                    # brins d'herbe, fleurs
        x, y = rr.randint(-100, 370), rr.randint(282, 470)
        c.px(x, y, lt(herbe, 0.18))
        c.px(x + 1, y - 1, dk(herbe, 0.82))
        if saison == "printemps" and rr.random() < 0.25:
            c.px(x + 2, y, rr.choice(((240, 220, 110), (236, 140, 160), (250, 250, 240))))
    for (rx_, ry_, w, h) in ((-84, 312, 14, 8), (150, 306, 9, 5), (338, 316, 12, 7)):
        r_ = c.mask_ell(rx_, ry_, w, h) & c.mask_rect(rx_ - w, ry_ - h, rx_ + w, ry_ + 2)
        c.shape(r_, T((150, 140, 120)), T((104, 98, 86)), T((186, 178, 160)), band=2)
    if saison == "pluie":
        c.tint(c.mask_rect(-105, 0, 375, 480), (90, 96, 110), 0.25)
    for y0_, kk in ((420, 0.10), (440, 0.18), (460, 0.26)):
        c.tint(c.mask_rect(-105, y0_, 375, 480), (30, 24, 20), kk)
    return relief(c, snap, sky), None


# ================================================================ la nuit entre les montagnes
def montagne_nuit(feu=False):
    """Une nuit noire entre les montagnes, sous la pluie : nuages bas, trois plans de crêtes déchiquetées (de plus en plus
    sombres vers l'avant), brume douce entre les plans, un gros rocher en surplomb à gauche (on s'y abrite), sol de pierres
    mouillées ; feu=True : très loin, sur le flanc de la montagne, une petite lueur de feu. La pluie : option « pluie ».
    Pieds y = 330."""
    c = _Px()
    c.vgrad(c.mask_rect(-105, 0, 375, 330), 0, 330, (10, 12, 22), (34, 36, 54), steps=8)
    for (cx, cy, rx, ry) in ((-40, 70, 130, 20), (150, 52, 150, 24), (300, 90, 110, 18), (60, 118, 170, 14)):
        c.fill(c.mask_ell(cx, cy, rx, ry), (24, 26, 38))
        c.fill(c.mask_ell(cx - 12, cy - 5, rx * 0.8, ry * 0.5), (32, 34, 48))
    plans = ((206, 58, (52, 52, 72), 3), (238, 66, (36, 36, 52), 5), (268, 46, (24, 24, 36), 7))
    for (base_y, amp, col, sd) in plans:
        r2 = R(sd)
        y = base_y - amp * 0.5
        brut = []
        for x in range(-105, 384, 6):
            y = min(base_y - 8, max(base_y - amp, y + r2.uniform(-7, 7)))
            brut.append(y)
        lisse = [sum(brut[max(0, i - 2):i + 3]) / len(brut[max(0, i - 2):i + 3]) for i in range(len(brut))]
        pts = [(-105 + 6 * i, yv) for i, yv in enumerate(lisse)]
        m = c.mask_poly(pts + [(380, 330), (-105, 330)])
        c.vgrad(m, base_y - amp, 330, lt(col, 0.14), dk(col, 0.72), steps=5)
        c.fill(m & ~np.roll(m, 1, axis=0), lt(col, 0.32))
        for _ in range(34):
            x = r2.randint(-100, 370)
            yy = r2.randint(base_y - amp + 8, 322)
            if m[yy, x + 105]:
                c.line(x, yy, x + r2.randint(-4, 4), yy + r2.randint(6, 14), lt(col, 0.16))
        if feu and sd == 3:
            fx, fy = 262, None
            col_ = m[:, fx + 105]
            haut_ = int(np.argmax(col_)) if col_.any() else 180
            fy = haut_ + 14
            c.glow(fx, fy, 44, (255, 150, 60), 0.38)
            c.fill(c.mask_ell(fx, fy, 2, 3), (255, 190, 90))
            c.px(fx, fy - 2, (255, 240, 190))

        def brume(yc, h, k):
            for dy in range(-h, h + 1):
                c.tint(c.mask_rect(-105, yc + dy, 375, yc + dy), (110, 118, 140), k * (1 - abs(dy) / (h + 1)))
        if sd == 5:
            brume(base_y - 6, 9, 0.14)
    rr = R(61)
    sol = c.mask_rect(-105, 300, 375, 480)
    c.vgrad(sol, 300, 480, (42, 40, 52), (16, 16, 24), steps=6)
    for _ in range(70):
        x, y = rr.randint(-100, 370), rr.randint(304, 470)
        c.fill(c.mask_ell(x, y, rr.randint(2, 5), rr.randint(1, 2)), (58, 56, 70))
    for _ in range(10):                                                      # flaques
        x, y = rr.randint(-80, 360), rr.randint(318, 420)
        c.fill(c.mask_ell(x, y, rr.randint(6, 12), 1.5), (60, 66, 92))
    abri = c.mask_poly([(-105, 196), (-30, 190), (30, 204), (70, 226), (40, 236), (-6, 234), (-6, 306), (-105, 306)])
    c.vgrad(abri, 190, 306, (64, 60, 76), (30, 28, 40), steps=5)
    c.fill(abri & ~np.roll(abri, 1, axis=0), (96, 92, 110))
    c.fill(abri & ~np.roll(abri, -2, axis=1) & c.mask_rect(-105, 190, 80, 236), (86, 82, 100))
    c.fill(c.mask_poly([(-6, 234), (40, 236), (-6, 252)]), (14, 12, 20))
    for (x0_, y0_) in ((-80, 220), (-50, 250), (-90, 270), (-30, 214)):
        c.line(x0_, y0_, x0_ + 14, y0_ + 6, (48, 44, 58))
    return c, None


# ================================================================ la vallée de Touwa : l'arbre où flambe le feu
ARBRE_FEU = (250, 306)                                                   # pied de l'arbre (coordonnées du dessin)


def vallee_tuwa(heure="nuit"):
    """Au pied de la montagne, au bord de la vallée : la montagne immense (granit, ravines), le sol de sable et de pierres,
    et l'arbre vert (couronne ronde et dense) où flambe un feu sans qu'il brûle ; les flammes sont l'animation
    « arbre_feu » (lueur douce et régulière). _aube : l'aube se lève derrière la montagne. Pieds y = 330."""
    c = _Px()
    nuit = heure == "nuit"
    if nuit:
        c.vgrad(c.mask_rect(-105, 0, 375, 330), 0, 330, (8, 10, 26), (30, 32, 60), steps=8)
        rr = R(71)
        for _ in range(120):
            c.px(rr.randint(-105, 374), rr.randint(0, 200), (200, 204, 240) if rr.random() < 0.3 else (120, 126, 180))
    else:
        _ciel(c, "aube", 260, (230, 150), seed=73)
    rr = R(72)
    roc = (96, 72, 70) if nuit else (150, 104, 96)
    loin = mix(roc, (40, 44, 80) if nuit else (230, 170, 150), 0.45)       # crête lointaine, plus pâle
    c.fill(c.mask_poly([(-105, 230), (-60, 196), (-10, 176), (60, 150), (200, 150), (260, 132), (330, 170), (375, 160),
                        (375, 300), (-105, 300)]), loin)
    pts, y_ = [], 120
    r3 = R(9)
    for x in range(-105, 384, 6):                                          # la montagne : crête déchiquetée
        cible = 210 - 140 * math.exp(-((x - 100) / 120.0) ** 2)
        y_ = max(cible - 14, min(cible + 14, y_ + r3.uniform(-9, 9)))
        pts.append((x, y_))
    mont = c.mask_poly(pts + [(380, 300), (-105, 300)])
    c.vgrad(mont, 70, 300, lt(roc, 0.1), dk(roc, 0.55), steps=6)
    for _ in range(16):                                                     # pans de roche, irréguliers
        x0_, y0_ = r3.randint(-100, 340), r3.randint(90, 250)
        w_, h_ = r3.randint(14, 40), r3.randint(20, 60)
        pan = mont & c.mask_poly([(x0_, y0_), (x0_ + w_, y0_ + h_ * 0.3), (x0_ + w_ * 0.8, y0_ + h_), (x0_ - w_ * 0.2, y0_ + h_ * 0.7)])
        c.tint(pan, dk(roc, 0.55) if r3.random() < 0.6 else lt(roc, 0.2), 0.22)
    c.fill(mont & ~np.roll(mont, 1, axis=0), lt(roc, 0.3))
    for _ in range(60):                                                    # ravines
        x = rr.randint(-90, 360)
        y = rr.randint(90, 290)
        if mont[y, x + 105]:
            for j in range(rr.randint(6, 18)):
                c.px(x + rr.randint(-1, 1), y + j, dk(roc, 0.7))
    for _ in range(40):
        x = rr.randint(-90, 360)
        y = rr.randint(90, 290)
        if mont[y, x + 105]:
            c.line(x, y, x + rr.randint(4, 10), y - rr.randint(2, 6), lt(roc, 0.12))
    sol_col = (70, 60, 60) if nuit else (190, 150, 110)
    sol = c.mask_rect(-105, 296, 375, 480)
    c.vgrad(sol, 296, 480, sol_col, dk(sol_col, 0.6), steps=6)
    for _ in range(80):
        x, y = rr.randint(-100, 370), rr.randint(300, 470)
        c.fill(c.mask_ell(x, y, rr.randint(2, 4), 1), lt(sol_col, 0.1))
    for (rx_, ry_, w, h) in ((-70, 304, 18, 10), (60, 300, 10, 6), (330, 306, 14, 8)):
        r_ = c.mask_ell(rx_, ry_, w, h) & c.mask_rect(rx_ - w, ry_ - h, rx_ + w, ry_ + 2)
        c.shape(r_, lt(roc, 0.1), dk(roc, 0.7), lt(roc, 0.25), band=2)
    # l'arbre vert
    ax, ay = ARBRE_FEU
    tronc = (70, 50, 40) if nuit else (100, 72, 52)
    c.shape(c.mask_poly([(ax - 3, ay), (ax + 3, ay), (ax + 2, ay - 22), (ax - 2, ay - 22)]), tronc, dk(tronc, 0.7), band=1)
    for (dx, dy) in ((-14, -34), (12, -36), (0, -40)):
        c.line(ax, ay - 20, ax + dx, ay + dy, tronc)
    vert = (60, 130, 70)
    for (cx, cy, rx, ry) in ((0, -46, 26, 18), (-16, -38, 14, 11), (16, -40, 14, 11), (0, -60, 16, 10)):
        m = c.mask_ell(ax + cx, ay + cy, rx, ry)
        c.fill(m, vert)
        c.fill(m & c.mask_ell(ax + cx - 3, ay + cy - 3, rx * 0.8, ry * 0.6), lt(vert, 0.15))
        c.fill(m & ~c.mask_ell(ax + cx, ay + cy - 2, rx, ry), dk(vert, 0.72))
    for _ in range(80):
        px_, py_ = ax + rr.uniform(-26, 26), ay - 46 + rr.uniform(-18, 18)
        if ((px_ - ax) / 26) ** 2 + ((py_ - ay + 46) / 18) ** 2 <= 1:
            c.px(px_, py_, dk(vert, 0.8) if rr.random() < 0.5 else lt(vert, 0.2))
    if nuit:                                                                 # la lueur de l'arbre éclaire la vallée
        c.glow(ax, ay - 46, 160, (255, 170, 90), 0.30)
        c.glow(ax, ay - 46, 60, (255, 210, 140), 0.25)
    return c, None


def anim_arbre_feu(force=1.0, x=ARBRE_FEU[0], y=ARBRE_FEU[1]):
    """Le feu qui flambe DANS l'arbre vert sans le brûler : de vraies flammes (gouttes qui s'étirent vers le haut, cœur
    jaune) qui dansent à un rythme régulier, toujours le même (jamais calé sur la voix) ; les feuilles restent vertes."""
    from PIL import Image, ImageDraw
    flammes = [(-16, -40, 0.0, 1.0), (-6, -50, 1.3, 1.2), (6, -44, 2.1, 1.1), (16, -36, 3.0, 0.9), (0, -34, 4.2, 1.0),
               (-10, -30, 5.1, 0.8), (4, -58, 0.7, 1.0), (-14, -54, 2.6, 0.8), (14, -52, 3.7, 0.9), (-2, -64, 1.9, 0.8),
               (20, -44, 4.8, 0.7), (-22, -46, 5.6, 0.7)]

    def f(img, u):
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for (dx, dy, ph, t_) in flammes:
            fl = 0.82 + 0.18 * math.sin(u * 4.0 + ph)
            X, Y = x + dx + 105, y + dy
            h = 11 * fl * force * t_
            sw = 0.6 * math.sin(u * 2.6 + ph * 1.7)
            d.polygon([(X - 2.5, Y), (X + 2.5, Y), (X + 1.4 + sw, Y - h * 0.55), (X + sw * 1.5, Y - h),
                       (X - 1.4 + sw, Y - h * 0.55)], fill=(255, 104, 36, 175))
            d.polygon([(X - 1.4, Y), (X + 1.4, Y), (X + 0.7 + sw, Y - h * 0.45), (X + sw, Y - h * 0.72),
                       (X - 0.7 + sw, Y - h * 0.45)], fill=(255, 196, 80, 235))
            d.rectangle([X - 0.5, Y - h * 0.32, X + 0.5, Y], fill=(255, 246, 210, 245))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ souvenirs : petites images sépia au-dessus d'un perso
_SOUV = {}


def _vignette(nom, w=120, h=62):
    """Petite image sépia encadrée d'un décor (ce qu'on voit dans le plan large), comme un souvenir."""
    if nom not in _SOUV:
        from PIL import Image
        bg, _fg = lieux.decor_large(nom)
        _h, _haut = egypte.SOL_HAUT.get(nom if nom in egypte.SOL_HAUT else nom.rsplit("_", 1)[0], (330, 110))
        a = bg.a[_haut:_haut + 250, :, :]
        im = Image.fromarray(a).resize((w, h), Image.BOX)
        g = np.array(im).astype(np.float32) @ np.array([0.30, 0.59, 0.11], np.float32)
        sep = np.clip(np.stack([g * 1.06 + 20, g * 0.92 + 10, g * 0.72 + 2], axis=-1), 0, 255).astype(np.uint8)
        cadre = Image.new("RGBA", (w + 4, h + 4), (238, 224, 186, 255))
        cadre.paste(Image.fromarray(sep).convert("RGBA"), (2, 2))
        _SOUV[nom] = cadre
    return _SOUV[nom]


def anim_souvenir(nom, t0, duree=2.8, cx=135, cy=200):
    """Le souvenir d'un lieu (décor `nom`) apparaît en fondu à (cx, cy) (coordonnées du dessin), reste, puis s'efface."""
    from PIL import Image

    def f(img, u):
        if not (t0 <= u <= t0 + duree):
            return
        a = max(0.0, min(1.0, (u - t0) / 0.5, (t0 + duree - u) / 0.6))
        v = _vignette(nom).copy()
        v.putalpha(int(235 * a))
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        lay.alpha_composite(v, (int(cx + 105 - v.width / 2), int(cy - v.height / 2)))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ le bâton qui devient serpent (20:19-21)
def anim_serpent(cles, y_sol=310, x_depart=165, x_buisson=322, x_rocher=24, x_retour=176):
    """Le serpent immense : `cles` = [(u, quoi)] remplie par {serpent quoi} — depart (il apparaît où était le bâton),
    avale (sa tête atteint le buisson, qui disparaît), engloutit (le rocher), revient (près de Moussa), fin (il redevient
    bâton : il disparaît). Il ondule et file entre ces points ; buisson et rocher sont dessinés ici."""
    from PIL import Image, ImageDraw
    pos = dict(depart=x_depart, avale=x_buisson, engloutit=x_rocher, revient=x_retour)

    def tete(u):
        ks = sorted(cles)
        if not ks or u < ks[0][0]:
            return None
        fin = next((c_[0] for c_ in ks if c_[1] == "fin"), None)
        if fin is not None and u >= fin + 0.5:
            return None
        pts = [(c_[0], c_[2] if len(c_) > 2 and c_[2] is not None else pos[c_[1]]) for c_ in ks if c_[1] in pos]
        x, d = pts[0][1], 1
        for (t0, x0), (t1, x1) in zip(pts, pts[1:]):
            d = 1 if x1 >= x0 else -1
            if u >= t1:
                x = x1
            else:
                e = max(0.0, (u - t0) / max(1e-3, t1 - t0))
                x = x0 + (x1 - x0) * e * e * (3 - 2 * e)
                break
        a = min(1.0, (u - ks[0][0]) / 0.4)
        if fin is not None and u > fin:
            a *= max(0.0, 1 - (u - fin) / 0.5)
        return x, d, a

    def bouffee(d_, x, y, u, t):                                     # petit nuage de poussière qui s'efface
        k = (u - t) / 0.7
        if 0 <= k < 1:
            for j, (dx, dy) in enumerate(((-4, -2), (3, -3), (0, -6), (-6, -5), (6, -1))):
                r = 2 + 3 * k
                d_.ellipse([x + dx * (1 + k) - r, y + dy * (1 + k) - r, x + dx * (1 + k) + r, y + dy * (1 + k) + r],
                           fill=(190, 170, 140, int(150 * (1 - k))))

    def f(img, u):
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d_ = ImageDraw.Draw(lay)
        t_av = next((c_[0] for c_ in cles if c_[1] == "avale"), None)
        t_en = next((c_[0] for c_ in cles if c_[1] == "engloutit"), None)
        bx, rx = x_buisson + 105, x_rocher + 105
        if t_av is None and t_en is None:                              # (au palais : ni buisson ni rocher)
            pass
        elif t_av is None or u < t_av:                                # le buisson
            d_.ellipse([bx - 9, y_sol - 12, bx + 9, y_sol], fill=(70, 110, 60, 255))
            d_.ellipse([bx - 6, y_sol - 14, bx + 5, y_sol - 5], fill=(92, 136, 72, 255))
            d_.line([(bx, y_sol), (bx, y_sol - 5)], fill=(90, 66, 44, 255))
        else:
            bouffee(d_, bx, y_sol - 4, u, t_av)
        if t_av is None and t_en is None:
            pass
        elif t_en is None or u < t_en:                                # le rocher
            d_.ellipse([rx - 10, y_sol - 11, rx + 10, y_sol + 1], fill=(118, 98, 92, 255))
            d_.ellipse([rx - 7, y_sol - 10, rx + 4, y_sol - 4], fill=(150, 128, 118, 255))
        else:
            bouffee(d_, rx, y_sol - 4, u, t_en)
        h = tete(u)
        if h is not None:
            hx, dirx, a = h
            al = int(255 * a)
            n = 40
            for i in range(n, -1, -1):
                s_ = i * 1.8
                px_ = hx - dirx * s_ + 105
                py_ = y_sol - 3 + 2.6 * math.sin(s_ / 6.0 - u * 9.0) * min(1.0, i / 4)
                r = 4.0 * (1 - 0.6 * i / n)
                d_.ellipse([px_ - r - 1, py_ - r - 1, px_ + r + 1, py_ + r + 1], fill=(30, 40, 24, al))
                d_.ellipse([px_ - r, py_ - r, px_ + r, py_ + r], fill=(118, 150, 64, al))
                if i % 3 == 0:
                    d_.ellipse([px_ - r * 0.6, py_ - r, px_ + r * 0.6, py_ - r * 0.2], fill=(70, 96, 40, al))
                if i % 4 == 2:
                    d_.point((px_, py_ + r * 0.5), fill=(214, 200, 120, al))
            X = hx + 105
            d_.ellipse([X - 6, y_sol - 9, X + 6, y_sol], fill=(30, 40, 24, al))
            d_.ellipse([X - 5, y_sol - 8, X + 5, y_sol - 1], fill=(128, 160, 70, al))
            d_.point((X + dirx * 2, y_sol - 6), fill=(250, 214, 80, al))
            if int(u * 6) % 2 == 0:
                d_.line([(X + dirx * 5, y_sol - 4), (X + dirx * 8, y_sol - 4)], fill=(210, 50, 50, al))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ registre
_DEC = dict(puits_madyan=puits_madyan, puits_madyan_jour=lambda: puits_madyan("jour"),
            puits_madyan_soir=lambda: puits_madyan("soir"),
            maison_madyan=maison_madyan, maison_madyan_jour=lambda: maison_madyan("jour"),
            maison_madyan_nuit=lambda: maison_madyan("nuit"),
            maison_madyan_int=maison_madyan_int, maison_madyan_int_jour=lambda: maison_madyan_int("jour"),
            collines_madyan=collines_madyan, collines_madyan_ete=lambda: collines_madyan("jour", "ete"),
            collines_madyan_pluie=lambda: collines_madyan("jour", "pluie"),
            collines_madyan_soir=lambda: collines_madyan("soir", "ete"),
            collines_madyan_nuit=lambda: collines_madyan("nuit", "printemps"),
            montagne_nuit=montagne_nuit, montagne_nuit_feu=lambda: montagne_nuit(feu=True),
            vallee_tuwa=vallee_tuwa, vallee_tuwa_aube=lambda: vallee_tuwa("aube"))
egypte.enregistre(_DEC, sol_haut=dict(puits_madyan=(330, 108), maison_madyan=(330, 104), maison_madyan_int=(330, 100),
                                      collines_madyan=(330, 110), montagne_nuit=(330, 100), vallee_tuwa=(330, 96)))
lieux.LUMIERES["puits_madyan"] = (lieux.JOUR, [])
lieux.LUMIERES["maison_madyan"] = (lieux.SOIR, [])
lieux.LUMIERES["maison_madyan_int"] = (lieux.NUIT, [(256, 904, 520, (255, 170, 90), 0.85)])
lieux.LUMIERES["maison_madyan_int_jour"] = (lieux.JOUR, [])
lieux.LUMIERES["collines_madyan"] = (lieux.JOUR, [])
lieux.LUMIERES["collines_madyan_pluie"] = (lieux.SOIR, [])
lieux.LUMIERES["montagne_nuit"] = (lieux.NUIT, [])
lieux.LUMIERES["montagne_nuit_feu"] = (lieux.NUIT, [])
lieux.LUMIERES["vallee_tuwa"] = (lieux.NUIT, [(1000, 1040, 640, (255, 170, 90), 0.75)])
lieux.LUMIERES["vallee_tuwa_aube"] = (lieux.SOIR, [])
