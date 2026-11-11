# DÉMONSTRATION EN IMAGE DU 07/11/2026 — Short duo ISL17 « Ne jure JAMAIS sur ta mère » (format consigne).
#   {jure PETIT}        accroche : un couloir de lycée en plein jour ; Petit en entier, très grand, la main levée, sûr de
#                       lui : bulle « SUR LA TÊTE DE MA MÈRE ! » ; derrière lui, son cahier « DEVOIRS » avec une grosse
#                       coche verte (il dit vrai) ; vers u = 1, un panneau STOP glisse doucement devant le bas de la bulle
#   {serment}           un tableau sombre ; en haut, la liste des serments interdits : SUR TON PÈRE / SUR TA MÈRE
#                       (blanc) ; {serment pere|mere} un trait rouge les barre ; {serment allah} en dessous, « PAR
#                       ALLAH » en or, avec une lueur douce (jamais barré, aucun trait ne le touche) ; {serment frere}
#                       SUR TON FRÈRE / SUR TA VIE arrivent seulement là (fondu glissé de 0,25 s, la liste s'allonge
#                       au-dessus de PAR ALLAH) puis sont barrés l'un après l'autre (+0,3 s, +0,55 s) ; {serment tais}
#                       juste sous PAR ALLAH, « … OU TU TE TAIS » (Petit, le doigt sur la bouche) : on lit « PAR ALLAH
#                       … OU TU TE TAIS » ; {serment vrai} « « NE JUREZ PAR ALLAH // QUE SI VOUS DITES VRAI » » et
#                       « ABOU DAWOUD 3248 » (Abou Dawoud 3248 · Boukhari 6646 · Mouslim 1646)
# Une étape qui ouvre un nouveau plan (ex. {serment frere} après une réplique de Petit) reprend le tableau où il en
# était : les étapes d'avant sont déjà faites. Mouvements doux (glissés, fondus) ; aucun prophète, ange ni Compagnon
# dessiné ; le nom d'Allah n'est jamais barré.
# Branché par explique_0611.py (CLES, ordre, fin_anim), comme explique_0411b.
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import cast
import pxv
from px import Px, TAHOMA
from pxv import smooth
from explique import _titre, _fade, _os, BLANC, JAUNE
from explique_0411 import OL, _peau, _sprite, _buste, _grand
from explique_0411b import _Base, _translucide, ROUGE, OR_

ENCRE = (24, 20, 34)
ROUGE_MOT = (212, 44, 44)


def _dk(c, k=0.72):
    return tuple(int(v * k) for v in c)


def _lt(c, k=0.25):
    return tuple(int(v + (255 - v) * k) for v in c)


def _sol_carreaux(c, y0, y1, cx, horizon, c1, c2, joint, cell=0.3, kx=120.0):
    """Carrelage en perspective (comme le couloir de la scène), dans un dessin Px, de y0 à y1."""
    m = c.mask_rect(0, y0, c.w, y1)
    c.fill(m, c1)
    dz = np.maximum(c.yy + 0.5 - horizon, 1.0)
    z = 160.0 / dz
    xw = (c.xx + 0.5 - cx) * z / kx
    c.fill(((np.floor(xw / cell) + np.floor(z / cell)) % 2 == 0) & m, c2)
    fx, fz = xw / cell - np.floor(xw / cell), z / cell - np.floor(z / cell)
    c.fill(((fx < 0.05) | (fz < 0.07)) & m, joint)
    return m


def _cahier(c, x0, y0, x1, y1):
    """Le cahier de devoirs ouvert, scotché sur les casiers : pages lignées, écriture, spirale, grosse coche verte."""
    xm = (x0 + x1) // 2
    c.tint(c.mask_rect(x0 + 2, y0 + 2, x1 + 2, y1 + 2), (20, 20, 44), 0.38)          # son ombre sur les casiers
    couv = c.mask_rrect(x0, y0, x1, y1, 2)
    c.shape(couv, (52, 86, 160), shade=(36, 62, 120), band=1, olcol=OL)
    rng = np.random.default_rng(7)
    for j, (a, b) in enumerate(((x0 + 2, xm - 1), (xm + 1, x1 - 2))):
        page = c.mask_rect(a, y0 + 1, b, y1 - 2)
        c.fill(page, (250, 250, 242))
        c.fill(c.mask_rect(a, y1 - 3, b, y1 - 2), (226, 226, 216))
        for y in range(y0 + 7, y1 - 3, 4):                                          # les lignes du cahier
            c.fill(c.mask_rect(a + 1, y, b - 1, y + 1), (184, 210, 238))
        if j == 0:
            c.fill(c.mask_rect(a + 4, y0 + 1, a + 5, y1 - 3), (238, 150, 150))       # la marge
        lignes = range(y0 + 6, y1 - 4, 4) if j == 0 else range(y0 + 6, y0 + 15, 4)
        for y in lignes:                                                            # l'écriture (au stylo bleu)
            x = a + (6 if j == 0 else 2)
            while x < b - 3:
                L = int(rng.integers(2, 6))
                c.fill(c.mask_rect(x, y - 1, min(b - 2, x + L), y), (58, 74, 146))
                x += L + 1 + int(rng.integers(0, 2))
    for y in range(y0 + 2, y1 - 2, 3):                                              # la spirale
        c.fill(c.mask_rect(xm - 1, y, xm + 1, y + 2), (96, 100, 118))
        c.px(xm - 1, y, (186, 190, 204))
    coche = _os(c, xm + 4, y0 + 21, xm + 10, y1 - 7, 4) | _os(c, xm + 10, y1 - 7, x1 + 2, y0 + 1, 4)
    c.shape(coche, (70, 190, 90), shade=(40, 138, 62), light=(150, 232, 158), band=1, olcol=OL)
    for (tx, ty) in ((x0 - 2, y0 - 2), (x1 - 6, y0 - 2)):                          # deux bouts de scotch
        sc = c.mask_rect(tx, ty, tx + 8, ty + 4)
        c.tint(sc, (255, 246, 196), 0.75)
        c.dither(sc, (255, 255, 236), 0.3)


class Serment(_Base):
    """{jure PETIT} : accroche, Petit très grand la main levée, « SUR LA TÊTE DE MA MÈRE ! », son cahier « DEVOIRS » coché
    derrière lui (il dit vrai), puis un panneau STOP glisse devant le bas de la bulle.
    {serment} : le tableau des serments (en haut les serments interdits, dessous « PAR ALLAH … OU TU TE TAIS », en bas
    la règle) ; {serment pere|mere|allah|frere|tais|vrai} (Abou Dawoud 3248 = Nasa'i 3769 ; Boukhari 6646 · Mouslim
    1646 : « que celui qui jure, jure par Allah ou se taise »)."""
    PW_, PH_ = 170, 160
    SOL = 116                                  # pied du mur (pixels du dessin)
    ETAPES = ("pere", "mere", "allah", "frere", "tais", "vrai")
    ENTREE = 0.3                               # une étape dite à l'apparition du tableau s'anime après son fondu
    # -- l'accroche (pixels d'écran)
    PIEDS = (520, 934)                         # milieu des pieds de Petit
    HAUT_PERSO = 670                           # sa taille à l'écran (≈ 70 % de l'image)
    BULLE = (110, 24)                          # coin haut-gauche de la bulle
    ZOOM = 0.03                                # on s'approche de lui (rien ne sort du cadre)
    QUEUE = 0.68                               # la queue de la bulle (fraction de sa largeur)
    STOP_C = (790, 276)                        # centre du panneau STOP, une fois arrivé
    T_STOP = 1.0                               # il glisse à partir de là (0,55 s)
    CAHIER = (6, 56, 62, 96)                   # le cahier (pixels du dessin)
    # -- le tableau, de haut en bas : les serments interdits, PAR ALLAH, « … OU TU TE TAIS », la règle (2 lignes), la
    #    source. PAS = écart (pixels d'écran) entre le milieu d'une ligne et celui de la précédente quand sa place est
    #    ouverte (une place fermée ne prend rien) ; HAUT / BAS = ce qui dépasse au-dessus de la 1re ligne / sous la
    #    dernière ; le bloc reste centré sur le tableau (CY), sans saut
    LIGNES = ("pere", "mere", "frere", "vie", "allah", "tais", "vrai", "src")
    PAS = dict(pere=0, mere=97, frere=97, vie=90, allah=100, tais=92, vrai=116, src=152)   # È : un peu plus d'air
    HAUT = 42
    BAS = dict(mere=42, frere=42, vie=35, allah=41, tais=75, vrai=116, src=27)
    CY = 452
    SERMENTS = (("pere", "SUR TON PÈRE", "pere", 0.0), ("mere", "SUR TA MÈRE", "mere", 0.0),
                ("frere", "SUR TON FRÈRE", "frere", 0.3), ("vie", "SUR TA VIE", "frere", 0.55))   # (ligne, texte, étape, barré à +…)
    TAIS = "… OU TU TE TAIS"
    REGLE = ("« NE JUREZ PAR ALLAH", "QUE SI VOUS DITES VRAI »")
    PAS_VRAI = 80                              # écart entre les deux lignes de la règle
    DX_CHUT = 16                               # écart entre Petit (le doigt sur la bouche) et « … OU TU TE TAIS »
    TAILLE = 64

    def __init__(s, cmd, mode="regle", who="PETIT"):
        super().__init__(cmd)
        s.mode = "jure" if mode == "jure" else "regle"
        s.who = who if who in cast.CAST else "PETIT"
        s.negatif = s.mode == "jure"

    # ------------------------------------------------------------ étapes (une étape sautée = déjà faite)
    def _te(s, nom):
        """Instant où l'étape s'anime : celui de son mot (au plus tôt après le fondu d'entrée) ; -9 si elle n'a pas de
        mot mais qu'une étape suivante en a un (nouveau plan : le tableau reprend où il en était) ; None sinon."""
        if nom in s.t:
            return max(s.t[nom], s.ENTREE)
        i = s.ETAPES.index(nom)
        if any(e in s.t for e in s.ETAPES[i + 1:]):
            return -9.0
        return None

    def _e(s, nom, u, d=0.35, dec=0.0):
        t0 = s._te(nom)
        if t0 is None or u < t0 + dec:
            return 0.0
        return smooth((u - t0 - dec) / d)

    def _suite(s):
        """Vrai si le tableau s'ouvre sur une étape déjà avancée (les premières étapes sont sous-entendues)."""
        return any(s._te(n) == -9.0 for n in s.ETAPES)

    def sons_el(s):
        if s.mode == "jure":
            return [(s.T_STOP, "tr_whoosh_doux", 0.02, None)]
        out = []
        for nom, son, g, dec in (("pere", "imp_tampon", 0.02, 0.0), ("mere", "imp_tampon", 0.02, 0.0),
                                 ("allah", "sa_scintillement", 0.04, 0.0),
                                 ("frere", "imp_tampon", 0.02, 0.3)):            # frere : sur le 1er trait (FRÈRE)
            if nom in s.t:
                out.append((s._te(nom) + dec, son, g, None))
        return out

    # ------------------------------------------------------------ l'accroche {jure PETIT}
    def _couloir(s):
        if "couloir" in s._cache:
            return s._cache["couloir"]
        W, H, SOL = s.PW_, s.PH_, s.SOL
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        mur = c.mask_rect(0, 0, W, SOL) & tout_
        c.vgrad(mur, 0, SOL, (232, 228, 206), (244, 240, 222), steps=5)
        for j in range(3):                                                         # le jour entre par la gauche
            x = 8 + 58 * j
            c.tint(c.mask_poly([(x, 0), (x + 20, 0), (x + 62, SOL), (x + 42, SOL)]) & mur, (255, 252, 236), 0.35)
        c.shape(c.mask_rect(0, 0, W, 6) & tout_, (238, 238, 232), shade=(206, 206, 198), band=1, sdir="bottom",
                olcol=(190, 190, 184))
        for x in (16, 70, 124):                                                    # néons du plafond
            c.shape(c.mask_rect(x, 7, x + 30, 9), (255, 254, 240), shade=(220, 220, 210), band=1, olcol=(150, 150, 146))
        for k in range(5):                                                         # les casiers (bleu / rouge)
            x0 = k * 13
            col_ = (60, 110, 190) if k % 2 == 0 else (200, 70, 70)
            lk = c.mask_rect(x0 + 1, 40, x0 + 13, SOL - 3) & tout_
            c.shape(lk, col_, shade=_dk(col_), light=_lt(col_, 0.2), band=1, olcol=OL)
            for y in (44, 47, 50):
                c.fill(c.mask_rect(x0 + 4, y, x0 + 10, y + 1), _dk(col_, 0.6))
            c.fill(c.mask_rect(x0 + 10, 76, x0 + 11, 84), (206, 210, 220))
        c.fill(c.mask_rect(0, 37, 66, 40), (78, 84, 98))                           # le dessus des casiers
        cadre = c.mask_rect(124, 36, 164, SOL - 3)                                 # la porte de la classe
        c.shape(cadre, (214, 214, 206), shade=(176, 176, 168), band=1, olcol=OL)
        porte = c.mask_rect(128, 40, 160, SOL - 3)
        c.shape(porte, (150, 104, 66), shade=(110, 74, 46), light=(176, 128, 86), band=2, olcol=OL)
        vitre = c.mask_rect(134, 47, 154, 70)
        c.fill(vitre, (186, 218, 238))
        c.dither(vitre & c.mask_poly([(134, 60), (146, 47), (150, 47), (134, 66)]), (232, 244, 252), 0.6)
        c.outline(vitre, (110, 74, 46))
        c.shape(c.mask_rect(153, 80, 157, 84), (226, 192, 90), shade=(176, 140, 60), band=1, olcol=OL)
        c.shape(c.mask_rect(0, SOL - 3, W, SOL) & tout_, (150, 160, 150), shade=(120, 130, 120), band=1, sdir="bottom",
                olcol=(104, 112, 104))
        sol = _sol_carreaux(c, SOL, H, 90, 58, (214, 220, 214), (198, 206, 200), (176, 184, 178)) & tout_
        c.dither(c.mask_rect(0, SOL, W, SOL + 8) & sol, (236, 240, 236), 0.25)
        for (xa, xb) in ((14, 44), (104, 136)):                                    # taches de soleil au sol
            c.tint(c.mask_poly([(xa, SOL + 1), (xb, SOL + 1), (xb + 16, H), (xa + 22, H)]) & sol, (255, 250, 228), 0.3)
        _cahier(c, *s.CAHIER)
        c.al &= tout_
        im = c.img(s.K, rgba=True)
        x0, y0, x1, y1 = s.CAHIER
        dv = _titre("DEVOIRS", BLANC, 50)
        im.alpha_composite(dv, (int((x0 + x1) / 2 * s.K - dv.width / 2), int(y0 * s.K - dv.height / 2 - 14)))
        s._cache["couloir"] = im
        return im

    def _perso(s, mix=0.0, cligne=False):
        """Petit en entier, agrandi ; mix > 0 : la main pas encore tout à fait levée (geste du moteur, pose_de) ;
        renvoie (image, (x, y) du milieu de ses pieds dans l'image)."""
        mix = round(mix * 10) / 10
        cle = ("perso", mix, cligne)
        if cle not in s._cache:
            if "bb_perso" not in s._cache:
                s._cache["bb_perso"] = _sprite(s.who, "salut", "content").getbbox()
            bb = s._cache["bb_perso"]
            k = max(6, min(10, int(s.HAUT_PERSO / (bb[3] - bb[1]))))
            kw = dict(pose_de="neutre", mix=mix) if mix > 0 else {}
            sp = _sprite(s.who, "salut", "content", cligne=cligne, **kw)
            s._cache[cle] = (_grand(sp.crop((0, bb[1] - 2, sp.width, bb[3])), k), (22 * k, (bb[3] - bb[1] + 2) * k))
        return s._cache[cle]

    def _bulle_jure(s):
        """Grosse bulle blanche à bord noir (pixel art), texte sombre, « MÈRE » en rouge ; renvoie (image, pointe)."""
        if "bulle" in s._cache:
            return s._cache["bulle"]
        K = s.K
        f = ImageFont.truetype(pxv.SEGOE_BLACK, 72)
        morceaux = [[("SUR LA TÊTE", ENCRE)], [("DE MA ", ENCRE), ("MÈRE", ROUGE_MOT), (" !", ENCRE)]]
        larg = [sum(f.getlength(t_) for t_, _ in l_) for l_ in morceaux]
        asc, desc = f.getmetrics()
        lh = asc + desc - 10
        tw, th = int(max(larg)) + 2, lh * 2
        pad_x, pad_y = 36, 22
        bw, bh = math.ceil((tw + 2 * pad_x) / K), math.ceil((th + 2 * pad_y) / K)
        Qh = 8                                                                     # hauteur de la queue (pixels du dessin)
        c = Px(bw + 2, bh + Qh + 3, alpha=True)
        corps = c.mask_rrect(1, 1, bw + 1, bh + 1, 6)
        qx = int(bw * s.QUEUE)
        queue = c.mask_poly([(qx - 5, bh - 1), (qx + 4, bh - 1), (qx + 6, bh + Qh)])
        m = corps | queue
        c.fill(m, (252, 252, 252))
        c.fill(c.mask_rect(2, bh - 1, bw, bh + 1) & corps, (228, 228, 238))         # petite ombre en bas
        c.outline(m, OL)
        im = c.img(K, rgba=True)
        d = ImageDraw.Draw(im)
        y = K + pad_y + (bh * K - th - 2 * pad_y) // 2
        for l_, w_ in zip(morceaux, larg):
            x = K + (bw * K - w_) / 2
            for t_, col in l_:
                d.text((x, y), t_, font=f, fill=(*col, 255))
                x += f.getlength(t_)
            y += lh
        pointe = ((qx + 6) * K + K // 2, (bh + Qh) * K)
        s._cache["bulle"] = (im, pointe)
        return s._cache["bulle"]

    def _stop(s):
        """Le panneau STOP (octogone rouge, liseré blanc, lettres blanches) et son ombre."""
        if "stop" in s._cache:
            return s._cache["stop"]
        N, R = 48, 22.5
        c = Px(N, N, alpha=True)
        ctr = N / 2

        def octo(r):
            return c.mask_poly([(ctr + r * math.cos(math.radians(22.5 + 45 * j)), ctr + r * math.sin(math.radians(22.5 + 45 * j)))
                                for j in range(8)])
        ext, inte = octo(R), octo(R - 2.6)
        c.fill(ext, (248, 248, 246))
        c.edge(ext, (212, 212, 214), "bottom", 1)
        c.outline(ext, OL)
        c.shape(inte, (214, 44, 44), shade=(166, 28, 32), light=(238, 92, 84), band=1, ol=False)
        m_txt = Px(N, N, alpha=True).text((ctr + 0.5, ctr + 1), "STOP", (255, 255, 255), size=13, font=TAHOMA, anchor="mm")
        c.fill(np.roll(np.roll(m_txt, 1, 0), 1, 1) & inte, (140, 20, 26))           # ombre des lettres
        c.fill(m_txt, (255, 255, 255))
        im = c.img(s.K, rgba=True)
        ombre = Image.new("RGBA", (im.width + 80, im.height + 80), (0, 0, 0, 0))
        a = np.array(im)[..., 3]
        sh = Image.fromarray((a > 0).astype(np.uint8) * 110, "L")
        lay = Image.new("RGBA", im.size, (20, 16, 30, 0))
        lay.putalpha(sh)
        ombre.alpha_composite(lay, (40, 40))
        ombre = ombre.filter(ImageFilter.GaussianBlur(10))
        s._cache["stop"] = (im, ombre)
        return s._cache["stop"]

    def _image_jure(s, u):
        im = s._couloir().copy()
        W_, H_ = im.size
        mix = 1 - smooth((u + 0.8) / 0.45)                                         # il lève la main pour jurer
        cligne = 2.3 <= u < 2.42                                                   # un clignement d'yeux, naturel
        sp, (ax, ay) = s._perso(mix, cligne)
        px_, py_ = s.PIEDS
        _translucide(im, lambda d: d.ellipse([px_ - 150, py_ - 16, px_ + 150, py_ + 14], fill=(60, 56, 60, 80)))
        im.alpha_composite(sp, (int(px_ - ax), int(py_ - ay)))
        # la bulle arrive en douceur (u -0.3 → 0.2) : elle grandit depuis la pointe de sa queue
        e_b = smooth((u + 0.3) / 0.5)
        if e_b > 0.01:
            b, (qx, qy) = s._bulle_jure()
            bx, by = s.BULLE
            tx, ty = bx + qx, by + qy                                               # la pointe, fixe
            k_ = 0.86 + 0.14 * e_b
            if k_ < 0.999:
                b = b.resize((int(b.width * k_), int(b.height * k_)), Image.BILINEAR)
            im.alpha_composite(_fade(b, e_b), (int(tx - qx * k_), int(ty - qy * k_)))
        # le panneau STOP glisse depuis la droite et se pose devant le bas de la bulle (sans secousse)
        e_s = smooth((u - s.T_STOP) / 0.55)
        if e_s > 0.001:
            st, om = s._stop()
            cx = s.STOP_C[0] + 360 * (1 - e_s)
            cy = s.STOP_C[1]
            a_s = smooth((u - s.T_STOP) / 0.2)
            im.alpha_composite(_fade(om, a_s), (int(cx - om.width / 2 + 10), int(cy - om.height / 2 + 14)))
            im.alpha_composite(_fade(st, a_s), (int(cx - st.width / 2), int(cy - st.height / 2)))
        # on s'approche lentement de lui
        z = 1.0 + s.ZOOM * smooth((u + 1.0) / 4.0)
        if z > 1.001:
            w2, h2 = int(W_ / z), int(H_ / z)
            xc, yc = (W_ - w2) // 2, (H_ - h2) // 2
            im = im.crop((xc, yc, xc + w2, yc + h2)).resize((W_, H_), Image.BILINEAR)
        return im

    # ------------------------------------------------------------ le tableau {serment …}
    def _tableau(s):
        if "tableau" in s._cache:
            return s._cache["tableau"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(1, 1, W - 1, H - 3, 4)
        c.shape(tout_, (150, 104, 66), shade=(110, 74, 46), light=(186, 138, 94), band=2, olcol=OL)
        for y in range(6, H - 4, 7):                                               # le grain du bois
            c.fill(c.mask_rect(1, y, W - 1, y + 1) & tout_ & ~c.mask_rect(4, 4, W - 4, 152), (136, 94, 58))
        tab = c.mask_rect(4, 4, W - 4, 151)
        c.vgrad(tab, 4, 151, (44, 70, 62), (32, 54, 48), steps=5)
        for (x, y, rx, ry) in ((34, 24, 26, 4), (132, 60, 24, 3), (46, 118, 30, 4), (128, 136, 22, 3)):
            c.dither(c.mask_ell(x, y, rx, ry) & tab, (52, 80, 71), 0.16)           # traces de craie effacée
        c.fill(c.mask_rect(4, 4, W - 4, 5), (24, 40, 36))                          # ombre du cadre
        c.fill(c.mask_rect(4, 4, 5, 151), (24, 40, 36))
        auget = c.mask_rect(2, 151, W - 2, 156)                                    # le rebord (craie, brosse)
        c.shape(auget, (160, 112, 72), shade=(116, 78, 48), light=(196, 146, 100), band=1, sdir="bottom", olcol=OL)
        c.shape(c.mask_rect(124, 148, 132, 151), (244, 244, 234), shade=(206, 206, 196), band=1, olcol=OL)
        brosse = c.mask_rect(24, 146, 40, 151)
        c.shape(brosse, (178, 150, 110), shade=(140, 116, 82), band=1, olcol=OL)
        c.fill(c.mask_rect(24, 149, 40, 151), (70, 76, 96))
        s._cache["tableau"] = c.img(s.K, rgba=True)
        return s._cache["tableau"]

    def _milieu(s, txt, size):
        """Décalage vertical (pixels) entre le centre d'une étiquette _titre et le milieu de ses majuscules (les
        accents et l'ombre portée décentrent l'image) : le trait rouge passe au milieu des lettres."""
        cle = ("mil", txt, size)
        if cle not in s._cache:
            f = ImageFont.truetype(pxv.SEGOE_BLACK, size)
            d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
            bb = d0.textbbox((0, 0), txt, font=f, stroke_width=8)
            hb = d0.textbbox((0, 0), "H", font=f)
            lab = s._lab(txt, BLANC, size)
            s._cache[cle] = 32 - bb[1] + (hb[1] + hb[3]) / 2 - lab.height / 2
        return s._cache[cle]

    def _barre(s, im, txt, xc, yc, p):
        """Trait rouge qui barre une ligne de gauche à droite (p = avancement 0 → 1), au milieu des lettres."""
        if p <= 0:
            return
        lab = s._lab(txt, BLANC, s.TAILLE)
        cle = ("bb", txt)
        if cle not in s._cache:
            s._cache[cle] = lab.getbbox()
        bb = s._cache[cle]
        ym = yc + s._milieu(txt, s.TAILLE)
        xa = xc - lab.width / 2 + bb[0] - 10
        xb = xc - lab.width / 2 + bb[2] + 10
        ya, yb = ym + 5, ym - 5                                                     # un peu penché, comme à la main
        xe, ye = xa + (xb - xa) * p, ya + (yb - ya) * p
        d = ImageDraw.Draw(im)
        d.line([(xa, ya + 5), (xe, ye + 5)], fill=(16, 12, 24, 255), width=10)       # son ombre, en dessous
        d.line([(xa, ya), (xe, ye)], fill=(*ROUGE, 255), width=11)

    def _chut(s):
        """Petit, l'index sur la bouche fermée (« chut » : « … OU TU TE TAIS »), en pixel art."""
        if "chut" in s._cache:
            return s._cache["chut"]
        b, (mx, my) = _buste("PETIT", "neutre")                                     # bouche en (15, 18), yeux rangée 12-14
        p = _peau("PETIT")
        c = Px(b.width, b.height + 3, alpha=True)
        c.paste(b, 0, 0)
        c.fill(c.mask_rect(mx - 3, my, mx + 5, my + 1), (150, 64, 70))              # la bouche, bien fermée
        manche = c.mask_rect(mx - 4, my + 8, mx + 6, b.height + 3)                  # la manche du sweat, en bas
        c.shape(manche, (200, 50, 50), shade=(146, 34, 48), light=(221, 111, 103), band=1, olcol=OL)
        doigt = c.mask_rect(mx, my - 1, mx + 2, my + 3)                             # l'index levé, sur les lèvres
        c.shape(doigt, p["b"], shade=p["s"], band=1, olcol=OL)
        poing = c.mask_rrect(mx - 3, my + 2, mx + 5, my + 9, 2)                     # le poing devant le menton
        c.shape(poing, p["b"], shade=p["s"], light=p["h"], band=1, olcol=OL)
        for x in (mx - 1, mx + 2):                                                  # les doigts repliés
            c.fill(c.mask_rect(x, my + 5, x + 1, my + 8), p["s"])
        c.fill(doigt, p["b"])                                                       # l'index sort du poing
        c.fill(c.mask_rect(mx + 1, my - 1, mx + 2, my + 3), p["s"])
        c.fill(c.mask_rect(mx, my - 1, mx + 2, my), (244, 204, 190))                # l'ongle
        s._cache["chut"] = c.img(5, rgba=True)
        return s._cache["chut"]

    def _ouvert(s, cle, u):
        """Place de la ligne cle dans le tableau (0 → 1). Une étape déjà faite, ou dite à l'ouverture du tableau, a sa
        place dès le début ; PAR ALLAH et « … OU TU TE TAIS » aussi (rien ne bouge à leur mot) ; FRÈRE / VIE : la
        liste s'allonge en douceur juste AVANT le mot (0,6 s), ils arrivent dans une place déjà ouverte ; la règle :
        le contenu remonte doucement à son mot (0,8 s)."""
        if cle in ("pere", "mere"):
            return 1.0
        etape = {"vie": "frere", "src": "vrai"}.get(cle, cle)
        t_ = s._te(etape)
        if t_ is None:
            return 0.0
        if t_ == -9.0 or s.t.get(etape, 99.0) <= s.ENTREE or etape in ("allah", "tais"):
            return 1.0
        if etape == "frere":
            return smooth((u - t_ + 0.6) / 0.6)
        return smooth((u - t_) / 0.8)

    def _places(s, u):
        """Milieu (pixels d'écran) de chaque ligne à l'instant u : chaque ligne se range sous la précédente à mesure
        que sa place s'ouvre, et le bloc reste centré sur le tableau (glissés doux, jamais de saut)."""
        Y, y, bas = {}, 0.0, s.BAS["mere"]
        for cle in s.LIGNES:
            o = s._ouvert(cle, u)
            y += s.PAS[cle] * o
            Y[cle] = y
            if cle in s.BAS:
                bas += (s.BAS[cle] - bas) * o
        y0 = s.CY - (y + bas - s.HAUT) / 2
        return {k_: v + y0 for k_, v in Y.items()}

    def _tais(s):
        """« … OU TU TE TAIS » avec, à sa gauche, Petit le doigt sur la bouche ; renvoie (image, dx) : dx = décalage du
        milieu de l'image par rapport au milieu du TEXTE (le texte se centre juste sous PAR ALLAH)."""
        if "tais_img" not in s._cache:
            ch, lab = s._chut(), s._lab(s.TAIS, BLANC, s.TAILLE)
            bb = lab.getbbox()
            comb = Image.new("RGBA", (ch.width + s.DX_CHUT + bb[2] - bb[0], max(ch.height, lab.height)), (0, 0, 0, 0))
            comb.alpha_composite(ch, (0, (comb.height - ch.height) // 2))
            comb.alpha_composite(lab, (ch.width + s.DX_CHUT - bb[0], (comb.height - lab.height) // 2 + 8))
            dx = comb.width / 2 - (ch.width + s.DX_CHUT + (bb[2] - bb[0]) / 2)
            s._cache["tais_img"] = (comb, dx)
        return s._cache["tais_img"]

    def _image_regle(s, u):
        im = s._tableau().copy()
        xc = im.width / 2
        Y = s._places(u)
        # la lueur de « PAR ALLAH » d'abord, derrière tout le reste (elle ne voile ni les traits ni le texte)
        e_a = s._e("allah", u, 0.45)
        y_a = Y["allah"] + 26 * (1 - e_a)
        if e_a > 0.01:
            if "lueur" not in s._cache:
                lay = Image.new("RGBA", (760, 260), (0, 0, 0, 0))
                ImageDraw.Draw(lay).ellipse([90, 66, 670, 194], fill=(255, 210, 90, 150))
                s._cache["lueur"] = lay.filter(ImageFilter.GaussianBlur(34))
            lu = s._cache["lueur"]
            al = e_a * (0.82 + 0.18 * math.sin(2 * math.pi * u / 2.6))
            im.alpha_composite(_fade(lu, al), (int(xc - lu.width / 2), int(y_a - lu.height / 2)))
        # en haut, les serments interdits : PÈRE et MÈRE dès le début ; FRÈRE et VIE seulement à {frere} (fondu glissé
        # de 0,25 s), puis barrés l'un après l'autre (+0,3 s, +0,55 s)
        suite, t_f = s._suite(), s._te("frere")
        for i, (cle, txt, etape, dec) in enumerate(s.SERMENTS):
            if etape != "frere":
                a_in = 1.0 if suite else smooth((u - 0.08 * i) / 0.35)
            elif t_f is None:
                continue
            else:
                a_in = 1.0 if t_f == -9.0 else smooth((u - t_f) / 0.25)
            if a_in <= 0.01:
                continue
            t0 = s._te(etape)
            p = smooth((u - t0 - dec) / 0.3) if t0 is not None and u >= t0 + dec else 0.0
            a = a_in * (1 - 0.2 * smooth((u - t0 - dec - 0.3) / 0.3)) if p >= 1 else a_in
            x = xc - 30 * (1 - a_in)
            s._pose(im, s._lab(txt, BLANC, s.TAILLE), x, Y[cle], a)
            s._barre(im, txt, x, Y[cle], p)
        # juste sous PAR ALLAH : « … OU TU TE TAIS » (le texte centré sous lui) et Petit, l'index sur la bouche
        e_t = s._e("tais", u, 0.35)
        if e_t > 0.01:
            comb, dx = s._tais()
            s._pose(im, comb, xc + dx - 30 * (1 - e_t), Y["tais"], e_t)
        # en bas, la règle (Abou Dawoud 3248), entre guillemets ; si le contenu doit d'abord remonter, elle attend un peu
        dec_v = 0.0 if s._ouvert("vrai", -9.0) >= 1.0 else 0.3
        e_v = s._e("vrai", u, 0.4, dec=dec_v)
        if e_v > 0.01:
            dy = 22 * (1 - e_v)
            for j, txt in enumerate(s.REGLE):
                s._pose(im, s._lab(txt, JAUNE, 60), xc, Y["vrai"] + j * s.PAS_VRAI + dy, e_v)
            s._pose(im, s._lab("ABOU DAWOUD 3248", BLANC, 44), xc, Y["src"], s._e("vrai", u, 0.35, dec=dec_v + 0.35))
        # « PAR ALLAH » en or : posé en dernier, rien ne le recouvre ni ne le touche
        if e_a > 0.01:
            s._pose(im, s._lab("PAR ALLAH", OR_, 84), xc, y_a, e_a)
        return im

    def image(s, u):
        return s._image_jure(u) if s.mode == "jure" else s._image_regle(u)


# ---------------------------------------------------------------- branchement (explique_0611 → explique.Schema)
CLES = ("jure", "serment")


def _norm(m):
    return (m.lower().replace("é", "e").replace("è", "e").replace("ê", "e").replace("â", "a").replace("î", "i")
            .replace("û", "u"))


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique_0611.ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
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

    if k == "jure":
        schema._ajoute(t, Serment(brut, "jure", qui if qui in cast.CAST else "PETIT"))
    elif k == "serment":
        if sous in Serment.ETAPES:
            etape(Serment, sous, "regle", lambda: Serment(brut, "regle"))
        else:
            schema._ajoute(t, Serment(brut, "regle"))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "jure":
        return t + 1.8
    if k == "serment":
        return t + dict(pere=0.7, mere=0.7, allah=1.1, frere=1.5, tais=1.1, vrai=1.8).get(sous, 0.9)
    return None
