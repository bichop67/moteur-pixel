# DÉMONSTRATIONS EN IMAGE DU 08/11/2026 — Short ISL31 « Le soleil se couche ? Rentre les petits ! » (consigne +
# avertissement). Textes : Mouslim 2013 (« les démons sortent quand le soleil se couche »), Boukhari 3304 · Mouslim 2012
# (« retenez vos enfants, car les démons se répandent à ce moment-là… fermez les portes, citez le nom d'Allah, car le
# Chaytan n'ouvre pas une porte fermée »). Niveau : sunna, conseil de protection (avis majoritaire).
# Règles de dessin : AUCUN Chaytan dessiné ni suggéré — la brume n'est qu'une nappe gris-violet au ras du sol, en
# paliers nets, SANS forme (ni visage, ni yeux, ni mains, ni silhouette) ; elle ne touche jamais personne, ne monte
# jamais sur une porte (les portes sont exclues de la nappe) et n'agit sur rien (lampadaires stables). Aucun texte sur
# une porte : le nom d'Allah est DIT (bulle de parole). Mouvements doux : glissés, fondus, jamais de secousse.
#   {coucher PETIT}        accroche, vue à ta place au bout de la rue : un GRAND soleil rouge-orangé (420 px) descend
#                          derrière les immeubles du fond (moitié cachée à 3 s), le ciel passe de l'orange au rouge ;
#                          Petit tire dans son ballon, le ballon roule VERS TOI et grossit (60 → 320 px) ; les ombres
#                          s'allongent vers toi, les lampadaires s'allument en fondu. Aucun texte (l'accroche du moteur).
#   {crepuscule}           (dès le DÉBUT de la réplique 3 : le schéma bouge pendant le ﷺ) la rue vue de face, trois
#                          maisons basses à la porte éclairée ; le ciel s'assombrit (≈ 1,4 s, avant la brume) ; l'enfant
#                          au sweat vert rentre chez lui (sa porte se ferme doucement), l'enfant au sweat bleu va dans
#                          l'encadrement de la sienne, Petit reste au milieu ; la brume naît, sans légende, tout au fond
#                          à gauche (fine bande au ras du sol).
#   {crepuscule tombe}     (sur « Quand la nuit tombe ») « QUAND LA NUIT TOMBE… », « RETENEZ VOS ENFANTS » (jaune),
#                          « SUNNA (AVIS MAJORITAIRE) » ; sans cette étape, elles arrivent au début de {crepuscule}.
#   {crepuscule repandent} la brume s'étale lentement au sol et au pied des murs (2 s) et s'arrête loin de Petit, qui
#                          s'inquiète (goutte) ; « LES DÉMONS SE RÉPANDENT » (blanc, contour rouge sombre),
#                          « (CHAYÂTÎN) », « À CE MOMENT-LÀ ».
#   {crepuscule porte}     (nouveau schéma) rapprochement lent (0,85 s) sur la porte de l'enfant au sweat bleu (de dos
#                          dans l'encadrement) ; Petit dehors à droite, inquiet ; la porte se ferme en 1,1 s sans rebond,
#                          une bulle « BISMILLAH ! » sort de l'entrebâillement, « = AU NOM D'ALLAH » dessous ; elle
#                          s'efface porte fermée ; en haut « FERMEZ LES PORTES ».
#   {crepuscule fermee}    la porte nue (sans aucun texte) ; un liseré doré doux naît autour du cadre, côté bulle ; la
#                          brume glisse jusqu'au seuil et s'arrête au liseré ; « LE CHAYTAN N'OUVRE PAS // UNE PORTE
#                          FERMÉE » (« FERMÉE » en jaune) + coche verte douce. (Seule, sans {crepuscule porte} avant :
#                          la porte est déjà fermée.)
#   {crepuscule claque}    la caméra glisse vers la maison de Petit (une AUTRE porte) ; Petit court (glissé fluide), la
#                          brume derrière lui, il entre, la porte se ferme vite sans tremblement (« clac » discret) ;
#                          bulle « BISMILLAH ! » depuis la fenêtre éclairée. Aucun autre texte.
#   {crepuscule nuit}      plan serré : la porte fermée de Petit et sa fenêtre éclairée, ciel de nuit, brume hors du
#                          cadre ; Grand arrive DE DOS à pas lents, s'arrête, petite bulle « ! » ; bandeau en fondu
#                          « QUAND LE DÉBUT DE LA NUIT EST PASSÉ, LES ENFANTS PEUVENT RESSORTIR » // « CONSEIL : SUNNA (AVIS
#                          MAJORITAIRE) » (sans guillemets ; lignes ≤ 760 px, hors des boutons). Rien sur les adultes.
# Les modes porte, fermee, claque et nuit redessinent tout (rue de nuit, maisons, brume) : ils partent sans l'état du
# mode précédent. Branché par explique_0811.py (import tardif).
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import cast
import pxv
from px import Px, TAHOMA
from pxv import smooth
from explique import _titre, _fade, BLANC, JAUNE
from explique_0411 import OL, _grand
from explique_0411b import _Base, _translucide
from explique_0611_dette import _texte_px, _colle, _lueur_px

K = 6
VERT_C = (86, 204, 116)                 # la coche
LUMIERE = (255, 214, 130)               # lumière chaude des portes et fenêtres
OR_DOUX = (255, 210, 110)               # le liseré doré
BRUME = (34, 26, 50)                    # gris-violet très foncé (cœur de la nappe : plus foncé ; bord : voile clair)
BRUME_FONCE = (20, 14, 32)
BRUME_CLAIR = (92, 82, 124)
BOIS = (112, 70, 44)


# ---------------------------------------------------------------- petits outils
def _mix(c1, c2, t):
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(c1, c2))


def _nuit(c, f=0.55):
    """Une couleur de jour assombrie et bleuie pour la nuit."""
    return _mix(c, (30, 26, 58), f)


def _teinte(im, f=0.22, col=(30, 26, 64)):
    a = np.array(im).astype(np.float32)
    a[..., :3] = a[..., :3] * (1 - f) + np.array(col, np.float32) * f
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def _dil(m, n=1):
    e = m.copy()
    for _ in range(n):
        e = e | np.roll(e, 1, 0) | np.roll(e, -1, 0) | np.roll(e, 1, 1) | np.roll(e, -1, 1)
    return e


def _bulle(txt, col_txt=(44, 30, 44), size=12, k=5, pointe="bas_gauche"):
    """Bulle de parole pixel (blanc chaud, contour sombre) ; renvoie (image, (x, y) de la pointe dans l'image)."""
    tx = _texte_px(txt, col_txt, size, k=k, pad=1)
    bw = int(math.ceil(tx.width / k)) + 8
    bh = int(math.ceil(tx.height / k)) + 5
    c = Px(bw + 2, bh + 10, alpha=True)
    corps = c.mask_rrect(1, 1, bw + 1, bh + 1, 4)
    if pointe == "bas_gauche":
        pts = [(9, bh - 1), (17, bh - 1), (5, bh + 9)]
        tip = (5 * k, (bh + 9) * k)
    else:
        pts = [(bw - 16, bh - 1), (bw - 8, bh - 1), (bw - 3, bh + 9)]
        tip = ((bw - 3) * k, (bh + 9) * k)
    m = corps | c.mask_poly(pts)
    c.shape(m, (252, 248, 236), shade=(222, 214, 196), light=(255, 255, 250), sdir="bottom", band=1, olcol=OL)
    im = c.img(k, rgba=True)
    im.alpha_composite(tx, (int(1 * k + (bw * k - tx.width) / 2), int(1 * k + (bh * k - tx.height) / 2)))
    return im, tip


def _coche():
    c = Px(22, 18, alpha=True)
    m = c.mask_poly([(2, 9), (6, 5), (9, 9), (17, 1), (21, 5), (9, 17)])
    c.shape(m, VERT_C, shade=(50, 150, 80), light=(150, 236, 170), band=1, olcol=OL)
    return c.img(K, rgba=True)


# ---------------------------------------------------------------- l'élément
class Coucher(_Base):
    """{coucher PETIT} : accroche, vue à ta place : le grand soleil qui se couche, Petit et son ballon qui roule vers
    toi. {crepuscule} : la rue, trois maisons, la nuit tombe ; {crepuscule tombe} « RETENEZ VOS ENFANTS » (sunna, avis
    majoritaire) ;
    {crepuscule repandent} la brume s'étale (sans forme), « LES DÉMONS SE RÉPANDENT ». {crepuscule porte} : la porte de
    l'enfant bleu se ferme, bulle « BISMILLAH ! » ; {crepuscule fermee} liseré doré, la brume s'arrête au seuil, « LE
    CHAYTAN N'OUVRE PAS UNE PORTE FERMÉE ». {crepuscule claque} : Petit rentre chez lui. {crepuscule nuit} : Grand
    devant la porte fermée, bandeau « QUAND LE DÉBUT DE LA NUIT EST PASSÉ… »."""
    PW_, PH_ = 170, 160
    ETAPES = ("tombe", "repandent", "fermee")
    # --- l'accroche (unités du dessin, ×6)
    VP = (85, 86)                       # point de fuite
    FOND = 102                          # le sol au bout de la rue
    SOL_X = (64, 106)                   # fin des façades au bout de la rue
    SOLEIL_R = 35                       # rayon (70 unités = 420 px)
    SOLEIL_Y = (44, 76)                 # centre du soleil à 0 s et à 3 s (moitié cachée)
    PETIT_A = (92, 116)                 # les pieds de Petit (accroche)
    BALLON = ((588, 684, 60), (540, 790, 320))     # (x, y, diamètre) au départ et à l'arrivée (pixels d'écran)
    D_BALLON = 2.7
    LAMPES_A = ((12, 152, 70), (55, 112, 27), (158, 152, 70), (115, 112, 27))   # (x, pied, hauteur)
    # --- la rue de face (unités du dessin)
    MAISONS = ((4, 54), (60, 110), (116, 166))
    PORTES = (29, 85, 141)              # centre des portes : l'enfant vert, l'enfant bleu, Petit
    DL, PT, PB = 8, 78, 118             # demi-largeur, haut, bas de l'ouverture
    FENETRES = (41, 97, 153)            # bord gauche des fenêtres (11 de large, y 80-95)
    LAMPES = (57, 113)
    PETIT_R = (124, 150)                # Petit dans la rue (pieds)
    KS = 3                              # échelle des persos dans la rue (porte ≈ 1,2 × perso)
    BR_MAX = 58                         # bord de la brume après « répandent » (loin de Petit et de l'enfant bleu)
    BR_SEUIL = 73                       # la brume s'arrête au liseré de la porte de l'enfant bleu
    VUE_PORTE = (28, 46)                # coin des vues serrées (×1,5) : la porte de l'enfant bleu, celle de Petit
    VUE_CLAQUE = (56, 46)
    Z = 1.5
    # --- le plan serré final
    SOLN = 122                          # le seuil (unités)
    PORTE_N = (60, 100, 36)             # gauche, droite, haut de la porte de Petit (plan serré)

    def __init__(s, cmd, mode="crepuscule", who="PETIT", deja=False):
        super().__init__(cmd)
        s.mode = mode
        s.who = who if who in ("PETIT", "GRAND") else "PETIT"
        s.deja = deja

    # ============================================================ sons
    def sons_el(s):
        if s.mode == "coucher":
            return [(0.05, "dv_ballon", 0.035, None)]
        out = []
        if s.mode == "crepuscule":
            if "repandent" in s.t:
                out.append((s.t["repandent"], "tr_whoosh_doux", 0.035, None))
        elif s.mode == "porte":
            if not s.deja:
                out.append((0.6, "dv_porte_bois", 0.022, None))
            if "fermee" in s.t:
                out.append((s.t["fermee"] + 0.15, "sa_scintillement", 0.035, None))
        elif s.mode == "claque":
            out += [(0.05, "dv_pas_course_maison", 0.03, None), (1.12, "dv_porte_claque", 0.02, None)]
        elif s.mode == "nuit":
            out.append((0.0, "dv_pas_pierre", 0.025, None))
        return out

    # ============================================================ image
    def image(s, u):
        if s.mode == "coucher":
            return s._image_coucher(u)
        if s.mode == "nuit":
            return s._image_nuit(u)
        if s.mode == "crepuscule":
            return s._image_crepuscule(u)
        if s.mode == "claque":
            return s._image_claque(u)
        return s._image_porte(u)

    # ---- outils communs
    def _perso(s, qui, face="neutre", back=False, sweat=False, couleur=None, pose="neutre", k=None, nuit=0.0):
        k = k or s.KS
        cle = ("p", qui, face, back, sweat, couleur, pose, k, nuit)
        if cle not in s._cache:
            r = cast.CAST[qui] if couleur is None else dict(cast.CAST[qui], couleur=couleur, chapeau=None)
            im = Image.fromarray(cast.dessine(r, pose, face, back=back, sweat=sweat).a, "RGBA")
            im = _grand(im, k)
            if nuit > 0:
                im = _teinte(im, nuit)
            s._cache[cle] = im
        return s._cache[cle]

    @staticmethod
    def _pose_perso(im, spr, x, y, a=1.0, k=3):
        """Colle un perso par ses pieds (x, y en pixels d'écran)."""
        if a > 0.01:
            im.alpha_composite(_fade(spr, a), (int(x - 23 * k), int(y - 95 * k)))

    def _noise(s):
        if "noise" not in s._cache:
            rng = np.random.default_rng(31)
            n1 = Image.fromarray((rng.random((20, 42)) * 255).astype(np.uint8)).resize((340, 160), Image.BICUBIC)
            n2 = Image.fromarray((rng.random((40, 85)) * 255).astype(np.uint8)).resize((340, 160), Image.BICUBIC)
            n = 0.62 * np.array(n1, np.float32) + 0.38 * np.array(n2, np.float32)
            n = (n - n.min()) / (n.max() - n.min())
            s._cache["noise"] = n
        return s._cache["noise"]

    def _brume(s, u, front, haut=100, exclus=(), a=1.0):
        """La nappe de brume (unités du dessin, ×6) : au sol et au pied des murs, à gauche de front ; paliers nets,
        aucune forme ; les rectangles exclus (portes, persos) restent nets."""
        if front <= 0.5 or a <= 0.01:
            return None
        n = s._noise()
        pos = u * 4.0                                       # glissé continu (interpolé entre deux colonnes : pas de saut)
        off, f = int(pos), pos - int(pos)
        c0 = (np.arange(170) + 340 - off % 340) % 340
        n = (1 - f) * n[:, c0] + f * n[:, (c0 - 1) % 340]
        x = np.arange(170, dtype=np.float32)
        y = np.arange(160, dtype=np.float32)
        hx = np.clip((front - x) / 13.0, 0, 1)
        vy = np.where(y < haut, 0.0, np.where(y < 116, (y - haut) / (116 - haut) * 0.75, 1.0)).astype(np.float32)
        d = vy[:, None] * hx[None, :] * (0.35 + 0.85 * n) - 0.18 * (1 - n)
        for (x0, y0, x1, y1) in exclus:
            d[max(0, int(y0)):max(0, int(y1)), max(0, int(x0)):max(0, int(x1))] = 0
        out = np.zeros((160, 170, 4), np.uint8)
        for seuil, col, al in ((0.22, BRUME_CLAIR, 84), (0.48, BRUME, 150), (0.74, BRUME_FONCE, 196)):
            m = d > seuil
            out[m] = (*col, int(al * a))
        return Image.fromarray(out, "RGBA").resize((170 * K, 160 * K), Image.NEAREST)

    def _vue(s, im, box):
        """Recadre l'image (1020 × 960) sur box = (x0, y0, largeur) en unités, à la taille de l'élément : net (×1,5
        au plus proche) quand la vue est posée, doux pendant le mouvement."""
        x0, y0, w = box
        h = w * 160 / 170
        if abs(w - 170 / s.Z) < 1e-3 and abs(x0 - round(x0)) < 1e-3 and abs(y0 - round(y0)) < 1e-3:
            return im.crop((int(round(x0)) * K, int(round(y0)) * K, int(round(x0)) * K + 680, int(round(y0)) * K + 640)
                           ).resize((1020, 960), Image.NEAREST)
        if w >= 169.99:
            return im
        return im.resize((1020, 960), Image.LANCZOS, box=(x0 * K, y0 * K, (x0 + w) * K, (y0 + h) * K))

    # ============================================================ l'accroche
    def _ciel_acc(s, v):
        cle = ("ciel", v)
        if cle not in s._cache:
            c = Px(170, 160)
            haut, bas = ((238, 128, 72), (255, 204, 124)) if v == 0 else ((118, 38, 82), (232, 86, 58))
            c.vgrad(c.mask_rect(0, 0, 170, 160), 0, 104, haut, bas, steps=7)
            s._cache[cle] = c.img(K)
        return s._cache[cle]

    def _soleil(s):
        if "soleil" not in s._cache:
            R = s.SOLEIL_R
            W = 2 * R + 30
            c = Px(W, W, alpha=True)
            cx = cy = W / 2
            for j, (rr, col) in enumerate(((R + 13, (255, 150, 80)), (R + 8, (255, 128, 70)), (R + 4, (255, 112, 64)))):
                pass
            disque = c.mask_ell(cx, cy, R, R)
            c.fill(disque, (250, 92, 52))
            c.fill(c.mask_ell(cx, cy - 3, R - 5, R - 6) & disque, (255, 132, 64))
            c.fill(c.mask_ell(cx, cy - 7, R - 13, R - 15) & disque, (255, 172, 92))
            for k_, y in enumerate(range(int(cy + 8), int(cy + R), 6)):     # bandes du couchant (pixel art)
                c.fill(c.mask_rect(0, y, W, y + 1 + k_ // 2) & disque, (236, 70, 52))
            im = c.img(K, rgba=True)
            halo = Image.new("RGBA", im.size, (0, 0, 0, 0))                        # halo en paliers (sans flou)
            hc = Px(W, W, alpha=True)
            a = np.zeros((W, W, 4), np.uint8)
            for rr, al in ((R + 14, 40), (R + 9, 70), (R + 4, 105)):
                a[hc.mask_ell(cx, cy, rr, rr)] = (255, 170, 96, al)
            halo = Image.fromarray(a, "RGBA").resize(im.size, Image.NEAREST)
            halo.alpha_composite(im)
            s._cache["soleil"] = halo
        return s._cache["soleil"]

    def _decor_acc(s):
        """Façades en contre-jour, immeubles du fond, trottoirs, route et lampadaires (tout sauf le ciel et le soleil)."""
        if "dacc" in s._cache:
            return s._cache["dacc"]
        c = Px(170, 160, alpha=True)
        vx, vy = s.VP
        xg, xd = s.SOL_X
        F = s.FOND
        # les immeubles du fond (la ligne derrière laquelle le soleil se couche)
        for (x0, x1, top) in ((60, 72, 71), (71, 80, 75), (79, 91, 73), (90, 99, 76), (98, 110, 72)):
            m = c.mask_rect(x0, top, x1, F + 1)
            c.shape(m, (78, 34, 66), shade=(60, 26, 54), light=(104, 50, 80), band=1, olcol=(44, 18, 40))
            for wx in range(x0 + 2, x1 - 2, 3):
                for wy in range(top + 3, F - 3, 4):
                    if (wx * 7 + wy * 3) % 5 == 0:
                        c.fill(c.mask_rect(wx, wy, wx + 1, wy + 2), (255, 196, 110))
        # les façades (perspective : leurs bords vont au point de fuite)
        def bord(x0, y0, x):
            return y0 + (vy - y0) * x / vx
        for cote in (0, 1):
            def X(x):
                return x if cote == 0 else 170 - x
            top0, bas0 = 22, 150
            pts = [(X(0), top0), (X(xg), bord(0, top0, xg)), (X(xg), bord(0, bas0, xg)), (X(0), bas0), (X(0), 160)]
            pts = [(X(0), top0), (X(xg), bord(0, top0, xg)), (X(xg), bord(0, bas0, xg)), (X(0), bas0)]
            fac = c.mask_poly(pts)
            col = (92, 50, 86) if cote == 0 else (84, 46, 80)
            c.shape(fac, col, shade=_mix(col, (40, 20, 40), 0.4), light=_mix(col, (255, 150, 100), 0.25), band=1,
                    olcol=(40, 18, 38))
            for i, f0 in enumerate((0.06, 0.30, 0.52, 0.70, 0.84)):                 # fenêtres en perspective
                f1 = f0 + (0.14, 0.12, 0.1, 0.08, 0.06)[i]
                xa, xb = f0 * xg, f1 * xg
                for j, (g0, g1) in enumerate(((0.12, 0.30), (0.40, 0.58), (0.68, 0.84))):
                    q = []
                    for (xx, gg) in ((xa, g0), (xb, g0), (xb, g1), (xa, g1)):
                        yt, yb = bord(0, top0, xx), bord(0, bas0, xx)
                        q.append((X(xx), yt + (yb - yt) * gg))
                    allume = (i + j + cote) % 3 != 1
                    wm = c.mask_poly(q) & fac
                    c.fill(wm, (255, 190, 104) if allume else (50, 28, 52))
                    if allume:
                        c.edge(wm, (226, 140, 80), "bottom", 1)
            # le trottoir
            ry = lambda y: vx - (15 / 16) * (y - vy)          # bord de la route (gauche) à la hauteur y
            tro = c.mask_poly([(X(xg), F), (X(70), F), (X(ry(160)), 160), (X(0), 160), (X(0), bas0)])
            c.fill(tro, (138, 96, 112))
            c.dither(tro, (120, 82, 100), 0.25)
            c.edge(tro, (176, 126, 128), "top", 1)
        route = c.mask_poly([(70, F), (100, F), (154.4, 160), (15.6, 160)])
        c.vgrad(route, F, 160, (128, 78, 90), (70, 50, 70), steps=6)
        c.dither(route, (62, 44, 62), 0.12)
        for i in range(7):                                                          # la ligne du milieu
            y0 = F + 2 + (i * (i + 3)) * 1.25
            y1 = y0 + 1.5 + i * 0.9
            if y0 >= 160:
                break
            w0 = 0.6 + (y0 - vy) * 0.035
            w1 = 0.6 + (min(y1, 160) - vy) * 0.035
            c.fill(c.mask_poly([(vx - w0, y0), (vx + w0, y0), (vx + w1, min(y1, 160)), (vx - w1, min(y1, 160))]),
                   (236, 200, 150))
        # lampadaires (le pied, le mât, la tête : allumés à part)
        for (lx, ly, lh) in s.LAMPES_A:
            e = max(1, int(round(lh / 35)))
            m = c.mask_rect(lx - e / 2, ly - lh, lx + e / 2 + 0.5, ly)
            sens = 1 if lx < 85 else -1
            bras = c.mask_rect(min(lx, lx + sens * lh * 0.12), ly - lh, max(lx, lx + sens * lh * 0.12) + 1, ly - lh + e)
            tete = c.mask_rect(lx + sens * lh * 0.12 - e * 1.5, ly - lh + e, lx + sens * lh * 0.12 + e * 1.5 + 1,
                               ly - lh + e * 2.5)
            c.fill(m | bras, (40, 26, 44))
            c.fill(tete, (60, 40, 56))
        s._cache["dacc"] = c.img(K, rgba=True)
        return s._cache["dacc"]

    def _lueurs_acc(s):
        if "lacc" not in s._cache:
            lay = Image.new("RGBA", (1020, 960), (0, 0, 0, 0))
            for (lx, ly, lh) in s.LAMPES_A:
                sens = 1 if lx < 85 else -1
                hx, hy = lx + sens * lh * 0.12, ly - lh + lh / 35 * 2.5
                r = max(4, lh * 0.16)
                _colle(lay, _lueur_px(r, r * 0.8, (255, 220, 120), niveaux=(36, 70, 120)), hx * K, hy * K + 6)
                d = ImageDraw.Draw(lay)
                e = max(1, int(round(lh / 35)))
                d.rectangle([int((hx - e * 1.2) * K), int((ly - lh + e * 2.3) * K), int((hx + e * 1.2) * K),
                             int((ly - lh + e * 2.9) * K)], fill=(255, 236, 170, 255))
            s._cache["lacc"] = lay
        return s._cache["lacc"]

    def _ballon(s, diam, phase):
        """Le ballon (dessin 40 × 40, agrandi au plus proche) ; phase = combien il a roulé (radians)."""
        ph = int(round(phase / (2 * math.pi) * 16)) % 16
        cle = ("bal", ph)
        if cle not in s._cache:
            N = 40
            c = Px(N, N, alpha=True)
            yy, xx = np.mgrid[0:N, 0:N]
            dx = (xx + 0.5 - N / 2) / (N / 2 - 1)
            dy = (yy + 0.5 - N / 2) / (N / 2 - 1)
            r2 = dx * dx + dy * dy
            disque = r2 <= 1.0
            dz = np.sqrt(np.clip(1 - r2, 0, 1))
            lat = np.arctan2(dy, dz) - ph * (2 * math.pi / 16)                   # il roule vers toi (vers le bas)
            lon = np.arcsin(np.clip(dx / np.maximum(np.sqrt(1 - np.clip(dy * dy, 0, 0.999)), 1e-3), -1, 1))
            gv = lat / 0.95
            row = np.floor(gv)
            gu = lon / 0.95 + 0.5 * (row % 2)
            cu, cv = gu - np.floor(gu) - 0.5, gv - row - 0.5
            noir = (cu * cu + cv * cv) < 0.085
            c.fill(disque, (246, 244, 240))
            c.fill(disque & (dy > 0.25), (214, 210, 214))
            c.fill(disque & (dy > 0.62), (178, 170, 184))
            c.fill(disque & noir, (36, 32, 44))
            c.fill(disque & (dy < -0.62) & ~noir, (255, 236, 200))               # liseré du couchant en haut
            c.outline(disque, OL)
            s._cache[cle] = c.img(1, rgba=True)
        b = s._cache[cle]
        d = max(8, int(round(diam)))
        return b.resize((d, d), Image.NEAREST)

    def _image_coucher(s, u):
        f = smooth(u / 3.2) * 0.9
        im = Image.blend(s._ciel_acc(0), s._ciel_acc(1), f).convert("RGBA")
        lin = min(1.0, max(0.0, u / 3.0))
        sy = s.SOLEIL_Y[0] + (s.SOLEIL_Y[1] - s.SOLEIL_Y[0]) * (0.7 * lin + 0.3 * smooth(lin))
        _colle(im, s._soleil(), 85 * K, sy * K)
        im.alpha_composite(s._decor_acc())
        ol = smooth((u - 0.5) / 1.3)                                                # les lampadaires s'allument
        if ol > 0.01:
            im.alpha_composite(_fade(s._lueurs_acc(), ol))
        lo = 0.25 + 0.75 * smooth(u / 3.0)                                         # les ombres s'allongent vers toi
        vx, vy = s.VP[0] * K, s.VP[1] * K
        px_, py_ = s.PETIT_A[0] * K, s.PETIT_A[1] * K
        bx0, by0, d0 = s.BALLON[0]
        bx1, by1, d1 = s.BALLON[1]
        p = min(1.0, max(0.0, u / s.D_BALLON))
        p = 1 - (1 - p) ** 2.4                                                      # il ralentit en arrivant
        bx, by, bd = bx0 + (bx1 - bx0) * p, by0 + (by1 - by0) * p, d0 + (d1 - d0) * p
        ombres = []
        for (lx, ly, lh) in s.LAMPES_A:
            ax, ay = lx * K, ly * K
            ux, uy = ax - vx, ay - vy
            n = math.hypot(ux, uy)
            L = lh * K * 0.9 * lo
            ex, ey = ux / n * L, uy / n * L
            w = max(4, lh * 0.12)
            ombres.append([(ax - w, ay), (ax + w, ay), (ax + ex + w * 1.6, ay + ey), (ax + ex - w * 1.6, ay + ey)])
        L = 230 * lo
        ombres.append([(px_ - 34, py_ - 4), (px_ + 34, py_ - 4), (px_ + 56 + 0.12 * L, py_ + L),
                       (px_ - 40 + 0.12 * L, py_ + L)])

        def dessin(d):
            for q in ombres:
                d.polygon(q, fill=(40, 12, 34, 92))
            d.ellipse([bx - bd * 0.5, by + bd * 0.36, bx + bd * 0.62, by + bd * 0.56], fill=(40, 12, 34, 110))
        _translucide(im, dessin)
        tir = smooth((u - 0.05) / 0.3)                                              # Petit vient de tirer
        pose = "lance" if u < 0.55 else "neutre"
        spr = s._perso(s.who, "content" if u < 0.55 else "rire", pose=pose, k=4, nuit=0.12)
        s._pose_perso(im, spr, px_ - 4 * (1 - tir), py_, 1.0, k=4)
        bal = s._ballon(bd, (p * 3.0) * 2 * math.pi)                               # s'arrête sur la phase 0 (motif classique, pas un « visage »)
        im.alpha_composite(bal, (int(bx - bal.width / 2), int(by - bal.height / 2)))
        return im

    # ============================================================ la rue de face
    def _rue(s, nuit):
        """La rue vue de face (sans portes mobiles, sans persos) ; nuit = 0 (fin du couchant) ou 1 (nuit)."""
        cle = ("rue", nuit)
        if cle in s._cache:
            return s._cache[cle]
        c = Px(170, 160)
        N = (lambda col: _nuit(col, 0.55)) if nuit else (lambda col: _nuit(col, 0.22))
        ciel = c.mask_rect(0, 0, 170, 62)
        if nuit:
            c.vgrad(ciel, 0, 58, (14, 14, 42), (52, 34, 84), steps=6)
            c.fill(c.mask_rect(0, 55, 170, 58), (150, 42, 56))                     # le fil rouge à l'horizon
            c.fill(c.mask_rect(0, 54, 170, 55), (96, 34, 66))
            rng = np.random.default_rng(5)
            for _ in range(26):
                x, y = int(rng.integers(2, 168)), int(rng.integers(2, 30))
                c.fill(c.mask_rect(x, y, x + 1, y + 1), (226, 222, 250))
        else:
            c.vgrad(ciel, 0, 58, (92, 48, 98), (226, 96, 70), steps=6)
            c.fill(c.mask_rect(0, 53, 170, 58), (240, 120, 64))
        rng = np.random.default_rng(9)
        x = 0
        while x < 170:                                                              # immeubles lointains
            w = int(rng.integers(9, 18))
            top = int(rng.integers(36, 50))
            m = c.mask_rect(x, top, x + w, 62)
            c.fill(m, (34, 26, 58) if nuit else (80, 42, 84))
            for wx in range(x + 2, x + w - 2, 3):
                for wy in range(top + 3, 58, 4):
                    if rng.random() < 0.25:
                        c.fill(c.mask_rect(wx, wy, wx + 1, wy + 2), (230, 180, 100) if nuit else (255, 200, 120))
            x += w
        murs = ((190, 132, 104), (150, 146, 180), (200, 164, 110))
        for i, (x0, x1) in enumerate(s.MAISONS):
            toit = c.mask_poly([(x0 - 3, 63), (x0 + 7, 51), (x1 - 7, 51), (x1 + 3, 63)])
            tc = N((150, 62, 54))
            c.shape(toit, tc, shade=_mix(tc, (0, 0, 0), 0.25), light=_mix(tc, (255, 255, 255), 0.15), sdir="bottom",
                    band=2, olcol=OL)
            for ty in range(54, 63, 3):
                c.fill(c.mask_rect(x0, ty, x1, ty + 1) & toit, _mix(tc, (0, 0, 0), 0.3))
            mur = c.mask_rect(x0, 62, x1, s.PB)
            mc = N(murs[i])
            c.shape(mur, mc, shade=_mix(mc, (0, 0, 0), 0.2), light=_mix(mc, (255, 255, 255), 0.1), band=2, olcol=OL)
            c.dither(mur, _mix(mc, (0, 0, 0), 0.1), 0.12)
            pc = s.PORTES[i]
            cadre = c.mask_rect(pc - s.DL - 2, s.PT - 2, pc + s.DL + 2, s.PB)
            c.shape(cadre, N((120, 82, 56)), band=1, olcol=OL)
            trou = c.mask_rect(pc - s.DL, s.PT, pc + s.DL, s.PB)
            c.vgrad(trou, s.PT, s.PB, (255, 232, 160), (236, 168, 92), steps=4)
            c.fill(c.mask_rect(pc - s.DL, s.PT, pc + s.DL, s.PT + 1), (200, 130, 70))
            fx = s.FENETRES[i]
            fen = c.mask_rect(fx, 80, fx + 11, 95)
            c.shape(fen, (255, 214, 124), shade=(236, 170, 90), band=1, olcol=OL)
            c.fill(c.mask_rect(fx + 5, 80, fx + 6, 95), N((120, 82, 56)))
            c.fill(c.mask_rect(fx, 87, fx + 11, 88), N((120, 82, 56)))
            c.fill(c.mask_rect(fx - 1, 95, fx + 12, 97), N((170, 160, 160)))
        tro = c.mask_rect(0, s.PB, 170, 127)
        c.fill(tro, N((168, 150, 160)))
        c.dither(tro, N((150, 132, 146)), 0.2)
        for xx in range(0, 170, 12):
            c.fill(c.mask_rect(xx, s.PB, xx + 1, 127), N((130, 112, 126)))
        c.fill(c.mask_rect(0, 126, 170, 128), N((110, 100, 116)))
        route = c.mask_rect(0, 128, 170, 160)
        c.fill(route, N((96, 86, 104)))
        c.dither(route, N((84, 74, 94)), 0.15)
        for xx in range(4, 170, 22):
            c.fill(c.mask_rect(xx, 143, xx + 11, 145), N((226, 216, 200)))
        for lx in s.LAMPES:
            c.fill(c.mask_rect(lx - 1, 64, lx + 1, s.PB + 2), (40, 34, 52))
            c.fill(c.mask_rect(lx - 3, s.PB + 1, lx + 3, s.PB + 3), (40, 34, 52))
            c.fill(c.mask_rect(lx - 3, 60, lx + 4, 64), (58, 50, 70))
            c.fill(c.mask_rect(lx - 2, 63, lx + 3, 65), (255, 236, 170))
        im = c.img(K).convert("RGBA")
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))                              # lueurs stables des lampadaires
        for lx in s.LAMPES:
            _colle(lay, _lueur_px(16, 12, (255, 220, 130), niveaux=(26, 52, 90)), lx * K + 3, 66 * K)
            _colle(lay, _lueur_px(14, 3, (255, 214, 130), niveaux=(24, 46, 70)), lx * K + 3, 123 * K)
        im.alpha_composite(lay)
        s._cache[cle] = im
        return im

    def _panneau(s, im, i, p, liseré=0.0):
        """La porte de la maison i, fermée à p (0 ouverte → 1 fermée ; charnière à gauche) ; liseré doré (0 → 1)."""
        pc = s.PORTES[i]
        x0, x1, y0, y1 = (pc - s.DL) * K, (pc + s.DL) * K, s.PT * K, s.PB * K
        if liseré > 0.01:
            cle = ("lis", i)
            if cle not in s._cache:
                m = np.zeros((160, 170), bool)
                m[s.PT - 2:s.PB, pc - s.DL - 2:pc + s.DL + 2] = True
                a = np.zeros((160, 170, 4), np.uint8)
                d1, d2, d3 = _dil(m, 1), _dil(m, 2), _dil(m, 3)
                a[d3 & ~m] = (*OR_DOUX, 40)
                a[d2 & ~m] = (*OR_DOUX, 84)
                a[d1 & ~m] = (*OR_DOUX, 150)
                a[s.PB:, :] = 0
                s._cache[cle] = Image.fromarray(a, "RGBA").resize((1020, 960), Image.NEAREST)
            im.alpha_composite(_fade(s._cache[cle], liseré))
        w = (x1 - x0) * min(1.0, p)
        if w < 1.0:                                     # battant de moins d'1 px : rien à dessiner (évite x1 < x0 dans Pillow)
            return
        sombre = 1 - min(1.0, p)
        d = ImageDraw.Draw(im)
        bois = _mix(_nuit(BOIS, 0.35), (20, 12, 20), 0.45 * sombre)
        d.rectangle([x0, y0, x0 + w - 1, y1 - 1], fill=(*bois, 255))
        if w > 3 * K:
            fonce = _mix(bois, (0, 0, 0), 0.25)
            for (a_, b_) in ((0.12, 0.44), (0.54, 0.9)):
                d.rectangle([x0 + w * 0.18, y0 + (y1 - y0) * a_, x0 + w * 0.82, y0 + (y1 - y0) * b_], outline=(*fonce, 255),
                            width=K)
            if p > 0.9:
                d.rectangle([x0 + w - 3.5 * K, y0 + (y1 - y0) * 0.52, x0 + w - 2.5 * K, y0 + (y1 - y0) * 0.52 + K],
                            fill=(236, 196, 96, 255))
        d.rectangle([x0, y0, x0 + w - 1, y1 - 1], outline=(*OL, 255), width=K)

    def _texte_rouge(s, txt):
        cle = ("rouge", txt)
        if cle not in s._cache:
            s._cache[cle] = _texte_px(txt, BLANC, 12, k=5, bord=(122, 18, 30), pad=3)
            h = _texte_px(txt, BLANC, 12, k=5, bord=(122, 18, 30), halo=(24, 6, 16), seul_halo=True, pad=3)
            h.alpha_composite(s._cache[cle])
            s._cache[cle] = h
        return s._cache[cle]

    def _deux_couleurs(s, a_txt, b_txt, size=60):
        cle = ("2c", a_txt, b_txt, size)
        if cle not in s._cache:
            a, b = _titre(a_txt, BLANC, size), _titre(b_txt, JAUNE, size)
            gap = int(size * 0.18)
            H = max(a.height, b.height)                 # alignés par le bas (l'accent de « FERMÉE » ne le décale plus)
            out = Image.new("RGBA", (a.width + b.width + gap, H), (0, 0, 0, 0))
            out.alpha_composite(a, (0, H - a.height))
            out.alpha_composite(b, (a.width + gap, H - b.height))
            s._cache[cle] = out
        return s._cache[cle]

    # ---- {crepuscule} et {crepuscule repandent}
    def _image_crepuscule(s, u):
        nf = smooth(u / 1.4)
        im = Image.blend(s._rue(0), s._rue(1), nf) if nf < 0.999 else s._rue(1).copy()
        k = s.KS
        tr = s.t.get("repandent")
        t0 = s.t.get("tombe", 0.0)                       # les étiquettes arrivent sur « Quand la nuit tombe »
        # l'enfant au sweat vert rentre chez lui, sa porte se ferme doucement
        v = smooth((u - 0.1) / 1.4)
        gx, gy = 44 + (29 - 44) * v, 146 + (118.5 - 146) * v
        bob = 3 * abs(math.sin(u * math.pi * 2.2)) * (1 - smooth((u - 1.4) / 0.2))
        ent = smooth((u - 1.5) / 0.4)
        spr = s._perso("PETIT", back=True, couleur=(64, 160, 92), nuit=0.25 * nf)
        s._pose_perso(im, spr, gx * K, (gy - 1.5 * ent) * K - bob, 1 - ent, k=k)
        s._panneau(im, 0, smooth((u - 1.9) / 1.0))
        # l'enfant au sweat bleu va dans l'encadrement de sa porte (il y reste)
        v = smooth((u - 0.3) / 1.6)
        bx, by = 66 + (85 - 66) * v, 148 + (118.5 - 148) * v
        bob = 3 * abs(math.sin(u * math.pi * 2.0)) * (1 - smooth((u - 1.8) / 0.2))
        spr = s._perso("PETIT", back=True, couleur=(60, 110, 204), nuit=0.25 * nf)
        s._pose_perso(im, spr, bx * K, by * K - bob, 1.0, k=k)
        # la brume : fine bande au fond (à gauche), puis elle s'étale après « répandent »
        front = 4 + 7 * smooth((u - 0.4) / 1.8)
        if tr is not None:
            front += (s.BR_MAX - front) * smooth((u - tr) / 2.0)
        exclus = [(pc - s.DL - 2, s.PT - 2, pc + s.DL + 2, s.PB) for pc in s.PORTES]
        br = s._brume(u, front, exclus=exclus, a=smooth((u - 0.4) / 0.8))
        if br is not None:
            im.alpha_composite(br)
        # Petit reste au milieu de la rue (inquiet après « répandent »)
        peur = tr is not None and u >= tr + 0.4
        spr = s._perso("PETIT", "peur" if peur else "content", sweat=peur, nuit=0.2 * nf)
        s._pose_perso(im, spr, s.PETIT_R[0] * K, s.PETIT_R[1] * K, 1.0, k=k)
        # les textes
        fin = s._a("repandent", u, 0.3) if tr is not None else 0.0
        s._pose(im, s._lab("QUAND LA NUIT TOMBE…", BLANC, 56), 510, 66, smooth((u - t0 - 0.1) / 0.35) * (1 - fin))
        s._pose(im, s._lab("RETENEZ VOS ENFANTS", JAUNE, 62), 510, 150, smooth((u - t0 - 0.85) / 0.35) * (1 - fin))
        s._pose(im, s._lab("SUNNA (AVIS MAJORITAIRE)", BLANC, 38), 510, 222, smooth((u - t0 - 1.1) / 0.35) * (1 - fin))
        if tr is not None:
            s._pose(im, s._texte_rouge("LES DÉMONS SE RÉPANDENT"), 510, 112, s._e("repandent", u, 0.4, dec=0.2))
            s._pose(im, s._lab("(CHAYÂTÎN)", BLANC, 40), 510, 196, s._e("repandent", u, 0.35, dec=0.45))
            s._pose(im, s._lab("À CE MOMENT-LÀ", BLANC, 46), 510, 256, s._e("repandent", u, 0.35, dec=0.65))
        return im

    # ---- {crepuscule porte} et {crepuscule fermee}
    def _rue_nuit_persos(s, u, front, liseré2=0.0, p2=1.0, p3=0.0, petit=True, bleu=True):
        im = s._rue(1).copy()
        if bleu:
            spr = s._perso("PETIT", back=True, couleur=(60, 110, 204), nuit=0.25)
            s._pose_perso(im, spr, s.PORTES[1] * K, 118.5 * K, 1.0, k=s.KS)
        s._panneau(im, 0, 1.0)
        s._panneau(im, 1, p2, liseré2)
        s._panneau(im, 2, p3)
        exclus = [(pc - s.DL - 4, s.PT - 4, pc + s.DL + 4, s.PB) for pc in s.PORTES]
        exclus.append((s.PETIT_R[0] - 12, 100, s.PETIT_R[0] + 12, 160))
        br = s._brume(u, front, exclus=exclus)
        if br is not None:
            im.alpha_composite(br)
        if petit:
            spr = s._perso("PETIT", "peur", sweat=True, nuit=0.2)
            s._pose_perso(im, spr, s.PETIT_R[0] * K, s.PETIT_R[1] * K, 1.0, k=s.KS)
        return im

    def _image_porte(s, u):
        tf = s.t.get("fermee")
        if s.deja:
            ez, p = 1.0, 1.0
        else:
            ez = smooth(u / 0.85)
            p = smooth((u - 0.6) / 1.1)
            if tf is not None:
                p = max(p, smooth((u - tf + 0.1) / 0.35))
        front = s.BR_MAX
        lis = 0.0
        if tf is not None:
            t_lis = max(tf, 0.6 + 1.1) if not s.deja else tf
            lis = smooth((u - t_lis) / 0.6)
            front += (s.BR_SEUIL - front) * smooth((u - tf - 0.2) / 1.5)
        im = s._rue_nuit_persos(u, front, liseré2=lis, p2=p)
        vx, vy = s.VUE_PORTE
        w = 170 + (170 / s.Z - 170) * ez
        out = s._vue(im, (vx * ez, vy * ez, w))
        # la bulle « BISMILLAH ! » sort de l'entrebâillement pendant que la porte se ferme
        if not s.deja:
            ab = smooth((u - 0.75) / 0.3) * (1 - smooth((u - 1.75) / 0.3))
            if ab > 0.01:
                b, (tx, ty) = s._bulle_cache("bism_g", "bas_gauche")
                gx = (s.PORTES[1] + s.DL - vx) * K * s.Z - 6                       # l'entrebâillement (à droite)
                gy = (s.PT + 12 - vy) * K * s.Z
                e = smooth((u - 0.75) / 0.35)
                sc = 0.7 + 0.3 * e
                bb = b if sc > 0.999 else b.resize((int(b.width * sc), int(b.height * sc)), Image.LANCZOS)
                ox, oy = min(gx + 14 - tx * sc + 10 * e, 1008 - bb.width), gy - ty * sc - 20 * e
                out.alpha_composite(_fade(bb, ab), (int(ox), int(oy)))
                s._pose(out, s._lab("= AU NOM D'ALLAH", BLANC, 40), int(ox + bb.width / 2), int(oy + bb.height + 30), ab,
                        maxw=520)
        a_haut = smooth((u - 0.2) / 0.35) if not s.deja else 1.0
        if tf is not None:
            a_haut *= 1 - smooth((u - tf) / 0.3)
        s._pose(out, s._lab("FERMEZ LES PORTES", BLANC, 60), 510, 74, a_haut)
        if tf is not None:
            s._pose(out, s._lab("LE CHAYTAN N'OUVRE PAS", BLANC, 58), 510, 70, s._e("fermee", u, 0.35, dec=0.15))
            s._pose(out, s._deux_couleurs("UNE PORTE", "FERMÉE", 62), 510, 152, s._e("fermee", u, 0.35, dec=0.35))
            ec = s._e("fermee", u, 0.45, dec=0.8)
            if ec > 0.01:
                co = s._cache.get("coche")
                if co is None:
                    co = s._cache["coche"] = _coche()
                sc = 0.6 + 0.15 * ec                    # plus petite et plus bas : entre le texte et le haut de la porte
                co_ = co.resize((int(co.width * sc), int(co.height * sc)), Image.LANCZOS)
                _colle(out, co_, (s.PORTES[1] - vx) * K * s.Z, (s.PT - 6.5 - vy) * K * s.Z, ec)
        return out

    def _bulle_cache(s, nom, pointe):
        if nom not in s._cache:
            s._cache[nom] = _bulle("BISMILLAH !", pointe=pointe)
        return s._cache[nom]

    # ---- {crepuscule claque}
    def _image_claque(s, u):
        k = s.KS
        im = s._rue(1).copy()
        s._panneau(im, 0, 1.0)
        s._panneau(im, 1, 1.0, 1.0)
        v = smooth((u - 0.05) / 0.6)                                                # Petit court vers sa porte
        x0, y0 = s.PETIT_R
        xd, yd = s.PORTES[2], 118.5
        px_, py_ = x0 + (xd - x0) * v, y0 + (yd - y0) * v
        bob = 3 * abs(math.sin(u * math.pi * 4.0)) * (1 - smooth((u - 0.6) / 0.15))     # sautillé doux
        ent = smooth((u - 0.62) / 0.22)
        exclus = [(pc - s.DL - 4, s.PT - 4, pc + s.DL + 4, s.PB) for pc in s.PORTES]
        br = s._brume(u, s.BR_SEUIL, exclus=exclus)
        if br is not None:
            im.alpha_composite(br)
        spr = s._perso("PETIT", back=True, nuit=0.2)
        s._pose_perso(im, spr, px_ * K, (py_ - 1.5 * ent) * K - bob, 1 - ent, k=k)
        p = smooth((u - 0.75) / 0.38)                                              # vite, sans rebond
        s._panneau(im, 2, p)
        e = smooth(u / 0.9)                                                         # la caméra glisse (doux) vers sa maison
        (ax, ay), (bx, by) = s.VUE_PORTE, s.VUE_CLAQUE
        vx = ax + (bx - ax) * e
        out = s._vue(im, (vx, ay, 170 / s.Z))
        ab = smooth((u - 0.85) / 0.3)                                               # « BISMILLAH ! » depuis la fenêtre
        if ab > 0.01:
            b, (tx, ty) = s._bulle_cache("bism_d", "bas_droite")
            fx = (s.FENETRES[2] + 3 - vx) * K * s.Z
            fy = (82 - ay) * K * s.Z
            out.alpha_composite(_fade(b, ab), (int(fx - tx), int(fy - ty - 16 * (1 - ab))))
        return out

    # ============================================================ {crepuscule nuit} : le plan serré
    def _decor_nuit(s):
        if "dnuit" in s._cache:
            return s._cache["dnuit"]
        c = Px(170, 160)
        S = s.SOLN
        gx0, gx1, gy0 = s.PORTE_N
        c.vgrad(c.mask_rect(0, 0, 170, 14), 0, 14, (12, 12, 38), (30, 24, 66), steps=3)
        rng = np.random.default_rng(12)
        for _ in range(10):
            x, y = int(rng.integers(2, 168)), int(rng.integers(1, 11))
            c.fill(c.mask_rect(x, y, x + 1, y + 1), (226, 222, 250))
        toit = c.mask_rect(0, 10, 170, 18)
        tc = _nuit((150, 62, 54), 0.55)
        c.shape(toit, tc, shade=_mix(tc, (0, 0, 0), 0.3), light=_mix(tc, (255, 255, 255), 0.12), sdir="bottom", band=2,
                olcol=OL)
        for tx in range(-3, 170, 8):
            c.fill(c.mask_rect(tx, 10, tx + 1, 18), _mix(tc, (0, 0, 0), 0.3))
        mur = c.mask_rect(0, 18, 170, S)
        mc = _nuit((200, 164, 110), 0.55)
        c.fill(mur, mc)
        c.dither(mur, _mix(mc, (0, 0, 0), 0.1), 0.14)
        for yy in range(24, S, 9):                                                  # crépi (traits discrets)
            for xx in range((yy * 7) % 13, 170, 19):
                c.fill(c.mask_rect(xx, yy, xx + 3, yy + 1) & mur, _mix(mc, (0, 0, 0), 0.12))
        cadre = c.mask_rect(gx0 - 3, gy0 - 3, gx1 + 3, S)
        c.shape(cadre, _nuit((120, 82, 56), 0.45), band=1, olcol=OL)
        porte = c.mask_rect(gx0, gy0, gx1, S)
        bois = _nuit(BOIS, 0.35)
        c.shape(porte, bois, shade=_mix(bois, (0, 0, 0), 0.25), light=_mix(bois, (255, 255, 255), 0.1), band=2, olcol=OL)
        for (a_, b_) in ((0.1, 0.44), (0.54, 0.92)):
            ya, yb = gy0 + (S - gy0) * a_, gy0 + (S - gy0) * b_
            pm = c.mask_rect(gx0 + 6, ya, gx1 - 6, yb) & ~c.mask_rect(gx0 + 7, ya + 1, gx1 - 7, yb - 1)
            c.fill(pm, _mix(bois, (0, 0, 0), 0.3))
        c.fill(c.mask_rect(gx1 - 7, 80, gx1 - 4, 83), (236, 196, 96))              # la poignée
        c.fill(c.mask_rect(gx0, S - 1, gx1, S), (255, 200, 110))                   # la lumière sous la porte
        fen = c.mask_rect(116, 42, 152, 82)
        c.shape(fen, (255, 214, 124), shade=(236, 170, 90), band=2, olcol=OL)
        c.fill(c.mask_rect(116, 42, 152, 82) & c.mask_ell(134, 62, 14, 16), (255, 230, 160))
        c.fill(c.mask_rect(133, 42, 135, 82), _nuit((120, 82, 56), 0.45))
        c.fill(c.mask_rect(116, 61, 152, 63), _nuit((120, 82, 56), 0.45))
        c.fill(c.mask_rect(114, 82, 154, 85), _nuit((170, 160, 160), 0.45))
        marche = c.mask_rect(gx0 - 6, S, gx1 + 6, S + 4)
        c.shape(marche, _nuit((170, 160, 160), 0.5), band=1, olcol=OL)
        tro = c.mask_rect(0, S + 4, 170, 160) | (c.mask_rect(0, S, 170, S + 4) & ~marche)
        c.fill(tro, _nuit((168, 150, 160), 0.55))
        c.dither(tro, _nuit((150, 132, 146), 0.55), 0.2)
        for xx in range(6, 170, 24):
            c.fill(c.mask_rect(xx, S + 4, xx + 1, 160), _nuit((130, 112, 126), 0.55))
        im = c.img(K).convert("RGBA")
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        _colle(lay, _lueur_px(30, 26, (255, 210, 120), niveaux=(18, 36, 56)), 134 * K, 62 * K)    # la fenêtre
        _colle(lay, _lueur_px(30, 4, (255, 204, 110), niveaux=(26, 50, 80)), 80 * K, (S + 4) * K)  # sous la porte
        m = np.zeros((160, 170), bool)                                              # le liseré doré (déjà là)
        m[gy0 - 3:S, gx0 - 3:gx1 + 3] = True
        a = np.zeros((160, 170, 4), np.uint8)
        a[_dil(m, 3) & ~m] = (*OR_DOUX, 34)
        a[_dil(m, 2) & ~m] = (*OR_DOUX, 70)
        a[_dil(m, 1) & ~m] = (*OR_DOUX, 120)
        a[S:, :] = 0
        lay.alpha_composite(Image.fromarray(a, "RGBA").resize(im.size, Image.NEAREST))
        im.alpha_composite(lay)
        s._cache["dnuit"] = im
        return im

    def _bandeau(s):
        if "bandeau" not in s._cache:
            l1 = _titre("QUAND LE DÉBUT DE LA NUIT EST PASSÉ,", BLANC, 46)
            l2 = _titre("LES ENFANTS PEUVENT RESSORTIR", BLANC, 46)
            l3 = _titre("CONSEIL : SUNNA (AVIS MAJORITAIRE)", JAUNE, 34)
            W_ = 1000
            ims = []
            for l_ in (l1, l2, l3):                 # 760 px au plus : rien sous les boutons TikTok/YouTube (x > 930)
                if l_.width > 760:
                    k_ = 760 / l_.width
                    l_ = l_.resize((int(l_.width * k_), int(l_.height * k_)), Image.LANCZOS)
                ims.append(l_)
            H_ = ims[0].height + ims[1].height + ims[2].height - 40 + 24
            out = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
            fond = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
            ImageDraw.Draw(fond).rounded_rectangle([6, 6, W_ - 6, H_ - 6], 26, fill=(14, 10, 28, 196))
            out.alpha_composite(fond.filter(ImageFilter.GaussianBlur(3)))
            y = 10
            for j, l_ in enumerate(ims):
                out.alpha_composite(l_, (int((W_ - l_.width) / 2), y))
                y += l_.height - (24 if j == 0 else 16)
            s._cache["bandeau"] = out
        return s._cache["bandeau"]

    def _image_nuit(s, u):
        im = s._decor_nuit().copy()
        S = s.SOLN
        v = smooth(u / 1.2)                                                         # Grand arrive de dos, à pas lents
        v = 0.25 * v + 0.75 * (1 - (1 - min(1.0, u / 1.2)) ** 2)
        gx = -30 + (72 + 30) * v
        bob = 5 * abs(math.sin(u * math.pi * 1.7)) * (1 - smooth((u - 1.0) / 0.25))
        spr = s._perso("GRAND", back=True, k=6, nuit=0.2)
        s._pose_perso(im, spr, gx * K, S * K - bob + 6, 1.0, k=6)
        ae = smooth((u - 1.2) / 0.25)                                               # « ! »
        if ae > 0.01:
            ex = s._cache.get("excl")
            if ex is None:
                ex = s._cache["excl"] = _bulle("!", col_txt=(214, 40, 48), size=14, k=6)
            b, (tx, ty) = ex
            hx, hy = gx * K + 70, (S - 78) * K
            im.alpha_composite(_fade(b, ae), (int(hx - tx), int(hy - ty - 14 * (1 - ae))))
        ba = smooth(u / 0.3)                                                        # le bandeau dès le début du plan (sans guillemets)
        if ba > 0.01:
            bd = s._bandeau()
            im.alpha_composite(_fade(bd, ba), (int((1020 - bd.width) / 2), int(958 - bd.height)))
        return im


# ---------------------------------------------------------------- branchement (via explique_0811.py)
CLES = ["coucher", "crepuscule", "crépuscule"]


def _norm(m):
    return m.lower().replace("é", "e").replace("è", "e").replace("ê", "e")


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique_0811.ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
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

    if k == "coucher":
        schema._ajoute(t, Coucher(brut, "coucher", qui if qui in ("PETIT", "GRAND") else "PETIT"))
    elif k == "crepuscule":
        if sous == "tombe":
            etape(Coucher, "tombe", "crepuscule", lambda: Coucher(brut, "crepuscule"))
        elif sous == "repandent":
            etape(Coucher, "repandent", "crepuscule", lambda: Coucher(brut, "crepuscule"))
        elif sous == "fermee":
            etape(Coucher, "fermee", "porte", lambda: Coucher(brut, "porte", deja=True))
        elif sous in ("porte", "claque", "nuit"):
            schema._ajoute(t, Coucher(brut, sous))
        else:
            schema._ajoute(t, Coucher(brut, "crepuscule"))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "coucher":
        return t + 3.0
    if k == "crepuscule":
        return t + dict(tombe=1.6, repandent=2.2, porte=1.9, fermee=1.6, claque=1.3, nuit=1.6).get(sous, 1.6)
    return None
