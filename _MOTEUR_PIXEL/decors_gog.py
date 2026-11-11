# FILM HORS-SÉRIE « GOG ET MAGOG » (10/11/2026) — décors et grandes animations.
# Toile 16:9 du film : x = -105 … 375, y = 0 … 480, fenêtre du plan large ≈ y 100 … 370, pieds à y = 330.
# Décors (tous avec les heures _soir, _nuit, et _fin = ciel de poussière rouge de la fin des temps) :
#   gog_col            le passage entre les Deux Barrières (deux montagnes), encore ouvert ; au fond, le pays d'où ils viennent
#   gog_barrage_fer    les blocs de fer empilés jusqu'en haut, entre les deux versants (18:96)
#   gog_barrage        le barrage fini : le fer couvert de cuivre fondu (18:96-97)
# Animations (posées sur un mot du scénario) :
#   {barrage_monte N}  sur gog_col : les rangées de blocs de fer montent, une par une, jusqu'au niveau des deux versants
#   {barrage_feu N}    le fer chauffe jusqu'à devenir une fournaise (« Soufflez ! »)
#   {barrage_cuivre N} le cuivre fondu coule d'en haut et recouvre tout ; le métal refroidit
#   {barrage_tombe N}  sur gog_barrage_fin : il se fissure, il est nivelé (18:98), la poussière monte, et ils sortent
#                      comme des flots (18:99, 21:96) : une marée humaine, du col et de chaque hauteur
# Gog et Magog : des êtres humains (fils d'Adam) ; montrés seulement en foule de silhouettes sombres, sans aucun trait
# inventé (ni taille, ni visage) : seul leur NOMBRE est montré.
import math

import numpy as np
from PIL import Image, ImageDraw

import egypte
import lieux
from egypte import _Px
from lieux import R, dk, lt, mix
from px import BAYER

# ---------------------------------------------------------------- géométrie du col
CX = 135                    # axe du passage
YT, YB = 186, 298           # haut du barrage (niveau des deux versants), pied du barrage
HEURES = ("jour", "soir", "nuit", "fin")
CIELS = dict(jour=((92, 150, 220), (212, 230, 244)), soir=((70, 58, 120), (250, 164, 104)),
             nuit=((8, 12, 34), (34, 42, 84)), fin=((54, 30, 40), (226, 128, 70)))
ROCS = dict(jour=(150, 124, 104), soir=(150, 104, 92), nuit=(54, 56, 84), fin=(112, 70, 62))
SOLS = dict(jour=(206, 178, 128), soir=(204, 150, 104), nuit=(52, 54, 80), fin=(150, 98, 70))
FER = (64, 70, 86)
CUIVRE = (184, 100, 52)
CUIVRE_CLAIR = (244, 170, 96)
CUIVRE_SOMBRE = (112, 54, 36)


def xl(y):
    """Bord intérieur du versant gauche (le passage s'élargit vers le haut)."""
    return 96 - (YB - y) * 0.17 + 3.0 * np.sin(y * 0.11) + 1.5 * np.sin(y * 0.37 + 1.0)


def xr(y):
    return 174 + (YB - y) * 0.17 + 3.0 * np.sin(y * 0.13 + 1.0) + 1.5 * np.sin(y * 0.41)


def _bay(c):
    return BAYER[c.yy % 4, (c.xx + c.ox) % 4]


def _stops(stops, t):
    ts = np.array([s for s, _ in stops], np.float32)
    cs = np.array([col for _, col in stops], np.float32)
    out = np.empty(t.shape + (3,), np.float32)
    for ch in range(3):
        out[..., ch] = np.interp(t, ts, cs[:, ch])
    return out


def _peint(c, m, t, stops, steps=12):
    q = np.floor(np.clip(t, 0, 1) * (steps - 1) + _bay(c)) / (steps - 1)
    col = _stops(stops, q)
    c.a[m] = np.clip(col[m], 0, 255).astype(np.uint8)
    c.al[m] = True


def _melange(c, m, col, k):
    a = c.a.astype(np.float32)
    kk = np.broadcast_to(np.asarray(k, np.float32), m.shape)
    sel = m & (kk > 0)
    a[sel] = a[sel] * (1 - kk[sel, None]) + np.array(col, np.float32) * kk[sel, None]
    c.a = np.clip(a, 0, 255).astype(np.uint8)


def _bruit(X, Y, seed=0.0):
    """Bruit doux (somme de sinus), entre -1 et 1 environ."""
    return (np.sin(X * 0.071 + Y * 0.043 + seed) + np.sin(X * 0.173 - Y * 0.097 + seed * 2.1)
            + np.sin(X * 0.031 + Y * 0.151 + seed * 0.7)) / 3.0


def _ciel(c, heure, y1, seed=3):
    sky = c.mask_rect(-105, 0, 375, y1)
    top, bot = CIELS[heure]
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    _peint(c, sky, Y / y1, [(0.0, top), (0.55, mix(top, bot, 0.55)), (1.0, bot)], 12)
    rr = R(seed)
    if heure == "nuit":
        for _ in range(170):
            x, y = rr.randint(-105, 374), rr.randint(0, y1 - 20)
            c.px(x, y, (232, 232, 255) if rr.random() < 0.3 else (130, 138, 200))
        moon = c.mask_ell(196, 124, 9, 9) & ~c.mask_ell(200, 121, 8, 8)
        c.fill(moon & sky, (250, 240, 206))
        c.glow(196, 124, 34, (180, 190, 255), 0.16, m=sky)
    elif heure == "fin":                                       # soleil voilé, bandes de poussière rouge
        c.glow(CX, YT - 8, 110, (255, 190, 110), 0.42, m=sky)
        c.fill(c.mask_ell(CX, YT - 8, 15, 15) & sky, (255, 226, 170))
        for k in range(9):
            yb = 104 + k * 13 + rr.randint(-4, 4)
            bande = sky & (np.abs(Y - yb - 5 * np.sin(X * 0.02 + k)) < 2.4 + 1.6 * np.sin(X * 0.045 + k * 2)) & (_bay(c) < 0.72)
            _melange(c, bande, (96, 46, 44) if k % 2 else (250, 160, 96), 0.42)
    elif heure == "soir":
        c.glow(CX + 10, YT - 14, 110, (255, 200, 130), 0.42, m=sky)
        c.fill(c.mask_ell(CX + 10, YT - 14, 12, 12) & sky, (255, 232, 180))
        for k in range(6):
            yb = 108 + k * 12 + rr.randint(-5, 5)
            x0 = rr.randint(-100, 260)
            nu = sky & c.mask_ell(x0 + 40, yb, rr.randint(30, 60), 3)
            _melange(c, nu & (_bay(c) < 0.8), (255, 190, 140), 0.5)
    else:                                                      # jour : nuages légers
        for k in range(7):
            x0, yb = rr.randint(-100, 330), rr.randint(104, 170)
            for j in range(4):
                nu = sky & c.mask_ell(x0 + j * 11, yb + (j % 2) * 2, rr.randint(9, 16), rr.randint(3, 5))
                _melange(c, nu, (250, 252, 255), 0.75)
    return sky


def _roche(c, m, roc, seed, lum=-1):
    """Texture d'un versant : dégradé, strates, facettes, ravines, arête éclairée. lum = côté de la lumière (-1 gauche)."""
    rr = R(seed)
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    _peint(c, m, (Y - 100) / 210.0, [(0.0, lt(roc, 0.16)), (0.45, roc), (1.0, dk(roc, 0.6))], 10)
    xs_m = X[m]
    cx_m = float(xs_m.mean()) if xs_m.size else 0.0
    n_c = 120                                                                              # pans de roche (cellules)
    gx = np.array([rr.uniform(-110, 380) for _ in range(n_c)], np.float32)
    gy = np.array([rr.uniform(90, 320) for _ in range(n_c)], np.float32)
    d1 = np.full(X.shape, 1e9, np.float32)
    d2 = np.full(X.shape, 1e9, np.float32)
    i1 = np.zeros(X.shape, np.int32)
    for i in range(n_c):
        dd = (X - gx[i] - (Y - gy[i]) * 0.35 * lum) ** 2 + ((Y - gy[i]) * 0.5) ** 2      # pans hauts, un peu penchés
        plus = dd < d1
        d2 = np.where(plus, d1, np.minimum(d2, dd))
        i1 = np.where(plus, i, i1)
        d1 = np.where(plus, dd, d1)
    ton = np.array([rr.uniform(-1, 1) for _ in range(n_c)], np.float32)
    ton = ton * 0.6 + np.clip((gx - cx_m) * lum / 90.0, -1, 1) * 0.55                       # un côté au soleil, l'autre à l'ombre
    tt_ = ton[i1]
    _melange(c, m & (tt_ > 0), lt(roc, 0.4), np.clip(tt_, 0, 1) * 0.5)
    _melange(c, m & (tt_ < 0), dk(roc, 0.4), np.clip(-tt_, 0, 1) * 0.5)
    bord = (np.sqrt(d2) - np.sqrt(d1)) < 1.1                                                # fentes entre les pans
    _melange(c, m & bord, dk(roc, 0.36), 0.5)
    _melange(c, m & np.roll(bord, -lum, axis=1) & ~bord, lt(roc, 0.4), 0.32)                # arête éclairée à côté
    strate = np.sin(Y * 0.30 + np.sin(X * 0.021 + seed) * 1.6 + X * 0.045) > 0.97           # quelques strates fines
    _melange(c, m & strate, dk(roc, 0.5), 0.16)
    for _ in range(18):                                                                    # ravines verticales
        x, y = rr.randint(-104, 373), rr.randint(100, 296)
        if m[y, x + c.ox]:
            L_ = rr.randint(8, 30)
            for j in range(L_):
                yy = y + j
                xx = x + int(round(1.4 * math.sin(j * 0.5 + x)))
                if 0 <= yy < 480 and -105 <= xx < 375 and m[yy, xx + c.ox]:
                    c.px(xx, yy, tuple(dk(roc, 0.5)))
                    if -105 <= xx - lum < 375 and m[yy, xx - lum + c.ox]:
                        c.px(xx - lum, yy, tuple(lt(roc, 0.2)))
    arete = m & ~np.roll(m, 1, axis=0)                                                     # arête du haut, éclairée
    c.fill(arete, tuple(lt(roc, 0.42)))
    c.fill(m & np.roll(arete, 1, axis=0) & (_bay(c) < 0.6), tuple(lt(roc, 0.3)))


def _crete(pts, seed, amp=5):
    """Ligne de crête déchiquetée passant par les points donnés."""
    rr = R(seed)
    out = []
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        n = max(1, int(abs(x1 - x0) / 5))
        for i in range(n):
            s = i / n
            out.append((x0 + (x1 - x0) * s, y0 + (y1 - y0) * s + (rr.uniform(-amp, amp) if i else 0)))
    out.append(pts[-1])
    return out


def _masque_mur(c):
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    return (Y >= YT) & (Y <= YB) & (X >= xl(Y) - 1) & (X <= xr(Y) + 1)


def _blocs(seed=77):
    """Les blocs de fer, rangée par rangée, du pied vers le haut : [(y0, y1, [(x0, x1), …]), …]."""
    rr = R(seed)
    rangs = []
    y = YB
    i = 0
    while y > YT:
        h = 7 if i % 3 else 8
        y0 = max(YT, y - h)
        x = float(xl(np.float32(y))) - 6 + (i % 2) * 7
        fin_ = float(xr(np.float32(y))) + 4
        bl = []
        while x < fin_:
            w = rr.randint(11, 17)
            bl.append((int(x), int(x + w - 1)))
            x += w
        rangs.append((y0, y, bl))
        y = y0
        i += 1
    return rangs


RANGS = _blocs()


def _mur_fer(c, m, heure):
    """Le barrage de fer : blocs massifs en rangées décalées, joints sombres, arêtes claires, rouille légère."""
    fer = dict(jour=FER, soir=mix(FER, (120, 70, 60), 0.25), nuit=dk(FER, 0.62), fin=mix(FER, (110, 56, 50), 0.3))[heure]
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    _peint(c, m, (Y - YT) / (YB - YT), [(0.0, lt(fer, 0.16)), (0.5, fer), (1.0, dk(fer, 0.66))], 8)
    rr = R(78)
    for (y0, y1, bl) in RANGS:
        for (x0, x1) in bl:
            b = m & c.mask_rect(x0, y0, x1, y1 - 1)
            if not b.any():
                continue
            k = rr.uniform(-0.12, 0.12)
            _melange(c, b, lt(fer, 0.5) if k > 0 else dk(fer, 0.4), abs(k) * 2.2)
            c.fill(m & c.mask_rect(x0, y0, x1, y0), tuple(lt(fer, 0.34)))                   # arête du haut
            c.fill(m & c.mask_rect(x0, y0, x0, y1 - 1), tuple(lt(fer, 0.16)))                # arête gauche
            c.fill(m & c.mask_rect(x1, y0, x1, y1 - 1), tuple(dk(fer, 0.5)))                 # joint
            c.fill(m & c.mask_rect(x0, y1 - 1, x1, y1 - 1), tuple(dk(fer, 0.42)))            # ombre du bas
            if rr.random() < 0.35:                                                           # traces de rouille
                rx = rr.randint(x0 + 1, max(x0 + 1, x1 - 2))
                c.fill(m & c.mask_rect(rx, y0 + 2, rx + rr.randint(1, 4), y0 + 3), tuple(mix(fer, (130, 74, 50), 0.6)))
    _melange(c, m & (X < xl(Y) + 8), (0, 0, 0), 0.30)                                        # ombre des versants
    _melange(c, m & (X > xr(Y) - 8), (0, 0, 0), 0.36)


def _mur_cuivre(c, m, heure):
    """Le barrage fini : le cuivre fondu a coulé sur le fer et rempli les joints ; métal lisse, coulures, reflets."""
    _mur_fer(c, m, heure)
    amb = dict(jour=1.0, soir=0.92, nuit=0.5, fin=0.82)[heure]
    cu, cl, cs = [tuple(int(v * amb) for v in col) for col in (CUIVRE, CUIVRE_CLAIR, CUIVRE_SOMBRE)]
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    t = (Y - YT) / (YB - YT)
    a0 = c.a.copy()
    _peint(c, m, t, [(0.0, lt(cu, 0.2)), (0.4, cu), (1.0, cs)], 10)
    joints = m & (np.abs(a0.astype(np.int32).sum(axis=2) - c.a.astype(np.int32).sum(axis=2)) >= 0)
    sombre = a0.astype(np.int32).sum(axis=2) < np.median(a0[m].astype(np.int32).sum(axis=1)) - 40
    _melange(c, joints & sombre, cs, 0.55)                                                    # les joints, en creux
    coul = np.sin(X * 1.9 + np.sin(Y * 0.045 + X * 0.3) * 1.2) > 0.86                          # coulures verticales
    _melange(c, m & coul, cl, 0.4 * (1 - t * 0.6))
    coul2 = np.sin(X * 1.3 + 2.0 + np.sin(Y * 0.06) * 0.8) < -0.9
    _melange(c, m & coul2, cs, 0.4)
    lustre = (np.exp(-((X - (CX - 22)) / 5.0) ** 2) + 0.7 * np.exp(-((X - (CX + 14)) / 3.0) ** 2)
              + 0.5 * np.exp(-((X - (CX - 44)) / 2.5) ** 2) + 0.4 * np.exp(-((X - (CX + 40)) / 4.0) ** 2))
    lustre = lustre * (0.55 + 0.45 * np.sin(Y * 0.16 + X * 0.05) ** 2) * (1 - t * 0.55)
    _melange(c, m & (_bay(c) < lustre * 1.3), (255, 226, 170) if heure != "nuit" else (170, 180, 230),
             np.clip(lustre, 0, 1) * (0.55 if heure != "nuit" else 0.35))                     # reflets verticaux du métal
    rideau = YT + 12 + 8 * np.sin(X * 0.33) + 5 * np.sin(X * 0.83 + 1.0) + 3 * np.sin(X * 1.7)
    nappe = m & (Y < rideau)                                                                  # la nappe épaisse du sommet
    _melange(c, nappe, lt(cu, 0.3), 0.6)
    _melange(c, m & (Y >= rideau) & (Y < rideau + 1.5), cl, 0.9)                              # bourrelet brillant
    _melange(c, m & (Y >= rideau + 1.5) & (Y < rideau + 3.5), cs, 0.5)                        # son ombre
    haut = m & (Y <= YT + 2)
    c.fill(haut, cl)                                                                          # bourrelet du sommet
    rr = R(81)
    for _ in range(70):                                                                       # gouttes figées
        x, y = rr.randint(60, 210), rr.randint(YT + 3, YB - 4)
        if m[y, x + c.ox]:
            L_ = rr.randint(3, 12)
            c.fill(m & c.mask_rect(x, y, x, y + L_), cl if rr.random() < 0.5 else cu)
            c.px(x, y + L_ + 1, cl)
    _melange(c, m & (X < xl(Y) + 8), (0, 0, 0), 0.28)
    _melange(c, m & (X > xr(Y) - 8), (0, 0, 0), 0.34)


def col(heure="jour", etat="vide"):
    """Le col entre les deux montagnes. etat : vide (passage ouvert), fer (blocs empilés), fini (fer + cuivre)."""
    c = _Px()
    sky = _ciel(c, heure, 306, seed=701)
    snap = c.a.copy()
    roc, sol = ROCS[heure], SOLS[heure]
    hz = CIELS[heure][1]
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    # le pays d'au-delà : crêtes lointaines dans la brume, vues par le passage
    for (base, amp, k, sd) in ((250, 22, 0.72, 11), (266, 16, 0.56, 12), (282, 12, 0.4, 13)):
        r3 = R(sd)
        pts, y_ = [], base
        for x in range(-105, 384, 5):
            y_ = max(base - amp, min(base + amp * 0.4, y_ + r3.uniform(-5, 5)))
            pts.append((x, y_))
        c.fill(c.mask_poly(pts + [(380, 300), (-105, 300)]), tuple(mix(dk(roc, 0.8), hz, k)))
    brume = c.mask_rect(-105, 270, 375, 302)
    _melange(c, brume, hz, np.clip((Y - 270) / 30.0, 0, 1) * 0.45)
    # le sol : plaine de terre, piste qui mène au passage
    terre = c.mask_rect(-105, YB, 375, 480)
    _peint(c, terre, (Y - YB) / (480 - YB), [(0.0, mix(sol, hz, 0.35)), (0.2, sol), (1.0, dk(sol, 0.62))], 10)
    rid = np.sin(np.maximum(Y - YB, 0) ** 0.72 * 2.3 + np.sin(X * 0.04) * 1.4) > 0.86
    _melange(c, terre & rid, dk(sol, 0.7), 0.22)
    d = (Y - YB) / (480 - YB)
    piste = terre & (np.abs(X - CX - 6 * np.sin(Y * 0.035)) < 9 + d * 86)
    _melange(c, piste, lt(sol, 0.3), 0.34)
    orn = piste & (np.abs(np.abs(X - CX - 6 * np.sin(Y * 0.035)) - (3 + d * 30)) < 0.6 + d * 2)
    _melange(c, orn, dk(sol, 0.6), 0.3)
    rr = R(702)
    for _ in range(150):                                                                     # cailloux, touffes sèches
        x, y = rr.randint(-104, 373), rr.randint(YB + 3, 476)
        s = (y - YB) / (480 - YB)
        if rr.random() < 0.6:
            w = 1 + s * 4
            c.fill(c.mask_ell(x, y, w, w * 0.5), tuple(dk(sol, 0.66)))
            c.fill(c.mask_rect(x - int(w * 0.5), y - int(w * 0.5), x, y - int(w * 0.5)), tuple(lt(sol, 0.3)))
        else:
            for j in range(int(2 + s * 5)):
                c.px(x + rr.randint(-2, 2), y - j, tuple(mix(sol, (110, 120, 60), 0.6)))
    # les deux montagnes
    g = [(-105, 196), (-80, 168), (-52, 142), (-18, 112), (8, 124), (34, 150), (56, 178), (float(xl(np.float32(YT))), YT)]
    bord_g = [(float(xl(np.float32(y))), y) for y in range(YT, YB + 1, 4)] + [(float(xl(np.float32(YB))), YB)]
    mg = c.mask_poly(_crete(g, 703) + bord_g + [(40, 306), (-105, 312)])
    dr = [(float(xr(np.float32(YT))), YT), (212, 176), (236, 146), (262, 120), (288, 104), (318, 128), (346, 122), (375, 150)]
    bord_d = [(float(xr(np.float32(y))), y) for y in range(YB, YT - 1, -4)]
    md = c.mask_poly([(375, 312), (230, 306), (float(xr(np.float32(YB))), YB)] + bord_d + _crete(dr, 704))
    loin_g = c.mask_poly(_crete([(-105, 150), (-70, 128), (-30, 160), (10, 200)], 705, 4) + [(10, 306), (-105, 306)])
    c.fill(loin_g & ~mg, tuple(mix(roc, hz, 0.5)))
    loin_d = c.mask_poly(_crete([(240, 190), (300, 150), (340, 136), (375, 118)], 706, 4) + [(375, 306), (240, 306)])
    c.fill(loin_d & ~md, tuple(mix(roc, hz, 0.5)))
    _roche(c, mg, roc, 707, lum=-1)
    _roche(c, md, dk(roc, 0.86), 708, lum=-1)
    _melange(c, mg & (X > xl(Y) - 10), (0, 0, 0), np.clip((X - xl(Y) + 10) / 10.0, 0, 1) * 0.34)   # parois du passage, à l'ombre
    _melange(c, md & (X < xr(Y) + 10), (0, 0, 0), np.clip((xr(Y) + 10 - X) / 10.0, 0, 1) * 0.42)
    for mm, sd in ((mg, 709), (md, 710)):                                                    # éboulis au pied des versants
        r4 = R(sd)
        for _ in range(40):
            x = r4.randint(-104, 373)
            ys_ = np.nonzero(mm[:, x + c.ox])[0]
            if len(ys_) and ys_.max() > 290:
                y = ys_.max() + r4.randint(-1, 5)
                w = r4.randint(2, 5)
                c.shape(c.mask_ell(x, y, w, w * 0.7), tuple(roc), tuple(dk(roc, 0.6)), tuple(lt(roc, 0.3)), band=1, ol=False)
    m = _masque_mur(c)
    if etat == "fer":
        _mur_fer(c, m, heure)
    elif etat == "fini":
        _mur_cuivre(c, m, heure)
    if etat != "vide":                                                                       # ombre portée au pied
        omb = terre & (Y <= YB + 7) & (X > xl(np.float32(YB)) - 2) & (X < xr(np.float32(YB)) + 8)
        _melange(c, omb, (0, 0, 0), 0.34 * (1 - (Y - YB) / 8.0))
        if heure in ("jour", "soir"):                                                        # pour l'échelle : un hameau au pied
            for (hx, w) in ((34, 9), (48, 7), (214, 8), (228, 10), (246, 7)):
                mur_ = tuple(mix((214, 190, 150), hz, 0.2))
                c.fill(c.mask_rect(hx, YB + 3, hx + w, YB + 8), mur_)
                c.fill(c.mask_rect(hx, YB + 3, hx + w, YB + 3), tuple(lt(mur_, 0.3)))
                c.fill(c.mask_rect(hx + 2, YB + 5, hx + 3, YB + 8), tuple(dk(mur_, 0.45)))
    if heure == "fin":
        c.tint(c.mask_rect(-105, 0, 375, 480), (255, 120, 60), 0.10)
    return lieux.relief(c, snap, sky), None


# ---------------------------------------------------------------- outils d'animation
def _calque(img):
    return Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))


def _pose(img, lay):
    lieux.pose_calque(img, lay)


def _smooth(k):
    k = min(1.0, max(0.0, k))
    return k * k * k * (k * (k * 6 - 15) + 10)


_IMG = {}


def _image(nom):
    """Image (480 x 480 x 3) d'un décor du film, gardée en mémoire."""
    if nom not in _IMG:
        bg = lieux.decor_large(nom)
        bg = bg[0] if isinstance(bg, tuple) else bg
        _IMG[nom] = np.array(bg.a, np.uint8)
    return _IMG[nom]


_GRILLE = []


def _grille():
    if not _GRILLE:
        xs = np.arange(-105, 375, dtype=np.float32)[None, :]
        ys = np.arange(0, 480, dtype=np.float32)[:, None]
        bay = BAYER[np.arange(480)[:, None] % 4, np.arange(480)[None, :] % 4]
        mur = (ys >= YT) & (ys <= YB) & (xs >= xl(ys) - 1) & (xs <= xr(ys) + 1)
        _GRILLE.append((xs, ys, bay, mur))
    return _GRILLE[0]


def _suffixe(bg):
    for h in ("soir", "nuit", "fin"):
        if bg.endswith("_" + h):
            return "_" + h
    return ""


# ---------------------------------------------------------------- la construction (18:96)
def anim_barrage_monte(t_debut=0.0, duree=10.0, suff=""):
    """Sur gog_col : les blocs de fer arrivent rangée par rangée (de gauche à droite), du pied jusqu'au niveau des deux
    versants ; un peu de poussière à chaque bloc posé ; de minuscules porteurs vont et viennent au pied."""
    rr = R(720)
    ordre = []
    n_tot = sum(len(bl) for (_, _, bl) in RANGS)
    i = 0
    for (y0, y1, bl) in RANGS:
        for (x0, x1) in bl:
            ordre.append((i / n_tot, x0, x1, y0, y1))
            i += 1
    porteurs = [(rr.uniform(0, 1), rr.uniform(0.5, 1.0), rr.choice((-1, 1))) for _ in range(26)]

    def f(img, u):
        if u < t_debut:
            return
        xs, ys, bay, mur = _grille()
        fer = _image("gog_barrage_fer" + suff)
        k = (u - t_debut) / duree
        a = np.zeros((480, 480, 4), np.uint8)
        a[..., :3] = fer
        if k >= 1.0:
            a[..., 3] = np.where(mur, 255, 0)
            _pose(img, Image.fromarray(a, "RGBA"))
            return
        kk = _smooth(k) * 0.35 + k * 0.65
        vis = np.zeros((480, 480), bool)
        lay_p = []
        for (s, x0, x1, y0, y1) in ordre:
            if s > kk:
                break
            age = (kk - s) * duree
            chute = max(0.0, 1 - age / 0.28)                         # le bloc descend sur sa rangée
            dy = int(round(-10 * chute))
            if dy == 0:
                vis[y0:y1, x0 + 105:x1 + 106] = True
            else:
                lay_p.append((x0, x1, y0 + dy, y1 + dy, y0))
            if age < 0.6:
                lay_p.append(("p", (x0 + x1) / 2, y1, age))
        a[..., 3] = np.where(vis & mur, 255, 0)
        lay = Image.fromarray(a, "RGBA")
        d = ImageDraw.Draw(lay)
        for it in lay_p:
            if it[0] == "p":                                         # poussière du bloc posé
                _, x, y, age = it
                al = int(150 * (1 - age / 0.6))
                r_ = 2 + age * 9
                d.ellipse([x + 105 - r_ * 1.5, y - r_ * 0.6, x + 105 + r_ * 1.5, y + r_ * 0.4], fill=(210, 190, 160, al))
            else:
                x0, x1, y0, y1, yy0 = it
                d.rectangle([x0 + 105, y0, x1 + 105, y1 - 1], fill=tuple(int(v) for v in fer[yy0 + 2, min(479, x0 + 108)]) + (255,))
                d.line([x0 + 105, y0, x1 + 105, y0], fill=(150, 160, 180, 255))
        for (ph, sp, sens) in porteurs:                              # porteurs minuscules au pied du barrage
            s = (ph + u * 0.07 * sp) % 1.0
            x = CX + sens * (10 + 120 * (1 - s))
            y = YB + 3 + 14 * (1 - s) ** 1.5
            X = x + 105
            d.rectangle([X, y - 3, X, y], fill=(60, 44, 40, 255))
            d.point((X, y - 4), fill=(196, 150, 116, 255))
            d.rectangle([X - 1, y - 6, X + 1, y - 5], fill=(70, 76, 92, 255))        # le bloc sur la tête
        _pose(img, lay)
    return f


def anim_barrage_feu(t_debut=0.0, duree=7.0, suff="", t_fin=None):
    """Le fer devient une fournaise : il rougit du pied vers le haut (soufflets au pied : flammes, braises, fumée),
    puis il est incandescent ; la lueur éclaire les deux versants. Reste jusqu'à t_fin (le cuivre prend la suite)."""
    rr = R(730)
    braises = [(rr.uniform(-1, 1), rr.uniform(0, 1), rr.uniform(0.5, 1.5)) for _ in range(150)]
    flammes = [(rr.uniform(-1, 1), rr.uniform(0, 6.28), rr.uniform(0.7, 1.3)) for _ in range(34)]

    def f(img, u):
        if u < t_debut or (t_fin is not None and u > t_fin):
            return
        xs, ys, bay, mur = _grille()
        fer = _image("gog_barrage_fer" + suff).astype(np.float32)
        k = min(1.0, (u - t_debut) / duree)
        tt = u - t_debut
        haut = (YB - ys) / (YB - YT)                                  # 0 au pied, 1 en haut
        ch = np.clip(_smooth(k) * 1.5 - haut * 0.5 + 0.06 * np.sin(xs * 0.3 + tt * 2) * k, 0, 1)   # chaleur locale
        pul = 0.06 * np.sin(tt * 3.1 + xs * 0.08) * k
        chaud = _stops([(0.0, (0, 0, 0)), (0.3, (150, 30, 20)), (0.6, (236, 96, 30)), (0.85, (255, 130, 40)),
                        (1.0, (255, 170, 60))], np.clip(ch + pul, 0, 1))
        q = np.clip(ch * 1.0, 0, 0.68)[..., None]
        rgb = fer * (1 - q) * 1.5 + chaud * q
        a = np.zeros((480, 480, 4), np.uint8)
        a[..., :3] = np.clip(rgb, 0, 255)
        a[..., 3] = np.where(mur, 255, 0)
        lay = Image.fromarray(a, "RGBA")
        lu = _calque(img)                                             # lueur sur les versants et le sol
        dl = ImageDraw.Draw(lu)
        for r_, al in ((150, 16), (110, 22), (70, 30)):
            dl.ellipse([CX + 105 - r_ * 1.2, (YT + YB) / 2 - r_, CX + 105 + r_ * 1.2, (YT + YB) / 2 + r_ * 1.2],
                       fill=(255, 130, 50, int(al * _smooth(k))))
        _pose(img, lu)
        d = ImageDraw.Draw(lay)
        for (a_, ph, sp) in flammes:                                  # flammes au pied (les soufflets attisent)
            x = CX + a_ * 44 + 105
            hfl = (7 + 9 * math.sin(tt * 7 * sp + ph) ** 2) * min(1.0, k * 3 + 0.3)
            d.polygon([(x - 3, YB + 3), (x + 3, YB + 3), (x + math.sin(tt * 5 + ph) * 2, YB + 3 - hfl)], fill=(255, 150, 40, 235))
            d.polygon([(x - 1.5, YB + 3), (x + 1.5, YB + 3), (x, YB + 3 - hfl * 0.55)], fill=(255, 236, 150, 245))
        for (a_, ph, sp) in braises:                                  # braises qui montent
            p = (ph + tt * 0.22 * sp) % 1.0
            x = CX + a_ * (40 + 30 * p) + 6 * math.sin(tt * 2 + ph * 20) + 105
            y = YB - p * (YB - YT + 40)
            al = int(255 * (1 - p) * min(1.0, k * 2.5))
            d.point((x, y), fill=(255, 200, 90, al))
        _pose(img, lay)
    return f


def anim_barrage_cuivre(t_debut=0.0, duree=8.0, suff=""):
    """Le cuivre fondu est versé d'en haut : des coulées éblouissantes descendent en langues inégales et recouvrent le
    fer ; derrière elles, le métal refroidit et prend sa couleur de cuivre ; vapeur ; à la fin, le barrage fini reste."""
    rr = R(740)
    ph_col = np.array([rr.uniform(0, 1) for _ in range(480)], np.float32)[None, :]
    vap = [(rr.uniform(-1, 1), rr.uniform(0, 1), rr.uniform(0.6, 1.4), rr.uniform(4, 9)) for _ in range(46)]

    def f(img, u):
        if u < t_debut:
            return
        xs, ys, bay, mur = _grille()
        fini = _image("gog_barrage" + suff).astype(np.float32)
        k = (u - t_debut) / duree
        a = np.zeros((480, 480, 4), np.uint8)
        if k >= 1.25:
            a[..., :3] = fini
            a[..., 3] = np.where(mur, 255, 0)
            _pose(img, Image.fromarray(a, "RGBA"))
            return
        tt = u - t_debut
        liss = (0.5 * np.sin(xs * 0.21 + 1.3) + 0.3 * np.sin(xs * 0.53) + 0.2 * np.sin(xs * 1.1 + 2)) * 0.5 + 0.5
        front = YT - 6 + (YB - YT + 30) * np.clip(k * (1.15 + 0.5 * liss) - 0.08 * ph_col, 0, 1.2)   # front de coulée
        dist = front - ys                                             # > 0 : déjà recouvert
        chaud = np.clip(1 - dist / (46 + 30 * liss), 0, 1)            # juste derrière le front : encore en fusion
        fin_ = _smooth((k - 0.9) / 0.35)                              # refroidissement général à la fin
        chaud = chaud * (1 - fin_)
        fus = _stops([(0.0, (0, 0, 0)), (0.25, (214, 80, 30)), (0.6, (255, 160, 50)), (1.0, (255, 246, 196))],
                     np.clip(chaud + 0.05 * np.sin(tt * 4 + xs * 0.2 + ys * 0.1), 0, 1))
        q = np.clip(chaud * 1.3, 0, 1)[..., None]
        rgb = fini * (1 - q) + fus * q
        a[..., :3] = np.clip(rgb, 0, 255)
        a[..., 3] = np.where(mur & (dist > 0), 255, 0)
        levre = mur & (dist > 0) & (dist < 2.5)
        a[levre, :3] = (255, 250, 214)
        lay = Image.fromarray(a, "RGBA")
        d = ImageDraw.Draw(lay)
        for (a_, ph, sp, r0) in vap:                                  # vapeur au-dessus du métal
            p = (ph + tt * 0.16 * sp) % 1.0
            x = CX + a_ * 60 + 8 * math.sin(tt + ph * 9) + 105
            y = YT + 10 - p * 60
            al = int(70 * (1 - p) * min(1.0, k * 4) * (1 - fin_))
            r_ = r0 * (0.6 + p)
            d.ellipse([x - r_, y - r_ * 0.7, x + r_, y + r_ * 0.7], fill=(236, 226, 214, al))
        _pose(img, lay)
    return f


# ---------------------------------------------------------------- la sortie (18:98-99, 21:96)
def _fissures(seed=750, n=7):
    """Fissures qui partent du pied et du milieu, en zigzag avec des branches : [(t_naissance, [(x, y), …]), …]."""
    rr = R(seed)
    out = []
    for i in range(n):
        x, y = CX + rr.uniform(-34, 34), rr.uniform(YB - 60, YB)
        ang = -math.pi / 2 + rr.uniform(-0.7, 0.7)
        pts = [(x, y)]
        for j in range(rr.randint(14, 26)):
            ang += rr.uniform(-0.7, 0.7)
            ang = max(-math.pi + 0.3, min(-0.3, ang))
            x += math.cos(ang) * rr.uniform(3, 7)
            y += math.sin(ang) * rr.uniform(3, 7)
            pts.append((x, y))
            if rr.random() < 0.22 and len(out) < 40:
                bx, by, ba = x, y, ang + rr.choice((-1, 1)) * rr.uniform(0.6, 1.2)
                br = [(bx, by)]
                for _ in range(rr.randint(3, 8)):
                    ba += rr.uniform(-0.5, 0.5)
                    bx += math.cos(ba) * rr.uniform(2, 6)
                    by += math.sin(ba) * rr.uniform(2, 6)
                    br.append((bx, by))
                out.append((i / n * 0.6 + j * 0.012, br))
        out.append((i / n * 0.6, pts))
    return out


def _silhouette(d, X, y, h, col, pas, lance, bras):
    """Un marcheur en silhouette, pieds en (X, y), hauteur h (pixels du dessin)."""
    if h < 2.2:
        d.point((X, y - 1), fill=col)
        return
    if h < 5:
        d.rectangle([X, y - h, X, y], fill=col)
        return
    w = max(1.0, h * 0.26)
    jambe = h * 0.42
    ec = math.sin(pas) * h * 0.16
    if h < 9:
        d.rectangle([X - w * 0.5, y - h + 1, X + w * 0.5, y - jambe], fill=col)
        d.line([X, y - jambe, X + ec, y], fill=col)
        d.line([X, y - jambe, X - ec, y], fill=col)
        d.rectangle([X - 0.5, y - h - 1, X + 0.5, y - h], fill=col)
    else:
        d.polygon([(X - w * 0.62, y - h * 0.82), (X + w * 0.62, y - h * 0.82), (X + w * 0.5, y - jambe + 1),
                   (X - w * 0.5, y - jambe + 1)], fill=col)
        lw = max(1, int(h * 0.09))
        d.line([X - w * 0.2, y - jambe, X + ec, y], fill=col, width=lw)
        d.line([X + w * 0.2, y - jambe, X - ec, y], fill=col, width=lw)
        r_ = h * 0.105
        d.ellipse([X - r_, y - h, X + r_, y - h + 2 * r_], fill=col)
        d.line([X + w * 0.5, y - h * 0.76, X + w * 0.5 - ec * 0.9, y - h * 0.46], fill=col, width=lw)
        if bras:                                                     # un bras levé
            d.line([X - w * 0.5, y - h * 0.78, X - w * 1.1, y - h * 1.08], fill=col, width=lw)
    if lance and h >= 5:
        d.line([X + w, y - h * 0.3, X + w + h * 0.1, y - h * 1.45], fill=col)


class Maree:
    """La marée humaine : des milliers de marcheurs qui sortent d'un point lointain et se déploient vers la caméra."""

    def __init__(s, n=4200, seed=760, x0=CX, y0=YB - 2, demi0=30, demi1=330, y1=376, vitesse=0.085, periode=11.0):
        rr = R(seed)
        s.a = np.array([rr.uniform(-1, 1) * abs(rr.uniform(-1, 1)) ** 0.25 for _ in range(n)], np.float32)
        s.tb = np.array([rr.uniform(0, periode) for _ in range(n)], np.float32)
        s.sp = np.array([rr.uniform(0.75, 1.3) for _ in range(n)], np.float32)
        s.ph = np.array([rr.uniform(0, 6.28) for _ in range(n)], np.float32)
        s.typ = np.array([rr.random() for _ in range(n)], np.float32)
        s.teinte = [rr.choice([(24, 16, 16), (34, 22, 20), (18, 14, 18), (44, 28, 22), (30, 20, 26)]) for _ in range(n)]
        s.x0, s.y0, s.demi0, s.demi1, s.y1, s.v, s.per = x0, y0, demi0, demi1, y1, vitesse, periode

    def dessine(s, d, tt, front=1.0, alpha=255, voile=None):
        """tt : secondes depuis le début de la sortie ; front : jusqu'où la marée est arrivée (0 = au col, 1 = partout)."""
        p = ((tt - s.tb) % s.per) * s.v * s.sp                        # avancée de chacun (0 = au col … 1 = à la caméra)
        ne = (tt - s.tb) >= 0                                         # pas encore sorti au premier passage
        ok = ne & (p <= front * 1.02) & (p < 1.06)
        idx = np.nonzero(ok)[0]
        idx = idx[np.argsort(p[idx])]
        for i in idx:
            pi = float(p[i])
            e = pi ** 1.25
            y = s.y0 + (s.y1 - s.y0) * e
            x = s.x0 + float(s.a[i]) * (s.demi0 + (s.demi1 - s.demi0) * pi ** 1.25) + 2.0 * math.sin(tt * 0.9 + float(s.ph[i]))
            h = 2.0 + 24.0 * pi ** 1.7
            col = s.teinte[i]
            if voile is not None and pi < 0.4:                        # au loin : noyés dans la poussière
                kv = (0.4 - pi) * 1.5
                col = tuple(int(c_ * (1 - kv) + v_ * kv) for c_, v_ in zip(col, voile))
            ty = float(s.typ[i])
            _silhouette(d, x + 105, y, h, col + (alpha,), tt * (7.5 - 3 * pi) * float(s.sp[i]) + float(s.ph[i]),
                        ty < 0.3, 0.3 <= ty < 0.42)
            if h >= 9:                                                # liseré de lumière (le soleil est derrière eux)
                d.point((x + 105 - h * 0.08, y - h + 1), fill=(236, 150, 90, alpha))


SENTIERS = [  # « de chaque hauteur » : par où ils dévalent les deux versants (du haut vers la plaine)
    [(-60, 96), (-40, 130), (-52, 170), (-20, 214), (-34, 262), (0, 300), (-30, 380), (-80, 470)],
    [(8, 60), (26, 104), (16, 150), (44, 196), (36, 250), (64, 296), (70, 372), (20, 478)],
    [(-100, 150), (-84, 196), (-96, 244), (-70, 290), (-104, 350)],
    [(262, 70), (250, 116), (268, 160), (236, 206), (252, 256), (214, 298), (210, 372), (270, 478)],
    [(322, 80), (300, 128), (318, 176), (290, 226), (306, 270), (270, 302), (300, 384), (350, 472)],
    [(372, 120), (352, 170), (366, 220), (340, 268), (372, 330)],
]


def _long(pts):
    L = [0.0]
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L.append(L[-1] + math.hypot(x1 - x0, y1 - y0))
    return L


def _sur(pts, L, s):
    """Point à la fraction s (0..1) du sentier."""
    cible = s * L[-1]
    for i in range(len(pts) - 1):
        if cible <= L[i + 1]:
            k = (cible - L[i]) / max(1e-6, L[i + 1] - L[i])
            return pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k
    return pts[-1]


class Hauteurs:
    """Ceux qui dévalent les versants : des files serrées de petites silhouettes le long des sentiers."""

    def __init__(s, n=150, seed=770, sentiers=SENTIERS):
        rr = R(seed)
        s.files = []
        for pts in sentiers:
            L = _long(pts)
            s.files.append((pts, L, [(rr.uniform(0, 1), rr.uniform(-3.5, 3.5), rr.uniform(0.8, 1.25), rr.uniform(0, 6.28),
                                      rr.random()) for _ in range(n)]))

    def dessine(s, d, tt, front=1.0, alpha=255, vitesse=0.06):
        for (pts, L, gens) in s.files:
            for (ph, dx, sp, ph2, ty) in gens:
                av = tt * vitesse * sp
                if av < ph:                                           # pas encore parti (la file se remplit par le haut)
                    continue
                q = (av - ph) % 1.0
                if q > front:
                    continue
                x, y = _sur(pts, L, q)
                e = max(0.0, (y - 60) / 420.0)
                h = 2.2 + 9 * e ** 1.6 + (22 * max(0.0, (y - 330) / 150.0) ** 1.5)
                _silhouette(d, x + dx * (0.5 + e) + 105, y, h, (26, 18, 18, alpha), tt * 7 * sp + ph2, ty < 0.25, False)


def anim_barrage_tombe(t_debut=0.0, duree=13.0, suff="_fin"):
    """Sur gog_barrage_fin. (1) Des fissures montent dans le métal, la poussière ruisselle. (2) Le barrage est nivelé :
    il s'affaisse colonne par colonne, des pans tombent, un nuage de poussière roule vers nous. (3) Dans la poussière,
    ils sortent : une marée de silhouettes qui déferle par le passage et dévale chaque hauteur — et ne s'arrête plus.
    Pas d'éclair, pas de secousse de l'image."""
    rr = R(780)
    fiss = _fissures()
    xs0 = np.arange(-105, 375, dtype=np.float32)
    retard = np.array([rr.uniform(0, 1) for _ in range(480)], np.float32)
    for _ in range(5):                                                # retard de chaque colonne, lissé (pans entiers)
        retard = (np.roll(retard, 1) + retard + np.roll(retard, -1)) / 3
    retard = (retard - retard.min()) / max(1e-6, retard.max() - retard.min())
    retard = 0.75 * retard + 0.25 * np.abs(xs0 - CX) / 80.0           # le centre cède d'abord
    debris = [(rr.uniform(-1, 1), rr.uniform(0, 1), rr.uniform(-18, 18), rr.uniform(2, 6), rr.uniform(0.2, 1.0),
               rr.random()) for _ in range(240)]
    nuages = [(rr.uniform(-1, 1), rr.uniform(0, 1), rr.uniform(10, 30), rr.uniform(0, 6.28), rr.uniform(0.6, 1.3),
               rr.random()) for _ in range(120)]
    filets = [(rr.uniform(-1, 1), rr.uniform(0, 1), rr.uniform(0.6, 1.5)) for _ in range(60)]
    cailloux = [(rr.choice((-1, 1)), rr.uniform(0, 1), rr.uniform(0, 1), rr.uniform(0.7, 1.4)) for _ in range(50)]
    maree = Maree()
    hauteurs = Hauteurs()
    T1, T2, T3 = 0.24, 0.50, 0.40                                     # fin des fissures seules, fin de la chute, début de la sortie
    POUSS = (206, 160, 122)

    def f(img, u):
        if u < t_debut:
            return
        xs, ys, bay, mur = _grille()
        tt = u - t_debut
        k = tt / duree
        vide = _image("gog_col" + suff)
        fini = _image("gog_barrage" + suff)
        # --- (2) le haut du barrage descend, colonne par colonne
        kc = np.clip((k - T1) / (T2 - T1) * 1.45 - 0.45 * retard, 0, 1)
        kc = kc * kc * (3 - 2 * kc)
        haut = YT + (YB - YT + 2) * kc[None, :]
        tombe = mur & (ys < haut)
        a = np.zeros((480, 480, 4), np.uint8)
        a[..., :3] = vide
        a[..., 3] = np.where(tombe, 255, 0)
        if k < T2 + 0.05:                                             # arête vive du métal qui cède
            arete = mur & (ys >= haut) & (ys < haut + 2) & (kc[None, :] > 0.01)
            a[arete, :3] = (255, 214, 150)
            a[arete, 3] = 255
        lay = Image.fromarray(a, "RGBA")
        d = ImageDraw.Draw(lay)
        # --- (1) fissures (sur ce qui reste debout)
        kf = min(1.0, k / T1)
        if k < T2:
            for (tn, pts) in fiss:
                if kf <= tn:
                    continue
                n_vis = int(len(pts) * min(1.0, (kf - tn) / 0.3))
                for (p0, p1) in zip(pts[:n_vis], pts[1:n_vis + 1]):
                    xi = int(min(479, max(0, p1[0] + 105)))
                    if p1[1] < haut[0, xi] or not (YT <= p1[1] <= YB) or not (YT <= p0[1] <= YB):
                        continue
                    if not (float(xl(np.float32(p1[1]))) + 1 < p1[0] < float(xr(np.float32(p1[1]))) - 1
                            and float(xl(np.float32(p0[1]))) + 1 < p0[0] < float(xr(np.float32(p0[1]))) - 1):
                        continue
                    d.line([p0[0] + 105, p0[1], p1[0] + 105, p1[1]], fill=(30, 14, 12, 255), width=1)
            for (a_, ph, sp) in filets:                               # filets de poussière qui ruissellent des fissures
                p = (ph + tt * 0.5 * sp) % 1.0
                x = CX + a_ * 46 + 105
                y = YT + 20 + (ph * 97 % 1.0) * 80 + p * 44
                if y < YB and kf > ph * 0.8:
                    d.line([x, y, x, y + 3], fill=POUSS + (int(170 * (1 - p)),))
        # --- débris qui tombent pendant la chute
        if T1 < k < T2 + 0.14:
            for (a_, t0_, vx, w, g_, ty) in debris:
                kd = (k - T1) / (T2 - T1) - t0_ * 1.1
                if kd < 0 or kd > 0.55:
                    continue
                td = kd * (T2 - T1) * duree
                x = CX + a_ * 50 + vx * td + 105
                y = YT + (YB - YT) * min(1.0, t0_ * 0.9) * 0.6 + 60 * g_ * td * td + 6 * td
                if y > YB + 12:
                    continue
                col = (150, 80, 46, 255) if ty < 0.5 else ((70, 44, 40, 255) if ty < 0.85 else (236, 150, 86, 255))
                d.rectangle([x, y, x + w, y + w * 0.7], fill=col)
        # --- cailloux qui roulent des versants
        if k < 0.8:
            for (cote, ph, yy, sp) in cailloux:
                p = (ph + tt * 0.3 * sp) % 1.0
                y = 140 + yy * 110 + p * 70
                x = (float(xl(np.float32(y))) - 14 - 22 * yy + p * 16) if cote < 0 else (float(xr(np.float32(y))) + 14 + 22 * yy - p * 16)
                d.rectangle([x + 105, y, x + 106, y + 1], fill=(64, 40, 36, int(255 * (1 - p))))
        _pose(img, lay)
        # --- (3) ils sortent
        if k > T3:
            ts = tt - T3 * duree
            front = min(1.0, 0.06 + ts / 9.5)
            lay2 = _calque(img)
            d2 = ImageDraw.Draw(lay2)
            masse = _smooth(ts / 3.0)                                 # au col : des rangs serrés, à perte de vue
            if masse > 0:
                w0 = (float(xr(np.float32(YB))) - float(xl(np.float32(YB)))) / 2 - 2
                for r_ in range(9):
                    yy = YB - 5 + r_ * 1.3
                    ton = int(58 - r_ * 3)
                    colr = (ton + 44, ton + 14, ton + 4, int(255 * masse))
                    for j in range(int(w0 * 2 / 2) + 1):
                        xx = CX - w0 + j * 2 + (r_ % 2)
                        hop = 1 if math.sin(tt * 6.0 + j * 2.3 + r_ * 1.9) > 0.2 else 0
                        d2.rectangle([xx + 105, yy - 2 - hop, xx + 105, yy], fill=colr)
                    if r_ % 3 == 0:                                   # quelques lances
                        for j in range(9):
                            xx = CX - w0 + 2 * w0 * ((j * 0.381966 + r_ * 0.21) % 1.0)
                            d2.line([xx + 105, yy - 2, xx + 105, yy - 6 - (j % 3)], fill=colr)
            hauteurs.dessine(d2, ts, front=min(1.0, 0.08 + ts / 8.0))
            maree.dessine(d2, ts, front=front, voile=POUSS)
            _pose(img, lay2)
        # --- la poussière (par-dessus tout) : elle naît au pied, roule vers nous, puis se dissipe
        kp = (k - T1 * 0.7) / 0.5
        if kp > 0:
            force = min(1.0, kp * 1.6) * (1.0 - 0.9 * _smooth((k - 0.55) / 0.5))
            dens = np.zeros((480, 480), np.float32)
            for (a_, ph, r0, ph2, sp, ty) in nuages:
                age = (kp * 1.3 - ph * 0.9)
                if age < 0:
                    continue
                e = min(1.0, age)
                x = CX + a_ * (36 + 200 * e) + 10 * math.sin(tt * 0.5 + ph2)
                y = YB - 6 - 62 * e * (0.15 + ty * 0.9) + 44 * e * e * (1 - ty) + 3 * math.sin(tt * 0.7 + ph2)
                r_ = r0 * (0.4 + 0.9 * e) * sp
                x0_, x1_ = int(max(0, x + 105 - r_ * 2.2)), int(min(480, x + 105 + r_ * 2.2))
                y0_, y1_ = int(max(0, y - r_ * 1.6)), int(min(480, y + r_ * 1.6))
                if x1_ <= x0_ or y1_ <= y0_:
                    continue
                gx_ = (xs[:, x0_:x1_] - x) / (r_ * 1.25)
                gy_ = (ys[y0_:y1_, :] - y) / (r_ * 0.85)
                dens[y0_:y1_, x0_:x1_] += np.exp(-(gx_ ** 2 + gy_ ** 2) * 1.6) * (1 - 0.5 * e) * (0.9 if ty > 0.4 else 0.6)
            dens = (1.0 - np.exp(-dens * 0.55)) * force
            a3 = np.zeros((480, 480, 4), np.uint8)
            n1 = dens > 0.16 + bay * 0.34                             # voile léger (tramé)
            n2 = dens > 0.52 + bay * 0.30                             # cœur du nuage
            n3 = dens > 0.80 + bay * 0.22                             # volutes claires
            a3[n1] = (176, 124, 96, 255)
            a3[n2] = POUSS + (255,)
            a3[n3] = (238, 198, 152, 255)
            _pose(img, Image.fromarray(a3, "RGBA"))
    return f


# ---------------------------------------------------------------- registre
_DEC = {}
for _h in HEURES:
    _s = "" if _h == "jour" else "_" + _h
    _DEC["gog_col" + _s] = (lambda h=_h: col(h, "vide"))
    _DEC["gog_barrage_fer" + _s] = (lambda h=_h: col(h, "fer"))
    _DEC["gog_barrage" + _s] = (lambda h=_h: col(h, "fini"))
egypte.enregistre(_DEC, sol_haut={n: (330, 100) for n in _DEC})
lieux.LUMIERES["gog_col_nuit"] = lieux.LUMIERES["gog_barrage_fer_nuit"] = lieux.LUMIERES["gog_barrage_nuit"] = (lieux.NUIT, [])


ANNOTATIONS = ("barrage_monte", "barrage_feu", "barrage_cuivre", "barrage_tombe", "horde_col")


def anim_horde_col(t_debut=0.0, duree=12.0):
    """Sur gog_col (passage ouvert) : au loin, ils sortent par le passage et se répandent un peu, puis s'effacent
    (ce que racontait le peuple : « par ce passage, ils sortaient »)."""
    mar = Maree(n=900, seed=765, demi0=24, demi1=58, y1=322, vitesse=0.06, periode=9.0)

    def f(img, u):
        if u < t_debut or u > t_debut + duree:
            return
        tt = u - t_debut
        al = int(255 * min(1.0, tt / 1.5) * min(1.0, (duree - tt) / 2.0))
        lay = _calque(img)
        mar.dessine(ImageDraw.Draw(lay), tt, front=min(0.5, 0.05 + tt / 12.0), alpha=al)
        _pose(img, lay)
    return f


def _annotation1(sc, k_, mots, t, bg):
    """Annotations posées sur un mot : {barrage_monte 10} {barrage_feu 7} {barrage_cuivre 8} {barrage_tombe 13}."""
    d_ = next((float(m_.rstrip("s").replace(",", ".")) for m_ in mots[1:] if m_.rstrip("s").replace(",", "").replace(".", "").isdigit()), None)
    suff = _suffixe(bg)
    if k_ == "barrage_monte":
        sc.anims.append(anim_barrage_monte(t, d_ or 10.0, suff))
    elif k_ == "barrage_feu":
        sc._gog_feu = [None]
        box = sc._gog_feu
        f0 = anim_barrage_feu(t, d_ or 7.0, suff)
        sc.anims.append(lambda img, u, f0=f0, box=box: None if (box[0] is not None and u > box[0]) else f0(img, u))
    elif k_ == "barrage_cuivre":
        dd = d_ or 8.0
        if getattr(sc, "_gog_feu", None):
            sc._gog_feu[0] = t + dd * 1.25                            # le feu s'efface quand le cuivre a tout recouvert
        sc.anims.append(anim_barrage_cuivre(t, dd, suff))
    elif k_ == "barrage_tombe":
        sc.anims.append(anim_barrage_tombe(t, d_ or 13.0, suff or "_fin"))
    elif k_ == "horde_col":
        sc.anims.append(anim_horde_col(t, d_ or 12.0))
    return True


import decors_gog2 as _g2   # noqa: E402  (la suite : autres décors, options et annotations)

ANNOTATIONS = ANNOTATIONS + tuple(_g2.ANNOTATIONS)


def option(sc, o, bg):
    """Options de bloc du film Gog et Magog (appelée par scenario.py pour chaque option) ; True si reconnue."""
    return _g2.option(sc, o, bg)


def annotation(sc, k_, mots, t, bg):
    if k_ in _g2.ANNOTATIONS:
        return _g2.annotation(sc, k_, mots, t, bg)
    return _annotation1(sc, k_, mots, t, bg)
