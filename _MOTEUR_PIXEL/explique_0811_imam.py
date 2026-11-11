# DÉMONSTRATIONS EN IMAGE DU 08/11/2026 — Short ISL26 « Ne te relève JAMAIS avant l'imam… crains la tête d'âne ! »
# (format consigne + avertissement). Même principe que explique_0611_dette.py : le sens propre du hadith, montré en grand,
# mouvements doux (glissés adoucis, fondus), jamais de secousse ni de flash. L'imam est un homme ordinaire, DE DOS dans
# les scènes (de profil dans la frise : pictogramme d'homme ordinaire avec visage, barbe, calotte, qamis — JAMAIS une
# silhouette blanche sans visage, qui pourrait passer pour un prophète, la frise étant sous Mouslim 426 / Boukhari 722),
# étiqueté « L'IMAM », sans lumière ni mise en valeur. Aucun âne dessiné ; Petit garde son visage normal : seule son
# OMBRE porte des oreilles d'âne (longues, pointues), en POINTILLÉS (une menace, pas un fait).
# Relecture du 08/11/2026 : frise en 4 temps avec le REDRESSEMENT debout (obligatoire, Boukhari 757) ; coches loin de
# « TOI AVANT » ; « MENACE : / TÊTE D'ÂNE » du côté de Petit, loin de « L'IMAM » ; Petit de dos dans le rang dans la
# chute (face à la qibla) ; prosternés de dos : calotte / casquette visible (« front au sol »).
#   {imam PETIT}     accroche, vue à TA place dans le 1er rang, en prosternation : tes mains (manches rouges) en grand
#                    sur le tapis, l'imam de dos encore prosterné au centre, un fidèle prosterné de chaque côté ; ta vue
#                    se relève doucement (1,2 s, parallaxe : tes mains glissent vers le bas, le mur de la qibla se
#                    découvre) pendant que tous restent prosternés ; « L'IMAM » au-dessus de lui ; flèche jaune vers le
#                    haut « TOI : DÉJÀ RELEVÉ ! » (dès 0,3 s, sous le texte d'accroche)
#   {ane}            la carte du hadith : parchemin « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : » puis la citation qui
#                    s'écrit au fil de la voix (calée sur {ane ombre} et {ane oreilles}) ; dessous, le mur de la
#                    mosquée (fondu chaud) : l'imam de dos, prosterné, étiqueté ; Petit (de dos, en bas à gauche)
#                    relève déjà la tête ; son ombre grise sur le mur ;
#                    {ane ombre} l'ombre grandit lentement (×1,25 en 1,2 s), vignette sombre douce ;
#                    {ane oreilles} sur l'OMBRE seulement, deux longues oreilles d'âne en pointillés poussent (1,5 s),
#                    « MENACE : / TÊTE D'ÂNE » (orange, au-dessus de Petit) ; elles s'estompent 3,2 s plus tard
#                    (elles restent pendant « Mes oreilles ?! »)
#   {ane suivre}     la frise (nouveau schéma) : « NE BOUGE JAMAIS AVANT L'IMAM » / « PÉCHÉ SI C'EST EXPRÈS » ; en
#                    bas à gauche la version fausse « TOI AVANT » (se relève pendant que l'imam, à côté, est encore
#                    prosterné) barrée ✗ ; quatre temps INCLINÉ → REDRESSÉ → PROSTERNÉ → RELEVÉ : l'imam fait son
#                    mouvement en entier, ARRIVE, et « TOI » ne commence que 0,15 s après ; coche verte sous chaque
#                    pose de « TOI » ; « L'IMAM… PUIS TOI ! »
#   {ane colle}      la chute (nouveau schéma) : la mosquée, tout le monde debout de dos (l'imam étiqueté) ; Petit
#                    seul encore prosterné, DE DOS dans le rang, face au mihrab, gouttes de sueur ; petit chrono gris
#                    « +3 S… +5 S… +8 S… +10 S… » sous lui (fondus, sans clignoter)
# Branché par explique_0811.py (import tardif). Bruitages discrets de _BRUITAGES (froissement, souffle doux, ting) ; aucun
# braiment ni bruitage comique.
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from px import Px
from pxv import smooth
from explique import _fade, _os, BLANC, JAUNE
from explique_0411 import OL, _peau
from explique_0411b import _Base, _fleche, ORANGE, VERT
from explique_0611_dette import _texte_px, _colle, _halo, PAPIER, ENCRE_P

PEAU = _peau("PETIT")
P3 = (PEAU["b"], PEAU["s"], PEAU["h"])
SWEAT = ((200, 50, 50), (150, 34, 40), (232, 92, 84))
JEAN = ((62, 96, 166), (44, 70, 128), (92, 126, 196))
CHAUSSETTE = ((240, 240, 244), (196, 196, 206), (255, 255, 255))
CASQ = ((40, 50, 90), (26, 32, 62), (70, 82, 130))
QAMIS = ((240, 238, 230), (198, 194, 184), (255, 255, 252))        # l'imam : qamis blanc, calotte blanche
KUFI = ((248, 248, 250), (206, 206, 214), (255, 255, 255))
CHEVEUX = ((40, 38, 44), (26, 24, 30), (72, 68, 78))
GRIS_Q = ((150, 158, 172), (112, 120, 136), (184, 192, 204))      # les fidèles
BLEU_T = ((54, 82, 120), (38, 58, 90), (84, 114, 156))
BEIGE = ((196, 178, 146), (156, 138, 108), (222, 206, 176))
VERT_T = ((70, 112, 92), (50, 84, 68), (100, 144, 120))
TAPIS = (150, 40, 48)
TAPIS_F = (118, 28, 38)
OR_T = (204, 152, 64)
ROUGE_D = (240, 112, 100)                                           # « rouge doux » du bandeau
GRIS_C = (206, 206, 216)                                            # le chrono, les pointillés


def _L(a, b, t):
    return a + (b - a) * t


def _grille(c):
    m = c.mask_rect(0, 0, 1, 1)
    H, W = m.shape
    return np.mgrid[0:H, 0:W]


# ---------------------------------------------------------------- les silhouettes
def _dos_geo(p, z):
    """Géométrie d'un fidèle vu de dos, à genoux : p = 0 prosterné (le dos, la tête cachée devant), p = 1 assis droit.
    Renvoie (q, haut du torse, demi-largeur, centre de la tête), en pixels du dessin, relatifs au sol."""
    q = smooth(p)
    yt = -_L(16, 33, q) * z
    rx = _L(14, 10.5, q) * z
    yh = yt + _L(5, -4.5, q) * z
    return q, yt, rx, yh


def _tete_dos(c, cx, hy, z, tete):
    hr = 5.5 * z
    tm = c.mask_ell(cx, hy, hr, hr * 1.05)
    oreilles = c.mask_ell(cx - hr, hy + 0.6 * z, 1.4 * z, 2.0 * z) | c.mask_ell(cx + hr, hy + 0.6 * z, 1.4 * z, 2.0 * z)
    c.shape(oreilles, PEAU["b"], shade=PEAU["s"], band=1, olcol=OL)
    c.shape(tm, CHEVEUX[0], shade=CHEVEUX[1], light=CHEVEUX[2], band=1, olcol=OL)
    c.fill(c.mask_rect(cx - hr * 0.6, hy + hr * 0.62, cx + hr * 0.6, hy + hr * 1.2) & tm, PEAU["s"])   # la nuque
    if tete == "kufi":
        cap = tm & c.mask_rect(cx - hr - 2, hy - hr - 2, cx + hr + 2, hy - 0.6 * z)
        c.shape(cap, KUFI[0], shade=KUFI[1], light=KUFI[2], band=1, olcol=OL)
    elif tete == "casquette":
        cap = tm & c.mask_rect(cx - hr - 2, hy - hr - 2, cx + hr + 2, hy + 0.9 * z)
        c.shape(cap, CASQ[0], shade=CASQ[1], light=CASQ[2], band=1, olcol=OL)
        c.fill(c.mask_rect(cx - 1.6 * z, hy - 0.2 * z, cx + 1.6 * z, hy + 0.9 * z) & cap, CHEVEUX[0])   # l'attache
        c.fill(c.mask_rect(cx - 2.4 * z, hy - 0.6 * z, cx + 2.4 * z, hy - 0.2 * z) & cap, CASQ[1])


def _dos(c, cx, base, z, p, haut, bas, pieds, tete, ombre_sol=True):
    """Un fidèle vu de dos, à genoux (prosterné → assis), dessiné dans le Px c (pixels du dessin)."""
    q, yt, rx, yh = _dos_geo(p, z)
    if ombre_sol:
        c.tint(c.mask_ell(cx, base - 1 * z, 15 * z, 3.2 * z), (20, 8, 16), 0.32)
    if q > 0.12:
        _tete_dos(c, cx, base + yh, z, tete)
    else:                                   # prosterné : la calotte / la casquette dépasse devant le dos (« front au sol »)
        hr = 5.5 * z
        col = KUFI if tete == "kufi" else (CASQ if tete == "casquette" else CHEVEUX)
        c.shape(c.mask_ell(cx, base + yt - 1.5 * z, hr * 0.9, hr * 0.55), col[0], shade=col[1], light=col[2], band=1,
                olcol=OL)
    jambes = c.mask_ell(cx, base - 5.5 * z, 12.5 * z, 5.5 * z)
    c.shape(jambes, bas[0], shade=bas[1], light=bas[2], band=max(1, int(z)), olcol=OL)
    yb, top = base - 5.5 * z, base + yt
    ry = (yb - top) / 2
    torse = c.mask_ell(cx, top + ry, rx, ry) | c.mask_rrect(cx - rx, top + ry * 0.8, cx + rx, yb, 2 * z)
    c.shape(torse, haut[0], shade=haut[1], light=haut[2], band=max(1, int(1.5 * z)), olcol=OL)
    c.fill(c.mask_rect(cx - 0.35 * z, top + 2.5 * z, cx + 0.35 * z, yb - 1 * z) & torse, haut[1])   # le pli du dos
    if tete == "casquette" and q > 0.45:                                                           # la capuche du sweat
        c.fill(c.mask_ell(cx, top + 2.2 * z, 5.2 * z, 2.4 * z) & torse, haut[1])
    for sx in (-1, 1):                                                                             # les plantes des pieds
        pl = c.mask_rrect(cx + sx * 5.5 * z - 2.7 * z, base - 5 * z, cx + sx * 5.5 * z + 2.7 * z, base, 1.2 * z)
        c.shape(pl, pieds[0], shade=pieds[1], light=pieds[2], band=1, olcol=OL)
        for j in range(3):                                                                         # les orteils (traits)
            x = cx + sx * 5.5 * z + (j - 1) * 1.6 * z
            c.fill(c.mask_rect(x - 0.2 * z, base - 1.3 * z, x + 0.2 * z, base - 0.2 * z) & pl, pieds[1])


def _debout_dos(c, cx, base, z, haut, tete):
    """Un fidèle debout, vu de dos (qamis jusqu'aux chevilles)."""
    c.tint(c.mask_ell(cx, base - 0.5 * z, 12 * z, 2.6 * z), (20, 8, 16), 0.3)
    corps = c.mask_poly([(cx - 8.5 * z, base - 37 * z), (cx + 8.5 * z, base - 37 * z), (cx + 10 * z, base - 2 * z),
                         (cx - 10 * z, base - 2 * z)]) | c.mask_ell(cx, base - 36.5 * z, 8.6 * z, 3 * z)
    for sx in (-1, 1):
        t_ = c.mask_rrect(cx + sx * 4 * z - 2 * z, base - 3 * z, cx + sx * 4 * z + 2 * z, base, 1 * z)
        c.shape(t_, PEAU["s"], shade=PEAU["d"], band=1, olcol=OL)
    c.shape(corps, haut[0], shade=haut[1], light=haut[2], band=max(1, int(1.5 * z)), olcol=OL)
    for sx in (-1, 1):                                                                             # les bras le long
        c.fill(c.mask_rect(cx + sx * 7.2 * z - 0.3 * z, base - 33 * z, cx + sx * 7.2 * z + 0.3 * z, base - 20 * z)
               & corps, haut[1])
    _tete_dos(c, cx, base - 42 * z, z, tete)


# poses de profil (unités ; le perso regarde à droite ; sol à y = 42)
DEBOUT = dict(p=(19, 42), g=(19, 33), b=(19, 24), n=(20, 11), t=(21, 5.5), c=(23, 18), m=(26, 15))
INCLINE = dict(p=(13, 42), g=(13, 33), b=(13, 24), n=(26, 22), t=(31.5, 22.5), c=(21, 27), m=(15, 32))
PROSTERNE = dict(p=(6, 42), g=(15, 41), b=(11, 32), n=(23, 37), t=(27.5, 38.2), c=(22, 40), m=(25, 42))
ASSIS = dict(p=(6, 42), g=(16, 41), b=(8, 37), n=(9, 24), t=(10, 18.5), c=(11, 31), m=(16, 37))


def _mix(P, Q, k):
    return {n: (P[n][0] + (Q[n][0] - P[n][0]) * k, P[n][1] + (Q[n][1] - P[n][1]) * k) for n in P}


def _profil(c, ox, oy, z, P, style="imam", yeux="ouverts"):
    """Un fidèle de profil (vers la droite) : style « imam » = HOMME ORDINAIRE (visage couleur peau, barbe et cheveux
    foncés, calotte blanche, qamis blanc cassé, mains et pieds nus) — jamais une silhouette blanche sans visage, qui
    pourrait passer pour la représentation d'un prophète ; « petit » = sweat rouge, jean, chaussettes, casquette (yeux
    « ouverts » ou « serres »)."""
    f = lambda k: (ox + P[k][0] * z, oy + P[k][1] * z)
    if style == "imam":
        jb = tr = br = QAMIS
        pied = P3
    else:
        jb, tr, br, pied = JEAN, SWEAT, SWEAT, CHAUSSETTE
    bx = f("p")
    pied_m = c.mask_ell(bx[0] + 2 * z, bx[1] - 1.1 * z, 3.2 * z, 1.5 * z)
    c.shape(pied_m, pied[0], shade=pied[1], light=pied[2], band=1, olcol=OL)
    jam = _os(c, *f("b"), *f("g"), 5.6 * z) | _os(c, *f("g"), *f("p"), 4.8 * z)
    c.shape(jam, jb[0], shade=jb[1], light=jb[2], band=1, olcol=OL)
    torse = _os(c, *f("b"), *f("n"), 9 * z)
    c.shape(torse, tr[0], shade=tr[1], light=tr[2], band=max(1, int(z)), olcol=OL)
    tx, ty = f("t")
    nx, ny = f("n")
    hr = 5 * z
    tete = c.mask_ell(tx, ty, hr, hr)
    c.shape(tete, PEAU["b"], shade=PEAU["s"], light=PEAU["h"], band=1, olcol=OL)
    dx, dy = tx - nx, ty - ny
    L_ = math.hypot(dx, dy) or 1
    ux, uy = dx / L_, dy / L_                             # vers le sommet du crâne
    fx, fy = -uy, ux                                      # vers le visage
    Y, X = _grille(c)
    rel_u = (X - tx) * ux + (Y - ty) * uy
    rel_f = (X - tx) * fx + (Y - ty) * fy
    cheveux = tete & (rel_f < -1.2 * z) & (rel_u > -2.5 * z)
    c.fill(cheveux, CHEVEUX[0])
    if style == "imam":                                   # homme ordinaire : barbe foncée, calotte blanche
        barbe = tete & (rel_u < -2.4 * z) & (rel_f > -1.0 * z)            # un collier court au menton

        c.fill(barbe, CHEVEUX[0])
        cap = tete & (rel_u > 2.0 * z)
        c.shape(cap, KUFI[0], shade=KUFI[1], light=KUFI[2], band=1, olcol=OL)
    else:
        cap = tete & (rel_u > 1.0 * z)
        c.shape(cap, CASQ[0], shade=CASQ[1], light=CASQ[2], band=1, olcol=OL)
    c.fill(c.mask_ell(tx - fx * 0.6 * z, ty - fy * 0.6 * z, 1.1 * z, 1.5 * z) & tete & ~cap & ~cheveux,
           PEAU["s"])                                     # l'oreille
    ex, ey = tx + fx * 2.9 * z + ux * 0.4 * z, ty + fy * 2.9 * z + uy * 0.4 * z
    if yeux == "serres":                                  # yeux fermés et serrés (peur) : un trait en chevron
        for j in (-1, 0, 1):
            c.fill(c.mask_ell(ex + ux * j * 0.9 * z + fx * abs(j) * 0.45 * z,
                              ey + uy * j * 0.9 * z + fy * abs(j) * 0.45 * z, 0.55 * z, 0.55 * z), OL)
    else:
        c.fill(c.mask_ell(ex, ey, 0.6 * z, 0.6 * z), OL)
    bras = _os(c, *f("n"), *f("c"), 3.6 * z) | _os(c, *f("c"), *f("m"), 3.3 * z)
    c.shape(bras, br[0], shade=br[1], light=br[2], band=1, olcol=OL)
    mx, my = f("m")
    c.shape(c.mask_ell(mx, my, 1.9 * z, 1.6 * z), PEAU["b"], shade=PEAU["s"], band=1, olcol=OL)


# ---------------------------------------------------------------- décors dessinés ici (aucun décor partagé modifié)
def _mur_tapis(c, W, H, y_j, mihrab=None, sombre=0.0):
    """Mur crème de la mosquée (frise verte en bas) et tapis rouge à rangs dorés à partir de y_j (pixels du dessin)."""
    tout_ = c.mask_rect(0, 0, W, H)
    mur = c.mask_rect(0, 0, W, y_j)
    c.vgrad(mur, 0, y_j, (190, 176, 152), (226, 212, 186), steps=6)
    if mihrab is not None:                                                # le mihrab (niche de la qibla), sans lumière
        mx, mw, mtop = mihrab
        arc = c.mask_arch(mx - mw, mx + mw, mtop, y_j - 4, pointed=0.35)
        c.shape(arc, OR_T, shade=(160, 114, 44), light=(232, 190, 104), band=1, olcol=OL)
        fond = c.mask_arch(mx - mw + 3, mx + mw - 3, mtop + 3, y_j - 4, pointed=0.35)
        c.vgrad(fond, mtop, y_j, (72, 112, 104), (52, 84, 80), steps=4)
        for x in range(int(mx - mw + 6), int(mx + mw - 5), 4):
            c.fill(c.mask_rect(x, y_j - 14, x + 2, y_j - 12) & fond, (96, 140, 128))
    frise = c.mask_rect(0, y_j - 6, W, y_j - 1)
    c.shape(frise, (54, 120, 96), shade=(36, 88, 70), light=(84, 156, 124), sdir="bottom", band=1, olcol=OL)
    for x in range(2, W, 6):
        c.fill(c.mask_rect(x, y_j - 4, x + 2, y_j - 3), (226, 200, 120))
    sol = c.mask_rect(0, y_j, W, H) & tout_
    c.fill(sol, TAPIS)
    c.dither(sol, TAPIS_F, 0.18)
    y, pas = y_j + 4, 5
    while y < H:                                                          # les rangs (plus espacés vers toi)
        c.fill(c.mask_rect(0, y, W, y + max(1, int(pas / 6))), OR_T)
        y += pas
        pas = int(pas * 1.55) + 1
    if sombre:
        c.tint(tout_, (20, 10, 20), sombre)


_VIGNETTES = {}


def _vignette(W, H, force=150):
    cle = (W, H, force)
    if cle not in _VIGNETTES:
        a = np.zeros((H, W), np.float32)
        Y, X = np.mgrid[0:H, 0:W]
        r = np.sqrt(((X - W / 2) / (W * 0.62)) ** 2 + ((Y - H / 2) / (H * 0.62)) ** 2)
        a = np.clip((r - 0.55) / 0.5, 0, 1) * force
        out = np.zeros((H, W, 4), np.uint8)
        out[..., :3] = (16, 8, 18)
        out[..., 3] = a.astype(np.uint8)
        _VIGNETTES[cle] = Image.fromarray(out, "RGBA")
    return _VIGNETTES[cle]


def _coche(d, x, y, r, a=1.0):
    A = int(255 * a)
    pts = [(x - r, y), (x - r * 0.3, y + r * 0.7), (x + r, y - r * 0.8)]
    d.line(pts, fill=(20, 16, 30, A), width=int(r * 0.55) + 8, joint="curve")
    d.line(pts, fill=(*VERT, A), width=int(r * 0.55), joint="curve")


def _croix(d, x, y, r, a=1.0):
    A = int(255 * a)
    for (x0, y0, x1, y1) in ((x - r, y - r, x + r, y + r), (x - r, y + r, x + r, y - r)):
        d.line([(x0, y0), (x1, y1)], fill=(20, 16, 30, A), width=int(r * 0.4) + 8)
    for (x0, y0, x1, y1) in ((x - r, y - r, x + r, y + r), (x - r, y + r, x + r, y - r)):
        d.line([(x0, y0), (x1, y1)], fill=(236, 60, 56, A), width=int(r * 0.4))


def _fleche_haut(d, x, y0, y1, col=JAUNE, a=1.0, ep=14):
    """Flèche verticale de y0 (bas) vers y1 (haut), pixels d'écran."""
    A = int(255 * a)
    if A <= 0:
        return
    d.line([(x, y0), (x, y1 + 24)], fill=(20, 16, 30, A), width=ep + 8)
    d.polygon([(x, y1 - 6), (x - 30, y1 + 32), (x + 30, y1 + 32)], fill=(20, 16, 30, A))
    d.line([(x, y0), (x, y1 + 24)], fill=(*col, A), width=ep)
    d.polygon([(x, y1), (x - 22, y1 + 28), (x + 22, y1 + 28)], fill=(*col, A))


# ---------------------------------------------------------------- {imam PETIT} : l'accroche
class Imam(_Base):
    """{imam PETIT} : vue à ta place dans le rang, en prosternation ; ta vue se relève (parallaxe douce) pendant que
    l'imam (de dos, étiqueté) et les fidèles restent prosternés ; « TOI : DÉJÀ RELEVÉ ! »."""
    W_, H_ = 1020, 960
    D = 150                              # de combien la vue « monte » (pixels d'écran)
    PAR = (0.6, 1.0, 1.4)                # parallaxe : mur et tapis, fidèles, tes mains
    T0, DUREE = -0.4, 1.6                # le glissé (u = 0 : déjà commencé, à ≈ 15 %)
    T_TOI = 0.3
    MARGE = 46                           # haut de l'image laissé transparent (place du texte d'accroche)

    def __init__(s, cmd, who="PETIT"):
        super().__init__(cmd)
        s.who = who

    def sons_el(s):
        return [(0.05, "dv_tissu", 0.025, None)]

    def _couche(s, n):
        cle = ("couche", n)
        if cle in s._cache:
            return s._cache[cle]
        K = 6
        W, H = s.W_ // K, (s.H_ + int(s.D * s.PAR[n])) // K + 1
        c = Px(W, H, alpha=True)
        if n == 0:                                                        # le mur de la qibla et le tapis
            _mur_tapis(c, W, H, 70, mihrab=(93, 17, 16))
        elif n == 1:                                                      # l'imam et les deux voisins, prosternés
            _dos(c, 4, 152, 3.1, 0.0, GRIS_Q, GRIS_Q, P3, "kufi")
            _dos(c, 168, 154, 3.1, 0.0, BLEU_T, BEIGE, P3, "nu")
            _dos(c, 93, 133, 2.6, 0.0, QAMIS, QAMIS, P3, "kufi")
        else:                                                             # tes mains à plat sur le tapis
            for sx in (-1, 1):
                X = (lambda x: x) if sx < 0 else (lambda x: W - x)
                man = c.mask_poly([(X(-2), H + 1), (X(-2), H - 30), (X(18), H - 38), (X(44), H - 20), (X(40), H + 1)])
                c.shape(man, SWEAT[0], shade=SWEAT[1], light=SWEAT[2], band=2, olcol=OL)
                for j in range(4):                                        # le poignet côtelé
                    c.fill(c.mask_poly([(X(24 + 3 * j), H - 36 + j), (X(26 + 3 * j), H - 36 + j),
                                        (X(30 + 3 * j), H - 24), (X(28 + 3 * j), H - 24)]) & man, SWEAT[1])
                paume = c.mask_ell(X(34), H - 44, 11, 7.5)
                c.shape(paume, PEAU["b"], shade=PEAU["s"], light=PEAU["h"], band=1, olcol=OL)
                for j, (dx, lg) in enumerate(((-7, 9), (-2.5, 11), (2, 10.5), (6.5, 8))):   # les doigts, vers l'avant
                    d_ = c.mask_rrect(min(X(34 + dx - 1.8), X(34 + dx + 1.8)), H - 46 - lg,
                                      max(X(34 + dx - 1.8), X(34 + dx + 1.8)), H - 44, 1.6)
                    c.shape(d_, PEAU["b"], shade=PEAU["s"], light=PEAU["h"], band=1, olcol=OL)
                pouce = _os(c, X(42), H - 42, X(49), H - 50, 3.6)
                c.shape(pouce, PEAU["b"], shade=PEAU["s"], light=PEAU["h"], band=1, olcol=OL)
                c.tint(c.mask_ell(X(34), H - 37, 13, 3) & ~man, (20, 8, 16), 0.25)
        s._cache[cle] = c.img(K, rgba=True)
        return s._cache[cle]

    def image(s, u):
        im = Image.new("RGBA", (s.W_, s.H_), (0, 0, 0, 0))
        g = smooth((u - s.T0) / s.DUREE)
        dys = []
        for n in range(3):
            lay = s._couche(n)
            dy = -s.D * s.PAR[n] * (1 - g)                                # au départ remontée, puis descend doucement
            im.alpha_composite(lay.crop((0, int(-dy), s.W_, int(-dy) + s.H_)))
            dys.append(dy)
            if n == 1:                                                    # « L'IMAM » suit l'imam
                s._pose(im, s._lab("L'IMAM", BLANC, 48), 558, int(133 * 6 - 2.6 * 21 * 6 - 46 + dy), 1.0, maxw=360)
        a = smooth((u - s.T_TOI) / 0.35)
        if a > 0.01:
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            _fleche_haut(ImageDraw.Draw(lay), 64, 330 + 20 * (1 - a), 150, a=a)
            im.alpha_composite(lay)
            s._pose(im, s._lab("TOI : DÉJÀ RELEVÉ !", JAUNE, 50), 270, 232 + 14 * (1 - a), a, maxw=440)
        # bande transparente en haut (MARGE px, fondu doux) : le texte d'ACCROCHE, juste au-dessus, ne touche pas l'image
        al = np.array(im.getchannel("A"), np.float32)
        al[:s.MARGE] = 0
        al[s.MARGE:s.MARGE + 12] *= np.linspace(0, 1, 12, dtype=np.float32)[:, None]
        im.putalpha(Image.fromarray(al.astype(np.uint8)))
        return im


# ---------------------------------------------------------------- {ane …}
CITE = (("« CELUI QUI LÈVE LA TÊTE", "AVANT L'IMAM…"),
        ("NE CRAINT-IL PAS QU'ALLAH", "CHANGE SA TÊTE"),
        ("EN TÊTE D'ÂNE ? »",))


class Ane(_Base):
    """{ane} la carte du hadith (Mouslim 427 · Boukhari 691) : parchemin, l'imam de dos prosterné, Petit qui relève la
    tête, son ombre ; {ane ombre} elle grandit ; {ane oreilles} oreilles en pointillés sur l'ombre, « MENACE : TÊTE
    D'ÂNE ». {ane suivre} la frise « L'IMAM… PUIS TOI » (Mouslim 426 · Boukhari 722). {ane colle} la chute."""
    ETAPES = ("ombre", "oreilles")
    W_, H_ = 1020, 960
    # la carte (pixels d'écran)
    Y_SOL = 846                         # bas du mur (début du tapis)
    PETIT_X, PETIT_B, PETIT_Z = 200, 952, 1.4
    IMAM_X, IMAM_B, IMAM_Z = 762, 868, 1.3
    OMBRE_X = 432
    Z_OMBRE = 1.02                      # taille de l'ombre (×1,3 avec {ane ombre})
    T_MUR, T_PERSO, T_LEVE = 0.1, 0.35, 1.3   # T_LEVE : au plus tôt ; sinon calé sur « Celui qui lève la tête »
    DEF_OMBRE, DEF_OREILLES = 4.4, 6.6  # si les étapes manquent (planche)
    T_ESTOMPE = 3.2                     # les oreilles restent pendant « Mes oreilles ?! » (Petit, en schéma)
    # la frise : 4 temps, le REDRESSEMENT debout après l'inclinaison est montré (obligatoire : Boukhari 757 « ثُمَّ
    # ارْفَعْ حَتَّى تَعْتَدِلَ قَائِمًا، ثُمَّ اسْجُدْ » ; Boukhari 690 : debout après « sami'a Allahou liman hamidah »)
    COLS = (285, 460, 635, 810)
    Y_IMAM, Y_TOI, Z_F = 430, 670, 0.82
    T_FAUX, T_CROIX = 0.15, 0.85
    T_COL, DT_COL, D_MV, ATT = 0.45, 0.75, 0.3, 0.15   # DT_COL = D_MV + ATT + D_MV : TOI arrive avant le temps suivant
    T_FINAL = 3.3
    # la chute : Petit dans le rang (entre les fidèles vert et bleu), de dos, face au mihrab (pixels du dessin, K = 6)
    PK_X, PK_B, PK_Z = 110, 107, 1.15
    CHRONO = (510, 740)                 # pixels d'écran

    def __init__(s, cmd, mode="carte"):
        super().__init__(cmd)
        s.mode = mode

    def sons_el(s):
        if s.mode == "carte":
            out = [(s.T_MUR, "tr_whoosh_doux", 0.02, None)]
            if "ombre" in s.t:
                out.append((s.t["ombre"], "tr_whoosh_doux", 0.025, None))
            return out
        if s.mode == "suivre":
            return [(s.T_FINAL, "sa_ting", 0.025, None)]
        return [(0.1, "dv_tissu", 0.02, None)]

    def image(s, u):
        if s.mode == "suivre":
            return s._image_suivre(u)
        if s.mode == "colle":
            return s._image_colle(u)
        return s._image_carte(u)

    # ============================================================ la carte
    def _parchemin(s):
        if "parch" in s._cache:
            return s._cache["parch"]
        K = 6
        W, H = 170, 68
        c = Px(W, H, alpha=True)
        X0, X1 = 9, 161
        f_ = c.mask_rect(X0, 5, X1, 63)
        c.fill(f_, PAPIER)
        c.dither(f_, (234, 218, 182), 0.16)
        c.edge(f_, (226, 206, 166), "right", 2)
        c.outline(f_, OL)
        for (y0, y1) in ((0, 7), (61, 67)):
            r = c.mask_rrect(X0 - 5, y0, X1 + 5, y1, 3)
            c.shape(r, (216, 188, 138), shade=(172, 142, 98), light=(238, 218, 176), sdir="bottom", band=2, olcol=OL)
            for xb in (X0 - 8, X1 + 3):
                c.shape(c.mask_rrect(xb, y0 + 1, xb + 5, y1 - 1, 2), (150, 98, 60), shade=(112, 70, 42), band=1,
                        olcol=OL)
        im = c.img(K, rgba=True)
        h = _texte_px("LE PROPHÈTE (PAIX ET SALUT SUR LUI) :", ENCRE_P, 12, k=3, pad=0)
        im.alpha_composite(h, (int(W * K / 2 - h.width / 2), 52))
        s._cache["parch"] = im
        return im

    def _lignes_cite(s):
        if "cite" not in s._cache:
            out = []
            for seg in CITE:
                out.append([_texte_px(l_, (150, 40, 40) if "ÂNE" in l_ else (62, 42, 34), 12, k=4, pad=0)
                            for l_ in seg])
            s._cache["cite"] = out
        return s._cache["cite"]

    def _ecrit(s, im, u):
        """La citation s'écrit de gauche à droite, segment par segment, au fil de la voix."""
        to = s.t.get("ombre", s.DEF_OMBRE)
        tr = s.t.get("oreilles", max(to + 1.6, s.DEF_OREILLES if "ombre" not in s.t else to + 2.0))
        bornes = ((max(1.8, to - 1.9), to), (to + 0.1, tr), (tr, tr + 0.9))
        y = 88
        for seg, (a0, a1) in zip(s._lignes_cite(), bornes):
            tot = sum(l_.width for l_ in seg)
            p = min(1.0, max(0.0, (u - a0) / max(0.3, a1 - a0)))
            vu = p * tot
            for l_ in seg:
                w = int(min(l_.width, max(0.0, vu)))
                vu -= l_.width
                if w > 0:
                    im.alpha_composite(l_.crop((0, 0, w, l_.height)), (int(510 - l_.width / 2), y))
                y += 52

    def _fond_carte(s):
        if "fondc" in s._cache:
            return s._cache["fondc"]
        W, H = s.W_, s.H_
        X = np.linspace(0, 1, W)[None, :]
        Y = np.linspace(0, 1, H)[:, None]
        clair = np.array((240, 222, 194), float)
        sombre = np.array((150, 122, 100), float)
        k = np.clip(0.75 * X + 0.25 * (1 - Y) ** 2, 0, 1)[..., None]       # la lumière vient de la gauche
        rgb = clair * (1 - k) + sombre * k
        out = np.zeros((H, W, 4), np.uint8)
        out[..., :3] = rgb.astype(np.uint8)
        out[..., 3] = 255
        out[s.Y_SOL:, :, :3] = (136, 36, 44)
        for j, y in enumerate((s.Y_SOL + 14, s.Y_SOL + 40, s.Y_SOL + 84)):
            out[y:y + 6, :, :3] = (184, 136, 60)
        out[s.Y_SOL - 30:s.Y_SOL - 6, :, :3] = (60, 118, 96)
        im = Image.fromarray(out, "RGBA").filter(ImageFilter.GaussianBlur(5))   # fond flou chaud
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 360, W - 1, H - 1], 30, fill=255)
        im.putalpha(m)
        s._cache["fondc"] = im
        return im

    def _ombre(s, p, zo):
        cle = ("ombre", round(p, 2), round(zo, 3))
        if cle in s._cache:
            return s._cache[cle]
        K = 6
        W, H = 70, 72
        c = Px(W, H, alpha=True)
        _dos(c, W / 2, H - 1, zo, p, SWEAT, JEAN, CHAUSSETTE, "casquette", ombre_sol=False)
        a = np.array(c.img(K, rgba=True))
        m = a[..., 3] > 0
        out = np.zeros_like(a)
        out[m] = (70, 60, 74, 150)
        im = Image.fromarray(out, "RGBA").filter(ImageFilter.GaussianBlur(2.5))
        if len(s._cache) > 150:
            s._cache = {k_: v for k_, v in s._cache.items() if k_[0] != "ombre"}
        s._cache[cle] = im
        return im

    def _imam_carte(s):
        if "ic" not in s._cache:
            K = 6
            c = Px(40, 30, alpha=True)
            _dos(c, 20, 28, s.IMAM_Z, 0.0, QAMIS, QAMIS, P3, "kufi")
            s._cache["ic"] = c.img(K, rgba=True)
        return s._cache["ic"]

    def _petit_carte(s, p):
        cle = ("pc", round(p, 2))
        if cle not in s._cache:
            K = 6
            c = Px(46, 66, alpha=True)
            _dos(c, 23, 64, s.PETIT_Z, p, SWEAT, JEAN, CHAUSSETTE, "casquette")
            s._cache[cle] = c.img(K, rgba=True)
        return s._cache[cle]

    def _oreilles(s, d, hx, htop, hr, g, a):
        """Deux longues oreilles d'ÂNE en pointillés (contour seul), attachées au crâne de l'ombre et écartées : base
        large, pointe fine (pas des boucles de lapin) ; g = pousse (0 → 1)."""
        if g <= 0.01 or a <= 0.01:
            return
        A = int(255 * a)
        L_ = 140 * g
        lb = 18 + 6 * g                                   # demi-largeur la plus grande (vers le premier tiers)
        n = 15
        for sx in (-1, 1):
            bx, by = hx + sx * hr * 0.75, htop + hr * 0.45
            ang = math.radians(sx * 28)
            ux, uy = math.sin(ang), -math.cos(ang)
            wx, wy = -uy, ux
            cote = []
            for i in range(n + 1):
                k = i / n
                lon = k * (L_ + 6)
                lar = lb * math.sin(math.pi * (0.25 + 0.75 * k))      # 0,7 à la base, 1 au premier tiers, 0 en pointe
                cote.append((lon, lar))
            pts = [(bx + ux * lo + wx * la, by + uy * lo + wy * la) for lo, la in cote]
            pts += [(bx + ux * lo - wx * la, by + uy * lo - wy * la) for lo, la in reversed(cote[:-1])]
            for i, (x, y) in enumerate(pts):
                if i % 2:
                    continue
                gx, gy = int(x // 6 * 6), int(y // 6 * 6)
                if gy > by + 4:
                    continue
                d.rectangle([gx - 3, gy - 3, gx + 8, gy + 8], fill=(40, 30, 44, A))
                d.rectangle([gx, gy, gx + 5, gy + 5], fill=(*GRIS_C, A))

    def _image_carte(s, u):
        W, H = s.W_, s.H_
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        am = smooth((u - s.T_MUR) / 0.5)
        if am > 0.01:
            im.alpha_composite(_fade(s._fond_carte(), am))
        # l'ombre de Petit sur le mur (et celle, basse, de l'imam) ; Petit et l'imam d'abord prosternés tous les deux,
        # Petit relève la tête pendant « Celui qui lève la tête avant l'imam… » (début de l'écriture de la citation)
        ap = smooth((u - s.T_PERSO) / 0.45)
        t_leve = max(s.T_LEVE, s.t.get("ombre", s.DEF_OMBRE) - 1.9)
        p = round((0.12 + 0.76 * smooth((u - t_leve) / 1.4)) * 50) / 50
        eo = s._e("ombre", u, 1.2)
        zo = round(s.Z_OMBRE * (1 + 0.25 * eo) / 0.005) * 0.005
        if ap > 0.01:
            io = s._ombre(0.0, 1.0)
            _colle(im, io, s.IMAM_X + 30, s.Y_SOL - io.height / 2 + 6, ap * 0.7)
            so = s._ombre(p, zo)
            im.alpha_composite(_fade(so, ap), (int(s.OMBRE_X - so.width / 2), int(s.Y_SOL + 6 - so.height)))
        if eo > 0:
            im.alpha_composite(_fade(_vignette(W, H), 0.7 * eo))
        # les oreilles (sur l'ombre seulement)
        tr = s.t.get("oreilles")
        if tr is not None:
            q, yt, rx, yh = _dos_geo(p, zo)
            K = 6
            hr = 5.5 * zo * K
            hy = s.Y_SOL + 6 - K * 1 + yh * K
            g = smooth((u - tr) / 1.5)
            fade_ = 1 - smooth((u - tr - s.T_ESTOMPE) / 0.8)
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            s._oreilles(ImageDraw.Draw(lay), s.OMBRE_X, hy - hr, hr, g, fade_)
            im.alpha_composite(lay)
            # l'avertissement du côté de PETIT (au-dessus de lui, à gauche des oreilles), loin de « L'IMAM » :
            # la menace vise celui qui lève la tête, pas l'imam (Mouslim 427a)
            a_m = smooth((u - tr - 0.2) / 0.4) * fade_
            s._pose(im, s._lab("MENACE :", ORANGE, 46), 175, 450, a_m, maxw=290)
            s._pose(im, s._lab("TÊTE D'ÂNE", ORANGE, 46), 175, 505, a_m, maxw=290)
        if ap > 0.01:
            ic = s._imam_carte()
            im.alpha_composite(_fade(ic, ap), (int(s.IMAM_X - 20 * 6), int(s.IMAM_B - 28 * 6)))
            pc = s._petit_carte(round(p * 50) / 50)
            im.alpha_composite(_fade(pc, ap), (int(s.PETIT_X - 23 * 6), int(s.PETIT_B - 64 * 6)))
            s._pose(im, s._lab("L'IMAM", BLANC, 46), s.IMAM_X - 6, s.IMAM_B - 21 * s.IMAM_Z * 6 - 40, ap, maxw=300)
        im.alpha_composite(s._parchemin())
        s._ecrit(im, u)
        return im

    # ============================================================ la frise
    def _fig(s, P, style, z):
        cle = ("fig", style, z, tuple((round(v[0], 1), round(v[1], 1)) for v in P.values()))
        if cle not in s._cache:
            K = 6
            c = Px(48, 46, alpha=True)
            _profil(c, 1, 1, z, P, style)
            s._cache[cle] = c.img(K, rgba=True)
        return s._cache[cle]

    def _pose_fig(s, im, P, style, cx, sol, a=1.0, z=None):
        z = z or s.Z_F
        f = s._fig(P, style, z)
        x = int(cx - (1 + 20 * z) * 6)
        y = int(sol - (1 + 42 * z) * 6)
        if a > 0.01:
            im.alpha_composite(_fade(f, a), (x, y))

    def _image_suivre(s, u):
        W, H = s.W_, s.H_
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        fond = s._cache.get("fondf")
        if fond is None:
            fond = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(fond).rounded_rectangle([0, 0, W - 1, H - 1], 34, fill=(30, 34, 58, 236),
                                                   outline=(84, 92, 130, 255), width=4)
            s._cache["fondf"] = fond
        im.alpha_composite(fond)
        s._pose(im, s._lab("NE BOUGE JAMAIS AVANT L'IMAM", ROUGE_D, 50), 470, 62, 1.0, maxw=880)
        s._pose(im, s._lab("PÉCHÉ SI C'EST EXPRÈS", BLANC, 38), 470, 128, smooth((u - 0.2) / 0.35), maxw=700)
        # les noms des lignes
        s._pose(im, s._lab("L'IMAM", BLANC, 38), 100, s.Y_IMAM - 90, 1.0, maxw=190)
        s._pose(im, s._lab("TOI", (255, 150, 140), 44), 100, s.Y_TOI - 90, 1.0, maxw=190)
        d = ImageDraw.Draw(im)
        d.line([(200, s.Y_IMAM + 8), (W - 140, s.Y_IMAM + 8)], fill=(84, 92, 130, 255), width=4)
        d.line([(200, s.Y_TOI + 8), (W - 140, s.Y_TOI + 8)], fill=(84, 92, 130, 255), width=4)
        # 4 temps : INCLINÉ → REDRESSÉ (debout, obligatoire) → PROSTERNÉ → RELEVÉ (assis)
        seq = ((DEBOUT, INCLINE, "INCLINÉ"), (INCLINE, DEBOUT, "REDRESSÉ"), (DEBOUT, PROSTERNE, "PROSTERNÉ"),
               (PROSTERNE, ASSIS, "RELEVÉ"))
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        for i, ((P0, P1, nom), cx) in enumerate(zip(seq, s.COLS)):
            t0 = s.T_COL + s.DT_COL * i
            a = smooth((u - t0 + 0.25) / 0.3)
            if a <= 0.01:
                continue
            s._pose(im, s._lab(nom, (220, 224, 240), 34), cx, 198, a, maxw=168)
            ki = smooth((u - t0) / s.D_MV)                                  # l'imam fait son mouvement en entier…
            t_toi = t0 + s.D_MV + s.ATT                                     # … TOI ne commence qu'après son arrivée
            kt = smooth((u - t_toi) / s.D_MV)
            s._pose_fig(im, _mix(P0, P1, ki), "imam", cx, s.Y_IMAM, a)
            s._pose_fig(im, _mix(P0, P1, kt), "petit", cx, s.Y_TOI, a)
            ac = smooth((u - t_toi - s.D_MV) / 0.25)
            if ac > 0.01:
                _coche(dl, cx, s.Y_TOI + 50, 22, ac)
        # la version fausse : TOI AVANT (il se relève pendant que l'imam est encore prosterné) — côte à côte, même sol
        af = smooth((u - s.T_FAUX) / 0.3)
        if af > 0.01:
            zf = 0.62
            kf = smooth((u - s.T_FAUX - 0.2) / 0.45)
            s._pose(im, s._lab("TOI AVANT", (255, 150, 140), 38), 165, 792, af, maxw=220)
            s._pose_fig(im, PROSTERNE, "imam", 95, 935, af, z=zf)
            s._pose_fig(im, _mix(PROSTERNE, ASSIS, kf), "petit", 240, 935, af, z=zf)
            ax_ = smooth((u - s.T_CROIX) / 0.25)
            if ax_ > 0.01:                                                  # la croix à côté : TOI reste visible
                _croix(dl, 328, 880, 28, ax_)
        im.alpha_composite(lay)
        s._pose(im, s._lab("L'IMAM… PUIS TOI !", JAUNE, 58), 650, 880, smooth((u - s.T_FINAL) / 0.4), maxw=500)
        return im

    # ============================================================ la chute
    def _fond_colle(s):
        if "fondk" in s._cache:
            return s._cache["fondk"]
        K = 6
        W, H = s.W_ // K, s.H_ // K
        c = Px(W, H, alpha=True)
        _mur_tapis(c, W, H, 70, mihrab=(118, 13, 18))
        _debout_dos(c, 107, 76, 0.95, QAMIS, "kufi")                      # l'imam, devant, près du mihrab
        _debout_dos(c, 38, 104, 1.15, GRIS_Q, "kufi")
        _debout_dos(c, 70, 106, 1.15, VERT_T, "nu")
        _debout_dos(c, 150, 104, 1.15, BLEU_T, "nu")
        # Petit, DANS le rang, de dos, face au mihrab comme tous (la qibla), encore prosterné : seul en bas
        _dos(c, s.PK_X, s.PK_B, s.PK_Z, 0.0, SWEAT, JEAN, CHAUSSETTE, "casquette")
        im = c.img(K, rgba=True)
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 30, fill=255)
        a = np.minimum(np.array(im.getchannel("A")), np.array(m))
        im.putalpha(Image.fromarray(a))
        s._cache["fondk"] = im
        return im

    def _image_colle(s, u):
        im = s._fond_colle().copy()
        s._pose(im, s._lab("L'IMAM", BLANC, 42), 642, 132, 1.0, maxw=260)
        # gouttes de sueur (elles glissent lentement), au-dessus du dos de Petit (dessiné dans le fond, de dos)
        K = 6
        q, yt, rx, yh = _dos_geo(0.0, s.PK_Z)
        hx, hy = s.PK_X * K, (s.PK_B + yt) * K
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for j, (dx, dy, ph) in enumerate(((-62, -30, 0.0), (0, -42, 0.6), (62, -26, 1.2))):
            v = ((u + ph) % 1.8) / 1.8
            a = smooth(v / 0.2) * (1 - smooth((v - 0.7) / 0.3))
            x, y = int(hx + dx), int(hy + dy + 26 * v)
            A = int(255 * a)
            d.polygon([(x, y - 16), (x - 9, y + 2), (x + 9, y + 2)], fill=(30, 40, 70, A))
            d.ellipse([x - 10, y - 6, x + 10, y + 12], fill=(30, 40, 70, A))
            d.polygon([(x, y - 12), (x - 6, y + 2), (x + 6, y + 2)], fill=(170, 222, 255, A))
            d.ellipse([x - 7, y - 3, x + 7, y + 9], fill=(170, 222, 255, A))
        # le chrono gris : « +3 S… » → « +10 S… » (fondus doux), juste sous Petit, sur le tapis vide (loin des pieds
        # des autres fidèles)
        cx, cy = s.CHRONO
        d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(40, 40, 54, 230), outline=GRIS_C + (255,), width=6)
        ang = math.radians(-90 + 60 * u)
        d.line([(cx, cy), (cx + 22 * math.cos(ang), cy + 22 * math.sin(ang))], fill=GRIS_C + (255,), width=6)
        d.rectangle([cx - 8, cy - 46, cx + 8, cy - 38], fill=GRIS_C + (255,))
        im.alpha_composite(lay)
        etapes = ((0.0, "+3 S…"), (0.7, "+5 S…"), (1.4, "+8 S…"), (2.1, "+10 S…"))
        for i, (t_, txt) in enumerate(etapes):
            a = smooth((u - t_ + 0.15) / 0.3)
            if i + 1 < len(etapes):
                a *= 1 - smooth((u - etapes[i + 1][0] + 0.15) / 0.3)
            s._pose(im, s._lab(txt, GRIS_C, 48), cx + 190, cy, a, maxw=300)
        return im


# ---------------------------------------------------------------- branchement (via explique_0811.py)
CLES = ["imam", "ane", "âne"]


def _norm(m):
    return (m.lower().replace("é", "e").replace("è", "e").replace("ê", "e").replace("â", "a"))


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique_0811.ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""

    def dernier(cls, mode=None):
        return next((it["el"] for it in reversed(schema._visibles(t + 0.01))
                     if isinstance(it["el"], cls) and (mode is None or getattr(it["el"], "mode", None) == mode)), None)

    def u_de(el):
        return t - next(it["t_in"] for it in schema.items if it["el"] is el)

    if k == "imam":
        qui = mots[1].upper() if len(mots) > 1 else "PETIT"
        schema._ajoute(t, Imam(brut, qui if qui in ("PETIT", "GRAND") else "PETIT"))
    elif k == "ane":
        if sous in Ane.ETAPES:
            el = dernier(Ane, "carte")
            if el is None:
                el = Ane(brut, "carte")
                schema._ajoute(t, el)
            el.t[sous] = u_de(el)
        elif sous in ("suivre", "colle"):
            schema._ajoute(t, Ane(brut, sous))
        else:
            schema._ajoute(t, Ane(brut, "carte"))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "imam":
        return t + 2.0
    if k == "ane":
        return t + dict(ombre=1.4, oreilles=2.2, suivre=3.9, colle=2.8).get(sous, 1.6)
    return None
