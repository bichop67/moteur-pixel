# EXPLICATIONS EN IMAGES : pendant qu'un perso explique, la vidéo passe sur un schéma animé dont chaque élément
# apparaît PILE sur le mot (miroir, photo, téléphone qui recule, chiffre qui monte, flèches, icônes…).
# Dans un scénario texte, on écrit les éléments entre accolades, à l'endroit exact du texte :
#   ETUDIANT (explique) : Dans le miroir, {miroir ADA grain} tu te vois à l'envers.
# (les accolades ne sont ni dites par la voix ni écrites dans les sous-titres). Liste des éléments : ELEMENTS ci-dessous.
import math, re
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import pxv, duo, cast, objets
from pxv import smooth
from px import Px

SEGOE = pxv.SEGOE_BLACK
BLANC, JAUNE, ENCRE = (255, 255, 255), (255, 214, 70), (22, 18, 30)

ELEMENTS = """
{perso ADA}                 le visage d'un perso (face=choc… possible : {perso ADA choc})
{miroir ADA}                le perso dans un miroir (image inversée) ; + grain : grain de beauté pour voir l'inversion
{photo ADA}                 le perso sur une photo (à l'endroit) ; + grain
{compare ADA}               miroir et photo côte à côte + flèche « INVERSÉ »
{icone cerveau}             une icône du catalogue, en grand (74 icônes : coeur, argent, horloge…)
{chiffre +30 %}             un chiffre qui monte jusqu'à sa valeur
{texte "C'EST TA VRAIE TÊTE"}  une phrase en gros sous le schéma
{fleche}  {fleche POURQUOI ?}  {double-fleche INVERSÉ}   une flèche entre les deux derniers éléments
{distance ADA 30 cm -> 1,5 m}  le téléphone recule, la règle s'allonge, le visage se déforme de moins en moins
{check}  {croix}            tampon vert / rouge sur le dernier élément
{source "WARD ET AL., 2018"}   la source, en petit en bas
{efface}                    tout disparaît en fondu (on recommence un schéma)
{coran}                     un Coran ouvert : la lumière suit la ligne, « +1 » par lettre lue (« +10 » après {chiffre ×10})
{defile}                    un téléphone dont le fil défile très vite (on scrolle)
{fond tableau}              le fond du schéma (par défaut : le décor de la scène, flou et assombri)
{radio PETIT}               radiographie : squelette, articulations rouges, compteur « 0 / 360 » ;
                            {radio articulations} une vague les montre ; {radio +1 "SUBHAN ALLAH"} une passe au vert ;
                            {radio reste} « ENCORE 357 ! » ; {radio tout "2 RAKATS DE DUHA"} toutes passent au vert
{orteil}                    gros plan : le pied qui se cogne contre le pied du lit (étoile, orteil rouge, « AÏE ! »)
{arbre "TES PÉCHÉS"}        un arbre aux feuilles sombres « PÉCHÉ » ; {feuilles} : elles tombent une à une
{balance "A" "B"}           une balance : A (le monde) contre B ; {balance + manette} un objet de plus ;
                            {balance pese} : elle penche lentement du côté de B
{fievre PETIT}              04/11 (explique_0411.py) : Petit malade, le thermomètre monte à 39,5 °C
{forge "…"} {soufflet}      la forge : le soufflet souffle, les croûtes « PÉCHÉ » partent, le fer brille
{glace}                     l'eau glacée du robinet sur les mains, « BRRR ! »
{ablutions PETIT}           {ablutions yeux|mains|pieds} : le voile « PÉCHÉ » part en lumière avec l'eau
{cauchemar PETIT}           la nuit : bulle de cauchemar, il se réveille en sursaut
{gestes PETIT}              {gestes souffle|refuge|tourne|chut|protege} : les gestes après un cauchemar
"""
CLES_0411 = ("fievre", "fièvre", "forge", "soufflet", "glace", "ablutions", "cauchemar", "gestes")
# 04/11 soir (explique_0411b.py) : {cent} {chemin …} {bute} {double …} {ecran} {dua …} {tombeau …} {chaleur}
# {soleil …} {brulure} {braises …} {datte …} — voir l'en-tête de explique_0411b.py
CLES_0411B = ("cent", "chemin", "bute", "double", "ecran", "écran", "dua", "tombeau", "chaleur", "soleil",
              "brulure", "brûlure", "braises", "datte")
# 07/11 (explique_0611.py + 6 modules) : {jure} {serment …} {atchoum} {chaine …} {rhume …} {enerve} {colere …}
# {porte} {maison …} {sms} {dette …} {carnet} {lit} {sommeil …} — voir l'en-tête de explique_0611.py
CLES_0611 = ("jure", "serment", "atchoum", "chaine", "rhume", "enerve", "colere", "colère", "porte", "maison",
             "sms", "dette", "carnet", "lit", "sommeil")
# 08/11 (explique_0811.py + 9 modules chargés à la demande) : {talon} {talons …} {gouttes} {tombes …} {repas}
# {maindroite …} {imam} {ane …} {soleilbas} {asr …} {ghiba} {chair …} {oreille} {plomb …} {astro} {quarante …}
# {coucher} {crepuscule …} — voir l'en-tête de explique_0811.py
CLES_0811 = ("talon", "talons", "gouttes", "tombes", "repas", "maindroite", "imam", "ane", "âne", "soleilbas",
             "asr", "ghiba", "chair", "oreille", "plomb", "astro", "quarante", "coucher", "crepuscule",
             "crépuscule")
# 09/11 (briques.py) : BRIQUES RÉUTILISABLES, réglées depuis le scénario (aucun code par sujet) : {liste …}
# {citation …} {jauge …} {focus …} {versus …} {bulles …} {trajet …} {grille …} — voir l'en-tête de briques.py
CLES_BRIQUES = ("liste", "citation", "jauge", "focus", "versus", "bulles", "trajet", "grille")


# ---------------------------------------------------------------- petits outils d'image
def _contour(im, r, col=BLANC):
    a = np.array(im)[..., 3] > 0
    e = a.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                e |= np.roll(np.roll(a, dy, 0), dx, 1)
    out = np.zeros(np.array(im).shape, np.uint8)
    out[e] = (*col, 255)
    o = Image.fromarray(out, "RGBA")
    o.alpha_composite(im)
    return o


def autocollant(im, r=6, ombre=True):
    """Style « autocollant » (comme les miniatures) : contour blanc épais + ombre douce."""
    pad = r + 14
    big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    big.alpha_composite(im, (pad, pad))
    big = _contour(big, r)
    if not ombre:
        return big
    sh = Image.new("RGBA", big.size, (0, 0, 0, 0))
    sh.putalpha(Image.fromarray(((np.array(big)[..., 3] > 0) * 120).astype(np.uint8)))
    sh = sh.filter(ImageFilter.GaussianBlur(7))
    out = Image.new("RGBA", (big.width + 10, big.height + 12), (0, 0, 0, 0))
    out.alpha_composite(sh, (8, 10))
    out.alpha_composite(big, (0, 0))
    return out


def _fade(im, a):
    if a >= 0.999:
        return im
    im = im.copy()
    im.putalpha(Image.fromarray((np.array(im)[..., 3] * max(0.0, a)).astype(np.uint8)))
    return im


def titre_img(txt, col=BLANC, size=64):
    return pxv.big_title([(txt, col)], size=size)


def petit_texte(txt, col=BLANC, ol=(30, 24, 40), size=9, k=4):
    return pxv.pixel_text(txt, col, ol, size=size, k=k, ol2=(12, 10, 16))


# ---------------------------------------------------------------- visages
def grain_xy(who, face="neutre"):
    """Position du grain de beauté sur la tête (pixels du dessin), comme dans tete(…, grain=True)."""
    r = cast.CAST[who]
    a = cast.dessine(r, "neutre", face, False).a
    g = cast.geo(r)
    zone = a[max(0, g.y0 - 14):g.y0 + 2, 8:36, 3]
    rows = np.where(zone.max(axis=1) > 0)[0]
    top = min(max(0, g.y0 - 14) + (int(rows[0]) if len(rows) else 14), g.y0 - 1)
    return g.hd["ex"] - 8 + 1, g.y0 + g.hd["ey"] - top + 5


def tete(who, face="neutre", grain=False):
    """Tête et épaules du perso (tableau RGBA, regard vers la droite) + position du nez."""
    if cast.has(who):
        r = cast.CAST[who]
        a = cast.dessine(r, "neutre", face, False).a
        g = cast.geo(r)
        zone = a[max(0, g.y0 - 14):g.y0 + 2, 8:36, 3]
        rows = np.where(zone.max(axis=1) > 0)[0]
        top = min(max(0, g.y0 - 14) + (int(rows[0]) if len(rows) else 14), g.y0 - 1)
        a = a[top: g.y0 + 26, 8:36].copy()
        nx, ny = g.hd["nose"][0] - 8, g.y0 + g.hd["nose"][1] - top
        if grain:                                             # grain de beauté sur la joue : on voit l'inversion
            gx, gy = g.hd["ex"] - 8 + 1, g.y0 + g.hd["ey"] - top + 5
            a[gy, gx, :3] = (70, 40, 34)
            a[gy, gx, 3] = 255
        return a, (nx, ny)
    a = duo.portrait(who, face).copy()
    return a, (a.shape[1] * 2 // 3, a.shape[0] // 2)


def deforme(im, cx, cy, rayon, force):
    """Effet « objectif trop près » : le centre du visage (le nez) grossit. force 0 = aucune déformation."""
    if force <= 0.001:
        return im
    a = np.array(im)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = xx - cx, yy - cy
    d = np.sqrt(dx * dx + dy * dy) / rayon
    m = np.clip(1 - d, 0, 1) ** 2 * force
    sx = np.clip(cx + dx * (1 - m), 0, w - 1).astype(np.int32)
    sy = np.clip(cy + dy * (1 - m), 0, h - 1).astype(np.int32)
    return Image.fromarray(a[sy, sx], "RGBA")


def visage_img(who, face="neutre", grain=False, k=9, miroir=False, nez=0.0):
    a, (nx, ny) = tete(who, face, grain)
    im = Image.fromarray(a, "RGBA").resize((a.shape[1] * k, a.shape[0] * k), Image.NEAREST)
    if nez:
        im = deforme(im, (nx + 0.5) * k, (ny + 0.5) * k, 13 * k, nez)
    if miroir:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im


# ---------------------------------------------------------------- les éléments
class Element:
    plein = False                     # True : prend tout le schéma (les autres s'effacent)
    label = None

    def __init__(s, cmd):
        s.cmd = cmd
        s._img = None

    def image(s, u):                  # u = temps depuis l'apparition
        if s._img is None:
            s._img = s.fabrique()
        return s._img


class Perso(Element):
    def __init__(s, cmd, who, face="neutre", grain=False):
        super().__init__(cmd)
        s.who, s.face, s.grain = who, face, grain

    def fabrique(s):
        v = visage_img(s.who, s.face, s.grain, k=14)
        fond = Image.new("RGBA", (v.width + 40, v.height + 30), (236, 232, 244, 255))
        ImageDraw.Draw(fond).rectangle([0, 0, fond.width - 1, fond.height - 1], outline=(*ENCRE, 255), width=6)
        fond.alpha_composite(v, (20, 30))
        return autocollant(fond)


class Miroir(Element):
    label = "MIROIR"

    def __init__(s, cmd, who, face="neutre", grain=False):
        super().__init__(cmd)
        s.who, s.face, s.grain = who, face, grain

    def fabrique(s):
        v = visage_img(s.who, s.face, s.grain, k=13, miroir=True)
        W_, H_ = v.width + 90, v.height + 110
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 46, fill=(196, 150, 70, 255), outline=(*ENCRE, 255), width=6)
        d.rounded_rectangle([14, 14, W_ - 15, H_ - 15], 36, fill=(232, 196, 110, 255))
        d.rounded_rectangle([30, 30, W_ - 31, H_ - 31], 28, fill=(170, 206, 222, 255), outline=(120, 86, 40, 255), width=5)
        glace = Image.new("RGBA", (W_ - 70, H_ - 70), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glace)
        for i in range(glace.height):                              # verre : léger dégradé
            c = int(214 - 40 * i / glace.height)
            gd.line([(0, i), (glace.width, i)], fill=(c - 30, c, min(255, c + 22), 255))
        glace.alpha_composite(v, ((glace.width - v.width) // 2, glace.height - v.height))
        m = Image.new("L", glace.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, glace.width - 1, glace.height - 1], 24, fill=255)
        im.paste(glace, (35, 35), m)
        s._glace = (35, 35, glace.size, m)
        if s.grain and cast.has(s.who):                            # le grain de beauté (image inversée)
            gx, gy = grain_xy(s.who, s.face)
            s.grain_pos = (20 + 35 + (glace.width - v.width) // 2 + v.width - (gx + 0.5) * 13,
                           20 + 35 + glace.height - v.height + (gy + 0.5) * 13)
        return im

    def image(s, u):                                               # reflet qui passe lentement sur le verre
        base = autocollant_cache(s, super().image(u))
        x0, y0, (gw, gh), m = s._glace
        x0, y0 = x0 + 20, y0 + 20                                  # décalage de l'autocollant (contour + marge)
        ph = (u * 0.45) % 1.6
        if ph > 1.0:
            return base
        im = base.copy()
        band = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
        bd = ImageDraw.Draw(band)
        x = -gh + (gw + 2 * gh) * ph
        bd.polygon([(x, gh), (x + 60, gh), (x + 60 + gh, 0), (x + gh, 0)], fill=(255, 255, 255, 70))
        bd.polygon([(x + 80, gh), (x + 96, gh), (x + 96 + gh, 0), (x + 80 + gh, 0)], fill=(255, 255, 255, 50))
        lay = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
        lay.paste(band, (0, 0), m)
        im.alpha_composite(lay, (x0, y0))
        return im


def autocollant_cache(el, base):
    if getattr(el, "_auto", None) is None:
        el._auto = autocollant(base)
    return el._auto


class Photo(Element):
    label = "PHOTO"

    def __init__(s, cmd, who, face="neutre", grain=False):
        super().__init__(cmd)
        s.who, s.face, s.grain = who, face, grain

    def fabrique(s):
        v = visage_img(s.who, s.face, s.grain, k=13)
        W_, H_ = v.width + 60, v.height + 120
        im = Image.new("RGBA", (W_, H_), (250, 248, 242, 255))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W_ - 1, H_ - 1], outline=(*ENCRE, 255), width=6)
        d.rectangle([24, 24, W_ - 25, 24 + v.height + 16], fill=(150, 186, 214, 255), outline=(*ENCRE, 255), width=4)
        im.alpha_composite(v, ((W_ - v.width) // 2, 24 + 16))
        rot = im.rotate(-3, resample=Image.BICUBIC, expand=True)
        if s.grain and cast.has(s.who):                            # le grain de beauté (à l'endroit), après la rotation
            gx, gy = grain_xy(s.who, s.face)
            px_, py_ = (W_ - v.width) // 2 + (gx + 0.5) * 13 - W_ / 2, 24 + 16 + (gy + 0.5) * 13 - H_ / 2
            ang = math.radians(3)
            rx, ry = px_ * math.cos(ang) - py_ * math.sin(ang), px_ * math.sin(ang) + py_ * math.cos(ang)
            s.grain_pos = (20 + rot.width / 2 + rx, 20 + rot.height / 2 + ry)
        return autocollant(rot)


class Icone(Element):
    def __init__(s, cmd, nom):
        super().__init__(cmd)
        s.nom = nom

    def fabrique(s):
        return autocollant(objets.icone(s.nom).img(22), r=8)


class Chiffre(Element):
    def __init__(s, cmd, txt):
        super().__init__(cmd)
        s.txt = txt.strip().strip('"')
        m = re.search(r"(\d+(?:[.,]\d+)?)", s.txt)
        s.val = float(m.group(1).replace(",", ".")) if m else None
        s.dec = (len(m.group(1).split(",")[1]) if m and "," in m.group(1) else 0) if m else 0
        s._cache = {}

    def image(s, u):
        e = smooth(u / 0.9)
        if s.val is None or e >= 1:
            txt = s.txt
        else:
            v = s.val * e
            num = f"{v:.{s.dec}f}".replace(".", ",")
            txt = s.txt.replace(re.search(r"(\d+(?:[.,]\d+)?)", s.txt).group(1), num, 1)
        if txt not in s._cache:
            s._cache[txt] = autocollant(pxv.big_title([(txt, JAUNE)], size=210), r=5, ombre=False)
        return s._cache[txt]


class Compteur(Element):
    """Un nombre qui monte de a à b (en accéléré) avec une légende dessous : {compteur 0 -> 100 "SUBHAN ALLAH"}."""

    def __init__(s, cmd, a, b, label=None, duree=2.6):
        super().__init__(cmd)
        s.a, s.b, s.legende, s.duree = a, b, label, duree
        s._cache = {}

    def image(s, u):
        e = smooth(u / s.duree)
        v = int(round(s.a + (s.b - s.a) * e))
        if v not in s._cache:
            n = pxv.big_title([(str(v), JAUNE if e >= 1 else BLANC)], size=260)
            if s.legende:
                l_ = pxv.big_title([(x, BLANC) for x in coupe(s.legende, 14)], size=44)
                im = Image.new("RGBA", (max(n.width, l_.width), n.height + l_.height - 10), (0, 0, 0, 0))
                im.alpha_composite(n, ((im.width - n.width) // 2, 0))
                im.alpha_composite(l_, ((im.width - l_.width) // 2, n.height - 10))
            else:
                im = n
            s._cache[v] = autocollant(im, r=4, ombre=False)
        return s._cache[v]


class Chrono(Element):
    """Un chrono qui défile jusqu'à une durée (« 2:00 »), en accéléré, puis une légende (« ≈ 2 MINUTES »)."""

    def __init__(s, cmd, fin="2:00", label=None, duree=1.5):
        super().__init__(cmd)
        m_ = re.match(r"(\d+):(\d+)", fin)
        s.total = (int(m_.group(1)) * 60 + int(m_.group(2))) if m_ else 120
        s.legende, s.duree = label, duree
        s._cache = {}
        s._ic = autocollant(objets.icone("horloge").img(13), r=6)

    def image(s, u):
        e = smooth(u / s.duree)
        sec = int(round(s.total * e))
        fini = e >= 1
        key = (sec, fini)
        if key not in s._cache:
            t_ = pxv.big_title([(f"{sec // 60}:{sec % 60:02d}", JAUNE if fini else BLANC)], size=150)
            parts = [s._ic, t_]
            if fini and s.legende:
                parts.append(pxv.big_title([(s.legende, BLANC)], size=56))
            w_ = max(p_.width for p_ in parts)
            h_ = sum(p_.height for p_ in parts) + 10 * (len(parts) - 1)
            im = Image.new("RGBA", (w_, h_), (0, 0, 0, 0))
            yy = 0
            for p_ in parts:
                im.alpha_composite(p_, ((w_ - p_.width) // 2, yy))
                yy += p_.height + 10
            s._cache[key] = im
        return s._cache[key]


class Lettres(Element):
    """Lettres arabes qui apparaissent une par une (de droite à gauche), « +10 » chacune, puis le total."""
    plein = True

    def __init__(s, cmd, lettres, par=10, label="BONNES ACTIONS", temps=None):
        super().__init__(cmd)
        s.lettres, s.par, s.legende = lettres, par, label
        n = len(lettres)
        s.temps = temps if temps and len(temps) == n else [i * 0.7 for i in range(n)]   # quand chaque lettre arrive
        s.t_total = s.temps[-1] + (0.6 if temps and len(temps) == n else 0.8) if n else 0.8
        s.f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 300)
        s._cache = {}

    def _lettre(s, ch):
        if ch not in s._cache:
            bb = s.f.getbbox(ch)
            im = Image.new("RGBA", (bb[2] - bb[0] + 60, bb[3] - bb[1] + 60), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            d.text((30 - bb[0], 30 - bb[1]), ch, font=s.f, fill=(255, 255, 255, 255), stroke_width=10, stroke_fill=(22, 18, 30, 255))
            s._cache[ch] = im
        return s._cache[ch]

    def image(s, u):
        n = len(s.lettres)
        W_, H_ = 1000, 860
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        pas = W_ / (n + 1)
        for i, ch in enumerate(s.lettres):
            t_in = s.temps[i]
            if i and u < t_in:                                        # pas encore dite
                break
            a = smooth((u - t_in) / 0.3)
            l_ = s._lettre(ch)
            cx = W_ - pas * (i + 1)                                   # de droite à gauche
            im.alpha_composite(_fade(l_, a), (int(cx - l_.width / 2), int(330 - l_.height / 2 + (1 - a) * 30)))
            plus = s._cache.setdefault(("p", s.par), autocollant(pxv.big_title([(f"+{s.par}", JAUNE)], size=80), r=3, ombre=False))
            b = smooth((u - t_in - 0.2) / 0.3)
            im.alpha_composite(_fade(plus, b), (int(cx - plus.width / 2), int(40 - (1 - b) * 20)))
        if u >= s.t_total:
            tot = s._cache.setdefault(("t", n), autocollant(pxv.big_title([(f"= {n * s.par} {s.legende}", JAUNE)], size=72),
                                                            r=4, ombre=False))
            c = smooth((u - s.t_total) / 0.4)
            im.alpha_composite(_fade(tot, c), (int(W_ / 2 - tot.width / 2), int(620 + (1 - c) * 20)))
        return im


class Coran(Element):
    """{coran} : un Coran ouvert en gros plan (lignes stylisées, illisibles) ; une lumière suit la ligne de droite à
    gauche et, de chaque lettre lue, sort « +1 » (une bonne action) ; à partir du {chiffre ×10} qui suit, ce sont des
    « +10 » et un badge « ×10 » s'affiche. Aucun total inventé."""
    plein = True

    def __init__(s, cmd, pas=0.3):
        super().__init__(cmd)
        s.pas = pas
        s.t_x10 = None
        s._cache = {}
        rng = np.random.default_rng(29)
        s.lignes = []                                                # par ligne : liste de (x0, x1) des traits
        for li in range(16):
            x, traits = 0, []
            while x < 80:
                l_ = int(rng.integers(2, 7))
                traits.append((x, min(80, x + l_)))
                x += l_ + int(rng.integers(1, 3))
            s.lignes.append((traits, [(int(rng.integers(0, 80)), int(rng.choice([-3, 3]))) for _ in range(4)]))

    def livre(s):
        if "livre" not in s._cache:
            c = Px(200, 132, alpha=True)
            c.fill(c.mask_rrect(0, 4, 200, 132, 6), (22, 18, 30))
            c.fill(c.mask_rrect(1, 5, 199, 131, 5), (34, 104, 66))            # couverture verte
            c.fill(c.mask_rect(3, 7, 197, 9), (212, 170, 70))
            c.fill(c.mask_rect(3, 127, 197, 129), (212, 170, 70))
            for (x0, x1) in ((6, 98), (102, 194)):                            # deux pages crème
                c.fill(c.mask_rect(x0, 10, x1, 124), (22, 18, 30))
                c.vgrad(c.mask_rect(x0 + 1, 11, x1 - 1, 123), 11, 123, (250, 242, 218), (232, 220, 190), steps=4)
                c.fill(c.mask_rect(x0 + 4, 14, x1 - 4, 15), (200, 160, 70))     # cadre doré
                c.fill(c.mask_rect(x0 + 4, 119, x1 - 4, 120), (200, 160, 70))
                c.fill(c.mask_rect(x0 + 4, 14, x0 + 5, 120), (200, 160, 70))
                c.fill(c.mask_rect(x1 - 5, 14, x1 - 4, 120), (200, 160, 70))
            c.fill(c.mask_rect(97, 10, 103, 124), (176, 160, 128))            # le pli du milieu
            c.fill(c.mask_rect(99, 10, 101, 124), (140, 124, 98))
            for p_, x_droite in enumerate((186, 90)):                         # lignes de texte (de droite à gauche)
                for li in range(8):
                    traits, points = s.lignes[p_ * 8 + li]
                    yl = 24 + li * 12
                    for (a_, b_) in traits:
                        c.fill(c.mask_rect(x_droite - b_, yl, x_droite - a_, yl + 2), (44, 36, 30))
                    for (px_, dy) in points:
                        c.px(x_droite - px_, yl + 1 + dy, (44, 36, 30))
            s._cache["livre"] = c.img(5, rgba=True)
        return s._cache["livre"]

    def _plus(s, txt, col):
        k_ = ("p", txt)
        if k_ not in s._cache:
            s._cache[k_] = autocollant(pxv.big_title([(txt, col)], size=96), r=4, ombre=False)
        return s._cache[k_]

    def image(s, u):
        base = s.livre()
        W_, H_ = base.width + 40, base.height + 330
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        ox, oy = 20, 200
        im.alpha_composite(base, (ox, oy))
        d = ImageDraw.Draw(im)
        n = int(u / s.pas) + 1
        for i in range(n):                                            # lettre i : où est-elle sur la page ?
            li, col_ = divmod(i, 11)
            if li >= 8:
                break
            xl = ox + (186 - 4 - col_ * 7.3) * 5
            yl = oy + (24 + li * 12) * 5
            t_i = i * s.pas
            if i == n - 1:                                            # la lumière sur la lettre qu'on lit
                d.rounded_rectangle([xl - 34, yl - 26, xl + 34, yl + 38], 10, fill=(255, 214, 70, 105))
                d.rounded_rectangle([xl - 22, yl - 16, xl + 22, yl + 28], 8, fill=(255, 226, 110, 150))
            v = u - t_i
            if 0 <= v < 1.0:
                dix = s.t_x10 is not None and t_i >= s.t_x10 - 0.05
                p = s._plus("+10" if dix else "+1", JAUNE if dix else BLANC)
                e = smooth(v / 0.25) * (1 - smooth((v - 0.6) / 0.4))
                im.alpha_composite(_fade(p, e), (int(xl - p.width / 2), int(yl - 40 - p.height - 110 * v)))
        leg = s._cache.setdefault("leg", autocollant(pxv.big_title([("EN ARABE · EN PRONONÇANT", BLANC)], size=50), r=3, ombre=False))
        e_l = smooth((u - 0.6) / 0.4)                                  # la récompense : lire en arabe, en prononçant
        im.alpha_composite(_fade(leg, e_l), (int(W_ / 2 - leg.width / 2), int(oy + base.height + 14)))
        if s.t_x10 is not None and u >= s.t_x10:                      # le badge « ×10 »
            b = s._cache.setdefault("x10", autocollant(pxv.big_title([("×10", JAUNE)], size=120), r=4, ombre=False))
            e = smooth((u - s.t_x10) / 0.35)
            im.alpha_composite(_fade(b, e), (int(30), int(oy - b.height * 0.55 + (1 - e) * 20)))
        return im


class Defile(Element):
    """{defile} : un téléphone en gros plan, le fil défile très vite (des lettres et des lettres qu'on scrolle)."""
    plein = True

    def __init__(s, cmd, vitesse=1100):
        super().__init__(cmd)
        s.vitesse = vitesse
        rng = np.random.default_rng(41)
        s.posts = []
        for k_ in range(14):
            s.posts.append(dict(c=tuple(int(x) for x in rng.integers(80, 230, 3)),
                                l=[int(rng.integers(160, 330)) for _ in range(3)], img=bool(rng.integers(0, 2))))
        s._cache = {}

    def image(s, u):
        Wt, Ht = 440, 800
        if "cadre" not in s._cache:
            cadre = Image.new("RGBA", (Wt, Ht), (0, 0, 0, 0))
            d = ImageDraw.Draw(cadre)
            d.rounded_rectangle([0, 0, Wt - 1, Ht - 1], 54, fill=(22, 18, 30, 255))
            d.rounded_rectangle([10, 10, Wt - 11, Ht - 11], 46, fill=(48, 44, 58, 255))
            d.rounded_rectangle([Wt / 2 - 50, 22, Wt / 2 + 50, 38], 8, fill=(22, 18, 30, 255))
            s._cache["cadre"] = cadre
        im = s._cache["cadre"].copy()
        ecran = Image.new("RGBA", (Wt - 44, Ht - 90), (244, 242, 248, 255))
        d = ImageDraw.Draw(ecran)
        haut_post = 250
        dec = (u * s.vitesse) % (haut_post * len(s.posts))
        for k_, p in enumerate(s.posts * 2):
            y0 = k_ * haut_post - dec
            if y0 > ecran.height or y0 + haut_post < 0:
                continue
            d.ellipse([16, y0 + 16, 60, y0 + 60], fill=(*p["c"], 255))
            d.rectangle([72, y0 + 24, 72 + 130, y0 + 36], fill=(60, 56, 70, 255))
            for j, l_ in enumerate(p["l"]):                           # des lignes de texte
                d.rectangle([16, y0 + 76 + j * 22, 16 + l_, y0 + 88 + j * 22], fill=(150, 146, 160, 255))
            if p["img"]:
                d.rounded_rectangle([16, y0 + 150, ecran.width - 16, y0 + 236], 10, fill=(*p["c"], 255))
            d.line([(0, y0 + haut_post - 2), (ecran.width, y0 + haut_post - 2)], fill=(214, 210, 222, 255), width=2)
        m = Image.new("L", ecran.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, ecran.width - 1, ecran.height - 1], 36, fill=255)
        im.paste(ecran, (22, 56), m)
        pouce = (u * 2.2) % 1.0                                       # le pouce qui fait défiler
        yp = 56 + ecran.height * (0.85 - 0.5 * smooth(pouce))
        dd = ImageDraw.Draw(im)
        al = int(200 * (1 - smooth(max(0.0, (pouce - 0.8) / 0.2))))
        dd.ellipse([Wt / 2 + 40, yp - 44, Wt / 2 + 128, yp + 44], fill=(224, 172, 132, al), outline=(22, 18, 30, al), width=6)
        return autocollant(im, r=6)


class Distance(Element):
    """Le téléphone recule : la règle s'allonge, la distance monte, le visage se déforme de moins en moins."""
    plein = True

    def __init__(s, cmd, who, d0="30 cm", d1="1,5 m", duree=2.6):
        super().__init__(cmd)
        s.who, s.duree = who, duree
        s.v0, s.v1 = _metres(d0), _metres(d1)
        s.l0, s.l1 = d0, d1
        s._vis = {}
        s._tel = autocollant(objets.icone("telephone").img(13), r=6)

    def image(s, u):
        e = smooth(max(0.0, u - 0.6) / s.duree)
        W_, H_ = 1040, 760
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        val = s.v0 + (s.v1 - s.v0) * e                          # marche dans les deux sens (recule ou s'approche)
        lo, hi = min(s.v0, s.v1), max(s.v0, s.v1)
        pos = (math.log(val) - math.log(lo)) / max(1e-6, math.log(hi) - math.log(lo))   # 0 = le plus près
        force = round((1 - pos) * 0.42, 2)
        if force not in s._vis:
            s._vis[force] = autocollant(visage_img(s.who, "neutre", False, k=12, nez=force), r=6)
        v = s._vis[force]
        vx, vy = W_ - v.width, 10
        im.alpha_composite(v, (vx, vy))
        cy = vy + v.height // 2
        tw = s._tel.width
        x_pres, x_loin = vx - tw + 30, 0                       # tout près du visage → au bord gauche
        xt = int(x_pres + (x_loin - x_pres) * pos)
        im.alpha_composite(s._tel, (xt, cy - s._tel.height // 2))
        d = ImageDraw.Draw(im)
        xa, xb = xt + tw // 2, vx + v.width // 2 - 40           # du téléphone au visage
        yr = vy + v.height + 40
        for c, w in ((ENCRE, 16), (JAUNE, 9)):                 # règle avec ses deux butées
            d.line([(xa, yr), (xb, yr)], fill=(*c, 255), width=w)
            for x in (xa, xb):
                d.line([(x, yr - 26), (x, yr + 26)], fill=(*c, 255), width=w)
        n = max(2, int((xb - xa) / 70))
        for i in range(1, n):
            x = xa + (xb - xa) * i / n
            d.line([(x, yr - 12), (x, yr + 12)], fill=(*JAUNE, 255), width=5)
        lab = s.l1 if e >= 0.999 else (s.l0 if e <= 0.001 else _fmt_m(val))
        t = pxv.big_title([(lab, BLANC)], size=110)
        im.alpha_composite(t, (int(max(0, min(W_ - t.width, (xa + xb) / 2 - t.width / 2))), yr + 34))
        return im


def _metres(t):
    m = re.match(r"\s*(\d+(?:[.,]\d+)?)\s*(cm|m|km)?", t)
    if not m:
        return 0.3
    v = float(m.group(1).replace(",", "."))
    return v / 100 if (m.group(2) or "cm") == "cm" else (v * 1000 if m.group(2) == "km" else v)


def _fmt_m(v):
    return f"{int(round(v * 100))} cm" if v < 1 else f"{v:.1f} m".replace(".", ",")


# ---------------------------------------------------------------- l'écran du téléphone (encart de la démonstration photo)
def ecran_photo(who, force=0.0, k=9, face="content"):
    """Le téléphone vu de face : ce qu'il filme (le visage, plus ou moins déformé), avec un bouton de photo."""
    v = visage_img(who, face, False, k=k, nez=force)
    a, (nx, ny) = tete(who, face)
    sw, sh = v.width + 40, int((v.width + 40) * 1.3)
    W_, H_ = sw + 36, sh + 90
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 40, fill=(26, 26, 32, 255), outline=(*BLANC, 255), width=6)
    scr = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scr)
    for i in range(sh):
        c = int(150 + 60 * i / sh)
        sd.line([(0, i), (sw, i)], fill=(c - 40, c - 10, c + 20, 255))
    vx, vy = (sw - v.width) // 2, sh - v.height - 30
    scr.alpha_composite(v, (vx, vy))
    sd.rectangle([0, 0, sw, 44], fill=(0, 0, 0, 120))
    sd.ellipse([sw // 2 - 34, sh - 26 - 34, sw // 2 + 34, sh - 26 + 34], outline=(255, 255, 255, 230), width=7)
    for (xx, yy) in ((14, 60), (sw - 14, 60), (14, sh - 70), (sw - 14, sh - 70)):     # coins du viseur
        sx = 1 if xx < sw // 2 else -1
        sy = 1 if yy < sh // 2 else -1
        sd.line([(xx, yy), (xx + sx * 40, yy)], fill=(255, 255, 255, 200), width=5)
        sd.line([(xx, yy), (xx, yy + sy * 40)], fill=(255, 255, 255, 200), width=5)
    m = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, sw - 1, sh - 1], 26, fill=255)
    im.paste(scr, (18, 46), m)
    d.rounded_rectangle([W_ // 2 - 50, 18, W_ // 2 + 50, 28], 5, fill=(60, 60, 70, 255))
    im.info["nez"] = (18 + vx + int((nx + 0.5) * k), 46 + vy + int((ny + 0.5) * k))   # le nez, dans l'encart
    return im



# ---------------------------------------------------------------- 03/11/2026 : radiographie, orteil, arbre, balance
# Quatre démonstrations en image pour les Shorts islam « duo » (sens propre du hadith, montré concrètement) :
#   {radio PETIT}  {radio +1 "SUBHAN ALLAH"}  {radio tout "2 RAKATS DE DUHA"}     (Mouslim 720 · 1007)
#   {orteil}                                                                     (le petit orteil contre le pied du lit)
#   {arbre "TES PÉCHÉS"}  {feuilles}                                              (Boukhari 5660)
#   {balance "LE MONDE ENTIER" "2 RAKATS"}  {balance + manette}  {balance pese}   (Mouslim 725)
def _erode(m, n=1):
    e = m.copy()
    for _ in range(n):
        e = e & np.roll(e, 1, 0) & np.roll(e, -1, 0) & np.roll(e, 1, 1) & np.roll(e, -1, 1)
    return e


def _os(c, x0, y0, x1, y1, ep):
    """Masque d'un segment épais aux bouts arrondis (un os, un fléau de balance…) dans un dessin Px."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L * ep / 2, dx / L * ep / 2
    m = c.mask_poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)])
    r = ep / 2 + 0.6
    return m | c.mask_ell(x0, y0, r, r) | c.mask_ell(x1, y1, r, r)


def _titre(txt, col=BLANC, size=60, r=3):
    return autocollant(pxv.big_title([(txt, col)], size=size), r=r, ombre=False)


def _titres(txt, col=BLANC, size=60):
    """« 2 RAKATS // SUNNA AVANT LE FAJR » : 1re ligne en grand (couleur), les suivantes plus petites, en blanc."""
    parts = [x.strip() for x in txt.split("//") if x.strip()]
    ims = [_titre(parts[0], col, size)] + [_titre(x, BLANC, int(size * 0.62)) for x in parts[1:]]
    if len(ims) == 1:
        return ims[0]
    W_ = max(i.width for i in ims)
    out = Image.new("RGBA", (W_, sum(i.height for i in ims) - 8 * (len(ims) - 1)), (0, 0, 0, 0))
    y = 0
    for i in ims:
        out.alpha_composite(i, (int(W_ / 2 - i.width / 2), y))
        y += i.height - 8
    return out


def _copie(c):
    d = Px(c.w, c.h, alpha=True)
    d.a, d.al = c.a.copy(), c.al.copy()
    return d


class Radio(Element):
    """{radio PETIT} : la radiographie du perso — squelette pixel (sa casquette passe aux rayons X), ses articulations
    en rouge qui battent (une aumône due pour chacune, chaque matin : Mouslim 720 · 1007), compteur « 0 / 360 ».
    {radio +1 "SUBHAN ALLAH"} : une articulation passe au vert, « +1 » (une aumône par dhikr), compteur 1 / 360 ;
    {radio tout "2 RAKATS DE DUHA"} : une ligne verte descend et les passe toutes au vert, « 360 / 360 », « ÇA SUFFIT ! »."""
    plein = True
    TOTAL = 360
    K = 5
    PW_, PH_ = 100, 172
    JOINTS = [(50, 34), (36, 43), (64, 43), (31, 70), (69, 70), (29, 94), (71, 94),
              (26, 101), (29, 103), (32, 101), (68, 101), (71, 103), (74, 101),
              (50, 42), (50, 50), (50, 58), (50, 66), (50, 74), (50, 82), (50, 90),
              (44, 104), (56, 104), (42, 135), (58, 135), (42, 162), (58, 162),
              (37, 167), (40, 168), (60, 168), (63, 167), (45, 30), (55, 30)]
    ORDRE = [5, 6, 22, 23, 1, 2, 3, 4]                     # les articulations qui passent au vert une par une (+1)

    def __init__(s, cmd, who="PETIT"):
        super().__init__(cmd)
        s.who = who
        s.plus, s.t_tout, s.lab_tout = [], None, None
        s.t_art, s.t_reste = None, None          # {radio articulations} : vague sur les articulations ; {radio reste}
        s.note_tout = None                       # {radio tout "2 RAKATS DE DOUHA" "SUNNA // PAS OBLIGATOIRE"} : la note
        s._cache = {}

    def sons_el(s):
        out = [(u, "sa_ting", 0.035, None) for (u, _) in s.plus]
        if s.t_art is not None:
            out.append((s.t_art, "tr_whoosh_doux", 0.04, None))
        if s.t_tout is not None:
            out.append((s.t_tout, "sa_scintillement", 0.05, None))
        return out

    def _etiquette(s, u):
        """L'étiquette du haut : la dernière annonce arrivée (articulations, dhikr, reste, Duha)."""
        evts = []
        if s.t_art is not None:
            evts.append((s.t_art, "360 ARTICULATIONS", BLANC))
        evts += [(t_, "« " + lab + " » = +1", BLANC) for (t_, lab) in s.plus if lab]
        if s.t_reste is not None:
            n_ = sum(1 for (t_, _) in s.plus if t_ <= s.t_reste)
            evts.append((s.t_reste, f"ENCORE {s.TOTAL - n_} !", (255, 120, 110)))
        if s.t_tout is not None and s.lab_tout:
            evts.append((s.t_tout, s.lab_tout, JAUNE))
        evts = [e for e in evts if u >= e[0]]
        return max(evts, key=lambda e: e[0]) if evts else None

    def _panneau(s):
        if "p" in s._cache:
            return s._cache["p"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        fond = c.mask_rrect(0, 0, W, H, 6)
        dedans = c.mask_rrect(2, 2, W - 2, H - 2, 5)
        c.fill(fond, (120, 196, 240))                                         # cadre lumineux
        c.fill(fond & ~c.mask_rrect(1, 1, W - 1, H - 1, 5), (8, 14, 30))
        c.vgrad(dedans, 2, H - 2, (24, 44, 78), (12, 22, 46), steps=5)
        for x in range(10, W - 4, 10):                                        # quadrillage discret
            c.fill(c.mask_rect(x, 3, x + 1, H - 3) & dedans, (28, 50, 84))
        for y in range(10, H - 4, 10):
            c.fill(c.mask_rect(3, y, W - 3, y + 1) & dedans, (28, 50, 84))
        chair = c.mask_ell(50, 22, 12, 13) | c.mask_rect(45, 30, 56, 40) | c.mask_rrect(33, 36, 68, 108, 8)
        for (a, b, ep) in (((36, 43), (31, 70), 9), ((31, 70), (29, 96), 8), ((64, 43), (69, 70), 9),
                           ((69, 70), (71, 96), 8), ((44, 104), (42, 135), 12), ((42, 135), (42, 164), 10),
                           ((56, 104), (58, 135), 12), ((58, 135), (58, 164), 10)):
            chair |= _os(c, *a, *b, ep)
        chair |= c.mask_ell(29, 101, 5, 6) | c.mask_ell(71, 101, 5, 6) | c.mask_ell(39, 166, 7, 4) | c.mask_ell(61, 166, 7, 4)
        chair &= dedans
        c.fill(chair, (34, 72, 122))                                          # la chair : un fantôme bleuté
        c.dither(chair & ~_erode(chair, 2), (56, 104, 160), 0.6)
        os_ = c.mask_ell(50, 21, 9, 10) | c.mask_rect(44, 27, 57, 32)         # crâne + mâchoire
        for y in range(34, 96, 4):
            os_ |= c.mask_rect(48, y, 53, y + 3)                              # vertèbres
        os_ |= _os(c, 49, 39, 36, 43, 2.4) | _os(c, 51, 39, 64, 43, 2.4)       # clavicules
        for i in range(5):                                                   # côtes
            y = 45 + i * 5
            ring = c.mask_ell(50, y + 7, 14 - i * 0.6, 8) & ~c.mask_ell(50, y + 7, 12 - i * 0.6, 6.2)
            os_ |= ring & c.mask_rect(0, 0, W, y + 7)
        os_ |= c.mask_rect(49, 44, 52, 68)                                    # sternum
        os_ |= (c.mask_ell(50, 101, 13, 8) & ~c.mask_ell(50, 104, 6, 5)) & c.mask_rect(0, 95, W, 110)   # bassin
        for (a, b, ep) in (((36, 43), (31, 70), 3.2), ((64, 43), (69, 70), 3.2),
                           ((31, 70), (28, 94), 1.6), ((32, 71), (30, 94), 1.6),
                           ((69, 70), (72, 94), 1.6), ((68, 71), (70, 94), 1.6),
                           ((44, 104), (42, 134), 3.8), ((56, 104), (58, 134), 3.8),
                           ((42, 136), (42, 161), 2.4), ((44, 137), (44, 160), 1.4),
                           ((58, 136), (58, 161), 2.4), ((56, 137), (56, 160), 1.4)):
            os_ |= _os(c, *a, *b, ep)
        for (x0, d) in ((29, -1), (71, 1)):                                   # mains
            for j in range(4):
                os_ |= _os(c, x0 + d * (j - 1.5) * 1.6, 97, x0 + d * (j - 1.5) * 2.4, 104 + (j % 2), 1.2)
        for (x0, d) in ((42, -1), (58, 1)):                                   # pieds
            os_ |= _os(c, x0, 163, x0 + d * 6, 167, 2.6) | _os(c, x0, 164, x0 + d * 2, 168, 2.0)
        os_ &= dedans
        c.shape(os_, (226, 238, 250), shade=(150, 182, 214), light=(255, 255, 255), band=1, olcol=(8, 14, 30))
        c.fill(c.mask_ell(46, 22, 2.3, 2.6) | c.mask_ell(54, 22, 2.3, 2.6) | c.mask_rect(49, 26, 51, 28), (8, 14, 30))
        for x in range(45, 57, 2):
            c.px(x, 29, (110, 132, 166))                                      # dents
        cas = (c.mask_ell(50, 16, 10, 7) & c.mask_rect(0, 0, W, 17)) | c.mask_rect(52, 15, 67, 18)
        c.shape(cas, (40, 50, 90), shade=(28, 34, 64), light=(80, 96, 156), band=1, olcol=(8, 14, 30))
        s._cache["p"] = c.img(s.K, rgba=True)
        return s._cache["p"]

    def _n(s, u):
        n = sum(1 for (t_, _) in s.plus if u >= t_)
        if s.t_tout is not None and u >= s.t_tout:
            return int(round(n + (s.TOTAL - n) * smooth((u - s.t_tout) / 0.9)))
        return n

    def image(s, u):
        K = s.K
        W_, H_ = 1010, 960
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        pan = s._panneau()
        px0, py0 = 0, 100
        im.alpha_composite(pan, (px0, py0))
        lay = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        cyc = (u % 2.8) / 2.8                                                 # le balayage des rayons X (en boucle)
        yb = py0 + 3 * K + (pan.height - 6 * K) * cyc
        d.rectangle([px0 + 2 * K, max(py0 + 2 * K, yb - 3 * K), px0 + pan.width - 2 * K, min(py0 + pan.height - 2 * K, yb + 3 * K)],
                    fill=(150, 226, 255, 34))
        verts = {s.ORDRE[i % len(s.ORDRE)] for i in range(sum(1 for (t_, _) in s.plus if u >= t_))}
        sweep = None
        if s.t_tout is not None and u >= s.t_tout:
            sweep = py0 + pan.height * smooth((u - s.t_tout) / 0.9)
            d.rectangle([px0 + 2 * K, max(py0 + 2 * K, sweep - 2 * K), px0 + pan.width - 2 * K,
                         min(py0 + pan.height - 2 * K, sweep + 2 * K)], fill=(120, 255, 150, 90 if u < s.t_tout + 0.9 else 0))
        puls = 0.5 + 0.5 * math.sin(2 * math.pi * u / 1.1)
        r = int(K * 1.4)
        for j, (jx, jy) in enumerate(s.JOINTS):
            X, Y = px0 + jx * K + K // 2, py0 + jy * K + K // 2
            vert = j in verts or (sweep is not None and Y <= sweep)
            if vert:
                col = (90, 230, 120)
                rr = r + K
                d.rectangle([X - rr, Y - rr, X + rr, Y + rr], fill=(120, 255, 150, 70))
            else:
                col = (int(215 + 40 * puls), int(48 + 40 * puls), int(48 + 30 * puls))
                rr = int(r + K * (0.5 + 0.8 * puls))
                d.rectangle([X - rr, Y - rr, X + rr, Y + rr], fill=(255, 70, 70, int(55 + 50 * puls)))
            r2 = r
            if s.t_art is not None:                                           # la vague : chacune grossit à son tour
                v_ = u - (s.t_art + 0.9 * jy / s.PH_)
                if 0 <= v_ < 0.45:
                    k_ = math.sin(math.pi * v_ / 0.45)
                    r2 = int(r + K * 1.6 * k_)
                    d.rectangle([X - r2 - K, Y - r2 - K, X + r2 + K, Y + r2 + K], fill=(255, 240, 160, int(150 * k_)))
            d.rectangle([X - r2 - 3, Y - r2 - 3, X + r2 + 3, Y + r2 + 3], fill=(8, 14, 30, 255))
            d.rectangle([X - r2, Y - r2, X + r2, Y + r2], fill=(*col, 255))
            d.rectangle([X - r2 + 2, Y - r2 + 2, X - r2 + 4, Y - r2 + 4], fill=(255, 255, 255, 210))
        im.alpha_composite(lay)
        for i, (t_, lab) in enumerate(s.plus):                               # « +1 » qui monte de l'articulation
            v = u - t_
            if 0 <= v < 1.1:
                jx, jy = s.JOINTS[s.ORDRE[i % len(s.ORDRE)]]
                X, Y = px0 + jx * K, py0 + jy * K
                p = s._cache.setdefault("+1", _titre("+1", JAUNE, 84))
                e = smooth(v / 0.25) * (1 - smooth((v - 0.7) / 0.4))
                im.alpha_composite(_fade(p, e), (int(X - p.width / 2), int(Y - 30 - p.height - 90 * v)))
        eti = s._etiquette(u)                                                # l'étiquette en haut
        if eti is not None:
            t_, txt_, col_ = eti
            lab_img = s._cache.setdefault(("l", txt_, col_), _titre(txt_, col_, 64 if col_ == JAUNE else 58))
            e = smooth((u - t_) / 0.3)
            im.alpha_composite(_fade(lab_img, e), (int(W_ / 2 - lab_img.width / 2), int(48 - lab_img.height / 2)))
        n = s._n(u)
        fini = s.t_tout is not None and u >= s.t_tout + 0.9
        col_n = JAUNE if fini else ((255, 120, 110) if n == 0 else BLANC)
        nb = s._cache.setdefault(("n", n, col_n), _titre(str(n), col_n, 190 if n < 100 else 150, r=4))
        sur = s._cache.setdefault("sur", _titre("/ 360", BLANC, 92))
        cap = s._cache.setdefault(("cap", fini), _titre("ÇA SUFFIT !" if fini else "AUMÔNES", JAUNE if fini else BLANC, 60))
        monte = smooth((u - s.t_tout - 0.6) / 0.4) if s.t_tout is not None else 0.0   # la colonne remonte (coche / note)
        cx, yy = 762, 330 - 60 * monte
        for part in (nb, sur, cap):
            im.alpha_composite(part, (int(cx - part.width / 2), int(yy)))
            yy += part.height - 6
        if fini and s.note_tout:                                              # la note (sunna…) à la place de la coche
            no = s._cache.setdefault(("note", s.note_tout), _titres(s.note_tout, BLANC, 50))
            e2 = smooth((u - s.t_tout - 0.9) / 0.3)
            im.alpha_composite(_fade(no, e2), (int(max(510, min(W_ - no.width, cx - no.width / 2))), int(yy + 14)))
        elif fini:
            st = s._cache.setdefault("ok", autocollant(objets.icone("check").img(7), r=5))
            e = smooth((u - s.t_tout - 0.9) / 0.3)
            im.alpha_composite(_fade(st, e), (int(cx - st.width / 2), int(yy + 6)))
        return im


class Orteil(Element):
    """{orteil} : gros plan sur un pied en chaussette qui se cogne contre le pied du lit (le petit orteil) : traits de
    vitesse, étoile du choc, orteil rouge qui bat, « AÏE ! ». Aucune secousse ni flash (mouvements doux)."""
    plein = True
    negatif = True                                                       # le pied s'élance AVANT le mot (choc pile sur « Aïe »)
    K = 6
    PW_, PH_ = 170, 120
    T_CHOC = 0.0
    ELAN = 0.42
    X_CHOC = 117                                                         # bout du pied au choc (le pied du lit : x 118)
    SOL = 106

    def __init__(s, cmd):
        super().__init__(cmd)
        s._cache = {}

    def sons_el(s):
        return [(s.T_CHOC, "imp_tambour", 0.07, None)]

    def _decor(s):
        if "d" in s._cache:
            return s._cache["d"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        mur = tout_ & c.mask_rect(0, 0, W, 80)
        c.vgrad(mur, 0, 80, (206, 214, 230), (178, 188, 208), steps=5)
        for x in range(6, W, 12):
            c.dither(mur & c.mask_rect(x, 0, x + 3, 80), (192, 200, 220), 0.5)      # papier peint à rayures
        c.fill(tout_ & c.mask_rect(0, 80, W, 86), (238, 238, 242))                  # plinthe
        c.fill(tout_ & c.mask_rect(0, 85, W, 86), (170, 170, 184))
        sol = tout_ & c.mask_rect(0, 86, W, H)
        c.vgrad(sol, 86, H, (176, 122, 76), (150, 100, 60), steps=4)
        for y in (92, 100, 110):
            c.fill(sol & c.mask_rect(0, y, W, y + 1), (124, 82, 50))
        for (x, y0, y1) in ((30, 86, 92), (88, 92, 100), (140, 86, 92), (52, 100, 110), (126, 100, 110), (20, 110, 120),
                            (96, 110, 120), (150, 110, 120)):
            c.fill(sol & c.mask_rect(x, y0, x + 1, y1), (124, 82, 50))
        couv = tout_ & c.mask_rect(108, 30, W, 60)                                   # le lit : couverture, cadre, pied
        c.fill(couv, (70, 112, 196))
        c.fill(tout_ & c.mask_rect(108, 30, W, 33), (112, 152, 228))
        c.dither(tout_ & c.mask_rect(108, 48, W, 60), (52, 88, 160), 0.5)
        c.fill(tout_ & c.mask_rect(108, 30, 109, 60), (40, 66, 130))
        c.shape(tout_ & c.mask_rect(106, 58, W, 67), (122, 78, 48), shade=(92, 58, 36), light=(152, 102, 64), band=1,
                olcol=(40, 26, 20))
        pied_lit = c.mask_rect(118, 66, 130, s.SOL)
        c.shape(pied_lit, (112, 72, 44), shade=(84, 54, 34), light=(146, 98, 60), olcol=(40, 26, 20))
        c.fill(c.mask_ell(124, s.SOL + 1, 10, 1.6) & ~pied_lit & sol, (122, 80, 50))  # ombre au sol
        s._cache["d"] = c
        return c

    def _pied(s, c, X, dy=0):
        Y = s.SOL + dy
        jean = c.mask_poly([(X - 70, -2), (X - 40, -2), (X - 34, Y - 18), (X - 57, Y - 18)])
        c.shape(jean, (62, 96, 166), shade=(44, 70, 128), light=(96, 132, 200), band=1, olcol=(24, 22, 40))
        c.fill(c.mask_rect(X - 58, Y - 22, X - 33, Y - 18) & jean, (48, 78, 140))       # ourlet
        pied = (c.mask_poly([(X - 57, Y), (X - 59, Y - 9), (X - 56, Y - 19), (X - 35, Y - 19), (X - 22, Y - 10),
                             (X - 8, Y - 8), (X - 2, Y - 6), (X, Y - 3), (X - 1, Y)])
                | c.mask_ell(X - 53, Y - 6, 6, 6))
        c.shape(pied, (240, 240, 246), shade=(196, 198, 214), light=(255, 255, 255), band=1, olcol=(40, 36, 52))
        c.fill(c.mask_rect(X - 58, Y - 1, X, Y) & pied, (176, 178, 196))              # semelle
        for x in (X - 10, X - 6):
            c.px(x, Y - 5, (186, 188, 206))                                             # les orteils
        return (X - 3, Y - 4)                                                           # le petit orteil

    def _etoile(s):
        if "e" not in s._cache:
            c = Px(32, 32, alpha=True)
            pts = []
            for i in range(16):
                ang = math.pi * 2 * i / 16 - math.pi / 2
                rr = 15 if i % 2 == 0 else 6
                pts.append((16 + rr * math.cos(ang), 16 + rr * math.sin(ang)))
            m = c.mask_poly(pts)
            c.fill(m, (255, 216, 64))
            c.fill(m & ~_erode(m, 1), (234, 128, 34))
            c.fill(c.mask_ell(16, 16, 5, 5), (255, 248, 196))
            s._cache["e"] = c.img(s.K, rgba=True)
        return s._cache["e"]

    def image(s, u):
        K, T = s.K, s.T_CHOC
        if u < T:
            e = max(0.0, (u - (T - s.ELAN)) / s.ELAN) ** 2                    # il accélère (il ne voit pas le lit)
            X, dy = s.X_CHOC - 66 * (1 - e), 0
        else:
            v = u - T
            X = s.X_CHOC - 7 * smooth(v / 0.2)
            dy = -4 * smooth(v / 0.2)                                         # il lève le pied
        c = _copie(s._decor())
        toe = s._pied(c, int(round(X)), int(round(dy)))
        im = c.img(K, rgba=True)
        d = ImageDraw.Draw(im)
        if u < T:                                                             # traits de vitesse derrière le talon
            a = int(200 * smooth((u - (T - s.ELAN)) / 0.15))
            for j, yy in enumerate((s.SOL - 15, s.SOL - 9, s.SOL - 3)):
                x1 = (X - 63) * K
                d.rectangle([x1 - (90 + 30 * j), yy * K, x1, yy * K + K - 1], fill=(255, 255, 255, a))
        else:
            v = u - T
            puls = 0.5 + 0.5 * math.sin(2 * math.pi * v / 0.55)
            tx, ty = toe[0] * K, toe[1] * K
            rr = int(K * (3.2 + 1.2 * puls))
            d.ellipse([tx - rr - 4, ty - rr - 4, tx + rr + 4, ty + rr + 4], fill=(120, 20, 30, int(90 + 60 * puls)))
            d.ellipse([tx - rr, ty - rr, tx + rr, ty + rr], fill=(240, 60, 60, int(170 + 70 * puls)))
            e_ = smooth((v - 0.15) / 0.2)
            for k_, (dx_, dy_) in enumerate(((-0.9, -2.2), (0.6, -2.5), (1.9, -1.7))):   # traits de douleur (vers le haut)
                ox, oy = tx + dx_ * K * 3.2, ty + dy_ * K * 3.2
                ln = K * (2.2 + 0.8 * puls)
                bout = (ox + ln * dx_ / 2.4, oy + ln * dy_ / 2.4)
                d.line([(ox, oy), bout], fill=(60, 10, 20, int(255 * e_)), width=K + 6)
                d.line([(ox, oy), bout], fill=(255, 70, 70, int(255 * e_)), width=K)
            st = s._etoile()
            es = smooth(v / 0.12) * (1 - smooth((v - 0.7) / 0.4))
            if es > 0.01:
                sz = max(4, int(st.width * (0.6 + 0.4 * smooth(v / 0.12))))
                st2 = _fade(st.resize((sz, sz), Image.NEAREST), es)
                im.alpha_composite(st2, (int((s.X_CHOC + 1) * K - sz / 2), int((s.SOL - 6) * K - sz / 2)))
            aie = s._cache.setdefault("aie", _titre("AÏE !", (255, 92, 80), 170, r=5))
            a = smooth((v - 0.04) / 0.2)
            k2 = 0.86 + 0.14 * smooth(v / 0.25)
            aie2 = aie.resize((int(aie.width * k2), int(aie.height * k2)), Image.LANCZOS)
            im.alpha_composite(_fade(aie2, a), (int(300 - aie2.width / 2), int(150 - aie2.height / 2)))
        return im


class Arbre(Element):
    """{arbre "TES PÉCHÉS"} : un arbre dont des feuilles sombres sont des péchés (certaines marquées « PÉCHÉ ») ;
    {feuilles} : un coup de vent doux, elles tombent une à une et s'effacent au sol (Boukhari 5660 : « comme l'arbre
    perd ses feuilles ») ; l'arbre reste vert et brille."""
    plein = True
    K = 5
    PW_, PH_ = 150, 176
    N = 14
    DT, CHUTE = 0.15, 1.5
    COURONNE = [(75, 62, 42, 30), (46, 76, 23, 18), (104, 74, 23, 18), (58, 44, 23, 18), (92, 44, 23, 18), (75, 33, 20, 15)]

    def __init__(s, cmd, titre="TES PÉCHÉS"):
        super().__init__(cmd)
        s.titre, s.t_chute = titre, None
        s._cache = {}
        c = Px(s.PW_, s.PH_, alpha=True)
        cour = s._couronne(c)
        rng = np.random.default_rng(11)
        pts = []
        essais = 0
        dedans = _erode(cour, 4)
        while len(pts) < s.N and essais < 4000:
            essais += 1
            x, y = int(rng.integers(30, 121)), int(rng.integers(26, 96))
            if not dedans[y, x] or any((x - a) ** 2 + (y - b) ** 2 < 13 ** 2 for (a, b) in pts):
                continue
            pts.append((x, y))
        marq = set(sorted(range(len(pts)), key=lambda i: pts[i][1])[1::4][:4])      # 4 étiquettes, bien réparties
        ordre = list(rng.permutation(len(pts)))
        s.feuilles = [dict(x=x, y=y, ph=float(rng.uniform(0, 6.28)), marq=i in marq, rang=ordre.index(i))
                      for i, (x, y) in enumerate(pts)]

    def _couronne(s, c):
        m = np.zeros((c.h, c.w), bool)
        for (cx, cy, rx, ry) in s.COURONNE:
            m |= c.mask_ell(cx, cy, rx, ry)
        return m

    def sons_el(s):
        return [(s.t_chute, "tr_whoosh_vent", 0.05, None)] if s.t_chute is not None else []

    def fin_chute(s):
        return None if s.t_chute is None else s.t_chute + (s.N - 1) * s.DT + s.CHUTE

    def _arbre(s):
        if "a" in s._cache:
            return s._cache["a"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        c.shape(c.mask_ell(75, 168, 58, 7), (92, 156, 72), shade=(66, 122, 56), light=(130, 190, 96), band=1,
                olcol=(34, 60, 34))                                                   # l'herbe
        tronc = c.mask_poly([(66, 168), (84, 168), (81, 140), (82, 110), (69, 110), (70, 140)])
        for (a, b, ep) in (((73, 116), (52, 84), 6), ((78, 112), (100, 84), 6), ((75, 112), (76, 72), 6)):
            tronc |= _os(c, *a, *b, ep)
        tronc |= c.mask_ell(65, 167, 5, 2) | c.mask_ell(85, 167, 5, 2)               # racines
        c.shape(tronc, (122, 80, 48), shade=(88, 56, 34), light=(156, 106, 64), olcol=(44, 28, 20))
        for (x, y0, y1) in ((72, 122, 160), (77, 128, 164), (74, 144, 166)):
            c.fill(c.mask_rect(x, y0, x + 1, y1) & tronc, (96, 62, 38))               # écorce
        cour = s._couronne(c)
        c.fill(cour, (70, 150, 70))
        c.edge(cour, (46, 110, 52), "bottom", 4)
        c.edge(cour, (46, 110, 52), "right", 3)
        c.edge(cour, (124, 196, 98), "top", 2)
        c.dither(cour & _erode(cour, 3), (96, 172, 84), 0.35)
        rng = np.random.default_rng(5)
        for _ in range(70):                                                           # petites feuilles claires
            x, y = int(rng.integers(30, 121)), int(rng.integers(10, 100))
            if cour[y, x]:
                c.fill(c.mask_rect(x, y, x + 2, y + 1) & cour, (128, 200, 104))
        c.outline(cour, (30, 60, 36))
        s._cache["a"] = c.img(s.K, rgba=True)
        return s._cache["a"]

    def _feuille(s):
        if "f" not in s._cache:
            c = Px(15, 10, alpha=True)
            m = c.mask_poly([(2, 5), (6, 2), (11, 2), (14, 5), (11, 8), (6, 8)])     # une vraie feuille, pointue
            c.fill(m, (98, 72, 64))                                                   # feuille morte, sombre
            c.edge(m, (70, 50, 46), "bottom", 1)
            c.fill(c.mask_rect(4, 5, 13, 6) & m, (138, 108, 92))                      # la nervure
            for x in (7, 10):
                c.px(x, 4, (138, 108, 92))
            c.outline(m, (32, 22, 24))
            c.fill(c.mask_rect(0, 5, 2, 6), (64, 44, 34))                             # la queue
            s._cache["f"] = c.img(s.K, rgba=True)
        return s._cache["f"]

    def image(s, u):
        K = s.K
        base = s._arbre()
        haut, MX = 80, 120                                                           # marges : les étiquettes tiennent
        W_, H_ = base.width + 2 * MX, base.height + haut
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        tit = s._cache.setdefault("t", _titre(s.titre, BLANC, 74))
        im.alpha_composite(tit, (int(W_ / 2 - tit.width / 2), int(haut / 2 - tit.height / 2)))
        im.alpha_composite(base, (MX, haut))
        f = s._feuille()
        lab = s._cache.setdefault("lab", autocollant(petit_texte("PÉCHÉ", (255, 236, 236), (96, 20, 34), size=9, k=4), r=3,
                                                     ombre=False))
        for fe in s.feuilles:
            t0 = None if s.t_chute is None else s.t_chute + fe["rang"] * s.DT
            if t0 is None or u < t0:
                X = MX + fe["x"] * K + 3 * math.sin(2 * math.pi * u / 1.7 + fe["ph"])
                Y, a = fe["y"] * K + haut, 1.0
            else:
                v = (u - t0) / s.CHUTE
                if v >= 1:
                    continue
                e = v ** 1.4
                Y = (fe["y"] + (166 - fe["y"]) * e) * K + haut
                X = MX + fe["x"] * K + 7 * K * math.sin(2 * math.pi * v * 1.3 + fe["ph"]) * min(1.0, v * 3)
                a = 1 - smooth((v - 0.72) / 0.28)
            im.alpha_composite(_fade(f, a), (int(X - f.width / 2), int(Y - f.height / 2)))
            if fe["marq"]:                                                            # l'étiquette, côté extérieur
                xl = X + f.width / 2 - 6 if fe["x"] >= 75 else X - f.width / 2 - lab.width + 6
                im.alpha_composite(_fade(lab, a), (int(max(0, min(W_ - lab.width, xl))), int(Y - lab.height / 2)))
        fin = s.fin_chute()
        if fin is not None and fin - 0.3 <= u < fin + 1.8:                            # l'arbre propre brille
            rng = np.random.default_rng(int(u * 6))
            d = ImageDraw.Draw(im)
            al = int(230 * smooth((u - fin + 0.3) / 0.3) * (1 - smooth((u - fin - 1.2) / 0.6)))
            for _ in range(7):
                x, y = MX + int(rng.integers(40, 112)) * K, int(rng.integers(24, 92)) * K + haut
                d.rectangle([x - K, y - 3 * K, x + K, y + 3 * K], fill=(255, 255, 230, al))
                d.rectangle([x - 3 * K, y - K, x + 3 * K, y + K], fill=(255, 255, 230, al))
        return im


class Balance(Element):
    """{balance "LE MONDE ENTIER" "2 RAKATS"} : une grande balance dorée. À gauche, le monde se remplit (la planète,
    voitures, argent, maisons, téléphones, diamants…) et l'emporte ; à droite, un tapis de prière qui brille.
    {balance + manette} : un objet de plus tombe sur le monde ; {balance pese} : la balance penche lentement du côté
    des 2 rakats (Mouslim 725 : « meilleures que ce bas monde et ce qu'il contient »), étincelles, coche."""
    plein = True
    K = 6
    PW_, PH_ = 170, 142
    PIV = (85, 26)
    BRAS = 62
    OBJETS = ["voiture", "sac_argent", "maison", "telephone", "diamant", "couronne", "pieces"]
    PILE = [(-64, -12), (64, -12), (-38, -86), (38, -86), (0, -132), (-70, -80), (70, -80), (0, -190), (-40, -170)]

    def __init__(s, cmd, gauche="LE MONDE ENTIER", droite="2 RAKATS", deja=False, en_plus=()):
        super().__init__(cmd)
        s.gauche, s.droite = gauche, droite
        s.deja = deja                       # « deja » : le monde est déjà entassé (on revient à la balance)
        s.ajouts = [(-1.0, nom) for nom in en_plus]
        s.t_pese = None
        s._cache = {}

    def sons_el(s):
        out = ([] if s.deja else [(0.3, "sa_ting", 0.03, None)]) + [(t_ + 0.25, "sa_ting", 0.035, None)
                                                                   for (t_, _) in s.ajouts if t_ >= 0]
        if s.t_pese is not None:
            out += [(s.t_pese, "tr_whoosh_doux", 0.05, None), (s.t_pese + 1.0, "sa_scintillement", 0.05, None)]
        return out

    def _arrivees(s):
        d0 = -5.0 if s.deja else 0.3
        return [(d0 + i * 0.22, nom) for i, nom in enumerate(s.OBJETS)] + list(s.ajouts)

    def _angle(s, u):
        a = -3.0 - sum(1.6 * smooth((u - t_) / 0.4) for (t_, _) in s._arrivees())
        if s.t_pese is not None and u >= s.t_pese:
            a = a + (16.0 - a) * smooth((u - s.t_pese) / 1.3)
        return a

    def _icone(s, nom, k):
        key = ("i", nom, k)
        if key not in s._cache:
            s._cache[key] = autocollant(objets.icone(nom).img(k), r=4)
        return s._cache[key]

    def image(s, u):
        K = s.K
        W, H = s.PW_, s.PH_
        a = math.radians(s._angle(u))
        c = Px(W, H, alpha=True)
        gold, gsh, gli, ol = (226, 182, 72), (172, 126, 42), (255, 230, 140), (60, 38, 18)
        c.shape(c.mask_poly([(58, 141), (112, 141), (104, 131), (66, 131)]), gold, shade=gsh, light=gli, band=1, olcol=ol)
        c.shape(c.mask_rect(82, 30, 89, 132), gold, shade=gsh, light=gli, band=1, olcol=ol)
        px_, py_ = s.PIV
        ca, sa = math.cos(a), math.sin(a)
        g = (px_ - s.BRAS * ca, py_ - s.BRAS * sa)
        dr = (px_ + s.BRAS * ca, py_ + s.BRAS * sa)
        c.shape(_os(c, g[0], g[1], dr[0], dr[1], 3.6), gold, shade=gsh, light=gli, band=1, olcol=ol)
        c.shape(c.mask_ell(px_, py_, 5, 5), gli, shade=gold, band=1, olcol=ol)
        plats = []
        for (ex, ey) in (g, dr):
            cy = ey + 44
            for dx in (-17, 17):
                c.line(ex, ey + 2, ex + dx, cy - 3, (140, 96, 30))
            plat = (c.mask_ell(ex, cy, 22, 6) & c.mask_rect(0, cy - 2, W, H)) | c.mask_rect(ex - 22, cy - 2, ex + 22, cy)
            c.shape(plat, gold, shade=gsh, light=gli, band=1, olcol=ol)
            plats.append((ex, cy - 2))
        ex, top = plats[1]                                                     # le tapis de prière, à droite
        tapis = c.mask_rect(ex - 13, top - 4, ex + 13, top)
        c.shape(tapis, (40, 130, 84), shade=(28, 96, 62), band=1, olcol=(20, 40, 30))
        c.fill(c.mask_rect(ex - 11, top - 3, ex + 11, top - 2), (206, 64, 60))
        c.fill(c.mask_rect(ex - 2, top - 4, ex + 2, top - 3), (236, 200, 96))
        for xx in (ex - 15, ex + 14):
            c.fill(c.mask_rect(xx, top - 3, xx + 1, top - 1), (240, 230, 200))
        bal = c.img(K, rgba=True)
        if "prie" not in s._cache:                                             # Petit qui prie, debout sur le tapis
            a_ = cast.dessine(cast.CAST["PETIT"], "priere", "calme", False).a
            s._cache["prie"] = autocollant(Image.fromarray(a_, "RGBA").resize((a_.shape[1] * 3, a_.shape[0] * 3),
                                                                               Image.NEAREST), r=3, ombre=False)
        prie = s._cache["prie"]
        bal.alpha_composite(prie, (int(plats[1][0] * K - prie.width / 2), int((plats[1][1] - 3) * K - prie.height + 30)))
        im = Image.new("RGBA", bal.size, (0, 0, 0, 0))
        gx, gy = plats[1][0] * K, (plats[1][1] - 3) * K                       # halo doré derrière les 2 rakats
        force = 0.35 + (0.65 * smooth((u - s.t_pese) / 0.6) if s.t_pese is not None and u >= s.t_pese else 0.0)
        halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
        dh = ImageDraw.Draw(halo)
        for j, rr in enumerate((150, 110, 74)):
            dh.ellipse([gx - rr, gy - rr * 0.8, gx + rr, gy + rr * 0.8], fill=(255, 220, 120, int((40 + 30 * j) * force)))
        im.alpha_composite(halo)
        im.alpha_composite(bal)
        lx, ly = plats[0][0] * K, plats[0][1] * K                              # le monde, sur le plateau gauche
        glo = s._icone("globe", 8)
        im.alpha_composite(glo, (int(lx - glo.width / 2), int(ly - glo.height + 14)))
        for i, (t_, nom) in enumerate(s._arrivees()):
            if u < t_:
                continue
            e = smooth((u - t_) / 0.3)
            ic = s._icone(nom, 5)
            ox, oy = (v_ * 1.2 for v_ in s.PILE[i % len(s.PILE)])
            x = lx + ox - ic.width / 2
            y = ly - glo.height * 0.55 + oy - ic.height / 2 - 150 * (1 - e)
            im.alpha_composite(_fade(ic, e), (int(x), int(y)))
        lg = s._cache.setdefault("lg", _titres(s.gauche, BLANC, 50))
        im.alpha_composite(lg, (int(max(0, min(im.width - lg.width, lx - lg.width / 2))), int(ly + 9 * K)))
        ld = s._cache.setdefault("ld", _titres(s.droite, JAUNE, 62))
        xld, yld = int(max(0, min(im.width - ld.width, gx - ld.width / 2))), int(plats[1][1] * K + 9 * K)
        im.alpha_composite(ld, (xld, yld))
        if s.t_pese is not None and u >= s.t_pese + 0.8:                       # étincelles + coche
            v = u - s.t_pese - 0.8
            d = ImageDraw.Draw(im)
            rng = np.random.default_rng(int(u * 5))
            al = int(230 * smooth(v / 0.3))
            for _ in range(6):
                x = gx + int(rng.integers(-150, 150))
                y = gy + int(rng.integers(-170, 10))
                d.rectangle([x - K, y - 3 * K, x + K, y + 3 * K], fill=(255, 250, 220, al))
                d.rectangle([x - 3 * K, y - K, x + 3 * K, y + K], fill=(255, 250, 220, al))
            st = s._cache.setdefault("ok", autocollant(objets.icone("check").img(7), r=5))
            e = smooth((v - 0.3) / 0.3)                                        # la coche, devant « 2 RAKATS »
            im.alpha_composite(_fade(st, e), (int(max(0, xld - st.width + 4)), int(yld + ld.height / 2 - st.height / 2)))
        return im


# ---------------------------------------------------------------- le schéma : éléments placés et animés dans le temps
class Schema:
    """Une suite d'ordres datés [(t, "miroir ADA grain"), …] (t en secondes dans le plan) → un dessin d'écran f(img, u)."""

    def __init__(s, ordres, demo=False):
        s.demo = demo
        s.items = []          # dict(el, t_in, t_out)
        s.liens = []          # dict(kind, txt, a, b, t_in, t_out)  flèche entre deux éléments
        s.tampons = []        # dict(nom, el, t_in, t_out)
        s.textes = []         # dict(img, t_in, t_out)
        s.sources = []        # dict(img, t_in)
        s.demos = []          # dict(img, t_in)
        s.etapes, s.t_abs = None, 0.0   # bandeaux d'étape (scénarios) + instant où le plan commence : la source glisse dessous
        s.decale = None                 # (u_fin, dy) : sous le texte d'accroche, le grand schéma descend de dy puis remonte
        for (t, cmd) in sorted(ordres, key=lambda o: o[0]):
            s._ordre(t, cmd)

    def sons(s):
        """Bruitages discrets des éléments : photo = papier, miroir = scintillement, tampon = tampon, autres = ting."""
        out, last = [], -9.0
        evts = [(it["t_in"], type(it["el"]).__name__) for it in s.items] + [(tp["t_in"], "Tampon") for tp in s.tampons]
        for (t, kind) in sorted(evts):
            if t - last < 0.5:
                continue
            nom, g = dict(Photo=("dv_parchemin", 0.05), Miroir=("sa_scintillement", 0.04), Tampon=("imp_tampon", 0.05),
                          Distance=(None, 0), Orteil=(None, 0), Fievre=(None, 0), Forge=(None, 0), Glace=(None, 0),
                          Ablutions=(None, 0), Cauchemar=(None, 0), Gestes=(None, 0), Chemin=(None, 0), Double=(None, 0),
                          Ecran=(None, 0), Tombeau=(None, 0), Chaleur=(None, 0), Soleil=(None, 0), Brulure=(None, 0),
                          Braises=(None, 0), Datte=(None, 0), Serment=(None, 0), Eternue=(None, 0),
                          Colere=(None, 0), Maison=(None, 0), Dette=(None, 0), Sommeil=(None, 0),
                          Liste=(None, 0), Citation=(None, 0), Jauge=(None, 0), Focus=(None, 0), Versus=(None, 0),
                          Bulles=(None, 0), Trajet=(None, 0), Grille=(None, 0)
                          ).get(kind, ("sa_ting", 0.03))
            if nom:
                out.append((t, nom, g, None))
                last = t
        for it in s.items:                                            # sons propres à un élément (choc, vent, balance…)
            f_ = getattr(it["el"], "sons_el", None)
            if f_ is not None:
                out += [(it["t_in"] + u_, nom_, g_, d_) for (u_, nom_, g_, d_) in f_()]
        return out

    def _visibles(s, t):
        return [it for it in s.items if it.get("t_vis", it["t_in"]) <= t and (it["t_out"] is None or t < it["t_out"])]

    def _ajoute(s, t, el):
        if el.plein:
            for it in s._visibles(t):
                it["t_out"] = t
        else:
            vis = [it for it in s._visibles(t) if not it["el"].plein]
            plein = any(it["el"].plein for it in s._visibles(t))
            if len(vis) >= (2 if plein else 3):
                vis[0]["t_out"] = t
        s.items.append(dict(el=el, t_in=t, t_out=None, t_vis=t))     # t_vis : visible dès (1re image d'un Short)

    def _ordre(s, t, cmd):
        brut = cmd.strip()
        mots = brut.split()
        if not mots:
            return
        k = mots[0].lower()
        reste = brut[len(mots[0]):].strip()
        opts = [m.lower() for m in mots[1:]]
        grain = "grain" in opts
        if s.demo and k not in ("source",):
            s.demos.append(dict(img=petit_texte("{" + brut + "}", JAUNE, (60, 40, 10), size=9, k=5), t_in=t))
        qui = mots[1].upper() if len(mots) > 1 else None
        face = next((m for m in opts[1:] if m not in ("grain",) and m in cast_faces()), "neutre")
        if k == "perso":
            s._ajoute(t, Perso(brut, qui, face, grain))
        elif k == "miroir":
            s._ajoute(t, Miroir(brut, qui, face, grain))
        elif k == "photo":
            s._ajoute(t, Photo(brut, qui, face, grain))
        elif k == "compare":
            s._ajoute(t, Miroir(brut, qui, face, grain))
            s._ajoute(t + 0.6, Photo(brut, qui, face, grain))
            s._lien(t + 1.0, "double", "INVERSÉ")
        elif k == "icone":
            s._ajoute(t, Icone(brut, mots[1].lower() if len(mots) > 1 else "question"))
        elif k == "chiffre":
            livre = next((it["el"] for it in s._visibles(t + 0.01) if isinstance(it["el"], Coran)), None)
            if livre is not None and re.search(r"10", reste):          # ×10 sur le Coran ouvert : les « +1 » deviennent « +10 »
                livre.t_x10 = t - next(it["t_in"] for it in s.items if it["el"] is livre)
            else:
                s._ajoute(t, Chiffre(brut, reste))
        elif k == "coran":
            s._ajoute(t, Coran(brut))
        elif k in ("defile", "défile", "scroll"):
            s._ajoute(t, Defile(brut))
        elif k == "compteur":
            m_ = re.match(r'(\d+)\s*->\s*(\d+)\s*(?:"(.+)")?', reste)
            if m_:
                s._ajoute(t, Compteur(brut, int(m_.group(1)), int(m_.group(2)), m_.group(3)))
        elif k == "chrono":
            m_ = re.match(r'(\d+:\d+)\s*(?:"(.+)")?', reste)
            s._ajoute(t, Chrono(brut, m_.group(1) if m_ else "2:00", m_.group(2) if m_ else None))
        elif k == "lettres":                                          # « @0,1.56,2.9 » = instants calés sur la voix
            toks = [c for c in reste.split() if c.strip()]
            temps = None
            if toks and toks[-1].startswith("@"):
                try:
                    temps = [float(x) for x in toks[-1][1:].split(",")]
                except ValueError:
                    temps = None
                toks = toks[:-1]
            s._ajoute(t, Lettres(brut.split(" @")[0], toks, temps=temps))
        elif k == "distance":
            m = re.match(r"(\S+)\s+(.+?)\s*->\s*(.+)$", reste)
            if m:
                s._ajoute(t, Distance(brut, m.group(1).upper(), m.group(2), m.group(3)))
            else:
                s._ajoute(t, Distance(brut, qui or "ADO"))
        elif k in ("fleche", "double-fleche", "doublefleche"):
            s._lien(t, "double" if k.startswith("double") else "simple", reste.strip('"') or None)
        elif k in ("check", "croix"):
            vis = s._visibles(t + 0.01)
            if vis:
                s.tampons.append(dict(nom=k, el=vis[-1]["el"], t_in=t))
        elif k == "radio":
            rad = next((it["el"] for it in reversed(s._visibles(t + 0.01)) if isinstance(it["el"], Radio)), None)
            m_ = re.search(r'"(.+)"', reste)
            sous = mots[1].lower() if len(mots) > 1 else ""
            if sous.startswith("+") or sous in ("tout", "articulations", "reste"):
                if rad is None:                                        # pas encore de radio dans ce plan : on l'ouvre
                    rad = Radio(brut, "PETIT")
                    s._ajoute(t, rad)
                u_ = t - next(it["t_in"] for it in s.items if it["el"] is rad)
                if sous == "tout":
                    labs_ = re.findall(r'"([^"]+)"', reste)
                    rad.t_tout, rad.lab_tout = u_, (labs_[0].upper() if labs_ else None)
                    rad.note_tout = labs_[1].upper() if len(labs_) > 1 else None
                elif sous == "articulations":
                    rad.t_art = u_
                elif sous == "reste":
                    rad.t_reste = u_
                else:
                    rad.plus.append((u_, m_.group(1).upper() if m_ else None))
            else:
                s._ajoute(t, Radio(brut, qui or "PETIT"))
        elif k == "orteil":
            s._ajoute(t, Orteil(brut))
        elif k == "arbre":
            m_ = re.search(r'"(.+)"', reste)
            s._ajoute(t, Arbre(brut, m_.group(1).upper() if m_ else "TES PÉCHÉS"))
        elif k in ("feuilles", "tombe"):
            arb = next((it["el"] for it in reversed(s._visibles(t + 0.01)) if isinstance(it["el"], Arbre)), None)
            if arb is not None:
                arb.t_chute = t - next(it["t_in"] for it in s.items if it["el"] is arb)
        elif k == "balance":
            bal = next((it["el"] for it in reversed(s._visibles(t + 0.01)) if isinstance(it["el"], Balance)), None)
            sous = mots[1].lower() if len(mots) > 1 else ""
            if bal is not None and sous in ("+", "pese", "pèse"):
                u_ = t - next(it["t_in"] for it in s.items if it["el"] is bal)
                if sous == "+":
                    bal.ajouts.append((u_, mots[2].lower() if len(mots) > 2 else "pieces"))
                else:
                    bal.t_pese = u_
            else:
                labs = re.findall(r'"([^"]+)"', reste)
                apres = re.sub(r'"[^"]*"', " ", reste).split()
                s._ajoute(t, Balance(brut, labs[0].upper() if labs else "LE MONDE ENTIER",
                                     labs[1].upper() if len(labs) > 1 else "2 RAKATS",
                                     deja=any(m.lower() in ("deja", "déjà") for m in apres),
                                     en_plus=[m.lower() for m in apres if m.lower() in objets.ICONES]))
        elif k in CLES_0411:                                         # éléments du 04/11 (explique_0411.py)
            import explique_0411
            explique_0411.ordre(s, t, brut, mots, reste)
        elif k in CLES_0411B:                                        # éléments du 04/11 soir (explique_0411b.py)
            import explique_0411b
            explique_0411b.ordre(s, t, brut, mots, reste)
        elif k in CLES_0611:                                         # éléments du 07/11 (explique_0611.py)
            import explique_0611
            explique_0611.ordre(s, t, brut, mots, reste)
        elif k in CLES_0811:                                         # éléments du 08/11 (explique_0811.py)
            import explique_0811
            explique_0811.ordre(s, t, brut, mots, reste)
        elif k in CLES_BRIQUES:                                      # briques réutilisables du 09/11 (briques.py)
            import briques
            briques.ordre(s, t, brut, mots, reste)
        elif k == "texte":
            for x in s.textes:
                if x["t_out"] is None:
                    x["t_out"] = t
            lignes = coupe(reste.strip('"'), 20)
            s.textes.append(dict(img=autocollant(pxv.big_title([(l_, BLANC) for l_ in lignes], size=70 if len(lignes) < 3 else 62),
                                                 r=3, ombre=False), t_in=t, t_out=None))
        elif k == "source":
            s.sources.append(dict(img=pxv.tag_img("SRC " + reste.strip('"').upper()) if hasattr(pxv, "tag_img")
                                  else petit_texte(reste.strip('"')), t_in=t))
        elif k == "efface":
            for it in s._visibles(t):
                it["t_out"] = t
            for x in s.textes:
                if x["t_out"] is None:
                    x["t_out"] = t
            for l in s.liens:
                if l["t_out"] is None:
                    l["t_out"] = t

    def _lien(s, t, kind, txt):
        vis = [it for it in s._visibles(t + 0.01) if not it["el"].plein]
        if len(vis) >= 2:
            s.liens.append(dict(kind=kind, txt=txt, a=vis[-2]["el"], b=vis[-1]["el"], t_in=t, t_out=None))

    # ---- placement
    def _places(s, t, W_, H_):
        """Centre de chaque élément visible à l'instant t (1 au centre, 2 côte à côte, 3 en ligne)."""
        vis = s._visibles(t)
        out = {}
        paysage = W_ > H_
        cy = H_ * (0.44 if paysage else 0.40)
        pleins = [it for it in vis if it["el"].plein]
        if pleins:
            autres = [it for it in vis if not it["el"].plein]
            dy_ = 0.0
            if s.decale:                                               # sous le texte d'accroche des 1res secondes
                fin_, d_ = s.decale
                dy_ = d_ * (1 - smooth((t - (fin_ - 0.35)) / 0.7))
            out[id(pleins[-1]["el"])] = (W_ / 2, cy + (H_ * 0.05 if autres else 0) + dy_)
            for it, x in zip(autres, {1: [0.5], 2: [0.3, 0.7]}.get(len(autres), [])):
                out[id(it["el"])] = (W_ * x, H_ * (0.17 if paysage else 0.205))      # au-dessus du grand schéma
            return out
        n = len(vis)
        xs = {1: [0.5], 2: [0.27, 0.73], 3: [0.19, 0.5, 0.81]}.get(n, [])
        if paysage:
            xs = {1: [0.5], 2: [0.32, 0.68], 3: [0.22, 0.5, 0.78]}.get(n, [])
        for it, x in zip(vis, xs):
            out[id(it["el"])] = (W_ * x, cy)
        return out

    def _pos(s, el, t, W_, H_):
        """Position douce : quand la disposition change, l'élément glisse vers sa nouvelle place (0,5 s)."""
        evts = sorted({x["t_in"] for x in s.items} | {x["t_out"] for x in s.items if x["t_out"] is not None})
        evts = [e for e in evts if e <= t]
        cur = s._places(t, W_, H_).get(id(el))
        if not evts or cur is None:
            return cur
        e = evts[-1]
        prev = s._places(e - 1e-4, W_, H_).get(id(el))
        if prev is None:
            return cur
        k = smooth((t - e) / 0.5)
        return (prev[0] + (cur[0] - prev[0]) * k, prev[1] + (cur[1] - prev[1]) * k)

    # ---- dessin
    def __call__(s, img, u):
        W_, H_ = img.size
        paysage = W_ > H_
        lim_w = W_ * (0.31 if paysage else 0.47)
        lim_h = H_ * (0.66 if paysage else 0.36)
        centres, coins = {}, {}
        for it in s.items:
            if u < it.get("t_vis", it["t_in"]) or (it["t_out"] is not None and u >= it["t_out"] + 0.3):
                continue
            el = it["el"]
            p = s._pos(el, min(u, it["t_out"] - 1e-3) if it["t_out"] is not None else u, W_, H_)
            if p is None:
                continue
            im = el.image((u - it["t_in"]) if getattr(el, "negatif", False) else max(0.0, u - it["t_in"]))
            vis = s._visibles(u)
            n = len([x for x in vis if not x["el"].plein])
            avec_plein = any(x["el"].plein for x in vis) and not el.plein
            lw = (W_ * (0.62 if paysage else 0.95) if el.plein else (lim_w if n <= 2 else W_ * 0.31))
            lh = H_ * (0.72 if paysage else 0.5) if el.plein else (H_ * 0.16 if avec_plein else lim_h)
            sc = min(1.0, lw / im.width, lh / im.height)
            if sc < 0.999:
                im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
            d_entre = 0.0 if (s.decale and it.get("t_vis", it["t_in"]) <= 0.05) else 0.35   # 1re image d'un Short : déjà là
            a = smooth((u - it["t_in"]) / d_entre) if d_entre else 1.0
            if it["t_out"] is not None and u >= it["t_out"]:
                a *= 1 - smooth((u - it["t_out"]) / 0.3)
            dy = ((1 - smooth((u - it["t_in"]) / 0.35)) * 26) if d_entre else 0.0
            if isinstance(el, Icone):
                dy += 6 * math.sin(2 * math.pi * (u - it["t_in"]) / 2.4)
            x, y = p[0] - im.width / 2, p[1] - im.height / 2 + dy
            img.alpha_composite(_fade(im, a), (int(x), int(y)))
            centres[id(el)] = (p[0], p[1], im.width, im.height, a)
            coins[id(el)] = (x, y, sc, el)
            if el.label and not el.plein:
                lab = petit_texte(el.label, BLANC, (30, 24, 40), size=10, k=5)
                img.alpha_composite(_fade(lab, a), (int(p[0] - lab.width / 2), int(p[1] + im.height / 2 + 4 + dy)))
        for l in s.liens:
            if u < l["t_in"] or id(l["a"]) not in centres or id(l["b"]) not in centres:
                continue
            ax, ay, aw, ah, aa = centres[id(l["a"])]
            bx, by, bw, bh, ba = centres[id(l["b"])]
            a = smooth((u - l["t_in"]) / 0.35) * min(aa, ba)
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            if bx - bw / 2 - (ax + aw / 2) > 120:                   # de la place entre les deux : flèche entre eux
                x0, x1, yf = ax + aw / 2 + 20, bx - bw / 2 - 20, (ay + by) / 2
                ylab = yf - 40
            else:                                                   # sinon : flèche sous les deux, avec le texte dessous
                yf = max(ay + ah / 2, by + bh / 2) + 95
                x0, x1 = ax + 30, bx - 30
                ylab = yf + 40
            _fleche(lay, x0, yf, x1, yf, l["kind"] == "double")
            if l["kind"] == "double":                              # miroir ↔ photo : on entoure le grain de beauté
                for el_ in (l["a"], l["b"]):
                    gp = getattr(el_, "grain_pos", None)
                    if gp is not None and id(el_) in coins:
                        x_, y_, sc_, _ = coins[id(el_)]
                        cx_, cy_ = x_ + gp[0] * sc_, y_ + gp[1] * sc_
                        rr = 34 * sc_ + 8
                        e_ = smooth((u - l["t_in"] - 0.4) / 0.35)
                        if e_ > 0:
                            dl = ImageDraw.Draw(lay)
                            dl.ellipse([cx_ - rr, cy_ - rr, cx_ + rr, cy_ + rr], outline=(230, 40, 40, int(255 * e_)), width=8)
            if l["txt"]:
                t = pxv.big_title([(l["txt"], JAUNE)], size=58)
                yy = ylab - t.height if ylab < yf else ylab
                lay.alpha_composite(t, (int((x0 + x1) / 2 - t.width / 2), int(yy)))
            img.alpha_composite(_fade(lay, a))
        for tp in s.tampons:
            if u < tp["t_in"] or id(tp["el"]) not in centres:
                continue
            cx, cy, w, h, aa = centres[id(tp["el"])]
            st = autocollant(objets.icone(tp["nom"]).img(13), r=5)
            a = smooth((u - tp["t_in"]) / 0.3) * aa
            img.alpha_composite(_fade(st, a), (int(cx + w / 2 - st.width * 0.75), int(cy - h / 2 - st.height * 0.25)))
        seul = not any(x["t_in"] <= u and (x["t_out"] is None or u < x["t_out"] + 0.3) for x in s.items)
        ytxt = H_ * (0.42 if seul else (0.80 if paysage else 0.672))
        for x in s.textes:
            if u < x["t_in"] or (x["t_out"] is not None and u >= x["t_out"] + 0.3):
                continue
            a = smooth((u - x["t_in"]) / 0.35)
            if x["t_out"] is not None and u >= x["t_out"]:
                a *= 1 - smooth((u - x["t_out"]) / 0.3)
            im = x["img"]
            if im.width > W_ - 60:
                im = im.resize((W_ - 60, int(im.height * (W_ - 60) / im.width)), Image.LANCZOS)
            img.alpha_composite(_fade(im, a), (int(W_ / 2 - im.width / 2), int(ytxt - im.height / 2)))
        for x in s.sources:
            if u >= x["t_in"]:
                a = smooth((u - x["t_in"]) / 0.35)
                apres_ = [y["t_in"] for y in s.sources if y["t_in"] > x["t_in"]]   # 04/11 : une source à la fois,
                if apres_ and u >= min(apres_):                                 # la suivante la remplace
                    a *= 1 - smooth((u - min(apres_)) / 0.25)
                    if a <= 0.01:
                        continue
                im = x["img"]
                y = int(H_ * (0.12 if paysage else 0.125))
                if s.decale:                                           # sous le texte d'accroche des 1res secondes
                    y += int(205 * (1 - smooth((u - (s.decale[0] - 0.35)) / 0.7)))
                if s.etapes is not None:                               # un bandeau d'étape en haut : elle glisse dessous
                    bas, al = s.etapes.bas(u + s.t_abs, W_, H_)
                    if al > 0:
                        y = int(y + smooth(al) * max(0, bas + 12 - y))
                img.alpha_composite(_fade(im, a), (40, y))
        for j, x in enumerate(s.demos):                                # démo : le code de chaque élément, 1,6 s
            if x["t_in"] <= u < x["t_in"] + 1.8:
                a = smooth((u - x["t_in"]) / 0.2) * (1 - smooth((u - x["t_in"] - 1.5) / 0.3))
                im = x["img"]
                rang = empile([d["t_in"] for d in s.demos], j)
                img.alpha_composite(_fade(im, a), (int(W_ / 2 - im.width / 2),
                                                   int(H_ * (0.03 if paysage else 0.06)) + rang * (im.height + 6)))


def coupe(txt, maxc=20):
    """Coupe un texte en lignes équilibrées d'environ maxc caractères (titres, citations).
    Les guillemets « » et la ponctuation ? ! : restent collés à leur mot (jamais seuls sur une ligne)."""
    for a_, b_ in (("« ", "«§"), (" »", "§»"), (" ?", "§?"), (" !", "§!"), (" :", "§:")):
        txt = txt.replace(a_, b_)
    mots, lignes, cur = [m.replace("§", " ") for m in txt.split()], [], ""
    for m in mots:
        if cur and len(cur) + 1 + len(m) > maxc:
            lignes.append(cur)
            cur = m
        else:
            cur = (cur + " " + m).strip()
    if cur:
        lignes.append(cur)
    return lignes or [txt]


def empile(debuts, j, duree=1.8):
    """Rang d'une étiquette de démo : combien d'étiquettes d'avant sont encore affichées (on les empile)."""
    return sum(1 for i in range(j) if debuts[i] + duree > debuts[j])


def _fleche(img, x0, y0, x1, y1, double=False, col=JAUNE, ep=22):
    d = ImageDraw.Draw(img)
    ang = math.atan2(y1 - y0, x1 - x0)
    tete = 46
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux
    for c, e in ((ENCRE, ep + 10), (col, ep)):
        xa, ya = (x0 + ux * tete * 0.8, y0 + uy * tete * 0.8) if double else (x0, y0)
        xb, yb = x1 - ux * tete * 0.8, y1 - uy * tete * 0.8
        d.line([(xa, ya), (xb, yb)], fill=(*c, 255), width=int(e))
        w2 = tete * (0.75 if c == col else 0.95)
        for (px, py, sgn) in ((x1, y1, 1),) + (((x0, y0, -1),) if double else ()):
            bx, by = px - sgn * ux * tete, py - sgn * uy * tete
            d.polygon([(px, py), (bx + nx * w2, by + ny * w2), (bx - nx * w2, by - ny * w2)], fill=(*c, 255))


_FACES = None


def cast_faces():
    global _FACES
    if _FACES is None:
        _FACES = set(cast.MOUTHMAP) | {"neutre"}
    return _FACES


# ---------------------------------------------------------------- balises dans le texte d'une réplique
BALISE = re.compile(r"\{([^}]*)\}")


def balises(texte):
    """« Dans le miroir, {miroir ADA} tu te vois » → (texte sans balises, [(numéro du mot, "miroir ADA")]).
    Le numéro compte les mots comme les sous-titres (la ponctuation isolée « ? ! » reste collée au mot d'avant)."""
    out, propre, pos = [], [], 0
    for m in BALISE.finditer(texte):
        propre.append(texte[pos:m.start()])
        avant = re.sub(r"\s+", " ", "".join(propre)).strip()
        out.append((_nb_mots(avant), m.group(1).strip()))
        pos = m.end()
    propre.append(texte[pos:])
    txt = re.sub(r"\s+", " ", "".join(propre)).strip()
    txt = re.sub(r"\s+([,.])", r"\1", txt)
    return txt, out


def _nb_mots(txt):
    n = 0
    for tok in txt.split():
        if n and tok in ("?", "!", ":", "?!", ";", "…", "!?"):
            continue
        n += 1
    return n


def temps(D, k, idx):
    """Instant (absolu) du mot n° idx de la réplique k (ou la fin de la réplique)."""
    L = D.lines[k]
    ws = L["words"]
    if idx < len(ws):
        return ws[idx]["s"]
    return max(ws[-1]["s"], L["t1"] - 0.6) if ws else L["t1"]
