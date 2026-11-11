# DÉMONSTRATION EN IMAGE DU 08/11/2026 — Short ISL25 « Tu manges de la main gauche ? Arrête ! » (format consigne +
# avertissement). Même principe que explique_0611_dette.py : le sens propre du hadith, montré en grand, avec des
# mouvements doux (glissés, fondus, échelles lentes ; jamais de secousse, de flash ni de rebond).
# RÈGLES DE CE MODULE : le Chaytan n'est JAMAIS dessiné (ni ombre, ni cornes, ni yeux, ni brume : seulement du TEXTE) ;
# l'homme du récit de Mouslim 2021 n'est JAMAIS dessiné (ni corps, ni main, ni silhouette) ; aucun prophète, ange ni
# Compagnon ; rien de gore (le plâtre est blanc et propre). Les mains sont celles de PETIT (sweat rouge) vues à ta place :
# la main GAUCHE est à GAUCHE de l'écran, la DROITE à DROITE. Le fil du téléphone reste abstrait (formes, cœurs).
#   {repas PETIT}         accroche, vue à ta place, au snack : ta main GAUCHE monte un tacos vers toi (il grandit et
#                         monte), ta main DROITE tient ton téléphone (le fil défile, le pouce bouge, lueur bleue) ; un
#                         cercle orange fin pulse autour de la main gauche.
#   {maindroite}          (à placer sur « Arrête ! ») la main gauche s'arrête en douceur à mi-chemin, le snack s'assombrit
#                         un peu ;
#   {maindroite chaytan}  l'étiquette rouge « COMME / LE CHAYTAN » descend au-dessus de la main gauche (sa pointe pulse
#                         lentement) ; en haut, la citation « « … LE CHAYTAN / MANGE DE LA GAUCHE » » mot par mot (jamais
#                         avant 3,05 s : l'ACCROCHE est encore là) — Mouslim 2019 · 2020.
#   {maindroite recit}    le récit SANS PERSONNE : vue de haut d'une nappe de cuir (soufra), un plat de pain, des dattes,
#                         une bouchée de pain posée ; bulle dorée « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : « MANGE DE TA
#                         MAIN DROITE. » » ; en petit « SAHIH MOUSLIM · RÉCIT DE SALAMA IBN AL-AKWA' » ;
#   {maindroite refus}    bulle grise « UN HOMME : « JE NE PEUX PAS. » » ;
#   {maindroite orgueil}  tampon « PAR ORGUEIL » (descente douce, sans rebond) + « SEUL L'ORGUEIL L'EN EMPÊCHAIT » ;
#   {maindroite plus}     la bulle dorée devient « « PUISSES-TU NE PAS POUVOIR ! » » (bulle grise et tampon restent) ;
#   {maindroite fleche}   depuis la bouchée (« SA MAIN DROITE », texte seul), une flèche pointillée monte vers
#                         « SA BOUCHE » (texte seul) et s'arrête à mi-chemin ; rond gris barré ; le tampon réduit glisse
#                         dans un coin ; bandeau « IL N'A PLUS LEVÉ SA DROITE / À SA BOUCHE » ; la lumière baisse de 20 %.
#   {maindroite avis}     retour au snack : la carte crème « MANGER DE LA GAUCHE SANS EXCUSE : » / « DÉCONSEILLÉ —
#                         SELON LA MAJORITÉ (AVIS RETENU DES 4 ÉCOLES) » / « PÉCHÉ — SELON IBN AL-'ARABI, IBN HAJAR… » /
#                         bandeau vert « SI TA DROITE NE PEUT PAS (BLESSURE, MALADIE…) : AUCUN REPROCHE » glisse du bas ;
#                         puis la main droite dans un plâtre blanc propre, « EXCUSE » et une coche verte ;
#   {maindroite echange}  les objets changent de main (glissé doux) : le tacos dans la DROITE, le téléphone dans la
#                         GAUCHE ; la carte devient un bandeau en haut (toujours lisible) ; la droite monte le tacos vers
#                         toi, « MAIN DROITE » en vert ;
#   {maindroite coche}    une grande coche verte se pose sur la main droite, « ✓ MAIN DROITE » ; le téléphone continue
#                         de défiler dans la gauche (la blague).
# Branché par explique_0811.py (import tardif dans explique.Schema._ordre et scenario._fin_anim).
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import pxv
from px import Px, TAHOMA
from pxv import smooth
from explique import _fade, _os, BLANC
from explique_0411 import OL, _peau
from explique_0411b import _Base, ROUGE, OR_
from explique_0611_dette import _texte_px, _colle, _halo, _tourne_net

K = 6
SWEAT = ((200, 50, 50), (150, 34, 40), (232, 92, 84))        # le sweat rouge de Petit (comme explique_0611_dette)
VERT_C = (40, 168, 76)                                       # la coche verte
VERT_F = (34, 132, 62)                                       # le bandeau vert de la carte
CREME = (250, 242, 222)
ENCRE = (54, 42, 34)
JAUNE_F = (176, 120, 0)                                      # « DÉCONSEILLÉ » (jaune foncé, lisible sur la crème)
ORANGE_F = (212, 86, 20)                                     # « PÉCHÉ »
BRUN = (70, 44, 24)                                          # le texte des bulles dorées
OR_B = (250, 214, 112)                                       # le fond des bulles dorées
GRIS_B = (120, 124, 140)                                     # la bulle « UN HOMME : … »
ROUGE_E = (196, 40, 48)                                      # l'étiquette « COMME LE CHAYTAN »
T_CITE_MIN = 3.05                                            # la citation du haut attend la fin de l'ACCROCHE (3,0 s)


# ---------------------------------------------------------------- petits outils
def _teinte(im, col, k):
    """Teinte une image RGBA vers col (k de 0 à 1), sans toucher à la transparence."""
    if k <= 0.001:
        return im
    a = np.array(im).astype(np.float32)
    a[..., :3] = a[..., :3] * (1 - k) + np.array(col, np.float32) * k
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def _assombrit(im, k):
    if k <= 0.001:
        return im
    a = np.array(im).astype(np.float32)
    a[..., :3] *= (1 - k)
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def _pile(ims, gap=0, align="c"):
    """Empile des images (centrées) avec gap pixels entre elles."""
    W_ = max(i.width for i in ims)
    out = Image.new("RGBA", (W_, sum(i.height for i in ims) + gap * (len(ims) - 1)), (0, 0, 0, 0))
    y = 0
    for i in ims:
        x = 0 if align == "l" else int((W_ - i.width) / 2)
        out.alpha_composite(i, (x, y))
        y += i.height + gap
    return out


def _txt_fit(txt, col, size, maxw, kmax=6, kmin=2, **kw):
    """Texte pixel net au plus grand agrandissement entier qui tient dans maxw."""
    for k in range(kmax, kmin - 1, -1):
        im = _texte_px(txt, col, size, k=k, pad=1, **kw)
        if im.width <= maxw:
            return im
    return _texte_px(txt, col, size, k=kmin, pad=1, **kw)


def _coche_img(r=1.0):
    """Grande coche verte pixel (bordée de blanc, contour sombre)."""
    W, H = 30, 24
    c = Px(W, H, alpha=True)
    m = _os(c, 4, 13, 11, 20, 6) | _os(c, 11, 20, 26, 4, 6)
    big = _os(c, 4, 13, 11, 20, 9) | _os(c, 11, 20, 26, 4, 9)
    c.fill(big, (255, 255, 255))
    c.outline(big, OL)
    c.shape(m, (64, 196, 96), shade=VERT_F, light=(140, 232, 150), band=1, ol=False)
    return c.img(int(K * r), rgba=True)


# ---------------------------------------------------------------- l'élément
class Droite(_Base):
    """{repas PETIT} (accroche, vue à ta place : tacos dans la main gauche, téléphone dans la droite) ; {maindroite} (la
    gauche s'arrête), {maindroite chaytan} (« COMME LE CHAYTAN » + citation de Mouslim 2019) ; {maindroite recit|refus|
    orgueil|plus|fleche} (le récit de Mouslim 2021 sans personne : nappe, pain, bulles, tampon, flèche qui s'arrête) ;
    {maindroite avis|echange|coche} (la carte des avis + l'excuse du plâtre ; les objets changent de main ; coche verte)."""
    ETAPES_REPAS = ("stop", "chaytan")
    ETAPES_RECIT = ("refus", "orgueil", "plus", "fleche")
    ETAPES_AVIS = ("echange", "coche")
    PW_, PH_ = 170, 150                 # panneau du snack (pixels du dessin ×6 = 1020 × 900)
    RW, RH = 170, 160                   # panneau du récit (1020 × 960)
    # le bras (pixels du dessin) : un bras droit, la prise (là où se tient l'objet) en G
    GW, GH = 64, 112
    G = (32, 62)
    # l'accroche (pixels d'écran, panneau 1020 × 900)
    PIV_G0, SC_G0 = (300, 965), 0.95    # le bras gauche au départ (bas du bras, échelle)
    PIV_G1, SC_G1 = (380, 985), 1.14    # … et là où il irait (vers ta bouche : il grandit surtout)
    D_MONTE = 2.7                       # durée de la montée (elle s'arrête en douceur sur « Arrête ! »)
    PIV_D, SC_D = (742, 912), 0.95      # le bras droit (téléphone)
    DY_AVIS = 240                       # les mains descendent sous la carte des avis
    # le récit (pixels d'écran, panneau 1020 × 960)
    BOUCHEE = (762, 672)                # la bouchée de pain posée
    STOP = (802, 500)                   # là où la flèche s'arrête
    BOUCHE = (840, 352)                 # l'étiquette « SA BOUCHE » (là où elle irait)

    def __init__(s, cmd, mode="repas", who="PETIT"):
        super().__init__(cmd)
        s.mode = mode
        s.who = "PETIT"
        s.negatif = mode == "repas"

    def sons_el(s):
        out = []
        if s.mode == "repas":
            if "chaytan" in s.t:
                out.append((s.t["chaytan"], "tr_whoosh_doux", 0.025, None))
            return out
        if s.mode == "recit":
            if "orgueil" in s.t:
                out.append((s.t["orgueil"] + 0.3, "imp_tampon", 0.03, None))
            if "fleche" in s.t:
                out.append((s.t["fleche"], "tr_whoosh_doux", 0.025, None))
            return out
        out.append((0.75, "sa_ting", 0.025, None))
        if "echange" in s.t:
            out.append((s.t["echange"], "tr_whoosh_doux", 0.025, None))
        if "coche" in s.t:
            out.append((s.t["coche"] + 0.1, "sa_ting", 0.03, None))
        return out

    def image(s, u):
        if s.mode == "recit":
            return s._image_recit(u)
        if s.mode == "avis":
            return s._image_avis(u)
        return s._image_repas(u)

    def _zoom(s, im, k, cle_im=None):
        k = round(k, 2)
        cle = ("z", cle_im if cle_im is not None else id(im), k)
        if cle_im is None or cle not in s._cache:
            z = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
            if cle_im is None:
                return z
            s._cache[cle] = z
        return s._cache[cle]

    # ============================================================ le snack (fond)
    def _snack(s):
        if "snack" in s._cache:
            return s._cache["snack"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        mur = c.mask_rect(0, 0, W, 98) & tout_
        c.vgrad(mur, 0, 98, (84, 40, 52), (150, 84, 70), steps=5)
        for j, y in enumerate(range(0, 98, 9)):                                    # le carrelage
            c.tint(c.mask_rect(0, y, W, y + 1) & mur, (30, 14, 18), 0.35)
            dec = 0 if j % 2 == 0 else 7
            for x in range(-dec, W, 14):
                c.tint(c.mask_rect(x, y, x + 1, y + 9) & mur, (30, 14, 18), 0.35)
                c.tint(c.mask_rect(x + 2, y + 2, x + 5, y + 3) & mur, (255, 220, 190), 0.10)
        frise = c.mask_rect(0, 74, W, 78) & tout_
        c.shape(frise, (196, 146, 60), shade=(150, 106, 40), light=(226, 182, 90), sdir="bottom", band=1, olcol=OL)
        tab = c.mask_rect(8, 30, 52, 66)                                           # le tableau du menu (images)
        c.shape(tab, (126, 84, 52), shade=(96, 62, 38), light=(150, 106, 70), band=1, olcol=OL)
        c.fill(c.mask_rect(10, 32, 50, 64), (36, 36, 44))
        c.fill(c.mask_poly([(14, 40), (30, 40), (27, 46), (17, 46)]), (232, 176, 82))     # un tacos (dessin)
        c.fill(c.mask_rect(16, 38, 28, 40), (96, 176, 74))
        c.fill(c.mask_poly([(35, 37), (45, 37), (44, 46), (36, 46)]), (210, 50, 50))     # des frites
        for x in (36, 38, 40, 42, 44):
            c.fill(c.mask_rect(x, 33 + (x % 3), x + 1, 38), (250, 210, 80))
        for j, y in enumerate((51, 55, 59)):                                       # les prix (traits)
            c.fill(c.mask_rect(13, y, 13 + (16, 12, 18)[j], y + 1), (196, 196, 206))
            c.fill(c.mask_rect(40, y, 46, y + 1), (250, 200, 80))
        neon = c.mask_rrect(116, 30, 160, 60, 6) & ~c.mask_rrect(118, 32, 158, 58, 5)   # le néon (cadre rose)
        c.glow(138, 45, 30, (255, 110, 160), k=0.25, m=mur)
        c.fill(neon, (255, 150, 196))
        c.fill(c.mask_rect(126, 41, 150, 43), (255, 214, 120))                     # un trait de néon jaune
        c.fill(c.mask_rect(130, 47, 146, 49), (255, 214, 120))
        table = c.mask_rect(0, 96, W, H) & tout_
        c.fill(table, (104, 68, 48))
        c.dither(table, (92, 58, 42), 0.25)
        c.fill(c.mask_rect(0, 96, W, 98) & tout_, (146, 100, 70))
        c.fill(c.mask_rect(0, 98, W, 99) & tout_, (70, 44, 34))
        plateau = c.mask_rrect(56, 112, 116, 152, 3)                               # le plateau rouge
        c.shape(plateau, (190, 44, 48), shade=(146, 30, 36), light=(226, 90, 86), band=2, olcol=OL)
        c.fill(c.mask_rrect(59, 115, 113, 152, 2), (176, 38, 44))
        papier = c.mask_poly([(64, 117), (104, 115), (106, 152), (62, 152)])       # le papier du plateau
        c.fill(papier, (236, 226, 204))
        c.dither(papier, (214, 204, 182), 0.18)
        frites = c.mask_poly([(76, 112), (96, 112), (93, 134), (79, 134)])         # la barquette de frites
        for x in range(78, 95, 3):
            fr = c.mask_rect(x, 101 + (x * 7) % 6, x + 2, 114)
            c.shape(fr, (250, 206, 80), shade=(214, 160, 50), band=1, olcol=OL)
        c.shape(frites, (210, 50, 50), shade=(160, 34, 40), light=(236, 96, 90), band=2, olcol=OL)
        c.fill(c.mask_rect(82, 120, 90, 126) & frites, (250, 210, 80))
        sauce = c.mask_ell(104, 128, 5, 3.5)                                       # la sauce blanche
        c.shape(sauce, (236, 236, 228), shade=(200, 200, 190), band=1, olcol=OL)
        im = c.img(K, rgba=True)
        lay = Image.new("RGBA", im.size, (20, 10, 20, 0))                           # pénombre douce sur les bords
        a = np.zeros((im.height, im.width, 4), np.uint8)
        a[..., :3] = (20, 10, 20)
        yy, xx = np.mgrid[0:im.height, 0:im.width]
        d = np.sqrt(((xx - im.width / 2) / (im.width * 0.62)) ** 2 + ((yy - im.height * 0.55) / (im.height * 0.66)) ** 2)
        a[..., 3] = (np.clip((d - 0.55) / 0.5, 0, 1) * 90).astype(np.uint8)
        a[..., 3] = np.minimum(a[..., 3], np.array(im)[..., 3])
        lay = Image.fromarray(a, "RGBA")
        im.alpha_composite(lay)
        s._cache["snack"] = im
        return im

    def _masque(s, W, H):
        cle = ("masque", W, H)
        if cle not in s._cache:
            m = Image.new("L", (W, H), 0)
            ImageDraw.Draw(m).rounded_rectangle([0, 0, W - 1, H - 1], 36, fill=255)
            s._cache[cle] = m
        return s._cache[cle]

    def _rogne(s, im):
        """Coupe ce qui dépasse du panneau arrondi (les bras sortent par le bas)."""
        a = np.array(im)
        a[..., 3] = np.minimum(a[..., 3], np.array(s._masque(im.width, im.height)))
        return Image.fromarray(a, "RGBA")

    # ============================================================ les objets
    def _tacos(s):
        """Le tacos tenu debout : la tortilla dorée en demi-lune, ouverte en haut (salade, viande, tomate, sauce blanche)."""
        if "tacos" in s._cache:
            return s._cache["tacos"]
        W, H = 58, 44
        c = Px(W, H, alpha=True)
        garni = c.mask_ell(29, 12, 25, 8)                                          # la garniture (au-dessus du bord)
        c.fill(garni, (120, 70, 44))
        for j, x in enumerate(range(6, 54, 5)):                                    # la salade qui dépasse
            y = 5 + (j * 5) % 4
            f_ = c.mask_ell(x, y, 3.6, 3)
            c.shape(f_, (110, 190, 76), shade=(70, 140, 50), light=(160, 220, 110), band=1, olcol=OL)
        for x in (14, 31, 44):                                                     # la tomate
            t_ = c.mask_ell(x, 9, 3, 2.2)
            c.shape(t_, (222, 60, 50), shade=(170, 40, 36), band=1, olcol=OL)
        for x in (21, 37):                                                         # la viande
            v_ = c.mask_ell(x, 11, 3.4, 2.4)
            c.shape(v_, (128, 74, 44), shade=(96, 52, 30), light=(160, 100, 64), band=1, olcol=OL)
        coque = c.mask_ell(29, 10, 28, 33) & c.mask_rect(0, 12, W, H)               # la tortilla (demi-lune)
        c.shape(coque, (232, 176, 82), shade=(194, 134, 52), light=(250, 214, 132), sdir="bottom", band=3,
                ldir="top", lband=1, olcol=OL)
        rng = np.random.default_rng(3)
        for _ in range(22):                                                        # les marques de grill
            x, y = int(rng.integers(6, W - 6)), int(rng.integers(16, 38))
            if coque[y, x] and coque[y, x + 2]:
                c.fill(c.mask_rect(x, y, x + 2, y + 1), (176, 112, 44))
        for x in range(5, 53, 2):                                                  # la sauce blanche (un filet ondulé
            y = 10 + int(round(1.2 * math.sin(x * 0.55)))                          # dans la garniture, pas de gouttes)
            c.fill(c.mask_rect(x, y, x + 2, y + 2) & garni, (246, 246, 236))
        bord = c.mask_rect(1, 12, W - 1, 14) & coque                               # le bord replié, plus clair
        c.fill(bord, (246, 204, 120))
        s._cache["tacos"] = (c.img(K, rgba=True), (29 * K, 37 * K))                # (l'image, le point tenu)
        return s._cache["tacos"]

    def _fil(s):
        """Le fil de vidéos (abstrait : blocs de couleur, cœurs, traits ; aucun visage), deux fois de suite."""
        if "fil" in s._cache:
            return s._cache["fil"]
        W, P = 28, 64
        c = Px(W, 2 * P, alpha=True)
        c.fill(c.mask_rect(0, 0, W, 2 * P), (18, 18, 26))
        cols = [((64, 132, 220), (120, 186, 255)), ((236, 132, 60), (255, 196, 110)), ((120, 200, 140), (186, 240, 196)),
                ((170, 96, 210), (214, 160, 250))]
        for rep in range(2):
            for j in range(2):
                y0 = rep * P + j * 32
                fond, clair = cols[(j + 2 * rep) % 4] if rep == 0 else cols[j]
                bloc = c.mask_rrect(2, y0 + 2, W - 2, y0 + 24, 2)
                c.vgrad(bloc, y0 + 2, y0 + 24, clair, fond, steps=4)
                c.fill(c.mask_ell(9 + 6 * j, y0 + 12, 4 + j, 3), clair)            # des formes abstraites
                c.fill(c.mask_rect(15 - 4 * j, y0 + 16, 22 - 4 * j, y0 + 19), fond)
                coeur = c.mask_ell(W - 7.5, y0 + 6.5, 1.6, 1.6) | c.mask_ell(W - 5.5, y0 + 6.5, 1.6, 1.6) | \
                    c.mask_poly([(W - 9.5, y0 + 7), (W - 3.5, y0 + 7), (W - 6.5, y0 + 10.5)])
                c.fill(coeur, (255, 80, 110))
                c.fill(c.mask_rect(3, y0 + 26, 18, y0 + 27), (196, 196, 210))      # deux traits gris (texte flou)
                c.fill(c.mask_rect(3, y0 + 29, 12, y0 + 30), (130, 130, 146))
        s._cache["fil"] = c.img(K, rgba=True)
        return s._cache["fil"]

    def _tel_base(s):
        if "telb" in s._cache:
            return s._cache["telb"]
        W, H = 34, 64
        c = Px(W, H, alpha=True)
        corps = c.mask_rrect(0, 0, W, H, 6)
        c.shape(corps, (42, 42, 54), shade=(24, 24, 32), light=(100, 100, 118), band=2, olcol=OL)
        c.fill(c.mask_rrect(3, 4, W - 3, H - 4, 3), (18, 18, 26))
        c.fill(c.mask_rrect(13, 5, 21, 7, 1), (8, 8, 12))                          # l'encoche
        s._cache["telb"] = (c.img(K, rgba=True), (17 * K, 54 * K))
        return s._cache["telb"]

    def _tel(s, u):
        """Le téléphone allumé : le fil défile doucement vers le haut (au pixel d'écran près)."""
        base, prise = s._tel_base()
        im = base.copy()
        fil = s._fil()
        P = 64 * K
        off = int((u * 52) % P)
        x0, y0, x1, y1 = 3 * K, 8 * K, 31 * K, 60 * K
        cr = fil.crop((0, off, fil.width, off + (y1 - y0)))
        m = Image.new("L", cr.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, cr.width - 1, cr.height - 1], 14, fill=255)
        im.paste(cr, (x0, y0), m)
        ImageDraw.Draw(im).rectangle([x0, y0, x1 - 1, y0 + 2 * K - 1], fill=(18, 18, 26, 255))   # la barre du haut
        for x in (5, 7, 9):
            ImageDraw.Draw(im).rectangle([x * K, y0 + 4, x * K + 5, y0 + 9], fill=(220, 220, 230, 255))
        return im, prise

    # ============================================================ la main
    def _main_px(s, objet, phase=0):
        """Main DROITE (vue à ta place) : arrière (manche, paume) et avant (pouce et doigts autour de l'objet)."""
        cle = ("main", objet, phase)
        if cle in s._cache:
            return s._cache[cle]
        p = _peau("PETIT")
        b, s_, h, dk = p["b"], p["s"], p["h"], p["d"]
        W, H = s.GW, s.GH
        gx, gy = s.G
        ar = Px(W, H, alpha=True)
        manche = ar.mask_poly([(16, H + 2), (50, H + 2), (46, gy + 18), (19, gy + 18)])
        ar.shape(manche, SWEAT[0], shade=SWEAT[1], light=SWEAT[2], band=3, olcol=OL)
        poignet = ar.mask_rrect(17, gy + 13, 48, gy + 22, 2)                       # le bord côtelé
        ar.shape(poignet, SWEAT[1], shade=(120, 26, 32), light=SWEAT[0], band=1, olcol=OL)
        for x in range(20, 46, 4):
            ar.fill(ar.mask_rect(x, gy + 14, x + 1, gy + 21) & poignet, (120, 26, 32))
        paume = ar.mask_ell(gx + 1, gy + 6, 14, 10)
        ar.shape(paume, b, shade=s_, light=h, band=2, olcol=OL)
        av = Px(W, H, alpha=True)
        hw = 25 if objet == "tacos" else 17
        for j in range(3):                                                         # les doigts, côté extérieur
            y = gy - 12 + 7 * j
            d_ = av.mask_rrect(gx + hw - 4, y, gx + hw + 5, y + 7, 3)
            av.shape(d_, b, shade=s_, light=h, band=1, olcol=OL)
            av.fill(av.mask_rect(gx + hw - 3, y + 5, gx + hw + 2, y + 6) & d_, s_)
        dy = (0, -1, -3, -1)[phase % 4] if objet == "tel" else 0
        if objet == "tacos":                                                       # le pouce sur le bord intérieur
            x0_, y0_, x1_, y1_ = gx - 13, gy + 6, gx - hw + 3, gy - 6
        else:                                                                      # le pouce sur l'écran (il défile)
            x0_, y0_, x1_, y1_ = gx - 10, gy + 6, gx - 5, gy - 9 + dy
        pouce = _os(av, x0_, y0_, x1_, y1_, 8)
        av.shape(pouce, b, shade=s_, light=h, band=1, olcol=OL)
        ongle = av.mask_ell(x1_, y1_ - 1, 2.4, 2) & pouce
        av.fill(ongle, (246, 216, 198))
        out = (ar.img(K, rgba=True), av.img(K, rgba=True))
        s._cache[cle] = out
        return out

    def _bras(s, cote, objet, u, a_obj=1.0, avants=None, lueur=None):
        """Le bras entier (image au dessin ×6, le bas du bras en bas au centre) : arrière, objet, avant.
        cote = 'g' (miroir) ou 'd' ; objet = 'tacos', 'tel' ou None ; avants = [(objet, opacité)] pour les doigts."""
        phase = int(u / 0.22) % 4
        if lueur is None:
            lueur = objet == "tel"
        ar, _ = s._main_px(objet or "tel", phase)
        W, H = s.GW * K, s.GH * K
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ar_ = ar.transpose(Image.FLIP_LEFT_RIGHT) if cote == "g" else ar
        im.alpha_composite(_teinte(ar_, (110, 160, 255), 0.18) if lueur else ar_)
        gx, gy = s.G[0] * K, s.G[1] * K
        if objet is not None and a_obj > 0.01:
            if objet == "tacos":
                ob, (ox, oy) = s._tacos()
            else:
                ob, (ox, oy) = s._tel(u)
                hal = _halo(ob.width + 60, ob.height + 40, (90, 150, 255), 26)     # la lueur bleue de l'écran
                _colle(im, hal, gx, gy - oy + ob.height / 2, 0.28 * a_obj)
            im.alpha_composite(_fade(ob, a_obj), (int(gx - ox), int(gy - oy)))
        for (ob_, a_) in (avants if avants is not None else [(objet, 1.0)]):
            if ob_ is None or a_ <= 0.01:
                continue
            _, av = s._main_px(ob_, phase)
            av_ = av.transpose(Image.FLIP_LEFT_RIGHT) if cote == "g" else av
            if ob_ == "tel":
                av_ = _teinte(av_, (110, 160, 255), 0.18)
            im.alpha_composite(_fade(av_, a_))
        return im

    def _pose_bras(s, im, bras, piv, sc):
        """Colle un bras réduit/agrandi : le milieu du bas du bras en piv (pixels d'écran)."""
        z = s._zoom(bras, sc)
        im.alpha_composite(z, (int(piv[0] - z.width / 2), int(piv[1] - z.height)))
        return (piv[0], piv[1] - (s.GH - s.G[1]) * K * sc)                        # où est la prise

    # ============================================================ {repas} {maindroite} {maindroite chaytan}
    def _montee(s, u):
        """Avancement de la main gauche vers ta bouche (0 → 1) ; après « stop », elle ralentit et s'arrête (0,3 s)."""
        ts = s.t.get("stop")
        if ts is not None and u > ts:
            x = min(1.0, (u - ts) / 0.3)
            u = ts + 0.3 * (1 - (1 - x) ** 2) / 2
        return smooth(max(0.0, u) / s.D_MONTE)

    def _gauche_tacos(s, u, dy=0.0):
        p = s._montee(u)
        piv = (s.PIV_G0[0] + (s.PIV_G1[0] - s.PIV_G0[0]) * p, s.PIV_G0[1] + (s.PIV_G1[1] - s.PIV_G0[1]) * p + dy)
        return piv, s.SC_G0 + (s.SC_G1 - s.SC_G0) * p

    def _citation(s, u):
        """La citation du haut, mot par mot : « … LE CHAYTAN / MANGE DE LA GAUCHE » (coupe marquée)."""
        tc = s.t.get("chaytan")
        if tc is None:
            return None
        t0 = max(tc, T_CITE_MIN)
        mots = [("« … LE CHAYTAN", 0), ("MANGE", 1), ("DE", 1), ("LA", 1), ("GAUCHE »", 1)]
        dts = (0.0, 0.18, 0.36, 0.48, 0.62)
        lay = Image.new("RGBA", (1020, 190), (0, 0, 0, 0))
        e = smooth((u - t0 + 0.1) / 0.35)
        if e <= 0.01:
            return None
        ImageDraw.Draw(lay).rounded_rectangle([24, 8, 996, 182], 26, fill=(16, 10, 18, int(190 * e)))
        ims = [s._lab(m_, BLANC if i < 1 else (255, 214, 70), 54) for i, (m_, _) in enumerate(mots)]
        ims[0] = s._lab(mots[0][0], BLANC, 54)
        l2 = ims[1:]
        esp = -8
        w2 = sum(i.width for i in l2) + esp * (len(l2) - 1)
        x = (1020 - w2) / 2
        pos = [(510 - ims[0].width / 2, 14)]
        for i in l2:
            pos.append((x, 92))
            x += i.width + esp
        for j, (im_, (x_, y_)) in enumerate(zip(ims, pos)):
            a = smooth((u - t0 - dts[j]) / 0.25)
            if a > 0.01:
                lay.alpha_composite(_fade(im_, a), (int(x_), int(y_ + 10 * (1 - a))))
        return lay

    def _etiquette(s):
        """L'étiquette rouge « COMME / LE CHAYTAN » (texte blanc) et sa pointe vers le bas (à part : elle pulse)."""
        if "etiq" in s._cache:
            return s._cache["etiq"]
        l1 = _texte_px("COMME", BLANC, 11, k=5, pad=1, gras=True)
        l2 = _texte_px("LE CHAYTAN", BLANC, 11, k=6, pad=1, gras=True)
        tx = _pile([l1, l2], gap=-6)
        W_, H_ = tx.width + 60, tx.height + 34
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 22, fill=(*OL, 255))
        d.rounded_rectangle([6, 6, W_ - 7, H_ - 7], 18, fill=(255, 255, 255, 255))
        d.rounded_rectangle([12, 12, W_ - 13, H_ - 13], 14, fill=(*ROUGE_E, 255))
        im.alpha_composite(tx, (int((W_ - tx.width) / 2), int((H_ - tx.height) / 2) + 2))
        po = Image.new("RGBA", (90, 70), (0, 0, 0, 0))
        dp = ImageDraw.Draw(po)
        dp.polygon([(4, 2), (86, 2), (45, 66)], fill=(*OL, 255))
        dp.polygon([(14, 6), (76, 6), (45, 54)], fill=(255, 255, 255, 255))
        dp.polygon([(23, 8), (67, 8), (45, 42)], fill=(*ROUGE_E, 255))
        s._cache["etiq"] = (im, po)
        return s._cache["etiq"]

    def _anneau(s, im, cx, cy, r, a, col=(255, 150, 60)):
        if a <= 0.01:
            return
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        A = int(255 * a)
        d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], outline=(20, 10, 16, int(A * 0.6)), width=14)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(*col, A), width=8)
        im.alpha_composite(lay)

    def _image_repas(s, u):
        im = s._snack().copy()
        ts = s.t.get("stop")
        if ts is not None:                                                         # le snack s'assombrit un peu
            im = _assombrit(im, 0.22 * smooth((u - ts) / 0.5))
        piv_d = (s.PIV_D[0] + 3 * math.sin(2 * math.pi * u / 3.1), s.PIV_D[1] + 6 * math.sin(2 * math.pi * u / 2.4))
        s._pose_bras(im, s._bras("d", "tel", u), piv_d, s.SC_D)
        piv_g, sc_g = s._gauche_tacos(u)
        gx, gy = s._pose_bras(im, s._bras("g", "tacos", u), piv_g, sc_g)
        cx, cy = gx, gy - 80 * sc_g                                                # le centre du tacos + la main
        tc = s.t.get("chaytan")
        a_ann = 1.0 - (smooth((u - tc) / 0.35) if tc is not None else 0.0)
        pul = 1.0 + 0.03 * (1 - math.cos(2 * math.pi * max(0.0, u) / 1.2))       # 1,0 → 1,06, cycle 1,2 s
        s._anneau(im, cx, cy + 20, 215 * sc_g * pul, a_ann * min(1.0, 0.6 + max(0.0, u + 0.4)))
        if tc is not None:                                                         # « COMME LE CHAYTAN »
            et, po = s._etiquette()
            e = smooth((u - tc) / 0.45)
            top_tacos = gy - 170 * sc_g
            ey = top_tacos - 34 - et.height / 2 - 60 * (1 - e)
            ex = min(max(cx, et.width / 2 + 24), 1020 - et.width / 2 - 24)
            pz = 1.0 + 0.025 * (1 - math.cos(2 * math.pi * max(0.0, u - tc) / 1.2))   # 1,0 → 1,05
            po_ = s._zoom(po, pz)
            _colle(im, po_, cx, ey + et.height / 2 + 22 + po_.height / 2 - 10, e)
            _colle(im, et, ex, ey, e)
        cit = s._citation(u)
        if cit is not None:
            im.alpha_composite(cit, (0, 6))
        return s._rogne(im)

    # ============================================================ {maindroite recit …}
    def _nappe(s):
        """Vue de haut : le sol sombre, la nappe de cuir (soufra), le plat de pain, les dattes, la bouchée posée.
        AUCUNE personne, aucune main."""
        if "nappe" in s._cache:
            return s._cache["nappe"]
        W, H = s.RW, s.RH
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        c.fill(tout_, (40, 24, 22))
        c.rgrad(tout_, 85, 112, 120, (92, 58, 40), (34, 20, 18), steps=6)          # la lumière chaude au centre
        rng = np.random.default_rng(11)
        for _ in range(140):                                                       # le sol (sable tassé)
            x, y = int(rng.integers(2, W - 2)), int(rng.integers(2, H - 2))
            c.tint(c.mask_rect(x, y, x + 2, y + 1) & tout_, (10, 4, 4), 0.25)
        nappe = c.mask_rrect(20, 80, 150, 152, 10)
        c.shape(nappe, (196, 146, 92), shade=(160, 112, 66), light=(220, 176, 120), sdir="bottom", band=3, olcol=OL)
        c.dither(nappe & ~c.mask_rrect(23, 83, 147, 149, 8), (170, 124, 76), 0.3)
        couture = c.mask_rrect(25, 85, 145, 147, 7) & ~c.mask_rrect(26, 86, 144, 146, 6)
        for y in range(80, 153):                                                   # les points de couture
            for x in range(18, 152):
                if couture[y, x] and (x + y) % 3 == 0:
                    c.px(x, y, (128, 84, 46))
        plat = c.mask_ell(52, 114, 25, 19)                                         # le plat en bois
        c.shape(plat, (150, 96, 52), shade=(112, 68, 36), light=(184, 128, 76), sdir="bottom", band=2, olcol=OL)
        c.fill(c.mask_ell(52, 114, 20, 14), (172, 114, 64))
        c.dither(c.mask_ell(52, 114, 20, 14), (156, 100, 54), 0.2)
        for (x, y, rx, ry) in ((45, 111, 11, 8), (60, 118, 11, 7.5)):              # deux pains plats
            pain = c.mask_ell(x, y, rx, ry)
            c.shape(pain, (226, 174, 96), shade=(186, 128, 62), light=(244, 208, 140), band=2, olcol=OL)
            for k_ in range(6):
                c.px(int(x - rx / 2 + (k_ * 7) % int(rx)), int(y - 2 + (k_ * 5) % 5), (176, 116, 54))
        bol = c.mask_ell(104, 100, 11, 8)                                          # le bol de dattes
        c.shape(bol, (176, 104, 66), shade=(132, 74, 44), light=(206, 138, 92), sdir="bottom", band=2, olcol=OL)
        for (x, y) in ((100, 98), (106, 97), (103, 102), (109, 101), (98, 102)):
            dt = c.mask_ell(x, y, 3, 2)
            c.shape(dt, (112, 44, 30), shade=(80, 28, 20), light=(164, 84, 56), band=1, olcol=OL)
        bx, by = s.BOUCHEE[0] / K, s.BOUCHEE[1] / K                                # la bouchée posée (elle ne bouge pas)
        bouchee = c.mask_poly([(bx - 6, by - 2), (bx - 2, by - 5), (bx + 5, by - 4), (bx + 6, by + 2), (bx + 1, by + 4),
                               (bx - 5, by + 3)])
        c.shape(bouchee, (230, 182, 104), shade=(186, 130, 64), light=(246, 214, 150), band=1, olcol=OL)
        c.px(int(bx - 1), int(by - 1), (176, 116, 54))
        c.px(int(bx + 2), int(by + 1), (176, 116, 54))
        s._cache["nappe"] = c.img(K, rgba=True)
        return s._cache["nappe"]

    def _bulle(s, cle, lignes, fond, bord, pointe=None, pad=(30, 18)):
        """Bulle arrondie ; lignes = images déjà rendues (empilées, centrées) ; pointe = x relatif (0..1) en bas."""
        if cle in s._cache:
            return s._cache[cle]
        tx = _pile(lignes, gap=2)
        W_, H_ = tx.width + 2 * pad[0], tx.height + 2 * pad[1]
        im = Image.new("RGBA", (W_ + 4, H_ + (40 if pointe is not None else 4)), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if pointe is not None:
            qx = int(W_ * pointe)
            d.polygon([(qx - 26, H_ - 10), (qx + 26, H_ - 10), (qx, H_ + 36)], fill=(*OL, 255))
        d.rounded_rectangle([0, 0, W_, H_], 28, fill=(*OL, 255))
        d.rounded_rectangle([6, 6, W_ - 6, H_ - 6], 23, fill=(*bord, 255))
        d.rounded_rectangle([11, 11, W_ - 11, H_ - 11], 19, fill=(*fond, 255))
        if pointe is not None:
            d.polygon([(qx - 15, H_ - 12), (qx + 15, H_ - 12), (qx, H_ + 22)], fill=(*bord, 255))
            d.polygon([(qx - 8, H_ - 13), (qx + 8, H_ - 13), (qx, H_ + 10)], fill=(*fond, 255))
        im.alpha_composite(tx, (pad[0], pad[1] + 2))
        s._cache[cle] = im
        return im

    def _bulle_or(s, quoi):
        qui = _txt_fit("LE PROPHÈTE (PAIX ET SALUT SUR LUI) :", (120, 80, 30), 11, 860, kmax=4)
        if quoi == "mange":
            l1, l2 = "« MANGE DE TA", "MAIN DROITE. »"
        else:
            l1, l2 = "« PUISSES-TU NE", "PAS POUVOIR ! »"
        a = _texte_px(l1, BRUN, 11, k=6, pad=1, gras=True)
        b = _texte_px(l2, BRUN, 11, k=6, pad=1, gras=True)
        return s._bulle(("bor", quoi), [qui, Image.new("RGBA", (1, 8)), a, b], OR_B, (255, 246, 210))

    def _bulle_grise(s):
        qui = _texte_px("UN HOMME :", (226, 228, 236), 11, k=4, pad=1)
        b = _texte_px("« JE NE PEUX PAS. »", BLANC, 11, k=5, pad=1, gras=True)
        return s._bulle("bgr", [qui, b], GRIS_B, (196, 200, 214), pointe=None, pad=(28, 14))

    def _tampon(s):
        """Le tampon orange-rouge « PAR ORGUEIL » (cadre double, encre un peu inégale), penché de −6°, bordé de clair."""
        if "tampon" in s._cache:
            return s._cache["tampon"]
        f1 = ImageFont.truetype(TAHOMA, 17)
        W, H = int(f1.getlength("PAR ORGUEIL")) + 22, 30
        c = Px(W, H, alpha=True)
        rouge = (222, 70, 34)
        cadre = c.mask_rrect(0, 0, W, H, 3) & ~c.mask_rrect(2, 2, W - 2, H - 2, 2)
        cadre |= c.mask_rrect(4, 4, W - 4, H - 4, 1) & ~c.mask_rrect(5, 5, W - 5, H - 5, 1)
        c.fill(cadre, rouge)
        c.text((W / 2, 22), "PAR ORGUEIL", rouge, size=17, font=TAHOMA, anchor="ms")
        encre = c.al.copy()
        rng = np.random.default_rng(9)
        c.fill(encre & (rng.random((H, W)) < 0.10), (184, 50, 24))
        c.outline(encre, (255, 244, 236))
        s._cache["tampon"] = _tourne_net(c.img(4, rgba=True), -6)
        return s._cache["tampon"]

    def _pointilles(s, im, a_, b_, f, fin_a=1.0):
        """Flèche pointillée blanche de a_ vers b_ (pixels d'écran), tracée jusqu'à la fraction f ; les 3 derniers
        points s'estompent."""
        L = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
        n = int(L / 34) + 1
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        vis = [i for i in range(n) if i / max(1, n - 1) <= f + 1e-6]
        for j, i in enumerate(vis):
            x = a_[0] + (b_[0] - a_[0]) * i / max(1, n - 1)
            y = a_[1] + (b_[1] - a_[1]) * i / max(1, n - 1)
            rest = n - 1 - i
            al = 1.0 if rest >= 3 else (0.35 + 0.22 * rest)
            A = int(255 * al * fin_a)
            d.rectangle([x - 13, y - 13, x + 13, y + 13], fill=(20, 12, 16, A))
            d.rectangle([x - 8, y - 8, x + 8, y + 8], fill=(255, 255, 255, A))
        im.alpha_composite(lay)

    def _barre(s, im, x, y, a):
        if a <= 0.01:
            return
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        A = int(255 * a)
        r = 40
        d.ellipse([x - r - 4, y - r - 4, x + r + 4, y + r + 4], outline=(20, 12, 16, A), width=14)
        d.ellipse([x - r, y - r, x + r, y + r], outline=(176, 176, 186, A), width=7)
        d.line([(x - 31, y + 31), (x + 31, y - 31)], fill=(20, 12, 16, A), width=14)
        d.line([(x - 28, y + 28), (x + 28, y - 28)], fill=(176, 176, 186, A), width=7)
        im.alpha_composite(lay)

    def _image_recit(s, u):
        e0 = smooth(u / 0.3)
        tf = s.t.get("fleche")
        fond = s._nappe()
        if tf is not None:                                                         # la lumière baisse (−20 %) et la
            v = u - tf                                                             # caméra dérive vers la flèche
            fond = _assombrit(fond, 0.2 * smooth(v / 1.5))
            dx, dy = -int(10 * smooth(v / 2.5)), int(8 * smooth(v / 2.5))
        else:
            dx = dy = 0
        if dx or dy:                                                               # (les bords découverts : le sol)
            im = Image.new("RGBA", fond.size, (30, 18, 16, 255))
            im.alpha_composite(fond.crop((max(0, -dx), max(0, -dy), fond.width, fond.height)), (max(0, dx), max(0, dy)))
        else:
            im = fond.copy()
        # la source du récit, en petit, en bas (elle laisse la place au bandeau de la flèche)
        a_src = e0 * (1 - (smooth((u - tf - 0.4) / 0.4) if tf is not None else 0.0))
        src = s._cache.get("src")
        if src is None:
            src = s._cache["src"] = _txt_fit("SAHIH MOUSLIM · RÉCIT DE SALAMA IBN AL-AKWA'", (200, 196, 190), 11, 820,
                                              kmax=3)
        s._pose(im, src, 510, 928, a_src)
        # la bulle dorée (dès l'entrée) ; {plus} : elle devient « PUISSES-TU NE PAS POUVOIR ! »
        tp = s.t.get("plus")
        ap = smooth((u - tp) / 0.4) if tp is not None else 0.0
        b1 = s._bulle_or("mange")
        if ap < 0.999:
            s._pose(im, b1, 510, 26 + b1.height / 2, e0 * (1 - ap))
        if ap > 0.01:
            b2 = s._bulle_or("puisses")
            s._pose(im, b2, 510, 26 + b2.height / 2, ap)
        y_or = 26 + b1.height
        # {refus} la bulle grise ; {orgueil} le tampon et la remarque de Salama ; {fleche} la bulle grise s'efface
        ar = s._a("refus", u, 0.3, fin="fleche", dfin=0.4)
        bg = s._bulle_grise()
        yg = y_or + 22 + bg.height / 2
        s._pose(im, bg, 40 + bg.width / 2, yg + 14 * (1 - s._e("refus", u, 0.3)), ar)
        to = s.t.get("orgueil")
        if to is not None and u >= to:
            tpn = s._tampon()
            f = smooth((u - to) / 0.35)
            g = s._e("fleche", u, 0.4)
            x0, y0 = 40 + bg.width / 2 + 90, yg + bg.height / 2 + 44                                # sur le coin de la bulle (le texte
            x1, y1 = 262, 540                                                      # « JE NE PEUX PAS » reste lisible)
            x_, y_ = x0 + (x1 - x0) * g, y0 + (y1 - y0) * g - 50 * (1 - f)
            z = (1.15 - 0.15 * f) * (1 - 0.3 * g)
            tz = s._zoom(tpn, z, "tampon")
            _colle(im, tz, x_, y_, min(1.0, f * 1.5))
            rq = s._cache.get("rq")
            if rq is None:                                                         # (sur un cartouche sombre)
                t_ = _txt_fit("SEUL L'ORGUEIL L'EN EMPÊCHAIT", (255, 232, 210), 11, 700, kmax=4)
                rq = Image.new("RGBA", (t_.width + 36, t_.height + 20), (0, 0, 0, 0))
                ImageDraw.Draw(rq).rounded_rectangle([0, 0, rq.width - 1, rq.height - 1], 16, fill=(18, 10, 12, 220))
                rq.alpha_composite(t_, (18, 10))
                s._cache["rq"] = rq
            s._pose(im, rq, x0 - 30, y0 + 104, s._a("orgueil", u, 0.35, fin="fleche", dfin=0.4, dec=0.25))
        if tf is not None and u >= tf:                                             # la flèche qui s'arrête
            v = u - tf
            a_ = (s.BOUCHEE[0] + dx, s.BOUCHEE[1] - 50 + dy)
            st = (s.STOP[0] + dx, s.STOP[1] + dy)
            s._pointilles(im, a_, st, smooth(v / 1.0))
            s._barre(im, st[0], st[1] - 54, smooth((v - 1.0) / 0.4))
            lb = s._lab("SA BOUCHE", BLANC, 50)
            s._pose(im, lb, s.BOUCHE[0], s.BOUCHE[1], smooth((v - 0.1) / 0.35), maxw=330)
            lm = s._lab("SA MAIN DROITE", BLANC, 44)
            s._pose(im, lm, s.BOUCHEE[0] - 24 + dx, s.BOUCHEE[1] + 70 + dy, smooth(v / 0.35), maxw=300)
            ab = smooth((v - 0.6) / 0.4)                                           # le bandeau du bas
            if ab > 0.01:
                bd = s._cache.get("bandeau")
                if bd is None:
                    tx = s._lab("IL N'A PLUS LEVÉ SA DROITE À SA BOUCHE", BLANC, 44)   # une ligne : la bouchée
                    #                                                                    et son étiquette restent visibles
                    bd = Image.new("RGBA", (980, int(tx.height * min(1.0, 940 / tx.width)) + 6), (0, 0, 0, 0))
                    ImageDraw.Draw(bd).rounded_rectangle([0, 0, bd.width - 1, bd.height - 1], 24, fill=(14, 8, 12, 215))
                    k_ = min(1.0, 940 / tx.width)
                    if k_ < 1:
                        tx = tx.resize((int(tx.width * k_), int(tx.height * k_)), Image.LANCZOS)
                    bd.alpha_composite(tx, (int((bd.width - tx.width) / 2), int((bd.height - tx.height) / 2)))
                    s._cache["bandeau"] = bd
                _colle(im, bd, 510, 960 - bd.height / 2 - 12 + 16 * (1 - ab), ab)
        return s._rogne(im)

    # ============================================================ {maindroite avis|echange|coche}
    def _carte(s):
        """La carte des avis (fond crème, bord vert) ; la majorité en premier."""
        if "carte" in s._cache:
            return s._cache["carte"]
        W_ = 960
        ent = _txt_fit("MANGER DE LA GAUCHE SANS EXCUSE :", ENCRE, 11, 880, kmax=4, gras=True)
        cw = 430
        g1 = _txt_fit("DÉCONSEILLÉ", JAUNE_F, 11, cw, kmax=6, gras=True)
        g2 = [_txt_fit(t_, ENCRE, 11, cw, kmax=3) for t_ in ("SELON LA MAJORITÉ", "(AVIS RETENU", "DES 4 ÉCOLES)")]
        d1 = _txt_fit("PÉCHÉ", ORANGE_F, 11, cw, kmax=6, gras=True)
        d2 = [_txt_fit(t_, ENCRE, 11, cw, kmax=3) for t_ in ("SELON IBN AL-'ARABI,", "IBN HAJAR…")]
        colg = _pile([g1, Image.new("RGBA", (1, 6))] + g2, gap=0)
        cold = _pile([d1, Image.new("RGBA", (1, 6))] + d2, gap=0)
        v1 = _texte_px("SI TA DROITE NE PEUT PAS", BLANC, 11, k=3, pad=1)
        v2 = _texte_px("(BLESSURE, MALADIE…) :", BLANC, 11, k=3, pad=1)
        v3 = _txt_fit("AUCUN REPROCHE", BLANC, 11, 560, kmax=5, gras=True)
        vert = _pile([v1, v2, Image.new("RGBA", (1, 6)), v3], gap=0)
        h_col = max(colg.height, cold.height)
        hv = vert.height + 36
        H_ = 26 + ent.height + 22 + h_col + 26 + hv + 22
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 30, fill=(*OL, 255))
        d.rounded_rectangle([6, 6, W_ - 7, H_ - 7], 25, fill=(*VERT_F, 255))
        d.rounded_rectangle([14, 14, W_ - 15, H_ - 15], 19, fill=(*CREME, 255))
        y = 26
        im.alpha_composite(ent, (int((W_ - ent.width) / 2), y))
        y += ent.height + 22
        d.line([(W_ / 2, y + 6), (W_ / 2, y + h_col - 6)], fill=(200, 186, 160, 255), width=4)
        im.alpha_composite(colg, (int(W_ / 4 - colg.width / 2 + 6), y))
        im.alpha_composite(cold, (int(3 * W_ / 4 - cold.width / 2 - 6), y))
        y += h_col + 26
        s._y_vert = (y, y + hv)
        d.rounded_rectangle([26, y, W_ - 27, y + hv], 18, fill=(*VERT_F, 255))
        im.alpha_composite(vert, (int(26 + 330 - vert.width / 2), y + 18))
        s._cache["carte"] = im
        s._cache["carte_vert"] = (y, y + hv)
        return im

    def _bandeau_avis(s):
        """La carte réduite en bandeau (≈ 220 px) : toujours lisible jusqu'à la fin."""
        if "bavis" in s._cache:
            return s._cache["bavis"]
        W_ = 960
        l1 = _txt_fit("MANGER DE LA GAUCHE SANS EXCUSE :", ENCRE, 11, 880, kmax=3, gras=True)
        a = _texte_px("DÉCONSEILLÉ", JAUNE_F, 11, k=4, pad=1, gras=True)
        a2 = _texte_px(" (MAJORITÉ)", ENCRE, 11, k=3, pad=1)
        b = _texte_px("PÉCHÉ", ORANGE_F, 11, k=4, pad=1, gras=True)
        b2 = _texte_px(" (IBN HAJAR…)", ENCRE, 11, k=3, pad=1)
        sep = _texte_px("  OU  ", (140, 120, 100), 11, k=3, pad=1)
        parts = [a, a2, sep, b, b2]
        lw = sum(p_.width for p_ in parts)
        lh = max(p_.height for p_ in parts)
        l2 = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
        x = 0
        for p_ in parts:
            l2.alpha_composite(p_, (x, lh - p_.height - (0 if p_.height == lh else 4)))
            x += p_.width
        if l2.width > 900:
            l2 = l2.resize((900, int(l2.height * 900 / l2.width)), Image.LANCZOS)
        l3 = _txt_fit("SI TA DROITE NE PEUT PAS : AUCUN REPROCHE", BLANC, 11, 860, kmax=3, gras=True)
        H_ = 18 + l1.height + 6 + l2.height + 10 + l3.height + 22 + 14
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 26, fill=(*OL, 255))
        d.rounded_rectangle([6, 6, W_ - 7, H_ - 7], 21, fill=(*VERT_F, 255))
        d.rounded_rectangle([12, 12, W_ - 13, H_ - 13], 16, fill=(*CREME, 255))
        y = 18
        im.alpha_composite(l1, (int((W_ - l1.width) / 2), y))
        y += l1.height + 6
        im.alpha_composite(l2, (int((W_ - l2.width) / 2), y))
        y += l2.height + 10
        d.rounded_rectangle([24, y - 6, W_ - 25, y + l3.height + 8], 14, fill=(*VERT_F, 255))
        im.alpha_composite(l3, (int((W_ - l3.width) / 2), y + 1))
        s._cache["bavis"] = im
        return im

    def _platre(s):
        """La main droite de Petit (manche rouge) dans un plâtre blanc propre : aucune plaie, rien d'abîmé."""
        if "platre" in s._cache:
            return s._cache["platre"]
        p = _peau("PETIT")
        W, H = 30, 40
        c = Px(W, H, alpha=True)
        manche = c.mask_poly([(6, H + 1), (24, H + 1), (23, 30), (7, 30)])
        c.shape(manche, SWEAT[0], shade=SWEAT[1], light=SWEAT[2], band=2, olcol=OL)
        for j in range(4):                                                         # les doigts qui dépassent
            d_ = c.mask_rrect(8 + 4 * j, 3 + (j % 2), 12 + 4 * j, 12, 2)
            c.shape(d_, p["b"], shade=p["s"], light=p["h"], band=1, olcol=OL)
        platre = c.mask_rrect(6, 9, 24, 32, 4)
        c.shape(platre, (246, 246, 244), shade=(206, 206, 210), light=(255, 255, 255), band=2, olcol=OL)
        for y in (14, 20, 26):                                                     # les tours de bande
            c.fill(c.mask_rect(8, y, 22, y + 1), (222, 222, 226))
        s._cache["platre"] = c.img(6, rgba=True)
        return s._cache["platre"]

    def _image_avis(s, u):
        im = s._snack().copy()
        im = _assombrit(im, 0.25)
        te = s.t.get("echange")
        tco = s.t.get("coche")
        # la carte : pleine taille, puis (après « Tacos à droite… ») elle devient le bandeau du haut
        kr = smooth((u - te - 0.95) / 0.5) if te is not None else 0.0
        dy_m = s.DY_AVIS * (1 - kr)                                                # les mains remontent avec
        # les mains : tacos à gauche / téléphone à droite ; {echange} : les objets changent de main (0,8 s)
        kx = smooth((u - te) / 0.8) if te is not None else 0.0
        piv_d = (s.PIV_D[0] + 3 * math.sin(2 * math.pi * u / 3.1), s.PIV_D[1] + dy_m + 6 * math.sin(2 * math.pi * u / 2.4))
        pg0, sg0 = s._gauche_tacos(10.0, dy_m)                                     # (la gauche arrêtée à mi-chemin)
        pg0 = (pg0[0] - 30, pg0[1])
        sg0 = 0.98
        rm = smooth((u - te - 0.6) / 1.0) if te is not None else 0.0              # la droite monte le tacos vers toi
        piv_d2 = (piv_d[0] - 20 * rm, piv_d[1] - 50 * rm)
        sc_d = s.SC_D + 0.13 * rm
        if kx <= 0.0:
            s._pose_bras(im, s._bras("d", "tel", u), piv_d, s.SC_D)
            s._pose_bras(im, s._bras("g", "tacos", u), pg0, sg0)
        elif kx >= 1.0:
            s._pose_bras(im, s._bras("g", "tel", u), (pg0[0], pg0[1] + 8), 0.95)
            gx, gy = s._pose_bras(im, s._bras("d", "tacos", u, lueur=False), piv_d2, sc_d)
        else:
            av_old, av_new = 1 - smooth(kx / 0.35), smooth((kx - 0.65) / 0.35)
            gd = s._pose_bras(im, s._bras("d", None, u, avants=[("tel", av_old), ("tacos", av_new)], lueur=False),
                              piv_d, s.SC_D)
            gg = s._pose_bras(im, s._bras("g", None, u, avants=[("tacos", av_old), ("tel", av_new)], lueur=False),
                              pg0, sg0)
            tac, (tox, toy) = s._tacos()                                           # le tacos passe par-dessus,
            tel, (lox, loy) = s._tel(u)                                            # le téléphone par-dessous
            x_t, y_t = gg[0] + (gd[0] - gg[0]) * kx, gg[1] + (gd[1] - gg[1]) * kx - 120 * math.sin(math.pi * kx)
            x_p, y_p = gd[0] + (gg[0] - gd[0]) * kx, gd[1] + (gg[1] - gd[1]) * kx + 60 * math.sin(math.pi * kx)
            sc_ = 0.97
            tz = s._zoom(tel, sc_)
            im.alpha_composite(tz, (int(x_p - lox * sc_), int(y_p - loy * sc_)))
            tz = s._zoom(tac, sc_, "tacos")
            im.alpha_composite(tz, (int(x_t - tox * sc_), int(y_t - toy * sc_)))
        if te is not None:                                                         # « MAIN DROITE » en vert
            md = s._cache.get("md")
            if md is None:
                md = s._cache["md"] = s._lab("MAIN DROITE", (110, 230, 130), 50)
            cx_d = piv_d2[0]
            y_md = max(300, piv_d2[1] - (s.GH - s.G[1]) * K * sc_d - 170 * sc_d - 50)   # au-dessus du tacos, sous
            #                                                                            le bandeau du haut
            if tco is not None and u >= tco:                                       # {coche} : « ✓ MAIN DROITE »
                ec = smooth((u - tco) / 0.4)
                ck = s._cache.get("ck_petit")
                if ck is None:
                    ck = s._cache["ck_petit"] = _coche_img(0.42)
                lab = s._cache.get("md2")
                if lab is None:
                    lab = Image.new("RGBA", (ck.width + 8 + md.width, max(ck.height, md.height)), (0, 0, 0, 0))
                    lab.alpha_composite(ck, (0, int((lab.height - ck.height) / 2)))
                    lab.alpha_composite(md, (ck.width + 8, int((lab.height - md.height) / 2)))
                    s._cache["md2"] = lab
                s._pose(im, md, cx_d, y_md, kr * (1 - ec), maxw=440)
                s._pose(im, lab, cx_d - 20, y_md, ec, maxw=480)
                big = s._cache.get("ck_grand")
                if big is None:
                    big = s._cache["ck_grand"] = _coche_img(1.0)
                z = 1.1 - 0.1 * ec
                bz = s._zoom(big, z, "ck_grand")
                _colle(im, bz, piv_d2[0] + 20, piv_d2[1] - 200 * sc_d, ec)
            else:
                s._pose(im, md, cx_d, y_md, kr, maxw=440)
        # la carte des avis, puis le bandeau
        ca = s._carte()
        y_fin = 24 + ca.height / 2
        ec = smooth(u / 0.5)
        if kr < 0.999:
            cy = y_fin + (1 - ec) * 520
            a_c = min(1.0, ec * 1.4) * (1 - smooth(kr / 0.6))
            if kr > 0.001:
                z = 1 - 0.45 * kr
                caz = s._zoom(ca, z)
                _colle(im, caz, 510, cy - (y_fin - 130) * kr, a_c)
            else:
                _colle(im, ca, 510, cy, a_c)
                v0, v1 = s._cache["carte_vert"]                                    # le plâtre, « EXCUSE », la coche
                ep = smooth((u - 0.75) / 0.3)
                if ep > 0.01:
                    x0 = 510 - ca.width / 2
                    y0 = cy - ca.height / 2
                    pl = s._platre()
                    _colle(im, pl, x0 + 690, y0 + (v0 + v1) / 2 - 6 + 12 * (1 - ep), ep)
                    ex = s._cache.get("excuse")
                    if ex is None:
                        ex = s._cache["excuse"] = _texte_px("EXCUSE", (210, 255, 210), 11, k=3, pad=1, gras=True,
                                                            bord=(20, 70, 34))
                    _colle(im, ex, x0 + 852, y0 + v0 + 8 + ex.height / 2, ep)
                    ck = s._cache.get("ck_mini")
                    if ck is None:
                        ck = s._cache["ck_mini"] = _coche_img(0.6)
                    _colle(im, ck, x0 + 852, y0 + (v0 + v1) / 2 + 30, smooth((u - 0.95) / 0.3))
                ah = smooth((u - 1.1) / 0.3) * (1 - smooth((u - 2.2) / 0.5))       # « AUCUN REPROCHE » : un liseré
                if ah > 0.01:                                                      # clair autour du bandeau vert
                    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
                    x0 = 510 - ca.width / 2
                    y0 = cy - ca.height / 2
                    ImageDraw.Draw(lay).rounded_rectangle([x0 + 20, y0 + v0 - 6, x0 + ca.width - 21, y0 + v1 + 6], 22,
                                                          outline=(255, 240, 150, int(255 * ah)), width=6)
                    im.alpha_composite(lay)
        if kr > 0.001:
            bv = s._bandeau_avis()
            _colle(im, bv, 510, 14 + bv.height / 2 + 30 * (1 - kr), smooth((kr - 0.2) / 0.6))
        return s._rogne(im)


# ---------------------------------------------------------------- branchement (via explique_0811.py)
CLES = ("repas", "maindroite")


def _norm(m):
    return m.lower().replace("é", "e").replace("è", "e").replace("ê", "e")


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique_0811.ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""

    def dernier(mode):
        return next((it["el"] for it in reversed(schema._visibles(t + 0.01))
                     if isinstance(it["el"], Droite) and it["el"].mode == mode), None)

    def u_de(el):
        return t - next(it["t_in"] for it in schema.items if it["el"] is el)

    def etape(mode, nom):
        el = dernier(mode)
        if el is None:
            el = Droite(brut, mode)
            schema._ajoute(t, el)
        el.t[nom] = u_de(el)

    if k == "repas":
        schema._ajoute(t, Droite(brut, "repas", "PETIT"))
    elif k == "maindroite":
        if sous in ("", "stop"):
            etape("repas", "stop")
        elif sous in Droite.ETAPES_REPAS:
            etape("repas", sous)
        elif sous == "recit":
            schema._ajoute(t, Droite(brut, "recit"))
        elif sous in Droite.ETAPES_RECIT:
            etape("recit", sous)
        elif sous == "avis":
            schema._ajoute(t, Droite(brut, "avis"))
        elif sous in Droite.ETAPES_AVIS:
            etape("avis", sous)
        else:
            return False
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "repas":
        return t + 1.7
    if k == "maindroite":
        return t + dict(stop=0.8, chaytan=1.6, recit=1.6, refus=0.8, orgueil=1.0, plus=1.0, fleche=2.6, avis=2.2,
                        echange=1.6, coche=1.4).get(sous or "stop", 0.8)
    return None
