# Le duo en pixel art dessiné à la main : le grand frère (qamis, barbe, calotte) et le petit frère (sweat, casquette).
import numpy as np
from px import Px, OUT

K = OUT
SK, SK2, SKH = (222, 168, 124), (182, 126, 92), (240, 196, 156)
HAIR, HAIR2 = (44, 30, 26), (78, 56, 44)

# ----------------------------------------------------------- visages (moitié gauche, complétée en miroir)
FACE_GRAND = [
    "........kkkkkkkk",
    "......kkwwwwwwww",
    ".....kwwwwwwwwww",
    "....kwwwWwwwwWww",
    "....kwwwwwwwwwww",
    "....kWWWWWWWWWWW",
    "...kbbbbbbbbbbbb",
    "...kbbhhssssssss",
    "...kbhssssssssss",
    "...kssssssssssss",
    "...kssbbbbbsssss",
    "...kssssssssssss",
    "..kksseeeppsssss",
    "..kssseeeppsssss",
    "..ksksssssssssss",
    "..ksksssssssssSs",
    "..kksssssssssSSs",
    "...kbssssssssshh",
    "...kbbssssssssss",
    "...kbbbsssssbbbb",
    "...kbbbbbbbbbmmm",
    "...kbbbbbbbbbbbb",
    "...kbbbbBbbbbbbb",
    "....kbbbbbbbbbbb",
    "....kbbbbbbBbbbb",
    ".....kbbbbbbbbbb",
    "......kbbbbbbbbb",
    ".......kkbbbbbbb",
    ".........kkkbbbb",
    "............kkkk",
]
FACE_PETIT = [
    "......kkkkkkkkkk",
    "....kkccccccccCc",
    "...kcccccCcccccc",
    "..kccccccccccccc",
    "..kccccccccccccc",
    ".kkkkkkkkkkkkkkk",
    "kvvvvvvvvvvvvvvv",
    ".kkvvvvvvvvvvvvv",
    "...kkkkkkkkkkkkk",
    "...kbbssssssssss",
    "...kbsssssssssss",
    "...ksskkkkssssss",
    "..kssseeeppsssss",
    "..kssseeeppsssss",
    "..ksksssssssssss",
    "..ksksssssssssSs",
    "..kkssssssssssss",
    "...kssrsssssssss",
    "...ksssssssssskk",
    "....ksssssssssss",
    ".....kssssssssss",
    "......kkssssssss",
    "........kkkkkkkk",
]
for r in FACE_GRAND + FACE_PETIT:
    assert len(r) == 16, r

PAL = dict(k=K, s=SK, S=SK2, h=SKH, b=HAIR, B=HAIR2, w=(244, 242, 236), W=(204, 200, 194), e=(250, 250, 250),
           p=(30, 20, 24), m=(140, 60, 56), c=(26, 26, 32), C=(70, 70, 84), v=(44, 44, 54), r=(232, 140, 120))


def _face(c, rows, x0, y0):
    """Dessine le visage puis ombre le côté droit (lumière venant de la gauche)."""
    c.sprite(rows, PAL, x0, y0, mirror=True)
    for j in range(len(rows)):
        for i in range(32):
            x, y = x0 + i, y0 + j
            if 0 <= x < c.w and 0 <= y < c.h and i >= 25 and tuple(c.a[y, x]) == SK:
                c.a[y, x] = SK2
            if 0 <= x < c.w and 0 <= y < c.h and i >= 26 and tuple(c.a[y, x]) == HAIR:
                c.a[y, x] = (30, 20, 18)


def _main(c, x, y, r=4):
    m = c.mask_ell(x, y, r + 0.5, r + 1)
    c.shape(m, SK, SK2, SKH, band=2, dith=False)


def _bras(c, x0, y0, x1, y1, col, col2, w=6):
    """Bras (manche) d'épaule (x0,y0) à poignet (x1,y1)."""
    import math
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * w, dx / L * w
    m = c.mask_poly([(x0 + nx, y0 + ny), (x1 + nx * 0.85, y1 + ny * 0.85), (x1 - nx * 0.85, y1 - ny * 0.85), (x0 - nx, y0 - ny)])
    m |= c.mask_ell(x0, y0, w, w)
    c.shape(m, col, col2, band=3)
    return m


def grand(c, x, yb, pose="repos"):
    """Grand frère : pieds en yb, centre x. Hauteur ~ 205 px."""
    hy = yb - 158
    Q, Q2, QH = (238, 234, 222), (196, 190, 176), (252, 250, 244)
    # pieds (sandales)
    for sd in (-1, 1):
        m = c.mask_ell(x + 12 * sd, yb - 3, 11, 4.5)
        c.shape(m, (120, 74, 42), (84, 50, 28), band=2, dith=False)
    # qamis
    body = c.mask_poly([(x - 19, hy + 31), (x + 19, hy + 31), (x + 27, hy + 39), (x + 31, yb - 7), (x - 31, yb - 7), (x - 27, hy + 39)])
    c.shape(body, Q, Q2, QH, band=7)
    for fx in (-14, 6, 20):                                             # plis
        c.line(x + fx * 0.8, hy + 100, x + fx, yb - 9, Q2)
    c.line(x, hy + 36, x, hy + 70, Q2)                                    # patte de boutonnage
    for k in range(4):
        c.px(x + 1, hy + 41 + k * 8, (150, 140, 120)); c.px(x + 1, hy + 42 + k * 8, (150, 140, 120))
    col = c.mask_ell(x, hy + 32, 9, 5)                                    # col rond
    c.fill(col & body, Q2); c.outline(col & ~c.mask_ell(x, hy + 30, 6, 3))
    # cou + tête
    neck = c.mask_rect(x - 6, hy + 26, x + 6, hy + 33); c.shape(neck, SK, SK2, band=2, dith=False)
    _face(c, FACE_GRAND, x - 16, hy)
    # bras
    if pose == "pointe":                                                  # montre vers la gauche (vers son frère)
        _bras(c, x + 25, hy + 42, x + 29, hy + 88, Q, Q2)
        _main(c, x + 29, hy + 92)
        _bras(c, x - 24, hy + 42, x - 58, hy + 56, Q, Q2)
        _main(c, x - 62, hy + 58)
        c.line(x - 66, hy + 57, x - 72, hy + 55, K); c.line(x - 66, hy + 58, x - 71, hy + 57, SK)   # index tendu
    elif pose == "explique":                                              # main ouverte devant lui
        _bras(c, x + 25, hy + 42, x + 29, hy + 88, Q, Q2)
        _main(c, x + 29, hy + 92)
        _bras(c, x - 24, hy + 42, x - 36, hy + 68, Q, Q2)
        _main(c, x - 32, hy + 72, r=5)
    else:
        for sd in (-1, 1):
            _bras(c, x + 25 * sd, hy + 42, x + 29 * sd, hy + 88, Q, Q2)
            _main(c, x + 29 * sd, hy + 92)


def petit(c, x, yb, pose="repos"):
    """Petit frère : hauteur ~ 172 px."""
    hy = yb - 132
    R, R2, RH = (214, 52, 52), (160, 32, 40), (238, 96, 86)
    J, J2 = (64, 96, 168), (42, 64, 120)
    for sd in (-1, 1):                                                    # baskets
        m = c.mask_ell(x + 10 * sd, yb - 4, 10, 5)
        c.shape(m, (246, 246, 246), (196, 196, 204), band=2, dith=False)
        c.line(x + 10 * sd - 8, yb - 1, x + 10 * sd + 8, yb - 1, (150, 150, 160))
        leg = c.mask_rect(x + 9 * sd - 7, hy + 84, x + 9 * sd + 7, yb - 7)  # jambes du jean
        c.shape(leg, J, J2, band=3)
    hood = c.mask_poly([(x - 17, hy + 24), (x + 17, hy + 24), (x + 24, hy + 31), (x + 25, hy + 88), (x - 25, hy + 88), (x - 24, hy + 31)])
    c.shape(hood, R, R2, RH, band=6)
    c.fill(c.mask_rect(x - 25, hy + 83, x + 25, hy + 88), R2)              # bas côtelé
    pk = c.mask_rrect(x - 12, hy + 60, x + 12, hy + 78, 3); c.fill(pk, R2); c.outline(pk & ~c.mask_rect(x - 11, hy + 60, x + 11, hy + 62))
    for sd in (-1, 1):                                                    # cordons
        c.line(x + 4 * sd, hy + 29, x + 5 * sd, hy + 46, (248, 248, 248))
        c.px(x + 5 * sd, hy + 47, (210, 210, 210))
    c.fill(c.mask_ell(x, hy + 26, 12, 6) & hood, R2)                       # capuche dans le dos
    neck = c.mask_rect(x - 5, hy + 20, x + 5, hy + 27); c.shape(neck, SK, SK2, band=2, dith=False)
    _face(c, FACE_PETIT, x - 16, hy)
    if pose == "question":                                                # main levée, paume ouverte
        _bras(c, x - 22, hy + 36, x - 26, hy + 74, R, R2, w=5)
        _main(c, x - 26, hy + 78)
        _bras(c, x + 22, hy + 36, x + 40, hy + 8, R, R2, w=5)
        _main(c, x + 41, hy + 3, r=5)
    else:
        for sd in (-1, 1):
            _bras(c, x + 22 * sd, hy + 36, x + 26 * sd, hy + 74, R, R2, w=5)
            _main(c, x + 26 * sd, hy + 78)
