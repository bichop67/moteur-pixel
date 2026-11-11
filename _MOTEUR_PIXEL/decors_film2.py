# DÉCORS DU FILM « MOUSSA » — parties 3 à 6 (suite de decors_film.py) — 16:9, toile x = -105 … 375, y = 0 … 480.
# Plan large : on voit environ x = -87 … 357 et y = 100 … 350 ; les pieds sont à y = 330 (sauf mention).
#   maison_nil (+ _jour _soir _aube)   la pièce de la maison au bord du Nil : banc, lampe, niche, fenêtre et porte sur le fleuve
#   rive_maison (+ _jour _soir)       la rive derrière la maison : porte, piquet, fleuve, roseaux ; rive_maison_corde : la
#                                     corde va du piquet au coffre (poser COFFRE place 600 1284)
# OBJETS POSÉS (coffre, berceau, plateau) : les mettre vers y = 1290 (un peu en retrait), sinon les sous-titres les cachent.
#   ruelle_nuit (+ _eteinte)          la ruelle devant la maison, la nuit : lueur sous la porte ; {devient ruelle_nuit_eteinte}
#   ruelle (+ _aube _soir)            la même ruelle de jour : linge qui sèche, escalier extérieur
#   couloir_palais (+ _nuit)          couloir à colonnes du palais, plafond étoilé, rais de soleil
#   chambre_asiya (+ _nuit)           chambre d'Asiya : loggia sur le jardin, lit de repos, lampes ; option « voiles » (ils ondulent)
#   marche_egypte                     le marché
#   avenue_palais                     l'allée du palais (option « petales » : pétales qui tombent)
#   ville_midi / ville_matin          Memphis à la sieste / au matin
#   desert (+ _nuit _soir _aube)      le désert entre l'Égypte et Madyan
#   porte_ville (+ _nuit)             la porte de la ville au crépuscule ; le désert devant
#   palais_ciel                       le ciel étoilé au-dessus du palais endormi (orbes placées haut)
#   carte_madyan                      la carte Égypte → Sinaï → Madyan ; option « chemin 0.5 14 » (le pointillé et les 8 nuits)
import math

import numpy as np

import lieux
import egypte
from lieux import dk, lt, mix, R, palmier, relief
from egypte import _Px, _ciel, CIELS, _papyrus, _roseaux, _brasero, _colonne_lotus
from decors_film import _T, _briques, _porte, _fenetre, _jarre, BRIQUE


# ================================================================ outils
def _clip(c, m, dessin):
    """dessin(c) n'est gardé que dans le masque m (ce qu'on voit par une fenêtre, une porte…)."""
    a0, al0 = c.a.copy(), c.al.copy()
    dessin(c)
    c.a[~m] = a0[~m]
    c.al[~m] = al0[~m]


def _assombrit(c, m, mul=(0.36, 0.38, 0.54), add=(4, 4, 14)):
    a = c.a[m].astype(np.float32) * np.array(mul, np.float32) + np.array(add, np.float32)
    c.a[m] = np.clip(a, 0, 255).astype(np.uint8)


def _trait(c, pts, larg, col):
    """Ligne brisée épaisse (fleuve, chemin) en coordonnées du dessin."""
    from PIL import Image, ImageDraw
    im = Image.new("L", (c.a.shape[1], c.a.shape[0]), 0)
    ox = getattr(c, "ox", 0)
    ImageDraw.Draw(im).line([(x + ox, y) for x, y in pts], fill=255, width=larg, joint="curve")
    m = np.array(im) > 0
    c.fill(m, col)
    return m


EAU = dict(aube=((168, 150, 176), (100, 100, 140)), jour=((122, 178, 208), (62, 118, 158)),
           soir=((214, 150, 110), (120, 78, 90)), nuit=((34, 44, 86), (14, 18, 42)))
RIVE = dict(aube=(96, 86, 96), jour=(118, 150, 84), soir=(84, 58, 60), nuit=(22, 24, 40))
PALME = dict(aube=((58, 56, 70), (70, 60, 64)), jour=((64, 124, 66), (128, 96, 60)), soir=((48, 34, 40), (56, 38, 40)),
             nuit=((16, 18, 32), (18, 18, 30)))


def _vue_fleuve(c, m, x0, y0, x1, y1, heure, hz=None, seed=5):
    """Le Nil vu par une ouverture (masque m) : ciel et astre, rive d'en face et ses palmiers, eau et reflets."""
    hz = hz if hz is not None else y0 + (y1 - y0) // 2

    def d(c):
        top, bot = CIELS[heure]
        c.vgrad(c.mask_rect(x0, y0, x1, hz), y0, hz, top, bot, steps=5)
        rnd = R(seed)
        if heure == "nuit":
            for _ in range(max(6, (x1 - x0) * (hz - y0) // 60)):
                c.px(rnd.randint(x0, x1), rnd.randint(y0, hz - 5), (226, 226, 252) if rnd.random() < 0.4 else (150, 156, 210))
        ax = x0 + (x1 - x0) * (0.72 if heure in ("nuit", "aube") else 0.28)
        ay = y0 + (hz - y0) * (0.32 if heure == "nuit" else 0.62)
        if heure == "nuit":
            c.fill(c.mask_ell(ax, ay, 5, 5) & ~c.mask_ell(ax + 3, ay - 2, 4.5, 4.5), (248, 240, 212))
            c.glow(ax, ay, 24, (190, 196, 255), 0.2, m=m)
        elif heure in ("aube", "soir"):
            col = (255, 206, 150) if heure == "aube" else (255, 180, 110)
            c.glow(ax, ay, 34, col, 0.45, m=m)
            c.fill(c.mask_ell(ax, ay, 5, 5), lt(col, 0.3))
        c.fill(c.mask_rect(x0, hz - 3, x1, hz), RIVE[heure])
        fr, tr = PALME[heure]
        for k, px_ in enumerate(range(x0 + 5, x1, 16)):
            palmier(c, px_ + (k * 7) % 5, hz - 2, h=11 + (k * 5) % 7, lean=(k % 3 - 1) * 3, seed=70 + k + seed, col=fr, trunk=tr)
        eh, eb = EAU[heure]
        c.vgrad(c.mask_rect(x0, hz + 1, x1, y1), hz + 1, y1, eh, eb, steps=4)
        for _ in range(max(4, (x1 - x0) * (y1 - hz) // 50)):
            x, y = rnd.randint(x0, x1), rnd.randint(hz + 2, y1)
            c.fill(c.mask_rect(x, y, x + rnd.randint(1, 5), y), lt(eh, 0.25))
        if heure != "jour":                                        # reflet de l'astre, en tirets
            col = (230, 230, 250) if heure == "nuit" else (255, 214, 160)
            for y in range(hz + 2, y1, 3):
                w_ = 1 + (y - hz) // 6
                c.fill(c.mask_rect(int(ax) - w_, y, int(ax) + w_, y), col)
    _clip(c, m, d)


# ================================================================ la maison au bord du Nil (intérieur)
def maison_nil(heure="nuit"):
    """La pièce de la maison de la mère de Moussa : murs de terre enduits, plafond de roseaux, niche à étagères, oignons
    suspendus, banc de terre avec natte et coussins, la lampe à huile posée sur le banc ; au centre la fenêtre sur le
    fleuve (volets ouverts), à droite la porte qui donne sur la rive (eau, roseaux), un filet de pêche. Pieds y = 330."""
    c = _Px()
    nuit = heure == "nuit"
    mur = (200, 164, 120)
    c.vgrad(c.mask_rect(-105, 0, 375, 306), 100, 306, dk(mur, 0.80), mur, steps=6)
    rr = R(14)
    for _ in range(70):                                            # enduit irrégulier
        x, y = rr.randint(-100, 370), rr.randint(112, 296)
        c.fill(c.mask_ell(x, y, rr.randint(4, 14), rr.randint(2, 5)), lt(mur, 0.05) if rr.random() < 0.5 else dk(mur, 0.94))
    for _ in range(12):                                            # fissures
        x, y = rr.randint(-100, 370), rr.randint(120, 288)
        for j in range(rr.randint(3, 7)):
            c.px(x + j, y + (j * j) // 5, dk(mur, 0.8))
    c.fill(c.mask_rect(-105, 293, 375, 306), dk(mur, 0.86))       # bas du mur usé
    c.fill(c.mask_rect(-105, 0, 375, 101), (112, 86, 58))           # plafond de roseaux sur poutres de palmier
    for x in range(-105, 375, 3):
        c.fill(c.mask_rect(x, 0, x, 101), (126, 98, 64))
    c.shape(c.mask_rect(-105, 101, 375, 108), (98, 68, 42), (72, 50, 30), band=1)
    for x in range(-100, 375, 44):
        c.shape(c.mask_rect(x, 99, x + 7, 112), (90, 62, 38), (66, 44, 26), band=1)
    # niche à étagères (gauche)
    c.fill(c.mask_rect(-97, 145, -37, 241), dk(mur, 0.74))
    c.fill(c.mask_rect(-94, 148, -40, 238), dk(mur, 0.6))
    for y in (178, 208):
        c.shape(c.mask_rect(-94, y, -40, y + 2), (122, 88, 56), (90, 64, 40), band=1)
    _jarre(c, -84, 178, (172, 106, 68), h=7)
    _jarre(c, -72, 178, (152, 94, 62), h=6)
    c.shape(c.mask_ell(-54, 175, 6, 2.5), (206, 176, 126), (156, 126, 86), band=1)
    c.shape(c.mask_rect(-88, 200, -66, 208), (222, 212, 192), (172, 162, 142), band=1)
    c.shape(c.mask_rect(-86, 194, -70, 200), (156, 72, 60), (112, 52, 42), band=1)
    _jarre(c, -50, 208, (178, 122, 78), h=7)
    for k in range(3):
        c.shape(c.mask_ell(-82 + k * 9, 234, 4, 2.5), (192, 152, 96), (150, 112, 70), band=1)
    # oignons et herbes suspendus à la poutre
    for k, x in enumerate((-30, -20)):
        c.line(x, 108, x, 122 + k * 5, (150, 120, 70))
        for j in range(4):
            c.shape(c.mask_ell(x + (j % 2) * 2 - 1, 125 + k * 5 + j * 5, 2.6, 2.6), (206, 166, 112), (160, 120, 80), band=1)
    c.line(-8, 108, -8, 118, (150, 120, 70))
    c.shape(c.mask_poly([(-13, 118), (-3, 118), (0, 140), (-16, 140)]), (112, 132, 72), (82, 100, 52), band=1)
    # banc de terre (mastaba) : natte, coussins, la lampe
    c.shape(c.mask_rect(-30, 284, 96, 306), dk(mur, 0.92), dk(mur, 0.76), lt(mur, 0.06), band=2)
    c.fill(c.mask_rect(-26, 282, 92, 285), (198, 168, 106))
    for x in range(-26, 93, 3):
        c.px(x, 283, (172, 142, 88))
    for (cx, col) in ((-12, (150, 70, 60)), (76, (70, 96, 150))):
        c.shape(c.mask_ell(cx, 278, 9, 5), col, dk(col, 0.72), lt(col, 0.15), band=1)
    lx, ly = 30, 281
    c.shape(c.mask_ell(lx, ly - 2, 6, 2.5) | c.mask_poly([(lx + 4, ly - 3), (lx + 9, ly - 5), (lx + 9, ly - 3)]),
            (172, 112, 72), (122, 78, 52), band=1)
    # fenêtre sur le fleuve (volets ouverts)
    fx0, fy0, fx1, fy1 = 104, 146, 184, 214
    c.fill(c.mask_rect(fx0 - 4, fy0 - 4, fx1 + 4, fy1 + 4), dk(mur, 0.72))
    vue_f = c.mask_rect(fx0, fy0, fx1, fy1)
    _vue_fleuve(c, vue_f, fx0, fy0, fx1, fy1, heure, hz=fy0 + 34)
    for (a, b) in ((fx0 - 17, fx0 - 5), (fx1 + 5, fx1 + 17)):
        v = c.mask_rect(a, fy0 - 2, b, fy1 + 2)
        c.shape(v, (124, 86, 52), (92, 62, 38), (150, 110, 70), band=1)
        for y in range(fy0 + 4, fy1, 6):
            c.fill(v & c.mask_rect(a, y, b, y), (100, 70, 42))
    c.shape(c.mask_rect(fx0 - 6, fy1 + 4, fx1 + 6, fy1 + 8), (156, 120, 84), (112, 86, 58), band=1)
    _jarre(c, fx1 - 8, fy1 + 4, (176, 116, 74), h=6)
    # grande jarre d'eau (zir) sur son support
    c.shape(c.mask_rect(206, 290, 236, 306), (110, 80, 52), (80, 58, 36), band=1)
    c.shape(c.mask_ell(221, 270, 15, 20) | c.mask_rect(214, 248, 228, 254), (178, 120, 78), (130, 86, 56), (204, 150, 100), band=2)
    c.fill(c.mask_ell(221, 250, 8, 2), (60, 40, 30))
    # porte sur la rive (droite) : l'eau, les roseaux
    porte = c.mask_arch(282, 330, 196, 306)
    c.fill(c.mask_arch(277, 335, 191, 306), dk(mur, 0.7))
    _vue_fleuve(c, porte, 282, 196, 330, 306, heure, hz=246, seed=8)

    def bord(c):
        c.fill(c.mask_rect(282, 292, 330, 306), dk(RIVE[heure], 0.9))
        _roseaux(c, 282, 300, 300, 26, PALME[heure][0], seed=4)
        _roseaux(c, 316, 330, 300, 30, PALME[heure][0], seed=5)
    _clip(c, porte, bord)
    # filet de pêche (droite)
    c.line(336, 126, 374, 126, (100, 80, 50))
    filet = c.mask_poly([(338, 127), (374, 127), (368, 236), (344, 236)])
    for x in range(336, 384, 4):
        c.fill(filet & c.mask_poly([(x, 127), (x + 1, 127), (x - 8, 236), (x - 9, 236)]), (126, 116, 90))
    for y in range(129, 237, 5):
        c.fill(filet & c.mask_rect(338, y, 374, y), (126, 116, 90))
    # sol de terre battue, natte, jarres, meule
    sol = c.mask_rect(-105, 306, 375, 480)
    c.vgrad(sol, 306, 480, (156, 122, 88), (84, 62, 46), steps=6)
    for _ in range(60):
        x, y = rr.randint(-100, 370), rr.randint(312, 470)
        c.fill(c.mask_ell(x, y, rr.randint(2, 5), 1), (140, 108, 78))
    nat = c.mask_poly([(14, 318), (250, 318), (268, 362), (-4, 362)])
    c.fill(nat, (198, 168, 106))
    for x in range(-4, 270, 4):
        c.fill(nat & c.mask_rect(x, 318, x, 362), (172, 142, 88))
    c.fill(nat & ~c.mask_poly([(18, 321), (246, 321), (263, 359), (1, 359)]), (152, 62, 52))
    c.shape(c.mask_ell(248, 312, 10, 4), (128, 122, 114), (90, 86, 80), band=1)       # meule à grain
    c.shape(c.mask_ell(248, 309, 6, 2), (150, 144, 136), (110, 106, 100), band=1)
    for (jx, col) in ((300, (172, 106, 68)), (314, (152, 94, 62)), (352, (178, 122, 78))):
        _jarre(c, jx, 316, col, h=8)
    # lumières
    vues = vue_f | porte
    if heure in ("nuit", "soir"):
        _assombrit(c, ~vues, *dict(nuit=((0.36, 0.38, 0.54), (4, 4, 14)), soir=((0.72, 0.60, 0.58), (10, 4, 4)))[heure])
        fl = (lx + 9, ly - 8)
        c.fill(c.mask_ell(fl[0], fl[1], 1.6, 3), (255, 214, 130))
        c.px(fl[0], fl[1] - 3, (255, 240, 200))
        c.glow(fl[0], fl[1], 130 if nuit else 90, (255, 166, 86), 0.42 if nuit else 0.3)
        c.glow(fl[0], fl[1], 46, (255, 210, 140), 0.32)
    tache = c.mask_poly([(282, 306), (330, 306), (352, 338), (262, 338)])
    rayon_f = c.mask_poly([(fx0 + 6, fy1 + 9), (fx1 - 6, fy1 + 9), (fx1 + 34, 318), (fx0 + 26, 318)])
    if nuit:
        c.tint(tache, (150, 160, 220), 0.22)
        c.tint(rayon_f, (150, 160, 220), 0.08)
    elif heure == "soir":
        c.tint(tache, (255, 170, 110), 0.22)
    else:
        c.tint(tache, (255, 240, 200), 0.28)
        c.tint(rayon_f, (255, 244, 214), 0.12)
    return c, None


# ================================================================ la rive derrière la maison
def rive_maison(heure="aube", corde=False):
    """La rive derrière la maison : à gauche le mur de briques et la porte de derrière, la berge de terre humide qui
    descend dans l'eau, un piquet planté au bord ; le Nil, la rive d'en face et ses palmiers, roseaux et papyrus.
    corde=True : une corde part du piquet et va jusqu'au coffre (COFFRE place 600 1284). Pieds y = 330 (sur la berge)."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 236, dict(aube=(300, 196), jour=(250, 60), soir=(-20, 196), nuit=(280, 70))[heure], seed=23)
    snap = c.a.copy()
    rr = R(41)
    c.fill(c.mask_rect(-105, 228, 375, 236), RIVE[heure])
    fr, tr = PALME[heure]
    for k, x in enumerate(range(-100, 375, 22)):
        palmier(c, x + (k * 9) % 7, 232, h=14 + (k * 5) % 9, lean=(k % 3 - 1) * 4, seed=90 + k, col=fr, trunk=tr)
    eh, eb = EAU[heure]
    c.vgrad(c.mask_rect(-105, 236, 375, 480), 236, 480, eh, eb, steps=6)
    for _ in range(170):
        x, y = rr.randint(-100, 370), rr.randint(240, 470)
        c.fill(c.mask_rect(x, y, x + rr.randint(2, 8), y), lt(eh, 0.22))
    ax = dict(aube=300, jour=250, soir=-20, nuit=280)[heure]
    if heure != "jour":
        col = (230, 230, 250) if heure == "nuit" else (255, 214, 160)
        for y in range(238, 330, 3):
            w_ = 1 + (y - 236) // 8
            c.fill(c.mask_rect(ax - w_, y, ax + w_, y), col)
    if heure == "aube":                                              # brume du matin sur l'eau
        for y0, k in ((236, 0.34), (244, 0.22), (254, 0.12)):
            c.tint(c.mask_rect(-105, y0, 375, y0 + 8), (232, 222, 238), k)
    terre = T((150, 118, 84))
    berge = c.mask_poly([(-105, 290), (40, 292), (84, 304), (108, 322), (118, 344), (108, 380), (70, 480), (-105, 480)])
    c.vgrad(berge, 290, 480, terre, dk(terre, 0.62), steps=6)
    mouille = berge & ~c.mask_poly([(-105, 290), (36, 292), (78, 304), (100, 322), (110, 344), (100, 380), (62, 480), (-105, 480)])
    c.fill(mouille, dk(terre, 0.7))                                   # terre mouillée au bord de l'eau
    for _ in range(40):
        x, y = rr.randint(-100, 90), rr.randint(296, 470)
        c.fill(berge & c.mask_ell(x, y, rr.randint(2, 4), 1), lt(terre, 0.08))
    # la maison (arrière)
    mur = T(BRIQUE[0])
    mm = c.mask_rect(-105, 150, 52, 296)
    c.shape(mm, mur, dk(mur, 0.82), lt(mur, 0.06), band=2)
    _briques(c, mm, mur, seed=12)
    c.shape(c.mask_rect(-108, 144, 56, 151), lt(mur, 0.05), dk(mur, 0.7), band=1)
    _porte(c, 8, 36, 236, 296, heure == "nuit", ouverte=True)
    c.shape(c.mask_rect(2, 294, 42, 299), dk(terre, 0.9), dk(terre, 0.7), band=1)
    _fenetre(c, -70, 200, 12, 10, heure == "nuit")
    for (jx, col) in ((-30, T((170, 104, 66))), (-18, T((150, 92, 60)))):
        _jarre(c, jx, 300, col, h=8)
    # le piquet (et la corde)
    px0 = 78
    c.shape(c.mask_rect(px0 - 2, 288, px0 + 1, 326), T((120, 86, 54)), T((84, 58, 36)), band=1)
    c.fill(c.mask_rect(px0 - 3, 300, px0 + 2, 302), T((196, 170, 112)))
    if corde:
        for t in np.linspace(0, 1, 60):                              # corde épaisse, bien visible
            x_, y_ = px0 + 2 + (139 - px0 - 2) * t, 301 + (316 - 301) * t + 7 * math.sin(math.pi * t)
            c.fill(c.mask_rect(x_, y_, x_ + 1, y_ + 1), T((128, 96, 60)))
            c.px(x_, y_, T((176, 140, 90)))
    # roseaux et papyrus
    _roseaux(c, 240, 375, 300, 40, T((80, 120, 60)), seed=6)
    _papyrus(c, 334, 306, 62, T((70, 120, 60)), seed=3)
    _papyrus(c, 262, 304, 50, T((76, 128, 64)), seed=7)
    fg = _Px(alpha=True)
    _roseaux(fg, 300, 375, 480, 90, T((60, 96, 50)), seed=8)
    return relief(c, snap, sky), fg


# ================================================================ la ruelle (nuit, jour)
def ruelle(heure="jour", eteinte=False):
    """La ruelle devant la maison de la mère : trois maisons serrées (escalier extérieur à gauche, LA porte au centre,
    une autre porte à droite), toits lointains et un palmier qui dépasse ; de jour du linge sèche sur une corde tendue ;
    la nuit une lampe brille derrière la petite fenêtre et sous la porte (eteinte=True : tout est noir). Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    nuit = heure == "nuit"
    sky = _ciel(c, heure, 170, dict(aube=(300, 120), jour=(60, 40), soir=(-20, 130), nuit=(250, 116))[heure], seed=17)
    snap = c.a.copy()
    rr = R(31)
    loin = mix(T((150, 120, 96)), CIELS[heure][1], 0.45)
    for (x0, x1, top) in ((-105, -40, 128), (-40, 30, 140), (30, 110, 122), (110, 200, 134), (200, 280, 120), (280, 375, 136)):
        c.fill(c.mask_rect(x0, top, x1, 170), loin)
        c.fill(c.mask_rect(x0, top, x1, top), lt(loin, 0.08))
    palmier(c, 228, 156, h=46, lean=6, seed=31, col=mix(T((60, 110, 60)), CIELS[heure][1], 0.25),
            trunk=mix(T((120, 90, 60)), CIELS[heure][1], 0.25))
    # les trois maisons
    for (x0, x1, top, k) in ((-105, 96, 150, 0), (96, 236, 160, 2), (236, 375, 142, 1)):
        mur = T(BRIQUE[k])
        mm = c.mask_rect(x0, top, x1, 306)
        c.shape(mm, mur, dk(mur, 0.84), lt(mur, 0.06), band=2)
        _briques(c, mm, mur, seed=60 + k)
        c.shape(c.mask_rect(x0 - 1, top - 5, x1 + 1, top), lt(mur, 0.06), dk(mur, 0.7), band=1)     # parapet du toit
        for x in range(x0 + 4, x1 - 4, 16):
            c.fill(c.mask_rect(x, top - 8, x + 6, top - 5), dk(mur, 0.9))
    mur0 = T(BRIQUE[0])
    for i in range(14):                                               # escalier extérieur (maison de gauche)
        x_, y_ = -6 + i * 7, 300 - i * 6
        c.shape(c.mask_rect(x_, y_, 95, y_ + 6), lt(mur0, 0.06), dk(mur0, 0.78), band=1)
    _porte(c, 70, 90, 188, 222, nuit and not eteinte, ouverte=False)
    _porte(c, 118, 152, 236, 306, nuit, ouverte=False)                # LA porte (au centre)
    c.shape(c.mask_rect(112, 230, 158, 236), T((120, 90, 60)), T((90, 64, 40)), band=1)
    _fenetre(c, 188, 184, 12, 10, nuit, lampe=nuit and not eteinte)
    c.fill(c.mask_rect(170, 262, 180, 276), dk(T(BRIQUE[2]), 0.62))     # petite niche, une cruche
    _jarre(c, 175, 276, T((176, 116, 74)), h=6)
    _porte(c, 300, 330, 240, 306, nuit, ouverte=False)
    _fenetre(c, 252, 180, 12, 10, nuit, lampe=False)
    _fenetre(c, -70, 200, 12, 10, nuit, lampe=nuit)
    if not nuit:                                                      # linge qui sèche, sur une corde tendue
        def corde(t):
            return 40 + (300 - 40) * t, 176 + (170 - 176) * t + 12 * math.sin(math.pi * t)
        for t in np.linspace(0, 1, 120):
            c.px(*corde(t), T((110, 90, 70)))
        couleurs = ((200, 60, 50), (236, 228, 210), (60, 96, 160), (226, 186, 90), (236, 228, 210), (120, 150, 90))
        for j, t in enumerate((0.1, 0.2, 0.34, 0.5, 0.64, 0.8)):
            x, y = corde(t)
            w_, h_ = (10, 14) if j % 2 else (14, 10)
            c.shape(c.mask_rect(x - w_ // 2, y + 1, x + w_ // 2, y + 1 + h_), T(couleurs[j]), dk(T(couleurs[j]), 0.8), band=1)
    sol = c.mask_rect(-105, 306, 375, 480)
    terre = T((168, 140, 104))
    c.vgrad(sol, 306, 480, terre, dk(terre, 0.66), steps=6)
    c.fill(c.mask_poly([(120, 330), (150, 330), (170, 480), (100, 480)]), dk(terre, 0.88))          # rigole
    for _ in range(50):
        x, y = rr.randint(-100, 370), rr.randint(312, 470)
        c.fill(c.mask_ell(x, y, 1.6, 1), lt(terre, 0.1))
    for (jx, col) in ((60, (170, 104, 66)), (72, (150, 92, 60)), (232, (176, 120, 76)), (344, (160, 110, 70))):
        _jarre(c, jx, 312, T(col), h=8)
    c.shape(c.mask_ell(250, 310, 8, 4) & c.mask_rect(242, 306, 258, 314), T((176, 140, 86)), T((130, 100, 60)), band=1)   # panier
    if nuit:
        c.tint(c.mask_rect(-105, 0, 375, 480), (8, 8, 30), 0.22)
        if not eteinte:
            c.fill(c.mask_rect(118, 305, 152, 306), (255, 190, 110))                   # lueur sous la porte
            c.glow(135, 308, 30, (255, 170, 90), 0.35)
            c.glow(194, 189, 26, (255, 170, 90), 0.3)
    return relief(c, snap, sky), None


# ================================================================ le couloir à colonnes du palais
def couloir_palais(heure="jour"):
    """Un long couloir du palais : plafond bleu étoilé, architrave peinte, une file de colonnes lotus devant des panneaux
    peints (fleurs, pas de figures), dallage ; de jour le soleil entre de biais (rais de lumière sur les colonnes et au
    sol) ; la nuit, des braseros. Deux colonnes sombres au premier plan, aux bords. Pieds y = 330."""
    c = _Px()
    nuit = heure == "nuit"
    pierre = (222, 200, 160)
    c.vgrad(c.mask_rect(-105, 0, 375, 306), 100, 306, dk(pierre, 0.84), dk(pierre, 0.96), steps=6)
    c.fill(c.mask_rect(-105, 0, 375, 112), (40, 60, 120))                # plafond bleu étoilé
    for y in range(4, 110, 8):
        for x in range(-104 + (y // 8 % 2) * 4, 375, 8):
            c.px(x, y, (232, 200, 92))
    c.shape(c.mask_rect(-105, 112, 375, 124), dk(pierre, 0.9), dk(pierre, 0.7), band=1)
    for y0, col in ((114, (40, 90, 160)), (117, (220, 170, 60)), (120, (190, 60, 40))):
        c.fill(c.mask_rect(-105, y0, 375, y0 + 1), col)
    for xc in range(-42, 375, 64):                                       # panneaux peints entre les colonnes
        pan = c.mask_rect(xc - 18, 150, xc + 18, 272)
        c.fill(pan, dk(pierre, 0.9))
        c.outline(pan, (220, 170, 60))
        for k in range(3):
            cy = 166 + k * 38
            c.fill(c.mask_poly([(xc, cy + 22), (xc - 9, cy), (xc, cy + 7), (xc + 9, cy)]), (60, 130, 110))
            c.fill(c.mask_rect(xc, cy + 18, xc, cy + 30), (60, 130, 110))
            c.fill(c.mask_ell(xc, cy - 3, 2.5, 2.5), (220, 170, 60))
    for x in range(-74, 375, 64):                                        # colonnes (chapiteaux visibles)
        _colonne_lotus(c, x, 133, 306, 16, dk(pierre, 0.93))
    sol = c.mask_rect(-105, 306, 375, 480)
    c.vgrad(sol, 306, 480, dk(pierre, 0.9), dk(pierre, 0.6), steps=6)
    for y in range(312, 480, 12):
        c.fill(sol & c.mask_rect(-105, y, 375, y), dk(pierre, 0.56))
    for x in range(-100, 375, 24):
        c.fill(sol & c.mask_rect(x, 306, x, 480), dk(pierre, 0.62))
    for x in range(-74, 375, 64):                                        # reflets des colonnes dans le dallage poli
        c.tint(c.mask_rect(x - 6, 308, x + 6, 340), lt(pierre, 0.1), 0.18)
    if not nuit:                                                         # rais de soleil, de biais
        for x0 in range(-112, 375, 64):
            c.tint(c.mask_poly([(x0 + 4, 124), (x0 + 22, 124), (x0 + 70, 306), (x0 + 52, 306)]), (255, 238, 196), 0.18)
            c.tint(c.mask_poly([(x0 + 52, 306), (x0 + 70, 306), (x0 + 96, 352), (x0 + 74, 352)]), (255, 238, 196), 0.24)
    else:
        _assombrit(c, c.mask_rect(-105, 0, 375, 480), (0.42, 0.42, 0.58), (6, 4, 16))
        for x in range(-42, 375, 128):
            _brasero(c, x, 306, True)
    fg = _Px(alpha=True)
    for x in (-98, 368):
        _colonne_lotus(fg, x, 20, 470, 34, dk(pierre, 0.62 if not nuit else 0.34), peint=False)
    return c, fg


# ================================================================ la chambre d'Asiya
def chambre_asiya(heure="jour"):
    """La chambre d'Asiya : frise de rosettes, grande loggia à deux colonnettes ouverte sur le jardin (palmiers, bassin,
    fleurs), lit de repos avec coussins, deux grands lampadaires de bronze, table basse aux fruits, tapis et coussins.
    Les voiles (qui ondulent) sont l'option « voiles ». Asiya est une orbe. Pieds y = 330."""
    c = _Px()
    nuit = heure == "nuit"
    mur = (238, 224, 198)
    c.fill(c.mask_rect(-105, 0, 375, 112), (60, 82, 140))                 # plafond peint
    for y in range(6, 110, 10):
        for x in range(-100 + (y // 10 % 2) * 5, 375, 10):
            c.px(x, y, (232, 200, 92))
    c.vgrad(c.mask_rect(-105, 112, 375, 306), 112, 306, dk(mur, 0.86), mur, steps=6)
    c.shape(c.mask_rect(-105, 112, 375, 124), (60, 130, 110), (40, 96, 80), band=1)       # frise de rosettes
    for x in range(-100, 375, 12):
        c.fill(c.mask_ell(x, 118, 3, 3), (226, 178, 70))
        c.px(x, 118, (190, 60, 40))
    c.fill(c.mask_rect(-105, 124, 375, 126), (220, 170, 60))
    c.fill(c.mask_rect(-105, 270, 375, 306), (64, 96, 150))                # soubassement peint
    for x in range(-104, 375, 8):
        c.fill(c.mask_poly([(x, 272), (x + 4, 278), (x + 8, 272)]), (226, 178, 70))
    c.fill(c.mask_rect(-105, 270, 375, 271), (226, 178, 70))
    # la loggia sur le jardin
    lx0, lx1, ly0, ly1 = 64, 256, 138, 270
    loggia = c.mask_rect(lx0, ly0, lx1, ly1)

    def jardin(c):
        top, bot = CIELS["nuit" if nuit else "jour"]
        c.vgrad(loggia, ly0, 210, top, bot, steps=5)
        if nuit:
            rnd = R(12)
            for _ in range(40):
                c.px(rnd.randint(lx0, lx1), rnd.randint(ly0, 200), (226, 226, 252))
            c.fill(c.mask_ell(220, 156, 6, 6) & ~c.mask_ell(223, 154, 5, 5), (248, 240, 212))
        vert = (70, 130, 76) if not nuit else (20, 34, 40)
        c.fill(c.mask_rect(lx0, 206, lx1, ly1), mix(vert, (120, 160, 90), 0.4) if not nuit else vert)
        for k, x in enumerate(range(lx0 + 8, lx1, 26)):
            palmier(c, x + (k * 7) % 9, 214, h=36 + (k * 11) % 16, lean=(k % 3 - 1) * 5, seed=210 + k,
                    col=(60, 130, 70) if not nuit else (16, 28, 34), trunk=(130, 98, 62) if not nuit else (24, 24, 30))
        bas = c.mask_ell(160, 240, 50, 7)
        c.fill(bas, (90, 160, 190) if not nuit else (30, 44, 80))
        c.outline(bas, (200, 186, 160) if not nuit else (60, 60, 80))
        for fx in range(116, 206, 12):
            c.fill(c.mask_ell(fx, 240, 3, 1.4), (90, 160, 90) if not nuit else (30, 50, 40))
        for fx in range(lx0 + 4, lx1, 7):                                  # massifs de fleurs
            c.px(fx, 256 + (fx % 3), (236, 120, 140) if not nuit else (70, 50, 70))
            c.px(fx + 3, 258, (250, 220, 110) if not nuit else (70, 70, 60))
        c.fill(c.mask_rect(lx0, 262, lx1, ly1), (214, 196, 160) if not nuit else (60, 56, 70))   # muret du jardin
    _clip(c, loggia, jardin)
    c.outline(loggia, (160, 120, 60))
    for xc in (128, 192):                                                  # colonnettes de la loggia
        _colonne_lotus(c, xc, 150, 272, 8, (236, 222, 196))
    c.shape(c.mask_rect(lx0 - 4, ly0 - 6, lx1 + 4, ly0), (230, 214, 186), (190, 170, 140), band=1)
    # lit de repos (gauche)
    bois = (176, 128, 60)
    c.shape(c.mask_rect(-96, 286, -14, 292), (236, 230, 216), (200, 194, 180), band=1)      # matelas
    c.shape(c.mask_rect(-98, 292, -12, 297), bois, dk(bois, 0.7), band=1)
    for x in (-94, -18):
        c.shape(c.mask_rect(x, 297, x + 3, 306), bois, dk(bois, 0.7), band=1)                # pieds
    c.shape(c.mask_rect(-100, 270, -94, 292), bois, dk(bois, 0.7), band=1)                   # tête de lit
    for (cx, col) in ((-80, (190, 70, 60)), (-66, (60, 96, 160)), (-28, (226, 178, 70))):
        c.shape(c.mask_ell(cx, 284, 7, 4), col, dk(col, 0.72), lt(col, 0.15), band=1)
    # lampadaires de bronze
    for x in (22, 300):
        c.shape(c.mask_rect(x - 1, 246, x + 1, 306), (170, 130, 60), (120, 90, 40), band=1)
        c.shape(c.mask_rect(x - 6, 302, x + 6, 306), (170, 130, 60), (120, 90, 40), band=1)
        c.shape(c.mask_ell(x, 245, 7, 3), (210, 160, 70), (150, 110, 40), band=1)
    # table basse aux fruits (droite)
    c.shape(c.mask_rect(318, 292, 362, 296), bois, dk(bois, 0.7), band=1)
    for x in (322, 356):
        c.shape(c.mask_rect(x, 296, x + 2, 306), bois, dk(bois, 0.7), band=1)
    c.shape(c.mask_ell(340, 289, 11, 3), (226, 182, 82), (176, 130, 50), band=1)
    for (fx, col) in ((334, (190, 60, 70)), (340, (110, 60, 120)), (346, (230, 160, 60)), (337, (120, 160, 70))):
        c.fill(c.mask_ell(fx, 285, 2.4, 2.4), col)
    # sol, tapis, coussins
    sol = c.mask_rect(-105, 306, 375, 480)
    c.vgrad(sol, 306, 480, dk(mur, 0.9), dk(mur, 0.62), steps=6)
    for y in range(314, 480, 14):
        c.fill(sol & c.mask_rect(-105, y, 375, y), dk(mur, 0.7))
    tapis = c.mask_poly([(40, 318), (280, 318), (306, 372), (14, 372)])
    c.fill(tapis, (150, 50, 60))
    c.fill(tapis & ~c.mask_poly([(44, 321), (276, 321), (300, 369), (20, 369)]), (220, 170, 60))
    for x in range(60, 270, 24):
        c.fill(c.mask_poly([(x, 334), (x + 8, 342), (x, 350), (x - 8, 342)]), (220, 170, 60))
    for (cx, col) in ((-40, (60, 90, 160)), (-24, (190, 70, 60)), (330, (226, 178, 70)), (346, (60, 130, 110))):
        c.shape(c.mask_ell(cx, 316, 9, 5), col, dk(col, 0.72), lt(col, 0.15), band=1)
    if nuit:
        _assombrit(c, ~loggia, (0.44, 0.42, 0.56), (6, 4, 14))
    for x in (22, 300):                                                    # les flammes des lampadaires
        c.fill(c.mask_ell(x, 239, 2.2, 4), (255, 200, 110))
        c.px(x, 236, (255, 240, 200))
        c.glow(x, 238, 60 if not nuit else 110, (255, 180, 100), 0.2 if not nuit else 0.42)
    if not nuit:                                                           # le jour entre par la loggia
        c.tint(c.mask_poly([(lx0, 306), (lx1, 306), (lx1 + 50, 372), (lx0 + 20, 372)]), (255, 244, 214), 0.12)
    return c, None


def anim_voiles(nuit=False, amp=3.0, periode=6.0):
    """Les voiles de la chambre d'Asiya : deux pans légers aux bords de la loggia, qui ondulent lentement."""
    from PIL import Image, ImageDraw
    col = (240, 236, 246, 150) if not nuit else (112, 108, 142, 130)
    pli = (214, 208, 228, 180) if not nuit else (90, 86, 120, 150)
    voiles = ((52, 84, 132, 300, 0.0), (236, 268, 132, 300, 1.9))

    def f(img, u):
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for (x0, x1, y0, y1, ph) in voiles:
            g_, d_ = [], []
            for y in range(y0, y1 + 1, 4):
                k = ((y - y0) / (y1 - y0)) ** 1.5
                dx = amp * k * math.sin(2 * math.pi * u / periode + ph + y * 0.025)
                g_.append((x0 + dx + 105, y))
                d_.append((x1 + dx * 1.25 + 105, y))
            d.polygon(g_ + d_[::-1], fill=col)
            for j in (0.22, 0.5, 0.78):
                d.line([(a[0] + (b[0] - a[0]) * j, a[1]) for a, b in zip(g_, d_)], fill=pli, width=1)
            d.rectangle([x0 - 3 + 105, y0 - 3, x1 + 3 + 105, y0 - 1], fill=(206, 164, 72, 255))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ le marché
def marche_egypte(heure="jour"):
    """Le marché : étals sous des toiles rayées (dattes, grain, jarres, étoffes, poissons), maisons derrière ; la foule
    se met en persos (et des ânes : ANE). Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 190, dict(aube=(300, 140), jour=(80, 40), soir=(-40, 140), nuit=(260, 50))[heure], seed=27)
    snap = c.a.copy()
    rr = R(44)
    x = -110
    k = 0
    while x < 380:
        w = rr.randint(50, 80)
        mur = T(BRIQUE[(k + 1) % 4])
        mm = c.mask_rect(x, rr.randint(150, 190), x + w, 300)
        c.shape(mm, mur, dk(mur, 0.82), band=2)
        _briques(c, mm, mur, seed=70 + k)
        _fenetre(c, x + 10, 210, 8, 7, heure == "nuit")
        x += w
        k += 1
    for i, x0 in enumerate(range(-100, 375, 70)):
        cols = ((200, 60, 50), (240, 230, 210)) if i % 2 else ((50, 90, 160), (240, 230, 210))
        toile = c.mask_poly([(x0, 236), (x0 + 60, 236), (x0 + 66, 252), (x0 - 6, 252)])
        c.fill(toile, T(cols[0]))
        for xx in range(x0 - 6, x0 + 66, 8):
            c.fill(toile & c.mask_rect(xx, 236, xx + 3, 252), T(cols[1]))
        c.outline(toile, (60, 40, 30))
        for px_ in (x0 - 2, x0 + 62):
            c.fill(c.mask_rect(px_, 252, px_ + 1, 300), T((120, 90, 56)))
        c.shape(c.mask_rect(x0, 284, x0 + 60, 300), T((150, 110, 70)), T((110, 80, 50)), band=1)
        for j in range(4):
            gx = x0 + 6 + j * 14
            kind = (i * 3 + j) % 5
            if kind in (0, 2):
                c.shape(c.mask_ell(gx, 282, 5, 3), T((170, 130, 76)), T((120, 90, 56)), band=1)
                c.fill(c.mask_ell(gx, 280, 4, 1.5), T((110, 50, 30) if kind == 0 else (220, 200, 120)))
            elif kind == 1:
                _jarre(c, gx, 284, T((176, 110, 70)), h=6)
            elif kind == 3:
                c.shape(c.mask_rect(gx - 5, 276, gx + 5, 284), T(((60, 90, 160), (190, 60, 50), (230, 200, 120))[(i + j) % 3]),
                        T((90, 70, 60)), band=1)
            else:                                                            # poissons sur une claie
                c.shape(c.mask_rect(gx - 6, 281, gx + 6, 284), T((130, 110, 80)), T((100, 80, 60)), band=1)
                for fy in (277, 280):
                    c.fill(c.mask_ell(gx - 1, fy, 4, 1.2) | c.mask_poly([(gx + 3, fy), (gx + 6, fy - 2), (gx + 6, fy + 2)]),
                           T((150, 166, 180)))
        if i % 3 == 1:                                                       # étoffes suspendues
            for j, col in enumerate(((190, 60, 50), (60, 96, 160), (226, 186, 90))):
                c.fill(c.mask_rect(x0 + 8 + j * 16, 253, x0 + 18 + j * 16, 266), T(col))
    sol = c.mask_rect(-105, 300, 375, 480)
    terre = T((176, 146, 104))
    c.vgrad(sol, 300, 480, lt(terre, 0.06), dk(terre, 0.7), steps=6)
    for _ in range(70):
        x, y = rr.randint(-100, 370), rr.randint(306, 470)
        c.fill(c.mask_ell(x, y, 1.6, 1), lt(terre, 0.1))
    for y0, kk in ((420, 0.10), (440, 0.18), (460, 0.26)):
        c.tint(c.mask_rect(-105, y0, 375, 480), (40, 24, 20), kk)
    return relief(c, snap, sky), None


# ================================================================ l'allée qui monte au palais
def avenue_palais(heure="jour"):
    """L'allée du palais : une large voie dallée qui file vers le grand pylône (au fond), bordée de palmiers ; les gens se
    tiennent sur les bords avec des cadeaux (persos). Option « petales » : des pétales tombent. Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 200, dict(aube=(320, 150), jour=(60, 50), soir=(-40, 150), nuit=(300, 60))[heure], seed=33)
    snap = c.a.copy()
    pierre = T((222, 196, 150))
    for x0, x1 in ((84, 128), (142, 186)):
        tour = c.mask_poly([(x0, 210), (x1, 210), (x1 - 4, 140), (x0 + 4, 140)])
        c.shape(tour, pierre, dk(pierre, 0.8), band=1)
        c.shape(c.mask_rect(x0 + 2, 134, x1 - 2, 141), lt(pierre, 0.06), dk(pierre, 0.7), band=1)
        for k, col in enumerate(((40, 90, 160), (190, 60, 40), (220, 170, 60))):           # bannières
            c.fill(c.mask_rect(x0 + 6 + k * 12, 146, x0 + 9 + k * 12, 176), T(col))
    c.fill(c.mask_rect(128, 170, 142, 210), dk(pierre, 0.6))
    c.fill(c.mask_rect(-105, 206, 375, 214), mix(T((90, 130, 80)), CIELS[heure][1], 0.3))
    voie = c.mask_poly([(122, 214), (148, 214), (300, 480), (-30, 480)])
    c.vgrad(voie, 214, 480, dk(pierre, 0.95), dk(pierre, 0.75), steps=6)
    for t in np.linspace(0, 1, 18):
        y = int(214 + 266 * t * t)
        c.fill(voie & c.mask_rect(int(122 - 152 * t * t), y, int(148 + 152 * t * t), y), dk(pierre, 0.68))
    bords = c.mask_rect(-105, 214, 375, 480) & ~voie
    c.vgrad(bords, 214, 480, T((190, 166, 120)), T((140, 116, 80)), steps=6)
    for k in range(7):
        t = k / 6
        y = int(216 + 200 * t * t)
        h = int(22 + 120 * t * t)
        for side in (-1, 1):
            x = int(135 + side * (22 + 190 * t * t + 10))
            palmier(c, x, y, h=h, lean=side * 4, seed=500 + k * 2 + (side > 0), col=T((60, 120, 66)), trunk=T((130, 98, 62)))
    return relief(c, snap, sky), None


def anim_petales(n=70, seed=5, vitesse=20.0):
    """Des pétales (roses, blancs) tombent doucement en tournoyant sur toute la scène."""
    from PIL import Image, ImageDraw
    rnd = R(seed)
    P = [(rnd.uniform(-105, 375), rnd.uniform(0, 400), rnd.uniform(0.6, 1.2), rnd.uniform(0, 6.28),
          rnd.choice(((250, 196, 210), (255, 238, 242), (240, 160, 186), (255, 214, 120)))) for _ in range(n)]

    def f(img, u):
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for (x, y0, v, ph, col) in P:
            y = 60 + (y0 + u * vitesse * v) % 400
            xx = x + 7 * math.sin(u * 1.1 * v + ph) + 105
            large = math.sin(u * 2.4 * v + ph) > 0
            d.rectangle([xx, y, xx + (2 if large else 1), y + 1], fill=(*col, 235))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ Memphis à l'heure de la sieste / au matin
def ville_midi(heure="jour"):
    """Memphis : la rue principale, maisons hautes et blanchies, portes et volets fermés, étals rabattus ; au milieu du
    jour pas une âme, le soleil écrase tout (ombres courtes). ville_matin : la même au petit matin. Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 180, dict(aube=(310, 150), jour=(140, 24), soir=(-30, 150), nuit=(300, 60))[heure], seed=41)
    if heure == "jour":
        c.tint(sky, (255, 248, 230), 0.25)
    snap = c.a.copy()
    rr = R(57)
    blanc = T((236, 226, 204))
    x = -110
    k = 0
    while x < 380:
        w = rr.randint(56, 92)
        mur = mix(blanc, T(BRIQUE[k % 4]), 0.25 + 0.15 * (k % 2))
        top = rr.randint(120, 170)
        c.shape(c.mask_rect(x, top, x + w, 306), mur, dk(mur, 0.86), lt(mur, 0.1), band=2)
        c.fill(c.mask_rect(x, 300, x + w, 306), dk(mur, 0.8))
        c.shape(c.mask_rect(x - 1, top - 4, x + w + 1, top), lt(mur, 0.1), dk(mur, 0.7), band=1)
        for j in range(2):
            _fenetre(c, x + 10 + j * (w - 28), top + 20, 9, 9, False)
        _porte(c, x + w // 2 - 7, x + w // 2 + 7, 270, 306, False, ouverte=False)
        if k % 3 == 1:
            tl = c.mask_rect(x + 4, 250, x + w - 4, 266)
            c.shape(tl, T((200, 180, 140)), T((160, 140, 100)), band=1)
            for xx in range(x + 6, x + w - 4, 6):
                c.fill(tl & c.mask_rect(xx, 250, xx, 266), T((170, 150, 110)))
        x += w
        k += 1
    sol = c.mask_rect(-105, 306, 375, 480)
    terre = T((200, 176, 136))
    c.vgrad(sol, 306, 480, lt(terre, 0.12), dk(terre, 0.78), steps=6)
    c.fill(c.mask_rect(-105, 306, 375, 309 if heure == "jour" else 318), dk(terre, 0.8))     # ombre des murs
    for _ in range(50):
        x, y = rr.randint(-100, 370), rr.randint(312, 470)
        c.fill(c.mask_ell(x, y, 1.6, 1), lt(terre, 0.15))
    if heure == "jour":
        c.tint(c.mask_rect(-105, 0, 375, 480), (255, 244, 220), 0.10)
    return relief(c, snap, sky), None


# ================================================================ le désert entre l'Égypte et Madyan
def desert(heure="jour"):
    """Le désert : dunes en plans successifs, rochers, une piste à peine marquée, un acacia isolé (à droite), herbes
    sèches ; la nuit, étoiles et dunes bleues. Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 230, dict(aube=(320, 210), jour=(60, 50), soir=(-60, 200), nuit=(300, 60))[heure], seed=61)
    snap = c.a.copy()
    rr = R(66)
    sable = T((216, 176, 118))
    c.fill(c.mask_rect(-105, 220, 375, 480), mix(sable, CIELS[heure][1], 0.35))
    for (ytop, amp, per, ph, k) in ((222, 8, 70, 0.0, 0.45), (246, 10, 54, 1.4, 0.28), (276, 12, 80, 2.6, 0.12)):
        m = c.yy >= ytop + amp * np.sin(c.xx / per + ph)
        col = mix(sable, CIELS[heure][1], k)
        c.vgrad(m, ytop - amp, 480, lt(col, 0.05), dk(col, 0.85), steps=5)
        c.fill(m & ~np.roll(m, 1, axis=0), lt(col, 0.18))
    for (rx, ry, w, h) in ((-70, 300, 26, 14), (40, 296, 14, 8), (300, 302, 22, 12)):
        r_ = c.mask_ell(rx, ry, w, h) & c.mask_rect(rx - w, ry - h, rx + w, ry + 2)
        c.shape(r_, T((150, 120, 96)), T((100, 80, 64)), T((186, 160, 130)), band=2)
    c.fill(c.mask_poly([(-105, 336), (375, 322), (375, 330), (-105, 346)]), dk(sable, 0.92))
    ac_x, ac_y = 250, 304
    c.fill(c.mask_rect(ac_x - 1, ac_y - 26, ac_x + 1, ac_y), T((96, 70, 50)))
    for (bx, by) in ((-14, -26), (12, -24), (-6, -32), (8, -30)):
        c.line(ac_x, ac_y - 18, ac_x + bx, ac_y + by, T((96, 70, 50)))
    canopee = c.mask_ell(ac_x, ac_y - 32, 24, 6)
    c.fill(canopee, T((86, 120, 70)))
    c.fill(canopee & c.mask_ell(ac_x - 4, ac_y - 34, 18, 3), T((110, 146, 84)))
    for _ in range(40):
        x, y = rr.randint(-100, 370), rr.randint(300, 460)
        for j in range(3):
            c.px(x + j - 1, y - (j % 2), T((170, 150, 90)))
    for y0, kk in ((420, 0.10), (440, 0.18), (460, 0.26)):
        c.tint(c.mask_rect(-105, y0, 375, 480), (40, 24, 20), kk)
    return relief(c, snap, sky), None


# ================================================================ la porte de la ville, au crépuscule
def porte_ville(heure="soir"):
    """La sortie de la ville : à gauche le rempart crénelé et sa grande porte ouverte (torches allumées), derrière lui les
    toits, les palmiers et les fenêtres éclairées ; à droite le désert à perte de vue et la piste qui s'y enfonce.
    Pieds y = 330 (la porte s'ouvre à y = 306 : faire sortir l'orbe en glissant vers l'avant)."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 236, dict(aube=(330, 214), jour=(300, 60), soir=(320, 218), nuit=(300, 60))[heure], seed=71)
    snap = c.a.copy()
    rr = R(72)
    sable = T((216, 176, 118))
    c.fill(c.mask_rect(-105, 226, 375, 480), mix(sable, CIELS[heure][1], 0.35))
    for (ytop, amp, per, ph, k) in ((228, 4, 60, 0.0, 0.5), (244, 6, 48, 1.4, 0.3), (268, 8, 70, 2.6, 0.15)):
        m = (c.yy >= ytop + amp * np.sin(c.xx / per + ph)) & (c.xx > 110)
        col = mix(sable, CIELS[heure][1], k)
        c.vgrad(m, ytop - amp, 480, lt(col, 0.05), dk(col, 0.85), steps=5)
        c.fill(m & ~np.roll(m, 1, axis=0), lt(col, 0.18))
    # la ville derrière le rempart
    for j, (x0, x1, top) in enumerate(((-105, -60, 150), (-60, -10, 134), (-10, 40, 156), (40, 96, 142), (96, 136, 164))):
        col = mix(T(BRIQUE[j % 4]), CIELS[heure][1], 0.25)
        c.fill(c.mask_rect(x0, top, x1, 200), col)
        c.fill(c.mask_rect(x0, top, x1, top), lt(col, 0.1))
        for _ in range(3):
            wx, wy = rr.randint(x0 + 4, x1 - 6), rr.randint(top + 6, 192)
            c.fill(c.mask_rect(wx, wy, wx + 2, wy + 2), (255, 200, 110) if heure in ("soir", "nuit") else dk(col, 0.6))
    for x, h in ((-80, 40), (20, 46), (110, 34)):
        palmier(c, x, 176, h=h, lean=4, seed=700 + x, col=mix(T((60, 110, 60)), CIELS[heure][1], 0.3),
                trunk=mix(T((120, 90, 60)), CIELS[heure][1], 0.3))
    # le rempart et la porte
    pierre = T((182, 146, 102))
    rempart = c.mask_rect(-105, 182, 140, 306)
    c.shape(rempart, pierre, dk(pierre, 0.8), lt(pierre, 0.06), band=2)
    _briques(c, rempart, pierre, pas_y=8, pas_x=14, seed=5)
    for x in range(-105, 141, 12):
        c.shape(c.mask_rect(x, 174, x + 7, 182), pierre, dk(pierre, 0.8), band=1)
    tour = c.mask_rect(124, 160, 156, 306)
    c.shape(tour, lt(pierre, 0.04), dk(pierre, 0.76), band=2)
    _briques(c, tour, pierre, pas_y=8, pas_x=14, seed=6)
    for x in range(124, 157, 10):
        c.shape(c.mask_rect(x, 152, x + 6, 160), pierre, dk(pierre, 0.8), band=1)
    ouv = c.mask_rect(34, 218, 86, 306)
    c.fill(ouv, (52, 36, 36))
    c.fill(c.mask_rect(44, 240, 76, 306), (90, 60, 50))                     # rue derrière la porte
    for wx in (50, 66):
        c.fill(c.mask_rect(wx, 252, wx + 3, 256), (255, 200, 110))
    c.shape(c.mask_rect(34, 222, 42, 306), T((110, 76, 46)), T((80, 54, 32)), band=1)    # battants ouverts
    c.shape(c.mask_rect(78, 222, 86, 306), T((110, 76, 46)), T((80, 54, 32)), band=1)
    c.shape(c.mask_rect(28, 210, 92, 218), lt(pierre, 0.06), dk(pierre, 0.7), band=1)     # linteau
    for tx in (22, 98):                                                      # torches
        c.shape(c.mask_rect(tx - 1, 236, tx + 1, 252), (90, 62, 40), (60, 40, 26), band=1)
        c.fill(c.mask_ell(tx, 232, 3, 5), (255, 150, 60))
        c.fill(c.mask_ell(tx, 233, 1.5, 3), (255, 226, 140))
        c.glow(tx, 232, 46, (255, 170, 80), 0.4)
    # la piste qui part de la porte vers le désert
    piste = c.mask_poly([(40, 306), (80, 306), (375, 318), (375, 338), (150, 340), (40, 330)])
    terre = mix(sable, CIELS[heure][1], 0.1)
    c.vgrad(c.mask_rect(-105, 306, 140, 480), 306, 480, terre, dk(terre, 0.7), steps=5)
    c.fill(piste & (c.yy >= 306), dk(sable, 0.92))
    for y0, kk in ((420, 0.10), (440, 0.18), (460, 0.26)):
        c.tint(c.mask_rect(-105, y0, 375, 480), (40, 24, 20), kk)
    return relief(c, snap, sky), None


# ================================================================ le ciel au-dessus du palais endormi
def palais_ciel():
    """Un grand ciel étoilé (voie lactée, lueur blanche très douce au milieu) au-dessus du palais endormi (silhouette :
    pylônes, colonnade, palmiers) et de son reflet dans le Nil. Les orbes se placent haut dans le ciel (y ≈ 600-800)."""
    c = _Px()
    c.vgrad(c.mask_rect(-105, 0, 375, 330), 0, 330, (8, 10, 30), (38, 48, 94), steps=8)
    rr = R(81)
    bande = c.mask_poly([(-105, 300), (-105, 230), (375, 40), (375, 120)])
    c.tint(bande, (120, 130, 190), 0.10)
    for _ in range(700):
        x, y = rr.randint(-105, 374), rr.randint(0, 318)
        if bande[y, x + 105] or rr.random() < 0.45:
            c.px(x, y, (236, 236, 255) if rr.random() < 0.25 else ((170, 176, 226) if rr.random() < 0.6 else (110, 118, 180)))
    c.glow(135, 170, 150, (220, 226, 255), 0.16)
    sil = (16, 18, 42)
    for x0, x1 in ((20, 74), (196, 250)):                                   # pylônes
        c.fill(c.mask_poly([(x0, 318), (x1, 318), (x1 - 6, 236), (x0 + 6, 236)]), sil)
        c.fill(c.mask_rect(x0 + 4, 230, x1 - 4, 236), sil)
    c.fill(c.mask_rect(74, 262, 196, 318), sil)                             # colonnade
    for x in range(80, 196, 12):
        c.fill(c.mask_rect(x, 266, x + 1, 318), (26, 30, 60))
    c.fill(c.mask_rect(-105, 294, 375, 318), sil)                           # terrasses
    for x, h in ((-80, 44), (-40, 36), (290, 46), (334, 38)):
        palmier(c, x, 300, h=h, lean=4, seed=800 + x, col=(14, 16, 38), trunk=(14, 16, 38))
    c.fill(c.mask_rect(-105, 318, 375, 480), (10, 12, 32))                  # le Nil, qui reflète le ciel
    for _ in range(140):
        x, y = rr.randint(-105, 370), rr.randint(322, 470)
        c.fill(c.mask_rect(x, y, x + rr.randint(1, 4), y), (60, 70, 120))
    for y in range(322, 352, 3):
        c.fill(c.mask_rect(132 - (y - 318) // 6, y, 138 + (y - 318) // 6, y), (150, 156, 210))
    return c, None


# ================================================================ la carte Égypte → Madyan
CHEMIN_MADYAN = [(32, 203), (58, 200), (86, 198), (106, 204), (128, 210), (152, 216), (176, 222), (200, 224), (222, 226),
                 (238, 232), (246, 250), (250, 270)]
CHEMIN_RETOUR = [(250, 270), (246, 250), (238, 232), (222, 228), (204, 236), (192, 248), (182, 262), (176, 270)]   # vers le Mont


def carte_madyan():
    """Carte peinte vue d'en haut : la Méditerranée, le Nil et son delta, le golfe de Suez, le Sinaï (montagnes au sud),
    le golfe d'Aqaba, Madyan de l'autre côté ; noms ÉGYPTE, SINAÏ, MADYAN. Le chemin s'anime avec l'option « chemin »."""
    c = _Px()
    mer, terre = (58, 104, 146), (216, 188, 138)
    c.fill(c.mask_rect(-105, 0, 375, 480), terre)
    rr = R(91)
    for _ in range(500):
        x, y = rr.randint(-105, 374), rr.randint(0, 479)
        c.px(x, y, lt(terre, 0.06) if rr.random() < 0.5 else dk(terre, 0.94))
    med = c.mask_poly([(-105, 0), (232, 0), (221, 80), (210, 101), (205, 110), (194, 122), (169, 131), (86, 123), (59, 110),
                       (-18, 113), (-45, 127), (-95, 138), (-105, 140)])
    rouge = c.mask_poly([(100, 195), (103, 215), (108, 248), (120, 270), (141, 297), (158, 319), (174, 347), (191, 380),
                         (210, 420), (230, 480), (365, 480), (330, 440), (290, 391), (262, 358), (235, 325), (210, 309),
                         (213, 300), (224, 281), (227, 254), (232, 237), (235, 219), (229, 221), (217, 248), (209, 276),
                         (202, 306), (194, 318), (180, 311), (158, 297), (141, 275), (125, 253), (111, 226), (103, 199)])
    eau = med | rouge | c.mask_ell(262, 102, 3, 9)
    c.fill(eau, mer)
    proche = eau & (np.roll(~eau, 2, 0) | np.roll(~eau, -2, 0) | np.roll(~eau, 2, 1) | np.roll(~eau, -2, 1))
    c.fill(proche, (92, 142, 178))
    c.fill(~eau & (np.roll(eau, 1, 0) | np.roll(eau, -1, 0) | np.roll(eau, 1, 1) | np.roll(eau, -1, 1)), dk(terre, 0.82))
    for (x, y, s) in ((160, 262, 9), (174, 272, 11), (186, 286, 9), (168, 284, 7), (150, 248, 6), (196, 276, 7),
                      (262, 240, 8), (276, 254, 10), (290, 236, 9), (270, 222, 7), (300, 262, 8), (284, 280, 7)):
        c.shape(c.mask_poly([(x - s, y + s * 0.6), (x, y - s * 0.7), (x + s, y + s * 0.6)]) & ~eau, (176, 140, 98),
                (140, 108, 74), (204, 176, 132), band=1)
    nil = [(18, 480), (22, 420), (24, 358), (31, 303), (26, 250), (29, 201), (28, 190)]
    _trait(c, nil, 7, (120, 160, 86))
    c.fill(c.mask_poly([(28, 186), (-24, 114), (62, 110)]) & ~eau, (120, 160, 86))
    _trait(c, nil, 2, (70, 120, 170))
    _trait(c, [(28, 190), (8, 150), (-18, 113)], 2, (70, 120, 170))
    _trait(c, [(28, 190), (44, 150), (59, 110)], 2, (70, 120, 170))
    for (px_, py_, s_) in ((12, 210, 4), (19, 212, 3), (7, 213, 2)):         # les pyramides, près de Memphis
        c.shape(c.mask_poly([(px_ - s_, py_), (px_, py_ - s_ * 1.2), (px_ + s_, py_)]), (236, 210, 150), (176, 146, 96), band=1)
    c.fill(c.mask_ell(29, 201, 2.5, 2.5), (120, 40, 40))                       # Memphis
    c.fill(c.mask_ell(250, 272, 2.5, 2.5), (120, 40, 40))                      # Madyan
    for (x, y, txt, s) in ((70, 300, "ÉGYPTE", 11), (156, 228, "SINAÏ", 10), (292, 286, "MADYAN", 10), (30, 190, "MEMPHIS", 6)):
        c.text((x, y), txt, (70, 44, 30), size=s, anchor="mm", ol=(236, 218, 176))
    c.tint(c.mask_rect(-105, 0, 375, 480) & ~c.mask_ell(135, 240, 300, 210), (60, 40, 24), 0.25)      # bords assombris
    return c, None


def anim_carte(t_debut=0.5, duree=14.0, nuits=8, chemin=CHEMIN_MADYAN):
    """Sur la carte : un pointillé doré avance de Memphis vers Madyan en `duree` secondes (petite lumière en tête) ; à
    chaque nuit de marche, une petite lune apparaît au-dessus du chemin (8 nuits)."""
    from PIL import Image, ImageDraw
    pts = chemin
    L = [0.0]
    for a, b in zip(pts, pts[1:]):
        L.append(L[-1] + math.dist(a, b))
    tot = L[-1]

    def point(dd):
        for i in range(len(pts) - 1):
            if L[i + 1] >= dd:
                e = (dd - L[i]) / max(1e-6, L[i + 1] - L[i])
                return pts[i][0] + (pts[i + 1][0] - pts[i][0]) * e, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * e
        return pts[-1]

    def f(img, u):
        p = max(0.0, min(1.0, (u - t_debut) / max(0.1, duree)))
        if p <= 0:
            return
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        dist = tot * p
        s = 0.0
        while s <= dist:
            x, y = point(s)
            d.rectangle([x + 105, y, x + 106, y + 1], fill=(250, 214, 110, 255))
            s += 6.0
        for k in range(1, nuits + 1):
            fk = k / (nuits + 0.6)
            if p >= fk:
                x, y = point(tot * fk)
                a = int(255 * min(1.0, (p - fk) * duree / 0.8))
                X, Y = x + 105, y - 9
                d.ellipse([X - 3, Y - 3, X + 3, Y + 3], fill=(250, 244, 214, a))
                d.ellipse([X - 1, Y - 4, X + 5, Y + 2], fill=(0, 0, 0, 0))
        x, y = point(dist)
        d.ellipse([x + 105 - 3, y - 3, x + 105 + 3, y + 3], fill=(255, 236, 170, 110))
        d.ellipse([x + 105 - 1, y - 1, x + 105 + 1, y + 1], fill=(255, 255, 236, 255))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ registre
_DEC = dict(maison_nil=maison_nil, maison_nil_jour=lambda: maison_nil("jour"), maison_nil_soir=lambda: maison_nil("soir"),
            maison_nil_aube=lambda: maison_nil("aube"),
            rive_maison=rive_maison, rive_maison_corde=lambda: rive_maison("aube", corde=True),
            rive_maison_jour=lambda: rive_maison("jour"), rive_maison_soir=lambda: rive_maison("soir"),
            ruelle_nuit=lambda: ruelle("nuit"), ruelle_nuit_eteinte=lambda: ruelle("nuit", eteinte=True),
            ruelle=ruelle, ruelle_aube=lambda: ruelle("aube"), ruelle_soir=lambda: ruelle("soir"),
            couloir_palais=couloir_palais, couloir_palais_nuit=lambda: couloir_palais("nuit"),
            chambre_asiya=chambre_asiya, chambre_asiya_nuit=lambda: chambre_asiya("nuit"),
            marche_egypte=marche_egypte, avenue_palais=avenue_palais, ville_midi=ville_midi,
            ville_matin=lambda: ville_midi("aube"),
            desert=desert, desert_nuit=lambda: desert("nuit"), desert_soir=lambda: desert("soir"),
            desert_aube=lambda: desert("aube"),
            porte_ville=porte_ville, porte_ville_nuit=lambda: porte_ville("nuit"),
            palais_ciel=palais_ciel, carte_madyan=carte_madyan)
egypte.enregistre(_DEC, sol_haut=dict(maison_nil=(330, 100), rive_maison=(330, 100), ruelle=(330, 100), ruelle_nuit=(330, 100),
                                      couloir_palais=(330, 100), chambre_asiya=(330, 100), marche_egypte=(330, 110),
                                      avenue_palais=(330, 110), ville_midi=(330, 104), ville_matin=(330, 104),
                                      desert=(330, 120), porte_ville=(330, 110), palais_ciel=(330, 100),
                                      carte_madyan=(330, 88)))
lieux.LUMIERES["maison_nil"] = (lieux.NUIT, [(156, 1092, 520, (255, 170, 90), 0.85)])
lieux.LUMIERES["maison_nil_soir"] = (lieux.SOIR, [(156, 1092, 420, (255, 170, 90), 0.6)])
lieux.LUMIERES["ruelle_nuit"] = (lieux.NUIT, [(540, 1232, 200, (255, 170, 90), 0.5)])
lieux.LUMIERES["ruelle_nuit_eteinte"] = (lieux.NUIT, [])
lieux.LUMIERES["chambre_asiya_nuit"] = (lieux.NUIT, [(88, 956, 360, (255, 190, 110), 0.6), (1200, 956, 360, (255, 190, 110), 0.6)])
lieux.LUMIERES["couloir_palais_nuit"] = (lieux.NUIT, [(-168, 1064, 360, (255, 170, 80), 0.6), (344, 1064, 360, (255, 170, 80), 0.6),
                                                      (856, 1064, 360, (255, 170, 80), 0.6), (1368, 1064, 360, (255, 170, 80), 0.6)])
lieux.LUMIERES["porte_ville"] = (lieux.SOIR, [(88, 928, 240, (255, 170, 80), 0.5), (392, 928, 240, (255, 170, 80), 0.5)])
lieux.LUMIERES["palais_ciel"] = (lieux.NUIT, [])
lieux.LUMIERES["carte_madyan"] = (lieux.JOUR, [])
