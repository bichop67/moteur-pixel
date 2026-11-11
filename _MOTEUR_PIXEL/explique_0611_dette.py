# DÉMONSTRATION EN IMAGE DU 07/11/2026 — Short ISL21 « Tu dois de l'argent ? Rends-le ! » (format consigne).
# Même principe que explique_0411b.py : le sens propre du hadith, montré en grand, avec des mouvements doux (jamais de
# secousse ni de flash). Le martyr n'est jamais dessiné : sa liste n'est que du texte et de la lumière.
#   {sms PETIT}        accroche, vue à ta place : TON téléphone dans ta main, au snack ; la conversation avec
#                      « KARIM » : sa bulle verte « TU ME RENDS MES 5 € ? » arrive, puis « ?? » ; au mur, le calendrier
#                      tourne ses pages : « 1 MOIS », « 2 MOIS », « 3 MOIS »
#   {dette}            la feuille « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : » (en petit) puis « MÊME LE MARTYR : » :
#                      5 lignes « PÉCHÉ » et « LA DETTE » (texte et lumière seulement : ni personnage, ni arme, ni
#                      drapeau, ni ange, ni main) ;
#                      {dette efface} les « PÉCHÉ » partent un à un dans une lumière dorée : « PARDONNÉS » ;
#                      {dette reste} « LA DETTE » reste, lueur rouge lente : « SAUF LA DETTE » (Mouslim 1886) et,
#                      dessous en petit, « = LE DROIT DES AUTRES » ;
#                      {dette injustice} la bulle de Petit « JE LUI RENDS DEMAIN… » reçoit le tampon à deux lignes
#                      « INJUSTICE // SI TU PEUX PAYER » (Boukhari 2287 · Mouslim 1564)
#   {carnet}           le carnet : « 5 € — À RENDRE LE 14/11 » s'écrit à la main (aucun nom) ; « QUAND VOUS
#                      CONTRACTEZ UNE DETTE À ÉCHÉANCE DÉTERMINÉE, METTEZ-LA PAR ÉCRIT » (Coran 2:282, extrait) ;
#                      « CONSEILLÉ SELON LA MAJORITÉ DES SAVANTS »
# Retouches du 07/11/2026 (relecture religieuse) : attribution au Prophète sur la feuille, « = LE DROIT DES AUTRES »,
# la condition DANS le tampon, le carnet sans nom et l'extrait du verset qui porte l'ordre d'écrire ; puis l'accent de
# « PROPHÈTE » décollé du rouleau, le stylo (plus droit) et le tampon (descente) qui ne sortent plus de l'image.
# Branché par explique_0611.py (import tardif dans explique.Schema._ordre et scenario._fin_anim).
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import objets
import pxv
from px import Px, TAHOMA
from pxv import smooth
from explique import _titre, _fade, _os, BLANC, JAUNE
from explique_0411 import OL, _peau, _buste, _grand
from explique_0411b import _Base, _translucide, ROUGE, OR_

MANUSCRITE = "C:/Windows/Fonts/segoeprb.ttf"      # Segoe Print gras, rendue en pixels : l'écriture à la main
ENCRE = (62, 42, 34)                              # encre brune du titre de la feuille
ENCRE_P = (98, 70, 52)                            # encre un peu plus claire : « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : »
GRIS_P = (76, 72, 84)                             # les lignes « PÉCHÉ » (gris foncé)
OR_ENCRE = (226, 156, 26)                         # un « PÉCHÉ » qui part dans la lumière
ROUGE_E = (190, 30, 40)                           # « LA DETTE » à l'encre rouge
STYLO = (30, 50, 138)                             # l'encre bleue du carnet
PAPIER = (244, 232, 200)
VERT_SMS = (58, 176, 92)
# le carnet (relecture du 07/11 : AUCUN nom ; l'extrait du verset qui porte l'ordre d'écrire)
MAIN_ECRITE = "5 € — À RENDRE LE 14/11"
TAILLE_MAIN = 16                                  # (Segoe Print ×3 : la ligne et le stylo tiennent dans l'image)
CITATION = ("« QUAND VOUS CONTRACTEZ UNE DETTE", "À ÉCHÉANCE DÉTERMINÉE,", "METTEZ-LA PAR ÉCRIT »")


# ---------------------------------------------------------------- petits outils
def _dilate(m, n=1):
    e = m.copy()
    for _ in range(n):
        e = e | np.roll(e, 1, 0) | np.roll(e, -1, 0) | np.roll(e, 1, 1) | np.roll(e, -1, 1)
    return e


def _texte_px(txt, col, size, k=6, puce=False, bord=None, halo=None, seul_halo=False, pad=4, font=TAHOMA,
              gras=False):
    """Texte pixel net (rendu sans lissage puis agrandi ×k) : l'encre sur la feuille, la page du calendrier, le
    carnet. puce = petit carré devant ; bord = liseré d'un pixel ; halo = lueur en 3 paliers nets autour des lettres
    (au-delà du liseré s'il y en a un ; seul_halo : la lueur seule) ; gras = trait épaissi d'un pixel. Marge de pad
    pixels du dessin autour ; le haut du texte (ascendante de la police) est à pad : deux textes de même taille ont la
    même ligne de base."""
    f = ImageFont.truetype(font, size)
    asc, desc = f.getmetrics()
    tw = int(math.ceil(f.getlength(txt))) if txt else 0
    x_t = pad + (7 if puce else 0)
    w, h = x_t + tw + pad + 2, pad + asc + desc + 1 + pad
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    d.fontmode = "1"
    if txt:
        d.text((x_t, pad), txt, font=f, fill=255, anchor="la")
    a = np.array(m) > 0
    if gras:
        a = a | np.roll(a, 1, 1)
    if puce:
        a[pad + asc - 6: pad + asc - 3, pad: pad + 3] = True
    out = np.zeros((h, w, 4), np.uint8)
    if halo is not None and seul_halo:                                              # la lueur seule (elle pulse à part)
        d1 = _dilate(_dilate(a, 1) if bord is not None else a, 1)
        d2 = _dilate(d1, 1)
        d3 = _dilate(d2, 1)
        out[d3] = (*halo, 46)
        out[d2] = (*halo, 100)
        out[d1] = (*halo, 170)
        out[_dilate(a, 1)] = (*halo, 170)
        return Image.fromarray(out, "RGBA").resize((w * k, h * k), Image.NEAREST)
    if bord is not None:
        out[_dilate(a, 1)] = (*bord, 255)
    out[a] = (*col, 255)
    return Image.fromarray(out, "RGBA").resize((w * k, h * k), Image.NEAREST)


def _lignes(lignes, col, size, serre=30):
    """Plusieurs lignes de la même couleur et de la même taille (style des étiquettes du moteur) ; serre = de combien
    chaque ligne remonte sur la précédente (pixels d'écran)."""
    ims = [_titre(l_, col, size) for l_ in lignes]
    W_ = max(i.width for i in ims)
    out = Image.new("RGBA", (W_, sum(i.height for i in ims) - serre * (len(ims) - 1)), (0, 0, 0, 0))
    y = 0
    for i in ims:
        out.alpha_composite(i, (int(W_ / 2 - i.width / 2), y))
        y += i.height - serre
    return out


def _lueur_px(rx, ry, col, k=6, niveaux=(48, 92, 140)):
    """Lueur en paliers nets (ellipses emboîtées, style pixel, sans flou) ; rx, ry en pixels du dessin."""
    W, H = int(2 * rx + 2), int(2 * ry + 2)
    c = Px(W, H, alpha=True)
    out = np.zeros((H, W, 4), np.uint8)
    for j, al in enumerate(niveaux):
        f_ = 1 - j / len(niveaux)
        out[c.mask_ell(W / 2, H / 2, rx * f_, ry * f_)] = (*col, al)
    return Image.fromarray(out, "RGBA").resize((W * k, H * k), Image.NEAREST)


_HALOS = {}


def _halo(w, h, col, flou):
    """Ombre douce (ellipse floutée) en cache ; à poser centrée avec _colle."""
    cle = (int(w), int(h), col, int(flou))
    if cle not in _HALOS:
        m = int(flou * 2.5)
        lay = Image.new("RGBA", (int(w) + 2 * m, int(h) + 2 * m), (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse([m, m, m + int(w), m + int(h)], fill=(*col, 255))
        _HALOS[cle] = lay.filter(ImageFilter.GaussianBlur(flou))
    return _HALOS[cle]


def _tourne_net(im, angle):
    """Rotation douce (degrés) en alpha prémultiplié : pas de liseré sombre sur les bords transparents."""
    return im.convert("RGBa").rotate(angle, resample=Image.BICUBIC, expand=True).convert("RGBA")


def _colle(im, sp, cx, cy, a=1.0):
    if a > 0.01:
        im.alpha_composite(_fade(sp, a), (int(cx - sp.width / 2), int(cy - sp.height / 2)))


def _etincelle(d, x, y, r, a, coeur=(255, 248, 200), bord=(232, 150, 30)):
    """Petite étoile pixel à 4 branches (bordée d'or foncé : on la voit aussi sur le papier clair)."""
    A = int(255 * a)
    if A <= 0:
        return
    for (w_, h_) in ((r, 3 * r), (3 * r, r)):
        d.rectangle([x - w_ - 3, y - h_ - 3, x + w_ + 3, y + h_ + 3], fill=(*bord, A))
    for (w_, h_) in ((r, 3 * r), (3 * r, r)):
        d.rectangle([x - w_, y - h_, x + w_, y + h_], fill=(*coeur, A))


# ---------------------------------------------------------------- {sms} {dette …} {carnet}
class Dette(_Base):
    """{sms PETIT} : accroche, vue à ta place : ton téléphone dans ta main, au snack ; « KARIM » réclame « TU ME RENDS
    MES 5 € ? » puis « ?? » ; le calendrier du mur tourne : 1, 2, 3 MOIS. {dette} : la feuille « LE PROPHÈTE (PAIX ET
    SALUT SUR LUI) : » / « MÊME LE MARTYR : » (5 « PÉCHÉ » + « LA DETTE ») ; {dette efface} les péchés partent dans une
    lumière dorée, « PARDONNÉS » ; {dette reste} « LA DETTE » reste, « SAUF LA DETTE » (Mouslim 1886), « = LE DROIT DES
    AUTRES » ; {dette injustice} le tampon « INJUSTICE // SI TU PEUX PAYER » sur « JE LUI RENDS DEMAIN… » (Boukhari
    2287). {carnet} : « 5 € — À RENDRE LE 14/11 » s'écrit, « QUAND VOUS CONTRACTEZ UNE DETTE À ÉCHÉANCE DÉTERMINÉE,
    METTEZ-LA PAR ÉCRIT » (Coran 2:282, extrait), conseillé selon la majorité des savants."""
    ETAPES = ("efface", "reste", "injustice")
    # l'accroche (pixels du dessin, ×6)
    TEL = (34, 8)                       # coin haut-gauche du téléphone
    TW, TH = 80, 150                    # le téléphone (le bas sort du cadre : il est dans ta main)
    PILE = 96                           # bas de la pile de bulles (dans le téléphone)
    KC = 15                             # le calendrier : l'icône agrandie ×15
    CAL = (760, 30)                     # coin haut-gauche du calendrier (pixels d'écran)
    T_PAGES = (0.3, 0.8, 1.3)           # « 1 MOIS », « 2 MOIS », « 3 MOIS »
    T_BULLE2 = 0.8                      # « ?? »
    # la feuille (pixels du dessin, ×6)
    Y_PRO = (84, 133)                   # haut de « LE PROPHÈTE » / « (PAIX ET SALUT SUR LUI) : » (en petit, ÉCRAN ;
    #                                     l'accent du È ne touche pas le rouleau)
    Y_TITRE = 33                        # haut de « MÊME LE MARTYR : »
    Y_LIG = (53, 67, 81, 95, 109)       # haut des 5 lignes « PÉCHÉ »
    Y_DETTE = 124                       # haut de la ligne « LA DETTE »
    X_LIG = 26                          # la puce de chaque ligne
    PAD = 4                             # marge des textes pixel (pixels du dessin)
    DT_EFF = 0.22                       # écart entre deux lignes qui partent
    # les étiquettes de la feuille (pixels d'écran) : « PARDONNÉS », « SAUF LA DETTE », « = LE DROIT DES AUTRES »
    Y_PARD, Y_SAUF, Y_DROIT = 385, 515, 600
    # le tampon et le carnet
    T_TAMPON = 0.85                     # le tampon touche la bulle (après {dette injustice})
    T_ECRIT, D_ECRIT = 0.25, 0.7        # la ligne du carnet s'écrit (pendant « mais on l'écrit »)
    T_CITE = 0.9                        # l'extrait du verset (puis la source à +0.3, la mention à +0.6)
    Y_BASE = 38                         # la ligne bleue où l'on écrit (pixels du dessin du carnet)
    Y_CITE, Y_CORAN, Y_MAJ = 512, 690, 836   # centres de l'extrait, de la source et de la mention (écran)

    def __init__(s, cmd, mode="liste", who="PETIT"):
        super().__init__(cmd)
        s.mode = mode
        s.who = who if who in ("PETIT", "GRAND") else "PETIT"
        s.negatif = mode == "sms"

    def sons_el(s):
        if s.mode == "sms":
            return [(-0.2, "dv_notifications", 0.03, None), (s.T_PAGES[2], "dv_clic", 0.03, None)]
        if s.mode == "carnet":
            return [(s.T_CITE, "sa_ting", 0.03, None)]
        out = []
        if "efface" in s.t:
            out.append((s.t["efface"], "sa_scintillement", 0.045, None))
        if "injustice" in s.t:
            out.append((s.t["injustice"] + s.T_TAMPON, "imp_tampon", 0.03, None))
        return out

    def image(s, u):
        if s.mode == "sms":
            return s._image_sms(u)
        if s.mode == "carnet":
            return s._image_carnet(u)
        return s._image_liste(u)

    def _zoom(s, im, k):
        """Agrandissement doux (en cache, au centième) d'une image."""
        k = round(k, 2)
        cle = ("z", id(im), k)
        if cle not in s._cache:
            s._cache[cle] = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        return s._cache[cle]

    # ============================================================ l'accroche : le téléphone
    def _decor_sms(s):
        """Le snack, derrière ton téléphone : mur carrelé, tableau du menu, table, soda et frites (tons assourdis)."""
        if "dsms" in s._cache:
            return s._cache["dsms"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        mur = c.mask_rect(0, 0, W, 106) & tout_
        c.vgrad(mur, 0, 106, (92, 54, 56), (148, 92, 74), steps=5)
        for j, y in enumerate(range(0, 106, 9)):                                   # les carreaux (joints plus sombres)
            c.tint(c.mask_rect(0, y, W, y + 1) & mur, (30, 14, 18), 0.35)
            dec = 0 if j % 2 == 0 else 7
            for x in range(-dec, W, 14):
                c.tint(c.mask_rect(x, y, x + 1, y + 9) & mur, (30, 14, 18), 0.35)
                c.tint(c.mask_rect(x + 2, y + 2, x + 5, y + 3) & mur, (255, 220, 190), 0.10)
        frise = c.mask_rect(0, 70, W, 74) & tout_
        c.shape(frise, (196, 146, 60), shade=(150, 106, 40), light=(226, 182, 90), sdir="bottom", band=1, olcol=OL)
        tab = c.mask_rect(3, 7, 31, 50)                                            # le tableau du menu (images, pas de mots)
        c.shape(tab, (126, 84, 52), shade=(96, 62, 38), light=(150, 106, 70), band=1, olcol=OL)
        c.fill(c.mask_rect(5, 9, 29, 48), (36, 36, 44))
        c.fill(c.mask_ell(11, 15, 4, 2.2), (226, 154, 70))                         # un burger
        c.fill(c.mask_rect(7, 16, 15, 18), (110, 62, 42))
        c.fill(c.mask_rect(7, 15, 15, 16), (96, 176, 74))
        c.fill(c.mask_rect(7, 18, 15, 20), (226, 154, 70))
        c.fill(c.mask_poly([(19, 13), (27, 13), (26, 20), (20, 20)]), (210, 50, 50))   # des frites
        for x in (20, 22, 24, 26):
            c.fill(c.mask_rect(x, 10 + (x % 3), x + 1, 14), (250, 210, 80))
        for j, y in enumerate((25, 30, 35, 40, 45)):                               # les prix (traits)
            c.fill(c.mask_rect(7, y, 7 + (12, 9, 14, 10, 13)[j], y + 1), (196, 196, 206))
            c.fill(c.mask_rect(24, y, 27, y + 1), (250, 200, 80))
        table = c.mask_rect(0, 104, W, H) & tout_
        c.fill(table, (112, 74, 52))
        c.dither(table, (98, 64, 46), 0.25)
        c.fill(c.mask_rect(0, 104, W, 106) & tout_, (150, 104, 72))
        c.fill(c.mask_rect(0, 106, W, 107) & tout_, (78, 50, 38))
        gob = c.mask_poly([(6, 92), (24, 92), (22, 124), (8, 124)])                # le soda (paille, couvercle)
        c.shape(gob, (200, 52, 56), shade=(150, 36, 44), light=(232, 96, 90), band=2, olcol=OL)
        c.fill(c.mask_rect(8, 104, 23, 109) & gob, (236, 236, 240))
        c.fill(c.mask_rect(5, 89, 25, 93), (236, 236, 242))
        c.outline(c.mask_rect(5, 89, 25, 93), OL)
        paille = c.mask_poly([(16, 89), (18, 89), (22, 74), (20, 74)])
        c.fill(paille, (250, 250, 250))
        c.outline(paille, OL)
        frites = c.mask_poly([(128, 112), (150, 112), (147, 134), (131, 134)])     # le cornet de frites
        for x in range(130, 149, 3):
            fr = c.mask_rect(x, 101 + (x * 7) % 6, x + 2, 114)
            c.shape(fr, (250, 206, 80), shade=(214, 160, 50), band=1, olcol=OL)
        c.shape(frites, (210, 50, 50), shade=(160, 34, 40), light=(236, 96, 90), band=2, olcol=OL)
        c.fill(c.mask_rect(135, 120, 143, 126) & frites, (250, 210, 80))
        im = c.img(s.K, rgba=True)
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))                              # pénombre douce sur les bords
        ImageDraw.Draw(lay).rectangle([0, 0, im.width, im.height], fill=(20, 10, 20, 70))
        trou = Image.new("L", im.size, 0)
        ImageDraw.Draw(trou).ellipse([150, 60, 870, 980], fill=255)
        trou = trou.filter(ImageFilter.GaussianBlur(90))
        a = np.array(lay)
        a[..., 3] = (a[..., 3].astype(float) * (1 - np.array(trou) / 255.0)).astype(np.uint8)
        a[..., 3] = np.minimum(a[..., 3], np.array(im)[..., 3])
        im.alpha_composite(Image.fromarray(a, "RGBA"))
        s._cache["dsms"] = im
        return im

    def _tel_sms(s):
        """Le téléphone : la conversation avec KARIM (en-tête, papier peint, barre de saisie) ; bulles posées à part."""
        if "tel" in s._cache:
            return s._cache["tel"]
        W, H = s.TW, s.TH
        c = Px(W, H, alpha=True)
        corps = c.mask_rrect(0, 0, W, H + 10, 10)
        c.shape(corps, (42, 42, 54), shade=(24, 24, 32), light=(100, 100, 118), band=2, olcol=OL)
        ecran = c.mask_rrect(4, 5, W - 4, H + 6, 7)
        c.fill(ecran, (234, 226, 210))
        rng = np.random.default_rng(2)
        for _ in range(26):                                                         # le papier peint (motifs pâles)
            x, y = int(rng.integers(7, W - 9)), int(rng.integers(36, H - 4))
            c.fill(c.mask_ell(x, y, 1.6, 1.6) & ecran, (222, 212, 194))
            c.px(x + 4, y + 3, (222, 212, 194))
        haut = ecran & c.mask_rect(0, 0, W, 31)
        c.fill(haut, (30, 92, 82))
        c.fill(c.mask_rect(4, 31, W - 4, 32), (22, 70, 62))
        c.fill(c.mask_rrect(31, 7, 49, 11, 2), (14, 14, 20))                       # l'encoche
        for x in (9, 12, 16, 19):                                                   # l'heure (blocs)
            c.fill(c.mask_rect(x, 7, x + 2, 11), (226, 240, 234))
        c.px(14, 8, (226, 240, 234))
        c.px(14, 10, (226, 240, 234))
        c.fill(c.mask_rect(64, 7, 71, 11), (226, 240, 234))                        # la batterie
        c.fill(c.mask_rect(71, 8, 72, 10), (226, 240, 234))
        c.fill(c.mask_rect(65, 8, 68, 10), (30, 92, 82))
        for (x0, y0, x1, y1) in ((10, 17, 7, 20), (7, 20, 10, 23)):                # « < » retour
            c.line(x0, y0, x1, y1, (226, 240, 234))
            c.line(x0 + 1, y0, x1 + 1, y1, (226, 240, 234))
        av = c.mask_ell(20.5, 21.5, 6.5, 6.5)                                      # l'avatar (rond neutre)
        c.fill(av, (238, 150, 72))
        c.fill(c.mask_ell(20.5, 19.5, 2.6, 2.6) & av, (255, 232, 206))
        c.fill(c.mask_ell(20.5, 27, 5, 3.4) & av, (255, 232, 206))
        c.outline(av, (18, 58, 52))
        c.text((30, 14), "KARIM", (255, 255, 255), size=12, font=TAHOMA)
        saisie = c.mask_rect(4, 112, W - 4, H) & ecran                             # la barre de saisie
        c.fill(saisie, (222, 214, 198))
        c.fill(c.mask_rrect(7, 116, 62, 127, 4), (255, 255, 255))
        c.outline(c.mask_rrect(7, 116, 62, 127, 4), (200, 192, 176))
        for x in range(12, 40, 6):                                                  # (rien d'écrit : des points pâles)
            c.px(x, 121, (214, 210, 204))
        micro = c.mask_ell(69.5, 121.5, 5.5, 5.5)
        c.fill(micro, (40, 168, 92))
        c.fill(c.mask_rrect(68, 117, 71, 123, 1), (255, 255, 255))
        c.fill(c.mask_rect(69, 124, 70, 126), (255, 255, 255))
        s._cache["tel"] = c.img(s.K, rgba=True)
        return s._cache["tel"]

    def _bulle_sms(s, lignes, size, fond, ombre, clair):
        """Bulle de message (dessin pixel) avec sa petite pointe en bas à gauche ; texte blanc."""
        cle = ("bsms", tuple(lignes), size, fond)
        if cle in s._cache:
            return s._cache[cle]
        K = s.K
        tx = pxv.big_title([(l_, BLANC) for l_ in lignes], size=size)
        bw = int(math.ceil((tx.width - 18) / K))
        bh = int(math.ceil((tx.height - 14) / K))
        c = Px(bw + 2, bh + 4, alpha=True)
        corps = c.mask_rrect(2, 0, bw + 2, bh, 4)
        pointe = c.mask_poly([(2, bh - 6), (8, bh - 1), (0, bh + 3)])
        c.shape(corps | pointe, fond, shade=ombre, light=clair, band=1, olcol=OL)
        b = c.img(K, rgba=True)
        b.alpha_composite(tx, (int(2 * K + (bw * K - tx.width) / 2 + 2), int((bh * K - tx.height) / 2 + 3)))
        s._cache[cle] = b
        return b

    def _main(s):
        """Ta main (vue à ta place) : les doigts tiennent le bord gauche, le pouce penché se pose sur le bord droit,
        la paume et la manche sortent par le bas (sweat rouge de Petit, qamis blanc de Grand)."""
        cle = ("main", s.who)
        if cle in s._cache:
            return s._cache[cle]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        p = _peau(s.who)
        b, s_, h, dk = p["b"], p["s"], p["h"], p["d"]
        X0, Y0 = s.TEL
        X1 = X0 + s.TW
        if s.who == "GRAND":
            man = ((232, 230, 220), (192, 190, 180), (250, 250, 246))
        else:
            man = ((200, 50, 50), (150, 34, 40), (232, 92, 84))
        manche = c.mask_poly([(X1 + 4, H + 2), (X1 + 9, 140), (X1 + 30, 133), (W + 2, 131), (W + 2, H + 2)])
        c.shape(manche, man[0], shade=man[1], light=man[2], band=2, olcol=OL)
        for j in range(5):                                                          # le bord côtelé du poignet
            x = X1 + 10 + 6 * j
            c.fill(c.mask_poly([(x, 139 - j * 1.6), (x + 2, 138.5 - j * 1.6), (x + 3, H), (x + 1, H)]) & manche, man[1])
        paume = c.mask_ell(X1 + 1, 151, 13, 11)                                     # la paume (en bas, hors du téléphone)
        c.shape(paume, b, shade=s_, light=h, band=1, olcol=OL)
        pouce = _os(c, X1 - 1, 146, X1 - 13, 121, 12)                               # le pouce, penché vers l'écran
        c.shape(pouce, b, shade=s_, light=h, band=1, olcol=OL)
        ongle = c.mask_poly([(X1 - 17, 121), (X1 - 13, 117), (X1 - 9, 119), (X1 - 12, 125)]) & pouce
        c.fill(ongle, (246, 216, 198))
        c.fill(c.mask_rect(X1 - 15, 120, X1 - 13, 121) & ongle, (255, 240, 230))
        c.fill(c.mask_poly([(X1 - 9, 134), (X1 - 3, 132), (X1 - 3, 133), (X1 - 9, 135)]) & pouce, s_)   # le pli
        for j, y in enumerate((92, 100, 108, 116)):                                 # les doigts, bord gauche
            d_ = c.mask_rrect(X0 - 6 + (j % 2), y, X0 + 4, y + 9, 3)
            c.shape(d_, b, shade=s_, light=h, band=1, olcol=OL)
            c.fill(c.mask_rect(X0 - 4 + (j % 2), y + 7, X0 + 1, y + 8) & d_, s_)
        bord = c.mask_poly([(X0 - 6, 124), (X0 + 2, 124), (X0 + 4, H + 2), (X0 - 10, H + 2)])
        c.shape(bord, s_, shade=dk, light=b, band=1, olcol=OL)
        im = c.img(s.K, rgba=True)
        bb = im.getbbox()
        s._cache[cle] = (im.crop(bb), (bb[0], bb[1]))
        return s._cache[cle]

    def _cal(s):
        if "cal" not in s._cache:
            s._cache["cal"] = objets.icone("calendrier").img(s.KC)
        return s._cache["cal"]

    def _page(s, n):
        """La page du calendrier (zone x 1..14, y 6..14 de l'icône) : celle de l'icône (n = 0), vierge (n = -1) ou
        « n MOIS »."""
        cle = ("page", n)
        if cle not in s._cache:
            k = s.KC
            pg = s._cal().crop((1 * k, 6 * k, 15 * k, 15 * k))
            if n:
                pg = pg.copy()
                ImageDraw.Draw(pg).rectangle([1 * k, 0, 13 * k - 1, 8 * k - 1], fill=(248, 248, 250, 255))
            if n > 0:
                num = _texte_px(str(n), (40, 40, 54), 17, k=4, pad=0)
                mois = _texte_px("MOIS", (204, 44, 52), 11, k=4, pad=0)
                cx = 7 * k
                pg.alpha_composite(num, (int(cx - num.width / 2), -14))
                pg.alpha_composite(mois, (int(cx - mois.width / 2), 8 * k - mois.height + 2))
            s._cache[cle] = pg
        return s._cache[cle]

    def _calendrier(s, im, u):
        """Le calendrier du mur : la page arrachée tombe doucement en s'effaçant, le nouveau mois apparaît dessous."""
        k = s.KC
        x, y = s.CAL
        im.alpha_composite(s._cal(), (x, y))
        cur = None
        for i, tp in enumerate(s.T_PAGES):
            f = (u - tp + 0.35) / 0.5                                               # le nouveau mois est lu à tp
            if f > 0:
                cur = (i, min(1.0, f))
        if cur is None:
            return
        i, f = cur
        px_, py_ = x + 1 * k, y + 6 * k
        neuf = s._page(i + 1)
        an = smooth((f - 0.25) / 0.5)
        if an < 1:
            im.alpha_composite(s._page(-1), (px_, py_))
        if an > 0:
            im.alpha_composite(_fade(neuf, an), (px_, py_))
        av = 1 - smooth((f - 0.12) / 0.5)                                           # l'ancienne page tombe, puis s'efface
        if av > 0.01:
            vieux = s._page(i)
            g = smooth(f / 0.75)
            v2 = _tourne_net(vieux, -8 * g) if g > 0.02 else vieux
            im.alpha_composite(_fade(v2, av), (int(px_ + 16 * g - (v2.width - vieux.width) / 2),
                                               int(py_ + 90 * g - (v2.height - vieux.height) / 2)))

    def _image_sms(s, u):
        K = s.K
        im = s._decor_sms().copy()
        dx = 2.0 * math.sin(2 * math.pi * u / 3.4)                                 # le téléphone respire
        dy = 5.0 * math.sin(2 * math.pi * u / 2.6)
        tx, ty = s.TEL[0] * K + dx, s.TEL[1] * K + dy
        tel = s._tel_sms()
        _colle(im, _halo(tel.width - 40, 120, (10, 4, 10), 30), tx + tel.width / 2 + 30, 150 * K - 10, 0.6)
        im.alpha_composite(tel, (int(tx), int(ty)))
        # les bulles de Karim : la 1re arrive (u -0.3 → 0.1), « ?? » la pousse vers le haut (u ≈ 0.8)
        b1 = s._bulle_sms(("TU ME RENDS", "MES 5 € ?"), 52, VERT_SMS, (40, 136, 70), (110, 210, 130))
        b2 = s._bulle_sms(("??",), 58, VERT_SMS, (40, 136, 70), (110, 210, 130))
        e1 = smooth((u + 0.3) / 0.4)
        e2 = smooth((u - s.T_BULLE2 + 0.15) / 0.35)
        x_b = tx + 5 * K
        bas = ty + s.PILE * K
        y1 = bas - b1.height - e2 * (b2.height + 2 * K)
        if e1 > 0.01:
            b1_ = b1 if e1 > 0.999 else s._zoom(b1, 0.82 + 0.18 * e1)              # elle grossit depuis sa pointe
            im.alpha_composite(_fade(b1_, e1), (int(x_b), int(y1 + b1.height - b1_.height + 40 * (1 - e1))))
        if e2 > 0.01:
            b2_ = b2 if e2 > 0.999 else s._zoom(b2, 0.82 + 0.18 * e2)
            im.alpha_composite(_fade(b2_, e2), (int(x_b), int(bas - b2_.height + 30 * (1 - e2))))
        main, (mx, my) = s._main()
        im.alpha_composite(main, (int(mx + dx), int(my + dy)))
        s._calendrier(im, u)
        return im

    # ============================================================ {dette} : la liste du martyr
    def _feuille(s):
        """Le parchemin clair (deux rouleaux) : en petit « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : » (deux lignes), puis le
        titre « MÊME LE MARTYR : » ; les lignes sont posées à part."""
        if "feuille" in s._cache:
            return s._cache["feuille"]
        W, H = 170, 160
        c = Px(W, H, alpha=True)
        X0, X1 = 18, 152
        feuille = c.mask_rect(X0, 7, X1, 152)
        c.fill(feuille, PAPIER)
        c.dither(feuille, (234, 218, 182), 0.16)
        c.edge(feuille, (226, 206, 166), "right", 2)
        c.edge(feuille, (252, 244, 222), "left", 1)
        c.outline(feuille, OL)
        for y in [y_ + 13 for y_ in s.Y_LIG] + [s.Y_DETTE + 14]:                    # lignes réglées, discrètes
            c.fill(c.mask_rect(X0 + 6, y, X1 - 6, y + 1), (228, 210, 172))
        for (y0, y1) in ((1, 12), (146, 158)):                                      # les deux rouleaux
            r = c.mask_rrect(X0 - 7, y0, X1 + 7, y1, 5)
            c.shape(r, (216, 188, 138), shade=(172, 142, 98), light=(238, 218, 176), sdir="bottom", band=3, ldir="top",
                    lband=2, olcol=OL)
            for xb in (X0 - 11, X1 + 5):
                bout = c.mask_rrect(xb, y0 + 2, xb + 6, y1 - 2, 2)
                c.shape(bout, (150, 98, 60), shade=(112, 70, 42), light=(184, 130, 84), band=1, olcol=OL)
        y = s.Y_TITRE
        c.text((85, y), "MÊME LE MARTYR :", ENCRE, size=12, font=TAHOMA, anchor="ma")
        c.fill(c.mask_rect(36, y + 15, 134, y + 16), (150, 116, 80))
        c.fill(c.mask_rect(44, y + 17, 126, y + 18), (190, 160, 118))
        im = c.img(s.K, rgba=True)
        for y, txt in zip(s.Y_PRO, ("LE PROPHÈTE", "(PAIX ET SALUT SUR LUI) :")):    # qui parle, en petit : la même
            l_ = _texte_px(txt, ENCRE_P, 12, k=4, pad=0)                            # police, en pixels plus fins (×4)
            im.alpha_composite(l_, (int(85 * s.K - l_.width / 2), y))
        s._cache["feuille"] = im
        return s._cache["feuille"]

    def _txt(s, nom, *a, **kw):
        cle = ("txt", nom)
        if cle not in s._cache:
            s._cache[cle] = _texte_px(*a, **kw)
        return s._cache[cle]

    def _seuils(s, i, w, h):
        """Seuils de dissolution d'une ligne (un par pixel du dessin) : le mot se défait pixel par pixel."""
        cle = ("seuil", i)
        if cle not in s._cache:
            rng = np.random.default_rng(60 + i)
            K = s.K
            thr = rng.random((h // K + 1, w // K + 1))
            thr = 0.75 * thr + 0.25 * np.linspace(0, 1, thr.shape[1])[None, :]     # un peu de gauche à droite
            s._cache[cle] = np.kron(thr, np.ones((K, K)))[:h, :w]
        return s._cache[cle]

    def _liste(s, u):
        K = s.K
        P = s.PAD * K
        im = s._feuille().copy()
        te = s.t.get("efface", s.t.get("reste"))
        tr = s.t.get("reste")
        gris = s._txt("peche", "PÉCHÉ", GRIS_P, 11, puce=True, pad=s.PAD)
        dore = s._txt("peche_or", "PÉCHÉ", OR_ENCRE, 11, puce=True, bord=(255, 240, 168), pad=s.PAD)
        lueur = s._cache.get("lueur")
        if lueur is None:
            lueur = s._cache["lueur"] = _lueur_px(31, 9, (255, 222, 110))
        etincelles = []
        for i, y in enumerate(s.Y_LIG):                                             # les 5 « PÉCHÉ »
            x0, y0 = s.X_LIG * K - P, y * K - P
            if te is None or u < te + s.DT_EFF * i:
                im.alpha_composite(gris, (x0, y0))
                continue
            v = u - te - s.DT_EFF * i
            cx, cy = x0 + gris.width / 2, y0 + gris.height / 2
            gl = smooth(v / 0.12) * (1 - smooth((v - 0.3) / 0.45))                  # la lumière dorée, en paliers
            _colle(im, lueur, cx, cy - 6, gl)
            dy = -12 * smooth(v / 0.55)
            ag = 1 - smooth(v / 0.12)                                               # le gris devient or…
            if ag > 0.01:
                im.alpha_composite(_fade(gris, ag), (x0, int(y0 + dy)))
            p = smooth((v - 0.1) / 0.45)                                            # … puis se défait pixel par pixel
            if p < 1:
                a = np.array(dore)
                a[..., 3] = np.where(s._seuils(i, dore.width, dore.height) >= p, a[..., 3], 0).astype(np.uint8)
                dor_ = Image.fromarray(a, "RGBA")
                im.alpha_composite(_fade(dor_, 1 - ag), (x0, int(y0 + dy)))
            rng = np.random.default_rng(40 + i)                                     # petites étincelles qui montent
            fin_e = 1 - s._e("reste", u, 0.3) if "efface" in s.t else 1.0          # (elles laissent la place à « reste »)
            for j in range(5):
                vv = v - 0.05 * j
                if 0 <= vv < 0.75:
                    ex = x0 + P + 30 + float(rng.uniform(0, gris.width - 2 * P - 40)) + 8 * math.sin(vv * 7 + j)
                    ey = cy + float(rng.uniform(-10, 10)) - 95 * smooth(vv / 0.75)
                    ea = smooth(vv / 0.1) * (1 - smooth((vv - 0.35) / 0.4)) * fin_e
                    etincelles.append((ex, ey, 4 if j % 2 else 5, ea))
        if etincelles:
            _translucide(im, lambda d: [_etincelle(d, x, y, r, a) for (x, y, r, a) in etincelles])
        if te is not None:                                                          # « PARDONNÉS »
            s._pose(im, s._lab("PARDONNÉS", OR_, 56), 700, s.Y_PARD, s._e("efface" if "efface" in s.t else "reste",
                                                                         u, 0.35, dec=0.3), maxw=440)
        # « LA DETTE » : elle reste ; {dette reste} elle glisse au milieu, grossit (×4/3), lueur rouge lente
        lg6 = s._txt("dette6", "LA DETTE", ROUGE_E, 12, pad=s.PAD)
        er = s._e("reste", u, 0.7)
        x_g = (s.X_LIG + 7) * K - P + lg6.width / 2                                 # centre au départ (aligné à gauche)
        cx = x_g + (510 - x_g) * er
        cy = s.Y_DETTE * K - P + lg6.height / 2 - 18 * er
        pu = s._txt("puce", "", ROUGE_E, 12, puce=True, pad=s.PAD)
        im.alpha_composite(_fade(pu, 1 - er), (s.X_LIG * K - P, s.Y_DETTE * K - P))
        if er <= 0:
            im.alpha_composite(lg6, (int(cx - lg6.width / 2), int(cy - lg6.height / 2)))
        else:
            v = u - tr
            pulse = 0.5 + 0.5 * math.sin(2 * math.pi * v / 1.6 - math.pi / 2)        # lente (1,6 s), douce
            cerne, lueur_r = (92, 8, 20), (240, 52, 44)
            if er >= 0.999:                                                         # au bout : le dessin net ×8
                txt = s._txt("dette8c", "LA DETTE", ROUGE_E, 12, k=8, pad=s.PAD, bord=cerne)
                hal = s._txt("halo8", "LA DETTE", ROUGE_E, 12, k=8, pad=s.PAD, bord=cerne, halo=lueur_r,
                             seul_halo=True)
            else:                                                                   # pendant qu'elle grossit (×6 → ×8)
                kz = 1 + er / 3
                txt = s._zoom(s._txt("dette6c", "LA DETTE", ROUGE_E, 12, pad=s.PAD, bord=cerne), kz)
                hal = s._zoom(s._txt("halo6", "LA DETTE", ROUGE_E, 12, pad=s.PAD, bord=cerne, halo=lueur_r,
                                     seul_halo=True), kz)
                if er < 0.5:
                    im.alpha_composite(_fade(s._zoom(lg6, kz), 1 - 2 * er), (int(cx - txt.width / 2),
                                                                              int(cy - txt.height / 2)))
            _colle(im, _halo(520, 120, (240, 60, 50), 30), cx, cy, er * (0.18 + 0.17 * pulse))
            _colle(im, hal, cx, cy, er * (0.5 + 0.5 * pulse))
            im.alpha_composite(_fade(txt, min(1.0, 2 * er)), (int(cx - txt.width / 2), int(cy - txt.height / 2)))
        if tr is not None:                                                          # « SAUF LA DETTE », puis ce qu'elle est
            s._pose(im, s._lab("SAUF LA DETTE", ROUGE, 56), 510, s.Y_SAUF, s._e("reste", u, 0.35, dec=0.2), maxw=600)
            e_d = s._e("reste", u, 0.4, dec=0.5)
            s._pose(im, s._lab("= LE DROIT DES AUTRES", BLANC, 44), 510, s.Y_DROIT + 14 * (1 - e_d), e_d, maxw=700)
        return im

    # ---- {dette injustice} : la bulle de Petit et le tampon
    def _bulle_grise(s):
        if "bg" in s._cache:
            return s._cache["bg"]
        K = s.K
        tx = pxv.big_title([("JE LUI RENDS", BLANC), ("DEMAIN…", BLANC)], size=54)
        bw = int(math.ceil((tx.width - 10) / K))
        bh = int(math.ceil((tx.height - 6) / K))
        c = Px(bw + 4, bh + 4, alpha=True)
        corps = c.mask_rrect(4, 0, bw + 4, bh, 5)
        pointe = c.mask_poly([(4, bh - 9), (10, bh - 2), (0, bh + 3)])
        c.shape(corps | pointe, (128, 132, 148), shade=(96, 100, 116), light=(164, 168, 184), band=1, olcol=OL)
        b = c.img(K, rgba=True)
        b.alpha_composite(tx, (int(4 * K + (bw * K - tx.width) / 2 + 2), int((bh * K - tx.height) / 2 + 3)))
        s._cache["bg"] = b
        return b

    def _tampon(s):
        """Le tampon rouge à deux lignes « INJUSTICE » / « SI TU PEUX PAYER » (la condition se lit avec le mot ; cadre
        double, filet entre les lignes, encre un peu inégale), penché, bordé de clair."""
        if "tampon" in s._cache:
            return s._cache["tampon"]
        f1, f2 = ImageFont.truetype(TAHOMA, 17), ImageFont.truetype(TAHOMA, 12)
        W, H = int(max(f1.getlength("INJUSTICE"), f2.getlength("SI TU PEUX PAYER"))) + 20, 45
        c = Px(W, H, alpha=True)
        rouge = (212, 34, 44)
        cadre = c.mask_rrect(0, 0, W, H, 3) & ~c.mask_rrect(2, 2, W - 2, H - 2, 2)
        cadre |= c.mask_rrect(4, 4, W - 4, H - 4, 1) & ~c.mask_rrect(5, 5, W - 5, H - 5, 1)
        cadre |= c.mask_rect(10, 24, W - 10, 25)                                    # le filet entre les deux lignes
        c.fill(cadre, rouge)
        c.text((W / 2, 21), "INJUSTICE", rouge, size=17, font=TAHOMA, anchor="ms")    # (ligne de base : 3 pixels
        c.text((W / 2, 37), "SI TU PEUX PAYER", rouge, size=12, font=TAHOMA, anchor="ms")  # libres autour de chaque ligne)
        encre = c.al.copy()
        rng = np.random.default_rng(7)
        c.fill(encre & (rng.random((H, W)) < 0.10), (176, 22, 34))                  # l'encre du tampon, inégale
        c.outline(encre, (255, 244, 238))                                          # liseré clair : lisible sur tout fond
        s._cache["tampon"] = _tourne_net(c.img(5, rgba=True), 8)
        return s._cache["tampon"]

    def _injustice(s, im, v):
        """v = temps depuis {dette injustice}."""
        ap = smooth((v - 0.2) / 0.35)
        if ap <= 0.01:
            return
        gene = smooth((v - s.T_TAMPON - 0.1) / 0.25)                               # gêné quand le tampon tombe
        for face, a in (("blase", 1 - gene), ("gene", gene)):
            if a > 0.01:
                cle = ("buste", face)
                if cle not in s._cache:
                    s._cache[cle] = _grand(_buste("PETIT", face)[0], 9)
                bu = s._cache[cle]
                im.alpha_composite(_fade(bu, ap * a), (56, int(540 - bu.height + 18 * (1 - ap))))
        b = s._bulle_grise()
        im.alpha_composite(_fade(b, ap), (330, int(250 + 18 * (1 - ap))))
        f = smooth((v - s.T_TAMPON + 0.45) / 0.45)                                 # le tampon descend en douceur
        if f > 0.01:                                                                # (d'en haut, sans rebond, sans
            tp = s._tampon()                                                        # sortir de l'image ; il touche le
            tp_ = s._zoom(tp, 1.05 - 0.05 * f) if f < 0.999 else tp                # coin de la bulle, pas Petit)
            _colle(im, tp_, 645, 521 - 60 * (1 - f), min(1.0, f * 1.6))

    def _image_liste(s, u):
        W_, H_ = 1020, 960
        ti = s.t.get("injustice")
        if ti is None:
            return s._liste(u)
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        a_l = 0.0 if ti < 0.1 else 1 - smooth((u - ti) / 0.3)                      # la feuille s'efface d'abord
        if a_l > 0.01:
            im.alpha_composite(_fade(s._liste(u), a_l))
        if u >= ti:
            s._injustice(im, u - ti)
        return im

    # ============================================================ {carnet}
    def _carnet(s):
        """Le petit carnet à spirale, ouvert : page crème, lignes bleues, marge rouge."""
        if "carnet" in s._cache:
            return s._cache["carnet"]
        W, H = 156, 57
        c = Px(W, H, alpha=True)
        dos = c.mask_rrect(3, 7, W, H, 3)
        c.shape(dos, (162, 118, 78), shade=(126, 88, 56), light=(190, 146, 100), band=1, olcol=OL)
        page = c.mask_rrect(0, 4, W - 4, H - 3, 3)
        c.shape(page, (252, 248, 234), shade=(222, 214, 192), light=(255, 255, 250), band=2, olcol=OL)
        for y in (s.Y_BASE - 16, s.Y_BASE, s.Y_BASE + 13):                         # (on écrit sur celle du milieu)
            c.fill(c.mask_rect(2, y, W - 6, y + 1) & page, (172, 198, 232))
        c.fill(c.mask_rect(15, 5, 16, H - 4) & page, (236, 140, 140))
        for x in range(8, W - 10, 8):                                               # la spirale
            c.fill(c.mask_ell(x + 1.5, 9, 1.6, 1.4), (90, 80, 70))
            anneau = c.mask_rrect(x, 0, x + 3, 10, 1)
            c.shape(anneau, (176, 182, 196), shade=(120, 126, 142), light=(220, 224, 236), band=1, olcol=OL)
        s._cache["carnet"] = c.img(s.K, rgba=True)
        return s._cache["carnet"]

    def _stylo(s):
        """Un stylo bille bleu, penché de 22° (la pointe en bas à gauche, en (3, 38) du dessin) : assez droit pour
        rester dans l'image au bout de la ligne (il ne dépasse que d'environ 100 pixels d'écran à droite de sa pointe)."""
        if "stylo" not in s._cache:
            c = Px(23, 40, alpha=True)
            sn, cs = math.sin(math.radians(22)), math.cos(math.radians(22))

            def p(d, e=0.0):                                                        # d : le long du stylo depuis
                return (3 + sn * d + cs * e, 38 - cs * d + sn * e)                  # la pointe ; e : sur le côté
            corps = _os(c, *p(11), *p(35), 5)
            c.shape(corps, (56, 96, 204), shade=(36, 66, 156), light=(116, 156, 240), band=1, olcol=OL)
            grip = _os(c, *p(5), *p(12), 5)
            c.shape(grip, (52, 52, 64), shade=(30, 30, 40), band=1, olcol=OL)
            pointe = c.mask_poly([p(0), p(6, -2.4), p(6, 2.4)])
            c.shape(pointe, (200, 202, 212), shade=(150, 152, 166), band=1, olcol=OL)
            c.fill(c.mask_poly([p(24, 0.6), p(33, 0.6), p(33, 1.9), p(24, 1.9)]), (220, 224, 236))   # l'agrafe
            s._cache["stylo"] = (c.img(s.K, rgba=True), (3 * s.K, 38 * s.K))
        return s._cache["stylo"]

    def _image_carnet(s, u):
        K = s.K
        W_, H_ = 1020, 960
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        nb = s._carnet()
        nx, ny = int((W_ - nb.width) / 2), 18
        im.alpha_composite(nb, (nx, ny))
        man = s._txt("man", MAIN_ECRITE, STYLO, TAILLE_MAIN, k=3, pad=1, font=MANUSCRITE, gras=True)
        asc = ImageFont.truetype(MANUSCRITE, TAILLE_MAIN).getmetrics()[0]
        mx = nx + 17 * K
        base = ny + s.Y_BASE * K                                                    # la ligne de base sur la 2e ligne bleue
        my = base - (1 + asc) * 3 + 6
        lin = min(1.0, max(0.0, (u - s.T_ECRIT) / s.D_ECRIT))
        p = 0.25 * smooth(lin) + 0.75 * lin                                        # à la main, de gauche à droite
        wv = int(man.width * p)
        if wv > 0:
            im.alpha_composite(man.crop((0, 0, wv, man.height)), (mx, my))
        st, (sx, sy) = s._stylo()
        lev = smooth((u - s.T_ECRIT - s.D_ECRIT - 0.05) / 0.45)                     # le stylo se lève et s'en va
        a_st = smooth((u - s.T_ECRIT + 0.25) / 0.25) * (1 - lev)                   # en s'effaçant (sans sortir
        if a_st > 0.01:                                                             # de l'image)
            px_ = mx + max(wv, 8) + 28 * lev
            py_ = base - 8 - 12 * lev
            im.alpha_composite(_fade(st, a_st), (int(px_ - sx), int(py_ - sy)))
        cite = s._cache.get("cite")
        if cite is None:                                                            # l'extrait qui porte l'ordre d'écrire
            cite = _lignes(CITATION, JAUNE, 47, serre=42)
            cite = s._cache["cite"] = cite.crop(cite.getbbox())
        s._pose(im, cite, W_ / 2, s.Y_CITE, smooth((u - s.T_CITE) / 0.4), maxw=W_ - 16)
        s._pose(im, s._lab("CORAN 2:282 · EXTRAIT", BLANC, 40), W_ / 2, s.Y_CORAN, smooth((u - s.T_CITE - 0.3) / 0.35))
        maj = s._cache.get("maj")
        if maj is None:
            maj = s._cache["maj"] = _lignes(["CONSEILLÉ SELON LA MAJORITÉ", "DES SAVANTS"], (206, 208, 218), 40)
        s._pose(im, maj, W_ / 2, s.Y_MAJ, smooth((u - s.T_CITE - 0.6) / 0.35))
        return im


# ---------------------------------------------------------------- branchement (via explique_0611.py)
CLES = ("sms", "dette", "carnet")


def _norm(m):
    return m.lower().replace("é", "e").replace("è", "e").replace("ê", "e")


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

    if k == "sms":
        schema._ajoute(t, Dette(brut, "sms", qui if qui in ("PETIT", "GRAND") else "PETIT"))
    elif k == "dette":
        if sous in Dette.ETAPES:
            etape(Dette, sous, "liste", lambda: Dette(brut, "liste"))
        else:
            schema._ajoute(t, Dette(brut, "liste"))
    elif k == "carnet":
        schema._ajoute(t, Dette(brut, "carnet"))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "sms":
        return t + 1.7
    if k == "dette":                                  # reste : le temps de lire « = LE DROIT DES AUTRES » (07/11)
        return t + dict(efface=1.6, reste=1.5, injustice=1.5).get(sous, 0.8)
    if k == "carnet":                                 # 07/11 : l'extrait en 3 lignes, la source et la mention à lire
        return t + 2.8
    return None
