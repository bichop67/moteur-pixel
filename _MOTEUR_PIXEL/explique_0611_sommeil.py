# DÉMONSTRATION EN IMAGE DU 07/11/2026 — Short ISL22 « T'es dans ton lit ? Dis ça » (scenarios/islam_22_dormir.txt).
#   {lit PETIT}        accroche : la nuit, chambre bleu nuit, Petit allongé sous la couette (vu du pied du lit), il
#                      tient son téléphone près du visage : on n'en voit que le DOS (aucun contenu), sa lueur bleue
#                      neutre éclaire son visage ; le réveil affiche « 01:12 » ; il cligne des yeux, fatigué ; l'image se
#                      rapproche lentement (zoom 1,00 → 1,05)
#   {sommeil}          la chambre la nuit, vue de côté (le lit le long du mur, sous la grande fenêtre : étoiles, lune) ;
#                      Petit couché sur le côté DROIT, face à nous, la main droite sous la joue droite (sunna, Boukhari
#                      6314), le téléphone posé sur la table de nuit ; la formule du coucher « BISMIKA-LLÂHOUMMA //
#                      AMOÛTOU WA AHYÂ » + « EN TON NOM, Ô ALLAH, // JE MEURS ET JE VIS » + l'étiquette « SUNNA »
#                      (Boukhari 6324)
#   {sommeil verset}   la formule s'efface : carte texte du verset 39:42 (Hamidullah, extrait) — JAMAIS d'âme dessinée
#                      (ni fantôme, ni lumière qui sort du corps), ni main ni rayon « d'en haut »
#   {sommeil nuit}     la carte s'efface : Petit dort sur le côté droit, la main sous la joue (yeux fermés, petit
#                      sourire), des « z » montent, le téléphone s'éteint
#   {sommeil reveil}   l'aube, l'heure du Fajr : AUCUN disque de soleil (le soleil levé voudrait dire une prière ratée),
#                      seulement une lueur rose-orangée sur l'horizon, derrière les toits, et le ciel qui s'éclaircit ;
#                      Petit ouvre les yeux ; « AU RÉVEIL : » puis l'invocation du réveil en entier (Boukhari 6324) et
#                      sa traduction
# Aucun prophète, ange, Compagnon ni Chaytan dessiné ; Allah n'est jamais représenté. Mouvements doux seulement (fondus,
# glissés, respirations lentes, zoom lent) : jamais de secousse, de flash ni de clignotement rapide.
# Branché par explique_0611.py (ordre / fin_anim / CLES), comme explique_0411b.
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import cast
from px import Px
from pxv import smooth
from explique import _titre, _fade, _erode, BLANC
from explique_0411 import OL, _buste, _grand
from explique_0411b import _Base, OR_

BLEU_TEL = (150, 206, 255)            # la lueur du téléphone (neutre, sans contenu)
LED = (255, 74, 62)                   # les chiffres du réveil
VERT_DOUX = (150, 218, 160)
Z_COL = (200, 212, 255)
NUIT_TEINTE = ((0.42, 0.46, 0.72), (6, 8, 26))      # ambiance de nuit (ce que la lueur n'éclaire pas)

# ---------------------------------------------------------------- petits outils
SEG7 = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc",
        "8": "abcdefg", "9": "abcdfg"}


def _chiffre7(c, x, y, ch, w=5, h=11, ep=2):
    """Masque d'un chiffre à 7 segments (dessin Px), coin haut-gauche (x, y)."""
    seg = SEG7.get(ch, "")
    m = np.zeros((c.h, c.w), bool)
    mid = y + (h - ep) // 2
    if "a" in seg:
        m |= c.mask_rect(x, y, x + w, y + ep)
    if "g" in seg:
        m |= c.mask_rect(x, mid, x + w, mid + ep)
    if "d" in seg:
        m |= c.mask_rect(x, y + h - ep, x + w, y + h)
    if "f" in seg:
        m |= c.mask_rect(x, y, x + ep, mid + ep)
    if "b" in seg:
        m |= c.mask_rect(x + w - ep, y, x + w, mid + ep)
    if "e" in seg:
        m |= c.mask_rect(x, mid, x + ep, y + h)
    if "c" in seg:
        m |= c.mask_rect(x + w - ep, mid, x + w, y + h)
    return m


T_LIGNES_VERSET = (1.0, 2.0, 3.1, 4.4)  # apparition des 4 lignes du verset depuis {sommeil verset} (voix d'ISL22 : « Allah
#                                         dit : » puis « Allah saisit les âmes » à +1,2 s, « au moment » +2,2, « ainsi » +3,2,
#                                         « au cours » +4,6)


def _pile(lignes, gap=-6):
    """Lignes de titre [(texte, couleur, taille)] centrées et serrées (chaque ligne recadrée sur son encre)."""
    ims = []
    for (t, c, sz) in lignes:
        im = _titre(t, c, sz)
        ims.append(im.crop(im.getbbox()))
    W_ = max(i.width for i in ims)
    H_ = sum(i.height for i in ims) + gap * (len(ims) - 1)
    out = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    y = 0
    for i in ims:
        out.alpha_composite(i, ((W_ - i.width) // 2, y))
        y += i.height + gap
    return out


def _lumin(rgb):
    return (0.3 * rgb[..., 0] + 0.59 * rgb[..., 1] + 0.11 * rgb[..., 2]) / 255.0


def _eclaire(im, mult, add, lumiere=None):
    """Éclairage pixel art d'un PETIT sprite RGBA (avant agrandissement, pour garder des pixels nets) : teinte
    d'ambiance partout (rgb * mult + add), puis, si lumiere = (x, y, rayon, couleur, gain), une lumière colorée en
    paliers nets (0, 1/3, 2/3, 1) autour du point (x, y)."""
    a = np.array(im).astype(float)
    rgb = a[..., :3]
    out = np.clip(rgb * np.array(mult, float) + np.array(add, float), 0, 255)
    if lumiere is not None:
        x0, y0, r, col, gain = lumiere
        h, w = rgb.shape[:2]
        yy, xx = np.mgrid[0:h, 0:w]
        d = np.sqrt((xx + 0.5 - x0) ** 2 + (yy + 0.5 - y0) ** 2) / r
        f = np.floor(np.clip(gain * (1 - d), 0, 1) * 3 + 0.5) / 3
        lit = np.clip(rgb * np.array((0.20, 0.38, 0.60)) + np.array(col, float) * _lumin(rgb)[..., None] * 0.85 + 8,
                      0, 255)
        out = out + (lit - out) * f[..., None]
    a[..., :3] = out
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def _couette(c, pts, pal, etoiles):
    """La couette bleue à étoiles (comme celle de explique_0411) + le drap replié le long du bord du haut."""
    m = c.mask_poly(pts)
    c.shape(m, pal["couette"], shade=pal["couette_s"], light=pal["couette_h"], band=2, olcol=OL)
    for (x, y) in etoiles:
        c.fill(c.mask_rect(x, y, x + 2, y + 2) & _erode(m, 1), pal["etoile"])
    haut = list(pts[1:-1])                                                          # le bord du haut
    drap = c.mask_poly(haut + [(x, y + 4) for (x, y) in reversed(haut)]) & m
    c.fill(drap, pal["drap"])
    c.fill(c.mask_poly([(x, y + 3) for (x, y) in haut] + [(x, y + 4.5) for (x, y) in reversed(haut)]) & m,
           pal["drap_s"])
    c.outline(m, OL)
    return m


def _lueur(c, cx, cy, rx, ry, col, k=0.5, m=None, levels=4):
    """Halo ELLIPTIQUE en paliers nets (comme Px.glow, mais aplati) : la lueur de l'aube posée sur l'horizon."""
    d = np.sqrt(((c.xx + 0.5 - cx) / rx) ** 2 + ((c.yy + 0.5 - cy) / ry) ** 2)
    q = np.clip(1 - d, 0, 1) ** 1.2 * levels
    lvl = np.floor(q)
    lvl = np.where((q - lvl > 0.82) & ((c.xx + c.yy) % 2 == 0), lvl + 1, lvl)      # bord tramé d'un pixel
    w = np.clip(lvl, 0, levels) / levels * k
    on = w > 0
    if m is not None:
        on &= m
    out = c.a.astype(float) * (1 - w[..., None]) + np.array(col, float)[None, None, :] * w[..., None]
    c.a[on] = out[on].astype(np.uint8)


NUIT = dict(mur_h=(30, 32, 80), mur_b=(15, 15, 44), papier=(37, 39, 90), bois=(84, 62, 76), bois_s=(62, 44, 58),
            bois_h=(108, 84, 98), bois_in=(92, 68, 84), oreiller=(170, 178, 216), oreiller_s=(132, 140, 186),
            oreiller_h=(200, 206, 236), couette=(52, 80, 160), couette_s=(36, 58, 124), couette_h=(76, 108, 186),
            etoile=(206, 196, 110), drap=(178, 186, 220), drap_s=(140, 148, 192), rideau=(62, 42, 98),
            rideau_s=(44, 30, 74), rideau_h=(84, 60, 122), cadre=(44, 44, 90), cadre_s=(32, 32, 70),
            cadre_h=(66, 68, 122), table=(66, 50, 70), table_s=(48, 36, 52), table_h=(88, 70, 92), tringle=(92, 84, 116),
            matelas=(126, 132, 182), matelas_s=(96, 102, 150), matelas_h=(150, 156, 204), toit=(22, 22, 52))
AUBE = dict(mur_h=(118, 86, 120), mur_b=(78, 56, 88), papier=(128, 94, 128), bois=(150, 104, 86), bois_s=(118, 78, 68),
            bois_h=(182, 132, 108), bois_in=(160, 112, 92), oreiller=(246, 226, 222), oreiller_s=(214, 182, 190),
            oreiller_h=(255, 244, 236), couette=(96, 112, 196), couette_s=(72, 84, 160), couette_h=(130, 146, 220),
            etoile=(250, 222, 130), drap=(250, 236, 230), drap_s=(220, 196, 204), rideau=(150, 92, 132),
            rideau_s=(118, 70, 108), rideau_h=(184, 122, 160), cadre=(132, 102, 140), cadre_s=(104, 78, 116),
            cadre_h=(166, 132, 170), table=(132, 96, 98), table_s=(104, 74, 80), table_h=(162, 122, 120),
            tringle=(176, 150, 160), matelas=(226, 200, 212), matelas_s=(196, 166, 186), matelas_h=(246, 228, 232),
            toit=(64, 46, 92))
NUIT_LIT = dict(NUIT, couette=(40, 62, 134), couette_s=(28, 44, 102), couette_h=(58, 86, 160), etoile=(168, 160, 96),
                drap=(146, 154, 196), drap_s=(112, 120, 168))   # l'accroche : la chambre est plus sombre


# ---------------------------------------------------------------- {lit PETIT} {sommeil …}
class Sommeil(_Base):
    """{lit PETIT} : accroche, la nuit, Petit au lit sur son téléphone à 01:12 (lueur bleue neutre, on ne voit que le dos
    du téléphone ; il cligne des yeux ; zoom lent). {sommeil} : la chambre la nuit vue de côté, Petit couché sur le
    côté droit, la main droite sous la joue droite (Boukhari 6314), la formule du coucher (Boukhari 6324) ; {sommeil
    verset} le verset 39:42 en carte texte ; {sommeil nuit} il dort, le téléphone s'éteint ; {sommeil reveil} l'aube
    du Fajr (lueur rose-orangée sur l'horizon, AUCUN disque de soleil), l'invocation du réveil. Aucune âme, aucune
    lumière qui sort du corps, aucune main ni aucun rayon « d'en haut »."""
    ETAPES = ("verset", "nuit", "reveil")
    KB_LIT = 14                      # échelle du buste dans l'accroche (gros plan)
    KP = 10                          # échelle de Petit couché dans la chambre
    PH_S = 160                       # hauteur du dessin de la chambre (1020 x 960)
    BX_LIT, BY_LIT = 373, 252        # l'accroche : le buste (pixels d'écran)
    OX_TEL, OY_TEL = 752, 382        # l'accroche : le téléphone (son bas passe sous le bord de la couette)
    ZOOM_C = (520, 450)              # l'accroche : le point fixe du zoom lent
    HX, HY = 250, 600                # la chambre : coin haut-gauche du dessin de Petit couché (pixels d'écran)
    VITRE = (20, 10, 150, 96)        # la chambre : la grande vitre d'un seul tenant (pixels du dessin, x6 à l'écran) :
    #                                  aucun croisillon, rien ne passe derrière les mots qui contiennent le nom d'Allah

    def __init__(s, cmd, mode="sommeil", who="PETIT"):
        super().__init__(cmd)
        s.mode = mode
        s.who = who if who in cast.CAST else "PETIT"
        s.negatif = mode == "lit"

    def sons_el(s):
        if s.mode == "lit":
            return []
        out = []
        if min(list(s.t.values()) + [9.0]) > 0.3:                                  # la formule s'affiche au début
            out.append((0.1, "sa_ting", 0.03, None))
        if "nuit" in s.t:                                                          # le téléphone s'éteint
            out.append((s.t["nuit"] + 0.15, "dv_clic", 0.03, None))
        if "reveil" in s.t:                                                        # l'aube se lève
            out.append((s.t["reveil"] + 0.3, "sa_scintillement", 0.045, None))
        return out

    def image(s, u):
        return s._image_lit(u) if s.mode == "lit" else s._image_sommeil(u)

    # ======================================================== l'accroche {lit PETIT}
    def _fond_lit(s):
        if "fl" in s._cache:
            return s._cache["fl"]
        W, H = 170, 150
        p = NUIT_LIT
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        c.vgrad(tout_, 0, H, p["mur_h"], p["mur_b"], steps=5)
        for x in range(4, W, 12):                                                  # papier peint à rayures
            c.dither(tout_ & c.mask_rect(x, 0, x + 3, H), p["papier"], 0.35)
        lx, ly = (s.OX_TEL + 2 * s.KB_LIT) / 6, (s.OY_TEL + 6.5 * s.KB_LIT) / 6      # le bord lumineux du téléphone
        # la fenêtre (en haut à gauche) : ciel de nuit, lune, étoiles
        fen = c.mask_rect(6, 4, 42, 52)
        c.shape(fen, p["cadre"], shade=p["cadre_s"], light=p["cadre_h"], band=1, olcol=OL)
        vitre = c.mask_rect(9, 7, 39, 49)
        c.vgrad(vitre, 7, 49, (12, 16, 50), (38, 44, 100), steps=4)
        c.fill(c.mask_ell(32, 16, 6, 6) & ~c.mask_ell(29, 14, 5.5, 5.5) & vitre, (250, 236, 170))
        for (x, y) in ((13, 12), (17, 38), (35, 44), (14, 28), (26, 10), (36, 31)):
            c.px(x, y, (255, 255, 230))
        c.fill(c.mask_rect(23, 7, 25, 49) | c.mask_rect(9, 27, 39, 29), p["cadre"])
        for x0 in (0, 38):                                                         # rideaux + tringle
            rid = c.mask_rect(x0, 2, x0 + 10, 60)
            c.shape(rid, p["rideau"], shade=p["rideau_s"], light=p["rideau_h"], band=1, olcol=OL)
            c.fill(c.mask_rect(x0 + 4, 4, x0 + 5, 58), p["rideau_s"])
        c.fill(c.mask_rect(0, 0, 54, 3), p["tringle"])
        # la tête de lit capitonnée
        tl = c.mask_rrect(44, 24, 150, 108, 10)
        c.shape(tl, p["bois"], shade=p["bois_s"], light=p["bois_h"], band=2, olcol=OL)
        pan = c.mask_rrect(51, 31, 143, 104, 8)
        c.fill(pan, p["bois_in"])
        for yy in range(40, 100, 14):
            for xx in range(60, 140, 16):
                dx = 8 if (yy // 14) % 2 else 0
                c.fill(c.mask_rect(xx + dx, yy, xx + 2 + dx, yy + 2) & pan, p["bois_s"])
        c.glow(lx, ly, 48, BLEU_TEL, k=0.30, m=pan)                                # la lueur sur la tête de lit
        # l'oreiller, éclairé en bleu du côté du téléphone (paliers)
        orei = c.mask_rrect(56, 50, 142, 100, 12)
        c.shape(orei, p["oreiller"], shade=p["oreiller_s"], light=p["oreiller_h"], band=2, olcol=OL)
        c.glow(lx, ly, 46, BLEU_TEL, k=0.45, m=orei)
        # la table de nuit (à gauche) et le réveil « 01:12 »
        c.glow(25, 82, 30, (255, 60, 50), k=0.30, m=tout_)
        tab = c.mask_rect(-2, 96, 48, 152)
        c.shape(tab, p["table"], shade=p["table_s"], light=p["table_h"], band=1, olcol=OL)
        c.fill(c.mask_rect(0, 96, 48, 99), p["table_h"])
        tir = c.mask_rect(6, 106, 40, 122)
        c.outline(tir, p["table_s"])
        c.fill(c.mask_rect(21, 112, 25, 115), p["table_h"])
        rev = c.mask_rrect(5, 68, 45, 96, 4)
        c.shape(rev, (60, 62, 90), shade=(42, 42, 62), light=(86, 88, 120), band=1, olcol=OL)
        ecr = c.mask_rrect(8, 71, 42, 93, 2)
        c.fill(ecr, (12, 8, 18))
        x0 = 10
        for x, ch in zip((x0, x0 + 7, x0 + 18, x0 + 25), "0112"):
            c.fill(_chiffre7(c, x, 76, "8"), (62, 18, 24))                          # segments éteints
            c.fill(_chiffre7(c, x, 76, ch), LED)
        c.fill(c.mask_rect(x0 + 14, 79, x0 + 16, 81) | c.mask_rect(x0 + 14, 83, x0 + 16, 85), LED)   # les deux points
        c.fill(c.mask_rect(9, 72, 41, 73) & ecr, (40, 30, 46))                     # reflet sur la vitre du réveil
        s._cache["fl"] = c.img(6, rgba=True)
        return s._cache["fl"]

    def _couette_lit(s):
        if "cl" in s._cache:
            return s._cache["cl"]
        c = Px(170, 150, alpha=True)
        pts = [(8, 152), (28, 104), (50, 98), (72, 94), (96, 92), (120, 93), (144, 96), (160, 100), (172, 103),
               (172, 152)]
        m = _couette(c, pts, NUIT_LIT, ((40, 112), (62, 104), (78, 122), (104, 108), (150, 116), (50, 136), (96, 138),
                                        (136, 140), (160, 128)))
        for (xa, ya, xb, yb) in ((70, 104, 56, 150), (71, 104, 57, 150), (124, 103, 140, 150), (125, 103, 141, 150)):
            c.line(xa, ya, xb, yb, NUIT_LIT["couette_s"])                         # deux plis doux (le corps dessous)
        c.glow((s.OX_TEL + 2 * s.KB_LIT) / 6, 97, 26, BLEU_TEL, k=0.26, m=m)       # la lueur du téléphone sur la couette
        s._cache["cl"] = c.img(6, rgba=True)
        return s._cache["cl"]

    def _buste_lit(s, cligne):
        cle = ("bl", cligne)
        if cle in s._cache:
            return s._cache[cle]
        b, bouche = _buste(s.who, "blase", cligne=cligne)
        a = np.array(b)
        r = cast.CAST[s.who]
        S = r["_peau"]
        g = cast.geo(r)
        ey = bouche[1] - (g.hd["mouth"][1] - g.hd["ey"])                            # la ligne des yeux (dans le buste)
        ex = g.hd["ex"] - 8
        for (x0, x1) in ((ex - 1, ex + 2), (ex + 5, ex + 7)):                      # cernes (il est fatigué)
            for x in range(x0, x1):
                if 0 <= ey + 3 < a.shape[0] and a[ey + 3, x, 3] > 0 and tuple(a[ey + 3, x, :3]) == S["b"]:
                    a[ey + 3, x, :3] = (172, 120, 122)
        b = Image.fromarray(a, "RGBA")
        lx = (s.OX_TEL + 2 * s.KB_LIT - s.BX_LIT) / s.KB_LIT                        # le bord du téléphone tourné vers lui
        ly = (s.OY_TEL + 6.5 * s.KB_LIT - s.BY_LIT) / s.KB_LIT
        b = _eclaire(b, *NUIT_TEINTE, lumiere=(lx, ly, 30, BLEU_TEL, 1.4))
        s._cache[cle] = _grand(b, s.KB_LIT)
        return s._cache[cle]

    def _main_tel(s):
        """Le téléphone qui dépasse de la couette, près de son visage, vu de DOS : aucun écran visible, seulement la
        lumière bleue qui déborde par le bord tourné vers lui. Sa main est sous la couette : on ne voit que le bout de
        trois doigts sur le dos du téléphone (à contre-jour)."""
        if "mt" in s._cache:
            return s._cache["mt"]
        S = cast.CAST[s.who]["_peau"]
        W, H = 11, 15
        c = Px(W, H, alpha=True)                                                   # le téléphone, de dos
        tel = c.mask_rrect(2, 0, 9, 14, 2)
        c.shape(tel, (58, 60, 80), shade=(38, 38, 52), light=(86, 88, 110), band=1, olcol=OL)
        c.fill(c.mask_rrect(3, 1, 6, 5, 1), (24, 24, 34))                          # le bloc photo
        c.px(4, 2, (130, 140, 172))
        c.px(4, 4, (130, 140, 172))
        a = np.array(_eclaire(c.img(1, rgba=True), (0.80, 0.84, 1.0), (0, 0, 8)))
        a[1:13, 2, :3] = BLEU_TEL                                                   # la lumière déborde sur le bord gauche
        a[0, 3:8, :3] = (120, 176, 236)                                              # … et en haut
        out = Image.fromarray(a, "RGBA")
        c = Px(W, H, alpha=True)                                                   # le bout des doigts (la main est dessous)
        for x0 in (2.5, 4.5, 6.5):
            doigt = c.mask_rrect(x0, 10, x0 + 2, 15, 1)
            c.shape(doigt, S["b"], shade=S["s"], light=S["h"], band=1, olcol=OL)
        out.alpha_composite(_eclaire(c.img(1, rgba=True), (0.74, 0.70, 0.90), (10, 8, 22),
                                     lumiere=(2.0, 11.5, 2.4, BLEU_TEL, 1.3)))
        s._cache["mt"] = _grand(out, s.KB_LIT)
        return s._cache["mt"]

    def _halos_lit(s):
        """La lumière du téléphone dans l'air : derrière sa tête (sur l'oreiller) et, plus légère, devant son visage.
        Chaque halo est recadré sur sa zone (rapide) : (image, x, y)."""
        if "hl" in s._cache:
            return s._cache["hl"]
        lx, ly = s.OX_TEL + 2 * s.KB_LIT, s.OY_TEL + 6.5 * s.KB_LIT
        out = []
        for (x0, y0, x1, y1, al, flou) in ((lx - 330, ly - 250, lx + 110, ly + 170, 90, 46),
                                           (lx - 170, ly - 110, lx + 16, ly + 100, 80, 34)):
            m = 3 * flou
            lay = Image.new("RGBA", (int(x1 - x0 + 2 * m), int(y1 - y0 + 2 * m)), (0, 0, 0, 0))
            ImageDraw.Draw(lay).ellipse([m, m, m + x1 - x0, m + y1 - y0], fill=(*BLEU_TEL, al))
            out.append((lay.filter(ImageFilter.GaussianBlur(flou)), int(x0 - m), int(y0 - m)))
        s._cache["hl"] = out
        return out

    def _image_lit(s, u):
        im = s._fond_lit().copy()
        W_, H_ = im.size
        (der, dx, dy), (dev, vx, vy) = s._halos_lit()
        resp = 0.86 + 0.14 * math.sin(u * 2.1)                                    # la lueur respire (lentement)
        im.alpha_composite(_fade(der, resp), (dx, dy))
        clignes = ((-0.95, -0.8), (0.55, 0.72), (1.95, 2.35), (3.5, 3.67), (4.9, 5.3), (6.5, 6.67), (8.0, 8.4))
        cl = any(a_ <= u < b_ for (a_, b_) in clignes)                             # il cligne des yeux (fatigué)
        im.alpha_composite(s._buste_lit(cl), (s.BX_LIT, s.BY_LIT))
        im.alpha_composite(s._main_tel(), (s.OX_TEL, s.OY_TEL))
        im.alpha_composite(s._couette_lit())
        im.alpha_composite(_fade(dev, resp), (vx, vy))
        z = 1.0 + 0.05 * smooth((u + 0.6) / 5.5)                                  # rapprochement lent
        if z > 1.0005:
            px_, py_ = s.ZOOM_C
            x0, y0 = px_ - px_ / z, py_ - py_ / z
            im = im.resize((W_, H_), Image.BICUBIC, box=(x0, y0, x0 + W_ / z, y0 + H_ / z))
        return im

    # ======================================================== la chambre {sommeil …} (vue de côté)
    def _chambre(s, aube):
        """La chambre vue de côté : le mur, la grande fenêtre (vitre transparente : le ciel est dessous), les rideaux,
        la table de nuit et le téléphone posé à plat (à gauche), le lit le long du mur (tête de lit à gauche), le
        matelas et l'oreiller ; aube = palette du matin."""
        cle = ("ch", aube)
        if cle in s._cache:
            return s._cache[cle]
        p = AUBE if aube else NUIT
        W, H = 170, s.PH_S
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        vx0, vy0, vx1, vy1 = s.VITRE
        vitre = c.mask_rect(vx0, vy0, vx1, vy1)
        mur = tout_ & ~vitre
        c.vgrad(mur, 0, H, p["mur_h"], p["mur_b"], steps=5)
        for x in range(4, W, 12):                                                  # papier peint à rayures
            c.dither(mur & c.mask_rect(x, 0, x + 3, H), p["papier"], 0.3)
        cadre = c.mask_rect(vx0 - 4, vy0 - 4, vx1 + 4, vy1 + 4) & ~vitre           # la fenêtre (une seule vitre)
        c.shape(cadre, p["cadre"], shade=p["cadre_s"], light=p["cadre_h"], band=1, olcol=OL)
        rebord = c.mask_rect(vx0 - 10, vy1 + 2, vx1 + 10, vy1 + 8)
        c.shape(rebord, p["cadre_h"], shade=p["cadre_s"], band=1, olcol=OL)
        for (x0, x1) in ((-2, 18), (152, 172)):                                    # les rideaux, ouverts
            pts = [(x0, 4), (x1, 4), (x1, 112)] + [(x1 - (x1 - x0) * k / 6, 112 + (2 if k % 2 else 0))
                                                   for k in range(1, 6)] + [(x0, 112)]
            rid = c.mask_poly(pts)
            c.shape(rid, p["rideau"], shade=p["rideau_s"], light=p["rideau_h"], band=1, olcol=OL)
            for k in (1, 3, 5):
                xx = x0 + (x1 - x0) * k / 6
                c.fill(c.mask_rect(xx, 7, xx + 1, 110) & rid, p["rideau_s"])
        c.fill(c.mask_rect(0, 2, W, 5), p["tringle"])
        c.outline(c.mask_rect(0, 2, W, 5), OL)
        tab = c.mask_rect(-2, 128, 27, 166)                                        # la table de nuit
        c.shape(tab, p["table"], shade=p["table_s"], light=p["table_h"], band=1, olcol=OL)
        c.fill(c.mask_rect(0, 128, 27, 131), p["table_h"])
        c.outline(c.mask_rect(4, 138, 22, 153), p["table_s"])                     # le tiroir
        c.fill(c.mask_rect(11, 144, 15, 146), p["table_h"])
        tel = c.mask_rect(5, 125, 21, 128)                                         # le téléphone posé (écran en l'air)
        c.shape(tel, (40, 40, 54), shade=(26, 26, 36), light=(70, 72, 92), band=1, olcol=OL)
        tl = c.mask_rrect(29, 100, 37, 170, 3)                                     # la tête de lit
        c.shape(tl, p["bois"], shade=p["bois_s"], light=p["bois_h"], band=1, olcol=OL)
        c.fill(c.mask_rect(31, 105, 35, 134) & tl, p["bois_in"])
        mat = c.mask_rrect(36, 147, W + 6, 156, 2)                                 # le matelas
        c.shape(mat, p["matelas"], shade=p["matelas_s"], light=p["matelas_h"], band=1, olcol=OL)
        bois = c.mask_rect(34, 156, W + 6, 170)                                    # le cadre du lit
        c.shape(bois, p["bois"], shade=p["bois_s"], light=p["bois_h"], band=1, olcol=OL)
        orei = c.mask_rrect(36, 118, 95, 151, 10)                                  # l'oreiller (sous la tête et la main)
        c.shape(orei, p["oreiller"], shade=p["oreiller_s"], light=p["oreiller_h"], band=2, olcol=OL)
        c.fill(c.mask_rect(46, 123, 88, 124) & _erode(orei, 2), p["oreiller_s"])  # un pli
        c.al &= tout_                                                              # les coins arrondis du cadre
        s._cache[cle] = c.img(6, rgba=True)
        return s._cache[cle]

    def _toits(s, c, aube):
        """Les toits de la ville au bas de la fenêtre (silhouettes) ; à l'aube, la lueur de l'horizon est derrière eux
        et quelques fenêtres s'allument (des gens se lèvent pour le Fajr)."""
        p = AUBE if aube else NUIT
        vx0, vy0, vx1, vy1 = s.VITRE
        m = np.zeros((c.h, c.w), bool)
        for (x0, x1, y) in ((20, 28, 85), (28, 38, 87), (38, 50, 83), (50, 62, 89), (62, 72, 81), (72, 86, 86),
                            (86, 98, 79), (98, 112, 85), (112, 124, 82), (124, 136, 88), (136, 150, 84)):
            m |= c.mask_rect(x0, y, x1, vy1)
        m |= c.mask_poly([(62, 81), (67, 76), (72, 81)]) | c.mask_poly([(112, 82), (118, 77), (124, 82)])
        c.fill(m, p["toit"])
        if aube:
            fens, coul = ((54, 92), (90, 83), (128, 91)), (255, 206, 150)
        else:
            fens, coul = ((23, 88), (30, 90), (54, 92), (65, 85), (90, 83), (102, 89), (128, 91), (139, 87),
                          (146, 90)), (255, 214, 140)
        for (x, y) in fens:
            c.fill(c.mask_rect(x, y, x + 2, y + 2), coul)

    def _ciel(s, aube):
        """Le ciel dans la vitre. Nuit : étoiles et lune. Aube (Fajr) : PAS de disque de soleil — le haut du ciel encore
        bleu nuit, une lueur rose-orangée posée sur l'horizon, de fins nuages éclairés par-dessous, les dernières
        étoiles pâles."""
        cle = ("ciel", aube)
        if cle in s._cache:
            return s._cache[cle]
        W, H = 170, s.PH_S
        c = Px(W, H, alpha=True)
        vx0, vy0, vx1, vy1 = s.VITRE
        vitre = c.mask_rect(vx0, vy0, vx1, vy1)
        if not aube:
            c.vgrad(vitre, vy0, vy1, (10, 14, 46), (40, 46, 104), steps=6)
            rng = np.random.default_rng(22)
            for _ in range(44):
                c.px(int(rng.integers(vx0 + 1, vx1 - 1)), int(rng.integers(vy0 + 1, vy1 - 22)), (236, 236, 255))
            for (x, y) in ((36, 15), (140, 16), (28, 70), (146, 62)):              # étoiles en croix : loin des textes
                c.fill(c.mask_rect(x - 1, y, x + 2, y + 1) | c.mask_rect(x, y - 1, x + 1, y + 2), (255, 255, 236))
            c.glow(123, 25, 20, (180, 190, 255), k=0.18, m=vitre)
            c.fill(c.mask_ell(126, 26, 9, 9) & ~c.mask_ell(122, 23, 8, 8), (250, 236, 170))   # la lune
        else:
            c.vgrad(vitre & c.mask_rect(0, 0, W, 40), vy0, 40, (40, 46, 120), (96, 86, 168), steps=5)
            c.vgrad(vitre & c.mask_rect(0, 40, W, 68), 40, 68, (96, 86, 168), (196, 120, 168), steps=5)
            c.vgrad(vitre & c.mask_rect(0, 68, W, H), 68, vy1, (196, 120, 168), (248, 160, 134), steps=4)
            _lueur(c, 85, vy1 + 4, 120, 40, (255, 184, 144), k=0.6, m=vitre)      # la lueur rose-orangée, étalée…
            _lueur(c, 85, vy1 + 2, 96, 15, (255, 218, 166), k=0.7, m=vitre)       # … plus claire au ras des toits
            for (x, y) in ((24, 13), (42, 12), (118, 12), (134, 14), (146, 24), (26, 40)):   # dernières étoiles
                c.px(x, y, (190, 188, 236))
            for (x0, x1, y) in ((20, 34, 34), (24, 31, 32), (137, 150, 35), (140, 147, 33)):   # fins nuages en
                n = c.mask_rrect(x0, y, x1, y + (3 if x1 - x0 > 9 else 2), 1) & vitre       # traînées, sur les côtés
                c.fill(n, (170, 112, 168))
                c.fill(n & ~np.roll(n, -1, axis=0), (252, 176, 160))               # le dessous éclairé par l'aube
        s._cache[cle] = c.img(6, rgba=True)
        return s._cache[cle]

    def _toits_img(s, aube):
        cle = ("toits", aube)
        if cle not in s._cache:
            c = Px(170, s.PH_S, alpha=True)
            s._toits(c, aube)
            s._cache[cle] = c.img(6, rgba=True)
        return s._cache[cle]

    def _couette_ch(s, aube):
        """La couette vue de côté, remontée jusqu'à l'épaule (dessous, le corps couché sur le côté : épaule, taille,
        hanche, genoux, pieds), qui retombe sur le bord du matelas ; le drap replié le long du cou. Le bras droit sort
        de dessous, par le bord côté tête (il est dessiné avec Petit)."""
        cle = ("cc", aube)
        if cle in s._cache:
            return s._cache[cle]
        p = AUBE if aube else NUIT
        c = Px(170, s.PH_S, alpha=True)
        haut = [(79, 157), (78.5, 136), (78, 114), (79, 107), (81.5, 102.5), (86, 100.5), (92, 101), (98, 103.5),
                (104, 107), (111, 107.5), (117, 105.5), (123, 105), (129, 106.5), (137, 111), (147, 115.5),
                (157, 117.5), (165, 118), (176, 119.5)]
        bas = [(176, 157)] + [(x, 156 + (1 if k % 2 else 0)) for k, x in enumerate(range(168, 80, -9))]
        m = c.mask_poly(haut + bas)
        c.shape(m, p["couette"], shade=p["couette_s"], light=p["couette_h"], band=2, olcol=OL)
        for (x, y) in ((92, 112), (104, 124), (118, 113), (132, 126), (146, 121), (160, 130), (90, 136), (110, 145),
                       (126, 140), (144, 147), (162, 145), (100, 150)):
            c.fill(c.mask_rect(x, y, x + 2, y + 2) & _erode(m, 1), p["etoile"])
        for (xa, ya, xb, yb) in ((105, 110, 109, 127), (106, 110, 110, 127), (148, 119, 152, 134)):   # plis doux
            c.line(xa, ya, xb, yb, p["couette_s"])
        bord = [(77, 157), (77, 114), (78, 107), (80.5, 102.5), (85, 100.5), (88, 101), (84, 103.5), (82.5, 108),
                (82, 114), (82, 157)]
        drap = c.mask_poly(bord) & m                                               # le drap replié le long du cou
        c.fill(drap, p["drap"])
        c.fill(c.mask_rect(81, 110, 83, 157) & drap, p["drap_s"])
        c.outline(m, OL)
        c.al &= c.mask_rrect(0, 0, c.w, c.h, 6)                                    # les coins arrondis du cadre
        s._cache[cle] = c.img(6, rgba=True)
        return s._cache[cle]

    def _main_joue(s):
        """La main droite de Petit sous sa joue droite, et sa manche qui sort de la couette (dessin à l'échelle du perso,
        déjà couché : tête à gauche, son côté droit en bas). La tête est collée PAR-DESSUS : la joue appuie sur la
        main, dont on voit le bas (doigts vers la nuque) entre l'oreille et l'oreiller."""
        if "mj" in s._cache:
            return s._cache["mj"]
        r = cast.CAST[s.who]
        S = r["_peau"]
        SL = cast.tons(r["couleur"])
        c = Px(32, 32, alpha=True)
        manche = c.mask_rrect(17, 22, 34, 29, 1)
        c.shape(manche, SL["b"], shade=SL["s"], light=SL["h"], band=1, olcol=OL)
        c.fill(c.mask_rect(17, 22, 19, 29) & manche, SL["s"])                     # le poignet (bord-côte du sweat)
        c.fill(c.mask_rect(19, 27, 32, 29) & manche, SL["s"])
        paume = c.mask_rrect(12, 23, 18, 29, 1)
        doigts = np.zeros((c.h, c.w), bool)
        for (y, x0) in ((23, 8), (25, 6), (27, 7)):                                # trois doigts, bouts vers la nuque
            doigts |= c.mask_rrect(x0, y, 14, y + 2, 1)
        main = paume | doigts
        c.fill(main, S["b"])
        for (y, x0) in ((25, 6), (27, 7)):                                         # les traits entre les doigts
            c.fill(c.mask_rect(x0 + 1, y, 13, y + 1) & main, S["s"])
        c.fill(c.mask_rect(12, 28, 18, 29) & main, S["s"])                         # le dessous, posé sur l'oreiller
        c.outline(main, OL)
        s._cache["mj"] = c.img(1, rgba=True)
        return s._cache["mj"]

    def _perso_ch(s, face, cligne, aube):
        """Petit couché sur le côté DROIT, face à nous, la tête à gauche sur l'oreiller, la main droite sous la joue
        droite : la main, puis par-dessus le buste tourné d'un quart de tour (son côté droit en bas), éclairés (nuit ou
        aube) et agrandis (pixels nets)."""
        cle = ("pc", face, cligne, aube)
        if cle in s._cache:
            return s._cache[cle]
        b, _ = _buste(s.who, face, cligne=cligne)
        can = s._main_joue().copy()
        can.alpha_composite(b.transpose(Image.ROTATE_90))
        if aube:
            can = _eclaire(can, (1.0, 0.88, 0.86), (20, 10, 6))
        else:
            can = _eclaire(can, (0.70, 0.74, 0.92), (6, 8, 22))
        s._cache[cle] = _grand(can, s.KP)
        return s._cache[cle]

    def _textes(s):
        if "tx" in s._cache:
            return s._cache["tx"]
        tx = {}
        tx["f_or"] = _pile([("BISMIKA-LLÂHOUMMA", OR_, 60), ("AMOÛTOU WA AHYÂ", OR_, 60)], gap=-4)
        tx["f_bl"] = _pile([("EN TON NOM, Ô ALLAH,", BLANC, 46), ("JE MEURS ET JE VIS", BLANC, 46)], gap=-6)
        tx["sunna"] = _pile([("SUNNA", VERT_DOUX, 44)])
        v = _pile([("« ALLAH SAISIT LES ÂMES", BLANC, 46), ("AU MOMENT DE LEUR MORT", BLANC, 46),
                   ("AINSI QUE CELLES QUI NE MEURENT PAS", BLANC, 46), ("AU COURS DE LEUR SOMMEIL. »", BLANC, 46)],
                  gap=-4)
        src = _pile([("CORAN 39:42 · EXTRAIT", OR_, 44)])
        pad = 16
        Wc = max(v.width, src.width) + 2 * pad
        Hc = v.height + src.height + 2 * pad + 8
        carte = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
        d = ImageDraw.Draw(carte)
        d.rounded_rectangle([0, 0, Wc - 1, Hc - 1], 26, fill=(16, 18, 46, 228), outline=(236, 226, 196, 210), width=4)
        d.rounded_rectangle([9, 9, Wc - 10, Hc - 10], 20, outline=(236, 226, 196, 70), width=2)
        vide = carte.copy()                                     # le cadre + la source, sans les 4 lignes du verset
        vide.alpha_composite(src, ((Wc - src.width) // 2, pad + v.height + 8))
        tx["carte_vide"] = vide
        lignes_v, y_ = [], pad                                  # chaque ligne à sa place (même pile que « v »)
        for (t_, c_, sz_) in (("« ALLAH SAISIT LES ÂMES", BLANC, 46), ("AU MOMENT DE LEUR MORT", BLANC, 46),
                              ("AINSI QUE CELLES QUI NE MEURENT PAS", BLANC, 46), ("AU COURS DE LEUR SOMMEIL. »", BLANC, 46)):
            li = _titre(t_, c_, sz_)
            li = li.crop(li.getbbox())
            lignes_v.append((li, (Wc - v.width) // 2 + (v.width - li.width) // 2, y_))
            y_ += li.height - 4
        tx["lignes_v"] = lignes_v
        carte.alpha_composite(v, ((Wc - v.width) // 2, pad))
        carte.alpha_composite(src, ((Wc - src.width) // 2, pad + v.height + 8))
        tx["carte"] = carte
        tx["r_titre"] = _pile([("AU RÉVEIL :", BLANC, 44)])
        tx["r_or"] = _pile([("AL-HAMDOU LILLÂHI LLADHÎ AHYÂNÂ", OR_, 46), ("BA'DA MÂ AMÂTANÂ", OR_, 46),
                            ("WA ILAYHI N-NOUCHOÛR", OR_, 46)], gap=-8)
        tx["r_bl"] = _pile([("LOUANGE À ALLAH", BLANC, 44), ("QUI NOUS A RENDU LA VIE", BLANC, 44),
                            ("APRÈS NOUS AVOIR FAIT MOURIR,", BLANC, 44), ("ET VERS LUI EST LA RÉSURRECTION", BLANC, 44)],
                           gap=-10)
        tx["z"] = [_titre("z", Z_COL, 56 + 14 * j, r=3) for j in range(3)]
        s._cache["tx"] = tx
        return tx

    def _image_sommeil(s, u):
        K = 6
        W_, H_ = 170 * K, s.PH_S * K
        tx = s._textes()
        t_v, t_n, t_r = s.t.get("verset"), s.t.get("nuit"), s.t.get("reveil")
        aube = s._e("reveil", u, 1.2)                                               # 0 = nuit, 1 = aube (Fajr)
        # le ciel (nuit → aube : la lueur monte sur l'horizon, AUCUN soleil), les toits, puis la chambre par-dessus
        im = s._ciel(False).copy()
        if aube > 0:
            im = Image.blend(im, s._ciel(True), aube)
        toits = s._toits_img(False)
        if aube > 0:
            toits = Image.blend(toits, s._toits_img(True), aube)
        im.alpha_composite(toits)
        ch = s._chambre(False)
        if aube > 0:
            ch = Image.blend(ch, s._chambre(True), aube)
        im.alpha_composite(ch)
        # le téléphone posé : allumé (lueur neutre, écran vers le plafond) jusqu'à « nuit », puis il s'éteint doucement
        # (un plan qui commence au réveil le trouve déjà éteint)
        reveil_seul = t_r is not None and t_r <= 0.3 and t_n is None and t_v is None
        on = 0.0 if reveil_seul else 1.0 - max(s._e("nuit", u, 0.6), s._e("reveil", u, 0.6))
        if on > 0.01:
            lay = s._cache.get("tel_on")
            if lay is None:
                lay = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
                ImageDraw.Draw(lay).ellipse([5 * K - 30, 112 * K, 21 * K + 30, 128 * K], fill=(*BLEU_TEL, 110))
                lay = lay.filter(ImageFilter.GaussianBlur(16))
                ImageDraw.Draw(lay).rectangle([6 * K, 125 * K, 20 * K - 1, 126 * K - 1], fill=(*BLEU_TEL, 255))
                s._cache["tel_on"] = lay
            im.alpha_composite(_fade(lay, on * (0.9 + 0.1 * math.sin(u * 2.0))))
        # Petit couché sur le côté droit, la main sous la joue : yeux ouverts → (verset) gêné → (nuit) il dort, petit
        # sourire → (réveil) il ouvre les yeux
        if t_r is not None and u >= t_r + 0.7:
            face = "content"
        elif t_n is not None and u >= t_n + (0.25 if t_n > 0.3 else -1.0):
            face = "calme"
        elif reveil_seul:                                                          # il dort encore, puis ouvre les yeux
            face = "calme"
        elif t_v is not None and u >= t_v + (0.3 if t_v > 0.3 else -1.0):
            face = "gene"
        else:
            face = "neutre"
        cl = face in ("neutre", "gene", "content") and ((u % 3.7) < 0.16)
        pn = s._perso_ch(face, cl, False)
        if aube > 0:
            pn = Image.blend(pn, s._perso_ch(face, cl, True), aube)
        im.alpha_composite(pn, (s.HX, s.HY))
        cc = s._couette_ch(False)
        if aube > 0:
            cc = Image.blend(cc, s._couette_ch(True), aube)
        im.alpha_composite(cc)
        # les « z » qui montent doucement (il dort), jusqu'au réveil
        if t_n is not None and u >= t_n:
            v = u - t_n
            fin = 1.0 if t_r is None else 1 - smooth((u - t_r) / 0.5)
            tx_, ty_ = s.HX + 16 * s.KP, s.HY + 2 * s.KP
            for j in range(3):
                vv = ((v + j * 0.6) % 1.8) / 1.8
                a = smooth(vv / 0.2) * (1 - smooth((vv - 0.7) / 0.3)) * smooth((v - 0.3) / 0.5) * fin
                if a > 0.01:
                    z_ = tx["z"][j]
                    im.alpha_composite(_fade(z_, a), (int(tx_ + j * 52 + 18 * math.sin(vv * 3 + j)),
                                                      int(ty_ - 40 - vv * 170 - j * 30)))
        # les textes
        debut = min([v_ for v_ in (t_v, t_n, t_r) if v_ is not None] + [9e9])
        if debut > 0.25:                                                             # la formule du coucher
            sort = 1 - smooth((u - debut) / 0.35)
            a_or = smooth(u / 0.4) * sort
            a_bl = smooth((u - 0.35) / 0.4) * sort
            a_su = smooth((u - 0.7) / 0.4) * sort
            s._pose(im, tx["sunna"], W_ / 2, 148, a_su)
            s._pose(im, tx["f_or"], W_ / 2, 280 + 10 * (1 - smooth(u / 0.4)), a_or)
            s._pose(im, tx["f_bl"], W_ / 2, 456 + 10 * (1 - smooth((u - 0.35) / 0.4)), a_bl)
        if t_v is not None:                                                         # le verset 39:42
            dec = 0.15 if t_v > 0.3 else 0.0
            a_c = s._a("verset", u, 0.6, fin=("nuit", "reveil"), dfin=0.45, dec=dec)
            if a_c > 0.01:
                # les 4 lignes du verset apparaissent l'une après l'autre, au rythme de la voix (07/11 : sans ça, la
                # carte restait 4 s immobile) ; le cadre et « CORAN 39:42 · EXTRAIT » sont là dès le début
                carte = tx["carte_vide"].copy()
                for (li, x_, y_), d_ in zip(tx["lignes_v"], T_LIGNES_VERSET):
                    al = smooth((u - t_v - d_) / 0.35)
                    if al > 0.01:
                        carte.alpha_composite(_fade(li, al), (int(x_), int(y_ + 10 * (1 - al))))
                s._pose(im, carte, W_ / 2, 300 + 16 * (1 - s._e("verset", u, 0.6, dec=dec)), a_c, maxw=W_ - 12)
        if t_r is not None:                                                         # au réveil
            a1 = s._e("reveil", u, 0.4, dec=0.35)
            a2 = s._e("reveil", u, 0.45, dec=0.8)
            a3 = s._e("reveil", u, 0.45, dec=1.25)
            s._pose(im, tx["r_titre"], W_ / 2, 52 + 8 * (1 - a1), a1)
            s._pose(im, tx["r_or"], W_ / 2, 204 + 10 * (1 - a2), a2, maxw=W_ - 20)
            s._pose(im, tx["r_bl"], W_ / 2, 456 + 10 * (1 - a3), a3, maxw=W_ - 20)       # au-dessus de la casquette
        return im


# ---------------------------------------------------------------- branchement (via explique_0611.py)
CLES = ("lit", "sommeil")


def _norm(m):
    return m.lower().replace("é", "e").replace("è", "e").replace("ê", "e")


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique_0611.ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte.
    {lit PETIT} : l'accroche (2e mot = le perso, PETIT par défaut). {sommeil} : la chambre et la formule ;
    {sommeil verset|nuit|reveil} : l'étape est ajoutée au dernier élément « sommeil » visible (ou en crée un)."""
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

    if k == "lit":
        schema._ajoute(t, Sommeil(brut, "lit", qui if qui in cast.CAST else "PETIT"))
    elif k == "sommeil":
        if sous in Sommeil.ETAPES:
            etape(Sommeil, sous, "sommeil", lambda: Sommeil(brut, "sommeil"))
        else:
            schema._ajoute(t, Sommeil(brut, "sommeil"))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "lit":
        return t + 1.6
    if k == "sommeil":
        return t + dict(verset=1.2, nuit=1.4, reveil=2.6).get(sous, 1.4)
    return None
