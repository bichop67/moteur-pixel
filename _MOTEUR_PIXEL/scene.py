# MISE EN SCÈNE : faire JOUER les personnages et VIVRE le décor (voir LISEZMOI_MOTEUR.txt, partie 8, et les démos).
#   sc = scene.Scene(t0, t1, "cuisine_nuit")                 # un plan, temps en secondes DANS le plan
#   ado = sc.role("ADO", x=330)                               # un personnage (x, y = pieds en pixels écran 1080x1920)
#   ado.entre(0.3, 2.0, depuis="gauche")                      # entre en marchant (bruit de pas discret)
#   ado.a(2.2, pose="question", face="gene")                  # change de pose / d'expression à 2,2 s
#   maman = sc.role("MAMAN", x=760, meuble="chaise")          # assise sur une chaise
#   sc.effet(maman, 1.0, 3.0, "colere")                       # réaction au-dessus de la tête
#   sc.donne(3.0, 3.8, ado, maman, "sac_courses")             # l'objet passe d'une main à l'autre
#   sc.pluie() ; sc.son(0.3, "dv_porte_bois") ; sc.ambiance("amb_pluie")
#   plan = sc.plan()                                          # -> un Shot comme les autres
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pxv, duo, cast, lieux, objets, sets
from px import Px, TAHOMA
from spr import Spr, stamp, INK
from pxv import Shot, Actor, smooth, W, H

R = np.random.default_rng


def _fade(im, a):
    if a >= 0.999:
        return im
    im = im.copy()
    im.putalpha(Image.fromarray((np.array(im)[..., 3] * max(0.0, a)).astype(np.uint8)))
    return im


def _env(u, d, fin=0.25, fout=0.3):
    """Enveloppe douce d'apparition / disparition sur une durée d."""
    return smooth(u / max(1e-6, fin)) * (1 - smooth((u - (d - fout)) / max(1e-6, fout)))


def _ascii(rows, pal):
    sp = Spr(max(len(r) for r in rows), len(rows))
    stamp(sp, rows, pal, 0, 0)
    return sp


# =================================================================== RÔLES (un personnage qui joue dans le temps)
class Role:
    def __init__(s, sc, who, x, y, k, regard, st):
        s.sc, s.who, s.k = sc, who, k
        s.x0, s.y0 = x, y
        s.etats = [(-1.0, dict(st))]
        s.moves = []                       # (t0, t1, x0, y0, x1, y1, "marche" | "glisse")
        s.regards = [(-1.0, regard)]
        s.alphas = []                      # (t0, t1, a0, a1)
        s.bobs = []                        # (t0, t1, amplitude)
        s.talks = []                       # (t0, t1) : bouche qui bouge sans voix
        s.reacs = []                       # (t0, t1, réglages) : réactions passagères (celui qui écoute)
        s.breathe = 0.0

    # ---- positions
    def pos(s, u):
        x, y = s.x0, s.y0
        for (t0, t1, xa, ya, xb, yb, kind) in sorted(s.moves):
            if u >= t1:
                x, y = xb, yb
            elif u >= t0:
                e = (u - t0) / max(1e-6, t1 - t0)
                e = smooth(e) if kind == "glisse" else 0.6 * e + 0.4 * smooth(e)
                x, y = xa + (xb - xa) * e, ya + (yb - ya) * e
                break
            else:
                break
        return x, y

    def miroir(s, u):
        best, mir = -1e9, False
        for (t, cote) in s.regards:
            if t <= u and t >= best:
                best, mir = t, cote == "gauche"
        for (t0, t1, xa, ya, xb, yb, kind) in s.moves:
            if kind in ("marche", "court") and t0 <= u and t0 >= best and xb != xa:
                best, mir = t0, xb < xa
        return mir

    def etat(s, u):
        st = {}
        for (t, d) in sorted(s.etats, key=lambda e: e[0]):
            if t <= u:
                st.update(d)
        for (t0, t1, d) in s.reacs:                          # réaction passagère, sauf si le script a changé ce réglage
            if t0 <= u < t1:
                for k, v in d.items():
                    if not any(t0 < t <= u and k in dd for (t, dd) in s.etats):
                        st[k] = v
        return st

    def reagit(s, t0, t1, **st):
        """Réaction passagère de t0 à t1 (ex. reagit(1.2, 2.4, face="gene", sweat=True)), puis retour à l'état d'avant."""
        s.reacs.append((t0, t1, st))
        return s

    # ---- jeu
    def a(s, t, **st):
        """À l'instant t : nouvelle pose, expression, objet… (ex. a(2.0, pose="question", face="choc"))."""
        s.etats.append((t, st))
        return s

    def regarde(s, t, cote):
        s.regards.append((t, cote))
        return s

    def tourne(s, t):
        s.regards.append((t, "droite" if s.miroir(t) else "gauche"))
        return s

    def marche(s, t0, t1, x, y=None, pas=True):
        xa, ya = s.pos(t0)
        s.moves.append((t0, t1, xa, ya, x, ya if y is None else y, "marche"))
        if pas and s.sc is not None:
            s.sc.son(t0, "dv_pas_pierre", 0.06, t1 - t0)
        return s

    def recule(s, t0, t1, x, y=None, pas=True):
        """Recule (ou avance) jusqu'à x en marchant SANS se retourner (il garde son regard)."""
        xa, ya = s.pos(t0)
        s.moves.append((t0, t1, xa, ya, x, ya if y is None else y, "recule"))
        if pas and s.sc is not None:
            s.sc.son(t0, "dv_pas_pierre", 0.06, t1 - t0)
        return s

    def court(s, t0, t1, x, y=None, pas=True):
        """Court jusqu'à x (pas deux fois plus rapides que la marche)."""
        xa, ya = s.pos(t0)
        s.moves.append((t0, t1, xa, ya, x, ya if y is None else y, "court"))
        if pas and s.sc is not None:
            s.sc.son(t0, "dv_pas_course_maison", 0.05, t1 - t0)
        return s

    def glisse(s, t0, t1, x, y=None):
        xa, ya = s.pos(t0)
        s.moves.append((t0, t1, xa, ya, x, ya if y is None else y, "glisse"))
        return s

    def entre(s, t0, t1, depuis=None, x=None):
        """Entre dans le champ en marchant jusqu'à x (par défaut : sa place de départ)."""
        x = s.x0 if x is None else x
        depuis = depuis or ("gauche" if x < W / 2 else "droite")
        s.x0 = -170 if depuis == "gauche" else W + 170
        return s.marche(t0, t1, x)

    def sort(s, t0, t1, vers="droite"):
        return s.marche(t0, t1, -190 if vers == "gauche" else W + 190)

    def apparait(s, t0, t1=None):
        s.alphas.append((t0, t1 or t0 + 0.4, 0.0, 1.0))
        return s

    def disparait(s, t0, t1=None):
        s.alphas.append((t0, t1 or t0 + 0.4, 1.0, 0.0))
        return s

    def cache(s):
        s.alphas.append((-1.0, -0.5, 0.0, 0.0))
        return s

    def rit(s, t0, t1, amp=9):
        s.bobs.append((t0, t1, amp))
        s.a(t0, face="rire")
        return s

    def sautille(s, t0, t1, amp=12):
        s.bobs.append((t0, t1, amp))
        return s

    def parle(s, t0, t1):
        s.talks.append((t0, t1))
        return s

    def assoit(s, t):
        return s.a(t, assis=True)

    def leve(s, t):
        return s.a(t, assis=False)

    # ---- pour le moteur
    def _alpha(s, u):
        a = 1.0
        for (t0, t1, a0, a1) in sorted(s.alphas):
            if u >= t1:
                a = a1
            elif u >= t0:
                a = a0 + (a1 - a0) * smooth((u - t0) / max(1e-6, t1 - t0))
        return a

    def _pose_avant(s, u):
        """(pose actuelle, instant où elle a commencé, pose d'avant) pour adoucir le geste de l'une à l'autre."""
        cur, tcur, prev = "neutre", -1e9, None
        for (t, d) in sorted(s.etats, key=lambda e: e[0]):
            if t <= u and "pose" in d:
                if d["pose"] != cur:
                    prev, cur, tcur = cur, d["pose"], t
        return cur, tcur, prev

    def state(s, u):
        st = s.etat(u)
        for (t0, t1, xa, ya, xb, yb, kind) in s.moves:
            if kind in ("marche", "recule", "court") and t0 <= u < t1 and s.who != "G" and not st.get("assis"):
                if s.who in cast.CAST:
                    st["step"] = int((u - t0) * (22 if kind == "court" else 12)) % 8   # marche en 8 images
                elif s.who == "P":
                    st["step"] = int((u - t0) * 6) % 4
                else:
                    st["step"] = int((u - t0) * 8) % 4         # animaux
        if s.who in cast.CAST:                                   # geste qui passe en douceur d'une pose à l'autre
            cur, tcur, prev = s._pose_avant(u)
            if prev is not None and tcur > 0 and u - tcur < 0.2:
                st["pose_de"] = prev
                st["mix"] = round((1 - (u - tcur) / 0.2) * 4) / 4
        st["_mirror"] = s.miroir(u)
        a = s._alpha(u)
        if a < 1:
            st["_alpha"] = a
        if any(t0 <= u < t1 for t0, t1 in s.talks):
            st["talk"] = (int(u * 30) // 3) % 3 != 2
        return st

    def path(s, u):
        x, y = s.pos(u)
        for (t0, t1, amp) in s.bobs:
            if t0 <= u < t1:
                y -= amp * abs(math.sin(2 * math.pi * (u - t0) * 1.5)) * _env(u - t0, t1 - t0, 0.15, 0.2)
        return x, y

    def actor(s):
        a = Actor(s.who, s.x0, s.y0, s.k, False, state=s.state, path=s.path, breathe=s.breathe)
        a.sol = lambda u: s.pos(u)[1]                            # l'ombre reste au sol quand il saute
        return a

    def main(s, u):
        """Position écran de la main avant (pour donner / recevoir un objet)."""
        x, y = s.path(u)
        st = s.etat(u)
        mir = s.miroir(u)
        if s.who in cast.CAST:
            r = cast.CAST[s.who]
            g = cast.geo(r, st.get("assis", False))
            pose = st.get("pose", "tient")
            near = cast.POSES.get(pose, cast.POSES["tient"])[1]
            hx, hy = cast._pt(near[1], g.sl, g.ay, g)
            foot = cast.FOOT
        else:
            hx, hy, foot = 31, 50, duo.FOOT
        dx = (hx - 23) * s.k
        return x + (-dx if mir else dx), y - (foot - hy + 3) * s.k


# =================================================================== MEUBLES ET OBJETS DU DÉCOR (même taille de pixel que les persos)
def _dk(c, k=0.72):
    return tuple(int(v * k) for v in c)


def _lt(c, k=0.3):
    return tuple(int(v + (255 - v) * k) for v in c)


def _box(sp, x0, y0, x1, y1, col, sh=True):
    m = sp.m_rect(x0, y0, x1, y1)
    sp.paint(m, col)
    if sh:
        sp.shade(m, _dk(col), dx=-1, dy=-1, depth=1)
        sp.light(m, _lt(col), dx=1, dy=1, depth=1)
    return m


def meuble_sprite(nom, col=None):
    """Sprite d'un meuble ; la dernière ligne touche le sol. Assise des chaises à 12 pixels du sol (= hanches assises)."""
    if nom in ("chaise", "tabouret", "fauteuil"):
        c = col or {"chaise": (150, 100, 62), "tabouret": (120, 80, 50), "fauteuil": (150, 50, 60)}[nom]
        sp = Spr(30, 36)
        seat = 36 - 12
        if nom == "fauteuil":
            _box(sp, 2, seat - 20, 8, seat + 3, c)
            _box(sp, 3, seat - 1, 27, seat + 4, _lt(c, 0.1))
            for x in (4, 24):
                _box(sp, x, seat + 5, x + 2, 35, (90, 60, 40))
        else:
            _box(sp, 3, seat, 27, seat + 2, c)
            for x in (4, 25):
                _box(sp, x, seat + 3, x + 1, 35, _dk(c, 0.8))
            if nom == "chaise":
                _box(sp, 3, seat - 18, 5, seat, c)
                _box(sp, 3, seat - 16, 6, seat - 13, _lt(c, 0.1))
        sp.outline()
        return sp
    if nom == "trone":                                         # trône égyptien : or, rayures bleues, pattes de lion
        G0, G1, G2, B0 = (226, 182, 70), (160, 120, 40), (250, 222, 130), (40, 84, 170)
        sp = Spr(34, 56)
        seat = 56 - 12
        dos = sp.m_rect(2, 8, 8, seat)
        sp.paint(dos, G0); sp.shade(dos, G1, dx=-1, dy=0, depth=2)
        for y in range(11, seat - 2, 4):
            sp.tone(dos & sp.m_rect(0, y, 34, y + 1), B0)
        sp.paint(sp.m_ell(5, 7, 4, 2.4), G2)                                        # fleuron en haut du dossier
        assise = sp.m_rect(2, seat, 30, seat + 3)
        sp.paint(assise, G0); sp.shade(assise, G1, dx=0, dy=-1, depth=1)
        sp.tone(sp.m_rect(2, seat, 30, seat), G2)
        coussin = sp.m_rect(8, seat - 2, 28, seat - 1)
        sp.paint(coussin, (170, 40, 50)); sp.tone(sp.m_rect(8, seat - 2, 28, seat - 2), (210, 80, 80))
        for x0 in (3, 25):                                                          # pattes de lion
            pat = sp.m_rect(x0, seat + 4, x0 + 3, 53) | sp.m_rect(x0 - 1, 54, x0 + 4, 55)
            sp.paint(pat, G0); sp.shade(pat, G1, dx=-1, dy=0, depth=1)
            sp.tone(sp.m_rect(x0 - 1, 55, x0 + 4, 55), G1)
        treillis = sp.m_rect(7, seat + 4, 24, seat + 7)                             # panneau ajouré sous l'assise
        sp.paint(treillis, B0)
        for x in range(7, 25, 3):
            sp.tone(treillis & sp.m_rect(x, 0, x, 99), G0)
        sp.outline()
        return sp
    if nom == "table":
        c = col or (160, 110, 70)
        sp = Spr(34, 40)
        _box(sp, 0, 40 - 22, 33, 40 - 19, c)
        for x in (3, 29):
            _box(sp, x, 40 - 18, x + 2, 39, _dk(c, 0.8))
        sp.outline()
        return sp
    if nom == "bureau":
        c = col or (120, 124, 136)
        sp = Spr(36, 44)
        _box(sp, 0, 44 - 22, 35, 44 - 19, c)
        for x in (3, 31):
            _box(sp, x, 44 - 18, x + 2, 43, _dk(c, 0.8))
        _box(sp, 6, 44 - 33, 8, 44 - 23, (40, 40, 48))                   # écran du portable (côté perso)
        _box(sp, 7, 44 - 23, 20, 44 - 22, (60, 60, 70))
        sp.paint(sp.m_rect(7, 44 - 32, 7, 44 - 24), (140, 200, 250))
        sp.outline()
        return sp
    if nom == "lampe":
        sp = Spr(20, 62)
        _box(sp, 8, 14, 10, 59, (60, 60, 66))
        _box(sp, 4, 59, 15, 61, (60, 60, 66))
        sp.paint(sp.m_poly([(2, 14), (17, 14), (14, 2), (5, 2)]), (240, 220, 170))
        sp.shade(sp.m_poly([(2, 14), (17, 14), (14, 2), (5, 2)]), (210, 186, 130), dx=-1, dy=-1, depth=2)
        sp.outline()
        return sp
    if nom == "plante":
        sp = Spr(24, 40)
        _box(sp, 6, 28, 17, 39, (190, 96, 60))
        rng = R(4)
        for _ in range(12):
            a = rng.uniform(-2.8, -0.35)
            L = rng.uniform(9, 18)
            pts = [(12 + math.cos(a) * L * f, 28 + math.sin(a) * L * f) for f in (0, 0.5, 1)]
            m = sp.m_line(pts, 3)
            sp.paint(m, (60, 140, 70)); sp.shade(m, (40, 100, 50), dx=-1, dy=-1, depth=1)
        sp.outline()
        return sp
    if nom == "tele":
        sp = Spr(40, 42)
        _box(sp, 2, 2, 37, 24, (30, 30, 36))
        sp.paint(sp.m_rect(4, 4, 35, 22), (20, 26, 40))
        _box(sp, 17, 25, 22, 28, (40, 40, 46))
        _box(sp, 4, 29, 35, 41, (120, 84, 54))
        sp.paint(sp.m_rect(8, 33, 31, 33), (90, 60, 40))
        sp.outline()
        return sp
    raise KeyError(nom)


_MEUBLES = {}


def _meuble_img(nom, k, mir, col=None):
    key = (nom, k, mir, col)
    if key not in _MEUBLES:
        im = meuble_sprite(nom, col).img(k)
        _MEUBLES[key] = im.transpose(Image.FLIP_LEFT_RIGHT) if mir else im
    return _MEUBLES[key]


def porte_sprite(ouverture=0.0, col=(150, 96, 60), mur=(26, 22, 30)):
    """Porte vue de face (34 x 62) ; ouverture 0 (fermée) → 1 (grande ouverte, battant presque de profil)."""
    sp = Spr(34, 62)
    _box(sp, 0, 0, 33, 61, (110, 72, 44))                                  # chambranle
    sp.paint(sp.m_rect(3, 3, 30, 61), mur)                                 # l'ouverture (couloir sombre)
    sp.tone(sp.m_rect(3, 3, 30, 8), _lt(mur, 0.06))
    w = int(round(27 * (1 - 0.85 * ouverture)))
    if w > 0:
        leaf = sp.m_rect(3, 3, 3 + w, 61)
        sp.paint(leaf, col); sp.shade(leaf, _dk(col), dx=-1, dy=-1, depth=1)
        if w > 8:
            for y0 in (8, 34):
                sp.tone(sp.m_rect(6, y0, 3 + w - 3, y0 + 20), _lt(col, 0.08))
                sp.tone(sp.m_rect(6, y0, 3 + w - 3, y0), _dk(col, 0.85))
            sp.paint(sp.m_ell(3 + w - 3, 34, 1.2, 1.2), (230, 190, 90))
    sp.outline()
    return sp


# =================================================================== EFFETS AU-DESSUS DES TÊTES
HEART = [".rr.rr.", "rwrrrrr", "rrrrrrr", ".rrrrr.", "..rrr..", "...r..."]
ZED = ["zzzzz", "...z.", "..z..", ".z...", "zzzzz"]
NOTE = ["..nnn", "..n.n", "..n..", "..n..", "nnn..", "nnn.."]
VEIN = ["vv.vv", "v...v", ".....", "v...v", "vv.vv"]
SPARK = ["..y..", "..y..", "yy.yy", "..y..", "..y.."]
PUFF = [".ww.", "wwww", "wwww", ".ww."]
EPAL = dict(r=(226, 44, 70), w=(255, 220, 230), z=(240, 240, 255), n=(40, 30, 60), v=(220, 40, 50), y=(255, 220, 90),
            x=(250, 250, 250))
_ESPR = {}


def _esprite(name, k):
    key = (name, k)
    if key not in _ESPR:
        rows = dict(coeur=HEART, z=ZED, note=NOTE, veine=VEIN, etincelle=SPARK, bouffee=PUFF)[name]
        pal = dict(EPAL)
        if name == "bouffee":
            pal["w"] = (236, 236, 240)
        sp = _ascii(rows, pal)
        sp.outline((40, 30, 40, 255) if name not in ("bouffee",) else (150, 150, 160, 255))
        _ESPR[key] = sp.img(k)
    return _ESPR[key]


def _put(img, spr, x, y, a=1.0):
    img.alpha_composite(_fade(spr, a), (int(x - spr.width / 2), int(y - spr.height / 2)))


def effet_fn(kind):
    """Fonctions (img, u, tête=(x, y_haut, k, miroir), durée) pour Shot.effets."""
    def coeurs(img, u, head, d):
        hx, hy, k, mir = head
        sp = _esprite("coeur", k)
        for i in range(3):
            v = u - i * 0.35
            if v < 0:
                continue
            ph = (v % 1.6) / 1.6
            x = hx + (i - 1) * 9 * k + math.sin(v * 4 + i) * 2 * k
            y = hy - 3 * k - ph * 16 * k
            _put(img, sp, x, y, (1 - ph) * _env(u, d))

    def zzz(img, u, head, d):
        hx, hy, k, mir = head
        for i in range(3):
            v = u - i * 0.45
            if v < 0:
                continue
            ph = (v % 1.5) / 1.5
            kk = max(2, int(k * (0.5 + 0.6 * ph)))
            sp = _esprite("z", kk)
            sgn = -1 if mir else 1
            _put(img, sp, hx + sgn * (6 + ph * 10) * k, hy - ph * 14 * k, (1 - ph * 0.8) * _env(u, d))

    def notes(img, u, head, d):
        hx, hy, k, mir = head
        sp = _esprite("note", k)
        for i in range(2):
            v = u - i * 0.6
            if v < 0:
                continue
            ph = (v % 1.4) / 1.4
            _put(img, sp, hx + (-8 + i * 16) * k + math.sin(v * 5) * 2 * k, hy - 2 * k - ph * 14 * k, (1 - ph) * _env(u, d))

    def colere(img, u, head, d):
        hx, hy, k, mir = head
        a = (0.75 + 0.25 * math.sin(u * 5)) * _env(u, d, 0.2, 0.3)
        sgn = -1 if mir else 1
        _put(img, _esprite("veine", k), hx + sgn * 5 * k, hy + 1 * k, a)
        sp = _esprite("bouffee", k)
        for i in range(2):
            v = u - i * 0.5
            if v < 0:
                continue
            ph = (v % 1.0) / 1.0
            _put(img, sp, hx + (-7 + 14 * i) * k, hy - 2 * k - ph * 9 * k, (1 - ph) * a)

    def idee(img, u, head, d):
        hx, hy, k, mir = head
        sp = objets.icone("ampoule").img(max(2, k // 2 + 1))
        a = _env(u, d, 0.3, 0.3)
        y = hy - 4 * k - 2 * k * smooth(u / 0.3)
        _put(img, sp, hx, y - sp.height / 2, a)
        sk = _esprite("etincelle", max(2, k // 2))
        for i, (dx, dy) in enumerate(((-11, -6), (11, -8), (0, -16))):
            if (u * 3 + i) % 1.2 < 0.8:
                _put(img, sk, hx + dx * k, y - sp.height / 2 + dy * k * 0.5, a)

    def larmes(img, u, head, d):
        hx, hy, k, mir = head
        sp = duo.goutte().img(max(2, k // 2 + 1))
        for i in range(4):
            v = u - i * 0.3
            if v < 0:
                continue
            ph = (v % 1.2) / 1.2
            side = -1 if i % 2 == 0 else 1
            x = hx + side * 5 * k + side * ph * 3 * k
            y = hy + 14 * k + ph * 14 * k
            _put(img, sp, x, y, (1 - ph) * _env(u, d))

    def goutte(img, u, head, d):
        hx, hy, k, mir = head
        sp = duo.goutte().img(k)
        sgn = -1 if mir else 1
        ph = smooth(min(1.0, u / max(0.6, d * 0.8)))
        _put(img, sp, hx - sgn * 8 * k, hy + 4 * k + ph * 6 * k, _env(u, d))

    def etoiles(img, u, head, d):
        hx, hy, k, mir = head
        sp = _esprite("etincelle", k)
        for i in range(3):
            a = u * 3 + i * 2.09
            _put(img, sp, hx + math.cos(a) * 11 * k, hy + 1 * k + math.sin(a) * 3 * k, _env(u, d))

    def points(img, u, head, d):
        hx, hy, k, mir = head
        n = min(3, int(u / 0.35) + 1)
        sz = max(2, k)
        lay = Image.new("RGBA", (16 * k, 4 * sz + 4), (0, 0, 0, 0))
        d_ = ImageDraw.Draw(lay)
        for i in range(n):
            x0 = 2 * k + i * 4 * k + sz
            d_.rectangle([x0 - sz, 2, x0 + sz, 2 + 2 * sz], fill=(30, 26, 34, 255))
            d_.rectangle([x0 - sz + 2, 4, x0 + sz - 2, 2 * sz], fill=(250, 250, 250, 255))
        _put(img, lay, hx, hy - 5 * k, _env(u, d))

    def brille(img, u, head, d):
        hx, hy, k, mir = head
        sp = _esprite("etincelle", max(2, k // 2 + 1))
        for i, (dx, dy) in enumerate(((-12, 2), (12, -2), (-8, -8), (9, 10))):
            ph = ((u * 1.6 + i * 0.37) % 1.0)
            if ph < 0.6:
                _put(img, sp, hx + dx * k, hy + dy * k, math.sin(ph / 0.6 * math.pi) * _env(u, d))

    fn = dict(coeurs=coeurs, zzz=zzz, notes=notes, colere=colere, idee=idee, larmes=larmes, goutte=goutte,
              etoiles=etoiles, points=points, brille=brille)[kind]

    def plus_grand(img, u, head, d):                      # un peu plus gros que les pixels du perso : lisible sur téléphone
        hx, hy, k, mir = head
        fn(img, u, (hx, hy, int(round(k * 1.45)), mir), d)
    return plus_grand


EFFETS = ("coeurs", "zzz", "notes", "colere", "idee", "larmes", "goutte", "etoiles", "points", "brille")


# =================================================================== DÉCOR ANIMÉ (dessiné en pixels du décor, x4)
def _ox(img):
    """Décalage horizontal de la scène élargie (format 16:9 : 420 px), 0 en vertical."""
    return (img.width - W) // 2 if img.width > W else 0


def _calque(img=None):
    if img is None:
        return Px(alpha=True)
    return Px(img.width // 4, img.height // 4, alpha=True)


def _colle(img, c):
    img.alpha_composite(c.img(4, rgba=True))


def pluie(intensite=1.0, seed=3):
    rng = R(seed)
    n = int(110 * intensite)
    x0, y0, sp = rng.uniform(0, 1, 2 * n), rng.uniform(0, 480, 2 * n), rng.uniform(0.85, 1.15, 2 * n)

    def f(img, u):
        c = _calque(img)
        for i in range(min(2 * n, n * c.w // 270)):
            y = (y0[i] + u * 620 * sp[i]) % 520 - 20
            x = (x0[i] * (c.w + 60) - (y - y0[i]) * 0.2) % (c.w + 30) - 15
            for j in range(6):
                c.px(x - j * 0.2, y - j, (200, 214, 240) if j < 4 else (150, 170, 210))
            if 330 < y < 470 and i % 9 == 0:
                c.px(x - 1, y + 1, (210, 226, 250)); c.px(x + 1, y + 1, (210, 226, 250))
        _colle(img, c)
    return f


def neige(intensite=1.0, seed=5):
    rng = R(seed)
    n = int(90 * intensite)
    x0, y0, sp, ph = rng.uniform(0, 1, 2 * n), rng.uniform(0, 480, 2 * n), rng.uniform(0.7, 1.3, 2 * n), rng.uniform(0, 6.3, 2 * n)

    def f(img, u):
        c = _calque(img)
        for i in range(min(2 * n, n * c.w // 270)):
            y = (y0[i] + u * 34 * sp[i]) % 490 - 5
            x = (x0[i] * c.w + math.sin(u * 1.3 + ph[i]) * 6) % c.w
            c.px(x, y, (250, 250, 255))
            if sp[i] > 1.1:
                c.px(x + 1, y, (230, 236, 250)); c.px(x, y + 1, (230, 236, 250)); c.px(x + 1, y + 1, (250, 250, 255))
        _colle(img, c)
    return f


def feuilles(n=16, seed=7, couleurs=((230, 130, 40), (200, 80, 40), (230, 180, 60))):
    rng = R(seed)
    x0, y0, sp, ph = rng.uniform(0, 1, 2 * n), rng.uniform(0, 480, 2 * n), rng.uniform(0.7, 1.3, 2 * n), rng.uniform(0, 6.3, 2 * n)
    cols = [couleurs[i % len(couleurs)] for i in range(2 * n)]

    def f(img, u):
        c = _calque(img)
        for i in range(min(2 * n, n * c.w // 270)):
            y = (y0[i] + u * 26 * sp[i]) % 500 - 10
            x = (x0[i] * (c.w + 10) + math.sin(u * 1.7 + ph[i]) * 14) % (c.w + 10) - 5
            flip = math.sin(u * 3 + ph[i]) > 0
            pts = [(0, 0), (1, 0), (2, 1)] if flip else [(0, 1), (1, 0), (2, 0)]
            for dx, dy in pts:
                c.px(x + dx, y + dy, cols[i])
            c.px(x + 1, y + 1, _dk(cols[i]))
        _colle(img, c)
    return f


def lucioles(n=18, seed=9, zone=(0, 150, 270, 330)):
    rng = R(seed)
    cx, cy = rng.uniform(zone[0], zone[2], n), rng.uniform(zone[1], zone[3], n)
    fx, fy, ph = rng.uniform(0.2, 0.5, n), rng.uniform(0.2, 0.5, n), rng.uniform(0, 6.3, n)

    def f(img, u):
        c = _calque(img)
        sx = c.w / 270
        for i in range(n):
            if math.sin(u * 2.2 + ph[i] * 3) < -0.3:
                continue
            x = cx[i] * sx + math.sin(u * fx[i] + ph[i]) * 14
            y = cy[i] + math.cos(u * fy[i] + ph[i] * 2) * 9
            c.px(x, y, (230, 255, 150))
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if (int(u * 10) + i) % 2:
                    c.px(x + dx, y + dy, (150, 200, 90))
        _colle(img, c)
    return f


def vapeur(x, y, n=3, couleur=(245, 245, 250)):
    """Vapeur qui monte (casserole, tasse, café) ; x, y en pixels écran."""
    def f(img, u):
        c = _calque(img)
        bx, by = (x + _ox(img)) / 4, y / 4
        for i in range(n):
            ph = ((u * 0.55 + i / n) % 1.0)
            yy = by - ph * 22
            xx = bx + math.sin(u * 2 + i * 2) * 3
            r = 1.2 + ph * 2.8
            m = c.mask_ell(xx, yy, r, r * 0.8)
            c.dither(m, couleur, 0.85 - ph * 0.7)
        _colle(img, c)
    return f


def fumee(x, y, n=4):
    return vapeur(x, y, n, (150, 150, 160))


def lueur(img, x, y, r, col, k):
    """Lumière additive douce (feu, lampe, écran) sur l'image écran."""
    x0, y0, x1, y1 = int(max(0, x - r)), int(max(0, y - r)), int(min(W, x + r)), int(min(H, y + r))
    if x1 <= x0 or y1 <= y0:
        return
    box = np.asarray(img.crop((x0, y0, x1, y1))).astype(np.float32)
    yy, xx = np.mgrid[y0:y1, x0:x1]
    d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / r
    w = np.clip(1 - d, 0, 1) ** 1.6 * k
    w = np.round(w * 6) / 6                                                 # paliers (style pixel)
    box[..., :3] = np.clip(box[..., :3] + np.array(col, np.float32) * w[..., None], 0, 255)
    img.paste(Image.fromarray(box.astype(np.uint8), "RGBA"), (x0, y0))


def feu(x, y, taille=1.0, lumiere=True):
    """Flammes qui dansent + lumière qui respire (feu de camp, cheminée, torche) ; x, y = base du feu (écran)."""
    def f(img, u):
        c = _calque(img)
        ox = _ox(img)
        bx, by = (x + ox) / 4, y / 4
        for i, (dx, hh, col) in enumerate(((0, 13, (250, 120, 40)), (-3, 9, (250, 150, 50)), (3, 10, (250, 150, 50)),
                                            (0, 8, (255, 210, 100)), (0, 4, (255, 246, 190)))):
            h = hh * taille * (0.85 + 0.15 * math.sin(u * 9 + i * 1.7))
            w = (4.5 - i * 0.6) * taille
            sway = math.sin(u * 6 + i) * 1.2
            c.fill(c.mask_poly([(bx + dx - w, by), (bx + dx + w, by), (bx + dx + sway, by - h)]), col)
        for j in range(3):
            ph = (u * 0.9 + j / 3) % 1
            c.px(bx + math.sin(u * 3 + j * 2) * 4, by - 14 * taille - ph * 18, (255, 200, 100))
        _colle(img, c)
        if lumiere:
            lueur(img, x + ox, y - 30 * taille, 260 * taille, (90, 46, 10), 0.55 + 0.08 * math.sin(u * 7))
    return f


def clignote(x, y, col=(255, 60, 60), periode=1.6, taille=3):
    def f(img, u):
        a = 0.5 + 0.5 * math.sin(u * 2 * math.pi / periode)
        if a > 0.2:
            lueur(img, x + _ox(img), y, 60 * taille / 3, col, 0.5 * a)
    return f


def voitures(y=1776, periode=7.0, couleurs=((70, 110, 190), (200, 60, 60), (230, 200, 70)), phares=False, decalage=0.0):
    """Voitures qui passent lentement sur la route (devant les persos : à mettre dans anims_avant)."""
    def f(img, u):
        c = _calque(img)
        for i, col in enumerate(couleurs):
            ph = ((u + decalage + i * periode / len(couleurs)) / periode) % 1.0
            sens = 1 if i % 2 == 0 else -1
            x = -70 + ph * (c.w + 140) if sens > 0 else c.w + 70 - ph * (c.w + 140)
            lieux.voiture(c, x, y / 4 + (6 if sens < 0 else 0), col=col, sens=sens, phares=phares)
        _colle(img, c)
    return f


def oiseaux(n=4, y=300, seed=11):
    rng = R(seed)
    off, yy, sp = rng.uniform(0, 1, n), rng.uniform(-30, 30, n), rng.uniform(0.8, 1.2, n)

    def f(img, u):
        c = _calque(img)
        for i in range(n):
            x = ((off[i] + u * 0.05 * sp[i]) % 1.2) * (c.w + 20) - 20
            by = y / 4 + yy[i] / 4 + math.sin(u * 2 + i) * 2
            up = (int(u * 6 + i) % 2) == 0
            pts = [(-3, -1 if up else 1), (-2, -1 if up else 0), (-1, 0), (0, 0), (1, 0), (2, -1 if up else 0), (3, -1 if up else 1)]
            for dx, dy in pts:
                c.px(x + dx, by + dy, (50, 50, 60))
        _colle(img, c)
    return f


def ecran_tv(x0, y0, x1, y1, seed=2):
    """Contenu d'un écran qui change doucement (télé, ordinateur) ; coordonnées écran."""
    rng = R(seed)
    cols = [tuple(int(v) for v in rng.integers(40, 230, 3)) for _ in range(6)]

    def f(img, u):
        ox = _ox(img)
        i = int(u / 1.8) % len(cols)
        ph = (u / 1.8) % 1
        a, b = cols[i], cols[(i + 1) % len(cols)]
        k = smooth((ph - 0.8) / 0.2) if ph > 0.8 else 0
        col = tuple(int(a[j] * (1 - k) + b[j] * k) for j in range(3))
        d = ImageDraw.Draw(img)
        d.rectangle([x0 + ox, y0, x1 + ox, y1], fill=(*col, 255))
        for yy in range(y0, y1, 8):
            d.rectangle([x0 + ox, yy, x1 + ox, yy + 1], fill=(*_dk(col, 0.85), 255))
        lueur(img, (x0 + x1) / 2 + ox, (y0 + y1) / 2, max(x1 - x0, y1 - y0), _dk(col, 0.45), 0.35)
    return f


COSTUMES = ("CHEVALIER", "ROI", "REINE", "ROMAIN", "SULTAN", "SAVANT", "DETECTIVE", "EXPLORATEUR", "PAYSAN",
            "VOYAGEUR", "SAGE", "POLICIER", "CUISINIER", "MEDECIN", "OUVRIER")


def passants(n=4, y=1290, k=5, vitesse=70, seed=1, qui=None, zone=None, exclure=()):
    """Figurants qui passent au fond (derrière les persos principaux). Par défaut : des gens d'aujourd'hui en
    tenue de ville (pas de roi ni de chevalier), jamais les persos qui jouent la scène (exclure = leurs noms)."""
    rng = R(seed)
    off = rng.uniform(0, 1, n)
    sens = [1 if rng.random() < 0.5 else -1 for _ in range(n)]
    choix = rng.uniform(0, 1, n)
    gens = []

    def f(img, u):
        if not gens:                                   # choisis au 1er dessin : la scène connaît alors tous ses rôles
            ex = set(exclure() if callable(exclure) else exclure)
            pool = qui or [n_ for n_ in cast.CAST if not n_.startswith("_") and n_ not in COSTUMES and n_ not in ex
                           and cast.CAST[n_]["haut"] not in ("armure", "toge")]
            gens.extend(pool[int(c * len(pool)) % len(pool)] for c in choix)
        z0, z1 = zone or (-80, img.width + 80)
        span = z1 - z0
        for i, who in enumerate(gens):
            ph = (off[i] + u * vitesse / span) % 1.0
            x = z0 + ph * span if sens[i] > 0 else z1 - ph * span
            st = dict(step=int(u * 10 + i) % 8)
            spr = duo.sprite(who, **st)
            foot = spr.info.get("foot", duo.FOOT)
            im = spr.resize((spr.width * k, spr.height * k), Image.NEAREST)
            if sens[i] < 0:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            arr = np.array(im)
            arr[..., :3] = (arr[..., :3] * 0.74 + np.array([40, 46, 62]) * 0.26).astype(np.uint8)   # un peu dans le lointain
            im = Image.fromarray(arr, "RGBA")
            img.alpha_composite(im, (int(x - im.width / 2), int(y - foot * k)))
    return f


# =================================================================== LE PLAN (Scene)
class Scene:
    def __init__(s, t0, t1, bg, k=None):
        s.t0, s.t1, s.bg = t0, t1, bg
        sp = lieux.SPOTS.get(bg, dict(gauche=(300, 1340), droite=(780, 1340), k=7, opts={}))
        s.sp = sp
        s.k = k or sp["k"]
        s.roles, s.anims, s.avant, s.fx, s.sons, s.bulles, s.over, s.ecr = [], [], [], [], [], [], [], []
        s.meubles = []
        s.lumieres = []                    # sources de lumière ajoutées (feu, lampe) : éclairent les persos
        s.fond2, s.amb, s.cam, s.tags, s.blur = None, None, None, [], 0

    def dur(s):
        return s.t1 - s.t0

    def role(s, who, x=None, y=None, k=None, regard=None, place=None, meuble=None, couleur_meuble=None, **st):
        if place:
            x, y = s.sp[place]
        x = s.sp["gauche"][0] if x is None else x
        y = s.sp["gauche"][1] if y is None else y
        opts = dict(s.sp.get("opts", {}))
        if meuble in ("chaise", "tabouret", "fauteuil", "trone"):
            opts["assis"] = True
        opts.update(st)
        regard = regard or ("gauche" if x > W / 2 else "droite")
        r = Role(s, who, x, y, k or s.k, regard, opts)
        s.roles.append(r)
        if meuble:
            s.meuble(meuble, x, y, k or s.k, regard=regard, col=couleur_meuble)
        return r

    def meuble(s, nom, x, y=None, k=None, regard="droite", col=None, devant=None):
        """Meuble posé au sol (chaise, tabouret, fauteuil, table, bureau, lampe, plante, tele).
        La table et le bureau se mettent devant le perso assis (devant=True par défaut)."""
        y = s.sp["gauche"][1] if y is None else y
        k = k or s.k
        devant = devant if devant is not None else nom in ("table", "bureau")
        mir = regard == "gauche"
        if nom in ("table", "bureau"):
            x = x + (-1 if mir else 1) * 15 * k

        def f(img, u, nom=nom, x=x, y=y, k=k, mir=mir, col=col):
            im = _meuble_img(nom, k, mir, col)
            xx = x + _ox(img)
            img.alpha_composite(im, (int(xx - im.width / 2), int(y - im.height)))
            if nom == "lampe":
                lueur(img, xx, y - im.height + 6 * k, 220, (70, 56, 20), 0.6)
        f._place = True                                       # lié aux places du plan large
        (s.avant if devant else s.anims).append(f)
        if nom == "lampe":
            s.lumieres.append((x, y - 56 * k, 520, (255, 210, 140), 0.7))
        return s

    def porte(s, x, y=None, t_ouvre=0.0, duree=0.6, t_ferme=None, k=None, col=(150, 96, 60), son=True):
        """Porte au mur qui s'ouvre (et se referme) ; un perso peut en sortir avec role.apparait + marche."""
        y = s.sp["gauche"][1] - 40 if y is None else y
        k = k or s.k

        def f(img, u):
            o = smooth((u - t_ouvre) / duree)
            if t_ferme is not None:
                o *= 1 - smooth((u - t_ferme) / duree)
            im = porte_sprite(round(o * 8) / 8, col).img(k)
            img.alpha_composite(im, (int(x + _ox(img) - im.width / 2), int(y - im.height)))
        s.anims.append(f)
        if son:
            s.son(t_ouvre, "dv_porte_bois", 0.12, 2.0)
        return s

    def effet(s, role, t0, t1, kind):
        s.fx.append((role, effet_fn(kind), t0, t1))
        return s

    def bulle(s, role, t0, t1, txt="!"):
        s.bulles.append((role, (lambda b=txt: duo.bulle(b)), t0, t1, 12, -2))
        return s

    def pensee(s, role, t0, t1, icone="ampoule"):
        s.bulles.append((role, (lambda i=icone: objets.pensee(i)), t0, t1, 14, -2))
        return s

    def donne(s, t0, t1, de, a, objet, pose_de="tient", pose_a="tient"):
        """L'objet passe de la main de `de` à celle de `a` (petite courbe douce)."""
        de.a(min(t0 - 0.35, t0), pose=pose_de, objet=objet)
        de.a(t0, objet="aucun", pose="explique")
        a.a(t1, pose=pose_a, objet=objet)
        k = de.k
        spr = _objet_img(objet, k)

        def f(img, u):
            if not (t0 <= u < t1):
                return
            e = smooth((u - t0) / (t1 - t0))
            xa, ya = de.main(t0)
            xb, yb = a.main(t1)
            x = xa + (xb - xa) * e + _ox(img)
            y = ya + (yb - ya) * e - math.sin(e * math.pi) * 9 * k
            im = spr.transpose(Image.FLIP_LEFT_RIGHT) if xb < xa else spr
            img.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
        f._place = True
        s.avant.append(f)
        s.son(t0, "dv_tissu", 0.08)
        return s

    # ---- décor vivant
    def anim(s, f, devant=False):
        (s.avant if devant else s.anims).append(f)
        return s

    def pluie(s, intensite=1.0):
        s.avant.append(pluie(intensite))
        return s

    def neige(s, intensite=1.0):
        s.avant.append(neige(intensite))
        return s

    def feuilles(s, n=16):
        s.avant.append(feuilles(n))
        return s

    def lucioles(s, n=18):
        s.anims.append(lucioles(n))
        return s

    def voitures(s, **kw):
        s.avant.append(voitures(**kw))
        return s

    def passants(s, **kw):
        """Figurants au fond : un peu plus haut et plus petits que les persos de la scène, jamais les mêmes qu'eux."""
        kw.setdefault("y", s.sp["gauche"][1] - 190)
        kw.setdefault("k", max(3, s.k - 3))
        kw.setdefault("exclure", lambda: [r.who for r in s.roles])
        f = passants(**kw)
        f._place = True                                       # pas dans le champ / contre-champ (fond plus calme)
        s.anims.append(f)
        return s

    def oiseaux(s, **kw):
        s.anims.append(oiseaux(**kw))
        return s

    def vapeur(s, x, y, **kw):
        s.anims.append(vapeur(x, y, **kw))
        return s

    def feu(s, x, y, **kw):
        s.anims.append(feu(x, y, **kw))
        s.lumieres.append((x, y - 80, 760, (255, 140, 50), 0.95))
        return s

    def lumiere_source(s, x, y, rayon=500, couleur=(255, 210, 140), force=0.7):
        """Ajoute une source de lumière qui éclaire les persos (lampe, écran, fenêtre…)."""
        s.lumieres.append((x, y, rayon, couleur, force))
        return s

    def regard_parleur(s, D, delai=0.15):
        """Pendant chaque réplique, les autres se tournent vers celui qui parle."""
        for L in D.lines:
            u = L["t0"] - s.t0
            if not (0 <= u < s.dur()):
                continue
            parleur = next((r for r in s.roles if r.who == L["who"]), None)
            if parleur is None:
                continue
            px_, _ = parleur.pos(u)
            for r in s.roles:
                if r is parleur or r.etat(u).get("pose") in ("prosterne", "allonge"):   # prosterné / étendu : il ne
                    continue                                                            # se retourne pas (02/11/2026)
                rx, _ = r.pos(u)
                r.regarde(u + delai, "gauche" if px_ < rx else "droite")
        return s

    def reactions(s, D, graine=3, sobre=False):
        """CELUI QUI ÉCOUTE RÉAGIT tout seul pendant chaque réplique (le jeu écrit dans le script reste prioritaire) :
        hoche la tête quand on lui explique, sourcils levés sur « ! », réfléchit (sourcils) à la fin d'une question,
        gêné avec une goutte quand on s'énerve contre lui, gêné quand l'autre est choqué, sourit (et rit un peu) quand
        l'autre rit, triste quand l'autre pleure, méfiant quand l'autre fait le malin, choqué quand l'autre a peur."""
        rng = R(graine)
        for L in D.lines:
            u0, u1 = L["t0"] - s.t0, L["t1"] - s.t0
            if u1 <= 0 or u0 >= s.dur():
                continue
            parleur = next((r for r in s.roles if r.who == L["who"]), None)
            txt = " ".join(w["t"] for w in L.get("words") or []).strip()
            fp = parleur.etat(u0 + 0.15).get("face", "neutre") if parleur is not None else "neutre"
            d = u1 - u0
            for r in s.roles:
                if r is parleur or r.who not in cast.CAST or r._alpha(u0) < 0.5:
                    continue
                if any(t0 < u1 and u0 < t1 for (t0, t1, *_) in r.moves):
                    continue
                st0 = r.etat(u0)
                if st0.get("face") == "dodo" or st0.get("back"):
                    continue
                a, b = u0 + min(0.5, 0.3 * d), u1 + 0.35
                if fp == "rire":                                 # le rire est contagieux : il sourit, puis rit un peu
                    mi = (a + b) / 2
                    r.reagit(a, mi, face="content")
                    r.reagit(mi, b, face="rire")
                    r.bobs.append((mi, b, 4))
                elif fp in ("pleure", "triste"):
                    r.reagit(a, b, face="triste")
                elif fp in ("enerve", "cri"):
                    r.reagit(a, b, face="gene", sweat=not sobre)          # film (sobre) : pas de goutte comique
                elif fp == "choc" or "?!" in txt:
                    r.reagit(a, b, face="gene")
                elif fp == "malin":
                    r.reagit(a, b, face="suspect")
                elif fp == "peur":
                    r.reagit(a, b, face="choc")
                elif txt.endswith("?"):
                    r.reagit(max(a, u1 - 0.3), u1 + 0.5, accent="?")
                elif txt.endswith("!"):
                    r.reagit(a, min(b, a + 1.0), accent="!")
                elif d >= 1.0:                                   # il écoute : petits hochements de tête
                    for frac in ((0.45,) if d < 2.2 else (0.3, 0.7)):
                        tn = u0 + d * frac + float(rng.uniform(-0.1, 0.1))
                        r.reagit(tn, tn + 0.14, hoche=1)
                        r.reagit(tn + 0.28, tn + 0.42, hoche=1)
        return s

    def champs(s, D, max_suite=2, forcer=(), interdits=()):
        """CHOIX AUTOMATIQUE DU CHAMP / CONTRE-CHAMP : chaque réplique qui RÉPOND à l'autre est filmée par-dessus
        l'épaule de celui qui écoute (la 1re réplique du plan reste en plan large, au plus `max_suite` d'affilée,
        seulement si les deux sont debout et immobiles). forcer / interdits : numéros des répliques (k).
        Renvoie [(t0, t1, parleur, écouteur)] en temps absolus."""
        out, prev, suite = [], None, 0
        for L in D.lines:
            u0, u1 = L["t0"] - s.t0, L["t1"] - s.t0
            if u0 < -0.05 or u1 > s.dur() + 0.2:
                continue
            k = L.get("k")
            r = next((x for x in s.roles if x.who == L["who"]), None)
            if r is None:
                prev, suite = None, 0
                continue
            ecoute = prev if (prev is not None and prev is not r) else None
            if ecoute is None and k in forcer:
                ecoute = next((x for x in s.roles if x is not r and x.who in cast.CAST), None)
            ok = ecoute is not None and k not in interdits and (k in forcer or suite < max_suite) and u1 - u0 >= 0.9

            def libre(x):
                return (x.who in cast.CAST and x._alpha(u0) > 0.99 and not x.etat(u0).get("assis")
                        and not x.etat(u1).get("assis")
                        and not any(t0 < u1 + 0.1 and u0 - 0.1 < t1 for (t0, t1, *_) in x.moves))
            if ok and libre(r) and libre(ecoute):
                out.append((L["t0"], L["t1"] + 0.08, r, ecoute))
                suite += 1
            else:
                suite = 0
            prev = r
        return out

    def plan_epaule(s, debut, fin, face, dos, cote=None, k_face=8, k_dos=15, **kw):
        """CHAMP / CONTRE-CHAMP : `face` (celui qui parle) vu de face, par-dessus l'épaule de `dos` (de dos, en grand,
        au premier plan). Chacun garde son jeu (expression, geste, bouche, réactions). cote = côté de `dos` à l'écran :
        par défaut le même que dans le plan large (règle des 180°)."""
        a, b = debut, fin
        off = a - s.t0
        if cote is None:
            cote = "gauche" if dos.pos(off)[0] < face.pos(off)[0] else "droite"
        y = s.sp["gauche"][1]
        xd, xf = (320, 770) if cote == "gauche" else (760, 310)
        cx = 0.65 * xf + 0.35 * xd                                   # cadré sur celui qui parle
        mir_f = cote == "gauche"
        garde = ("pose", "face", "objet", "blush", "sweat", "larmes", "pose_de", "mix", "talk", "accent", "hoche", "cligne")

        def st_face(u):
            st = {k: v for k, v in face.state(u + off).items() if k in garde}
            st["_mirror"] = mir_f
            al = face._alpha(u + off)
            if al < 1:
                st["_alpha"] = al
            return st

        def st_dos(u):
            st = {k: v for k, v in dos.state(u + off).items() if k in ("pose", "objet", "hoche")}
            st["back"] = True
            st["_mirror"] = cote == "droite"
            return st
        af = Actor(face.who, xf, y + 40, k_face, mir_f, state=st_face, breathe=2)
        af.sol = lambda u: y + 40
        ad = Actor(dos.who, xd, y + 800, k_dos, cote == "droite", state=st_dos, talk_with=None)
        dans = lambda t0, t1: t1 - off > 0 and t0 - off < b - a
        effets = [(0, fn, t0 - off, t1 - off) for (r, fn, t0, t1) in s.fx if r is face and dans(t0, t1)]
        bubbles = [(0, fn, t0 - off, t1 - off, dx, dy) for (r, fn, t0, t1, dx, dy) in s.bulles if r is face and dans(t0, t1)]
        dec = lambda fs: [(lambda img, u, f=f: f(img, u + off)) for f in fs if not getattr(f, "_place", False)]
        sons = [(t - off,) + tuple(x[1:]) for x in s.sons for t in [x[0]] if 0 <= t - off < b - a]
        sh = Shot(a, b, s.bg, [af, ad], cam=(1.28, 1.33, (cx, 1060), (cx + (12 if cote == "gauche" else -12), 1045)),
                  blur=2, fg=False, anims=dec(s.anims), anims_avant=dec(s.avant), effets=effets, bubbles=bubbles, sons=sons,
                  ambiance=s.amb, overlays=dec(s.over), tags=s.tags, ecran=dec(s.ecr), **kw)
        sh.lumieres = list(s.lumieres)
        return sh

    def plan_schema(s, debut, fin, ordres, fond=None, demo=False, etapes=None, **kw):
        """EXPLICATION EN IMAGES : le plan quitte la scène pendant l'explication ; fond = le décor flou et assombri
        (ou un autre décor : fond="tableau") ; ordres = [(t absolu, "miroir ADA grain"), …] : chaque élément
        apparaît pile à son instant (voir explique.py). La voix et les sous-titres continuent.
        etapes = bandeaux d'étape du scénario (la source du schéma glisse dessous quand ils sont là)."""
        import explique
        a, b = debut, fin
        off = a - s.t0
        sch = explique.Schema([(t - a, c) for (t, c) in ordres], demo=demo)
        sch.etapes, sch.t_abs = etapes, a
        voile = {}

        def assombrit(img, u):
            if img.size not in voile:
                voile[img.size] = Image.new("RGBA", img.size, (14, 10, 24, 70 if fond else 125))
            img.alpha_composite(voile[img.size])
        dec = lambda fs: [(lambda img, u, f=f: f(img, u + off)) for f in fs if not getattr(f, "_place", False)]
        sh = Shot(a, b, fond or s.bg, [], cam=(1.04, 1.08, (540, 960), (540, 950)), blur=2 if fond else 7, fg=False,
                  anims=[assombrit], ecran=[sch] + dec(s.ecr), ambiance=s.amb,
                  sons=[(0.0, "tr_whoosh_doux", 0.05, None)] + sch.sons(), **kw)
        sh.relief = False
        return sh

    def plan_photo(s, debut, fin, modele, photographe, etapes, extras=(), demo=False, paysage=False, **kw):
        """DÉMONSTRATION JOUÉE : `photographe` tient le téléphone devant le visage de `modele` et prend la photo, puis
        recule / avance (etapes = [(t absolu, distance en mètres), …]). Une règle au sol suit la distance, et l'écran
        du téléphone (en encart) montre la photo en direct : visage déformé de près, normal de loin.
        extras = ordres datés en plus : « chiffre +30 % » (près du nez, quand c'est près), « check », « texte … », « source … »."""
        import explique
        a, b = debut, fin
        off = a - s.t0
        y = s.sp["gauche"][1]
        k = s.k
        xm = 860                                                   # le modèle, tourné vers la gauche
        gm, gp = cast.geo(cast.CAST[modele.who]), cast.geo(cast.CAST[photographe.who])
        nez = (gm.hd["nose"][0] + 1 - 23) * k                      # avant du visage (par rapport au centre du perso)
        near = cast.POSES["photo"][1]
        hx, hy = cast._pt(near[1], gp.sl, gp.ay, gp)
        main = (hx + 4 - 23) * k                                   # le téléphone, devant la main
        y_tel = y - (cast.FOOT - hy + 3) * k                       # hauteur du téléphone dans le monde
        haut = (cast.FOOT - cast.head_top(modele.who)) * k
        ppm = haut / 1.62                                          # pixels par mètre (taille du modèle ≈ 1,62 m)
        xp = lambda d: xm - nez - d * ppm - main
        # déplacements : chaque étape part de la distance d'avant (vitesse de marche tranquille)
        et = sorted([(t - a, max(0.12, d)) for (t, d) in etapes])
        moves = []
        d_cur = et[0][1] if et else 0.3
        for (u, d) in et[1:]:
            dur = min(2.6, max(1.0, abs(xp(d) - xp(d_cur)) / 230))
            moves.append((u, u + dur, d_cur, d))
            d_cur = d

        def dist(u):
            d = et[0][1] if et else 0.3
            for (u0, u1, d0, d1) in moves:
                if u >= u1:
                    d = d1
                elif u >= u0:
                    e = smooth((u - u0) / (u1 - u0))
                    return d0 + (d1 - d0) * e
            return d

        def bouge(u):
            return any(u0 <= u < u1 for (u0, u1, _, _) in moves)
        garde = ("face", "talk", "accent", "hoche", "cligne", "blush", "sweat", "larmes")

        def st_p(u):
            st = {kk: v for kk, v in photographe.state(u + off).items() if kk in garde}
            st.update(pose="photo", objet="telephone", _mirror=False)
            if bouge(u):
                st["step"] = int(u * 11) % 8
            return st

        def st_m(u):
            st = {kk: v for kk, v in modele.state(u + off).items() if kk in garde}
            st.update(pose="neutre", objet="aucun", _mirror=True)
            return st
        ap = Actor(photographe.who, xp(dist(0)), y, k, False, state=st_p, path=lambda u: (xp(dist(u)), y))
        am = Actor(modele.who, xm, y, k, True, state=st_m)
        sons = [(0.0, "tr_whoosh_doux", 0.05, None), (0.35, "dv_clic", 0.10, None)]
        sons += [(u1 + 0.15, "dv_clic", 0.10, None) for (_, u1, _, _) in moves]
        sons += [(u0, "dv_pas_pierre", 0.06, u1 - u0) for (u0, u1, _, _) in moves]
        flashs = [0.35] + [u1 + 0.15 for (_, u1, _, _) in moves]

        def regle(img_, u):                                        # règle au sol + repères (dessin technique)
            img = Image.new("RGBA", img_.size, (0, 0, 0, 0))
            ox = _ox(img_)
            d = dist(u)
            x0, x1 = xp(d) + main + ox, xm - nez + ox
            yr = y + 26
            dr = ImageDraw.Draw(img)
            for yy in range(int(y_tel), int(yr), 14):              # pointillés : téléphone et nez jusqu'au sol
                dr.line([(x0, yy), (x0, yy + 7)], fill=(255, 255, 255, 170), width=3)
                dr.line([(x1, yy), (x1, yy + 7)], fill=(255, 255, 255, 170), width=3)
            if x1 - x0 > 140:
                explique._fleche(img, x0, yr, x1, yr, double=True, ep=10)
            else:                                                  # trop court pour des flèches : un trait et deux butées
                for c, w in (((22, 18, 30), 14), ((255, 214, 70), 8)):
                    dr.line([(x0, yr), (x1, yr)], fill=(*c, 255), width=w)
                    for xx in (x0, x1):
                        dr.line([(xx, yr - 18), (xx, yr + 18)], fill=(*c, 255), width=w)
            lab = explique.titre_img(explique._fmt_m(d) if abs(d - round(d, 1)) > 0.005 or d < 1 else
                                     f"{d:.1f} m".replace(".", ","), size=70)
            img.alpha_composite(lab, (int((x0 + x1) / 2 - lab.width / 2), int(yr + 18)))
            img_.alpha_composite(img)
        ordres = sorted(extras, key=lambda o: o[0])
        t_chiffre = next(((t - a, c.split(None, 1)[1]) for (t, c) in ordres if c.lower().startswith("chiffre ")), None)
        t_check = next((t - a for (t, c) in ordres if c.lower().split()[0] in ("check", "croix")), None)
        textes = [(t - a, c.split(None, 1)[1].strip('"')) for (t, c) in ordres if c.lower().startswith("texte ")]
        sources = [(t - a, c.split(None, 1)[1].strip('"')) for (t, c) in ordres if c.lower().startswith("source ")]
        demos = [(t - a, c) for (t, c) in ordres] if demo else []
        cache = {}

        def ecran(img, u):                                         # l'écran du téléphone, en encart
            W_, H_ = img.size
            d = dist(u)
            lo, hi = 0.3, 1.5
            pos = min(1.0, max(0.0, (math.log(max(d, 0.1)) - math.log(lo)) / (math.log(hi) - math.log(lo))))
            force = round((1 - pos) * 0.42, 2)
            key = (force, W_ > H_)
            if key not in cache:
                cache[key] = explique.ecran_photo(modele.who, force)
            im = cache[key]
            al = smooth(u / 0.35)
            x, yy = (W_ - im.width - 50, 70) if W_ > H_ else (int(W_ * 0.06), int(H_ * 0.055))
            img.alpha_composite(explique._fade(im, al), (x, yy))
            for tf in flashs:                                      # petit flash doux sur l'écran à chaque photo
                if tf <= u < tf + 0.25:
                    fl = Image.new("RGBA", im.size, (255, 255, 255, int(150 * (1 - (u - tf) / 0.25))))
                    msk = im.getchannel("A")
                    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
                    lay.paste(fl, (0, 0), msk)
                    img.alpha_composite(lay, (x, yy))
            nx, ny = im.info.get("nez", (im.width // 2, im.height // 2))     # le nez dans l'encart
            if t_chiffre and u >= t_chiffre[0]:                    # « +30 % » près du nez, tant que c'est près
                aa = smooth((u - t_chiffre[0]) / 0.35) * (1 - smooth((pos - 0.25) / 0.3))
                if aa > 0.01:
                    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
                    dd = ImageDraw.Draw(lay)
                    cx, cy = x + nx, yy + ny
                    dd.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], outline=(230, 40, 40, 255), width=9)
                    lab = cache.setdefault(("chiffre", t_chiffre[1]), explique.autocollant(
                        explique.titre_img(t_chiffre[1], explique.JAUNE, size=120), r=4, ombre=False))
                    if W_ > H_:                                    # 16:9 : l'encart est à droite, le chiffre à sa gauche
                        lx = x - lab.width - 40
                        explique._fleche(lay, x - 30, cy, cx - 56, cy, col=(230, 40, 40), ep=12)
                        lay.alpha_composite(lab, (int(lx), int(cy - lab.height / 2 - 90)))
                    else:
                        lx = x + im.width + 30
                        explique._fleche(lay, lx + 10, cy, cx + 56, cy, col=(230, 40, 40), ep=12)
                        lay.alpha_composite(lab, (int(lx + 20), int(cy - lab.height / 2 - 90)))
                    img.alpha_composite(explique._fade(lay, aa))
            if moves and u >= moves[-1][1] + 0.3:                    # les deux photos côte à côte : avant / après
                d0, d1 = (et[0][1] if et else 0.3), moves[-1][3]
                pos0 = min(1.0, max(0.0, (math.log(max(d0, 0.1)) - math.log(lo)) / (math.log(hi) - math.log(lo))))
                k0 = ("pola", round((1 - pos0) * 0.42, 2), W_ > H_)
                if k0 not in cache:
                    ph = explique.ecran_photo(modele.who, round((1 - pos0) * 0.42, 2))
                    ph = ph.resize((int(ph.width * 0.86), int(ph.height * 0.86)), Image.LANCZOS)
                    cache[k0] = ph
                ph = cache[k0]
                ea = smooth((u - moves[-1][1] - 0.3) / 0.45)
                px_ = x - ph.width - 40 if W_ > H_ else x + im.width + 40
                img.alpha_composite(explique._fade(ph, ea), (int(px_), int(yy + (1 - ea) * 30)))
                n0 = ph.info.get("nez")
                if n0 and pos0 < 0.3:
                    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
                    ImageDraw.Draw(lay).ellipse([px_ + n0[0] * 0.86 - 40, yy + n0[1] * 0.86 - 40,
                                                 px_ + n0[0] * 0.86 + 40, yy + n0[1] * 0.86 + 40],
                                                outline=(230, 40, 40, 255), width=8)
                    img.alpha_composite(explique._fade(lay, ea))
                for (txt_, xx_, ww_) in ((explique._fmt_m(d0) if d0 < 1 else f"{d0:.1f} m".replace(".", ","), px_, ph.width),
                                         (explique._fmt_m(d1) if d1 < 1 else f"{d1:.1f} m".replace(".", ","), x, im.width)):
                    tl = cache.setdefault(("lab", txt_), explique.autocollant(explique.titre_img(txt_.upper(), size=52), r=3,
                                                                               ombre=False))
                    img.alpha_composite(explique._fade(tl, ea), (int(xx_ + ww_ / 2 - tl.width / 2), int(yy + im.height + 6)))
            if t_check is not None and u >= t_check and pos > 0.85:
                st_ = cache.setdefault("check", explique.autocollant(objets.icone("check").img(12), r=5))
                aa = smooth((u - t_check) / 0.35)
                img.alpha_composite(explique._fade(st_, aa), (int(x + im.width - st_.width * 0.6), int(yy - st_.height * 0.3)))
            for (tt, txt) in textes:
                if u >= tt:
                    t_ = cache.setdefault(("t", txt), explique.autocollant(explique.titre_img(txt, size=62), r=3, ombre=False))
                    img.alpha_composite(explique._fade(t_, smooth((u - tt) / 0.35)),
                                        (int(W_ / 2 - t_.width / 2), int(H_ * (0.80 if W_ > H_ else 0.66))))
            for (tt, txt) in sources:
                if u >= tt:
                    t_ = cache.setdefault(("s", txt), pxv.tag_img("SRC " + txt.upper()))
                    img.alpha_composite(explique._fade(t_, smooth((u - tt) / 0.35)), (int(W_ - t_.width - 40), int(H_ * 0.125)))
            for j, (tt, c) in enumerate(demos):
                if tt <= u < tt + 1.8:
                    t_ = cache.setdefault(("d", c), explique.petit_texte("{" + c + "}", explique.JAUNE, (60, 40, 10), size=9, k=5))
                    aa = smooth((u - tt) / 0.2) * (1 - smooth((u - tt - 1.5) / 0.3))
                    rang = explique.empile([d[0] for d in demos], j)
                    img.alpha_composite(explique._fade(t_, aa), (int(W_ / 2 - t_.width / 2),
                                                                 int(H_ * 0.012) + rang * (t_.height + 6)))
        def cadre(d):                                              # de près : on se rapproche ; de loin : on recule
            lo, hi = 0.3, 1.5
            pos = min(1.0, max(0.0, (math.log(max(d, 0.1)) - math.log(lo)) / (math.log(hi) - math.log(lo))))
            mid = (xp(d) + main + xm - nez) / 2
            if paysage:
                return (1.15 - 0.08 * pos, mid + 250, 1200 - 10 * pos)
            return (1.22 - 0.10 * pos, mid, 1150 - 20 * pos)
        cles = [(0.0,) + cadre(dist(0.0))]
        if moves and moves[0][0] > 1.5:                           # longue pose avant de reculer : on se rapproche
            z_, x_, y_ = cadre(dist(0.0))                          # doucement (l'image ne reste jamais figée)
            cles.append((moves[0][0] - 0.1, z_ + 0.09, x_ + 25, y_ - 25))
        for (u0, u1, d0, d1) in moves:
            cles += [(u0,) + (cles[-1][1:] if cles[-1][0] >= u0 - 0.2 else cadre(d0)), (u1,) + cadre(d1)]
        cles.append((b - a,) + cadre(dist(b - a)))
        cam = [(u, z, (x, yy)) for (u, z, x, yy) in cles]
        sh = Shot(a, b, s.bg, [ap, am], cam=cam, fg=False,
                  anims=[f for f in s.anims if not getattr(f, "_place", False)], overlays=[regle], sons=sons,
                  ambiance=s.amb, ecran=[ecran], **kw)
        sh.lumieres = list(s.lumieres)
        return sh

    # ---- MONTRER dans la scène : étiquette, règle, projecteur, loupe (elles suivent les persos ; plan large seulement)
    def _tete(s, r, u, img):
        x, y = r.path(u)
        x += _ox(img)
        haut = (cast.FOOT - cast.head_top(r.who)) * r.k if r.who in cast.CAST else 70 * r.k
        return x, y, y - haut

    def _env_annot(s, u, t0, t1):
        return smooth((u - t0) / 0.3) * (1 - smooth((u - (t1 - 0.3)) / 0.3)) if t0 <= u < t1 else 0.0

    def etiquette(s, role, t0, t1, texte, couleur=(255, 214, 70)):
        """Étiquette au-dessus d'un perso (« TOI », « TON POTE », « 1,62 m »…), avec une petite flèche vers sa tête."""
        import explique
        lignes = explique.coupe(texte, 11)
        lab = explique.autocollant(pxv.big_title([(l_, couleur) for l_ in lignes], size=54 if len(lignes) > 1 else 58),
                                   r=3, ombre=False)
        win = dict(t0=t0, t1=t1)                                     # prolongée si on la barre / coche plus tard
        role._etiq_last = win

        def f(img, u):
            t0, t1 = win["t0"], win["t1"]
            a = s._env_annot(u, t0, t1)
            if a <= 0:
                return
            x, y, yt = s._tete(role, u, img)
            lay = Image.new("RGBA", (lab.width, lab.height + 44), (0, 0, 0, 0))
            lay.alpha_composite(lab, (0, 0))
            d = ImageDraw.Draw(lay)
            cx = lab.width // 2
            d.polygon([(cx - 20, lab.height - 6), (cx + 20, lab.height - 6), (cx, lab.height + 30)], fill=(22, 18, 30, 255))
            d.polygon([(cx - 13, lab.height - 4), (cx + 13, lab.height - 4), (cx, lab.height + 20)], fill=(*couleur, 255))
            if hasattr(role, "_barres"):                             # (scénarios) la barre de CETTE étiquette
                bt = next((x_ for x_ in role._barres if t0 - 0.05 <= x_ < t1), None)
            else:
                bt = getattr(role, "_barre", None)                   # étiquette barrée en rouge (« c'est faux »)
            if bt is not None and u >= bt:
                e_ = smooth((u - bt) / 0.35)
                lay = lay.copy()
                dl = ImageDraw.Draw(lay)
                x0_, y0_, x1_, y1_ = 8, lab.height * 0.78, 8 + (lab.width - 16) * e_, lab.height * 0.22
                dl.line([(x0_, y0_), (x1_, y0_ + (y1_ - y0_) * e_)], fill=(22, 18, 30, 255), width=20)
                dl.line([(x0_, y0_), (x1_, y0_ + (y1_ - y0_) * e_)], fill=(230, 40, 40, 255), width=12)
            if hasattr(role, "_coches"):                             # (scénarios) la coche de CETTE étiquette
                ct = next((x_ for x_ in role._coches if t0 - 0.05 <= x_ < t1), None)
            else:
                ct = getattr(role, "_coche", None)                   # étiquette cochée en vert
            if ct is not None and u >= ct:
                if not hasattr(role, "_coche_img"):
                    role._coche_img = explique.autocollant(objets.icone("check").img(8), r=4, ombre=False)
                ck = role._coche_img
                big = Image.new("RGBA", (lay.width + ck.width // 2 + 10, lay.height + 20), (0, 0, 0, 0))
                big.alpha_composite(lay, (0, 20))
                big.alpha_composite(explique._fade(ck, smooth((u - ct) / 0.3)), (big.width - ck.width, 0))
                lay = big
            lx = min(max(x - lay.width / 2, 12), img.width - lay.width - 12)       # jamais coupée par le bord
            if abs(lx - (x - lay.width / 2)) > 1:                               # la flèche reste sur la tête
                lay2 = Image.new("RGBA", lay.size, (0, 0, 0, 0))
                lay2.alpha_composite(lab, (0, 0))
                d2 = ImageDraw.Draw(lay2)
                cx2 = min(max(x - lx, 24), lay.width - 24)
                d2.polygon([(cx2 - 20, lab.height - 6), (cx2 + 20, lab.height - 6), (cx2, lab.height + 30)], fill=(22, 18, 30, 255))
                d2.polygon([(cx2 - 13, lab.height - 4), (cx2 + 13, lab.height - 4), (cx2, lab.height + 20)], fill=(*couleur, 255))
                lay = lay2
            img.alpha_composite(explique._fade(lay, a), (int(lx), int(yt - lay.height - 16)))
        f._place = True
        s.over.append(f)
        s.son(t0, "sa_ting", 0.03)
        return s

    def mesure(s, ra, rb, t0, t1, taille=1.65):
        """Règle au sol entre deux persos, avec la distance en mètres (d'après la taille d'un perso ≈ 1,65 m)."""
        import explique

        def f(img, u):
            a = s._env_annot(u, t0, t1)
            if a <= 0:
                return
            xa, ya, ta = s._tete(ra, u, img)
            xb, yb, tb = s._tete(rb, u, img)
            if xa > xb:
                xa, ya, ta, xb, yb, tb = xb, yb, tb, xa, ya, ta
            ppm = (ya - ta) / taille
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            yr = max(ya, yb) + 30
            explique._fleche(lay, xa, yr, xb, yr, double=True, ep=10)
            d_m = abs(xb - xa) / max(1.0, ppm)
            lab = pxv.big_title([(explique._fmt_m(d_m), (255, 255, 255))], size=64)
            lay.alpha_composite(lab, (int((xa + xb) / 2 - lab.width / 2), int(yr + 16)))
            img.alpha_composite(explique._fade(lay, a))
        f._place = True
        s.over.append(f)
        return s

    def projecteur(s, role, t0, t1, force=150):
        """Projecteur : tout s'assombrit sauf le perso (cercle de lumière doux qui le suit)."""
        trou = {}

        def f(img, u):
            a = s._env_annot(u, t0, t1)
            if a <= 0:
                return
            x, y, yt = s._tete(role, u, img)
            r = int((y - yt) * 0.75)
            if r not in trou:
                yy, xx = np.mgrid[-r:r, -r:r].astype(np.float32)
                dd = np.sqrt(xx * xx + yy * yy) / r
                trou[r] = np.clip((dd - 0.62) / 0.38, 0, 1)
            al = np.full((img.height, img.width), 1.0, np.float32)
            cy = int((y + yt) / 2)
            x0, y0 = int(x) - r, cy - r
            sx0, sy0 = max(0, -x0), max(0, -y0)
            sx1, sy1 = min(2 * r, img.width - x0), min(2 * r, img.height - y0)
            if sx1 > sx0 and sy1 > sy0:
                al[y0 + sy0:y0 + sy1, x0 + sx0:x0 + sx1] = trou[r][sy0:sy1, sx0:sx1]
            lay = np.zeros((img.height, img.width, 4), np.uint8)
            lay[..., :3] = (10, 8, 18)
            lay[..., 3] = (al * force * a).astype(np.uint8)
            img.alpha_composite(Image.fromarray(lay, "RGBA"))
        f._place = True
        s.over.append(f)
        return s

    def loupe(s, role, t0, t1):
        """Loupe : le visage du perso en grand dans un rond au-dessus de lui, relié à sa tête (son expression du moment)."""
        import explique
        cache = {}

        def f(img, u):
            a = s._env_annot(u, t0, t1)
            if a <= 0:
                return
            x, y, yt = s._tete(role, u, img)
            face = role.etat(u).get("face", "neutre")
            if face not in cache:
                v = explique.visage_img(role.who, face, False, k=9)
                R_ = 150
                rond = Image.new("RGBA", (2 * R_, 2 * R_), (0, 0, 0, 0))
                fond = Image.new("RGBA", (2 * R_, 2 * R_), (236, 232, 244, 255))
                fond.alpha_composite(v, (R_ - v.width // 2, 2 * R_ - v.height + 10))
                m = Image.new("L", (2 * R_, 2 * R_), 0)
                ImageDraw.Draw(m).ellipse([0, 0, 2 * R_ - 1, 2 * R_ - 1], fill=255)
                rond.paste(fond, (0, 0), m)
                ImageDraw.Draw(rond).ellipse([0, 0, 2 * R_ - 1, 2 * R_ - 1], outline=(22, 18, 30, 255), width=10)
                cache[face] = explique.autocollant(rond, r=6)
            im = cache[face]
            cx = min(max(x, im.width / 2 + 10), img.width - im.width / 2 - 10)
            cy = yt - 60 - im.height / 2
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            d.line([(cx, cy + im.height / 2 - 20), (x, yt + 20)], fill=(255, 255, 255, 230), width=8)
            d.ellipse([x - 40, yt - 10, x + 40, yt + 70], outline=(255, 255, 255, 230), width=6)
            lay.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
            img.alpha_composite(explique._fade(lay, a))
        f._place = True
        s.over.append(f)
        return s

    def pensees(s, role, t0, t1, t_repousse=None, style=None):
        """Pensées noires (waswas) : des nuages sombres tournent autour de la tête ; à t_repousse, il fait « stop »
        et ils s'en vont en fondu. style="peches" : ses péchés = des paquets d'écume SALE autour de lui (certains
        marqués « PÉCHÉ »), la même image que l'écume du rivage qu'on lave ensuite."""
        rng = R(sum(map(ord, role.who)))
        bulles = [(-130, -40, 1.0), (115, -70, 0.85), (-60, -150, 0.75), (70, -175, 0.9), (0, -95, 0.6)]
        signes = ["?", "!", "?", "...", "!?"]
        coul = dict()
        if style == "peches":
            bulles = [(-150, 60, 0.95), (155, 20, 0.9), (-120, -95, 0.8), (125, -135, 0.85), (5, -200, 0.8),
                      (-170, 205, 0.7), (170, 170, 0.75)]
            signes = ["PÉCHÉ", "", "PÉCHÉ", "", "PÉCHÉ", "", ""]
            coul = dict(sombre=(52, 48, 58), fond=(176, 172, 176), encre=(72, 50, 38), ol=(240, 234, 222), k=3, sale=True)
        ph = rng.uniform(0, 6.28, len(bulles))

        def nuage(r_, signe):
            return _nuage_img(r_, signe, **coul)

        def f(img, u):
            if u < t0 or u >= t1 + 0.9:
                return
            x, y, yt = s._tete(role, u, img)
            a_in = smooth((u - t0) / 0.5)
            part = 0.0 if t_repousse is None or u < t_repousse else smooth((u - t_repousse) / 0.9)
            a = a_in * (1 - part) * (1 - smooth((u - t1) / 0.4) if t_repousse is None else 1)
            if a <= 0.01:
                return
            for i, (dx, dy, sc_) in enumerate(bulles):
                ang = ph[i] + u * 0.9
                ox_, oy_ = 14 * math.cos(ang), 9 * math.sin(ang * 1.3)
                fuite = 1 + part * 2.2                              # repoussés : ils s'éloignent
                im = nuage(int((56 if style == "peches" else 48) * sc_), signes[i % len(signes)])
                cx, cy = x + (dx * fuite + ox_), yt + dy * (1 + part * 0.8) + oy_
                img.alpha_composite(_fade(im, a), (int(cx - im.width / 2), int(cy - im.height / 2)))
        f._place = True
        s.over.append(f)
        if t_repousse is not None:
            role.a(t_repousse, pose="arret")
            role.a(t_repousse + 1.4, pose="neutre")
            s.son(t_repousse, "tr_whoosh_vent", 0.04)
        return s

    def orbes(s, x, y, texte, n=1, grand=False, dore=False, pensees=False, t_chasse=None, t_in=0.0):
        """ORBES DE LUMIÈRE à la place d'un prophète ou de Compagnons (on ne les dessine JAMAIS) : n boules lumineuses
        qui flottent doucement, avec un nom dessous (« LE PROPHÈTE », « DES COMPAGNONS ») ; pensees = un petit nuage
        sombre « ! » au-dessus de chacune, HORS de leur lumière (ce qu'ils trouvaient en eux ; jamais de « ? » : ce
        n'était pas du doute, selon an-Nawawi) ; à t_chasse (la réponse du Prophète), leur lumière les chasse."""
        import explique
        r4 = 19 if grand else 13                                    # rayon en gros pixels (x4 à l'écran)
        col = (255, 204, 104) if dore else (160, 208, 255)
        clair = (255, 252, 232) if dore else (240, 250, 255)
        bord = tuple(int(v * 0.62) for v in col)
        ecart = r4 * 4 * 2.6
        pos = [(x + (i - (n - 1) / 2) * ecart, y - (34 if i % 2 else 0)) for i in range(n)]
        lab = explique.autocollant(pxv.big_title([(texte, (255, 255, 255))], size=44), r=3, ombre=False)
        cache = {}

        def boule():
            if "b" not in cache:
                c = Px(2 * r4 + 5, 2 * r4 + 5, alpha=True)
                cx_ = cy_ = r4 + 2.5
                m_out = c.mask_ell(cx_, cy_, r4 + 1, r4 + 1)
                c.fill(m_out, bord)
                m = c.mask_ell(cx_, cy_, r4, r4)
                c.rgrad(m, cx_ - r4 * 0.3, cy_ - r4 * 0.35, r4 * 1.3, clair, col, steps=5)
                c.fill(c.mask_ell(cx_ - r4 * 0.38, cy_ - r4 * 0.42, max(1.5, r4 * 0.22), max(1.2, r4 * 0.16)), (255, 255, 255))
                cache["b"] = c.img(4, rgba=True)
            return cache["b"]

        def f(img, u):
            ox = _ox(img)
            a = smooth((u - t_in) / 0.8)                             # t_in : il apparaît sur un mot
            if a <= 0.01:
                return
            b = boule()
            eclat = 1 + 0.6 * (1 - smooth((u - t_in) / 0.9)) if t_in > 0 else 1.0   # halo plus fort en apparaissant
            for i, (px_, py_) in enumerate(pos):
                cx, cy = px_ + ox, py_ + 10 * math.sin(u * 1.5 + i * 1.9)
                lueur(img, cx, cy, r4 * 4 * 3.4, col, min(0.85, 0.5 * a * eclat))   # halo (paliers, style pixel)
                lueur(img, cx, cy, r4 * 4 * 1.8, clair, 0.35 * a)
                img.alpha_composite(_fade(b, a), (int(cx - b.width / 2), int(cy - b.height / 2)))
                d = ImageDraw.Draw(img)
                for j in range(3):                                     # petits scintillements autour
                    ang = u * 1.1 + i * 2.1 + j * 2.09
                    rr = r4 * 4 * 1.75
                    sx, sy = cx + rr * math.cos(ang), cy + rr * 0.75 * math.sin(ang)
                    tw = 0.5 + 0.5 * math.sin(u * 4.2 + j * 1.7 + i)
                    if tw > 0.45:
                        z = 8 if tw > 0.85 else 4
                        al = int(230 * a * tw)
                        d.rectangle([sx - z / 2, sy - z * 1.5, sx + z / 2, sy + z * 1.5], fill=(*clair, al))
                        d.rectangle([sx - z * 1.5, sy - z / 2, sx + z * 1.5, sy + z / 2], fill=(*clair, al))
                if pensees:                                            # le nuage noir, au-dessus, hors du halo
                    part = 0.0 if t_chasse is None or u < t_chasse else smooth((u - t_chasse) / 1.1)
                    if part < 0.99:
                        nu = _nuage_img(40, "!")
                        yy = cy - r4 * 4 * 2.6 - nu.height + 6 * math.sin(u * 1.3 + i) - 260 * part
                        img.alpha_composite(_fade(nu, a * (1 - part)), (int(cx - nu.width / 2 + (i - 1) * 40 * part), int(yy)))
            yl = max(py_ for _, py_ in pos) + r4 * 4 + 46
            img.alpha_composite(_fade(lab, a), (int(x + ox - lab.width / 2), int(yl)))
        f._place = True
        s.anims.append(f)
        if t_in > 0:
            s.son(t_in, "sa_scintillement", 0.04)
        return s

    def rayon(s, role, t0, t1):
        """Une lumière douce descend du ciel sur le perso (pardon, bénédiction) : faisceau doré + étincelles qui tombent."""
        def f(img, u):
            a = s._env_annot(u, t0, t1)
            if a <= 0:
                return
            x, y, yt = s._tete(role, u, img)
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            for (lw, al) in ((230, 52), (150, 66), (86, 84)):          # faisceau en paliers (style pixel)
                d.polygon([(x - lw * 0.45, 0), (x + lw * 0.45, 0), (x + lw, y + 12), (x - lw, y + 12)],
                          fill=(255, 228, 150, int(al * a)))
            for i in range(12):                                         # étincelles qui descendent doucement
                ph_ = (u * 0.32 + i / 12) % 1.0
                sx = x + 80 * math.sin(i * 2.3 + u * 0.7)
                sy = ph_ * (y - 30)
                z = 6 if i % 3 == 0 else 4
                al = int(220 * a * (1 - 0.6 * ph_))
                d.rectangle([sx - z / 2, sy - z * 1.5, sx + z / 2, sy + z * 1.5], fill=(255, 250, 220, al))
                d.rectangle([sx - z * 1.5, sy - z / 2, sx + z * 1.5, sy + z / 2], fill=(255, 250, 220, al))
            img.alpha_composite(lay)
            lueur(img, x, (y + yt) / 2, max(60, (y - yt) * 0.95), (255, 220, 140), 0.45 * a)
        f._place = True
        s.over.append(f)
        s.son(t0, "sa_scintillement", 0.05)
        return s

    def main_blanche(s, role, t0, duree=4.5):
        """La main de Moussa qui ressort blanche et lumineuse (28:32) : une lumière blanche pure grandit à côté de l'orbe
        (en douceur, jamais un éclair brusque), rayonne lentement, puis s'apaise."""
        def f(img, u):
            if not (t0 <= u < t0 + duree):
                return
            a = smooth((u - t0) / 0.9) * (1 - smooth((u - (t0 + duree - 1.2)) / 1.2))
            if a <= 0:
                return
            x, y, yt = s._tete(role, u, img)
            cx, cy = x + 13 * role.k, y - 0.55 * (y - yt)
            lueur(img, cx, cy, 80 * role.k / 4, (255, 255, 255), 0.7 * a)
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            for i in range(8):
                ang = i * math.pi / 4 + u * 0.35
                L = (64 + 18 * math.sin(u * 1.6 + i)) * role.k / 4
                d.line([(cx, cy), (cx + L * math.cos(ang), cy + L * math.sin(ang))], fill=(255, 255, 255, int(140 * a)),
                       width=max(2, role.k // 2))
            r_ = 9 * role.k / 4
            d.ellipse([cx - r_, cy - r_, cx + r_, cy + r_], fill=(255, 255, 255, int(250 * a)))
            img.alpha_composite(lay)
        f._place = True
        s.over.append(f)
        s.son(t0, "sa_scintillement", 0.06)
        return s

    def ecume(s, t0, texte="TES PÉCHÉS", y=None, duree=3.6):
        """L'écume de la mer (décor plage) : des paquets d'écume sur le rivage avec une étiquette, puis ils
        s'effacent en scintillant (ex. « tes péchés… même s'ils sont comme l'écume de la mer »)."""
        import explique
        rng = R(5)
        y = 1150 if y is None else y
        paquets = [(float(rng.uniform(-40, 1120)), float(rng.uniform(-14, 14)), float(rng.uniform(26, 48))) for _ in range(16)]
        lab = explique.autocollant(pxv.big_title([(texte, (255, 255, 255))], size=58), r=3, ombre=False)

        def f(img, u):
            v = u - t0
            if v < 0 or v >= duree:
                return
            ox = _ox(img)
            a_in = smooth(v / 0.5)
            lave = smooth((v - 1.9) / 1.2)                          # la vague emporte tout
            d = ImageDraw.Draw(img)
            for i, (px_, py_, r_) in enumerate(paquets):
                rr = r_ * (1 - 0.8 * lave)
                if rr < 2:
                    continue
                al = int(235 * a_in * (1 - lave))
                cx, cy = px_ + ox, y + py_ + 4 * math.sin(v * 2 + i)
                d.ellipse([cx - rr * 1.6, cy - rr * 0.55, cx + rr * 1.6, cy + rr * 0.55], fill=(255, 255, 255, al))
                d.ellipse([cx - rr * 0.9, cy - rr * 0.9, cx + rr * 0.6, cy + rr * 0.2], fill=(240, 248, 255, al))
            if 0.3 < lave < 0.98:                                   # étincelles
                for i in range(10):
                    sx = paquets[i][0] + ox + 30 * math.sin(i * 7.1)
                    sy = y - 40 - 120 * lave - 20 * (i % 3)
                    rr = 6 + 6 * math.sin(math.pi * lave)
                    d.polygon([(sx, sy - rr * 2), (sx + rr * 0.5, sy - rr * 0.5), (sx + rr * 2, sy), (sx + rr * 0.5, sy + rr * 0.5),
                               (sx, sy + rr * 2), (sx - rr * 0.5, sy + rr * 0.5), (sx - rr * 2, sy), (sx - rr * 0.5, sy - rr * 0.5)],
                              fill=(255, 250, 220, int(220 * (1 - lave))))
            img.alpha_composite(explique._fade(lab, a_in * (1 - smooth((v - 2.2) / 0.8))),
                                (int(img.width / 2 - lab.width / 2), int(y - 230)))
        f._place = True
        s.anims.append(f)
        s.son(t0 + 1.9, "sa_scintillement", 0.05)
        return s

    def plan_ecume(s, debut, fin, texte="TES PÉCHÉS", y=1150, t_vague=None, sale=False, propre=None, rocher=(), **kw):
        """L'ÉCUME DE LA MER en plan rapproché (décor plage) : beaucoup d'écume sur le rivage, une étiquette, puis une
        vague passe et emporte tout (t_vague = instant de la vague, en secondes dans le plan).
        sale=True : chaque paquet d'écume est un petit péché (écume sale, plusieurs marqués « PÉCHÉ ») ; à t_vague, des
        vagues arrivent l'une après l'autre de gauche à droite et lavent les paquets UN PAR UN (éclat blanc,
        étincelles) ; propre = (t, texte) : autocollant vert coché sur le rivage propre ; rocher = [(t, texte), …] :
        un gros rocher sombre que les vagues ne lavent pas (1er texte = son nom, 2e en orange = ce qu'il faut faire)."""
        import explique
        a, b = debut, fin
        d_ = b - a
        tv = min(max(1.6, d_ * 0.55), d_ - 1.0) if t_vague is None else t_vague
        rng = R(5)
        paquets = [(float(rng.uniform(150, 930)), float(rng.uniform(-30, 40)), float(rng.uniform(22, 44))) for _ in range(26)]
        lab = explique.autocollant(pxv.big_title([(texte, (255, 255, 255))], size=64), r=3, ombre=False)
        if sale:
            return s._plan_ecume_sale(a, b, lab, y, tv, propre, rocher, **kw)

        def mer(img_, u):
            img = Image.new("RGBA", img_.size, (0, 0, 0, 0))       # calque : vrai fondu, sans points noirs
            ox = _ox(img_)
            d = ImageDraw.Draw(img)
            lave = smooth((u - tv) / 1.1)
            a_in = smooth(u / 0.6)
            for i, (px_, py_, r_) in enumerate(paquets):           # l'écume (elle disparaît sous la vague)
                rr = r_ * (1 - 0.85 * lave)
                if rr < 2:
                    continue
                al = int(240 * a_in * (1 - lave))
                cx, cy = px_ + ox, y + py_ + 3 * math.sin(u * 2.2 + i)
                d.ellipse([cx - rr * 1.7, cy - rr * 0.6, cx + rr * 1.7, cy + rr * 0.6], fill=(255, 255, 255, al))
                d.ellipse([cx - rr * 0.8, cy - rr * 0.95, cx + rr * 0.7, cy + rr * 0.1], fill=(236, 246, 255, al))
            if tv - 0.5 <= u < tv + 1.6:                            # la vague
                e = smooth((u - (tv - 0.5)) / 1.4)
                yv = y - 230 + 330 * e
                al = int(200 * (1 - smooth((u - tv - 0.8) / 0.8)))
                for k_, (ep, col) in enumerate(((70, (120, 190, 230)), (34, (200, 236, 250)), (12, (255, 255, 255)))):
                    pts = [(xx + ox, yv + k_ * 10 + 16 * math.sin(xx / 70 + u * 3)) for xx in range(-40, 1130, 30)]
                    d.line(pts, fill=(*col, al), width=ep)
            if 0.3 < lave < 0.99:                                   # étincelles
                for i in range(12):
                    sx = paquets[i][0] + ox + 25 * math.sin(i * 7.1)
                    sy = y - 60 - 160 * lave - 25 * (i % 3)
                    rr = 7 + 7 * math.sin(math.pi * lave)
                    d.polygon([(sx, sy - rr * 2), (sx + rr * 0.5, sy - rr * 0.5), (sx + rr * 2, sy), (sx + rr * 0.5, sy + rr * 0.5),
                               (sx, sy + rr * 2), (sx - rr * 0.5, sy + rr * 0.5), (sx - rr * 2, sy), (sx - rr * 0.5, sy - rr * 0.5)],
                              fill=(255, 250, 220, int(230 * (1 - lave))))
            img_.alpha_composite(img)

        def etiquette_ecran(img, u):
            al = smooth((u - 0.4) / 0.4) * (1 - smooth((u - tv - 0.3) / 0.6))
            if al > 0.01:
                img.alpha_composite(explique._fade(lab, al), (int(img.width / 2 - lab.width / 2), int(img.height * 0.30)))
        cam = (1.55, 1.62, (540, y - 40), (540, y - 50))
        sons = [(0.0, "tr_whoosh_doux", 0.05, None), (tv - 0.4, "amb_vagues_mer", 0.10, 2.2), (tv + 0.4, "sa_scintillement", 0.05, None)]
        sh = Shot(a, b, s.bg, [], cam=cam, fg=False, anims=[mer], ecran=[etiquette_ecran], ambiance=s.amb, sons=sons, **kw)
        sh.lumieres = list(s.lumieres)
        return sh

    def _plan_ecume_sale(s, a, b, lab, y, tv, propre=None, rocher=(), **kw):
        """Voir plan_ecume(sale=True) : chaque paquet d'écume sale = un petit péché, lavé un par un par les vagues."""
        import explique
        d_ = b - a
        rng = R(11)
        xr, yr = s._x_rocher if getattr(s, "_x_rocher", None) else 640, y + 18   # le rocher (grands péchés) : jamais lavé
        paquets = []
        while len(paquets) < 24:
            px_, py_ = float(rng.uniform(205, 885)), float(rng.uniform(-38, 58))
            if abs(px_ - xr) < 95 and abs(py_ - 18) < 60:
                continue
            paquets.append((px_, py_, float(rng.uniform(26, 44))))
        paquets.sort(key=lambda p_: p_[0])
        n_sec = 6                                                   # 6 vagues, chacune lave sa portion du rivage
        x_a, x_b = 190.0, 900.0
        larg = (x_b - x_a) / n_sec
        t_sec = [tv + 0.45 * j for j in range(n_sec)]

        def t_lave(px_):
            j = min(n_sec - 1, max(0, int((px_ - x_a) / larg)))
            return t_sec[j] + 0.32 + 0.12 * ((px_ - x_a - j * larg) / larg)
        tags = set()
        for cible in (240, 400, 560, 830, 330, 660):                 # quelques paquets marqués « PÉCHÉ »
            i_ = min(range(len(paquets)), key=lambda k_: abs(paquets[k_][0] - cible) + (999 if k_ in tags else 0))
            tags.add(i_)
        tag_img = explique.autocollant(pxv.pixel_text("PÉCHÉ", (255, 246, 232), (70, 50, 36), size=10, k=3), r=2, ombre=False)
        cache = {}

        def roc():
            if "r" not in cache:
                c = Px(44, 28, alpha=True)
                m = c.mask_ell(22, 17, 21, 11) | c.mask_ell(15, 12, 11, 9) | c.mask_ell(29, 11, 12, 9)
                c.fill(m, (22, 18, 30))
                m2 = c.mask_ell(22, 17, 20, 10) | c.mask_ell(15, 12, 10, 8) | c.mask_ell(29, 11, 11, 8)
                c.rgrad(m2, 17, 8, 26, (112, 106, 116), (52, 48, 58), steps=5)
                for (x_, y_) in ((12, 18), (24, 21), (31, 16), (19, 9)):
                    c.px(x_, y_, (40, 36, 46)); c.px(x_ + 1, y_, (40, 36, 46))
                cache["r"] = c.img(4, rgba=True)
            return cache["r"]

        def mer(img_, u):
            img = Image.new("RGBA", img_.size, (0, 0, 0, 0))
            ox = _ox(img_)
            d = ImageDraw.Draw(img)
            a_in = smooth(u / 0.6)
            for i, (px_, py_, r_) in enumerate(paquets):            # l'écume sale (les petits péchés)
                tl = t_lave(px_)
                p = (u - tl) / 0.9
                if p >= 1:
                    continue
                cx, cy = px_ + ox, y + py_ + 3 * math.sin(u * 2.2 + i)
                if p < 0:
                    rr, base, haut, al = r_, (164, 162, 168), (200, 198, 204), int(245 * a_in)
                else:
                    blanc = smooth(min(1.0, p / 0.3))
                    rr = r_ * (1 + 0.18 * blanc) * (1 - smooth(max(0.0, (p - 0.3) / 0.7)))
                    base = tuple(int(c0 + (255 - c0) * blanc) for c0 in (164, 162, 168))
                    haut = tuple(int(c0 + (255 - c0) * blanc) for c0 in (200, 198, 204))
                    al = int(245 * (1 - smooth(max(0.0, (p - 0.45) / 0.55))))
                if rr < 2 or al <= 2:
                    continue
                d.ellipse([cx - rr * 1.7 - 5, cy - rr * 0.6 - 5, cx + rr * 1.7 + 5, cy + rr * 0.6 + 5], fill=(58, 52, 60, al))
                d.ellipse([cx - rr * 1.7, cy - rr * 0.6, cx + rr * 1.7, cy + rr * 0.6], fill=(*base, al))
                d.ellipse([cx - rr * 0.8, cy - rr * 0.95, cx + rr * 0.7, cy + rr * 0.1], fill=(*haut, al))
                if p < 0:                                            # points sombres (c'est sale)
                    for k_ in range(3):
                        sx = cx + rr * (k_ - 1) * 0.8
                        sy = cy + rr * 0.15 * ((k_ % 2) * 2 - 1)
                        d.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(84, 74, 62, al))
                if p >= 0.25:                                        # il est lavé : étincelles qui montent
                    e = (p - 0.25) / 0.75
                    for k_ in range(3):
                        sx = cx + (k_ - 1) * 26
                        sy = cy - 30 - 90 * e - 14 * k_
                        z = 7 * (1 - e) + 2
                        al2 = int(235 * (1 - e))
                        d.rectangle([sx - z / 2, sy - z * 1.6, sx + z / 2, sy + z * 1.6], fill=(255, 250, 215, al2))
                        d.rectangle([sx - z * 1.6, sy - z / 2, sx + z * 1.6, sy + z / 2], fill=(255, 250, 215, al2))
            for j in range(n_sec):                                   # les vagues : une langue d'eau par portion
                v = u - (t_sec[j] - 0.25)
                if not (0 <= v < 1.1):
                    continue
                monte = smooth(min(1.0, v / 0.5))
                recule = smooth(max(0.0, (v - 0.55) / 0.55))
                haut_ = y - 64                                       # le bord de l'eau
                bas = haut_ + 10 + 150 * monte - 110 * recule
                al = int(200 * (1 - recule))
                x0 = x_a + j * larg - 40 + ox
                x1 = x0 + larg + 80
                xs_ = np.linspace(x0, x1, 16)
                pts = [(xx, haut_ + (bas - haut_) * math.sin(math.pi * (xx - x0) / (x1 - x0)) ** 0.6
                        + 8 * math.sin(xx / 30 + u * 5)) for xx in xs_]
                d.polygon([(x0, haut_)] + pts + [(x1, haut_)], fill=(110, 186, 228, int(al * 0.62)))
                pts2 = [(xx, haut_ + (yy - haut_) * 0.55) for (xx, yy) in pts]
                d.polygon([(x0, haut_)] + pts2 + [(x1, haut_)], fill=(150, 210, 240, int(al * 0.5)))
                d.line(pts, fill=(255, 255, 255, al), width=14)
                for k_, (xx, yy) in enumerate(pts[1:-1]):             # bulles d'écume blanche au bord
                    if k_ % 2 == 0:
                        d.ellipse([xx - 9, yy - 6, xx + 9, yy + 8], fill=(255, 255, 255, al))
            img_.alpha_composite(img)
            r_img = roc()                                            # le rocher reste, les vagues ne le lavent pas
            img_.alpha_composite(_fade(r_img, a_in), (int(xr + ox - r_img.width / 2), int(yr - r_img.height * 0.7)))
            j_r = min(n_sec - 1, max(0, int((xr - x_a) / larg)))      # la vague se brise sur le rocher : éclaboussure
            v = u - (t_sec[j_r] + 0.2)
            if 0 <= v < 0.8:
                dd = ImageDraw.Draw(img_)
                for k_ in range(9):
                    ang = math.pi * (0.15 + 0.7 * k_ / 8)
                    rr = 40 + 150 * smooth(v / 0.8)
                    sx = xr + ox + rr * math.cos(ang) * (1 if k_ % 2 else -1) * 0.9
                    sy = yr - r_img.height * 0.6 - rr * math.sin(ang) * 0.7 + 120 * (v / 0.8) ** 2
                    z = 9 if k_ % 3 == 0 else 6
                    dd.rectangle([sx - z, sy - z, sx + z, sy + z], fill=(255, 255, 255, int(230 * (1 - v / 0.8))))
            for i in tags:                                           # étiquettes « PÉCHÉ » (partent avec leur paquet)
                px_, py_, r_ = paquets[i]
                p = (u - t_lave(px_)) / 0.5
                if p >= 1:
                    continue
                al = a_in * (1 - smooth(max(0.0, p)))
                yy = y + py_ - r_ - tag_img.height - 6 - 30 * max(0.0, p)
                img_.alpha_composite(_fade(tag_img, al), (int(px_ + ox - tag_img.width / 2), int(yy)))

        cam = (1.55, 1.62, (540, y - 40), (540, y - 50))

        def vers_ecran(u, wx, wy, W_, H_):                           # même calcul que la caméra du plan (pxv)
            e = smooth(u / max(1e-6, d_))
            z = cam[0] + (cam[1] - cam[0]) * e
            cx = cam[2][0] + (cam[3][0] - cam[2][0]) * e
            cy = cam[2][1] + (cam[3][1] - cam[2][1]) * e
            w, h = W_ / z, H_ / z
            x0 = min(max(0, cx - w / 2), W - w)
            y0 = min(max(0, cy - h / 2), H - h)
            return (wx - x0) * z, (wy - y0) * z

        def coll(txt, col, size=56, cocher=False):
            lignes = explique.coupe(txt, 14)
            im = explique.autocollant(pxv.big_title([(l_, col) for l_ in lignes], size=size), r=3, ombre=False)
            if cocher:
                ck = explique.autocollant(objets.icone("check").img(8), r=4, ombre=False)
                big = Image.new("RGBA", (im.width + ck.width // 2 + 10, im.height + 24), (0, 0, 0, 0))
                big.alpha_composite(im, (0, 24))
                big.alpha_composite(ck, (big.width - ck.width, 0))
                im = big
            return im
        lab_p = coll(propre[1], (110, 220, 120), cocher=True) if propre else None
        badge = explique.autocollant(pxv.big_title([("100 × SUBHAN ALLAH", (255, 214, 70)), ("WA BIHAMDIH", (255, 255, 255))],
                                                   size=54), r=3, ombre=False)
        labs_r = [coll(txt_, (255, 255, 255) if k_ == 0 else (255, 170, 70), size=56 if k_ == 0 else 50)
                  for k_, (_, txt_) in enumerate(rocher)]

        def textes(img, u):
            W_, H_ = img.size
            al = smooth((u - 0.4) / 0.4) * (1 - smooth((u - tv - 0.2) / 0.5))
            if al > 0.01:                                            # « TES PÉCHÉS » jusqu'aux vagues
                img.alpha_composite(explique._fade(lab, al), (int(W_ / 2 - lab.width / 2), int(H_ * 0.31)))
            ab = smooth((u - 0.2) / 0.4) * (1 - smooth((u - tv - 2.4) / 0.5))
            if ab > 0.01:                                            # le dhikr (100 fois) : c'est LUI qui lave
                pul = 1 + 0.12 * math.sin(math.pi * min(1.0, max(0.0, (u - tv + 0.15) / 0.5)))
                bi = badge if abs(pul - 1) < 1e-3 else badge.resize((int(badge.width * pul), int(badge.height * pul)), Image.LANCZOS)
                img.alpha_composite(explique._fade(bi, ab), (int(W_ / 2 - bi.width / 2), int(H_ * 0.205 - (bi.height - badge.height) / 2)))
            if lab_p is not None and u >= propre[0]:
                sx, sy = vers_ecran(u, 380, y - 40, W_, H_)
                e = smooth((u - propre[0]) / 0.35)
                xx = min(max(sx - lab_p.width / 2, 30), W_ - 170 - lab_p.width)
                img.alpha_composite(explique._fade(lab_p, e), (int(xx), int(sy - 250 - lab_p.height + (1 - e) * 20)))
            sx, sy = vers_ecran(u, xr, yr - 40, W_, H_)
            yy = sy - 50
            for k_ in range(len(labs_r) - 1, -1, -1):                # empilés au-dessus du rocher
                im = labs_r[k_]
                yy -= im.height + 8
                if u < rocher[k_][0]:
                    continue
                e = smooth((u - rocher[k_][0]) / 0.35)
                xx = min(max(sx - im.width / 2, 30), W_ - 150 - im.width)
                img.alpha_composite(explique._fade(im, e), (int(xx), int(yy + (1 - e) * 20)))
        sons = [(0.0, "tr_whoosh_doux", 0.05, None), (tv - 0.3, "amb_vagues_mer", 0.10, 3.6),
                (tv + 0.7, "sa_scintillement", 0.05, None), (tv + 2.0, "sa_scintillement", 0.04, None)]
        sons += [(t_, "sa_ting", 0.03, None) for t_ in ([propre[0]] if propre else []) + [t_ for (t_, _) in rocher]]
        sh = Shot(a, b, s.bg, [], cam=cam, fg=False, anims=[mer], ecran=[textes], ambiance=s.amb, sons=sons, **kw)
        sh.lumieres = list(s.lumieres)
        return sh

    def accessoire(s, nom, x, y=None):
        """Un objet posé par terre (trottinette, branche, caillou, carton) ; on peut le pousser : sc.pousse(…)."""
        y = s.sp["gauche"][1] if y is None else y
        obj = dict(nom=nom, x0=x, y=y, moves=[], ymoves=[])
        s.accessoires = getattr(s, "accessoires", []) + [obj]
        k = s.k

        def pos(u):
            x_ = obj["x0"]
            for (t0, t1, xa, xb) in obj["moves"]:
                if u >= t1:
                    x_ = xb
                elif u >= t0:
                    x_ = xa + (xb - xa) * smooth((u - t0) / (t1 - t0))
            return x_
        obj["pos"] = pos

        def posy(u):                                                 # rangé contre le mur : il recule (y plus petit)
            y_ = obj["y"]
            for (t0, t1, ya, yb) in obj["ymoves"]:
                if u >= t1:
                    y_ = yb
                elif u >= t0:
                    y_ = ya + (yb - ya) * smooth((u - t0) / (t1 - t0))
            return y_

        def f(img, u):
            im = _accessoire_img(nom, k)
            xx = pos(u) + _ox(img)
            img.alpha_composite(im, (int(xx - im.width / 2), int(posy(u) - im.height + k)))
        f._place = True
        s.anims.append(f)
        return obj

    def pousse(s, role, t, nom, vers=None, apres="revient"):
        """Le perso va jusqu'à l'objet et le pousse hors du chemin (vers = x d'arrivée de l'objet), puis
        apres = "revient" (retourne à sa place, face à la scène), "continue" (poursuit sa route et sort) ou "reste"."""
        obj = next((o for o in getattr(s, "accessoires", []) if o["nom"] == nom), None)
        if obj is None:
            return s
        xo = obj["pos"](t)
        xr = role.pos(t)[0]
        cote = -1 if xr < xo else 1                                 # il arrive par la gauche ou par la droite
        if vers == "mur":                                           # il le range contre le mur : le passage est libre
            ecart = 95
            role.marche(t, t + 0.9, xo + cote * ecart)
            role.a(t + 0.9, pose="tient")
            obj["ymoves"].append((t + 1.0, t + 2.0, obj["y"], obj["y"] - 85))
            obj["moves"].append((t + 1.0, t + 2.0, xo, xo + cote * 20))
            role.a(t + 2.1, pose="neutre")
            if apres == "revient":
                role.marche(t + 2.3, t + 3.3, xr)
                role.regarde(t + 3.4, "droite" if xr < 540 else "gauche")
            s.son(t + 1.0, "dv_tissu", 0.06)
            return s
        vers = (xo + 270 * (-cote)) if vers is None else vers
        ecart = 105
        role.marche(t, t + 0.9, xo + cote * ecart)
        role.a(t + 0.9, pose="tient")
        role.marche(t + 1.0, t + 2.3, vers + cote * ecart)
        obj["moves"].append((t + 1.0, t + 2.3, xo, vers))
        role.a(t + 2.4, pose="neutre")
        if apres == "revient":
            role.marche(t + 2.6, t + 3.8, xr)
            role.regarde(t + 3.9, "droite" if xr < 540 else "gauche")
        elif apres == "continue":
            role.sort(t + 2.7, t + 4.6, vers="droite" if cote < 0 else "gauche")
        s.son(t + 1.0, "dv_tissu", 0.06)
        return s

    def plan_selfie(s, debut, fin, role, extras=(), demo=False, paysage=False, **kw):
        """SELFIE : le perso se prend en photo, bras tendu ; l'écran de son téléphone (en encart) montre le selfie,
        avec son expression du moment et la déformation d'un téléphone trop près."""
        import explique
        a, b = debut, fin
        off = a - s.t0
        y = s.sp["gauche"][1]
        x = 400
        garde = ("face", "talk", "accent", "hoche", "cligne", "blush", "sweat", "larmes")

        def st(u):
            d = {kk: v for kk, v in role.state(u + off).items() if kk in garde}
            d.update(pose="selfie", objet="telephone", _mirror=False)
            return d
        acteur = Actor(role.who, x, y, s.k, False, state=st)
        cache = {}
        demos = [(t - a, c) for (t, c) in sorted(extras)] if demo else []

        def ecran(img, u):
            W_, H_ = img.size
            face = role.etat(u + off).get("face", "neutre")
            if face not in cache:
                cache[face] = explique.ecran_photo(role.who, 0.33, face=face)
            im = cache[face]
            al = smooth(u / 0.35)
            xx, yy = (W_ - im.width - 50, 60) if W_ > H_ else (W_ - im.width - 50, int(H_ * 0.06))
            img.alpha_composite(explique._fade(im, al), (xx, yy))
            if 0.4 <= u < 0.65:                                    # le petit flash du selfie (sur l'écran seulement)
                fl = Image.new("RGBA", im.size, (255, 255, 255, int(150 * (1 - (u - 0.4) / 0.25))))
                lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
                lay.paste(fl, (0, 0), im.getchannel("A"))
                img.alpha_composite(lay, (xx, yy))
            for j, (tt, c) in enumerate(demos):
                if tt <= u < tt + 1.8:
                    t_ = cache.setdefault(("d", c), explique.petit_texte("{" + c + "}", explique.JAUNE, (60, 40, 10), size=9, k=5))
                    aa = smooth((u - tt) / 0.2) * (1 - smooth((u - tt - 1.5) / 0.3))
                    rang = explique.empile([d[0] for d in demos], j)
                    img.alpha_composite(explique._fade(t_, aa), (int(W_ / 2 - t_.width / 2), int(H_ * 0.012) + rang * (t_.height + 6)))
        cam = (1.42, 1.48, (x + 170, y - 300), (x + 160, y - 310)) if not paysage else (1.25, 1.3, (x + 350, y - 330), (x + 340, y - 335))
        sh = Shot(a, b, s.bg, [acteur], cam=cam, fg=False, anims=[f for f in s.anims if not getattr(f, "_place", False)],
                  ecran=[ecran], ambiance=s.amb, sons=[(0.0, "tr_whoosh_doux", 0.04, None), (0.4, "dv_clic", 0.10, None)], **kw)
        sh.lumieres = list(s.lumieres)
        return sh

    def plan_reflet(s, debut, fin, role, extras=(), demo=False, D=None, paysage=False, face=None, **kw):
        """MIROIR : le perso de dos au premier plan, son reflet dans un grand miroir au mur (inversé, il bouge et
        parle comme lui). extras : « texte … », « source … »."""
        import explique
        a, b = debut, fin
        off = a - s.t0
        y = s.sp["gauche"][1]
        garde = ("face", "talk", "accent", "hoche", "cligne", "blush", "sweat", "larmes", "pose_de", "mix")

        def st_dos(u):
            return dict(pose="neutre", back=True, _mirror=False)

        def st_reflet(u):
            st = {kk: v for kk, v in role.state(u + off).items() if kk in garde}
            st.update(pose="neutre", objet="aucun", _mirror=True)
            if face:
                st["face"] = face
            return st
        etoiles = face in ("content", "fier", "coeur", "etoile", "malin", "rire")
        if paysage:                                                # 16:9 : on voit moins haut, tout est plus petit
            mx0, my0, mx1, my1 = 230, 460, 850, 1190
            k_ref = 8
        else:
            mx0, my0, mx1, my1 = 250, 300, 830, 1230               # le miroir (coordonnées du format vertical)
            k_ref = 11
        cadre = {}

        def miroir(img, u):
            ox = _ox(img)
            key = img.size
            if key not in cadre:
                w_, h_ = mx1 - mx0, my1 - my0
                fr = Image.new("RGBA", (w_ + 60, h_ + 60), (0, 0, 0, 0))
                d = ImageDraw.Draw(fr)
                d.rounded_rectangle([0, 0, w_ + 59, h_ + 59], 70, fill=(196, 150, 70, 255), outline=(22, 18, 30, 255), width=8)
                d.rounded_rectangle([16, 16, w_ + 43, h_ + 43], 58, fill=(232, 196, 110, 255))
                d.rounded_rectangle([30, 30, w_ + 29, h_ + 29], 46, fill=(150, 186, 204, 255))
                m = Image.new("L", (w_, h_), 0)
                ImageDraw.Draw(m).rounded_rectangle([0, 0, w_ - 1, h_ - 1], 46, fill=255)
                cadre[key] = (fr, m)
            fr, m = cadre[key]
            img.alpha_composite(fr, (mx0 - 30 + ox, my0 - 30))
            glace = Image.new("RGBA", (mx1 - mx0, my1 - my0), (0, 0, 0, 0))
            gd = ImageDraw.Draw(glace)
            for i in range(0, glace.height, 4):
                c = int(200 - 50 * i / glace.height)
                gd.rectangle([0, i, glace.width, i + 3], fill=(c - 40, c - 6, min(255, c + 24), 255))
            st = st_reflet(u)
            st.pop("_mirror", None)
            if D is not None and D.talking(role.who, a + u):          # le reflet parle comme lui
                st["talk"] = True
                if hasattr(D, "bouche"):
                    st["bouche"] = D.bouche(role.who, a + u)
            if pxv.blink(a + u, (sum(map(ord, role.who)) % 17) / 5.0):
                st["cligne"] = True
            spr = duo.sprite(role.who, **st)
            im = spr.resize((spr.width * k_ref, spr.height * k_ref), Image.NEAREST).transpose(Image.FLIP_LEFT_RIGHT)
            yh = cast.head_top(role.who) * k_ref
            glace.alpha_composite(im, (int(glace.width / 2 - im.width / 2), int((70 if paysage else 120) - yh)))
            ph = (u * 0.4) % 1.7                                     # reflet de lumière qui passe
            if ph < 1.0:
                bd = ImageDraw.Draw(glace)
                gh = glace.height
                xx = -gh + (glace.width + 2 * gh) * ph
                bd.polygon([(xx, gh), (xx + 90, gh), (xx + 90 + gh, 0), (xx + gh, 0)], fill=(255, 255, 255, 40))
            if etoiles:                                              # petites étincelles : elle se trouve belle
                sd = ImageDraw.Draw(glace)
                hx_ = glace.width / 2
                for i, (dx_, dy_) in enumerate(((-150, 60), (140, 20), (-110, 230), (160, 200))):
                    al_ = 0.5 + 0.5 * math.sin(2 * math.pi * (u * 0.9 + i * 0.27))
                    if al_ < 0.15:
                        continue
                    cx_, cy_, rr = hx_ + dx_, (70 if paysage else 120) + dy_, 10 + 8 * al_
                    col_ = (255, 250, 220, int(230 * al_))
                    sd.polygon([(cx_, cy_ - rr * 2), (cx_ + rr * 0.5, cy_ - rr * 0.5), (cx_ + rr * 2, cy_),
                                (cx_ + rr * 0.5, cy_ + rr * 0.5), (cx_, cy_ + rr * 2), (cx_ - rr * 0.5, cy_ + rr * 0.5),
                                (cx_ - rr * 2, cy_), (cx_ - rr * 0.5, cy_ - rr * 0.5)], fill=col_)
            lay = Image.new("RGBA", glace.size, (0, 0, 0, 0))
            lay.paste(glace, (0, 0), m)
            img.alpha_composite(lay, (mx0 + ox, my0))
        ad = Actor(role.who, 540, y + (700 if paysage else 820), 12 if paysage else 15, False, state=st_dos, talk_with=None)
        ordres = sorted(extras, key=lambda o: o[0])
        textes = [(t - a, c.split(None, 1)[1].strip('"')) for (t, c) in ordres if c.lower().startswith("texte ")]
        sources = [(t - a, c.split(None, 1)[1].strip('"')) for (t, c) in ordres if c.lower().startswith("source ")]
        demos = [(t - a, c) for (t, c) in ordres] if demo else []
        cache = {}

        def ecran(img, u):
            W_, H_ = img.size
            for (tt, txt) in textes:
                if u >= tt:
                    t_ = cache.setdefault(("t", txt), explique.autocollant(explique.titre_img(txt, size=66), r=3, ombre=False))
                    pos_t = (int(W_ * 0.80 - t_.width / 2), int(H_ * 0.42)) if W_ > H_ else                         (int(W_ / 2 - t_.width / 2), int(H_ * 0.085))          # 16:9 : à droite du miroir
                    img.alpha_composite(explique._fade(t_, smooth((u - tt) / 0.35)), pos_t)
            for (tt, txt) in sources:
                if u >= tt:
                    t_ = cache.setdefault(("s", txt), pxv.tag_img("SRC " + txt.upper()))
                    img.alpha_composite(explique._fade(t_, smooth((u - tt) / 0.35)), (40, int(H_ * 0.125)))
            for j, (tt, c) in enumerate(demos):
                if tt <= u < tt + 1.8:
                    t_ = cache.setdefault(("d", c), explique.petit_texte("{" + c + "}", explique.JAUNE, (60, 40, 10), size=9, k=5))
                    aa = smooth((u - tt) / 0.2) * (1 - smooth((u - tt - 1.5) / 0.3))
                    rang = explique.empile([d[0] for d in demos], j)
                    img.alpha_composite(explique._fade(t_, aa), (int(W_ / 2 - t_.width / 2),
                                                                 int(H_ * 0.03) + rang * (t_.height + 6)))
        sh = Shot(a, b, s.bg, [ad], cam=(1.0, 1.04, (540, 960), (540, 940)), blur=3, fg=False,
                  anims=[miroir], ecran=[ecran], ambiance=s.amb,
                  sons=[(0.0, "tr_whoosh_doux", 0.05, None), (0.3, "sa_scintillement", 0.04, None)], **kw)
        sh.relief = False
        return sh

    def decoupe(s, coupes, **kw):
        """Le plan large coupé par d'autres plans [(t0, t1, plan)] (gros plans, champ / contre-champ, SMS…) :
        on revient au plan large entre eux, là où la scène en est."""
        plans, cur = [], s.t0
        for (a, b, sh) in sorted(coupes, key=lambda c: c[0]):
            if a > cur + 0.04:
                plans.append(s.plan(debut=cur, fin=a, **kw))
            sh.t0 = max(sh.t0, cur)
            plans.append(sh)
            cur = sh.t1
        if s.t1 > cur + 0.04:
            plans.append(s.plan(debut=cur, fin=s.t1, **kw))
        elif plans:
            plans[-1].t1 = s.t1
        return plans

    def plans_auto(s, D, max_suite=2, **kw):
        """Tout seul : plan large + champ / contre-champ sur les répliques qui se répondent + réactions de ceux qui
        écoutent. Renvoie la liste des plans de la scène."""
        s.reactions(D)
        band = kw.get("band", True)
        return s.decoupe([(a, b, s.plan_epaule(a, b, f, d, band=band)) for (a, b, f, d) in s.champs(D, max_suite)], **kw)

    def clignote(s, x, y, **kw):
        s.anims.append(clignote(x, y, **kw))
        return s

    def ecran(s, x0, y0, x1, y1, **kw):
        s.anims.append(ecran_tv(x0, y0, x1, y1, **kw))
        return s

    def lumiere(s, t, vers, duree=1.2):
        """À l'instant t, le décor se transforme lentement en un autre (ex. "cuisine" → "cuisine_nuit")."""
        s.fond2 = (vers, t, duree)
        return s

    # ---- son, caméra, textes
    def son(s, t, nom, gain=0.15, duree=None):
        s.sons.append((t, nom, gain, duree))
        return s

    def ambiance(s, nom, gain=0.5):
        s.amb = (nom, gain)
        return s

    def camera(s, cles):
        """Liste de clés [(t, zoom, (cx, cy)), …] : la caméra glisse doucement de l'une à l'autre."""
        s.cam = list(cles)
        return s

    def suit(s, D, gauche, droite, zoom=1.1, ecart=120, cy=1060):
        """La caméra dérive doucement vers celui qui parle (lignes du dialogue D)."""
        keys = [(0.0, zoom, (540, cy))]
        for L in D.lines:
            u = L["t0"] - s.t0
            if 0 <= u < s.dur():
                cx = 540 - ecart if L["who"] == gauche else (540 + ecart if L["who"] == droite else 540)
                keys.append((u + 0.9, zoom, (cx, cy)))
        s.cam = keys
        return s

    def notification(s, t0, t1, titre, texte, icone="bulle"):
        s.ecr.append(notification(t0, t1, titre, texte, icone))
        s.son(t0, "dv_notifications", 0.12, 1.0)
        return s

    def legende(s, titre, code=None, y=250):
        s.ecr.append(legende(titre, code, y))
        return s

    def texte(s, f):
        """Ajoute un dessin fixe à l'écran (ne bouge pas avec la caméra) : f(img, u)."""
        s.ecr.append(f)
        return s

    def plan(s, debut=None, fin=None, **kw):
        """Le plan entier, ou seulement un morceau [debut, fin] (temps absolus) : on peut couper une même scène
        par un gros plan ou un écran de SMS, puis y revenir — les persos continuent leur jeu là où ils en étaient."""
        a = s.t0 if debut is None else debut
        b = s.t1 if fin is None else fin
        off = a - s.t0
        order = sorted(range(len(s.roles)), key=lambda i: s.roles[i].y0)
        idx = {id(s.roles[i]): j for j, i in enumerate(order)}
        actors = [_decale_actor(s.roles[i].actor(), off) for i in order]
        effets = [(idx[id(r)], fn, t0 - off, t1 - off) for (r, fn, t0, t1) in s.fx if t1 - off > 0 and t0 - off < b - a]
        bubbles = [(idx[id(r)], fn, t0 - off, t1 - off, dx, dy) for (r, fn, t0, t1, dx, dy) in s.bulles
                   if t1 - off > 0 and t0 - off < b - a]
        cam = s.cam or (1.0, 1.05, (540, 1080), (540, 1060))
        if isinstance(cam, list):
            cam = [(u - off, z, c) for (u, z, c) in cam]
        dec = lambda fs: [(lambda img, u, f=f: f(img, u + off)) for f in fs] if off else list(fs)
        sons = [(t - off,) + tuple(x[1:]) for x in s.sons for t in [x[0]] if 0 <= t - off < b - a]
        fond2 = (s.fond2[0], s.fond2[1] - off, s.fond2[2]) if s.fond2 else None
        sh = Shot(a, b, s.bg, actors, cam=cam, anims=dec(s.anims), anims_avant=dec(s.avant), effets=effets,
                  bubbles=bubbles, fond2=fond2, sons=sons, ambiance=s.amb, overlays=dec(s.over),
                  tags=s.tags, blur=s.blur, ecran=dec(s.ecr), **kw)
        sh.lumieres = list(s.lumieres)
        return sh


def _decale_actor(a, off):
    if not off:
        return a
    st, pa, so = a.state, a.path, getattr(a, "sol", None)
    a.state = lambda u: st(u + off)
    if pa is not None:
        a.path = lambda u: pa(u + off)
    if so is not None:
        a.sol = lambda u: so(u + off)
    return a


_OBJ = {}


def _objet_img(nom, k):
    key = (nom, k)
    if key not in _OBJ:
        sp = Spr(24, 30)
        r = dict(cast.DEFAUT); r["couleurs_acc"] = None
        cast.objet(sp, nom, 8, 22, "tient", r)
        sp.outline()
        a = sp.a
        ys, xs = np.where(a[..., 3] > 0)
        crop = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1] if len(xs) else a
        _OBJ[key] = Image.fromarray(crop, "RGBA").resize((crop.shape[1] * k, crop.shape[0] * k), Image.NEAREST)
    return _OBJ[key]


_ACC = {}


_NUAGES = {}


def _nuage_img(r_, signe, sombre=(18, 12, 26), fond=(78, 64, 98), encre=(235, 225, 255), ol=(40, 26, 60), k=4, sale=False):
    """Un petit nuage (pensée noire, ou paquet d'écume sale : sale=True, points sombres et bulles) avec un mot dedans."""
    key = (r_, signe, sombre, fond, encre, ol, k, sale)
    if key not in _NUAGES:
        w_ = int(r_ * 2.4)
        im = Image.new("RGBA", (w_ + 16, int(r_ * 1.7) + 16), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx, cy = im.width / 2, im.height / 2 + 4
        for (dx, dy, rr) in ((-r_ * 0.6, 4, r_ * 0.55), (r_ * 0.6, 6, r_ * 0.5), (0, -r_ * 0.25, r_ * 0.7),
                             (-r_ * 0.2, r_ * 0.25, r_ * 0.55), (r_ * 0.3, r_ * 0.2, r_ * 0.55)):
            d.ellipse([cx + dx - rr - 5, cy + dy - rr - 5, cx + dx + rr + 5, cy + dy + rr + 5], fill=(*sombre, 255))
        for (dx, dy, rr) in ((-r_ * 0.6, 4, r_ * 0.55), (r_ * 0.6, 6, r_ * 0.5), (0, -r_ * 0.25, r_ * 0.7),
                             (-r_ * 0.2, r_ * 0.25, r_ * 0.55), (r_ * 0.3, r_ * 0.2, r_ * 0.55)):
            d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=(*fond, 255))
        if sale:                                                    # écume sale : bulles claires + taches
            for (dx, dy, rr, col) in ((-r_ * 0.75, -r_ * 0.05, r_ * 0.16, (236, 234, 238)), (r_ * 0.55, -r_ * 0.3, r_ * 0.13, (236, 234, 238)),
                                      (-r_ * 0.15, -r_ * 0.62, r_ * 0.12, (236, 234, 238)), (r_ * 0.8, r_ * 0.3, r_ * 0.1, (110, 100, 92)),
                                      (-r_ * 0.55, r_ * 0.45, r_ * 0.11, (110, 100, 92)), (r_ * 0.15, r_ * 0.55, r_ * 0.09, (110, 100, 92))):
                d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=(*col, 255))
        if signe:
            g = pxv.pixel_text(signe, encre, ol, size=10, k=k)
            im.alpha_composite(g, (int(cx - g.width / 2), int(cy - g.height / 2)))
        _NUAGES[key] = im
    return _NUAGES[key]


def _accessoire_img(nom, k):
    """Objets posés par terre, dessinés en pixels comme le reste (même taille de pixel que les persos)."""
    key = (nom, k)
    if key in _ACC:
        return _ACC[key]
    if nom == "trottinette":
        a = Image.new("RGBA", (34, 34), (0, 0, 0, 0))
        d = ImageDraw.Draw(a)
        d.rectangle([4, 27, 28, 29], fill=(40, 40, 50, 255))                 # plateau
        d.rectangle([5, 27, 27, 27], fill=(80, 140, 220, 255))
        d.line([(27, 28), (25, 4)], fill=(60, 60, 70, 255), width=2)          # colonne
        d.rectangle([20, 3, 31, 4], fill=(30, 30, 36, 255))                   # guidon
        d.rectangle([20, 3, 22, 4], fill=(230, 60, 60, 255))
        for cx in (6, 27):                                                    # roues
            d.ellipse([cx - 3, 28, cx + 3, 33], fill=(26, 26, 30, 255))
            d.point((cx, 30), fill=(170, 170, 180, 255))
    elif nom == "branche":                                                    # branche d'épines : grosse et bien visible
        a = Image.new("RGBA", (62, 22), (0, 0, 0, 0))
        d = ImageDraw.Draw(a)
        d.line([(2, 18), (59, 11)], fill=(110, 76, 44, 255), width=3)
        d.line([(3, 19), (58, 13)], fill=(84, 56, 32, 255), width=1)
        for (x0, y0, x1, y1) in ((12, 17, 18, 6), (26, 15, 33, 4), (40, 13, 47, 3), (22, 16, 17, 21), (50, 12, 56, 5)):
            d.line([(x0, y0), (x1, y1)], fill=(110, 76, 44, 255), width=2)
        for (x_, y_) in ((7, 15), (11, 12), (15, 9), (20, 14), (24, 9), (29, 12), (31, 6), (36, 11), (39, 7),
                         (44, 9), (46, 5), (51, 10), (54, 7), (57, 9), (19, 19), (9, 19), (34, 16), (48, 14)):
            d.point((x_, y_ - 1), fill=(240, 232, 214, 255))                  # épines (pointes claires)
            d.point((x_, y_ - 2), fill=(240, 232, 214, 255))
        for (x_, y_) in ((18, 5), (33, 3), (47, 2), (56, 4)):
            d.rectangle([x_ - 1, y_ - 1, x_ + 1, y_ + 1], fill=(86, 148, 64, 255))
    elif nom == "rocher":                                                     # gros rocher sombre (les grands péchés)
        a = Image.new("RGBA", (26, 16), (0, 0, 0, 0))
        d = ImageDraw.Draw(a)
        d.ellipse([1, 4, 25, 15], fill=(70, 66, 76, 255))
        d.ellipse([4, 1, 17, 12], fill=(84, 80, 90, 255))
        d.ellipse([12, 3, 23, 13], fill=(66, 62, 72, 255))
        d.ellipse([6, 3, 12, 7], fill=(110, 106, 116, 255))
        d.point((9, 11), fill=(44, 40, 50, 255)); d.point((18, 9), fill=(44, 40, 50, 255))
    elif nom == "caillou":
        a = Image.new("RGBA", (16, 10), (0, 0, 0, 0))
        d = ImageDraw.Draw(a)
        d.ellipse([1, 2, 15, 9], fill=(130, 126, 120, 255))
        d.ellipse([3, 3, 9, 6], fill=(165, 160, 152, 255))
    else:                                                                     # carton
        a = Image.new("RGBA", (22, 16), (0, 0, 0, 0))
        d = ImageDraw.Draw(a)
        d.rectangle([1, 3, 20, 15], fill=(196, 150, 96, 255))
        d.rectangle([1, 3, 20, 5], fill=(170, 124, 74, 255))
        d.line([(10, 3), (10, 15)], fill=(150, 108, 64, 255))
    arr = np.array(a)
    m = arr[..., 3] > 0
    e = m.copy()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        e |= np.roll(np.roll(m, dy, 0), dx, 1)
    out = np.zeros_like(arr)
    out[e] = (22, 18, 30, 255)
    out[m] = arr[m]
    im = Image.fromarray(out, "RGBA")
    im = im.resize((im.width * k, im.height * k), Image.NEAREST)
    _ACC[key] = im
    return im


# =================================================================== TEXTES À L'ÉCRAN (cartons, notifications, légendes)
def _pix(txt, col, ol, size=10, k=5, ol2=(14, 10, 18)):
    return pxv.pixel_text(txt, col, ol, size=size, k=k, ol2=ol2)


def legende(titre, code=None, y=250):
    """Légende de démonstration (titre + nom de la commande), en haut de l'écran (ou y=1780 : en bas)."""
    tailles = {}

    def textes(largeur):
        """Titre et code réduits si besoin pour tenir dans l'image (jamais coupés)."""
        if largeur not in tailles:
            for ka, kb in ((5, 4), (4, 3), (3, 3), (3, 2)):
                a = _pix(titre, (255, 255, 255), (30, 30, 60), size=10, k=ka)
                b = _pix(code, (255, 220, 110), (60, 40, 10), size=8, k=kb) if code else None
                if max(a.width, b.width if b else 0) + 60 <= largeur - 40:
                    break
            tailles[largeur] = (a, b)
        return tailles[largeur]

    def f(img, u):
        a, b = textes(img.width)
        al = smooth(u / 0.3)
        w = max(a.width, b.width if b else 0) + 60
        h = a.height + (b.height + 6 if b else 0) + 40
        box = Image.new("RGBA", (w, h), (16, 14, 26, int(205 * al)))
        d = ImageDraw.Draw(box)
        d.rectangle([0, 0, 7, h], fill=(120, 230, 255, int(255 * al)))
        box.alpha_composite(_fade(a, al), (34, 16))
        if b:
            box.alpha_composite(_fade(b, al), (34, 22 + a.height))
        img.alpha_composite(box, (int(img.width / 2 - w / 2), y))
    return f


def notification(t0, t1, titre, texte, icone="bulle"):
    """Bandeau de notification de téléphone qui descend doucement en haut de l'image."""
    def f(img, u):
        if not (t0 <= u < t1):
            return
        v = u - t0
        e = smooth(v / 0.45) * (1 - smooth((v - (t1 - t0 - 0.45)) / 0.45))
        c = Px(250, 50, alpha=True)
        card = c.mask_rrect(0, 0, 249, 49, 8)
        c.fill(card, (248, 248, 252))
        c.outline(card, (60, 60, 80))
        ic = objets.icone(icone).img(2)
        c.paste(ic, 8, 9)
        c.text((50, 8), titre, (30, 30, 40), size=10)
        c.text((50, 26), texte[:34], (80, 80, 96), size=9, font="C:/Windows/Fonts/tahoma.ttf")
        im = c.img(4, rgba=True)
        y = int(-im.height + (260 + im.height) * e)
        img.alpha_composite(_fade(im, e), (int(img.width / 2 - im.width / 2), y))
    return f


def carton(t0, t1, texte, sous=None, fond="noir", couleur=(255, 255, 255), couleur_sous=(255, 214, 110)):
    """Carton plein écran (« LE LENDEMAIN… », « 23 H 47 ») : texte qui apparaît et disparaît en fondu."""
    a = pxv.big_title([(texte, couleur)], size=96)
    b = _pix(sous, couleur_sous, (40, 30, 10), size=10, k=5) if sous else None
    d = t1 - t0

    def f(img, u):
        al = _env(u, d, 0.4, 0.4)
        img.alpha_composite(_fade(a, al), (int(img.width / 2 - a.width / 2), int(img.height * 0.427)))
        if b:
            img.alpha_composite(_fade(b, al * smooth((u - 0.3) / 0.4)), (int(img.width / 2 - b.width / 2), int(img.height * 0.52)))
    return Shot(t0, t1, fond, [], cam=(1.0, 1.03, (540, 960), (540, 960)), band=False, ecran=[f])


# =================================================================== ÉCRAN DE TÉLÉPHONE (SMS)
F_B = "C:/Windows/Fonts/tahomabd.ttf"
F_R = "C:/Windows/Fonts/tahoma.ttf"
F9 = ImageFont.truetype(F_R, 9)


def _largeur(txt):
    """Largeur réelle du texte en pixels (dessiné sans anticrénelage, comme dans la bulle)."""
    im = Image.new("L", (12 * len(txt) + 20, 24), 0)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    d.text((0, 0), txt, font=F9, fill=255)
    bb = im.getbbox()
    return bb[2] if bb else 0


def _wrap_px(txt, font, maxw):
    words, lines, cur = txt.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if cur and _largeur(t) > maxw:
            lines.append(cur); cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def sms(t0, t1, contact, messages, bg="chambre_ado", heure="23:47", avatar=None, theme=None):
    """Plan : le téléphone en grand, la conversation s'écrit. messages = [(t, "lui" | "moi", "texte"), …]
    (t dans le plan). « lui » : l'indicateur « … » apparaît 0,8 s avant, + son de notification discret."""
    d = t1 - t0
    face = avatar or contact
    av = None
    try:
        a = duo.portrait(face) if face in ("P", "G") or cast.has(face) else None
        if a is not None:
            av = Image.fromarray(a, "RGBA")
    except Exception:
        av = None
    lay = []
    for (t, side, txt) in messages:
        lines = _wrap_px(txt, F_R, 92)
        lay.append((t, side, lines))

    def phone(img, u):
        c = Px(270, 480, alpha=True)
        body = c.mask_rrect(46, 40, 224, 446, 16)
        c.fill(body, (24, 24, 30))
        c.outline(body, (8, 8, 12))
        scr = c.mask_rrect(54, 54, 216, 432, 8)
        c.fill(scr, (236, 238, 244))
        c.fill(c.mask_rect(54, 54, 216, 92) & scr, (250, 250, 252))
        c.fill(c.mask_rect(54, 91, 216, 92), (210, 212, 220))
        c.fill(c.mask_rrect(116, 46, 154, 50, 2), (40, 40, 48))
        c.text((62, 57), heure, (40, 40, 50), size=8, font=F_B)
        c.fill(c.mask_rect(196, 59, 208, 64), (60, 60, 70)); c.fill(c.mask_rect(197, 60, 200, 63), (220, 60, 60))
        if av is not None:
            avi = av.resize((av.width, av.height), Image.NEAREST)
            m = c.mask_ell(76, 78, 9, 9)
            c.fill(m, (200, 204, 214))
            c.paste(avi.crop((2, 0, min(avi.width, 26), min(avi.height, 22))).resize((18, 16), Image.NEAREST), 67, 70)
        c.text((92, 72), contact, (30, 30, 40), size=9, font=F_B)
        c.text((92, 82), "en ligne", (90, 170, 90), size=7, font=F_R)
        # messages visibles (les derniers en bas, la liste remonte doucement)
        items = [(t, side, lines) for (t, side, lines) in lay if u >= t]
        typing = [(t, side) for (t, side, _) in lay if side == "lui" and t - 0.8 <= u < t]
        hs = [len(lines) * 11 + 8 for (_, _, lines) in items]
        bottom = 422 - (16 if typing else 0)
        total = sum(hs) + 6 * len(hs)
        y = bottom - total
        for (t, side, lines), h in zip(items, hs):
            e = smooth((u - t) / 0.25)
            w = max(_largeur(l) for l in lines) + 13
            x0 = 60 if side == "lui" else 210 - w
            yy = y + (1 - e) * 6
            if yy > 96:
                bub = c.mask_rrect(x0, yy, x0 + w, yy + h, 6)
                col = (255, 255, 255) if side == "lui" else (70, 150, 250)
                c.fill(bub, col)
                c.outline(bub, (200, 202, 212) if side == "lui" else (50, 110, 200))
                for i, l in enumerate(lines):
                    c.text((x0 + 6, yy + 3 + i * 11), l, (30, 30, 40) if side == "lui" else (255, 255, 255), size=9, font=F_R)
            y += h + 6
        if typing:
            bub = c.mask_rrect(60, 404, 92, 418, 6)
            c.fill(bub, (255, 255, 255)); c.outline(bub, (200, 202, 212))
            for i in range(3):
                on = int(u * 4 + i) % 3 == 0
                c.fill(c.mask_ell(68 + i * 8, 411, 2, 2), (90, 90, 100) if on else (180, 180, 190))
        im = c.img(4, rgba=True)
        if img.height != im.height:                                     # format 16:9 : le téléphone est réduit et centré
            sc_ = img.height / im.height
            im = im.resize((int(im.width * sc_), img.height), Image.NEAREST)
        e = smooth(u / 0.35) * (1 - smooth((u - (d - 0.3)) / 0.3))
        img.alpha_composite(_fade(im, e), (int((img.width - im.width) / 2), int(40 * (1 - e))))
    sons = [(t, "dv_notifications", 0.12, 1.0) for (t, side, _) in messages if side == "lui"]
    sons += [(t, "dv_clic", 0.08, None) for (t, side, _) in messages if side == "moi"]
    return Shot(t0, t1, bg, [], cam=(1.04, 1.08, (540, 960), (540, 940)), blur=6, fg=False, ecran=[phone], sons=sons)


# =================================================================== PLANS TOUT FAITS
def epaule(t0, t1, bg, dos, face, k_dos=15, k_face=8, st_dos=None, st_face=None, cote="gauche"):
    """Plan par-dessus l'épaule : `dos` de dos en grand au premier plan, `face` en face plus loin."""
    sp = lieux.SPOTS.get(bg, dict(gauche=(300, 1340), droite=(780, 1340), k=7, opts={}))
    y = sp["gauche"][1]
    xd, xf = (190, 720) if cote == "gauche" else (890, 360)
    a_face = Actor(face, xf, y + 40, k_face, cote == "gauche", state=lambda u, s=dict(st_face or {}): dict(s), breathe=3)
    a_dos = Actor(dos, xd, y + 860, k_dos, False, state=lambda u, s=dict(st_dos or {}): dict(s, back=True), talk_with=None)
    return Shot(t0, t1, bg, [a_face, a_dos], cam=(1.0, 1.04, (540, 1000), (540 + (30 if cote == "gauche" else -30), 980)), blur=2)


def etablissement(t0, t1, bg, cible=(540, 700), zoom=1.28, **kw):
    """Plan d'ensemble : la caméra s'approche lentement d'un point (une fenêtre allumée…)."""
    sc = Scene(t0, t1, bg)
    sc.camera([(0.0, 1.0, (540, 960)), (t1 - t0, zoom, cible)])
    return sc
