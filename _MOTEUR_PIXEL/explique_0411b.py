# DÉMONSTRATIONS EN IMAGE DU 04/11/2026 (soir) — 6 Shorts duo : trois « buzz » (l'homme aux cent meurtres pardonné,
# le Coran lu avec difficulté, le téléphone cassé) et trois sur l'après-mort (la tombe, le soleil du Jour du Jugement,
# le moins puni de l'Enfer). Même principe que explique_0411.py : le sens propre du hadith, montré en grand, avec des
# mouvements doux (jamais de secousse ni de flash). Aucun prophète, Compagnon ni ange dessiné : les anges sont des
# boules de lumière. Rien de sanglant : on ne montre ni meurtre, ni coup, ni brûlure de chair.
#   {cent}                  accroche : l'homme, de dos, devant sa ville la nuit ; un grand « 100 » rouge
#   {chemin}                la route entre SA VILLE (la nuit) et LE BON PAYS (l'aube) : le savant montre le chemin, il
#                           marche ; {chemin mort} il s'effondre à mi-chemin, la poitrine vers le bon pays ;
#                           {chemin anges} deux lumières « CHÂTIMENT » / « MISÉRICORDE » se disputent ;
#                           {chemin rapproche} le bon pays avance, la ville recule ; {chemin mesure} deux cordes :
#                           « PLUS PROCHE D'UN EMPAN » ; {chemin pardon} lumière dorée, « PARDONNÉ »
#                           (Boukhari 3470, Mouslim 2766)
#   {bute PETIT}            accroche : Petit, gêné, lit le Coran en butant (la lumière avance par à-coups, « ? »)
#   {double}                le Coran lu en butant ; {double lit} « +1 TU LIS » ; {double dur} « +1 C'EST DUR POUR
#                           TOI » ; {double x2} « ×2 » ; {double anges} : la lecture fluide, avec les anges nobles
#                           (Mouslim 798, Boukhari 4937)
#   {ecran}                 accroche : vu d'en haut, le téléphone tombe à tes pieds, l'écran se fend, « CRAC ! »
#   {dua}                   le téléphone fendu + « INNA LILLAHI… » ; {dua recompense} « ALLAHOUMMA AJIRNI… » et la
#                           récompense ; {dua mieux} « WA AKHLIF LI KHAYRAN MINHA » et la boîte « MIEUX » ;
#                           {dua iphone} bulle « un iPhone ? » ; {dua choisit} « C'EST ALLAH QUI CHOISIT » (Mouslim 918)
#   {tombeau}               la tombe en coupe, la nuit : le linceul, les pas de ceux qui repartent (« TAC… ») ;
#                           {tombeau anges} deux lumières descendent, il est assis, « QUE DISAIS-TU DE CET HOMME ? » ;
#                           {tombeau paradis} le croyant : sa place en Enfer se ferme, sa place au Paradis s'ouvre ;
#                           {tombeau cri} « L'HYPOCRITE ET LE MÉCRÉANT » : « JE NE SAIS PAS… » ; {tombeau crie} le cri
#                           traverse la terre : les oiseaux et le chat l'entendent, les passants humains non
#                           (Boukhari 1374)
#   {chaleur PETIT}         accroche : Petit en nage sous un soleil de plomb, au stade
#   {soleil}                le Jour du Jugement : le soleil tout près, quatre silhouettes ; {soleil mile} « 1 MILE » ;
#                           {soleil chevilles|genoux|taille|bouche} la sueur monte jusque-là (Mouslim 2864) ;
#                           {soleil ombre} une ombre douce et un jeune qui a grandi dans l'adoration d'Allah, à part
#                           (Boukhari 660) ; {soleil jeune} son étiquette
#   {brulure}               accroche : le doigt de Petit touche la poêle chaude, « AÏE ! »
#   {braises}               le moins puni de l'Enfer : une silhouette sombre, deux braises sous la plante des pieds, la
#                           chaleur qui monte, des bulles au-dessus de la tête (Boukhari 6562) ; {braises pense} bulle
#                           « PERSONNE N'EST PLUS PUNI QUE MOI » (Mouslim 213)
#   {datte}                 une datte coupée en deux, la moitié donnée, un bouclier de lumière devant le feu (Boukhari
#                           1417) ; {datte tacos} la moitié de datte devient une moitié de tacos ; {datte parole}
#                           « UNE BONNE PAROLE » (Boukhari 6540)
# Branchées dans explique.Schema._ordre (import tardif) et scenario._fin_anim, comme explique_0411.
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import objets
import pxv
from px import Px
from pxv import smooth
from explique import Element, Coran, _titre, _titres, _fade, _copie, autocollant, BLANC, JAUNE
from explique_0411 import OL, _peau, _sprite, _buste, _grand, _tourne, _goutte, _brille, _frissons

ROUGE = (240, 76, 66)
ORANGE = (255, 150, 60)
OR_ = (255, 214, 90)
VERT = (120, 226, 132)
ANGE_OR = (255, 226, 140)
ANGE_BLEU = (186, 214, 255)


# ---------------------------------------------------------------- petits outils
_ORBES = {}


def _orbe_img(r, col):
    """Boule de lumière (un ange : jamais dessiné) : cœur clair, halo doux. r en pixels d'écran."""
    cle = (int(r), col)
    if cle not in _ORBES:
        R = int(r * 3)
        lay = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for rr, al in ((2.8, 40), (2.1, 72), (1.5, 120)):
            d.ellipse([R - r * rr, R - r * rr, R + r * rr, R + r * rr], fill=(*col, al))
        lay = lay.filter(ImageFilter.GaussianBlur(max(2, r * 0.45)))
        d = ImageDraw.Draw(lay)
        clair = tuple(min(255, v + 40) for v in col)
        d.ellipse([R - r, R - r, R + r, R + r], fill=(*col, 255))
        d.ellipse([R - r * 0.72, R - r * 0.72, R + r * 0.72, R + r * 0.72], fill=(*clair, 255))
        d.ellipse([R - r * 0.52, R - r * 0.6, R - r * 0.04, R - r * 0.18], fill=(255, 255, 255, 230))
        _ORBES[cle] = lay
    return _ORBES[cle]


def _orbe(im, x, y, r, col, a=1.0):
    if a <= 0.01:
        return
    o = _orbe_img(r, col)
    im.alpha_composite(_fade(o, a), (int(x - o.width / 2), int(y - o.height / 2)))


def _deux(l1, c1, s1, l2, c2, s2):
    """Deux lignes empilées et centrées (chacune avec sa couleur et sa taille)."""
    a, b = _titre(l1, c1, s1), _titre(l2, c2, s2)
    out = Image.new("RGBA", (max(a.width, b.width), a.height + b.height - 10), (0, 0, 0, 0))
    out.alpha_composite(a, ((out.width - a.width) // 2, 0))
    out.alpha_composite(b, ((out.width - b.width) // 2, a.height - 10))
    return out


def _bulle(lignes, fond=(40, 60, 120), size=44, queue=0.5, pensee=False, pad=24):
    """Bulle sombre à texte blanc (comme la bulle « A'OUDHOU BILLAH ») ; queue = position de la pointe (fraction de la
    largeur, en bas) ; pensee = petits ronds au lieu d'une pointe."""
    tx = pxv.big_title([(l_, c_) for (l_, c_) in lignes], size=size)
    hb = tx.height + 2 * pad
    b = Image.new("RGBA", (tx.width + 2 * pad, hb + 46), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    qx = int(b.width * queue)
    if pensee:
        for j, (dx, dy, r) in enumerate(((0, 14, 11), (-12, 34, 7))):
            d.ellipse([qx + dx - r - 5, hb + dy - r - 5, qx + dx + r + 5, hb + dy + r + 5], fill=(255, 255, 255, 255))
            d.ellipse([qx + dx - r, hb + dy - r, qx + dx + r, hb + dy + r], fill=(*fond, 245))
    elif queue is not None:
        d.polygon([(qx - 24, hb - 8), (qx + 24, hb - 8), (qx, hb + 38)], fill=(255, 255, 255, 255))
        d.polygon([(qx - 15, hb - 10), (qx + 15, hb - 10), (qx, hb + 26)], fill=(*fond, 245))
    d.rounded_rectangle([0, 0, b.width - 1, hb], 26, fill=(*fond, 245), outline=(255, 255, 255, 255), width=6)
    if not pensee and queue is not None:
        d.polygon([(qx - 15, hb - 6), (qx + 15, hb - 6), (qx, hb + 26)], fill=(*fond, 245))
    b.alpha_composite(tx, (pad, pad))
    return b


def _translucide(im, dessin):
    """Dessine des formes semi-transparentes sur un calque puis les pose sur l'image (ImageDraw ne mélange pas les
    couleurs sur une image RGBA : dessiner en transparence directement y ferait des trous)."""
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dessin(ImageDraw.Draw(lay))
    im.alpha_composite(lay)


def _fleche(d, x0, y, x1, col=JAUNE, a=1.0, ep=10):
    """Petite flèche horizontale de x0 vers x1 (pixels d'écran)."""
    if a <= 0.01:
        return
    sgn = 1 if x1 > x0 else -1
    A = int(255 * a)
    d.line([(x0, y), (x1 - sgn * 18, y)], fill=(20, 16, 30, A), width=ep + 8)
    d.polygon([(x1 + sgn * 6, y), (x1 - sgn * 26, y - 22), (x1 - sgn * 26, y + 22)], fill=(20, 16, 30, A))
    d.line([(x0, y), (x1 - sgn * 18, y)], fill=(*col, A), width=ep)
    d.polygon([(x1, y), (x1 - sgn * 22, y - 16), (x1 - sgn * 22, y + 16)], fill=(*col, A))


def _silhouette(im, col, rim=None, rim_bas=None):
    """Un perso en silhouette unie (on ne voit pas son visage) ; rim = liseré clair à droite, rim_bas = lueur du bas."""
    a = np.array(im)
    m = a[..., 3] > 0
    out = np.zeros_like(a)
    out[m] = (*col, 255)
    if rim is not None:
        bord = m & ~np.roll(m, -1, axis=1)
        out[bord] = (*rim, 255)
    if rim_bas is not None:
        h = a.shape[0]
        for y in range(h):
            f = max(0.0, (y / h - 0.55) / 0.45)
            if f > 0:
                ligne = m[y]
                c = np.array(col, float) + (np.array(rim_bas, float) - np.array(col, float)) * f * 0.7
                out[y][ligne] = (*[int(v) for v in c], 255)
    return Image.fromarray(out, "RGBA")


def _flammes(c, x0, x1, base, u, haut=12, col=(214, 70, 30), coeur=(255, 170, 60), pas=12, boost=0.0):
    """Rangée de flammes (dessin Px) entre x0 et x1, pied à y = base."""
    for j, fx in enumerate(range(int(x0), int(x1), pas)):
        h = (haut + 5 * math.sin(u * 6.3 + j * 1.9) + 3 * math.sin(u * 11.7 + j)) * (1 + boost)
        w = pas * 0.62
        fl = c.mask_poly([(fx - w, base), (fx - w * 0.4, base - h * 0.55), (fx + 1.5 * math.sin(u * 8 + j), base - h),
                          (fx + w * 0.5, base - h * 0.5), (fx + w, base)])
        c.fill(fl, col)
        c.fill(c.mask_poly([(fx - w * 0.5, base), (fx, base - h * 0.6), (fx + w * 0.5, base)]), coeur)


class _Base(Element):
    """Socle commun : étapes datées (s.t), étiquettes en cache, apparitions douces."""
    plein = True
    K = 6
    PW_, PH_ = 170, 150

    def __init__(s, cmd):
        super().__init__(cmd)
        s.t = {}
        s._cache = {}

    def _lab(s, txt, col=BLANC, size=56):
        cle = ("lab", txt, col, size)
        if cle not in s._cache:
            s._cache[cle] = _titres(txt, col, size) if "//" in txt else _titre(txt, col, size)
        return s._cache[cle]

    def _pose(s, im, lab, x, y, a=1.0, maxw=None):
        """Colle une image centrée en (x, y) (pixels d'écran), réduite si trop large, sans sortir du cadre."""
        if a <= 0.01:
            return
        maxw = maxw or im.width - 16
        if lab.width > maxw:
            cle = ("r", id(lab), int(maxw))
            if cle not in s._cache:
                k_ = maxw / lab.width
                s._cache[cle] = lab.resize((int(lab.width * k_), int(lab.height * k_)), Image.LANCZOS)
            lab = s._cache[cle]
        x0 = int(max(8, min(im.width - lab.width - 8, x - lab.width / 2)))
        y0 = int(max(0, min(im.height - lab.height, y - lab.height / 2)))
        im.alpha_composite(_fade(lab, a), (x0, y0))

    def _e(s, nom, u, d=0.35, dec=0.0):
        """Avancement doux (0 → 1) depuis l'étape nom (+ décalage) ; 0 si l'étape n'a pas encore eu lieu."""
        t0 = s.t.get(nom)
        if t0 is None or u < t0 + dec:
            return 0.0
        return smooth((u - t0 - dec) / d)

    def _a(s, nom, u, d=0.3, fin=None, dfin=0.3, dec=0.0):
        """Opacité : apparaît à l'étape nom, disparaît à l'étape fin (si elle a lieu)."""
        a = s._e(nom, u, d, dec)
        if fin is not None:
            for f_ in (fin if isinstance(fin, tuple) else (fin,)):
                if f_ in s.t and u >= s.t[f_]:
                    a *= 1 - smooth((u - s.t[f_]) / dfin)
        return a


# ---------------------------------------------------------------- {cent} {chemin …}
class Chemin(_Base):
    """{cent} : accroche (l'homme de dos devant sa ville, la nuit, « 100 » en rouge). {chemin} : la route, de SA VILLE
    (la nuit) vers LE BON PAYS (l'aube) ; étapes {chemin mort|anges|rapproche|mesure|pardon} (Boukhari 3470 :
    « Allah ordonna à celle-ci de se rapprocher et à celle-là de s'éloigner… il en était plus proche d'un empan : il
    fut pardonné » ; Mouslim 2766 : le savant, « des gens y adorent Allah », mort à mi-chemin)."""
    PW_, PH_ = 186, 150
    ROUTE = 100                   # haut de la route (pixels du dessin)
    SOL = 108                     # les pieds sur la route
    XG, XD = 47, 147              # bord de la ville (à gauche) et du bon pays (à droite), au début
    PAS = 5                       # de combien chaque ville se déplace
    X0, XM = 54, 77               # départ et endroit où il meurt (ses pieds)
    KP = 2                        # échelle des persos sur la route
    LONG = 98 * 2 / 6             # longueur du corps couché (pixels du dessin)
    ETAPES = ("part", "mort", "anges", "rapproche", "mesure", "pardon")

    def __init__(s, cmd, mode="chemin"):
        super().__init__(cmd)
        s.mode = mode
        s.negatif = mode == "cent"

    def sons_el(s):
        if s.mode == "cent":
            return [(0.0, "imp_grondement", 0.025, None)]
        out = [(0.2, "dv_pas_sable", 0.03, None)]
        for nom, son, g in (("mort", "tr_whoosh_doux", 0.03), ("rapproche", "tr_whoosh_vent", 0.04),
                            ("mesure", "sa_ting", 0.03), ("pardon", "sa_scintillement", 0.05)):
            if nom in s.t:
                out.append((s.t[nom], son, g, None))
        return out

    # -- le décor
    def _fond(s, nuit=False):
        cle = ("fond", nuit)
        if cle in s._cache:
            return s._cache[cle]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        nuit_h, nuit_b = (22, 18, 46), (58, 42, 80)
        aube_h, aube_b = (78, 92, 150), (252, 172, 112)
        for x in range(0, W, 8):
            f = 0.0 if nuit else x / (W - 1)
            f = f * f * (3 - 2 * f)
            h_ = tuple(int(a + (b - a) * f) for a, b in zip(nuit_h, aube_h))
            b_ = tuple(int(a + (b - a) * f) for a, b in zip(nuit_b, aube_b))
            c.vgrad(tout_ & c.mask_rect(x, 0, x + 8, 92), 0, 92, h_, b_, steps=6)
        rng = np.random.default_rng(5)
        for _ in range(40 if nuit else 24):
            x, y = int(rng.integers(2, W if nuit else 86)), int(rng.integers(2, 64))
            c.px(x, y, (232, 232, 255))
        if nuit:
            c.fill(c.mask_ell(150, 22, 8, 8), (240, 236, 210))                     # la lune
            c.fill(c.mask_ell(153, 20, 7, 7), nuit_h)
        else:
            ciel = c.mask_rect(0, 0, W, 92) & tout_                               # le soleil se lève derrière le bon pays
            c.fill(c.mask_ell(166, 92, 19, 19) & ciel, (255, 206, 140))
            c.fill(c.mask_ell(166, 92, 13, 13) & ciel, (255, 232, 186))
        sol = c.mask_rect(0, 88, W, H) & tout_
        c.vgrad(sol, 88, H, (150, 116, 84) if not nuit else (86, 66, 62), (112, 82, 60) if not nuit else (58, 44, 44), steps=5)
        dune = c.mask_poly([(0, 92), (34, 86), (64, 90), (100, 84), (136, 89), (186, 85), (186, 96), (0, 96)]) & tout_
        c.fill(dune, (130, 100, 76) if not nuit else (74, 58, 56))
        route = c.mask_rect(0, s.ROUTE, W, s.ROUTE + 13) & tout_
        c.fill(route, (198, 166, 122) if not nuit else (110, 92, 84))
        c.dither(route, (178, 148, 108) if not nuit else (96, 80, 74), 0.25)
        c.fill(c.mask_rect(0, s.ROUTE, W, s.ROUTE + 1) & tout_, (216, 188, 146) if not nuit else (124, 106, 96))
        for x in range(4, W, 9):
            c.px(x, s.ROUTE + 15 + (x * 7) % 6, (96, 70, 52) if not nuit else (60, 46, 44))
        s._cache[cle] = c.img(s.K, rgba=True)
        return s._cache[cle]

    def _ville(s, bonne):
        cle = ("ville", bonne)
        if cle in s._cache:
            return s._cache[cle]
        W, H = 46, 64
        c = Px(W, H, alpha=True)
        if bonne:
            murs, ombre, clair, fen = (236, 214, 176), (196, 168, 130), (252, 236, 206), (255, 216, 100)
            maisons = [(3, 30, 16, 64), (14, 20, 29, 64), (27, 33, 39, 64), (35, 25, 46, 64)]
        else:
            murs, ombre, clair, fen = (66, 56, 84), (46, 38, 62), (86, 74, 104), (150, 58, 60)
            maisons = [(0, 28, 13, 64), (11, 17, 27, 64), (25, 31, 37, 64), (33, 23, 45, 64)]
        if bonne:                                                                  # palmiers derrière les maisons
            for px_ in (9, 31):
                tronc = c.mask_rect(px_, 12, px_ + 2, 40)
                c.shape(tronc, (132, 98, 62), shade=(100, 72, 44), band=1, olcol=OL)
                for ang in (-160, -120, -60, -20):
                    a = math.radians(ang)
                    pts = [(px_ + 1, 12), (px_ + 1 + 12 * math.cos(a), 12 + 12 * math.sin(a) + 5),
                           (px_ + 1 + 8 * math.cos(a), 12 + 8 * math.sin(a) + 7)]
                    c.fill(c.mask_poly(pts), (62, 162, 82))
        for (x0, y0, x1, y1) in maisons:
            m = c.mask_rect(x0, y0, x1, y1)
            c.shape(m, murs, shade=ombre, light=clair, band=1, olcol=OL)
            c.fill(c.mask_rect(x0, y0, x1, y0 + 2), ombre)
            for wy in range(y0 + 6, y1 - 10, 9):
                for wx in range(x0 + 3, x1 - 3, 6):
                    c.fill(c.mask_rect(wx, wy, wx + 2, wy + 3), fen)
            mx = (x0 + x1) // 2
            c.fill(c.mask_rect(mx - 2, y1 - 9, mx + 2, y1), ombre)
        s._cache[cle] = c.img(s.K, rgba=True)
        return s._cache[cle]

    def _homme(s, step=None, back=False):
        cle = ("h", step, back)
        if cle not in s._cache:
            kw = dict(back=back)
            if step is not None:
                kw["step"] = step
            s._cache[cle] = _sprite("VOYAGEUR", "neutre", "triste", **kw)
        return s._cache[cle]

    def _savant(s):
        if "sav" not in s._cache:
            s._cache["sav"] = _grand(_sprite("SAGE", "pointe", "calme"), s.KP)
        return s._cache["sav"]

    # -- l'accroche
    def _image_cent(s, u):
        K = s.K
        im = s._fond(nuit=True).copy()
        W_, H_ = im.size
        v = s._ville(False)
        for j in range(3):
            im.alpha_composite(v, (int(W_ / 2 - 1.5 * v.width + j * v.width), int((s.ROUTE - 64) * K)))
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))                            # brume froide au pied des maisons
        ImageDraw.Draw(lay).rectangle([0, (s.ROUTE - 10) * K, W_, (s.ROUTE + 4) * K], fill=(30, 24, 50, 120))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(20)))
        h = _grand(s._homme(None, back=True), 4)
        hx, hy = W_ / 2 - h.width / 2, (s.SOL + 22) * K - h.height
        d = ImageDraw.Draw(im)
        d.ellipse([W_ / 2 - 90, (s.SOL + 21) * K - 16, W_ / 2 + 90, (s.SOL + 21) * K + 16], fill=(10, 8, 20, 150))
        im.alpha_composite(h, (int(hx), int(hy)))
        cent = s._cache.setdefault("100", _titre("100", ROUGE, 230, r=5))
        e = smooth((u + 0.5) / 0.6)
        k2 = 0.9 + 0.1 * e
        c2 = cent.resize((int(cent.width * k2), int(cent.height * k2)), Image.LANCZOS)
        halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        hd = ImageDraw.Draw(halo)
        cx, cy = W_ / 2, 150
        al = int((70 + 40 * math.sin(u * 3)) * e)
        hd.ellipse([cx - 260, cy - 110, cx + 260, cy + 110], fill=(255, 40, 40, al))
        im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(40)))
        im.alpha_composite(_fade(c2, e), (int(cx - c2.width / 2), int(cy - c2.height / 2)))
        z = 1.0 + 0.07 * smooth((u + 0.5) / 4.5)                                   # on s'approche lentement de lui
        if z > 1.001:
            w2, h2 = int(W_ / z), int(H_ / z)
            x0, y0 = (W_ - w2) // 2, int((H_ - h2) * 0.62)
            im = im.crop((x0, y0, x0 + w2, y0 + h2)).resize((W_, H_), Image.BILINEAR)
        return im

    # -- la route
    def image(s, u):
        if s.mode == "cent":
            return s._image_cent(u)
        K = s.K
        im = s._fond().copy()
        W_, H_ = im.size
        d = ImageDraw.Draw(im)
        e_r = s._e("rapproche", u, 1.4)
        xg = s.XG - s.PAS * e_r                                                    # la ville recule
        xd = s.XD - s.PAS * e_r                                                    # le bon pays avance
        vg, vd = s._ville(False), s._ville(True)
        im.alpha_composite(vg, (int((xg - 46) * K), int((s.ROUTE - 64) * K)))
        im.alpha_composite(vd, (int(xd * K), int((s.ROUTE - 64) * K)))
        # étiquettes des deux pays
        s._pose(im, s._lab("SA VILLE // UNE TERRE DU MAL", (200, 180, 255), 46), (xg - 23) * K, 18 * K, 1.0, maxw=330)
        s._pose(im, s._lab("LE BON PAYS // ON Y ADORE ALLAH", OR_, 46), (xd + 20) * K, 18 * K, 1.0, maxw=360)
        # le savant (au départ) : il montre le chemin, puis on le laisse derrière
        a_sav = 1 - s._e("mort", u, 0.6)
        if a_sav > 0.01:
            sv = s._savant()
            im.alpha_composite(_fade(sv, a_sav), (int(30 * K - sv.width / 2), int(s.SOL * K - sv.height + 2)))
        # le chemin à prendre : une ligne dorée qui part vers le bon pays (sur « Va… »)
        if "part" in s.t:
            f = smooth((u - s.t["part"]) / 1.2) * (1 - s._e("mort", u, 0.5))
            if f > 0:
                y_ = (s.ROUTE + 7) * K
                x_a, x_b = s.X0 * K, (s.X0 + (xd - s.X0) * min(1.0, smooth((u - s.t["part"]) / 1.2))) * K

                def chemin_dore(dd):
                    xx = x_a
                    while xx < x_b:
                        dd.rectangle([xx, y_ - 5, min(x_b, xx + 26), y_ + 5], fill=(255, 214, 90, int(230 * f)))
                        xx += 44
                _translucide(im, chemin_dore)
        # sa question (Mouslim 2766 : « y a-t-il un repentir pour lui ? »), puis la réponse du savant
        tp_ = s.t.get("part")
        aq = smooth((u - 0.3) / 0.35) * (1 - smooth((u - tp_) / 0.3) if tp_ is not None else 1.0)
        if aq > 0.01:
            b = s._cache.get("bq")
            if b is None:
                b = s._cache["bq"] = _bulle([("« Y A-T-IL UN REPENTIR", BLANC), ("POUR MOI ? »", BLANC)], fond=(70, 46, 96),
                                            size=38, queue=0.35)
            im.alpha_composite(_fade(b, aq), (int(max(10, s.X0 * K - b.width * 0.35)),
                                              int(s.SOL * K - 210 - b.height + 10 * (1 - aq))))
        if tp_ is not None:
            ar = smooth((u - tp_) / 0.35) * (1 - smooth((u - tp_ - 2.8) / 0.4)) * (1 - s._e("mort", u, 0.3))
            if ar > 0.01:
                b = s._cache.get("bs")
                if b is None:
                    b = s._cache["bs"] = _bulle([("« VA DANS TEL PAYS :", BLANC), ("DES GENS Y ADORENT ALLAH »", JAUNE)],
                                                fond=(40, 80, 60), size=38, queue=0.18)
                im.alpha_composite(_fade(b, ar), (int(max(10, 30 * K - b.width * 0.18)),
                                                  int(s.SOL * K - 220 - b.height + 10 * (1 - ar))))
        # l'homme : il marche vers le bon pays, puis s'effondre, la poitrine vers lui
        tm = s.t.get("mort")
        tp = s.t.get("part", 0.0)                                                  # il part sur « Va… »
        if tm is None or u < tm:
            duree = (tm if tm is not None else tp + 4.5) - tp
            f = min(1.0, max(0.0, (u - tp) / max(0.6, duree)))
            xp = s.X0 + (s.XM - s.X0) * f
            spr = s._homme(int(u * 7) % 8 if (u >= tp and f < 1) else None)
            angle = 0.0
        else:
            xp = s.XM
            spr = s._homme(None)
            angle = -86 * smooth((u - tm) / 0.9)
        big = _grand(spr, s.KP)
        piv = (23 * s.KP, 96 * s.KP)
        rot, (dx, dy) = _tourne(big, angle, piv)
        ombre_l = 50 + 60 * abs(angle) / 86
        bx_ = [xp * K - 30 + (abs(angle) / 86) * 90 - ombre_l / 2, s.SOL * K - 8,
               xp * K + 30 + (abs(angle) / 86) * 90 + ombre_l / 2, s.SOL * K + 10]
        _translucide(im, lambda dd: dd.ellipse(bx_, fill=(40, 26, 20, 90)))
        im.alpha_composite(rot, (int(xp * K - dx), int(s.SOL * K - dy)))
        centre = s.XM + s.LONG / 2                                                  # le milieu du corps couché
        # les deux lumières (anges) qui se disputent : jamais dessinés
        ea = s._e("anges", u, 0.8)
        ep = s._e("pardon", u, 0.9)
        if ea > 0:
            v = u - s.t["anges"]
            for j, (col, l1, l2, dxo) in enumerate(((ANGE_BLEU, "ANGES DU", "CHÂTIMENT", -33),
                                                    (ANGE_OR, "ANGES DE LA", "MISÉRICORDE", 33))):
                x = (centre + dxo) * K
                y = (60 - 9 * (1 - smooth(v / 0.9)) + 2.5 * math.sin(u * 2.2 + j * 2.1)) * K
                a = ea
                r = 7 * K * (1 + 0.12 * math.sin(u * 5 + j * math.pi))             # l'une puis l'autre : la dispute
                if j == 0:
                    a *= 1 - ep
                elif ep > 0:                                                       # la miséricorde l'emporte
                    x = x + (centre * K - x) * ep
                    y = y + ((s.SOL - 14) * K - y) * ep
                _orbe(im, x, y, r, col, a)
                s._pose(im, s._deux(l1, BLANC, 34, l2, col, 46), x, y - 14 * K, a * (1 - ep), maxw=340)
        # le bon pays avance, la ville recule (deux flèches pendant le mouvement)
        if "rapproche" in s.t:
            v = u - s.t["rapproche"]
            a = smooth(v / 0.3) * (1 - smooth((v - 1.6) / 0.4))
            if a > 0:
                _translucide(im, lambda dd: (
                    _fleche(dd, (xd + 4) * K + 40, (s.ROUTE + 22) * K, (xd + 4) * K - 60, OR_, a),
                    _fleche(dd, (xg - 4) * K + 40, (s.ROUTE + 22) * K, (xg - 4) * K - 60, (200, 180, 255), a)))
        # on mesure : deux cordes, du corps à chaque pays
        if "mesure" in s.t:
            v = u - s.t["mesure"]
            yc = (s.ROUTE + 26) * K
            for j, (x_bout, col) in enumerate(((xg, (200, 180, 255)), (xd, OR_))):
                f = smooth((v - 0.55 * j) / 0.5)
                if f <= 0:
                    continue
                x_a, x_b = centre * K, (centre + (x_bout - centre) * f) * K
                lo, hi = min(x_a, x_b), max(x_a, x_b)
                d.line([(lo, yc), (hi, yc)], fill=(20, 16, 30, 255), width=16)
                xx = lo
                while xx < hi:
                    d.line([(xx, yc), (min(hi, xx + 22), yc)], fill=(*col, 255), width=8)
                    xx += 34
                for xb in (x_a, x_b):
                    d.ellipse([xb - 9, yc - 9, xb + 9, yc + 9], fill=(*col, 255), outline=(20, 16, 30, 255), width=3)
            a = smooth((v - 1.2) / 0.35)
            s._pose(im, s._deux("PLUS PROCHE", JAUNE, 58, "D'UN EMPAN (≈ 22 CM)", BLANC, 40), (centre + xd) / 2 * K + 40,
                    (s.ROUTE + 37) * K, a, maxw=560)
        # pardonné : lumière dorée sur lui
        if ep > 0:
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            cx = centre * K
            ld.polygon([(cx - 70, 0), (cx + 70, 0), (cx + 190, (s.SOL + 2) * K), (cx - 190, (s.SOL + 2) * K)],
                       fill=(255, 226, 140, int(110 * ep)))
            ld.ellipse([cx - 230, (s.SOL - 16) * K, cx + 230, (s.SOL + 8) * K], fill=(255, 236, 170, int(120 * ep)))
            im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(26)))
            zone = (int(cx - 200), int((s.SOL - 30) * K), int(cx + 200), int((s.SOL - 2) * K))
            _translucide(im, lambda dd: _brille(dd, np.random.default_rng(int(u * 6)), zone, 5, K, int(230 * ep)))
            s._pose(im, s._lab("PARDONNÉ", OR_, 96), cx, 70 * K, ep, maxw=700)
        return im

    def _deux(s, l1, c1, s1, l2, c2, s2):
        cle = ("deux", l1, l2)
        if cle not in s._cache:
            s._cache[cle] = _deux(l1, c1, s1, l2, c2, s2)
        return s._cache[cle]


# ---------------------------------------------------------------- {bute PETIT} {double …}
class Double(_Base):
    """{bute PETIT} : accroche, Petit gêné lit le Coran en butant. {double} : le Coran lu en butant ; {double lit},
    {double dur}, {double x2} : « +1 TU LIS », « +1 C'EST DUR POUR TOI », « ×2 ». {double anges} : la lecture
    fluide avec les anges nobles ; « CELUI QUI LIT BIEN EST MEILLEUR » (Mouslim 798 ; an-Nawawi)."""
    PAS = 0.42
    BUTE = [0, 1, 1, 0, 1, 2, 2, 3, 2, 3, 3, 4, 5, 4, 5, 6, 6, 7, 6, 7, 8]
    ETAPES = ("lit", "dur", "x2")

    def __init__(s, cmd, mode="double", who="PETIT"):
        super().__init__(cmd)
        s.mode = mode
        s.who = who
        s.negatif = mode == "bute"
        s.co = Coran("coran")

    def sons_el(s):
        out = []
        for nom, son, g in (("lit", "sa_ting", 0.03), ("dur", "sa_ting", 0.03), ("x2", "sa_scintillement", 0.045)):
            if nom in s.t:
                out.append((s.t[nom], son, g, None))
        if s.mode == "anges":
            out.append((0.3, "sa_scintillement", 0.04, None))
        return out

    @staticmethod
    def _lettre(li, col_, ox, oy):
        return ox + (186 - 4 - col_ * 7.3) * 5, oy + (24 + li * 12) * 5

    def _lumiere(s, d, xl, yl, fort=1.0):
        d.rounded_rectangle([xl - 46, yl - 34, xl + 46, yl + 48], 12, fill=(255, 214, 70, int(105 * fort)))
        d.rounded_rectangle([xl - 28, yl - 20, xl + 28, yl + 34], 9, fill=(255, 226, 110, int(160 * fort)))

    def _bute(s, im, u, ox, oy):
        """La lecture qui bute : la lumière avance d'une lettre, recule, hésite ; un « ? » quand ça bloque."""
        i = int(max(0.0, u + 0.6) / s.PAS)
        i = min(i, len(s.BUTE) - 1)
        xl, yl = s._lettre(0, s.BUTE[i], ox, oy)
        _translucide(im, lambda dd: s._lumiere(dd, xl, yl))
        q = s._cache.setdefault("q", _titre("?", JAUNE, 96, r=4))
        for j in range(1, i + 1):
            if s.BUTE[j] <= s.BUTE[j - 1]:                                         # bloqué ou retour en arrière
                v = max(0.0, u + 0.6) - j * s.PAS
                if 0 <= v < 0.9:
                    a = smooth(v / 0.15) * (1 - smooth((v - 0.5) / 0.4))
                    x2, y2 = s._lettre(0, s.BUTE[j], ox, oy)
                    im.alpha_composite(_fade(q, a), (int(x2 + 20), int(max(0, y2 - q.height - 20 - 40 * v))))

    def image(s, u):
        livre = s.co.livre()
        W_, H_ = 1020, 960
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        if s.mode == "bute":
            ox, oy = 10, 130
            im.alpha_composite(livre, (ox, oy))
            s._bute(im, u, ox, oy)
            cle = ("buste", s.who)
            if cle not in s._cache:
                b, _ = _buste(s.who, "gene", sweat=True, blush=True)
                s._cache[cle] = _grand(b, 14)
            bus = s._cache[cle]
            bx, by = -10, H_ - bus.height
            im.alpha_composite(bus, (bx, by))
            g_ = s._cache.setdefault("g", _goutte((150, 214, 255), k=6))              # gouttes de gêne sur le front
            for j, (gx, gy, dec) in enumerate(((bx + 242, by + 110, 0.0), (bx + 318, by + 152, 0.7))):
                v = ((u + 2 + dec) % 1.4) / 1.4
                a = smooth(v / 0.15) * (1 - smooth((v - 0.75) / 0.25))
                im.alpha_composite(_fade(g_, a), (int(gx), int(gy + 70 * v)))
            return im
        ox, oy = 10, 200
        im.alpha_composite(livre, (ox, oy))
        if s.mode == "anges":                                                       # celui qui lit bien : fluide
            n = int(max(0.0, u) / 0.11)
            li, col_ = divmod(n, 11)
            li %= 8
            xl, yl = s._lettre(li, col_, ox, oy)
            _translucide(im, lambda dd: s._lumiere(dd, xl, yl, 0.9))
            for j, (x, y) in enumerate(((70, 250), (950, 250), (70, 820), (950, 820), (510, 175))):
                a = smooth((u - 0.15 * j) / 0.5)
                _orbe(im, x + 10 * math.sin(u * 1.7 + j), y + 12 * math.sin(u * 2.1 + j * 1.3), 26, ANGE_OR, a)
            s._pose(im, s._cache.setdefault("t_ang", _deux("CELUI QUI LE MAÎTRISE", BLANC, 60,
                                                            "EST AVEC LES ANGES NOBLES ET PIEUX", JAUNE, 46)),
                    W_ / 2, 90, smooth(u / 0.4))
            s._pose(im, s._lab("ET IL RESTE MEILLEUR (AL-QADI 'IYAD)", BLANC, 40), W_ / 2, 905, smooth((u - 1.2) / 0.4))
            return im
        s._bute(im, u, ox, oy)                                                     # « double » : il bute toujours
        a1, a2 = s._a("lit", u), s._a("dur", u)
        s._pose(im, s._lab("+1 : TU LIS", BLANC, 60), W_ / 2, 50 + 14 * (1 - a1), a1)
        s._pose(im, s._lab("+1 : C'EST DUR POUR TOI", JAUNE, 60), W_ / 2, 130 + 14 * (1 - a2), a2)
        ax = s._a("x2", u, 0.3)
        if ax > 0:
            b = s._cache.setdefault("x2", autocollant(pxv.big_title([("×2", JAUNE)], size=170), r=5, ombre=False))
            k2 = 1.15 - 0.15 * smooth((u - s.t["x2"]) / 0.3)
            b2 = b.resize((int(b.width * k2), int(b.height * k2)), Image.LANCZOS)
            im.alpha_composite(_fade(b2, ax), (int(W_ - b2.width - 10), int(oy - 40)))
            s._pose(im, s._lab("2 RÉCOMPENSES", JAUNE, 66), W_ / 2, 905, ax)
        return im


# ---------------------------------------------------------------- {ecran} {dua …}
def _telephone():
    c = Px(64, 116, alpha=True)
    corps = c.mask_rrect(0, 0, 64, 116, 10)
    c.shape(corps, (42, 42, 54), shade=(24, 24, 32), light=(100, 100, 118), band=2, olcol=OL)
    ecran = c.mask_rrect(4, 5, 60, 111, 7)
    c.vgrad(ecran, 5, 111, (66, 94, 198), (182, 88, 172), steps=8)
    c.dither(ecran & c.mask_ell(46, 30, 18, 18), (112, 142, 232), 0.4)
    c.dither(ecran & c.mask_ell(14, 94, 22, 22), (206, 112, 196), 0.4)
    c.fill(c.mask_rrect(24, 7, 40, 12, 2), (16, 16, 22))                          # l'encoche
    for i in range(4):                                                            # l'heure (blocs stylisés)
        x = 15 + i * 9 + (3 if i >= 2 else 0)
        c.fill(c.mask_rect(x, 18, x + 6, 28), (245, 245, 255))
        c.fill(c.mask_rect(x + 2, 20, x + 4, 26), (120, 120, 210))
    c.fill(c.mask_rect(32, 21, 33, 22), (245, 245, 255))
    c.fill(c.mask_rect(32, 25, 33, 26), (245, 245, 255))
    cols = [(240, 90, 80), (90, 200, 120), (250, 200, 70), (90, 160, 250), (200, 110, 240), (250, 140, 60),
            (70, 200, 220), (240, 240, 240)]
    for r_ in range(3):
        for k_ in range(4):
            x, y = 9 + k_ * 12, 44 + r_ * 14
            c.shape(c.mask_rrect(x, y, x + 9, y + 9, 2), cols[(r_ * 4 + k_) % len(cols)], band=1, olcol=(30, 30, 50))
    c.fill(c.mask_rrect(8, 96, 56, 107, 4), (255, 255, 255))                       # le dock
    c.dither(c.mask_rrect(8, 96, 56, 107, 4), (220, 210, 240), 0.5)
    for k_ in range(4):
        x = 11 + k_ * 11
        c.shape(c.mask_rrect(x, 98, x + 8, 105, 2), cols[k_ + 3], band=1, olcol=(30, 30, 50))
    return c


class Ecran(_Base):
    """{ecran} : accroche, vu d'en haut (à ta place) : ton téléphone tombe entre tes baskets, l'écran se fend, « CRAC ! ».
    {dua} : le téléphone fendu et l'invocation (Mouslim 918) ligne par ligne ; {dua recompense} la récompense,
    {dua mieux} la boîte « MIEUX », {dua iphone} bulle « un iPhone ? », {dua choisit} « C'EST ALLAH QUI CHOISIT »."""
    IMPACT = (17, 88)
    T_IMP = 0.25
    ETAPES = ("inna", "recompense", "mieux", "iphone", "choisit")

    def __init__(s, cmd, mode="chute"):
        super().__init__(cmd)
        s.mode = mode
        s.negatif = mode == "chute"
        rng = np.random.default_rng(11)
        s.fentes = []
        ix, iy = s.IMPACT
        for j in range(9):
            a = 2 * math.pi * j / 9 + float(rng.uniform(-0.25, 0.25))
            L = float(rng.uniform(26, 84))
            pts, x, y = [(ix, iy)], ix, iy
            n = int(rng.integers(4, 7))
            for _ in range(n):
                a += float(rng.uniform(-0.45, 0.45))
                x, y = x + L / n * math.cos(a), y + L / n * math.sin(a)
                x, y = min(58.5, max(5.5, x)), min(109.5, max(6.5, y))
                pts.append((x, y))
            s.fentes.append(pts)
        s.anneaux = []
        for r in (5, 11):
            s.anneaux.append([(ix + r * math.cos(2 * math.pi * j / 9 + 0.3), iy + r * math.sin(2 * math.pi * j / 9 + 0.3))
                              for j in range(10)])

    def sons_el(s):
        if s.mode == "chute":
            return [(-0.4, "tr_whoosh_doux", 0.02, None), (s.T_IMP, "imp_vaisselle_brise", 0.03, None)]
        out = []
        for nom, son, g in (("recompense", "sa_ting", 0.03), ("mieux", "sa_scintillement", 0.045),
                            ("choisit", "sa_ting", 0.03)):
            if nom in s.t:
                out.append((s.t[nom], son, g, None))
        return out

    def _tel(s, K, fendu):
        """Le téléphone en pixels d'écran ; fendu = avancement des fissures (0 → 1)."""
        cle = ("tel", K, round(fendu, 2))
        if cle in s._cache:
            return s._cache[cle]
        base = s._cache.setdefault(("tel0", K), _telephone().img(K, rgba=True))
        im = base.copy()
        if fendu > 0:
            d = ImageDraw.Draw(im)
            for passe in (0, 1):
                col, ep = ((20, 18, 30, 230), K + 3) if passe == 0 else ((250, 252, 255, 255), max(2, K - 2))
                for pts in s.fentes:
                    L_tot = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
                    reste = L_tot * fendu
                    for i in range(len(pts) - 1):
                        seg = math.dist(pts[i], pts[i + 1])
                        if reste <= 0:
                            break
                        f = min(1.0, reste / seg)
                        x0, y0 = pts[i]
                        x1 = x0 + (pts[i + 1][0] - x0) * f
                        y1 = y0 + (pts[i + 1][1] - y0) * f
                        d.line([(x0 * K, y0 * K), (x1 * K, y1 * K)], fill=col, width=ep)
                        reste -= seg
                if fendu > 0.5:
                    for an in s.anneaux:
                        d.line([(x * K, y * K) for (x, y) in an], fill=col, width=ep)
            ix, iy = s.IMPACT
            d.ellipse([ix * K - 3 * K, iy * K - 3 * K, ix * K + 3 * K, iy * K + 3 * K], fill=(240, 244, 255, 230))
        if len(s._cache) > 60:
            for k_ in [k_ for k_ in s._cache if isinstance(k_, tuple) and k_[0] == "tel"][:20]:
                s._cache.pop(k_, None)
        s._cache[cle] = im
        return im

    def _trottoir(s):
        if "trot" in s._cache:
            return s._cache["trot"]
        W, H = 170, 160
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        c.fill(tout_, (118, 118, 128))
        rng = np.random.default_rng(3)
        for y in range(0, H, 24):
            dec = 0 if (y // 24) % 2 == 0 else 12
            for x in range(-dec, W, 24):
                dalle = c.mask_rect(x + 1, y + 1, x + 24, y + 24) & tout_
                g = int(rng.integers(146, 164))
                c.fill(dalle, (g, g, g + 8))
                c.dither(dalle, (g - 10, g - 10, g - 4), 0.12)
        for (x0, x1) in ((42, 70), (100, 128)):                                      # tes baskets (vues d'en haut)
            cxs = (x0 + x1) / 2
            semelle = c.mask_rrect(x0 - 1, 106, x1 + 1, 158, 13)
            c.shape(semelle, (196, 198, 210), shade=(164, 166, 180), band=1, olcol=OL)
            dessus = c.mask_rrect(x0 + 2, 109, x1 - 2, 156, 11)
            c.fill(dessus, (246, 246, 250))
            c.dither(dessus & c.mask_rect(x0, 109, cxs - 6, 158), (222, 222, 232), 0.5)
            c.fill(c.mask_ell(cxs, 116, (x1 - x0) / 2 - 4, 6) & dessus, (228, 230, 238))   # le bout renforcé
            c.fill(c.mask_rrect(cxs - 7, 124, cxs + 7, 146, 3), (226, 228, 236))         # la languette
            for j in range(5):                                                         # les lacets
                c.fill(c.mask_rect(cxs - 7, 126 + 4 * j, cxs + 7, 127 + 4 * j), (150, 150, 168))
            c.fill(c.mask_poly([(x1 - 2, 124), (x1 - 2, 136), (x0 + 6, 146), (x0 + 6, 142)]) & dessus, (226, 60, 56))
        for (x0, x1) in ((42, 70), (100, 128)):                                      # le bas du jean par-dessus
            jean = c.mask_rrect(x0 - 4, 148, x1 + 4, 176, 6)
            c.shape(jean, (60, 94, 164), shade=(44, 70, 128), light=(96, 132, 200), band=1, olcol=OL)
            c.fill(c.mask_rect(x0 - 3, 150, x1 + 3, 152) & jean, (96, 132, 200))
        s._cache["trot"] = c.img(s.K, rgba=True)
        return s._cache["trot"]

    def _image_chute(s, u):
        K = s.K
        im = s._trottoir().copy()
        W_, H_ = im.size
        v = u - s.T_IMP
        f_chute = smooth((u + 0.45) / (s.T_IMP + 0.45))
        if v < 0:
            k_ = 1.65 - 0.65 * f_chute                                             # il tombe : il s'éloigne de toi
            ang = 22 - 16 * f_chute
        else:
            k_ = 1.0 - 0.03 * math.sin(math.pi * min(1.0, v / 0.25))               # petit rebond
            ang = 6.0
        fendu = smooth((v - 0.02) / 0.28) if v > 0 else 0.0
        tel = s._tel(5, fendu)
        t2 = tel.resize((int(tel.width * k_), int(tel.height * k_)), Image.LANCZOS)
        t2 = t2.rotate(ang, resample=Image.BICUBIC, expand=True)
        cx, cy = W_ / 2 + 10, 450 - 40 * (1 - f_chute)
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))                              # l'ombre se resserre en tombant
        ox, oy = 14 + 60 * (1 - f_chute), 18 + 70 * (1 - f_chute)
        so = 1.0 - 0.2 * (1 - f_chute)
        ImageDraw.Draw(lay).rounded_rectangle([cx + ox - 160 * so, cy + oy - 290 * so, cx + ox + 160 * so, cy + oy + 290 * so],
                                              50, fill=(20, 20, 30, int(90 + 70 * f_chute)))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(22 - 14 * f_chute)))
        im.alpha_composite(t2, (int(cx - t2.width / 2), int(cy - t2.height / 2)))
        if v > 0:
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            rng = np.random.default_rng(21)                                         # petits éclats de verre
            ix = cx - 160 + s.IMPACT[0] * 5
            iy = cy - 290 + s.IMPACT[1] * 5
            for j in range(9):
                a_ = rng.uniform(0, 2 * math.pi)
                r_ = rng.uniform(60, 160) * smooth(v / 0.4)
                al = int(240 * (1 - smooth((v - 0.25) / 0.35)))
                if al > 0:
                    x, y = ix + r_ * math.cos(a_), iy + r_ * math.sin(a_)
                    d.rectangle([x - 5, y - 5, x + 5, y + 5], fill=(236, 244, 255, al))
            im.alpha_composite(lay)
            cr = s._cache.setdefault("crac", _titre("CRAC !", ROUGE, 150, r=5))
            a = smooth((v - 0.04) / 0.18)
            k2 = 0.85 + 0.15 * smooth(v / 0.25)
            c2 = cr.resize((int(cr.width * k2), int(cr.height * k2)), Image.LANCZOS)
            im.alpha_composite(_fade(c2, a), (int(W_ - c2.width - 30), int(150 - c2.height / 2)))
        return im

    def _image_dua(s, u):
        W_, H_ = 1020, 960
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        tel = s._tel(4, 1.0)
        tx, ty = int(W_ / 2 - tel.width / 2), int(14 + 8 * math.sin(u * 1.7))        # il flotte doucement
        ec = s._e("choisit", u, 0.6)
        if ec > 0:                                                                  # la boîte « mieux » brille
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(lay).ellipse([700, 60, 990, 360], fill=(255, 226, 140, int(150 * ec)))
            im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(30)))
        im.alpha_composite(tel, (tx, ty))
        # l'invocation, ligne par ligne (sur les mots) ; {dua inna} : la 1re ligne sur « Inna lillahi »
        a1 = s._a("inna", u) if "inna" in s.t else smooth(u / 0.35)
        s._pose(im, s._cache.setdefault("l1", _deux("INNA LILLAHI", BLANC, 62, "WA INNA ILAYHI RAJI'OUN", BLANC, 56)),
                W_ / 2, 580, a1)
        s._pose(im, s._lab("ALLAHOUMMA-JOURNI FI MOUSSIBATI", JAUNE, 52), W_ / 2, 730, s._a("recompense", u))
        s._pose(im, s._lab("WA AKHLIF LI KHAYRAN MINHA", JAUNE, 52), W_ / 2, 820, s._a("mieux", u))
        # à gauche : la récompense ; à droite : « mieux »
        ar = s._a("recompense", u, 0.35)
        if ar > 0:
            med = s._cache.setdefault("med", autocollant(objets.icone("medaille").img(10), r=5))
            im.alpha_composite(_fade(med, ar), (int(170 - med.width / 2), int(190 - med.height / 2 + 20 * (1 - ar))))
            s._pose(im, s._lab("LA RÉCOMPENSE", OR_, 44), 170, 330, ar, maxw=320)
        am = s._a("mieux", u, 0.35)
        if am > 0:
            cad = s._cache.setdefault("cad", autocollant(objets.icone("cadeau").img(10), r=5))
            im.alpha_composite(_fade(cad, am), (int(850 - cad.width / 2), int(190 - cad.height / 2 + 20 * (1 - am))))
            s._pose(im, s._lab("MIEUX", JAUNE, 70), 850, 335, am, maxw=320)
            q = s._cache.setdefault("q", _titre("?", JAUNE, 110, r=4))
            aq = am * (1 - ec)
            im.alpha_composite(_fade(q, aq), (int(850 + 40), int(190 - q.height - 40 + 6 * math.sin(u * 3))))
        ai = s._a("iphone", u, 0.3, fin="choisit")
        if ai > 0:                                                                  # « le dernier iPhone ? »
            b = s._cache.get("bul")
            if b is None:
                ic = objets.icone("telephone").img(7)
                b = _bulle([("?", BLANC)], fond=(60, 60, 110), size=60, queue=0.3, pensee=True, pad=20)
                bb = Image.new("RGBA", (b.width + ic.width + 10, max(b.height, ic.height + 40)), (0, 0, 0, 0))
                bb.alpha_composite(b, (ic.width + 10, 0))
                bb.alpha_composite(ic, (0, 10))
                b = s._cache["bul"] = bb
            im.alpha_composite(_fade(b, ai), (int(W_ - b.width - 10), int(10 + 10 * (1 - ai))))
        if ec > 0:
            s._pose(im, s._cache.setdefault("ch", _deux("C'EST ALLAH", OR_, 48, "QUI CHOISIT", OR_, 48)), 850, 452, ec,
                    maxw=330)
        return im

    def image(s, u):
        return s._image_chute(u) if s.mode == "chute" else s._image_dua(u)


# ---------------------------------------------------------------- {tombeau …}
class Tombeau(_Base):
    """{tombeau} : la tombe en coupe, la nuit (Boukhari 1374 : « quand on le pose dans sa tombe et que ses compagnons
    s'en vont, il entend le bruit de leurs sandales »). {tombeau anges} deux lumières descendent, il est assis, « QUE
    DISAIS-TU DE CET HOMME ? » ; {tombeau paradis} le croyant : « sa place en Enfer » se ferme, « sa place au Paradis »
    s'ouvre ; {tombeau cri} l'hypocrite et le mécréant : « JE NE SAIS PAS… » ; {tombeau crie} le cri traverse la terre :
    les oiseaux s'envolent, le chat sursaute, les humains passent sans rien entendre. Le coup n'est jamais montré."""
    negatif = True
    SURF = 36
    CH = (40, 82, 130, 134)                 # la niche (lahd) : x0, y0, x1, y1
    HANCHES = (80, 127)
    ETAPES = ("anges", "paradis", "cri", "crie")

    def __init__(s, cmd):
        super().__init__(cmd)

    def sons_el(s):
        out = [(-0.2, "dv_pas_pierre", 0.05, None), (1.6, "dv_pas_pierre", 0.04, None)]
        if "anges" in s.t:
            out.append((s.t["anges"], "sa_scintillement", 0.04, None))
        if "paradis" in s.t:
            out.append((s.t["paradis"] + 1.6, "sa_scintillement", 0.04, None))
        tc = s._t_crie()
        if tc is not None:
            out += [(tc, "imp_cri_ciel", 0.03, None), (tc + 0.6, "an_oiseaux_envol", 0.04, None)]
        return out

    def _t_crie(s):
        if "crie" in s.t:
            return s.t["crie"]
        if "cri" in s.t:
            return s.t["cri"] + 2.0
        return None

    def _fond(s):
        if "f" in s._cache:
            return s._cache["f"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        ciel = c.mask_rect(0, 0, W, s.SURF) & tout_
        c.vgrad(ciel, 0, s.SURF, (14, 16, 40), (40, 40, 76), steps=4)
        rng = np.random.default_rng(9)
        for _ in range(30):
            c.px(int(rng.integers(2, W - 2)), int(rng.integers(2, s.SURF - 8)), (230, 232, 255))
        c.fill(c.mask_ell(26, 10, 6, 6), (244, 238, 212))                          # la lune
        c.fill(c.mask_ell(29, 8, 5, 5) & tout_, (20, 22, 50))
        terre = c.mask_rect(0, s.SURF, W, H) & tout_                              # la terre, de plus en plus sombre
        c.vgrad(terre, s.SURF, H, (104, 74, 54), (46, 32, 26), steps=6)
        for y in (54, 76, 104, 128):
            c.fill(c.mask_rect(0, y, W, y + 1) & terre, (82, 58, 44))
        for _ in range(60):
            x, y = int(rng.integers(2, W - 2)), int(rng.integers(s.SURF + 3, H - 2))
            c.fill(c.mask_rect(x, y, x + 2, y + 1) & terre, (126, 96, 74) if rng.random() < 0.5 else (60, 42, 34))
        herbe = c.mask_rect(0, s.SURF - 2, W, s.SURF + 1) & tout_
        c.fill(herbe, (52, 92, 60))
        for x in range(0, W, 3):
            c.px(x, s.SURF - 3, (70, 120, 74))
        x0, y0, x1, y1 = s.CH
        fosse = c.mask_rect(68, s.SURF, 102, y0)                                   # la fosse comblée
        c.fill(fosse, (122, 90, 66))
        c.dither(fosse, (100, 72, 54), 0.35)
        c.fill(c.mask_ell(85, s.SURF - 1, 21, 4) & c.mask_rect(0, 0, W, s.SURF + 1), (128, 96, 70))   # le monticule
        niche = c.mask_rrect(x0, y0, x1, y1, 4)
        c.fill(niche, (30, 22, 20))
        c.fill(c.mask_rect(x0, y1 - 2, x1, y1), (44, 32, 28))
        c.outline(niche, (20, 14, 12))
        for (sx, sh) in ((8, 10), (118, 8), (136, 11)):                             # pierres tombales
            pierre = c.mask_rrect(sx, s.SURF - sh - 1, sx + 9, s.SURF + 1, 3)
            c.shape(pierre, (150, 150, 160), shade=(110, 110, 122), light=(186, 186, 196), band=1, olcol=OL)
        tronc = c.mask_poly([(152, s.SURF), (156, s.SURF), (155, 16), (153, 16)])   # l'arbre nu (les oiseaux)
        c.fill(tronc, (50, 36, 34))
        for (xa, ya, xb, yb) in ((154, 20, 146, 13), (154, 18, 164, 11), (154, 24, 162, 20)):
            c.line(xa, ya, xb, yb, (50, 36, 34))
        s._cache["f"] = c.img(s.K, rgba=True)
        return s._cache["f"]

    def _corps(s):
        """Le linceul en deux morceaux : les jambes (fixes) et le haut du corps (qui se redresse)."""
        if "corps" in s._cache:
            return s._cache["corps"]
        K = s.K
        blanc, ombre, clair = (238, 236, 226), (198, 196, 188), (255, 255, 250)
        j = Px(34, 14, alpha=True)
        m = j.mask_rrect(0, 1, 34, 13, 5)
        j.shape(m, blanc, shade=ombre, light=clair, band=1, olcol=OL)
        for x in (4, 18):
            j.fill(j.mask_rect(x, 1, x + 1, 13) & m, (170, 160, 140))
        h = Px(40, 14, alpha=True)
        m2 = h.mask_rect(0, 1, 28, 13) | h.mask_ell(32, 7, 6.5, 6.5)
        h.shape(m2, blanc, shade=ombre, light=clair, band=1, olcol=OL)
        for x in (10, 25):
            h.fill(h.mask_rect(x, 1, x + 1, 13) & m2, (170, 160, 140))
        s._cache["corps"] = (j.img(K, rgba=True), h.img(K, rgba=True))
        return s._cache["corps"]

    def _jambes_passants(s, who, step):
        cle = ("p", who, step)
        if cle not in s._cache:
            spr = _sprite(who, "neutre", "neutre", step=step)
            s._cache[cle] = _grand(spr.crop((0, 50, spr.width, spr.height)), 4)
        return s._cache[cle]

    def image(s, u):
        K = s.K
        im = s._fond().copy()
        W_, H_ = im.size
        d = ImageDraw.Draw(im)
        x0, y0, x1, y1 = s.CH
        ea = s._e("anges", u, 1.2)
        ec = s._e("cri", u, 0.6)
        tc = s._t_crie()
        if ea > 0:                                                                  # la lumière des anges dans la niche
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            col = (255, 236, 190) if ec < 0.5 else (170, 60, 90)
            ImageDraw.Draw(lay).ellipse([x0 * K - 40, y0 * K - 30, x1 * K + 40, y1 * K + 30], fill=(*col, int(80 * ea)))
            im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(30)))
        # le mort dans son linceul : couché, puis assis (« ils le font asseoir »)
        jambes, haut = s._corps()
        hx, hy = s.HANCHES
        im.alpha_composite(jambes, (int((hx - 33) * K), int((hy - 7) * K)))
        e_s = s._e("anges", u, 0.8, dec=1.0)
        rot, (dx, dy) = _tourne(haut, 84 * e_s, (0, 7 * K))
        im.alpha_composite(rot, (int(hx * K - dx), int(hy * K - dy)))
        ang = math.radians(84 * e_s)
        tete = (hx * K + 32 * K * math.cos(ang), hy * K - 32 * K * math.sin(ang))
        # les gens qui repartent après l'enterrement (on ne voit que leurs jambes) : « TAC… TAC… »
        for j, (who, x_dep) in enumerate((("GRAND", 92), ("PAPA", 106), ("TONTON", 78))):
            x = (x_dep + 9.5 * (u + 1.0) - 6 * j) * K
            if x > W_ + 60:
                continue
            leg = s._jambes_passants(who, int((u + j * 0.3) * 8) % 8)
            im.alpha_composite(leg, (int(x - leg.width / 2), int(s.SURF * K - leg.height + 6)))
        tac = s._cache.setdefault("tac", _titre("TAC…", BLANC, 40, r=3))
        for i in range(8):
            t_ = -0.4 + i * 0.55
            v = u - t_
            if 0 <= v < 0.6:
                x = (92 + 9.5 * (t_ + 1.0) - 6 * (i % 3)) * K
                if x < W_ - 40:
                    im.alpha_composite(_fade(tac, smooth(v / 0.1) * (1 - smooth((v - 0.3) / 0.3))),
                                       (int(x - tac.width / 2 + 40), int(s.SURF * K - 150 - 20 * v)))
        # deux lumières (les anges, jamais dessinés) descendent jusqu'à lui
        if ea > 0:
            v = u - s.t["anges"]
            for j, xo in enumerate((54, 110)):
                y = (-8 + (y0 + 20 + 8) * smooth(v / 1.2)) * K
                _orbe(im, xo * K, y + 2 * K * math.sin(u * 2 + j), 6 * K, ANGE_OR if ec < 0.5 else (230, 210, 230), ea)
        aq = s._a("anges", u, 0.3, fin=("paradis", "cri"), dec=1.3)
        if aq > 0:                                                                  # la question
            b = s._cache.get("bq")
            if b is None:
                b = s._cache["bq"] = _bulle([("QUE DISAIS-TU", BLANC), ("DE CET HOMME ?", BLANC), ("(MOUHAMMAD)", JAUNE)],
                                            fond=(40, 60, 120), size=44, queue=0.5)
            im.alpha_composite(_fade(b, aq), (int(W_ / 2 - b.width / 2), int(y0 * K - b.height - 6)))
        # le croyant
        ap = s._a("paradis", u, 0.35, fin="cri")
        if ap > 0:
            s._pose(im, s._lab("LE CROYANT", VERT, 48), W_ / 2, (s.SURF + 4) * K, ap)
            b = s._cache.get("br")
            if b is None:
                b = s._cache["br"] = _bulle([("« J'ATTESTE QU'IL EST", BLANC), ("LE SERVITEUR D'ALLAH", BLANC),
                                             ("ET SON MESSAGER »", BLANC)], fond=(30, 104, 66), size=34, queue=0.5)
            im.alpha_composite(_fade(b, ap), (int(W_ / 2 - b.width / 2), int(y0 * K - b.height - 6)))
            for (wx0, wx1, enfer) in ((3, 37, True), (133, 167, False)):          # les deux places
                aw = s._a("paradis", u, 0.5, fin="cri", dec=0.7)
                if aw <= 0:
                    continue
                ferme = s._e("paradis", u, 0.6, dec=1.7) if enfer else 0.0
                ouvre = 1.0 if enfer else s._e("paradis", u, 0.6, dec=1.7)
                lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
                ld = ImageDraw.Draw(lay)
                bx = [wx0 * K, 92 * K, wx1 * K, 126 * K]
                if enfer:
                    ld.rounded_rectangle(bx, 18, fill=(160, 40, 24, 255))
                    for k_ in range(5):
                        fx = bx[0] + 20 + k_ * 38
                        hh = 60 + 30 * math.sin(u * 6 + k_ * 1.7)
                        ld.polygon([(fx - 18, bx[3]), (fx, bx[3] - hh), (fx + 18, bx[3])], fill=(255, 150, 40, 255))
                    if ferme > 0:                                                  # elle se ferme
                        ld.rounded_rectangle([bx[0], bx[1], bx[2], bx[1] + (bx[3] - bx[1]) * ferme], 18,
                                             fill=(40, 30, 28, 255))
                else:
                    ld.rounded_rectangle(bx, 18, fill=(120, 200, 255, 255))
                    ld.rectangle([bx[0], bx[1] + 120, bx[2], bx[3]], fill=(80, 180, 90, 255))
                    for k_ in range(4):
                        tx_ = bx[0] + 30 + k_ * 50
                        ld.ellipse([tx_ - 22, bx[1] + 70, tx_ + 22, bx[1] + 120], fill=(40, 140, 70, 255))
                    ld.ellipse([bx[2] - 70, bx[1] + 10, bx[2] - 20, bx[1] + 60], fill=(255, 240, 170, 255))
                ld.rounded_rectangle(bx, 18, outline=(255, 255, 255, 255), width=6)
                im.alpha_composite(_fade(lay, aw * (ouvre if not enfer else 1.0)))
                if not enfer and ouvre > 0:
                    lay2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
                    ImageDraw.Draw(lay2).ellipse([bx[0] - 60, bx[1] - 60, bx[2] + 60, bx[3] + 60],
                                                 fill=(255, 236, 170, int(90 * ouvre * aw)))
                    im.alpha_composite(lay2.filter(ImageFilter.GaussianBlur(24)))
                lab = "SA PLACE // EN ENFER" if enfer else "SA PLACE // AU PARADIS"
                s._pose(im, s._lab(lab, ROUGE if enfer else OR_, 44), (wx0 + wx1) / 2 * K, 83 * K,
                        aw * (1 - 0.6 * ferme) * (ouvre if not enfer else 1.0), maxw=300)
        # l'hypocrite et le mécréant
        if ec > 0:
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(lay).rounded_rectangle([x0 * K, y0 * K, x1 * K, y1 * K], 24, fill=(60, 10, 40, int(110 * ec)))
            im.alpha_composite(lay)
            s._pose(im, s._lab("L'HYPOCRITE ET LE MÉCRÉANT", ROUGE, 46), W_ / 2, (s.SURF + 4) * K, ec)
            ab = s._a("cri", u, 0.3, dec=0.3)
            b = s._cache.get("bj")
            if b is None:
                b = s._cache["bj"] = _bulle([("« JE NE SAIS PAS… »", BLANC)], fond=(112, 36, 52), size=48, queue=0.5)
            im.alpha_composite(_fade(b, ab), (int(W_ / 2 - b.width / 2), int(y0 * K - b.height - 6)))
        if tc is not None and u >= tc:                                              # le cri : des ondes dans la terre
            v = u - tc
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            for i in range(4):
                vv = v - i * 0.4
                if 0 <= vv < 1.8:
                    r = (10 + 120 * (vv / 1.8)) * K
                    a = int(220 * (1 - vv / 1.8))
                    ld.ellipse([tete[0] - r, tete[1] - r * 0.8, tete[0] + r, tete[1] + r * 0.8], outline=(255, 226, 226, a),
                               width=K)
            im.alpha_composite(lay)
            # les oiseaux s'envolent, le chat sursaute : ils entendent
            vb = v - 0.6
            for j, (bx0, by0) in enumerate(((146, 13), (163, 11))):
                if vb < 0:
                    xb, yb, aile = bx0 * K, by0 * K - 8, 0
                else:
                    xb = (bx0 + 24 * vb + 8 * j * vb) * K
                    yb = (by0 - 22 * vb) * K
                    aile = int(u * 10 + j) % 2
                if xb < W_ + 30 and yb > -30:
                    pts = [(xb - 36, yb - (22 if aile else -6)), (xb, yb), (xb + 36, yb - (22 if aile else -6))]
                    d.line(pts, fill=(20, 16, 30, 255), width=16)
                    d.line(pts, fill=(236, 236, 246, 255), width=7)
            sx, sy = 30 * K, s.SURF * K
            saut = 12 * K * math.sin(math.pi * min(1.0, max(0.0, vb) / 0.5)) if vb > 0 else 0
            z = 1.5                                                                 # le chat (silhouette)
            d.ellipse([sx - 34 * z, sy - 40 * z - saut, sx + 34 * z, sy - 2 - saut], fill=(24, 20, 28, 255))
            d.ellipse([sx + 14 * z, sy - 66 * z - saut, sx + 50 * z, sy - 30 * z - saut], fill=(24, 20, 28, 255))
            d.polygon([(sx + 16 * z, sy - 58 * z - saut), (sx + 20 * z, sy - 82 * z - saut), (sx + 30 * z, sy - 62 * z - saut)],
                      fill=(24, 20, 28, 255))
            d.polygon([(sx + 34 * z, sy - 62 * z - saut), (sx + 46 * z, sy - 82 * z - saut), (sx + 48 * z, sy - 56 * z - saut)],
                      fill=(24, 20, 28, 255))
            d.line([(sx - 30 * z, sy - 20 * z - saut), (sx - 56 * z, sy - 50 * z - saut)], fill=(24, 20, 28, 255), width=12)
            d.ellipse([sx + 24 * z, sy - 54 * z - saut, sx + 30 * z, sy - 48 * z - saut], fill=(250, 220, 90, 255))
            if vb > 0:
                ex = s._cache.setdefault("ex", _titre("!", JAUNE, 80, r=3))
                im.alpha_composite(_fade(ex, smooth(vb / 0.2)), (int(sx + 60), int(sy - 200 - saut)))
            # deux passants (humains) : ils marchent sans rien entendre
            for j, who in enumerate(("ETUDIANT", "VOISIN")):
                x = (-20 + 14 * (v + 0.5) + 26 * j) * K
                if -60 < x < 60 * K:
                    leg = s._jambes_passants(who, int((u + j * 0.4) * 8) % 8)
                    im.alpha_composite(leg, (int(x - leg.width / 2), int(s.SURF * K - leg.height + 6)))
            s._pose(im, s._cache.setdefault("tout", _deux("TOUT CE QUI L'ENTOURE L'ENTEND…", BLANC, 42,
                                                            "SAUF LES HUMAINS ET LES DJINNS", JAUNE, 40)),
                    W_ / 2, 16 * K, smooth((v - 1.0) / 0.4))
        return im


# ---------------------------------------------------------------- {chaleur PETIT}
class Chaleur(_Base):
    """{chaleur PETIT} : accroche, Petit en nage au stade sous un soleil de plomb (gouttes, vapeur, sweat mouillé)."""
    negatif = True

    def __init__(s, cmd, who="PETIT"):
        super().__init__(cmd)
        s.who = who

    def sons_el(s):
        return []

    def _fond(s):
        if "f" in s._cache:
            return s._cache["f"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        c.vgrad(tout_, 0, H, (255, 236, 170), (255, 178, 104), steps=6)
        trib = c.mask_poly([(0, 84), (W, 70), (W, 128), (0, 128)]) & tout_            # les tribunes
        c.fill(trib, (150, 120, 120))
        rng = np.random.default_rng(4)
        for y in range(76, 126, 5):
            c.fill(c.mask_rect(0, y, W, y + 1) & trib, (126, 98, 100))
            for _ in range(22):
                x = int(rng.integers(0, W))
                if trib[min(H - 1, y + 2), x]:
                    c.fill(c.mask_rect(x, y + 1, x + 2, y + 3), [(220, 70, 60), (70, 120, 220), (240, 220, 80),
                                                              (240, 240, 240)][int(rng.integers(0, 4))])
        pel = c.mask_rect(0, 128, W, H) & tout_
        c.fill(pel, (90, 170, 80))
        for x in range(0, W, 14):
            c.fill(c.mask_rect(x, 128, x + 7, H) & pel, (104, 184, 92))
        s._cache["f"] = c.img(s.K, rgba=True)
        return s._cache["f"]

    def image(s, u):
        K = s.K
        im = s._fond().copy()
        W_, H_ = im.size
        sx, sy = 805, 150                                                           # le soleil de plomb
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.ellipse([sx - 300, sy - 300, sx + 300, sy + 300], fill=(255, 255, 220, 120))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(50)))
        d = ImageDraw.Draw(im)
        for j in range(12):
            a = u * 0.25 + j * math.pi / 6
            r0, r1 = 150, 230 + 16 * math.sin(u * 3 + j)
            d.line([(sx + r0 * math.cos(a), sy + r0 * math.sin(a)), (sx + r1 * math.cos(a), sy + r1 * math.sin(a))],
                   fill=(255, 240, 160, 255), width=18)
        d.ellipse([sx - 130, sy - 130, sx + 130, sy + 130], fill=(255, 246, 200, 255), outline=(255, 190, 80, 255), width=10)

        def air(dd):                                                                # l'air qui ondule (léger)
            for j in range(3):
                y = 330 + j * 60 - (u * 40) % 60
                dd.line([(x, y + 7 * math.sin(x / 40 + u * 3 + j)) for x in range(0, W_, 20)], fill=(255, 255, 255, 60),
                        width=4)
        _translucide(im, air)
        cle = ("b", s.who)
        if cle not in s._cache:
            b, _ = _buste(s.who, "triste", sweat=True, blush=True)
            bb = _grand(b, 15)
            tache = Image.new("RGBA", bb.size, (0, 0, 0, 0))                        # le sweat trempé (taches sombres)
            td = ImageDraw.Draw(tache)
            for (ex, ey, rx, ry) in ((60, bb.height - 50, 62, 42), (bb.width - 56, bb.height - 60, 58, 46)):
                td.ellipse([ex - rx, ey - ry, ex + rx, ey + ry], fill=(110, 16, 26, 120))
            ta = np.array(tache)
            ta[..., 3] = np.minimum(ta[..., 3], np.array(bb)[..., 3])
            bb.alpha_composite(Image.fromarray(ta, "RGBA"))
            s._cache[cle] = bb
        bus = s._cache[cle]
        bx, by = 90, H_ - bus.height + 10
        im.alpha_composite(bus, (bx, by))
        g_ = s._cache.setdefault("g", _goutte((150, 214, 255), k=7))
        for j, (gx, gy, dec) in enumerate(((bx + 88, by + 112, 0.0), (bx + 288, by + 88, 0.5), (bx + 375, by + 200, 0.9),
                                           (bx + 150, by + 250, 1.3))):
            v = ((u + 2 + dec) % 1.6) / 1.6
            a = smooth(v / 0.12) * (1 - smooth((v - 0.8) / 0.2))
            im.alpha_composite(_fade(g_, a), (int(gx), int(gy + 130 * v)))
        def vapeur(dd):                                                             # la vapeur qui sort de sa tête
            for j in range(3):
                v = ((u + j * 0.6) % 1.8) / 1.8
                x = bx + 130 + j * 90 + 14 * math.sin(u * 3 + j)
                y = by - 10 - 120 * v
                a = int(170 * smooth(v / 0.2) * (1 - smooth((v - 0.6) / 0.4)))
                dd.line([(x + 12 * math.sin(v * 9 + k_), y - k_ * 14) for k_ in range(5)], fill=(255, 255, 255, a), width=8)
        _translucide(im, vapeur)
        return im


# ---------------------------------------------------------------- {soleil …}
class Soleil(_Base):
    """{soleil} : le Jour du Jugement, le soleil tout près, quatre silhouettes ; {soleil mile} « 1 MILE » ;
    {soleil chevilles|genoux|taille|bouche} : la sueur monte jusque-là, « SELON SES ACTES » (Mouslim 2864).
    {soleil ombre} : une ombre douce, un jeune qui a grandi dans l'adoration d'Allah (Boukhari 660) ; {soleil jeune}."""
    NIV = (("chevilles", 0.11, "CHEVILLES"), ("genoux", 0.30, "GENOUX"), ("taille", 0.52, "TAILLE"),
           ("bouche", 0.84, "BOUCHE"))
    XS = (24, 64, 106, 146)
    WHO = ("GRAND", "MAMAN", "VOYAGEUR", "PAPI")
    PIEDS = 138
    KP = 3
    ETAPES = ("mile", "chevilles", "genoux", "taille", "bouche", "sueur", "jeune")

    def __init__(s, cmd, mode="soleil"):
        super().__init__(cmd)
        s.mode = mode

    def sons_el(s):
        out = [(0.0, "imp_grondement", 0.02, None)] if s.mode == "soleil" else [(0.2, "sa_scintillement", 0.045, None)]
        for nom, _, _ in s.NIV:
            if nom in s.t:
                out.append((s.t[nom], "tr_whoosh_doux", 0.018, None))
        return out

    def _t_niv(s, i):
        nom = s.NIV[i][0]
        if nom in s.t:
            return s.t[nom]
        if "sueur" in s.t:
            return s.t["sueur"] + 0.8 * i
        return None

    def _fond(s):
        if "f" in s._cache:
            return s._cache["f"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        c.vgrad(tout_ & c.mask_rect(0, 0, W, 74), 0, 74, (255, 252, 226), (255, 206, 136), steps=6)
        sol = c.mask_rect(0, 72, W, H) & tout_
        c.vgrad(sol, 72, H, (236, 222, 196), (204, 184, 152), steps=5)
        rng = np.random.default_rng(6)
        for _ in range(90):                                                         # la foule immense, au loin
            x, y = int(rng.integers(0, W)), int(rng.integers(72, 80))
            c.fill(c.mask_rect(x, y - 3, x + 1, y + 1), (150, 126, 110))
            c.px(x, y - 4, (150, 126, 110))
        s._cache["f"] = c.img(s.K, rgba=True)
        return s._cache["f"]

    def _silh(s, who, col=(78, 80, 104)):
        cle = ("s", who, col)
        if cle not in s._cache:
            s._cache[cle] = _grand(_silhouette(_sprite(who, "neutre", "neutre"), col, rim=(140, 140, 170)), s.KP)
        return s._cache[cle]

    def _soleil(s, im, u, e=1.0):
        """Le soleil tout près (e < 1 : il est encore plus haut et descend vers les gens)."""
        cle = "sol"
        if cle not in s._cache:
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            cx, cy, R = im.width / 2, -60, 300
            ld.ellipse([cx - R * 1.9, cy - R * 1.9, cx + R * 1.9, cy + R * 1.9], fill=(255, 240, 170, 110))
            lay = lay.filter(ImageFilter.GaussianBlur(60))
            ld = ImageDraw.Draw(lay)
            ld.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(255, 250, 222, 255), outline=(255, 176, 70, 255), width=14)
            ld.ellipse([cx - R * 0.8, cy - R * 0.8, cx + R * 0.8, cy + R * 0.8], fill=(255, 255, 240, 255))
            s._cache[cle] = lay
        dy = int(330 * (1 - e))
        im.alpha_composite(s._cache[cle], (0, 0), (0, dy))

        def air(dd):
            for j in range(3):
                y = 320 + j * 50 - (u * 40) % 50
                dd.line([(x, y + 6 * math.sin(x / 36 + u * 3 + j)) for x in range(0, im.width, 20)],
                        fill=(255, 255, 255, 70), width=4)
        _translucide(im, air)

    def _sueur(s, im, x, niveau, a=1.0):
        """La sueur autour d'une personne, jusqu'à la hauteur niveau (fraction de sa taille)."""
        if niveau <= 0.005 or a <= 0.01:
            return
        K = s.K
        haut = 98 * s.KP * niveau
        yb = s.PIEDS * K + 8
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        w = 92
        pts = [(x - w, yb)]
        for k_ in range(13):
            xx = x - w + 2 * w * k_ / 12
            pts.append((xx, yb - haut + 6 * math.sin(k_ * 1.3 + niveau * 20)))
        pts.append((x + w, yb))
        ld.polygon(pts, fill=(96, 170, 255, int(130 * a)))
        ld.line(pts[1:-1], fill=(200, 230, 255, int(230 * a)), width=6)
        im.alpha_composite(lay)

    def image(s, u):
        K = s.K
        im = s._fond().copy()
        W_, H_ = im.size
        s._soleil(im, u, smooth((u + 0.2) / 4.6) if s.mode == "soleil" else 1.0)
        if s.mode == "ombre":
            return s._image_ombre(u, im)
        d = ImageDraw.Draw(im)
        for i, (x, who) in enumerate(zip(s.XS, s.WHO)):                            # ils respirent, se balancent
            sp = s._silh(who)
            dx = 1.6 * K * math.sin(u * 1.3 + i * 1.7)
            dy = K * 0.6 * (1 + math.sin(u * 2.4 + i))
            im.alpha_composite(sp, (int(x * K - sp.width / 2 + dx), int(s.PIEDS * K - sp.height + 6 + dy)))
        for i, x in enumerate(s.XS):
            t_ = s._t_niv(i)
            if t_ is None or u < t_:
                continue
            niv = s.NIV[i][1] * smooth((u - t_) / 0.8)
            s._sueur(im, x * K, niv)
            s._pose(im, s._lab(s.NIV[i][2], BLANC, 36), x * K, (s.PIEDS + 6) * K, smooth((u - t_) / 0.3), maxw=250)
        t0 = s._t_niv(0)
        if t0 is not None:
            s._pose(im, s._lab("SELON SES ACTES", JAUNE, 62), W_ / 2, 62 * K, smooth((u - t0) / 0.35))
        am = s._a("mile", u, 0.4)
        if t0 is not None and u > t0:                                               # « 1 MILE » laisse la place
            am *= 1 - smooth((u - t0) / 0.3)
        if am > 0:                                                                  # « 1 MILE » : du soleil aux têtes
            xm = 86 * K
            y_a, y_b = 42 * K, 86 * K
            yy = y_a
            while yy < y_a + (y_b - y_a) * am:
                d.line([(xm, yy), (xm, min(y_b, yy + 22))], fill=(20, 16, 30, 255), width=12)
                d.line([(xm, yy), (xm, min(y_b, yy + 22))], fill=(255, 120, 60, 255), width=6)
                yy += 34
            s._pose(im, s._lab("1 MILE", ROUGE, 60), xm + 150, (y_a + y_b) / 2 - 30, am, maxw=300)
            s._pose(im, s._cache.setdefault("khol", _deux("OU UN BÂTONNET DE KHÔL ?", BLANC, 34, "(LE RAPPORTEUR HÉSITE)",
                                                          BLANC, 28)), xm + 180, (y_a + y_b) / 2 + 50, am, maxw=420)
        return im

    def _image_ombre(s, u, im):
        K = s.K
        W_, H_ = im.size
        for i, (x, who, niv) in enumerate(((16, "GRAND", 0.30), (46, "MAMAN", 0.52), (76, "PAPI", 0.84))):
            sp = s._silh(who, (96, 96, 116))
            im.alpha_composite(sp, (int(x * K - sp.width / 2), int(s.PIEDS * K - sp.height + 6)))
            s._sueur(im, x * K, niv, 0.8)
        e = smooth(u / 0.7)
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))                              # l'ombre douce, à part
        ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle([104 * K, -60, W_ + 80, (s.PIEDS + 6) * K], 70, fill=(36, 64, 118, int(190 * e)))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(28)))
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))                              # des rayons frais, très doux
        ld = ImageDraw.Draw(lay)
        for j in range(3):
            x = (114 + 18 * j) * K
            ld.polygon([(x - 18, 0), (x + 18, 0), (x + 70, s.PIEDS * K), (x - 6, s.PIEDS * K)],
                       fill=(196, 224, 255, int(40 * e)))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10)))
        ej = s._e("jeune", u, 0.6) if "jeune" in s.t else smooth((u - 1.0) / 0.6)
        cle = "jeune"
        if cle not in s._cache:
            s._cache[cle] = _grand(_sprite("ADO", "neutre", "calme"), 4)
        jn = s._cache[cle]
        xj = 138 * K
        if ej > 0:
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(lay).ellipse([xj - 150, (s.PIEDS - 70) * K, xj + 150, (s.PIEDS + 4) * K],
                                        fill=(255, 230, 160, int(80 * ej)))
            im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(30)))
            im.alpha_composite(_fade(jn, ej), (int(xj - jn.width / 2), int(s.PIEDS * K - jn.height + 6)))
        s._pose(im, s._cache.setdefault("t7", _deux("7 SORTES DE GENS", OR_, 64, "À L'OMBRE CE JOUR-LÀ", BLANC, 48)),
                W_ / 2, 60 * K, e)
        s._pose(im, s._cache.setdefault("tj", _deux("DONT LE JEUNE QUI A GRANDI", BLANC, 44, "EN ADORANT ALLAH", JAUNE, 50)),
                W_ / 2, (s.PIEDS + 5) * K, ej)
        return im


# ---------------------------------------------------------------- {brulure}
class Brulure(_Base):
    """{brulure} : accroche, gros plan sur la cuisinière : le doigt de Petit touche le bord de la poêle chaude AVANT le
    mot et recule pile sur lui ; le bout du doigt rougit, « AÏE ! », petite vapeur. Rien de plus."""
    negatif = True
    ELAN = 0.5

    def __init__(s, cmd, who="PETIT"):
        super().__init__(cmd)
        s.who = who

    def sons_el(s):
        return [(-0.4, "dv_feu_allumage", 0.025, None), (0.0, "tr_whoosh_doux", 0.03, None)]

    def _fond(s):
        if "f" in s._cache:
            return s._cache["f"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        mur = c.mask_rect(0, 0, W, 98) & tout_
        c.fill(mur, (226, 234, 240))
        for x in range(0, W, 14):
            c.fill(c.mask_rect(x, 0, x + 1, 98) & mur, (196, 208, 218))
        for y in range(0, 98, 14):
            c.fill(c.mask_rect(0, y, W, y + 1) & mur, (196, 208, 218))
        plaque = c.mask_rect(0, 98, W, H) & tout_
        c.shape(plaque, (58, 58, 66), shade=(40, 40, 46), light=(90, 90, 100), band=2, olcol=OL)
        c.fill(c.mask_ell(76, 106, 42, 6) & plaque, (36, 36, 42))                    # le brûleur
        c.fill(c.mask_ell(76, 106, 30, 4) & plaque, (80, 80, 90))
        s._cache["f"] = c
        return c

    def image(s, u):
        K = s.K
        from explique import _copie
        c = _copie(s._fond())
        for j, fx in enumerate(range(40, 114, 8)):                                  # les flammes bleues
            h = 5 + 2 * math.sin(u * 9 + j * 1.7)
            c.fill(c.mask_poly([(fx - 3, 103), (fx, 103 - h), (fx + 3, 103)]), (80, 140, 255))
            c.fill(c.mask_poly([(fx - 1.5, 103), (fx, 103 - h * 0.6), (fx + 1.5, 103)]), (200, 230, 255))
        poele = c.mask_poly([(48, 86), (120, 86), (114, 99), (54, 99)])             # la poêle
        c.shape(poele, (40, 40, 48), shade=(24, 24, 30), light=(86, 86, 98), band=2, olcol=OL)
        c.fill(c.mask_rect(48, 86, 120, 88), (110, 110, 122))
        manche = c.mask_rrect(118, 88, 166, 93, 2)
        c.shape(manche, (30, 30, 36), shade=(18, 18, 22), light=(70, 70, 80), band=1, olcol=OL)
        # la main : l'index tendu arrive de la gauche, touche le bord de la poêle, recule
        e = smooth((u + s.ELAN) / s.ELAN)
        v = u
        recul = (-10 * smooth(v / 0.12) - 6 * smooth((v - 0.1) / 0.5)) if v >= 0 else 0.0
        tip_x = 48 - 34 * (1 - e) + recul
        tip_y = 84 - 10 * (1 - e) - (8 * smooth(v / 0.3) if v >= 0 else 0)
        rouge = smooth((v - 0.05) / 0.4) if v >= 0 else 0.0
        p = _peau(s.who)
        b, s_, h = p["b"], p["s"], p["h"]
        X, Y, S = tip_x, tip_y, 1.45                                               # S : la main en plus grand

        def P(dx, dy):
            return (X + dx * S, Y + dy * S)
        manche_ = c.mask_poly([P(-100, -9), P(-56, -8), P(-54, 12), P(-100, 15)])
        c.shape(manche_, (200, 50, 50), shade=(150, 34, 40), light=(232, 92, 84), band=1, olcol=OL)
        c.fill(manche_ & c.mask_rect(P(-60, 0)[0], 0, P(-54, 0)[0], c.h), (150, 34, 40))
        poing = c.mask_poly([P(-58, -6), P(-22, -7), P(-16, -2), P(-18, 9), P(-30, 12), P(-58, 11)])
        c.shape(poing, b, shade=s_, light=h, band=1, olcol=OL)
        for j in range(3):
            x_, y_ = P(-30 + j * 4, 3)
            c.fill(c.mask_rect(x_, y_, x_ + 1, y_ + 6 * S), s_)
        index = c.mask_rrect(*P(-24, -5), *P(1, 1), 3)
        c.shape(index, b, shade=s_, light=h, band=1, olcol=OL)
        if rouge > 0:
            bout = c.mask_rrect(*P(-7, -5), *P(1, 1), 3) & index
            c.fill(bout, tuple(int(v_ + (w - v_) * rouge) for v_, w in zip(b, (236, 92, 84))))
        c.fill(c.mask_rect(*P(-5, -4), *P(-1, -3)), (250, 230, 220))                # l'ongle
        pouce = c.mask_poly([P(-40, -7), P(-34, -12), P(-26, -12), P(-24, -8)])
        c.shape(pouce, b, shade=s_, light=h, band=1, olcol=OL)
        im = c.img(K, rgba=True)
        d = ImageDraw.Draw(im)
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for j in range(4):                                                          # la vapeur de la poêle
            vv = ((u + j * 0.45) % 1.8) / 1.8
            x = (64 + j * 16) * K + 10 * math.sin(u * 2 + j)
            y = 84 * K - 260 * vv
            a = int(170 * smooth(vv / 0.2) * (1 - smooth((vv - 0.6) / 0.4)))
            ld.line([(x + 14 * math.sin(vv * 8 + k_), y - k_ * 18) for k_ in range(5)], fill=(255, 255, 255, a), width=9)
        if v >= 0:
            pf = smooth(v / 0.4)
            for j in range(5):                                                      # « pschitt » au contact
                r_ = (12 + 40 * pf) * (0.6 + 0.2 * j)
                a = int(200 * (1 - smooth((v - 0.2) / 0.4)))
                cx_, cy_ = 48 * K + 20 * j - 40, 82 * K - 30 * pf * K / 2 - 10 * j
                if a > 0:
                    ld.ellipse([cx_ - r_, cy_ - r_, cx_ + r_, cy_ + r_], fill=(255, 255, 255, a))
        im.alpha_composite(lay)
        if v >= 0:
            ai = s._cache.setdefault("aie", _titre("AÏE !", ORANGE, 170, r=5))
            a = smooth((v - 0.03) / 0.2)
            k2 = 0.85 + 0.15 * smooth(v / 0.25)
            a2 = ai.resize((int(ai.width * k2), int(ai.height * k2)), Image.LANCZOS)
            im.alpha_composite(_fade(a2, a), (int(W_milieu(im) - a2.width / 2 + 60), int(150 - a2.height / 2)))
            _frissons(d, (tip_x - 6) * K, (tip_y - 2) * K, 22 * K, u, K, col=(255, 200, 120))
        return im


def W_milieu(im):
    return im.width / 2


# ---------------------------------------------------------------- {braises …}
class Braises(_Base):
    """{braises} : le moins puni de l'Enfer (Boukhari 6562) : une silhouette sombre (sans visage), deux braises sous la
    plante des pieds, la chaleur qui monte, des bulles au-dessus de la tête, la marmite qui bout ; {braises pense} :
    bulle « PERSONNE N'EST PLUS PUNI QUE MOI » puis « … ET C'EST LE MOINS PUNI » (Mouslim 213)."""
    PIEDS = 124
    KP = 5
    ETAPES = ("pense",)

    def __init__(s, cmd):
        super().__init__(cmd)

    def sons_el(s):
        return [(0.0, "dv_feu_allumage", 0.03, None)]

    def _fond(s):
        if "f" in s._cache:
            return s._cache["f"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        c.vgrad(tout_, 0, H, (22, 8, 14), (84, 20, 12), steps=7)
        s._cache["f"] = c
        return c

    def image(s, u):
        K = s.K
        from explique import _copie
        c = _copie(s._fond())
        _flammes(c, 0, 176, 152, u, haut=16, col=(150, 30, 20), coeur=(220, 80, 30), pas=14)
        im = c.img(K, rgba=True)
        W_, H_ = im.size
        cle = "sil"
        if cle not in s._cache:
            s._cache[cle] = _grand(_silhouette(_sprite("VOYAGEUR", "neutre", "neutre"), (12, 8, 14), rim=(255, 130, 60),
                                               rim_bas=(150, 50, 24)), s.KP)
        sil = s._cache[cle]
        sx, sy = W_ / 2 - sil.width / 2, s.PIEDS * K - sil.height
        # une lueur rouge derrière lui (pour qu'on voie sa silhouette), la chaleur qui monte des pieds à la tête
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.ellipse([W_ / 2 - 260, sy - 60, W_ / 2 + 260, s.PIEDS * K + 60], fill=(210, 70, 30, 150))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(50)))
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        tete_x, tete_y = W_ / 2 + 2, sy + 22 * s.KP
        for j in range(3):
            x = W_ / 2 - 70 + j * 70
            pts = [(x + 18 * math.sin((y / 46) - u * 6 + j), y) for y in range(int(s.PIEDS * K), int(tete_y), -16)]
            if len(pts) > 1:
                ld.line(pts, fill=(255, 160, 60, 140), width=12)
        ld.ellipse([tete_x - 70, tete_y - 70, tete_x + 70, tete_y + 60], fill=(255, 70, 30, int(110 + 40 * math.sin(u * 5))))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(16)))
        im.alpha_composite(sil, (int(sx), int(sy)))
        d = ImageDraw.Draw(im)
        # deux braises sous la plante des pieds
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for fx in (W_ / 2 - 34, W_ / 2 + 24):
            ld.ellipse([fx - 70, s.PIEDS * K - 34, fx + 70, s.PIEDS * K + 34], fill=(255, 120, 40, 220))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(18)))
        for j, fx in enumerate((W_ / 2 - 34, W_ / 2 + 24)):
            br = 0.8 + 0.2 * math.sin(u * 7 + j * 2)
            d.ellipse([fx - 40, s.PIEDS * K - 15, fx + 40, s.PIEDS * K + 15], fill=(255, int(120 * br) + 40, 40, 255),
                      outline=(90, 20, 10, 255), width=4)
            d.ellipse([fx - 20, s.PIEDS * K - 7, fx + 20, s.PIEDS * K + 7], fill=(255, 232, 150, 255))
        rng = np.random.default_rng(int(u * 9) % 997)
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for _ in range(8):                                                          # étincelles
            x = W_ / 2 + rng.uniform(-90, 90)
            y = s.PIEDS * K - rng.uniform(0, 120)
            ld.rectangle([x, y, x + 6, y + 6], fill=(255, 200, 90, 220))
        # les bulles au-dessus de la tête (« son cerveau bout »)
        for j in range(7):
            vv = ((u * 1.3 + j * 0.37) % 1.0)
            x = W_ / 2 - 50 + (j * 37) % 100 + 6 * math.sin(u * 4 + j)
            y = sy + 12 - 140 * vv
            r_ = 10 + 8 * ((j * 3) % 4) * (1 - vv)
            a = int(230 * smooth(vv / 0.15) * (1 - smooth((vv - 0.75) / 0.25)))
            ld.ellipse([x - r_, y - r_, x + r_, y + r_], outline=(255, 210, 150, a), width=5)
            ld.ellipse([x - r_ * 0.35, y - r_ * 0.6, x, y - r_ * 0.2], fill=(255, 255, 255, a))
        # la marmite qui bout, à côté
        mx, my = 830, 330
        ld.ellipse([mx - 90, my - 20, mx + 90, my + 20], fill=(255, 120, 40, 120))
        im.alpha_composite(lay)
        d.chord([mx - 80, my - 70, mx + 80, my + 70], 0, 180, fill=(40, 34, 40, 255), outline=(14, 10, 16, 255), width=6)
        d.rectangle([mx - 92, my - 10, mx + 92, my + 6], fill=(60, 54, 62, 255), outline=(14, 10, 16, 255), width=5)

        def bulles(dd):
            for j in range(5):
                vv = ((u * 1.6 + j * 0.23) % 1.0)
                x = mx - 50 + j * 25
                y = my - 18 - 70 * vv
                dd.ellipse([x - 9, y - 9, x + 9, y + 9], outline=(255, 230, 200, int(220 * (1 - vv))), width=4)
        _translucide(im, bulles)
        s._pose(im, s._lab("COMME UNE MARMITE // QUI BOUT", ORANGE, 40), mx, my + 110, smooth((u - 0.8) / 0.4), maxw=330)
        s._pose(im, s._lab("LE MOINS PUNI // DE L'ENFER", ROUGE, 70), W_ / 2, 70, smooth(u / 0.35))
        ap = s._a("pense", u, 0.35)
        lab_bas = s._lab("2 BRAISES SOUS LES PIEDS", ORANGE, 50)
        lab_fin = s._lab("… ET C'EST LE MOINS PUNI", JAUNE, 54)
        af = s._e("pense", u, 0.4, dec=1.2)
        s._pose(im, lab_bas, W_ / 2, (s.PIEDS + 12) * K, smooth((u - 0.3) / 0.35) * (1 - af))
        s._pose(im, lab_fin, W_ / 2, (s.PIEDS + 12) * K, af)
        if ap > 0:
            b = s._cache.get("bp")
            if b is None:
                b = s._cache["bp"] = _bulle([("« PERSONNE N'EST", BLANC), ("PLUS PUNI QUE MOI »", BLANC)],
                                            fond=(70, 24, 40), size=40, queue=0.82, pensee=True)
            im.alpha_composite(_fade(b, ap), (int(30), int(230 + 10 * (1 - ap))))
        return im


# ---------------------------------------------------------------- {datte …}
def _datte():
    c = Px(26, 36, alpha=True)
    m = c.mask_ell(13, 18, 11, 16.5)
    c.shape(m, (122, 62, 34), shade=(84, 40, 22), light=(176, 100, 56), band=2, olcol=OL)
    for (x0, y0, x1, y1) in ((8, 8, 10, 28), (15, 6, 16, 22), (12, 24, 19, 30)):
        c.line(x0, y0, x1, y1, (96, 48, 26))
    c.fill(c.mask_rect(9, 8, 11, 12) & m, (210, 140, 90))
    c.fill(c.mask_rect(11, 0, 15, 3), (160, 130, 80))                               # la queue
    return c


def _tacos():
    c = Px(40, 30, alpha=True)
    m = c.mask_rrect(0, 4, 40, 28, 5)
    c.shape(m, (232, 196, 132), shade=(196, 156, 98), light=(250, 224, 170), band=2, olcol=OL)
    for x in range(5, 36, 7):                                                       # les marques du grill
        c.fill(c.mask_poly([(x, 6), (x + 3, 6), (x - 2, 26), (x - 5, 26)]) & m, (170, 120, 70))
    coupe = c.mask_rect(33, 6, 40, 26)                                              # la coupe : frites, sauce
    c.fill(coupe & m, (250, 220, 120))
    for y in range(8, 25, 4):
        c.fill(c.mask_rect(34, y, 40, y + 2) & m, (255, 236, 150))
    c.fill(c.mask_rect(33, 12, 40, 14) & m, (230, 120, 60))
    return c


class Datte(_Base):
    """{datte} : une datte se coupe en deux, une moitié part dans une main tendue, un bouclier de lumière se lève
    devant le feu : « PROTÈGE-TOI DU FEU, MÊME AVEC LA MOITIÉ D'UNE DATTE » (Boukhari 1417) ; {datte tacos} la moitié
    de datte devient une moitié de tacos ; {datte parole} « UNE BONNE PAROLE » (Boukhari 6540)."""
    ETAPES = ("tacos", "parole")

    def __init__(s, cmd):
        super().__init__(cmd)

    def sons_el(s):
        out = [(0.45, "sa_ting", 0.03, None), (1.1, "sa_scintillement", 0.05, None)]
        for nom in ("tacos", "parole"):
            if nom in s.t:
                out.append((s.t[nom], "sa_ting", 0.03, None))
        return out

    def _moities(s):
        if "m" not in s._cache:
            dt = _datte().img(9, rgba=True)
            w = dt.width // 2
            s._cache["m"] = (dt.crop((0, 0, w, dt.height)), dt.crop((w, 0, dt.width, dt.height)), dt)
        return s._cache["m"]

    def image(s, u):
        W_, H_ = 1020, 960
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        c = Px(170, 40, alpha=True)                                                 # le feu, en bas
        _flammes(c, 0, 176, 40, u, haut=22, col=(200, 60, 24), coeur=(255, 170, 60), pas=12)
        es = smooth((u - 1.1) / 0.6)                                                # le bouclier se lève
        feu = c.img(6, rgba=True)
        if es > 0:
            a = np.array(feu)
            xs = np.arange(feu.width)
            att = 1 - 0.75 * es * np.clip(1 - np.abs(xs - feu.width / 2) / 330, 0, 1)
            a[..., 3] = (a[..., 3] * att[None, :]).astype(np.uint8)
            feu = Image.fromarray(a, "RGBA")
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).rectangle([0, H_ - 200, W_, H_], fill=(200, 50, 20, 110))
        im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(40)))
        im.alpha_composite(feu, (0, H_ - feu.height))
        if es > 0:
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ld = ImageDraw.Draw(lay)
            ld.chord([W_ / 2 - 330, H_ - 420, W_ / 2 + 330, H_ + 240], 180, 360, fill=(255, 220, 120, int(120 * es)))
            im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(16)))
            bo = s._cache.setdefault("bouclier", autocollant(objets.icone("bouclier").img(15), r=5))
            k2 = 0.8 + 0.2 * es
            b2 = bo.resize((int(bo.width * k2), int(bo.height * k2)), Image.LANCZOS)
            im.alpha_composite(_fade(b2, es), (int(W_ / 2 - b2.width / 2), int(H_ - 300 - b2.height / 2)))
        g, dr, entiere = s._moities()
        e_c = smooth((u - 0.35) / 0.5)                                              # elle se coupe en deux
        cx, cy = W_ / 2, 340
        if e_c <= 0:
            im.alpha_composite(entiere, (int(cx - entiere.width / 2), int(cy - entiere.height / 2)))
        else:
            im.alpha_composite(g, (int(cx - g.width - 20 * e_c), int(cy - g.height / 2)))
            hx, hy = 820, 520                                                       # la main tendue qui reçoit
            md = s._cache.get("main")
            if md is None:
                p = _peau("PAPI")
                mc = Px(48, 30, alpha=True)
                manche = mc.mask_poly([(30, 14), (48, 12), (48, 26), (32, 28)])
                mc.shape(manche, (120, 104, 90), shade=(90, 76, 66), light=(150, 132, 116), band=1, olcol=OL)
                paume = mc.mask_poly([(6, 12), (32, 12), (34, 18), (30, 26), (12, 27), (4, 22)])
                mc.shape(paume, p["b"], shade=p["s"], light=p["h"], band=1, olcol=OL)
                for j in range(4):                                                  # les doigts repliés vers le haut
                    doigt = mc.mask_rrect(3 + 5 * j, 6 + (j % 2), 7 + 5 * j, 15, 2)
                    mc.shape(doigt, p["b"], shade=p["s"], light=p["h"], band=1, olcol=OL)
                pouce = mc.mask_poly([(26, 13), (30, 5), (34, 6), (33, 14)])
                mc.shape(pouce, p["b"], shade=p["s"], light=p["h"], band=1, olcol=OL)
                c_ = mc.mask_rect(8, 15, 30, 17) & paume                            # le creux de la main
                mc.fill(c_, p["s"])
                md = s._cache["main"] = mc.img(6, rgba=True)
            em = smooth((u - 0.2) / 0.4)
            im.alpha_composite(_fade(md, em), (int(hx - md.width / 2), int(hy)))
            f = smooth((u - 0.6) / 0.6)
            x = cx + (hx - 20 - cx) * f
            y = cy + (hy - 80 - cy) * f - 90 * math.sin(math.pi * f)
            at = s._e("tacos", u, 0.4)
            if at < 1:
                im.alpha_composite(_fade(dr, 1 - at), (int(x - dr.width / 2), int(y - dr.height / 2)))
            if at > 0:
                tc = s._cache.setdefault("tacos", _tacos().img(6, rgba=True))
                im.alpha_composite(_fade(tc, at), (int(x - tc.width / 2), int(y - tc.height / 2)))
        s._pose(im, s._cache.setdefault("t1", _deux("PROTÈGE-TOI DU FEU", OR_, 64, "MÊME AVEC LA MOITIÉ D'UNE DATTE", BLANC, 44)),
                W_ / 2, 70, smooth((u - 0.1) / 0.35))
        s._pose(im, s._lab("UNE AUMÔNE AUSSI", JAUNE, 44), 820, 400, s._e("tacos", u, 0.3, dec=0.3), maxw=380)
        ap = s._a("parole", u, 0.35)
        if ap > 0:
            bp = s._cache.get("bpar")
            if bp is None:
                co = objets.icone("coeur").img(6)
                b = _bulle([("UNE BONNE", BLANC), ("PAROLE", JAUNE)], fond=(40, 90, 70), size=50, queue=0.25)
                bp = Image.new("RGBA", (b.width + 20, b.height + co.height // 2), (0, 0, 0, 0))
                bp.alpha_composite(b, (0, co.height // 2))
                bp.alpha_composite(co, (b.width - co.width + 10, 0))
                s._cache["bpar"] = bp
            im.alpha_composite(_fade(bp, ap), (20, int(360 + 14 * (1 - ap))))
        return im


# ---------------------------------------------------------------- branchement dans explique.Schema
CLES = ("cent", "chemin", "bute", "double", "ecran", "écran", "dua", "tombeau", "chaleur", "soleil", "brulure",
        "brûlure", "braises", "datte")


def _norm(m):
    return m.lower().replace("é", "e").replace("û", "u").replace("×", "x")


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

    if k == "cent":
        schema._ajoute(t, Chemin(brut, "cent"))
    elif k == "chemin":
        if sous in Chemin.ETAPES:
            etape(Chemin, sous, "chemin", lambda: Chemin(brut, "chemin"))
        else:
            schema._ajoute(t, Chemin(brut, "chemin"))
    elif k == "bute":
        schema._ajoute(t, Double(brut, "bute", qui if qui in ("PETIT", "GRAND") else "PETIT"))
    elif k == "double":
        if sous == "anges":
            schema._ajoute(t, Double(brut, "anges"))
        elif sous in Double.ETAPES:
            etape(Double, sous, "double", lambda: Double(brut, "double"))
        else:
            schema._ajoute(t, Double(brut, "double"))
    elif k == "ecran":
        schema._ajoute(t, Ecran(brut, "chute"))
    elif k == "dua":
        if sous in Ecran.ETAPES:
            etape(Ecran, sous, "dua", lambda: Ecran(brut, "dua"))
        else:
            schema._ajoute(t, Ecran(brut, "dua"))
    elif k == "tombeau":
        if sous in Tombeau.ETAPES:
            etape(Tombeau, sous)
        else:
            schema._ajoute(t, Tombeau(brut))
    elif k == "chaleur":
        schema._ajoute(t, Chaleur(brut, qui if qui in ("PETIT", "GRAND") else "PETIT"))
    elif k == "soleil":
        if sous == "ombre":
            schema._ajoute(t, Soleil(brut, "ombre"))
        elif sous in Soleil.ETAPES:
            el = dernier(Soleil)
            if el is None:
                el = Soleil(brut, "ombre" if sous == "jeune" else "soleil")
                schema._ajoute(t, el)
            el.t[sous] = u_de(el)
        else:
            schema._ajoute(t, Soleil(brut, "soleil"))
    elif k == "brulure":
        schema._ajoute(t, Brulure(brut))
    elif k == "braises":
        if sous in Braises.ETAPES:
            etape(Braises, sous)
        else:
            schema._ajoute(t, Braises(brut))
    elif k == "datte":
        if sous in Datte.ETAPES:
            etape(Datte, sous)
        else:
            schema._ajoute(t, Datte(brut))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "cent":
        return t + 1.6
    if k == "chemin":
        return t + dict(mort=1.2, anges=1.4, rapproche=1.7, mesure=1.9, pardon=1.3).get(sous, 0.8)
    if k == "bute":
        return t + 1.6
    if k == "double":
        return t + dict(x2=1.3, anges=1.8).get(sous, 0.9)
    if k == "ecran":
        return t + 1.2
    if k == "dua":
        return t + dict(choisit=1.5, iphone=0.9).get(sous, 1.0)
    if k == "tombeau":
        return t + dict(anges=2.4, paradis=2.5, cri=1.4, crie=2.4).get(sous, 1.0)
    if k == "chaleur":
        return t + 1.4
    if k == "soleil":
        return t + (1.8 if sous in ("ombre", "jeune") else 0.9)
    if k == "brulure":
        return t + 1.4
    if k == "braises":
        return t + (1.8 if sous == "pense" else 1.4)
    if k == "datte":
        return t + (1.8 if not sous else 1.2)
    return None
