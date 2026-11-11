# DÉMONSTRATION EN IMAGE DU 07/11/2026 — Short duo ISL20 « Tu rentres chez toi ? Dis ça » (Bismillah en rentrant,
# Mouslim 2018). Même principe que explique_0411b.py : le sens propre du hadith, montré en grand, avec des mouvements
# doux (jamais de secousse, de flash ni de clignotement).
#   {porte} / {porte PETIT}   accroche, vue à ta place, la nuit : TA porte d'entrée (lanterne, paillasson) ; ta main
#                             tourne la clé dans la serrure (u -0.4 → 0.1), pousse la porte qui s'ouvre VERS L'INTÉRIEUR
#                             sur un couloir chaud et éclairé (personne dedans) ; au-dessus de la porte, une petite
#                             enseigne d'hôtel « CHAMBRE LIBRE » (verte) s'allume lentement : on se demande pourquoi.
#   {maison}                  la façade de la maison la nuit (toit, 2 fenêtres, porte au centre), une enseigne d'hôtel
#                             éteinte sur le toit, la lune ;
#   {maison entre}            la porte s'illumine, « BISMILLAH » (« = AU NOM D'ALLAH ») au-dessus ;
#   {maison mange}            une fenêtre s'allume sur la table (assiette), « BISMILLAH » près de l'assiette ;
#   {maison pas}              l'enseigne (deux tubes de néon, un par ligne) s'allume en rouge « PAS DE CHAMBRE / PAS DE
#                             DÎNER » ; dessous, du texte seulement : « LE CHAYTAN, AUX SIENS : » « NI NUIT NI DÎNER
#                             POUR VOUS ! » ;
#   {maison libre}            (il entre sans citer Allah) SEUL le « BISMILLAH = AU NOM D'ALLAH » de la porte s'efface
#                             et la porte s'éteint ; la fenêtre du repas reste allumée avec son BISMILLAH ; sur
#                             l'enseigne, la 1re ligne passe au vert « CHAMBRE LIBRE » (pulsation lente de 1,2 s), la
#                             2e reste rouge « PAS DE DÎNER » : « VOUS AVEZ TROUVÉ OÙ PASSER LA NUIT ! ». Sur un plan
#                             neuf (« libre » sans les étapes d'avant) : cet état final directement.
# Le Chaytan n'est jamais dessiné ni suggéré (ni cornes, ni yeux dans le noir, ni ombre, ni fumée) : seulement du texte.
# Branché par explique_0611.py (CLES, ordre, fin_anim), comme explique_0411b.
import math

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

import cast
import pxv
from px import Px, TAHOMA
from pxv import smooth
from explique import _titre, _fade, _erode, autocollant, BLANC, JAUNE
from explique_0411b import _Base, OR_
from explique_0411 import OL, _peau

LAITON, LAITON_O, LAITON_C = (226, 182, 72), (170, 128, 40), (255, 232, 150)
NEON = {  # (cœur du tube, tube, lueur)
    "vert": ((206, 255, 212), (60, 222, 112), (70, 255, 130)),
    "rouge": ((255, 214, 204), (238, 58, 58), (255, 60, 54)),
}
TUBE_ETEINT = ((52, 56, 68), (38, 40, 52))
CHAUD = (255, 200, 120)


# ---------------------------------------------------------------- petits outils
def _dilate(m, n=1):
    e = m.copy()
    for _ in range(n):
        e = e | np.roll(e, 1, 0) | np.roll(e, -1, 0) | np.roll(e, 1, 1) | np.roll(e, -1, 1)
    return e


def _texte_px(W, H, lignes, size):
    """Masque (H x W) de lignes de texte en police pixel nette (Tahoma gras, sans lissage) :
    lignes = [(texte, x du milieu, y de la ligne de base)] en pixels du dessin."""
    f = ImageFont.truetype(TAHOMA, size)
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    for (txt, cx, yb) in lignes:
        d.text((cx, yb), txt, font=f, fill=255, anchor="ms")
    return np.array(im) > 127


def _neon(c, m, coul):
    """Lettres de néon sur un dessin Px : cœur clair, tube coloré autour (1 pixel)."""
    coeur, tube = coul[0], coul[1]
    c.fill(_dilate(m) & ~m, tube)
    c.fill(m, coeur)


def _lueur(m, K, col, flou, gain=1.0, marge=0):
    """Lueur douce (écran) autour d'un masque du dessin : renvoie (image RGBA, (x, y)) recadrée sur la lueur."""
    ys, xs = np.where(m)
    if not len(xs):
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0)), (0, 0)
    pad = int(flou * 3 / K) + 2 + marge
    x0, x1 = max(0, xs.min() - pad), min(m.shape[1], xs.max() + 1 + pad)
    y0, y1 = max(0, ys.min() - pad), min(m.shape[0], ys.max() + 1 + pad)
    sous = Image.fromarray((m[y0:y1, x0:x1] * 255).astype(np.uint8), "L")
    sous = sous.resize((sous.width * K, sous.height * K), Image.NEAREST).filter(ImageFilter.GaussianBlur(flou))
    a = (np.array(sous).astype(np.float32) * gain).clip(0, 255).astype(np.uint8)
    out = np.zeros((a.shape[0], a.shape[1], 4), np.uint8)
    out[..., :3] = col
    out[..., 3] = a
    return Image.fromarray(out, "RGBA"), (x0 * K, y0 * K)


def _borne(g, pos, y_coupe, dessus, fondu):
    """Lueur g (posée en pos, pixels d'écran) gardée d'un seul côté de la ligne y_coupe (au-dessus si dessus) : de
    l'autre côté, elle s'éteint en douceur sur « fondu » pixels (chaque ligne de l'enseigne garde ainsi sa couleur)."""
    a = np.array(g)
    ys = np.arange(a.shape[0], dtype=np.float32) + pos[1]
    au_dela = (ys - y_coupe) if dessus else (y_coupe - ys)
    w = np.clip(1 - au_dela / fondu, 0, 1)
    a[..., 3] = (a[..., 3].astype(np.float32) * w[:, None]).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def _homographie(src, dst):
    """Coefficients PIL (Image.PERSPECTIVE) qui envoient chaque point de l'image de sortie (dst) sur la texture (src)."""
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        b.append(v)
    return tuple(np.linalg.solve(np.array(A, float), np.array(b, float)))


def _teinte(col, k):
    return tuple(int(max(0, min(255, v * k))) for v in col)


# ---------------------------------------------------------------- {porte} {maison …}
class Maison(_Base):
    """{porte} : accroche, vue à ta place, la nuit : ta main tourne la clé, la porte s'ouvre vers l'intérieur sur un
    couloir chaud ; au-dessus, une petite enseigne d'hôtel « CHAMBRE LIBRE » s'allume doucement.
    {maison} : la façade de nuit, enseigne éteinte sur le toit ; {maison entre|mange|pas|libre} (Mouslim 2018)."""
    ETAPES = ("entre", "mange", "pas", "libre")
    # -- l'accroche : une vraie perspective (point de fuite au milieu de la porte, à hauteur des yeux)
    CX, YH, F = 85.0, 50.0, 120.0           # point de fuite, focale (pixels du dessin)
    X0, X1, Y0, Y1 = 57, 113, 30, 128       # l'ouverture de la porte (plan de la porte, z = 0)
    TW = 8                                  # épaisseur du mur : la façade est à z = -TW
    PL = (56, 98)                           # le dessin de la porte (à plat)
    SERR = (50, 57)                         # le trou de la serrure dans ce dessin
    COUL = (37, 133, 22, 160)               # le couloir : mur gauche, mur droit, plafond, profondeur
    ANG = 80                                # ouverture finale de la porte (degrés)
    T_CLE = (-0.4, 0.1)                     # la clé tourne
    T_PORTE = (0.12, 1.3)                   # la porte s'ouvre
    T_LACHE = (0.5, 1.05)                   # la main lâche la porte et repart
    T_ENS = (0.7, 1.7)                      # l'enseigne s'allume (fondu lent, 1 s)
    S_MAIN = 1.0                            # taille de la main
    ROT = 80                                # la clé tourne de tant de degrés
    # -- la façade (hôtel)
    PORTE_H = (73, 98, 97, 136)             # la porte de la façade : x0, y0, x1, y1
    FEN_G = (22, 96, 54, 124)
    FEN_D = (116, 96, 148, 124)
    ENS = (29, 2, 141, 36)                  # l'enseigne sur le toit
    Y_COUPE = 17                            # ses deux tubes (un par ligne) : en haut jusqu'à 15, en bas dès 18

    def __init__(s, cmd, mode="hotel", who="PETIT"):
        super().__init__(cmd)
        s.mode = mode
        s.who = who if who in cast.CAST else "PETIT"
        s.negatif = mode == "porte"

    def sons_el(s):
        if s.mode == "porte":
            return [(0.02, "dv_clic", 0.03, None), (0.2, "dv_porte_bois", 0.03, None)]
        out = []
        d_libre = 0.1 if s._neuf() else 0.25                      # le clic quand « CHAMBRE LIBRE » s'allume
        for nom, son, dec in (("entre", "sa_ting", 0.0), ("pas", "dv_clic", 0.0), ("libre", "dv_clic", d_libre)):
            if nom in s.t:
                out.append((s.t[nom] + dec, son, 0.03, None))
        return out

    def image(s, u):
        return s._image_porte(u) if s.mode == "porte" else s._image_hotel(u)

    # ================================================================ l'accroche : TA porte
    def _pj(s, x, y, z):
        k = s.F / (s.F + z)
        return (s.CX + (x - s.CX) * k, s.YH + (y - s.YH) * k)

    def _couloir(s, c):
        """Le couloir chaud et éclairé derrière la porte (perspective à un point de fuite). Personne dedans."""
        P = s._pj
        xa, xb, yc, D = s.COUL
        ys = s.Y1
        quad = c.mask_poly
        c.fill(quad([P(xa, yc, 0), P(xb, yc, 0), P(xb, yc, D), P(xa, yc, D)]), (246, 224, 178))      # plafond
        for x_, col, lam in ((xa, (234, 192, 132), (208, 152, 98)), (xb, (220, 178, 120), (196, 140, 90))):
            c.fill(quad([P(x_, yc, 0), P(x_, ys, 0), P(x_, ys, D), P(x_, yc, D)]), col)            # les murs
            c.fill(quad([P(x_, 98, 0), P(x_, ys, 0), P(x_, ys, D), P(x_, 98, D)]), lam)            # lambris
            c.line(*P(x_, 98, 0), *P(x_, 98, D), (240, 214, 168))
            c.fill(quad([P(x_, 124, 0), P(x_, ys, 0), P(x_, ys, D), P(x_, 124, D)]), (232, 206, 164))
        sol = quad([P(xa, ys, 0), P(xb, ys, 0), P(xb, ys, D), P(xa, ys, D)])
        c.fill(sol, (182, 112, 64))                                                                # le parquet
        xs_ = list(range(xa, xb + 1, 8))
        for i, x in enumerate(xs_):
            c.line(*P(x, ys, 0), *P(x, ys, D), (150, 88, 50))
            if i + 1 < len(xs_):
                for z in range((i * 17) % 40, D, 44):                                              # bouts des lames
                    c.line(*P(x, ys, z), *P(xs_[i + 1], ys, z), (150, 88, 50))
        tapis = quad([P(68, ys, 6), P(102, ys, 6), P(102, ys, 140), P(68, ys, 140)])               # le tapis
        c.fill(tapis, (178, 56, 50))
        c.dither(tapis, (150, 42, 44), 0.25)
        c.fill(tapis & ~_erode(tapis, 1), (236, 186, 92))
        fx0, fy0 = P(xa, yc, D)
        fx1, fy1 = P(xb, ys, D)
        c.fill(c.mask_rect(fx0, fy0, fx1 + 1, fy1), (240, 210, 156))                                # le mur du fond
        _, ylam = P(xa, 98, D)
        c.fill(c.mask_rect(fx0, ylam, fx1 + 1, fy1), (210, 156, 100))
        c.fill(c.mask_rect(fx0, ylam, fx1 + 1, ylam + 1), (252, 232, 190))
        cadre = c.mask_rect(*P(74, 50, D), *P(97, 69, D))                                           # un tableau
        c.shape(cadre, (226, 178, 76), shade=(176, 128, 48), band=1, olcol=OL)
        ix0, iy0 = P(76, 52, D)
        ix1, iy1 = P(95, 67, D)
        c.fill(c.mask_rect(ix0, iy0, ix1, iy1), (160, 210, 236))
        c.fill(c.mask_rect(ix0, iy0 + 4, ix1, iy1), (98, 170, 98))
        c.px(ix1 - 2, iy0 + 1, (255, 230, 120))
        tx0, ty0 = P(70, 100, D)                                                                   # la console
        tx1, ty1 = P(100, 103, D)
        c.fill(c.mask_rect(tx0, ty0, tx1, ty1 + 1), (150, 96, 56))
        for xl in (72, 97):
            c.line(*P(xl, 103, D), *P(xl, 128, D), (120, 74, 42))
        lx, ly = P(85, 92, D)                                                                       # sa lampe
        c.fill(c.mask_poly([(lx - 3, ly), (lx + 3, ly), (lx + 2, ly - 3), (lx - 2, ly - 3)]), (255, 236, 170))
        c.fill(c.mask_rect(lx - 0.5, ly, lx + 1, ty0), (120, 74, 42))
        c.glow(lx, ly - 1, 9, (255, 236, 170), k=0.45)
        cx_, cy_ = P(85, yc, 70)                                                                    # la suspension
        bx_, by_ = P(85, 31, 70)
        c.glow(bx_, by_ + 3, 22, (255, 236, 180), k=0.35)
        c.line(cx_, cy_, bx_, by_, (150, 112, 80))
        c.fill(c.mask_poly([(bx_ - 4, by_ + 3), (bx_ + 4, by_ + 3), (bx_ + 2, by_), (bx_ - 2, by_)]), (255, 240, 190))
        c.px(*P(xa + 2, 80, 30), (250, 246, 236))                                                   # interrupteur

    def _fond_porte(s):
        """Le palier la nuit (façade, lanterne, encadrement, seuil, paillasson, enseigne éteinte) + le couloir
        derrière l'ouverture ; renvoie un dict : fond (image d'écran), lit (lettres allumées), gl1 / gl2 (lueurs de
        l'enseigne), spill (la lumière du couloir sur le palier), chacun avec sa position."""
        if "fp" in s._cache:
            return s._cache["fp"]
        W, H, K = s.PW_, s.PH_, s.K
        P = s._pj
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        ex0, ey0 = P(s.X0, s.Y0, -s.TW)
        ex1, ey1 = P(s.X1, s.Y1, -s.TW)
        mur = tout_ & c.mask_rect(0, 0, W, ey1)
        c.rgrad(mur, 34, 42, 110, (176, 150, 136), (66, 68, 104), steps=7)                          # éclairé par la lanterne
        for y in range(10, int(ey1), 21):                                                          # crépi : petits joints
            c.fill(mur & c.mask_rect(0, y, W, y + 1) & ~c.mask_rect(46, 0, 124, H), (78, 78, 112))
        sol = tout_ & c.mask_rect(0, ey1, W, H)                                                    # dalles du palier
        c.fill(sol, (70, 68, 92))
        for z in (-12, -18, -26):
            _, yz = P(0, s.Y1, z)
            c.fill(sol & c.mask_rect(0, yz, W, yz + 1), (54, 52, 74))
        for xw in range(-31, 205, 16):
            c.line(*P(xw, s.Y1, -s.TW), *P(xw, s.Y1, -34), (54, 52, 74))
        tap = c.mask_poly([P(60, s.Y1, -10), P(110, s.Y1, -10), P(112, s.Y1, -40), P(58, s.Y1, -40)])  # paillasson
        c.shape(tap, (150, 112, 68), shade=(112, 80, 48), light=(178, 140, 92), band=1, olcol=OL)
        c.dither(_erode(tap, 2), (128, 92, 56), 0.35)
        c.fill(tap & ~_erode(tap, 2), (96, 66, 42))
        # l'encadrement (pierre claire) et l'épaisseur du mur
        enc = c.mask_rect(ex0 - 5, ey0 - 5, ex1 + 5, ey1) & ~c.mask_rect(ex0, ey0, ex1, ey1)
        c.shape(enc, (150, 146, 168), shade=(112, 108, 132), light=(186, 182, 202), band=1, olcol=OL)
        c.fill(c.mask_rect(ex0, ey0, s.X0, ey1), (52, 50, 76))                                    # tableau gauche (ombre)
        c.fill(c.mask_rect(s.X1, ey0, ex1, ey1), (126, 114, 124))                                 # tableau droit (éclairé)
        c.fill(c.mask_rect(ex0, ey0, ex1, s.Y0), (46, 44, 68))                                    # le haut
        seuil = c.mask_poly([P(s.X0, s.Y1, 0), P(s.X1, s.Y1, 0), P(s.X1, s.Y1, -s.TW), P(s.X0, s.Y1, -s.TW)])
        c.fill(seuil, (138, 134, 150))
        c.fill(seuil & c.mask_rect(0, ey1 - 1, W, ey1), (176, 172, 188))
        # la lanterne, à gauche de la porte
        lx, ly = 34, 44
        c.fill(c.mask_rect(lx - 1, ly - 12, lx + 6, ly - 10), (30, 28, 36))                        # la potence
        c.fill(c.mask_rect(lx + 5, ly - 14, lx + 8, ly - 4), (30, 28, 36))
        toit = c.mask_poly([(lx - 6, ly - 7), (lx + 6, ly - 7), (lx + 3, ly - 11), (lx - 3, ly - 11)])
        c.shape(toit, (40, 38, 48), light=(70, 68, 80), band=1, olcol=OL)
        vitre = c.mask_rect(lx - 4, ly - 7, lx + 5, ly + 5)
        c.shape(vitre, (255, 214, 120), shade=(240, 170, 80), light=(255, 246, 200), band=1, olcol=OL)
        c.fill(c.mask_rect(lx - 1, ly - 5, lx + 2, ly + 3), (255, 248, 214))
        c.fill(c.mask_rect(lx - 5, ly + 5, lx + 6, ly + 7), (40, 38, 48))
        c.fill(c.mask_rect(lx, ly - 7, lx + 1, ly + 5), (40, 38, 48))
        c.glow(lx, ly - 1, 30, (255, 210, 140), k=0.35)
        # la sonnette
        c.shape(c.mask_rect(ex1 + 8, 74, ex1 + 12, 80), (196, 196, 206), band=1, olcol=OL)
        c.fill(c.mask_rect(ex1 + 9, 76, ex1 + 11, 78), (232, 210, 120))
        # l'enseigne d'hôtel, au-dessus de la porte (éteinte : on devine les tubes)
        bx0, by0, bx1, by1 = 33, 5, 137, 22
        for xp in (44, 126):                                                                      # pattes de fixation
            c.fill(c.mask_rect(xp, by1, xp + 2, ey0 - 5), (36, 34, 44))
        board = c.mask_rrect(bx0, by0, bx1, by1, 2)
        c.shape(board, (104, 108, 126), shade=(70, 72, 88), light=(150, 154, 172), band=1, olcol=OL)
        c.fill(c.mask_rect(bx0 + 2, by0 + 2, bx1 - 2, by1 - 2), (24, 26, 36))
        m_txt = _texte_px(W, H, [("CHAMBRE LIBRE", (bx0 + bx1) / 2, by0 + 13)], 11)
        _neon(c, m_txt, TUBE_ETEINT)
        # le couloir, derrière l'ouverture
        co = Px(W, H, alpha=True)
        s._couloir(co)
        ouv = co.mask_rect(s.X0, s.Y0, s.X1, s.Y1)
        co.al &= ouv
        c.al &= ~ouv
        fond = co.img(K, rgba=True)
        fond.alpha_composite(c.img(K, rgba=True))
        # les lueurs (calculées une fois) : la lanterne, l'enseigne allumée, la lumière du couloir sur le palier
        lay = Image.new("RGBA", fond.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse([lx * K - 150, (ly - 1) * K - 130, lx * K + 150, (ly - 1) * K + 130],
                                    fill=(255, 200, 120, 70))
        fond.alpha_composite(lay.filter(ImageFilter.GaussianBlur(40)))
        lit = Px(W, H, alpha=True)
        _neon(lit, m_txt, NEON["vert"])
        lit_im = lit.img(K, rgba=True)
        bb = (int(bx0 * K), int(by0 * K), int(bx1 * K), int(by1 * K))
        lit_im = lit_im.crop(bb)
        gl1, p1 = _lueur(_dilate(m_txt), K, NEON["vert"][2], 9, 1.3)
        gl2, p2 = _lueur(c.mask_rect(bx0, by0, bx1, by1), K, NEON["vert"][2], 34, 0.42, marge=6)
        lay = Image.new("RGBA", fond.size, (0, 0, 0, 0))                                          # la lumière du couloir
        ld = ImageDraw.Draw(lay)
        ld.polygon([(s.X0 * K, s.Y1 * K), (s.X1 * K, s.Y1 * K), (150 * K, H * K + 40), (40 * K, H * K + 40)],
                   fill=(*CHAUD, 120))
        ld.rectangle([s.X0 * K - 30, s.Y0 * K - 20, s.X1 * K + 30, s.Y1 * K], fill=(*CHAUD, 40))
        spill = lay.filter(ImageFilter.GaussianBlur(26))
        sb = spill.getbbox() or (0, 0, 1, 1)
        s._cache["fp"] = dict(fond=fond, lit=(lit_im, bb[:2]), gl1=(gl1, p1), gl2=(gl2, p2),
                              spill=(spill.crop(sb), sb[:2]))
        return s._cache["fp"]

    def _porte_tex(s):
        """Ta porte à plat (56 x 98) : bois, six panneaux, plaque en laiton, poignée, serrure."""
        if "ptex" in s._cache:
            return s._cache["ptex"]
        W, H = s.PL
        c = Px(W, H, alpha=True)
        p = c.mask_rect(0, 0, W, H)
        c.vgrad(p, 0, H, (146, 88, 56), (104, 60, 40), steps=5)                   # la lanterne éclaire le haut
        for x in range(3, W, 5):
            c.dither(p & c.mask_rect(x, 0, x + 1, H), (118, 70, 46), 0.3)        # le fil du bois
        for (x0, x1) in ((7, 25), (31, 49)):
            for (y0, y1) in ((8, 28), (34, 62), (68, 91)):
                pan = c.mask_rect(x0, y0, x1, y1)
                c.fill(pan, (112, 64, 42))
                c.fill(pan & c.mask_rect(x0, y0, x1, y0 + 1), (78, 42, 28))
                c.fill(pan & c.mask_rect(x0, y0, x0 + 1, y1), (78, 42, 28))
                c.fill(pan & c.mask_rect(x0, y1 - 1, x1, y1), (164, 106, 70))
                c.fill(pan & c.mask_rect(x1 - 1, y0, x1, y1), (150, 96, 64))
                inn = c.mask_rect(x0 + 3, y0 + 3, x1 - 3, y1 - 3)
                c.fill(inn, (130, 78, 50))
                c.fill(inn & c.mask_rect(x0 + 3, y0 + 3, x1 - 3, y0 + 4), (160, 104, 68))
        c.outline(p, OL)
        c.fill(c.mask_rect(0, 0, 1, H), OL)
        c.fill(c.mask_rect(W - 1, 0, W, H), OL)
        sx, sy = s.SERR
        plaque = c.mask_rrect(sx - 3, sy - 13, sx + 4, sy + 5, 2)                  # la plaque en laiton
        c.shape(plaque, LAITON, shade=LAITON_O, light=LAITON_C, band=1, olcol=OL)
        poig = c.mask_rect(sx - 9, sy - 9, sx + 2, sy - 6)                         # la poignée
        c.shape(poig, LAITON, shade=LAITON_O, light=LAITON_C, band=1, olcol=OL)
        c.fill(c.mask_ell(sx + 0.5, sy - 7.5, 2.2, 2.2), LAITON_O)
        c.fill(c.mask_rect(sx, sy - 1, sx + 1, sy + 3) | c.mask_ell(sx + 0.5, sy - 0.5, 1.2, 1.2), (30, 22, 20))
        for (yh) in (12, 84):                                                      # les gonds
            c.fill(c.mask_rect(0, yh, 2, yh + 5), (60, 56, 64))
        s._cache["ptex"] = c.img(1, rgba=True)
        return s._cache["ptex"]

    def _ang(s, u):
        a, b = s.T_PORTE
        return s.ANG * smooth((u - a) / (b - a))

    def _porte_ouverte(s, im, ang):
        """Pose la porte tournée de ang degrés autour de ses gonds (à gauche), vers l'intérieur (elle s'éloigne)."""
        K = s.K
        W_, H_ = s.PL
        th = math.radians(ang)
        xf, zf = s.X0 + W_ * math.cos(th), W_ * math.sin(th)
        q = [s._pj(s.X0, s.Y0, 0), s._pj(xf, s.Y0, zf), s._pj(xf, s.Y1, zf), s._pj(s.X0, s.Y1, 0)]
        q = [(x * K, y * K) for (x, y) in q]
        x0 = int(math.floor(min(x for x, _ in q)))
        x1 = int(math.ceil(max(x for x, _ in q)))
        y0 = int(math.floor(min(y for _, y in q)))
        y1 = int(math.ceil(max(y for _, y in q)))
        if x1 - x0 < 2:
            return
        co = _homographie([(0, 0), (W_, 0), (W_, H_), (0, H_)], [(x - x0, y - y0) for (x, y) in q])
        pan = s._porte_tex().transform((x1 - x0, y1 - y0), Image.PERSPECTIVE, co, Image.NEAREST)
        if ang > 0.5:                                                               # elle tourne le dos à la lanterne
            a = np.array(pan)
            a[..., :3] = (a[..., :3].astype(np.float32) * (1 - 0.28 * math.sin(th))).astype(np.uint8)
            pan = Image.fromarray(a, "RGBA")
        im.alpha_composite(pan, (x0, y0))

    def _main(s, c, P, ang, S):
        """Ta main droite, vue de derrière (comme la tienne) : le poing tient la clé et tourne de ang degrés (sens des
        aiguilles d'une montre) autour du trou de la serrure P ; l'avant-bras, plus près de toi, arrive du bas à droite
        et ne tourne pas. S = échelle. Couleurs du perso (peau, manche)."""
        px_, py_ = P
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))

        def R(x, y):
            x, y = x * S, y * S
            return (px_ + x * ca - y * sa, py_ + x * sa + y * ca)

        def ell(cx, cy, rx, ry, n=22):
            return [R(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]

        def poly(pts):
            return c.mask_poly([R(*q) for q in pts])
        p = _peau(s.who)
        b, s_, h = p["b"], p["s"], p["h"]
        # la clé : l'anneau de la clé (laiton) et son col, qui dépassent entre le pouce et l'index
        col_ = poly([(-11.2, -18.0), (-6.8, -18.0), (-6.8, -10.0), (-11.2, -10.0)])
        c.shape(col_, LAITON, shade=LAITON_O, light=LAITON_C, band=1, olcol=OL)
        tete = c.mask_poly(ell(-9.0, -22.6, 5.6, 5.4))
        c.shape(tete, LAITON, shade=LAITON_O, light=LAITON_C, band=1, olcol=OL)
        c.fill(poly([(-10.3, -25.6), (-7.7, -25.6), (-7.7, -23.0), (-10.3, -23.0)]), (40, 28, 26))   # le trou
        c.fill(poly([(-12.6, -22.0), (-11.4, -22.0), (-11.4, -19.6), (-12.6, -19.6)]) & tete, LAITON_C)  # reflet
        # le dos de la main
        dos = poly([(-12, -5), (11, -4), (12.5, 2), (9, 9), (-5, 10.5), (-11.5, 5)])
        c.shape(dos, b, shade=s_, light=h, band=2, olcol=OL)
        # les doigts repliés : on voit leurs premières phalanges, de dos, avec les jointures
        for (x0, x1, y0) in ((-12, -6, -11.5), (-6, 0, -12.6), (0, 6, -11.8), (6, 11.2, -9.8)):
            doigt = poly([(x0, -3), (x0, y0 + 2), (x0 + 1.5, y0), (x1 - 1.5, y0), (x1, y0 + 2), (x1, -3)])
            c.shape(doigt, b, shade=s_, light=h, band=1, olcol=OL)
            c.fill(poly([(x0 + 1.5, y0 + 1), (x1 - 2, y0 + 1), (x1 - 2, y0 + 2.2), (x0 + 1.5, y0 + 2.2)]) & doigt, h)
        # le pouce, sur le côté, qui pince la clé (l'ongle au bout)
        pouce = poly([(-11, 6), (-14.8, 1), (-15.6, -5), (-13.8, -10.6), (-11, -12.2), (-9.6, -9.4), (-10.8, -4),
                      (-8.6, 2)])
        c.shape(pouce, b, shade=s_, light=h, band=1, olcol=OL)
        c.fill(poly([(-13.6, -10.2), (-11.2, -11.6), (-10.4, -9.6), (-12.6, -8.4)]) & pouce, (246, 214, 200))
        # l'avant-bras (la manche) : plus près de toi, il cache le poignet ; il ne tourne pas
        col = cast.CAST[s.who].get("couleur", (200, 50, 50))
        sh, li = _teinte(col, 0.72), tuple(min(255, int(v * 1.12 + 26)) for v in col)
        cx_, cy_ = px_ + 4.0 * S, py_ + 9.5 * S
        ox, oy = cx_ + 46, cy_ + 92
        L = math.hypot(ox - cx_, oy - cy_)
        dx, dy = (ox - cx_) / L, (oy - cy_) / L
        nx, ny = -dy, dx
        w1, w2 = 9.5 * S, 40
        n_ = 16
        arc = [(cx_ + nx * w1 * math.cos(math.pi * i / n_) - dx * w1 * 0.55 * math.sin(math.pi * i / n_),
                cy_ + ny * w1 * math.cos(math.pi * i / n_) - dy * w1 * 0.55 * math.sin(math.pi * i / n_))
               for i in range(n_ + 1)]
        bras = c.mask_poly([(cx_ + nx * w1, cy_ + ny * w1), (ox + nx * w2, oy + ny * w2), (ox - nx * w2, oy - ny * w2),
                            (cx_ - nx * w1, cy_ - ny * w1)]) | c.mask_poly(arc)
        c.shape(bras, col, shade=sh, light=li, band=2, olcol=OL)

        def bande(f0, f1):
            return c.mask_poly([(cx_ + nx * w1 + dx * f0 * S, cy_ + ny * w1 + dy * f0 * S),
                                (cx_ - nx * w1 + dx * f0 * S, cy_ - ny * w1 + dy * f0 * S),
                                (cx_ - nx * w1 + dx * f1 * S, cy_ - ny * w1 + dy * f1 * S),
                                (cx_ + nx * w1 + dx * f1 * S, cy_ + ny * w1 + dy * f1 * S)])
        c.fill((c.mask_poly(arc) | bande(0, 6)) & _erode(bras, 1), _teinte(col, 0.86))   # le bord-côte du poignet
        for j in range(-3, 4):
            xa_, ya_ = cx_ + nx * j * 2.5 * S, cy_ + ny * j * 2.5 * S
            c.line(xa_ - dx * 2 * S, ya_ - dy * 2 * S, xa_ + dx * 5.4 * S, ya_ + dy * 5.4 * S, sh)
        c.fill(bande(6, 7) & bras, sh)
        for (f0, f1, o) in ((14, 30, 0.45), (30, 52, -0.25)):                       # deux plis du tissu
            c.line(cx_ + nx * w1 * o + dx * f0, cy_ + ny * w1 * o + dy * f0,
                   cx_ + nx * (w1 + 6) * o + dx * f1, cy_ + ny * (w1 + 6) * o + dy * f1, sh)

    def _image_porte(s, u):
        K = s.K
        fp = s._fond_porte()
        im = fp["fond"].copy()
        W_, H_ = im.size
        ang = s._ang(u)
        o = ang / s.ANG
        if o > 0.01:                                                                # la lumière du couloir sort
            sp, pos = fp["spill"]
            im.alpha_composite(_fade(sp, smooth(o * 1.4)), pos)
        s._porte_ouverte(im, ang)
        # l'enseigne : un fondu lent, sans clignoter
        ae = smooth((u - s.T_ENS[0]) / (s.T_ENS[1] - s.T_ENS[0]))
        if ae > 0.01:
            for cle in ("gl2", "gl1"):
                g, pos = fp[cle]
                im.alpha_composite(_fade(g, ae), pos)
            l_, pos = fp["lit"]
            im.alpha_composite(_fade(l_, ae), pos)
        # ta main : elle tourne la clé, pousse la porte, puis lâche et repart vers toi
        t0, t1 = s.T_CLE
        rot = s.ROT * smooth((u - t0) / (t1 - t0))
        la, lb = s.T_LACHE
        S0 = s.S_MAIN
        sx, sy = s.SERR
        if u < la:
            th = math.radians(ang)
            zl = sx * math.sin(th)
            P = s._pj(s.X0 + sx * math.cos(th), s.Y0 + sy, zl)
            S = S0 * s.F / (s.F + zl)
            if u < t0:                                                              # avant : elle enfonce la clé
                e_in = 1 - smooth((u - t0 + 0.6) / 0.6)
                P = (P[0] + 5 * e_in, P[1] + 7 * e_in)
                S *= 1 + 0.08 * e_in
        else:
            th = math.radians(s._ang(la))
            zl = sx * math.sin(th)
            P0 = s._pj(s.X0 + sx * math.cos(th), s.Y0 + sy, zl)
            S1 = S0 * s.F / (s.F + zl)
            r = smooth((u - la) / (lb - la))
            P = (P0[0] + 62 * r, P0[1] + 84 * r)
            S = S1 * (1 + 0.3 * r)
            rot = s.ROT - 30 * r
        if u < lb:                                  # dessinée au pixel du dessin, posée au pixel d'écran (glisse douce)
            ix, iy = math.floor(P[0]), math.floor(P[1])
            c = Px(s.PW_, s.PH_, alpha=True)
            s._main(c, (ix, iy), rot, S)
            im.alpha_composite(c.img(K, rgba=True), (int(round((P[0] - ix) * K)), int(round((P[1] - iy) * K))))
        # on avance doucement vers la porte
        z = 1.0 + 0.05 * smooth((u - 0.3) / 3.2)
        if z > 1.001:
            w2, h2 = W_ / z, H_ / z
            x0, y0 = (W_ - w2) / 2, (H_ - h2) * 0.42
            im = im.resize((W_, H_), Image.BILINEAR, box=(x0, y0, x0 + w2, y0 + h2))
        return s._coins(im)

    def _coins(s, im):
        """Coins arrondis (comme les autres schémas) : rien ne déborde, même la manche ou le zoom."""
        m = s._cache.get("coins")
        if m is None:
            m = Image.new("L", im.size, 0)
            ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 6 * s.K, fill=255)
            s._cache["coins"] = m
        im.putalpha(ImageChops.multiply(im.getchannel("A"), m))
        return im

    # ================================================================ la façade (hôtel)
    def _labc(s, txt, col, size):
        """Étiquette recadrée sur son encre (pour la placer au pixel près)."""
        cle = ("labc", txt, col, size)
        if cle not in s._cache:
            im = _titre(txt, col, size)
            s._cache[cle] = im.crop(im.getbbox())
        return s._cache[cle]

    def _citation(s, l1, l2):
        """Citation sur deux lignes serrées (jaune), recadrée sur son encre."""
        cle = ("cit", l1, l2)
        if cle not in s._cache:
            im = autocollant(pxv.big_title([(l1, JAUNE), (l2, JAUNE)], size=50), r=3, ombre=False)
            s._cache[cle] = im.crop(im.getbbox())
        return s._cache[cle]

    def _ciel(s):
        if "ciel" in s._cache:
            return s._cache["ciel"]
        W, H, K = s.PW_, s.PH_, s.K
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        c.vgrad(tout_, 0, 136, (14, 16, 46), (52, 44, 96), steps=7)
        mx, my = 156, 52                                                            # la lune (un croissant)
        c.glow(mx, my, 18, (150, 150, 210), k=0.3)
        c.fill(c.mask_ell(mx, my, 7, 7) & ~c.mask_ell(mx + 3.5, my - 2.5, 6.2, 6.2), (246, 238, 206))
        rng = np.random.default_rng(20)
        etoiles = []
        ex0, ey0, ex1, ey1 = s.ENS
        while len(etoiles) < 24:
            x, y = int(rng.integers(3, W - 3)), int(rng.integers(3, 66))
            if ex0 - 4 <= x <= ex1 + 4 and y <= ey1 + 6:                            # pas sur l'enseigne
                continue
            if abs(x - mx) < 12 and abs(y - my) < 12:
                continue
            if any(abs(x - a) + abs(y - b) < 10 for (a, b) in etoiles):               # jamais deux points serrés
                continue
            etoiles.append((x, y))
            c.px(x, y, (232, 232, 255) if rng.random() < 0.7 else (180, 186, 230))
        s._cache["ciel"] = c.img(K, rgba=True)
        s._cache["etoiles"] = etoiles
        return s._cache["ciel"]

    def _nuage(s, j):
        cle = ("nuage", j)
        if cle not in s._cache:
            w, h = (34, 10) if j == 0 else (26, 8)
            c = Px(w, h, alpha=True)
            m = c.mask_ell(w * 0.3, h * 0.62, w * 0.3, h * 0.38) | c.mask_ell(w * 0.58, h * 0.45, w * 0.3, h * 0.45) | \
                c.mask_ell(w * 0.8, h * 0.66, w * 0.2, h * 0.34)
            c.fill(m, (66, 68, 114))
            c.fill(m & ~np.roll(m, 1, 0), (104, 106, 150))
            c.fill(m & ~np.roll(m, -1, 0), (52, 52, 92))
            s._cache[cle] = c.img(s.K, rgba=True)
        return s._cache[cle]

    def _cadre_ens(s, c):
        ex0, ey0, ex1, ey1 = s.ENS
        return c.mask_rect(ex0 + 3, ey0 + 3, ex1 - 3, ey1 - 3) & ~c.mask_rect(ex0 + 4, ey0 + 4, ex1 - 4, ey1 - 4)

    def _tubes(s, c):
        """Le cadre de l'enseigne en deux tubes de néon, un par ligne (en haut ∩, en bas ∪, séparés de 2 pixels sur les
        côtés, entre les deux lignes) : chaque ligne peut avoir sa couleur."""
        cadre = s._cadre_ens(c)
        return cadre & c.mask_rect(0, 0, c.w, s.Y_COUPE - 1), cadre & c.mask_rect(0, s.Y_COUPE + 1, c.w, c.h)

    def _neuf(s):
        """« libre » arrive sur un élément neuf (nouveau plan) : aucune des étapes d'avant n'y a eu lieu."""
        return "libre" in s.t and not any(k in s.t for k in ("entre", "mange", "pas"))

    def _acquis(s, nom, u, d, dec=0.0):
        """Comme _e ; mais une étape absente alors que « libre » est là est déjà acquise (l'état final : le repas béni,
        PAS DE DÎNER) : tout de suite si « libre » ouvre le plan (le moteur fait déjà entrer l'élément en fondu), sinon
        en fondu à « libre »."""
        if nom not in s.t and "libre" in s.t:
            return 1.0 if s.t["libre"] <= 0.05 else s._e("libre", u, d, dec)
        return s._e(nom, u, d, dec)

    def _maison(s):
        """La maison (calque sans le ciel) : toit, enseigne éteinte sur ses poteaux, murs, porte, deux fenêtres."""
        if "mai" in s._cache:
            return s._cache["mai"]
        W, H, K = s.PW_, s.PH_, s.K
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        # le sol : herbe de nuit, allée en pierres
        sol = tout_ & c.mask_rect(0, 134, W, H)
        c.fill(sol, (36, 64, 58))
        c.dither(sol, (46, 80, 66), 0.3)
        allee = c.mask_poly([(68, 138), (102, 138), (112, 150), (58, 150)])
        c.fill(allee, (96, 92, 112))
        for y in (141, 145):
            c.fill(allee & c.mask_rect(0, y, W, y + 1), (72, 70, 90))
        # l'enseigne d'hôtel sur le toit (éteinte), sur deux poteaux
        ex0, ey0, ex1, ey1 = s.ENS
        for xp in (50, 117):
            c.shape(c.mask_rect(xp, ey1 - 1, xp + 3, 42), (60, 60, 72), light=(90, 90, 104), band=1, olcol=OL)
        board = c.mask_rrect(ex0, ey0, ex1, ey1, 3)
        c.shape(board, (98, 102, 122), shade=(66, 68, 86), light=(144, 148, 168), band=1, olcol=OL)
        c.fill(c.mask_rect(ex0 + 2, ey0 + 2, ex1 - 2, ey1 - 2), (22, 24, 34))
        t_haut, t_bas = s._tubes(c)
        c.fill(t_haut | t_bas, TUBE_ETEINT[1])
        # le toit (tuiles, de nuit)
        toit = c.mask_poly([(46, 40), (124, 40), (164, 66), (6, 66)])
        c.fill(toit, (112, 58, 60))
        for y in range(42, 66, 4):
            c.fill(toit & c.mask_rect(0, y, W, y + 1), (84, 42, 48))
            dec = 0 if (y // 4) % 2 else 3
            for x in range(dec, W, 6):
                c.fill(toit & c.mask_rect(x, y + 1, x + 1, y + 4), (92, 46, 52))
            c.fill(toit & c.mask_rect(0, y + 1, W, y + 2), (132, 76, 76))
        c.outline(toit, OL)
        c.fill(c.mask_rect(46, 39, 124, 41), (70, 40, 46))
        # les murs
        murs = tout_ & c.mask_rect(14, 66, 156, 136)
        c.shape(murs, (118, 108, 136), shade=(92, 86, 114), light=(138, 128, 156), band=2, olcol=OL)
        c.dither(murs & c.mask_rect(14, 70, 156, 136), (108, 100, 128), 0.12)
        c.fill(c.mask_rect(14, 66, 156, 70), (62, 46, 56))                                       # sous le toit
        c.fill(c.mask_rect(6, 66, 164, 68), (54, 36, 44))
        base = c.mask_rect(14, 131, 156, 136)
        c.fill(base, (86, 80, 104))
        c.fill(base & c.mask_rect(0, 131, W, 132), (104, 98, 122))
        # la porte (bois sombre, petite vitre en haut), son encadrement, la marche
        x0, y0, x1, y1 = s.PORTE_H
        enc = c.mask_rect(x0 - 3, y0 - 3, x1 + 3, y1) & ~c.mask_rect(x0, y0, x1, y1)
        c.shape(enc, (166, 160, 180), shade=(126, 120, 142), light=(196, 190, 210), band=1, olcol=OL)
        porte = c.mask_rect(x0, y0, x1, y1)
        c.shape(porte, (104, 62, 46), shade=(78, 44, 34), light=(132, 84, 60), band=1, olcol=OL)
        for (py0, py1) in ((y0 + 15, y0 + 26), (y0 + 29, y1 - 3)):
            pan = c.mask_rect(x0 + 4, py0, x1 - 4, py1)
            c.fill(pan, (92, 54, 40))
            c.fill(pan & c.mask_rect(0, py0, W, py0 + 1), (70, 38, 30))
            c.fill(pan & c.mask_rect(0, py1 - 1, W, py1), (126, 80, 58))
        c.shape(c.mask_rect(*s._vitre_porte()), (30, 36, 70), light=(52, 60, 104), band=1, olcol=OL)
        c.fill(c.mask_rect(x1 - 5, y0 + 23, x1 - 2, y0 + 25), LAITON)
        marche = c.mask_rect(x0 - 7, y1, x1 + 7, y1 + 3)
        c.shape(marche, (124, 120, 138), shade=(96, 92, 110), light=(156, 152, 170), band=1, olcol=OL)
        # les deux fenêtres (éteintes) : rideaux à gauche, la salle à manger à droite
        for (fx0, fy0, fx1, fy1), gauche in ((s.FEN_G, True), (s.FEN_D, False)):
            lin = c.mask_rect(fx0 - 2, fy0 - 3, fx1 + 2, fy0)
            c.shape(lin, (150, 144, 164), shade=(118, 112, 134), band=1, olcol=OL)
            cad = c.mask_rect(fx0, fy0, fx1, fy1)
            c.shape(cad, (196, 192, 206), shade=(150, 146, 166), band=1, olcol=OL)
            vit = c.mask_rect(fx0 + 2, fy0 + 2, fx1 - 2, fy1 - 2)
            c.vgrad(vit, fy0, fy1, (26, 30, 66), (40, 46, 92), steps=4)
            for k_ in range(6):                                                    # reflet de la lune
                c.fill(vit & c.mask_rect(fx0 + 6 + k_, fy0 + 14 - 2 * k_, fx0 + 8 + k_, fy0 + 16 - 2 * k_),
                       (58, 66, 118))
            if gauche:
                for (rx0, rx1) in ((fx0 + 2, fx0 + 8), (fx1 - 8, fx1 - 2)):
                    rid = c.mask_rect(rx0, fy0 + 2, rx1, fy1 - 2)
                    c.shape(rid, (104, 70, 120), shade=(80, 52, 96), light=(128, 92, 144), band=1, ol=False)
            c.fill(c.mask_rect((fx0 + fx1) // 2 - 1, fy0 + 2, (fx0 + fx1) // 2 + 1, fy1 - 2), (196, 192, 206))
            c.fill(c.mask_rect(fx0 + 2, (fy0 + fy1) // 2 - 1, fx1 - 2, (fy0 + fy1) // 2), (196, 192, 206))
            app = c.mask_rect(fx0 - 2, fy1, fx1 + 2, fy1 + 2)
            c.shape(app, (150, 144, 164), shade=(118, 112, 134), band=1, olcol=OL)
        s._cache["mai"] = c.img(K, rgba=True)
        return s._cache["mai"]

    def _vitre_porte(s):
        x0, y0, x1, y1 = s.PORTE_H
        return (x0 + 5, y0 + 4, x1 - 5, y0 + 12)

    def _lumieres(s):
        """Ce qui s'allume (calculé une fois) : la porte (vitre, bois réchauffé, halo, lumière sur la marche), la salle
        à manger, l'enseigne ligne par ligne (lettres, tube, lueurs) : r1 « PAS DE CHAMBRE » et r2 « PAS DE DÎNER »
        en rouge, v1 « CHAMBRE LIBRE » en vert (à la place de r1)."""
        if "lum" in s._cache:
            return s._cache["lum"]
        W, H, K = s.PW_, s.PH_, s.K
        out = {}
        # -- la porte : vitre chaude, bois réchauffé, filet de lumière sous la porte
        x0, y0, x1, y1 = s.PORTE_H
        c = Px(W, H, alpha=True)
        vx0, vy0, vx1, vy1 = s._vitre_porte()
        c.shape(c.mask_rect(vx0, vy0, vx1, vy1), (255, 218, 130), light=(255, 246, 206), band=1, olcol=OL)
        c.fill(c.mask_rect(vx0 + 1, vy0 + 1, vx1 - 1, vy0 + 3), (255, 246, 206))
        c.fill(c.mask_rect((vx0 + vx1) // 2, vy0 + 1, (vx0 + vx1) // 2 + 1, vy1 - 1), (200, 150, 80))
        c.fill(c.mask_rect(x0 + 1, y1 - 1, x1 - 1, y1), (255, 226, 140))
        bb = (int((x0 - 4) * K), int((y0 - 4) * K), int((x1 + 4) * K), int((y1 + 1) * K))
        porte = c.img(K, rgba=True)
        lay = Image.new("RGBA", porte.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).rectangle([x0 * K, y0 * K, x1 * K - 1, y1 * K - 1], fill=(255, 196, 110, 62))
        lay.alpha_composite(porte)
        out["porte"] = (lay.crop(bb), bb[:2])
        lay = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle([(x0 - 11) * K, (y0 - 10) * K, (x1 + 11) * K, (y1 + 2) * K], 70, fill=(*CHAUD, 150))
        ld.polygon([((x0 - 6) * K, (y1 + 1) * K), ((x1 + 6) * K, (y1 + 1) * K), ((x1 + 18) * K, H * K),
                    ((x0 - 18) * K, H * K)], fill=(*CHAUD, 140))
        lay = lay.filter(ImageFilter.GaussianBlur(30))
        b2 = lay.getbbox() or (0, 0, 1, 1)
        out["halo_porte"] = (lay.crop(b2), b2[:2])
        # -- la salle à manger (fenêtre de droite) : le mur chaud, la suspension, la table, l'assiette
        fx0, fy0, fx1, fy1 = s.FEN_D
        c = Px(W, H, alpha=True)
        vit = c.mask_rect(fx0 + 2, fy0 + 2, fx1 - 2, fy1 - 2)
        c.vgrad(vit, fy0, fy1, (252, 214, 150), (230, 170, 104), steps=4)
        mx = (fx0 + fx1) / 2
        c.line(mx + 6, fy0 + 2, mx + 6, fy0 + 6, (110, 80, 60))
        c.fill(c.mask_poly([(mx + 2, fy0 + 9), (mx + 10, fy0 + 9), (mx + 8, fy0 + 6), (mx + 4, fy0 + 6)]),
               (255, 246, 210))
        c.glow(mx + 6, fy0 + 9, 9, (255, 246, 210), k=0.4, m=vit)
        table = c.mask_rect(fx0 + 2, fy1 - 9, fx1 - 2, fy1 - 2)
        c.fill(table, (150, 92, 52))
        c.fill(table & c.mask_rect(0, fy1 - 9, W, fy1 - 8), (186, 122, 72))
        c.fill(c.mask_rect(fx0 + 4, fy1 - 9, fx1 - 4, fy1 - 6), (238, 236, 226))     # la nappe
        ax, ay = mx - 4, fy1 - 10                                                   # l'assiette (vue de biais)
        c.shape(c.mask_ell(ax, ay, 6.5, 2.2), (250, 250, 246), shade=(206, 206, 210), band=1, olcol=OL)
        c.fill(c.mask_ell(ax, ay - 0.6, 3.2, 1.2), (226, 150, 64))                    # le plat
        c.px(ax - 1, ay - 1, (120, 176, 80))
        c.px(ax + 1, ay - 1, (196, 84, 60))
        c.shape(c.mask_rect(mx + 7, fy1 - 15, mx + 10, fy1 - 9), (196, 230, 250), light=(240, 250, 255), band=1,
                olcol=OL)                                                          # un verre d'eau
        c.shape(c.mask_ell(mx - 13, fy1 - 10, 2.6, 1.6), (222, 176, 110), shade=(186, 136, 80), band=1, olcol=OL)  # pain
        cr = (196, 192, 206)
        c.fill(c.mask_rect(int(mx) - 1, fy0 + 2, int(mx) + 1, fy1 - 2), cr)        # les croisillons
        c.fill(c.mask_rect(fx0 + 2, (fy0 + fy1) // 2 - 1, fx1 - 2, (fy0 + fy1) // 2), cr)
        bb = (int(fx0 * K), int(fy0 * K), int(fx1 * K), int(fy1 * K))
        out["fenetre"] = (c.img(K, rgba=True).crop(bb), bb[:2])
        lay = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle([(fx0 - 8) * K, (fy0 - 7) * K, (fx1 + 8) * K, (fy1 + 6) * K], 60,
                                              fill=(*CHAUD, 100))
        lay = lay.filter(ImageFilter.GaussianBlur(28))
        b2 = lay.getbbox() or (0, 0, 1, 1)
        out["halo_fen"] = (lay.crop(b2), b2[:2])
        # -- l'enseigne, ligne par ligne (chaque ligne a son tube) : PAS DE CHAMBRE et PAS DE DÎNER (rouges), puis
        #    CHAMBRE LIBRE (vert) à la place de la 1re ligne
        ex0, ey0, ex1, ey1 = s.ENS
        mid = (ex0 + ex1) / 2
        bb = (int(ex0 * K), int(ey0 * K), int(ex1 * K), int(ey1 * K))
        for nom, txt, yb, coul, bas in (("r1", "PAS DE CHAMBRE", ey0 + 14, "rouge", False),
                                        ("r2", "PAS DE DÎNER", ey0 + 27, "rouge", True),
                                        ("v1", "CHAMBRE LIBRE", ey0 + 14, "vert", False)):
            m = _texte_px(W, H, [(txt, mid, yb)], 11)
            c = Px(W, H, alpha=True)
            tube = s._tubes(c)[1 if bas else 0]
            moitie = c.mask_rect(ex0, s.Y_COUPE, ex1, ey1) if bas else c.mask_rect(ex0, ey0, ex1, s.Y_COUPE)
            c.fill(tube, NEON[coul][1])
            _neon(c, m, NEON[coul])
            out[nom] = (c.img(K, rgba=True).crop(bb), bb[:2])
            out["gl_" + nom] = _lueur(_dilate(m) | tube, K, NEON[coul][2], 10, 1.2)
            g2, p2 = _lueur(moitie, K, NEON[coul][2], 40, 0.5, marge=8)        # le grand halo, de son côté seulement
            out["gl2_" + nom] = (_borne(g2, p2, s.Y_COUPE * K, not bas, 3 * K), p2)
        s._cache["lum"] = out
        return out

    def _image_hotel(s, u):
        K = s.K
        im = s._ciel().copy()
        W_, H_ = im.size
        # le ciel vit doucement : deux nuages qui glissent, quelques étoiles qui respirent
        for j, (x0, y0, v) in enumerate(((150, 18, 2.2), (20, 50, 1.6))):
            nu = s._nuage(j)
            x = ((x0 - v * u) % 230) - 40
            im.alpha_composite(_fade(nu, 0.85), (int(x * K), int(y0 * K)))
        d = ImageDraw.Draw(im)
        for j, (x, y) in enumerate(s._cache["etoiles"][:8]):
            a = 0.5 + 0.5 * math.sin(u * 1.6 + j * 2.3)
            if a > 0.6:
                al = int(200 * (a - 0.6) / 0.4)
                d.rectangle([x * K - K, y * K + 2, x * K + 2 * K - 1, y * K + K - 3], fill=(255, 255, 255, al))
                d.rectangle([x * K + 2, y * K - K, x * K + K - 3, y * K + 2 * K - 1], fill=(255, 255, 255, al))
        lum = s._lumieres()
        # la porte s'illumine ({maison entre}) et s'éteint ({maison libre}) ; la salle à manger s'allume ({maison mange})
        # et RESTE allumée à « libre » (sur un plan neuf ouvert par « libre » : allumée d'emblée)
        ap = s._a("entre", u, 0.6, fin="libre", dfin=0.6)
        aw = s._acquis("mange", u, 0.6)
        for cle, a in (("halo_porte", ap), ("halo_fen", aw)):
            if a > 0.01:
                h_, pos = lum[cle]
                im.alpha_composite(_fade(h_, a), pos)
        im.alpha_composite(s._maison())
        for cle, a in (("porte", ap), ("fenetre", aw)):
            if a > 0.01:
                l_, pos = lum[cle]
                im.alpha_composite(_fade(l_, a), pos)
        # l'enseigne, un tube par ligne : {maison pas} les deux lignes en rouge ; {maison libre} la 1re passe au vert
        # « CHAMBRE LIBRE », qui pulse lentement (1,2 s), la 2e reste rouge « PAS DE DÎNER »
        neuf = s._neuf()
        pul = 1.0
        if "libre" in s.t and u > s.t["libre"] + 0.85:
            pul = 0.5 + 0.5 * math.cos(2 * math.pi * (u - s.t["libre"] - 0.85) / 1.2)
        lignes = (("r1", s._a("pas", u, 0.6, fin="libre", dfin=0.35), 1.0),
                  ("r2", s._acquis("pas", u, 0.6), 1.0),
                  ("v1", s._e("libre", u, 0.5 if neuf else 0.6, dec=0.0 if neuf else 0.25), pul))
        for pref, k0 in (("gl2_", 0.55), ("gl_", 0.75)):                    # les lueurs d'abord, les lettres dessus
            for nom, a, p in lignes:
                if a > 0.01:
                    g, pos = lum[pref + nom]
                    im.alpha_composite(_fade(g, a * (k0 + (1 - k0) * p)), pos)
        for nom, a, p in lignes:
            if a > 0.01:
                l_, pos = lum[nom]
                im.alpha_composite(_fade(l_, a * (0.9 + 0.1 * p)), pos)
        # les textes : sous l'enseigne (sur le toit) la parole du Chaytan ; au-dessus de la porte et sous la fenêtre,
        # les BISMILLAH
        # (une colonne qui descend du bas de l'enseigne : en-tête, citation, BISMILLAH, « = AU NOM D'ALLAH », puis la
        # porte ; les hauteurs sont celles de l'encre, ombre comprise)
        ex0, ey0, ex1, ey1 = s.ENS
        x0, y0, x1, y1 = s.PORTE_H
        cxp = (x0 + x1) / 2 * K
        hh = s._labc("LE CHAYTAN, AUX SIENS :", BLANC, 44)
        q1 = s._citation("« NI NUIT NI DÎNER", "POUR VOUS ! »")
        q2 = s._citation("« VOUS AVEZ TROUVÉ", "OÙ PASSER LA NUIT ! »")
        h1, h2 = s._labc("BISMILLAH", OR_, 52), s._labc("= AU NOM D'ALLAH", BLANC, 44)
        y_h = ey1 * K + 4                                                           # haut de l'en-tête
        y_q = y_h + hh.height - 6                                                   # haut de la citation
        y_b = y_q + max(q1.height, q2.height) - 4                                   # haut de BISMILLAH (porte)
        y_n = y_b + h1.height - 10                                                  # haut de « = AU NOM D'ALLAH »
        a1 = s._a("entre", u, 0.4, dec=0.15, fin="libre", dfin=0.4)
        a2 = s._a("entre", u, 0.4, dec=0.5, fin="libre", dfin=0.4)
        s._pose(im, h1, cxp, y_b + h1.height / 2 + 10 * (1 - a1), a1)
        s._pose(im, h2, cxp, y_n + h2.height / 2 + 8 * (1 - a2), a2)
        a3 = s._acquis("mange", u, 0.4, dec=0.2)              # le BISMILLAH du repas reste, même à « libre »
        fx0, fy0, fx1, fy1 = s.FEN_D
        h3 = s._labc("BISMILLAH", OR_, 50)
        s._pose(im, h3, (fx0 + fx1) / 2 * K, (fy1 + 2) * K + 6 + h3.height / 2 + 8 * (1 - a3), a3, maxw=400)
        ah = max(s._e("pas", u, 0.4, dec=0.2), s._e("libre", u, 0.4, dec=0.2))
        if ah > 0.01:                       # une carte sombre (sans pointe) : ses paroles, à part des BISMILLAH
            carte = s._cache.get("carte")
            if carte is None:
                w = max(hh.width, q1.width, q2.width) + 64
                h = y_q + max(q1.height, q2.height) - y_h + 6
                carte = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
                ImageDraw.Draw(carte).rounded_rectangle([0, 0, carte.width - 1, carte.height - 1], 30,
                                                        fill=(16, 12, 34, 150))
                s._cache["carte"] = carte
            im.alpha_composite(_fade(carte, ah), (int(W_ / 2 - carte.width / 2), int(y_h - 2)))
        s._pose(im, hh, W_ / 2, y_h + hh.height / 2 + 8 * (1 - ah), ah)
        aq = s._a("pas", u, 0.4, dec=0.6, fin="libre", dfin=0.35)
        s._pose(im, q1, W_ / 2, y_q + q1.height / 2 + 10 * (1 - aq), aq)
        al = s._e("libre", u, 0.45, dec=0.4)
        s._pose(im, q2, W_ / 2, y_q + q2.height / 2 + 10 * (1 - al), al)
        return s._coins(im)


# ---------------------------------------------------------------- branchement (par explique_0611.py)
CLES = ("porte", "maison")


def _norm(m):
    return m.lower().replace("é", "e").replace("è", "e").replace("î", "i")


def ordre(schema, t, brut, mots, reste):
    """Appelé (via explique_0611.ordre) pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    qui = mots[1].upper() if len(mots) > 1 else "PETIT"

    def dernier(cls, mode=None):
        return next((it["el"] for it in reversed(schema._visibles(t + 0.01))
                     if isinstance(it["el"], cls) and (mode is None or getattr(it["el"], "mode", None) == mode)), None)

    def u_de(el):
        return t - next(it["t_in"] for it in schema.items if it["el"] is el)

    def etape(cls, nom, mode=None, nouveau=None):
        el = dernier(cls, mode)
        if el is None:
            el = nouveau() if nouveau else cls(brut)
            schema._ajoute(t, el)
        el.t[nom] = u_de(el)

    if k == "porte":
        schema._ajoute(t, Maison(brut, "porte", qui if qui in cast.CAST else "PETIT"))
    elif k == "maison":
        if sous in Maison.ETAPES:
            etape(Maison, sous, "hotel", lambda: Maison(brut, "hotel"))
        else:
            schema._ajoute(t, Maison(brut, "hotel"))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "porte":
        return t + 2.2                       # porte ouverte à 1,3 s, enseigne allumée à 1,7 s, + le temps de la lire
    if k == "maison":
        return t + dict(entre=1.0, mange=0.9, pas=1.4, libre=1.6).get(sous, 0.6)
    return None
