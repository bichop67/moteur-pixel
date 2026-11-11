# ANIMAUX pixel art (même style que les persos : contour sombre, ombre et reflet), tournés vers la DROITE.
#   Actor("CHAT", x, y, k=7)  ou  sc.role("CHEVAL", x=700)  puis  .marche(…), .a(t, pose="mange")
# Noms : CHAT, CHAT_NOIR, CHAT_GRIS, CHIEN, CHIEN_NOIR, CHIEN_BLANC, CHEVAL, CHEVAL_BLANC, CHEVAL_NOIR, ANE, CHAMEAU,
#        MOUTON, CHEVRE, PIGEON.   Poses : debout, assis (chat, chien), couche (chat, chien, chameau),
#        mange (cheval, âne, chameau, mouton, chèvre), vole (pigeon). Marche : step = 0..3.
import numpy as np
from spr import Spr, INK


def _t(c):
    c = np.array(c, float)
    t = lambda v: tuple(int(x) for x in np.clip(v, 0, 255))
    return dict(b=t(c), s=t(c * 0.74 + np.array([-4, -4, 8])), d=t(c * 0.52 + np.array([-4, -4, 10])), h=t(c + (255 - c) * 0.3))


def _blob(sp, m, P, light=True):
    sp.paint(m, P["b"])
    sp.shade(m, P["s"], dx=-1, dy=-1, depth=1)
    if light:
        sp.light(m, P["h"], dx=1, dy=1, depth=1)
    return m


def _jambes(sp, xs, y0, y1, w, P, step, sabot=None, plie=None):
    """Quatre pattes ; la marche décale les pattes en diagonale (avant gauche + arrière droite ensemble)."""
    off = [(0, 0, 0, 0), (1, -1, -1, 1), (0, 0, 0, 0), (-1, 1, 1, -1)][step % 4] if step is not None else (0, 0, 0, 0)
    lift = [(0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0), (0, 1, 1, 0)][step % 4] if step is not None else (0, 0, 0, 0)
    for i, x in enumerate(xs):
        far = i in (1, 3)
        col = P["s"] if far else P["b"]
        yy1 = y1 - lift[i]
        m = sp.m_rect(x + off[i], y0, x + off[i] + w - 1, yy1)
        sp.paint(m, col)
        if not far:
            sp.tone(sp.m_rect(x + off[i], y0, x + off[i], yy1), P["h"])
        if sabot:
            sp.paint(sp.m_rect(x + off[i], yy1 - 1, x + off[i] + w - 1, yy1), sabot)


def chat(robe=(230, 140, 60), pose="debout", step=None, rayures=True):
    P = _t(robe)
    sp = Spr(30, 22)
    if pose == "couche":
        body = sp.m_ell(13, 17, 10, 3.6)
        _blob(sp, body, P)
        sp.paint(sp.m_line([(4, 18), (1, 19), (1, 20)], 2), P["s"])
        hx, hy = 24, 14
    elif pose == "assis":
        sp.paint(sp.m_line([(9, 20), (3, 20), (2, 17)], 2), P["s"])
        body = sp.m_ell(13, 14, 6, 6.6)
        _blob(sp, body, P)
        sp.paint(sp.m_rect(15, 16, 17, 20), P["b"]); sp.paint(sp.m_rect(12, 18, 14, 20), P["s"])
        hx, hy = 17, 7
    else:
        sp.paint(sp.m_line([(5, 12), (2, 9), (1, 5), (2, 3)], 2), P["s"])
        _jambes(sp, [7, 9, 19, 21], 15, 21, 2, P, step)
        body = sp.m_ell(13, 13, 9, 4.4)
        _blob(sp, body, P)
        hx, hy = 24, 9
    head = sp.m_ell(hx, hy, 4.4, 4.0)
    _blob(sp, head, P)
    for ex in ((hx - 3, hx - 1, hx - 2), (hx + 1, hx + 3, hx + 2)):
        sp.paint(sp.m_poly([(ex[0], hy - 2), (ex[1], hy - 2), (ex[2], hy - 6)]), P["b"], newpart=False)
        sp.px(ex[2], hy - 4, (240, 150, 160))
    if rayures and robe == (230, 140, 60):
        for x in (9, 13, 17):
            sp.tone(sp.m_rect(x, 9, x, 12) & body, P["s"])
    sp.pxs([(hx + 1, hy - 1), (hx + 3, hy - 1)], (120, 210, 90)); sp.pxs([(hx + 1, hy), (hx + 3, hy)], (30, 30, 36))
    sp.px(hx + 4, hy + 1, (240, 140, 150))
    sp.pxs([(hx + 5, hy + 1), (hx + 6, hy), (hx + 5, hy + 2), (hx + 6, hy + 3)], (240, 240, 240))
    sp.outline()
    return sp, 18


def chien(robe=(150, 100, 60), pose="debout", step=None, tache=None):
    P = _t(robe)
    sp = Spr(38, 30)
    if pose == "couche":
        body = sp.m_ell(16, 24, 11, 4)
        _blob(sp, body, P)
        sp.paint(sp.m_rect(24, 26, 33, 28), P["b"])
        hx, hy = 29, 20
    elif pose == "assis":
        sp.paint(sp.m_line([(9, 27), (4, 27)], 2), P["s"])
        body = sp.m_ell(15, 20, 7, 7.5)
        _blob(sp, body, P)
        sp.paint(sp.m_rect(19, 22, 21, 28), P["b"]); sp.paint(sp.m_rect(16, 25, 18, 28), P["s"])
        hx, hy = 22, 11
    else:
        sp.paint(sp.m_line([(6, 13), (3, 9), (4, 5)], 2), P["s"])
        _jambes(sp, [9, 12, 21, 24], 19, 28, 3, P, step)
        body = sp.m_ell(16, 15, 10, 5)
        _blob(sp, body, P)
        hx, hy = 28, 10
    head = sp.m_ell(hx, hy, 5, 4.6)
    _blob(sp, head, P)
    snout = sp.m_rect(hx + 3, hy, hx + 7, hy + 3)
    _blob(sp, snout, P)
    sp.paint(sp.m_ell(hx - 2, hy - 1, 2, 4.2), P["d"], newpart=False)
    if tache:
        sp.tone(sp.m_ell(13, 14, 4, 2.5) & body, tache)
    sp.px(hx + 2, hy - 2, (30, 30, 36)); sp.px(hx + 7, hy, (20, 20, 24))
    sp.pxs([(hx - 3, hy + 4), (hx - 2, hy + 5), (hx - 1, hy + 5)], (210, 40, 50))
    sp.outline()
    return sp, 24


def cheval(robe=(130, 80, 50), pose="debout", step=None, ane=False):
    P = _t(robe)
    M = _t((50, 40, 40)) if not ane else _t((90, 90, 96))
    sp = Spr(64, 60)
    sp.paint(sp.m_line([(12, 27), (8, 36), (7, 46)], 4), M["b"])                     # queue
    _jambes(sp, [16, 21, 37, 42], 36, 58, 3, P, step, sabot=(40, 34, 34))
    body = sp.m_ell(29, 30, 17, 9)
    _blob(sp, body, P)
    if pose == "mange":
        neck = sp.m_poly([(38, 24), (45, 26), (52, 48), (46, 50)])
        hx, hy = 52, 50
    else:
        neck = sp.m_poly([(37, 26), (44, 30), (51, 14), (45, 10)])
        hx, hy = 52, 13
    _blob(sp, neck, P)
    head = sp.m_ell(hx, hy, 6.5, 4.2)
    _blob(sp, head, P)
    sp.paint(sp.m_rect(hx + 3, hy - 1, hx + 8, hy + 3), P["s"], newpart=False)
    if pose == "mange":
        sp.paint(sp.m_line([(39, 24), (46, 44)], 2), M["b"], newpart=False)
    else:
        sp.paint(sp.m_line([(38, 25), (45, 10)], 2), M["b"], newpart=False)
    ear_h = 6 if ane else 3
    sp.paint(sp.m_poly([(hx - 4, hy - 3), (hx - 1, hy - 3), (hx - 3, hy - 3 - ear_h)]), P["b"], newpart=False)
    sp.px(hx + 1, hy - 1, (20, 18, 22)); sp.px(hx + 7, hy + 1, (40, 30, 30))
    sp.outline()
    return sp, 40


def vache(robe=(140, 96, 60), pose="debout", step=None, taches=None, pis=True):
    """Vache vue de profil (tournée vers la droite) : corps trapu, cornes claires, mufle clair, pis rose, queue à touffe."""
    P = _t(robe)
    sp = Spr(64, 56)
    sp.paint(sp.m_line([(12, 26), (9, 36), (9, 44)], 2), P["s"])
    sp.paint(sp.m_ell(9, 45, 2, 2.5), (60, 44, 34), newpart=False)
    _jambes(sp, [16, 21, 36, 41], 36, 53, 4, P, step, sabot=(50, 40, 36))
    body = sp.m_ell(28, 30, 18, 10)
    _blob(sp, body, P)
    if taches is not None:
        for (tx, ty, rx, ry) in ((22, 27, 5, 3), (33, 32, 4, 3), (28, 24, 3, 2), (16, 32, 3, 2)):
            sp.paint(sp.m_ell(tx, ty, rx, ry) & body, taches, newpart=False)
    if pis:
        sp.paint(sp.m_ell(30, 40, 4, 2.5), (226, 160, 160), newpart=False)
    if pose == "mange":
        neck = sp.m_poly([(40, 26), (46, 28), (50, 44), (44, 46)])
        hx, hy = 50, 46
    else:
        neck = sp.m_poly([(39, 24), (46, 27), (50, 22), (45, 18)])
        hx, hy = 51, 21
    _blob(sp, neck, P)
    _blob(sp, sp.m_ell(hx, hy, 5.5, 4.5), P)
    sp.paint(sp.m_ell(hx + 4, hy + 2, 3, 2.4), P["h"], newpart=False)
    corne = (236, 226, 200)
    sp.paint(sp.m_line([(hx - 2, hy - 4), (hx - 4, hy - 8)], 1), corne, newpart=False)
    sp.paint(sp.m_line([(hx + 1, hy - 4), (hx + 2, hy - 8)], 1), corne, newpart=False)
    sp.paint(sp.m_poly([(hx - 5, hy - 2), (hx - 9, hy - 1), (hx - 5, hy + 1)]), P["s"], newpart=False)
    sp.px(hx + 1, hy - 1, (20, 18, 22)); sp.px(hx + 6, hy + 2, (60, 40, 40))
    sp.outline()
    return sp, 40


def chameau(robe=(200, 160, 100), pose="debout", step=None):
    P = _t(robe)
    sp = Spr(68, 64)
    if pose == "couche":
        body = sp.m_ell(30, 52, 18, 8)
        _blob(sp, body, P)
        _blob(sp, sp.m_ell(28, 42, 8, 6), P)
        neck = sp.m_poly([(44, 50), (50, 52), (58, 36), (53, 33)])
        hx, hy = 59, 33
    else:
        _jambes(sp, [17, 22, 37, 42], 38, 62, 2, P, step, sabot=(120, 90, 60))
        body = sp.m_ell(30, 32, 17, 8)
        _blob(sp, body, P)
        _blob(sp, sp.m_ell(28, 22, 8, 6.5), P)
        if pose == "mange":
            neck = sp.m_poly([(42, 30), (48, 32), (56, 54), (50, 56)])
            hx, hy = 56, 56
        else:
            neck = sp.m_poly([(42, 30), (49, 33), (55, 16), (50, 12)])
            hx, hy = 57, 12
    _blob(sp, neck, P)
    head = sp.m_ell(hx, hy, 5.5, 3.4)
    _blob(sp, head, P)
    sp.paint(sp.m_rect(hx - 4, hy - 4, hx - 3, hy - 3), P["s"], newpart=False)
    sp.px(hx + 1, hy - 1, (20, 18, 22)); sp.px(hx + 5, hy + 1, (60, 40, 30))
    sp.paint(sp.m_line([(13, 30), (11, 38)], 2), P["s"], newpart=False)
    sp.outline()
    return sp, 44


def mouton(pose="debout", step=None):
    W_ = _t((240, 236, 226)); F = _t((60, 50, 52))
    sp = Spr(34, 24)
    _jambes(sp, [9, 12, 21, 24], 15, 23, 2, F, step)
    wool = sp.m_ell(15, 12, 11, 6)
    for (cx, cy) in ((8, 10), (12, 7), (17, 7), (22, 9), (9, 15), (21, 15)):
        wool |= sp.m_ell(cx, cy, 3.2, 3)
    _blob(sp, wool, W_)
    for (cx, cy) in ((10, 11), (15, 9), (19, 12), (13, 14)):
        sp.tone(sp.m_ell(cx, cy, 1.4, 1) & wool, W_["s"])
    hx, hy = (28, 16) if pose == "mange" else (27, 9)
    head = sp.m_ell(hx, hy, 3.6, 3)
    _blob(sp, head, F)
    sp.paint(sp.m_ell(hx - 2, hy - 1, 2, 1.2), F["s"], newpart=False)
    sp.px(hx + 1, hy - 1, (240, 240, 240))
    sp.outline()
    return sp, 22


def chevre(pose="debout", step=None):
    P = _t((236, 230, 220)); T = _t((150, 100, 60))
    sp = Spr(32, 28)
    _jambes(sp, [8, 11, 20, 23], 17, 27, 2, T, step)
    body = sp.m_ell(15, 14, 9, 5)
    _blob(sp, body, P)
    sp.tone(sp.m_ell(10, 15, 4, 3) & body, T["b"])
    hx, hy = (26, 22) if pose == "mange" else (25, 8)
    head = sp.m_ell(hx, hy, 3.6, 3.2)
    _blob(sp, head, P)
    sp.paint(sp.m_line([(hx - 1, hy - 3), (hx - 4, hy - 7)], 1), (120, 110, 100), newpart=False)
    sp.paint(sp.m_line([(hx + 2, hy + 2), (hx + 2, hy + 5)], 1), (190, 180, 170), newpart=False)
    sp.px(hx + 1, hy - 1, (30, 30, 30))
    sp.outline()
    return sp, 20


def pigeon(pose="debout", step=None):
    P = _t((150, 154, 170))
    sp = Spr(16, 14)
    if pose == "vole":
        up = step is not None and step % 2 == 0
        wing = sp.m_poly([(5, 6), (11, 6), (9, 0 if up else 12)])
        _blob(sp, wing, P)
    else:
        sp.paint(sp.m_rect(6, 11, 6, 13), (230, 120, 130)); sp.paint(sp.m_rect(9, 11, 9, 13), (230, 120, 130))
    body = sp.m_ell(8, 8, 5, 3.2)
    _blob(sp, body, P)
    sp.paint(sp.m_poly([(2, 7), (4, 7), (0, 10)]), P["s"], newpart=False)
    head = sp.m_ell(12, 5, 2.4, 2.2)
    _blob(sp, head, P)
    sp.pxs([(11, 7), (12, 7)], (90, 170, 130)); sp.px(10, 7, (150, 90, 170))
    sp.px(13, 4, (230, 100, 40)); sp.px(15, 5, (230, 190, 120)); sp.px(14, 5, (230, 190, 120))
    sp.outline()
    return sp, 9


ANIMAUX = dict(
    CHAT=lambda **k: chat((230, 140, 60), **k), CHAT_NOIR=lambda **k: chat((54, 50, 60), **k), CHAT_GRIS=lambda **k: chat((150, 150, 160), **k),
    CHIEN=lambda **k: chien((150, 100, 60), **k), CHIEN_NOIR=lambda **k: chien((60, 54, 58), **k),
    CHIEN_BLANC=lambda **k: chien((236, 232, 224), tache=(150, 100, 60), **k),
    CHEVAL=lambda **k: cheval((130, 80, 50), **k), CHEVAL_BLANC=lambda **k: cheval((232, 228, 222), **k),
    CHEVAL_NOIR=lambda **k: cheval((54, 48, 54), **k), ANE=lambda **k: cheval((150, 146, 150), ane=True, **k),
    CHAMEAU=lambda **k: chameau((200, 160, 100), **k), MOUTON=lambda **k: mouton(**k), CHEVRE=lambda **k: chevre(**k),
    PIGEON=lambda **k: pigeon(**k),
    VACHE=lambda **k: vache((140, 96, 60), **k), VACHE_NOIRE=lambda **k: vache((60, 54, 56), **k),
    VACHE_BLANCHE=lambda **k: vache((232, 228, 220), taches=(50, 44, 46), **k),
    VACHE_ROUSSE=lambda **k: vache((176, 100, 56), **k), VACHE_GRISE=lambda **k: vache((150, 146, 140), **k),
    VACHE_JAUNE=lambda **k: vache((240, 196, 56), **k))


def has(nom):
    return nom in ANIMAUX


def ane_rocher(pose="debout", step=None, **_):
    """L'âne qui porte le rocher des douze sources (2:60) : un bloc de pierre carré sanglé sur son dos."""
    sp, ombre = cheval((150, 146, 150), pose=pose, step=step, ane=True)
    roc = sp.m_poly([(20, 9), (36, 7), (40, 10), (40, 21), (23, 23), (18, 20), (18, 12)])
    sp.paint(roc, (150, 144, 136))
    sp.tone(roc & sp.m_rect(0, 0, 63, 11), (184, 178, 168))                     # le dessus, plus clair
    sp.tone(roc & sp.m_rect(36, 0, 63, 63), (118, 112, 106))                    # le flanc à l'ombre
    sp.paint(sp.m_line([(26, 13), (29, 17), (28, 20)], 1) & roc, (104, 98, 92), newpart=False)   # une fissure
    sangle = sp.m_line([(30, 21), (31, 38)], 1) & (sp.a[..., 3] > 0) & ~roc
    sp.paint(sangle, (96, 64, 40), newpart=False)
    o = roc.copy()
    e = o.copy()
    e[1:, :] |= o[:-1, :]; e[:-1, :] |= o[1:, :]; e[:, 1:] |= o[:, :-1]; e[:, :-1] |= o[:, 1:]
    sp.a[e & ~o] = (34, 22, 16, 255)
    return sp, ombre


class _Reduit:
    """Un jeune animal : le même dessin, réduit (pixels nets)."""
    def __init__(s, sp, f):
        from PIL import Image
        im = sp.img()
        w, h = max(1, round(im.width * f)), max(1, round(im.height * f))
        s._im = im.resize((w, h), Image.NEAREST)
        s.h = h

    def img(s):
        return s._im


def _jeune(fn, f=0.72):
    def g(pose="debout", step=None, **k):
        sp, ombre = fn(pose=pose, step=step, **k)
        return _Reduit(sp, f), int(ombre * f)
    return g


ANIMAUX.update(TAUREAU=lambda **k: vache((76, 56, 46), pis=False, **k), ANE_ROCHER=lambda **k: ane_rocher(**k), VACHE_JAUNE_TACHES=lambda **k: vache((240, 196, 56), taches=(250, 244, 226), **k),
               VEAU_JEUNE=_jeune(lambda **k: vache((196, 150, 104), **k)))


def image(nom, pose="debout", step=None, **_):
    sp, ombre = ANIMAUX[nom](pose=pose, step=step)
    im = sp.img()
    im.info["foot"] = sp.h
    im.info["ombre"] = ombre
    return im
