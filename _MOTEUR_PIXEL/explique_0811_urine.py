# DÉMONSTRATION EN IMAGE DU 08/11/2026 — Short ISL24 « Tu sors des toilettes ? Nettoie-toi bien ! » (format
# consigne + avertissement). Même principe que les modules du 07/11 (explique_0611_dette.py) : le sens propre du hadith
# (Boukhari 216 · 6055 · Mouslim 292), montré en grand, avec des mouvements doux (jamais de secousse ni de flash).
# Rien de dégoûtant (jamais d'urine jaune, de flaque, de tache, de cuvette), aucun mort visible (niches vides et
# sombres), aucune couleur chaude autour des tombes (aucun texte ne dit la forme de leur châtiment), aucun prophète,
# ange, Compagnon ni Chaytan dessiné.
#   {gouttes PETIT}    accroche, vue à ta place : Petit sort EN COURANT d'une cabine « WC » (porte de bois clair qui
#                      s'ouvre doucement, mur carrelé neutre, AUCUNE eau : ni robinet, ni bassin, ni flaque) ; il grandit
#                      de 70 % à 100 % en 1,2 s (il vient vers toi) ; sur le bas de son pantalon et ses baskets,
#                      7 petites gouttes très pâles (crème presque transparente, ni bleu-eau ni jaune), 3 cerclées
#                      d'orange (pulsation douce 1,0 → 1,08) ; à gauche « GOUTTES // D'URINE ! » en orange et une flèche
#                      vers les baskets. Rien au niveau de l'entrejambe.
#   {tombes}           cimetière la nuit, VUE EN COUPE : ciel bleu nuit, étoiles, croissant de lune à gauche ; deux
#                      tombes (monticule de terre, pierre dressée sans inscription) ; sous terre, deux niches
#                      ENTIÈREMENT SOMBRES (ni linceul, ni forme humaine) ; entrée en glissé doux du bas (0,5 s) ;
#                      toujours une dérive lente de la caméra (le plan n'est jamais figé).
#   {tombes chaties}   ondes concentriques grises qui montent du sol au-dessus des deux tombes (les voix entendues,
#                      Boukhari 216 ; traits de 2 pixels, bien visibles) et voile froid gris-bleu qui respire au-dessus
#                      des niches (opacité 55 ↔ 85 %, 1,6 s) ; la caméra s'enfonce lentement vers les niches (zoom
#                      1,00 → 1,06 en 3 s, le décor seulement : les textes ne bougent pas) ; bandeau sombre « CHÂTIÉS
#                      DANS LEUR TOMBE » en rouge brique (seule touche chaude, en haut, loin des tombes).
#   {tombes urine}     pancarte de bois sur la tombe de GAUCHE (glisse du haut) : « IL NE SE // PROTÉGEAIT // PAS DE SON //
#                      URINE » + icône de goutte pâle cerclée ; le voile de gauche s'assombrit doucement (0,6 s).
#   {tombes namima}    même pancarte à DROITE : « IL COLPORTAIT // LES PAROLES // POUR SEMER // LA DISCORDE » (les deux
#                      dernières lignes en jaune : indispensables au sens) + icône de deux bulles reliées par une flèche ;
#                      le voile de droite s'assombrit.
#   {tombes facile}    (PLUS UTILISÉ depuis la relecture du 08/11 : la réplique « Facile à éviter… » est retirée, son
#                      explication va dans la description ; code gardé pour mémoire) badge « PAS DIFFICILE À ÉVITER ».
#   {tombes grave}     le tampon rouge (−6°) « NÉGLIGER L'URINE // = GRAND PÉCHÉ » se pose doucement dans le ciel,
#                      au-dessus de la tombe de GAUCHE (celle de l'urine) (descente 0,35 s, échelle 1,15 → 1,0, sans rebond) ; la caméra
#                      dérive lentement vers lui. (« LE NÉGLIGER » seul ne renvoyait à rien sans le son.)
# Les pancartes restent jusqu'à la fin du schéma. Zones sûres : tout le texte important est à gauche de 900 px (pixels
# de l'élément) sous le milieu de l'image, rien en haut sous l'accroche.
# Branché par explique_0811.py (import tardif dans explique.Schema._ordre et scenario._fin_anim).
import math
import unicodedata

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import cast
from px import Px
from pxv import smooth
from explique import _fade, BLANC, JAUNE
from explique_0411 import OL
from explique_0411b import _Base
from explique_0611_dette import _texte_px, _halo, _colle, _tourne_net

ORANGE_V = (255, 150, 60)          # les cercles, la flèche et « GOUTTES D'URINE ! »
ORANGE_B = (60, 26, 10)            # leur liseré sombre
GOUTTE = (240, 234, 214)           # une goutte : crème très pâle (ni bleu-eau, ni jaune)
GOUTTE_OL = (168, 160, 140)
BRIQUE = (218, 88, 68)             # « CHÂTIÉS DANS LEUR TOMBE » (sur le bandeau, loin des tombes)
VOILE = (64, 80, 108)              # le voile froid gris-bleu
VOILE_F = (22, 28, 44)             # le voile qui s'assombrit
ONDE = (150, 158, 178)             # les ondes des voix (gris)
VERT_B = (30, 84, 58)              # le badge « PAS DIFFICILE À ÉVITER »
ROUGE_T = (196, 36, 40)            # l'encre du tampon
GRIS_T = (206, 208, 218)


def _norm(m):
    m = unicodedata.normalize("NFD", m.lower())
    return "".join(ch for ch in m if unicodedata.category(ch) != "Mn")


def _bloc(lignes, k=4, gap=10, size=12):
    """Plusieurs lignes de texte pixel net (couleur par ligne), centrées, rognées au plus juste, gap pixels d'écran
    entre deux lignes. lignes = [(texte, couleur, liseré)…]."""
    ims = []
    for txt, col, bord in lignes:
        im = _texte_px(txt, col, size, k=k, bord=bord, pad=2)
        ims.append(im.crop(im.getbbox()))
    W_ = max(i.width for i in ims)
    H_ = sum(i.height for i in ims) + gap * (len(ims) - 1)
    out = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    y = 0
    for i in ims:
        out.alpha_composite(i, (int(W_ / 2 - i.width / 2), y))
        y += i.height + gap
    return out


# ---------------------------------------------------------------- {gouttes PETIT}
class Gouttes(_Base):
    """{gouttes PETIT} : accroche, vue à ta place : Petit sort en courant d'une cabine « WC » et vient vers toi ; de
    petites gouttes très pâles sur le bas de son pantalon et ses baskets, trois cerclées d'orange ; « GOUTTES //
    D'URINE ! » et une flèche vers les baskets. Aucune eau près de lui, rien au niveau de l'entrejambe."""
    PW_, PH_ = 170, 150
    PORTE = (66, 112, 20, 128)          # l'ouverture de la cabine (x0, x1, y_haut, y_bas), pixels du dessin
    K0, K1, D_K = 8.4, 12.0, 1.2        # échelle du perso : 70 % → 100 % en 1,2 s
    PIEDS0, PIEDS1 = 772, 884           # ligne des pieds (écran) au début et à la fin : il vient vers toi
    CX = 534                            # centre du perso (écran) : devant la porte
    # les gouttes (pixels du sprite de Petit, 46 × 98) : bas du pantalon et baskets ; True = cerclée
    GTS = ((16.5, 82.0, False), (25.5, 85.0, True), (20.0, 87.5, False), (27.5, 80.0, False),
           (15.5, 90.5, True), (23.5, 91.0, False), (29.0, 90.5, True))
    DROP = ("..O..", ".OXO.", ".OXO.", "OHXXO", "OXXXO", "OXXXO", ".OOO.")

    def __init__(s, cmd, who="PETIT"):
        super().__init__(cmd)
        s.who = who if who in ("PETIT", "GRAND") else "PETIT"
        s.negatif = True                                 # déjà là sur la 1re image

    def sons_el(s):
        # (pas de son de porte : _BRUITAGES n'a que « dv_porte_claque », trop sec pour une porte qui s'ouvre doucement)
        return [(0.0, "dv_pas_course_maison", 0.03, None)]

    # -- le décor : mur carrelé, devanture de la cabine, sol
    def _decor(s):
        if "decor" in s._cache:
            return s._cache["decor"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        mur = c.mask_rect(0, 0, W, 128) & tout_
        c.vgrad(mur, 0, 128, (168, 180, 192), (196, 204, 210), steps=5)
        for j, y in enumerate(range(0, 128, 10)):                                   # carreaux neutres
            c.tint(c.mask_rect(0, y, W, y + 1) & mur, (110, 120, 132), 0.45)
            for x in range(0 if j % 2 == 0 else 5, W, 10):
                c.tint(c.mask_rect(x, y, x + 1, y + 10) & mur, (110, 120, 132), 0.45)
                c.tint(c.mask_rect(x + 2, y + 2, x + 4, y + 3) & mur, (255, 255, 255), 0.18)
        x0, x1, yh, yb = s.PORTE
        panneau = c.mask_rect(x0 - 16, 6, x1 + 16, yb) & tout_                      # la devanture de la cabine
        c.shape(panneau, (214, 206, 190), shade=(176, 168, 152), light=(232, 226, 212), sdir="right", band=2,
                olcol=OL)
        for xp in (x0 - 16, x1 + 15):                                               # les pieds de la cloison
            c.fill(c.mask_rect(xp - 1, yb - 4, xp + 2, yb), (120, 124, 134))
        cadre = c.mask_rect(x0 - 3, yh - 3, x1 + 3, yb)
        c.shape(cadre, (150, 112, 74), shade=(116, 84, 54), light=(182, 142, 98), band=1, olcol=OL)
        trou = c.mask_rect(x0, yh, x1, yb)                                          # l'intérieur, dans l'ombre
        c.vgrad(trou, yh, yb, (46, 46, 56), (70, 70, 80), steps=4)
        c.fill(c.mask_rect(x0, yb - 3, x1, yb), (84, 84, 94))
        plaque = c.mask_rrect(79, 8, 99, 18, 2)                                     # la plaque « WC » (neutre)
        c.shape(plaque, (250, 250, 252), shade=(206, 210, 220), band=1, olcol=OL)
        c.text((89, 9), "WC", (36, 60, 120), size=9, anchor="ma")
        sol = c.mask_rect(0, 128, W, H) & tout_                                    # le sol carrelé
        c.vgrad(sol, 128, H, (150, 154, 162), (122, 126, 136), steps=4)
        c.fill(c.mask_rect(0, 128, W, 129) & tout_, (98, 100, 110))
        for y in (134, 142):
            c.tint(c.mask_rect(0, y, W, y + 1) & sol, (80, 84, 94), 0.4)
        for xb in range(-60, W + 70, 22):                                           # joints en perspective
            for yy in range(129, H):
                f_ = (yy - 128) / (H - 128)
                x = int(89 + (xb - 89) * (0.35 + 0.65 * f_))
                if 0 <= x < W:
                    c.tint(c.mask_rect(x, yy, x + 1, yy + 1) & sol, (80, 84, 94), 0.4)
        im = c.img(s.K, rgba=True)
        lay = Image.new("RGBA", im.size, (14, 16, 24, 90))                          # pénombre douce sur les bords
        trou_ = Image.new("L", im.size, 0)
        ImageDraw.Draw(trou_).ellipse([120, 40, 940, 900], fill=255)
        trou_ = trou_.filter(ImageFilter.GaussianBlur(100))
        a = np.array(lay)
        a[..., 3] = (a[..., 3].astype(float) * (1 - np.array(trou_) / 255.0)).astype(np.uint8)
        a[..., 3] = np.minimum(a[..., 3], np.array(im)[..., 3])
        im.alpha_composite(Image.fromarray(a, "RGBA"))
        s._cache["decor"] = im
        return im

    def _porte(s, ang):
        """Le battant de bois clair, charnière à gauche, ouvert vers toi de ang degrés (vu de face : il rétrécit)."""
        ang = int(round(ang / 3.0) * 3)
        cle = ("porte", ang)
        if cle in s._cache:
            return s._cache[cle]
        W, H = s.PW_, s.PH_
        x0, x1, yh, yb = s.PORTE
        c = Px(W, H, alpha=True)
        r = math.radians(ang)
        w = (x1 - x0) * math.cos(r)
        p = 6 * math.sin(r)                                   # le bord libre, plus près de toi, paraît plus haut
        bat = c.mask_poly([(x0, yh), (x0 - w, yh - p), (x0 - w, yb + p * 0.6), (x0, yb)])
        c.shape(bat, (226, 192, 142), shade=(190, 154, 108), light=(240, 214, 170), sdir="left", band=1, olcol=OL)
        if w > 6:
            c.fill(c.mask_rect(int(x0 - w * 0.86), int(yh + 52), int(x0 - w * 0.86) + 2, int(yh + 56)),
                   (120, 124, 134))                           # la poignée
        s._cache[cle] = c.img(s.K, rgba=True)
        return s._cache[cle]

    def _sprite(s, step):
        cle = ("spr", step)
        if cle not in s._cache:
            a = cast.dessine(cast.CAST[s.who], "neutre", "content", step=step).a
            im = Image.fromarray(a, "RGBA")
            s._cache[cle] = im.resize((im.width * 12, im.height * 12), Image.NEAREST)
        return s._cache[cle]

    def _goutte(s, dk):
        cle = ("goutte", dk)
        if cle not in s._cache:
            rows = s.DROP
            out = np.zeros((len(rows), len(rows[0]), 4), np.uint8)
            pal = {"O": (*GOUTTE_OL, 235), "X": (*GOUTTE, 215), "H": (255, 255, 255, 255)}
            for y, r_ in enumerate(rows):
                for x, ch in enumerate(r_):
                    if ch in pal:
                        out[y, x] = pal[ch]
            im = Image.fromarray(out, "RGBA")
            s._cache[cle] = im.resize((im.width * dk, im.height * dk), Image.NEAREST)
        return s._cache[cle]

    def image(s, u):
        u = max(u, 0.0)
        im = s._decor().copy()
        ang = 52 + 30 * smooth(u / 0.6)                                             # la porte finit de s'ouvrir
        im.alpha_composite(s._porte(ang))
        e = smooth(u / s.D_K)
        k = s.K0 + (s.K1 - s.K0) * e
        pieds = s.PIEDS0 + (s.PIEDS1 - s.PIEDS0) * e
        hop = -abs(math.sin(math.pi * u / 0.30)) * (10 if u < 1.4 else 4)           # sautillement de course léger
        step = int(u / 0.075) % 8
        _colle(im, _halo(30 * k, 5 * k, (20, 20, 30), 14), s.CX, pieds - 2, 0.55)
        spr = s._sprite(step)
        f_ = round(k / 12.0, 2)
        cle = ("z", step, f_)
        if cle not in s._cache:
            s._cache[cle] = spr if f_ >= 0.999 else spr.resize((int(spr.width * f_), int(spr.height * f_)),
                                                               Image.LANCZOS)
        sp = s._cache[cle]
        kk = sp.width / 46.0
        x0, y0 = s.CX - 23 * kk, pieds + hop - 94 * kk
        im.alpha_composite(sp, (int(x0), int(y0)))
        # les gouttes, puis les cercles et la flèche (sur un calque)
        dk = max(4, int(round(k * 0.62)))
        g = s._goutte(dk)
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        cibles = []
        for (gx, gy, cerc) in s.GTS:
            X, Y = x0 + gx * kk, y0 + gy * kk
            im.alpha_composite(g, (int(X - g.width / 2), int(Y - g.height / 2)))
            if cerc:
                cibles.append((X, Y))
        puls = 1.0 + 0.08 * (0.5 - 0.5 * math.cos(2 * math.pi * u / 0.9))
        wr = max(5, int(dk * 1.4))
        for i, (X, Y) in enumerate(cibles):
            R = (g.height * 0.72 + 8) * puls
            d.ellipse([X - R, Y - R, X + R, Y + R], outline=(*ORANGE_B, 210), width=wr + 6)
            d.ellipse([X - R + 3, Y - R + 3, X + R - 3, Y + R - 3], outline=(*ORANGE_V, 255), width=wr)
        lab = s._cache.get("lab")
        if lab is None:
            lab = s._cache["lab"] = _bloc([("GOUTTES", ORANGE_V, ORANGE_B), ("D'URINE !", ORANGE_V, ORANGE_B)],
                                          k=5, gap=14)
        # l'étiquette bien à gauche (elle ne touche jamais le bras de Petit, même quand il est tout près)
        lx, ly = 158, 455 + 4 * math.sin(2 * math.pi * u / 1.8)
        # la flèche : du dessous de l'étiquette vers la goutte cerclée de la basket gauche
        tx, ty = cibles[1]
        R = (g.height * 0.72 + 8) * puls
        ax0, ay0 = lx + 40, ly + lab.height / 2 + 26
        vx, vy = tx - ax0, ty - ay0
        L = math.hypot(vx, vy) or 1.0
        ux, uy = vx / L, vy / L
        bx, by = tx - ux * (R + 12), ty - uy * (R + 12)
        nx, ny = -uy, ux
        pointe = [(bx, by), (bx - ux * 46 + nx * 26, by - uy * 46 + ny * 26),
                  (bx - ux * 46 - nx * 26, by - uy * 46 - ny * 26)]
        cx_, cy_ = bx - ux * 40, by - uy * 40
        d.line([(ax0, ay0), (cx_, cy_)], fill=(*ORANGE_B, 230), width=26)
        d.polygon([(px_ + ux * 5, py_ + uy * 5) for (px_, py_) in pointe], fill=(*ORANGE_B, 230))
        d.line([(ax0, ay0), (cx_, cy_)], fill=(*ORANGE_V, 255), width=14)
        d.polygon(pointe, fill=(*ORANGE_V, 255))
        im.alpha_composite(lay)
        s._pose(im, lab, lx, ly)
        return im


# ---------------------------------------------------------------- {tombes …}
class Tombes(_Base):
    """{tombes} : deux tombes la nuit, en coupe (niches entièrement sombres, rien dedans). {tombes chaties} : ondes
    grises des voix, voile froid qui respire, « CHÂTIÉS DANS LEUR TOMBE ». {tombes urine} / {tombes namima} : une
    pancarte sur chaque tombe. {tombes facile} : « PAS DIFFICILE À ÉVITER » (plus utilisé depuis le 08/11). {tombes
    grave} : le tampon « NÉGLIGER L'URINE = GRAND PÉCHÉ » (Boukhari 216 · 6055)."""
    ETAPES = ("chaties", "urine", "namima", "facile", "grave")
    PW_, PH_ = 176, 166                 # le grand dessin (marge de 3 pixels autour pour la dérive de la caméra)
    M = 18                              # marge (écran) : on découpe 1020 × 960 dedans
    W_, H_ = 1020, 960
    G = 72                              # la surface du sol (pixels du dessin)
    XS = (40, 118)                      # centre des deux tombes (pixels du dessin)
    NICHE = (80, 99)                    # haut et bas des niches
    # positions à l'écran (pixels de l'élément)
    Y_BANDEAU = 46
    Y_BADGE, Y_SAVANTS, Y_TAMPON = 146, 226, 222   # tampon dans le ciel, au-dessus des pierres (plus de badge)
    X_TAMPON = 300                      # au-dessus de la tombe de GAUCHE (celle de l'urine), pas sur celle de la namîma
    POUSSEE, D_POUSSEE = 0.06, 3.0      # la caméra s'enfonce vers les niches à partir de « châtiés »
    Y_PANC = 752                        # centre des pancartes (sous les niches)

    def __init__(s, cmd):
        super().__init__(cmd)

    def sons_el(s):
        out = [(0.0, "tr_whoosh_doux", 0.025, None)]
        for nom, son, g, dec in (("chaties", "imp_grondement", 0.025, 0.0), ("urine", "tr_whoosh_doux", 0.02, 0.0),
                                 ("namima", "tr_whoosh_doux", 0.02, 0.0), ("facile", "sa_ting", 0.025, 0.0),
                                 ("grave", "imp_tampon", 0.03, 0.33)):
            if nom in s.t:
                out.append((s.t[nom] + dec, son, g, None))
        return out

    # -- le cimetière en coupe (fixe)
    def _fond(s):
        if "fond" in s._cache:
            return s._cache["fond"]
        W, H, G = s.PW_, s.PH_, s.G
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rect(0, 0, W, H)
        ciel = c.mask_rect(0, 0, W, G)
        c.vgrad(ciel, 0, G, (10, 14, 36), (34, 44, 82), steps=6)
        rng = np.random.default_rng(24)
        for _ in range(46):                                                         # les étoiles
            x, y = int(rng.integers(2, W - 2)), int(rng.integers(2, G - 14))
            c.px(x, y, (190, 200, 232) if rng.random() < 0.7 else (240, 244, 255))
        for (x, y) in ((30, 10), (150, 18), (96, 6)):
            for (dx, dy) in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                c.px(x + dx, y + dy, (240, 244, 255))
        lune = c.mask_ell(14, 58, 5.5, 5.5) & ~c.mask_ell(17, 56, 5, 5)             # le croissant, à gauche
        c.fill(lune, (238, 232, 196))
        c.glow(14, 58, 9, (120, 130, 170), k=0.25, m=ciel & ~c.mask_ell(14, 58, 5.5, 5.5), levels=2)
        terre = c.mask_rect(0, G + 2, W, H)
        c.vgrad(terre, G + 2, H, (74, 54, 40), (36, 26, 24), steps=6)
        c.dither(terre, (60, 44, 34), 0.22)
        for _ in range(26):                                                         # des cailloux
            x, y = int(rng.integers(4, W - 4)), int(rng.integers(G + 8, H - 4))
            if any(abs(x - X) < 26 and s.NICHE[0] - 4 < y < s.NICHE[1] + 4 for X in s.XS):
                continue
            pierre = c.mask_ell(x, y, 1.6 + rng.random() * 1.4, 1.1 + rng.random())
            c.shape(pierre, (96, 86, 78), shade=(70, 62, 56), light=(122, 112, 102), band=1, olcol=(30, 22, 20))
        for X in s.XS:
            remb = c.mask_rect(X - 15, G + 2, X + 16, s.NICHE[0])                   # la terre remise (plus claire)
            c.tint(remb, (110, 84, 62), 0.25)
            niche = c.mask_rrect(X - 20, s.NICHE[0], X + 21, s.NICHE[1], 2)
            c.fill(c.mask_rrect(X - 22, s.NICHE[0] - 2, X + 23, s.NICHE[1] + 2, 3), (44, 32, 28))
            c.fill(niche, (9, 9, 14))
            c.edge(niche, (16, 16, 22), "top", 1)
        sol = c.mask_rect(0, G - 1, W, G + 3)                                       # l'herbe sombre
        c.fill(sol, (30, 54, 40))
        c.fill(c.mask_rect(0, G + 2, W, G + 3), (22, 38, 30))
        for x in range(0, W, 3):
            h_ = 1 + (x * 7) % 3
            c.fill(c.mask_rect(x, G - 1 - h_, x + 1, G - 1), (36, 66, 46))
        for X in s.XS:
            butte = c.mask_ell(X, G + 1, 21, 6) & c.mask_rect(0, 0, W, G + 2)       # le monticule
            c.shape(butte, (104, 80, 58), shade=(78, 58, 42), light=(128, 100, 74), sdir="bottom", band=1,
                    olcol=(28, 20, 18))
            st = c.mask_rrect(X - 7, G - 18, X + 8, G - 1, 4) | c.mask_rect(X - 7, G - 12, X + 8, G - 1)
            c.shape(st, (122, 126, 136), shade=(88, 92, 104), light=(156, 160, 172), sdir="right", band=2,
                    olcol=(20, 20, 28))                                             # la pierre dressée, sans rien dessus
        im = c.img(s.K, rgba=True)
        s._cache["fond"] = im
        return im

    def _voile(s, col):
        cle = ("voile", col)
        if cle not in s._cache:
            s._cache[cle] = _halo(300, 190, col, 34)
        return s._cache[cle]

    def _ondes(s, u, a):
        """Ondes concentriques grises qui montent du sol au-dessus des deux tombes (pixels nets, ×6)."""
        W, H = s.PW_, s.PH_
        low = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(low)
        for j, X in enumerate(s.XS):
            for i in range(3):
                p = ((u / 1.9) + i / 3.0 + j * 0.17) % 1.0
                r = 4 + 15 * p
                cy = s.G - 20 - 10 * p              # au-dessus des pierres (sur la pierre, l'arc faisait une bouche)
                al = min(1.0, a * 1.5 * (1 - p) * min(1.0, p * 5))
                if al > 0.02:
                    d.arc([X - r, cy - r * 0.62, X + r, cy + r * 0.62], 200, 340, fill=(*ONDE, int(255 * al)),
                          width=2)
        return low.resize((W * s.K, H * s.K), Image.NEAREST)

    def _bandeau(s):
        if "bandeau" not in s._cache:
            t = _bloc([("CHÂTIÉS DANS LEUR TOMBE", BRIQUE, (40, 12, 12))], k=5)
            if t.width > 900:
                t = _bloc([("CHÂTIÉS DANS LEUR TOMBE", BRIQUE, (40, 12, 12))], k=4)
            b = Image.new("RGBA", (t.width + 60, t.height + 34), (0, 0, 0, 0))
            ImageDraw.Draw(b).rounded_rectangle([0, 0, b.width - 1, b.height - 1], 14, fill=(16, 12, 22, 225),
                                                outline=(70, 30, 30, 255), width=4)
            b.alpha_composite(t, (30, 17))
            s._cache["bandeau"] = b
        return s._cache["bandeau"]

    def _icone(s, quoi):
        """Petite icône ronde posée sur le haut de la pancarte : goutte pâle cerclée, ou deux bulles et une flèche."""
        c = Px(17, 17, alpha=True)
        rond = c.mask_ell(8.5, 8.5, 8, 8)
        c.shape(rond, (52, 40, 32), shade=(36, 28, 22), band=1, olcol=OL)
        if quoi == "urine":
            g = c.mask_poly([(8.5, 3), (11.5, 9), (11, 12), (8.5, 13.5), (6, 12), (5.5, 9)])
            c.fill(g, GOUTTE)
            c.outline(g, GOUTTE_OL)
            c.px(7, 10, (255, 255, 255))
            anneau = c.mask_ell(8.5, 8.5, 7.5, 7.5) & ~c.mask_ell(8.5, 8.5, 6.4, 6.4)
            c.fill(anneau, ORANGE_V)
        else:
            for (x0, x1) in ((2, 8), (10, 16)):
                b = c.mask_rrect(x0, 4, x1, 9, 2) | c.mask_poly([(x0 + 1, 8), (x0 + 3, 8), (x0 + 1, 11)])
                c.fill(b, (236, 236, 242))
                c.outline(b, (90, 90, 100))
            c.line(5, 12, 12, 12, JAUNE)
            c.line(11, 11, 12, 12, JAUNE)
            c.line(11, 13, 12, 12, JAUNE)
        return c.img(6, rgba=True)

    def _pancarte(s, quoi):
        cle = ("panc", quoi)
        if cle in s._cache:
            return s._cache[cle]
        OLT = (30, 18, 12)
        if quoi == "urine":
            lig = [("IL NE SE", BLANC, OLT), ("PROTÉGEAIT", BLANC, OLT), ("PAS DE SON", BLANC, OLT), ("URINE", BLANC, OLT)]
        else:
            lig = [("IL COLPORTAIT", BLANC, OLT), ("LES PAROLES", BLANC, OLT), ("POUR SEMER", JAUNE, OLT),
                   ("LA DISCORDE", JAUNE, OLT)]
        t = _bloc(lig, k=4, gap=12)
        if t.width > 420:
            t = _bloc(lig, k=3, gap=10)
        pw, ph = int(math.ceil((t.width + 52) / 6.0)), int(math.ceil((t.height + 70) / 6.0))
        c = Px(pw, ph, alpha=True)
        planche = c.mask_rrect(0, 0, pw, ph, 2)
        c.shape(planche, (98, 66, 42), shade=(72, 46, 30), light=(126, 88, 58), sdir="bottom", band=1, olcol=OL)
        for y in range(5, ph - 2, 6):                                               # les veines du bois
            c.tint(c.mask_rect(2, y, pw - 2, y + 1) & planche, (52, 32, 20), 0.35)
        for (x, y) in ((3, 3), (pw - 4, 3), (3, ph - 4), (pw - 4, ph - 4)):          # les clous
            c.px(x, y, (190, 190, 200))
        im = c.img(6, rgba=True)
        out = Image.new("RGBA", (im.width, im.height + 60), (0, 0, 0, 0))
        out.alpha_composite(im, (0, 60))
        out.alpha_composite(t, (int(im.width / 2 - t.width / 2), 60 + 46))
        ic = s._icone(quoi)
        out.alpha_composite(ic, (int(im.width / 2 - ic.width / 2), 0))
        s._cache[cle] = out
        return out

    def _badge(s):
        if "badge" not in s._cache:
            t = _bloc([("PAS DIFFICILE À ÉVITER", BLANC, (12, 40, 26))], k=4)
            b = Image.new("RGBA", (t.width + 64, t.height + 40), (0, 0, 0, 0))
            ImageDraw.Draw(b).rounded_rectangle([0, 0, b.width - 1, b.height - 1], 18, fill=(*VERT_B, 240),
                                                outline=(150, 220, 170, 255), width=4)
            b.alpha_composite(t, (32, 20))
            s._cache["badge"] = b
            s._cache["savants"] = _bloc([("EXPLICATION DES SAVANTS", GRIS_T, (16, 16, 24)),
                                         ("(AL-BAGHAWI, IBN DAQIQ AL-'ID)", GRIS_T, (16, 16, 24))], k=3, gap=8)
        return s._cache["badge"], s._cache["savants"]

    def _tampon(s):
        if "tampon" not in s._cache:
            t = _bloc([("NÉGLIGER L'URINE", ROUGE_T, None), ("= GRAND PÉCHÉ", ROUGE_T, None)], k=4, gap=12)
            b = Image.new("RGBA", (t.width + 70, t.height + 56), (0, 0, 0, 0))
            d = ImageDraw.Draw(b)
            d.rounded_rectangle([0, 0, b.width - 1, b.height - 1], 20, fill=(248, 240, 226, 238),
                                outline=(*ROUGE_T, 255), width=8)
            d.rounded_rectangle([14, 14, b.width - 15, b.height - 15], 12, outline=(*ROUGE_T, 255), width=3)
            b.alpha_composite(t, (35, 28))
            s._cache["tampon"] = _tourne_net(b, -6)
        return s._cache["tampon"]

    def _zoom(s, im, k, nom):
        k = round(k, 2)
        cle = ("z", nom, k)
        if cle not in s._cache:
            s._cache[cle] = im if k == 1.0 else im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))),
                                                         Image.LANCZOS)
        return s._cache[cle]

    def image(s, u):
        u = max(u, 0.0)
        K, M = s.K, s.M
        big = s._fond().copy()
        X = [x * K for x in s.XS]
        yn = (s.NICHE[0] + s.NICHE[1]) / 2 * K
        # le voile froid (respire) et son assombrissement à chaque cause
        ech = s._e("chaties", u, 0.6)
        if ech > 0.01:
            resp = 0.55 + 0.30 * (0.5 - 0.5 * math.cos(2 * math.pi * (u - s.t["chaties"]) / 1.6))
            for j, nom in enumerate(("urine", "namima")):
                _colle(big, s._voile(VOILE), X[j], yn - 30, ech * resp)
                ef = s._e(nom, u, 0.6)
                if ef > 0.01:
                    _colle(big, s._voile(VOILE_F), X[j], yn - 10, 0.5 * ef)
            big.alpha_composite(s._ondes(u - s.t["chaties"], ech))
            # la caméra s'enfonce lentement vers les niches (le décor seulement, les textes restent nets et en place)
            z = 1.0 + s.POUSSEE * s._e("chaties", u, s.D_POUSSEE)
            if z > 1.001:
                cx, cy = (s.XS[0] + s.XS[1]) / 2 * K, yn
                w_, h_ = big.size
                bx0, by0 = cx - cx / z, cy - cy / z
                big = big.resize((w_, h_), Image.LANCZOS, box=(bx0, by0, bx0 + w_ / z, by0 + h_ / z))
        # les pancartes (sous les niches), qui glissent du haut
        for j, nom in enumerate(("urine", "namima")):
            e = s._e(nom, u, 0.45)
            if e > 0.01:
                p = s._pancarte(nom)
                _colle(big, p, X[j], M + s.Y_PANC - 70 * (1 - e), e)
        # le bandeau du haut
        e = s._e("chaties", u, 0.4)
        if e > 0.01:
            _colle(big, s._bandeau(), M + s.W_ / 2, M + s.Y_BANDEAU - 24 * (1 - e), e)
        # le badge des savants
        e = s._e("facile", u, 0.4)
        if e > 0.01:
            b, sv = s._badge()
            _colle(big, b, M + s.W_ / 2, M + s.Y_BADGE + 16 * (1 - e), e)
            e2 = s._e("facile", u, 0.35, dec=0.25)
            _colle(big, sv, M + s.W_ / 2, M + s.Y_SAVANTS + 10 * (1 - e2), e2)
        # le tampon : descente douce, sans rebond
        e = s._e("grave", u, 0.35)
        if e > 0.01:
            tp = s._zoom(s._tampon(), 1.15 - 0.15 * e, "tampon")
            _colle(big, tp, M + s.X_TAMPON, M + s.Y_TAMPON - 50 * (1 - e), min(1.0, e * 1.6))
        # la caméra : entrée en glissé du bas, puis dérive lente (vers le tampon à la fin)
        ent = 1 - smooth(u / 0.5)
        eg = s._e("grave", u, 2.0)
        dx = 9 * math.sin(2 * math.pi * u / 8.0) * (1 - eg)
        dy = 7 * math.sin(2 * math.pi * u / 10.0) * (1 - eg) - 14 * eg
        ox, oy = int(round(M + dx)), int(round(M + dy - 70 * ent))
        return big.crop((ox, oy, ox + s.W_, oy + s.H_))


# ---------------------------------------------------------------- branchement (via explique_0811.py)
CLES = ("gouttes", "tombes")


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique_0811.ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    qui = mots[1].upper() if len(mots) > 1 else "PETIT"

    def dernier(cls):
        return next((it["el"] for it in reversed(schema._visibles(t + 0.01)) if isinstance(it["el"], cls)), None)

    def u_de(el):
        return t - next(it["t_in"] for it in schema.items if it["el"] is el)

    if k == "gouttes":
        schema._ajoute(t, Gouttes(brut, qui if qui in ("PETIT", "GRAND") else "PETIT"))
    elif k == "tombes":
        if sous in Tombes.ETAPES:
            el = dernier(Tombes)
            if el is None:
                el = Tombes(brut)
                schema._ajoute(t, el)
            el.t[sous] = u_de(el)
            if sous == "facile":
                # « Facile à éviter… » est l'explication des savants, pas le hadith : la source de la réplique d'avant
                # (BOUKHARI 216 · MOUSLIM 292) doit être partie avant elle. Le schéma n'affiche qu'une source à la
                # fois (la suivante la remplace en 0,25 s) : on pose une « source » vide, invisible, 0,3 s avant le
                # mot (pendant le silence entre les deux répliques). La source BOUKHARI 216 · 6055 arrive ensuite
                # avec la réplique « le négliger : grand péché ! ».
                schema.sources.append(dict(img=Image.new("RGBA", (1, 1), (0, 0, 0, 0)), t_in=t - 0.3))
        else:
            schema._ajoute(t, Tombes(brut))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "gouttes":
        return t + 1.4
    if k == "tombes":                                 # le temps de lire chaque pancarte, le badge et le tampon
        return t + dict(chaties=1.0, urine=1.2, namima=1.6, facile=1.6, grave=1.5).get(sous, 0.8)
    return None
