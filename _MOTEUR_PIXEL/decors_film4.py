# DÉCORS DU FILM « MOUSSA » — parties 14 à 17 — 16:9, toile x = -105 … 375, y = 0 … 480 ; pieds à y = 330.
#   champs_nil (+ _secs _inondes)   les champs d'Égypte au bord du Nil : verts ; desséchés et craquelés ; noyés sous l'eau
#   grenier                         un grenier égyptien : silos de terre, tas de blé, sacs, jarres (les petites bêtes)
#   nil_sang                        le Nil (même décor que nil) dont l'eau est devenue rouge sombre ({devient nil_sang 4})
#   terrasse_nuit                   une terrasse au bord du Nil, la nuit étoilée ; au loin le palais illuminé de Pharaon
#   rivage_mer (+ _aube)            le rivage : la mer immense à droite, la plage, des rochers ; (la poursuite, l'armée)
#   mer_ouverte                     la mer ouverte : des chemins secs entre de hautes murailles d'eau ({devient mer_ouverte 4})
#   village_idoles                  un village où l'on se prosterne devant des statues (idoles, sans visage)
#   camp_desert (+ _nuit)           le camp des fils d'Israël au pied de la montagne : tentes, feux, troupeaux
#   montagne_sinai (+ _nuit)        sur la montagne : une crête, le ciel immense, un mont voisin ; _effondre : le mont n'est
#                                   plus que poussière ({devient montagne_sinai_effondre 2.5})
# Animations : anim_sauterelles, anim_betes (dans le blé), anim_grenouilles, anim_poussiere_armee (cavaliers au loin),
# anim_vagues (l'eau devant les persos : Pharaon dans les flots).
import math

import numpy as np

import lieux
import egypte
from lieux import dk, lt, mix, R, palmier, relief
from egypte import _Px, _ciel, CIELS, _colonne_lotus, _roseaux, _papyrus
from decors_film import _T, _briques, _porte, _fenetre, _jarre, BRIQUE
from decors_film2 import _clip, _assombrit, EAU, RIVE, PALME


# ================================================================ les champs d'Égypte
def champs_nil(heure="jour", etat="vert"):
    """Les champs au bord du Nil : canaux d'irrigation, parcelles, palmiers, une petite maison de paysan, le fleuve au
    fond. etat = vert (blé), secs (terre craquelée, arbres sans fruits, ciel blanc), inondes (l'eau couvre tout, la pluie
    tombe : option « pluie »). Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 220, dict(aube=(320, 180), jour=(70, 40), soir=(-30, 180), nuit=(300, 60))[heure], seed=401)
    if etat == "secs":
        c.tint(sky, (250, 240, 214), 0.45)
    elif etat == "inondes":
        c.tint(sky, (110, 116, 130), 0.6)
    snap = c.a.copy()
    rr = R(402)
    c.fill(c.mask_rect(-105, 210, 375, 220), T((118, 150, 84)) if etat != "secs" else T((176, 160, 110)))
    eh, eb = EAU["jour"]
    c.vgrad(c.mask_rect(-105, 220, 375, 232), 220, 232, T(eh), T(eb), steps=3)
    for k, x in enumerate(range(-100, 375, 30)):
        palmier(c, x + (k * 11) % 13, 218, h=18 + (k * 5) % 9, lean=(k % 3 - 1) * 3, seed=410 + k,
                col=T((64, 120, 66)) if etat != "secs" else T((150, 140, 90)), trunk=T((126, 94, 60)))
    sol = c.mask_rect(-105, 232, 375, 480)
    if etat == "vert":
        c.vgrad(sol, 232, 480, T((150, 176, 86)), T((96, 120, 56)), steps=6)
        for y in range(240, 480, 9):                                         # rangs de blé
            c.fill(sol & c.mask_rect(-105, y, 375, y), T((176, 196, 100)))
        for _ in range(260):
            x, y = rr.randint(-100, 370), rr.randint(236, 470)
            c.px(x, y, T((206, 200, 110)))
    elif etat == "secs":
        terre = T((206, 176, 128))
        c.vgrad(sol, 232, 480, lt(terre, 0.05), dk(terre, 0.7), steps=6)
        for _ in range(140):                                                 # craquelures
            x, y = rr.randint(-100, 370), rr.randint(236, 470)
            for j in range(rr.randint(3, 9)):
                x += rr.choice((-1, 0, 1, 1))
                y += rr.choice((0, 1))
                c.px(x, y, dk(terre, 0.62))
    else:
        c.vgrad(sol, 232, 480, T((120, 150, 150)), T((70, 96, 110)), steps=6)
        for _ in range(140):
            x, y = rr.randint(-100, 370), rr.randint(236, 470)
            c.fill(c.mask_rect(x, y, x + rr.randint(2, 7), y), T((170, 200, 210)))
        for x in range(-100, 375, 17):                                       # pointes de blé noyées
            c.fill(c.mask_rect(x, 250 + (x * 7) % 60, x, 254 + (x * 7) % 60), T((120, 140, 80)))
    for (cx_, y0_) in ((-60, 250), (120, 262), (260, 248)):                 # canaux d'irrigation
        c.fill(c.mask_poly([(cx_ - 2, y0_), (cx_ + 2, y0_), (cx_ + 40, 480), (cx_ + 30, 480)]),
               T((90, 140, 170)) if etat != "secs" else dk(T((206, 176, 128)), 0.8))
    maison = c.mask_rect(250, 226, 300, 262)                                 # maison de paysan
    mur = T(BRIQUE[2])
    c.shape(maison, mur, dk(mur, 0.8), band=1)
    _porte(c, 268, 280, 244, 262, heure == "nuit", ouverte=False)
    if etat == "secs":                                                       # arbre sans fruits, branches nues
        tx, ty = -40, 300
        c.fill(c.mask_rect(tx - 2, ty - 40, tx + 2, ty), T((110, 84, 60)))
        for (bx, by) in ((-18, -60), (16, -58), (-10, -70), (10, -66), (0, -76)):
            c.line(tx, ty - 34, tx + bx, ty + by, T((110, 84, 60)))
    if etat == "inondes":
        c.tint(c.mask_rect(-105, 0, 375, 480), (90, 100, 120), 0.2)
    for y0_, kk in ((420, 0.10), (440, 0.18), (460, 0.26)):
        c.tint(c.mask_rect(-105, y0_, 375, 480), (30, 24, 20), kk)
    return relief(c, snap, sky), None


# ================================================================ le grenier
def grenier():
    """Un grenier égyptien : silos de terre en coupole, tas de blé doré, sacs, jarres, une lucarne qui éclaire la
    poussière ; (les petites bêtes qui rongent le blé : animation « betes »). Pieds y = 330."""
    c = _Px()
    mur = (196, 160, 116)
    c.vgrad(c.mask_rect(-105, 0, 375, 306), 100, 306, dk(mur, 0.7), mur, steps=6)
    c.fill(c.mask_rect(-105, 0, 375, 104), (104, 80, 54))
    for x in range(-105, 375, 4):
        c.fill(c.mask_rect(x, 0, x + 1, 104), (118, 92, 62))
    c.shape(c.mask_rect(-105, 104, 375, 110), (90, 64, 40), (66, 46, 28), band=1)
    for (sx, w, h) in ((-60, 40, 120), (40, 46, 136), (150, 40, 116)):     # silos en coupole
        silo = c.mask_rect(sx - w // 2, 306 - h + w // 2, sx + w // 2, 306) | c.mask_ell(sx, 306 - h + w // 2, w // 2, w // 2)
        c.shape(silo, (176, 140, 98), (130, 100, 70), (204, 170, 124), band=2)
        c.fill(c.mask_rect(sx - 6, 270, sx + 6, 290), (60, 44, 34))
        c.fill(c.mask_poly([(sx - 10, 306), (sx + 10, 306), (sx + 6, 292), (sx - 6, 292)]), (220, 190, 110))
    lu = c.mask_rect(240, 130, 270, 160)                                     # lucarne et rayon de poussière
    c.fill(lu, (255, 240, 200))
    c.tint(c.mask_poly([(240, 160), (270, 160), (330, 330), (280, 330)]), (255, 236, 190), 0.18)
    sol = c.mask_rect(-105, 306, 375, 480)
    c.vgrad(sol, 306, 480, (170, 136, 98), (96, 74, 54), steps=6)
    for (hx, w, h) in ((240, 60, 22), (330, 40, 16), (-20, 36, 12)):        # tas de blé
        tas = c.mask_ell(hx, 318, w // 2, h) & c.mask_rect(hx - w // 2, 318 - h, hx + w // 2, 320)
        c.shape(tas, (226, 196, 110), (190, 156, 80), (246, 222, 140), band=2)
    for (bx, by) in ((300, 300), (318, 304), (-90, 306)):                    # sacs
        c.shape(c.mask_ell(bx, by, 9, 11), (200, 180, 140), (160, 140, 100), band=1)
        c.fill(c.mask_rect(bx - 3, by - 13, bx + 3, by - 10), (150, 120, 80))
    for (jx, col) in ((190, (170, 104, 66)), (204, (150, 92, 60))):
        _jarre(c, jx, 312, col, h=9)
    return c, None


# ================================================================ le Nil devenu sang
def nil_sang():
    """Le décor « nil » (le fleuve, la maison au bord de l'eau) dont l'eau est devenue rouge sombre."""
    bg, fg = egypte.nil("jour")
    a = bg.a.astype(np.float32)
    b, g, r_ = a[..., 2], a[..., 1], a[..., 0]
    lignes = np.arange(a.shape[0])[:, None]
    eau = (b > r_ + 18) & (b > g - 10) & (lignes >= 246) & (lignes <= 324)    # pixels « bleus » du fleuve (pas le ciel)
    rouge = np.stack([np.clip(70 + 0.55 * b, 0, 255), 0.18 * g + 10, 0.18 * b + 12], axis=-1)
    a[eau] = rouge[eau]
    bg.a = a.astype(np.uint8)
    return bg, fg


# ================================================================ la terrasse au bord du Nil, la nuit
def terrasse_nuit():
    """Une terrasse de pierre au bord du Nil, la nuit : ciel étoilé immense, le fleuve qui reflète la lune, et au loin,
    sur l'autre rive, le palais illuminé de Pharaon (fenêtres et braseros) ; un parapet et deux jarres. Pieds y = 330."""
    c = _Px()
    c.vgrad(c.mask_rect(-105, 0, 375, 250), 0, 250, (8, 10, 30), (36, 44, 86), steps=8)
    rr = R(431)
    for _ in range(320):
        c.px(rr.randint(-105, 374), rr.randint(0, 236), (236, 236, 255) if rr.random() < 0.25 else (150, 156, 210))
    c.fill(c.mask_ell(300, 70, 8, 8) & ~c.mask_ell(304, 67, 7, 7), (248, 240, 212))
    c.glow(300, 70, 40, (190, 196, 255), 0.18)
    sil = (20, 22, 46)
    for (x0, x1) in ((40, 76), (150, 186)):                                   # le palais au loin, illuminé
        c.fill(c.mask_poly([(x0, 250), (x1, 250), (x1 - 4, 196), (x0 + 4, 196)]), sil)
    c.fill(c.mask_rect(76, 214, 150, 250), sil)
    c.fill(c.mask_rect(-20, 232, 260, 250), sil)
    for _ in range(26):
        x, y = rr.randint(-10, 250), rr.randint(204, 246)
        if rr.random() < 0.7:
            c.fill(c.mask_rect(x, y, x + 1, y + 1), (255, 200, 110))
    for x in (60, 170):
        c.glow(x, 196, 20, (255, 170, 80), 0.4)
    c.fill(c.mask_rect(-105, 250, 375, 300), (14, 18, 42))                    # le Nil
    for _ in range(80):
        x, y = rr.randint(-100, 370), rr.randint(252, 298)
        c.fill(c.mask_rect(x, y, x + rr.randint(1, 4), y), (60, 70, 120))
    for y in range(254, 298, 3):
        c.fill(c.mask_rect(300 - (y - 250) // 6, y, 300 + (y - 250) // 6, y), (190, 196, 236))
    for _ in range(40):                                                       # reflets du palais
        x, y = rr.randint(-10, 250), rr.randint(252, 280)
        c.px(x, y, (200, 150, 90))
    pierre = (120, 104, 96)
    c.shape(c.mask_rect(-105, 292, 375, 306), pierre, dk(pierre, 0.7), lt(pierre, 0.1), band=1)   # parapet
    for x in range(-100, 375, 18):
        c.fill(c.mask_rect(x, 292, x, 306), dk(pierre, 0.75))
    sol = c.mask_rect(-105, 306, 375, 480)
    c.vgrad(sol, 306, 480, (96, 84, 80), (40, 36, 40), steps=6)
    for y in range(312, 480, 12):
        c.fill(sol & c.mask_rect(-105, y, 375, y), (70, 62, 62))
    for (jx, col) in ((-70, (120, 80, 60)), (-56, (100, 70, 54))):
        _jarre(c, jx, 312, col, h=9)
    return c, None


# ================================================================ animations des fléaux
def anim_sauterelles(t_debut=0.3, n=260, seed=11, duree_arrivee=3.0):
    """Une nuée de sauterelles qui arrive par la droite et envahit tout le ciel et les champs (vols en tourbillons)."""
    from PIL import Image, ImageDraw
    rnd = R(seed)
    P = [(rnd.uniform(-105, 375), rnd.uniform(60, 330), rnd.uniform(0, 6.28), rnd.uniform(0.6, 1.4), rnd.random()) for _ in range(n)]

    def f(img, u):
        if u < t_debut:
            return
        k = min(1.0, (u - t_debut) / duree_arrivee)
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        front = 375 - k * 520                                                 # le front de la nuée avance vers la gauche
        for (x, y, ph, v, z) in P:
            if x < front:
                continue
            xx = x + 9 * math.sin(u * 2.2 * v + ph) + 105
            yy = y + 5 * math.sin(u * 3.1 * v + ph * 1.3)
            col = (120, 100, 50, 230) if z < 0.5 else (92, 110, 50, 230)
            ail = int(u * 14 + ph * 3) % 2
            d.rectangle([xx, yy, xx + 1 + ail, yy], fill=col)
        lieux.pose_calque(img, lay)
    return f


def anim_betes(t_debut=0.3, n=90, seed=13, zone=(-90, 300, 360, 340)):
    """De petites bêtes noires qui grouillent sur le blé et sur le sol (le blé rongé jusque dans les greniers)."""
    from PIL import Image, ImageDraw
    rnd = R(seed)
    x0, y0, x1, y1 = zone
    P = [(rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(0, 6.28), rnd.uniform(0.5, 1.5)) for _ in range(n)]

    def f(img, u):
        if u < t_debut:
            return
        k = min(1.0, (u - t_debut) / 2.5)
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for i, (x, y, ph, v) in enumerate(P):
            if i > n * k:
                break
            xx = x + 6 * math.sin(u * 1.4 * v + ph) + 105
            yy = y + 2 * math.sin(u * 2.3 * v + ph)
            d.point((xx, yy), fill=(30, 24, 20, 255))
            d.point((xx + 1, yy), fill=(50, 40, 30, 255))
        lieux.pose_calque(img, lay)
    return f


def anim_grenouilles(t_debut=0.3, n=46, seed=17, zone=(-95, 296, 365, 350)):
    """Des grenouilles partout, qui sautent : elles arrivent peu à peu, puis grouillent sur le sol et sur le lit."""
    from PIL import Image, ImageDraw
    rnd = R(seed)
    x0, y0, x1, y1 = zone
    P = [(rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(0, 6.28), rnd.uniform(0.6, 1.3)) for _ in range(n)]

    def f(img, u):
        if u < t_debut:
            return
        k = min(1.0, (u - t_debut) / 3.0)
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for i, (x, y, ph, v) in enumerate(P):
            if i > n * k:
                break
            cyc = (u * 0.8 * v + ph) % 1.0
            saut = math.sin(min(1.0, cyc / 0.3) * math.pi) * 5 if cyc < 0.3 else 0.0
            xx = x + 105 + 3 * math.sin(ph + int(u * 0.8 * v + ph))
            yy = y - saut
            d.ellipse([xx - 2, yy - 2, xx + 2, yy + 1], fill=(30, 50, 26, 255))
            d.ellipse([xx - 1.5, yy - 1.5, xx + 1.5, yy + 0.5], fill=(90, 140, 60, 255))
            d.point((xx - 1, yy - 2), fill=(230, 220, 120, 255))
            d.point((xx + 1, yy - 2), fill=(230, 220, 120, 255))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ la mer : le rivage, la mer ouverte
RIVAGE = [(30, 200), (120, 262), (214, 330), (262, 400), (300, 480)]          # la ligne du rivage (sable à gauche, mer à droite)


def rivage_mer(heure="aube"):
    """Le rivage : à droite la mer immense jusqu'à l'horizon (vagues, écume le long du bord), à gauche la plage et, au
    loin, les montagnes du désert d'où vient l'armée ; des rochers. Pieds y = 330 sur le sable (x < 860 environ)."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 200, dict(aube=(300, 170), jour=(260, 50), soir=(-30, 170), nuit=(280, 60))[heure], seed=451)
    snap = c.a.copy()
    rr = R(452)
    loin = mix(T((150, 120, 100)), CIELS[heure][1], 0.5)
    c.fill(c.mask_poly([(-105, 200), (-105, 176), (-60, 168), (-20, 180), (20, 172), (60, 190), (80, 200)]), loin)
    eh, eb = EAU[heure]
    mer = c.mask_rect(-105, 200, 375, 480) & ~c.mask_poly([(-105, 200)] + RIVAGE + [(-105, 480)])
    c.vgrad(mer, 200, 480, T(lt(eh, 0.05)), T(dk(eb, 0.85)), steps=6)
    for _ in range(260):
        x, y = rr.randint(-100, 374), rr.randint(202, 476)
        if mer[y, x + 105]:
            w_ = 2 + (y - 200) // 30
            c.fill(c.mask_rect(x, y, x + w_, y), T(lt(eh, 0.3)))
    if heure != "jour":
        sx = 300
        for y in range(204, 360, 3):
            w_ = 1 + (y - 200) // 10
            c.fill(mer & c.mask_rect(sx - w_, y, sx + w_, y), (255, 214, 160))
    sable = T((214, 188, 140))
    plage = c.mask_poly([(-105, 200)] + RIVAGE + [(-105, 480)])
    c.vgrad(plage, 200, 480, lt(sable, 0.05), dk(sable, 0.72), steps=6)
    for _ in range(90):
        x, y = rr.randint(-100, 300), rr.randint(204, 470)
        if plage[y, x + 105]:
            c.fill(c.mask_ell(x, y, 1.6, 1), lt(sable, 0.1) if rr.random() < 0.5 else dk(sable, 0.9))
    c.fill(plage & ~c.mask_poly([(-105, 200)] + [(x - 4, y) for x, y in RIVAGE] + [(-105, 480)]), dk(sable, 0.85))
    for k, (xa, ya) in enumerate(RIVAGE[:-1]):
        xb, yb = RIVAGE[k + 1]
        for t in np.linspace(0, 1, 40):
            x, y = xa + (xb - xa) * t, ya + (yb - ya) * t
            c.fill(c.mask_rect(x + 1, y, x + 4, y), (240, 244, 246))
    for (rx_, ry_, w, h) in ((-80, 300, 18, 10), (60, 296, 10, 6), (-20, 360, 14, 8)):
        r_ = c.mask_ell(rx_, ry_, w, h) & c.mask_rect(rx_ - w, ry_ - h, rx_ + w, ry_ + 2)
        c.shape(r_, T((150, 128, 110)), T((104, 88, 76)), T((186, 166, 146)), band=2)
    return relief(c, snap, sky), None


def mer_ouverte():
    """La mer ouverte : un chemin de sable sec, mouillé par endroits, file entre deux murailles d'eau immenses (bleu
    profond en bas, vert d'eau en haut, écume au sommet, quelques poissons) ; dans les murailles, des ouvertures laissent
    voir les chemins voisins (douze chemins, un par tribu). Le ciel n'est plus qu'une bande au-dessus. Pieds y = 330."""
    c = _Px()
    _ciel(c, "aube", 200, (135, 150), seed=461)
    rr = R(462)
    vp = (135, 196)
    sol = c.mask_poly([(vp[0] - 8, vp[1]), (vp[0] + 8, vp[1]), (330, 480), (-60, 480)])
    c.vgrad(sol, vp[1], 480, (196, 176, 136), (150, 128, 96), steps=6)
    for _ in range(120):
        x, y = rr.randint(-60, 330), rr.randint(200, 476)
        if sol[y, x + 105]:
            c.fill(c.mask_ell(x, y, rr.randint(1, 3), 1), (120, 104, 84) if rr.random() < 0.6 else (230, 220, 200))

    def muraille(m):
        c.vgrad(m, 0, 480, (110, 190, 196), (16, 50, 96), steps=8)
        for _ in range(500):
            x, y = rr.randint(-105, 374), rr.randint(0, 479)
            if m[y, x + 105]:
                c.fill(c.mask_rect(x, y, x + rr.randint(1, 5), y), (150, 220, 226) if y < 200 else (40, 90, 140))
        for _ in range(14):
            x, y = rr.randint(-105, 374), rr.randint(60, 440)
            if m[y, x + 105]:
                d_ = 1 if rr.random() < 0.5 else -1
                c.fill(c.mask_ell(x, y, 3, 1.4) | c.mask_poly([(x - 3 * d_, y), (x - 6 * d_, y - 2), (x - 6 * d_, y + 2)]),
                       (20, 50, 80))
    gauche = c.mask_poly([(-105, 0), (vp[0] - 8, 120), (vp[0] - 8, vp[1]), (-60, 480), (-105, 480)])
    droite = c.mask_poly([(375, 0), (vp[0] + 8, 120), (vp[0] + 8, vp[1]), (330, 480), (375, 480)])
    muraille(gauche)
    muraille(droite)
    for m, sgn in ((gauche, -1), (droite, 1)):
        bord = m & ~np.roll(m, sgn * 3, axis=1)
        c.tint(bord, (210, 240, 246), 0.5)
        sommet = m & ~np.roll(m, 2, axis=0)
        c.fill(sommet, (246, 250, 252))
        c.fill(m & ~np.roll(m, 5, axis=0) & ~sommet, (200, 230, 236))
    for m in (gauche, droite):                                                 # l'eau qui ruisselle (traînées verticales)
        for _ in range(60):
            x, y = rr.randint(-105, 374), rr.randint(20, 400)
            if m[y, x + 105]:
                c.fill(m & c.mask_rect(x, y, x, y + rr.randint(8, 24)), (90, 160, 186))
    for (cx_, cy_, w_, h_) in ((-40, 240, 20, 30), (310, 250, 20, 30)):        # ouvertures : on voit un chemin voisin
        ouv = c.mask_arch(cx_ - w_ // 2, cx_ + w_ // 2, cy_ - h_, cy_)
        c.tint(ouv, (190, 230, 236), 0.55)
        c.fill(ouv & c.mask_rect(cx_ - w_ // 2, cy_ - 5, cx_ + w_ // 2, cy_), (176, 160, 124))
    c.tint(c.mask_ell(vp[0], vp[1], 60, 30), (255, 240, 210), 0.25)
    return c, None


def anim_poussiere_armee(t_debut=0.3, duree=6.0, x0=-105, x1=70, y=198):
    """Au loin, à gauche, l'armée de Pharaon : un nuage de poussière qui grandit, des cavaliers minuscules à perte de vue."""
    from PIL import Image, ImageDraw
    rnd = R(23)
    cav = [(rnd.uniform(x0, x1), rnd.uniform(0, 6.28)) for _ in range(70)]

    def f(img, u):
        if u < t_debut:
            return
        k = min(1.0, (u - t_debut) / duree)
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for j in range(9):
            cx = x0 + (x1 - x0) * (j + 0.5) / 9 + 105
            r = (6 + 8 * k) * (0.8 + 0.3 * math.sin(j * 1.7 + u * 0.6))
            d.ellipse([cx - r * 1.6, y - r * 1.4 - 2, cx + r * 1.6, y + 2], fill=(200, 176, 140, int(150 * k)))
        for (x, ph) in cav:
            if x > x0 + (x1 - x0) * min(1.0, k * 1.3):
                continue
            X = x + 105 + 0.6 * math.sin(u * 6 + ph)
            d.rectangle([X, y - 3, X + 1, y], fill=(50, 40, 40, int(230 * k)))
            d.point((X, y - 4), fill=(50, 40, 40, int(230 * k)))
        lieux.pose_calque(img, lay)
    return f


def anim_vagues(t_debut=0.0, niveau=300, duree=1.5):
    """La mer DEVANT les persos (par-dessus) : à partir de t_debut, les flots montent jusqu'au niveau `niveau` (coordonnées
    du dessin), seulement dans la partie « mer » du rivage, avec des vagues qui roulent (Pharaon englouti)."""
    from PIL import Image, ImageDraw
    poly = [(-105, 200)] + RIVAGE + [(-105, 480)]

    def f(img, u):
        if u < t_debut:
            return
        k = min(1.0, (u - t_debut) / duree)
        n_ = 480 - (480 - niveau) * k * k * (3 - 2 * k)
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        pts = [(x + 105, n_ + 2.5 * math.sin(x / 9.0 + u * 2.4)) for x in range(-105, 376, 3)]
        d.polygon(pts + [(480, 480), (0, 480)], fill=(40, 96, 140, 255))
        d.line(pts, fill=(220, 240, 246, 255), width=2)
        for x in range(-105, 376, 11):
            yy = n_ + 10 + 6 * math.sin(x * 0.7 + u)
            d.line([(x + 105, yy), (x + 110, yy)], fill=(120, 180, 210, 255))
        a = np.array(lay)
        im_p = Image.new("L", (a.shape[1], a.shape[0]), 0)
        ImageDraw.Draw(im_p).polygon([(x + 105, y) for x, y in poly], fill=255)
        a[np.array(im_p) > 0] = 0
        lieux.pose_calque(img, Image.fromarray(a, "RGBA"))
    return f


# ================================================================ le village des idoles
def village_idoles(heure="jour"):
    """Un village au-delà de la mer : maisons basses, palmiers ; sur une place, des statues de pierre sans visage (les
    idoles) sur des socles, des offrandes ; les gens s'y prosternent (persos, pose « prosterne »). Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 210, dict(aube=(320, 170), jour=(70, 40), soir=(-30, 170), nuit=(300, 60))[heure], seed=471)
    snap = c.a.copy()
    rr = R(472)
    x = -110
    k = 0
    while x < 380:
        w = rr.randint(40, 70)
        mur = T(BRIQUE[k % 4])
        mm = c.mask_rect(x, rr.randint(196, 226), x + w, 296)
        c.shape(mm, mur, dk(mur, 0.82), band=2)
        _fenetre(c, x + 10, 240, 7, 6, heure == "nuit")
        x += w
        k += 1
    for x_ in (-70, 60, 210, 330):
        palmier(c, x_, 230, h=34, lean=4, seed=480 + x_, col=T((64, 120, 66)), trunk=T((126, 94, 60)))
    sol = c.mask_rect(-105, 296, 375, 480)
    terre = T((206, 176, 128))
    c.vgrad(sol, 296, 480, lt(terre, 0.05), dk(terre, 0.7), steps=6)
    pierre = T((150, 140, 130))
    for (ix, h) in ((150, 54), (200, 64), (250, 50)):                         # les idoles : statues sans visage
        socle = c.mask_rect(ix - 12, 290, ix + 12, 306)
        c.shape(socle, dk(pierre, 0.9), dk(pierre, 0.65), lt(pierre, 0.08), band=2)
        corps = c.mask_poly([(ix - 9, 290), (ix + 9, 290), (ix + 7, 290 - h + 16), (ix - 7, 290 - h + 16)])
        tete = c.mask_ell(ix, 290 - h + 10, 7, 9)
        c.shape(corps | tete, pierre, dk(pierre, 0.7), lt(pierre, 0.12), band=2)
        c.fill(c.mask_rect(ix - 11, 290 - h + 24, ix + 11, 290 - h + 28), dk(pierre, 0.85))
        for (ox_, col) in ((-8, (190, 60, 50)), (6, (226, 186, 90))):          # offrandes
            c.fill(c.mask_ell(ix + ox_, 312, 3, 2), T(col))
    for y0_, kk in ((420, 0.10), (440, 0.18), (460, 0.26)):
        c.tint(c.mask_rect(-105, y0_, 375, 480), (40, 24, 20), kk)
    return relief(c, snap, sky), None


# ================================================================ le camp au pied de la montagne
def camp_desert(heure="jour"):
    """Le camp des fils d'Israël dans le désert, au pied d'une haute montagne : tentes rayées en rangs, feux de camp,
    jarres, troupeaux ; la montagne domine le fond. Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    nuit = heure == "nuit"
    sky = _ciel(c, heure, 230, dict(aube=(320, 190), jour=(300, 50), soir=(-30, 190), nuit=(300, 60))[heure], seed=491)
    snap = c.a.copy()
    rr = R(492)
    roc = T((150, 110, 96))
    mont = c.mask_poly([(-105, 250), (-40, 200), (40, 120), (90, 70), (130, 90), (180, 60), (250, 140), (320, 190),
                        (375, 210), (375, 250)])
    c.vgrad(mont, 60, 250, lt(roc, 0.1), dk(roc, 0.6), steps=6)
    for _ in range(14):
        x0_, y0_ = rr.randint(-80, 330), rr.randint(90, 230)
        pan = mont & c.mask_poly([(x0_, y0_), (x0_ + 24, y0_ + 8), (x0_ + 18, y0_ + 40), (x0_ - 6, y0_ + 28)])
        c.tint(pan, dk(roc, 0.55) if rr.random() < 0.6 else lt(roc, 0.2), 0.22)
    c.fill(mont & ~np.roll(mont, 1, axis=0), lt(roc, 0.3))
    sable = T((210, 178, 124))
    sol = c.mask_rect(-105, 246, 375, 480)
    c.vgrad(sol, 246, 480, mix(sable, CIELS[heure][1], 0.2), dk(sable, 0.7), steps=6)
    for row, (y_, n_, s_) in enumerate(((262, 9, 0.6), (284, 7, 0.85))):    # tentes, deux rangs
        for j in range(n_):
            tx = -100 + j * (480 // n_) + (row * 26)
            w_, h_ = int(30 * s_), int(20 * s_)
            col = T(((110, 84, 60), (150, 60, 50), (60, 70, 100), (176, 150, 110))[(j + row) % 4])
            tente = c.mask_poly([(tx - w_, y_), (tx, y_ - h_), (tx + w_, y_)])
            c.fill(tente, col)
            for k in range(-w_, w_, 4):
                c.fill(tente & c.mask_rect(tx + k, y_ - h_, tx + k + 1, y_), dk(col, 0.8))
            c.fill(c.mask_poly([(tx - 3, y_), (tx, y_ - h_ // 2), (tx + 3, y_)]), (40, 30, 26))
            c.outline(tente, (40, 30, 26))
    for (fx, fy) in ((-30, 300), (150, 296), (300, 302)):                     # feux de camp
        c.fill(c.mask_ell(fx, fy, 6, 2), (70, 60, 50))
        c.fill(c.mask_ell(fx, fy - 4, 3, 5), (255, 150, 60))
        c.fill(c.mask_ell(fx, fy - 3, 1.5, 3), (255, 226, 140))
        c.glow(fx, fy - 4, 30 if not nuit else 60, (255, 170, 80), 0.3 if not nuit else 0.5)
    for _ in range(60):
        x, y = rr.randint(-100, 370), rr.randint(300, 470)
        c.fill(c.mask_ell(x, y, 1.6, 1), lt(sable, 0.1))
    if nuit:
        c.tint(c.mask_rect(-105, 0, 375, 480), (10, 10, 36), 0.25)
    return relief(c, snap, sky), None


# ================================================================ sur la montagne
def montagne_sinai(heure="jour", effondre=False):
    """Sur la montagne : une crête rocheuse au premier plan (Moussa s'y tient), le vide, et en face un mont voisin
    immense ; effondre=True : à la place du mont, un amas de poussière et de rochers. Pieds y = 330."""
    c = _Px()
    nuit = heure == "nuit"
    if nuit:
        c.vgrad(c.mask_rect(-105, 0, 375, 330), 0, 330, (6, 8, 26), (30, 34, 66), steps=8)
        rr0 = R(501)
        for _ in range(260):
            c.px(rr0.randint(-105, 374), rr0.randint(0, 300), (226, 226, 252) if rr0.random() < 0.3 else (130, 136, 190))
    else:
        _ciel(c, heure, 332, dict(aube=(300, 200), jour=(60, 40), soir=(-30, 200))[heure], seed=502)
    T = _T(heure)
    rr = R(503)
    roc = T((140, 104, 92))
    if not effondre:
        mont = c.mask_poly([(60, 330), (110, 150), (150, 80), (170, 96), (200, 60), (240, 120), (300, 200), (360, 330)])
        c.vgrad(mont, 60, 330, lt(roc, 0.12), dk(roc, 0.55), steps=6)
        for _ in range(16):
            x0_, y0_ = rr.randint(100, 320), rr.randint(90, 300)
            pan = mont & c.mask_poly([(x0_, y0_), (x0_ + 20, y0_ + 6), (x0_ + 14, y0_ + 34), (x0_ - 6, y0_ + 24)])
            c.tint(pan, dk(roc, 0.55) if rr.random() < 0.6 else lt(roc, 0.2), 0.25)
        c.fill(mont & ~np.roll(mont, 1, axis=0), lt(roc, 0.3))
    else:
        tas = c.mask_poly([(60, 330), (110, 270), (170, 250), (240, 262), (300, 290), (360, 330)])
        c.vgrad(tas, 250, 330, lt(roc, 0.2), dk(roc, 0.6), steps=5)
        for _ in range(60):
            x, y = rr.randint(70, 350), rr.randint(256, 326)
            if tas[y, x + 105]:
                c.fill(c.mask_ell(x, y, rr.randint(2, 5), rr.randint(1, 3)), dk(roc, 0.7) if rr.random() < 0.5 else lt(roc, 0.15))
        for (y0_, k) in ((240, 0.18), (256, 0.12), (226, 0.08)):
            c.tint(c.mask_ell(210, y0_, 150, 20), (200, 180, 160), k)
    crete = c.mask_poly([(-105, 300), (-60, 290), (0, 296), (40, 306), (70, 330), (90, 480), (-105, 480)])   # notre crête
    c.vgrad(crete, 290, 480, lt(roc, 0.05), dk(roc, 0.5), steps=6)
    c.fill(crete & ~np.roll(crete, 1, axis=0), lt(roc, 0.3))
    sol = c.mask_rect(-105, 330, 375, 480) & ~crete
    c.vgrad(sol, 330, 480, dk(roc, 0.55), dk(roc, 0.35), steps=4)
    plat = c.mask_rect(-105, 318, 140, 480)                                   # le replat où se tient Moussa
    c.vgrad(plat, 318, 480, dk(roc, 0.95), dk(roc, 0.55), steps=5)
    c.fill(plat & ~np.roll(plat, 1, axis=0), lt(roc, 0.25))
    if nuit:
        c.tint(c.mask_rect(-105, 0, 375, 480), (10, 10, 40), 0.3)
    return c, None


def anim_etoiles_tournent(t_debut=0.0, vitesse=0.06, pole=(135, -20), n=160, seed=61):
    """Les nuits qui passent : les étoiles tournent lentement autour du pôle (traînées courtes)."""
    from PIL import Image, ImageDraw
    rnd = R(seed)
    E = [(rnd.uniform(40, 360), rnd.uniform(0, 6.28), rnd.random()) for _ in range(n)]

    def f(img, u):
        if u < t_debut:
            return
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for (r, a0, b) in E:
            for k in range(4):                                                 # traînée
                a = a0 + vitesse * (u - t_debut) - k * 0.012
                x, y = pole[0] + r * math.cos(a) + 105, pole[1] + r * math.sin(a)
                if 0 <= y <= 300:
                    al = int((230 if b < 0.3 else 140) * (1 - k * 0.25))
                    d.point((x, y), fill=(230, 230, 255, al))
        lieux.pose_calque(img, lay)
    return f


def anim_poussiere_mont(t_debut=0.0, duree=5.0, cx=210, cy=200):
    """Le mont pulvérisé : un grand nuage de poussière qui s'élève et se disperse lentement (pas d'éclair)."""
    from PIL import Image, ImageDraw
    rnd = R(67)
    B = [(rnd.uniform(-120, 120), rnd.uniform(-60, 60), rnd.uniform(8, 22), rnd.uniform(0, 6.28)) for _ in range(40)]

    def f(img, u):
        if u < t_debut or u > t_debut + duree + 2:
            return
        k = (u - t_debut) / duree
        a = min(1.0, k * 3) * max(0.0, 1 - max(0.0, k - 0.6) / 0.6)
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for (dx, dy, r, ph) in B:
            x = cx + dx * (0.5 + k) + 105
            y = cy + dy * (0.6 + 0.6 * k) - 20 * k
            rr_ = r * (0.6 + k)
            d.ellipse([x - rr_, y - rr_, x + rr_, y + rr_], fill=(200, 180, 160, int(120 * a)))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ les cailles (2:57)
def anim_cailles(t_debut=0.0, n=60, seed=57):
    """Des cailles arrivent par vols du ciel, à droite, planent et se posent par dizaines autour du camp ; posées, elles
    picorent (petits sauts). Lent, sans à-coup."""
    from PIL import Image, ImageDraw
    rnd = R(seed)
    Q = []
    for i in range(n):
        arr = rnd.uniform(0, 4.0)                                              # arrivées étalées
        xs, ys = rnd.uniform(240, 420), rnd.uniform(110, 170)                  # d'où elles viennent (haut, à droite)
        xe, ye = rnd.uniform(-90, 350), rnd.uniform(294, 316)                  # où elles se posent
        Q.append((arr, xs, ys, xe, ye, rnd.uniform(2.0, 3.0), rnd.uniform(0, 6.28)))

    def f(img, u):
        if u < t_debut:
            return
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for (arr, xs, ys, xe, ye, vol, ph) in sorted(Q, key=lambda q: q[4]):
            a_ = u - t_debut - arr
            if a_ < 0:
                continue
            k = min(1.0, a_ / vol)
            e = k * k * (3 - 2 * k)
            x = xs + (xe - xs) * e + 105
            y = ys + (ye - ys) * e - 12 * math.sin(math.pi * e)
            al = int(255 * min(1.0, a_ * 2.0))
            corps, tete, ventre = (150, 112, 72, al), (92, 66, 42, al), (220, 200, 160, al)
            if k < 1:                                                          # en vol : ailes qui battent
                h_ = 2 if int((u + ph) * 6) % 2 else -2
                d.line([(x - 5, y + h_), (x - 1, y)], fill=(120, 90, 58, al), width=1)
                d.line([(x + 1, y), (x + 5, y + h_)], fill=(120, 90, 58, al), width=1)
                d.ellipse([x - 2, y - 1, x + 2, y + 1], fill=corps)
                d.point((x - 3, y - 1), fill=tete)
            else:                                                              # posée : elle picore
                sau = 1 if (math.sin((u + ph) * 2.4) > 0.86) else 0
                d.ellipse([x - 3, y - 3 - sau, x + 3, y - sau], fill=corps)
                d.line([(x - 1, y - 1 - sau), (x + 2, y - 1 - sau)], fill=ventre)
                d.rectangle([x - 4, y - 4 - sau, x - 3, y - 3 - sau], fill=tete)
                d.point((x - 5, y - 3 - sau), fill=(60, 44, 30, al))
        lieux.pose_calque(img, lay)
    return f

# ================================================================ la foudre qui saisit les soixante-dix (2:55)
def anim_foudre(t_debut=0.0, cx=200, duree=2.8):
    """La foudre, en douceur (jamais un éclair brusque) : une colonne de lumière pâle descend du ciel sur le groupe,
    s'intensifie en 0,8 s puis s'éteint lentement."""
    from PIL import Image, ImageDraw

    def f(img, u):
        if u < t_debut or u > t_debut + duree:
            return
        v = u - t_debut
        a = min(1.0, v / 0.8) * (1.0 if v < 1.2 else max(0.0, 1 - (v - 1.2) / (duree - 1.2)))
        a = a * a * (3 - 2 * a)
        if a <= 0.01:
            return
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        x = cx + 105
        for (w_, al) in ((150, 0.16), (110, 0.2), (70, 0.24), (34, 0.3)):
            d.polygon([(x - w_ * 0.35, 0), (x + w_ * 0.35, 0), (x + w_, 340), (x - w_, 340)],
                      fill=(240, 244, 255, int(255 * al * a)))
        for (r_, al) in ((140, 0.12), (90, 0.18), (50, 0.22)):
            d.ellipse([x - r_, 300 - r_ * 0.35, x + r_, 300 + r_ * 0.35], fill=(250, 250, 255, int(255 * al * a)))
        lieux.pose_calque(img, lay)
    return f

# ================================================================ les cendres du veau d'or dispersées dans les flots (20:97)
def anim_cendres(t_debut=0.0, duree=4.5, x0=130, y0=280, n=260, seed=97):
    """Les cendres du veau d'or : un petit nuage gris (bouffées douces) et des paillettes d'or partent du rivage, emportés
    par le vent vers la mer ; ils s'étirent, retombent doucement dans les flots et disparaissent (lent, pas d'éclair)."""
    from PIL import Image, ImageDraw
    rnd = R(seed)
    P = []
    for i in range(n):
        nait = rnd.uniform(0, duree * 0.55)                                   # les cendres partent par bouffées
        vx, vy = rnd.uniform(16, 40), rnd.uniform(-10, -3)
        dor = rnd.random() < 0.3
        gros = rnd.random() < 0.4
        P.append((nait, rnd.uniform(-5, 5), rnd.uniform(-4, 4), vx, vy, dor, gros, rnd.uniform(0, 6.28)))
    B = [(rnd.uniform(0, duree * 0.5), rnd.uniform(-4, 4), rnd.uniform(-3, 3), rnd.uniform(12, 24), rnd.uniform(4, 7))
         for _ in range(16)]                                                   # bouffées de fumée grise

    def f(img, u):
        if u < t_debut or u > t_debut + duree + 4.0:
            return
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for (nait, dx, dy, vx, r0) in B:
            a_ = u - t_debut - nait
            if a_ < 0 or a_ > 3.2:
                continue
            x, y = x0 + dx + vx * a_, y0 + dy - 4 * a_ + 2.2 * a_ * a_
            r_ = r0 * (0.6 + 0.35 * a_)
            al = int(70 * min(1.0, a_ * 2.5) * (1 - a_ / 3.2))
            d.ellipse([x + 105 - r_, y - r_ * 0.7, x + 105 + r_, y + r_ * 0.7], fill=(128, 120, 116, al))
        for (nait, dx, dy, vx, vy, dor, gros, ph) in P:
            a_ = u - t_debut - nait
            if a_ < 0:
                continue
            x = x0 + dx + vx * a_ + 3 * math.sin(a_ * 1.7 + ph)
            y = y0 + dy + vy * a_ + 4.0 * a_ * a_                             # le vent les porte, puis elles retombent
            vie = 1.0 - a_ / 3.8
            if vie <= 0:
                continue
            col = (244, 204, 92) if dor else (104, 98, 94)
            al = int(255 * min(1.0, a_ * 3) * min(1.0, vie * 1.6))
            if gros:
                d.rectangle([x + 105, y, x + 106, y + 1], fill=(*col, al))
            else:
                d.point((x + 105, y), fill=(*col, al))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ le mont brandi au-dessus du camp (2:63)
def camp_desert_mont(heure="jour"):
    """Le camp au pied de la montagne, mais la montagne s'est soulevée et reste suspendue au-dessus du peuple comme un
    nuage de pierre (sa base déchiquetée, des pierres qui pendent), son ombre couvre tout le camp."""
    bg, fg = camp_desert(heure)
    c = bg
    T = _T(heure)
    rr = R(511)
    sky = _ciel(c, heure, 250, dict(aube=(320, 190), jour=(300, 50), soir=(-30, 190), nuit=(300, 60))[heure], seed=491)
    roc = T((150, 110, 96))
    pts_bas = []
    for x in range(-110, 384, 8):                                            # base déchiquetée du mont soulevé
        pts_bas.append((x, 202 + rr.randint(-6, 10)))                        # (il flotte juste au-dessus des tentes)
    mont = c.mask_poly([(-110, 196), (-60, 150), (-10, 118), (40, 78), (90, 38), (130, 56), (180, 28), (250, 96),
                        (320, 142), (384, 168)] + pts_bas[::-1])
    c.vgrad(mont, 28, 212, lt(roc, 0.1), dk(roc, 0.45), steps=6)
    for _ in range(14):
        x0_, y0_ = rr.randint(-80, 330), rr.randint(80, 190)
        pan = mont & c.mask_poly([(x0_, y0_), (x0_ + 24, y0_ + 8), (x0_ + 18, y0_ + 40), (x0_ - 6, y0_ + 28)])
        c.tint(pan, dk(roc, 0.5), 0.25)
    c.fill(mont & ~np.roll(mont, -1, axis=0), dk(roc, 0.4))
    for (x, y) in pts_bas[::3]:                                              # pierres qui pendent sous le mont
        c.fill(c.mask_poly([(x - 3, y), (x + 3, y), (x, y + rr.randint(4, 9))]), dk(roc, 0.5))
    c.tint(c.mask_rect(-105, 214, 375, 480), (20, 16, 30), 0.38)             # l'ombre sur tout le camp
    bg.lointain = None
    return bg, fg


# ================================================================ la terre sainte
def terre_sainte(heure="jour"):
    """Au bord d'une terre verte et fertile : collines cultivées, oliviers, une rivière, et au loin les murailles d'une
    ville forte (le peuple redoutable) ; au premier plan le désert d'où vient le peuple. Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, 200, dict(aube=(320, 160), jour=(80, 40), soir=(-30, 160), nuit=(300, 60))[heure], seed=521)
    snap = c.a.copy()
    rr = R(522)
    vert, vert2 = T((96, 150, 70)), T((126, 176, 86))
    for (ytop, amp, per, ph, k) in ((196, 8, 50, 0.3, 0.35), (214, 10, 60, 2.0, 0.18), (236, 12, 70, 4.1, 0.05)):
        m = c.yy >= ytop + amp * np.sin(c.xx / per + ph)
        col = mix(vert, CIELS[heure][1], k)
        c.vgrad(m, ytop - amp, 480, lt(col, 0.06), dk(col, 0.8), steps=5)
        c.fill(m & ~np.roll(m, 1, axis=0), lt(col, 0.16))
    mur = mix(T((200, 176, 140)), CIELS[heure][1], 0.3)                      # la ville forte au loin
    c.fill(c.mask_rect(150, 168, 290, 198), mur)
    for x in range(150, 291, 8):
        c.fill(c.mask_rect(x, 164, x + 4, 168), mur)
    for x in (150, 196, 244, 286):
        c.fill(c.mask_rect(x - 4, 156, x + 6, 198), lt(mur, 0.06))
        for xx in range(x - 4, x + 7, 4):
            c.fill(c.mask_rect(xx, 152, xx + 2, 156), lt(mur, 0.06))
    c.fill(c.mask_rect(212, 182, 222, 198), dk(mur, 0.6))
    for _ in range(26):                                                      # oliviers
        x, y = rr.randint(-100, 370), rr.randint(206, 270)
        s_ = 0.6 + (y - 200) / 80
        c.fill(c.mask_rect(x, y - int(5 * s_), x, y), T((90, 70, 50)))
        c.fill(c.mask_ell(x, y - 7 * s_, 5 * s_, 3.5 * s_), T((110, 140, 96)))
    riv = c.mask_poly([(80, 230), (96, 230), (140, 300), (180, 330), (150, 330), (110, 300)])
    c.fill(riv, T((110, 170, 200)))
    desert_ = c.mask_poly([(-105, 290), (40, 296), (160, 312), (375, 318), (375, 480), (-105, 480)])
    sable = T((214, 182, 128))
    c.vgrad(desert_, 290, 480, lt(sable, 0.05), dk(sable, 0.7), steps=6)
    for _ in range(60):
        x, y = rr.randint(-100, 370), rr.randint(300, 470)
        if desert_[y, x + 105]:
            c.fill(c.mask_ell(x, y, 1.6, 1), lt(sable, 0.1))
    return relief(c, snap, sky), None


# ================================================================ les douze sources, la manne, le nuage, les cailles
def anim_sources(t_debut=0.0, x=135, y=300, n=12):
    """Douze sources jaillissent du rocher frappé (2:60) : douze jets d'eau en éventail, partis du haut du rocher, qui
    retombent en arc et forment des flaques qui s'élargissent ; l'eau coule (reflets qui descendent les jets)."""
    from PIL import Image, ImageDraw
    y_haut = y - 18                                                           # le haut du rocher
    J = []
    for i in range(n):
        f_ = i / (n - 1)
        dx = -64 + 128 * f_                                                   # éventail de -64 à +64 px
        yb = y + 4 + 6 * abs(f_ - 0.5) * 2                                    # retombe au sol, devant le rocher
        h_ = 26 + 10 * (1 - abs(f_ - 0.5) * 2)                                # les jets du milieu montent plus haut
        J.append((dx, yb, h_, 0.08 * (i % 4)))

    def f(img, u):
        if u < t_debut:
            return
        v = u - t_debut
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        X = x + 105
        for (dx, yb, h_, dec) in J:                                          # les flaques, sous les jets
            k = max(0.0, min(1.0, (v - dec - 0.8) / 2.5))
            if k > 0:
                rx = 3 + 7 * k
                d.ellipse([X + dx - rx, yb - 1.5 - k, X + dx + rx, yb + 1.5 + k], fill=(104, 168, 214, int(210 * k)))
        for (dx, yb, h_, dec) in J:
            k = max(0.0, min(1.0, (v - dec) / 0.7))                           # le jet sort en 0,7 s
            if k <= 0:
                continue
            pts = []
            for j in range(19):
                tt = j / 18 * k
                px_ = X + dx * tt
                py_ = y_haut + (yb - y_haut) * tt - 4 * h_ * tt * (1 - tt)
                pts.append((px_, py_))
            d.line(pts, fill=(126, 196, 240, 235), width=3)
            d.line(pts, fill=(228, 244, 255, 230), width=1)
            for m_ in range(3):                                               # reflets qui descendent le jet
                ph = ((v * 1.6 + m_ / 3 + dec) % 1.0) * k
                j_ = int(ph * 18)
                if 0 < j_ < len(pts):
                    d.point(pts[j_], fill=(255, 255, 255, 255))
            if k >= 1:                                                        # éclaboussures à l'arrivée
                ex, ey = pts[-1]
                for m_ in range(3):
                    a_ = (v * 5 + m_ * 2.1 + dx) % 6.28
                    d.point((ex + 3 * math.cos(a_), ey - 2 - abs(2 * math.sin(a_ * 1.3))), fill=(236, 248, 255, 220))
        lieux.pose_calque(img, lay)
    return f


def anim_manne(t_debut=0.0, n=460, seed=31):
    """Au matin, une rosée blanche et sucrée couvre peu à peu le sol (la manne) : des centaines de grains blancs qui
    apparaissent en fondu, dans la partie du sol qu'on voit (devant les tentes, au-dessus des sous-titres)."""
    from PIL import Image, ImageDraw
    rnd = R(seed)
    P = [(rnd.uniform(-100, 370), rnd.uniform(292, 350), rnd.uniform(0, 3.4), rnd.random() < 0.35) for _ in range(n)]

    def f(img, u):
        if u < t_debut:
            return
        v = u - t_debut
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for (x, y, nait, gros) in P:
            a_ = min(1.0, (v - nait) / 0.6)
            if a_ <= 0:
                continue
            col = (252, 250, 240, int(240 * a_))
            if gros:
                d.rectangle([x + 105, y, x + 106, y], fill=col)
            else:
                d.point((x + 105, y), fill=col)
        lieux.pose_calque(img, lay)
    return f


def anim_nuage(t_debut=0.0, duree=4.0, cy=150):
    """Un nuage immense vient se placer au-dessus du camp (dans le haut du cadre) et étend son ombre sur tout le sol
    (abri du soleil) ; il glisse lentement de la gauche."""
    from PIL import Image, ImageDraw

    def f(img, u):
        if u < t_debut:
            return
        k = min(1.0, (u - t_debut) / duree)
        e = k * k * (3 - 2 * k)
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        cx = -260 + 390 * e + 105
        d.rectangle([0, 246, 480, 480], fill=(30, 26, 40, int(64 * e)))     # l'ombre sur le sol
        for (dx, dy, r) in ((-150, 14, 46), (-90, 0, 60), (-20, -10, 70), (60, -4, 64), (130, 8, 52), (190, 16, 40),
                            (20, 18, 80)):
            d.ellipse([cx + dx - r, cy + dy - r * 0.42, cx + dx + r, cy + dy + r * 0.42],
                      fill=(214, 216, 226, int(220 * e)))
        for (dx, dy, r) in ((-80, -8, 50), (-10, -18, 58), (70, -12, 50), (140, 2, 38)):
            d.ellipse([cx + dx - r, cy + dy - r * 0.38, cx + dx + r, cy + dy + r * 0.38],
                      fill=(248, 248, 252, int(235 * e)))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ registre
_DEC = dict(champs_nil=champs_nil, champs_nil_secs=lambda: champs_nil("jour", "secs"),
            champs_nil_inondes=lambda: champs_nil("jour", "inondes"), grenier=grenier, nil_sang=nil_sang,
            terrasse_nuit=terrasse_nuit, rivage_mer=rivage_mer, rivage_mer_jour=lambda: rivage_mer("jour"),
            mer_ouverte=mer_ouverte, village_idoles=village_idoles, camp_desert=camp_desert,
            camp_desert_nuit=lambda: camp_desert("nuit"), camp_desert_soir=lambda: camp_desert("soir"),
            camp_desert_aube=lambda: camp_desert("aube"),
            montagne_sinai=montagne_sinai, montagne_sinai_nuit=lambda: montagne_sinai("nuit"),
            montagne_sinai_effondre=lambda: montagne_sinai("jour", effondre=True),
            montagne_sinai_aube=lambda: montagne_sinai("aube"), camp_desert_mont=camp_desert_mont,
            terre_sainte=terre_sainte, terre_sainte_soir=lambda: terre_sainte("soir"))
egypte.enregistre(_DEC, sol_haut=dict(champs_nil=(330, 110), grenier=(330, 100), nil_sang=(335, 130), terrasse_nuit=(330, 100),
                                      rivage_mer=(330, 100), mer_ouverte=(330, 96), village_idoles=(330, 106),
                                      camp_desert=(330, 104), montagne_sinai=(330, 100), camp_desert_mont=(330, 100),
                                      terre_sainte=(330, 104)))
lieux.LUMIERES["grenier"] = (lieux.JOUR, [])
lieux.LUMIERES["terrasse_nuit"] = (lieux.NUIT, [])
lieux.LUMIERES["champs_nil_inondes"] = (lieux.SOIR, [])
