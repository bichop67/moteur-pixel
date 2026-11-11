# DÉCORS DU FILM « MOUSSA » — parties 22 à 24 — 16:9, toile x = -105 … 375, y = 0 … 480 ; pieds à y = 330.
#   confluent (+ _soir)         le confluent des deux mers : deux eaux de couleurs différentes qui se rejoignent ; un grand
#                               rocher sur la plage (le poisson y reprend vie : anim_poisson)
#   village_mur                 un village de maisons de terre aux portes fermées ; au bout de la rue, la place du mur
#                               penché (dessiné par anim_mur : il se redresse de bas en haut)
#   demeure_qaroun              la demeure de Qaroun : salle immense, colonnes, coffres ouverts débordant d'or
#   palais_qaroun (+ _vide)     la demeure vue du dehors, sur une place ; _vide : le terrain nu, fendu (après)
#                               (anim_engloutit : la demeure s'enfonce dans la terre, poussière, puis plus rien)
#   dune_rouge                  la nuit, au bord d'une route, une dune de sable rouge sous la lune (anim_lueur : la
#                               lumière douce qui monte de la tombe — rien d'autre n'est montré)
#   cieux                       le ciel immense du Voyage nocturne : étoiles, voiles de lumière ; anim_echelle (l'échelle
#                               de lumière)
#   montagne_sinai_soir         la montagne (décor de la partie 17) au soleil couchant
# Tableaux (dessinés à l'écran, par-dessus le plan, pour les explications) : anim_tableau(nom, t0, duree) — un morceau
# de décor net (pixels x4) avec des persos et des objets, dans un cadre, qui apparaît puis s'efface en douceur.
import math

import numpy as np

import lieux
import egypte
from lieux import dk, lt, mix, R, palmier, relief
from egypte import _Px, _ciel, CIELS, _colonne_lotus
from decors_film import _T, _briques, _porte, _fenetre, _jarre, BRIQUE
from decors_film2 import _clip, _assombrit, EAU


def _smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


# ================================================================ le confluent des deux mers (18:60-64)
CONFLUENT_SEAM = (118, 0.42)                     # la ligne où les deux mers se rejoignent : x = 118 + 0.42 * (y - 196)


def confluent(heure="jour"):
    """Le confluent des deux mers : une eau bleu profond à gauche, une eau vert turquoise à droite, qui se rejoignent
    le long d'une ligne d'écume ; au loin la côte ; au premier plan une plage de sable et de galets ; à droite, le grand
    rocher où ils se sont reposés. Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    nuit = heure == "nuit"
    sky = _ciel(c, heure, 196, dict(aube=(300, 170), jour=(250, 52), soir=(-30, 170), nuit=(280, 60))[heure], seed=601)
    snap = c.a.copy()
    rr = R(602)
    loin = mix(T((150, 128, 110)), CIELS[heure][1], 0.5)                       # la côte, au loin
    c.fill(c.mask_poly([(-105, 197), (-105, 178), (-74, 170), (-40, 178), (-6, 171), (26, 184), (58, 197)]), loin)
    c.fill(c.mask_poly([(250, 197), (282, 186), (318, 182), (350, 188), (375, 184), (375, 197)]), lt(loin, 0.08))
    x0, pente = CONFLUENT_SEAM
    mer = c.mask_rect(-105, 196, 375, 304)
    gauche = mer & (c.xx < x0 + pente * (c.yy - 196))
    droite = mer & ~gauche
    c.vgrad(gauche, 196, 304, T((66, 104, 170)), T((30, 58, 116)), steps=7)       # la mer profonde
    c.vgrad(droite, 196, 304, T((104, 186, 178)), T((52, 136, 136)), steps=7)     # l'autre mer, turquoise
    for y in range(197, 304):                                                  # la rencontre : une ligne d'écume
        x = x0 + pente * (y - 196)
        c.fill(c.mask_rect(int(x) - 1, y, int(x), y), lt(T((150, 200, 214)), 0.25))
    for _ in range(300):                                                       # reflets
        x, y = rr.randint(-100, 372), rr.randint(200, 300)
        g_ = x < x0 + pente * (y - 196)
        col = lt(T((66, 104, 170)), 0.35) if g_ else lt(T((104, 186, 178)), 0.3)
        w_ = rr.randint(2, 5)
        c.fill(c.mask_rect(x, y, x + w_, y), col)
    sable = T((214, 188, 142))
    plage = c.yy >= 298 + 3 * np.sin(c.xx / 9.0 + 0.6)
    c.vgrad(plage, 294, 480, lt(sable, 0.06), dk(sable, 0.72), steps=6)
    bord = plage & ~np.roll(plage, 1, axis=0)
    c.fill(bord, (238, 242, 238) if not nuit else (150, 160, 180))             # l'écume au bord de l'eau
    c.fill(np.roll(bord, 1, axis=0) & plage, lt(sable, 0.2))
    for _ in range(90):                                                        # galets
        x, y = rr.randint(-100, 370), rr.randint(306, 470)
        g = T(rr.choice([(150, 140, 128), (120, 112, 104), (176, 164, 146)]))
        c.fill(c.mask_ell(x, y, rr.uniform(1.2, 2.8), rr.uniform(0.8, 1.6)), g)
    roc = c.mask_poly([(206, 330), (212, 270), (226, 244), (250, 230), (276, 236), (294, 258), (302, 296), (300, 330)])
    c.vgrad(roc, 230, 330, T((156, 144, 132)), T((96, 88, 82)), steps=5)       # le grand rocher
    for (p_, k_) in (([(226, 250), (250, 236), (262, 262), (238, 280)], 0.25), ([(270, 250), (292, 266), (286, 300)], 0.35),
                     ([(214, 292), (240, 300), (232, 324), (210, 322)], 0.3)):
        c.tint(roc & c.mask_poly(p_), dk(T((156, 144, 132)), 0.6), k_)
    c.fill(roc & ~np.roll(roc, 1, axis=0), lt(T((156, 144, 132)), 0.25))
    c.outline(roc, (54, 44, 40))
    c.fill(c.mask_ell(254, 331, 52, 3), dk(sable, 0.6))
    if nuit:
        c.tint(c.mask_rect(-105, 0, 375, 480), (10, 10, 36), 0.25)
    return relief(c, snap, sky), None


def anim_poisson(t_debut=0.0, x0=196, y0=316, x1=150, y1=288, fin=(30, 214), duree_trace=3.6):
    """Le poisson saute du panier (x0, y0), retombe dans la mer (x1, y1) et file vers le large en laissant derrière lui un
    sillage clair, comme un tunnel dans l'eau, qui reste (18:61, 63 ; Boukhari 3401). Doux, sans éclair."""
    from PIL import Image, ImageDraw

    def f(img, u):
        v = u - t_debut
        if v < 0:
            return
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        if v < 0.9:                                                            # le saut
            k = v / 0.9
            x = x0 + (x1 - x0) * k
            y = y0 + (y1 - y0) * k - 16 * math.sin(math.pi * k)
            ang = math.atan2((y1 - y0) - 16 * math.pi * math.cos(math.pi * k), (x1 - x0))
            dx, dy = math.cos(ang) * 3, math.sin(ang) * 3
            d.line([(x - dx + 105, y - dy), (x + dx + 105, y + dy)], fill=(214, 224, 232, 255), width=2)
            d.polygon([(x - dx * 1.6 + 105, y - dy * 1.6 - 1.5), (x - dx * 1.6 + 105, y - dy * 1.6 + 1.5),
                       (x - dx + 105, y - dy)], fill=(170, 186, 200, 255))
        if 0.85 <= v < 1.8:                                                    # l'éclaboussure
            k = (v - 0.85) / 0.95
            for i in range(8):
                a_ = math.pi * (0.1 + 0.8 * i / 7)
                d.point((x1 + 105 + math.cos(a_) * 6 * k, y1 - math.sin(a_) * 5 * k + 4 * k * k),
                        fill=(240, 248, 255, int(230 * (1 - k))))
        if v >= 0.9:                                                           # le sillage : un tunnel clair dans l'eau
            k = min(1.0, (v - 0.9) / duree_trace)
            n = 40
            pts = []
            for i in range(int(n * k) + 1):
                t_ = i / n
                pts.append((x1 + (fin[0] - x1) * t_ + 105 + 4 * math.sin(t_ * 6), y1 + (fin[1] - y1) * t_ - 6 * math.sin(math.pi * t_)))
            if len(pts) > 1:
                d.line(pts, fill=(196, 230, 246, 150), width=3)
                d.line(pts, fill=(246, 252, 255, 200), width=1)
                hx, hy = pts[-1]
                if k < 1:
                    d.ellipse([hx - 2, hy - 1, hx + 2, hy + 1], fill=(40, 60, 80, 200))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ le village au mur penché (18:77)
def village_mur(heure="jour"):
    """Un village de maisons de terre aux toits plats, portes de bois fermées, petites fenêtres, quelques palmiers ;
    la rue de terre battue ; à droite (x 262 … 350), un espace libre devant un fond de maisons basses : c'est là que se
    tient le mur penché (anim_mur). Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    nuit = heure == "nuit"
    sky = _ciel(c, heure, 318, dict(aube=(300, 170), jour=(60, 40), soir=(-30, 170), nuit=(300, 60))[heure], seed=611)
    snap = c.a.copy()
    rr = R(612)
    for (x, h_, s_) in ((-60, 70, 1), (150, 64, 2), (330, 60, 3)):
        palmier(c, x, 240, h=h_, lean=10 * (1 if s_ % 2 else -1), seed=610 + s_)
    terre = T((206, 170, 124))
    murs = [(-105, -20, 236, 0), (-18, 70, 222, 1), (72, 160, 230, 2), (162, 256, 218, 3)]
    for (xa, xb, yt, i) in murs:                                               # les maisons, porte fermée
        m = c.mask_rect(xa, yt, xb, 318)
        col = T(mix((206, 170, 124), (180, 140, 100), 0.3 * (i % 2)))
        c.fill(m, col)
        _briques(c, m, col, pas_y=6, pas_x=10, seed=620 + i)
        c.fill(c.mask_rect(xa, yt - 3, xb, yt), lt(col, 0.12))                 # le rebord du toit
        c.fill(c.mask_rect(xa, yt, xb, yt + 1), dk(col, 0.7))
        xm = (xa + xb) // 2
        _porte(c, xm - 9, xm + 9, 284, 318, nuit, bois=T((98, 64, 40)), ouverte=False)
        for xf in (xa + 10, xb - 18):
            if xb - xa > 60:
                _fenetre(c, xf, yt + 16, 8, 8, nuit, lampe=False)
        c.outline(m, (60, 44, 34))
    c.fill(c.mask_rect(257, 262, 375, 318), T((190, 156, 116)))               # au fond à droite : maisons basses
    _briques(c, c.mask_rect(257, 262, 375, 318), T((190, 156, 116)), seed=631)
    c.fill(c.mask_rect(257, 259, 375, 262), lt(T((190, 156, 116)), 0.12))
    rue = c.mask_rect(-105, 318, 375, 480)
    c.vgrad(rue, 318, 480, lt(terre, 0.04), dk(terre, 0.7), steps=6)
    for _ in range(70):
        x, y = rr.randint(-100, 370), rr.randint(322, 470)
        c.fill(c.mask_ell(x, y, 1.5, 0.8), dk(terre, 0.85))
    for (x, y) in ((40, 318), (120, 318), (200, 318)):
        _jarre(c, x, y, T((170, 110, 70)))
    if nuit:
        c.tint(c.mask_rect(-105, 0, 375, 480), (10, 10, 36), 0.25)
    return relief(c, snap, sky), None


def anim_mur(cles, x0=272, x1=346, y_base=330, h=78, angle=12.0):
    """Le mur sur le point de s'écrouler : un vieux mur de briques penché (bords droits et inclinés, fissures, briques
    tombées) ; {mur redresse} : il se redresse en 3 s, de bas en haut (les rangées du bas d'abord) ; puis droit."""
    from PIL import Image, ImageDraw
    pas = 5
    lignes = list(range(0, h, pas))
    brique, joint, clair, ombre = (184, 146, 104), (120, 90, 64), (210, 176, 132), (150, 116, 82)

    def f(img, u):
        t_r = next((t_ for (t_, quoi) in sorted(cles) if quoi == "redresse"), None)

        def ang(frac):                                                          # l'angle à cette hauteur du mur
            if t_r is None or u < t_r:
                return angle
            return angle * (1 - _smooth((u - t_r) / 3.0 * 1.6 - frac * 0.6))

        dec_cache = {}

        def dec(dy):                                                            # décalage horizontal à la hauteur dy
            if dy not in dec_cache:                                             # (somme des pentes des rangées dessous)
                tot, y_ = 0.0, 0
                while y_ < dy:
                    st = min(pas, dy - y_)
                    tot += -math.tan(math.radians(ang(y_ / h))) * st
                    y_ += st
                dec_cache[dy] = tot
            return dec_cache[dy]

        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        X = 105
        for j, dy in enumerate(lignes):
            ya, yb = y_base - dy - pas, y_base - dy                             # haut et bas de la rangée
            da, db = dec(dy + pas), dec(dy)
            poly = [(x0 + db + X, yb), (x1 + db + X, yb), (x1 + da + X, ya), (x0 + da + X, ya)]
            d.polygon(poly, fill=(*brique, 255))
            d.polygon([(x1 - 6 + db + X, yb), (x1 + db + X, yb), (x1 + da + X, ya), (x1 - 6 + da + X, ya)], fill=(*ombre, 255))
            off = 0 if j % 2 else 5
            for xx in range(x0 + off, x1, 10):
                d.line([(xx + db + X, yb), (xx + da + X, ya)], fill=(*joint, 255))
            d.line([(x0 + da + X, ya), (x1 + da + X, ya)], fill=(*clair, 255))
        dt = dec(lignes[-1] + pas)
        d.line([(x0 + X, y_base), (x0 + dt + X, y_base - lignes[-1] - pas)], fill=(60, 44, 34, 255))
        d.line([(x1 + X, y_base), (x1 + dt + X, y_base - lignes[-1] - pas)], fill=(60, 44, 34, 255))
        d.line([(x0 + dt + X, y_base - lignes[-1] - pas), (x1 + dt + X, y_base - lignes[-1] - pas)], fill=(60, 44, 34, 255))
        if t_r is None or u < t_r + 1.0:                                        # fissures et briques tombées (avant)
            al = 255 if t_r is None or u < t_r else int(255 * max(0.0, 1 - (u - t_r)))
            for (fx, fdy, gx, gdy) in ((300, 30, 308, 46), (308, 46, 303, 60), (322, 12, 330, 28)):
                d.line([(fx + dec(fdy) + X, y_base - fdy), (gx + dec(gdy) + X, y_base - gdy)], fill=(70, 50, 36, al))
            for (bx, by) in ((352, 328), (361, 329), (262, 329)):
                d.rectangle([bx + X, by - 3, bx + 6 + X, by], fill=(*brique, al), outline=(60, 44, 34, al))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ Qaroun : la demeure, l'or ; la terre l'engloutit (28:76-82)
OR = (236, 192, 72)


def _tas_or(c, x, y, w, h, T, rr):
    m = c.mask_poly([(x - w, y), (x - w * 0.6, y - h * 0.7), (x, y - h), (x + w * 0.6, y - h * 0.7), (x + w, y)])
    c.vgrad(m, y - h, y, lt(T(OR), 0.2), dk(T(OR), 0.75), steps=4)
    for _ in range(int(w * h / 6)):
        px_, py_ = rr.randint(int(x - w * 0.8), int(x + w * 0.8)), rr.randint(int(y - h * 0.8), int(y))
        if m[py_, px_ + 105]:
            c.fill(c.mask_rect(px_, py_, px_, py_), lt(T(OR), 0.45))
    c.outline(m, (110, 76, 30))


def _coffre_or(c, x, y, w, T, rr, ouvert=True):
    """Un coffre de bois cerclé de fer, ouvert, débordant d'or."""
    bois = T((120, 74, 44))
    corps = c.mask_rect(x - w, y - 14, x + w, y)
    c.fill(corps, bois)
    c.fill(c.mask_rect(x - w, y - 14, x + w, y - 13), lt(bois, 0.2))
    for xx in (x - w + 3, x + w - 4):
        c.fill(c.mask_rect(xx, y - 14, xx + 1, y), T((90, 90, 96)))
    c.fill(c.mask_rect(x - 2, y - 11, x + 1, y - 8), T(OR))
    if ouvert:
        c.fill(c.mask_poly([(x - w, y - 14), (x - w + 2, y - 26), (x + w + 2, y - 26), (x + w, y - 14)]), dk(bois, 0.8))
        _tas_or(c, x, y - 13, w - 1, 7, T, rr)
    c.outline(corps, (50, 32, 20))


def demeure_qaroun(heure="jour"):
    """La demeure de Qaroun : une salle immense aux colonnes peintes, des tentures pourpres, des lampes, et partout des
    coffres ouverts débordant d'or, des tas de pièces, des vases d'or. Pieds y = 330."""
    c = _Px()
    T = _T("jour")
    rr = R(641)
    mur = T((214, 184, 140))
    c.vgrad(c.mask_rect(-105, 0, 375, 300), 0, 300, lt(mur, 0.08), dk(mur, 0.82), steps=7)
    for x in range(-100, 376, 34):                                             # frise et panneaux
        c.fill(c.mask_rect(x, 120, x + 28, 250), dk(mur, 0.93))
        c.fill(c.mask_rect(x + 2, 122, x + 26, 124), T(OR))
    c.fill(c.mask_rect(-105, 96, 375, 104), T((120, 40, 70)))                  # bande pourpre
    c.fill(c.mask_rect(-105, 100, 375, 101), T(OR))
    for x in (-70, 40, 150, 260, 362):                                        # tentures pourpres
        m = c.mask_poly([(x - 14, 104), (x + 14, 104), (x + 10, 230), (x - 10, 230)])
        c.vgrad(m, 104, 230, T((150, 40, 80)), T((90, 20, 50)), steps=5)
        c.fill(c.mask_rect(x - 14, 104, x + 14, 106), T(OR))
    for x in (-20, 95, 205, 318):
        _colonne_lotus(c, x, 110, 300, 16, T((222, 206, 170)))
    sol = c.mask_rect(-105, 300, 375, 480)
    c.vgrad(sol, 300, 480, T((176, 140, 96)), T((112, 84, 56)), steps=6)
    for y in range(306, 480, 12):
        c.fill(c.mask_rect(-105, y, 375, y), dk(T((176, 140, 96)), 0.9))
    for (x, y, w) in ((-80, 300, 16), (-40, 304, 14), (60, 298, 15), (130, 302, 16), (240, 300, 14), (300, 304, 16),
                      (350, 298, 12)):
        _coffre_or(c, x, y, w, T, rr)
    for (x, y, w, h) in ((10, 312, 14, 8), (180, 310, 18, 9), (270, 314, 12, 6), (-100, 314, 10, 5)):
        _tas_or(c, x, y, w, h, T, rr)
    for (x, y) in ((-58, 300), (108, 298), (220, 300), (330, 300)):             # vases d'or
        _jarre(c, x, y, T(OR), h=9)
    for x in (-50, 120, 290):                                                  # lampes
        c.fill(c.mask_ell(x, 70, 5, 3), T(OR))
        c.glow(x, 72, 40, (255, 200, 120), 0.35)
    return c, None


def _maison_qaroun_sprite():
    """La demeure de Qaroun vue du dehors (image RGBA, pixels du dessin) : une grande façade à colonnes, coupoles dorées,
    portail, frise d'or ; 210 x 132, le bas = le sol."""
    from PIL import Image
    c = _Px()
    c.a[:] = 0
    W_, H_ = 210, 132
    T = _T("jour")
    m_all = np.zeros(c.a.shape[:2], bool)
    ox, oy = -100, 160                                                          # dessinée dans la toile, puis découpée
    pierre = T((226, 206, 166))
    corps = c.mask_rect(ox + 10, oy + 40, ox + 200, oy + 132)
    c.fill(corps, pierre)
    _briques(c, corps, pierre, pas_y=8, pas_x=14, seed=651)
    m_all |= corps
    for (cx_, r_) in ((ox + 55, 26), (ox + 105, 34), (ox + 155, 26)):         # coupoles dorées
        dome = c.mask_ell(cx_, oy + 40, r_, r_ * 0.9) & c.mask_rect(ox, oy - 40, ox + 210, oy + 40)
        c.vgrad(dome, oy + 40 - r_, oy + 40, lt(T(OR), 0.25), dk(T(OR), 0.8), steps=5)
        c.outline(dome, (110, 76, 30))
        c.fill(c.mask_rect(cx_, oy + 40 - r_ - 8, cx_, oy + 40 - r_), T(OR))
        m_all |= dome | c.mask_rect(cx_, oy + 40 - r_ - 8, cx_, oy + 40 - r_)
    for x in range(ox + 20, ox + 200, 22):                                     # colonnes
        col_ = c.mask_rect(x, oy + 58, x + 6, oy + 132)
        c.fill(col_, lt(pierre, 0.12))
        c.fill(c.mask_rect(x, oy + 58, x + 6, oy + 60), T(OR))
    c.fill(c.mask_rect(ox + 10, oy + 44, ox + 200, oy + 50), T((130, 40, 70)))  # frise pourpre et or
    c.fill(c.mask_rect(ox + 10, oy + 47, ox + 200, oy + 47), T(OR))
    portail = c.mask_arch(ox + 92, ox + 118, oy + 86, oy + 132)
    c.fill(portail, T((110, 70, 40)))
    c.fill(c.mask_rect(ox + 104, oy + 90, ox + 105, oy + 132), T(OR))
    c.outline(corps | portail, (70, 52, 38))
    m_all |= portail
    a = np.zeros((H_ + 50, W_, 4), np.uint8)
    y_a = oy - 50
    blk = c.a[y_a:oy + 132, ox + 105:ox + 105 + W_, :3]
    msk = m_all[y_a:oy + 132, ox + 105:ox + 105 + W_]
    # le contour sombre ajouté par outline() hors du masque : on le garde (pixels non noirs autour)
    autour = np.zeros_like(msk)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        autour |= np.roll(np.roll(msk, dy, 0), dx, 1)
    garde = msk | (autour & (blk.sum(axis=-1) > 0))
    a[..., :3] = blk
    a[..., 3] = np.where(garde, 255, 0)
    return Image.fromarray(a, "RGBA")


_MAISON = {}


def _maison():
    if "im" not in _MAISON:
        _MAISON["im"] = _maison_qaroun_sprite()
    return _MAISON["im"]


QAROUN_SOL = 292                                                               # le sol sous la demeure (pieds du bâtiment)
QAROUN_X = 30                                                                  # bord gauche de la demeure (dessin)


def _place_ville(heure="jour", vide=False):
    """Une place de la ville : des maisons et des palmiers de chaque côté ; au fond, la demeure de Qaroun (ou, vide, le
    terrain nu et fendu là où elle était). Pieds y = 330."""
    c = _Px()
    T = _T(heure)
    sky = _ciel(c, heure, QAROUN_SOL, dict(aube=(300, 170), jour=(300, 46), soir=(-30, 170), nuit=(300, 60))[heure],
                seed=661)
    snap = c.a.copy()
    rr = R(662)
    loin = mix(T((196, 170, 132)), CIELS[heure][1], 0.45)                     # la ville au loin, derrière la place
    xs_ = -105
    while xs_ < 375:
        w_ = rr.randint(14, 30)
        h_ = rr.randint(12, 34)
        c.fill(c.mask_rect(xs_, QAROUN_SOL - h_, xs_ + w_, QAROUN_SOL), loin if rr.random() < 0.6 else lt(loin, 0.06))
        if rr.random() < 0.5:
            c.fill(c.mask_rect(xs_ + w_ // 2 - 1, QAROUN_SOL - h_ + 5, xs_ + w_ // 2 + 1, QAROUN_SOL - h_ + 8), dk(loin, 0.8))
        xs_ += w_ + rr.randint(-2, 3)
    for (xa, xb, yt, i) in ((-105, -40, 220, 0), (-40, 22, 236, 1), (262, 316, 230, 2), (316, 375, 214, 3)):
        m = c.mask_rect(xa, yt, xb, QAROUN_SOL)
        col = T(mix((206, 170, 124), (186, 146, 106), 0.4 * (i % 2)))
        c.fill(m, col)
        _briques(c, m, col, seed=670 + i)
        c.fill(c.mask_rect(xa, yt - 3, xb, yt), lt(col, 0.12))
        _fenetre(c, (xa + xb) // 2 - 4, yt + 14, 8, 8, heure == "nuit", lampe=False)
        c.outline(m, (60, 44, 34))
    for x in (-74, 300):
        palmier(c, x, QAROUN_SOL, h=86, lean=8, seed=680 + x)
    sol = c.mask_rect(-105, QAROUN_SOL, 375, 480)
    terre = T((210, 176, 128))
    c.vgrad(sol, QAROUN_SOL, 480, lt(terre, 0.05), dk(terre, 0.7), steps=6)
    for _ in range(60):
        x, y = rr.randint(-100, 370), rr.randint(QAROUN_SOL + 4, 470)
        c.fill(c.mask_ell(x, y, 1.5, 0.8), dk(terre, 0.86))
    if vide:                                                                   # le terrain nu, la terre fendue
        zone = c.mask_poly([(QAROUN_X - 6, QAROUN_SOL + 1), (QAROUN_X + 216, QAROUN_SOL + 1),
                            (QAROUN_X + 230, QAROUN_SOL + 22), (QAROUN_X - 20, QAROUN_SOL + 22)])
        c.tint(zone, dk(terre, 0.6), 0.45)
        for (pts) in ([(40, 294), (60, 300), (74, 296), (96, 306), (120, 300)], [(130, 296), (150, 304), (176, 298),
                      (196, 308), (220, 300)], [(90, 302), (100, 312), (118, 310)]):
            for (a_, b_) in zip(pts, pts[1:]):
                c.line(a_[0], a_[1], b_[0], b_[1], (80, 58, 40))
        for _ in range(26):
            x, y = rr.randint(QAROUN_X, QAROUN_X + 210), rr.randint(QAROUN_SOL + 2, QAROUN_SOL + 18)
            c.fill(c.mask_ell(x, y, 1.5, 1), (130, 104, 80))
    else:
        c.paste(_maison(), QAROUN_X, QAROUN_SOL - _maison().height + 1)
    if heure == "nuit":
        c.tint(c.mask_rect(-105, 0, 375, 480), (10, 10, 36), 0.25)
    return relief(c, snap, sky), None


def anim_engloutit(cles, duree=5.0):
    """La terre engloutit la demeure : à partir de t_debut, la terre se fend devant elle, elle s'enfonce lentement
    (coupée au niveau du sol), un nuage de poussière monte, puis la terre se referme : il ne reste rien. À utiliser sur
    le décor palais_qaroun_vide (avant t_debut, la demeure est dessinée par l'animation)."""
    from PIL import Image, ImageDraw
    rnd = R(91)
    B = [(rnd.uniform(-10, 220), rnd.uniform(0, 1), rnd.uniform(8, 18)) for _ in range(26)]

    def f(img, u):
        t_debut = min(cles) if cles else 1e9                                   # {engloutit} : l'instant où ça commence
        v = u - t_debut
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        mai = _maison()
        k = _smooth(v / duree) if v > 0 else 0.0
        enf = int(round(k * (mai.height + 4)))
        if enf < mai.height:                                                   # la demeure, coupée au sol
            vis = mai.crop((0, 0, mai.width, mai.height - enf))
            lay.alpha_composite(vis, (QAROUN_X + 105, QAROUN_SOL - mai.height + 1 + enf))
        d = ImageDraw.Draw(lay)
        if 0 < v < duree + 1.5:                                                # la faille et la poussière
            a_ = min(1.0, v / 0.8) * (1 if v < duree else max(0.0, 1 - (v - duree) / 1.5))
            d.line([(QAROUN_X + 100, QAROUN_SOL + 1), (QAROUN_X + 105 + 215, QAROUN_SOL + 1)], fill=(40, 26, 18, int(230 * a_)), width=2)
            for (dx, ph, r_) in B:
                hh = (v * 9 + ph * 20) % 40
                x = QAROUN_X + 105 + dx + math.sin(v + ph * 6) * 4
                y = QAROUN_SOL - hh
                rr_ = r_ * (0.6 + hh / 50)
                d.ellipse([x - rr_, y - rr_ * 0.6, x + rr_, y + rr_ * 0.6],
                          fill=(196, 170, 136, int(110 * a_ * (1 - hh / 44))))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ la dune rouge, la nuit (Boukhari 3407, Mouslim 2375)
def dune_rouge(heure="nuit"):
    """La nuit, au bord d'une route : une grande dune de sable rouge sous la lune, le ciel étoilé, la route pâle au
    premier plan ; au loin, les collines de la Terre sainte. Pieds y = 330 (sur la route)."""
    c = _Px()
    rr = R(691)
    c.vgrad(c.mask_rect(-105, 0, 375, 300), 0, 300, (8, 12, 34), (34, 40, 80), steps=8)
    for _ in range(220):
        x, y = rr.randint(-104, 374), rr.randint(0, 250)
        c.fill(c.mask_rect(x, y, x, y), mix((255, 255, 255), (150, 160, 210), rr.random() * 0.6))
    snap = c.a.copy()
    sky = c.mask_rect(-105, 0, 375, 300)
    c.fill(c.mask_ell(300, 60, 11, 11), (246, 242, 220))                       # la lune
    c.glow(300, 60, 60, (220, 220, 240), 0.25)
    c.fill(c.mask_poly([(-105, 250), (-60, 236), (-10, 244), (40, 232), (90, 246), (130, 238), (180, 250), (180, 300),
                        (-105, 300)]), (40, 44, 70))                           # collines lointaines
    dune = c.yy >= 210 + 0.0 * c.xx
    dune = c.mask_poly([(-30, 300), (40, 250), (110, 214), (170, 206), (230, 222), (300, 262), (375, 290), (375, 312),
                        (-30, 312)])
    c.vgrad(dune, 206, 312, (164, 72, 56), (96, 40, 40), steps=6)              # la dune rouge, au clair de lune
    c.fill(dune & ~np.roll(dune, 1, axis=0), (196, 104, 84))
    for _ in range(40):
        x, y = rr.randint(0, 370), rr.randint(220, 308)
        if dune[y, x + 105]:
            c.fill(c.mask_rect(x, y, x + rr.randint(2, 6), y), (130, 56, 48))
    sable = c.mask_rect(-105, 300, 375, 480)
    c.vgrad(sable, 300, 480, (92, 60, 60), (40, 30, 40), steps=6)
    route = c.mask_poly([(-105, 318), (375, 312), (375, 340), (-105, 348)])
    c.vgrad(route, 312, 348, (126, 112, 104), (86, 76, 74), steps=3)          # la route pâle
    for _ in range(50):
        x, y = rr.randint(-100, 370), rr.randint(318, 344)
        if route[y, x + 105]:
            c.fill(c.mask_rect(x, y, x + 1, y), (104, 92, 88))
    return relief(c, snap, sky), None


def anim_lueur(t_debut=0.0, x=170, y=262, duree=3.0):
    """Une lumière douce monte de la tombe (au pied de la dune) : une colonne pâle qui grandit lentement et respire."""
    from PIL import Image, ImageDraw

    def f(img, u):
        v = u - t_debut
        if v < 0:
            return
        a = _smooth(v / duree) * (0.85 + 0.15 * math.sin(v * 1.6))
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        X = x + 105
        for (w_, al) in ((34, 0.10), (22, 0.14), (12, 0.2), (5, 0.28)):
            d.polygon([(X - w_ * 0.4, y - 150 * a), (X + w_ * 0.4, y - 150 * a), (X + w_, y), (X - w_, y)],
                      fill=(255, 236, 190, int(255 * al * a)))
        for (r_, al) in ((40, 0.1), (24, 0.16), (10, 0.26)):
            d.ellipse([X - r_, y - r_ * 0.35, X + r_, y + r_ * 0.35], fill=(255, 240, 200, int(255 * al * a)))
        lieux.pose_calque(img, lay)
    return f


# ================================================================ les cieux (le Voyage nocturne, Mouslim 162)
def cieux(heure="nuit"):
    """Le ciel immense : un bleu nuit profond semé d'étoiles, des voiles de lumière douce (violets, dorés), aucun sol ;
    tout en bas, une mer de nuages pâles. Pieds y = 330 (les orbes y flottent)."""
    c = _Px()
    rr = R(701)
    c.vgrad(c.mask_rect(-105, 0, 375, 480), 0, 480, (6, 8, 30), (40, 34, 86), steps=10)
    for (cx_, cy_, rx, ry, col) in ((40, 140, 160, 40, (120, 90, 170)), (240, 230, 180, 36, (200, 160, 110)),
                                     (100, 300, 220, 30, (90, 110, 190))):
        for k_ in range(5):
            f_ = 1 - k_ / 5
            c.tint(c.mask_ell(cx_, cy_, rx * f_, ry * f_), col, 0.06)
    for _ in range(420):
        x, y = rr.randint(-104, 374), rr.randint(0, 470)
        b = rr.random()
        c.fill(c.mask_rect(x, y, x, y), mix((255, 255, 255), (170, 180, 230), 0.7 * (1 - b)))
        if b > 0.93:
            for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                c.fill(c.mask_rect(x + dx, y + dy, x + dx, y + dy), (190, 200, 240))
    nuages = c.mask_rect(-105, 340, 375, 480)
    for i in range(30):                                                        # mer de nuages, tout en bas
        x, y = rr.randint(-110, 370), rr.randint(342, 420)
        c.fill(c.mask_ell(x, y, rr.randint(16, 40), rr.randint(5, 10)), mix((200, 200, 230), (90, 90, 150), y / 480))
    return c, None


def anim_echelle(t_debut=0.0, x=170, y_bas=330, y_haut=0, duree=2.5):
    """L'échelle de lumière (le Mi'raj) : deux montants de lumière et des barreaux qui s'allument de bas en haut,
    puis restent et scintillent doucement."""
    from PIL import Image, ImageDraw

    def f(img, u):
        v = u - t_debut
        if v < 0:
            return
        k = _smooth(v / duree)
        lay = Image.new("RGBA", (img.width // 4, img.height // 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        X = x + 105
        top = y_bas - (y_bas - y_haut) * k
        for (w_, al) in ((26, 0.08), (16, 0.12)):
            d.rectangle([X - w_, top, X + w_, y_bas], fill=(255, 236, 190, int(255 * al)))
        for xs in (X - 9, X + 9):
            d.line([(xs, top), (xs, y_bas)], fill=(255, 240, 200, 200), width=1)
        for yy in range(int(y_bas) - 6, int(top), -12):
            sc_ = 0.75 + 0.25 * math.sin(v * 2 + yy * 0.3)
            d.line([(X - 9, yy), (X + 9, yy)], fill=(255, 246, 214, int(200 * sc_)), width=1)
        lieux.pose_calque(img, lay)
    return f


# ================================================================ tableaux (explications, visions) : à l'écran
TABLEAUX = {}


def tableau(nom, decor, x0, y0, w=300, h=150, persos=(), objets=(), dessin=None):
    """Déclare un tableau : le morceau (x0, y0, w, h) du décor (pixels du dessin) avec des persos [(qui, x, y, état)]
    et des objets [(qui, x, y, pose)] posés dedans (x, y : pieds, en pixels du dessin) ; dessin(img_rgba) en plus."""
    TABLEAUX[nom] = dict(decor=decor, x0=x0, y0=y0, w=w, h=h, persos=persos, objets=objets, dessin=dessin)


_TAB = {}


def _image_tableau(nom):
    if nom in _TAB:
        return _TAB[nom]
    from PIL import Image
    import duo
    import film
    t = TABLEAUX[nom]
    bg, _fg = lieux.decor_large(t["decor"])
    a = bg.a[t["y0"]:t["y0"] + t["h"], t["x0"] + 105:t["x0"] + 105 + t["w"], :3]
    im = Image.fromarray(np.ascontiguousarray(a)).convert("RGBA")
    if t["dessin"] is not None:                                                # dessin en plus (sous les persos)
        t["dessin"](im)
    tout = [(y, 0, qui, x, pose) for (qui, x, y, pose) in t["objets"]] +            [(y, 1, qui, x, etat) for (qui, x, y, etat) in t["persos"]]
    for (y, est_perso, qui, x, quoi) in sorted(tout, key=lambda e: e[0]):  # du plus loin au plus près
        if est_perso:
            etat = dict(quoi)
            mir = etat.pop("miroir", False)
            sp = duo.sprite(qui, **etat) if duo.anime(qui) else duo.sprite(qui)
            if mir:
                sp = sp.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            sp = film.image(qui, pose=quoi)
        im.alpha_composite(sp, (int(x - t["x0"] - sp.width / 2), int(y - t["y0"] - sp.info.get("foot", sp.height))))
    cadre = Image.new("RGBA", (im.width + 6, im.height + 6), (238, 224, 186, 255))
    cadre.paste(Image.new("RGBA", (im.width + 2, im.height + 2), (90, 70, 50, 255)), (2, 2))
    cadre.alpha_composite(im, (3, 3))
    _TAB[nom] = cadre.resize((cadre.width * 4, cadre.height * 4), Image.NEAREST)
    return _TAB[nom]


def anim_tableau(nom, t0, duree=6.0, cy=0.44):
    """À l'écran (sc.texte) : le tableau `nom` apparaît en fondu (0,7 s) au milieu de l'image, reste, puis s'efface."""
    def f(img, u):
        if not (t0 <= u <= t0 + duree):
            return
        a = max(0.0, min(1.0, (u - t0) / 0.7, (t0 + duree - u) / 0.7))
        im = _image_tableau(nom)
        k = min(1.0, img.width * 0.72 / im.width)
        if k < 1:
            from PIL import Image
            im = im.resize((int(im.width * k), int(im.height * k)), Image.NEAREST)
        lay = im.copy()
        al = np.array(lay.getchannel("A"), np.float32) * a
        from PIL import Image
        lay.putalpha(Image.fromarray(al.astype(np.uint8)))
        img.alpha_composite(lay, (int(img.width / 2 - lay.width / 2), int(img.height * cy - lay.height / 2)))
    return f


def _mur_droit_et_tresor(im):
    """Pour le tableau du trésor : le mur redressé (droit, solide) et, sous lui, la cachette avec le coffre."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    ox, oy = 75, 206                                                           # origine du tableau dans le dessin
    for j, dy in enumerate(range(0, 78, 5)):
        ya, yb = 330 - dy - 5 - oy, 330 - dy - 1 - oy
        d.rectangle([272 - ox, ya, 346 - ox, yb], fill=(184, 146, 104, 255))
        off = 0 if j % 2 else 5
        for xx in range(272 + off, 346, 10):
            d.line([(xx - ox, ya), (xx - ox, yb)], fill=(120, 90, 64, 255))
        d.line([(272 - ox, ya), (346 - ox, ya)], fill=(210, 176, 132, 255))
    d.rectangle([272 - ox, 252 - oy, 346 - ox, 330 - oy], outline=(60, 44, 34, 255))
    d.rectangle([280 - ox, 333 - oy, 340 - ox, 149], fill=(54, 38, 30, 255), outline=(30, 20, 14, 255))


def _etoiles_annees(im):
    """Pour le tableau du taureau : des années qui passent comme des étoiles (petits points de lumière)."""
    from PIL import ImageDraw
    rnd = R(733)
    d = ImageDraw.Draw(im)
    for _ in range(46):
        x, y = rnd.randint(4, im.width - 4), rnd.randint(4, 70)
        d.point((x, y), fill=(255, 246, 214, 255))
        if rnd.random() < 0.3:
            d.line([(x - 4, y - 1), (x, y)], fill=(255, 236, 190, 160))


tableau("bateau_roi", "rivage_mer_jour", 40, 190, persos=(("SOLDAT", 92, 322, dict(pose="pointe")),
                                                          ("SOLDAT2", 124, 326, dict(face="blase")),
                                                          ("PECHEUR", 250, 306, dict(face="content", miroir=True)),
                                                          ("PECHEUR2", 282, 306, dict(miroir=True))),
        objets=(("BATEAU", 262, 316, "breche"),))
tableau("parents", "village_mur", -60, 200, persos=(("PERE_CROYANT", 40, 330, dict(face="content")),
                                                    ("FILLETTE_A", 76, 330, dict(face="content")),
                                                    ("MERE_CROYANTE", 108, 330, dict(face="content", miroir=True))))
tableau("tresor", "village_mur", 75, 206, persos=(("ORPHELIN", 196, 330, dict(face="content")),
                                                  ("ORPHELIN2", 226, 330, dict(face="neutre", miroir=True))),
        objets=(("TRESOR", 310, 353, "neutre"),), dessin=_mur_droit_et_tresor)
tableau("taureau", "terre_sainte_soir", 20, 140, objets=(), persos=(("TAUREAU", 170, 284, dict()),),
        dessin=_etoiles_annees)


# ================================================================ registre
_DEC = dict(confluent=confluent, confluent_soir=lambda: confluent("soir"), village_mur=village_mur,
            demeure_qaroun=demeure_qaroun, palais_qaroun=lambda: _place_ville("jour"),
            palais_qaroun_vide=lambda: _place_ville("jour", vide=True),
            palais_qaroun_vide_aube=lambda: _place_ville("aube", vide=True), dune_rouge=dune_rouge, cieux=cieux)
import decors_film4  # noqa: E402

_DEC["montagne_sinai_soir"] = lambda: decors_film4.montagne_sinai("soir")
egypte.enregistre(_DEC, sol_haut=dict(confluent=(330, 104), village_mur=(330, 104), demeure_qaroun=(330, 96),
                                      palais_qaroun=(330, 104), dune_rouge=(330, 104), cieux=(330, 96)))
lieux.LUMIERES["demeure_qaroun"] = (lieux.JOUR, [])
lieux.LUMIERES["dune_rouge"] = (lieux.NUIT, [])
lieux.LUMIERES["cieux"] = (lieux.NUIT, [])
