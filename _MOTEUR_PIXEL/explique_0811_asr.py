# DÉMONSTRATIONS EN IMAGE DU 08/11/2026 — Short ISL27 « Encore un match ? Prie l'Asr d'abord ! » (consigne +
# avertissement). Même principe que explique_0611_dette.py : le sens propre du hadith, montré en grand, mouvements
# doux (glissés, fondus, jamais de secousse ni de flash). Aucun prophète, ange, Compagnon ni Chaytan dessiné (ni ombre
# à cornes) ; la famille = silhouettes neutres sans visage ; rien de cassé, personne ne meurt. Partout un soleil
# d'après-midi HAUT et BLANC (Boukhari 550) ; du jaune seulement sur la zone « jaunissement » de la frise.
#   {soleilbas PETIT}  accroche, vue à ta place, au city stade du parc en plein après-midi : ciel bleu, soleil haut
#                      et blanc, grillage vert et ombres longues ; le BALLON roule du fond vers toi, grossit et
#                      s'arrête devant tes baskets ; au premier plan ton téléphone posé au bord du terrain : la
#                      notification « (mosquée) ASR » apparaît en fondu et glisse vers toi ; au fond à gauche, Petit
#                      bras en l'air sautille, bulle blanche « ENCORE UN MATCH ! »
#   {asr}              la carte « COMME SI… » : en haut « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : » (petit),
#                      « « CELUI QUI RATE L'ASR… », en jaune « … C'EST COMME SI ON LUI AVAIT PRIS SA FAMILLE ET SES
#                      BIENS » » (entre guillemets : parole du Prophète) ; sur une table en bois (lumière d'après-midi
#                      en biais) arrivent l'un après l'autre PENDANT le ﷺ (u = 1,0 / 2,4 / 3,8 s) un cadre photo
#                      (4 silhouettes neutres), une maison-maquette (fenêtres éclairées) et un portefeuille ouvert
#                      (billets), et la caméra avance lentement (+5 % sur 6 s) : jamais de carte figée ;
#                      « SA FAMILLE », accolade « SES BIENS » ; bandeau « COMME SI… » en italique tout du long ;
#                      {asr famille} les silhouettes s'effacent une à une, le cadre reste vide (reflet), « SA
#                      FAMILLE » passe en gris ;
#                      {asr biens} la maison et le portefeuille s'estompent en montant (vapeur dorée), « SES
#                      BIENS » en gris ;
#                      {asr vide} la caméra recule doucement, le cadre vide glisse au centre : « NI FAMILLE NI
#                      BIENS… » (rouge doux) et « C'EST AUSSI GRAVE QUE ÇA » ; la console posée sur la table
#                      s'estompe elle aussi ; vignette de Petit choqué (goutte de sueur), après le glissé du cadre
#   {asr rater}        ciel d'après-midi ; la grande frise horaire monte du bas : « DÉBUT DE L'ASR » (soleil haut,
#                      blanc), « LE SOLEIL JAUNIT », « COUCHER » ; un soleil-curseur blanc glisse ; « RATER L'ASR = »
#                      « LA LAISSER PASSER SON HEURE, SANS EXCUSE » ; « RATÉE AU COUCHER DU SOLEIL — OU DÈS LE
#                      JAUNISSEMENT, POUR CERTAINS SAVANTS » (reste pendant {asr jaune}) ; « OUBLI OU SOMMEIL :
#                      PRIE-LA DÈS QUE TU T'EN SOUVIENS (MOUSLIM 684) » ; rien ne recouvre « SANS EXCUSE » ;
#                      {asr jaune} la zone « HEURE NORMALE » (étiquette AU-DESSUS de la barre, hors du chemin du
#                      curseur) s'éclaire en vert, la zone jaunissement → coucher en orange doux et son ciel en jaune
#                      pâle (1,5 s), la caméra s'approche de la limite (zoom doux de 10 %), le curseur s'arrête AVANT
#                      la limite ; « SON HEURE NORMALE : AVANT QUE LE SOLEIL JAUNISSE » (Mouslim 612 selon
#                      an-Nawawi : l'heure sans réprobation ; jamais « rater = laisser jaunir ») ; « DÉJÀ JAUNE ? PRIE
#                      QUAND MÊME, TOUT DE SUITE ! (BOUKHARI 579) » (jamais « RATÉ »)
#   {asr court}        retour au parc d'après-midi, plan large : Petit laisse le ballon (« APRÈS ! ») et part EN
#                      MARCHANT (Mouslim 602a) vers la mosquée du quartier ; Grand, à gauche, sourit, pouce levé ;
#                      même soleil blanc et haut, « LE SOLEIL N'A PAS ENCORE JAUNI » (coche verte) ; « PRIE L'ASR
#                      AVANT QUE LE SOLEIL JAUNISSE » (textes sous la zone du carton « ABONNE-TOI » de la fin)
# Branché par explique_0811.py (import tardif dans explique.Schema._ordre et scenario._fin_anim).
import math

import numpy as np
from PIL import Image, ImageDraw

from px import Px, TAHOMA
from pxv import smooth
from explique import _fade, BLANC, JAUNE
from explique_0411 import OL, _sprite, _buste, _grand
from explique_0411b import _Base, _translucide, OR_, VERT
from explique_0611_dette import _texte_px, _halo, _colle, _etincelle, _lignes

W_, H_ = 1020, 960                                # taille de chaque image (le moteur la pose en grand schéma)
K = 6
SOLEIL = (255, 255, 250)                          # le soleil d'après-midi : BLANC
ROUGE_DOUX = (236, 92, 84)
GRIS_L = (150, 150, 160)                          # une étiquette « éteinte »
ORANGE_DOUX = (246, 170, 92)
JAUNE_PALE = (250, 236, 150)
NOIR_T = (34, 30, 44)
CX_T = 470                                        # centre des textes (loin des 150 px de droite de l'écran)
PHI = (1 + 5 ** 0.5) / 2
_ICO = []
for _a in (-1, 1):
    for _b in (-PHI, PHI):
        for _v in ((0, _a, _b), (_a, _b, 0), (_b, 0, _a)):
            _n = math.sqrt(sum(x * x for x in _v))
            _ICO.append(tuple(x / _n for x in _v))


# ---------------------------------------------------------------- petits outils
def _italique(im, k=0.22):
    """Penche une image (italique) : le haut glisse vers la droite."""
    h = im.height
    out = im.transform((im.width + int(k * h) + 2, h), Image.AFFINE, (1, k, -k * h, 0, 1, 0), resample=Image.NEAREST)
    return out


def _ballon(D, ph):
    """Le ballon blanc et noir (dessin pixel D x D, ×6) ; ph = angle de roulis (il roule vers toi)."""
    c = Px(D + 2, D + 2, alpha=True)
    cx = cy = (D + 2) / 2
    R = D / 2
    disc = c.mask_ell(cx, cy, R, R)
    c.shape(disc, (246, 246, 248), shade=(186, 192, 212), light=(255, 255, 255), sdir="left",
            band=max(1, D // 7), olcol=OL)
    if D >= 6:
        cs, sn = math.cos(ph), math.sin(ph)
        for (x, y, z) in _ICO:
            y2, z2 = y * cs + z * sn, -y * sn + z * cs
            if z2 > 0.12:
                pr = R * 0.30 * (0.55 + 0.45 * z2)
                c.fill(c.mask_ell(cx + R * 0.9 * x, cy + R * 0.9 * y2, pr, pr * (0.5 + 0.5 * z2)) & disc, (38, 38, 48))
        if D >= 12:
            c.fill(c.mask_ell(cx + R * 0.38, cy - R * 0.45, R * 0.18, R * 0.12) & disc, (255, 255, 255))
    else:
        c.px(int(cx), int(cy), (38, 38, 48))
    c.outline(disc, OL)
    return c.img(K, rgba=True)


_BALLONS = {}


def _ballon_c(D, ph):
    cle = (D, int(round(ph / (2 * math.pi) * 24)) % 24)
    if cle not in _BALLONS:
        _BALLONS[cle] = _ballon(D, cle[1] / 24 * 2 * math.pi)
    return _BALLONS[cle]


def _soleil_px(c, x, y, r, col=SOLEIL):
    """Disque de soleil pixel avec deux paliers de lueur nets (dessin Px)."""
    c.tint(c.mask_ell(x, y, r + 7, r + 7), col, 0.18)
    c.tint(c.mask_ell(x, y, r + 3.5, r + 3.5), col, 0.35)
    c.fill(c.mask_ell(x, y, r, r), col)


def _grillage(c, x0, x1, y0, y1, pas=4, col=(46, 120, 74), poteaux=26):
    """Grillage vert (mailles en losange) et ses poteaux."""
    zone = c.mask_rect(x0, y0, x1, y1)
    yy, xx = np.mgrid[0:zone.shape[0], 0:zone.shape[1]]
    maille = (((xx + yy) % pas) == 0) | (((xx - yy) % pas) == 0)
    c.tint(zone & maille, col, 0.75)
    c.fill(c.mask_rect(x0, y0, x1, y0 + 1), (40, 104, 64))
    for x in range(x0 + 2, x1, poteaux):
        p = c.mask_rect(x, y0 - 1, x + 2, y1)
        c.shape(p, (70, 150, 96), shade=(40, 100, 62), band=1, olcol=OL)


def _mosquee(c, x0, base, s=1.0, mur=(238, 230, 212), dome=(70, 156, 112)):
    """Petite mosquée de quartier (dôme vert, minaret, croissant) ; x0 = bord gauche, base = sol."""
    w = int(26 * s)
    corps = c.mask_rect(x0, base - int(14 * s), x0 + w, base)
    c.shape(corps, mur, shade=(204, 194, 176), light=(250, 246, 236), band=1, olcol=OL)
    dm = c.mask_ell(x0 + w / 2, base - 14 * s, 8 * s, 8 * s) & c.mask_rect(0, 0, x0 + w, base - int(14 * s))
    c.shape(dm, dome, shade=(46, 116, 82), light=(110, 196, 150), band=1, olcol=OL)
    c.fill(c.mask_rect(int(x0 + w / 2), int(base - 24 * s), int(x0 + w / 2) + 1, int(base - 21 * s)), (240, 200, 80))
    mx = x0 + w + 1
    mn = c.mask_rect(mx, base - int(30 * s), mx + int(4 * s), base)
    c.shape(mn, mur, shade=(204, 194, 176), band=1, olcol=OL)
    tete = c.mask_poly([(mx - 1, base - 30 * s), (mx + 2 * s, base - 36 * s), (mx + 4 * s + 1, base - 30 * s)])
    c.shape(tete, dome, shade=(46, 116, 82), band=1, olcol=OL)
    for k_ in range(3):                                                       # fenêtres en arc
        fx = x0 + int(4 * s) + k_ * int(8 * s)
        f = c.mask_arch(fx, fx + int(3 * s), base - int(10 * s), base - int(4 * s))
        c.fill(f, (92, 120, 150))
    porte = c.mask_arch(int(x0 + w / 2 - 2 * s), int(x0 + w / 2 + 2 * s), base - int(8 * s), base)
    c.fill(porte, (120, 82, 54))


# ---------------------------------------------------------------- l'élément
class Asr(_Base):
    """{soleilbas PETIT} (accroche : le ballon roule vers toi, la notification ASR) · {asr} la carte « COMME SI… »
    ({asr famille|biens|vide}) · {asr rater} la frise ({asr jaune}) · {asr court} Petit part EN MARCHANT prier."""
    PW_, PH_ = 170, 160
    ETAPES_CARTE = ("famille", "biens", "vide")
    # accroche (pixels du dessin)
    HORIZON = 62
    SOL_PETIT = (22, 78)                     # pieds de Petit au fond (x, y)
    # la carte (pixels d'écran)
    Y_ATT, Y_CELUI, Y_COMME = 26, 96, 205
    OBJ = dict(cadre=(170, 650), maison=(470, 650), bourse=(745, 650))     # centre bas de chaque objet
    T_OBJ = dict(cadre=1.0, maison=2.4, bourse=3.8)  # étalés pendant le ﷺ (relecture du 08/11 : pas de carte figée)
    Y_LAB = 712
    Y_BANDEAU = 896
    # la frise (pixels d'écran)
    BX0, BX1, BY = 60, 876, 540              # la barre horaire
    F_LIM = 0.68                             # « LE SOLEIL JAUNIT » (fraction de la barre)
    X_NORMALE = 340                          # étiquette « HEURE NORMALE », au-dessus de la zone verte

    def __init__(s, cmd, mode="carte", who="PETIT"):
        super().__init__(cmd)
        s.mode = mode
        s.who = who if who in ("PETIT", "GRAND") else "PETIT"
        s.negatif = mode == "soleilbas"

    # ============================================================ sons (bruitages discrets)
    def sons_el(s):
        if s.mode == "soleilbas":
            return [(-0.2, "dv_ballon", 0.03, None), (0.15, "sa_ting", 0.025, None)]
        if s.mode == "carte":
            out = [(s.T_OBJ["cadre"], "tr_whoosh_doux", 0.02, None)]
            if "famille" in s.t:
                out.append((s.t["famille"], "tr_whoosh_doux", 0.025, None))
            if "biens" in s.t:
                out.append((s.t["biens"], "sa_scintillement", 0.03, None))
            return out
        if s.mode == "frise":
            out = [(0.0, "tr_whoosh_doux", 0.025, None)]
            if "jaune" in s.t:
                out.append((s.t["jaune"] + 1.9, "sa_ting", 0.03, None))
            return out
        if s.mode == "court":
            return [(0.5, "dv_pas_sable", 0.02, None), (0.9, "sa_ting", 0.025, None)]
        return []

    def image(s, u):
        return {"soleilbas": s._image_accroche, "frise": s._image_frise,
                "court": s._image_court}.get(s.mode, s._image_carte)(u)

    def _lab(s, txt, col=BLANC, size=56):
        cle = ("lab", txt, col, size)
        if cle not in s._cache:
            if " // " in txt:                                                      # lignes serrées (au contour près)
                ims = [super(Asr, s)._lab(l_, col, size) for l_ in txt.split(" // ")]
                ims = [i.crop(i.getbbox()) for i in ims]
                gap = max(4, size // 7)
                out = Image.new("RGBA", (max(i.width for i in ims), sum(i.height for i in ims) + gap * (len(ims) - 1)),
                                (0, 0, 0, 0))
                y = 0
                for i in ims:
                    out.alpha_composite(i, (int(out.width / 2 - i.width / 2), y))
                    y += i.height + gap
                s._cache[cle] = out
            else:
                s._cache[cle] = super()._lab(txt, col, size)
        return s._cache[cle]

    # ============================================================ {soleilbas} : l'accroche
    def _decor_stade(s):
        if "stade" in s._cache:
            return s._cache["stade"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        hz = s.HORIZON
        ciel = c.mask_rect(0, 0, W, hz + 4) & tout_
        c.vgrad(ciel, 0, hz, (92, 156, 228), (176, 212, 242), steps=6)
        for (x, y, w) in ((18, 14, 22), (60, 30, 16)):                             # deux petits nuages
            n = c.mask_ell(x, y, w / 2, 3) | c.mask_ell(x + w * 0.2, y - 2, w / 4, 3)
            c.shape(n, (250, 252, 255), shade=(214, 226, 242), sdir="bottom", band=1, ol=False)
        _soleil_px(c, 132, 17, 7)
        for j, x in enumerate(range(-4, W + 6, 9)):                               # les arbres du parc derrière
            h_ = 9 + (j * 7) % 6
            a_ = c.mask_ell(x, hz - h_ / 2 + 2, 7, h_ / 2 + 2) & tout_
            c.shape(a_, (64, 138, 76), shade=(44, 104, 58), light=(96, 170, 96), sdir="left", band=2, olcol=(30, 70, 40))
        sol = c.mask_rect(0, hz, W, H) & tout_
        c.vgrad(sol, hz, H, (60, 146, 82), (92, 180, 96), steps=7)
        y, hb, j = hz + 2, 2.0, 0                                                  # bandes de tonte en perspective
        while y < H:
            if j % 2:
                c.tint(c.mask_rect(0, int(y), W, int(y + hb)) & sol, (255, 255, 230), 0.07)
            y += hb
            hb *= 1.35
            j += 1
        L = (238, 242, 236)                                                        # lignes blanches du terrain
        for (x0, y0, x1, y1) in ((30, hz + 6, -10, H), (140, hz + 6, 180, H)):
            c.line(x0, y0, x1, y1, L)
            c.line(x0 + (1 if x1 < x0 else -1), y0 + 3, x1 + (1 if x1 < x0 else -1), y1, L)
        c.fill(c.mask_rect(30, hz + 6, 141, hz + 7), L)
        cerc = c.mask_ell(85, 98, 34, 9) & ~c.mask_ell(85, 98, 32.5, 7.8)
        c.fill(cerc, L)
        c.fill(c.mask_rect(0, 97, W, 99) & ~c.mask_rect(0, 0, 1, 1) & sol & (c.mask_rect(18, 0, 154, H)), L)
        but = c.mask_rect(70, 50, 100, hz + 6)                                     # la petite cage au fond
        filet = but & ~c.mask_rect(72, 52, 98, hz + 6)
        yy, xx = np.mgrid[0:H, 0:W]
        c.tint(c.mask_rect(72, 52, 98, hz + 6) & ((((xx + yy) % 3) == 0) | (((xx - yy) % 3) == 0)), (235, 235, 240), 0.55)
        c.shape(filet, (246, 246, 248), shade=(196, 196, 206), band=1, olcol=OL)
        _grillage(c, 0, W, 34, hz + 6)                                             # le grillage du city stade
        for x in range(2, W, 26):                                                  # ombres longues des poteaux (vers
            om = c.mask_poly([(x, hz + 6), (x + 2, hz + 6), (x - 18, hz + 30), (x - 21, hz + 30)])    # le bas-gauche)
            c.tint(om & sol, (30, 60, 130), 0.3)
        c.tint(c.mask_poly([(0, hz + 6), (W, hz + 6), (W - 14, hz + 14), (0, hz + 14)]) & sol, (30, 60, 130), 0.16)
        # ton téléphone, posé au bord du terrain (premier plan, à gauche)
        tel = c.mask_poly([(6, 128), (40, 124), (46, 146), (9, 151)])
        c.shape(tel, (40, 40, 52), shade=(24, 24, 32), light=(96, 96, 116), band=1, olcol=OL)
        ecran = c.mask_poly([(9, 129), (38, 126), (43, 144), (12, 148)])
        c.fill(ecran, (40, 64, 104))
        c.tint(c.mask_poly([(12, 129), (20, 128), (14, 147), (12, 147)]) & ecran, (255, 255, 255), 0.18)
        c.tint(c.mask_poly([(4, 151), (46, 146), (52, 149), (8, 155)]) & sol, (20, 40, 90), 0.3)
        # tes baskets (vue à ta place), en bas
        acc = (200, 50, 50) if s.who == "PETIT" else (56, 136, 84)
        for x in (66, 112):
            semelle = c.mask_ell(x, 160, 17, 10)
            c.shape(semelle, (214, 214, 222), shade=(170, 170, 184), band=1, olcol=OL)
            dessus = c.mask_ell(x, 161, 15, 8.5)
            c.shape(dessus, (244, 244, 248), shade=(200, 202, 214), light=(255, 255, 255), sdir="left", band=2,
                    olcol=OL)
            c.fill(c.mask_poly([(x - 10, 158), (x + 6, 154), (x + 9, 156), (x - 8, 160)]) & dessus, acc)
            for k_ in range(3):
                c.fill(c.mask_rect(x - 3, 153 + 2 * k_, x + 4, 154 + 2 * k_) & dessus, (176, 178, 192))
        s._cache["stade"] = c.img(K, rgba=True)
        return s._cache["stade"]

    def _notif(s):
        if "notif" in s._cache:
            return s._cache["notif"]
        c = Px(46, 18, alpha=True)
        corps = c.mask_rrect(0, 0, 46, 18, 5)
        c.shape(corps, (250, 250, 252), shade=(214, 214, 224), sdir="bottom", band=1, olcol=OL)
        ic = c.mask_rrect(3, 3, 16, 15, 3)
        c.fill(ic, (40, 150, 96))
        c.fill(c.mask_rect(5, 10, 12, 14), (255, 255, 255))                        # la mosquée de l'icône
        c.fill(c.mask_ell(8.5, 10, 3.2, 3.2) & c.mask_rect(0, 0, 46, 10), (255, 255, 255))
        c.fill(c.mask_rect(13, 5, 14, 14), (255, 255, 255))
        c.px(8, 5, (255, 255, 255))
        im = c.img(K, rgba=True)
        tx = _texte_px("ASR", NOIR_T, 13, k=6, pad=0, gras=True)
        im.alpha_composite(tx, (19 * K, int((18 * K - tx.height) / 2) - 2))
        s._cache["notif"] = im
        return im

    def _bulle_blanche(s, txt):
        cle = ("bb", txt)
        if cle in s._cache:
            return s._cache[cle]
        tx = _texte_px(txt, NOIR_T, 13, k=4, pad=0, gras=True)
        w, h = tx.width + 56, tx.height + 40
        b = Image.new("RGBA", (w, h + 40), (0, 0, 0, 0))
        d = ImageDraw.Draw(b)
        q = 90
        d.polygon([(q - 26, h - 8), (q + 20, h - 8), (q - 30, h + 34)], fill=(*OL, 255))
        d.rounded_rectangle([0, 0, w - 1, h], 24, fill=(255, 255, 255, 255), outline=(*OL, 255), width=6)
        d.polygon([(q - 19, h - 7), (q + 12, h - 7), (q - 24, h + 24)], fill=(255, 255, 255, 255))
        b.alpha_composite(tx, (28, 18))
        s._cache[cle] = b
        return b

    def _image_accroche(s, u):
        im = s._decor_stade().copy()
        # Petit au fond à gauche, bras en l'air, sautille (doucement)
        cle = ("petit_v",)
        if cle not in s._cache:
            s._cache[cle] = _grand(_sprite("PETIT", "victoire", "content"), 3)
        sp = s._cache[cle]
        saut = abs(math.sin(math.pi * max(u, 0) / 0.62)) * 14
        px_, py_ = s.SOL_PETIT[0] * K, s.SOL_PETIT[1] * K
        _colle(im, _halo(110, 26, (20, 40, 90), 6), px_ - 14, py_ - 2, 0.45 - 0.2 * saut / 14)
        im.alpha_composite(sp, (int(px_ - sp.width / 2), int(py_ - 94 * 3 - saut)))
        bu = s._bulle_blanche("ENCORE UN MATCH !")
        im.alpha_composite(bu, (60, int(py_ - 66 * 3 - bu.height - 6 - 0.4 * saut)))
        # la notification « ASR » : fondu, puis elle glisse vers toi
        e = smooth((u + 1.0) / 0.5)                      # déjà là à l'image 0 (l'élément démarre un peu après 0 s)
        if e > 0.01:
            dr = smooth((u + 0.3) / 2.2)                 # elle glisse lentement vers toi
            k = 1.05 + 0.25 * e + 0.08 * dr
            no = s._notif()
            no_ = no.resize((int(no.width * k), int(no.height * k)), Image.LANCZOS)
            cx, cy = 210 + 8 * dr, 590 + 70 * e + 20 * dr
            _colle(im, _halo(240, 90, (255, 255, 255), 18), 160, 820, 0.35 * e)    # l'écran s'allume
            _colle(im, no_, cx, cy, e)
        # le ballon roule du fond vers toi et s'arrête devant tes pieds
        v = min(1.0, max(0.0, (u + 1.3) / 2.9))         # déjà bien gros à l'image 0, il arrive vers 1,6 s
        p = 1 - (1 - v) ** 2.2
        y = 70 + 62 * p
        r = (y - s.HORIZON) * 0.27
        x = 118 - 26 * p
        D = max(3, int(round(2 * r)))
        ph = 7 * math.pi * p
        sx, sy = x * K, y * K
        rr = D * K / 2
        _colle(im, _halo(rr * 2.4, rr * 0.6, (20, 40, 100), max(2, rr * 0.12)), sx - rr * 0.7, sy + rr * 0.85, 0.5)
        b = _ballon_c(D, ph)
        im.alpha_composite(b, (int(sx - b.width / 2), int(sy - b.height / 2)))
        return im

    # ============================================================ {asr} : la carte « COMME SI… »
    def _table(s):
        """Le mur et la table en bois, plus grands que l'image (marge pour le recul de la caméra)."""
        if "table" in s._cache:
            return s._cache["table"]
        W, H = s.PW_ + 20, s.PH_ + 20
        c = Px(W, H, alpha=True)
        mur = c.mask_rect(0, 0, W, 68)
        c.vgrad(mur, 0, 68, (70, 48, 44), (118, 82, 62), steps=6)
        c.dither(mur, (84, 58, 50), 0.12)
        tab = c.mask_rect(0, 66, W, H)
        c.vgrad(tab, 66, H, (150, 98, 60), (176, 118, 72), steps=6)
        c.dither(tab, (138, 88, 52), 0.22)
        for y in (80, 98, 122, 152):                                               # planches en perspective
            c.fill(c.mask_rect(0, y, W, y + 1), (110, 70, 42))
        rng = np.random.default_rng(5)
        for _ in range(40):                                                        # veinage
            x, y = int(rng.integers(0, W - 20)), int(rng.integers(70, H - 2))
            c.fill(c.mask_rect(x, y, x + int(rng.integers(6, 20)), y + 1), (132, 84, 50))
        c.fill(c.mask_rect(0, 66, W, 68), (196, 140, 88))
        c.fill(c.mask_rect(0, 68, W, 69), (96, 60, 38))
        for (a, b) in ((0, 30), (44, 68)):                                         # la lumière d'après-midi, en biais
            rai = c.mask_poly([(a, 0), (b, 0), (b + 120, H), (a + 120, H)])
            c.tint(rai, (255, 226, 170), 0.13)
        s._cache["table"] = c.img(K, rgba=True)
        return s._cache["table"]

    def _cadre(s, vide=False):
        """Le cadre photo (bois) ; les 4 silhouettes sont posées à part. Renvoie l'image ×6."""
        cle = ("cadre", vide)
        if cle in s._cache:
            return s._cache[cle]
        c = Px(38, 42, alpha=True)
        bois = c.mask_rrect(0, 0, 38, 42, 2)
        c.shape(bois, (180, 122, 70), shade=(132, 86, 48), light=(214, 160, 100), band=2, olcol=OL)
        mat = c.mask_rect(4, 4, 34, 38)
        c.fill(mat, (240, 230, 206))
        photo = c.mask_rect(6, 6, 32, 36)
        c.vgrad(photo, 6, 36, (170, 204, 236), (214, 230, 244), steps=4)
        c.fill(c.mask_rect(6, 30, 32, 36), (140, 196, 124))
        c.outline(photo, (150, 130, 100))
        im = c.img(K, rgba=True)
        s._cache[cle] = im
        return im

    def _silhouettes(s):
        """Les 4 silhouettes neutres (sans visage), chacune sur son calque de la taille du cadre."""
        if "sil" in s._cache:
            return s._cache["sil"]
        out = []
        for (x, tete, r, larg) in ((11, 11, 3.2, 5.0), (17, 16, 2.4, 3.6), (23, 17, 2.2, 3.2), (28, 11, 3.2, 5.0)):
            c = Px(38, 42, alpha=True)
            corps = c.mask_ell(x, 36, larg, 36 - tete - r - 1.5) & c.mask_rect(0, 0, 38, 36)
            t_ = c.mask_ell(x, tete + r, r, r)
            c.shape(corps | t_, (92, 102, 132), shade=(70, 78, 106), light=(120, 130, 160), band=1, olcol=(60, 66, 90))
            out.append(c.img(K, rgba=True))
        s._cache["sil"] = out
        return out

    def _reflet(s):
        if "reflet" not in s._cache:
            c = Px(38, 42, alpha=True)
            c.fill(c.mask_poly([(22, 6), (28, 6), (14, 36), (8, 36)]), (255, 255, 255))
            c.fill(c.mask_poly([(30, 6), (32, 6), (18, 36), (16, 36)]), (255, 255, 255))
            s._cache["reflet"] = c.img(K, rgba=True)
        return s._cache["reflet"]

    def _maison(s):
        if "maison" in s._cache:
            return s._cache["maison"]
        c = Px(40, 38, alpha=True)
        ch = c.mask_rect(27, 3, 31, 12)
        c.shape(ch, (150, 84, 64), shade=(110, 60, 46), band=1, olcol=OL)
        mur = c.mask_rect(5, 17, 35, 37)
        c.shape(mur, (240, 226, 196), shade=(206, 188, 156), light=(252, 244, 222), band=2, olcol=OL)
        toit = c.mask_poly([(1, 18), (20, 3), (39, 18)])
        c.shape(toit, (190, 74, 58), shade=(146, 52, 42), light=(222, 110, 86), sdir="bottom", band=2, olcol=OL)
        for (x0, y0) in ((9, 21), (25, 21)):                                       # fenêtres éclairées
            f = c.mask_rect(x0, y0, x0 + 6, y0 + 6)
            c.shape(f, (255, 222, 120), shade=(236, 176, 70), band=1, olcol=OL)
            c.fill(c.mask_rect(x0 + 3, y0, x0 + 4, y0 + 6), (140, 96, 60))
            c.fill(c.mask_rect(x0, y0 + 3, x0 + 6, y0 + 4), (140, 96, 60))
        porte = c.mask_rect(17, 26, 23, 37)
        c.shape(porte, (70, 104, 160), shade=(50, 76, 124), band=1, olcol=OL)
        c.px(21, 31, (250, 210, 90))
        im = c.img(K, rgba=True)
        s._cache["maison"] = im
        return im

    def _bourse(s):
        if "bourse" in s._cache:
            return s._cache["bourse"]
        c = Px(40, 30, alpha=True)
        for j, (x, y, a) in enumerate(((8, 2, 0), (15, 0, 0), (21, 3, 0))):         # les billets qui dépassent
            b = c.mask_rect(x, y, x + 14, y + 16)
            c.shape(b, (132, 196, 132), shade=(96, 160, 100), light=(176, 226, 170), band=1, olcol=OL)
            c.fill(c.mask_ell(x + 7, y + 6, 2.5, 2.5) & b, (96, 160, 100))
            c.fill(c.mask_rect(x + 2, y + 2, x + 4, y + 3), (90, 150, 92))
        corps = c.mask_rrect(1, 12, 39, 30, 3)
        c.shape(corps, (128, 76, 46), shade=(94, 54, 32), light=(164, 104, 66), band=2, olcol=OL)
        rabat = c.mask_rrect(1, 12, 39, 18, 2)
        c.shape(rabat, (146, 90, 56), shade=(110, 66, 40), band=1, olcol=OL)
        for x in range(4, 37, 3):                                                  # la couture
            c.px(x, 27, (196, 150, 104))
        c.fill(c.mask_rrect(30, 18, 38, 23, 1), (210, 170, 90))
        im = c.img(K, rgba=True)
        s._cache["bourse"] = im
        return im

    def _console(s):
        if "console" in s._cache:
            return s._cache["console"]
        c = Px(30, 16, alpha=True)
        corps = c.mask_rrect(0, 2, 30, 16, 6)
        c.shape(corps, (60, 62, 80), shade=(38, 40, 54), light=(100, 104, 128), band=2, olcol=OL)
        c.fill(c.mask_rect(6, 6, 7, 11), (200, 200, 214))                          # la croix
        c.fill(c.mask_rect(4, 8, 9, 9), (200, 200, 214))
        for (x, y, col) in ((21, 6, (230, 80, 80)), (24, 9, (90, 200, 120)), (18, 9, (90, 140, 230))):
            c.fill(c.mask_ell(x, y, 1.4, 1.4), col)
        c.fill(c.mask_rrect(11, 4, 19, 8, 1), (40, 40, 52))
        im = c.img(K, rgba=True)
        s._cache["console"] = im
        return im

    def _accolade(s, x0, x1, y, col):
        """Accolade horizontale (pointe vers le bas) de x0 à x1, en pixels d'écran."""
        cle = ("acc", x0, x1, y, col)
        if cle not in s._cache:
            lay = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            m = (x0 + x1) / 2
            pts = [(x0, y - 18), (x0 + 12, y - 2), (m - 18, y - 2), (m, y + 16), (m + 18, y - 2), (x1 - 12, y - 2),
                   (x1, y - 18)]
            d.line(pts, fill=(*OL, 255), width=16, joint="curve")
            d.line(pts, fill=(*col, 255), width=8, joint="curve")
            s._cache[cle] = lay
        return s._cache[cle]

    def _bandeau(s):
        if "bandeau" not in s._cache:
            s._cache["bandeau"] = _italique(s._lab("COMME SI…", (255, 240, 170), 58))
        return s._cache["bandeau"]

    def _image_carte(s, u):
        tf, tb, tv = s.t.get("famille"), s.t.get("biens"), s.t.get("vide")
        ev = s._e("vide", u, 1.0)
        # --- le calque de la table (il recule pendant {asr vide})
        tab = s._table()
        lay = tab.copy()
        M = 60                                                                     # marge du calque (pixels d'écran)
        sil = s._silhouettes()
        # le cadre : il glisse au centre pendant {asr vide}
        cx_c = s.OBJ["cadre"][0] + (CX_T - s.OBJ["cadre"][0]) * ev
        for nom in ("cadre", "maison", "bourse"):
            t0 = s.T_OBJ[nom]
            e = smooth((u - t0) / 0.4)
            if e <= 0.01:
                continue
            ox, oy = s.OBJ[nom]
            if nom == "cadre":
                ox = cx_c
            dy = 50 * (1 - e)
            a = e
            if nom != "cadre" and tb is not None and u >= tb:                      # {asr biens} : vapeur dorée
                f = smooth((u - tb) / 0.8)
                a *= 1 - f
                dy -= 20 * f
            sp = {"cadre": s._cadre, "maison": s._maison, "bourse": s._bourse}[nom]()
            X, Y = M + ox - sp.width / 2, M + oy - sp.height + dy
            if a > 0.01:
                _colle(lay, _halo(sp.width * 0.9, 40, (40, 22, 14), 10), M + ox + 10, M + oy + 4, 0.55 * a)
                lay.alpha_composite(_fade(sp, a), (int(X), int(Y)))
            if nom == "cadre" and a > 0.01:
                for i, si in enumerate(sil):
                    ai = 1.0 if tf is None else 1 - smooth((u - tf - 0.22 * i) / 0.5)
                    if ai > 0.01:
                        lay.alpha_composite(_fade(si, a * ai), (int(X), int(Y)))
                vide_ = 0.0 if tf is None else smooth((u - tf - 0.6) / 0.6)
                lay.alpha_composite(_fade(s._reflet(), a * (0.25 + 0.3 * vide_)), (int(X), int(Y)))
        if tb is not None and 0 <= u - tb < 1.3:                                   # étincelles dorées qui montent
            v = u - tb
            et = []
            rng = np.random.default_rng(9)
            for nom in ("maison", "bourse"):
                ox, oy = s.OBJ[nom]
                for j in range(6):
                    vv = v - 0.07 * j
                    if 0 <= vv < 1.0:
                        ex = M + ox + float(rng.uniform(-100, 100)) + 8 * math.sin(vv * 6 + j)
                        ey = M + oy - float(rng.uniform(40, 200)) - 120 * smooth(vv / 1.0)
                        et.append((ex, ey, 4 if j % 2 else 5, smooth(vv / 0.15) * (1 - smooth((vv - 0.45) / 0.5))))
            _translucide(lay, lambda d: [_etincelle(d, x, y, r, a) for (x, y, r, a) in et])
        # la console (un « bien » de Petit) : elle apparaît avec le recul, puis s'estompe
        if tv is not None:
            co = s._console()
            a_c = smooth((u - tv - 0.15) / 0.35) * (1 - smooth((u - tv - 1.0) / 0.8))
            if a_c > 0.01:
                dyc = -18 * smooth((u - tv - 1.0) / 0.8)
                _colle(lay, _halo(co.width * 0.9, 30, (40, 22, 14), 8), M + 770, M + 668, 0.5 * a_c)
                lay.alpha_composite(_fade(co, a_c), (int(M + 770 - co.width / 2), int(M + 668 - co.height + dyc)))
        # étiquettes « SA FAMILLE » et accolade « SES BIENS » (elles partent pendant {asr vide})
        a_lab = 1 - smooth((u - tv) / 0.4) if tv is not None else 1.0
        if a_lab > 0.01:
            gf = 0.0 if tf is None else smooth((u - tf - 0.6) / 0.4)
            gb = 0.0 if tb is None else smooth((u - tb - 0.4) / 0.4)
            e1 = smooth((u - s.T_OBJ["cadre"] - 0.4) / 0.35) * a_lab
            e2 = smooth((u - s.T_OBJ["bourse"] - 0.4) / 0.35) * a_lab
            for col, a in ((BLANC, 1 - gf), (GRIS_L, gf)):
                s._pose(lay, s._lab("SA FAMILLE", col, 42), M + s.OBJ["cadre"][0], M + s.Y_LAB + 8, e1 * a)
            for col, a in ((BLANC, 1 - gb), (GRIS_L, gb)):
                if e2 * a > 0.01:
                    lay.alpha_composite(_fade(s._accolade(330, 870, 712, JAUNE if col == BLANC else GRIS_L), e2 * a),
                                        (M, M))
                    s._pose(lay, s._lab("SES BIENS", col, 42), M + 600, M + s.Y_LAB + 62, e2 * a)
        # --- la caméra avance lentement (+5 % sur 6 s, jusqu'à {asr famille}), puis recule ({asr vide})
        zp = 0.05 * smooth(min(u, tf if tf is not None else u) / 6.0)
        z = (1 + zp) * (1 - 0.1 * ev)
        if abs(z - 1) > 0.001:
            lay = lay.resize((int(lay.width * z), int(lay.height * z)), Image.LANCZOS)
        ox, oy = (lay.width - W_) / 2, (lay.height - H_) / 2 + 20 * ev
        im = lay.crop((int(ox), int(oy), int(ox) + W_, int(oy) + H_))
        rond = Image.new("L", (W_, H_), 0)
        ImageDraw.Draw(rond).rounded_rectangle([0, 0, W_ - 1, H_ - 1], 36, fill=255)
        im.putalpha(Image.fromarray(np.minimum(np.array(im)[..., 3], np.array(rond)), "L"))
        # --- les textes (fixes) : le hadith, mot pour mot
        a0 = smooth((u + 0.05) / 0.25)
        s._pose(im, s._cache.setdefault("att", _texte_px("LE PROPHÈTE (PAIX ET SALUT SUR LUI) :", (226, 214, 196), 12,
                                                         k=3, pad=0)), CX_T, s.Y_ATT + 10, a0)
        s._pose(im, s._lab("« CELUI QUI RATE L'ASR…", BLANC, 58), CX_T, s.Y_CELUI, a0, maxw=820)
        s._pose(im, s._lab("… C'EST COMME SI ON LUI AVAIT PRIS // SA FAMILLE ET SES BIENS »", JAUNE, 50), CX_T,
                s.Y_COMME, a0, maxw=860)
        if tv is not None:                                                         # « NI FAMILLE NI BIENS… »
            e3 = s._e("vide", u, 0.45, dec=0.35)
            s._pose(im, s._lab("NI FAMILLE NI BIENS…", ROUGE_DOUX, 60), CX_T, 742 + 16 * (1 - e3), e3, maxw=820)
            e4 = s._e("vide", u, 0.4, dec=0.75)
            s._pose(im, s._lab("C'EST AUSSI GRAVE QUE ÇA", BLANC, 42), CX_T, 812 + 12 * (1 - e4), e4, maxw=760)
            e5 = s._e("vide", u, 0.4, dec=0.7)                                  # après le glissé du cadre
            if e5 > 0.01:                                                          # vignette : Petit choqué
                if "vign" not in s._cache:
                    bu = _grand(_buste("PETIT", "choc", sweat=True)[0], 6)
                    v_ = Image.new("RGBA", (bu.width + 24, bu.height + 24), (0, 0, 0, 0))
                    ImageDraw.Draw(v_).rounded_rectangle([0, 0, v_.width - 1, v_.height - 1], 20, fill=(70, 96, 150, 255),
                                                         outline=(255, 255, 255, 255), width=6)
                    v_.alpha_composite(bu, (12, 12))
                    s._cache["vign"] = v_
                vg = s._cache["vign"]
                im.alpha_composite(_fade(vg, e5), (40, int(470 - vg.height / 2 + 20 * (1 - e5))))
        s._pose(im, s._bandeau(), CX_T, s.Y_BANDEAU, smooth((u - 0.3) / 0.4))
        return im

    # ============================================================ {asr rater} {asr jaune} : la frise horaire
    def _ciel(s):
        if "ciel" in s._cache:
            return s._cache["ciel"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        c.vgrad(tout_, 0, H, (96, 160, 228), (186, 220, 244), steps=7)
        for (x, y, w) in ((26, 40, 26), (120, 30, 20), (70, 128, 30)):
            n = c.mask_ell(x, y, w / 2, 3.2) | c.mask_ell(x + w * 0.18, y - 2.4, w / 4, 3)
            c.shape(n, (250, 252, 255), shade=(214, 226, 242), sdir="bottom", band=1, ol=False)
        sol = c.mask_rect(0, 146, W, H) & tout_
        c.fill(sol, (98, 172, 92))
        c.fill(c.mask_rect(0, 146, W, 147) & tout_, (76, 140, 76))
        for j, x in enumerate(range(-4, W + 6, 8)):
            h_ = 6 + (j * 5) % 5
            a_ = c.mask_ell(x, 146 - h_ / 2 + 1, 5, h_ / 2 + 1) & tout_
            c.shape(a_, (70, 144, 82), shade=(48, 108, 60), band=1, olcol=(34, 74, 44))
        s._cache["ciel"] = c.img(K, rgba=True)
        return s._cache["ciel"]

    def _barre(s, jaune):
        """La barre horaire (pixels du dessin ×6) : neutre, ou verte (heure de l'Asr) + orange doux (jaunissement)."""
        cle = ("barre", jaune)
        if cle in s._cache:
            return s._cache[cle]
        L = int((s.BX1 - s.BX0) / K)
        c = Px(L, 9, alpha=True)
        xl = int(L * s.F_LIM)
        g = c.mask_rrect(0, 0, xl + 3, 9, 3)
        d_ = c.mask_rrect(xl - 3, 0, L, 9, 3) & c.mask_rect(xl, 0, L, 9)
        g = g & c.mask_rect(0, 0, xl, 9)
        if jaune:
            c.shape(g, (124, 210, 132), shade=(84, 168, 96), light=(170, 236, 170), sdir="bottom", band=2, olcol=OL)
            c.shape(d_, ORANGE_DOUX, shade=(214, 132, 66), light=(255, 204, 140), sdir="bottom", band=2, olcol=OL)
        else:
            c.shape(g, (236, 242, 250), shade=(196, 208, 226), light=(255, 255, 255), sdir="bottom", band=2, olcol=OL)
            c.shape(d_, (214, 216, 226), shade=(178, 182, 198), light=(236, 238, 244), sdir="bottom", band=2, olcol=OL)
        im = c.img(K, rgba=True)                  # l'étiquette « HEURE NORMALE » est posée AU-DESSUS de la barre
        s._cache[cle] = im                        # (_image_frise) : le soleil-curseur ne passe plus dessus
        return im

    def _icone_soleil(s, r, col, demi=False):
        cle = ("isol", r, col, demi)
        if cle not in s._cache:
            n = int(2 * r + 12)
            c = Px(n, n, alpha=True)
            m = n / 2
            c.tint(c.mask_ell(m, m, r + 4, r + 4), col, 0.35)
            disc = c.mask_ell(m, m, r, r)
            if demi:
                disc &= c.mask_rect(0, 0, n, int(m) + 1)
                c.al[int(m) + 1:, :] = False
                c.fill(c.mask_rect(1, int(m) + 1, n - 1, int(m) + 2), (60, 60, 80))
            c.shape(disc, col, shade=tuple(int(v * 0.9) for v in col), band=1, olcol=OL)
            s._cache[cle] = c.img(K, rgba=True)
        return s._cache[cle]

    def _image_frise(s, u):
        tj = s.t.get("jaune")
        ej = s._e("jaune", u, 1.5)                                                  # le jaunissement (1,5 s)
        lay = s._ciel().copy()
        xl = s.BX0 + (s.BX1 - s.BX0) * s.F_LIM
        if ej > 0.01:                                                              # le ciel de la zone jaunit
            m = np.zeros((H_, W_), np.float32)
            xs = np.arange(W_, dtype=np.float32)
            m[:] = np.clip((xs - xl + 30) / 60, 0, 1)[None, :]
            ys = np.arange(H_, dtype=np.float32)
            m *= np.clip((876 - ys) / 60, 0, 1)[:, None]
            jaune = Image.new("RGBA", (W_, H_), (*JAUNE_PALE, 0))
            jaune.putalpha(Image.fromarray((m * 140 * ej).astype(np.uint8), "L"))
            lay.alpha_composite(jaune)
        # la frise monte du bas
        em = smooth(u / 0.55)
        fr = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        b0, b1 = s._barre(False), s._barre(True)
        by = s.BY - b0.height / 2
        fr.alpha_composite(b0, (s.BX0, int(by)))
        eb = s._e("jaune", u, 0.6)
        if eb > 0.01:
            fr.alpha_composite(_fade(b1, eb), (s.BX0, int(by)))
            s._pose(fr, s._lab("HEURE NORMALE", VERT, 36), s.X_NORMALE, s.BY - 96, eb, maxw=320)
        d = ImageDraw.Draw(fr)
        for y in range(int(s.BY - 118), int(s.BY + 40), 22):                       # la limite (tirets)
            d.rectangle([xl - 5, y, xl + 5, y + 12], fill=(*OL, 255))
            d.rectangle([xl - 2, y + 2, xl + 2, y + 10], fill=(255, 236, 140, 255))
        for x in (s.BX0, s.BX1):
            d.rectangle([x - 4, s.BY - 40, x + 4, s.BY + 40], fill=(*OL, 255))
            d.rectangle([x - 1, s.BY - 37, x + 1, s.BY + 37], fill=(255, 255, 255, 255))
        # les soleils repères : haut et blanc, puis jauni, puis couché
        _colle(fr, s._icone_soleil(6, SOLEIL), s.BX0 + 46, s.BY - 120)
        _colle(fr, s._icone_soleil(5, (250, 222, 120)), xl + 60, s.BY - 70)
        _colle(fr, s._icone_soleil(5, (244, 150, 80), demi=True), s.BX1 - 30, s.BY - 56)
        s._pose(fr, s._lab("LE SOLEIL JAUNIT", (255, 236, 140), 32), xl - 20, s.BY - 150, 1.0, maxw=420)
        s._pose(fr, s._lab("DÉBUT DE L'ASR", BLANC, 36), 210, s.BY + 70, 1.0, maxw=330)
        s._pose(fr, s._lab("COUCHER", BLANC, 34), 790, s.BY + 70, 1.0, maxw=200)
        # le soleil-curseur (blanc) : il glisse, puis s'arrête AVANT la limite
        f = 0.03 + 0.37 * smooth((u - 0.4) / 2.0)
        if tj is not None:                                                      # lent (3,2 s) : pas de plan figé
            f += 0.23 * smooth((u - tj) / 3.2)
        cx = s.BX0 + (s.BX1 - s.BX0) * f
        _colle(fr, _halo(110, 110, (255, 255, 230), 14), cx, s.BY, 0.55)
        _colle(fr, s._icone_soleil(5, SOLEIL), cx, s.BY)
        lay.alpha_composite(_fade(fr, em), (0, int(260 * (1 - em))))
        # la caméra s'approche de la limite ({asr jaune}, +10 % en 3,5 s, puis +2 % de plus, très lentement)
        ez = s._e("jaune", u, 3.5)
        if ez > 0.01:
            z = 1 + 0.10 * ez + 0.02 * s._e("jaune", u, 3.0, dec=3.5)
            big = lay.resize((int(W_ * z), int(H_ * z)), Image.LANCZOS)
            ox, oy = xl * z - xl, s.BY * z - s.BY
            lay = big.crop((int(ox), int(oy), int(ox) + W_, int(oy) + H_))
            rond = Image.new("L", (W_, H_), 0)
            ImageDraw.Draw(rond).rounded_rectangle([0, 0, W_ - 1, H_ - 1], 36, fill=255)
            lay.putalpha(rond)
        im = lay
        # textes fixes
        a_r = smooth((u - 0.15) / 0.35) * (1 - s._e("jaune", u, 0.4))
        # (relecture du 08/11 : l'écran ne redéfinit jamais « rater » par le jaunissement ; « son heure normale » =
        # Mouslim 612 selon an-Nawawi ; « ratée au coucher » = Nafi', préféré par Ibn Hajar ; chaque note a sa source)
        s._pose(im, s._lab("RATER L'ASR =", BLANC, 50), CX_T, 30, a_r)
        s._pose(im, s._lab("LA LAISSER PASSER SON HEURE, // SANS EXCUSE", JAUNE, 42), CX_T, 156, a_r, maxw=860)
        a_j = s._e("jaune", u, 0.45, dec=0.25)
        s._pose(im, s._lab("SON HEURE NORMALE : // AVANT QUE LE SOLEIL JAUNISSE", VERT, 48), CX_T, 110, a_j,
                maxw=860)
        s._pose(im, s._lab("RATÉE AU COUCHER DU SOLEIL — // OU DÈS LE JAUNISSEMENT, POUR CERTAINS SAVANTS",
                           BLANC, 27), CX_T, 280, smooth((u - 0.6) / 0.4), maxw=860)
        a_d = s._e("jaune", u, 0.45, dec=0.9)
        s._pose(im, s._lab("DÉJÀ JAUNE ? PRIE QUAND MÊME, // TOUT DE SUITE ! (BOUKHARI 579)", ORANGE_DOUX, 42),
                CX_T + 40, 738, a_d, maxw=780)
        s._pose(im, s._lab("OUBLI OU SOMMEIL : PRIE-LA // DÈS QUE TU T'EN SOUVIENS (MOUSLIM 684)", (220, 226, 236), 30),
                CX_T, 892, smooth((u - 1.0) / 0.4), maxw=820)
        return im

    # ============================================================ {asr court} : il part prier, en marchant
    def _parc(s):
        if "parc" in s._cache:
            return s._cache["parc"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        hz = 96
        c.vgrad(c.mask_rect(0, 0, W, hz + 2) & tout_, 0, hz, (94, 160, 228), (178, 214, 242), steps=6)
        _soleil_px(c, 24, 20, 7)                       # haut à gauche : les textes restent sous « ABONNE-TOI »
        _mosquee(c, 112, hz + 2, s=1.0)
        for j, x in enumerate(range(-4, 108, 9)):                                  # arbres
            h_ = 12 + (j * 7) % 8
            a_ = c.mask_ell(x, hz - h_ / 2 + 2, 7, h_ / 2 + 2) & tout_
            c.shape(a_, (64, 138, 76), shade=(44, 104, 58), light=(96, 170, 96), sdir="right", band=2,
                    olcol=(30, 70, 40))
        herbe = c.mask_rect(0, hz, W, H) & tout_
        c.vgrad(herbe, hz, H, (92, 168, 86), (112, 188, 98), steps=6)
        c.dither(herbe, (100, 178, 90), 0.15)
        ch = c.mask_poly([(118, hz + 2), (128, hz + 2), (150, H), (98, H)]) & tout_ # le chemin vers la mosquée
        c.fill(ch, (214, 194, 150))
        c.dither(ch, (196, 176, 134), 0.2)
        # le city stade (à gauche) : sol orange, grillage, petite cage
        st = c.mask_poly([(0, 108), (60, 108), (66, 150), (0, 150)]) & tout_
        c.fill(st, (70, 150, 86))
        c.fill(c.mask_rect(0, 128, 63, 129) & st, (236, 240, 236))
        _grillage(c, 0, 62, 70, 110, poteaux=20)
        for x in (2, 22, 42):                                                      # ombres longues (vers la droite)
            om = c.mask_poly([(x, 110), (x + 2, 110), (x + 26, 128), (x + 22, 128)])
            c.tint(om & herbe, (30, 60, 130), 0.28)
        s._cache["parc"] = c.img(K, rgba=True)
        return s._cache["parc"]

    def _coche(s):
        if "coche" not in s._cache:
            c = Px(12, 10, alpha=True)
            m = c.mask_poly([(0, 5), (3, 3), (5, 6), (10, 0), (12, 3), (5, 10)])
            c.shape(m, VERT, shade=(80, 180, 96), band=1, olcol=OL)
            s._cache["coche"] = c.img(5, rgba=True)
        return s._cache["coche"]

    def _image_court(s, u):
        im = s._parc().copy()
        # Grand à gauche, sourit, pouce levé
        if "grand_p" not in s._cache:
            s._cache["grand_p"] = _grand(_sprite("GRAND", "pouce", "content"), 3)
        g = s._cache["grand_p"]
        _colle(im, _halo(120, 26, (20, 40, 90), 6), 190, 878, 0.45)
        im.alpha_composite(g, (int(190 - g.width / 2), int(880 - 94 * 3)))
        # le ballon reste au bord du terrain : « APRÈS ! »
        b = _ballon_c(10, 0.6)
        _colle(im, _halo(80, 18, (20, 40, 90), 5), 352, 878, 0.45)
        im.alpha_composite(b, (int(360 - b.width / 2), int(872 - b.height / 2 - 24)))
        s._pose(im, s._lab("APRÈS !", JAUNE, 44), 360, 760, smooth((u - 0.8) / 0.35), maxw=300)
        # Petit part EN MARCHANT (pas calme et décidé) vers la mosquée
        v = max(0.0, u - 0.35)
        x = 430 + 95 * v
        y = 880 - 14 * v
        step = int(v * 7) % 8 if u > 0.35 else None
        cle = ("petit_m", step)
        if cle not in s._cache:
            s._cache[cle] = _grand(_sprite("PETIT", "neutre", "content", step=step), 3)
        p = s._cache[cle]
        a = 1 - smooth((x - 760) / 80)
        if a > 0.01:
            _colle(im, _halo(110, 24, (20, 40, 90), 6), x + 4, y - 2, 0.45 * a)
            im.alpha_composite(_fade(p, a), (int(x - p.width / 2), int(y - 94 * 3)))
        # textes
        # (08/11 : textes descendus sous la zone du carton de fin « ABONNE-TOI », y < 210 du schéma, que le plan
        # chevauche pendant ses dernières 0,6 s)
        s._pose(im, s._lab("PRIE L'ASR AVANT QUE // LE SOLEIL JAUNISSE", BLANC, 50), CX_T, 272, smooth(u / 0.35),
                maxw=860)
        e = smooth((u - 0.6) / 0.4)
        lab = s._lab("LE SOLEIL N'A PAS // ENCORE JAUNI", VERT, 36)
        s._pose(im, lab, 330, 414, e, maxw=480)
        co = s._coche()
        _colle(im, co, 330 + min(lab.width, 480) / 2 + 40, 426, e)
        return im


# ---------------------------------------------------------------- branchement (via explique_0811.py)
CLES = ["soleilbas", "asr"]


def _norm(m):
    return m.lower().replace("é", "e").replace("è", "e").replace("ê", "e")


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique_0811.ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""

    def dernier(mode):
        return next((it["el"] for it in reversed(schema._visibles(t + 0.01))
                     if isinstance(it["el"], Asr) and it["el"].mode == mode), None)

    def u_de(el):
        return t - next(it["t_in"] for it in schema.items if it["el"] is el)

    def etape(nom, mode):
        el = dernier(mode)
        if el is None:
            el = Asr(brut, mode)
            schema._ajoute(t, el)
        el.t[nom] = u_de(el)

    if k == "soleilbas":
        qui = mots[1].upper() if len(mots) > 1 else "PETIT"
        schema._ajoute(t, Asr(brut, "soleilbas", qui))
    elif k == "asr":
        if sous in Asr.ETAPES_CARTE:
            etape(sous, "carte")
        elif sous == "rater":
            schema._ajoute(t, Asr(brut, "frise"))
        elif sous == "jaune":
            etape("jaune", "frise")
        elif sous == "court":
            schema._ajoute(t, Asr(brut, "court"))
        else:
            schema._ajoute(t, Asr(brut, "carte"))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "soleilbas":
        return t + 2.4
    if k == "asr":
        return t + dict(famille=1.3, biens=1.2, vide=1.9, rater=2.6, jaune=2.4, court=1.2).get(sous, 1.2)
    return None
