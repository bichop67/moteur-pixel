# DÉMONSTRATION EN IMAGE DU 08/11/2026 — Short ISL29 « Tu écoutes derrière la porte ? Arrête ! » (consigne +
# avertissement). Le sens propre du hadith (Boukhari 7042 : « celui qui écoute la conversation de gens alors qu'ils ne le
# veulent pas… on versera dans son oreille du plomb fondu le Jour de la Résurrection »), montré en grand, avec des
# mouvements doux (jamais de secousse ni de flash). Personne ne verse le plomb (passif du texte) : ni main, ni bras, ni
# ange, ni gardien ; aucune flamme, aucun Enfer (le texte ne le dit pas) ; rien de gore : « celui qui écoute » est une
# silhouette sombre, unie, sans visage, et l'image passe au noir AVANT que le filet touche l'oreille.
#   {oreille PETIT}    accroche, vue à ta place, la nuit : la porte fermée du salon remplit l'écran (bois chaud, poignée à
#                      droite, raie de lumière jaune dessous) ; au premier plan à gauche, la tête de Petit vue de derrière
#                      (casquette, sweat rouge), penchée, l'oreille contre le bois, sa main à plat sur la porte ; derrière
#                      le bois, des bulles floues « … », « ?! » (aucun mot lisible, personne de dessiné) et des ondes qui
#                      arrivent vers l'oreille ; la caméra avance doucement vers l'oreille (×1,00 → ×1,08 en 2 s)
#   {oreille console}  la même vue : une bulle plus nette passe derrière la porte avec une manette dedans (le cadeau
#                      qu'il avait DÉJÀ entendu : « Trop tard… ») ; la tête de Petit est déjà un peu écartée du bois
#                      dès le début (il a arrêté d'écouter : relecture religieuse du 08/11)
#   porte_salon(sc)    sur la scène (option de décor « == entree_nuit, porte_salon ») : la porte du salon FERMÉE au mur
#                      libre de l'entrée (x 410, bas 1272 ; elle ne s'ouvre jamais), la raie de lumière jaune dessous,
#                      deux bulles floues « … » qui passent au-dessus, le paillasson du décor caché (sol redessiné à
#                      l'identique) pour qu'on ne la prenne pas pour la porte d'entrée
#   {plomb}            fond sombre : le creuset en fonte, pendu à une tige qui sort du haut du cadre (personne ne le
#                      tient), le plomb fondu orange-rouge qui rougeoie, bulles lentes, chaleur qui ondule ; le petit
#                      titre « LE PLOMB FONDU » ;
#                      {plomb carte} une carte blanche glisse : « « CELUI QUI ÉCOUTE / DES GENS / MALGRÉ EUX… » » ;
#                      {plomb goutte} une silhouette de profil, sombre, neutre (sans visage ni casquette), seule
#                      l'oreille éclairée en orange ; le creuset s'incline, un mince filet de plomb est VERSÉ et descend
#                      lentement ; aux 2/3 du trajet, fondu au noir (aucun contact) ; la carte devient « « … ON LUI
#                      VERSERA / DU PLOMB FONDU / DANS L'OREILLE » » ;
#                      {plomb jour} sur le noir : « LE JOUR DE LA / RÉSURRECTION » (blanc cassé, halo orange léger,
#                      ×1,00 → ×1,04 très lent) ; une petite lueur floue reste en haut (le creuset)
#   {plomb accident}   deux cartes : à gauche (rouge doux) Petit collé à une porte, « EXPRÈS, / MALGRÉ EUX », la croix
#                      se pose ; à droite (vert doux) Petit qui s'éloigne de la porte à petits pas, « ENTENDU SANS / LE
#                      VOULOIR ? », « → ÉLOIGNE-TOI », la coche se pose sur le geste
# Zones sûres (1080 x 1920) : l'élément plein (1020 x 960) est posé au centre, haut vers y ≈ 288 ; rien d'important dans
# ses 230 px du haut pendant l'ACCROCHE ; rien d'important à droite de x ≈ 900 (écran 930 : les 150 px de droite) —
# titre « LE PLOMB FONDU » et carte verte de {plomb accident} rentrés le 08/11 (planche ISL29_el4).
# Branché par explique_0811.py (import tardif dans explique.Schema._ordre et scenario._fin_anim).
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import objets
from px import Px, TAHOMA
from pxv import smooth
from explique import _fade, _os, BLANC
from explique_0411 import OL, _peau, _sprite, _buste, _grand, _tourne
from explique_0411b import _Base, _translucide, ROUGE
from explique_0611_dette import _texte_px, _lignes, _halo, _colle

W_, H_ = 1020, 960
ORANGE_P = (255, 198, 140)                         # « LE PLOMB FONDU » (orange pâle)
ENCRE = (44, 32, 30)                               # l'encre des cartes
ROUGE_C = (186, 40, 40)                            # titres de la carte rouge
VERT_C = (28, 122, 64)                             # titres de la carte verte
CARTE1 = ("« CELUI QUI ÉCOUTE", "DES GENS", "MALGRÉ EUX… »")
CARTE2 = ("« … ON LUI VERSERA", "DU PLOMB FONDU", "DANS L'OREILLE »")


# ---------------------------------------------------------------- petits outils
def _rot(pts, a, ox, oy):
    """Tourne des points (degrés, sens des aiguilles d'une montre à l'écran) autour de l'origine, puis les décale."""
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    return [(ox + x * ca - y * sa, oy + x * sa + y * ca) for (x, y) in pts]


def _ell_pts(cx, cy, rx, ry, n=24):
    return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def _panneau(fond, r=28):
    """Image pleine (W_ x H_) aux coins arrondis à partir d'un tableau numpy RGB."""
    im = Image.fromarray(np.dstack([fond.astype(np.uint8), np.full(fond.shape[:2], 255, np.uint8)]), "RGBA")
    m = Image.new("L", (W_, H_), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, W_ - 1, H_ - 1], r, fill=255)
    im.putalpha(m)
    return im


def _croix(d, cx, cy, r, a, col=(214, 50, 50)):
    A = int(255 * a)
    for (w_, c_) in ((30, (255, 255, 255)), (18, col)):
        d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=(*c_, A), width=w_)
        d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=(*c_, A), width=w_)


def _coche(d, cx, cy, r, a, col=(40, 168, 80)):
    A = int(255 * a)
    pts = [(cx - r, cy), (cx - r * 0.3, cy + r * 0.7), (cx + r, cy - r * 0.8)]
    for (w_, c_) in ((30, (255, 255, 255)), (18, col)):
        d.line(pts, fill=(*c_, A), width=w_, joint="curve")


# ---------------------------------------------------------------- {oreille …} {plomb …}
class Ecoute(_Base):
    """{oreille PETIT} : accroche, vue à ta place : la porte du salon, la tête de Petit de dos, l'oreille contre le
    bois, des bulles floues derrière ; {oreille console} : la manette passe dans une bulle. {plomb} : le creuset de
    plomb fondu ; étapes {plomb carte|goutte|jour}. {plomb accident} : EXPRÈS, MALGRÉ EUX ✗ / SANS LE VOULOIR →
    ÉLOIGNE-TOI ✓."""
    ETAPES = ("carte", "goutte", "jour")
    PW_, PH_ = 170, 160
    # l'accroche (pixels d'écran de l'élément)
    TETE = (330, 1010)                  # milieu du bas du buste de Petit (il sort par le bas du cadre)
    OREILLE = (492, 600)                # le point vers lequel la caméra avance (≈ l'oreille dessinée, cf. _tete)
    SOURCE_ONDES = (880, 640)           # d'où partent les ondes (la conversation, derrière la porte ; sous la main)
    BULLES = ((660, 330, "…"), (860, 290, "?!"), (820, 470, "…"))
    # le creuset (pixels du dessin, ×6)
    PIVOT = (70, 5)                     # le crochet (le creuset pend à une tige qui sort du haut du cadre)
    A0, A1 = 5.0, 24.0                  # inclinaison au repos, puis quand il verse
    BEC = (42, 17)                      # le bec (repère local du creuset)
    OREILLE_S = (101, 131)              # l'oreille de la silhouette (pixels du dessin)
    T_PENCHE, T_COULE = 0.5, 2.0        # {plomb goutte} : il s'incline (0,5 s), puis le filet descend (2 s, lent :
    #                                     le noir tombe juste avant « le Jour de la Résurrection », sans trou vide)
    T_NOIR = 0.6                        # fondu au noir aux 2/3 du trajet (avant tout contact)
    CARTE_X, CARTE_Y = 302, 515        # centre de la carte (écran)

    def __init__(s, cmd, mode="plomb"):
        super().__init__(cmd)
        s.mode = mode
        s.negatif = mode in ("oreille", "console")

    def sons_el(s):
        if s.mode == "oreille":
            return [(0.0, "amb_foule_murmure", 0.018, 2.6)]
        if s.mode == "console":
            return [(0.35, "sa_ting", 0.025, None)]
        if s.mode == "accident":
            return [(0.0, "tr_whoosh_doux", 0.025, None), (0.6, "imp_tampon", 0.03, None), (1.3, "sa_ting", 0.03, None)]
        out = [(0.0, "amb_feu_camp", 0.02, 4.0)]
        if "goutte" in s.t:
            out.append((s.t["goutte"] + s.T_PENCHE, "tr_whoosh_doux", 0.022, None))
        if "jour" in s.t:
            out.append((s.t["jour"], "imp_grondement", 0.02, None))
        return out

    def image(s, u):
        if s.mode in ("oreille", "console"):
            return s._image_oreille(u)
        if s.mode == "accident":
            return s._image_accident(u)
        return s._image_plomb(u)

    def _zoom(s, im, k):
        k = round(k, 3)
        cle = ("z", id(im), k)
        if cle not in s._cache:
            if len([c for c in s._cache if c[0] == "z"]) > 40:
                for c in [c for c in s._cache if c[0] == "z"]:
                    del s._cache[c]
            s._cache[cle] = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        return s._cache[cle]

    # ============================================================ l'accroche : la porte du salon
    def _porte(s):
        """La porte intérieure, vue de très près, la nuit : deux panneaux moulurés, poignée et serrure à droite, la
        raie de lumière jaune dessous, le sol qui en reçoit un peu."""
        if "porte" in s._cache:
            return s._cache["porte"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        bois = c.mask_rect(0, 0, W, 147)
        c.fill(bois, (124, 80, 50))
        rng = np.random.default_rng(3)
        for x in range(0, W, 2):                                                   # le fil du bois
            c.tint(c.mask_rect(x, 0, x + 1, 147) & bois, (64, 36, 22), float(rng.uniform(0.04, 0.18)))
        for _ in range(9):
            x, y = int(rng.integers(4, W - 6)), int(rng.integers(4, 140))
            c.tint(c.mask_ell(x, y, 1.2, 3.5) & bois, (70, 40, 24), 0.25)
        c.fill(c.mask_rect(0, 0, 4, 147), (86, 54, 32))                            # le chambranle à gauche
        c.fill(c.mask_rect(4, 0, 5, 147), (150, 104, 66))
        for (x0, y0, x1, y1) in ((18, 10, 150, 70), (18, 82, 150, 138)):           # les deux panneaux moulurés
            c.fill(c.mask_rect(x0, y0, x1, y1), (92, 58, 34))
            c.fill(c.mask_rect(x0 + 1, y1 - 2, x1, y1), (156, 108, 70))
            c.fill(c.mask_rect(x1 - 2, y0 + 1, x1, y1), (148, 100, 64))
            inner = c.mask_rect(x0 + 3, y0 + 3, x1 - 3, y1 - 3)
            c.shape(inner, (128, 84, 52), shade=(104, 66, 40), light=(150, 102, 64), band=1, olcol=(80, 50, 30))
        ros = c.mask_ell(152, 100, 4.5, 4.5)                                       # la poignée (laiton)
        c.shape(ros, (196, 156, 70), shade=(140, 104, 40), light=(236, 204, 120), band=1, olcol=OL)
        lev = c.mask_rrect(140, 98, 154, 102, 1)
        c.shape(lev, (206, 166, 80), shade=(150, 112, 46), light=(244, 214, 134), band=1, olcol=OL)
        c.fill(c.mask_rrect(150, 108, 155, 116, 1), (190, 150, 66))                # la serrure (un peu de lumière)
        c.fill(c.mask_rect(152, 110, 153, 114), (255, 214, 120))
        c.fill(c.mask_rect(0, 147, W, 150), (255, 212, 118))                       # la raie de lumière sous la porte
        c.fill(c.mask_rect(0, 146, W, 147), (70, 44, 28))
        sol = c.mask_rect(0, 150, W, H)
        c.vgrad(sol, 150, H, (128, 96, 66), (44, 32, 34), steps=4)
        im = c.img(s.K, rgba=True)
        a = np.array(im).astype(float)                                             # la nuit : plus sombre en haut,
        yy = np.linspace(0, 1, im.height)[:, None]                                 # la lumière vient d'en bas
        ombre = 0.50 - 0.34 * yy
        a[..., :3] = a[..., :3] * (1 - ombre[..., None]) + np.array((14, 8, 22)) * ombre[..., None]
        chaud = np.clip((yy - 0.78) / 0.22, 0, 1) * 0.30
        a[..., :3] = a[..., :3] * (1 - chaud[..., None]) + np.array((255, 196, 110)) * chaud[..., None]
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")
        m = Image.new("L", (W_, H_), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, W_ - 1, H_ - 1], 28, fill=255)
        im.putalpha(m)
        s._cache["porte"] = im
        return im

    def _bulle_floue(s, sym, nette=False):
        """Une bulle de parole de l'autre côté de la porte : floue (on ne lit rien) ; nette = celle de la manette."""
        cle = ("bf", sym, nette)
        if cle in s._cache:
            return s._cache[cle]
        m = 30
        bw, bh = (230, 150) if nette else (200, 112)
        lay = Image.new("RGBA", (bw + 2 * m, bh + 40 + 2 * m), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        fond = (255, 244, 220, 255)
        d.rounded_rectangle([m, m, m + bw, m + bh], 34, fill=fond, outline=(60, 40, 40, 255) if nette else None,
                            width=6)
        d.polygon([(m + 40, m + bh - 6), (m + 84, m + bh - 6), (m + 30, m + bh + 36)], fill=fond)
        if nette:
            d.line([(m + 40, m + bh - 2), (m + 30, m + bh + 36), (m + 84, m + bh - 2)], fill=(60, 40, 40, 255), width=6)
            ic = objets.icone("manette").img(8)
            lay.alpha_composite(ic, (int(m + bw / 2 - ic.width / 2), int(m + bh / 2 - ic.height / 2)))
        else:
            f = ImageFont.truetype(TAHOMA, 64)
            d.text((m + bw / 2, m + bh / 2 + 2), sym, font=f, fill=(96, 70, 60, 255), anchor="mm")
            lay = lay.filter(ImageFilter.GaussianBlur(9))
        s._cache[cle] = lay
        return lay

    def _tete(s):
        """La tête et les épaules de Petit vues de derrière (le dessin du perso, ×20), son OREILLE droite dessinée en
        plus (peau, contour) contre la porte, les épaules prolongées vers le bas ; penchée de 6° vers la porte.
        Renvoie (image, (x, y) du pivot = milieu du bas, (x, y) de l'oreille), dans l'image tournée."""
        if "tete" in s._cache:
            return s._cache["tete"]
        a = np.array(_buste("PETIT", "neutre", back=True)[0])
        a = np.concatenate([a, np.repeat(a[-1:], 5, axis=0)], axis=0)             # les épaules continuent sous le cadre
        a = np.concatenate([a, np.zeros((a.shape[0], 3, 4), np.uint8)], axis=1)
        p = _peau("PETIT")
        for (x, y) in ((22, 9), (23, 9), (24, 10), (24, 11), (24, 12), (23, 13), (22, 13)):
            a[y, x] = (*OL, 255)                                                   # le contour de l'oreille
        for (x, y) in ((22, 10), (23, 10), (22, 11), (22, 12), (23, 12)):
            a[y, x] = (*p["b"], 255)
        a[11, 23] = (*p["s"], 255)
        a[10, 23] = (*p["h"], 255)
        K = 20
        bu = _grand(Image.fromarray(a, "RGBA"), K)
        piv = (bu.width / 2, bu.height)
        ang = -6
        im, (dx, dy) = _tourne(bu, ang, piv)
        (ox, oy), = _rot([(23.5 * K - piv[0], 11.5 * K - piv[1])], -ang, 0, 0)
        s._cache["tete"] = (im, (dx, dy), (dx + ox, dy + oy))
        return s._cache["tete"]

    def _main(s):
        """Son bras (manche rouge) et sa main à plat sur la porte (on voit le dos de la main)."""
        if "main" in s._cache:
            return s._cache["main"]
        c = Px(s.PW_, s.PH_, alpha=True)
        p = _peau("PETIT")
        b, s_, h = p["b"], p["s"], p["h"]
        X, Y = 14, -14                                                             # (à droite de l'oreille, plus haut)
        bras = _os(c, 96, 176, 87 + X, 112 + Y, 12)
        c.shape(bras, (200, 50, 50), shade=(150, 34, 40), light=(232, 92, 84), band=2, olcol=OL)
        poignet = _os(c, 85 + X, 117 + Y, 88 + X, 110 + Y, 12) & bras
        c.fill(poignet, (170, 40, 44))
        paume = c.mask_rrect(82 + X, 92 + Y, 98 + X, 108 + Y, 4)
        doigts = c.mask_rect(0, 0, 1, 1) & c.mask_rect(1, 1, 0, 0)
        for j, x in enumerate((83, 87, 91, 95)):
            doigts = doigts | c.mask_rrect(x + X, 79 + Y + (2 if j in (0, 3) else 0), x + X + 3, 95 + Y, 1)
        pouce = _os(c, 82 + X, 104 + Y, 77 + X, 95 + Y, 3.4)
        main = paume | doigts | pouce
        c.shape(main, b, shade=s_, light=h, band=1, olcol=OL)
        for x in (86, 90, 94):
            c.fill(c.mask_rect(x + X, 84 + Y, x + X + 1, 95 + Y) & main, s_)
        im = c.img(s.K, rgba=True)
        s._cache["main"] = im
        return im

    def _ondes(s, d, u, a_g=1.0):
        """Des ondes sonores qui partent de la conversation et arrivent vers l'oreille (arcs qui s'élargissent)."""
        sx, sy = s.SOURCE_ONDES
        ox, oy = s.OREILLE
        ang = math.degrees(math.atan2(oy - sy, ox - sx))
        dist = math.hypot(ox - sx, oy - sy)
        for i in range(3):
            f = (u * 0.7 + i / 3.0) % 1.0
            r = 40 + (dist - 70) * f
            a = a_g * smooth(f / 0.15) * (1 - smooth((f - 0.65) / 0.35))
            if a <= 0.02:
                continue
            bb = [sx - r, sy - r, sx + r, sy + r]
            d.arc(bb, ang - 17, ang + 17, fill=(30, 18, 20, int(170 * a)), width=22)
            d.arc(bb, ang - 15, ang + 15, fill=(255, 228, 160, int(255 * a)), width=12)

    def _image_oreille(s, u):
        console = s.mode == "console"
        _, (px_, py_), (ex_, ey_) = s._tete()
        s.OREILLE = (s.TETE[0] - px_ + ex_ + 10, s.TETE[1] - py_ + ey_)             # l'oreille dessinée (écran)
        im = s._porte().copy()
        for i, (bx, by, sym) in enumerate(s.BULLES):                               # la conversation, derrière le bois
            b = s._bulle_floue(sym)
            x = bx + 16 * math.sin(u * 0.8 + 1.7 * i)
            y = by + 8 * math.sin(u * 1.2 + 2.3 * i)
            a = 0.34 + 0.12 * math.sin(u * 2.1 + i * 1.9)
            if console and i == 2:
                a *= 1 - smooth((u - 0.2) / 0.4)
            _colle(im, b, x, y, a)
        if console:                                                                # la manette passe dans une bulle
            e = smooth((u - 0.2) / 0.5)
            if e > 0.01:
                b = s._bulle_floue("manette", nette=True)
                b_ = b if e > 0.999 else s._zoom(b, 0.85 + 0.15 * e)
                _colle(im, b_, 850 + 8 * math.sin(u * 0.9), 330 + 20 * (1 - e), 0.92 * e)
        _translucide(im, lambda d: s._ondes(d, u, 1.0 if not console else 0.3))
        dx = 12 * smooth(u / 2.0) if not console else -20.0  # il se colle… ; « console » : déjà écarté (il a arrêté),
        if not console:                                      # la main n'est plus sur la porte (relecture du 08/11)
            im.alpha_composite(s._main(), (int(dx * 0.5), 0))
        tete, (px_, py_), _ = s._tete()
        im.alpha_composite(tete, (int(s.TETE[0] + dx - px_), int(s.TETE[1] - py_)))
        z = 1.08 if console else 1.0 + 0.08 * smooth(u / 2.0)                      # la caméra avance vers l'oreille
        z += 0.004 * math.sin(2 * math.pi * u / 3.0)
        if z > 1.001:
            fx, fy = s.OREILLE
            big = im.resize((int(W_ * z), int(H_ * z)), Image.LANCZOS)
            x0, y0 = int(fx * z - fx), int(fy * z - fy)
            im2 = big.crop((x0, y0, x0 + W_, y0 + H_))
            m = Image.new("L", (W_, H_), 0)
            ImageDraw.Draw(m).rounded_rectangle([0, 0, W_ - 1, H_ - 1], 28, fill=255)
            im2.putalpha(m)
            im = im2
        return im

    # ============================================================ {plomb} : le creuset
    def _fond_plomb(s):
        """Fond sombre (brun-noir, vignette), une lueur chaude autour du creuset, la tige qui tient le crochet."""
        if "fondp" in s._cache:
            return s._cache["fondp"]
        K = s.K
        yy, xx = np.mgrid[0:H_, 0:W_].astype(float)
        cx, cy = s.PIVOT[0] * K, 210
        r = np.hypot((xx - cx) / 1.25, yy - cy)
        f = np.clip(1 - r / 760, 0, 1) ** 1.6
        fond = np.array((18, 12, 12), float) + np.array((70, 34, 20), float) * f[..., None]
        v = np.hypot((xx - W_ / 2) / (W_ / 2), (yy - H_ / 2) / (H_ / 2))
        fond *= np.clip(1.15 - 0.45 * v, 0.55, 1)[..., None]
        im = _panneau(fond)
        c = Px(s.PW_, s.PH_, alpha=True)
        tige = c.mask_rect(s.PIVOT[0] - 1, 0, s.PIVOT[0] + 2, s.PIVOT[1])
        c.shape(tige, (70, 66, 74), shade=(40, 36, 44), light=(120, 114, 124), band=1, olcol=OL)
        im.alpha_composite(c.img(K, rgba=True))
        s._cache["fondp"] = im
        return im

    def _creuset(s, a):
        """Le creuset en fonte (bec à droite, anse accrochée au crochet), incliné de a degrés autour du crochet ; le
        plomb fondu dedans (orange-rouge, cœur plus clair). Renvoie l'image (tout le cadre) en cache."""
        a = round(a * 2) / 2
        cle = ("cr", a)
        if cle in s._cache:
            return s._cache[cle]
        c = Px(s.PW_, s.PH_, alpha=True)
        ox, oy = s.PIVOT

        def P(pts):
            return c.mask_poly(_rot(pts, a, ox, oy))
        anse = None
        pts_anse = [(x, 22 * (x / 30.0) ** 2 + 1) for x in np.linspace(-30, 30, 13)]
        for (p0, p1) in zip(pts_anse[:-1], pts_anse[1:]):
            (x0, y0), (x1, y1) = _rot([p0, p1], a, ox, oy)
            seg = _os(c, x0, y0, x1, y1, 1.6)
            anse = seg if anse is None else anse | seg
        c.shape(anse, (88, 84, 92), shade=(52, 48, 56), light=(130, 124, 134), band=1, olcol=OL)
        crochet = c.mask_ell(ox, oy + 0.5, 2.2, 2.2)
        c.shape(crochet, (96, 92, 100), shade=(56, 52, 60), band=1, olcol=OL)
        bol = P([(-28, 19), (28, 19), (27, 31), (23, 44), (15, 52), (0, 55), (-15, 52), (-23, 44), (-27, 31)])
        bec = P([(25, 16), (43, 15), (43, 19.5), (26, 25)])
        oreilles = P([(-32, 20), (-27, 20), (-27, 27), (-32, 27)]) | P([(27, 20), (32, 20), (32, 27), (27, 27)])
        corps = bol | bec | oreilles
        c.shape(corps, (62, 58, 66), shade=(36, 32, 40), light=(104, 98, 108), band=2, olcol=OL)
        c.dither(bol, (48, 44, 52), 0.18)
        bord = P([(-30, 15.5), (30, 15.5), (30, 20.5), (-30, 20.5)])
        c.shape(bord, (78, 72, 80), shade=(46, 42, 50), light=(132, 124, 132), band=1, olcol=OL)
        c.tint(P([(-27, 21), (27, 21), (25, 30), (-25, 30)]) & bol, (255, 120, 40), 0.22)   # le fer rougi au bord
        plomb = c.mask_poly(_rot(_ell_pts(0, 17.5, 26, 3.4), a, ox, oy))
        c.fill(plomb, (226, 82, 26))
        c.fill(c.mask_poly(_rot(_ell_pts(-2, 17.6, 19, 2.2), a, ox, oy)), (252, 140, 44))
        c.fill(c.mask_poly(_rot(_ell_pts(-5, 17.6, 9, 1.2), a, ox, oy)), (255, 206, 120))
        c.fill(P([(28, 16.5), (42, 16), (42, 17.6), (28, 18.6)]) & bec, (240, 110, 34))     # le plomb dans le bec
        s._cache[cle] = c.img(s.K, rgba=True)
        return s._cache[cle]

    def _local(s, a, x, y):
        (X, Y), = _rot([(x, y)], a, *s.PIVOT)
        return X * s.K, Y * s.K

    def _silhouette(s):
        """« Celui qui écoute » : une silhouette de profil, sombre, unie, sans visage ni cheveux ni casquette (ce n'est
        pas Petit) ; un liseré chaud sur le haut ; seule l'oreille est éclairée en orange par la lueur du creuset."""
        if "sil" in s._cache:
            return s._cache["sil"]
        c = Px(s.PW_, s.PH_, alpha=True)
        ex, ey = s.OREILLE_S
        tete = c.mask_ell(ex - 3, ey - 1, 16, 18)
        nez = c.mask_poly([(ex - 19, ey - 4), (ex - 22.5, ey + 3), (ex - 18, ey + 6)])
        menton = c.mask_ell(ex - 9, ey + 11, 10, 7)
        cou = c.mask_poly([(ex - 9, ey + 12), (ex + 8, ey + 9), (ex + 12, 160), (ex - 8, 160)])
        epaule = c.mask_ell(ex + 14, 172, 44, 18)
        m = tete | nez | menton | cou | epaule
        c.fill(m, (44, 32, 34))
        haut = m & ~np.roll(m, 2, 0)
        c.fill(haut, (150, 76, 40))
        c.fill(m & ~np.roll(m, 1, 0), (206, 112, 52))
        c.fill(c.mask_ell(ex - 8, ey - 8, 12, 10) & m & ~haut, (56, 40, 40))
        ore = c.mask_ell(ex, ey, 3.6, 5.4)                                         # l'oreille, éclairée
        c.shape(ore, (236, 132, 60), shade=(180, 82, 36), light=(255, 196, 120), band=1, olcol=(30, 18, 18))
        c.fill(c.mask_ell(ex + 0.6, ey + 0.4, 1.4, 2.8) & ore, (168, 74, 32))
        s._cache["sil"] = c.img(s.K, rgba=True)
        return s._cache["sil"]

    def _carte(s, lignes, cle):
        """Une carte blanche (bord arrondi, ombre douce) avec la parole entre guillemets, à l'encre sombre ; la 2e ligne
        de la carte « versera » (« DU PLOMB FONDU ») à l'encre rouge orangé."""
        if cle in s._cache:
            return s._cache[cle]
        ims = []
        for i, l_ in enumerate(lignes):
            col = (184, 56, 20) if (cle == "carte2" and i == 1) else ENCRE
            ims.append(_texte_px(l_, col, 12, k=4, pad=0, gras=True))
        lw = max(i.width for i in ims)
        pad, gap = 30, 14
        cw = lw + 2 * pad
        ch = sum(i.height for i in ims) + gap * (len(ims) - 1) + 2 * pad
        out = Image.new("RGBA", (cw + 24, ch + 24), (0, 0, 0, 0))
        d = ImageDraw.Draw(out)
        d.rounded_rectangle([8, 14, cw + 14, ch + 20], 20, fill=(0, 0, 0, 110))
        d.rounded_rectangle([4, 4, cw + 4, ch + 4], 20, fill=(250, 246, 236, 255), outline=(255, 214, 160, 255),
                            width=4)
        y = 4 + pad
        for i in ims:
            out.alpha_composite(i, (int(4 + cw / 2 - i.width / 2), y))
            y += i.height + gap
        s._cache[cle] = out
        return out

    def _jour(s):
        if "jour" not in s._cache:
            s._cache["jour"] = _lignes(["LE JOUR DE LA", "RÉSURRECTION"], (246, 238, 224), 80, serre=34)
        return s._cache["jour"]

    def _image_plomb(s, u):
        K = s.K
        im = s._fond_plomb().copy()
        tg, tj = s.t.get("goutte"), s.t.get("jour")
        v = (u - tg) if tg is not None else -1.0
        a = s.A0 + 1.2 * math.sin(2 * math.pi * u / 3.2)                           # il se balance à peine…
        if v >= 0:                                                                 # … puis s'incline pour verser
            a = a + (s.A1 - a) * smooth(v / s.T_PENCHE)
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * u / 1.7)
        lx, ly = s._local(a, 0, 17.5)                                              # le centre du plomb (écran)
        _colle(im, _halo(380, 190, (255, 96, 30), 46), lx, ly + 20, 0.30 + 0.10 * pulse)
        cr = s._creuset(a)
        im.alpha_composite(cr)
        rng = np.random.default_rng(11)                                            # bulles lentes à la surface,
        bulles, chaleur = [], []                                                   # ondulation de chaleur au-dessus
        for j in range(6):
            per = float(rng.uniform(1.2, 2.0))
            ph = float(rng.uniform(0, per))
            xl = float(rng.uniform(-20, 16))
            f = ((u + ph) % per) / per
            if f < 0.7:
                bx, by = s._local(a, xl, 17.3)
                r = 3 + 6 * smooth(f / 0.5)
                bulles.append((bx, by, r, smooth(f / 0.15) * (1 - smooth((f - 0.45) / 0.25))))
        for j in range(3):
            x0 = -14 + 14 * j
            pts = []
            for k in range(12):
                yl = 12 - 4.5 * k
                pts.append(s._local(a, x0 + 2.2 * math.sin(k * 0.8 + u * 3.1 + j * 2), yl))
            chaleur.append(pts)

        def dessin(d):
            for (bx, by, r, al) in bulles:
                d.ellipse([bx - r, by - r * 0.6, bx + r, by + r * 0.6], fill=(255, 226, 150, int(220 * al)))
                d.ellipse([bx - r * 0.5, by - r * 0.3, bx + r * 0.5, by + r * 0.3], fill=(255, 150, 60, int(200 * al)))
            for k_, pts in enumerate(chaleur):
                d.line(pts, fill=(255, 176, 120, int(34 + 16 * math.sin(u * 2 + k_))), width=8)
        _translucide(im, dessin)
        # « celui qui écoute » et le filet de plomb versé
        if v >= 0:
            a_s = smooth(v / 0.4)
            _colle(im, _halo(240, 200, (255, 120, 40), 40), s.OREILLE_S[0] * K, s.OREILLE_S[1] * K, 0.20 * a_s)
            im.alpha_composite(_fade(s._silhouette(), a_s))
            w = v - s.T_PENCHE
            if w > 0:
                tx, ty = s._local(a, s.BEC[0], s.BEC[1] + 0.5)
                ex, ey = s.OREILLE_S[0] * K, s.OREILLE_S[1] * K - 30
                L_full = ey - ty
                L = L_full * (2 / 3) * min(1.0, smooth(w / s.T_COULE) * 0.4 + 0.6 * min(1.0, w / s.T_COULE))
                xs = [tx + (ex - tx) * min(1.0, (yy / max(1.0, L_full))) ** 0.5 for yy in np.linspace(0, L, 24)]
                ys = list(ty + np.linspace(0, L, 24))
                pts = [(x + 2.5 * math.sin(u * 5 + y * 0.03), y) for x, y in zip(xs, ys)]

                def filet(d):
                    d.line(pts, fill=(255, 110, 30, 70), width=44)
                    d.line(pts, fill=(214, 70, 24, 255), width=22)
                    d.line(pts, fill=(255, 176, 70, 255), width=11)
                    d.line(pts[: max(2, len(pts) * 2 // 3)], fill=(255, 232, 160, 255), width=4)
                    bx, by = pts[-1]
                    d.ellipse([bx - 12, by - 10, bx + 12, by + 14], fill=(214, 70, 24, 255))
                    d.ellipse([bx - 6, by - 6, bx + 6, by + 8], fill=(255, 176, 70, 255))
                _translucide(im, filet)
        # la carte : la parole, entre guillemets
        tc = s.t.get("carte")
        if tc is not None:
            e = smooth((u - tc) / 0.4)
            c1, c2 = s._carte(CARTE1, "carte1"), s._carte(CARTE2, "carte2")
            mix = smooth((v - 0.2) / 0.35) if v >= 0 else 0.0
            for car, al in ((c1, 1 - mix), (c2, mix)):
                if al > 0.01:
                    _colle(im, car, s.CARTE_X, s.CARTE_Y + 40 * (1 - e), e * al)
        # le petit titre (en haut à droite, sous la zone sûre du haut ; bord droit ≈ x 890 = écran 920, hors des 150 px
        # de droite)
        ti = s._lab("LE PLOMB FONDU", ORANGE_P, 46)
        s._pose(im, ti, 730, 64, smooth((u - 0.2) / 0.4), maxw=320)
        # le noir, AVANT le contact ; puis « LE JOUR DE LA RÉSURRECTION »
        noir = smooth((v - s.T_PENCHE - s.T_COULE) / s.T_NOIR) if v >= 0 else 0.0
        if tj is not None:
            noir = max(noir, smooth((u - tj) / 0.45))
        if noir > 0.001:
            lay = Image.new("RGBA", (W_, H_), (6, 4, 6, int(255 * noir)))
            im.alpha_composite(lay)
            im.putalpha(s._fond_plomb().getchannel("A"))
        if tj is not None and u >= tj:
            q = u - tj
            _colle(im, _halo(300, 120, (255, 110, 40), 50), lx, ly,                # la lueur du creuset pulse
                   (0.18 + 0.06 * math.sin(2 * math.pi * q / 1.7)) * smooth(q / 0.6))   # doucement (plan tenu)
            ej = smooth((q - 0.15) / 0.6)
            jr = s._jour()
            jz = s._zoom(jr, 1.0 + 0.04 * min(1.0, q / 3.0))
            _colle(im, _halo(jr.width + 80, jr.height + 40, (255, 120, 40), 40), W_ / 2, 500, 0.16 * ej)
            _colle(im, jz, W_ / 2, 500, ej)
        return im

    # ============================================================ {plomb accident} : la nuance
    def _mini_porte(s):
        if "mporte" in s._cache:
            return s._cache["mporte"]
        c = Px(26, 44, alpha=True)
        cadre = c.mask_rect(0, 0, 26, 42)
        c.fill(cadre, (232, 222, 206))
        c.outline(cadre, OL)
        p = c.mask_rect(3, 3, 23, 41)
        c.shape(p, (150, 98, 60), shade=(116, 74, 44), light=(178, 124, 80), band=1, olcol=OL)
        for (y0, y1) in ((6, 19), (23, 37)):
            c.outline(c.mask_rect(6, y0, 20, y1), (112, 72, 42))
        c.fill(c.mask_rect(17, 21, 21, 23), (226, 186, 90))
        c.outline(c.mask_rect(17, 21, 21, 23), OL)
        c.fill(c.mask_rect(3, 41, 23, 42), (255, 214, 110))
        c.fill(c.mask_rect(0, 42, 26, 44), (170, 160, 150))
        s._cache["mporte"] = c.img(6, rgba=True)
        return s._cache["mporte"]

    def _petit(s, face="malin", step=None, gauche=False):
        cle = ("pt", face, step, gauche)
        if cle not in s._cache:
            sp = _sprite("PETIT", "neutre", face, step=step) if step is not None else _sprite("PETIT", "neutre", face)
            sp = sp.crop(sp.getbbox())
            if gauche:
                sp = sp.transpose(Image.FLIP_LEFT_RIGHT)
            s._cache[cle] = _grand(sp, 3)
        return s._cache[cle]

    def _carte_acc(s, rouge):
        cle = ("cacc", rouge)
        if cle in s._cache:
            return s._cache[cle]
        cw, ch = 420, 610
        im = Image.new("RGBA", (cw + 16, ch + 16), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        fond, bord = ((252, 228, 224), (206, 74, 70)) if rouge else ((226, 246, 230), (58, 160, 92))
        d.rounded_rectangle([8, 12, cw + 8, ch + 12], 26, fill=(0, 0, 0, 70))
        d.rounded_rectangle([0, 0, cw, ch], 26, fill=(*fond, 255), outline=(*bord, 255), width=7)
        col = ROUGE_C if rouge else VERT_C
        lignes = ("EXPRÈS,", "MALGRÉ EUX") if rouge else ("ENTENDU SANS", "LE VOULOIR ?")
        y = 34
        for l_ in lignes:
            t_ = _texte_px(l_, col, 12, k=4, pad=0, gras=True)
            if t_.width > cw - 30:
                t_ = t_.resize((cw - 30, int(t_.height * (cw - 30) / t_.width)), Image.LANCZOS)
            im.alpha_composite(t_, (int(cw / 2 - t_.width / 2), y))
            y += t_.height + 12
        d.line([(40, y + 8), (cw - 40, y + 8)], fill=(*bord, 160), width=4)
        porte = s._mini_porte()
        im.alpha_composite(porte, (cw - porte.width - 46, 488 - porte.height))
        d.rectangle([20, 486, cw - 20, 490], fill=(*bord, 90))
        s._cache[cle] = im
        return im

    def _image_accident(s, u):
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        XL, XR, Y0 = 12, 462, 26                       # carte de droite : bord ≈ x 898 (écran 928)
        for i, (rouge, x0) in enumerate(((True, XL), (False, XR))):
            e = smooth((u - 0.4 * i) / 0.4)
            if e <= 0.01:
                continue
            ca = s._carte_acc(rouge).copy()
            porte_x = 420 - 156 - 46                                                # bord gauche de la mini-porte
            bul = s._bulle_floue("…")
            _colle(ca, s._zoom(bul, 0.55), porte_x + 70 + 6 * math.sin(u * 1.1 + i), 262 + 4 * math.sin(u * 1.6 + i),
                   0.55)
            if rouge:                                                               # collé à la porte, penché
                p = s._petit("malin")
                pr, (dx, dy) = _tourne(p, -7, (p.width / 2, p.height))
                ca.alpha_composite(pr, (int(porte_x - p.width / 2 + 4 - dx), int(486 - dy)))
                _translucide(ca, lambda d: _croix(d, 112, 552, 34, smooth((u - 0.6) / 0.3)))
            else:                                                                   # il s'éloigne à petits pas
                w = smooth((u - 0.9) / 1.4)
                marche = 0.9 < u < 2.3
                st = int((u - 0.9) * 10) % 8 if marche else None
                p = s._petit("calme", st, gauche=True)
                x_p = porte_x - p.width / 2 + 6 - 150 * w
                ca.alpha_composite(p, (int(x_p), int(486 - p.height)))
                e2 = smooth((u - 1.1) / 0.35)
                if "eloigne" not in s._cache:                                       # tient dans la carte (marges 24 px)
                    el = _texte_px("→ ÉLOIGNE-TOI", VERT_C, 12, k=4, pad=0, gras=True)
                    if el.width > 420 - 48:
                        el = el.resize((420 - 48, int(el.height * (420 - 48) / el.width)), Image.LANCZOS)
                    s._cache["eloigne"] = el
                _colle(ca, s._cache["eloigne"], 210, 556, e2)
                _translucide(ca, lambda d: _coche(d, x_p + p.width / 2, 486 - p.height - 40, 28,
                                                  smooth((u - 1.3) / 0.3)))
            im.alpha_composite(_fade(ca, e), (x0, int(Y0 + 40 * (1 - e))))
        return im


# ---------------------------------------------------------------- la porte du salon, sur la scène (entree_nuit)
_SOL = {}


def _sol_sans_paillasson():
    """Le sol de l'entrée (nuit) redessiné SANS le paillasson : mêmes carreaux, même teinte que lieux.entree("nuit")
    (contrôlé au pixel près hors du paillasson le 08/11/2026). Rectangle écran x 232-584, y 1276-1372."""
    if "sol" not in _SOL:
        import lieux
        p = lieux.Px()
        lieux.sol_carreaux(p, 318, 480, horizon=250, c1=(214, 204, 190), c2=(186, 172, 156), grout=(160, 150, 140),
                           cell=0.8)
        lieux.teinte(p, "nuit", interieur=True)
        _SOL["sol"] = p.img(4).convert("RGBA").crop((232, 1276, 584, 1372))
    return _SOL["sol"]


def porte_salon(sc, x=410, y=1272):
    """Option de décor « porte_salon [x] » (ISL29) : la porte intérieure du salon, FERMÉE (elle ne s'ouvre jamais, pas
    de bruit), au mur libre de l'entrée ; la raie de lumière jaune dessous (la famille est de l'autre côté), une lueur
    douce sur le sol, deux bulles floues « … » qui passent au-dessus (aucun mot lisible, personne de dessiné) ; le
    paillasson est caché. Petit se place contre elle avec « PETIT place 250, stop » en tête de bloc."""
    import scene
    ox_sol = 232

    def sol(img, u):                                                    # le paillasson disparaît (sol identique)
        img.alpha_composite(_sol_sans_paillasson(), (ox_sol + scene._ox(img), 1276))
    sc.anims.append(sol)
    sc.porte(x, y, t_ouvre=1e9, son=False)
    k = sc.k
    bulle = None

    def lumiere(img, u):
        nonlocal bulle
        ox = scene._ox(img)
        x0, x1 = int(x - 17 * k + 3 * k) + ox, int(x - 17 * k + 30 * k) + ox     # le battant (porte_sprite 34 x 62)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        a = 0.85 + 0.15 * math.sin(2 * math.pi * u / 2.3)
        d.rectangle([x0, y - k, x1 - 1, y - 1], fill=(255, 212, 118, int(255 * a)))          # la raie sous la porte
        d.polygon([(x0, y), (x1, y), (x1 + 34, y + 30), (x0 - 34, y + 30)], fill=(255, 210, 120, int(46 * a)))
        img.alpha_composite(lay)
        if bulle is None:                                                # une petite bulle floue « … »
            m = 16
            b = Image.new("RGBA", (120 + 2 * m, 74 + 22 + 2 * m), (0, 0, 0, 0))
            db = ImageDraw.Draw(b)
            db.rounded_rectangle([m, m, m + 120, m + 74], 26, fill=(255, 244, 220, 255))
            db.polygon([(m + 26, m + 70), (m + 54, m + 70), (m + 18, m + 96)], fill=(255, 244, 220, 255))
            db.text((m + 60, m + 36), "…", font=ImageFont.truetype(TAHOMA, 48), fill=(96, 70, 60, 255), anchor="mm")
            bulle = b.filter(ImageFilter.GaussianBlur(5))
        for i in range(2):                                               # elles passent l'une après l'autre
            f = ((u + 1.6 * i) % 3.2) / 3.2
            al = 0.5 * smooth(f / 0.2) * (1 - smooth((f - 0.7) / 0.3))
            if al > 0.02:
                bx = x - 50 + 110 * i + 10 * math.sin(u * 1.1 + i)
                by = y - 62 * k - 40 - 30 * f
                img.alpha_composite(_fade(bulle, al), (int(bx - bulle.width / 2) + ox, int(by - bulle.height / 2)))
    sc.anims.append(lumiere)
    return sc


# ---------------------------------------------------------------- branchement (via explique_0811.py)
CLES = ("oreille", "plomb")


def _norm(m):
    return m.lower().replace("é", "e").replace("è", "e").replace("ê", "e")


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique_0811.ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""

    def dernier(mode):
        return next((it["el"] for it in reversed(schema._visibles(t + 0.01))
                     if isinstance(it["el"], Ecoute) and it["el"].mode == mode), None)

    if k == "oreille":
        schema._ajoute(t, Ecoute(brut, "console" if sous == "console" else "oreille"))
    elif k == "plomb":
        if sous in Ecoute.ETAPES:
            el = dernier("plomb")
            if el is None:
                el = Ecoute(brut, "plomb")
                schema._ajoute(t, el)
            el.t[sous] = t - next(it["t_in"] for it in schema.items if it["el"] is el)
        elif sous == "accident":
            schema._ajoute(t, Ecoute(brut, "accident"))
        else:
            schema._ajoute(t, Ecoute(brut, "plomb"))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "oreille":
        return t + (1.6 if sous == "console" else 2.2)
    if k == "plomb":
        return t + dict(carte=1.4, goutte=2.9, jour=2.0, accident=2.4).get(sous, 1.0)
    return None
