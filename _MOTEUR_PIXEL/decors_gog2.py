# FILM HORS-SÉRIE « GOG ET MAGOG » (10/11/2026) — suite : les autres décors et animations (voir decors_gog.py).
# Décors : gog_hauteurs (+ _fin), gog_forteresse (+ _fin), gog_lac (+ _fin : lit asséché ; option « lac » = plein),
#   gog_tour_nuit / _aube (vu du Mont : la corniche, la plaine en bas), gog_rempart_aube (vu du rempart),
#   gog_plaine_aube / gog_plaine, gog_miroir, gog_benie, gog_couchant, gog_levant, gog_medine_nuit, gog_mur_pres,
#   gog_mille, gog_kaaba, gog_derriere (l'autre côté du barrage, la nuit).
# Options de bloc : passage (une foule de silhouettes passe au premier plan), colonne (l'armée du roi, au loin),
#   plaine_horde / plaine_fige (la plaine couverte, vue d'en haut : vivante / immobile), bande (au loin, sur la plaine),
#   lac (le lac plein), tawaf, escalade, horde_hauteurs (ils dévalent chaque colline), contourne (autour de la ville).
# Annotations : {lac_bu N} {fleches N} {trou} {mille N} {dix N} {oiseaux_emportent N} {horde_fige} {horde_hauteurs}
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import egypte
import film
import lieux
import decors_gog as G
from decors_gog import (_Px, _peint, _melange, _bay, _stops, _roche, _crete, _calque, _pose, _smooth, _silhouette,
                        CX, YT, YB)
from lieux import R, dk, lt, mix

G.CIELS["aube"] = ((92, 104, 160), (250, 196, 156))
G.ROCS["aube"] = (140, 110, 108)
G.SOLS["aube"] = (196, 160, 130)
VERT = (86, 150, 74)

film.orbe("DHOUL_QARNAYN", "DHOUL-QARNAYN", "or_", r=10, hauteur=42)   # roi juste et croyant (prophète ou non : divergence)
film.orbe("ISSA", "'ISSA", "or_", r=10, hauteur=42)
film.VOIX_SEULES.add("UN_DES_LEURS")                                # l'un de Ya'jouj et Ma'jouj : une voix, jamais un visage
film.orbe("ZAYNAB", "ZAYNAB", "rose", r=9, hauteur=40)                # Zaynab bint Jahch, épouse du Prophète


def _fond(c, heure, y1, soleil=None, r_sol=11, seed=5):
    """Ciel simple (dégradé tramé, étoiles la nuit, soleil / lune au choix)."""
    top, bot = G.CIELS[heure]
    sky = c.mask_rect(-105, 0, 375, y1)
    Y = c.yy.astype(np.float32)
    _peint(c, sky, (Y - 90) / max(1, y1 - 90), [(0.0, top), (0.6, mix(top, bot, 0.6)), (1.0, bot)], 12)
    rr = R(seed)
    if heure == "nuit":
        for _ in range(170):
            x, y = rr.randint(-105, 374), rr.randint(96, max(100, y1 - 16))
            c.px(x, y, (232, 232, 255) if rr.random() < 0.3 else (130, 138, 200))
    if soleil:
        col = dict(aube=(255, 214, 160), jour=(255, 248, 214), soir=(255, 190, 110), fin=(255, 200, 130),
                   nuit=(250, 240, 206))[heure]
        c.glow(soleil[0], soleil[1], r_sol * 6, col, 0.34 if heure != "nuit" else 0.16, m=sky)
        disque = c.mask_ell(soleil[0], soleil[1], r_sol, r_sol) & sky
        if heure == "nuit":
            disque &= ~c.mask_ell(soleil[0] + 4, soleil[1] - 3, r_sol - 1, r_sol - 1)
        c.fill(disque, lt(col, 0.3))
    if heure in ("jour", "aube"):
        for k in range(6):
            x0, yb = rr.randint(-100, 330), rr.randint(108, max(112, y1 - 60))
            for j in range(4):
                nu = sky & c.mask_ell(x0 + j * 11, yb + (j % 2) * 2, rr.randint(9, 16), rr.randint(3, 5))
                _melange(c, nu, (250, 252, 255) if heure == "jour" else (255, 226, 206), 0.7)
    if heure == "fin":
        X = c.xx.astype(np.float32)
        for k in range(8):
            yb = 104 + k * 14 + rr.randint(-4, 4)
            bande = sky & (np.abs(Y - yb - 5 * np.sin(X * 0.02 + k)) < 2.4 + 1.6 * np.sin(X * 0.045 + k * 2)) & (_bay(c) < 0.72)
            _melange(c, bande, (96, 46, 44) if k % 2 else (250, 160, 96), 0.42)
    return sky


def _terre(c, m, y0, y1, sol, hz, seed, rides=True, cailloux=90):
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    _peint(c, m, (Y - y0) / max(1, y1 - y0), [(0.0, mix(sol, hz, 0.4)), (0.25, sol), (1.0, dk(sol, 0.62))], 10)
    if rides:
        rid = np.sin(np.maximum(Y - y0, 0) ** 0.72 * 2.3 + np.sin(X * 0.04) * 1.4) > 0.86
        _melange(c, m & rid, dk(sol, 0.7), 0.2)
    rr = R(seed)
    for _ in range(cailloux):
        x, y = rr.randint(-104, 373), rr.randint(int(y0) + 2, int(y1) - 3)
        if not m[y, x + c.ox]:
            continue
        s = (y - y0) / max(1, y1 - y0)
        w = 1 + s * 3.5
        c.fill(c.mask_ell(x, y, w, w * 0.5) & m, tuple(dk(sol, 0.66)))
        c.fill(c.mask_rect(x - int(w * 0.5), y - int(w * 0.5), x, y - int(w * 0.5)) & m, tuple(lt(sol, 0.3)))


def _collines(c, base, amp, seed, col, y_bas, pas=5, lisse=5):
    r3 = R(seed)
    pts, y_ = [], base
    for x in range(-105, 384, pas):
        y_ = max(base - amp, min(base + amp * 0.35, y_ + r3.uniform(-lisse, lisse)))
        pts.append((x, y_))
    m = c.mask_poly(pts + [(380, y_bas), (-105, y_bas)])
    c.fill(m, tuple(col))
    c.fill(m & ~np.roll(m, 1, axis=0), tuple(lt(col, 0.2)))
    return m


# ---------------------------------------------------------------- les collines (« de chaque hauteur »)
HILLS = [(232, 34, 58.0, 0.4, 2.1), (258, 30, 46.0, 2.2, 0.7), (288, 26, 38.0, 4.0, 1.3)]     # (base, amp, longueur, ph, ph2)


def _ridge(i, x):
    base, amp, wl, ph, ph2 = HILLS[i]
    return base - amp * (0.5 + 0.5 * np.sin(x / wl + ph)) - 0.28 * amp * np.sin(x / (wl * 0.37) + ph2)


def hauteurs(heure="fin"):
    """Des collines à perte de vue, en trois plans, sous le ciel de la fin des temps ; un vallon au premier plan."""
    c = _Px()
    sky = _fond(c, heure, 250, soleil=(250, 150), r_sol=13, seed=801)
    snap = c.a.copy()
    roc, sol, hz = G.ROCS[heure], G.SOLS[heure], G.CIELS[heure][1]
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    _collines(c, 214, 20, 802, mix(dk(roc, 0.8), hz, 0.6), 320)
    for i, k in enumerate((0.42, 0.22, 0.06)):
        m = (Y >= _ridge(i, X)) & (Y < 480)
        col = mix(mix(roc, sol, 0.35 + 0.2 * i), hz, k)
        _peint(c, m, (Y - _ridge(i, X)) / 70.0, [(0.0, lt(col, 0.14)), (0.3, col), (1.0, dk(col, 0.6))], 8)
        pli = np.sin(X * 0.21 + (Y - _ridge(i, X)) * 0.13 + i) > 0.9                        # plis du terrain
        _melange(c, m & pli, dk(col, 0.6), 0.2)
        c.fill(m & ~np.roll(m, 1, axis=0), tuple(lt(col, 0.3)))
    bas = c.mask_rect(-105, 322, 375, 480)
    _terre(c, bas, 322, 480, sol, mix(sol, hz, 0.3), 803)
    for (x, y, w, h) in ((-70, 330, 16, 9), (310, 336, 20, 11), (40, 420, 12, 7)):
        r_ = c.mask_ell(x, y, w, h) & c.mask_rect(x - w, y - h, x + w, y + 1)
        c.shape(r_, tuple(roc), tuple(dk(roc, 0.6)), tuple(lt(roc, 0.3)), band=2, ol=False)
    if heure == "fin":
        c.tint(c.mask_rect(-105, 0, 375, 480), (255, 120, 60), 0.10)
    return lieux.relief(c, snap, sky), None


class Coulees:
    """Ils dévalent chaque colline : des milliers de points qui passent les crêtes et coulent le long des pentes."""

    def __init__(s, n=2600, seed=810):
        rr = R(seed)
        s.ag = [(rr.choice((0, 0, 1, 1, 1, 2, 2, 2, 2)), rr.uniform(-105, 375), rr.uniform(0, 1), rr.uniform(0.7, 1.3),
                 rr.uniform(-6, 6), rr.random()) for _ in range(n)]
        s.ag.sort(key=lambda a: a[0])

    def dessine(s, d, tt, alpha=255):
        for (i, x0, ph, sp, drift, ty) in s.ag:
            delai = i * 1.6
            av = (tt - delai) * 0.16 * sp
            if av < ph:
                continue
            q = (av - ph) % 1.0
            L = (26, 32, 40)[i]
            x = x0 + drift * q
            y0 = float(_ridge(i, np.float32(x0)))
            y = y0 - 1 + q * L
            if i < 2 and y > float(_ridge(i + 1, np.float32(x))) + 1:          # caché par la colline de devant
                continue
            h = (2, 3, 4.6)[i]
            ton = (58, 44, 30)[i]
            col = (ton + 20, ton + 2, ton - 4, alpha)
            if h < 4:
                d.rectangle([x + 105, y - h, x + 105, y], fill=col)
            else:
                _silhouette(d, x + 105, y, h + 1.5 * q, col, tt * 7 * sp + ph * 9, ty < 0.3, False)


def anim_horde_hauteurs(t_debut=0.0, maree=True):
    coul = Coulees()
    mar = G.Maree(n=2600, seed=811, x0=CX, y0=318, demi0=200, demi1=360, y1=378, vitesse=0.075, periode=12.0)

    def f(img, u):
        if u < t_debut:
            return
        tt = u - t_debut
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        coul.dessine(d, tt)
        if maree and tt > 4.5:
            mar.dessine(d, tt - 4.5, front=min(1.0, 0.1 + (tt - 4.5) / 8.0), voile=(170, 110, 84))
        _pose(img, lay)
    return f


def anim_fleches(t_debut=0.0, duree=9.0):
    """Des volées de flèches montent vers le ciel (traits fins), disparaissent, puis retombent : pointes rouges."""
    rr = R(820)
    fl = [(rr.uniform(-60, 330), rr.uniform(0, 0.3), rr.uniform(-0.5, 0.5), rr.uniform(0.85, 1.2)) for _ in range(150)]

    def f(img, u):
        if u < t_debut or u > t_debut + duree + 6:
            return
        k = (u - t_debut) / duree
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        for (x0, t0_, vx, sp) in fl:
            a = (k - t0_) / 0.26 * sp                                  # montée
            if 0 <= a <= 1:
                y = 318 - 240 * (1 - (1 - a) ** 2)
                x = x0 + vx * 30 * a + 105
                d.line([x, y, x - vx * 2, y + 7], fill=(40, 26, 22, 255))
                d.point((x, y), fill=(220, 200, 170, 255))
            b = (k - 0.52 - t0_) / 0.22 * sp                           # retour
            if 0 <= b:
                bb = min(1.0, b)
                y = 90 + (236 + (x0 * 7 % 80)) * bb * bb
                x = x0 + vx * 30 + 12 * vx * bb + 105
                d.line([x, y - 8, x, y], fill=(52, 30, 26, 255))
                d.line([x, y - 3, x, y], fill=(200, 24, 28, 255))        # la pointe teinte de sang
                if bb >= 1.0:
                    d.point((x, y + 1), fill=(120, 20, 22, 255))
        _pose(img, lay)
    return f


# ---------------------------------------------------------------- la ville fortifiée
def forteresse(heure="fin"):
    """Une ville derrière ses murailles (tours, créneaux, grande porte fermée, toits et coupoles), dans la plaine."""
    c = _Px()
    sky = _fond(c, heure, 304, soleil=(-40, 170), r_sol=12, seed=831)
    snap = c.a.copy()
    roc, sol, hz = G.ROCS[heure], G.SOLS[heure], G.CIELS[heure][1]
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    _collines(c, 268, 26, 832, mix(dk(roc, 0.8), hz, 0.55), 310)
    _collines(c, 288, 16, 833, mix(roc, hz, 0.35), 310)
    terre = c.mask_rect(-105, 302, 375, 480)
    _terre(c, terre, 302, 480, sol, mix(sol, hz, 0.3), 834)
    pierre = mix((200, 170, 130), hz, 0.18) if heure != "nuit" else (70, 70, 100)
    rr = R(835)
    for i in range(16):                                                 # la ville derrière le mur : toits, coupoles
        x = 46 + i * 15 + rr.randint(-3, 3)
        h = rr.randint(10, 30)
        mm = tuple(mix(lt(pierre, 0.1), hz, 0.25))
        c.fill(c.mask_rect(x, 240 - h, x + 12, 244), mm)
        c.fill(c.mask_rect(x, 240 - h, x + 12, 240 - h), tuple(lt(mm, 0.3)))
        c.fill(c.mask_rect(x + 9, 240 - h, x + 12, 244), tuple(dk(mm, 0.8)))
        if rr.random() < 0.4:
            c.fill(c.mask_ell(x + 6, 240 - h, 6, 5) & c.mask_rect(x, 230 - h, x + 12, 240 - h), tuple(dk(mm, 0.9)))
        elif rr.random() < 0.5:
            c.fill(c.mask_rect(x + 4, 246 - h, x + 6, 250 - h), tuple(dk(mm, 0.45)))
    c.fill(c.mask_rect(198, 186, 206, 244), tuple(mix(lt(pierre, 0.1), hz, 0.2)))          # une haute tour
    c.fill(c.mask_rect(196, 196, 208, 198), tuple(dk(pierre, 0.7)))
    c.fill(c.mask_poly([(197, 186), (207, 186), (202, 174)]), tuple(dk(pierre, 0.7)))
    mur = c.mask_rect(36, 240, 306, 304)
    _peint(c, mur, (Y - 240) / 64.0, [(0.0, lt(pierre, 0.12)), (0.4, pierre), (1.0, dk(pierre, 0.62))], 8)
    for y in range(244, 304, 6):                                         # assises de pierre
        off = 6 if (y // 6) % 2 else 0
        c.fill(mur & c.mask_rect(36, y, 306, y), tuple(dk(pierre, 0.74)))
        for x in range(36 + off, 306, 12):
            c.fill(mur & c.mask_rect(x, y, x, y + 5), tuple(dk(pierre, 0.8)))
    for x in range(36, 306, 8):                                          # créneaux
        c.fill(c.mask_rect(x, 235, x + 4, 240), tuple(lt(pierre, 0.1)))
        c.fill(c.mask_rect(x + 4, 235, x + 4, 240), tuple(dk(pierre, 0.7)))
    for tx in (30, 106, 196, 296):                                       # tours
        t_ = c.mask_rect(tx, 222, tx + 18, 304)
        c.shape(t_, tuple(lt(pierre, 0.06)), tuple(dk(pierre, 0.64)), tuple(lt(pierre, 0.25)), band=4, ol=False)
        for x in range(tx - 1, tx + 19, 7):
            c.fill(c.mask_rect(x, 216, x + 4, 222), tuple(lt(pierre, 0.1)))
        c.fill(c.mask_rect(tx + 8, 240, tx + 9, 248), tuple(dk(pierre, 0.35)))
    arche = c.mask_arch(140, 172, 256, 304)                             # la grande porte, fermée
    c.fill(c.mask_arch(137, 175, 252, 304), tuple(dk(pierre, 0.6)))
    bois = (104, 70, 44) if heure != "nuit" else (50, 40, 50)
    c.fill(arche, bois)
    for x in range(142, 172, 5):
        c.fill(arche & c.mask_rect(x, 256, x, 304), tuple(dk(bois, 0.7)))
    c.fill(arche & c.mask_rect(156, 256, 156, 304), tuple(dk(bois, 0.45)))
    for y in (270, 288):
        c.fill(arche & c.mask_rect(140, y, 172, y + 1), (60, 60, 70))
    _melange(c, terre & (Y < 310), (0, 0, 0), 0.26 * (1 - (Y - 302) / 8.0))
    if heure == "fin":
        c.tint(c.mask_rect(-105, 0, 375, 480), (255, 120, 60), 0.10)
    return lieux.relief(c, snap, sky), None


class Flux:
    """Une foule de silhouettes qui passe (de gauche à droite si sens = 1), en rangs de profondeur entre y0 et y1."""

    def __init__(s, n=380, y0=320, y1=372, sens=1, seed=840, h0=9, h1=26, vitesse=16.0, clair=False, entree=False,
                 x_min=-130, x_max=400, trou=None):
        rr = R(seed)
        s.ag = sorted((rr.uniform(0, 1) ** 1.3, rr.uniform(0, 1), rr.uniform(0.8, 1.25), rr.uniform(0, 6.28), rr.random())
                      for _ in range(n))
        s.p = (y0, y1, sens, h0, h1, vitesse, clair, entree, x_min, x_max, trou)

    def dessine(s, d, tt, alpha=255, fige=None):
        y0, y1, sens, h0, h1, v, clair, entree, x_min, x_max, trou = s.p
        W = x_max - x_min
        tm = tt if fige is None else min(tt, fige)
        for (q, ph, sp, ph2, ty) in s.ag:
            y = y0 + (y1 - y0) * q
            h = h0 + (h1 - h0) * q
            dist = tm * v * sp * (0.5 + q)
            if entree and dist < ph * W:
                continue
            x = x_min + (ph * W + dist) % W
            if sens < 0:
                x = x_max - (x - x_min)
            if trou and trou[0] < x < trou[1]:
                continue
            if clair:
                col = ((196, 176, 140), (150, 120, 96), (224, 214, 196), (120, 96, 80))[int(ty * 4) % 4] + (alpha,)
            else:
                ton = int(60 - 36 * q)
                col = (ton + 14, ton - 2, ton - 4, alpha)
            _silhouette(d, x + 105, y, h, col, tm * 7.5 * sp + ph2, ty < 0.3, 0.3 <= ty < 0.4)
            if clair and h >= 5 and ty > 0.86:                           # une bannière de temps en temps
                d.rectangle([x + 105, y - h * 1.7, x + 105 + 3, y - h * 1.45], fill=(170, 60, 50, alpha))
                d.line([x + 105, y - h * 1.7, x + 105, y - h * 0.4], fill=(70, 50, 40, alpha))


def _anim_flux(fl, t_debut=0.0, fige=None):
    def f(img, u):
        if u < t_debut:
            return
        lay = _calque(img)
        fl.dessine(ImageDraw.Draw(lay), u - t_debut, fige=fige)
        _pose(img, lay)
    return f


# ---------------------------------------------------------------- le lac de Tibériade
LAC = (135, 290, 300, 40)                                              # centre x, y, rayons


def lac(heure="jour"):
    """Un grand lac entre des collines, vu de la rive — dessiné ASSÉCHÉ (vase craquelée, pierres, une barque
    échouée) ; l'eau est l'animation (option « lac », puis {lac_bu N})."""
    c = _Px()
    sky = _fond(c, heure, 262, soleil=(60, 150) if heure != "fin" else (250, 160), r_sol=12, seed=851)
    snap = c.a.copy()
    roc, sol, hz = G.ROCS[heure], G.SOLS[heure], G.CIELS[heure][1]
    vert = mix(VERT, hz, 0.3) if heure == "jour" else mix(roc, sol, 0.5)
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    _collines(c, 222, 24, 852, mix(dk(vert, 0.85), hz, 0.6), 270)
    _collines(c, 242, 16, 853, mix(vert, hz, 0.36), 270)
    terre = c.mask_rect(-105, 258, 375, 480)
    _terre(c, terre, 258, 480, mix(sol, vert, 0.25), mix(sol, hz, 0.3), 854)
    cx, cy, rx, ry = LAC
    dist = np.sqrt(((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2)
    lit = dist < 1.0 + 0.03 * np.sin(X * 0.11) + 0.03 * np.sin(X * 0.31 + 1)
    vase = mix((104, 84, 68), sol, 0.25) if heure != "nuit" else (40, 40, 60)
    _peint(c, lit, dist, [(0.0, dk(vase, 0.62)), (0.6, vase), (1.0, lt(vase, 0.2))], 8)
    bord = lit & (dist > 0.9)
    _melange(c, bord, dk(vase, 0.6), 0.3)
    rr = R(855)
    for _ in range(90):                                                  # craquelures
        x, y = rr.randint(-80, 350), rr.randint(int(cy - ry) + 2, int(cy + ry) - 2)
        if lit[y, x + c.ox]:
            a = rr.uniform(0, 3.14)
            for j in range(rr.randint(4, 12)):
                xx, yy = int(x + math.cos(a) * j), int(y + math.sin(a) * j * 0.3)
                if 0 <= yy < 480 and -105 <= xx < 375 and lit[yy, xx + c.ox]:
                    c.px(xx, yy, tuple(dk(vase, 0.5)))
                a += rr.uniform(-0.4, 0.4)
    for _ in range(26):
        x, y = rr.randint(-70, 340), rr.randint(int(cy - ry) + 3, int(cy + ry) - 3)
        if lit[y, x + c.ox]:
            c.fill(c.mask_ell(x, y, rr.randint(2, 4), 1.4), tuple(lt(vase, 0.3)))
    bx, by = 60, 300                                                     # la barque échouée, penchée
    coque = c.mask_poly([(bx - 14, by - 5), (bx + 16, by - 7), (bx + 11, by + 1), (bx - 9, by + 2)])
    c.shape(coque, (120, 84, 52), (80, 54, 36), (160, 120, 80), band=1)
    c.line(bx + 1, by - 6, bx + 5, by - 22, (90, 64, 44))
    for x in range(-100, 372, 3):                                        # roseaux secs sur la rive
        if rr.random() < 0.3:
            yb = int(cy + ry * math.sqrt(max(0.0, 1 - ((x - cx) / rx) ** 2))) + rr.randint(2, 6)
            for j in range(rr.randint(3, 8)):
                c.px(x, yb - j, tuple(mix((150, 130, 80), sol, 0.3)))
    if heure == "fin":
        c.tint(c.mask_rect(-105, 0, 375, 480), (255, 120, 60), 0.10)
    return lieux.relief(c, snap, sky), None


def anim_lac(events, suff=""):
    """L'eau du lac. Pleine tant qu'aucun {lac_bu N} n'est arrivé ; ensuite le niveau baisse en N secondes : la rive
    recule vers le centre, la vase mouillée brille puis sèche, les reflets s'éteignent."""
    rr = R(860)
    eclats = [(rr.uniform(-1, 1), rr.uniform(-1, 1), rr.uniform(0, 6.28), rr.randint(2, 7)) for _ in range(220)]
    xs = np.arange(-105, 375, dtype=np.float32)[None, :]
    ys = np.arange(0, 480, dtype=np.float32)[:, None]
    cx, cy, rx, ry = LAC
    dist = np.sqrt(((xs - cx) / rx) ** 2 + ((ys - cy) / ry) ** 2)
    ond = 0.03 * np.sin(xs * 0.11) + 0.03 * np.sin(xs * 0.31 + 1)
    nuit = suff == "_nuit"
    fin = suff == "_fin"
    c0, c1 = ((150, 200, 226), (36, 96, 150)) if not (nuit or fin) else (((200, 150, 120), (70, 60, 90)) if fin else ((60, 76, 120), (14, 24, 56)))
    eau_rgb = _stops([(0.0, c1), (0.75, mix(c1, c0, 0.5)), (1.0, c0)], np.clip(dist, 0, 1) + 0 * xs)

    def f(img, u):
        niv = 1.0
        for (t, d_) in events:
            if u >= t:
                niv = 1.0 - _smooth((u - t) / d_) * 1.0
        if niv <= 0.004:
            return
        s = niv ** 0.75
        eau = dist < (1.0 + ond * s) * s
        a = np.zeros((480, 480, 4), np.uint8)
        a[..., :3] = eau_rgb
        a[..., 3] = np.where(eau, 255, 0)
        if niv < 0.995:                                                # vase mouillée entre l'ancienne rive et l'eau
            mouille = (~eau) & (dist < (1.0 + ond * s) * min(1.0, s + 0.16))
            a[mouille] = (60, 52, 56, 150)
        rive = eau & (dist > (1.0 + ond * s) * s - 0.035)
        a[rive, :3] = (226, 240, 246) if not fin else (250, 214, 180)
        lay = Image.fromarray(a, "RGBA")
        d = ImageDraw.Draw(lay)
        for (ax, ay, ph, L_) in eclats:                                 # reflets qui dansent
            x, y = cx + ax * rx * s * 0.94, cy + ay * ry * s * 0.9
            if (ax * ax + ay * ay) > 0.92:
                continue
            if math.sin(u * 2.2 + ph) > 0.2:
                d.line([x + 105, y, x + 105 + L_ * s, y], fill=(236, 246, 250, 210) if not fin else (255, 220, 180, 210))
        _pose(img, lay)
    return f


# ---------------------------------------------------------------- vu d'en haut : le Mont, le rempart
def belvedere(heure="nuit", kind="mont"):
    """Vu du Mont (corniche de roche) ou du rempart (parapet crénelé) : la plaine immense, en bas, jusqu'aux montagnes."""
    c = _Px()
    sky = _fond(c, heure, 232, soleil=(300, 130) if heure == "nuit" else (40, 222), r_sol=9 if heure == "nuit" else 13, seed=871)
    snap = c.a.copy()
    roc, sol, hz = G.ROCS[heure], G.SOLS[heure], G.CIELS[heure][1]
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    _collines(c, 222, 18, 872, mix(dk(roc, 0.8), hz, 0.6), 240)
    plaine_ = c.mask_rect(-105, 232, 375, 330)
    _peint(c, plaine_, (Y - 232) / 98.0, [(0.0, mix(sol, hz, 0.6)), (0.4, mix(sol, hz, 0.25)), (1.0, dk(sol, 0.75))], 10)
    lign = np.sin(np.maximum(Y - 232, 0) ** 0.6 * 5 + np.sin(X * 0.03) * 2) > 0.9
    _melange(c, plaine_ & lign, dk(sol, 0.7), 0.16)
    if kind == "mont":
        pts = _crete([(-105, 296), (-40, 290), (30, 295), (110, 288), (190, 295), (270, 289), (375, 296)], 873, 3)
        corn = c.mask_poly(pts + [(375, 480), (-105, 480)])
        _roche(c, corn, roc, 874, lum=-1)
        rr = R(875)
        for _ in range(60):
            x, y = rr.randint(-104, 373), rr.randint(326, 474)
            w = rr.randint(2, 6)
            c.shape(c.mask_ell(x, y, w, w * 0.6), tuple(roc), tuple(dk(roc, 0.6)), tuple(lt(roc, 0.3)), band=1, ol=False)
        for (x, y, w, h) in ((-84, 298, 20, 16), (336, 300, 24, 20)):
            r_ = c.mask_ell(x, y, w, h) & c.mask_rect(x - w, y - h, x + w, y + 2)
            c.shape(r_, tuple(roc), tuple(dk(roc, 0.6)), tuple(lt(roc, 0.3)), band=2, ol=False)
    else:
        pierre = mix((196, 168, 132), hz, 0.2) if heure != "nuit" else (66, 66, 96)
        par = c.mask_rect(-105, 284, 375, 322)
        _peint(c, par, (Y - 284) / 38.0, [(0.0, lt(pierre, 0.15)), (1.0, dk(pierre, 0.66))], 6)
        for x in range(-105, 376, 26):                                   # merlons
            me = c.mask_rect(x, 270, x + 15, 284)
            c.shape(me, tuple(lt(pierre, 0.08)), tuple(dk(pierre, 0.62)), tuple(lt(pierre, 0.3)), band=3, ol=False)
        for y in (294, 304, 313):
            c.fill(par & c.mask_rect(-105, y, 375, y), tuple(dk(pierre, 0.7)))
        for x in range(-100, 376, 17):
            c.fill(par & c.mask_rect(x, 284, x, 322), tuple(dk(pierre, 0.78)))
        sol_ = c.mask_rect(-105, 322, 375, 480)
        _peint(c, sol_, (Y - 322) / 158.0, [(0.0, dk(pierre, 0.9)), (1.0, dk(pierre, 0.55))], 8)
        for y in range(330, 480, 14):                                    # dalles du chemin de ronde
            c.fill(sol_ & c.mask_rect(-105, y, 375, y), tuple(dk(pierre, 0.5)))
            for x in range(-105 + (y % 28), 376, 30):
                c.fill(sol_ & c.mask_rect(x, y, x, y + 13), tuple(dk(pierre, 0.5)))
    return lieux.relief(c, snap, sky), None


class Plaine:
    """La plaine couverte, vue d'en haut : des milliers de points serrés, qui remuent (ou plus du tout)."""

    def __init__(s, n=5200, seed=880, y0=235, y1=290, torches=0):
        rr = R(seed)
        s.pt = sorted((rr.uniform(0, 1) ** 0.8, rr.uniform(-105, 375), rr.uniform(0, 6.28), rr.random()) for _ in range(n))
        s.y0, s.y1 = y0, y1
        s.torches = [(rr.uniform(-100, 370), rr.uniform(0, 1) ** 0.8, rr.uniform(0, 6.28)) for _ in range(torches)]

    def dessine(s, d, tt, fige=None, alpha=255, clair=False):
        vivant = 1.0 if fige is None else max(0.0, min(1.0, (fige - tt) / 1.5))
        for (q, x, ph, ty) in s.pt:
            y = s.y0 + (s.y1 - s.y0) * q
            h = 1 + 2.6 * q
            xx = x + vivant * (1.2 + 2 * q) * math.sin(tt * (1.2 + ty) + ph)
            ton = int(54 - 30 * q) if not clair else int(96 - 30 * q)
            hop = vivant * (math.sin(tt * 5 * (0.7 + ty) + ph) > 0.5)
            hh = h if vivant > 0.05 else max(1.0, h * 0.45)             # immobiles : plus bas, au sol
            d.rectangle([xx + 105, y - hh - hop, xx + 105 + (1 if q > 0.55 else 0), y], fill=(ton + 10, ton - 4, ton - 2, alpha))
            if vivant > 0.3 and q > 0.5 and ty < 0.2:
                d.line([xx + 106, y - hh, xx + 106, y - hh - 3 - 2 * q], fill=(ton, ton - 8, ton - 6, alpha))
        for (x, q, ph) in s.torches:
            if vivant <= 0.05:
                continue
            y = s.y0 + (s.y1 - s.y0) * q
            al = int(alpha * vivant * (0.6 + 0.4 * math.sin(tt * 9 + ph)))
            d.point((x + 105, y - 4 - 3 * q), fill=(255, 190, 90, al))
            d.point((x + 105, y - 5 - 3 * q), fill=(255, 120, 50, al // 2))


def anim_plaine(events, torches=60, fige_debut=False, bg=""):
    pl = Plaine(torches=torches)

    def f(img, u):
        fige = -10.0 if fige_debut else None
        for t in events:
            if u >= t or fige is None:
                fige = t if fige is None or t < fige or fige < 0 else fige
        lay = _calque(img)
        pl.dessine(ImageDraw.Draw(lay), u, fige=fige if (fige_debut or events) else None)
        _pose(img, lay)
    return f


# ---------------------------------------------------------------- la plaine au matin, les oiseaux, le miroir
def plaine(heure="aube"):
    """La plaine au niveau du sol, immense et vide, au petit matin ; des collines basses au loin, une piste."""
    c = _Px()
    sky = _fond(c, heure, 270, soleil=(210, 262) if heure == "aube" else (250, 130), r_sol=14, seed=891)
    snap = c.a.copy()
    roc, sol, hz = G.ROCS[heure], G.SOLS[heure], G.CIELS[heure][1]
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    _collines(c, 258, 12, 892, mix(dk(roc, 0.85), hz, 0.6), 274)
    terre = c.mask_rect(-105, 268, 375, 480)
    _terre(c, terre, 268, 480, sol, mix(sol, hz, 0.45), 893, cailloux=130)
    d = (Y - 268) / 212.0
    piste = terre & (np.abs(X - 150 - 14 * np.sin(Y * 0.03)) < 6 + d * 60)
    _melange(c, piste, lt(sol, 0.3), 0.3)
    return lieux.relief(c, snap, sky), None


def anim_bande(events=(), y=272):
    """Au loin, sur la plaine : une longue bande sombre, immobile (on ne distingue rien). {oiseaux_emportent N} : de
    grands oiseaux au long cou descendent, repartent en portant de petites formes sombres ; la bande s'efface."""
    rr = R(900)
    tas = [(rr.uniform(-105, 375), rr.uniform(0, 1), rr.uniform(2, 7), rr.uniform(1, 3.4)) for _ in range(900)]
    ois = [(rr.uniform(0, 1), rr.uniform(-80, 350), rr.uniform(0.8, 1.2), rr.uniform(0, 6.28), rr.choice((-1, 1))) for _ in range(34)]

    def oiseau(d, x, y, s, bat, sens, charge):
        col = (46, 38, 44, 255)
        d.ellipse([x - 4 * s, y - 1.6 * s, x + 4 * s, y + 1.6 * s], fill=col)             # corps
        d.line([x + 3 * s * sens, y - 1 * s, x + 7 * s * sens, y - 5 * s], fill=col, width=max(1, int(s)))   # long cou
        d.ellipse([x + 7.3 * s * sens - 0.9 * s, y - 6.2 * s, x + 7.3 * s * sens + 0.9 * s, y - 4.6 * s], fill=col)
        d.line([x + 8 * s * sens, y - 5.4 * s, x + 10 * s * sens, y - 5 * s], fill=(190, 150, 90, 255))
        a = math.sin(bat) * 5 * s
        d.polygon([(x - 2 * s, y), (x + 2 * s, y), (x - 1 * s * sens, y - 3 * s - a)], fill=col)   # aile
        d.polygon([(x - 2 * s, y), (x + 2 * s, y), (x - 3 * s * sens, y - 1 * s + a * 0.6)], fill=(70, 58, 60, 255))
        if charge:
            d.rectangle([x - 2 * s, y + 2 * s, x + 2 * s, y + 3.6 * s], fill=(28, 20, 22, 255))

    def f(img, u):
        reste, t_o, d_o = 1.0, None, 1.0
        for (t, d_) in events:
            if u >= t:
                t_o, d_o = t, d_
                reste = 1.0 - _smooth((u - t - d_ * 0.15) / (d_ * 0.8))
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        for (x, ph, w, h) in tas:
            if ph > reste:
                continue
            yy = y + ph * 12
            e = 0.4 + ph * 0.9
            d.ellipse([x + 105 - w * e, yy - h * e, x + 105 + w * e, yy + 1], fill=(58, 44, 44, 255))
        if t_o is not None and u < t_o + d_o * 1.25:
            k = (u - t_o) / d_o
            for (ph, x0, sp, ph2, sens) in ois:
                q = (k * 1.25 - ph * 0.9) / 0.34 * sp                       # 0-1 : descend ; 1-2 : remonte chargé
                if q < 0 or q > 2:
                    continue
                if q <= 1:
                    xx = x0 - sens * 60 * (1 - q)
                    yy = 110 + (y + 6 - 110) * _smooth(q)
                else:
                    xx = x0 + sens * 90 * (q - 1)
                    yy = y + 6 - (y - 80) * _smooth(q - 1)
                s = 1.1 + 1.3 * (yy - 100) / 180.0
                oiseau(d, xx + 105, yy, s, u * 9 + ph2, sens, q > 1)
        _pose(img, lay)
    return f


def miroir():
    """La terre lavée par la pluie : lisse et brillante « comme un miroir » — le ciel, les nuages et le soleil s'y
    reflètent ; quelques pierres, une ligne de collines au loin."""
    c = _Px()
    H = 262
    sky = _fond(c, "jour", H, soleil=(230, 170), r_sol=13, seed=911)
    snap = c.a.copy()
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    col_ = c.mask_rect(-105, H - 5, 375, H)
    _collines(c, H - 2, 6, 912, (150, 170, 190), H)
    src = c.a.copy()
    for y in range(H, 480):                                              # le reflet : le ciel retourné, un peu assombri
        ys_ = int(H - 1 - (y - H) * (H - 96) / (480.0 - H))
        dx = int(round(1.5 * math.sin(y * 0.45)))
        ligne = np.roll(src[max(96, ys_)], dx, axis=0).astype(np.float32)
        k = 0.86 - 0.22 * (y - H) / (480.0 - H)
        c.a[y] = np.clip(ligne * k + np.array((30, 40, 60), np.float32) * (1 - k), 0, 255).astype(np.uint8)
    sol_ = c.mask_rect(-105, H, 375, 480)
    raies = (np.sin(np.maximum(Y - H, 0) ** 0.7 * 4.0 + np.sin(X * 0.05) * 1.5) > 0.93) & sol_
    _melange(c, raies, (250, 252, 255), 0.3)
    rr = R(913)
    for _ in range(26):
        x, y = rr.randint(-100, 370), rr.randint(H + 10, 470)
        s = (y - H) / (480.0 - H)
        w = 2 + s * 6
        c.shape(c.mask_ell(x, y, w, w * 0.5), (120, 112, 110), (80, 74, 80), (170, 164, 160), band=1, ol=False)
        c.fill(c.mask_ell(x, y + w * 0.6, w, w * 0.3), (70, 84, 110))
    return lieux.relief(c, snap, sky), None


def benie():
    """La terre bénie : collines vertes, arbres chargés de fruits, ruisseau, fleurs — et, à droite, une grenade
    immense dont l'écorce ouverte fait un abri (Mouslim 2937)."""
    c = _Px()
    sky = _fond(c, "jour", 262, soleil=(20, 140), r_sol=12, seed=921)
    snap = c.a.copy()
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    hz = G.CIELS["jour"][1]
    _collines(c, 236, 22, 922, mix((70, 130, 90), hz, 0.5), 300)
    _collines(c, 256, 18, 923, mix(VERT, hz, 0.22), 300)
    pre = c.mask_rect(-105, 284, 375, 480)
    _peint(c, pre, (Y - 284) / 196.0, [(0.0, lt(VERT, 0.2)), (0.4, VERT), (1.0, dk(VERT, 0.66))], 10)
    herbe = (np.sin(X * 0.9 + Y * 0.37) + np.sin(X * 0.33 - Y * 0.71)) > 1.25
    _melange(c, pre & herbe, lt(VERT, 0.3), 0.4)
    ruis = pre & (np.abs(X - (40 + 46 * np.sin(Y * 0.035) + (Y - 284) * 0.2)) < 3 + (Y - 284) * 0.06)
    _peint(c, ruis, (Y - 284) / 196.0, [(0.0, (170, 214, 236)), (1.0, (70, 140, 196))], 6)
    _melange(c, ruis & (np.sin(Y * 1.3 + X * 0.4) > 0.8), (240, 250, 255), 0.6)
    rr = R(924)
    for (tx, ty, s) in ((-70, 300, 1.0), (-22, 292, 0.8), (140, 290, 0.8), (184, 296, 1.0), (100, 286, 0.6)):
        c.shape(c.mask_rect(tx - 2 * s, ty - 22 * s, tx + 2 * s, ty), (104, 74, 50), (70, 50, 36), band=1, ol=False)
        for (dx, dy, r_) in ((0, -34, 17), (-11, -27, 11), (11, -28, 11)):
            m = c.mask_ell(tx + dx * s, ty + dy * s, r_ * s, r_ * 0.8 * s)
            c.fill(m, (54, 124, 64))
            c.fill(m & c.mask_ell(tx + dx * s - 3, ty + dy * s - 3, r_ * 0.7 * s, r_ * 0.5 * s), (84, 160, 80))
        for _ in range(int(14 * s)):                                     # fruits
            fx, fy = tx + rr.uniform(-18, 18) * s, ty - 30 * s + rr.uniform(-12, 10) * s
            c.px(int(fx), int(fy), rr.choice([(230, 70, 60), (250, 190, 60), (240, 120, 50)]))
    for _ in range(170):                                                 # fleurs
        x, y = rr.randint(-104, 373), rr.randint(292, 476)
        if not ruis[y, x + c.ox]:
            c.px(x, y, rr.choice([(250, 240, 120), (250, 250, 250), (240, 130, 160), (200, 150, 240)]))
    # la grenade : une demi-écorce posée comme un toit
    gx, gy, gr = 292, 336, 74
    dehors = c.mask_ell(gx, gy, gr, gr * 0.92) & c.mask_rect(gx - gr, gy - gr, gx + gr, gy)
    dedans = c.mask_ell(gx - 4, gy + 2, gr - 9, gr * 0.92 - 10) & c.mask_rect(gx - gr, gy - gr, gx + gr, gy)
    rouge = (196, 44, 54)
    c.shape(dehors, rouge, dk(rouge, 0.62), lt(rouge, 0.3), band=5, ol=False)
    _melange(c, dehors & (np.sin(X * 0.5 + Y * 0.3) > 0.9), lt(rouge, 0.35), 0.4)
    c.fill(dedans, (250, 232, 200))                                      # la peau blanche du dedans
    ombre = c.mask_ell(gx - 6, gy + 6, gr - 16, gr * 0.92 - 18) & c.mask_rect(gx - gr, gy - gr, gx + gr, gy)
    _peint(c, ombre, (Y - (gy - gr)) / gr, [(0.0, (120, 30, 44)), (1.0, (60, 24, 40))], 6)
    for _ in range(200):                                                 # les grains, au plafond de l'écorce
        a = rr.uniform(3.4, 6.0)
        r_ = rr.uniform(gr - 30, gr - 14)
        x, y = gx - 6 + math.cos(a) * r_, gy + 6 + math.sin(a) * r_ * 0.9
        if ombre[int(y), int(x) + c.ox]:
            c.fill(c.mask_ell(x, y, 2.2, 2.6), (226, 40, 70))
            c.px(int(x) - 1, int(y) - 1, (255, 170, 180))
    cour = c.mask_poly([(gx - 8, gy - gr * 0.92 + 2), (gx - 12, gy - gr * 0.92 - 8), (gx - 4, gy - gr * 0.92 - 4),
                        (gx + 2, gy - gr * 0.92 - 10), (gx + 6, gy - gr * 0.92 - 3), (gx + 12, gy - gr * 0.92 - 8),
                        (gx + 9, gy - gr * 0.92 + 2)])
    c.fill(cour, dk(rouge, 0.8))                                         # la couronne du fruit
    _melange(c, pre & c.mask_ell(gx - 4, gy + 4, gr - 8, 10), (20, 50, 30), 0.4)   # l'ombre au sol
    return lieux.relief(c, snap, sky), None


# ---------------------------------------------------------------- le Couchant, le Levant
def couchant():
    """Au bout des terres, le soir : le rivage de vase, l'eau sombre et boueuse jusqu'à l'horizon, et le soleil qui
    semble s'y enfoncer (18:86 : ce qu'il a VU depuis le rivage) ; à gauche, les huttes d'un peuple."""
    c = _Px()
    H = 252
    sky = _fond(c, "soir", H, soleil=(150, H), r_sol=20, seed=931)
    snap = c.a.copy()
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    mer = c.mask_rect(-105, H, 375, 322)
    _peint(c, mer, (Y - H) / 70.0, [(0.0, (150, 84, 60)), (0.15, (84, 54, 48)), (0.6, (48, 34, 36)), (1.0, (30, 22, 28))], 10)
    rr = R(932)
    for y in range(H + 1, 322):
        d = (y - H) / 70.0
        for _ in range(int(3 + d * 8)):
            x = rr.randint(-105, 374)
            L_ = int(2 + d * rr.randint(3, 14))
            c.fill(mer & c.mask_rect(x, y, x + L_, y), (70, 48, 44) if rr.random() < 0.6 else (24, 16, 22))
        w_ = 3 + d * 30                                                  # le reflet du soleil
        for _ in range(int(2 + d * 4)):
            x = 150 + rr.uniform(-w_, w_)
            c.fill(mer & c.mask_rect(x, y, x + 1 + int(d * 5), y), (255, 170, 90) if rr.random() < 0.6 else (236, 120, 70))
    vase = c.mask_rect(-105, 318, 375, 480) | (c.mask_rect(-105, 312, 375, 320) & (np.sin(X * 0.07) * 4 + 316 < Y))
    _peint(c, vase, (Y - 314) / 166.0, [(0.0, (84, 60, 52)), (0.4, (66, 48, 44)), (1.0, (38, 28, 30))], 8)
    for _ in range(22):                                                  # flaques qui reflètent le ciel
        x, y = rr.randint(-100, 370), rr.randint(326, 474)
        _melange(c, vase & c.mask_ell(x, y, rr.randint(8, 22), rr.randint(1, 2)), (236, 150, 100), 0.45)
    for _ in range(80):
        x, y = rr.randint(-104, 373), rr.randint(322, 476)
        c.fill(c.mask_ell(x, y, rr.randint(2, 5), 1) & vase, (30, 22, 26))
    for hx in (-86, -58, -34, -8):                                        # les huttes
        hy = 318 + (hx % 5)
        hut = c.mask_ell(hx, hy, 11, 13) & c.mask_rect(hx - 11, hy - 13, hx + 11, hy)
        c.shape(hut, (120, 88, 60), (70, 50, 40), (176, 130, 84), band=2, ol=False)
        c.fill(c.mask_rect(hx - 2, hy - 7, hx + 2, hy), (30, 20, 20))
    for x in range(250, 372, 2):                                         # roseaux
        if rr.random() < 0.5:
            for j in range(rr.randint(6, 18)):
                c.px(x + (1 if j > 9 else 0), 326 - j, (58, 60, 40) if j < 12 else (120, 96, 60))
    c.tint(c.mask_rect(-105, 0, 375, 480), (255, 150, 80), 0.08)
    return lieux.relief(c, snap, sky), None


def levant():
    """À l'endroit où le soleil se lève : une terre nue, plate, craquelée — pas une maison, pas un arbre (18:90) —
    et un soleil énorme sur l'horizon."""
    c = _Px()
    H = 266
    sky = _fond(c, "aube", H, soleil=(135, H - 4), r_sol=30, seed=941)
    snap = c.a.copy()
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    sol = (224, 186, 132)
    terre = c.mask_rect(-105, H, 375, 480)
    _peint(c, terre, (Y - H) / 214.0, [(0.0, (255, 220, 170)), (0.12, lt(sol, 0.15)), (1.0, dk(sol, 0.64))], 10)
    rr = R(942)
    for _ in range(240):                                                 # craquelures en perspective
        x, y = rr.randint(-104, 373), rr.randint(H + 3, 476)
        s = (y - H) / 214.0
        a = rr.uniform(0, 3.14)
        for j in range(int(3 + s * 16)):
            xx, yy = int(x + math.cos(a) * j), int(y + math.sin(a) * j * 0.3)
            if H < yy < 480 and -105 <= xx < 375:
                c.px(xx, yy, tuple(dk(sol, 0.6)))
            a += rr.uniform(-0.5, 0.5)
    chaleur = terre & (Y < H + 10) & (np.sin(X * 0.3 + Y * 2) > 0.3)
    _melange(c, chaleur, (255, 240, 200), 0.35)
    return lieux.relief(c, snap, sky), None


# ---------------------------------------------------------------- Médine, le mur de près, le tableau, la Ka'ba
def medine():
    """Médine, la nuit : une maison de briques de terre (porte et petite fenêtre éclairées), des palmiers, les étoiles."""
    c = _Px()
    sky = _fond(c, "nuit", 300, soleil=(300, 140), r_sol=8, seed=951)
    snap = c.a.copy()
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    _collines(c, 270, 14, 952, (30, 34, 66), 304)
    for i, x in enumerate((-92, -60, 278, 318, 352)):
        lieux.palmier(c, x, 306, h=44 + (i * 13) % 22, lean=(-8, 6, 9, -5, 7)[i], seed=60 + i, col=(34, 70, 60), trunk=(60, 50, 56))
    for (x0, w, h) in ((-40, 44, 30), (236, 50, 26)):                     # maisons voisines
        c.fill(c.mask_rect(x0, 304 - h, x0 + w, 306), (56, 50, 70))
        c.fill(c.mask_rect(x0, 304 - h, x0 + w, 304 - h), (86, 78, 100))
        c.fill(c.mask_rect(x0 + 8, 304 - h + 9, x0 + 12, 304 - h + 14), (240, 180, 96))
    mur = c.mask_rect(40, 214, 232, 308)
    _peint(c, mur, (Y - 214) / 94.0, [(0.0, (98, 84, 96)), (1.0, (56, 48, 64))], 8)
    for y in range(218, 308, 5):
        off = 5 if (y // 5) % 2 else 0
        c.fill(mur & c.mask_rect(40, y, 232, y), (60, 52, 68))
        for x in range(40 + off, 232, 11):
            c.fill(mur & c.mask_rect(x, y, x, y + 4), (64, 56, 72))
    c.fill(c.mask_rect(36, 210, 236, 214), (112, 98, 108))
    for x in range(44, 232, 14):                                         # bouts des poutres de palmier
        c.fill(c.mask_rect(x, 215, x + 3, 218), (70, 54, 50))
    porte = c.mask_arch(122, 152, 250, 308)
    c.fill(c.mask_arch(119, 155, 246, 308), (40, 34, 48))
    _peint(c, porte, (Y - 250) / 58.0, [(0.0, (255, 214, 140)), (1.0, (214, 140, 70))], 6)
    c.fill(c.mask_rect(184, 244, 196, 258), (250, 196, 110))
    c.fill(c.mask_rect(190, 244, 190, 258), (90, 66, 50))
    c.fill(c.mask_rect(184, 251, 196, 251), (90, 66, 50))
    c.glow(137, 284, 70, (255, 180, 90), 0.26)
    c.glow(190, 251, 26, (255, 180, 90), 0.2)
    sol_ = c.mask_rect(-105, 306, 375, 480)
    _peint(c, sol_, (Y - 306) / 174.0, [(0.0, (62, 58, 84)), (1.0, (26, 26, 44))], 8)
    lum = sol_ & (np.abs(X - 137) < 16 + (Y - 306) * 0.5) & (Y < 380)
    _melange(c, lum, (255, 190, 110), 0.3 * (1 - (Y - 306) / 74.0))
    rr = R(953)
    for _ in range(60):
        x, y = rr.randint(-104, 373), rr.randint(312, 474)
        c.fill(c.mask_ell(x, y, rr.randint(1, 3), 1), (44, 42, 64))
    return lieux.relief(c, snap, sky), None


TROU = (150, 252)


def mur_pres():
    """Le barrage vu de tout près : d'énormes blocs sous la peau de cuivre, coulures, reflets (pour le petit trou)."""
    c = _Px()
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    tout = c.mask_rect(-105, 0, 375, 480)
    _peint(c, tout, (Y - 90) / 300.0, [(0.0, lt(G.CUIVRE, 0.2)), (0.5, G.CUIVRE), (1.0, G.CUIVRE_SOMBRE)], 10)
    rr = R(961)
    for i, y in enumerate(range(60, 480, 30)):
        c.fill(c.mask_rect(-105, y, 375, y + 1), G.CUIVRE_SOMBRE)
        c.fill(c.mask_rect(-105, y + 2, 375, y + 2), lt(G.CUIVRE, 0.3))
        x = -105 - (i % 2) * 26
        while x < 376:
            w = rr.randint(44, 64)
            c.fill(c.mask_rect(x, y, x + 1, y + 29), G.CUIVRE_SOMBRE)
            c.fill(c.mask_rect(x + 2, y + 2, x + 2, y + 29), lt(G.CUIVRE, 0.25))
            _melange(c, c.mask_rect(x + 3, y + 3, x + w - 1, y + 29), (0, 0, 0) if rr.random() < 0.5 else (255, 200, 140), rr.uniform(0.02, 0.12))
            x += w
    coul = np.sin(X * 1.1 + np.sin(Y * 0.03 + X * 0.2) * 1.4) > 0.9
    _melange(c, coul, G.CUIVRE_CLAIR, 0.35)
    _melange(c, np.sin(X * 0.7 + 2 + np.sin(Y * 0.04)) < -0.93, G.CUIVRE_SOMBRE, 0.4)
    lustre = np.exp(-((X - 60) / 26.0) ** 2) + 0.6 * np.exp(-((X - 260) / 14.0) ** 2)
    _melange(c, _bay(c) < lustre, (255, 230, 180), np.clip(lustre, 0, 1) * 0.4)
    for _ in range(120):
        x, y = rr.randint(-104, 373), rr.randint(92, 380)
        L_ = rr.randint(4, 20)
        c.fill(c.mask_rect(x, y, x, y + L_), G.CUIVRE_CLAIR if rr.random() < 0.5 else G.CUIVRE_SOMBRE)
    return c, None


def anim_trou(t_debut=0.0):
    """Un petit trou rond s'ouvre dans le métal (bord clair, intérieur noir), un peu de poussière tombe."""
    rr = R(962)
    grains = [(rr.uniform(-5, 5), rr.uniform(0, 1), rr.uniform(0.6, 1.4)) for _ in range(30)]
    x0, y0 = TROU

    def f(img, u):
        if u < t_debut:
            return
        tt = u - t_debut
        r_ = 6.0 * _smooth(tt / 1.6)
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        if r_ > 0.5:
            d.ellipse([x0 + 105 - r_ - 1.5, y0 - r_ - 1.5, x0 + 105 + r_ + 1.5, y0 + r_ + 1.5], fill=(255, 214, 150, 255))
            d.ellipse([x0 + 105 - r_ - 0.5, y0 - r_ + 0.5, x0 + 105 + r_ + 0.5, y0 + r_ + 1.5], fill=(90, 44, 30, 255))
            d.ellipse([x0 + 105 - r_, y0 - r_, x0 + 105 + r_, y0 + r_], fill=(10, 6, 10, 255))
        if tt < 4:
            for (dx, ph, sp) in grains:
                p = (ph + tt * 0.5 * sp) % 1.0
                d.point((x0 + 105 + dx, y0 + r_ + p * 40), fill=(230, 180, 130, int(220 * (1 - p) * max(0.0, 1 - tt / 4))))
        _pose(img, lay)
    return f


def mille():
    """Fond sombre et sobre pour deux tableaux animés : « mille pour un » et « dix signes »."""
    c = _Px()
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    tout = c.mask_rect(-105, 0, 375, 480)
    r_ = np.sqrt(((X - 135) / 300.0) ** 2 + ((Y - 235) / 190.0) ** 2)
    _peint(c, tout, r_, [(0.0, (40, 40, 70)), (0.6, (24, 24, 48)), (1.0, (10, 10, 24))], 10)
    sol_ = c.mask_rect(-105, 330, 375, 480)
    _peint(c, sol_, (Y - 330) / 150.0, [(0.0, (34, 32, 56)), (1.0, (12, 12, 26))], 6)
    return c, None


_POLICE = "C:/Windows/Fonts/tahomabd.ttf"


def anim_mille(t_debut=0.0, duree=7.0):
    """À gauche, UN petit homme clair ; à droite, des silhouettes sombres qui arrivent rang après rang… jusqu'à mille
    (le compteur monte avec elles)."""
    cols, rangs = 50, 20
    pol = ImageFont.truetype(_POLICE, 64)

    def f(img, u):
        if u < t_debut:
            return
        tt = u - t_debut
        k = _smooth(tt / duree)
        n = int(1000 * k)
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        a1 = int(255 * min(1.0, tt / 0.6))
        _silhouette(d, -40 + 105, 300, 30, (250, 232, 190, a1), 0.0, False, False)
        for i in range(n):
            r_, cc = i // cols, i % cols
            x = 28 + cc * 6.6 + (r_ % 2) * 3
            y = 178 + r_ * 7.4
            _silhouette(d, x + 105, y, 6, (150 - r_ * 2, 60, 56, 255), 0.0, False, False)
        _pose(img, lay)
        dd = ImageDraw.Draw(img)
        dd.text((260, 1010), "1", font=pol, fill=(250, 232, 190, a1), anchor="mm", stroke_width=5, stroke_fill=(10, 10, 24, a1))
        if n:
            dd.text((1150, 620), f"{n:,}".replace(",", " "), font=pol, fill=(255, 214, 70, 255), anchor="mm", stroke_width=5,
                    stroke_fill=(10, 10, 24, 255))
    return f


def anim_part(t_debut=0.0, duree=9.0):
    """« De chaque millier, neuf cent quatre-vingt-dix-neuf » : mille petits hommes clairs en rangs ; ils s'assombrissent
    l'un après l'autre ; un seul reste clair (Boukhari 3348)."""
    cols, rangs = 50, 20
    rr = R(965)
    ordre = list(range(cols * rangs))
    rr.shuffle(ordre)
    rang_de = {i: n for n, i in enumerate(ordre)}
    seul = 9 * cols + 24

    def f(img, u):
        if u < t_debut:
            return
        tt = u - t_debut
        app = _smooth(tt / 1.5)
        k = _smooth((tt - 2.0) / max(0.1, duree - 2.0))
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        for i in range(cols * rangs):
            r_, cc = i // cols, i % cols
            if cc / cols > app * 1.02:
                continue
            x = -30 + cc * 6.6 + (r_ % 2) * 3
            y = 178 + r_ * 7.4
            sombre = i != seul and rang_de[i] / 1000.0 < k
            if i == seul and k > 0.5:
                d.ellipse([x + 105 - 6, y - 9, x + 105 + 6, y + 3], fill=(255, 220, 140, int(90 * k)))
            _silhouette(d, x + 105, y, 6, (150, 60, 56, 255) if sombre else (250, 232, 190, 255), 0.0, False, False)
        _pose(img, lay)
    return f


def anim_dix(t_debut=0.0, duree=5.0, lequel=5):
    """Dix lampes s'allument une à une ; l'une d'elles (Ya'jouj et Ma'jouj) brille plus fort — l'ordre n'est pas
    celui du temps (Mouslim 2901 ne donne pas l'ordre)."""
    def f(img, u):
        if u < t_debut:
            return
        tt = u - t_debut
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        for i in range(10):
            x = -64 + i * 44 + 105
            y = 236
            on = _smooth((tt - i * duree / 12.0) / 0.5)
            d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=(90, 90, 130, 255))
            if on > 0:
                fort = i == lequel and tt > duree
                p = 1.0 + (0.25 * math.sin(tt * 4) + 0.5 if fort else 0.0)
                for r_, al in ((16 * p, 40), (11 * p, 90)):
                    d.ellipse([x - r_, y - r_, x + r_, y + r_], fill=((255, 120, 60) if fort else (255, 214, 120)) + (int(al * on),))
                d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=((255, 170, 90) if fort else (255, 236, 170)) + (int(255 * on),))
        _pose(img, lay)
    return f


def kaaba():
    """La Maison d'Allah, de loin, au petit matin : la Ka'ba dans sa cour, les collines autour ; l'option « tawaf »
    fait tourner de minuscules pèlerins vêtus de blanc."""
    c = _Px()
    sky = _fond(c, "aube", 262, soleil=(280, 240), r_sol=12, seed=971)
    snap = c.a.copy()
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    hz = G.CIELS["aube"][1]
    _collines(c, 236, 26, 972, mix((120, 100, 104), hz, 0.5), 270)
    _collines(c, 252, 14, 973, mix((150, 120, 110), hz, 0.25), 270)
    cour = c.mask_rect(-105, 262, 375, 480)
    _peint(c, cour, (Y - 262) / 218.0, [(0.0, (214, 190, 166)), (0.3, (190, 164, 140)), (1.0, (130, 110, 100))], 10)
    for y in range(270, 480, 9):
        c.fill(cour & c.mask_rect(-105, y, 375, y) & (_bay(c) < 0.5), (170, 146, 126))
    k = c.mask_rect(113, 250, 157, 300)
    c.shape(k, (30, 28, 34), (14, 12, 18), (58, 54, 62), band=6, ol=False)
    c.fill(c.mask_rect(113, 262, 157, 265), (214, 170, 70))
    c.fill(c.mask_rect(113, 266, 157, 266), (150, 110, 40))
    c.fill(c.mask_rect(138, 280, 146, 300), (200, 160, 70))
    _melange(c, cour & c.mask_ell(140, 302, 30, 4), (0, 0, 0), 0.3)
    return lieux.relief(c, snap, sky), None


def anim_tawaf():
    rr = R(980)
    pel = [(rr.uniform(0, 6.28), rr.uniform(34, 110), rr.uniform(0.8, 1.2)) for _ in range(420)]

    def f(img, u):
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        pts = []
        for (a0, r_, sp) in pel:
            a = a0 - u * 0.22 * sp * (60 / r_)
            pts.append((304 + math.sin(a) * r_ * 0.36, 135 + math.cos(a) * r_))
        for (y, x) in sorted(pts):
            if 113 < x < 157 and y < 300:
                continue
            h = 2 + (y - 270) / 22.0
            d.rectangle([x + 105, y - h, x + 105 + (1 if h > 3 else 0), y], fill=(246, 244, 236, 255))
            d.point((x + 105, y - h - 1), fill=(150, 110, 90, 255))
        _pose(img, lay)
    return f


def anim_vent(n=90, seed=995):
    """De fines poussières qui traversent l'image, portées par le vent (pour qu'un plan posé reste vivant)."""
    rr = R(seed)
    pts = [(rr.uniform(0, 1), rr.uniform(120, 350), rr.uniform(14, 40), rr.uniform(0, 6.28), rr.randint(1, 3)) for _ in range(n)]

    def f(img, u):
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        for (ph, y, v, ph2, L_) in pts:
            x = (ph * 520 + u * v) % 520 - 20
            yy = y + 5 * math.sin(u * 0.8 + ph2)
            d.line([x, yy, x + L_, yy], fill=(230, 214, 190, 110))
        _pose(img, lay)
    return f


def derriere():
    """L'autre côté du barrage, la nuit : le même mur, vu du pays de Ya'jouj et Ma'jouj (teinte sombre et rousse)."""
    c, _ = G.col("nuit", "fini")
    for nom in ("a", "al", "lointain", "ciel_m"):
        v = getattr(c, nom, None)
        if v is not None:
            setattr(c, nom, v[:, ::-1].copy())
    c.tint(c.mask_rect(-105, 0, 375, 480), (120, 40, 30), 0.16)
    return c, None


def anim_escalade():
    """Au pied du barrage : des silhouettes essaient de monter (elles glissent et retombent) et de percer (étincelles)."""
    rr = R(990)
    gr = [(rr.uniform(-1, 1), rr.uniform(0, 1), rr.uniform(0.7, 1.3), rr.uniform(14, 46)) for _ in range(60)]
    base = Flux(n=260, y0=302, y1=340, h0=5, h1=12, vitesse=0.0, seed=991, x_min=10, x_max=260)

    def f(img, u):
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        for (a_, ph, sp, hmax) in gr:
            p = (ph + u * 0.16 * sp) % 1.0
            x = CX + a_ * 34
            if p < 0.7:
                y = YB - hmax * _smooth(p / 0.7)
            else:
                y = YB - hmax * (1 - ((p - 0.7) / 0.3) ** 2)
            _silhouette(d, x + 105, y, 5, (26, 18, 22, 255), u * 8 + ph * 9, False, p < 0.7)
            if 0.66 < p < 0.72:
                d.point((x + 106, y - 5), fill=(255, 220, 150, 255))
        base.dessine(d, u)
        for j in range(8):                                              # étincelles des outils sur le métal
            if math.sin(u * 7 + j * 2.1) > 0.86:
                xx = CX - 30 + j * 8.5 + 105
                d.point((xx, YB - 4 - (j % 3) * 2), fill=(255, 230, 160, 255))
                d.point((xx + 1, YB - 5 - (j % 3) * 2), fill=(255, 160, 80, 255))
        _pose(img, lay)
    return f


# ---------------------------------------------------------------- registre, options, annotations
_DEC = dict(gog_hauteurs=lambda: hauteurs("fin"), gog_hauteurs_jour=lambda: hauteurs("jour"),
            gog_forteresse=lambda: forteresse("fin"), gog_forteresse_jour=lambda: forteresse("jour"),
            gog_lac=lambda: lac("jour"), gog_lac_fin=lambda: lac("fin"),
            gog_tour_nuit=lambda: belvedere("nuit", "mont"), gog_tour_aube=lambda: belvedere("aube", "mont"),
            gog_tour_fin=lambda: belvedere("fin", "mont"),
            gog_rempart_aube=lambda: belvedere("aube", "rempart"), gog_rempart_nuit=lambda: belvedere("nuit", "rempart"),
            gog_plaine_aube=lambda: plaine("aube"), gog_plaine=lambda: plaine("jour"),
            gog_miroir=miroir, gog_benie=benie, gog_couchant=couchant, gog_levant=levant, gog_medine_nuit=medine,
            gog_mur_pres=mur_pres, gog_mille=mille, gog_kaaba=kaaba, gog_derriere=derriere)
egypte.enregistre(_DEC, sol_haut={n: (330, 100) for n in _DEC})
for _n in ("gog_tour_nuit", "gog_rempart_nuit", "gog_medine_nuit", "gog_derriere", "gog_mille"):
    lieux.LUMIERES[_n] = (lieux.NUIT, [])

ANNOTATIONS = ("part_feu", "lac_bu", "fleches", "trou", "mille", "dix", "oiseaux_emportent", "horde_fige", "horde_hauteurs")


def option(sc, o, bg):
    suff = G._suffixe(bg)
    if o == "passage" or o == "passage gauche":
        sc.anims.append(_anim_flux(Flux(sens=-1 if o.endswith("gauche") else 1)))
    elif o == "passage loin":
        sc.anims.append(_anim_flux(Flux(n=500, y0=312, y1=330, h0=4, h1=9, vitesse=9.0, seed=842)))
    elif o == "colonne":
        sc.anims.append(_anim_flux(Flux(n=260, y0=318, y1=336, h0=5, h1=9, vitesse=14.0, clair=True, seed=843, entree=True)))
    elif o == "contourne":
        sc.anims.append(_anim_flux(Flux(n=260, y0=304, y1=316, h0=3, h1=6, vitesse=26.0, seed=844, entree=True, trou=(28, 316))))
        sc.anims.append(_anim_flux(Flux(n=420, y0=322, y1=374, h0=8, h1=26, vitesse=44.0, seed=845, entree=True)))
    elif o in ("plaine_horde", "plaine_fige"):
        if not hasattr(sc, "_gog_fige"):
            sc._gog_fige = []
            sc.anims.append(anim_plaine(sc._gog_fige, torches=70 if suff == "_nuit" else 0, fige_debut=(o == "plaine_fige")))
    elif o == "bande":
        if not hasattr(sc, "_gog_bande"):
            sc._gog_bande = []
            sc.anims.append(anim_bande(sc._gog_bande))
    elif o == "lac":
        if not hasattr(sc, "_gog_lac"):
            sc._gog_lac = []
            sc.anims.append(anim_lac(sc._gog_lac, suff))
    elif o == "vent":                                                # poussière légère portée par le vent
        sc.avant.append(anim_vent())
    elif o == "feu_camp":
        sc.feu(540, 1336)
    elif o == "tawaf":
        sc.anims.append(anim_tawaf())
    elif o == "escalade":
        sc.anims.append(anim_escalade())
    elif o == "horde_hauteurs":
        sc.anims.append(anim_horde_hauteurs(0.0))
    elif o == "effondre":                                            # le barrage tombe dès le début du plan
        sc.anims.append(G.anim_barrage_tombe(0.0, 13.0, suff or "_fin"))
    else:
        return False
    return True


def annotation(sc, k_, mots, t, bg):
    d_ = next((float(m_.rstrip("s").replace(",", ".")) for m_ in mots[1:]
               if m_.rstrip("s").replace(",", "").replace(".", "").isdigit()), None)
    suff = G._suffixe(bg)
    if k_ == "lac_bu":
        if not hasattr(sc, "_gog_lac"):
            sc._gog_lac = []
            sc.anims.append(anim_lac(sc._gog_lac, suff))
        sc._gog_lac.append((t, d_ or 9.0))
    elif k_ == "fleches":
        sc.anims.append(anim_fleches(t, d_ or 9.0))
    elif k_ == "trou":
        sc.anims.append(anim_trou(t))
    elif k_ == "mille":
        if getattr(sc, "_gog_part", None):
            sc._gog_part[0] = t
        sc.anims.append(anim_mille(t, d_ or 7.0))
    elif k_ == "part_feu":
        sc._gog_part = [None]
        f0, box = anim_part(t, d_ or 9.0), sc._gog_part
        sc.anims.append(lambda img, u, f0=f0, box=box: None if (box[0] is not None and u >= box[0]) else f0(img, u))
    elif k_ == "dix":
        sc.anims.append(anim_dix(t, d_ or 5.0))
    elif k_ == "oiseaux_emportent":
        if not hasattr(sc, "_gog_bande"):
            sc._gog_bande = []
            sc.anims.append(anim_bande(sc._gog_bande))
        sc._gog_bande.append((t, d_ or 10.0))
    elif k_ == "horde_fige":
        if not hasattr(sc, "_gog_fige"):
            sc._gog_fige = []
            sc.anims.append(anim_plaine(sc._gog_fige, torches=70 if suff == "_nuit" else 0))
        sc._gog_fige.append(t)
    elif k_ == "horde_hauteurs":
        sc.anims.append(anim_horde_hauteurs(t))
    return True
