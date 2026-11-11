# CRÉATEUR DE PERSONNAGES pixel art — même style que le duo (contour sombre, 3 tons, vue de 3/4 vers la droite).
# Un personnage = une « recette » : taille, peau, coiffure, barbe, haut, bas, chaussures, chapeau, lunettes, accessoires.
#   import cast
#   cast.nouveau("NADIA", genre="f", peau="brune", cheveux="queue", haut="blouse", couleur="blanc", acc=["stethoscope"])
# Ensuite "NADIA" s'utilise partout comme "P" ou "G" : Actor("NADIA", ...), sous-titres, vignette, bulles.
# Dessin : cast.dessine(recette, pose=, face=, talk=, back=, assis=, step=, objet=, cligne=, blush=, sweat=, larmes=)
import numpy as np
from spr import Spr, INK
from px import BAYER
import duo

W, H, FOOT = 46, 98, 93          # toile plus haute que celle du duo (place pour les chapeaux hauts) ; pieds sur la ligne 93
YY, XX = np.mgrid[0:H, 0:W]
EYE, WHITE, TONGUE, BLUSH, SWEAT = duo.EYE, duo.WHITE, duo.TONGUE, duo.BLUSH, duo.SWEAT
TEAR = (120, 192, 250)

# ===================================================================== couleurs
COULEURS = {"rouge": (210, 54, 56), "bordeaux": (128, 30, 44), "rose": (232, 132, 168), "rose_pale": (244, 190, 204),
            "orange": (234, 128, 48), "jaune": (242, 200, 64), "moutarde": (206, 160, 40), "vert": (60, 150, 80),
            "vert_fonce": (34, 96, 66), "kaki": (122, 120, 74), "olive": (104, 110, 56), "turquoise": (40, 170, 170),
            "bleu": (56, 110, 200), "bleu_ciel": (124, 182, 236), "marine": (36, 48, 86), "violet": (120, 72, 170),
            "lilas": (176, 150, 214), "marron": (120, 76, 46), "camel": (184, 134, 76), "beige": (214, 192, 152),
            "creme": (240, 232, 212), "blanc": (242, 242, 244), "gris": (140, 144, 152), "gris_clair": (200, 202, 208),
            "anthracite": (64, 66, 74), "noir": (40, 38, 44), "or": (226, 182, 70), "argent": (190, 196, 206),
            "jean": (62, 96, 166), "jean_clair": (112, 152, 208), "jean_noir": (52, 54, 66)}
CHEVEUX = {"noir": (40, 30, 36), "brun": (80, 52, 40), "chatain": (126, 86, 56), "blond": (222, 184, 104),
           "roux": (194, 94, 46), "gris": (154, 154, 160), "blanc": (230, 230, 234), "bleu": (64, 110, 206),
           "rose": (232, 122, 170), "violet": (124, 82, 184), "vert": (64, 160, 104)}
PEAUX = {"claire": dict(b=(246, 212, 184), s=(214, 168, 142), d=(170, 124, 104), h=(255, 232, 210)),
         "rosee": dict(b=(240, 196, 162), s=(208, 150, 124), d=(160, 108, 90), h=(252, 220, 192)),
         "doree": dict(duo.SKIN_P), "mate": dict(duo.SKIN_S), "halee": dict(duo.SKIN_G),
         "brune": dict(b=(172, 114, 76), s=(136, 86, 58), d=(100, 62, 44), h=(198, 142, 100)),
         "foncee": dict(b=(130, 84, 58), s=(102, 64, 44), d=(76, 46, 34), h=(158, 108, 76)),
         "noire": dict(b=(100, 64, 46), s=(76, 48, 36), d=(56, 34, 28), h=(128, 88, 64))}
METAL = dict(b=(176, 184, 196), s=(124, 132, 148), d=(84, 90, 106), h=(232, 236, 244))


def col(v):
    if v is None:
        return None
    if isinstance(v, str):
        return COULEURS.get(v) or CHEVEUX.get(v) or (255, 0, 255)
    return tuple(int(x) for x in v)


def tons(c):
    """Base, ombre, ombre profonde, reflet (ombres un peu froides, reflets un peu chauds)."""
    c = np.array(col(c), float)
    lum = (0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]) / 255
    ks = 0.70 + 0.16 * lum
    cool = np.array([-6.0, -4.0, 10.0])
    t = lambda v: tuple(int(round(x)) for x in np.clip(v, 0, 255))
    return dict(b=t(c), s=t(c * ks + cool), d=t(c * (ks - 0.24) + cool * 1.6),
                h=t(c + (255 - c) * 0.28 + np.array([6.0, 4.0, -4.0])))


# ===================================================================== gabarits
TAILLES = dict(enfant=(50, 14, 11), ado=(64, 20, 15), adulte=(69, 23, 17), grand=(73, 25, 18))   # hauteur, buste, bras
BUILD = dict(mince=dict(L=13, R=30, sl=14, sr=30, lw=-1, legs=((16, 5), (22, 5))),
             normal=dict(L=12, R=31, sl=13, sr=31, lw=0, legs=((15, 6), (22, 6))),
             fort=dict(L=10, R=33, sl=12, sr=32, lw=1, legs=((14, 7), (22, 7))))
HEADS = dict(
    jeune=dict(cran=(21, 9, 8.3, 7.6), face=(22.5, 13.2, 7.0, 6.5), chin=[(19, 17), (26, 17), (24, 20), (21, 20)],
               neck=(19, 18, 24, 22), ex=20, ey=11, nose=(28, 15), mouth=(23, 17), ear=(15.8, 12.6), body=22, chin_y=20),
    adulte=dict(cran=(21, 9.5, 8.6, 7.4), face=(22.5, 13.5, 7.2, 6.9), chin=[(18, 18), (27, 18), (25, 21), (20, 21)],
                neck=(19, 17, 24, 21), ex=20, ey=10, nose=(28, 13), mouth=(23, 16), ear=(15.6, 12.2), body=21, chin_y=21),
    femme=dict(cran=(21, 9.2, 8.3, 7.5), face=(22.6, 13.2, 6.7, 6.4), chin=[(19, 17), (25, 17), (23, 20), (21, 20)],
               neck=(19, 18, 23, 22), ex=20, ey=11, nose=(28, 14), mouth=(23, 17), ear=(15.8, 12.6), body=22, chin_y=20))
LONGS = ("qamis", "djellaba", "abaya", "toge", "robe_longue")          # jusqu'aux chevilles
KNEE = ("blouse", "redingote", "tunique")                               # jusqu'aux genoux (ou mi-cuisse)
SHORT_SLEEVES = ("tshirt", "polo", "maillot", "tablier", "robe")


class Geo:
    pass


def geo(r, assis=False, dy=0):
    g = _geo(r, assis)
    if dy:                                                # léger rebond du corps pendant la marche (les pieds restent au sol)
        g.y0 += dy; g.top += dy; g.hem += dy; g.ay += dy
    return g


def _geo(r, assis=False):
    ht, tl, L = TAILLES[r["taille"]]
    g = Geo()
    g.L, g.ky = L, L / 15.0
    hk = "femme" if r["genre"] == "f" else ("jeune" if r["taille"] in ("enfant", "ado") else "adulte")
    g.hd = HEADS[hk]
    y0 = FOOT - ht
    top = y0 + g.hd["body"]
    hem = top + tl
    g.foot = FOOT - 4                                 # haut des chaussures
    if assis:                                         # hanches à hauteur de chaise, pieds toujours au sol
        hip = {"enfant": 10, "ado": 12}.get(r["taille"], 13)
        dy = (g.foot - hip) - hem
        y0, top, hem = y0 + dy, top + dy, hem + dy
    g.y0, g.top, g.hem, g.assis = y0, top, hem, assis
    g.ay = top + 3                                    # départ des bras
    b = BUILD[r["corpulence"]]
    g.b = b
    g.sl, g.sr = b["sl"], b["sr"]
    g.lw = 5 + b["lw"] - (1 if r["taille"] == "enfant" else 0)
    g.kh = hem + int((g.foot - hem) * 0.55) if not assis else hem + 3     # bas d'un vêtement aux genoux
    return g


# ===================================================================== poses (bras)
# Un bras = (coude, main, type de main, chute de la main). Points : ("s", dx, dy) = depuis l'épaule (dy proportionnel
# à la longueur du bras) ; ("t", x, dy) = position fixe sur la toile, dy compté depuis le haut de la tête.
N_ = (("s", 1, 8), ("s", 1, 15), "poing", 2)
NN = (("s", -1, 8), ("s", -1, 15), "poing", 2)
POSES = dict(
    neutre=(N_, NN),
    explique=((("s", 4, 8), ("s", 8, 5), "ouverte", 0), NN),
    pointe=((("s", 5, 1), ("s", 9, 1), "index_droite", 0), NN),
    index=((("s", 5, 4), ("s", 7, -4), "index_haut", 0), NN),
    question=((("s", 5, 4), ("s", 5, -6), "index_haut", -1), NN),
    panique=((("s", 6, 6), ("s", 6, -1), "ouverte", -1), (("s", -6, 6), ("s", -6, -1), "ouverte", -1)),
    bras_croises=((("s", 0, 9), ("s", -15, 9), "poing", 0), (("s", 1, 8), ("s", 16, 8), "poing", 0)),
    salut=((("s", 6, 0), ("s", 7, -8), "ouverte", 0), NN),
    salut2=((("s", 6, 0), ("s", 9, -7), "ouverte", 0), NN),
    pouce=((("s", 5, 5), ("s", 8, -1), "pouce", 0), NN),
    hanches=((("s", 6, 5), ("s", 1, 11), "poing", 0), (("s", -6, 5), ("s", -1, 11), "poing", 0)),
    facepalm=(N_, (("s", 4, 5), ("t", 25, 12), "ouverte", 0)),
    menton=((("s", 0, 9), ("s", -12, 9), "poing", 0), (("s", 6, 9), ("t", 24, 21), "poing", 0)),
    haussement=((("s", 5, 6), ("s", 9, 4), "ouverte", 0), (("s", -5, 6), ("s", -9, 4), "ouverte", 0)),
    victoire=((("s", 4, -4), ("s", 5, -12), "poing", 0), (("s", -4, -4), ("s", -5, -12), "poing", 0)),
    tient=(N_, (("s", 1, 8), ("s", 8, 6), "poing", 0)),
    lance=(N_, (("s", -1, 8), ("s", -2, 13), "poing", 0)),                                  # lance / bâton le long du corps
    telephone=(N_, (("s", 2, 8), ("s", 9, 3), "poing", 0)),
    appel=(N_, (("s", -4, 5), ("t", 16, 14), "poing", 0)),
    micro=(N_, (("s", 3, 8), ("t", 27, 22), "poing", 0)),
    clavier=((("s", 3, 8), ("s", 10, 9), "poing", 0), (("s", 3, 8), ("s", 12, 9), "poing", 0)),
    arret=((("s", 6, 2), ("s", 10, -3), "ouverte", 0), NN),
    montre=((("s", 5, 6), ("s", 12, 5), "ouverte", 0), NN),
    doua=((("s", 3, 6), ("s", 8, 0), "ouverte", 0), (("s", 3, 6), ("s", 10, 1), "ouverte", 0)),
    priere=((("s", 0, 8), ("s", -8, 9), "poing", 0), (("s", 1, 8), ("s", 11, 9), "poing", 0)),
    the=(N_, (("s", 1, 9), ("s", 9, 9), "poing", 0)),
    photo=((("s", 4, 0), ("s", 5, -11), "poing", 0), (("s", 11, 1), ("s", 21, -11), "poing", 0)),   # prend une photo
    selfie=(N_, (("s", 14, -3), ("s", 28, -13), "poing", 0)),                                   # bras tendu, selfie
)
POSE_OBJET = dict(the="verre_the", telephone="telephone", appel="telephone", micro="micro", photo="telephone",
                  selfie="telephone")


def _pt(spec, sx, sy, g):
    kind, dx, dy = spec
    if kind == "s":
        return (sx + dx, sy + dy * g.ky)
    return (dx, g.y0 + dy)


# ===================================================================== mains et bras
def hand(sp, x, y, S, kind):
    if kind in ("poing", None):
        return duo._hand(sp, x, y, S)
    if kind == "index_haut":
        return duo._hand(sp, x, y, S, finger="up")
    if kind == "index_droite":
        return duo._hand(sp, x, y, S, finger="right")
    xi, yi = int(round(x)), int(round(y))
    if kind == "ouverte":
        m = sp.m_ell(x, y, 2.4, 2.7)
        sp.paint(m, S["b"]); sp.shade(m, S["s"], dx=-1, dy=-1, depth=1)
        for dx in (-1, 0, 1):
            sp.px(xi + dx, yi - 3, S["b"])
        sp.px(xi + 3, yi - 1, S["b"])
        return m
    if kind == "pouce":
        m = duo._hand(sp, x, y, S)
        sp.paint(sp.m_rect(xi - 1, yi - 5, xi, yi - 2), S["b"], newpart=False)
        sp.px(xi, yi - 4, S["s"])
        return m


def _along(pts, frac):
    """Point situé à une fraction de la longueur d'une ligne brisée."""
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    lens = [((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 for a, b in segs]
    goal = sum(lens) * frac
    for (a, b), L in zip(segs, lens):
        if goal <= L or L == 0:
            f = goal / L if L else 0
            return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
        goal -= L
    return pts[-1]


def arm(sp, g, pts, hk, drop, S, sleeve, short, cuff=None):
    m = sp.m_line(pts, g.lw)
    if short:
        sp.paint(m, S["b"]); sp.shade(m, S["s"], dx=-1, dy=-1, depth=1)
        ms = sp.m_line([pts[0], _along(pts, 0.28)], g.lw + 1)
        sp.paint(ms, sleeve["b"], newpart=False); sp.shade(ms, sleeve["s"], dx=-1, dy=-1, depth=1)
    else:
        sp.paint(m, sleeve["b"]); sp.shade(m, sleeve["s"], dx=-1, dy=-1, depth=1)
        if cuff is not None:
            mc = sp.m_line([_along(pts, 0.86), pts[-1]], g.lw)
            sp.tone(mc, cuff)
    hx, hy = pts[-1]
    hand(sp, hx, hy + drop, S, hk)
    return hx, hy + drop


# ===================================================================== tête
def head_mask(sp, g, back):
    hd, y0 = g.hd, g.y0
    cx, cy, rx, ry = hd["cran"]
    cran = sp.m_ell(cx, y0 + cy, rx, ry)
    if back:
        return cran | sp.m_ell(21, y0 + 13, rx - 1.1, ry - 1.2)
    fx, fy, frx, fry = hd["face"]
    return cran | sp.m_ell(fx, y0 + fy, frx, fry) | sp.m_poly([(x, y0 + y) for x, y in hd["chin"]])


def hair(sp, g, r, head, S, back):
    st, hat = r["cheveux"], r["chapeau"]
    y0, hd = g.y0, g.hd
    if hat in ("hijab", "keffieh", "capuche"):
        return None
    if st in (None, "chauve"):
        if hat is None:
            sp.tone(sp.m_ell(18, y0 + 3, 3.2, 1.4) & head, S["h"])
        return None
    P = tons(r["couleur_cheveux"])
    cx, cy, rx, ry = hd["cran"]
    cy += y0
    if back:
        m = head & (YY < y0 + 17)
        if st == "vieux":
            m = head & (YY > y0 + 7) & (YY < y0 + 16)
        if st == "afro":
            m |= sp.m_ell(21, y0 + 7, 11.5, 10)
        if st in ("boucle", "herisse"):
            m |= sp.m_ell(cx, cy - 1, rx + 1.4, ry + 1.4) & (YY < y0 + 15)
        sp.paint(m, P["b"]); sp.shade(m, P["s"], dx=-1, dy=-1, depth=1)
        sp.tone(m & sp.m_ell(cx - 2, y0 + 3, 5, 2), P["h"])
        if st == "vieux":
            sp.tone(sp.m_ell(20, y0 + 4, 5, 2.4) & head, S["h"])
        return m
    hl = np.where(XX >= 22, y0 + 6.0, np.where(XX >= 17, y0 + 6 + (22 - XX) * 1.2, y0 + 15.0))
    vol = sp.m_ell(cx, cy - 0.6, rx + 0.6, ry + 1.0)
    if st in ("long", "frange"):
        hl = np.where(XX < 18, y0 + 22.0, hl)
    if st == "carre":
        hl = np.where(XX < 18, y0 + 19.0, hl)
    if st == "frange":
        hl = np.where(XX >= 19, y0 + 8.4, hl)
    if st in ("queue", "chignon", "tresses", "rase"):
        vol = head
    m = (head | vol) & (YY < hl)
    if st == "court":
        for x in (23, 25, 27):                                         # mèches sur le front
            m[int(y0 + 6), x] = True
    elif st == "degrade":
        m |= sp.m_ell(22.5, y0 + 2.4, 6.6, 2.6)
    elif st == "meche":
        m |= sp.m_poly([(19, y0 + 1), (30, y0 + 3), (31, y0 + 8), (28, y0 + 7), (25, y0 + 8), (22, y0 + 6)])
    elif st == "herisse":
        for bx, hgt in ((12, 3), (15, 5), (19, 6), (23, 6), (27, 4), (30, 2)):
            m |= sp.m_poly([(bx - 2, y0 + 4), (bx + 3, y0 + 4), (bx - 2, y0 + 3 - hgt)])
    elif st == "boucle":
        m = (head | sp.m_ell(cx, cy - 1.3, rx + 1.8, ry + 2.0)) & (YY < hl + 1)
    elif st == "afro":
        big = sp.m_ell(19.5, y0 + 6, 12.5, 10.5)
        m = big & ((YY < y0 + 7) | ((XX < 18) & (YY < y0 + 16)) | ((XX < 21) & (YY < y0 + 9)))
    elif st == "carre":
        m |= sp.m_ell(cx - 1, cy + 3, rx + 1.4, ry + 1.6) & (XX < 19) & (YY < y0 + 20)
        m |= sp.m_poly([(24, y0 + 4), (30, y0 + 5), (30, y0 + 9), (27, y0 + 7)])
    elif st == "vieux":
        m = head & (XX < 19) & (YY > y0 + 6) & (YY < y0 + 15)
        m |= head & (XX < 25) & (YY > y0 + 4) & (YY < y0 + 7) & (XX > 13)
        m &= ~sp.m_ell(21, y0 + 2, 6, 3.4)
    sp.paint(m, P["b"])
    sp.shade(m, P["s"], dx=-1, dy=-1, depth=1)
    sp.tone(m & sp.m_ell(cx - 3, y0 + 2.6, 4.6, 1.7), P["h"])
    if st in ("boucle", "afro"):                                        # texture bouclée
        sp.tone(m & (((XX * 2 + YY * 3) % (7 if st == "boucle" else 11)) == 0), P["h"])
        sp.tone(m & (((XX * 3 + YY) % 9) == 0), P["s"])
    elif st == "degrade":                                               # côtés plus courts : teinte mêlée à la peau
        side = m & (XX < 19) & (YY > y0 + 8)
        sp.tone(side, tuple(int(P["b"][i] * 0.55 + S["s"][i] * 0.45) for i in range(3)))
    elif st == "rase":
        sp.tone(m, tuple(int(P["b"][i] * 0.6 + S["s"][i] * 0.4) for i in range(3)))
        sp.tone(m & sp.m_ell(cx - 3, y0 + 2.6, 4.6, 1.7), tuple(int(P["h"][i] * 0.6 + S["b"][i] * 0.4) for i in range(3)))
    elif st in ("long", "frange", "carre"):
        for x in (14, 17):
            sp.tone(m & sp.m_rect(x, y0 + 10, x, y0 + 21), P["s"])
    elif st == "vieux":
        sp.tone(sp.m_ell(20, y0 + 3, 4, 1.6) & head & ~m, S["h"])
    if st == "chignon":
        bun = sp.m_ell(14, y0 + 3, 4.6, 4.0)
        sp.paint(bun, P["b"]); sp.shade(bun, P["s"], dx=-1, dy=-1, depth=1)
        sp.tone(bun & sp.m_ell(13, y0 + 1.5, 2, 1), P["h"])
        sp.tone(sp.m_rect(17, y0 + 3, 18, y0 + 5) & bun, col(r.get("couleur_acc_cheveux") or "rouge"))
    return m


def beard(sp, g, r, head):
    b = r["barbe"]
    if not b:
        return
    P = tons(r["couleur_barbe"] or r["couleur_cheveux"])
    y0, hd = g.y0, g.hd
    my = y0 + hd["mouth"][1]
    bt = my - 2
    chin_y = y0 + hd["chin_y"]
    full = head & (sp.m_rect(0, bt, W, H) | sp.m_rect(15, bt - 4, 19, H)) & sp.m_rect(15, 0, W, H)
    full &= ~sp.m_rect(20, bt - 4, 30, bt)
    if b in ("courte", "longue"):
        m = full
        if b == "longue":
            m = m | sp.m_poly([(17, chin_y - 2), (28, chin_y - 2), (26, chin_y + 5), (22, chin_y + 8), (18, chin_y + 4)])
        sp.paint(m, P["b"], newpart=False)
        sp.shade(m, P["s"], dx=-1, dy=-1, depth=1)
        sp.tone(m & sp.m_rect(16, bt + 1, 17, bt + 3), P["h"])
        if b == "longue":
            for x in (20, 23):
                sp.tone(m & sp.m_rect(x, chin_y, x, chin_y + 5), P["s"])
        sp.tone(sp.m_rect(22, my - 1, 27, my - 1) & head, P["s"])        # moustache
    elif b == "postiche":                                             # barbe d'apparat, droite et tressée
        m = sp.m_rect(23, chin_y, 24, chin_y + 3)
        Pp = tons(r["couleur_barbe"] if r["couleur_barbe"] else (92, 66, 48))
        sp.paint(m, Pp["b"], newpart=False)
        sp.tone(m & sp.m_rect(0, chin_y + 1, W, chin_y + 1), Pp["h"])
        sp.tone(m & sp.m_rect(0, chin_y + 3, W, chin_y + 3), Pp["s"])
    elif b == "bouc":
        m = head & sp.m_rect(21, my + 1, 27, H)
        sp.paint(m, P["b"], newpart=False); sp.shade(m, P["s"], dx=-1, dy=-1, depth=1)
        sp.paint(sp.m_rect(22, my - 1, 27, my - 1) & head, P["b"], newpart=False)
    elif b == "moustache":
        sp.paint(sp.m_rect(22, my - 1, 27, my - 1) & head, P["b"], newpart=False)
        sp.pxs([(22, my), (27, my)], P["s"])
    elif b == "3j":                                                   # barbe de 3 jours : ombre unie (pas de damier)
        S = r["_peau"]
        mix = tuple(int(S["s"][i] * 0.5 + P["b"][i] * 0.5) for i in range(3))
        sp.tone(full & ~sp.m_rect(0, 0, W, bt - 1), mix)


# ===================================================================== visage
OPEN = ("neutre", "parle", "content", "gene", "malin_ouvert")


def one_eye(sp, x0, ey, kind, far):
    xa = x0 - (0 if far else 1)
    if kind in OPEN:
        sp.pxs([(x0, ey), (x0 + 1, ey)] + ([] if far else [(x0 - 1, ey)]), EYE)
        if not far:
            sp.px(x0 - 1, ey + 1, WHITE); sp.px(x0 - 1, ey + 2, WHITE)
        sp.pxs([(x0, ey + 1), (x0 + 1, ey + 1), (x0, ey + 2), (x0 + 1, ey + 2)], EYE)
        sp.px(x0 + 1, ey + 1, (90, 90, 120))
    elif kind == "choc":
        sp.pxs([(xa, ey - 1), (x0, ey - 1), (x0 + 1, ey - 1)], EYE)
        for yy in (ey, ey + 1, ey + 2):
            sp.pxs([(xa, yy), (x0 + 1, yy)], EYE)
            sp.px(x0, yy, WHITE)
        sp.px(x0, ey + 1, EYE)
        sp.pxs([(xa, ey + 3), (x0, ey + 3), (x0 + 1, ey + 3)], EYE)
    elif kind in ("ferme", "rire"):
        sp.pxs([(xa, ey + 2), (x0, ey + 1), (x0 + 1, ey + 2)], EYE)
    elif kind in ("malin", "blase"):
        sp.pxs([(xa, ey + 1), (x0, ey + 1), (x0 + 1, ey + 1)], EYE)
        sp.pxs([(x0, ey + 2), (x0 + 1, ey + 2)], EYE)
        if not far:
            sp.px(x0 - 1, ey + 2, WHITE)
    elif kind == "pleure":                                                # yeux fermés tristes (u)
        sp.pxs([(xa, ey + 1), (x0, ey + 2), (x0 + 1, ey + 1)], EYE)
    elif kind == "bas":                                                   # regarde vers le bas (téléphone)
        sp.pxs([(xa, ey + 1), (x0, ey + 1), (x0 + 1, ey + 1)], EYE)
        sp.pxs([(x0, ey + 2), (x0 + 1, ey + 2)], EYE)
        sp.px(x0 + 1, ey + 2, (90, 90, 120))
    elif kind == "coeur":
        c = (226, 40, 74)
        sp.pxs([(xa, ey), (x0 + 1, ey), (xa, ey + 1), (x0, ey + 1), (x0 + 1, ey + 1), (x0, ey + 2)], c)
        if not far:
            sp.px(x0, ey, c)
    elif kind == "etoile":
        c = (250, 214, 80)
        sp.pxs([(x0, ey), (xa, ey + 1), (x0, ey + 1), (x0 + 1, ey + 1), (x0, ey + 2)], c)


EYEMAP = dict(parle="neutre", enerve="neutre", cri="neutre", triste="neutre", peur="choc", surpris="choc",
              suspect="malin", dodo="ferme", fier="rire", degoute="malin", calme="ferme", gene="neutre")
BROWMAP = dict(enerve="enerve", cri="enerve", triste="triste", pleure="triste", peur="triste", suspect="suspect",
               choc="choc", surpris="choc", gene="gene", malin="malin", clin="malin")
MOUTHMAP = dict(neutre="neutre", choc="choc", content="content", rire="rire", gene="gene", malin="malin", ferme="neutre",
                blase="blase", enerve="colere", cri="cri", triste="triste", pleure="pleure", peur="o", suspect="malin",
                dodo="o", fier="content", degoute="degoute", clin="malin", coeur="content", bas="neutre", surpris="o",
                calme="content", etoile="rire")
BLINKABLE = ("neutre", "content", "gene", "malin", "blase", "enerve", "triste", "suspect", "bas", "coeur", "etoile",
             "surpris", "peur", "choc", "degoute")


def eyes(sp, ex, ey, kind, cligne=False, far_dx=5):
    if kind == "clin":
        one_eye(sp, ex, ey, "ferme", False); one_eye(sp, ex + far_dx, ey, "neutre", True)
        return
    k = EYEMAP.get(kind, kind)
    if cligne and kind in BLINKABLE:
        k = "ferme"
    for i, x0 in enumerate((ex, ex + far_dx)):
        one_eye(sp, x0, ey, k, i == 1)


def brows(sp, ex, ey, kind, c, thick=1, far_dx=5):
    k = BROWMAP.get(kind, "neutre")
    y = ey - 2 - (1 if k == "choc" else 0)
    for i, x0 in enumerate((ex, ex + far_dx)):
        far = i == 1
        xa = x0 - (0 if far else 1)
        pts = [(xa, y), (x0, y), (x0 + 1, y)]
        if k == "gene":
            pts = [(xa, y + (0 if far else 1)), (x0, y), (x0 + 1, y + (1 if far else 0))]
        elif k == "malin":
            pts = [(xa, y), (x0, y), (x0 + 1, y + (1 if not far else 0))]
        elif k == "enerve":
            pts = [(xa, y - 1), (x0, y), (x0 + 1, y + 1)] if not far else [(x0, y + 1), (x0 + 1, y), (x0 + 2, y - 1)]
        elif k == "triste":
            pts = [(xa, y + 1), (x0, y), (x0 + 1, y - 1)] if not far else [(x0, y - 1), (x0 + 1, y), (x0 + 2, y + 1)]
        elif k == "suspect":
            pts = [(xa, y + 1), (x0, y + 1), (x0 + 1, y + 1)] if not far else [(x0, y - 1), (x0 + 1, y - 2), (x0 + 2, y - 1)]
        sp.pxs(pts, c)
        if thick > 1:
            sp.pxs([(x, yy - 1) for (x, yy) in pts[:2]], c)


def mouth(sp, mx, my, kind, mc):
    if kind == "neutre":
        sp.pxs([(mx, my), (mx + 1, my)], mc)
    elif kind == "parle":
        sp.pxs([(mx + i, my + j) for i in range(3) for j in range(2)], mc); sp.px(mx + 1, my + 1, TONGUE)
    elif kind == "choc":
        sp.pxs([(mx + i, my + j) for i in range(2) for j in range(3)], mc); sp.pxs([(mx, my + 2), (mx + 1, my + 2)], TONGUE)
    elif kind in ("content", "rire"):
        sp.pxs([(mx - 1, my), (mx, my + 1), (mx + 1, my + 1), (mx + 2, my + 1), (mx + 3, my)], mc)
        if kind == "rire":
            sp.pxs([(mx, my), (mx + 1, my), (mx + 2, my)], mc); sp.px(mx + 1, my + 1, TONGUE)
    elif kind == "malin":
        sp.pxs([(mx, my), (mx + 1, my), (mx + 2, my - 1)], mc)
    elif kind == "gene":
        sp.pxs([(mx, my), (mx + 1, my + 1), (mx + 2, my)], mc)
    elif kind == "blase":
        sp.pxs([(mx, my), (mx + 1, my), (mx + 2, my)], mc)
    elif kind == "colere":
        sp.pxs([(mx - 1, my + 1), (mx, my), (mx + 1, my), (mx + 2, my), (mx + 3, my + 1)], mc)
    elif kind == "triste":
        sp.pxs([(mx, my + 1), (mx + 1, my), (mx + 2, my + 1)], mc)
    elif kind == "cri":
        sp.pxs([(mx + i, my + j) for i in range(-1, 3) for j in range(3)], mc)
        sp.pxs([(mx, my), (mx + 1, my)], WHITE); sp.pxs([(mx, my + 2), (mx + 1, my + 2)], TONGUE)
    elif kind == "pleure":
        sp.pxs([(mx - 1, my + 1), (mx, my), (mx + 1, my), (mx + 2, my), (mx + 3, my + 1)], mc)
        sp.pxs([(mx, my + 1), (mx + 1, my + 1), (mx + 2, my + 1)], mc); sp.px(mx + 1, my + 1, TONGUE)
    elif kind == "o":
        sp.pxs([(mx, my), (mx + 1, my), (mx, my + 1), (mx + 1, my + 1)], mc)
    elif kind == "degoute":
        sp.pxs([(mx - 1, my), (mx, my + 1), (mx + 1, my), (mx + 2, my + 1), (mx + 3, my)], mc)
    # formes de bouche selon le son prononcé (A, O, E, M/B/P, F/V)
    elif kind == "A":
        sp.pxs([(mx + i, my + j) for i in range(3) for j in range(3)], mc); sp.pxs([(mx + 1, my + 2), (mx, my + 2)], TONGUE)
    elif kind == "O":
        sp.pxs([(mx + 1, my), (mx, my + 1), (mx + 2, my + 1), (mx + 1, my + 2), (mx + 1, my + 1)], mc)
    elif kind == "E":
        sp.pxs([(mx - 1, my), (mx, my), (mx + 1, my), (mx + 2, my), (mx, my + 1), (mx + 1, my + 1)], mc)
        sp.pxs([(mx, my), (mx + 1, my)], WHITE)
    elif kind == "M":
        sp.pxs([(mx, my), (mx + 1, my), (mx + 2, my)], mc)
    elif kind == "F":
        sp.pxs([(mx, my + 1), (mx + 1, my + 1), (mx + 2, my + 1)], mc); sp.pxs([(mx, my), (mx + 1, my)], WHITE)


def glasses(sp, ex, ey, kind, c):
    if kind == "soleil":
        for x0, x1 in ((ex - 2, ex + 2), (ex + 4, ex + 7)):
            sp.paint(sp.m_rect(x0, ey - 1, x1, ey + 2), (30, 28, 40), newpart=False)
            sp.px(x0 + 1, ey, (130, 140, 176))
        sp.px(ex + 3, ey, (30, 28, 40))
    else:
        lens = (222, 238, 248)
        for x0, x1 in ((ex - 2, ex + 2), (ex + 4, ex + 7)):
            for x in range(x0 + 1, x1):                       # le haut de l'œil devient du verre (sinon : un bloc noir)
                if tuple(sp.a[ey, x, :3]) == EYE:
                    sp.px(x, ey, lens)
            sp.pxs([(x, ey - 1) for x in range(x0, x1 + 1)] + [(x, ey + 3) for x in range(x0 + 1, x1)] +
                   [(x0, ey), (x0, ey + 1), (x0, ey + 2), (x1, ey), (x1, ey + 1), (x1, ey + 2)], c)
        sp.px(ex + 3, ey, c)
    for x in range(16, ex - 2):
        sp.px(x, ey, c)


def _lum(c):
    return (0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]) / 255


def draw_face(sp, g, r, kind, talk, cligne, blush, sweat, larmes, S, bouche=None, accent=None):
    y0, hd = g.y0, g.hd
    ex, ey = hd["ex"], y0 + hd["ey"]
    fem = r["genre"] == "f"
    hc = r["couleur_cheveux"] if r["cheveux"] not in (None, "chauve") else (r["couleur_barbe"] or (70, 54, 58))
    hairc = tons(hc)["s"] if _lum(hc) > 0.45 else hc
    eyes(sp, ex, ey, kind, cligne)
    thick = 2 if (r["genre"] == "h" and r["taille"] in ("adulte", "grand")) else 1
    bk = "choc" if accent == "!" else ("suspect" if accent == "?" else kind)       # sourcils sur les mots forts
    brows(sp, ex, ey - (1 if r["lunettes"] == "lunettes" else 0), bk, hairc, thick)
    if fem and EYEMAP.get(kind, kind) in OPEN and not cligne:
        sp.pxs([(ex - 2, ey), (ex + 7, ey - 1)], EYE)
    nx, ny = hd["nose"]
    sp.px(nx, y0 + ny, S["s"])
    lum = (0.3 * S["b"][0] + 0.59 * S["b"][1] + 0.11 * S["b"][2]) / 255
    mc = (64, 22, 30) if lum < 0.5 else ((170, 64, 86) if fem else duo.MOUTH)
    mx, my = hd["mouth"]
    mk = MOUTHMAP.get(kind, "neutre")
    if talk:
        mk = "cri" if kind in ("enerve", "cri") else ("pleure" if kind == "pleure" else (bouche or "parle"))
        if kind in ("enerve", "cri") and bouche in ("M", "F"):
            mk = bouche
    if r["barbe"] in ("courte", "longue"):
        sp.tone(sp.m_rect(mx - 1, y0 + my, mx + 3, y0 + my + 1) & head_mask(sp, g, False), S["s"])
    mouth(sp, mx, y0 + my, mk, mc)
    if r["age"] == "vieux":
        sk = (sp.a[..., 0] == S["b"][0]) & (sp.a[..., 1] == S["b"][1]) & (sp.a[..., 2] == S["b"][2])
        for (x, y) in ((ex + 1, ey - 4), (ex + 2, ey - 4), (ex + 3, ey - 4), (ex - 2, ey + 1), (ex - 2, ey + 3),
                       (mx - 2, y0 + my - 2), (mx - 2, y0 + my - 1)):
            if 0 <= y < H and sk[y, x]:
                sp.px(x, y, S["s"])
    if blush or (fem and kind not in ("enerve", "cri", "peur")):
        sp.pxs([(ex - 1, ey + 4), (ex, ey + 4), (ex + 7, ey + 4)], BLUSH)
    if sweat:
        sp.pxs([(13, y0 + 9), (13, y0 + 10), (12, y0 + 11), (13, y0 + 11), (14, y0 + 11), (13, y0 + 12)], SWEAT)
    if larmes or kind == "pleure":
        for x0, n in ((ex - 1, 5), (ex + 5, 4)):
            for k in range(n):
                sp.px(x0, ey + 3 + k, TEAR)
    if r["lunettes"]:
        glasses(sp, ex, ey, r["lunettes"], col(r["couleur_lunettes"]))


# ===================================================================== chapeaux / coiffes
def hat(sp, g, r, S, back):
    k = r["chapeau"]
    if not k:
        return
    y0 = g.y0
    P = tons(r["couleur_chapeau"])
    if k in ("casquette", "casquette_arriere"):
        crown = sp.m_ell(21, y0 + 6.2, 8.9, 6.0) & sp.m_rect(0, 0, W, y0 + 8)
        sp.paint(crown, P["b"]); sp.tone(crown & sp.m_ell(17.5, y0 + 3.5, 4.5, 2.6), P["h"])
        sp.shade(crown, P["s"], dx=-1, dy=0, depth=2)
        sp.tone(sp.m_rect(12, y0 + 8, 30, y0 + 8) & head_mask(sp, g, back), P["s"])
        if not back:
            if k == "casquette":
                sp.paint(sp.m_rect(26, y0 + 7, 33, y0 + 8) | sp.m_rect(25, y0 + 8, 34, y0 + 8), P["d"])
                sp.tone(sp.m_rect(27, y0 + 7, 32, y0 + 7), P["b"])
                sp.tone(sp.m_rect(21, y0 + 9, 29, y0 + 9) & head_mask(sp, g, False), S["s"])
            else:
                sp.paint(sp.m_rect(8, y0 + 7, 14, y0 + 8), P["d"])
                sp.tone(sp.m_rect(9, y0 + 7, 13, y0 + 7), P["b"])
            sp.px(21, y0 + 1, P["s"])
    elif k == "bonnet":
        m = sp.m_ell(21, y0 + 6.5, 9.3, 7.2) & sp.m_rect(0, 0, W, y0 + 8)
        sp.paint(m, P["b"]); sp.shade(m, P["s"], dx=-1, dy=0, depth=2)
        sp.tone(m & sp.m_ell(17, y0 + 2.5, 4, 2), P["h"])
        band = m & sp.m_rect(0, y0 + 5, W, y0 + 8)
        sp.tone(band, P["s"]); sp.tone(band & ((XX % 2) == 0), P["b"])
        if r.get("pompon", True):
            pp = sp.m_ell(20, y0 - 1.5, 2.6, 2.4)
            sp.paint(pp, P["h"]); sp.shade(pp, P["b"], dx=-1, dy=-1, depth=1)
    elif k == "chapeau":
        crown = sp.m_poly([(13, y0 + 5), (29, y0 + 5), (28, y0 - 3), (23, y0 - 4), (21, y0 - 2), (19, y0 - 4), (14, y0 - 3)])
        sp.paint(crown, P["b"]); sp.shade(crown, P["s"], dx=-1, dy=0, depth=2)
        sp.tone(crown & sp.m_rect(0, y0 + 2, W, y0 + 3), col(r.get("couleur_ruban") or "noir"))
        brim = sp.m_ell(21.5, y0 + 5.2, 13.2, 2.1)
        sp.paint(brim, P["b"]); sp.shade(brim, P["s"], dx=0, dy=-1, depth=1)
        sp.tone(brim & sp.m_rect(0, 0, W, y0 + 4), P["h"])
    elif k == "haut_de_forme":
        crown = sp.m_poly([(14, y0 + 5), (28, y0 + 5), (29, y0 - 10), (13, y0 - 10)])
        sp.paint(crown, P["b"]); sp.shade(crown, P["s"], dx=-1, dy=0, depth=2)
        sp.tone(crown & sp.m_rect(14, y0 - 9, 15, y0 + 4), P["h"])
        sp.tone(crown & sp.m_rect(0, y0 + 1, W, y0 + 3), col(r.get("couleur_ruban") or "bordeaux"))
        brim = sp.m_ell(21, y0 + 5.4, 11.8, 1.9)
        sp.paint(brim, P["b"]); sp.shade(brim, P["s"], dx=0, dy=-1, depth=1)
    elif k == "couronne":
        G_ = tons("or")
        m = sp.m_rect(13, y0 + 1, 29, y0 + 4)
        for bx in (13, 17, 21, 25, 29):
            m |= sp.m_poly([(bx - 2, y0 + 1), (bx + 2, y0 + 1), (bx, y0 - 4)])
        m &= sp.m_rect(12, 0, 30, H)
        sp.paint(m, G_["b"]); sp.shade(m, G_["s"], dx=-1, dy=-1, depth=1)
        sp.tone(m & sp.m_rect(13, y0 + 1, 29, y0 + 1), G_["h"])
        for bx, c in ((17, (200, 30, 50)), (21, (40, 110, 220)), (25, (200, 30, 50))):
            sp.px(bx, y0 + 2, c); sp.px(bx, y0 + 3, c)
    elif k in ("nemes", "khat"):
        # nemes = coiffe royale rayée or / bleu (Pharaon) ; khat = coiffe de lin unie, serrée derrière (notables, soldats)
        nem = k == "nemes"
        raye = nem or bool(r.get("rayures"))
        A_ = tons(r.get("couleur_rayures") or ("or" if nem else "blanc"))
        B_ = tons((40, 84, 170) if nem else r["couleur_chapeau"])
        if nem:
            cap = sp.m_poly([(11, y0 + 9), (12, y0 + 3), (16, y0 - 1), (25, y0 - 1), (29, y0 + 2), (31, y0 + 6), (31, y0 + 8)])
            wing = sp.m_poly([(10, y0 + 6), (17, y0 + 7), (17, y0 + 15), (16, y0 + 19), (18, g.top + 1), (18, g.top + 9),
                              (11, g.top + 9), (9, g.top + 2), (9, y0 + 12)])
            if back:
                wing = sp.m_poly([(9, y0 + 6), (33, y0 + 6), (34, g.top + 6), (8, g.top + 6)])
        else:
            cap = sp.m_poly([(12, y0 + 9), (13, y0 + 3), (17, y0 + 0), (25, y0 + 0), (29, y0 + 3), (30, y0 + 7), (30, y0 + 9)])
            wing = sp.m_poly([(11, y0 + 7), (17, y0 + 8), (17, y0 + 16), (14, y0 + 20), (10, y0 + 18), (10, y0 + 11)])
            if back:
                wing = sp.m_poly([(10, y0 + 7), (32, y0 + 7), (31, y0 + 19), (11, y0 + 19)])
        cloth = cap | wing
        sp.paint(cloth, B_["b"])
        if raye:                                                           # rayures horizontales
            sp.tone(cloth & ((((YY - y0) // 2) % 2) == 0), A_["b"])
        edge = cloth & ~(np.roll(cloth, -1, 1) & np.roll(cloth, -1, 0))
        sp.tone(edge & ((((YY - y0) // 2) % 2) == 0) if raye else edge, A_["s"] if raye else B_["s"])
        if raye:
            sp.tone(edge & ((((YY - y0) // 2) % 2) == 1), B_["s"])
        if not nem:                                                        # plis du tissu qui tombe derrière l'oreille
            for fx in (12, 15):
                sp.tone(wing & sp.m_rect(fx, y0 + 10, fx, y0 + 19), B_["s"] if not raye else A_["s"])
        sp.tone(cloth & sp.m_ell(17, y0 + 1, 3.5, 1.4), A_["h"] if raye else B_["h"])
        if not back:
            band = sp.m_rect(12, y0 + 7, 31, y0 + 8) & (sp.m_ell(21, y0 + 9.5, 10.2, 8.2))
            Gb = tons("or") if nem else tons(r.get("couleur_bandeau") or B_["s"])
            sp.paint(band, Gb["b"], newpart=False)
            sp.tone(band & sp.m_rect(0, y0 + 8, W, y0 + 8), Gb["s"] if nem else B_["d"])
            if nem:                                                        # cobra dressé sur le front (uræus)
                sp.pxs([(30, y0 + 6), (30, y0 + 5), (31, y0 + 4), (30, y0 + 3), (31, y0 + 2)], col("or"))
                sp.px(31, y0 + 3, (200, 40, 50))
    elif k == "kufi":
        m = sp.m_ell(21, y0 + 5.8, 8.8, 4.6) & sp.m_rect(0, 0, W, y0 + 7)
        sp.paint(m, P["b"]); sp.shade(m, P["s"], dx=-1, dy=0, depth=2)
        for x in range(14, 30, 2):
            sp.px(x, y0 + 5, P["s"])
        sp.tone(sp.m_rect(12, y0 + 7, 30, y0 + 7) & m, P["s"])
    elif k == "turban":
        m = sp.m_ell(21, y0 + 5, 10.2, 7.2) & sp.m_rect(0, 0, W, y0 + 8)
        sp.paint(m, P["b"]); sp.shade(m, P["s"], dx=-1, dy=-1, depth=2)
        for i in range(4):
            sp.tone(m & (np.abs((YY - (y0 + 1 + i * 2.2)) - (XX - 21) * 0.45) < 0.6), P["s"])
        sp.tone(m & sp.m_ell(17, y0 + 1, 3, 1.4), P["h"])
        if r.get("bijou", True):
            sp.px(26, y0 + 5, (200, 30, 50)); sp.px(26, y0 + 4, col("or"))
    elif k == "keffieh":
        cloth = sp.m_ell(21, y0 + 8, 10.2, 9.4) & sp.m_rect(0, 0, W, y0 + 9)
        cloth |= sp.m_poly([(11, y0 + 6), (19, y0 + 8), (19, g.top + 3), (13, g.top + 6), (8, g.top + 4)])
        sp.paint(cloth, (240, 238, 232)); sp.shade(cloth, (196, 196, 204), dx=-1, dy=-1, depth=2)
        sp.tone(cloth & ((((XX + YY) % 3) == 0) | (((XX - YY) % 3) == 0)) & ~sp.m_rect(0, 0, W, y0 + 1), P["b"])
        agal = sp.m_ell(21, y0 + 6.2, 9.6, 4.6) & ~sp.m_ell(21, y0 + 6.2, 9.6, 2.8) & sp.m_rect(0, y0 + 4, W, y0 + 9)
        sp.paint(agal & cloth, (34, 30, 36), newpart=False)
    elif k == "hijab":
        drape = sp.m_ell(21.5, g.top - 1, 11, 6) | sp.m_ell(21, y0 + 10, 9.6, 9.6)
        sp.paint(drape, P["b"]); sp.shade(drape, P["s"], dx=-1, dy=-1, depth=2)
        sp.tone(sp.m_ell(17, y0 + 5, 3, 2) & drape, P["h"])
        fm = sp.m_ell(23, y0 + 12.5, 5.8, 6.4)
        sp.paint(fm, S["b"]); sp.shade(fm, S["s"], dx=-1, dy=-1, depth=1)
        sp.tone(sp.m_rect(16, y0 + 4, 30, y0 + 6) & fm, P["s"])
    elif k == "capuche":
        hood = sp.m_ell(21, y0 + 9, 10.4, 10.2) | sp.m_ell(21.5, g.top - 1, 11, 5)
        sp.paint(hood, P["b"]); sp.shade(hood, P["s"], dx=-1, dy=-1, depth=2)
        sp.tone(hood & sp.m_ell(16, y0 + 3, 3.5, 2.5), P["h"])
        fm = sp.m_ell(23.2, y0 + 12.8, 5.9, 6.6)
        sp.paint(fm, S["b"]); sp.shade(fm, S["s"], dx=-1, dy=-1, depth=1)
        sp.tone(sp.m_rect(16, y0 + 5, 30, y0 + 8) & fm, S["d"])          # ombre de la capuche
        sp.tone(sp.m_ell(23.2, y0 + 12.8, 7, 7.6) & ~fm & hood, P["d"])
    elif k == "casque_chantier":
        Y_ = tons(r["couleur_chapeau"] if r["couleur_chapeau"] != (40, 44, 60) else "jaune")
        m = sp.m_ell(21, y0 + 5.5, 9.4, 6.6) & sp.m_rect(0, 0, W, y0 + 7)
        m |= sp.m_rect(10, y0 + 7, 32, y0 + 8)
        sp.paint(m, Y_["b"]); sp.shade(m, Y_["s"], dx=-1, dy=-1, depth=1)
        sp.tone(m & sp.m_rect(20, y0 - 1, 22, y0 + 6), Y_["h"])
    elif k == "toque":
        m = sp.m_ell(21, y0 - 3.5, 9.4, 7.4) | sp.m_rect(13, y0 - 2, 29, y0 + 7)
        m &= sp.m_rect(0, 0, W, y0 + 7)
        sp.paint(m, (248, 248, 250)); sp.shade(m, (206, 208, 218), dx=-1, dy=-1, depth=2)
        for x in (17, 21, 25):
            sp.tone(m & sp.m_rect(x, y0 - 7, x, y0 + 1), (214, 216, 226))
        sp.tone(m & sp.m_rect(0, y0 + 3, W, y0 + 3), (214, 216, 226))
    elif k == "casquette_police":
        Pp = tons(r["couleur_chapeau"] if r["couleur_chapeau"] != (40, 44, 60) else "marine")
        top_ = sp.m_ell(20.5, y0 + 2.2, 10.6, 3.6)
        band = sp.m_rect(13, y0 + 3, 29, y0 + 7)
        sp.paint(band, Pp["b"]); sp.shade(band, Pp["s"], dx=-1, dy=0, depth=1)
        sp.paint(top_, Pp["b"]); sp.shade(top_, Pp["s"], dx=-1, dy=-1, depth=1); sp.tone(top_ & sp.m_ell(17, y0 + 1, 4, 1.4), Pp["h"])
        sp.tone(sp.m_rect(13, y0 + 6, 29, y0 + 7) & band, (30, 30, 36))
        if not back:
            sp.paint(sp.m_rect(25, y0 + 7, 33, y0 + 8), (26, 24, 30))
            sp.pxs([(22, y0 + 3), (23, y0 + 3), (22, y0 + 4), (23, y0 + 4)], col("or"))
    elif k == "bandeau":
        m = sp.m_rect(12, y0 + 5, 30, y0 + 7) & head_mask(sp, g, back)
        sp.paint(m, P["b"], newpart=False); sp.tone(m & sp.m_rect(0, y0 + 7, W, y0 + 7), P["s"])
    elif k == "casque_audio":
        C = P if r["couleur_chapeau"] != (40, 44, 60) else tons((226, 60, 80))
        arc = sp.m_ell(19, y0 + 10, 10.6, 11.2) & ~sp.m_ell(19, y0 + 10, 8.6, 9.4) & sp.m_rect(0, 0, W, y0 + 11) & sp.m_rect(9, 0, 31, H)
        sp.paint(arc, (52, 52, 62)); sp.tone(arc & sp.m_rect(0, 0, W, y0 - 1), (110, 110, 126))
        cup = sp.m_ell(15.4, y0 + 12.6, 3.3, 4.0)
        sp.paint(cup, C["b"]); sp.shade(cup, C["s"], dx=-1, dy=-1, depth=1)
        sp.tone(cup & sp.m_ell(14.6, y0 + 11.4, 1.2, 1.4), C["h"])
        sp.tone(cup & sp.m_rect(18, 0, W, H), (40, 40, 48))
    elif k == "laurier":
        Gr = tons(r["couleur_chapeau"] if r["couleur_chapeau"] != (40, 44, 60) else "vert")
        for i, x in enumerate(range(12, 31, 3)):
            yy_ = y0 + 6 - (1 if 16 < x < 27 else 0)
            lf = sp.m_ell(x, yy_, 2.0, 1.2)
            sp.paint(lf, Gr["b"], newpart=False); sp.tone(lf & sp.m_rect(0, 0, W, yy_ - 1), Gr["h"])
    elif k == "beret":
        m = sp.m_poly([(10, y0 + 4), (14, y0 + 0), (24, y0 - 1), (31, y0 + 2), (29, y0 + 5), (12, y0 + 6)])
        sp.paint(m, P["b"]); sp.shade(m, P["s"], dx=-1, dy=-1, depth=1)
        sp.tone(m & sp.m_ell(18, y0 + 1, 5, 1.4), P["h"])
        sp.px(20, y0 - 2, P["d"])
    elif k == "bob":
        m = sp.m_ell(21, y0 + 5, 9.2, 6.2) & sp.m_rect(0, 0, W, y0 + 6)
        m |= sp.m_poly([(9, y0 + 9), (34, y0 + 9), (31, y0 + 6), (12, y0 + 6)])
        sp.paint(m, P["b"]); sp.shade(m, P["s"], dx=-1, dy=-1, depth=1)
        sp.tone(m & sp.m_rect(0, y0 + 6, W, y0 + 6), P["s"])


def covers_ear(r):
    return r["cheveux"] in ("long", "frange", "carre", "afro") or r["chapeau"] in ("hijab", "keffieh", "capuche", "casque_audio", "nemes", "khat")


# ===================================================================== bas du corps
def shoe(sp, x0, yy, kind, c, S):
    if kind == "baskets":
        m = sp.paint(sp.m_rect(x0, yy, x0 + 8, yy + 3) & ~sp.m_rect(x0, yy, x0, yy), (244, 244, 248))
        sp.tone(sp.m_rect(x0, yy + 3, x0 + 8, yy + 3), (150, 150, 164))
        sp.tone(sp.m_rect(x0 + 2, yy + 1, x0 + 4, yy + 1), c)
    elif kind == "ville":
        m = sp.paint(sp.m_rect(x0, yy + 1, x0 + 8, yy + 3) | sp.m_rect(x0, yy, x0 + 5, yy), c)
        sp.tone(sp.m_rect(x0, yy + 3, x0 + 8, yy + 3), tuple(int(v * 0.6) for v in c))
        sp.px(x0 + 6, yy + 1, tuple(min(255, v + 70) for v in c))
    elif kind == "bottes":
        m = sp.paint(sp.m_rect(x0, yy - 4, x0 + 6, yy + 3) | sp.m_rect(x0, yy + 1, x0 + 8, yy + 3), c)
        sp.tone(sp.m_rect(x0, yy - 4, x0 + 6, yy - 4), tuple(min(255, v + 40) for v in c))
        sp.tone(sp.m_rect(x0, yy + 3, x0 + 8, yy + 3), tuple(int(v * 0.55) for v in c))
        sp.tone(sp.m_rect(x0 + 1, yy - 3, x0 + 1, yy + 1), tuple(min(255, v + 30) for v in c))
    elif kind == "sandales":
        sp.paint(sp.m_rect(x0 + 2, yy, x0 + 6, yy), S["b"])
        m = sp.paint(sp.m_rect(x0, yy + 1, x0 + 7, yy + 3), (132, 82, 46))
        sp.tone(sp.m_rect(x0, yy + 3, x0 + 7, yy + 3), (92, 56, 32))
        sp.tone(sp.m_rect(x0 + 2, yy + 1, x0 + 5, yy + 1), S["b"])
    elif kind == "talons":
        sp.paint(sp.m_rect(x0 + 2, yy, x0 + 6, yy), S["b"])
        m = sp.paint(sp.m_rect(x0 + 1, yy + 1, x0 + 7, yy + 2), c)
        sp.px(x0 + 1, yy + 3, c); sp.px(x0 + 7, yy + 3, c); sp.px(x0 + 6, yy + 3, c)
        sp.px(x0 + 5, yy + 1, tuple(min(255, v + 60) for v in c))
    else:                                                                     # pieds nus
        m = sp.paint(sp.m_rect(x0 + 1, yy + 1, x0 + 7, yy + 3), S["b"])
        sp.tone(sp.m_rect(x0 + 1, yy + 3, x0 + 7, yy + 3), S["s"])


def leg_paint(sp, m, r, P, S, ytop, ybot, x0, x1):
    bas = r["bas"]
    if bas in ("short",):
        knee = ytop + int((ybot - ytop) * 0.45)
        sk = m & sp.m_rect(0, knee + 1, W, H)
        sp.paint(m & ~sk, P["b"]); sp.shade(m & ~sk, P["s"], dx=-1, dy=0, depth=2)
        sp.paint(sk, S["b"]); sp.shade(sk, S["s"], dx=-1, dy=0, depth=1)
    elif bas == "jupe":
        sp.paint(m, S["b"] if not r.get("collant") else col(r["collant"]))
        sp.shade(m, S["s"] if not r.get("collant") else tons(r["collant"])["s"], dx=-1, dy=0, depth=1)
    else:
        sp.paint(m, P["b"]); sp.shade(m, P["s"], dx=-1, dy=0, depth=2)
        sp.tone(sp.m_rect(x0, ytop, x0, ybot) & m, P["h"])
        if bas == "jogging":
            sp.tone(m & sp.m_rect(x1 - 1, ytop, x1 - 1, ybot - 1), (236, 236, 240))
            sp.tone(m & sp.m_rect(x0, ybot - 1, x1, ybot), P["s"])
        elif bas in ("pantalon", "costume"):
            sp.tone(m & sp.m_rect((x0 + x1) // 2, ytop + 3, (x0 + x1) // 2, ybot), P["s"])
        elif bas == "cargo":
            sp.tone(m & sp.m_rect(x0 + 1, ytop + 7, x1 - 1, ytop + 10), P["s"])
            sp.tone(m & sp.m_rect(x0 + 1, ytop + 7, x1 - 1, ytop + 7), P["d"])
        elif bas == "armure":
            sp.tone(m & sp.m_rect(x0, ytop + (ybot - ytop) // 2, x1, ytop + (ybot - ytop) // 2 + 1), METAL["h"])


def legs(sp, g, r, step, S, back):
    k = r["haut"]
    P = METAL if r["bas"] == "armure" else tons(r["couleur_bas"])
    sc = col(r["couleur_chaussures"])
    hidden = k in LONGS and not g.assis
    if g.assis:
        seat = g.hem
        x0 = g.b["legs"][0][0] - 1
        knee = 35
        for k2, (dx, dy) in enumerate(((1, -1), (0, 0))):
            th = sp.m_rect(x0 + dx, seat - 2 + dy, knee + dx, seat + 4 + dy)
            sh = sp.m_rect(knee - 5 + dx, seat + 2 + dy, knee + dx, g.foot)
            m = th | sh
            if r["bas"] == "short":
                sp.paint(th, P["b"]); sp.shade(th, P["s"], dx=0, dy=-1, depth=2)
                sp.paint(sh & ~th, S["b"]); sp.shade(sh & ~th, S["s"], dx=-1, dy=0, depth=1)
            elif r["bas"] == "jupe":
                sp.paint(m, S["b"]); sp.shade(m, S["s"], dx=-1, dy=-1, depth=1)
            else:
                sp.paint(m, P["b"]); sp.shade(m, P["s"], dx=-1, dy=-1, depth=2)
                sp.tone(sp.m_rect(x0 + dx, seat - 2 + dy, knee + dx, seat - 2 + dy), P["h"])
            if k2 == 0:
                sp.tone(m, P["s"] if r["bas"] not in ("short", "jupe") else S["s"])
            shoe(sp, knee - 5 + dx, g.foot, r["chaussures"], sc, S)
        return
    p = step % 8                                          # marche en 8 images (jambes qui se croisent en douceur)
    nd = [0, -1, -2, -1, 0, 1, 2, 1][p]
    offs = (nd, -nd)
    for k2, (lx, w) in enumerate(g.b["legs"]):
        dx = offs[k2]
        lift = 1 if (k2 == 1 and p in (1, 2)) or (k2 == 0 and p in (5, 6)) else 0
        x0, x1 = lx + dx, lx + dx + w
        ytop, ybot = g.hem - 1, g.foot - lift
        if not hidden:
            m = sp.m_rect(x0, ytop, x1, ybot)
            leg_paint(sp, m, r, P, S, ytop, ybot, x0, x1)
        shoe(sp, (lx - 1 if k2 == 0 else lx) + dx, ybot + (1 if hidden and r["chaussures"] == "sandales" else 0),
             r["chaussures"], sc, S)
    if not hidden and step % 2 == 0 and r["bas"] in ("jean", "pantalon", "costume", "jogging", "cargo"):
        xm = g.b["legs"][1][0] - 1
        sp.tone(sp.m_rect(xm, g.hem + 2, xm, g.foot) & (sp.a[..., 3] > 0), P["d"])


# ===================================================================== haut du corps
def torso_poly(g, r, ext=0, hem=None):
    L, R = g.b["L"] - ext, g.b["R"] + ext
    t = g.top
    h = g.hem if hem is None else hem
    if r["genre"] == "f" and r["corpulence"] != "fort":
        mid = t + (g.hem - t) // 2
        return [(L + 1, t), (R - 1, t), (R + 1, t + 3), (R, mid), (R + 1, h), (L - 1, h), (L, mid), (L - 1, t + 3)]
    return [(L, t), (R, t), (R + 2, t + 3), (R + 1, h), (L - 1, h), (L - 2, t + 3)]


def long_poly(g, r, hem, flare=1):
    L, R = g.b["L"], g.b["R"]
    t = g.top
    if r["genre"] == "f" and r["corpulence"] != "fort":
        mid = t + (g.hem - t) // 2
        return [(L + 1, t), (R - 1, t), (R + 1, t + 3), (R, mid), (R + 2 + flare, hem), (L - 2 - flare, hem), (L, mid), (L - 1, t + 3)]
    return [(L, t), (R, t), (R + 2, t + 3), (R + 2 + flare, hem), (L - 2 - flare, hem), (L - 2, t + 3)]


DIGITS = {"0": ["xxx", "x.x", "x.x", "x.x", "xxx"], "1": [".x.", "xx.", ".x.", ".x.", "xxx"], "2": ["xxx", "..x", "xxx", "x..", "xxx"],
          "3": ["xxx", "..x", ".xx", "..x", "xxx"], "4": ["x.x", "x.x", "xxx", "..x", "..x"], "5": ["xxx", "x..", "xxx", "..x", "xxx"],
          "6": ["xxx", "x..", "xxx", "x.x", "xxx"], "7": ["xxx", "..x", ".x.", ".x.", ".x."], "8": ["xxx", "x.x", "xxx", "x.x", "xxx"],
          "9": ["xxx", "x.x", "xxx", "..x", "xxx"]}


def digits(sp, txt, x, y, c):
    for ch in txt:
        for j, row in enumerate(DIGITS.get(ch, [])):
            for i, v in enumerate(row):
                if v == "x":
                    sp.px(x + i, y + j, c)
        x += 4


def motif(sp, kind, cx, cy, c, body):
    pts = dict(etoile=[(0, -2), (-1, -1), (0, -1), (1, -1), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (-1, 1), (1, 1), (-2, 2), (2, 2)],
               coeur=[(-1, -1), (1, -1), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (-1, 1), (0, 1), (1, 1), (0, 2)],
               eclair=[(1, -2), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (0, 1), (-1, 2)],
               rond=[(x, y) for x in range(-2, 3) for y in range(-2, 3) if x * x + y * y <= 5],
               logo=[(x, y) for x in range(-2, 3) for y in range(-1, 2)])
    for dx, dy in pts.get(kind, []):
        if body[cy + dy, cx + dx]:
            sp.px(cx + dx, cy + dy, c)


def garment(sp, g, r, back):
    k = r["haut"]
    P, P2 = tons(r["couleur"]), tons(r["couleur2"])
    t, hm = g.top, g.hem
    L, R = g.b["L"], g.b["R"]
    hem = hm
    if k in LONGS:
        hem = g.foot if not g.assis else hm + 2
        body = sp.m_poly(long_poly(g, r, hem, flare=3 if k == "abaya" else 1))
    elif k in KNEE:
        hem = g.kh if k != "tunique" else hm + int((g.foot - hm) * 0.3)
        body = sp.m_poly(long_poly(g, r, hem, flare=1))
    elif k in ("robe",):
        hem = g.kh
        body = sp.m_poly(torso_poly(g, r)) | sp.m_poly([(L, hm - 4), (R, hm - 4), (R + 4, hem), (L - 4, hem)])
    elif k == "doudoune":
        body = sp.m_poly(torso_poly(g, r, ext=1))
    else:
        body = sp.m_poly(torso_poly(g, r))
    if r["corpulence"] == "fort" and k not in LONGS:
        body |= sp.m_ell(R, t + (hm - t) * 0.62, 4.5, (hm - t) * 0.38) & sp.m_rect(0, t + 4, W, hm)
    MAIN = METAL if k == "armure" else P
    if k == "tablier":
        MAIN = P2
    sp.paint(body, MAIN["b"])
    sp.shade(body, MAIN["s"], dx=-1, dy=-1, depth=3)
    sp.tone(sp.m_rect(L - 2, t + 2, L - 1, hem - 2) & body & ~sp.m_rect(L, 0, W, H), MAIN["h"])
    if g.assis and (k in LONGS or k in KNEE or k == "robe"):
        lap = sp.m_rect(L - 1, hm - 3, 37, hm + 5)
        if k in LONGS or k == "robe":
            lap |= sp.m_rect(30, hm + 5, 37, g.foot - (2 if k in LONGS else 5))
        sp.paint(lap, MAIN["b"], newpart=False); sp.shade(lap, MAIN["s"], dx=-1, dy=-1, depth=2)
        sp.tone(lap & sp.m_rect(0, hm - 3, W, hm - 3), MAIN["h"])
    if back:
        sp.tone(body & sp.m_rect(21, t + 3, 21, hem - 1), MAIN["s"])
        if k == "sweat":
            sp.tone(sp.m_ell(21.5, t + 2, 7.5, 4.5) & body, P["s"]); sp.tone(sp.m_ell(21.5, t + 1, 5.5, 2.5) & body, P["d"])
        return body
    # ----- détails de face
    if k in ("tshirt", "maillot", "pull", "polo"):
        sp.tone(sp.m_ell(21.5, t + 0.5, 4.2, 1.6) & body, P["d"])
        sp.tone(sp.m_rect(L - 2, hm, R + 2, hm) & body, P["s"])
    if k == "pull":
        band = sp.m_rect(L - 2, hm - 2, R + 2, hm) & body
        sp.tone(band, P["s"]); sp.tone(band & ((XX % 2) == 0), P["d"])
        if r["motif"] == "bande":
            sp.tone(body & sp.m_rect(0, t + 6, W, t + 8), P2["b"]); sp.tone(body & sp.m_rect(0, t + 7, W, t + 7), P2["s"])
    if k == "polo":
        sp.pxs([(18, t), (19, t + 1), (20, t + 2), (25, t), (24, t + 1), (23, t + 2)], P["h"])
        sp.pxs([(21, t + 3), (21, t + 5)], P["d"])
    if k == "maillot":
        sp.pxs([(18, t), (19, t + 1), (20, t + 2), (21, t + 3), (22, t + 2), (23, t + 1), (24, t)], P2["b"])
        digits(sp, str(r.get("numero", 10)), 18, t + 6, P2["b"])
        sp.tone(body & sp.m_rect(R + 1, t + 3, R + 2, hm), P2["b"])
    if k in ("tshirt", "sweat", "pull") and r["motif"] and r["motif"] != "bande":
        motif(sp, r["motif"], 22, t + 6, P2["b"], body)
    if k == "sweat":
        ph = hm - 10
        pk = sp.m_rect(15, ph, 27, ph + 5)
        sp.tone(pk, P["s"]); sp.tone(sp.m_rect(15, ph, 27, ph), P["d"])
        sp.tone(sp.m_rect(15, ph, 15, ph + 5), P["d"]); sp.tone(sp.m_rect(27, ph, 27, ph + 5), P["d"])
        sp.tone(sp.m_rect(L - 1, hm - 2, R + 1, hm - 1) & body, P["s"])
        for cx in (19, 23):
            sp.tone(sp.m_rect(cx, t + 1, cx, t + 6), P2["b"] if r["couleur2"] != (242, 242, 244) else WHITE)
            sp.px(cx, t + 7, (210, 210, 220))
        sp.tone(sp.m_ell(21.5, t + 0.5, 6.5, 2.2), P["d"])
    if k in ("chemise", "police"):
        sp.paint(sp.m_poly([(17, t - 1), (21, t), (20, t + 3)]) | sp.m_poly([(26, t - 1), (22, t), (23, t + 3)]), P["h"], newpart=False)
        sp.tone(body & sp.m_rect(21, t + 3, 21, hm - 1), P["s"])
        for yy in range(t + 5, hm - 1, 4):
            sp.px(21, yy, P["d"])
        sp.tone(sp.m_rect(L - 2, hm, R + 2, hm) & body, P["s"])
        if k == "chemise":
            sp.tone(sp.m_rect(25, t + 5, 28, t + 5) | sp.m_rect(25, t + 5, 25, t + 8) | sp.m_rect(28, t + 5, 28, t + 8) |
                    sp.m_rect(25, t + 8, 28, t + 8), P["s"])
    if k == "police":
        star = [(26, t + 4), (25, t + 5), (26, t + 5), (27, t + 5), (25, t + 6), (27, t + 6)]
        sp.pxs(star, col("or")); sp.px(26, t + 6, (170, 130, 40))
        sp.tone(body & (sp.m_rect(L, t, L + 4, t + 1) | sp.m_rect(R - 4, t, R, t + 1)), P["d"])
        sp.paint(sp.m_rect(L - 2, hm - 2, R + 2, hm - 1) & body, (30, 28, 34), newpart=False)
        sp.pxs([(21, hm - 2), (22, hm - 2), (21, hm - 1), (22, hm - 1)], (200, 204, 214))
        sp.paint(sp.m_rect(13, t + 4, 15, t + 8), (30, 30, 36), newpart=False); sp.px(14, t + 3, (30, 30, 36))
    if k == "chemise_ouverte":
        band = sp.m_rect(18, t, 24, hm) & body
        sp.paint(band, P2["b"], newpart=False); sp.shade(band, P2["s"], dx=-1, dy=-1, depth=1)
        sp.tone(body & (sp.m_rect(17, t, 17, hm) | sp.m_rect(25, t, 25, hm)), P["d"])
        sp.paint(sp.m_poly([(15, t - 1), (19, t), (18, t + 4)]) | sp.m_poly([(28, t - 1), (24, t), (25, t + 4)]), P["h"], newpart=False)
        sp.tone(sp.m_rect(L - 2, hm, R + 2, hm) & body, P["s"])
    if k in ("costume", "blazer", "redingote", "blouse"):
        vb = t + 11 if k in ("costume", "blazer") else (t + 9 if k == "blouse" else hm - 2)
        inner = P2 if k != "costume" or r["couleur2"] != (242, 242, 244) else tons("blanc")
        if k == "redingote":
            v = sp.m_poly([(18, t), (25, t), (23, vb), (20, vb)]) & body
        else:
            v = sp.m_poly([(18, t), (25, t), (21.5, vb)]) & body
        sp.paint(v, inner["b"], newpart=False); sp.shade(v, inner["s"], dx=-1, dy=-1, depth=1)
        for a, b_ in (((17, t), (21, vb)), ((26, t), (22, vb))):
            n = max(1, vb - t)
            for i in range(n + 1):
                x = round(a[0] + (b_[0] - a[0]) * i / n); y = round(a[1] + (b_[1] - a[1]) * i / n)
                if body[y, x]:
                    sp.px(x, y, P["h"])
        if k == "costume" and "sans_cravate" not in r["acc"]:
            tc = col((r["couleurs_acc"] or {}).get("cravate", "rouge"))
            sp.paint(sp.m_rect(21, t, 22, t + 1), tc, newpart=False)
            sp.paint(sp.m_poly([(21, t + 2), (22, t + 2), (23, t + 8), (21.5, t + 10), (20, t + 8)]), tc, newpart=False)
            sp.tone(sp.m_rect(21, t + 3, 21, t + 8), tuple(int(v * 0.75) for v in tc))
            sp.pxs([(19, t), (24, t)], (250, 250, 252))
        if k in ("costume", "blazer"):
            sp.pxs([(21, vb + 2), (21, vb + 5)], P["d"])
            sp.tone(body & (sp.m_rect(25, hm - 6, 29, hm - 6) | sp.m_rect(13, hm - 6, 17, hm - 6)), P["s"])
            sp.tone(sp.m_rect(L - 2, hm, R + 2, hm) & body, P["s"])
        if k == "blouse":
            sp.tone(body & sp.m_rect(21, vb, 22, hem), P["s"])
            for x0 in (13, 25):
                sp.tone(body & (sp.m_rect(x0, hm, x0 + 4, hm) | sp.m_rect(x0, hm, x0, hm + 3) | sp.m_rect(x0 + 4, hm, x0 + 4, hm + 3)), P["s"])
            sp.tone(sp.m_rect(25, t + 5, 28, t + 5), P["s"]); sp.pxs([(26, t + 3), (26, t + 4)], (60, 90, 190))
        if k == "redingote":
            for yy in range(t + 3, hm - 2, 3):
                sp.px(21, yy, col("or"))
            sp.paint(sp.m_rect(20, t - 1, 23, t + 1), (246, 244, 236), newpart=False)
            sp.pxs([(19, t + 2), (24, t + 2), (20, t + 2), (23, t + 2)], (246, 244, 236))
            sp.tone(body & sp.m_rect(L - 2, hm - 1, R + 3, hm - 1), P["s"])
    if k == "cuir":
        band = sp.m_rect(19, t, 24, hm) & body
        sp.paint(band, P2["b"], newpart=False); sp.shade(band, P2["s"], dx=-1, dy=-1, depth=1)
        sp.tone(body & (sp.m_rect(18, t, 18, hm) | sp.m_rect(25, t, 25, hm)), P["h"])
        sp.paint(sp.m_poly([(14, t - 1), (19, t), (18, t + 4)]) | sp.m_poly([(29, t - 1), (24, t), (25, t + 4)]), P["h"], newpart=False)
        sp.tone(sp.m_rect(L - 2, hm - 1, R + 2, hm) & body, P["d"])
        sp.pxs([(26, t + 8), (27, t + 9), (28, t + 10)], P["h"])
    if k == "doudoune":
        for yy in range(t + 4, hm, 4):
            sp.tone(body & sp.m_rect(0, yy, W, yy), P["s"])
        col_ = sp.m_rect(17, t - 2, 26, t + 1)
        sp.paint(col_, P["b"], newpart=False); sp.shade(col_, P["s"], dx=-1, dy=-1, depth=1)
        sp.tone(body & sp.m_rect(21, t + 1, 21, hm), P["d"])
    if k == "survet":
        sp.tone(body & sp.m_rect(21, t, 21, hm), (220, 220, 228))
        sp.tone(body & (sp.m_rect(L - 1, t + 3, L - 1, hm) | sp.m_rect(R + 1, t + 3, R + 1, hm)), P2["b"])
        sp.tone(sp.m_rect(17, t - 1, 26, t + 1) & body, P["s"])
        sp.tone(sp.m_rect(L - 2, hm - 1, R + 2, hm) & body, P["s"])
    if k == "tablier":
        apron = (sp.m_rect(17, t + 2, 26, t + 9) | sp.m_poly([(L - 1, t + 9), (R + 1, t + 9), (R + 2, g.kh), (L - 2, g.kh)]))
        sp.paint(apron, P["b"], newpart=False); sp.shade(apron, P["s"], dx=-1, dy=-1, depth=2)
        sp.pxs([(17, t + 1), (18, t), (26, t + 1), (25, t)], P["b"])
        sp.tone(apron & sp.m_rect(0, t + 9, W, t + 9), P["s"])
        sp.tone(apron & (sp.m_rect(19, hm - 4, 24, hm - 4) | sp.m_rect(19, hm - 4, 19, hm) | sp.m_rect(24, hm - 4, 24, hm)), P["s"])
        sp.tone(sp.m_ell(21.5, t + 0.5, 4.2, 1.6) & body, P2["d"])
    if k in ("qamis", "djellaba", "abaya", "robe_longue", "toge"):
        if k in ("qamis",):
            for kk in range(3):
                sp.px(21, t + 4 + kk * 4, P["d"])
        if k == "djellaba":
            sp.tone(body & sp.m_rect(21, t + 1, 22, hem), P2["b"])
            for yy in range(t + 2, t + 14, 3):
                sp.px(21, yy, P2["d"])
        f0 = t + int((hem - t) * 0.55)
        for fx, d0 in ((16, 4), (25, 0), (29, 8)):
            sp.tone(body & sp.m_rect(fx, f0 + d0, fx, hem - 1), MAIN["s"])
        sp.tone(body & sp.m_rect(0, hem - 1, W, hem), MAIN["d"])
        if k == "toge":
            sash = sp.m_poly([(L - 2, t + 1), (L + 4, t), (R + 3, hm + 5), (R - 2, hm + 8)]) & body
            sp.paint(sash, P2["b"], newpart=False); sp.shade(sash, P2["s"], dx=-1, dy=-1, depth=1)
            sp.tone(sash & sp.m_rect(0, 0, L + 2, H), P2["h"])
    if k == "robe":
        sp.tone(body & sp.m_rect(L - 4, hm - 4, R + 4, hm - 3), P2["b"])
        sp.pxs([(19, t), (20, t + 1), (21, t + 2), (22, t + 2), (23, t + 1), (24, t)], P["d"])
        for fx in (16, 21, 27):
            sp.tone(body & sp.m_rect(fx, hm + 1, fx, hem - 1), P["s"])
    if k == "tunique":
        sp.paint(sp.m_rect(L - 2, hm - 2, R + 2, hm - 1) & body, (92, 60, 34), newpart=False)
        sp.pxs([(21, hm - 2), (22, hm - 2), (21, hm - 1), (22, hm - 1)], col("or"))
        sp.tone(body & sp.m_rect(21, t, 21, t + 4), P["d"])
        sp.tone(body & sp.m_rect(0, hem - 1, W, hem), P["s"])
    if k == "armure":
        for yy in (t + 8, t + 14):
            sp.tone(body & sp.m_rect(0, yy, W, yy), METAL["d"])
        sp.tone(body & sp.m_rect(L, t + 2, L + 1, hm - 3), METAL["h"])
        tab = sp.m_rect(17, t + 3, 26, max(g.kh - 4, hm + 2))
        sp.paint(tab, P2["b"], newpart=False); sp.shade(tab, P2["s"], dx=-1, dy=-1, depth=1)
        cy_ = t + 9
        sp.pxs([(21, cy_ - 2), (22, cy_ - 2), (20, cy_ - 1), (23, cy_ - 1), (20, cy_), (23, cy_), (21, cy_ + 1), (22, cy_ + 1)], col("or"))
        sp.paint(sp.m_rect(L - 1, hm - 1, R + 1, hm), (92, 60, 34), newpart=False)
    if k == "combinaison":
        sp.tone(body & sp.m_rect(21, t, 21, hm), P["d"])
        sp.tone(body & sp.m_rect(L - 2, hm - 1, R + 2, hm - 1), P["s"])
        sp.paint(sp.m_rect(14, t + 3, 16, t + 5), P2["b"], newpart=False)
        sp.tone(sp.m_rect(24, t + 4, 28, t + 7) & body, P["s"])
    return body


def body_acc(sp, g, r, back):
    acc, ca = r["acc"], (r["couleurs_acc"] or {})
    t, hm = g.top, g.hem
    L, R = g.b["L"], g.b["R"]
    if back:
        return
    if "gilet" in acc:
        V = tons(ca.get("gilet", (34, 104, 84)))
        v = sp.m_poly([(L, t + 1), (R, t + 1), (R + 1, t + 4), (R + 1, min(hm, t + 23)), (L - 1, min(hm, t + 23)), (L - 1, t + 4)]) & \
            ~sp.m_poly([(19, t + 1), (25, t + 1), (23, t + 15), (21, t + 15)])
        sp.paint(v, V["b"], newpart=False); sp.shade(v, V["s"], dx=-1, dy=-1, depth=2)
        sp.tone(sp.m_rect(L - 1, t + 5, L - 1, t + 22) & v, V["h"])
        trim = v & ~(np.roll(v, 1, 1) & np.roll(v, -1, 1) & np.roll(v, 1, 0) & np.roll(v, -1, 0)) & sp.m_rect(17, t + 1, 27, t + 17)
        sp.tone(trim, col(ca.get("liseré", "or")))
    if "collier" in acc:                                   # grand collier égyptien (usekh) : rangs de perles
        cc = ca.get("collier")
        rangs = [col("or"), (40, 120, 180), col("or"), (190, 60, 50), (60, 170, 160)] if cc is None else \
            [col(cc), tons(cc)["s"], col(cc), tons(cc)["s"]]
        cy_ = t - 1
        rho = np.sqrt(((XX - 21.5) / 9.6) ** 2 + ((YY - cy_) / 7.4) ** 2)
        zone = (rho <= 1.0) & (rho >= 0.42) & (YY >= t - 1) & sp.m_rect(L - 1, 0, R + 1, H)
        n = len(rangs)
        for i, c in enumerate(rangs):
            lo, hi = 0.42 + (1.0 - 0.42) * i / n, 0.42 + (1.0 - 0.42) * (i + 1) / n
            sp.paint(zone & (rho >= lo) & (rho <= hi + 0.001), c, newpart=(i == 0))
        sp.tone(zone & (rho > 0.9) & ((XX % 2) == 0), tons(rangs[0])["s"])
    if "devanteau" in acc and not g.assis:                                 # tablier d'apparat qui pend devant la ceinture (Pharaon)
        dv = sp.m_poly([(18, hm - 1), (25, hm - 1), (26, hm + 13), (17, hm + 13)])
        sp.paint(dv, col("or"), newpart=False)
        for yy in range(hm + 1, hm + 13, 3):
            sp.tone(dv & sp.m_rect(0, yy, W, yy), (40, 84, 170))
        sp.tone(dv & sp.m_rect(17, hm - 1, 17, hm + 13), tons("or")["s"])
    if "ceinture" in acc:
        sp.paint(sp.m_rect(L - 2, hm - 2, R + 2, hm - 1) & (sp.a[..., 3] > 0), col(ca.get("ceinture", (44, 32, 30))), newpart=False)
        sp.pxs([(21, hm - 2), (22, hm - 2), (21, hm - 1), (22, hm - 1)], col("or"))
    if "cravate" in acc:
        tc = col(ca.get("cravate", "rouge"))
        sp.paint(sp.m_rect(21, t, 22, t + 1), tc, newpart=False)
        sp.paint(sp.m_poly([(21, t + 2), (22, t + 2), (23, t + 9), (21.5, t + 11), (20, t + 9)]), tc, newpart=False)
        sp.tone(sp.m_rect(21, t + 3, 21, t + 9), tuple(int(v * 0.75) for v in tc))
    if "noeud" in acc:
        tc = col(ca.get("noeud", "noir"))
        sp.pxs([(19, t), (19, t + 1), (19, t + 2), (20, t + 1), (21, t + 1), (22, t + 1), (23, t + 1), (24, t), (24, t + 1), (24, t + 2)], tc)
    if "chaine" in acc:
        gc = col(ca.get("chaine", "or"))
        for i, x in enumerate(range(17, 26)):
            sp.px(x, t + 5 - abs(x - 21), gc)
        sp.pxs([(21, t + 6), (22, t + 6), (21, t + 7), (22, t + 7)], gc); sp.px(21, t + 6, (255, 240, 170))
    if "stethoscope" in acc:
        gc = (110, 116, 128)
        sp.pxs([(17, t), (17, t + 1), (17, t + 2), (17, t + 3), (18, t + 4), (18, t + 5), (18, t + 6), (18, t + 7)], gc)
        sp.pxs([(26, t), (26, t + 1), (26, t + 2), (25, t + 3), (25, t + 4), (25, t + 5)], gc)
        sp.paint(sp.m_ell(18, t + 9, 1.6, 1.6), (210, 214, 224), newpart=False)
    if "badge" in acc:
        sp.paint(sp.m_rect(24, t + 6, 28, t + 8), (248, 248, 250), newpart=False)
        sp.tone(sp.m_rect(24, t + 6, 28, t + 6), col(ca.get("badge", "bleu")))
    if "medaille" in acc:
        rc = col(ca.get("medaille", "rouge"))
        sp.pxs([(19, t), (20, t + 1), (20, t + 2), (21, t + 3), (23, t), (22, t + 1), (22, t + 2), (21, t + 4)], rc)
        sp.paint(sp.m_ell(21.5, t + 6, 1.6, 1.6), col("or"), newpart=False)
    if "echarpe" in acc:
        E = tons(ca.get("echarpe", "rouge"))
        m = sp.m_rect(16, t - 2, 27, t + 1) | sp.m_rect(15, t + 1, 18, t + 10)
        sp.paint(m, E["b"], newpart=False); sp.shade(m, E["s"], dx=-1, dy=-1, depth=1)
        sp.tone(m & sp.m_rect(0, t + 4, W, t + 4), E["s"]); sp.tone(m & sp.m_rect(0, t + 7, W, t + 7), E["s"])
        for x in (15, 17):
            sp.px(x, t + 11, E["b"])
    if "sac" in acc:
        sp.paint(sp.m_line([(14, t), (15, t + 11)], 2), col(ca.get("sac_bretelle", (40, 40, 48))), newpart=False)
    if "cape" in acc:
        sp.pxs([(L, t + 1), (R, t + 1)], col("or"))


def back_layer(sp, g, r, back):
    st, hat, acc = r["cheveux"], r["chapeau"], r["acc"]
    ca = r["couleurs_acc"] or {}
    t, y0 = g.top, g.y0
    covered = hat in ("hijab", "keffieh", "capuche", "nemes", "khat")
    HP = tons(r["couleur_cheveux"])
    if hat in ("nemes", "khat") and not back:
        nem = hat == "nemes"
        Bq = tons((40, 84, 170) if nem else r["couleur_chapeau"])
        tail = sp.m_poly([(9, y0 + 9), (14, y0 + 10), (15, t + 3), (9, t + 4), (7, y0 + 16)]) if nem else \
            sp.m_poly([(9, y0 + 10), (13, y0 + 11), (12, y0 + 21), (8, y0 + 20)])
        sp.paint(tail, Bq["b"])
        if nem:
            sp.tone(tail & ((((YY - y0) // 2) % 2) == 0), tons(r.get("couleur_rayures") or "or")["s"])
        sp.shade(tail, Bq["s"], dx=-1, dy=0, depth=1)
    if "cape" in acc:
        C = tons(ca.get("cape", "rouge"))
        L, R = g.b["L"], g.b["R"]
        m = sp.m_poly([(L - 1, t), (R + 1, t), (R + 4, g.foot - 1), (L - 6, g.foot - 1)])
        sp.paint(m, C["b"]); sp.shade(m, C["s"], dx=-1, dy=-1, depth=2)
        for fx in (L - 3, R + 2):
            sp.tone(m & sp.m_rect(fx, t + 8, fx, g.foot - 2), C["d"])
    if "sac" in acc:
        B = tons(ca.get("sac", "marine"))
        m = sp.m_rect(5, t + 1, 11, t + 15) & ~sp.m_rect(5, t + 1, 5, t + 1)
        sp.paint(m, B["b"]); sp.shade(m, B["s"], dx=-1, dy=-1, depth=1)
        sp.tone(sp.m_rect(5, t + 9, 11, t + 9), B["d"])
    if r["haut"] == "djellaba" and not back:
        P = tons(r["couleur"])
        hood = sp.m_poly([(9, t - 1), (17, t - 2), (18, t + 7), (12, t + 10), (8, t + 6)])
        sp.paint(hood, P["s"]); sp.tone(hood & sp.m_rect(0, t + 5, W, H), P["d"])
    if covered:
        return
    if st in ("long", "frange"):
        m = sp.m_poly([(12, y0 + 7), (24, y0 + 7), (25, y0 + 20), (23, t + 14), (9, t + 16), (8, y0 + 20)])
        if back:
            m = sp.m_poly([(12, y0 + 8), (31, y0 + 8), (33, t + 6), (31, t + 15), (11, t + 15), (9, t + 6)])
        sp.paint(m, HP["b"]); sp.shade(m, HP["s"], dx=-1, dy=-1, depth=1)
        for x in (11, 14, 17, 26, 29):
            sp.tone(m & sp.m_rect(x, y0 + 14, x, t + 15), HP["s"])
    elif st == "queue":
        tail = sp.m_line([(13, y0 + 6), (9, y0 + 12), (8, y0 + 19), (9, y0 + 25)], 4)
        sp.paint(tail, HP["b"]); sp.shade(tail, HP["s"], dx=-1, dy=-1, depth=1)
        sp.tone(tail & sp.m_rect(0, y0 + 8, 9, y0 + 20), HP["h"])
        sp.paint(sp.m_rect(10, y0 + 7, 12, y0 + 8), col(r.get("couleur_acc_cheveux") or "rouge"), newpart=False)
    elif st == "tresses":
        for i in range(5):
            x = 9 + i * 2.6
            m = sp.m_line([(x + 3, y0 + 8), (x, t + 4 + (i % 2) * 3)], 2)
            sp.paint(m, HP["b"] if i % 2 else HP["s"])
            sp.px(int(x), t + 5 + (i % 2) * 3, col(r.get("couleur_acc_cheveux") or "or"))


# ===================================================================== objets tenus en main
def objet(sp, kind, hx, hy, pose, r):
    hx, hy = int(round(hx)), int(round(hy))
    ca = r["couleurs_acc"] or {}
    if kind == "telephone":
        if pose == "selfie":                                  # au bout du bras, l'écran tourné vers soi
            sp.paint(sp.m_rect(hx, hy - 7, hx + 2, hy + 1), (34, 32, 42), newpart=False)
            sp.tone(sp.m_rect(hx, hy - 6, hx, hy), (150, 210, 250))
        elif pose == "photo":                                 # tenu droit devant les yeux, vu de profil
            sp.paint(sp.m_rect(hx + 1, hy - 7, hx + 3, hy + 1), (34, 32, 42), newpart=False)
            sp.tone(sp.m_rect(hx + 3, hy - 7, hx + 3, hy + 1), (84, 84, 96))
            sp.px(hx + 3, hy - 6, (150, 210, 250))
        elif pose == "appel":
            sp.paint(sp.m_rect(hx - 1, hy - 4, hx + 1, hy + 2), (34, 32, 42), newpart=False)
        else:
            sp.paint(sp.m_rect(hx + 1, hy - 6, hx + 4, hy), (34, 32, 42), newpart=False)
            sp.paint(sp.m_rect(hx + 2, hy - 5, hx + 3, hy - 1), (150, 210, 250), newpart=False)
            sp.px(hx + 2, hy - 5, (230, 246, 255))
    elif kind == "tasse":
        c = col(ca.get("tasse", "rouge"))
        sp.paint(sp.m_rect(hx + 1, hy - 5, hx + 5, hy), (246, 246, 248), newpart=False)
        sp.tone(sp.m_rect(hx + 1, hy - 3, hx + 5, hy - 2), c)
        sp.pxs([(hx + 6, hy - 4), (hx + 7, hy - 3), (hx + 6, hy - 2)], (246, 246, 248))
        sp.tone(sp.m_rect(hx + 1, hy - 5, hx + 5, hy - 5), (120, 70, 40))
        sp.pxs([(hx + 2, hy - 7), (hx + 3, hy - 8), (hx + 4, hy - 10)], (230, 230, 236))
    elif kind == "verre_the":
        gx, gy = hx + 2, hy - 6
        glass = sp.m_poly([(gx, gy), (gx + 4, gy), (gx + 3, gy + 6), (gx + 1, gy + 6)])
        sp.paint(glass, (190, 226, 236), newpart=False)
        sp.tone(glass & sp.m_rect(gx, gy + 2, gx + 4, gy + 6), (196, 120, 46))
        sp.tone(glass & sp.m_rect(gx + 1, gy + 3, gx + 1, gy + 5), (236, 176, 96))
        sp.pxs([(gx + 1, gy - 2), (gx + 2, gy - 3), (gx + 3, gy - 5)], (230, 230, 236))
    elif kind == "micro":
        c = col(ca.get("micro", "rouge"))
        sp.paint(sp.m_rect(hx - 1, hy - 3, hx, hy + 3), (34, 34, 40), newpart=False)
        sp.paint(sp.m_rect(hx - 2, hy - 4, hx + 1, hy - 2), c, newpart=False)
        head = sp.m_ell(hx - 0.5, hy - 6.5, 2.2, 2.2)
        sp.paint(head, (120, 124, 136), newpart=False)
        sp.tone(head & ((XX + YY) % 2 == 0), (70, 74, 86)); sp.px(hx - 1, hy - 7, (220, 224, 236))
    elif kind == "livre":
        c = col(ca.get("livre", "bordeaux"))
        sp.paint(sp.m_rect(hx, hy - 7, hx + 6, hy), c, newpart=False)
        sp.tone(sp.m_rect(hx + 6, hy - 7, hx + 6, hy), (246, 240, 224))
        sp.tone(sp.m_rect(hx + 1, hy - 5, hx + 4, hy - 5), col("or"))
    elif kind == "coran":                                     # le Coran : couverture verte, motif doré
        sp.paint(sp.m_rect(hx, hy - 7, hx + 6, hy), (24, 96, 60), newpart=False)
        sp.tone(sp.m_rect(hx + 6, hy - 7, hx + 6, hy), (246, 240, 224))
        sp.tone(sp.m_rect(hx + 2, hy - 5, hx + 4, hy - 2), col("or"))
        sp.px(hx + 3, hy - 4, (24, 96, 60))
    elif kind == "parchemin":
        sp.paint(sp.m_rect(hx, hy - 6, hx + 7, hy + 1), (236, 220, 176), newpart=False)
        sp.tone(sp.m_rect(hx, hy - 6, hx, hy + 1) | sp.m_rect(hx + 7, hy - 6, hx + 7, hy + 1), (186, 160, 112))
        for yy in (hy - 4, hy - 2):
            sp.tone(sp.m_rect(hx + 2, yy, hx + 5, yy), (150, 120, 90))
    elif kind == "ballon":
        m = sp.m_ell(hx + 3, hy - 1, 3.2, 3.2)
        sp.paint(m, (250, 250, 250), newpart=False)
        sp.pxs([(hx + 3, hy - 1), (hx + 2, hy - 2), (hx + 4, hy - 2), (hx + 1, hy + 1), (hx + 5, hy + 1), (hx + 3, hy - 4)], (40, 40, 46))
    elif kind == "manette":
        sp.paint(sp.m_rect(hx - 1, hy - 2, hx + 6, hy + 1) | sp.m_rect(hx - 2, hy, hx - 1, hy + 2) | sp.m_rect(hx + 6, hy, hx + 7, hy + 2),
                 (44, 44, 54), newpart=False)
        sp.pxs([(hx + 4, hy - 1), (hx + 5, hy)], (220, 60, 70)); sp.px(hx + 1, hy - 1, (90, 200, 120))
    elif kind == "billets":
        for i, (dx, dy) in enumerate(((0, 0), (2, -1), (4, -2))):
            sp.paint(sp.m_rect(hx + dx, hy - 7 + dy, hx + dx + 4, hy - 1 + dy), (120, 190, 110), newpart=False)
            sp.tone(sp.m_rect(hx + dx + 1, hy - 5 + dy, hx + dx + 3, hy - 3 + dy), (70, 140, 80))
    elif kind == "stylo":
        sp.pxs([(hx + 1, hy - 1), (hx + 2, hy - 2), (hx + 3, hy - 3), (hx + 4, hy - 4)], (40, 70, 170)); sp.px(hx + 5, hy - 5, (30, 30, 36))
    elif kind == "epee":
        sp.paint(sp.m_rect(hx, hy - 20, hx + 1, hy - 3), (214, 220, 232), newpart=False)
        sp.tone(sp.m_rect(hx + 1, hy - 20, hx + 1, hy - 3), (150, 158, 176))
        sp.px(hx, hy - 21, (214, 220, 232))
        sp.paint(sp.m_rect(hx - 2, hy - 3, hx + 3, hy - 2), col("or"), newpart=False)
        sp.px(hx, hy + 2, col("or"))
    elif kind == "briques":                                # trois briques crues portées contre la poitrine
        for yy in (hy - 1, hy - 4, hy - 7):
            sp.paint(sp.m_rect(hx - 4, yy - 2, hx + 4, yy), (184, 140, 96), newpart=False)
            sp.tone(sp.m_rect(hx - 4, yy - 2, hx + 4, yy - 2), (206, 168, 120))
            sp.tone(sp.m_rect(hx - 4, yy, hx + 4, yy), (140, 104, 70))
    elif kind == "panier":                                 # panier de terre porté sur l'épaule
        sp.paint(sp.m_ell(hx - 1, hy - 8, 5, 3.5), (170, 130, 76), newpart=False)
        sp.tone(sp.m_rect(hx - 6, hy - 10, hx + 4, hy - 9), (120, 90, 56))
        sp.tone(sp.m_ell(hx - 1, hy - 11, 4, 1.5), (120, 92, 64))
    elif kind == "jarre":                                  # jarre d'eau en terre cuite, portée sur l'épaule
        sp.paint(sp.m_ell(hx - 1, hy - 9, 4, 5), (182, 112, 70), newpart=False)
        sp.paint(sp.m_rect(hx - 2, hy - 16, hx, hy - 13), (182, 112, 70), newpart=False)
        sp.tone(sp.m_rect(hx - 3, hy - 16, hx + 1, hy - 16), (150, 88, 54))
        sp.tone(sp.m_ell(hx + 1, hy - 8, 1.5, 3.5), (140, 82, 50))
        sp.tone(sp.m_rect(hx - 4, hy - 11, hx - 3, hy - 9), (214, 150, 104))
    elif kind == "lance":                                  # lance de soldat, tenue droite, pointe de bronze
        sp.paint(sp.m_rect(hx + 1, hy - 26, hx + 1, FOOT - 2), (120, 80, 44), newpart=False)
        sp.paint(sp.m_poly([(hx - 1, hy - 26), (hx + 3, hy - 26), (hx + 1, hy - 32)]), (200, 150, 80), newpart=False)
        sp.px(hx + 1, hy - 30, (240, 200, 130))
    elif kind == "baton":                                  # bâton de berger, droit, plus haut que la tête
        sp.paint(sp.m_line([(hx + 1, hy - 18), (hx + 2, FOOT - 1)], 2), (120, 78, 42), newpart=False)
        sp.pxs([(hx + 1, hy - 19), (hx + 2, hy - 20)], (150, 100, 56))
    elif kind == "fouet":                                  # fouet de contremaître (manche + lanière qui pend)
        sp.paint(sp.m_line([(hx, hy), (hx + 4, hy - 6)], 2), (110, 70, 40), newpart=False)
        sp.paint(sp.m_line([(hx + 4, hy - 6), (hx + 8, hy - 4), (hx + 9, hy + 2), (hx + 7, hy + 7)], 1), (70, 46, 30), newpart=False)
    elif kind == "crosse":                                 # crosse royale or et bleu, tenue en travers (Pharaon)
        tige = sp.m_line([(hx - 1, hy + 5), (hx + 4, hy - 5)], 2)
        sp.paint(tige, col("or"), newpart=False)
        sp.tone(tige & ((XX + YY) % 3 == 0), (40, 84, 170))
        sp.paint(sp.m_line([(hx + 4, hy - 5), (hx + 6, hy - 8), (hx + 9, hy - 8), (hx + 10, hy - 6)], 1), col("or"), newpart=False)
    elif kind == "canne":
        sp.paint(sp.m_line([(hx + 1, hy - 2), (hx + 4, FOOT - 1)], 2), (120, 76, 40), newpart=False)
        sp.pxs([(hx - 1, hy - 3), (hx, hy - 4), (hx + 1, hy - 4)], (120, 76, 40))
    elif kind == "torche":
        sp.paint(sp.m_line([(hx, hy + 1), (hx + 2, hy - 9)], 2), (110, 70, 40), newpart=False)
        fl = sp.m_ell(hx + 2, hy - 12, 2.2, 3.4)
        sp.paint(fl, (250, 150, 40), newpart=False); sp.tone(fl & sp.m_ell(hx + 2, hy - 11, 1.2, 1.8), (255, 236, 140))
    elif kind == "loupe":
        sp.paint(sp.m_line([(hx, hy), (hx + 3, hy - 3)], 2), (90, 60, 40), newpart=False)
        ring = sp.m_ell(hx + 5.5, hy - 5.5, 3.2, 3.2)
        sp.paint(ring, (200, 204, 214), newpart=False)
        sp.paint(sp.m_ell(hx + 5.5, hy - 5.5, 2.0, 2.0), (190, 230, 250), newpart=False); sp.px(hx + 5, hy - 6, (250, 250, 255))
    elif kind == "fiole":
        c = col(ca.get("fiole", "vert"))
        sp.paint(sp.m_rect(hx + 1, hy - 8, hx + 2, hy - 5) | sp.m_poly([(hx - 1, hy), (hx + 4, hy), (hx + 3, hy - 5), (hx, hy - 5)]),
                 (210, 236, 246), newpart=False)
        sp.tone(sp.m_poly([(hx - 1, hy), (hx + 4, hy), (hx + 3, hy - 3), (hx, hy - 3)]), c)
    elif kind == "sac_courses":
        sp.paint(sp.m_rect(hx - 3, hy + 2, hx + 3, hy + 9), (214, 180, 130), newpart=False)
        sp.tone(sp.m_rect(hx - 3, hy + 2, hx + 3, hy + 2), (170, 136, 90))
        sp.pxs([(hx - 1, hy), (hx - 1, hy + 1), (hx + 1, hy), (hx + 1, hy + 1)], (170, 136, 90))
        sp.pxs([(hx - 2, hy + 1), (hx + 2, hy + 1)], (90, 160, 70))
    elif kind == "manette_tv":
        sp.paint(sp.m_rect(hx + 1, hy - 5, hx + 2, hy + 1), (40, 40, 48), newpart=False); sp.px(hx + 1, hy - 4, (220, 60, 70))
    elif kind == "passeport":
        sp.paint(sp.m_rect(hx + 1, hy - 6, hx + 5, hy), (128, 26, 44), newpart=False)
        sp.tone(sp.m_rect(hx + 5, hy - 6, hx + 5, hy), (90, 16, 30))
        sp.pxs([(hx + 3, hy - 4), (hx + 2, hy - 3), (hx + 4, hy - 3), (hx + 3, hy - 2)], col("or"))
    elif kind == "valise":
        c = col(ca.get("valise", "bleu"))
        sp.pxs([(hx - 1, hy), (hx - 1, hy + 1), (hx + 2, hy), (hx + 2, hy + 1), (hx, hy - 1), (hx + 1, hy - 1)], (40, 34, 40))
        body = sp.m_rect(hx - 4, hy + 2, hx + 5, hy + 12)
        sp.paint(body, c, newpart=False)
        sp.tone(sp.m_rect(hx - 4, hy + 6, hx + 5, hy + 7), tuple(int(v * 0.7) for v in c))
        sp.tone(sp.m_rect(hx - 4, hy + 2, hx + 5, hy + 2), tuple(min(255, int(v * 1.25) + 20) for v in c))
        sp.pxs([(hx - 3, hy + 13), (hx + 4, hy + 13)], (40, 34, 40))


# ===================================================================== dessin complet
SWING = [0, 1, 2, 1, 0, -1, -2, -1]


def dessine(r, pose="neutre", face="neutre", talk=False, back=False, assis=False, step=None, blush=False, sweat=False,
            cligne=False, objet=None, larmes=False, bouche=None, accent=None, hoche=0, pose_de=None, mix=0.0, **_):
    """step (0-7) = marche ; pose_de + mix = geste en cours entre l'ancienne pose et la nouvelle ;
    bouche = forme du son prononcé (A, O, E, M, F) ; accent = "!" ou "?" (sourcils) ; hoche = tête baissée d'un pixel."""
    sp = Spr(W, H)
    marche = step is not None and not assis and not back
    g = geo(r, assis, dy=-1 if (marche and step % 4 == 0) else 0)
    S = r["_peau"]
    if pose not in POSES:
        pose = "neutre"
    obj = globals()["objet"]
    if objet is None:
        objet = POSE_OBJET.get(pose)

    def bras(pz):
        f_, n_ = POSES[pz] if not back else (N_, NN)
        fp = [(g.sr, g.ay), _pt(f_[0], g.sr, g.ay, g), _pt(f_[1], g.sr, g.ay, g)]
        npts = [(g.sl, g.ay), _pt(n_[0], g.sl, g.ay, g), _pt(n_[1], g.sl, g.ay, g)]
        return f_, n_, fp, npts
    far, near, farpts, nearpts = bras(pose)
    if pose_de in POSES and mix > 0 and not back:            # geste intermédiaire entre deux poses
        f2, n2, fp2, np2 = bras(pose_de)
        lerp = lambda a, b: (a[0] + (b[0] - a[0]) * mix, a[1] + (b[1] - a[1]) * mix)
        farpts = [lerp(a, b) for a, b in zip(farpts, fp2)]
        nearpts = [lerp(a, b) for a, b in zip(nearpts, np2)]
        if mix >= 0.5:
            far, near = f2, n2
    if marche and pose in ("neutre", "tient", "telephone", "the"):    # les bras se balancent en marchant
        sw = SWING[step % 8]
        farpts = [farpts[0], (farpts[1][0] + sw / 2, farpts[1][1]), (farpts[2][0] + sw, farpts[2][1])]
        if pose == "neutre":
            nearpts = [nearpts[0], (nearpts[1][0] - sw / 2, nearpts[1][1]), (nearpts[2][0] - sw, nearpts[2][1])]
    k = r["haut"]
    if k == "armure":
        sleeve, short = METAL, False
    elif k == "tablier":
        sleeve, short = tons(r["couleur2"]), True
    else:
        sleeve, short = tons(r["couleur"]), k in SHORT_SLEEVES
    cuff = sleeve["s"] if k in ("sweat", "pull", "survet", "doudoune") else None
    if not back:
        back_layer(sp, g, r, back)
        arm(sp, g, farpts, far[2], far[3], S, sleeve, short, cuff)
    legs(sp, g, r, step if marche else 0, S, back)
    garment(sp, g, r, back)
    if back:
        back_layer(sp, g, r, back)
    body_acc(sp, g, r, back)
    hd, y0 = g.hd, g.y0
    nx0, ny0, nx1, ny1 = hd["neck"]
    sp.paint(sp.m_rect(nx0, y0 + ny0, nx1, y0 + ny1), S["s"])
    if k == "pull" and r.get("col_roule"):
        P = tons(r["couleur"])
        m = sp.m_rect(18, y0 + ny0 + 1, 25, g.top + 1)
        sp.paint(m, P["b"]); sp.shade(m, P["s"], dx=-1, dy=-1, depth=1)
    head = head_mask(sp, g, back)
    sp.paint(head, S["b"])
    sp.shade(head, S["s"], dx=-1, dy=-1, depth=1)
    hair(sp, g, r, head, S, back)
    if not back:
        beard(sp, g, r, head)
        if not covers_ear(r):
            ex_, ey_ = hd["ear"]
            ear = sp.m_ell(ex_, y0 + ey_, 1.7, 2.3)
            sp.paint(ear, S["b"]); sp.px(int(ex_ + 0.2), y0 + int(ey_ + 0.4), S["s"]); sp.px(int(ex_ - 0.8), y0 + int(ey_ - 0.6), S["s"])
            if "boucles" in r["acc"]:
                sp.px(int(ex_), y0 + int(ey_) + 3, col("or"))
    hat(sp, g, r, S, back)
    if not back:
        draw_face(sp, g, r, face, talk, cligne, blush, sweat, larmes, S, bouche=bouche, accent=accent)
        if hoche:                                         # petit hochement : la tête descend d'un pixel
            r0, r1 = max(0, g.y0 - 16), g.y0 + hd["chin_y"]
            sp.a[r0 + 1:r1 + 2] = sp.a[r0:r1 + 1].copy()
            sp.a[r0] = 0
        hx, hy = arm(sp, g, nearpts, near[2], near[3], S, sleeve, short, cuff)
        if objet:
            obj(sp, objet, hx, hy, pose, r)
    else:
        for pts in (farpts, nearpts):
            arm(sp, g, pts, "poing", 2, S, sleeve, short, cuff)
    if k == "armure" and not back:
        for cx_ in (g.b["L"] - 1, g.b["R"] + 1):
            pa = sp.m_ell(cx_, g.top + 2, 3.6, 2.6)
            sp.paint(pa, METAL["b"], newpart=False); sp.shade(pa, METAL["s"], dx=-1, dy=-1, depth=1)
            sp.tone(pa & sp.m_rect(0, 0, W, g.top + 1), METAL["h"])
    sp.outline()
    return sp


# ===================================================================== registre des personnages
DEFAUT = dict(taille="adulte", genre="h", corpulence="normal", peau="doree", age=None,
              cheveux="court", couleur_cheveux="noir", barbe=None, couleur_barbe=None,
              haut="tshirt", couleur="bleu", couleur2="blanc", motif=None,
              bas="jean", couleur_bas="jean", chaussures="baskets", couleur_chaussures="rouge",
              chapeau=None, couleur_chapeau=(40, 44, 60), lunettes=None, couleur_lunettes=(64, 46, 52),
              acc=(), couleurs_acc=None, cadre=None, cote="droite", nom=None, description="")
CAST = {}
PALETTE_CADRES = [(226, 62, 62), (46, 176, 160), (240, 170, 50), (90, 130, 230), (190, 90, 200), (90, 190, 90),
                  (240, 120, 160), (200, 200, 210)]


def nouveau(ident, **kw):
    """Enregistre un personnage. ident = nom court en MAJUSCULES (sert aussi de nom des fichiers voix)."""
    r = dict(DEFAUT)
    r.update(kw)
    for key in ("couleur", "couleur2", "couleur_bas", "couleur_chaussures", "couleur_chapeau", "couleur_lunettes"):
        r[key] = col(r[key])
    r["couleur_cheveux"] = col(r["couleur_cheveux"])
    r["couleur_barbe"] = col(r["couleur_barbe"])
    r["acc"] = tuple(r["acc"] or ())
    r["_peau"] = PEAUX[r["peau"]] if isinstance(r["peau"], str) else r["peau"]
    if r["cadre"] is None:
        r["cadre"] = PALETTE_CADRES[len(CAST) % len(PALETTE_CADRES)]
    r["cadre"] = col(r["cadre"])
    if r["haut"] in ("costume",) and r["bas"] == "jean":
        r["bas"], r["couleur_bas"] = "costume", r["couleur"]
    if r["haut"] == "combinaison":
        r["bas"], r["couleur_bas"] = "pantalon", r["couleur"]
    CAST[ident] = r
    return r


def has(ident):
    return ident in CAST


def image(ident, **kw):
    im = dessine(CAST[ident], **kw).img()
    im.info["foot"] = FOOT
    return im


def head_top(ident, **kw):
    """Haut réel du dessin (chapeau compris) sur la toile du sprite : sert à placer les bulles."""
    a = np.array(duo.sprite(ident, **{k: v for k, v in kw.items() if k in ("assis", "pose", "back")}))
    rows = np.where(a[..., 3].max(axis=1) > 0)[0]
    return int(rows[0]) + 1 if len(rows) else 0


def portrait(ident, face="neutre", talk=False):
    """Vignette des sous-titres : tête et épaules (chapeaux compris)."""
    r = CAST[ident]
    a = dessine(r, "neutre", face, talk).a
    g = geo(r)
    zone = a[max(0, g.y0 - 14):g.y0 + 2, 8:36, 3]
    rows = np.where(zone.max(axis=1) > 0)[0]
    top = max(0, g.y0 - 14) + (int(rows[0]) if len(rows) else 14)
    top = min(top, g.y0 - 1)
    return a[top: g.y0 + 26, 8:36].copy()


def speaker(ident):
    r = CAST[ident]
    fr = r["cadre"]
    ol = tuple(int(v * 0.45) for v in fr)
    bg = tuple(int(v * 0.22 + 30) for v in fr)
    return dict(ol=ol, frame=fr, name=r["nom"] or ident, side="left" if r["cote"] == "gauche" else "right", bg=bg)


import troupe  # noqa: E402,F401  (les personnages prêts à l'emploi)
