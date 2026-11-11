# Le duo IslamArcade en pixel art (style « Faux Positif ») : petits sprites chunky, contour sombre, 3 tons.
# P = le petit frère (sweat rouge, casquette, jean) ; G = le grand frère (qamis, gilet vert, barbe, calotte).
# Les sprites regardent vers la DROITE (3/4) ; miroir pour regarder vers la gauche.
import numpy as np
from spr import Spr, stamp, INK

W, H = 46, 86                    # taille de la toile d'un sprite
FOOT = 81                        # ligne des pieds

# ---------------------------------------------------------------- palettes
SKIN_P = dict(b=(232, 178, 132), s=(196, 136, 100), d=(150, 98, 74), h=(248, 206, 166))
SKIN_G = dict(b=(206, 148, 104), s=(168, 110, 78), d=(126, 80, 58), h=(228, 176, 130))
HAIR = dict(b=(40, 30, 36), s=(26, 18, 24), h=(84, 66, 74))
RED = dict(b=(210, 54, 56), s=(160, 34, 46), d=(112, 22, 38), h=(240, 102, 92))
CAP = dict(b=(34, 38, 58), s=(22, 24, 40), h=(78, 86, 116), brim=(26, 28, 44))
JEAN = dict(b=(62, 96, 166), s=(42, 66, 124), d=(30, 46, 90), h=(96, 132, 198))
SHOE = dict(b=(244, 244, 248), s=(194, 196, 210), sole=(150, 150, 164), acc=(210, 54, 56))
QAMIS = dict(b=(238, 234, 222), s=(204, 198, 184), d=(166, 158, 146), h=(252, 251, 246))
VEST = dict(b=(34, 104, 84), s=(22, 70, 58), d=(14, 46, 40), h=(64, 146, 116), trim=(222, 178, 84))
KUFI = dict(b=(248, 248, 242), s=(208, 208, 200), dot=(180, 180, 172))
SANDAL = dict(b=(132, 82, 46), s=(92, 56, 32))
WHITE = (252, 252, 252)
EYE = (26, 20, 30)
MOUTH = (110, 40, 44)
TONGUE = (214, 96, 96)
BLUSH = (238, 120, 120)
SWEAT = (150, 210, 250)


# ---------------------------------------------------------------- outils
def _limb(sp, pts, w, pal, part=True):
    m = sp.m_line(pts, w)
    sp.paint(m, pal["b"])
    sp.shade(m, pal["s"], dx=-1, dy=-1, depth=1)
    return m


def _hand(sp, x, y, skin, r=2.2, finger=None):
    m = sp.m_ell(x, y, r, r)
    sp.paint(m, skin["b"])
    sp.shade(m, skin["s"], dx=-1, dy=-1, depth=1)
    if finger == "up":                              # index levé
        sp.paint(sp.m_rect(int(round(x)), int(round(y - r - 3)), int(round(x)) + 1, int(round(y - r))), skin["b"], newpart=False)
        sp.px(int(round(x)) + 1, int(round(y - r - 2)), skin["s"])
    elif finger == "right":                         # index tendu vers la droite
        sp.paint(sp.m_rect(int(round(x + r)), int(round(y)) - 1, int(round(x + r + 3)), int(round(y))), skin["b"], newpart=False)
        sp.px(int(round(x + r + 3)), int(round(y)), skin["s"])
    return m


def _eyes(sp, ex, ey, kind, far_dx=5):
    """Deux yeux (3/4 vers la droite) : ex,ey = coin haut-gauche de l'œil proche."""
    for k, x0 in enumerate((ex, ex + far_dx)):
        far = k == 1
        if kind in ("neutre", "parle", "content", "gene", "malin_ouvert"):
            sp.pxs([(x0, ey), (x0 + 1, ey)] + ([] if far else [(x0 - 1, ey)]), EYE)          # cils
            if not far:
                sp.px(x0 - 1, ey + 1, WHITE); sp.px(x0 - 1, ey + 2, WHITE)
            sp.pxs([(x0, ey + 1), (x0 + 1, ey + 1), (x0, ey + 2), (x0 + 1, ey + 2)], EYE)
            sp.px(x0 + 1, ey + 1, (90, 90, 120))                                            # petit reflet
        elif kind == "choc":                                                               # yeux ronds
            sp.pxs([(x0 - (0 if far else 1), ey - 1), (x0, ey - 1), (x0 + 1, ey - 1)], EYE)
            for yy in (ey, ey + 1, ey + 2):
                sp.pxs([(x0 - (0 if far else 1), yy), (x0 + 1, yy)], EYE)
                sp.px(x0, yy, WHITE)
            sp.px(x0, ey + 1, EYE)
            sp.pxs([(x0 - (0 if far else 1), ey + 3), (x0, ey + 3), (x0 + 1, ey + 3)], EYE)
        elif kind in ("ferme", "rire"):                                                    # yeux fermés ^^
            sp.pxs([(x0 - (0 if far else 1), ey + 2), (x0, ey + 1), (x0 + 1, ey + 2)], EYE)
        elif kind in ("malin", "blase"):                                                   # paupières mi-closes
            sp.pxs([(x0 - (0 if far else 1), ey + 1), (x0, ey + 1), (x0 + 1, ey + 1)], EYE)
            sp.pxs([(x0, ey + 2), (x0 + 1, ey + 2)], EYE)
            if not far:
                sp.px(x0 - 1, ey + 2, WHITE)


def _brows(sp, ex, ey, kind, col, far_dx=5, thick=1):
    for k, x0 in enumerate((ex, ex + far_dx)):
        far = k == 1
        y = ey - 2
        if kind == "choc":
            y -= 1
        pts = [(x0 - (0 if far else 1), y), (x0, y), (x0 + 1, y)]
        if kind in ("gene", "inquiet"):                 # sourcils en accent circonflexe inversé
            pts = [(x0 - (0 if far else 1), y + (0 if far else 1)), (x0, y), (x0 + 1, y + (1 if far else 0))]
        if kind == "malin":
            pts = [(x0 - (0 if far else 1), y), (x0, y), (x0 + 1, y + (1 if not far else 0))]
        sp.pxs(pts, col)
        if thick > 1:
            sp.pxs([(x, yy - 1) for (x, yy) in pts[:2]], col)


def _mouth(sp, mx, my, kind):
    if kind in ("neutre",):
        sp.pxs([(mx, my), (mx + 1, my)], MOUTH)
    elif kind in ("parle",):
        sp.pxs([(mx, my), (mx + 1, my), (mx + 2, my)], MOUTH)
        sp.pxs([(mx, my + 1), (mx + 1, my + 1), (mx + 2, my + 1)], MOUTH)
        sp.px(mx + 1, my + 1, TONGUE)
    elif kind in ("choc",):
        sp.pxs([(mx, my), (mx + 1, my), (mx, my + 1), (mx + 1, my + 1), (mx, my + 2), (mx + 1, my + 2)], MOUTH)
        sp.px(mx, my + 2, TONGUE); sp.px(mx + 1, my + 2, TONGUE)
    elif kind in ("content", "rire"):
        sp.pxs([(mx - 1, my), (mx, my + 1), (mx + 1, my + 1), (mx + 2, my + 1), (mx + 3, my)], MOUTH)
        if kind == "rire":
            sp.pxs([(mx, my), (mx + 1, my), (mx + 2, my)], MOUTH); sp.px(mx + 1, my + 1, TONGUE)
    elif kind in ("malin", "malin_ouvert"):                        # sourire en coin
        sp.pxs([(mx, my), (mx + 1, my), (mx + 2, my - 1)], MOUTH)
    elif kind in ("gene",):                                       # bouche tordue
        sp.pxs([(mx, my), (mx + 1, my + 1), (mx + 2, my)], MOUTH)
    elif kind == "blase":
        sp.pxs([(mx, my), (mx + 1, my), (mx + 2, my)], MOUTH)


# ---------------------------------------------------------------- le petit frère
def petit(pose="neutre", face="neutre", talk=False, blush=False, sweat=False, back=False, step=0):
    sp = Spr(W, H)
    S = SKIN_P
    y0 = FOOT - 64 - (1 if step in (1, 3) else 0)    # haut de la casquette (petit rebond en marchant)
    # bras arrière (côté droit, derrière le corps)
    far_arm = dict(neutre=[(31, y0 + 25), (32, y0 + 33), (32, y0 + 40)],
                   question=[(31, y0 + 25), (36, y0 + 29), (36, y0 + 19)],
                   panique=[(31, y0 + 25), (37, y0 + 31), (37, y0 + 24)],
                   nez=[(31, y0 + 25), (34, y0 + 30), (30, y0 + 16)],
                   priere=[(31, y0 + 25), (31, y0 + 32), (24, y0 + 33)],
                   pointe=[(31, y0 + 25), (36, y0 + 26), (40, y0 + 26)],
                   ablution=[(31, y0 + 25), (34, y0 + 32), (38, y0 + 31)])[pose]
    near_arm = dict(neutre=[(13, y0 + 25), (12, y0 + 33), (12, y0 + 40)],
                    question=[(13, y0 + 25), (12, y0 + 33), (12, y0 + 40)],
                    panique=[(13, y0 + 25), (7, y0 + 31), (7, y0 + 24)],
                    nez=[(13, y0 + 25), (12, y0 + 33), (12, y0 + 40)],
                    priere=[(13, y0 + 25), (14, y0 + 33), (22, y0 + 33)],
                    pointe=[(13, y0 + 25), (12, y0 + 33), (12, y0 + 40)],
                    ablution=[(13, y0 + 25), (16, y0 + 33), (36, y0 + 33)])[pose]
    if not back:
        _limb(sp, far_arm, 5, RED)
        hx, hy = far_arm[-1]
        _hand(sp, hx, hy + (2 if pose in ("neutre", "pointe") else -1), S,
              finger="up" if pose == "question" else ("right" if pose == "pointe" else None))
    # jambes
    yb = FOOT - 64                                   # les pieds restent au sol
    offs = {0: (0, 0), 1: (-2, 2), 2: (0, 0), 3: (2, -2)}[step % 4]
    for k, lx in enumerate((15, 22)):
        dx = offs[k]
        lift = 1 if (step % 4 == 1 and k == 1) or (step % 4 == 3 and k == 0) else 0
        m = sp.paint(sp.m_rect(lx + dx, y0 + 41, lx + dx + 6, yb + 60 - lift), JEAN["b"])
        sp.shade(m, JEAN["s"], dx=-1, dy=0, depth=2)
        sp.tone(sp.m_rect(lx + dx, y0 + 41, lx + dx, yb + 60 - lift), JEAN["h"])
    if step % 2 == 0:
        sp.tone(sp.m_rect(21, y0 + 44, 21, yb + 60), JEAN["d"])
    # chaussures (vers la droite)
    for k, lx in enumerate((14, 22)):
        dx = offs[k]
        lift = 1 if (step % 4 == 1 and k == 1) or (step % 4 == 3 and k == 0) else 0
        x0, yy = lx + dx, yb + 60 - lift
        m = sp.paint(sp.m_rect(x0, yy, x0 + 8, yy + 3) & ~sp.m_rect(x0, yy, x0, yy), SHOE["b"])
        sp.tone(sp.m_rect(x0, yy + 3, x0 + 8, yy + 3), SHOE["sole"])
        sp.tone(sp.m_rect(x0 + 2, yy + 1, x0 + 4, yy + 1), SHOE["acc"])
    # sweat
    torso = sp.m_poly([(12, y0 + 22), (31, y0 + 22), (33, y0 + 25), (32, y0 + 42), (11, y0 + 42), (10, y0 + 25)])
    sp.paint(torso, RED["b"])
    sp.shade(torso, RED["s"], dx=-1, dy=-1, depth=3)
    sp.tone(sp.m_rect(11, y0 + 24, 11, y0 + 40) & torso, RED["h"])
    sp.tone(sp.m_rect(11, y0 + 39, 32, y0 + 41) & torso, RED["s"])                  # bord côtelé
    if not back:
        pk = sp.m_rect(15, y0 + 32, 27, y0 + 37)                                    # poche kangourou
        sp.tone(pk, RED["s"]); sp.tone(sp.m_rect(15, y0 + 32, 27, y0 + 32), RED["d"])
        sp.tone(sp.m_rect(15, y0 + 32, 15, y0 + 37), RED["d"]); sp.tone(sp.m_rect(27, y0 + 32, 27, y0 + 37), RED["d"])
        for cx in (19, 23):                                                         # cordons
            sp.tone(sp.m_rect(cx, y0 + 23, cx, y0 + 28), WHITE)
            sp.px(cx, y0 + 29, (210, 210, 220))
        hood = sp.m_ell(21.5, y0 + 22.5, 6.5, 2.2)
        sp.tone(hood, RED["d"])
    else:
        hood = sp.m_ell(21.5, y0 + 24, 7.5, 4.5) & torso                            # capuche dans le dos
        sp.tone(hood, RED["s"]); sp.tone(sp.m_ell(21.5, y0 + 23, 5.5, 2.5) & torso, RED["d"])
    # cou
    sp.paint(sp.m_rect(19, y0 + 18, 24, y0 + 22), S["s"])
    # tête
    cran = sp.m_ell(21, y0 + 9, 8.3, 7.6)
    facem = sp.m_ell(22.5, y0 + 13.2, 7.0, 6.5) | sp.m_poly([(19, y0 + 17), (26, y0 + 17), (24, y0 + 20), (21, y0 + 20)])
    head = cran | facem
    if back:
        head = cran | sp.m_ell(21, y0 + 13, 7.2, 6.4)
    sp.paint(head, S["b"])
    sp.shade(head, S["s"], dx=-1, dy=-1, depth=1)
    # cheveux sous la casquette (derrière / nuque)
    hair = head & ((sp.m_rect(12, y0 + 7, 17, y0 + 15) & ~sp.m_poly([(17, y0 + 15), (17, y0 + 11), (15, y0 + 15)])) |
                   sp.m_rect(17, y0 + 8, 19, y0 + 11))
    if back:
        hair = head & sp.m_rect(10, y0 + 6, 32, y0 + 17) & ~sp.m_rect(18, y0 + 17, 24, y0 + 17)
    sp.tone(hair, HAIR["b"])
    sp.tone(hair & sp.m_rect(12, y0 + 7, 32, y0 + 8), HAIR["h"])
    # oreille
    if not back:
        ear = sp.m_ell(15.8, y0 + 12.6, 1.7, 2.3)
        sp.paint(ear, S["b"]); sp.px(16, y0 + 13, S["s"]); sp.px(15, y0 + 12, S["s"])
    # casquette
    crown = sp.m_ell(21, y0 + 6.2, 8.9, 6.0) & sp.m_rect(0, 0, W, y0 + 8)
    sp.paint(crown, CAP["b"])
    sp.tone(crown & sp.m_ell(17.5, y0 + 3.5, 4.5, 2.6), CAP["h"])
    sp.shade(crown, CAP["s"], dx=-1, dy=0, depth=2)
    sp.tone(sp.m_rect(12, y0 + 8, 30, y0 + 8) & head, CAP["s"])                      # bandeau
    if not back:
        brim = sp.m_rect(26, y0 + 7, 33, y0 + 8) | sp.m_rect(25, y0 + 8, 34, y0 + 8)
        sp.paint(brim, CAP["brim"])
        sp.tone(sp.m_rect(27, y0 + 7, 32, y0 + 7), CAP["b"])
        sp.tone(sp.m_rect(21, y0 + 9, 29, y0 + 9) & head, S["s"])                     # ombre sous la visière
        sp.px(21, y0 + 2, CAP["h"]); sp.px(21, y0 + 1, CAP["s"])                      # bouton
    else:
        sp.tone(sp.m_rect(18, y0 + 9, 24, y0 + 9) & head, CAP["s"])                   # attache réglable
        sp.tone(sp.m_rect(20, y0 + 9, 22, y0 + 10) & head, HAIR["b"])
    # visage
    if not back:
        ex, ey = 20, y0 + 11
        _eyes(sp, ex, ey, face)
        _brows(sp, ex, ey, face if face in ("choc", "gene", "malin") else "neutre", HAIR["b"])
        sp.px(28, y0 + 15, S["s"])                                                    # nez
        mk = "parle" if talk else {"neutre": "neutre", "choc": "choc", "content": "content", "rire": "rire",
                                   "gene": "gene", "malin": "malin", "ferme": "neutre", "blase": "blase"}.get(face, "neutre")
        _mouth(sp, 23, y0 + 17, mk)
        if blush:
            sp.pxs([(19, y0 + 15), (20, y0 + 15), (27, y0 + 15)], BLUSH)
        if sweat:
            sp.pxs([(13, y0 + 9), (13, y0 + 10), (12, y0 + 11), (13, y0 + 11), (14, y0 + 11), (13, y0 + 12)], SWEAT)
    # bras avant
    if not back:
        _limb(sp, near_arm, 5, RED)
        hx, hy = near_arm[-1]
        _hand(sp, hx + (1 if pose == "ablution" else 0), hy + (2 if pose in ("neutre", "question", "nez", "pointe") else 0), S)
    else:
        for x in (10, 33):                                                           # coudes (bras croisés devant)
            m = sp.paint(sp.m_rect(x - 1, y0 + 25, x + 1, y0 + 34), RED["b"])
            sp.shade(m, RED["s"], dx=-1, dy=0, depth=1)
    sp.outline()
    return sp


# ---------------------------------------------------------------- le grand frère
def grand(pose="neutre", face="neutre", talk=False, back=False, the=False, qamis=None, gilet=True, kufi=True, skin=None):
    sp = Spr(W, H)
    S = skin or SKIN_G
    Q = qamis or QAMIS
    y0 = FOOT - 73
    far_arm = dict(neutre=[(32, y0 + 23), (33, y0 + 33), (33, y0 + 41)],
                   explique=[(32, y0 + 23), (36, y0 + 31), (40, y0 + 28)],
                   pointe=[(32, y0 + 23), (37, y0 + 27), (39, y0 + 19)],
                   the=[(32, y0 + 23), (33, y0 + 33), (33, y0 + 41)],
                   priere=[(32, y0 + 23), (32, y0 + 31), (24, y0 + 32)],
                   bras_croises=[(32, y0 + 23), (32, y0 + 32), (16, y0 + 32)])[pose]
    near_arm = dict(neutre=[(11, y0 + 23), (10, y0 + 33), (10, y0 + 41)],
                    explique=[(11, y0 + 23), (10, y0 + 33), (10, y0 + 41)],
                    pointe=[(11, y0 + 23), (10, y0 + 33), (10, y0 + 41)],
                    the=[(11, y0 + 23), (12, y0 + 32), (20, y0 + 32)],
                    priere=[(11, y0 + 23), (12, y0 + 31), (22, y0 + 32)],
                    bras_croises=[(11, y0 + 23), (12, y0 + 31), (28, y0 + 31)])[pose]
    if not back:
        _limb(sp, far_arm, 5, Q)
        hx, hy = far_arm[-1]
        _hand(sp, hx, hy + (2 if pose in ("neutre", "the") else 0), S,
              finger="up" if pose == "pointe" else None)
    # sandales
    for lx in (14, 24):
        m = sp.paint(sp.m_rect(lx, y0 + 70, lx + 7, y0 + 72), SANDAL["b"])
        sp.tone(sp.m_rect(lx, y0 + 72, lx + 7, y0 + 72), SANDAL["s"])
        sp.tone(sp.m_rect(lx + 2, y0 + 69, lx + 5, y0 + 69), S["b"])
    # qamis long
    body = sp.m_poly([(12, y0 + 21), (31, y0 + 21), (33, y0 + 24), (34, y0 + 69), (9, y0 + 69), (10, y0 + 24)])
    sp.paint(body, Q["b"])
    sp.shade(body, Q["s"], dx=-1, dy=-1, depth=3)
    sp.tone(sp.m_rect(10, y0 + 26, 10, y0 + 67) & body, Q["h"])
    for fx, f0 in ((16, 50), (25, 46), (29, 54)):                                    # plis
        sp.tone(sp.m_rect(fx, y0 + f0, fx, y0 + 68) & body, Q["s"])
    sp.tone(sp.m_rect(9, y0 + 68, 34, y0 + 69) & body, Q["d"])
    if gilet and not back:
        v = sp.m_poly([(12, y0 + 22), (31, y0 + 22), (32, y0 + 25), (32, y0 + 45), (11, y0 + 45), (11, y0 + 25)]) & \
            ~sp.m_poly([(19, y0 + 22), (25, y0 + 22), (23, y0 + 37), (21, y0 + 37)])
        sp.paint(v, VEST["b"], newpart=False)
        sp.shade(v, VEST["s"], dx=-1, dy=-1, depth=2)
        sp.tone(sp.m_rect(11, y0 + 26, 11, y0 + 44) & v, VEST["h"])
        trim = v & ~(np.roll(v, 1, 1) & np.roll(v, -1, 1) & np.roll(v, 1, 0) & np.roll(v, -1, 0)) & sp.m_rect(17, y0 + 22, 27, y0 + 39)
        sp.tone(trim, VEST["trim"])
        for k in range(3):                                                          # boutons du qamis
            sp.px(22, y0 + 26 + k * 4, Q["d"])
    elif gilet and back:
        v = sp.m_poly([(12, y0 + 22), (31, y0 + 22), (32, y0 + 25), (32, y0 + 45), (11, y0 + 45), (11, y0 + 25)])
        sp.paint(v, VEST["b"], newpart=False); sp.shade(v, VEST["s"], dx=-1, dy=-1, depth=2)
    # cou
    sp.paint(sp.m_rect(19, y0 + 17, 24, y0 + 21), S["s"])
    # tête
    cran = sp.m_ell(21, y0 + 9.5, 8.6, 7.4)
    facem = sp.m_ell(22.5, y0 + 13.5, 7.2, 6.9) | sp.m_poly([(18, y0 + 18), (27, y0 + 18), (25, y0 + 21), (20, y0 + 21)])
    head = cran | facem if not back else cran | sp.m_ell(21, y0 + 13, 7.4, 6.8)
    sp.paint(head, S["b"])
    sp.shade(head, S["s"], dx=-1, dy=-1, depth=1)
    hair = head & sp.m_rect(10, y0 + 5, 19, y0 + 13) & ~sp.m_poly([(19, y0 + 13), (19, y0 + 8), (16, y0 + 13)])
    if back:
        hair = head & sp.m_rect(0, 0, W, y0 + 15)
    sp.tone(hair, HAIR["b"])
    if not back:                                                                    # barbe courte
        beard = head & (sp.m_rect(0, y0 + 14, W, H) | (sp.m_rect(15, y0 + 10, 19, H))) & sp.m_rect(15, 0, W, H)
        beard &= ~sp.m_rect(20, y0 + 10, 30, y0 + 14)
        sp.tone(beard, HAIR["b"])
        sp.tone(beard & sp.m_rect(16, y0 + 15, 17, y0 + 17), HAIR["h"])
        sp.tone(sp.m_rect(22, y0 + 15, 27, y0 + 15) & head, HAIR["s"])                # moustache
        ear = sp.m_ell(15.6, y0 + 12.2, 1.7, 2.3)
        sp.paint(ear, S["b"]); sp.px(16, y0 + 12, S["s"]); sp.px(15, y0 + 11, S["s"])
    if kufi:
        k = sp.m_ell(21, y0 + 5.8, 8.8, 4.6) & sp.m_rect(0, 0, W, y0 + 7)
        sp.paint(k, KUFI["b"])
        sp.shade(k, KUFI["s"], dx=-1, dy=0, depth=2)
        for x in range(14, 30, 2):
            sp.px(x, y0 + 5, KUFI["dot"])
        sp.tone(sp.m_rect(12, y0 + 7, 30, y0 + 7) & k, KUFI["s"])
    if not back:
        ex, ey = 20, y0 + 10
        _eyes(sp, ex, ey, face)
        _brows(sp, ex, ey, face if face in ("choc", "gene", "malin") else "neutre", HAIR["b"], thick=2)
        sp.px(28, y0 + 13, S["s"])
        mk = "parle" if talk else {"neutre": "neutre", "choc": "choc", "content": "content", "rire": "rire",
                                   "malin": "malin", "blase": "blase", "ferme": "neutre"}.get(face, "neutre")
        # la bouche est dans la barbe : on dégage un peu de peau autour
        sp.tone(sp.m_rect(22, y0 + 16, 26, y0 + 17) & head, S["s"])
        _mouth(sp, 23, y0 + 16, mk)
    if not back:
        _limb(sp, near_arm, 5, Q)
        hx, hy = near_arm[-1]
        _hand(sp, hx, hy + (2 if pose in ("neutre", "explique", "pointe") else 0), S)
        if pose == "the" or the:                                                     # verre de thé à la menthe
            gx, gy = near_arm[-1][0] + 2, near_arm[-1][1] - 6
            glass = sp.m_poly([(gx, gy), (gx + 4, gy), (gx + 3, gy + 6), (gx + 1, gy + 6)])
            sp.paint(glass, (190, 226, 236))
            sp.tone(glass & sp.m_rect(gx, gy + 2, gx + 4, gy + 6), (196, 120, 46))
            sp.tone(glass & sp.m_rect(gx + 1, gy + 3, gx + 1, gy + 5), (236, 176, 96))
            sp.pxs([(gx + 1, gy - 2), (gx + 2, gy - 3), (gx + 3, gy - 5)], (230, 230, 236))   # vapeur
    else:
        for x in (10, 33):
            m = sp.paint(sp.m_rect(x - 1, y0 + 24, x + 1, y0 + 33), Q["b"])
            sp.shade(m, Q["s"], dx=-1, dy=0, depth=1)
    sp.outline()
    return sp


# ---------------------------------------------------------------- fidèles (de dos) pour les rangs de prière
FIDELES = [dict(qamis=dict(b=(238, 234, 222), s=(204, 198, 184), d=(166, 158, 146), h=(252, 251, 246)), kufi=True),
           dict(qamis=dict(b=(150, 172, 200), s=(118, 138, 166), d=(90, 106, 132), h=(178, 198, 222)), kufi=False),
           dict(qamis=dict(b=(176, 148, 112), s=(144, 118, 88), d=(110, 88, 64), h=(204, 178, 142)), kufi=True),
           dict(qamis=dict(b=(120, 136, 112), s=(94, 108, 88), d=(70, 82, 66), h=(150, 166, 140)), kufi=False)]


def fidele(k=0, skin=None):
    f = FIDELES[k % len(FIDELES)]
    return grand("priere", back=True, qamis=f["qamis"], gilet=False, kufi=f["kufi"], skin=skin)


# ---------------------------------------------------------------- bulles et icônes (même grille de pixels que les persos)
GLYPH = {
    "!": ["..x..", "..x..", "..x..", "..x..", ".....", "..x.."],
    "?": [".xxx.", "x...x", "...x.", "..x..", ".....", "..x.."],
    ".": [".....", ".....", ".....", ".....", ".....", "..x.."],
}


def bulle(txt="!", kind="dit"):
    """Petite bulle blanche au-dessus de la tête : '!', '?', '?!', '...'."""
    glyphs = [GLYPH[ch] for ch in txt]
    gw = sum(5 for _ in glyphs) + (len(glyphs) - 1)
    w, h = gw + 6, 12
    sp = Spr(w + 4, h + 6)
    body = sp.m_rect(1, 1, w, h - 1) & ~sp.m_rect(1, 1, 1, 1) & ~sp.m_rect(w, 1, w, 1) & ~sp.m_rect(1, h - 1, 1, h - 1) & ~sp.m_rect(w, h - 1, w, h - 1)
    sp.paint(body, (252, 252, 252))
    if kind == "dit":
        sp.paint(sp.m_poly([(3, h - 1), (7, h - 1), (3, h + 3)]), (252, 252, 252), newpart=False)
    else:                                                 # bulle de pensée : petits ronds
        sp.paint(sp.m_ell(4, h + 1.5, 1.4, 1.2), (252, 252, 252), newpart=False)
        sp.paint(sp.m_ell(2, h + 4, 0.9, 0.9), (252, 252, 252), newpart=False)
    x = 4
    for g in glyphs:
        for j, row in enumerate(g):
            for i, ch in enumerate(row):
                if ch == "x":
                    sp.px(x + i, 3 + j, (200, 40, 50) if txt[0] == "!" else (30, 30, 60))
        x += 6
    sp.outline()
    return sp


def goutte():
    """Goutte de sueur (gêne)."""
    sp = Spr(5, 7)
    sp.pxs([(2, 0), (2, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3), (1, 4), (2, 4), (3, 4), (2, 5)], SWEAT)
    sp.px(1, 3, (230, 246, 255))
    sp.outline((40, 70, 110, 255))
    return sp


ICONS = {
    "nez_sang": (["....kkk.....",
                  "...ksssk....",
                  "...kssssk...",
                  "..ksssssk...",
                  "..kssssssk..",
                  ".ksssssSsk..",
                  ".kssssSSssk.",
                  "kssSkkkkSsk.",
                  "kssk.r.ksk..",
                  ".kk..rr.k...",
                  ".....rr.....",
                  "......r.....",
                  "............"],
                 dict(k=INK[:3], s=SKIN_P["b"], S=SKIN_P["s"], r=(220, 30, 40))),
    "oreille": (["...kkkk...",
                 "..kssssk..",
                 ".ksSSSssk.",
                 ".kSkkkSsk.",
                 ".kS..kSsk.",
                 ".kSk.kSsk.",
                 "..kSSSsk..",
                 "...kSssk..",
                 "...ksssk..",
                 "....kssk..",
                 ".....kk..."],
                dict(k=INK[:3], s=SKIN_P["b"], S=SKIN_P["s"])),
    "nez": (["....kk....",
             "...kssk...",
             "...ksssk..",
             "..ksssssk.",
             "..ksssSsk.",
             ".kssssSSsk",
             "ksSSkkkSsk",
             "kssk..ksk.",
             ".kk....k.."],
            dict(k=INK[:3], s=SKIN_P["b"], S=SKIN_P["s"])),
}


def icone(name):
    rows, pal = ICONS[name]
    sp = Spr(max(len(r) for r in rows), len(rows))
    stamp(sp, rows, {k: v for k, v in pal.items()}, 0, 0)
    return sp


def pensee(icon="nez_sang"):
    """Bulle de pensée contenant une icône."""
    ic = icone(icon)
    w, h = ic.w + 6, ic.h + 5
    sp = Spr(w + 2, h + 7)
    body = sp.m_ell((w + 1) / 2, h / 2 + 0.5, w / 2, h / 2)
    sp.paint(body, (252, 252, 252))
    sp.paint(sp.m_ell(4, h + 1.8, 1.6, 1.3), (252, 252, 252), newpart=False)
    sp.paint(sp.m_ell(2, h + 4.6, 1.0, 1.0), (252, 252, 252), newpart=False)
    sp.a[3:3 + ic.h, 4:4 + ic.w][ic.a[..., 3] > 0] = ic.a[ic.a[..., 3] > 0]
    sp.outline()
    return sp


def pensee_saigne():
    """Bulle de pensée : la tête du petit frère qui saigne du nez (ce que croient les voisins)."""
    p = petit("neutre", "gene")
    y0 = FOOT - 64
    head = Spr(26, 23)
    head.a[:] = p.a[y0 - 1:y0 + 22, 9:35]
    for (x, y) in ((19, 16), (19, 17), (18, 18), (19, 18), (18, 19)):     # goutte rouge sous le nez
        head.px(x, y, (220, 30, 40))
    head.px(19, 19, (150, 16, 26))
    w, h = head.w + 8, head.h + 6
    sp = Spr(w + 2, h + 8)
    sp.paint(sp.m_ell((w + 1) / 2, h / 2 + 0.5, w / 2, h / 2), (252, 252, 252))
    sp.paint(sp.m_ell(5, h + 2.0, 1.8, 1.5), (252, 252, 252), newpart=False)
    sp.paint(sp.m_ell(2.5, h + 5.2, 1.1, 1.1), (252, 252, 252), newpart=False)
    m = head.a[..., 3] > 0
    sp.a[4:4 + head.h, 5:5 + head.w][m] = head.a[m]
    sp.outline()
    return sp


# ---------------------------------------------------------------- la sœur (hijab, abaya)
SKIN_S = dict(b=(224, 166, 124), s=(186, 128, 94), d=(146, 96, 72), h=(242, 196, 156))
ABAYA = dict(b=(84, 58, 96), s=(62, 42, 72), d=(44, 30, 52), h=(112, 82, 126))
HIJAB = dict(b=(214, 150, 160), s=(178, 112, 126), d=(140, 84, 98), h=(236, 186, 192))


def soeur(pose="neutre", face="neutre", talk=False, nails=None, henne=False):
    """Grande sœur : abaya longue, hijab. nails = couleur des ongles (vernis), henne = mains teintes."""
    sp = Spr(W, H)
    S = SKIN_S
    y0 = FOOT - 68
    arms = dict(neutre=([(31, y0 + 24), (32, y0 + 34), (32, y0 + 42)], [(12, y0 + 24), (11, y0 + 34), (11, y0 + 42)]),
                mains=([(31, y0 + 24), (34, y0 + 32), (38, y0 + 30)], [(12, y0 + 24), (16, y0 + 33), (33, y0 + 32)]),
                ablution=([(31, y0 + 24), (34, y0 + 33), (39, y0 + 33)], [(12, y0 + 24), (17, y0 + 34), (36, y0 + 34)]))[pose]
    far, near = arms

    def hand(x, y):
        m = sp.m_ell(x, y, 2.6, 2.6)
        sp.paint(m, (196, 110, 70) if henne else S["b"]); sp.shade(m, S["s"], dx=-1, dy=-1, depth=1)
        if nails:
            sp.pxs([(int(x) + 2, int(y) - 1), (int(x) + 2, int(y)), (int(x) + 2, int(y) + 1)], nails)
        if henne:
            sp.px(int(x), int(y), (120, 50, 30)); sp.px(int(x) - 1, int(y) + 1, (120, 50, 30))
    _limb(sp, far, 5, ABAYA); hand(*far[-1])
    for lx in (15, 24):                                                 # chaussures
        sp.paint(sp.m_rect(lx, y0 + 64, lx + 6, y0 + 66), (50, 40, 46))
    body = sp.m_poly([(13, y0 + 21), (30, y0 + 21), (32, y0 + 25), (35, y0 + 65), (8, y0 + 65), (11, y0 + 25)])
    sp.paint(body, ABAYA["b"]); sp.shade(body, ABAYA["s"], dx=-1, dy=-1, depth=3)
    sp.tone(sp.m_rect(10, y0 + 27, 10, y0 + 63) & body, ABAYA["h"])
    for fx in (17, 26):
        sp.tone(sp.m_rect(fx, y0 + 44, fx, y0 + 64) & body, ABAYA["s"])
    # hijab : drapé sur les épaules + tour du visage
    drape = sp.m_ell(21.5, y0 + 21, 11, 6) | sp.m_ell(21, y0 + 10, 9.6, 9.6)
    sp.paint(drape, HIJAB["b"]); sp.shade(drape, HIJAB["s"], dx=-1, dy=-1, depth=2)
    sp.tone(sp.m_ell(17, y0 + 5, 3, 2) & drape, HIJAB["h"])
    face_m = sp.m_ell(23, y0 + 12.5, 5.8, 6.4)
    sp.paint(face_m, S["b"]); sp.shade(face_m, S["s"], dx=-1, dy=-1, depth=1)
    sp.tone(sp.m_rect(16, y0 + 4, 30, y0 + 6) & face_m, HIJAB["s"])
    ex, ey = 21, y0 + 10
    _eyes(sp, ex, ey, face, far_dx=4)
    sp.pxs([(ex - 2, ey), (ex + 6, ey - 1)], EYE)                       # cils
    sp.px(28, y0 + 14, S["s"])
    mk = "parle" if talk else {"neutre": "neutre", "choc": "choc", "content": "content", "rire": "rire",
                               "gene": "gene", "malin": "malin", "ferme": "neutre", "blase": "blase"}.get(face, "neutre")
    _mouth(sp, 23, y0 + 16, mk)
    sp.pxs([(19, y0 + 14), (27, y0 + 14)], BLUSH)
    _limb(sp, near, 5, ABAYA); hand(*near[-1])
    sp.outline()
    return sp


# ---------------------------------------------------------------- icônes du tableau (dessinées à la main)
ICONS2 = {
    "main_vernis": ["..k.k.k.....",
                    ".krkrkrk....",
                    ".kskskskk...",
                    ".ksssssskk..",
                    ".kssssssssk.",
                    "kSssssssssk.",
                    "kSsssssssk..",
                    ".kSsssssk...",
                    "..kSssssk...",
                    "...kssssk...",
                    "...kSsssk...",
                    "....kkkk...."],
    "main_henne": ["..k.k.k.....",
                   ".khkhkhk....",
                   ".kskhkskk...",
                   ".kshhhhskk..",
                   ".kshsshsssk.",
                   "kSshhhhsssk.",
                   "kSsshhsssk..",
                   ".kSsssssk...",
                   "..kSssssk...",
                   "...kssssk...",
                   "...kSsssk...",
                   "....kkkk...."],
    "faux_ongle": ["..kk.kk.kk..",
                   ".kpkkpkkpk..",
                   ".kpkkpkkpk..",
                   ".kpkkpkkpk..",
                   ".kskskskskk.",
                   ".ksssssssssk",
                   "kSsssssssssk",
                   "kSssssssssk.",
                   ".kSsssssssk.",
                   "..kSssssk...",
                   "...kssssk...",
                   "....kkkk...."],
    "goutte": [".....k......",
               "....kbk.....",
               "...kbbbk....",
               "..kbwbbbk...",
               ".kbwbbbbbk..",
               ".kbwbbbbbk..",
               "kbbbbbbbbbk.",
               "kbbbbbbbbbk.",
               ".kbbbbbbbk..",
               "..kbbbbbk...",
               "...kkkkk...."],
    "mascara": ["....kkk.....",
                "...kgggk....",
                "...kgggk....",
                "...kkkkk....",
                "...kdddk....",
                "...kdddk....",
                "...kdddk....",
                "...kdddk....",
                "...kdddk....",
                "...kdddk....",
                "...kkkkk...."],
    "khol": ["...........k",
             "..........kd",
             ".........kdk",
             "........kdk.",
             ".......kgk..",
             "......kgk...",
             ".....kgk....",
             "....kgk.....",
             "...kgk......",
             "..kgk.......",
             ".kkk........"],
    "bras_tatoue": ["kkkkkkkkkkkk",
                    "ksssssssssss",
                    "ksstttsssssk",
                    "kstsstsssssk",
                    "ksstttssssSk",
                    "kssstsssSSSk",
                    "kSSSSSSSSkk.",
                    "kkkkkkkkk..."],
    "reveil": ["..kk....kk..",
               ".krrk..krrk.",
               "..kkkkkkkk..",
               ".kwwwwwwwwk.",
               "kwwwwkwwwwwk",
               "kwwwwkwwwwwk",
               "kwwwwkkkwwwk",
               "kwwwwwwwwwwk",
               ".kwwwwwwwwk.",
               "..kkkkkkkk..",
               ".kk......kk."],
}
ICPAL = dict(k=INK[:3], s=SKIN_S["b"], S=SKIN_S["s"], r=(220, 40, 60), h=(176, 84, 40), p=(240, 120, 170),
             b=(110, 190, 240), w=(240, 248, 255), g=(200, 170, 90), d=(40, 40, 50), t=(40, 60, 110))


def icone2(name):
    rows = ICONS2[name]
    sp = Spr(max(len(r) for r in rows), len(rows))
    stamp(sp, rows, ICPAL, 0, 0)
    return sp


# ---------------------------------------------------------------- cache (un sprite n'est dessiné qu'une fois)
_CACHE = {}


def sprite(who, **kw):
    key = (who, tuple(sorted(kw.items())))
    if key not in _CACHE:
        if who == "P":
            _CACHE[key] = petit(**kw).img()
        elif who == "G":
            _CACHE[key] = grand(**kw).img()
        elif who.startswith("F") and who[1:].isdigit():
            _CACHE[key] = fidele(int(who[1:])).img()
        elif who == "S":
            _CACHE[key] = soeur(**kw).img()
        elif who == "IMAM":
            _CACHE[key] = grand("priere", back=True, gilet=False).img()
        else:                                             # personnages du créateur (cast.py / troupe.py), animaux
            import cast
            import film                                    # orbes (prophètes, figures vénérées) et voix sans corps
            if cast.has(who):
                _CACHE[key] = cast.image(who, **kw)
            elif film.has(who):
                _CACHE[key] = film.image(who, **kw)
            else:
                import animaux
                _CACHE[key] = animaux.image(who, **kw)
    return _CACHE[key]


def is_char(who):
    """Personnage animé (bouche, clignement) : le duo, la sœur, et tous les personnages du créateur."""
    if who in ("P", "G", "S"):
        return True
    import cast
    return cast.has(who)


def anime(who):
    """Sprite qui reçoit un état (pose, marche…) : personnages et animaux."""
    if is_char(who):
        return True
    import animaux
    import film
    return animaux.has(who) or film.has(who)


class _Tops(dict):
    """Haut de la tête sur la toile du sprite ; les personnages du créateur sont calculés à la demande."""
    def get(s, k, d=None):
        if dict.__contains__(s, k):
            return dict.__getitem__(s, k)
        import cast
        return cast.head_top(k) if cast.has(k) else d


HEAD_TOP = _Tops(S=FOOT - 68, P=FOOT - 64, G=FOOT - 73, IMAM=FOOT - 73, F0=FOOT - 73, F1=FOOT - 73, F2=FOOT - 73, F3=FOOT - 73)


def head_top(who, st=None):
    if dict.__contains__(HEAD_TOP, who):
        return HEAD_TOP[who]
    import cast
    if cast.has(who):
        return cast.head_top(who, **(st or {}))
    a = np.array(sprite(who, **{k: v for k, v in (st or {}).items() if k in ("pose", "step")}))
    rows = np.where(a[..., 3].max(axis=1) > 0)[0]
    return int(rows[0]) if len(rows) else 0


# ---------------------------------------------------------------- portrait (vignette des sous-titres)
def portrait(who, face="neutre", talk=False):
    if who not in ("P", "G"):
        import cast
        return cast.portrait(who, face, talk)
    sp = petit("neutre", face, talk) if who == "P" else grand("neutre", face, talk)
    a = sp.a
    y0 = (FOOT - 64) if who == "P" else (FOOT - 73)
    crop = a[max(0, y0 - 1): y0 + 26, 8: 36].copy()
    return crop


if __name__ == "__main__":
    import sys
    from PIL import Image, ImageDraw
    items = []
    for pose, face, kw in [("neutre", "neutre", {}), ("question", "neutre", dict(talk=True)), ("panique", "choc", {}),
                           ("nez", "gene", dict(blush=True, sweat=True)), ("priere", "ferme", {}), ("pointe", "malin", {}),
                           ("ablution", "content", {}), ("neutre", "neutre", dict(back=True))]:
        items.append(petit(pose, face, **kw).img(6))
    for pose, face, kw in [("neutre", "neutre", {}), ("explique", "neutre", dict(talk=True)), ("pointe", "malin", {}),
                           ("the", "blase", {}), ("bras_croises", "malin", {}), ("priere", "ferme", {})]:
        items.append(grand(pose, face, **kw).img(6))
    for k in range(4):
        items.append(fidele(k).img(6))
    cols = 6
    w, h = items[0].size
    sheet = Image.new("RGBA", (cols * w, ((len(items) + cols - 1) // cols) * h), (120, 110, 100, 255))
    for i, im in enumerate(items):
        sheet.alpha_composite(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(sys.argv[1])
