# Décors détaillés (270x480 pixels, agrandis x4) pour la série « VALABLE OU PAS ? » en dialogue.
# Chaque décor renvoie (fond RGB, avant-plan RGBA ou None).
import math, random
import numpy as np
from px import Px, OUT, INK, BAYER

R = random.Random


def zellige_band(c, y0, y1, seed=1, cols=((236, 230, 214), (28, 110, 140), (24, 120, 96), (226, 176, 70), (170, 50, 50))):
    """Frise de zellige : étoiles à 8 branches sur carreaux 10x10."""
    T = ["wwwwgwwwww",
         "wwwgygwwww",
         "wwgyyygwww",
         "wgyybyygww",
         "gyybbbyygw",
         "wgyybyygww",
         "wwgyyygwww",
         "wwwgygwwww",
         "wwwwgwwwww",
         "wwwwwwwwww"]
    pal = dict(w=cols[0], g=cols[1], y=cols[3], b=cols[4])
    for ty in range(y0, y1, 10):
        for tx in range(0, c.w, 10):
            alt = ((tx // 10) + (ty // 10)) % 2
            p = dict(pal); p["g"] = cols[1] if alt else cols[2]
            c.sprite([r[:max(0, min(10, c.w - tx))] for r in T[:max(0, min(10, y1 - ty))]], p, tx, ty)


def books(c, x0, x1, y_base, h0=16, h1=24, seed=3):
    rnd = R(seed)
    x = x0
    pal = [(150, 40, 46), (30, 90, 70), (40, 60, 120), (180, 140, 60), (110, 70, 40), (90, 40, 90), (200, 190, 170)]
    while x < x1 - 3:
        w = rnd.choice((3, 4, 4, 5))
        h = rnd.randint(h0, h1)
        col = rnd.choice(pal)
        if rnd.random() < 0.1 and x + 8 < x1:                         # livre penché
            m = c.mask_poly([(x, y_base), (x + 4, y_base), (x + 9, y_base - h + 3), (x + 5, y_base - h + 1)])
            c.shape(m, col, tuple(int(v * 0.75) for v in col), ol=True)
            x += 10
            continue
        m = c.mask_rect(x, y_base - h, x + w, y_base)
        c.shape(m, col, tuple(int(v * 0.72) for v in col), tuple(min(255, int(v * 1.25)) for v in col), band=1)
        if w >= 4:                                                    # titre doré
            c.fill(c.mask_rect(x + 1, y_base - h + 4, x + w - 1, y_base - h + 5), (226, 186, 90))
        x += w + 1


def cushion_row(c, y0, y1, x0=0, x1=None, base=(150, 34, 44), stripe=(222, 172, 70), seed=2):
    x1 = c.w if x1 is None else x1
    rnd = R(seed)
    x = x0 - 6
    while x < x1:
        w = rnd.randint(38, 46)
        m = c.mask_rrect(x, y0, x + w, y1, 7)
        c.shape(m, base, tuple(int(v * 0.7) for v in base), tuple(min(255, int(v * 1.25)) for v in base), band=3)
        for k, yy in enumerate(range(y0 + 8, y1 - 4, 7)):
            c.fill(m & c.mask_rect(x + 3, yy, x + w - 3, yy + 1), stripe if k % 2 == 0 else (90, 24, 34))
        c.fill(m & c.mask_rect(x + w // 2 - 1, y0 + 4, x + w // 2 + 1, y1 - 6), tuple(int(v * 0.8) for v in base))
        x += w - 2


def lantern(c, cx, top, size=1.0):
    """Lanterne marocaine en laiton (fanous) + verres colorés + halo."""
    c.line(cx, 0, cx, top, (120, 84, 44))
    for k in range(0, top, 4):
        c.px(cx, k, (168, 124, 60))
    s = size
    cap = c.mask_poly([(cx - 9 * s, top + 8 * s), (cx + 9 * s, top + 8 * s), (cx + 3 * s, top), (cx - 3 * s, top)])
    c.shape(cap, (214, 162, 70), (160, 112, 40), (246, 210, 120), band=2)
    body = c.mask_poly([(cx - 11 * s, top + 8 * s), (cx + 11 * s, top + 8 * s), (cx + 13 * s, top + 26 * s),
                        (cx + 6 * s, top + 40 * s), (cx - 6 * s, top + 40 * s), (cx - 13 * s, top + 26 * s)])
    c.shape(body, (196, 140, 54), (140, 96, 34), (240, 196, 110), band=2)
    glass = [(250, 210, 120), (230, 110, 80), (120, 200, 160), (250, 230, 160)]
    for i, gx in enumerate((-8, -3, 2, 7)):
        g = c.mask_rect(cx + gx * s, top + 12 * s, cx + (gx + 3) * s, top + 33 * s) & body
        c.fill(g, glass[i])
        for yy in range(int(top + 13 * s), int(top + 33 * s), 4):
            c.px(cx + gx * s + 1, yy, (255, 248, 220))
    c.fill(c.mask_poly([(cx - 4 * s, top + 40 * s), (cx + 4 * s, top + 40 * s), (cx, top + 48 * s)]), (196, 140, 54))
    c.outline(c.mask_poly([(cx - 4 * s, top + 40 * s), (cx + 4 * s, top + 40 * s), (cx, top + 48 * s)]))


def star_light(c, cx, cy, n=60, r0=30, r1=150, seed=7, col=(255, 214, 140), m=None):
    """Petites étoiles de lumière projetées par la lanterne sur les murs."""
    rnd = R(seed)
    for _ in range(n):
        a = rnd.uniform(0, 6.283); r = rnd.uniform(r0, r1)
        x, y = int(cx + math.cos(a) * r), int(cy + math.sin(a) * r * 0.8)
        if m is not None and not (0 <= x < c.w and 0 <= y < c.h and m[y, x]):
            continue
        c.px(x, y, col)
        if rnd.random() < 0.4:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if rnd.random() < 0.6:
                    c.px(x + dx, y + dy, tuple(int(v * 0.85) for v in col))


def rug(c, y0, y1, cx=135, wtop=170, wbot=330, cols=((150, 32, 40), (30, 40, 90), (226, 196, 140), (210, 150, 60))):
    """Tapis à motifs en perspective (calcul par pixel)."""
    base, navy, cream, gold = [np.array(v) for v in cols]
    yy, xx = c.yy, c.xx
    t = np.clip((yy - y0) / max(1, y1 - y0), 0, 1)
    half = (wtop + (wbot - wtop) * t) / 2
    inside = (yy >= y0) & (yy < y1) & (np.abs(xx - cx) <= half)
    u = (xx - cx) / np.maximum(half, 1)                       # -1..1 en largeur
    z = 1.0 / (0.35 + t)                                      # profondeur
    v = (z - 1 / 1.35) / (1 / 0.35 - 1 / 1.35)                # 0 (près) .. 1 (loin)
    img = np.zeros((c.h, c.w, 3)); img[:] = base
    border = (np.abs(u) > 0.84) | (v > 0.9) | (v < 0.06)
    img[border] = navy
    fine = ((np.abs(u) > 0.80) & (np.abs(u) < 0.84)) | ((np.abs(u) > 0.9) & (np.abs(u) < 0.93))
    img[fine] = gold
    med = (np.abs(u) * 3.0) ** 2 + ((v - 0.5) * 5.0) ** 2
    img[(med < 1.0) & ~border] = navy
    img[(med < 0.55) & ~border] = cream
    img[(med < 0.25) & ~border] = base
    diam = (np.abs((u * 6) % 2 - 1) + np.abs((v * 9) % 2 - 1)) < 0.35
    img[diam & ~border & (med > 1.05)] = gold * 0.85
    c.a[inside] = img[inside].astype(np.uint8)
    c.outline(inside)


# =================================================================== SALON (le repaire des deux frères)
def salon():
    c = Px()
    wall = c.mask_rect(0, 0, 270, 305)
    c.vgrad(wall, 0, 300, (92, 52, 46), (196, 126, 88), steps=8)
    # poutre du plafond
    c.shape(c.mask_rect(0, 0, 270, 9), (84, 52, 36), (60, 36, 26), band=2, sdir="bottom")
    for x in range(4, 270, 12):
        c.fill(c.mask_rect(x, 3, x + 6, 5), (120, 80, 50))
    # fenêtre en arc : nuit, lune, ville
    win = c.mask_arch(26, 112, 50, 190)
    c.vgrad(win, 50, 190, (14, 18, 52), (60, 52, 112), steps=6)
    rnd = R(11)
    for _ in range(26):
        x, y = rnd.randint(30, 108), rnd.randint(58, 150)
        if win[y, x]:
            c.px(x, y, (230, 230, 255) if rnd.random() < 0.5 else (150, 150, 210))
    moon = c.mask_ell(88, 86, 9, 9) & ~c.mask_ell(92, 83, 8, 8)
    c.fill(moon & win, (252, 240, 200))
    for k, (x0, w, h) in enumerate([(26, 14, 34), (40, 10, 50), (50, 18, 28), (68, 9, 58), (77, 15, 40), (92, 20, 30)]):
        b = c.mask_rect(x0, 190 - h, x0 + w, 190) & win
        c.fill(b, (22, 22, 46) if k % 2 else (30, 28, 58))
        for yy in range(190 - h + 4, 188, 5):
            for xx in range(x0 + 2, x0 + w - 1, 3):
                if rnd.random() < 0.45:
                    c.px(xx, yy, (250, 214, 110))
    c.fill(c.mask_rect(26, 118, 112, 120) & win, (110, 66, 40)); c.fill(c.mask_rect(68, 50, 70, 190) & win, (110, 66, 40))
    c.outline(win, (70, 40, 28))
    c.shape(c.mask_rect(20, 189, 118, 196), (130, 84, 54), (96, 60, 40), (160, 110, 74), band=2, sdir="bottom")
    c.glow(68, 120, 60, (120, 120, 210), 0.25)
    # rideaux
    for x0, x1 in ((10, 30), (108, 128)):
        cur = c.mask_rect(x0, 40, x1, 246) & ~c.mask_poly([(x0 + (x1 - x0) // 2, 170), (x1 + 4, 140), (x1 + 4, 200)] if x0 < 60 else
                                                           [(x0 + (x1 - x0) // 2, 170), (x0 - 4, 140), (x0 - 4, 200)])
        c.shape(cur, (140, 28, 40), (98, 18, 30), (178, 54, 60), band=2)
        for fx in range(x0 + 4, x1 - 2, 5):
            c.fill(cur & c.mask_rect(fx, 44, fx + 1, 246), (110, 22, 34))
        c.shape(c.mask_rect(x0 + 2, 166, x1 - 2, 171), (226, 180, 80), (170, 124, 50), band=1)
    c.shape(c.mask_rect(4, 36, 134, 41), (170, 124, 60), (120, 84, 40), (214, 170, 90), band=1)     # tringle
    # cadre calligraphie (motif abstrait, aucun texte réel)
    fr = c.mask_rect(142, 64, 178, 118)
    c.shape(fr, (210, 166, 70), (150, 110, 40), (246, 208, 120), band=2)
    inner = c.mask_rect(146, 68, 174, 114)
    c.fill(inner, (24, 70, 58))
    rnd = R(5)
    for _ in range(9):
        x, y = rnd.randint(149, 168), rnd.randint(72, 106)
        c.line(x, y, x + rnd.randint(3, 6), y + rnd.randint(-3, 3), (230, 190, 100))
    c.line(150, 100, 170, 100, (230, 190, 100)); c.line(152, 82, 168, 82, (230, 190, 100))
    # bibliothèque
    sh = c.mask_rect(186, 60, 264, 214)
    c.shape(sh, (104, 64, 40), (76, 44, 28), (132, 86, 54), band=3)
    c.fill(c.mask_rect(190, 64, 260, 210), (62, 36, 24))
    for k, yb in enumerate((98, 136, 174, 210)):
        books(c, 191, 259, yb - 1, 18, 28, seed=20 + k)
        c.shape(c.mask_rect(188, yb - 1, 262, yb + 2), (124, 80, 50), (90, 56, 34), (150, 104, 66), band=1, sdir="bottom")
    vase = c.mask_ell(250, 122, 5, 7); c.shape(vase, (40, 110, 140), (24, 76, 100), (90, 170, 200), band=2)
    c.fill(c.mask_rect(248, 111, 252, 116), (40, 110, 140)); c.outline(c.mask_rect(248, 111, 252, 116))
    # frise de zellige
    zellige_band(c, 200, 240, seed=1)
    c.shape(c.mask_rect(0, 196, 270, 200), (24, 100, 84), (16, 70, 60), band=1, sdir="bottom")
    for x in range(2, 270, 6):
        c.px(x, 198, (226, 186, 90))
    # lanterne + étoiles de lumière + halo
    star_light(c, 150, 70, n=90, r0=40, r1=150, m=wall & ~win & ~sh)
    lantern(c, 150, 24, size=1.0)
    c.glow(150, 50, 150, (255, 200, 120), 0.32)
    # banquette (sedari)
    cushion_row(c, 222, 264)
    seat = c.mask_rect(0, 258, 270, 284)
    c.shape(seat, (176, 46, 54), (126, 30, 40), (210, 84, 82), band=3, sdir="bottom")
    for x in range(0, 270, 22):
        c.fill(seat & c.mask_rect(x, 262, x + 1, 282), (140, 34, 44))
    base = c.mask_rect(0, 284, 270, 306)
    c.shape(base, (96, 58, 36), (66, 40, 26), (126, 82, 52), band=2, sdir="bottom")
    for x in range(6, 270, 14):
        c.fill(c.mask_poly([(x, 288), (x + 6, 288), (x + 3, 300)]), (120, 76, 46))
    # sol + tapis
    floor = c.mask_rect(0, 306, 270, 480)
    c.vgrad(floor, 306, 480, (120, 76, 56), (150, 98, 70), steps=5)
    for y in range(312, 480, 18):
        c.fill(floor & c.mask_rect(0, y, 270, y + 1), (106, 66, 48))
    rug(c, 318, 480, wtop=210, wbot=380)
    # plante en pot (coin gauche)
    pot = c.mask_poly([(6, 286), (30, 286), (27, 306), (9, 306)])
    c.shape(pot, (186, 96, 60), (140, 66, 40), (214, 130, 90), band=2)
    rnd = R(9)
    for _ in range(14):
        a = rnd.uniform(-2.6, -0.5); L = rnd.randint(16, 34)
        x2, y2 = 18 + math.cos(a) * L, 286 + math.sin(a) * L
        leaf = c.mask_ell((18 + x2) / 2, (286 + y2) / 2, 3.5, L / 2.2)
        c.shape(leaf, (54, 130, 64), (34, 92, 46), (96, 170, 90), band=1)
    c.glow(150, 50, 260, (255, 190, 120), 0.12)

    # ---- avant-plan : table basse (meida) + plateau de thé
    f = Px(alpha=True)
    tray = f.mask_ell(135, 446, 112, 30)
    f.shape(tray, (196, 120, 60), (150, 84, 40), (232, 170, 96), band=3, sdir="bottom")
    for r in (0.82, 0.6, 0.38):
        e = f.mask_ell(135, 446, 112 * r, 30 * r) & ~f.mask_ell(135, 446, 112 * r - 2, 30 * r - 1)
        f.fill(e, (214, 146, 74))
    f.fill(f.mask_rect(30, 470, 240, 480) & ~tray, (84, 50, 32)); f.al[f.mask_rect(30, 470, 240, 480)] = True
    # théière
    pot = f.mask_ell(104, 430, 16, 13)
    f.shape(pot, (206, 210, 220), (150, 156, 170), (244, 246, 250), band=3)
    lid = f.mask_ell(104, 416, 8, 4); f.shape(lid, (206, 210, 220), (150, 156, 170), band=1)
    f.shape(f.mask_ell(104, 410, 3, 3), (226, 186, 90), (170, 130, 50), band=1)
    sp = f.mask_poly([(118, 428), (124, 426), (136, 412), (138, 414), (126, 432)])
    f.shape(sp, (206, 210, 220), (150, 156, 170), band=1)
    hd = f.mask_ell(86, 428, 6, 9) & ~f.mask_ell(86, 428, 4, 7)
    f.shape(hd, (190, 194, 206), (140, 146, 160), band=1)
    # verres de thé
    for gx in (148, 166, 184):
        g = f.mask_poly([(gx, 420), (gx + 11, 420), (gx + 9, 444), (gx + 2, 444)])
        f.fill(g, (204, 232, 240))
        f.fill(g & f.mask_rect(gx, 428, gx + 12, 444), (176, 98, 36))
        f.fill(g & f.mask_rect(gx + 2, 430, gx + 3, 442), (232, 160, 84))
        f.fill(g & f.mask_rect(gx + 1, 424, gx + 10, 425), (226, 186, 90))
        f.outline(g)
    # assiette de dattes
    pl = f.mask_ell(212, 444, 20, 7); f.shape(pl, (236, 232, 222), (196, 190, 176), band=1)
    for k, (dx, dy) in enumerate(((-9, -3), (-3, -4), (4, -3), (10, -2), (-6, 0), (2, 0), (8, 1))):
        d = f.mask_ell(212 + dx, 442 + dy, 3.4, 2.2)
        f.shape(d, (110, 54, 30), (78, 36, 20), (150, 84, 50), band=1)
    return c, f


def carpet_rows(c, y0, y1, horizon, cx=135, base=(146, 28, 38), dark=(108, 18, 30), gold=(214, 168, 70), green=(24, 96, 74),
                row_len=1.0, cell=0.62):
    """Moquette de mosquée : rangées parallèles au mur de la qibla, motif d'arc répété, vue en perspective."""
    yy, xx = c.yy, c.xx
    m = (yy >= y0) & (yy < y1)
    dz = np.maximum(yy - horizon, 1).astype(float)
    z = 420.0 / dz                                         # profondeur (grand = loin)
    xw = (xx - cx) * z / 105.0
    row = z / row_len
    fr = row - np.floor(row)                               # 0..1 dans la rangée (0 = devant)
    cu = (xw / cell) - np.floor(xw / cell)                 # 0..1 dans la case
    img = np.zeros((c.h, c.w, 3)); img[:] = base
    sep = fr < 0.07
    img[sep] = gold
    img[(fr >= 0.07) & (fr < 0.12)] = dark
    # arc de prière dans chaque case : piliers + voûte
    ux = np.abs(cu - 0.5) * 2                              # 0 au centre, 1 au bord
    pil = (ux > 0.78) & (ux < 0.92) & (fr > 0.12) & (fr < 0.8)
    vault = (np.abs(np.sqrt(ux ** 2 + ((fr - 0.8) / 0.18) ** 2) - 0.85) < 0.08) & (fr >= 0.8)
    img[pil | vault] = dark
    inner = (ux < 0.6) & (fr > 0.25) & (fr < 0.75)
    img[inner & (((xx + yy) % 3) == 0)] = np.array(base) * 0.9
    img[(ux < 0.12) & (fr > 0.35) & (fr < 0.62)] = green
    c.a[m] = img[m].astype(np.uint8)


def chandelier(c, cx, y_top, chain_y=0, rx=34, ry=7):
    c.line(cx, chain_y, cx, y_top, (150, 110, 50))
    for sgn in (-1, 1):
        c.line(cx, y_top, cx + sgn * rx * 0.8, y_top + 18, (170, 126, 56))
    ring = c.mask_ell(cx, y_top + 20, rx, ry) & ~c.mask_ell(cx, y_top + 20, rx - 3, ry - 2)
    c.shape(ring, (214, 164, 72), (160, 112, 40), (246, 210, 120), band=1)
    for k in range(10):
        a = k / 10 * 2 * math.pi
        x, y = cx + math.cos(a) * rx, y_top + 20 + math.sin(a) * ry
        if math.sin(a) > -0.2:
            bulb = c.mask_ell(x, y - 3, 2.2, 3)
            c.fill(bulb, (255, 240, 190)); c.outline(bulb, (150, 110, 50))
    hub = c.mask_ell(cx, y_top + 22, 6, 5); c.shape(hub, (214, 164, 72), (160, 112, 40), band=1)
    c.glow(cx, y_top + 20, 70, (255, 230, 170), 0.35)


def mosquee():
    c = Px()
    H0 = 300                                    # pied du mur de la qibla
    wall = c.mask_rect(0, 0, 270, H0)
    c.vgrad(wall, 0, H0, (214, 198, 172), (240, 228, 206), steps=6)
    # plafond à caissons
    ceil = c.mask_rect(0, 0, 270, 46)
    c.vgrad(ceil, 0, 46, (120, 86, 60), (160, 120, 84), steps=4)
    for x in range(0, 270, 30):
        c.shape(c.mask_rect(x + 3, 4, x + 27, 38), (146, 106, 72), (118, 82, 56), (178, 138, 96), band=2, ol=False)
        c.fill(c.mask_ell(x + 15, 21, 5, 5), (210, 164, 80))
    c.shape(c.mask_rect(0, 44, 270, 52), (24, 100, 84), (16, 70, 60), band=1, sdir="bottom")
    for x in range(2, 270, 5):
        c.px(x, 47, (226, 186, 90)); c.px(x + 2, 49, (226, 186, 90))
    # vitraux en hauteur
    for wx in (40, 230):
        w = c.mask_arch(wx - 14, wx + 14, 64, 128)
        c.vgrad(w, 64, 128, (60, 110, 190), (30, 70, 140), steps=4)
        for yy in range(70, 128, 10):                                   # losanges or / turquoise
            for xx in range(wx - 12, wx + 14, 8):
                d = c.mask_poly([(xx, yy - 4), (xx + 4, yy), (xx, yy + 4), (xx - 4, yy)]) & w
                c.fill(d, (232, 192, 96) if ((xx + yy) // 8) % 2 else (90, 190, 190))
                c.px(xx, yy, (250, 240, 200))
        c.fill(w & c.mask_rect(wx - 14, 96, wx + 14, 97), (90, 60, 40))
        c.fill(w & c.mask_rect(wx, 64, wx + 1, 128), (90, 60, 40))
        c.outline(w, (90, 60, 40))
        c.glow(wx, 96, 46, (255, 236, 190), 0.3)
    # arcades (colonnes du milieu)
    for ax in (62, 208):
        col = c.mask_rect(ax - 6, 150, ax + 6, H0)
        c.shape(col, (232, 222, 204), (196, 184, 162), (248, 242, 230), band=2)
        cap = c.mask_rect(ax - 9, 146, ax + 9, 153); c.shape(cap, (214, 170, 84), (164, 124, 54), band=1, sdir="bottom")
        base = c.mask_rect(ax - 9, H0 - 8, ax + 9, H0); c.shape(base, (200, 188, 168), (164, 150, 130), band=1)
    for x0, x1 in ((62, 208),):
        arch = c.mask_arch(x0 + 4, x1 - 4, 62, 150) & ~c.mask_arch(x0 + 8, x1 - 8, 66, 151)
        c.fill(arch & c.mask_rect(0, 56, 270, 150), (24, 100, 84))
        c.fill(c.mask_arch(x0 + 8, x1 - 8, 66, 151) & ~c.mask_arch(x0 + 10, x1 - 10, 68, 152) & c.mask_rect(0, 56, 270, 150), (226, 182, 84))
    # mihrab
    mx0, mx1, mtop = 104, 166, 120
    outer = c.mask_arch(mx0 - 8, mx1 + 8, mtop - 10, H0, pointed=0.25)
    c.shape(outer, (34, 90, 150), (24, 64, 112), band=1)
    for k, yy in enumerate(range(mtop - 6, H0, 6)):                     # bordure de zellige
        for xx in range(mx0 - 8, mx1 + 9, 6):
            if outer[min(479, yy), min(269, xx)]:
                c.px(xx + 1, yy + 1, (236, 230, 214)); c.px(xx + 2, yy + 1, (226, 176, 70))
    gold = c.mask_arch(mx0 - 2, mx1 + 2, mtop - 4, H0, pointed=0.25) & ~c.mask_arch(mx0 + 1, mx1 - 1, mtop - 1, H0, pointed=0.25)
    c.fill(gold, (226, 182, 84))
    niche = c.mask_arch(mx0 + 1, mx1 - 1, mtop - 1, H0, pointed=0.25)
    c.vgrad(niche, mtop, H0, (16, 64, 56), (30, 104, 86), steps=5)
    for yy in range(mtop + 30, H0 - 6, 12):                            # mosaïque d'étoiles
        for xx in range(mx0 + 8, mx1 - 6, 12):
            if niche[yy, xx]:
                c.fill(c.mask_poly([(xx, yy - 4), (xx + 4, yy), (xx, yy + 4), (xx - 4, yy)]) & niche, (226, 182, 84))
                c.px(xx, yy, (30, 104, 86))
    lamp = c.mask_ell(135, mtop + 32, 5, 6); c.line(135, mtop + 6, 135, mtop + 26, (226, 182, 84))
    c.shape(lamp, (240, 200, 110), (190, 140, 60), band=1); c.glow(135, mtop + 32, 26, (255, 230, 160), 0.45, m=niche)
    # bandeau de calligraphie (motif abstrait, aucun texte réel)
    cal = c.mask_rect(mx0 - 24, mtop - 40, mx1 + 24, mtop - 22)
    c.shape(cal, (24, 70, 58), (16, 50, 42), band=1)
    for x in range(mx0 - 22, mx1 + 22, 8):
        c.line(x, mtop - 31, x + 4, mtop - 35, (232, 194, 104)); c.line(x + 4, mtop - 35, x + 8, mtop - 31, (232, 194, 104))
        c.line(x, mtop - 31, x + 4, mtop - 27, (232, 194, 104)); c.line(x + 4, mtop - 27, x + 8, mtop - 31, (232, 194, 104))
        c.px(x + 4, mtop - 31, (240, 210, 130))
    # minbar (escalier en bois à droite du mihrab)
    mb = c.mask_poly([(172, H0), (172, 228), (184, 228), (206, 272), (206, H0)])
    c.shape(mb, (130, 82, 46), (96, 58, 32), (164, 110, 66), band=2)
    for k in range(6):
        c.line(184 + k * 4, 232 + k * 8, 206, 232 + k * 8, (96, 58, 32))
    dome = c.mask_ell(178, 220, 7, 6) & c.mask_rect(170, 212, 186, 221); c.shape(dome, (214, 168, 76), (160, 116, 48), band=1)
    c.shape(c.mask_rect(172, 220, 184, 228), (150, 98, 58), (110, 70, 40), band=1)
    # tableau des horaires de prière (chiffres LED)
    bd = c.mask_rect(70, 176, 98, 222)
    c.shape(bd, (40, 30, 34), (24, 18, 22), band=1)
    times = ["05:42", "13:05", "15:48", "18:21", "19:47", "06:58"]
    for k, tt in enumerate(times):
        y = 179 + k * 7
        for i, ch in enumerate(tt):
            x = 73 + i * 4 + (1 if i > 2 else 0)
            if ch != ":":
                c.fill(c.mask_rect(x, y, x + 3, y + 5), (90, 20, 20))
                c.fill(c.mask_rect(x, y + 1, x + 2, y + 4), (240, 70, 60))
            else:
                c.px(x + 1, y + 1, (240, 70, 60)); c.px(x + 1, y + 3, (240, 70, 60))
    c.outline(bd)
    # étagère de Corans (près de la colonne gauche)
    shelf = c.mask_rect(28, 248, 56, 300); c.shape(shelf, (120, 78, 44), (88, 56, 32), band=2)
    for yb in (268, 290):
        books(c, 30, 55, yb, 14, 17, seed=yb)
        c.fill(c.mask_rect(28, yb, 56, yb + 2), (96, 62, 36))
    # sol : moquette à rangées
    carpet_rows(c, H0, 480, horizon=236)
    c.fill(c.mask_rect(0, H0, 270, H0 + 2), (110, 76, 52))
    # grandes colonnes au premier plan (cadre)
    for x0, x1, sd in ((0, 20, "right"), (250, 270, "left")):
        col = c.mask_rect(x0, 0, x1, 480)
        c.shape(col, (236, 226, 208), (196, 182, 160), (252, 248, 238), band=4, sdir=sd, ldir="left" if sd == "right" else "right")
        for yy in (150, 156):
            c.fill(c.mask_rect(x0, yy, x1, yy + 3), (214, 170, 84))
    # rayons de lumière depuis les vitraux
    for wx, d in ((40, 1), (230, -1)):
        ray = c.mask_poly([(wx - 8, 128), (wx + 8, 128), (wx + 8 + d * 70, 480), (wx - 30 + d * 70, 480)])
        c.tint(ray & ~c.mask_rect(0, 0, 20, 480) & ~c.mask_rect(250, 0, 270, 480) & c.mask_rect(0, 0, 270, 300), (255, 244, 214), 0.08)
    chandelier(c, 135, 60, chain_y=40)
    c.glow(135, 250, 220, (255, 236, 200), 0.10)
    return c, None


def planks(c, y0, y1, horizon, cx=135, col=(150, 100, 62), dark=(112, 72, 44), light=(176, 124, 80)):
    """Parquet en perspective."""
    yy, xx = c.yy, c.xx
    m = (yy >= y0) & (yy < y1)
    dz = np.maximum(yy - horizon, 1).astype(float)
    z = 420.0 / dz
    xw = (xx - cx) * z / 105.0
    img = np.zeros((c.h, c.w, 3)); img[:] = col
    seam = ((xw / 0.5) - np.floor(xw / 0.5)) < 0.06
    img[seam] = dark
    off = np.floor(xw / 0.5) * 0.37
    cross = (((z + off) / 2.2) - np.floor((z + off) / 2.2)) < 0.025
    img[cross] = dark
    grain = (((xw * 9 + z * 2) - np.floor(xw * 9 + z * 2)) < 0.12) & ~seam
    img[grain & ((xx + yy) % 2 == 0)] = light
    c.a[m] = img[m].astype(np.uint8)


def tableau():
    c = Px()
    wall = c.mask_rect(0, 0, 270, 318)
    c.vgrad(wall, 0, 318, (176, 196, 172), (214, 224, 198), steps=6)
    for x in range(0, 270, 18):                                          # papier peint à rayures
        c.fill(wall & c.mask_rect(x, 0, x + 2, 300), (196, 212, 186))
    # horloge
    clk = c.mask_ell(135, 34, 13, 13)
    c.shape(clk, (246, 244, 236), (206, 202, 192), band=1); c.outline(c.mask_ell(135, 34, 15, 15) & ~clk, (90, 60, 40))
    c.line(135, 34, 135, 25, INK); c.line(135, 34, 142, 37, INK)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        c.px(135 + round(math.cos(a) * 10), 34 + round(math.sin(a) * 10), (90, 80, 70))
    # tableau noir (vert) avec cadre en bois
    fr = c.mask_rect(14, 60, 256, 262)
    c.shape(fr, (128, 84, 48), (92, 58, 32), (162, 112, 70), band=3)
    bd = c.mask_rect(22, 68, 248, 252)
    c.vgrad(bd, 68, 252, (30, 70, 58), (40, 86, 70), steps=4)
    rnd = R(17)
    for _ in range(6):                                                  # traces de craie effacée
        x, y = rnd.randint(30, 230), rnd.randint(80, 240)
        c.dither(c.mask_ell(x, y, rnd.randint(14, 30), rnd.randint(4, 8)) & bd, (64, 104, 88), 0.3)
    tray = c.mask_rect(18, 252, 252, 258); c.shape(tray, (140, 94, 56), (100, 66, 38), band=1, sdir="bottom")
    for x, col in ((60, (246, 246, 240)), (70, (240, 220, 120)), (200, (246, 246, 240))):
        c.fill(c.mask_rect(x, 249, x + 7, 252), col); c.outline(c.mask_rect(x, 249, x + 7, 252))
    er = c.mask_rect(150, 245, 168, 252); c.shape(er, (60, 60, 80), (40, 40, 56), band=1)
    c.fill(c.mask_rect(150, 250, 168, 252), (210, 210, 210))
    # soubassement en bois
    c.shape(c.mask_rect(0, 296, 270, 320), (120, 80, 50), (88, 58, 36), (150, 104, 66), band=2, sdir="bottom")
    for x in range(0, 270, 30):
        c.fill(c.mask_rect(x, 298, x + 1, 318), (96, 64, 40))
    planks(c, 320, 480, horizon=250)
    c.glow(135, 140, 200, (255, 250, 230), 0.10)
    return c, None


def ablutions():
    c = Px()
    wall = c.mask_rect(0, 0, 270, 330)
    c.vgrad(wall, 0, 220, (234, 212, 176), (246, 230, 200), steps=6)
    # fenêtres en arc + lumière
    for wx in (45, 135, 225):
        w = c.mask_arch(wx - 20, wx + 20, 40, 150)
        c.vgrad(w, 40, 150, (210, 238, 252), (140, 196, 236), steps=5)
        for gx in (wx - 7, wx + 7):
            c.fill(w & c.mask_rect(gx - 1, 30, gx + 1, 150), (130, 90, 56))
        c.fill(w & c.mask_rect(wx - 20, 96, wx + 20, 98), (130, 90, 56))
        c.outline(w, (110, 72, 46))
        c.shape(c.mask_rect(wx - 24, 150, wx + 24, 156), (214, 182, 140), (176, 144, 104), band=1, sdir="bottom")
        c.glow(wx, 100, 60, (255, 250, 230), 0.25)
    # lanternes murales
    for lx in (90, 180):
        c.shape(c.mask_rect(lx - 2, 150, lx + 2, 160), (120, 84, 44), (90, 60, 30), band=1)
        lan = c.mask_poly([(lx - 6, 160), (lx + 6, 160), (lx + 7, 172), (lx, 180), (lx - 7, 172)])
        c.shape(lan, (232, 182, 70), (176, 120, 40), (252, 226, 140), band=1)
        c.glow(lx, 170, 30, (255, 220, 150), 0.4)
    # frise de zellige
    zellige_band(c, 210, 300, seed=3, cols=((240, 236, 222), (24, 118, 140), (30, 130, 104), (226, 176, 70), (60, 80, 150)))
    c.shape(c.mask_rect(0, 204, 270, 210), (24, 110, 120), (16, 76, 84), band=1, sdir="bottom")
    for x in range(2, 270, 6):
        c.px(x, 207, (226, 186, 90))
    # robinets + filets d'eau
    for k, x in enumerate(range(22, 270, 45)):
        pipe = c.mask_rect(x - 2, 240, x + 3, 252) | c.mask_rect(x - 9, 248, x + 3, 253)
        c.shape(pipe, (206, 212, 222), (140, 146, 160), (252, 252, 254), band=1)
        knob = c.mask_ell(x + 1, 238, 3.5, 3); c.shape(knob, (214, 64, 64), (150, 30, 30), band=1)
        if k % 2 == 1:
            for yy in range(254, 304):
                c.px(x - 7, yy, (160, 214, 248)); c.px(x - 6, yy, (226, 246, 255) if (yy // 3) % 3 else (160, 214, 248))
            c.fill(c.mask_ell(x - 6, 305, 5, 1.5), (200, 236, 252))
    # rebord en pierre + rigole
    ledge = c.mask_rect(0, 300, 270, 314)
    c.shape(ledge, (210, 200, 184), (166, 154, 138), (236, 230, 218), band=3, sdir="bottom", ldir="top")
    c.fill(c.mask_rect(0, 314, 270, 322), (84, 150, 204))
    for x in range(0, 270, 9):
        c.fill(c.mask_rect(x, 316, x + 3, 317), (214, 242, 255))
    c.fill(c.mask_rect(0, 322, 270, 330), (150, 140, 126))
    # sol carrelé + bonde
    floor = c.mask_rect(0, 330, 270, 480)
    c.fill(floor, (200, 194, 182))
    yy, xx = c.yy, c.xx
    dz = np.maximum(yy - 260, 1).astype(float); z = 420.0 / dz; xw = (xx - 135) * z / 105.0
    chk = ((np.floor(xw / 0.7) + np.floor(z / 0.7)) % 2 == 0) & floor
    c.fill(chk, (176, 168, 156))
    grout = ((((xw / 0.7) - np.floor(xw / 0.7)) < 0.05) | (((z / 0.7) - np.floor(z / 0.7)) < 0.05)) & floor
    c.fill(grout, (150, 142, 130))
    drain = c.mask_rect(120, 420, 150, 428); c.shape(drain, (120, 122, 130), (90, 92, 100), band=1)
    for x in range(122, 150, 3):
        c.fill(c.mask_rect(x, 421, x + 1, 427), (60, 62, 70))
    # tabourets en pierre
    for x in (40, 130, 220):
        t = c.mask_rrect(x - 17, 340, x + 17, 351, 3)
        c.shape(t, (200, 190, 174), (156, 146, 130), (228, 222, 208), band=2, sdir="bottom", ldir="top")
        p = c.mask_rect(x - 9, 351, x + 9, 368); c.shape(p, (180, 170, 154), (136, 126, 112), band=2)
    # sandales posées
    for x, col in ((70, (60, 60, 70)), (188, (130, 80, 46))):
        for dx in (0, 9):
            s = c.mask_ell(x + dx, 462, 3.5, 8); c.shape(s, col, tuple(int(v * 0.7) for v in col), band=1)
    # porte-serviettes
    c.shape(c.mask_rect(240, 222, 268, 226), (170, 130, 70), (120, 90, 40), band=1)
    for k, (x, col) in enumerate(((244, (210, 70, 70)), (256, (60, 120, 190)))):
        t = c.mask_rect(x, 226, x + 9, 262); c.shape(t, col, tuple(int(v * 0.72) for v in col), band=2)
        c.fill(c.mask_rect(x, 254, x + 9, 256), (240, 240, 240))
    # flaques (reflets)
    for x, y, rx in ((90, 380, 16), (200, 430, 22)):
        c.dither(c.mask_ell(x, y, rx, 3) & floor, (226, 240, 250), 0.5)
    return c, None


def carte_titre(col=(22, 92, 96), col2=(16, 70, 74)):
    """Fond de la carte d'accroche : toile texturée + ficelle (la photo et le titre sont posés au montage)."""
    c = Px()
    c.fill(c.mask_rect(0, 0, 270, 480), col)
    rnd = R(5)
    weave = ((c.xx % 3 == 0) & (c.yy % 2 == 0)) | ((c.yy % 3 == 0) & (c.xx % 2 == 1))
    c.fill(weave, tuple(int(v * 0.92) for v in col))
    for _ in range(700):
        x, y = rnd.randint(0, 269), rnd.randint(0, 479)
        c.px(x, y, col2 if rnd.random() < 0.6 else tuple(min(255, int(v * 1.15)) for v in col))
    d = ((c.xx - 135) / 150.0) ** 2 + ((c.yy - 240) / 265.0) ** 2
    for k, (th, f) in enumerate(((1.0, 0.9), (1.25, 0.8), (1.6, 0.7))):
        ring = (d > th) & ~((d > th - 0.04) & ((c.xx + c.yy) % 2 == 0) & (d < th + 0.0))
        c.tint(ring, (0, 0, 0), 0.10)
    # ficelle en léger arc
    for x in range(0, 270):
        y = int(150 + 10 * math.sin(x / 270 * math.pi))
        c.px(x, y, (226, 214, 190)); c.px(x, y + 1, (150, 140, 120))
    return c, None


def chambre():
    """Chambre du petit frère, en plein jour : fenêtre au soleil, lit défait, réveil, tapis de prière roulé."""
    c = Px()
    wall = c.mask_rect(0, 0, 270, 300)
    c.vgrad(wall, 0, 300, (150, 170, 196), (196, 206, 220), steps=6)
    win = c.mask_rect(150, 50, 250, 170)
    c.vgrad(win, 50, 170, (150, 210, 250), (220, 240, 255), steps=5)
    sun = c.mask_ell(222, 82, 14, 14); c.fill(sun & win, (255, 236, 140))
    for x0, w in ((150, 30), (186, 26), (214, 36)):
        c.fill(c.mask_rect(x0, 140, x0 + w, 170) & win, (190, 206, 220))
    c.fill(c.mask_rect(198, 50, 201, 170), (240, 240, 244)); c.fill(c.mask_rect(150, 108, 250, 111), (240, 240, 244))
    c.outline(win, (90, 100, 120))
    c.shape(c.mask_rect(144, 168, 256, 175), (236, 236, 240), (196, 196, 206), band=1, sdir="bottom")
    ray = c.mask_poly([(150, 170), (250, 170), (200, 480), (60, 480)])
    c.tint(ray & c.mask_rect(0, 0, 270, 480), (255, 246, 210), 0.10)
    # poster et étagère
    po = c.mask_rect(30, 70, 90, 150); c.shape(po, (40, 60, 110), (30, 44, 84), band=2)
    c.fill(c.mask_ell(60, 100, 16, 16) & po, (226, 186, 90)); c.fill(c.mask_rect(36, 128, 84, 134), (226, 186, 90))
    sh = c.mask_rect(20, 176, 110, 181); c.shape(sh, (150, 100, 62), (112, 72, 44), band=1, sdir="bottom")
    books(c, 24, 70, 176, 12, 16, seed=8)
    # sol
    floor = c.mask_rect(0, 300, 270, 480)
    planks(c, 300, 480, horizon=230, col=(176, 126, 86), dark=(140, 96, 62), light=(200, 152, 106))
    c.shape(c.mask_rect(0, 296, 270, 302), (236, 236, 240), (196, 196, 206), band=1, sdir="bottom")
    # lit
    frame = c.mask_rect(10, 230, 190, 330); c.shape(frame, (120, 80, 50), (88, 58, 36), (150, 104, 66), band=3)
    c.shape(c.mask_rect(4, 190, 26, 330), (120, 80, 50), (88, 58, 36), band=2)
    mat = c.mask_rect(24, 232, 188, 262); c.shape(mat, (240, 240, 244), (206, 206, 214), band=2, sdir="bottom")
    pil = c.mask_rrect(28, 218, 76, 240, 6); c.shape(pil, (250, 250, 252), (210, 210, 220), band=2)
    blank = c.mask_poly([(60, 236), (190, 228), (196, 300), (54, 306)])
    c.shape(blank, (60, 120, 190), (40, 90, 150), (90, 150, 214), band=3)
    for k in range(4):
        c.line(80 + k * 26, 240, 74 + k * 28, 300, (44, 96, 156))
    # table de nuit + réveil
    tb = c.mask_rect(200, 250, 244, 320); c.shape(tb, (150, 100, 62), (112, 72, 44), (176, 126, 86), band=2)
    c.fill(c.mask_rect(206, 276, 238, 278), (112, 72, 44)); c.fill(c.mask_rect(220, 282, 224, 284), (226, 186, 90))
    ck = c.mask_rect(206, 232, 238, 250); c.shape(ck, (40, 40, 52), (24, 24, 34), band=1)
    c.fill(c.mask_rect(209, 235, 235, 247), (20, 16, 24))
    c.text((222, 236), "09:12", (255, 70, 60), size=8, anchor="ma")
    # tapis de prière roulé contre le mur
    rug_ = c.mask_rrect(246, 240, 262, 300, 5); c.shape(rug_, (24, 110, 90), (16, 76, 62), band=2)
    for y in range(246, 298, 8):
        c.fill(c.mask_rect(248, y, 260, y + 1), (226, 186, 90))
    return c, None


DECORS = dict(salon=salon, mosquee=mosquee, tableau=tableau, ablutions=ablutions, carte=carte_titre, chambre=chambre)

if __name__ == "__main__":
    import sys
    name = sys.argv[1]
    bg, fg = DECORS[name]()
    im = bg.img(4).convert("RGBA")
    if fg is not None:
        im.alpha_composite(fg.img(4, rgba=True))
    im.convert("RGB").save(sys.argv[2])
