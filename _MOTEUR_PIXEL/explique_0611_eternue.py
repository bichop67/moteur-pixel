# DÉMONSTRATION EN IMAGE DU 06/11/2026 — Short duo « Tu éternues ? Dis ça » (scénario islam_18_eternuement). Même
# principe que explique_0411b.py : le sens propre des hadiths, montré en grand, avec des mouvements doux (jamais de
# secousse ni de flash). Aucun prophète ni Compagnon dessiné : le hadith est une carte de TEXTE. Rien de liquide (ni
# goutte, ni morve) : seul le mot « ATCHOUM ! » sort, ÉTOUFFÉ, avec deux petits traits d'air.
# Retouches du 07/11/2026 (relecture religieuse) : éternuement étouffé dans la manche (la sunna : couvrir la bouche
# ET baisser la voix, Abou Dawoud 5029) ; la carte du rhume dit qui parle et la dou'a de guérison est à part, en blanc,
# « conseillée par les savants » (elle n'est pas dans le hadith) ; Petit commence « Yahdîkou… » avant le 2e éternuement
# (Boukhari 6224) ; Grand sourit (il ne rit pas pendant la parole du Prophète ﷺ). Finitions : les anciennes bulles
# montent plus lentement et libèrent la place avant la nouvelle ; à {rhume enrhume}, le « ATCHOUM ! » s'efface avec les
# bulles (le thermomètre prend sa place) ; la main de Grand sort en fondu de sous son cadre, sa manche va jusqu'au bord,
# sur un plan neuf ({rhume reponse|deux|enrhume} sans le {rhume} du début), pas de 1er « ATCHOUM ! ».
#   {atchoum PETIT}  accroche : le salon, Petit en très grand ; « aaah… » (la tête part en arrière, yeux plissés), son
#                    bras plié remonte : il éternue DANS SON COUDE (Abou Dawoud 5029) ; « ATCHOUM ! » naît contre la
#                    manche, petit, tassé et pâle, puis glisse doucement vers toi en grossissant ; puis il relève la
#                    tête, gêné (u = T0 = 0 : le mot « atchoum »)
#   {chaine}         les trois bulles qui se répondent (Boukhari 6224) : {chaine aime} la carte « ALLAH AIME
#                    L'ÉTERNUEMENT » (Boukhari 6223) ; {chaine hamd} Petit « AL-HAMDOULILLAH » ; {chaine reponse}
#                    Grand « YARHAMOUKA-LLÂH » ; {chaine retour} Petit « YAHDÎKOUMOULLÂH WA YOUSLIHOU BÂLAKOUM » ;
#                    {chaine rien} sans « Al-hamdoulillah » : sa bulle reste vide, pas de réponse (Mouslim 2992)
#   {rhume}          Petit enrhumé (nez rouge, mouchoirs) : « ATCHOUM ! » + « AL-HAMDOULILLAH ! » ; {rhume reponse}
#                    Grand « YARHAMOUKA-LLÂH ! » ; {rhume deux} la 2e fois : une petite bulle « YAHDÎKOU… », effacée
#                    par le 2e « ATCHOUM ! » (+0,6 s), puis « AL-HAMDOULILLAH ! » (les anciennes bulles montent et
#                    pâlissent) ; {rhume enrhume} thermomètre, Grand (souriant) tend un mouchoir ; carte « LE PROPHÈTE
#                    (PAIX ET SALUT SUR LUI) : « L'HOMME EST ENRHUMÉ » » (Mouslim 2993), puis plus bas, à part, en
#                    blanc : « QU'ALLAH TE GUÉRISSE » / « DOU'A CONSEILLÉE PAR LES SAVANTS » (an-Nawawi, al-Adhkâr)
# Branchement (comme explique_0411b) : CLES, ordre(schema, t, brut, mots, reste) et fin_anim(t, mots), en bas.
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import cast
import objets
import pxv
from px import Px
from pxv import smooth
from explique import _fade, _os, BLANC, JAUNE
from explique_0411 import OL, _peau, _grand
from explique_0411b import _Base, _bulle, _translucide, OR_

GRIS = (180, 184, 198)
GRIS_CLAIR = (206, 210, 228)       # la dou'a « conseillée par les savants » : en blanc et gris clair, jamais en or
ROUGE_DOUX = (246, 132, 120)
FOND_P = (98, 32, 50)              # bulles de Petit (bordeaux, comme son sweat)
FOND_G = (24, 80, 60)              # bulles de Grand (vert, comme son gilet)
FOND_CARTE = (28, 24, 46)
NEZ = ((226, 84, 84), (240, 118, 106), (250, 160, 146))


# ---------------------------------------------------------------- textes et bulles
def _bloc(lignes, serre=14, caches=()):
    """Lignes empilées et centrées, chacune avec sa couleur et sa taille : [(texte, couleur, taille), …] ; les lignes
    dont le numéro est dans caches gardent leur place mais ne sont pas dessinées (elles arrivent plus tard)."""
    ims = [pxv.big_title([(t_, c_)], size=z_) for (t_, c_, z_) in lignes]
    W_ = max(i.width for i in ims)
    out = Image.new("RGBA", (W_, sum(i.height for i in ims) - serre * (len(ims) - 1)), (0, 0, 0, 0))
    y = 0
    for j, i in enumerate(ims):
        if j not in caches:
            out.alpha_composite(i, ((W_ - i.width) // 2, y))
        y += i.height - serre
    return out


def _bulle_cote(tx, fond, cote="g", yq=None, pad=(28, 20), r=28, q=36, larg=None, haut=None):
    """Bulle sombre à bord blanc (comme explique_0411b._bulle) autour de l'image texte tx ; la pointe sort sur le côté
    (cote "g" : vers un perso à gauche, "d" : à droite) à la hauteur yq (pixels depuis le haut de la bulle) ;
    larg / haut = taille imposée (texte centré)."""
    w = max(larg or 0, tx.width + 2 * pad[0])
    h = max(haut or 0, tx.height + 2 * pad[1])
    b = Image.new("RGBA", (w + q, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    yq = int(h * 0.42) if yq is None else int(max(r + 10, min(h - r - 30, yq)))
    x0 = q if cote == "g" else 0
    xb = x0 if cote == "g" else w - 1                                       # le bord d'où sort la pointe
    sg = -1 if cote == "g" else 1
    pointe = (xb + sg * (q - 2), yq + 16)
    d.polygon([(xb - sg * 10, yq - 22), (xb - sg * 10, yq + 20), pointe], fill=(255, 255, 255, 255))
    d.rounded_rectangle([x0, 0, x0 + w - 1, h - 1], r, fill=(*fond, 245), outline=(255, 255, 255, 255), width=6)
    d.polygon([(xb - sg * 8, yq - 13), (xb - sg * 8, yq + 11), (xb + sg * (q - 14), yq + 13)], fill=(*fond, 245))
    b.alpha_composite(tx, (x0 + (w - tx.width) // 2, (h - tx.height) // 2))
    return b


def _contour_rrect(x0, y0, x1, y1, r, n=10):
    """Points du tour d'un rectangle arrondi (dans le sens des aiguilles d'une montre)."""
    pts = []
    for (cx, cy, a0) in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts.append(pts[0])
    return pts


def _pointilles(d, pts, col, ep=6, tiret=24, trou=14):
    """Trace une ligne brisée en pointillés (tirets de `tiret` pixels)."""
    fin = []
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(xb - xa, yb - ya)))
        fin += [(xa + (xb - xa) * i / n, ya + (yb - ya) * i / n) for i in range(n)]
    fin.append(pts[-1])
    cur = []
    for i, p in enumerate(fin):
        if i % (tiret + trou) < tiret:
            cur.append(p)
        else:
            if len(cur) > 1:
                d.line(cur, fill=col, width=ep)
            cur = []
    if len(cur) > 1:
        d.line(cur, fill=col, width=ep)


def _bulle_vide(w, h, cote="d", yq=None, col=(226, 226, 236), r=28, q=36):
    """La place d'une bulle qui ne vient pas : contour en pointillés (et sa pointe), rien dedans."""
    b = Image.new("RGBA", (w + q, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    x0 = q if cote == "g" else 0
    yq = int(h * 0.42) if yq is None else int(max(r + 10, min(h - r - 30, yq)))
    xb = x0 + 4 if cote == "g" else x0 + w - 5
    sg = -1 if cote == "g" else 1
    contour = _contour_rrect(x0 + 4, 4, x0 + w - 5, h - 5, r)
    queue = [(xb + sg * 2, yq - 8), (xb + sg * (q - 8), yq + 14), (xb + sg * 2, yq + 14)]
    for c_, ep in (((20, 16, 30, 190), 12), ((*col, 255), 6)):
        _pointilles(d, contour, c_, ep=ep)
        _pointilles(d, queue, c_, ep=ep, tiret=12, trou=8)
    return b


def _carte(tx, fond=FOND_CARTE, bord=OR_, pad=(46, 30)):
    """Carte sobre (sombre, fin liseré) autour d'un bloc de texte."""
    w, h = tx.width + 2 * pad[0], tx.height + 2 * pad[1]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=(*fond, 240), outline=(14, 10, 22, 255), width=8)
    d.rounded_rectangle([12, 12, w - 13, h - 13], 22, outline=(*bord, 255), width=4)
    im.alpha_composite(tx, ((w - tx.width) // 2, pad[1]))
    return im


# ---------------------------------------------------------------- persos
def _manche(who):
    """Les tons de la manche du perso (sweat de Petit, qamis de Grand…) et s'il a un poignet côtelé."""
    r = cast.CAST[who]
    return cast.tons(r["couleur"]), r["haut"] in ("sweat", "pull", "survet", "doudoune")


def _retouche(a, r, g, plisse=False, nez=False):
    """Retouches du visage sur le dessin du perso (tableau RGBA, coordonnées du sprite) : yeux plissés « > < » (il va
    éternuer) ; nez rouge (enrhumé)."""
    S = r["_peau"]
    ex, ey = g.hd["ex"], g.y0 + g.hd["ey"]
    if plisse:
        yeux = {tuple(cast.EYE), tuple(cast.WHITE), (90, 90, 120)}
        for x0 in (ex, ex + 5):
            for y in range(ey - 1, ey + 4):
                for x in range(x0 - 1, x0 + 2):
                    if tuple(int(v) for v in a[y, x, :3]) in yeux:
                        a[y, x] = (*S["b"], 255)
        for (x, y) in ((ex - 1, ey), (ex, ey + 1), (ex + 1, ey + 1), (ex - 1, ey + 2),
                       (ex + 6, ey), (ex + 5, ey + 1), (ex + 4, ey + 1), (ex + 6, ey + 2)):
            a[y, x] = (*cast.EYE, 255)
    if nez:                                                      # un petit nez rouge qui dépasse d'un pixel
        nx, ny = g.hd["nose"]
        ny += g.y0
        for (x, y, col) in ((nx, ny, NEZ[1]), (nx + 1, ny, NEZ[0]), (nx + 1, ny - 1, NEZ[2]), (nx + 2, ny - 1, NEZ[0]),
                            (nx + 2, ny, NEZ[0])):
            a[y, x] = (*col, 255)
        for (x, y) in ((nx + 3, ny - 1), (nx + 3, ny), (nx + 2, ny + 1), (nx + 2, ny - 2)):
            if a[y, x, 3] == 0 or tuple(int(v) for v in a[y, x, :3]) == OL:
                a[y, x] = (*OL, 255)


def _buste_a(who, face="neutre", plisse=False, nez=False, **kw):
    """Tête et épaules du perso (tableau RGBA, même cadrage que explique_0411._buste), avec les retouches."""
    r = cast.CAST[who]
    a = cast.dessine(r, "neutre", face, **kw).a.copy()
    g = cast.geo(r)
    _retouche(a, r, g, plisse, nez)
    zone = a[max(0, g.y0 - 14):g.y0 + 2, 8:36, 3]
    rows = np.where(zone.max(axis=1) > 0)[0]
    top = min(max(0, g.y0 - 14) + (int(rows[0]) if len(rows) else 14), g.y0 - 1)
    return a[top: g.y0 + 26, 8:36].copy()


_POSE_SANS = "_eternue_sans_bras"


def _sprite_sans_bras(who, face, **kw):
    """Le perso en entier SANS son bras du fond (on le dessine nous-mêmes, plié devant le visage) : une pose
    temporaire, retirée aussitôt, où ce bras se réduit à l'épaule (caché derrière le corps)."""
    r = cast.CAST[who]
    g = cast.geo(r)
    cast.POSES[_POSE_SANS] = ((("t", g.sr, g.ay - g.y0), ("t", g.sr, g.ay - g.y0), "poing", 0), cast.NN)
    try:
        a = cast.dessine(r, _POSE_SANS, face, objet="", **kw).a.copy()
    finally:
        cast.POSES.pop(_POSE_SANS, None)
    return a, g


def _bras(c, S, E, W, who, ep=5.0, plie=True):
    """Un bras plié (dessin Px, en cellules) : épaule S → coude E → poignet W, manche et poing. plie : l'avant-bras
    passe devant le haut du bras (pli du coude) ; sinon le bras est d'un seul tenant."""
    tons, cote = _manche(who)
    p = _peau(who)
    L = math.hypot(W[0] - E[0], W[1] - E[1]) or 1.0
    ux, uy = (W[0] - E[0]) / L, (W[1] - E[1]) / L
    haut = _os(c, S[0], S[1], E[0], E[1], ep + 0.6)
    av = _os(c, E[0], E[1], W[0], W[1], ep)
    if plie:
        c.shape(haut, tons["b"], shade=tons["s"], light=tons["h"], band=1, olcol=OL)
        c.shape(av, tons["b"], shade=tons["s"], light=tons["h"], band=1, olcol=OL)
        for d_ in (1.0, 2.4):                                                   # les plis au creux du coude
            x, y = E[0] + ux * d_, E[1] + uy * d_
            c.line(x, y + 0.6, x - uy * 1.6, y + ux * 1.6 + 1.6, tons["s"])
    else:
        c.shape(haut | av, tons["b"], shade=tons["s"], light=tons["h"], band=1, olcol=OL)
    if cote:                                                                    # le poignet côtelé du sweat
        x0, y0 = W[0] - ux * 2.0, W[1] - uy * 2.0
        pg = _os(c, x0, y0, W[0], W[1], ep - 0.6) & av
        c.fill(pg, tons["s"])
        for j in (0.5, 1.4):
            x, y = x0 + ux * j, y0 + uy * j
            c.line(x - uy * 1.6, y + ux * 1.6, x + uy * 1.6, y - ux * 1.6, tons["d"])
    F = (W[0] + ux * 1.5, W[1] + uy * 1.5)                                        # le poing
    pm = c.mask_ell(F[0], F[1], ep * 0.44, ep * 0.48)
    c.shape(pm, p["b"], shade=p["s"], light=p["h"], band=1, olcol=OL)
    for j in (-0.8, 0.6):                                                         # les doigts repliés
        x, y = F[0] + ux * 0.9 - uy * j, F[1] + uy * 0.9 + ux * j
        c.px(x, y, p["s"])


# le bras du fond, plié devant le bas du visage (en cellules du buste, 28 × 27) : il éternue dans son coude. Le haut
# du bras monte tout droit devant l'épaule, l'avant-bras barre le nez et la bouche, le poing contre la joue.
COUDE = dict(S=(22.5, 36.0), E=(23.5, 18.3), W=(13.0, 17.4))


def _avec_bras(a, who):
    """Le buste (tableau) avec le bras plié devant le bas du visage (coupé au bord du buste)."""
    h_, w_ = a.shape[:2]
    c = Px(w_, h_, alpha=True)
    _bras(c, COUDE["S"], COUDE["E"], COUDE["W"], who)
    out = a.copy()
    out[c.al, :3] = c.a[c.al]
    out[c.al, 3] = 255
    return out


def _avatar(who, face="neutre", miroir=False, eternue=False, k=6, **kw):
    """Petit buste dans un cadre arrondi à sa couleur (comme une photo de profil) ; eternue = yeux plissés et coude
    devant le visage ; miroir = tourné vers la gauche."""
    r = cast.CAST[who]
    a = _buste_a(who, "triste" if eternue else face, plisse=eternue, **kw)
    if eternue:
        a = _avec_bras(a, who)
    if miroir:
        a = a[:, ::-1].copy()
    Wc, Hc = 34, 32
    c = Px(Wc, Hc, alpha=True)
    m_out = c.mask_rrect(1, 1, Wc - 1, Hc - 1, 6)
    m_in = c.mask_rrect(2, 2, Wc - 2, Hc - 2, 5)
    cadre = tuple(r["cadre"])
    c.fill(m_out, cadre)
    c.vgrad(m_in, 2, Hc - 2, tuple(int(v * 0.42 + 26) for v in cadre), tuple(int(v * 0.2 + 16) for v in cadre),
            steps=4)
    ox, oy = 3, 3
    h_, w_ = a.shape[:2]
    vis = (a[..., 3] > 0) & m_in[oy:oy + h_, ox:ox + w_]
    c.a[oy:oy + h_, ox:ox + w_][vis] = a[..., :3][vis]
    c.al[oy:oy + h_, ox:ox + w_][vis] = True
    c.outline(m_out, OL)
    return c.img(k, rgba=True)


AV_BOUCHE_Y = 3 + 18               # la hauteur de la bouche dans le cadre (cellules)


# ---------------------------------------------------------------- petits décors
def _boite_mouchoirs():
    c = Px(20, 19, alpha=True)
    boite = c.mask_rrect(1, 7, 19, 18, 2)
    c.shape(boite, (96, 168, 214), shade=(66, 126, 178), light=(146, 204, 238), band=1, olcol=OL)
    c.fill(c.mask_rect(2, 7, 18, 9) & boite, (150, 206, 238))
    for (x, y) in ((4, 12), (8, 15), (12, 11), (15, 14)):                       # petites fleurs
        c.fill(c.mask_rect(x, y, x + 2, y + 2), (236, 244, 252))
        c.px(x + 1, y + 1, (250, 200, 90))
    c.fill(c.mask_ell(10, 8, 4, 1.1), (40, 62, 96))                             # la fente
    mo = c.mask_poly([(6, 8), (6, 4), (8, 1), (10, 3), (12, 0), (14, 3), (14, 8)])
    c.shape(mo, (250, 250, 252), shade=(206, 214, 232), light=(255, 255, 255), band=1, olcol=OL)
    c.line(9, 3, 10, 7, (220, 226, 240))
    return c


def _petite_table():
    c = Px(22, 24, alpha=True)
    plateau = c.mask_rrect(0, 0, 22, 4, 2)
    c.shape(plateau, (178, 122, 78), shade=(138, 92, 58), light=(208, 152, 102), band=1, olcol=OL)
    for x in (2, 16):
        pied = c.mask_rect(x, 4, x + 4, 24)
        c.shape(pied, (152, 102, 64), shade=(118, 78, 48), light=(182, 128, 84), band=1, olcol=OL)
    tab = c.mask_rect(2, 15, 20, 17)
    c.shape(tab, (166, 112, 72), shade=(128, 86, 54), band=1, olcol=OL)
    return c


def _main_mouchoir(who, long_=46):
    """La main de Grand qui tend un mouchoir plié (la manche part vers la droite, sous son cadre ; long_ = largeur du
    dessin en cellules : la manche va jusqu'au bout)."""
    tons, _ = _manche(who)
    p = _peau(who)
    c = Px(long_, 24, alpha=True)
    manche = c.mask_rrect(17, 11, long_ + 6, 23, 4)
    c.shape(manche, tons["b"], shade=tons["s"], light=tons["h"], band=1, olcol=OL)
    c.fill(c.mask_rect(17, 12, 19, 22) & manche, tons["s"])
    mo = c.mask_poly([(2, 4), (12, 1), (15, 11), (5, 14)])                     # le mouchoir (un carré plié)
    c.shape(mo, (250, 250, 252), shade=(204, 212, 230), light=(255, 255, 255), band=1, olcol=OL)
    c.line(4, 8, 13, 5, (214, 220, 236))
    c.fill(c.mask_poly([(10, 2), (12, 1), (13, 4)]) & mo, (226, 232, 246))     # le coin replié
    main = c.mask_poly([(6, 13), (11, 11), (18, 12), (19, 20), (15, 22), (8, 21), (5, 17)])
    c.shape(main, p["b"], shade=p["s"], light=p["h"], band=1, olcol=OL)
    for x in (9, 12, 15):                                                        # les doigts repliés
        c.line(x, 15, x, 19, p["s"])
    pouce = c.mask_rrect(10, 8, 15, 13, 2)                                        # le pouce tient le mouchoir
    c.shape(pouce, p["b"], shade=p["s"], light=p["h"], band=1, olcol=OL)
    return c


# ---------------------------------------------------------------- {atchoum PETIT} {chaine …} {rhume …}
class Eternue(_Base):
    """{atchoum PETIT} : accroche, le salon ; Petit en très grand fait « aaah… » (la tête part en arrière, yeux
    plissés), son bras plié remonte et il éternue DANS SON COUDE (Abou Dawoud 5029) ; « ATCHOUM ! » naît étouffé
    contre la manche puis glisse doucement vers toi, il relève la tête, gêné. {chaine} : les bulles qui se répondent
    (Boukhari 6223 · 6224 · Mouslim 2992) ; étapes {chaine aime|hamd|reponse|retour|rien}. {rhume} : Petit enrhumé ;
    étapes {rhume reponse|deux|enrhume} (Mouslim 2993 ; la dou'a de guérison : an-Nawawi)."""
    ETAPES = ("aime", "hamd", "reponse", "retour", "rien", "deux", "enrhume")
    ETAPES_MODE = {"atchoum": (), "chaine": ("aime", "hamd", "reponse", "retour", "rien"),
                   "rhume": ("reponse", "deux", "enrhume")}
    T0 = 0.0                          # accroche : l'instant du « atchoum » (secondes depuis la balise)
    KB = 18                           # accroche : échelle du grand buste
    BX, BY = 228, 900 - 27 * 18       # accroche : coin du buste au repos (pixels)
    PIV = (14, 36)                    # accroche : il se penche autour de ce point (cellules, sous le cadre)
    ATCH_NE = (600, 792)              # accroche : « ATCHOUM ! » naît ici, contre le bas de la manche (centre, pixels)…
    ATCH_FIN = (512, 818)             # … et glisse doucement jusqu'ici, vers toi (vers le bas), en grossissant
    ATCH_K = (0.6, 0.95)              # … de 60 % à 95 % de sa taille (136 px)
    AVK = 6                           # petits bustes encadrés (34 × 32 cellules)
    KS = 7                            # rhume : Petit en entier
    SX, SY = 290, 945                 # rhume : milieu de ses pieds (pixels)
    PALIER = 135                      # rhume : de combien une bulle monte quand une autre arrive
    T_YA = 1.2                        # rhume : {rhume deux} « Yahdîkou… », puis le 2e « atchoum » 1,2 s plus tard
    #                                   (calé sur la vraie voix d'ISL18 : « atchoum » à +1,25 s, « Al-hamdoulillah » à +2,3 s)

    def __init__(s, cmd, mode="chaine", who="PETIT", t0=None):
        super().__init__(cmd)
        s.mode = mode if mode in s.ETAPES_MODE else "chaine"
        s.who = who if who in cast.CAST else "PETIT"
        s.negatif = s.mode == "atchoum"
        if t0 is not None:                                                       # {atchoum PETIT 0.7} : le « atchoum »
            s.T0 = float(t0)                                                     # 0,7 s après la balise

    def sons_el(s):
        if s.mode == "atchoum":
            return [(s.T0, "tr_whoosh_doux", 0.025, None)]
        if s.mode == "chaine":
            evts = (("aime", "sa_scintillement", 0.04, 0.0), ("reponse", "sa_ting", 0.03, 0.05),
                    ("rien", "tr_whoosh_doux", 0.02, 0.0))
            out = []
        else:                                                                    # (le 2e « atchoum » : T_YA après deux)
            evts = (("deux", "tr_whoosh_doux", 0.02, s.T_YA), ("enrhume", "sa_ting", 0.03, 0.1))
            out = [] if s._neuf() else [(0.0, "tr_whoosh_doux", 0.02, None)]
        for nom, son, g, dec in evts:
            if nom in s.t:
                out.append((s.t[nom] + dec, son, g, None))
        return out

    def image(s, u):
        if s.mode == "atchoum":
            return s._image_atchoum(u)
        if s.mode == "rhume":
            return s._image_rhume(u)
        return s._image_chaine(u)

    def _garde(s, cle, f):
        if cle not in s._cache:
            s._cache[cle] = f()
        return s._cache[cle]

    def _av(s, qui, face, eternue=False):
        """Petit buste encadré : qui = "P" (Petit, tourné vers la droite) ou "G" (Grand, tourné vers la gauche)."""
        who = "PETIT" if qui == "P" else "GRAND"
        return s._garde(("av", qui, face, eternue),
                        lambda: _avatar(who, face, miroir=qui == "G", eternue=eternue, k=s.AVK,
                                        blush=face == "gene"))

    # ------------------------------------------------------------ l'accroche
    def _salon(s):
        if "salon" in s._cache:
            return s._cache["salon"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        c.vgrad(tout_, 0, H, (246, 212, 162), (226, 176, 126), steps=5)           # le mur, chaud
        for x in range(0, W, 14):                                                # papier peint à rayures
            c.dither(tout_ & c.mask_rect(x + 9, 0, x + 13, H), (234, 192, 140), 0.5)
        cadre = c.mask_rect(14, 18, 58, 88) & tout_                              # la fenêtre : un soir doux
        c.shape(cadre, (250, 244, 232), shade=(212, 202, 190), light=(255, 255, 255), band=1, olcol=OL)
        vitre = c.mask_rect(17, 21, 55, 85)
        c.vgrad(vitre, 21, 85, (112, 116, 196), (252, 178, 132), steps=6)
        c.fill(c.mask_ell(44, 76, 7, 7) & vitre, (255, 214, 150))
        c.fill(c.mask_ell(44, 76, 4.5, 4.5) & vitre, (255, 236, 196))
        toits = c.mask_poly([(17, 86), (17, 74), (24, 74), (24, 69), (31, 69), (31, 76), (37, 76), (37, 67),
                             (46, 67), (46, 78), (55, 78), (55, 86)]) & vitre
        c.fill(toits, (98, 74, 116))
        for (x, y) in ((19, 77), (26, 72), (33, 79), (40, 70), (40, 74), (49, 81)):
            c.fill(c.mask_rect(x, y, x + 2, y + 2) & toits, (255, 214, 120))
        for (x, y) in ((22, 26), (31, 31), (50, 28), (26, 40)):
            c.px(x, y, (236, 236, 255))
        c.fill(c.mask_rect(35, 21, 37, 85) | c.mask_rect(17, 50, 55, 52), (250, 244, 232))   # les croisillons
        c.fill(c.mask_rect(10, 88, 62, 91), (236, 226, 212))                    # le rebord
        c.outline(c.mask_rect(10, 88, 62, 91), OL)
        for (x0, x1) in ((6, 17), (55, 66)):                                     # les rideaux
            rid = c.mask_rect(x0, 12, x1, 97) & tout_
            c.shape(rid, (212, 98, 72), shade=(166, 66, 50), light=(238, 140, 100), band=1, olcol=OL)
            for x in range(x0 + 3, x1 - 1, 3):
                c.fill(c.mask_rect(x, 14, x + 1, 97) & rid, (186, 78, 58))
        c.fill(c.mask_rect(2, 9, 70, 12), (122, 86, 60))                        # la tringle
        c.outline(c.mask_rect(2, 9, 70, 12), OL)
        pied = c.mask_rect(150, 60, 153, 100)                                    # le lampadaire (à droite)
        c.shape(pied, (90, 76, 70), shade=(64, 54, 50), light=(130, 112, 104), band=1, olcol=OL)
        abat = c.mask_poly([(141, 42), (162, 42), (167, 61), (136, 61)])
        c.shape(abat, (252, 232, 178), shade=(232, 196, 130), light=(255, 248, 220), band=1, olcol=OL)
        c.fill(c.mask_rect(137, 59, 167, 61) & abat, (255, 246, 214))
        dos = c.mask_rrect(4, 98, 166, 160, 7) & tout_                           # le canapé
        c.shape(dos, (64, 140, 150), shade=(44, 106, 118), light=(98, 174, 180), band=2, olcol=OL)
        for (x0, x1) in ((10, 86), (84, 160)):                                   # les coussins du dossier
            co = c.mask_rrect(x0, 106, x1, 160, 6) & tout_
            c.shape(co, (76, 156, 164), shade=(52, 120, 130), light=(112, 188, 192), band=1, olcol=OL)
        for (x0, x1) in ((-4, 14), (156, 174)):                                  # les accoudoirs
            ac = c.mask_rrect(x0, 104, x1, 160, 6) & tout_
            c.shape(ac, (56, 126, 138), shade=(40, 96, 108), light=(90, 160, 168), band=1, olcol=OL)
        cous = c.mask_ell(26, 118, 11, 10)                                       # un petit coussin moutarde
        c.shape(cous, (234, 184, 76), shade=(196, 144, 52), light=(250, 214, 120), band=1, olcol=OL)
        c.fill(c.mask_rect(25, 109, 27, 128) & cous, (210, 160, 60))
        im = c.img(s.K, rgba=True)
        lum = (255, 228, 156)                                                    # la lumière chaude de la lampe
        lay = Image.new("RGBA", im.size, (*lum, 0))                              # (fond de la même couleur : le flou
        ld = ImageDraw.Draw(lay)                                                 # ne fait pas d'anneau sombre)
        ld.ellipse([151 * 6 - 210, 52 * 6 - 150, 151 * 6 + 210, 52 * 6 + 230], fill=(*lum, 80))
        ld.polygon([(137 * 6, 61 * 6), (166 * 6, 61 * 6), (186 * 6, 102 * 6), (116 * 6, 102 * 6)], fill=(*lum, 60))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(34)))
        s._cache["salon"] = im
        return im

    def _gros_buste(s, visage, ang):
        """Le grand buste (prolongé sous le cadre pour pencher sans trou), tourné de ang degrés autour de PIV ;
        visage : "aah" (yeux plissés, bouche ouverte) ou "gene"."""
        q = round(ang * 2) / 2
        cle = ("gb", visage, q)
        if cle in s._cache:
            return s._cache[cle]
        base = s._cache.get(("gb0", visage))
        if base is None:
            if visage == "aah":
                a = _buste_a(s.who, "triste", plisse=True, talk=True, bouche="A")
            else:
                a = _buste_a(s.who, "gene", blush=True)
            a = np.vstack([a, np.repeat(a[-1:], 6, axis=0)])
            base = s._cache[("gb0", visage)] = _grand(Image.fromarray(a, "RGBA"), s.KB)
        M = 100
        can = Image.new("RGBA", (base.width + 2 * M, base.height + 2 * M), (0, 0, 0, 0))
        can.paste(base, (M, M))
        piv = (s.PIV[0] * s.KB + M, s.PIV[1] * s.KB + M)
        if abs(q) > 0.01:
            can = can.rotate(q, resample=Image.NEAREST, center=piv)
        vieux = [k_ for k_ in s._cache if isinstance(k_, tuple) and k_[0] == "gb"]
        if len(vieux) > 24:
            for k_ in vieux[:8]:
                s._cache.pop(k_, None)
        s._cache[cle] = (can, piv)
        return s._cache[cle]

    def _image_atchoum(s, u):
        KB = s.KB
        im = s._salon().copy()
        W_, H_ = im.size
        v = u - s.T0
        lean = smooth((v + 0.95) / 0.75)                                         # « aaah… » : il part en arrière
        dip = smooth((v + 0.06) / 0.28)                                          # « atchoum » : dans son coude
        rel = smooth((v - 0.55) / 0.5)                                           # il relève la tête, gêné
        ang = 7.0 * lean * (1 - dip) - 5.0 * dip * (1 - rel)
        dy = -10 * lean * (1 - dip) + 14 * dip * (1 - rel) + 3 * math.sin(u * 2.2)    # + il respire
        bus, piv = s._gros_buste("aah" if v < 0.6 else "gene", ang)
        px_, py_ = s.BX + s.PIV[0] * KB, s.BY + s.PIV[1] * KB
        im.alpha_composite(bus, (int(px_ - piv[0]), int(py_ - piv[1] + dy)))
        e_b = smooth((v + 0.42) / 0.3) * (1 - smooth((v - 0.72) / 0.4))          # le bras plié monte, puis redescend
        if e_b > 0.001:
            br = s._garde("gbras", s._bras_grand)
            im.alpha_composite(br, (int(s.BX + KB * (1 - e_b)), int(s.BY + 20 * KB * (1 - e_b))))
        if 0 <= v < 0.5:                                    # étouffé : à peine deux petits traits d'air au coude
            f = smooth(v / 0.4)
            a = smooth(v / 0.1) * (1 - smooth((v - 0.18) / 0.27))
            cx, cy = s.BX + 26 * KB, s.BY + 18 * KB

            def air(d):
                for ang_ in (-42, -14):
                    t_ = math.radians(ang_)
                    r0 = 42 + 26 * f
                    r1 = r0 + 30
                    pts = [(cx + r0 * math.cos(t_), cy + r0 * math.sin(t_)),
                           (cx + r1 * math.cos(t_), cy + r1 * math.sin(t_))]
                    d.line(pts, fill=(20, 16, 30, int(190 * a)), width=13)
                    d.line(pts, fill=(255, 255, 255, int(225 * a)), width=6)
            _translucide(im, air)
        if v >= 0:                       # « ATCHOUM ! » étouffé : il naît contre la manche, petit, tassé, un peu pâle,
            e = smooth((v - 0.12) / 0.8)                 # puis glisse doucement vers toi en grossissant (sans claquer)
            k = s.ATCH_K[0] + (s.ATCH_K[1] - s.ATCH_K[0]) * e
            tas = 0.8 + 0.2 * smooth((v - 0.05) / 0.6)                          # les lettres tassées se déplient
            tx = s._atchoum(round(k * 200) / 200, round(k * tas * 200) / 200)
            a = smooth(v / 0.2) * (0.7 + 0.3 * smooth((v - 0.35) / 0.6))       # pâle (70 %) puis net
            (x0, y0), (x1, y1) = s.ATCH_NE, s.ATCH_FIN
            x = x0 + (x1 - x0) * e
            y = y0 + (y1 - y0) * e + 3 * math.sin(v * 2.4) * smooth((v - 0.9) / 0.4)
            im.alpha_composite(_fade(tx, a), (int(x - tx.width / 2), int(y - tx.height / 2)))
        return im

    def _atchoum(s, kx, ky):
        """« ATCHOUM ! » à kx de sa largeur et ky de sa hauteur (en cache, seulement les dernières tailles)."""
        cle = ("atch", kx, ky)
        if cle not in s._cache:
            base = s._garde("atch0", lambda: pxv.big_title([("ATCHOUM !", BLANC)], size=136))
            vieux = [k_ for k_ in s._cache if isinstance(k_, tuple) and k_[0] == "atch"]
            for k_ in vieux[:-10]:
                s._cache.pop(k_, None)
            s._cache[cle] = base.resize((max(1, int(base.width * kx)), max(1, int(base.height * ky))), Image.LANCZOS)
        return s._cache[cle]

    def _bras_grand(s):
        c = Px(34, 46, alpha=True)
        _bras(c, COUDE["S"], COUDE["E"], COUDE["W"], s.who, ep=5.6)
        return c.img(s.KB, rgba=True)

    # ------------------------------------------------------------ {chaine …}
    def _chaine_objets(s):
        """Les bulles, la carte et les places (en cache)."""
        if "ch" in s._cache:
            return s._cache["ch"]
        W_, H_ = 1020, 960
        o = {}
        o["carte"] = _carte(_bloc([("LE PROPHÈTE", BLANC, 46), ("(PAIX ET SALUT SUR LUI) :", BLANC, 44),
                                   ("« ALLAH AIME", OR_, 84), ("L'ÉTERNUEMENT »", OR_, 84)], serre=16))
        av_w, av_h = 34 * s.AVK, 32 * s.AVK
        o["xP"], o["xG"] = 4, W_ - av_w - 4
        by = AV_BOUCHE_Y * s.AVK + s.AVK // 2 - 16                               # la pointe vise la bouche du buste
        textes = (("P", [("AL-HAMDOULILLAH", OR_, 56), ("LOUANGE À ALLAH", BLANC, 44)], (28, 20)),
                  ("G", [("YARHAMOUKA-LLÂH", OR_, 56), ("QU'ALLAH TE FASSE", BLANC, 44), ("MISÉRICORDE", BLANC, 44)],
                   (28, 20)),
                  ("P", [("YAHDÎKOUMOULLÂH", OR_, 48), ("WA YOUSLIHOU BÂLAKOUM", OR_, 48),
                         ("QU'ALLAH VOUS GUIDE", BLANC, 44), ("ET AMÉLIORE VOTRE ÉTAT", BLANC, 44)], (22, 20)))
        bulles = [(qui, _bulle_cote(_bloc(lg), FOND_P if qui == "P" else FOND_G, "g" if qui == "P" else "d",
                                    yq=by, pad=pad)) for (qui, lg, pad) in textes]
        hs = [max(b.height, av_h) for _, b in bulles]
        M = 14
        gap = (H_ - 2 * M - sum(hs)) / 2
        ys = [M, M + hs[0] + gap, M + hs[0] + hs[1] + 2 * gap]
        o["rangs"] = []
        for (qui, b), y in zip(bulles, ys):
            x = o["xP"] + av_w + 2 if qui == "P" else o["xG"] - 2 - b.width
            o["rangs"].append(dict(qui=qui, b=b, x=x, y=y))
        # {chaine rien} : Petit éternue (petit « ATCHOUM » gris), sa bulle reste vide ; à la place de la réponse de
        # Grand, des pointillés et « PAS D'AL-HAMDOULILLAH / PAS DE RÉPONSE »
        b1, b2 = bulles[0][1], bulles[1][1]
        o["atch"] = pxv.big_title([("ATCHOUM", GRIS)], size=52)
        o["vide"] = _bulle_cote(_bloc([("…", (232, 232, 242), 110)]), FOND_P, "g", yq=by - 30,
                                larg=b1.width - 36, haut=170)
        o["videG"] = _bulle_vide(b2.width - 36, 170, "d", yq=by - 4)
        o["lab"] = _bloc([("PAS D'AL-HAMDOULILLAH", ROUGE_DOUX, 48), ("PAS DE RÉPONSE", ROUGE_DOUX, 48)])
        hP = 64 + 170                                                             # rang de Petit : ATCHOUM, bulle vide
        hG = 170 + 22 + o["lab"].height                                           # rang de Grand : pointillés, texte
        y0 = (H_ - hP - 40 - hG) / 2
        o["rien"] = dict(yP=y0, yG=y0 + hP + 40)
        s._cache["ch"] = o
        return o

    def _image_chaine(s, u):
        W_, H_ = 1020, 960
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        o = s._chaine_objets()
        t = s.t
        tr = t.get("rien")
        apres = [t[n] for n in ("hamd", "reponse", "retour", "rien") if n in t]
        t_aime = t.get("aime", 0.0 if not apres or min(apres) > 0.3 else None)
        if t_aime is not None:                                                   # la carte du hadith
            a = smooth((u - t_aime) / 0.45)
            if apres:
                a *= 1 - smooth((u - min(apres)) / 0.35)
            if a > 0.01:
                ca = o["carte"]
                im.alpha_composite(_fade(ca, a), (int(W_ / 2 - ca.width / 2), int(340 - ca.height / 2 + 16 * (1 - a))))
        er = smooth((u - tr - 0.12) / 0.5) if tr is not None else 0.0             # {chaine rien} : tout s'efface,
        ar = 1 - smooth((u - tr) / 0.3) if tr is not None else 1.0                # puis on se recentre
        rp, rg = o["rangs"][0], o["rangs"][1]
        yP = rp["y"] + (o["rien"]["yP"] + 64 - 30 - rp["y"]) * er                 # le buste de Petit, puis de Grand
        yG = rg["y"] + (o["rien"]["yG"] - rg["y"]) * er
        for i, (nom, r_) in enumerate(zip(("hamd", "reponse", "retour"), o["rangs"])):
            t_i = t.get(nom)
            e_i = smooth((u - t_i - 0.2) / 0.35) if t_i is not None else 0.0          # après la carte
            a_b = e_i * ar
            if a_b > 0.01:                                                        # la bulle
                sg = -1 if r_["qui"] == "P" else 1
                im.alpha_composite(_fade(r_["b"], a_b), (int(r_["x"] + sg * 30 * (1 - e_i)), int(r_["y"])))
            if i == 2:                                                            # le 3e buste s'en va avec sa bulle
                if a_b > 0.01:
                    im.alpha_composite(_fade(s._av("P", "content"), a_b), (o["xP"], int(r_["y"])))
        a_rien = smooth((u - tr) / 0.3) if tr is not None else 0.0
        e1 = max(smooth((u - t["hamd"] - 0.2) / 0.35) if "hamd" in t else 0.0, a_rien)
        e2 = max(smooth((u - t["reponse"] - 0.2) / 0.35) if "reponse" in t else 0.0, a_rien)
        if e2 > 0.01:                                                              # Grand (il ne répond pas)
            im.alpha_composite(_fade(s._av("G", "content"), e2), (o["xG"], int(yG)))
            en = smooth((u - tr) / 0.3) if tr is not None else 0.0
            if en > 0.01:                                                          # fondu enchaîné : l'image du
                im.alpha_composite(_fade(s._av("G", "neutre"), e2 * en), (o["xG"], int(yG)))   # dessous reste pleine
        if e1 > 0.01:                                                              # Petit (il éternue à {chaine rien})
            if tr is not None and u >= tr:
                v = u - tr
                ec = smooth((v - 0.2) / 0.22) * (1 - smooth((v - 0.95) / 0.25))
                base = s._av("P", "content" if v < 0.6 else "neutre")
                im.alpha_composite(_fade(base, e1), (o["xP"], int(yP)))
                if ec > 0.01:
                    im.alpha_composite(_fade(s._av("P", "triste", True), e1 * ec), (o["xP"], int(yP)))
            else:
                im.alpha_composite(_fade(s._av("P", "content"), e1), (o["xP"], int(yP)))
        if tr is not None and u >= tr:
            v = u - tr
            xb = o["xP"] + 34 * s.AVK + 2
            ea = smooth((v - 0.4) / 0.25)
            if ea > 0.01:                                                          # petit « ATCHOUM » gris
                ta = o["atch"]
                k = 0.86 + 0.14 * smooth((v - 0.4) / 0.35)
                t2 = ta.resize((int(ta.width * k), int(ta.height * k)), Image.LANCZOS) if k < 0.999 else ta
                im.alpha_composite(_fade(t2, ea), (int(xb + 40), int(o["rien"]["yP"] + 32 - t2.height / 2)))
            ev = smooth((v - 0.95) / 0.35)
            if ev > 0.01:                                                          # sa bulle reste vide
                bv = o["vide"]
                im.alpha_composite(_fade(bv, ev), (int(xb - 24 * (1 - ev)), int(o["rien"]["yP"] + 64)))
            eg = smooth((v - 1.5) / 0.4)
            if eg > 0.01:                                                          # pas de réponse
                bg = o["videG"]
                xg = o["xG"] - 2 - bg.width
                im.alpha_composite(_fade(bg, eg), (int(xg + 24 * (1 - eg)), int(o["rien"]["yG"])))
                lab = o["lab"]
                s._pose(im, lab, xg + (bg.width - 36) / 2, o["rien"]["yG"] + 170 + 22 + lab.height / 2,
                        smooth((v - 1.7) / 0.4))
        return im

    # ------------------------------------------------------------ {rhume …}
    def _petit(s, e, plisse):
        """Petit en entier, enrhumé (nez rouge) ; e = son bras du fond plié devant le visage (0 → 1)."""
        q = round(e * 8) / 8
        cle = ("pe", q, plisse)
        if cle in s._cache:
            return s._cache[cle]
        r = cast.CAST[s.who]
        face = "triste" if plisse else "gene"
        if q <= 0:
            a = cast.dessine(r, "neutre", face, blush=not plisse).a.copy()
            g = cast.geo(r)
            _retouche(a, r, g, plisse, nez=True)
        else:
            a, g = _sprite_sans_bras(s.who, face, blush=not plisse)
            _retouche(a, r, g, plisse, nez=True)
            c = Px(a.shape[1], a.shape[0], alpha=True)
            S = (g.sr, g.ay + 0.5)
            E0, W0 = (g.sr + 1, g.ay + 8 * g.ky), (g.sr + 1, g.ay + 14.5 * g.ky)
            E1, W1 = (g.sr + 3.0, g.y0 + 17.6), (24.0, g.y0 + 16.6)              # le coude ressort devant le nez
            E = (E0[0] + (E1[0] - E0[0]) * q, E0[1] + (E1[1] - E0[1]) * q)
            W = (W0[0] + (W1[0] - W0[0]) * q, W0[1] + (W1[1] - W0[1]) * q)
            _bras(c, S, E, W, s.who, ep=4.6, plie=q >= 0.3)
            a[c.al, :3] = c.a[c.al]
            a[c.al, 3] = 255
        im = _grand(Image.fromarray(a, "RGBA"), s.KS)
        s._cache[cle] = im
        return im

    def _neuf(s):
        """Le rhume est né directement à une étape ({rhume reponse|deux|enrhume} sur un plan neuf, sans le {rhume} du
        début) : pas de 1er « ATCHOUM ! » (il a déjà eu lieu)."""
        return s.mode == "rhume" and bool(s.t) and min(s.t.values()) < 0.05

    def _t_atch(s):
        """Les instants des « ATCHOUM ! » du rhume (depuis l'apparition) : au début (sauf sur un plan neuf), puis T_YA
        après {rhume deux}."""
        return ([] if s._neuf() else [0.0]) + ([s.t["deux"] + s.T_YA] if "deux" in s.t else [])

    def _rhume_bulles(s):
        """Le fil des bulles : (instant, quoi, pousse, fin), dans l'ordre ; la plus récente en bas : quand une bulle qui
        « pousse » arrive, les autres montent d'un cran. À {rhume deux}, la petite bulle « YAHDÎKOU… » ("Y") prend la
        place du bas, s'efface quand le 2e « ATCHOUM ! » arrive, et le 2e « AL-HAMDOULILLAH ! » vient à sa place (sans
        pousser : les anciennes bulles ne montent qu'une fois). Sur un plan neuf, seulement les bulles de la phrase
        en cours (pas de 1re bulle de Petit)."""
        evs = [] if s._neuf() else [(0.55, "P", True, None)]
        if "reponse" in s.t:
            evs.append((s.t["reponse"] + 0.1, "G", True, None))
        if "deux" in s.t:
            td = s.t["deux"]
            evs.append((td + 0.05, "Y", True, td + s.T_YA - 0.08))
            evs.append((td + s.T_YA + 0.95, "P", False, None))
        return sorted(evs, key=lambda e_: e_[0])

    def _rhume_fond(s):
        """Ce qui ne bouge pas : les ombres au sol, la petite table et la boîte de mouchoirs (à côté de Petit)."""
        W_, H_, KS = 1020, 960, s.KS
        sx, sy = s.SX, s.SY
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        tab = _petite_table().img(KS, rgba=True)
        tx_, ty_ = 10, sy - tab.height + 4

        def ombres(d):
            d.ellipse([sx - 130, sy - 14, sx + 130, sy + 14], fill=(16, 12, 24, 110))
            d.ellipse([tx_ - 6, sy - 10, tx_ + tab.width + 6, sy + 12], fill=(16, 12, 24, 90))
        _translucide(im, ombres)
        im.alpha_composite(tab, (tx_, int(ty_)))
        bo = _boite_mouchoirs().img(KS, rgba=True)
        im.alpha_composite(bo, (int(tx_ + tab.width / 2 - bo.width / 2), int(ty_ - bo.height + 5)))
        return im

    def _bulle_rhume(s, qui):
        if qui == "P":
            return _bulle([("AL-HAMDOULILLAH !", OR_)], fond=FOND_P, size=48, queue=0.44, pad=20)
        if qui == "Y":                                     # la petite bulle coupée par l'éternuement (pointe au milieu)
            return _bulle([("YAHDÎKOU…", OR_)], fond=FOND_P, size=44, queue=0.5, pad=18)
        return _bulle([("YARHAMOUKA-LLÂH !", OR_)], fond=FOND_G, size=48, queue=0.84, pad=20)

    def _cartes_rhume(s):
        """{rhume enrhume} : la carte du hadith (qui parle, puis la parole, en jaune) et, à part, la dou'a de guérison
        en blanc, conseillée par les savants (elle n'est pas dans le hadith : an-Nawawi)."""
        c1 = _carte(_bloc([("LE PROPHÈTE (PAIX ET SALUT SUR LUI) :", BLANC, 40),
                           ("« L'HOMME EST ENRHUMÉ »", JAUNE, 56)], serre=16), bord=JAUNE, pad=(40, 22))
        c2 = _carte(_bloc([("QU'ALLAH TE GUÉRISSE", BLANC, 50),
                           ("DOU'A CONSEILLÉE PAR LES SAVANTS", GRIS_CLAIR, 36)], serre=16),
                    bord=GRIS_CLAIR, pad=(36, 18))
        return c1, c2

    def _image_rhume(s, u):
        W_, H_ = 1020, 960
        KS = s.KS
        t_deux, t_enr = s.t.get("deux"), s.t.get("enrhume")
        sx, sy = s.SX, s.SY
        im = s._garde("rh_fond", s._rhume_fond).copy()                          # ombres, table, mouchoirs
        e_b = 0.0                                                                # Petit : le coude à chaque « atchoum »
        for T in s._t_atch():
            e_b = max(e_b, smooth((u - T + 0.05) / 0.2) * (1 - smooth((u - T - 0.45) / 0.35)))
        pe = s._petit(e_b, e_b > 0.5)
        X0, Y0 = sx - 23 * KS, sy - 98 * KS
        im.alpha_composite(pe, (int(X0), int(Y0)))
        g = cast.geo(cast.CAST[s.who])
        tete = (X0 + 24 * KS, Y0 + (g.y0 + 10) * KS)                             # le milieu de sa tête
        haut_tete = Y0 + (g.y0 - 1) * KS
        avx, avy = W_ - 34 * s.AVK - 6, int(haut_tete + 6)                       # Grand (petit buste, à droite)
        a_g = smooth((u - s.t["reponse"]) / 0.35) if "reponse" in s.t else 0.0
        if t_enr is not None:
            a_g = max(a_g, smooth((u - t_enr) / 0.35))
        e_m = s._e("enrhume", u, 0.7, dec=0.45)                                  # il tend un mouchoir
        if e_m > 0.01 and a_g > 0.01:                        # (la manche sort de sous son cadre et va jusqu'au bord
            long_ = int((W_ - (avx - 190)) / KS) + 2         # droit, sans bout coupé en l'air ; la main en fondu)
            mm = s._garde("mouch", lambda: _main_mouchoir("GRAND", long_).img(KS, rgba=True))
            mx = avx + 40 - 230 * e_m
            im.alpha_composite(_fade(mm, a_g * smooth(e_m / 0.35)), (int(mx), int(avy + 100)))
        if a_g > 0.01:                                       # il sourit (il ne rit pas pendant la parole du Prophète ﷺ)
            im.alpha_composite(_fade(s._av("G", "content"), a_g), (int(avx), int(avy)))
        at = s._garde("atch_r", lambda: pxv.big_title([("ATCHOUM !", BLANC)], size=58))
        a_fin = 1 - s._e("enrhume", u, 0.35)                                     # tout s'efface à {rhume enrhume}
        for T in s._t_atch():                                                    # « ATCHOUM ! » (à chaque fois)
            v = u - T
            if 0 <= v < 1.5:
                a = smooth(v / 0.15) * (1 - smooth((v - 1.0) / 0.4)) * a_fin     # (avant le thermomètre, à sa place)
                k = 0.86 + 0.14 * smooth(v / 0.3)
                a2 = at.resize((int(at.width * k), int(at.height * k)), Image.LANCZOS)
                im.alpha_composite(_fade(a2, a), (int(tete[0] + 100), int(tete[1] - 30 - a2.height / 2)))
        evs = s._rhume_bulles()                                                  # le fil des bulles
        for j, (c_j, qui, _, fin) in enumerate(evs):
            if u < c_j:
                continue
            monte = sum(smooth((u - (c_k - 0.35)) / 0.55) for (c_k, _, p_k, _) in evs[j + 1:]   # (glissé lent,
                        if p_k and u >= c_k - 0.35)                    # libère la place avant la nouvelle bulle)
            a = smooth((u - c_j) / 0.3) * a_fin
            if fin is not None:                                                  # « YAHDÎKOU… » : coupé par l'atchoum
                a *= 1 - smooth((u - fin) / 0.3)
            if t_deux is not None and c_j < t_deux:                             # les anciennes bulles pâlissent
                a *= 1 - 0.55 * smooth((u - t_deux) / 0.5)
            if a <= 0.01:
                continue
            b = s._garde(("rb", qui), lambda qui=qui: s._bulle_rhume(qui))
            y = haut_tete - 4 - (b.height - 8) - s.PALIER * monte + 14 * (1 - smooth((u - c_j) / 0.3))
            x = {"P": 22, "Y": tete[0] - b.width / 2}.get(qui, W_ - 14 - b.width)
            im.alpha_composite(_fade(b, a), (int(x), int(y)))
        if t_enr is not None and u >= t_enr:                                     # « l'homme est enrhumé »
            v = u - t_enr
            et = smooth((v - 0.25) / 0.35)
            th = s._garde("thermo", lambda: objets.icone("thermometre").img(9))
            im.alpha_composite(_fade(th, et), (int(tete[0] + 110), int(tete[1] + 4 - th.height / 2
                                                                         + 6 * math.sin(u * 2))))
            c1, c2 = s._garde("cartes", s._cartes_rhume)
            a1, a2 = smooth((v - 0.3) / 0.4), smooth((v - 1.0) / 0.4)          # après l'effacement des bulles
            y1 = 6 + c1.height / 2 + 14 * (1 - a1)                               # en haut : la parole du Prophète ﷺ
            s._pose(im, c1, W_ / 2, y1, a1)
            y2 = 6 + c1.height + 16 + c2.height / 2 + 14 * (1 - a2)              # plus bas, à part : la dou'a
            s._pose(im, c2, W_ / 2, y2, a1 * a2)
        return im


# ---------------------------------------------------------------- branchement dans explique.Schema
CLES = ("atchoum", "chaine", "rhume")


def _norm(m):
    m = m.lower()
    for a_, b_ in (("é", "e"), ("è", "e"), ("ê", "e"), ("à", "a"), ("â", "a"), ("î", "i"), ("ô", "o"), ("û", "u"),
                   ("ç", "c")):
        m = m.replace(a_, b_)
    return m


def _decalage(mots):
    """{atchoum PETIT 0.7} : 3e mot facultatif = le « atchoum » 0,7 s après la balise (balise posée sur « Aaah… »)."""
    if len(mots) > 2:
        try:
            return max(0.0, min(3.0, float(mots[2].replace(",", "."))))
        except ValueError:
            pass
    return None


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique.Schema._ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
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

    if k == "atchoum":
        schema._ajoute(t, Eternue(brut, "atchoum", qui if qui in ("PETIT", "GRAND") else "PETIT", _decalage(mots)))
    elif k in ("chaine", "rhume"):
        if sous in Eternue.ETAPES_MODE[k]:
            etape(Eternue, sous, k, lambda: Eternue(brut, k))
        else:
            schema._ajoute(t, Eternue(brut, k))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "atchoum":
        d_ = _decalage(mots)
        return t + (Eternue.T0 if d_ is None else d_) + 1.6
    if k == "chaine":
        return t + dict(aime=1.4, hamd=1.0, reponse=1.0, retour=1.2, rien=2.4).get(sous, 0.8)
    if k == "rhume":                     # deux : « Yahdîkou… », atchoum à +1,2 s, « Al-hamdoulillah ! » net à +2,45 s
        return t + dict(reponse=1.0, deux=2.7, enrhume=2.0).get(sous, 1.4)
    return None
