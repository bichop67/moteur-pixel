# LA MER QUI S'OUVRE (film « Moussa », version conte, 02/11/2026) — séquence refaite en entier après le retour de
# l'utilisateur sur l'ancienne mer_ouverte (« c'est quoi cette daube ? les graphismes sont ignobles »).
# Toile 16:9 du film : x = -105 … 375, y = 0 … 480, fenêtre visible du plan large ≈ y 100 … 370, pieds à y = 330.
#   mer_rivage (+ _jour)   vue de côté : la plage à gauche, la mer immense à droite, le soleil bas ; (la poursuite)
#   mer_face               vue de face depuis la plage : la mer fermée jusqu'à l'horizon (avant le coup de bâton)
#   mer_canyon             vue de face : la mer fendue, deux murailles d'eau, le chemin sec jusqu'au soleil
#                          (état final de {mer_fend N} ; utilisable seul)
#   mer_fendue             vue d'en haut : douze chemins secs entre les murailles (option « tribus » : les tribus marchent)
#   mer_couloir            dans un chemin, vue de côté : la muraille d'eau (poissons, coraux, une fenêtre sur le chemin
#                          voisin), le fond de la mer sec ; option « mer_vie » : poissons, bulles, lumière qui joue
#   sous_la_mer            sous les flots : la surface vue d'en dessous, rayons de lumière, bulles, débris qui coulent
#   mer_rivage_corps       la mer redevenue calme ; au loin, sur une hauteur, une petite forme sombre (le corps de Pharaon)
# Animations : anim_mer_fend (la mer se fend et se dresse), anim_mer_referme (les murailles s'écroulent, devant les persos),
#   anim_tribus (les tribus dans les douze chemins), anim_vie_couloir, anim_vie_rivage, anim_sous_mer.
import math

import numpy as np
from PIL import Image, ImageDraw

import egypte
import lieux
from egypte import _Px, _ciel
from lieux import R, dk, lt, mix
from px import BAYER

# ---------------------------------------------------------------- palette
EAU_HAUT = (104, 204, 216)          # haut d'une muraille (la lumière la traverse)
EAU_MI = (40, 132, 176)
EAU_BAS = (14, 50, 98)
EAU_FOND = (8, 28, 62)
ECUME = (236, 248, 250)
ECUME2 = (196, 232, 240)
SABLE = (228, 204, 156)
SABLE_OMB = (182, 152, 108)
SABLE_MOUILLE = (150, 128, 100)
HORIZON_AUBE = (250, 196, 156)
SOLEIL = (255, 232, 180)


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
    """Remplit le masque m avec un dégradé à plusieurs couleurs le long de t (0..1), en paliers tramés (pixel art)."""
    q = np.floor(np.clip(t, 0, 1) * (steps - 1) + _bay(c)) / (steps - 1)
    col = _stops(stops, q)
    c.a[m] = np.clip(col[m], 0, 255).astype(np.uint8)
    c.al[m] = True


def _melange(c, m, col, k):
    """Teinte douce (k = 0..1, tableau ou nombre) vers col, dans le masque m."""
    a = c.a.astype(np.float32)
    kk = np.broadcast_to(np.asarray(k, np.float32), m.shape)
    sel = m & (kk > 0)
    a[sel] = a[sel] * (1 - kk[sel, None]) + np.array(col, np.float32) * kk[sel, None]
    c.a = np.clip(a, 0, 255).astype(np.uint8)


def _tri(c, pts):
    return c.mask_poly(pts)


# ---------------------------------------------------------------- textures d'eau
def _muraille(c, m, ytop, ybot, seed, lum_x=None, poissons=10, coraux=True, base=None):
    """Une face de muraille d'eau, de ytop (crête) à ybot (pied) : dégradé profond, bandes de lumière, réseau de
    caustiques, traînées, poissons en ombre, bulles ; au pied, algues et coraux. lum_x : x d'où vient la lumière
    (la face s'éclaire de ce côté)."""
    rr = R(seed)
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    t = (Y - ytop) / max(1, ybot - ytop)
    _peint(c, m, t, [(0.0, lt(EAU_HAUT, 0.12)), (0.18, EAU_HAUT), (0.42, EAU_MI), (0.75, EAU_BAS), (1.0, EAU_FOND)], 14)
    if lum_x is not None:                                        # la face s'éclaire du côté de la lumière
        d = np.clip(1 - np.abs(X - lum_x) / 160.0, 0, 1) ** 1.6
        _melange(c, m, (150, 226, 236), d * 0.22 * (1 - t * 0.7))
    band = np.sin(Y * 0.85 + np.sin(X * 0.06) * 2.4) > 0.965     # bandes de lumière horizontales (réfraction)
    _melange(c, m & band & (t < 0.7), (176, 236, 242), 0.24)
    v = (np.sin(X * 0.19 + 1.7 * np.sin(Y * 0.05)) + np.sin(Y * 0.23 + 1.3 * np.sin(X * 0.07))
         + np.sin((X + Y) * 0.11 + 0.8))
    proba = np.clip(1.0 - t / 0.6, 0, 1)                           # caustiques : fin réseau de lumière, en haut
    reseau = (np.abs(v) < 0.16) & (_bay(c) < proba)
    _melange(c, m & reseau, (204, 246, 250), 0.5)
    _melange(c, m & (np.abs(v) < 0.34) & ~reseau & (_bay(c) < proba * 0.6), (160, 226, 238), 0.16)
    for _ in range(int(m.sum() / 1700)):                          # traînées verticales (l'eau qui coule dans la paroi)
        x, y = rr.randint(-105, 374), rr.randint(int(ytop), int(ybot))
        if m[y, x + c.ox]:
            L_ = rr.randint(5, 22)
            seg = m & c.mask_rect(x, y, x, y + L_)
            _melange(c, seg, (150, 214, 230) if y < (ytop + ybot) / 2 else (60, 130, 170), 0.35)
    for _ in range(poissons):                                     # poissons en ombre (la lumière passe autour)
        x, y = rr.randint(-100, 370), rr.randint(int(ytop + (ybot - ytop) * 0.25), int(ytop + (ybot - ytop) * 0.8))
        if not m[y, x + c.ox]:
            continue
        s_ = rr.choice((1, 1, 1.4, 2))
        d_ = 1 if rr.random() < 0.5 else -1
        f = (c.mask_ell(x, y, 3.2 * s_, 1.3 * s_) |
             c.mask_poly([(x - 3 * s_ * d_, y), (x - 6 * s_ * d_, y - 2.2 * s_), (x - 6 * s_ * d_, y + 2.2 * s_)]))
        _melange(c, f & m, (10, 34, 62), 0.55)
    for _ in range(int(m.sum() / 700)):                           # petites bulles
        x, y = rr.randint(-105, 374), rr.randint(int(ytop), int(ybot))
        if m[y, x + c.ox]:
            c.fill(m & c.mask_rect(x, y, x, y), (172, 226, 238) if rr.random() < 0.7 else (220, 246, 250))
    if coraux:                                                    # au pied : algues, coraux, rochers du fond
        yb = int(ybot)
        for _ in range(int(m[yb - 1].sum() / 7) + 1):
            x = rr.randint(-105, 374)
            if not m[yb - 1, x + c.ox]:
                continue
            kind = rr.random()
            if kind < 0.55:                                       # algue qui ondule
                h = rr.randint(6, 18)
                ph = rr.uniform(0, 6.28)
                col = rr.choice([(26, 88, 74), (34, 110, 84), (20, 70, 64)])
                for j in range(h):
                    xx = int(round(x + math.sin(j * 0.45 + ph) * 1.6))
                    c.fill(m & c.mask_rect(xx, yb - 1 - j, xx, yb - 1 - j), col if j < h - 2 else lt(col, 0.25))
            elif kind < 0.8:                                      # corail
                col = rr.choice([(196, 104, 92), (214, 140, 96), (170, 90, 120)])
                for j in range(rr.randint(2, 4)):
                    xx = x + rr.randint(-3, 3)
                    hh = rr.randint(3, 7)
                    c.fill(m & c.mask_rect(xx, yb - hh, xx, yb - 1), dk(col, 0.85))
                    c.fill(m & c.mask_rect(xx - 1, yb - hh, xx + 1, yb - hh), col)
            else:                                                 # rocher du fond
                w_ = rr.randint(3, 6)
                r_ = c.mask_ell(x, yb - 1, w_, w_ * 0.7) & c.mask_rect(x - w_, yb - w_, x + w_, yb - 1)
                c.fill(m & r_, (40, 70, 92))
                c.fill(m & r_ & ~np.roll(r_, 1, axis=0), (70, 108, 126))


def _crete(c, m_mur, ytop_f, seed, epaisseur=3):
    """Écume de la crête : bande blanche ondulée au sommet de la muraille + embruns au-dessus."""
    rr = R(seed)
    X = c.xx.astype(np.float32)
    Y = c.yy.astype(np.float32)
    top = ytop_f(X)
    ond = top + 1.5 * np.sin(X * 0.31) + 1.0 * np.sin(X * 0.83 + 1.7)
    bande = m_mur & (Y <= ond + epaisseur) & (Y >= top - 1)
    c.fill(bande, ECUME)
    c.fill(m_mur & (Y > ond + epaisseur) & (Y <= ond + epaisseur + 2) & (_bay(c) < 0.5), ECUME2)
    for _ in range(int(np.count_nonzero(bande) / 9) + 6):         # embruns
        x = rr.randint(-105, 374)
        cols = np.nonzero(bande[:, x + c.ox])[0]
        if len(cols):
            y = cols.min() - rr.randint(1, 6)
            if y > 0:
                c.px(x, y, ECUME if rr.random() < 0.6 else ECUME2)


def _sable(c, m, y0, y1, seed, ripples=True, mouille=0.0, coquillages=40):
    """Le fond de la mer asséché / la plage : dégradé, rides du sable, coquillages, cailloux."""
    rr = R(seed)
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    t = (Y - y0) / max(1, y1 - y0)
    _peint(c, m, t, [(0.0, lt(SABLE, 0.08)), (0.5, SABLE), (1.0, SABLE_OMB)], 10)
    if ripples:                                                    # rides parallèles (sable sculpté par la mer)
        rid = np.sin(Y * 1.15 + np.sin(X * 0.09) * 2.2 + np.sin(X * 0.023) * 3) > 0.82
        _melange(c, m & rid, dk(SABLE, 0.78), 0.55)
        rid2 = np.sin(Y * 1.15 + np.sin(X * 0.09) * 2.2 + np.sin(X * 0.023) * 3 - 0.7) > 0.9
        _melange(c, m & rid2, (246, 230, 196), 0.5)
    if mouille:
        tache = (np.sin(X * 0.05 + 1.2) * np.sin(Y * 0.11) + np.sin(X * 0.11 - Y * 0.07)) > 1.15
        _melange(c, m & tache, SABLE_MOUILLE, mouille)
    for _ in range(coquillages):
        x, y = rr.randint(-100, 370), rr.randint(int(y0) + 2, int(y1) - 2)
        if not m[y, x + c.ox]:
            continue
        k = rr.random()
        if k < 0.4:                                               # coquillage clair
            c.fill(c.mask_ell(x, y, 1.6, 1.0) & m, (248, 236, 222))
            c.px(x, y + 1, (190, 160, 140))
        elif k < 0.65:                                            # caillou
            c.fill(c.mask_ell(x, y, 2.2, 1.3) & m, (150, 136, 120))
            c.px(x - 1, y - 1, (190, 178, 162))
        elif k < 0.8:                                             # étoile de mer
            col = (224, 126, 84)
            for (dx, dy) in ((0, -2), (-2, 0), (2, 0), (-1, 2), (1, 2), (0, 0), (0, -1), (-1, 0), (1, 0), (0, 1)):
                c.px(x + dx, y + dy, col)
        else:                                                     # touffe d'algue échouée
            for j in range(3):
                c.px(x + j - 1, y - (j % 2), (60, 96, 70))


def _rocher(c, x, y, w, h, base=(120, 104, 92), seed=1):
    rr = R(seed)
    m = c.mask_ell(x, y, w, h) & c.mask_rect(x - w, y - h, x + w, y + 1)
    for _ in range(3):
        m |= c.mask_ell(x + rr.randint(-w // 2, w // 2), y - rr.randint(0, h // 2), w * 0.6, h * 0.7) & \
            c.mask_rect(x - w, y - h, x + w, y + 1)
    c.shape(m, base, dk(base, 0.7), lt(base, 0.18), band=2, olcol=dk(base, 0.45))
    return m


# ---------------------------------------------------------------- la mer vue de côté (rivage)
RIVE = [(-20, 196), (70, 250), (170, 314), (230, 372), (270, 480)]     # ligne du rivage (plage à gauche)


def mer_rivage(heure="aube", corps=False):
    """Vue de côté : la plage à gauche (dunes, rochers, herbes), la mer immense à droite jusqu'à l'horizon, le soleil
    bas sur l'eau et sa traînée de lumière ; au loin à gauche, les montagnes d'Égypte (d'où vient l'armée).
    corps=True : la mer calme (jour) et, au loin à droite, sur un rocher qui domine l'eau, une petite forme sombre."""
    c = _Px()
    H = 196                                                       # horizon
    sol = dict(aube=(296, 176), jour=(250, 70))[heure]
    sky = _ciel(c, heure, H, sol, seed=811)
    snap = c.a.copy()
    rr = R(812)
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    # montagnes lointaines (à gauche, derrière la plage)
    for (pts, col) in (([(-105, H), (-105, 168), (-70, 160), (-40, 170), (-10, 156), (30, 172), (60, 166), (90, H)],
                        mix((150, 120, 140), lieux.mix((250, 196, 156), (200, 214, 236), 0.0 if heure == "aube" else 1.0), 0.45)),
                       ([(-105, H), (-105, 180), (-60, 176), (-20, 182), (20, 178), (70, 186), (110, H)],
                        mix((170, 132, 128), (236, 200, 170) if heure == "aube" else (210, 220, 236), 0.35))):
        c.fill(c.mask_poly(pts), col)
    # la mer
    mer = c.mask_rect(-105, H, 375, 480) & ~c.mask_poly([(-105, H)] + RIVE + [(-105, 480)])
    hz = (210, 176, 176) if heure == "aube" else (176, 210, 230)
    t = (Y - H) / (480 - H)
    _peint(c, mer, t, [(0.0, hz), (0.08, (120, 140, 176) if heure == "aube" else (96, 160, 200)),
                       (0.35, (44, 104, 150)), (0.75, (22, 66, 116)), (1.0, (12, 42, 84))], 14)
    for y in range(H + 2, 480, 1):                                 # vagues en perspective
        d = (y - H) / (480 - H)
        n = int(3 + d * 10)
        for _ in range(n):
            x = rr.randint(-105, 374)
            L_ = int(1 + d * rr.randint(3, 16))
            if mer[y, x + c.ox] and rr.random() < 0.55:
                seg = mer & c.mask_rect(x, y, x + L_, y)
                c.fill(seg, mix((200, 228, 240), hz, 0.4 * (1 - d)) if rr.random() < 0.5 else dk(c.a[y, x + c.ox].tolist(), 0.8))
    sx = sol[0]                                                    # la traînée du soleil sur l'eau
    for y in range(H + 1, 420, 2):
        d = (y - H) / (420 - H)
        w_ = 2 + d * 26
        for _ in range(int(2 + d * 5)):
            x = sx + rr.uniform(-w_, w_)
            L_ = int(1 + d * 6)
            seg = mer & c.mask_rect(x, y, x + L_, y)
            c.fill(seg, (255, 222, 170) if heure == "aube" else (255, 248, 226))
    # plage
    plage = c.mask_poly([(-105, H)] + RIVE + [(-105, 480)])
    _sable(c, plage, H, 480, seed=813, ripples=False, coquillages=70)
    mouille = plage & ~c.mask_poly([(-105, H)] + [(x - 7, y) for x, y in RIVE] + [(-105, 480)])
    _melange(c, mouille, SABLE_MOUILLE, 0.65)
    _melange(c, mouille, (180, 170, 190) if heure == "aube" else (170, 200, 220), 0.25)
    for k in range(len(RIVE) - 1):                                 # l'écume au bord de l'eau
        (xa, ya), (xb, yb) = RIVE[k], RIVE[k + 1]
        for s in np.linspace(0, 1, 60):
            x, y = xa + (xb - xa) * s, ya + (yb - ya) * s
            c.fill(c.mask_rect(x + 1, y, x + 3 + rr.randint(0, 2), y), ECUME)
            if rr.random() < 0.5:
                c.fill(c.mask_rect(x + 5, y, x + 6, y), ECUME2)
    # herbes des dunes et rochers
    for _ in range(26):
        x, y = rr.randint(-100, 120), rr.randint(H + 6, 300)
        if plage[y, x + c.ox] and not mouille[y, x + c.ox]:
            for j in range(rr.randint(3, 6)):
                xx = x + rr.randint(-3, 3)
                hh = rr.randint(3, 7)
                for k in range(hh):
                    c.px(xx + (1 if k > hh * 0.6 and j % 2 else 0), y - k, (126, 140, 84) if k < hh - 1 else (176, 186, 120))
    _rocher(c, -84, 304, 16, 10, seed=814)
    _rocher(c, 40, 262, 9, 6, seed=815)
    _rocher(c, -40, 372, 22, 12, base=(110, 96, 86), seed=816)
    if corps:                                                      # au loin, sur le rivage : une petite hauteur rocheuse
        hm = _rocher(c, 6, 226, 11, 9, base=(150, 136, 124), seed=817)  # et, dessus, une petite forme sombre (de loin)
        _rocher(c, 16, 229, 6, 4, base=(142, 128, 116), seed=818)
        top_y = int(np.nonzero(hm[:, 6 + c.ox - 3:6 + c.ox + 4].any(axis=1))[0].min())
        c.fill(c.mask_rect(2, top_y - 1, 8, top_y - 1), (60, 48, 50))
        c.px(9, top_y - 1, (226, 192, 96))
        for (x, y, L_) in ((150, 340, 9), (196, 372, 7), (120, 356, 6)):   # quelques débris rejetés sur le sable
            c.fill(c.mask_rect(x, y, x + L_, y), (110, 92, 74))
    return lieux.relief(c, snap, sky), None


# ---------------------------------------------------------------- vue de face (depuis la plage)
HF, YS, VP = 176, 306, (135, 176)                                 # horizon, bord de l'eau, point de fuite
W0, TOP = 58, 122                                                 # demi-largeur du chemin au bord, crête des murailles


def _plage_face(c, rr, ferme=True):
    plage = c.mask_rect(-105, YS, 375, 480)
    _sable(c, plage, YS, 480, seed=821, ripples=False, coquillages=60)
    m_ = plage & c.mask_rect(-105, YS, 375, YS + 9)
    _melange(c, m_, SABLE_MOUILLE, 0.6)
    _melange(c, m_, (200, 170, 170), 0.2)
    X = c.xx.astype(np.float32)
    ec = YS + 1.4 * np.sin(X * 0.17) + np.sin(X * 0.53 + 1)
    e = plage & (c.yy <= ec + 1.5)
    if not ferme:
        e &= (X < VP[0] - W0) | (X > VP[0] + W0)
    c.fill(e, ECUME)
    for _ in range(20):
        x, y = rr.randint(-100, 370), rr.randint(YS + 14, 400)
        for j in range(rr.randint(3, 6)):
            xx = x + rr.randint(-3, 3)
            hh = rr.randint(3, 7)
            for k in range(hh):
                c.px(xx, y - k, (126, 140, 84) if k < hh - 1 else (176, 186, 120))
    _rocher(c, -96, 360, 20, 13, seed=822)
    _rocher(c, 362, 352, 22, 14, base=(112, 98, 88), seed=823)


def mer_face():
    """Vue de face, depuis la plage : la mer fermée, immense, jusqu'à l'horizon ; le soleil se lève juste au-dessus ;
    au loin, l'autre rive (montagnes bleutées). Les persos se tiennent sur la plage (pieds y = 330)."""
    c = _Px()
    rr = R(820)
    _ciel(c, "aube", HF, (VP[0] + 4, HF - 6), seed=824)
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    c.fill(c.mask_poly([(-105, HF), (-105, 170), (-40, 166), (20, 171), (80, 164), (150, 170), (220, 163),
                        (300, 169), (375, 165), (375, HF)]), (150, 132, 170))
    mer = c.mask_rect(-105, HF, 375, YS)
    t = (Y - HF) / (YS - HF)
    _peint(c, mer, t, [(0.0, (230, 186, 170)), (0.06, (150, 150, 186)), (0.3, (60, 112, 160)), (0.7, (30, 80, 132)),
                       (1.0, (22, 64, 114))], 14)
    for y in range(HF + 1, YS):
        d = (y - HF) / (YS - HF)
        for _ in range(int(4 + d * 14)):
            x = rr.randint(-105, 374)
            L_ = int(1 + d * rr.randint(3, 14))
            if rr.random() < 0.5:
                c.fill(mer & c.mask_rect(x, y, x + L_, y), mix((200, 226, 240), (230, 186, 170), 0.5 * (1 - d)))
            elif rr.random() < 0.6:
                c.fill(mer & c.mask_rect(x, y, x + L_, y), mix((16, 50, 96), (150, 150, 186), 0.6 * (1 - d)))
    for y in range(HF + 1, YS, 2):                                 # la traînée du soleil
        d = (y - HF) / (YS - HF)
        w_ = 1 + d * 22
        for _ in range(int(2 + d * 4)):
            x = VP[0] + 4 + rr.uniform(-w_, w_)
            c.fill(mer & c.mask_rect(x, y, x + int(1 + d * 5), y), (255, 222, 172))
    _plage_face(c, rr, ferme=True)
    return c, None


def _crete_canyon(xs):
    """Ligne de crête des murailles vues de face (un peu plus haute près du chemin, ondulée)."""
    pres = np.exp(-((xs - VP[0]) / 90.0) ** 2)
    return TOP - 6 * pres + 1.6 * np.sin(xs * 0.07) + 1.2 * np.sin(xs * 0.19 + 1.1)


def mer_canyon():
    """Vue de face : la mer fendue. Deux murailles d'eau montent plus haut que l'image, de chaque côté d'un chemin de
    sable sec qui file jusqu'au soleil levant, sur l'autre rive. Faces avant : eau profonde (lumière, poissons, coraux
    au pied) ; parois du chemin éclairées par le ciel ; brume dorée au loin."""
    c = _Px()
    rr = R(830)
    _ciel(c, "aube", HF, (VP[0], HF - 5), seed=831)
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    xl, xr = VP[0] - W0, VP[0] + W0
    crete_f = _crete_canyon
    gauche = c.mask_rect(-105, 0, xl, YS) & (Y >= crete_f(X))
    droite = c.mask_rect(xr + 1, 0, 375, YS) & (Y >= crete_f(X))
    _muraille(c, gauche, TOP, YS, seed=832, lum_x=xl, poissons=12)
    _muraille(c, droite, TOP, YS, seed=833, lum_x=xr, poissons=12)
    loin_bord = np.clip(np.abs(X - VP[0]) / 240.0, 0, 1) ** 1.5     # les faces s'assombrissent vers les bords de l'image
    _melange(c, gauche | droite, (8, 26, 58), loin_bord * 0.35)
    _crete(c, gauche | droite, crete_f, seed=834, epaisseur=3)
    # les parois du chemin (en perspective), éclairées par le ciel
    pl = _tri(c, [(xl, YS), (xl, TOP), VP])
    pr = _tri(c, [(xr, YS), (xr, TOP), VP])
    for (pm, xe, sgn) in ((pl, xl, 1), (pr, xr, -1)):
        h = (YS - Y) / (YS - TOP)                                 # 0 au pied, 1 en haut, sur l'arête avant
        prof = np.clip(np.abs(X - VP[0]) / W0, 0, 1)               # 1 près de nous, 0 au loin
        haut = np.clip((Y - (VP[1] + (TOP - VP[1]) * prof)) / np.maximum(1, (YS - TOP) * prof), 0, 1)
        _peint(c, pm, haut, [(0.0, (150, 222, 230)), (0.3, (86, 176, 204)), (0.7, (36, 112, 160)), (1.0, (20, 70, 120))], 12)
        lvl = np.abs(np.sin(haut * 34))                            # lignes qui filent vers le point de fuite
        _melange(c, pm & (lvl < 0.08), (180, 236, 242), 0.35)
        brume = (1 - prof) ** 1.5
        _melange(c, pm, HORIZON_AUBE, brume * 0.7)
        arete = pm & (np.abs(X - xe) <= 1)
        c.fill(arete & (Y > TOP + 2), (214, 246, 250))
    for (xe, sg) in ((xl, 1), (xr, -1)):                          # écume sur l'arête haute des parois
        for s_ in np.linspace(0, 1, 120):
            x = xe + (VP[0] - xe) * s_
            y = TOP + (VP[1] - TOP) * s_
            if rr.random() < 0.8 * (1 - s_) + 0.1:
                c.px(int(round(x)), int(round(y)) + rr.randint(-1, 1), ECUME if rr.random() < 0.6 else ECUME2)
    # le sol du chemin : sable sec, rides en perspective, brume dorée au loin
    sol = _tri(c, [(xl, YS + 1), (xr, YS + 1), VP]) & (Y >= VP[1])
    z = np.clip((YS - VP[1]) / np.maximum(0.6, Y - VP[1]), 1, 60)  # profondeur (1 = au bord)
    _peint(c, sol, np.clip((z - 1) / 14, 0, 1), [(0.0, SABLE_OMB), (0.35, SABLE), (1.0, (248, 222, 182))], 10)
    rid = (np.sin(z * 5.2) > 0.75) & (z < 18)
    _melange(c, sol & rid, dk(SABLE, 0.78), 0.45)
    _melange(c, sol, HORIZON_AUBE, np.clip((z - 4) / 30, 0, 1) * 0.8)
    for _ in range(26):                                            # coquillages et flaques sur le sol
        y = rr.randint(VP[1] + 18, YS)
        half = W0 * (y - VP[1]) / (YS - VP[1])
        x = VP[0] + rr.uniform(-half * 0.8, half * 0.8)
        if rr.random() < 0.4:
            c.fill(c.mask_ell(x, y, 2 + (y - VP[1]) / 40, 0.8 + (y - VP[1]) / 120) & sol, (176, 186, 196))
        else:
            c.px(int(x), y, (248, 238, 224))
    # le ciel dans la fente, au loin : le soleil qui se lève sur l'autre rive
    fente = _tri(c, [(xl, TOP), (xr, TOP), VP]) & ~pl & ~pr
    c.glow(VP[0], VP[1] - 4, 70, (255, 214, 160), 0.55, m=fente | sol | pl | pr)
    c.fill(c.mask_ell(VP[0], VP[1] - 4, 6, 6) & (Y < VP[1]), SOLEIL)
    # écume au pied des murailles et sur les arêtes
    for (xe, sg) in ((xl, -1), (xr, 1)):
        for y in range(TOP + 3, YS, 1):
            if rr.random() < 0.35:
                c.px(int(xe + sg * rr.randint(0, 2)), y, ECUME if rr.random() < 0.5 else ECUME2)
    pied = (gauche | droite) & (Y >= YS - 3)
    c.fill(pied & (np.sin(X * 0.4) + np.sin(X * 0.9) > -0.6), ECUME)
    _plage_face(c, rr, ferme=False)
    sol_plage = c.mask_rect(xl, YS, xr, YS + 10)                   # le chemin continue sur la plage (sable sec)
    _melange(c, sol_plage, SABLE, 0.6)
    return c, None


# ---------------------------------------------------------------- vue d'en haut : douze chemins
HA, YA, VPA = 150, 300, (135, 150)
CHEMINS = [-84 + i * 39 for i in range(12)]                        # x des douze chemins au bord de l'eau
WC = 5                                                             # demi-largeur d'un chemin au bord


def _z_a(Y):
    return np.clip((YA - VPA[1]) / np.maximum(0.6, Y - VPA[1]), 1, 80)


def mer_fendue():
    """Vue d'en haut, depuis la dune : la mer est coupée par douze chemins secs qui filent vers l'autre rive, entre de
    longues murailles d'eau (dessus des murailles : la mer, avec l'écume des crêtes le long des chemins). Brume dorée
    au loin, soleil levant. Premier plan : la dune où l'on se tient (pieds y = 330)."""
    c = _Px()
    rr = R(840)
    _ciel(c, "aube", HA, (VPA[0] + 30, HA - 10), seed=841)
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    c.fill(c.mask_poly([(-105, HA), (-105, 142), (-30, 138), (40, 144), (110, 136), (190, 143), (260, 137),
                        (375, 142), (375, HA)]), (156, 128, 160))
    mer = c.mask_rect(-105, HA, 375, YA + 8)                        # (sous le bord de la dune : pas de trou)
    z = _z_a(Y)
    t = (Y - HA) / (YA - HA)
    _peint(c, mer, t, [(0.0, (232, 190, 168)), (0.08, (140, 150, 184)), (0.35, (54, 116, 164)), (1.0, (26, 82, 136))], 14)
    for y in range(HA + 1, YA):                                     # vagues sur le dessus des murailles
        d = (y - HA) / (YA - HA)
        for _ in range(int(3 + d * 12)):
            x = rr.randint(-105, 374)
            if rr.random() < 0.55:
                c.fill(mer & c.mask_rect(x, y, x + int(1 + d * rr.randint(2, 9)), y),
                       mix((196, 226, 240), (232, 190, 168), 0.5 * (1 - d)))
    for xc in CHEMINS:                                               # les douze chemins
        a, b = (xc - WC, YA), (xc + WC, YA)
        ch = _tri(c, [a, b, VPA]) & (Y > HA)
        sh = _tri(c, [(xc - WC - 5, YA), (xc - WC, YA), VPA]) & (Y > HA)       # paroi à l'ombre
        lu = _tri(c, [(xc + WC, YA), (xc + WC + 3, YA), VPA]) & (Y > HA)       # paroi éclairée
        _peint(c, sh, np.clip((z - 1) / 12, 0, 1), [(0.0, (14, 46, 90)), (1.0, (60, 90, 140))], 6)
        _peint(c, lu, np.clip((z - 1) / 12, 0, 1), [(0.0, (110, 196, 218)), (1.0, (180, 200, 214))], 6)
        _peint(c, ch, np.clip((z - 1) / 20, 0, 1), [(0.0, SABLE), (1.0, (246, 220, 182))], 8)
        cr = (_tri(c, [(xc - WC - 7, YA), (xc - WC - 5, YA), VPA]) | _tri(c, [(xc + WC + 3, YA), (xc + WC + 5, YA), VPA])) & (Y > HA)
        c.fill(cr & (_bay(c) < 0.55), ECUME)
    _melange(c, mer, HORIZON_AUBE, np.clip((z - 3) / 26, 0, 1) * 0.85)   # brume dorée au loin
    c.glow(VPA[0] + 30, HA - 10, 80, (255, 214, 160), 0.45)
    c.fill(c.mask_ell(VPA[0] + 30, HA - 9, 6, 6) & (Y < HA), SOLEIL)
    # la dune au premier plan
    dune = c.mask_poly([(-105, YA - 4), (0, YA - 2), (80, YA + 2), (180, YA - 1), (260, YA + 3), (375, YA - 3), (375, 480), (-105, 480)])
    _sable(c, dune, YA - 4, 480, seed=842, ripples=False, coquillages=30)
    bord = dune & ~np.roll(dune, 2, axis=0)
    c.fill(bord, lt(SABLE, 0.18))
    for _ in range(24):
        x, y = rr.randint(-100, 370), rr.randint(YA + 10, 400)
        for j in range(rr.randint(3, 6)):
            xx = x + rr.randint(-3, 3)
            hh = rr.randint(3, 8)
            for k in range(hh):
                c.px(xx, y - k, (120, 136, 82) if k < hh - 1 else (172, 184, 118))
    _rocher(c, -92, 352, 22, 13, seed=843)
    _rocher(c, 360, 344, 20, 12, base=(112, 98, 88), seed=844)
    return c, None


# ---------------------------------------------------------------- dans un chemin, vue de côté
YC_TOP, YC_SOL = 128, 318
FENETRES = [(-30, 206, 26, 70), (262, 214, 24, 64)]                # (x centre, y haut, largeur, hauteur)


def mer_couloir():
    """Dans un des douze chemins, vue de côté : derrière, la muraille d'eau monte jusqu'au ciel (crête d'écume, lumière
    qui la traverse, poissons, coraux et algues au pied) ; deux « fenêtres » dans l'eau laissent voir le chemin voisin ;
    devant, le fond de la mer asséché (sable ridé, coquillages, étoiles de mer). Pieds y = 330."""
    c = _Px()
    rr = R(850)
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    ciel = c.mask_rect(-105, 0, 375, YC_TOP + 6)
    _peint(c, ciel, Y / (YC_TOP + 6), [(0.0, (120, 150, 206)), (0.6, (226, 206, 200)), (1.0, (255, 222, 186))], 10)
    mur = c.mask_rect(-105, 0, 375, YC_SOL) & (Y >= YC_TOP + 1.5 * np.sin(X * 0.05) + 2 * np.sin(X * 0.013 + 1))
    _muraille(c, mur, YC_TOP, YC_SOL, seed=851, lum_x=None, poissons=22)
    raies = ((np.mod(X + Y * 0.55, 74) < 9) & (Y < YC_SOL - 30))    # rayons de lumière obliques dans l'eau
    _melange(c, mur & raies, (190, 240, 246), np.clip(1 - (Y - YC_TOP) / 170, 0, 1) * 0.22)
    _crete(c, mur, lambda xs: YC_TOP + 1.5 * np.sin(xs * 0.05) + 2 * np.sin(xs * 0.013 + 1), seed=852, epaisseur=3)
    for (xf, yf, wf, hf) in FENETRES:                               # fenêtres sur le chemin voisin
        f = c.mask_arch(xf - wf // 2, xf + wf // 2, yf, yf + hf)
        _peint(c, f, (Y - yf) / hf, [(0.0, (150, 214, 226)), (0.65, (96, 170, 200)), (1.0, (70, 140, 176))], 8)
        sol_f = f & (Y >= yf + hf - 7)
        _peint(c, sol_f, (Y - (yf + hf - 7)) / 7, [(0.0, (222, 206, 170)), (1.0, (196, 176, 136))], 4)
        bord = f & ~(np.roll(f, 1, 0) & np.roll(f, -1, 0) & np.roll(f, 1, 1) & np.roll(f, -1, 1))
        c.fill(bord & (Y < yf + hf - 6), (214, 246, 250))
        ext = (np.roll(f, 2, 1) | np.roll(f, -2, 1) | np.roll(f, -2, 0)) & ~f & mur
        _melange(c, ext, ECUME2, 0.5)
    sol = c.mask_rect(-105, YC_SOL, 375, 480)
    _sable(c, sol, YC_SOL, 480, seed=853, ripples=True, mouille=0.0, coquillages=70)
    pied = sol & (Y <= YC_SOL + 2)
    c.fill(pied, (120, 104, 84))
    c.fill(sol & (Y == YC_SOL + 3) & (_bay(c) < 0.5), (150, 130, 100))
    return c, None


# ---------------------------------------------------------------- sous les flots
def sous_la_mer():
    """Sous l'eau : en haut, la surface vue d'en dessous (ligne claire qui ondule) ; des rayons de lumière obliques ;
    l'eau devient noire vers le fond ; des particules en suspension. Personne n'est montré."""
    c = _Px()
    rr = R(860)
    X, Y = c.xx.astype(np.float32), c.yy.astype(np.float32)
    tout = c.mask_rect(-105, 0, 375, 480)
    _peint(c, tout, (Y - 96) / 290, [(0.0, (120, 196, 214)), (0.12, (60, 140, 176)), (0.4, (22, 78, 120)),
                                       (0.75, (10, 36, 70)), (1.0, (4, 14, 30))], 14)
    surf = 104 + 1.8 * np.sin(X * 0.09) + 1.2 * np.sin(X * 0.23 + 1)
    c.fill(tout & (Y <= surf), (176, 226, 236))
    c.fill(tout & (Y > surf) & (Y <= surf + 2) & (_bay(c) < 0.5), (140, 206, 222))
    for k in range(7):                                             # rayons de lumière
        x0 = -80 + k * 64 + rr.randint(-10, 10)
        r_ = c.mask_poly([(x0, 104), (x0 + 12, 104), (x0 + 70, 380), (x0 + 40, 380)])
        _melange(c, r_, (170, 226, 236), np.clip(1 - (Y - 104) / 260, 0, 1) * 0.16)
    for _ in range(420):                                           # particules
        x, y = rr.randint(-105, 374), rr.randint(110, 420)
        c.px(x, y, mix(tuple(int(v) for v in c.a[y, x + c.ox]), (180, 220, 230), 0.5))
    return c, None


# ---------------------------------------------------------------- animations
def _calque(img):
    return Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))


def _pose(img, lay):
    lieux.pose_calque(img, lay)


def _smooth(k):
    k = min(1.0, max(0.0, k))
    return k * k * k * (k * (k * 6 - 15) + 10)


_CANYON = []


def _canyon_rgb():
    """(image de mer_canyon, même image où la zone du chemin est remplie par l'eau des murailles, en miroir)."""
    if not _CANYON:
        bg = lieux.decor_large("mer_canyon")
        bg = bg[0] if isinstance(bg, tuple) else bg
        can = np.array(bg.a, np.uint8)
        eau = can.copy()
        c0 = VP[0] + 105
        for dx in range(0, W0 + 1):                               # colonnes du chemin <- colonnes de la muraille voisine
            eau[:, c0 - dx] = can[:, c0 - W0 - 1 - (W0 - dx)]
            eau[:, c0 + dx] = can[:, c0 + W0 + 1 + (W0 - dx)]
        _CANYON.append((can, eau))
    return _CANYON[0]


def anim_mer_fend(t_debut=0.0, duree=6.0):
    """Sur mer_face : la mer se fend. Une ligne d'écume file du bord jusqu'à l'horizon ; le chemin s'ouvre ; les deux
    murailles se dressent depuis la surface (plus vite près du chemin), crête d'écume ondulée et embruns qui jaillissent,
    jusqu'à l'image de mer_canyon, qui reste ensuite."""
    rr = R(870)
    gouttes = [(rr.uniform(-105, 375), rr.uniform(0, 1), rr.uniform(0.6, 1.5)) for _ in range(420)]
    xs = np.arange(-105, 375, dtype=np.float32)[None, :]
    ys = np.arange(0, 480, dtype=np.float32)[:, None]
    bay = BAYER[np.arange(480)[:, None] % 4, np.arange(480)[None, :] % 4]

    def f(img, u):
        if u < t_debut:
            return
        can, eau = _canyon_rgb()
        k = (u - t_debut) / duree
        if k >= 1.0:
            _pose(img, Image.fromarray(np.dstack([can, np.full(can.shape[:2], 255, np.uint8)]), "RGBA"))
            return
        tt = u - t_debut
        k1 = _smooth(min(1.0, k / 0.22))                           # la fente file jusqu'à l'horizon
        k2 = _smooth(max(0.0, (k - 0.1) / 0.6))                    # le chemin s'ouvre
        k3 = _smooth(max(0.0, (k - 0.16) / 0.84))                  # les murailles montent
        prof = np.clip((ys - VP[1]) / (YS - VP[1]), 0, 1)           # 1 au bord, 0 à l'horizon
        demi = W0 * k2 * prof
        dans_chemin = ((np.abs(xs - VP[0]) <= np.maximum(demi, 0.7 * k1)) & (ys >= VP[1]) & (prof >= 1 - k1)
                       & (ys <= YS + 10))
        pres = np.exp(-((xs - VP[0]) / 110.0) ** 2)                 # l'eau monte d'abord près du chemin
        kk = np.clip(k3 * (1.0 + 0.35 * pres) - 0.12 * (1 - pres) * (1 - k3), 0, 1)
        ond = (1 - k3) * (4 * np.sin(xs * 0.09 + tt * 3.1) + 2.5 * np.sin(xs * 0.23 - tt * 4.3))
        haut_mur = YS - (YS - (_crete_canyon(xs) - 1)) * kk + ond
        fente = W0 * k2 * np.clip((VP[1] - ys) / (VP[1] - TOP), 0, 1)        # au-dessus de l'horizon : la fente du ciel
        ecart = np.where(ys >= VP[1], demi, fente)
        mur = (np.abs(xs - VP[0]) > np.maximum(ecart, 0.5)) & (ys >= haut_mur) & (ys <= YS)
        m = dans_chemin | mur
        a = np.zeros((480, 480, 4), np.uint8)
        pas_ouvert = mur & (ys >= VP[1]) & (np.abs(xs - VP[0]) <= W0 * prof + 1)    # sous le chemin final, pas encore ouvert
        a[..., :3] = np.where(pas_ouvert[..., None], eau, can)
        a[..., 3] = np.where(m, 255, 0)
        if 0.0 < k3 < 0.97:                                          # la crête qui monte : écume épaisse, tramée
            crete = mur & (ys <= haut_mur + 3 + 2 * np.sin(xs * 0.5 + tt * 6))
            a[crete, :3] = ECUME
            sous = mur & (ys > haut_mur + 3) & (ys <= haut_mur + 7) & (bay < 0.5)
            a[sous, :3] = ECUME2
        bord = (dans_chemin & ~np.roll(dans_chemin, 2, axis=1)) | (dans_chemin & ~np.roll(dans_chemin, -2, axis=1))
        bord &= (ys < YS) & (bay < 0.75)
        a[bord, :3] = ECUME
        a[bord, 3] = 255
        lay = Image.fromarray(a, "RGBA")
        over = Image.new("RGBA", lay.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(over)
        if 0.02 < k3 < 0.97:                                         # embruns jetés vers le haut, gouttes qui retombent
            for (x, ph, sp) in gouttes:
                if abs(x - VP[0]) < W0 * k2:
                    continue
                xi = int(min(479, max(0, x + 105)))
                yc = float(haut_mur[0, xi])
                p = (ph + tt * 0.8 * sp) % 1.0
                y = yc - 26 * sp * 4 * p * (1 - p)
                X = x + 105 + math.sin(ph * 40 + tt) * 3 * p
                al = int(235 * (1 - p) * min(1.0, k3 * 5))
                d.point((X, y), fill=(242, 250, 252, al))
                if sp > 1.15:
                    d.point((X + 1, y), fill=(214, 238, 246, al))
                    d.point((X, y + 1), fill=(214, 238, 246, al // 2))
        if k1 < 1.0:                                                 # la ligne d'écume qui file vers l'horizon
            y_tete = YS - (YS - VP[1]) * k1
            d.line([(VP[0] + 105, YS), (VP[0] + 105, y_tete)], fill=ECUME + (255,), width=1)
        lay.alpha_composite(over)
        _pose(img, lay)
    return f


def anim_mer_referme(t_debut=0.0, duree=3.4):
    """Sur mer_couloir, DEVANT les persos : la crête de la muraille se recourbe et s'abat (lèvre d'écume, embruns),
    l'eau de l'autre muraille monte d'en bas ; les deux se rejoignent, l'eau brassée (écume, bulles, taches de
    lumière) remplit l'image puis s'assombrit vers le bleu profond de sous_la_mer. Aucun corps montré."""
    rr = R(880)
    bulles = [(rr.uniform(-105, 375), rr.uniform(100, 420), rr.uniform(0.5, 1.6)) for _ in range(220)]
    traines = [(rr.uniform(-105, 375), rr.uniform(0, 1), rr.randint(4, 22), rr.uniform(0.6, 1.4)) for _ in range(140)]
    taches = [(rr.uniform(-105, 375), rr.uniform(120, 380), rr.uniform(14, 40), rr.uniform(0, 6.28)) for _ in range(18)]
    embruns = [(rr.uniform(-105, 375), rr.uniform(0, 1), rr.uniform(0.6, 1.5)) for _ in range(200)]
    xs = np.arange(-105, 375, dtype=np.float32)[None, :]
    ys = np.arange(0, 480, dtype=np.float32)[:, None]
    bay = BAYER[np.arange(480)[:, None] % 4, np.arange(480)[None, :] % 4]
    colH = _stops([(0.0, (96, 196, 214)), (0.5, (40, 128, 172)), (1.0, (22, 82, 132))],
                  np.clip((ys - 100) / 300, 0, 1) + 0 * xs)
    colB = _stops([(0.0, (30, 100, 150)), (1.0, (12, 46, 90))], np.clip((ys - 150) / 330, 0, 1) + 0 * xs)

    def f(img, u):
        if u < t_debut:
            return
        k = min(1.0, (u - t_debut) / duree)
        tt = u - t_debut
        ka = _smooth(min(1.0, k / 0.5))                             # la lèvre du haut s'abat
        kb = _smooth(min(1.0, max(0.0, (k - 0.08) / 0.5)))          # l'eau d'en bas monte
        levre = (YC_TOP - 4 + (430 - YC_TOP) * ka + 9 * np.sin(xs * 0.045 + tt * 2.2) + 5 * np.sin(xs * 0.13 - tt * 3.0)
                 + 3 * np.sin(xs * 0.31 + tt * 5))
        monte = (490 - (490 - 120) * kb + 7 * np.sin(xs * 0.06 - tt * 2.6) + 4 * np.sin(xs * 0.17 + tt * 3.7)
                 + 3 * np.sin(xs * 0.41 + tt * 6.1) + 2 * np.sin(xs * 0.83 - tt * 4.4))
        haut = ys <= levre
        bas = ys >= monte
        a = np.zeros((480, 480, 4), np.uint8)
        a[..., :3] = np.where(haut[..., None], colH, colB).astype(np.uint8)
        a[..., 3] = np.where(haut | bas, 255, 0)
        lev = haut & (ys >= levre - 5 - 3 * np.abs(np.sin(xs * 0.21 + tt * 4)))      # lèvre d'écume
        a[lev, :3] = ECUME
        a[lev & (bay < 0.4), :3] = ECUME2
        mon = bas & (ys <= monte + 2 + 3 * np.abs(np.sin(xs * 0.4 + tt * 5))) & (bay < 1.0 - 0.8 * kb)
        a[mon, :3] = ECUME2
        lay = Image.fromarray(a, "RGBA")
        over = Image.new("RGBA", lay.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(over)
        for (x, ph, sp) in embruns:                                  # embruns au-dessus de la lèvre qui tombe
            if ka >= 0.99:
                continue
            xi = int(min(479, max(0, x + 105)))
            p = (ph + tt * 1.2 * sp) % 1.0
            y = float(levre[0, xi]) - 18 * sp * 4 * p * (1 - p) + 6
            d.point((x + 105, y), fill=(240, 250, 252, int(220 * (1 - p))))
        plein = min(1.0, max(0.0, (k - 0.35) / 0.3))
        if plein > 0:
            for (x, y, r_, ph) in taches:                            # taches de lumière qui tournent dans l'eau brassée
                X = x + 105 + 10 * math.sin(tt * 0.9 + ph)
                Y = y + 6 * math.cos(tt * 0.7 + ph)
                d.ellipse([X - r_ * 0.6, Y - r_ * 0.2, X + r_ * 0.6, Y + r_ * 0.2], fill=(150, 214, 230, int(22 * plein)))
            fin_ = 1 - max(0.0, k - 0.8) / 0.2
            for (x, ph, L_, sp) in traines:                          # traînées d'écume brassée
                y = 110 + ((ph + tt * 0.28 * sp) % 1.0) * 320
                X = x + 105 + 12 * math.sin(tt * 1.3 + ph * 6)
                d.line([(X, y), (X + L_, y + 3 * math.sin(ph * 9))], fill=(226, 244, 248, int(190 * plein * fin_)))
        if k >= 0.3:
            for (x, y0, sp) in bulles:
                y = y0 - (tt * 34 * sp) % 320
                if y > 100:
                    X = x + 105 + 2 * math.sin(tt * 3 + y0)
                    if sp > 1.2:
                        d.ellipse([X - 1.5, y - 1.5, X + 1.5, y + 1.5], outline=(206, 240, 248, 210))
                    else:
                        d.point((X, y), fill=(206, 240, 248, 210))
        if plein > 0:                                                # l'eau brassée ne laisse plus rien voir derrière
            ap = np.array(lay)
            ap[..., 3] = np.maximum(ap[..., 3], np.uint8(255 * plein))
            lay = Image.fromarray(ap, "RGBA")
        lay.alpha_composite(over)
        if k > 0.6:                                                  # vers le bleu profond (sous_la_mer)
            fon = _smooth((k - 0.6) / 0.4)
            lay.alpha_composite(Image.new("RGBA", lay.size, (16, 56, 96, int(255 * fon * 0.8))))
        _pose(img, lay)
    return f


def anim_tribus(t_debut=0.0, n=9, vitesse=0.05):
    """Sur mer_fendue : dans chacun des douze chemins, une file de minuscules marcheurs (et quelques bêtes) avance du
    bord vers l'horizon et rapetisse au loin."""
    rr = R(890)
    files = []
    for i, xc in enumerate(CHEMINS):
        gens = [(rr.uniform(0, 1), rr.choice([(120, 90, 70), (150, 120, 90), (90, 70, 60), (176, 160, 130), (110, 60, 50)]),
                 rr.random() < 0.15) for _ in range(n)]
        files.append((xc, gens, rr.uniform(0.7, 1.2)))

    def f(img, u):
        if u < t_debut:
            return
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        for (xc, gens, sp) in files:
            for (ph, col, bete) in gens:
                s = (ph + (u - t_debut) * vitesse * sp) % 1.0          # 0 = au bord, 1 = très loin
                z = 1.0 / (1.0 - 0.94 * s)                              # profondeur
                y = VPA[1] + (YA - VPA[1]) / z
                x = VPA[0] + (xc - VPA[0]) / z
                h = max(1, int(round(9 / z ** 0.85)))
                if y < HA + 2:
                    continue
                al = int(255 * min(1.0, (1 - s) * 3))
                X = x + 105
                if bete:
                    d.rectangle([X - h * 0.5, y - h * 0.5, X + h * 0.5, y], fill=(236, 230, 218, al))
                else:
                    w_ = 1 if h >= 5 else 0
                    d.rectangle([X - w_, y - h + 1, X + (1 if h >= 7 else 0), y], fill=col + (al,))
                    if h >= 3:
                        d.rectangle([X - w_ * 0.5, y - h - 1, X + w_ * 0.5, y - h], fill=(66, 46, 36, al))
        _pose(img, lay)
    return f


def anim_vie_couloir(t_debut=0.0, passants=True):
    """Sur mer_couloir : poissons qui nagent dans la muraille, bulles qui montent, lumière qui joue, et, dans les
    fenêtres, des silhouettes qui marchent dans le chemin voisin."""
    rr = R(900)
    poissons = [(rr.uniform(-105, 375), rr.uniform(150, 290), rr.uniform(4, 12) * rr.choice((-1, 1)),
                 rr.choice((1, 1, 2)), rr.uniform(0, 6.28)) for _ in range(16)]
    bulles = [(rr.uniform(-105, 375), rr.uniform(0, 1), rr.uniform(6, 14)) for _ in range(60)]
    voisins = [(rr.uniform(0, 1), rr.choice([(90, 70, 60), (120, 96, 76), (70, 56, 50)])) for _ in range(6)]

    def f(img, u):
        if u < t_debut:
            return
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        for (x0, y0, v, s, ph) in poissons:
            x = (x0 + v * u + 105) % 520 - 20
            y = y0 + 3 * math.sin(u * 0.8 + ph)
            dr = 1 if v > 0 else -1
            col = (12, 40, 70, 150)
            d.ellipse([x - 3 * s, y - 1.2 * s, x + 3 * s, y + 1.2 * s], fill=col)
            d.polygon([(x - 3 * s * dr, y), (x - 6 * s * dr, y - 2 * s), (x - 6 * s * dr, y + 2 * s)], fill=col)
        for (x, ph, sp) in bulles:
            y = YC_SOL - 6 - ((ph * 190 + u * sp) % 190)
            if y > YC_TOP + 6:
                d.point((x + 105 + math.sin(u * 2 + ph * 9), y), fill=(206, 240, 248, 210))
        if passants:
            for (xf, yf, wf, hf) in FENETRES:
                for (ph, col) in voisins:
                    s = (ph + u * 0.05) % 1.0
                    x = xf - wf / 2 - 4 + (wf + 8) * s
                    if abs(x - xf) < wf / 2 - 1:
                        yb = yf + hf - 4
                        d.rectangle([x + 105, yb - 5, x + 106, yb], fill=col + (255,))
                        d.point((x + 105, yb - 6), fill=(60, 44, 36, 255))
        _pose(img, lay)
    return f


def anim_vie_rivage(rive=None, ligne_face=False, t_fin=None):
    """L'écume qui va et vient au bord de l'eau (rivage de côté, ou bord de la plage vu de face)."""
    def f(img, u):
        if t_fin is not None and u > t_fin:
            return
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        if ligne_face:
            off = 2.5 * math.sin(u * 0.9)
            pts = [(x + 105, YS + 3 + off + 1.2 * math.sin(x * 0.2 + u * 1.7)) for x in range(-105, 376, 3)]
            d.line(pts, fill=ECUME + (200,), width=1)
        else:
            pts_r = rive or RIVE
            for k in range(len(pts_r) - 1):
                (xa, ya), (xb, yb) = pts_r[k], pts_r[k + 1]
                for s in np.linspace(0, 1, 30):
                    x, y = xa + (xb - xa) * s, ya + (yb - ya) * s
                    o = 3 + 2.5 * math.sin(u * 1.1 + y * 0.05)
                    d.line([(x + 105 + o, y), (x + 105 + o + 3, y)], fill=ECUME + (210,))
        _pose(img, lay)
    return f


def anim_sous_mer(t_debut=0.0):
    """Sous l'eau : bulles qui montent, rayons qui ondulent, quelques débris (lance, bouclier, roue) qui coulent."""
    rr = R(910)
    bulles = [(rr.uniform(-105, 375), rr.uniform(0, 1), rr.uniform(10, 28), rr.choice((1, 1, 2))) for _ in range(90)]
    debris = [("lance", -40, 0.0), ("bouclier", 120, 0.35), ("roue", 260, 0.15), ("lance", 330, 0.55)]

    def f(img, u):
        lay = _calque(img)
        d = ImageDraw.Draw(lay)
        for (x, ph, sp, s) in bulles:
            y = 400 - ((ph * 300 + (u - t_debut) * sp) % 300)
            X = x + 105 + 1.5 * math.sin(u * 2 + ph * 7)
            if s == 1:
                d.point((X, y), fill=(210, 240, 248, 220))
            else:
                d.ellipse([X - 1.5, y - 1.5, X + 1.5, y + 1.5], outline=(210, 240, 248, 220))
        for k in range(6):
            x0 = -60 + k * 76 + 8 * math.sin(u * 0.4 + k)
            d.polygon([(x0 + 105, 106), (x0 + 117, 106), (x0 + 175, 380), (x0 + 145, 380)], fill=(190, 236, 244, 14))
        for (sorte, x, ph) in debris:
            y = 150 + ((u - t_debut) * 9 + ph * 120) % 240
            al = int(220 * min(1.0, (380 - y) / 60))
            X = x + 105
            col = (14, 34, 54, max(0, al))
            if sorte == "lance":
                d.line([(X - 10, y - 3), (X + 10, y + 3)], fill=col)
                d.polygon([(X + 10, y + 3), (X + 14, y + 4), (X + 10, y + 6)], fill=col)
            elif sorte == "bouclier":
                d.ellipse([X - 5, y - 5, X + 5, y + 5], fill=col)
            else:
                d.ellipse([X - 6, y - 6, X + 6, y + 6], outline=col)
                d.line([(X - 6, y), (X + 6, y)], fill=col)
                d.line([(X, y - 6), (X, y + 6)], fill=col)
        _pose(img, lay)
    return f


# ---------------------------------------------------------------- registre
_DEC = dict(mer_rivage=mer_rivage, mer_rivage_jour=lambda: mer_rivage("jour"),
            mer_rivage_corps=lambda: mer_rivage("jour", corps=True),
            mer_face=mer_face, mer_canyon=mer_canyon, mer_fendue=mer_fendue, mer_couloir=mer_couloir,
            sous_la_mer=sous_la_mer)
egypte.enregistre(_DEC, sol_haut=dict(mer_rivage=(330, 100), mer_face=(330, 100), mer_canyon=(330, 100),
                                      mer_fendue=(330, 100), mer_couloir=(330, 100), sous_la_mer=(330, 100)))
lieux.LUMIERES["sous_la_mer"] = (lieux.NUIT, [])
