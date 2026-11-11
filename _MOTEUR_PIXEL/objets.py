# ICÔNES pixel art (16x16, contour sombre, ombre et reflet) pour les tableaux, les bulles de pensée et les écrans.
#   import objets ; sp = objets.icone("trophee") ; sp.img(5)  -> image PIL agrandie x5
#   objets.pensee("argent") -> bulle de pensée qui contient l'icône (comme duo.pensee)
# Liste complète : objets.ICONES (voir aussi la planche CATALOGUE/icones.png).
import math
import numpy as np
from spr import Spr, INK


def _dk(c, k=0.7):
    return tuple(int(v * k) for v in c)


def _lt(c, k=0.35):
    return tuple(int(v + (255 - v) * k) for v in c)


class Ic:
    def __init__(s, w=16, h=16):
        s.sp = Spr(w, h)

    def _p(s, m, col, shade=True):
        s.sp.paint(m, col)
        if shade:
            s.sp.shade(m, _dk(col, 0.72), dx=-1, dy=-1, depth=1)
            s.sp.light(m, _lt(col, 0.4), dx=1, dy=1, depth=1)
        return m

    def ell(s, cx, cy, rx, ry, col, shade=True):
        return s._p(s.sp.m_ell(cx, cy, rx, ry), col, shade)

    def rect(s, x0, y0, x1, y1, col, shade=True):
        return s._p(s.sp.m_rect(x0, y0, x1, y1), col, shade)

    def poly(s, pts, col, shade=True):
        return s._p(s.sp.m_poly(pts), col, shade)

    def line(s, pts, w, col):
        m = s.sp.m_line(pts, w)
        s.sp.paint(m, col)
        return m

    def px(s, pts, col):
        for x, y in pts:
            s.sp.px(x, y, col)

    def done(s, ol=True):
        if ol:
            s.sp.outline()
        return s.sp


GOLD, RED, GREEN, BLUE, WHITE, YEL = (238, 186, 60), (220, 50, 56), (70, 180, 90), (60, 130, 230), (248, 248, 250), (250, 210, 60)
DARK, GREY, PINK, ORANGE, BROWN, CYAN = (44, 44, 54), (150, 156, 170), (240, 140, 170), (240, 140, 50), (130, 86, 50), (90, 210, 240)


def _star(cx, cy, r1, r2, n=5, rot=-math.pi / 2):
    return [(cx + math.cos(rot + k * math.pi / n) * (r1 if k % 2 == 0 else r2),
             cy + math.sin(rot + k * math.pi / n) * (r1 if k % 2 == 0 else r2)) for k in range(2 * n)]


def _coeur(i, col):
    i.ell(5.2, 5.5, 3.4, 3.2, col, False); i.ell(10.8, 5.5, 3.4, 3.2, col, False)
    i.poly([(2, 6.5), (14, 6.5), (8, 13.8)], col, False)
    m = i.sp.a[..., 3] > 0
    i.sp.shade(m, _dk(col), dx=-1, dy=-1, depth=1)
    i.px([(4, 4), (5, 4), (4, 5)], _lt(col, 0.6))


def _icones():
    D = {}

    def reg(name):
        def deco(fn):
            D[name] = fn
            return fn
        return deco

    @reg("argent")
    def _():
        i = Ic(); i.rect(1, 4, 14, 11, (120, 196, 110)); i.rect(3, 6, 12, 9, (90, 166, 90), False)
        i.ell(7.5, 7.5, 1.6, 1.6, (200, 240, 190), False); i.px([(2, 5), (13, 10)], (200, 240, 190)); return i.done()

    @reg("pieces")
    def _():
        i = Ic()
        for y in (12, 9, 6):
            i.ell(8, y, 6, 2.4, GOLD); i.px([(6, y - 1), (7, y - 1)], _lt(GOLD, 0.6))
        return i.done()

    @reg("sac_argent")
    def _():
        i = Ic(); i.ell(8, 10, 6, 5, (214, 186, 130)); i.rect(6, 3, 9, 5, (214, 186, 130)); i.rect(5, 5, 10, 6, GOLD, False)
        i.px([(7, 8), (8, 8), (9, 8), (6, 9), (6, 10), (7, 10), (8, 10), (6, 11), (7, 12), (8, 12), (9, 12)], (110, 80, 40)); return i.done()

    @reg("telephone")
    def _():
        i = Ic(); i.rect(4, 1, 11, 14, DARK); i.rect(5, 3, 10, 11, (120, 190, 240), False)
        i.px([(7, 13), (8, 13)], GREY); i.px([(6, 4), (7, 4)], WHITE); i.ell(10, 3, 1.5, 1.5, RED, False); return i.done()

    @reg("coeur")
    def _():
        i = Ic(); _coeur(i, RED); return i.done()

    @reg("coeur_brise")
    def _():
        i = Ic(); _coeur(i, RED)
        i.px([(8, 3), (7, 5), (9, 7), (7, 9), (8, 11)], DARK); i.px([(8, 4), (8, 6), (8, 8), (8, 10)], DARK); return i.done()

    @reg("etoile")
    def _():
        i = Ic(); i.poly(_star(8, 8.4, 7.4, 3.2), YEL); return i.done()

    @reg("eclair")
    def _():
        i = Ic(); i.poly([(10, 0), (3, 9), (7.5, 9), (5, 15.5), (13, 5.5), (8.5, 5.5), (12, 0)], YEL); return i.done()

    @reg("feu")
    def _():
        i = Ic(); i.poly([(8, 0), (13, 7), (13, 11), (8, 15), (3, 11), (3, 7), (6, 4), (7, 7)], ORANGE)
        i.poly([(8, 6), (11, 10), (10, 13), (6, 13), (5, 10)], YEL, False); return i.done()

    @reg("ampoule")
    def _():
        i = Ic(); i.ell(8, 6, 5, 5, YEL); i.rect(6, 10, 9, 13, GREY); i.px([(6, 11), (9, 11), (6, 12), (9, 12)], _dk(GREY))
        i.px([(7, 14), (8, 14)], DARK); i.px([(6, 4), (6, 5), (7, 3)], WHITE); return i.done()

    @reg("horloge")
    def _():
        i = Ic(); i.ell(8, 8, 7, 7, RED); i.ell(8, 8, 5.2, 5.2, WHITE, False)
        i.px([(8, 4), (8, 5), (8, 6), (8, 7), (9, 8), (10, 9), (11, 9)], DARK); return i.done()

    @reg("sablier")
    def _():
        i = Ic(); i.rect(3, 0, 12, 1, BROWN); i.rect(3, 14, 12, 15, BROWN)
        i.poly([(4, 2), (11, 2), (8.5, 7.5), (8.5, 8.5), (11, 13), (4, 13), (6.5, 8.5), (6.5, 7.5)], (210, 236, 246))
        i.poly([(5.5, 3.5), (9.5, 3.5), (7.5, 7)], (240, 200, 100), False); i.poly([(5, 13), (10, 13), (7.5, 10)], (240, 200, 100), False)
        return i.done()

    @reg("calendrier")
    def _():
        i = Ic(); i.rect(1, 2, 14, 14, WHITE); i.rect(1, 2, 14, 5, RED, False)
        for x in (4, 11):
            i.rect(x, 0, x + 1, 3, GREY, False)
        for y in (8, 11):
            for x in (3, 6, 9, 12):
                i.px([(x, y)], GREY)
        i.px([(9, 11)], RED); return i.done()

    @reg("cadeau")
    def _():
        i = Ic(); i.rect(1, 6, 14, 14, RED); i.rect(0, 4, 15, 7, _lt(RED, 0.2)); i.rect(7, 4, 8, 14, YEL, False)
        i.ell(5, 2.5, 2.6, 1.8, YEL); i.ell(10.5, 2.5, 2.6, 1.8, YEL); return i.done()

    @reg("trophee")
    def _():
        i = Ic(); i.poly([(3, 1), (12, 1), (11, 6), (8.5, 9), (6.5, 9), (4, 6)], GOLD)
        i.line([(3, 2), (1, 3), (1, 5), (4, 7)], 1, GOLD); i.line([(12, 2), (14, 3), (14, 5), (11, 7)], 1, GOLD)
        i.rect(7, 9, 8, 11, _dk(GOLD, 0.85)); i.rect(4, 12, 11, 14, BROWN); i.px([(5, 2), (5, 3), (6, 4)], _lt(GOLD, 0.7)); return i.done()

    @reg("medaille")
    def _():
        i = Ic(); i.poly([(3, 0), (7, 0), (8, 7), (5, 7)], BLUE); i.poly([(12, 0), (8, 0), (7, 7), (10, 7)], RED)
        i.ell(7.5, 10.5, 4.6, 4.6, GOLD); i.poly(_star(7.5, 10.6, 2.6, 1.2), _lt(GOLD, 0.5), False); return i.done()

    @reg("couronne")
    def _():
        i = Ic(); i.poly([(1, 13), (14, 13), (15, 4), (11, 8), (7.5, 2), (4, 8), (0, 4)], GOLD)
        i.rect(1, 11, 14, 13, _dk(GOLD, 0.85), False); i.px([(4, 12), (11, 12)], RED); i.px([(7, 12), (8, 12)], BLUE); return i.done()

    @reg("diamant")
    def _():
        i = Ic(); i.poly([(4, 2), (11, 2), (15, 6), (7.5, 15), (0, 6)], CYAN)
        i.poly([(4, 2), (7.5, 6), (0, 6)], _lt(CYAN, 0.5), False); i.poly([(11, 2), (15, 6), (7.5, 6)], _dk(CYAN, 0.85), False)
        i.poly([(0, 6), (7.5, 6), (7.5, 15)], _lt(CYAN, 0.25), False); return i.done()

    @reg("cle")
    def _():
        i = Ic(); i._p(i.sp.m_ell(4.5, 4.5, 4, 4) & ~i.sp.m_ell(4.5, 4.5, 1.7, 1.7), GOLD)
        i.line([(7, 7), (14, 14)], 2, GOLD); i.px([(11, 13), (12, 12), (13, 11), (10, 12)], _dk(GOLD)); return i.done()

    @reg("cadenas")
    def _():
        i = Ic(); m = i.sp.m_ell(8, 6, 5, 5) & ~i.sp.m_ell(8, 6, 3, 3) & i.sp.m_rect(0, 0, 15, 7)
        i.sp.paint(m, GREY); i.rect(2, 7, 13, 15, GOLD); i.rect(7, 10, 8, 12, DARK, False); return i.done()

    @reg("loupe")
    def _():
        i = Ic(); i.line([(10, 10), (14, 14)], 3, BROWN); i.ell(6.5, 6.5, 5.6, 5.6, GREY); i.ell(6.5, 6.5, 4, 4, (190, 230, 250), False)
        i.px([(5, 4), (4, 5)], WHITE); return i.done()

    @reg("cerveau")
    def _():
        i = Ic(); i.ell(5.5, 7.5, 4.8, 5.4, PINK); i.ell(10.5, 7.5, 4.8, 5.4, PINK)
        i.px([(8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11)], _dk(PINK, 0.7))
        i.px([(4, 5), (5, 6), (3, 8), (4, 9), (11, 5), (12, 6), (10, 9), (11, 10), (5, 11), (12, 11)], _dk(PINK, 0.78)); return i.done()

    @reg("livre")
    def _():
        i = Ic(); i.rect(2, 1, 13, 14, (170, 40, 56)); i.rect(12, 2, 13, 14, (244, 238, 220), False)
        i.rect(4, 4, 10, 5, GOLD, False); i.rect(4, 7, 9, 7, GOLD, False); return i.done()

    @reg("ordinateur")
    def _():
        i = Ic(); i.rect(2, 2, 13, 10, DARK); i.rect(3, 3, 12, 9, (90, 170, 240), False)
        i.poly([(0, 11), (15, 11), (14, 14), (1, 14)], GREY); i.px([(4, 4), (5, 4), (4, 5)], WHITE); return i.done()

    @reg("manette")
    def _():
        i = Ic(); i.poly([(2, 5), (13, 5), (15, 12), (12, 13), (10, 10), (5, 10), (3, 13), (0, 12)], DARK)
        i.px([(4, 7), (3, 8), (4, 8), (5, 8), (4, 9)], GREY); i.px([(11, 7)], RED); i.px([(12, 8)], GREEN); i.px([(10, 8)], BLUE); return i.done()

    @reg("micro")
    def _():
        i = Ic(); i.ell(8, 4.5, 4, 4.4, GREY); i.rect(6, 8, 9, 13, DARK); i.rect(5, 8, 10, 9, RED, False)
        i.px([(6, 2), (6, 3)], WHITE); i.rect(5, 14, 10, 15, DARK); return i.done()

    @reg("maison")
    def _():
        i = Ic(); i.rect(3, 7, 12, 14, (240, 230, 210)); i.poly([(0, 8), (15, 8), (7.5, 0)], RED)
        i.rect(6, 10, 9, 14, BROWN, False); i.rect(10, 9, 11, 10, (120, 190, 240), False); return i.done()

    @reg("voiture")
    def _():
        i = Ic(); i.poly([(0, 11), (15, 11), (15, 8), (12, 7), (10, 4), (4, 4), (2, 7), (0, 8)], RED)
        i.poly([(4.5, 5), (7, 5), (7, 7), (3.5, 7)], (170, 220, 250), False); i.poly([(8, 5), (9.5, 5), (11, 7), (8, 7)], (170, 220, 250), False)
        i.ell(4, 12, 2, 2, DARK); i.ell(12, 12, 2, 2, DARK); return i.done()

    @reg("avion")
    def _():
        i = Ic(); i.poly([(0, 8), (2, 6), (14, 6), (15, 7.5), (14, 9), (2, 9)], WHITE)
        i.poly([(6, 7), (10, 7), (6, 14), (4, 14)], GREY); i.poly([(6, 7), (10, 7), (6, 1), (4, 1)], GREY)
        i.poly([(0, 7), (2, 7), (1, 3), (0, 3)], RED); i.px([(11, 7), (12, 7)], BLUE); return i.done()

    @reg("fusee")
    def _():
        i = Ic(); i.poly([(8, 0), (11, 4), (11, 11), (5, 11), (5, 4)], WHITE); i.ell(8, 6, 1.6, 1.6, BLUE, False)
        i.poly([(5, 8), (2, 12), (5, 12)], RED); i.poly([(11, 8), (14, 12), (11, 12)], RED)
        i.poly([(6, 12), (10, 12), (8, 15.5)], ORANGE); i.px([(8, 13)], YEL); return i.done()

    @reg("globe")
    def _():
        i = Ic(); i.ell(8, 8, 7, 7, BLUE); i.poly([(3, 4), (7, 3), (8, 6), (5, 9), (3, 7)], GREEN, False)
        i.poly([(9, 8), (13, 7), (13, 11), (10, 13)], GREEN, False); i.px([(5, 3), (4, 4)], _lt(BLUE, 0.6)); return i.done()

    @reg("soleil")
    def _():
        i = Ic()
        for k in range(8):
            a = k * math.pi / 4
            i.line([(8 + math.cos(a) * 5, 8 + math.sin(a) * 5), (8 + math.cos(a) * 7.4, 8 + math.sin(a) * 7.4)], 1, ORANGE)
        i.ell(8, 8, 4.2, 4.2, YEL); return i.done()

    @reg("lune")
    def _():
        i = Ic(); m = i.sp.m_ell(8, 8, 6.6, 6.6) & ~i.sp.m_ell(11, 6, 5.4, 5.4)
        i.sp.paint(m, (250, 236, 170)); i.sp.shade(m, (210, 190, 120), dx=-1, dy=-1, depth=1); return i.done()

    @reg("nuage")
    def _():
        i = Ic(); m = i.sp.m_ell(5, 9, 4, 3.5) | i.sp.m_ell(9, 7, 4.6, 4.6) | i.sp.m_ell(12, 10, 3.4, 3) | i.sp.m_rect(4, 10, 13, 12)
        i.sp.paint(m, WHITE); i.sp.shade(m, (200, 210, 226), dx=-1, dy=-1, depth=1); return i.done()

    @reg("pluie")
    def _():
        i = Ic(); m = i.sp.m_ell(5, 6, 4, 3.5) | i.sp.m_ell(9, 4.5, 4.6, 4) | i.sp.m_ell(12, 7, 3.4, 3) | i.sp.m_rect(4, 7, 13, 9)
        i.sp.paint(m, (190, 200, 216)); i.sp.shade(m, (150, 160, 180), dx=-1, dy=-1, depth=1)
        for x in (4, 8, 12):
            i.px([(x, 11), (x - 1, 13)], BLUE)
        return i.done()

    @reg("burger")
    def _():
        i = Ic(); m = i.sp.m_ell(8, 6, 7, 4.6) & i.sp.m_rect(0, 0, 15, 6); i.sp.paint(m, (230, 160, 70)); i.sp.shade(m, (190, 120, 50), -1, -1, 1)
        i.rect(1, 7, 14, 7, GREEN, False); i.rect(1, 8, 14, 9, (120, 60, 40), False); i.rect(1, 10, 14, 10, YEL, False)
        i.rect(1, 11, 14, 13, (230, 160, 70)); i.px([(5, 3), (8, 2), (11, 3)], (250, 236, 200)); return i.done()

    @reg("pizza")
    def _():
        i = Ic(); i.poly([(1, 2), (14, 2), (7.5, 15)], (240, 200, 110)); i.rect(1, 1, 14, 3, (200, 140, 60))
        for x, y in ((5, 5), (9, 6), (7, 9)):
            i.ell(x, y, 1.4, 1.4, RED, False)
        return i.done()

    @reg("cafe")
    def _():
        i = Ic(); i.rect(2, 5, 11, 14, WHITE); i.rect(3, 5, 10, 6, (120, 70, 40), False)
        m = i.sp.m_ell(12, 9, 3, 3) & ~i.sp.m_ell(12, 9, 1.4, 1.4) & i.sp.m_rect(12, 0, 15, 15); i.sp.paint(m, WHITE)
        i.px([(5, 3), (6, 2), (8, 3), (9, 1)], (210, 210, 220)); return i.done()

    @reg("pomme")
    def _():
        i = Ic(); i.ell(6, 9, 4.6, 5, RED); i.ell(10, 9, 4.6, 5, RED); i.line([(8, 4), (9, 1)], 1, BROWN)
        i.ell(11, 2.5, 2.4, 1.4, GREEN); i.px([(4, 7), (4, 8)], _lt(RED, 0.6)); return i.done()

    @reg("pilule")
    def _():
        i = Ic(); m1 = i.sp.m_line([(3, 12), (8, 7)], 6); m2 = i.sp.m_line([(8, 7), (12, 3)], 6)
        i.sp.paint(m1, RED); i.sp.paint(m2 & ~m1, WHITE); i.sp.shade(m1 | m2, (150, 150, 170), -1, -1, 1); return i.done()

    @reg("thermometre")
    def _():
        i = Ic(); i.rect(6, 0, 9, 11, WHITE); i.ell(7.5, 12.5, 3, 3, RED); i.rect(7, 4, 8, 11, RED, False)
        for y in (2, 4, 6, 8):
            i.px([(10, y)], GREY)
        return i.done()

    @reg("check")
    def _():
        i = Ic(); i.ell(8, 8, 7.4, 7.4, GREEN); i.line([(4, 8), (7, 11), (12, 4)], 2, WHITE); return i.done()

    @reg("croix")
    def _():
        i = Ic(); i.ell(8, 8, 7.4, 7.4, RED); i.line([(5, 5), (11, 11)], 2, WHITE); i.line([(11, 5), (5, 11)], 2, WHITE); return i.done()

    @reg("interdit")
    def _():
        i = Ic(); m = i.sp.m_ell(8, 8, 7.4, 7.4) & ~i.sp.m_ell(8, 8, 5.2, 5.2); i.sp.paint(m, RED)
        i.line([(4, 4), (12, 12)], 2, RED); i.sp.shade(i.sp.a[..., 3] > 0, _dk(RED), -1, -1, 1); return i.done()

    @reg("alerte")
    def _():
        i = Ic(); i.poly([(8, 0), (15.5, 14), (0.5, 14)], YEL); i.rect(7, 4, 8, 9, DARK, False); i.rect(7, 11, 8, 12, DARK, False); return i.done()

    @reg("question")
    def _():
        i = Ic(); i.ell(8, 8, 7.4, 7.4, BLUE)
        i.px([(6, 4), (7, 3), (8, 3), (9, 3), (10, 4), (10, 5), (9, 6), (8, 7), (8, 8), (8, 11), (7, 11), (7, 8), (7, 7)], WHITE); return i.done()

    @reg("exclamation")
    def _():
        i = Ic(); i.ell(8, 8, 7.4, 7.4, RED); i.rect(7, 3, 8, 9, WHITE, False); i.rect(7, 11, 8, 12, WHITE, False); return i.done()

    @reg("fleche_haut")
    def _():
        i = Ic(); i.poly([(8, 0), (15, 8), (11, 8), (11, 15), (5, 15), (5, 8), (1, 8)], GREEN); return i.done()

    @reg("fleche_bas")
    def _():
        i = Ic(); i.poly([(8, 15), (15, 7), (11, 7), (11, 0), (5, 0), (5, 7), (1, 7)], RED); return i.done()

    @reg("graphique")
    def _():
        i = Ic(); i.rect(0, 0, 15, 15, WHITE); i.rect(2, 10, 4, 13, BLUE, False); i.rect(6, 7, 8, 13, BLUE, False); i.rect(10, 4, 12, 13, BLUE, False)
        i.line([(2, 8), (6, 5), (9, 6), (13, 2)], 1, GREEN); return i.done()

    @reg("pouce")
    def _():
        i = Ic(); i.rect(1, 7, 4, 14, BLUE); i.poly([(5, 7), (8, 1), (10, 2), (9, 6), (14, 6), (15, 9), (13, 14), (5, 14)], (240, 196, 150)); return i.done()

    @reg("pouce_bas")
    def _():
        i = Ic(); i.rect(1, 1, 4, 8, RED); i.poly([(5, 8), (8, 14), (10, 13), (9, 9), (14, 9), (15, 6), (13, 1), (5, 1)], (240, 196, 150)); return i.done()

    @reg("mail")
    def _():
        i = Ic(); i.rect(0, 3, 15, 13, WHITE); i.line([(0, 3), (7.5, 9), (15, 3)], 1, (180, 186, 200)); i.ell(13, 3, 2.4, 2.4, RED, False); return i.done()

    @reg("bulle")
    def _():
        i = Ic(); i.poly([(1, 1), (14, 1), (14, 10), (7, 10), (3, 14), (4, 10), (1, 10)], WHITE)
        for x in (4, 7, 10):
            i.px([(x, 5), (x + 1, 5)], GREY)
        return i.done()

    @reg("wifi")
    def _():
        i = Ic()
        for r, c in ((7, BLUE), (4.6, BLUE), (2.2, BLUE)):
            m = i.sp.m_ell(8, 13, r + 0.9, r + 0.9) & ~i.sp.m_ell(8, 13, r - 0.6, r - 0.6) & i.sp.m_rect(0, 0, 15, 12)
            m &= np.abs(np.mgrid[0:16, 0:16][1] - 8) <= (13 - np.mgrid[0:16, 0:16][0]) * 1.1
            i.sp.paint(m, c)
        i.ell(8, 13, 1.2, 1.2, BLUE, False); return i.done()

    @reg("batterie")
    def _():
        i = Ic(); i.rect(0, 4, 13, 11, WHITE); i.rect(14, 6, 15, 9, GREY, False); i.rect(2, 6, 4, 9, RED, False); return i.done()

    @reg("cible")
    def _():
        i = Ic()
        for r, c in ((7.4, RED), (5.4, WHITE), (3.4, RED), (1.6, WHITE)):
            i.ell(8, 8, r, r, c, r > 7)
        return i.done()

    @reg("balance")
    def _():
        i = Ic(); i.rect(7, 2, 8, 13, GOLD); i.rect(1, 3, 14, 3, GOLD); i.rect(4, 14, 11, 15, GOLD)
        for x in (3, 12):
            i.line([(x, 4), (x - 2, 9)], 1, GOLD); i.line([(x, 4), (x + 2, 9)], 1, GOLD)
            m = i.sp.m_ell(x, 9, 3, 1.6) & i.sp.m_rect(0, 9, 15, 15); i.sp.paint(m, GOLD)
        return i.done()

    @reg("marteau")
    def _():
        i = Ic(); i.line([(4, 13), (10, 7)], 2, BROWN); i.poly([(8, 1), (15, 8), (12, 11), (5, 4)], (150, 100, 60))
        i.rect(1, 13, 8, 15, (110, 70, 40)); return i.done()

    @reg("atome")
    def _():
        i = Ic()
        for a in (0, math.pi / 3, -math.pi / 3):
            for k in range(36):
                t = k / 36 * 2 * math.pi
                x, y = 6.8 * math.cos(t), 2.6 * math.sin(t)
                i.px([(round(8 + x * math.cos(a) - y * math.sin(a)), round(8 + x * math.sin(a) + y * math.cos(a)))], BLUE)
        i.ell(8, 8, 1.8, 1.8, RED, False); return i.done(ol=False)

    @reg("adn")
    def _():
        i = Ic()
        for y in range(16):
            x1 = 8 + 4.5 * math.sin(y / 15 * 2 * math.pi); x2 = 8 - 4.5 * math.sin(y / 15 * 2 * math.pi)
            i.px([(round(x1), y)], BLUE); i.px([(round(x2), y)], RED)
            if y % 3 == 0:
                for x in range(min(round(x1), round(x2)) + 1, max(round(x1), round(x2))):
                    i.px([(x, y)], GREY)
        return i.done(ol=False)

    @reg("fiole")
    def _():
        i = Ic(); i.rect(6, 0, 9, 5, (220, 240, 248)); i.poly([(6, 5), (9, 5), (14, 14), (1, 14)], (220, 240, 248))
        i.poly([(4.5, 9), (10.5, 9), (14, 14), (1, 14)], (120, 220, 120), False); i.px([(6, 11), (9, 12)], (200, 255, 200)); return i.done()

    @reg("crane")
    def _():
        i = Ic(); i.ell(8, 6.5, 6.4, 6, (240, 236, 226)); i.rect(5, 11, 10, 14, (240, 236, 226))
        i.ell(5.5, 7, 1.8, 1.8, DARK, False); i.ell(10.5, 7, 1.8, 1.8, DARK, False); i.px([(8, 9), (7, 10), (8, 10)], DARK)
        i.px([(6, 13), (8, 13), (10, 13)], (160, 156, 146)); return i.done()

    @reg("oeil")
    def _():
        i = Ic(); m = i.sp.m_ell(8, 8, 7.4, 4.4); i.sp.paint(m, WHITE); i.ell(8, 8, 3.4, 3.4, (80, 140, 90), False)
        i.ell(8, 8, 1.6, 1.6, DARK, False); i.px([(7, 6)], WHITE); return i.done()

    @reg("fantome")
    def _():
        i = Ic(); i.poly([(2, 15), (2, 6), (5, 1), (11, 1), (14, 6), (14, 15), (11.5, 13), (8, 15), (4.5, 13)], WHITE)
        i.ell(6, 7, 1.4, 2, DARK, False); i.ell(10, 7, 1.4, 2, DARK, False); return i.done()

    @reg("carte")
    def _():
        i = Ic(); i.poly([(0, 2), (5, 0), (10, 2), (15, 0), (15, 13), (10, 15), (5, 13), (0, 15)], (236, 220, 170))
        i.line([(2, 12), (5, 8), (8, 9), (12, 4)], 1, RED); i.px([(12, 3), (11, 4), (13, 4), (12, 5)], RED); return i.done()

    @reg("boussole")
    def _():
        i = Ic(); i.ell(8, 8, 7.4, 7.4, GOLD); i.ell(8, 8, 5.6, 5.6, WHITE, False)
        i.poly([(8, 3), (9.5, 8), (6.5, 8)], RED, False); i.poly([(8, 13), (9.5, 8), (6.5, 8)], DARK, False); return i.done()

    @reg("epee")
    def _():
        i = Ic(); i.line([(3, 12), (13, 2)], 2, (214, 220, 232)); i.line([(2, 10), (6, 14)], 2, GOLD); i.line([(1, 14), (3, 12)], 2, BROWN); return i.done()

    @reg("bouclier")
    def _():
        i = Ic(); i.poly([(1, 1), (14, 1), (14, 7), (7.5, 15), (1, 7)], BLUE)
        i.poly(_star(7.5, 6.8, 4.6, 2.0), GOLD, False); return i.done()

    @reg("drapeau")
    def _():
        i = Ic(); i.rect(1, 0, 2, 15, GREY)
        m = i.sp.m_rect(3, 1, 14, 9); i.sp.paint(m, WHITE)
        yy, xx = np.mgrid[0:16, 0:16]
        i.sp.tone(m & ((((xx - 3) // 3) + ((yy - 1) // 3)) % 2 == 0), DARK); return i.done()

    @reg("parchemin")
    def _():
        i = Ic(); i.rect(2, 2, 13, 13, (236, 220, 176)); i.rect(1, 1, 3, 14, (200, 176, 130)); i.rect(12, 1, 14, 14, (200, 176, 130))
        for y in (5, 8, 11):
            i.px([(x, y) for x in range(5, 11)], (150, 120, 90))
        return i.done()

    @reg("bougie")
    def _():
        i = Ic(); i.rect(5, 6, 10, 15, (240, 236, 220)); i.ell(7.5, 3, 1.8, 3, ORANGE, False); i.px([(7, 3), (8, 3)], YEL); return i.done()

    @reg("euro")
    def _():
        i = Ic(); i.ell(8, 8, 7.4, 7.4, GOLD)
        i.px([(10, 4), (9, 4), (8, 4), (7, 5), (6, 6), (6, 7), (6, 8), (6, 9), (7, 10), (8, 11), (9, 11), (10, 11),
              (4, 7), (5, 7), (7, 7), (8, 7), (4, 9), (5, 9), (7, 9), (8, 9)], (130, 90, 20)); return i.done()

    @reg("cigarette_interdite")
    def _():
        i = Ic(); i.rect(2, 7, 12, 9, WHITE); i.rect(10, 7, 12, 9, ORANGE, False)
        m = i.sp.m_ell(8, 8, 7.4, 7.4) & ~i.sp.m_ell(8, 8, 5.6, 5.6); i.sp.paint(m, RED); i.line([(3, 3), (13, 13)], 2, RED); return i.done()

    return D


ICONES = _icones()


def icone(nom):
    if nom in ICONES:
        return ICONES[nom]()
    import duo
    if nom in duo.ICONS2:
        return duo.icone2(nom)
    return duo.icone(nom)


def pensee(nom="ampoule", scale_icon=1):
    """Bulle de pensée blanche contenant une icône."""
    ic = icone(nom)
    w, h = ic.w + 8, ic.h + 6
    sp = Spr(w + 2, h + 9)
    sp.paint(sp.m_ell((w + 1) / 2, h / 2 + 0.5, w / 2, h / 2), (252, 252, 252))
    sp.paint(sp.m_ell(5, h + 2.0, 1.8, 1.5), (252, 252, 252), newpart=False)
    sp.paint(sp.m_ell(2.5, h + 5.4, 1.1, 1.1), (252, 252, 252), newpart=False)
    m = ic.a[..., 3] > 0
    sp.a[3:3 + ic.h, 5:5 + ic.w][m] = ic.a[m]
    sp.outline()
    return sp
