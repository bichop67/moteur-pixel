# DÉCORS DU FILM « MOUSSA » — parties 10 à 13 — 16:9, toile x = -105 … 375, y = 0 … 480 ; pieds à y = 330.
#   porte_palais (+ _ouverte _soir)  la grande porte du palais entre deux pylônes peints (motifs, jamais de figures),
#                                    obélisques, mâts à flammes ; _ouverte : les battants ouverts sur la cour lumineuse
#                                    ({devient porte_palais_ouverte 3})
#   esplanade_fete                   l'esplanade de la fête au bord du Nil : tentures, bannières, gradins pleins de monde,
#                                    l'estrade dorée de Pharaon à gauche (PHARAON place estrade, sur le trône)
#   tour_haman (+ _soir)             le chantier de la tour : fours à briques qui fument, la tour en échafaudages
#   cour_soleil                      une cour du palais écrasée de soleil (Asiya) ; sol blanc, ombre seulement sur les bords
# Animations : anim_rassemblement (carte : les magiciens arrivent de tout le pays), anim_duel (cordes et bâtons qui
# semblent ramper, puis le serpent du bâton de Moussa qui happe tout).
import math

import numpy as np

import lieux
import egypte
from lieux import dk, lt, mix, R, palmier, relief
from egypte import _Px, _ciel, CIELS, _colonne_lotus, _brasero, _eau
from decors_film import _T, _briques, _jarre, BRIQUE
from decors_film2 import _clip, _assombrit


# ================================================================ la grande porte du palais
def _pylone(c, x0, x1, y_bas, y_haut, pierre, rr):
    """Un pylône égyptien : tour trapézoïdale, corniche, bandes peintes et motifs géométriques (pas de figures)."""
    m = c.mask_poly([(x0, y_bas), (x1, y_bas), (x1 - 8, y_haut), (x0 + 8, y_haut)])
    c.shape(m, pierre, dk(pierre, 0.8), lt(pierre, 0.08), band=2)
    for y in range(y_haut + 14, y_bas, 9):                                 # assises de pierre
        c.fill(m & c.mask_rect(x0, y, x1, y), dk(pierre, 0.9))
    c.shape(c.mask_rect(x0 + 4, y_haut - 7, x1 - 4, y_haut), lt(pierre, 0.06), dk(pierre, 0.7), band=1)
    for k, col in enumerate(((40, 90, 160), (220, 170, 60), (190, 60, 40))):
        c.fill(m & c.mask_rect(x0, y_haut + 2 + k * 2, x1, y_haut + 2 + k * 2), col)
    cx = (x0 + x1) // 2
    pan = c.mask_rect(cx - 16, y_haut + 18, cx + 16, y_bas - 30)
    c.fill(pan, dk(pierre, 0.92))
    c.outline(pan, (220, 170, 60))
    for j, y in enumerate(range(y_haut + 26, y_bas - 34, 16)):           # losanges et lotus peints
        c.fill(c.mask_poly([(cx, y - 6), (cx + 9, y), (cx, y + 6), (cx - 9, y)]), ((40, 90, 160), (190, 60, 40))[j % 2])
        c.fill(c.mask_ell(cx, y, 2, 2), (220, 170, 60))


def porte_palais(heure="jour", ouverte=False):
    """La grande porte du palais : deux pylônes peints, une immense porte de cèdre à clous de bronze (fermée ; ouverte :
    la cour lumineuse derrière), deux obélisques, des mâts à flammes, un parvis dallé. Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 210, dict(aube=(320, 160), jour=(40, 30), soir=(330, 150), nuit=(300, 60))[heure], seed=301)
    snap = c.a.copy()
    rr = R(302)
    pierre = T((224, 198, 150))
    for k, x in enumerate(range(-100, 375, 26)):                            # palmiers derrière l'enceinte
        palmier(c, x + (k * 9) % 11, 236, h=30 + (k * 7) % 14, lean=(k % 3 - 1) * 4, seed=360 + k,
                col=T((64, 120, 66)), trunk=T((126, 94, 60)))
    enceinte = T((214, 190, 146))                                          # le mur d'enceinte du palais
    m_enc = c.mask_rect(-105, 226, 375, 306)
    c.shape(m_enc, enceinte, dk(enceinte, 0.82), lt(enceinte, 0.06), band=2)
    _briques(c, m_enc, enceinte, pas_y=7, pas_x=12, seed=4)
    for x in range(-105, 375, 10):
        c.shape(c.mask_rect(x, 220, x + 5, 226), enceinte, dk(enceinte, 0.8), band=1)
    c.fill(c.mask_rect(-105, 236, 375, 237), T((40, 90, 160)))
    for (x0, x1) in ((-20, 112), (158, 290)):
        _pylone(c, x0, x1, 306, 118, pierre, rr)
    for x in (-6, 98, 172, 276):                                            # mâts et flammes
        c.fill(c.mask_rect(x, 70, x + 1, 300), T((150, 112, 60)))
        col = ((40, 90, 160), (190, 60, 40), (220, 170, 60), (40, 90, 160))[(x // 7) % 4]
        c.fill(c.mask_poly([(x + 2, 72), (x + 20, 76), (x + 2, 82)]), T(col))
    # la porte
    porte = c.mask_rect(112, 176, 158, 306)
    c.shape(c.mask_rect(108, 168, 162, 176), lt(pierre, 0.06), dk(pierre, 0.7), band=1)
    if ouverte:
        c.vgrad(porte, 176, 306, (255, 246, 214), (236, 214, 170), steps=4)
        for x in range(116, 158, 10):                                       # colonnes de la cour, dans la lumière
            c.fill(c.mask_rect(x, 200, x + 3, 300), (226, 206, 168))
        c.shape(c.mask_poly([(112, 176), (120, 182), (120, 300), (112, 306)]), T((120, 76, 40)), T((84, 52, 28)), band=1)
        c.shape(c.mask_poly([(158, 176), (150, 182), (150, 300), (158, 306)]), T((120, 76, 40)), T((84, 52, 28)), band=1)
        c.glow(135, 250, 70, (255, 240, 200), 0.3)
    else:
        bois = T((120, 76, 40))
        c.shape(porte, bois, dk(bois, 0.7), lt(bois, 0.1), band=2)
        c.fill(c.mask_rect(134, 176, 135, 306), dk(bois, 0.55))
        for y in range(186, 300, 14):
            for x in range(118, 156, 8):
                c.fill(c.mask_rect(x, y, x + 1, y + 1), T((220, 180, 80)))
        c.fill(c.mask_rect(112, 236, 158, 239), T((176, 140, 70)))
    for (ox_, h_) in ((-80, 150), (338, 150)):                              # obélisques
        ob = c.mask_poly([(ox_ - 7, 306), (ox_ + 7, 306), (ox_ + 5, 306 - h_), (ox_, 306 - h_ - 10), (ox_ - 5, 306 - h_)])
        c.shape(ob, T((200, 176, 140)), T((150, 126, 96)), T((230, 210, 176)), band=2)
        c.fill(c.mask_poly([(ox_ + 5, 306 - h_), (ox_, 306 - h_ - 10), (ox_ - 5, 306 - h_)]), T((236, 200, 110)))
        for y in range(306 - h_ + 14, 296, 12):
            c.fill(c.mask_rect(ox_ - 2, y, ox_ + 2, y + 1), T((150, 126, 96)))
    sol = c.mask_rect(-105, 306, 375, 480)
    dalle = T((214, 192, 150))
    c.vgrad(sol, 306, 480, dalle, dk(dalle, 0.68), steps=6)
    for y in range(312, 480, 10):
        c.fill(sol & c.mask_rect(-105, y, 375, y), dk(dalle, 0.84))
    for x in range(-100, 375, 22):
        c.fill(sol & c.mask_rect(x, 306, x, 480), dk(dalle, 0.86))
    if heure == "jour":
        c.tint(c.mask_rect(-105, 0, 375, 480), (255, 246, 226), 0.08)
    return relief(c, snap, sky), None


# ================================================================ l'esplanade de la fête
PLACE_ESTRADE = (-140, 1066)                                                 # Pharaon sur son estrade (coordonnées du monde)


def esplanade_fete(heure="jour"):
    """L'esplanade de la fête, au bord du Nil, au matin : le fleuve et la rive d'en face au fond, des gradins couverts de
    monde sous des tentures rayées, des bannières, l'estrade dorée de Pharaon (dais) à gauche, le sable de l'arène au
    centre où se tient le duel. Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 190, dict(aube=(300, 150), jour=(90, 40), soir=(-30, 150), nuit=(300, 60))[heure], seed=311)
    snap = c.a.copy()
    rr = R(312)
    c.fill(c.mask_rect(-105, 182, 375, 190), T((118, 150, 84)))             # rive d'en face
    for k, x in enumerate(range(-100, 375, 24)):
        palmier(c, x + (k * 7) % 9, 186, h=16 + (k * 5) % 8, lean=(k % 3 - 1) * 3, seed=320 + k,
                col=T((64, 120, 66)), trunk=T((126, 94, 60)))
    eau = c.mask_rect(-105, 190, 375, 214)
    c.vgrad(eau, 190, 214, T((122, 178, 208)), T((80, 140, 176)), steps=3)
    for _ in range(60):
        x, y = rr.randint(-100, 370), rr.randint(192, 212)
        c.fill(c.mask_rect(x, y, x + rr.randint(2, 6), y), T((180, 214, 230)))
    # gradins couverts de monde, sous des tentures
    for i, x0 in enumerate(range(-105, 375, 80)):
        cols = ((200, 60, 50), (240, 230, 210)) if i % 2 else ((50, 90, 160), (240, 230, 210))
        toile = c.mask_poly([(x0, 206), (x0 + 80, 206), (x0 + 84, 220), (x0 - 4, 220)])
        c.fill(toile, T(cols[0]))
        for xx in range(x0 - 4, x0 + 84, 8):
            c.fill(toile & c.mask_rect(xx, 206, xx + 3, 220), T(cols[1]))
        c.outline(toile, (60, 40, 30))
        for px_ in (x0, x0 + 78):
            c.fill(c.mask_rect(px_, 220, px_ + 1, 262), T((120, 90, 56)))
    gradins = c.mask_rect(-105, 222, 375, 266)
    c.fill(gradins, T((150, 120, 84)))
    barriere = c.mask_rect(-105, 266, 375, 290)                             # muret de bois devant les gradins
    c.shape(barriere, T((150, 110, 66)), T((110, 80, 50)), T((180, 140, 90)), band=2)
    for x in range(-100, 375, 12):
        c.fill(barriere & c.mask_rect(x, 266, x, 290), T((120, 88, 52)))
    c.fill(c.mask_rect(-105, 272, 375, 273), T((190, 60, 50)))
    for y in range(226, 266, 8):                                            # rangées de spectateurs (têtes, habits)
        c.fill(c.mask_rect(-105, y + 6, 375, y + 7), T((120, 92, 64)))
        for x in range(-104, 375, 4):
            habit = rr.choice(((236, 228, 206), (210, 196, 160), (150, 118, 82), (60, 84, 140), (170, 70, 60), (226, 200, 150)))
            peau = rr.choice(((198, 150, 110), (170, 122, 86), (120, 84, 60), (220, 176, 136)))
            c.fill(c.mask_rect(x, y + 3, x + 2, y + 5), T(habit))
            c.fill(c.mask_rect(x + 1, y + 1, x + 1, y + 2), T(peau))
    for x in range(-100, 375, 46):                                          # bannières
        c.fill(c.mask_rect(x, 150, x, 206), T((150, 112, 60)))
        c.fill(c.mask_poly([(x + 1, 152), (x + 14, 156), (x + 1, 164)]), T(((40, 90, 160), (190, 60, 40), (220, 170, 60))[(x // 46) % 3]))
    # l'estrade de Pharaon (gauche)
    or_ = T((226, 182, 82))
    est = c.mask_rect(-90, 266, 20, 288)
    c.shape(est, or_, dk(or_, 0.72), lt(or_, 0.12), band=2)
    for x in range(-86, 20, 10):
        c.fill(c.mask_rect(x, 270, x + 4, 284), dk(or_, 0.86))
    c.shape(c.mask_rect(-96, 286, 26, 292), dk(or_, 0.85), dk(or_, 0.6), band=1)
    for x in (-84, 14):                                                     # le dais
        c.fill(c.mask_rect(x, 214, x + 2, 266), or_)
    c.shape(c.mask_poly([(-90, 214), (20, 214), (26, 222), (-96, 222)]), T((40, 90, 160)), T((28, 60, 110)), band=1)
    for x in range(-94, 26, 6):
        c.fill(c.mask_rect(x, 222, x + 2, 226), or_)
    sol = c.mask_rect(-105, 288, 375, 480)
    sable = T((220, 192, 140))
    c.vgrad(sol, 288, 480, lt(sable, 0.06), dk(sable, 0.72), steps=6)
    c.fill(c.mask_rect(-105, 288, 375, 291), dk(sable, 0.82))
    for _ in range(80):
        x, y = rr.randint(-100, 370), rr.randint(294, 470)
        c.fill(c.mask_ell(x, y, 1.6, 1), lt(sable, 0.1))
    for y0_, kk in ((420, 0.10), (440, 0.18), (460, 0.26)):
        c.tint(c.mask_rect(-105, y0_, 375, 480), (40, 24, 20), kk)
    return relief(c, snap, sky), None


# ================================================================ le chantier de la tour de Haman
def tour_haman(heure="jour"):
    """Le chantier de la tour : la tour carrée qui monte vers le ciel (vue d'en bas), ses échafaudages et ses rampes,
    des fours à briques qui fument à gauche, des tas d'argile, des briques cuites empilées. Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 300, dict(aube=(320, 220), jour=(300, 50), soir=(-40, 220), nuit=(300, 60))[heure], seed=331)
    snap = c.a.copy()
    rr = R(332)
    brique = T((176, 96, 66))
    tour = c.mask_poly([(120, 306), (250, 306), (236, 20), (134, 20)])     # la tour, très haute (contre-plongée)
    c.shape(tour, brique, dk(brique, 0.74), lt(brique, 0.08), band=3)
    _briques(c, tour, brique, pas_y=5, pas_x=9, seed=9)
    for y in range(40, 300, 46):                                            # étages et rampes
        c.shape(c.mask_poly([(122 + (306 - y) * 0.05, y), (248 - (306 - y) * 0.05, y), (248 - (306 - y) * 0.05, y + 4),
                             (122 + (306 - y) * 0.05, y + 4)]), dk(brique, 0.85), dk(brique, 0.6), band=1)
    bois = T((130, 96, 56))
    for x in (110, 130, 240, 260):                                          # échafaudages
        c.fill(c.mask_rect(x, 40, x + 1, 306), bois)
    for y in range(50, 306, 20):
        c.fill(c.mask_rect(108, y, 134, y), bois)
        c.fill(c.mask_rect(236, y, 262, y), bois)
        c.line(110, y, 130, y + 20, bois)
        c.line(260, y, 240, y + 20, bois)
    c.fill(c.mask_poly([(250, 306), (320, 306), (250, 230)]), dk(brique, 0.8))   # rampe de terre
    for (fx, fy) in ((-70, 306), (0, 306)):                                 # fours à briques
        four = c.mask_ell(fx, fy - 16, 26, 22) & c.mask_rect(fx - 26, fy - 38, fx + 26, fy)
        c.shape(four, T((150, 110, 80)), T((100, 72, 52)), T((180, 140, 100)), band=2)
        c.fill(c.mask_arch(fx - 8, fx + 8, fy - 16, fy), (40, 20, 16))
        c.fill(c.mask_ell(fx, fy - 4, 6, 6), (255, 150, 60))
        c.glow(fx, fy - 6, 30, (255, 150, 60), 0.35)
        for k in range(5):                                                  # fumée
            c.tint(c.mask_ell(fx + k * 6 - 4, fy - 46 - k * 16, 10 + k * 3, 7 + k * 2), (110, 104, 104), 0.35 - k * 0.05)
    for (px_, py_) in ((290, 300), (330, 304), (-30, 312)):                 # tas d'argile, briques empilées
        c.shape(c.mask_ell(px_, py_, 16, 7) & c.mask_rect(px_ - 16, py_ - 7, px_ + 16, py_ + 1), T((150, 110, 76)), T((110, 80, 54)), band=1)
    for j in range(4):
        c.shape(c.mask_rect(40 + j * 2, 298 - j * 4, 70 - j * 2, 302 - j * 4), brique, dk(brique, 0.7), band=1)
    sol = c.mask_rect(-105, 306, 375, 480)
    terre = T((190, 150, 106))
    c.vgrad(sol, 306, 480, lt(terre, 0.05), dk(terre, 0.7), steps=6)
    for _ in range(70):
        x, y = rr.randint(-100, 370), rr.randint(310, 470)
        c.fill(c.mask_ell(x, y, rr.randint(1, 3), 1), dk(terre, 0.86))
    for y0_, kk in ((420, 0.10), (440, 0.18), (460, 0.26)):
        c.tint(c.mask_rect(-105, y0_, 375, 480), (40, 24, 20), kk)
    return relief(c, snap, sky), None


# ================================================================ la cour du palais en plein soleil
def cour_soleil():
    """Une cour du palais écrasée de soleil : dallage blanc éblouissant, hauts murs ocre, une colonnade dont l'ombre
    reste sur les bords ; au centre, rien pour s'abriter. (Asiya : rien de violent n'est montré.) Pieds y = 330."""
    c = _Px()
    sky = _ciel(c, "jour", 150, (135, 24), seed=341)
    c.tint(sky, (255, 250, 236), 0.35)
    snap = c.a.copy()
    mur = (226, 200, 156)
    c.shape(c.mask_rect(-105, 120, 375, 300), mur, dk(mur, 0.84), lt(mur, 0.06), band=2)
    for y0_, col in ((126, (40, 90, 160)), (129, (220, 170, 60))):
        c.fill(c.mask_rect(-105, y0_, 375, y0_ + 1), col)
    for x in range(-90, 375, 52):                                           # colonnade (ombre seulement sur les bords)
        _colonne_lotus(c, x, 150, 300, 14, (236, 214, 176))
    c.fill(c.mask_rect(-105, 300, 375, 306), dk(mur, 0.7))
    sol = c.mask_rect(-105, 306, 375, 480)
    c.vgrad(sol, 306, 480, (250, 240, 220), (214, 196, 166), steps=6)
    for y in range(312, 480, 12):
        c.fill(sol & c.mask_rect(-105, y, 375, y), (224, 210, 180))
    c.tint(c.mask_poly([(-105, 306), (-40, 306), (-70, 480), (-105, 480)]), (90, 70, 60), 0.25)
    c.tint(c.mask_poly([(310, 306), (375, 306), (375, 480), (340, 480)]), (90, 70, 60), 0.25)
    c.tint(c.mask_rect(-105, 0, 375, 480), (255, 248, 230), 0.14)          # chaleur blanche
    c.glow(135, 40, 160, (255, 252, 230), 0.25)
    return relief(c, snap, sky), None


# ================================================================ animations
VILLES = [(18, 470), (-60, 300), (-90, 150), (60, 112), (-20, 112), (110, 240), (24, 420)]


def anim_rassemblement(t_debut=0.5, duree=6.0, cible=(29, 201), villes=VILLES):
    """Sur la carte : de petites lumières partent des villes d'Égypte et convergent vers la capitale (les magiciens)."""
    from PIL import Image, ImageDraw

    def f(img, u):
        p = max(0.0, min(1.0, (u - t_debut) / max(0.1, duree)))
        if p <= 0:
            return
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for i, (vx, vy) in enumerate(villes):
            q = max(0.0, min(1.0, p * 1.25 - i * 0.04))
            e = q * q * (3 - 2 * q)
            x, y = vx + (cible[0] - vx) * e + 105, vy + (cible[1] - vy) * e
            for k in range(1, 6):                                           # traînée
                e2 = max(0.0, e - k * 0.03)
                tx, ty = vx + (cible[0] - vx) * e2 + 105, vy + (cible[1] - vy) * e2
                d.rectangle([tx, ty, tx + 1, ty + 1], fill=(255, 214, 120, 200 - k * 35))
            d.ellipse([x - 2.5, y - 2.5, x + 2.5, y + 2.5], fill=(255, 236, 170, 140))
            d.rectangle([x - 0.5, y - 0.5, x + 0.5, y + 0.5], fill=(255, 255, 240, 255))
        lieux.pose_calque(img, lay)
    return f


def anim_duel(cles, y_sol=318, cordes=(150, 176, 198, 222, 246, 268, 290, 160, 210, 256), x_depart=60, x_fin=330):
    """Le duel du jour de la fête. `cles` = [(u, quoi)] rempli par {duel quoi} :
    cordes (les magiciens jettent : cordes et bâtons qui semblent ramper), jette (le bâton de Moussa devient un serpent
    immense, à x_depart), happe (le serpent file vers la droite et happe chaque corde au passage), fin (il redevient
    bâton). Les cordes tracées en pixels du décor ; le serpent comme dans anim_serpent."""
    from PIL import Image, ImageDraw
    rnd = R(7)
    cordes = [(x, y_sol - (i % 3) * 5, rnd.uniform(0, 6.28), i % 2) for i, x in enumerate(cordes)]

    def t_de(q):
        return next((t for t, k in sorted(cles) if k == q), None)

    def f(img, u):
        t_c, t_j, t_h, t_f = t_de("cordes"), t_de("jette"), t_de("happe"), t_de("fin")
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d_ = ImageDraw.Draw(lay)
        tete = None
        if t_j is not None and u >= t_j and (t_f is None or u < t_f + 0.5):
            if t_h is None or u < t_h:
                hx = x_depart
            else:
                e = min(1.0, (u - t_h) / 3.0)
                hx = x_depart + (x_fin - x_depart) * e * e * (3 - 2 * e)
            a = min(1.0, (u - t_j) / 0.4) * (1.0 if t_f is None or u < t_f else max(0.0, 1 - (u - t_f) / 0.5))
            tete = (hx, a)
        if t_c is not None and u >= t_c:                                    # les cordes qui semblent ramper
            a_c = min(1.0, (u - t_c) / 0.5)
            for (x, y, ph, baton) in cordes:
                if tete is not None and t_h is not None and u >= t_h and tete[0] >= x:
                    continue                                                 # happée
                for j in range(18):
                    s_ = j * 1.3
                    px_ = x - 11 + s_ + 105
                    py_ = y + (2.2 if not baton else 1.0) * math.sin(s_ / 3.2 + u * 7.0 + ph)
                    col_ = (176, 140, 90) if not baton else (120, 86, 52)
                    d_.rectangle([px_ - 0.5, py_ - 1, px_ + 1.5, py_ + 1], fill=(40, 30, 20, int(255 * a_c)))
                    d_.rectangle([px_, py_ - 0.5, px_ + 1, py_ + 0.5], fill=col_ + (int(255 * a_c),))
        if tete is not None:                                                 # le serpent du bâton de Moussa
            hx, a = tete
            al = int(255 * a)
            n = 46
            for i in range(n, -1, -1):
                s_ = i * 1.9
                px_ = hx - s_ + 105
                py_ = y_sol - 3 + 2.8 * math.sin(s_ / 6.0 - u * 9.0) * min(1.0, i / 4)
                r = 4.6 * (1 - 0.6 * i / n)
                d_.ellipse([px_ - r - 1, py_ - r - 1, px_ + r + 1, py_ + r + 1], fill=(30, 40, 24, al))
                d_.ellipse([px_ - r, py_ - r, px_ + r, py_ + r], fill=(118, 150, 64, al))
                if i % 3 == 0:
                    d_.ellipse([px_ - r * 0.6, py_ - r, px_ + r * 0.6, py_ - r * 0.2], fill=(70, 96, 40, al))
            X = hx + 105
            d_.ellipse([X - 7, y_sol - 10, X + 7, y_sol + 1], fill=(30, 40, 24, al))
            d_.ellipse([X - 6, y_sol - 9, X + 6, y_sol], fill=(128, 160, 70, al))
            d_.point((X + 3, y_sol - 7), fill=(250, 214, 80, al))
            if int(u * 6) % 2 == 0:
                d_.line([(X + 6, y_sol - 4), (X + 10, y_sol - 4)], fill=(210, 50, 50, al))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ registre
_DEC = dict(porte_palais=porte_palais, porte_palais_ouverte=lambda: porte_palais("jour", ouverte=True),
            porte_palais_soir=lambda: porte_palais("soir"),
            esplanade_fete=esplanade_fete, tour_haman=tour_haman, tour_haman_soir=lambda: tour_haman("soir"),
            cour_soleil=cour_soleil)
egypte.enregistre(_DEC, sol_haut=dict(porte_palais=(330, 100), esplanade_fete=(330, 104), tour_haman=(330, 96),
                                      cour_soleil=(330, 100)),
                  places=dict(esplanade_fete=dict(estrade=PLACE_ESTRADE)))
lieux.LUMIERES["porte_palais"] = (lieux.JOUR, [])
lieux.LUMIERES["porte_palais_ouverte"] = (lieux.JOUR, [])
lieux.LUMIERES["cour_soleil"] = (lieux.JOUR, [])
