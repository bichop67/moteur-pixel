# Miniatures « MOÏSE CONTRE PHARAON » (épisode 14), dans l'esprit de la miniature du Dajjal :
# une silhouette géante et menaçante à contre-jour, les yeux qui brillent, Moussa = une orbe de lumière face à lui,
# le titre énorme (jaune + blanc, gros contour noir). Pixel art dessiné en code (480x270 agrandi x4), aucune image IA.
#   python mini_pharaon.py <dossier_sortie> [A|B|tout]
import sys, math, random, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 480, 270, 4
FONT = "C:/Windows/Fonts/seguibl.ttf"
JAUNE, BLANC, NOIR = (255, 212, 72), (255, 255, 255), (10, 6, 8)
BAYER = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) + 0.5) / 16.0
YY, XX = np.mgrid[0:H, 0:W]


# ------------------------------------------------------------------ outils pixel
def degrade(t, pal):
    """Champ t (0..1) -> couleurs de la palette, avec tramage ordonné (dégradé pixel art)."""
    n = len(pal) - 1
    lv = np.clip(np.nan_to_num(t), 0, 1) * n
    base = np.floor(lv).astype(int)
    by = BAYER[YY % 4, XX % 4]
    idx = np.clip(base + ((lv - base) > by), 0, n)
    return np.array(pal, np.uint8)[idx]


def erode(m):
    p = np.pad(m, 1, constant_values=False)
    p[-1, :] = True          # le bas du cadre n'est pas un bord éclairé
    return m & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]


def colle(base, lay):
    a = np.array(lay)
    m = a[..., 3] > 0
    base[m] = a[m][:, :3]
    return m


def melange(base, m, col, k):
    base[m] = (base[m].astype(np.float32) * (1 - k) + np.array(col, np.float32) * k).astype(np.uint8)


# ------------------------------------------------------------------ Pharaon (géant, à contre-jour)
def pharaon(cx, rim_g=(255, 128, 56), rim_d=(255, 128, 56), rim2=(120, 36, 20), glint=(255, 204, 104),
            oeil=(255, 56, 18), oeil2=(255, 230, 176)):
    """Buste de Pharaon (némès rayé, uræus, barbe postiche, collier ousekh, bras croisés avec crosse et fléau),
    presque noir, liseré de lumière sur les bords. Renvoie l'image RGBA 480x270."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    SH, SH2 = (13, 6, 8, 255), (19, 8, 10, 255)
    NG, NB = (44, 30, 12, 255), (11, 13, 32, 255)
    GD, CR, CT = (98, 64, 22, 255), (50, 12, 11, 255), (9, 36, 40, 255)
    # corps et épaules
    d.polygon([(cx - 34, 126), (cx - 98, 143), (cx - 128, 157), (cx - 142, 182), (cx - 156, H), (cx + 156, H),
               (cx + 142, 182), (cx + 128, 157), (cx + 98, 143), (cx + 34, 126)], fill=SH)
    d.rectangle([cx - 17, 106, cx + 17, 140], fill=SH)
    a = np.array(lay)
    # collier ousekh : bandes concentriques
    dd = np.hypot(XX - cx, (YY - 110) * 1.05)
    corps = a[..., 3] > 0
    for r0, r1, col in [(35, 40, GD), (40, 45, CT), (45, 50, CR), (50, 55, GD), (55, 61, CT), (61, 66, CR),
                        (66, 72, GD)]:
        a[corps & (dd >= r0) & (dd < r1) & (YY > 118)] = col
    for ang in np.arange(0.18, math.pi - 0.17, 0.065):
        bx, by = cx + 75 * math.cos(ang), 110 + 75 * math.sin(ang) / 1.05
        if by > 122:
            a[int(by) - 1:int(by) + 3, int(bx) - 1:int(bx) + 1] = GD if int(ang / 0.065) % 2 else CR
    lay = Image.fromarray(a)
    d = ImageDraw.Draw(lay)
    # némès : dôme + pans évasés derrière la tête + pans avant sur la poitrine
    nem = Image.new("L", (W, H), 0)
    dn = ImageDraw.Draw(nem)
    dn.ellipse([cx - 44, 27, cx + 44, 92], fill=255)
    dn.rectangle([cx - 40, 40, cx + 40, 60], fill=255)
    dn.polygon([(cx - 41, 52), (cx - 50, 86), (cx - 62, 116), (cx - 72, 134), (cx - 62, 141), (cx + 62, 141),
                (cx + 72, 134), (cx + 62, 116), (cx + 50, 86), (cx + 41, 52)], fill=255)
    for s in (-1, 1):
        dn.polygon([(cx + s * 48, 100), (cx + s * 30, 104), (cx + s * 29, 180), (cx + s * 32, 186),
                    (cx + s * 46, 186), (cx + s * 50, 180)], fill=255)
    nm = np.array(nem) > 0
    a = np.array(lay)
    rayure = ((YY + 1) // 3) % 2 == 0
    a[nm & rayure] = NG
    a[nm & ~rayure] = NB
    lay = Image.fromarray(a)
    d = ImageDraw.Draw(lay)
    # visage (mâchoire carrée), dans l'ombre
    d.ellipse([cx - 26, 54, cx + 26, 112], fill=SH2)
    d.polygon([(cx - 26, 86), (cx - 22, 108), (cx - 11, 121), (cx + 11, 121), (cx + 22, 108), (cx + 26, 86)],
              fill=SH2)
    # bandeau doré + uræus (cobra dressé sur le front)
    d.rectangle([cx - 34, 57, cx + 34, 61], fill=GD)
    d.ellipse([cx - 5, 44, cx + 5, 55], fill=GD)
    d.rectangle([cx - 1, 50, cx + 1, 62], fill=GD)
    d.rectangle([cx - 1, 40, cx + 1, 45], fill=GD)
    # barbe postiche
    d.polygon([(cx - 6, 118), (cx + 6, 118), (cx + 5, 146), (cx + 2, 150), (cx - 2, 150), (cx - 5, 146)],
              fill=(32, 21, 9, 255))
    for y in range(120, 149, 3):
        d.line([(cx - 5, y), (cx + 5, y)], fill=(52, 35, 13, 255))
    # sourcils froncés, nez, bouche dure
    for s in (-1, 1):
        d.polygon([(cx + s * 24, 76), (cx + s * 5, 82), (cx + s * 5, 85), (cx + s * 24, 80)], fill=(6, 3, 4, 255))
    d.line([(cx + 1, 87), (cx + 2, 101)], fill=(34, 16, 15, 255))
    d.line([(cx - 3, 102), (cx + 4, 102)], fill=(6, 3, 4, 255))
    d.line([(cx - 9, 110), (cx + 9, 110)], fill=(5, 2, 3, 255))
    d.point([(cx - 10, 111), (cx + 10, 111)], fill=(5, 2, 3, 255))
    # bras croisés, bracelets, poings
    for s in (1, -1):
        d.line([(cx - s * 136, 258), (cx + s * 14, 214)], fill=SH2, width=24)
    for s in (1, -1):
        px_, py_ = cx - s * 76, 240
        d.line([(px_ - 4, py_ - 9), (px_ + 4, py_ + 9)], fill=GD, width=6)
    def baton(p0, p1, w):
        n = int(math.hypot(p1[0] - p0[0], p1[1] - p0[1]))
        for i in range(n):
            t = i / n
            x, y = p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t
            d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=GD if (i // 4) % 2 == 0 else NB)
    baton((cx - 4, 250), (cx - 62, 150), 6)                      # crosse
    d.line([(cx - 62, 151), (cx - 64, 143), (cx - 70, 138), (cx - 77, 140), (cx - 80, 147), (cx - 77, 153)],
           fill=GD, width=6, joint="curve")
    baton((cx + 4, 250), (cx + 58, 152), 5)                      # fléau
    for (ex, ey) in [(cx + 82, 184), (cx + 74, 190), (cx + 66, 193)]:
        for i in range(11):
            t = i / 10
            x, y = cx + 58 + (ex - cx - 58) * t, 152 + (ey - 152) * t
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=GD if i % 2 == 0 else CR)
    for s in (1, -1):
        d.ellipse([cx + s * 14 - 11, 204, cx + s * 14 + 11, 224], fill=SH2)
        d.line([(cx + s * 14 - 8, 207), (cx + s * 14 + 8, 207)], fill=(30, 14, 14, 255))
    a = np.array(lay)
    m = a[..., 3] > 0
    # la lumière de derrière « mord » les bords : rayures du némès plus claires près du contour
    e = m.copy()
    for _ in range(5):
        e = erode(e)
    bord = m & ~e
    a[bord & np.all(a[..., :3] == NG[:3], axis=2), :3] = (150, 100, 36)
    a[bord & np.all(a[..., :3] == NB[:3], axis=2), :3] = (34, 38, 78)
    # éclats sur le haut des éléments dorés
    gold = np.all(a[..., :3] == GD[:3], axis=2)
    haut = gold & ~np.roll(gold, 1, axis=0)
    a[haut & (((XX * 7 + YY * 3) % 5) != 0), :3] = glint
    # yeux qui brillent (fentes en colère)
    for s in (-1, 1):
        for (x, y) in [(6, 85), (7, 85), (8, 85), (9, 85), (10, 85), (11, 85), (12, 85), (13, 85), (14, 86),
                       (15, 86), (16, 86), (17, 86), (18, 87), (19, 87), (7, 86), (8, 86), (9, 86), (10, 86),
                       (11, 86), (12, 86), (13, 86), (9, 87), (10, 87), (11, 87), (12, 87), (13, 87), (14, 87),
                       (15, 87), (16, 87)]:
            a[y, cx + s * x, :3] = oeil
        for (x, y) in [(10, 86), (11, 86), (12, 86), (11, 85), (13, 86)]:
            a[y, cx + s * x, :3] = oeil2
    # liseré de lumière (2 pixels) + lueur intérieure
    e1 = erode(m); e2 = erode(e1); e3 = erode(e2)
    r1, r2, r3 = m & ~e1, e1 & ~e2, e2 & ~e3
    fa = np.array(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), np.float32)
    gx = np.zeros_like(fa); gx[:, 1:-1] = fa[:, 2:] - fa[:, :-2]
    gauche = gx > 0
    for msk, k in ((r1, 1.0), (r2, 0.75)):
        a[msk & gauche, :3] = (a[msk & gauche, :3] * (1 - k) + np.array(rim_g) * k).astype(np.uint8)
        a[msk & ~gauche, :3] = (a[msk & ~gauche, :3] * (1 - k) + np.array(rim_d) * k).astype(np.uint8)
    a[r3, :3] = (a[r3, :3].astype(np.float32) * 0.45 + np.array(rim2, np.float32) * 0.55).astype(np.uint8)
    return Image.fromarray(a)


# ------------------------------------------------------------------ orbe de Moussa (comme dans le film)
def orbe(base, ox, oy, r):
    d2 = np.hypot(XX - ox, YY - oy)
    for rr, col, k in [(r + 10, (150, 120, 76), 0.4), (r + 5, (214, 178, 110), 0.6)]:
        melange(base, (d2 < rr) & (d2 >= r), col, k)
    m = d2 < r
    t = np.clip(np.hypot(XX - (ox - r * 0.3), YY - (oy - r * 0.35)) / (r * 1.25), 0, 1)
    base[m] = degrade(1 - t, [(196, 140, 58), (232, 182, 86), (255, 222, 140), (255, 240, 196), (255, 252, 236)])[m]
    base[(d2 < r) & (d2 >= r - 1.2)] = (176, 118, 46)
    for (dx, dy) in [(-0.4, -0.45), (-0.3, -0.5), (-0.45, -0.35)]:
        base[int(oy + dy * r), int(ox + dx * r)] = (255, 255, 255)


# ------------------------------------------------------------------ passes haute définition
def hd(arr):
    return np.array(Image.fromarray(arr).resize((W * K, H * K), Image.NEAREST), np.float32)


def hd_calque(lay):
    return lay.resize((W * K, H * K), Image.NEAREST)


def halo(img, x, y, rx, ry, col, force):
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = ((xx - x) / rx) ** 2 + ((yy - y) / ry) ** 2
    img += (np.exp(-d * 2.2) * force)[..., None] * np.array(col, np.float32)


def bloom(img, seuil=170, f1=0.42, f2=0.5):
    lum = img[..., 0] * 0.3 + img[..., 1] * 0.59 + img[..., 2] * 0.11
    m = np.clip((lum - seuil) / (255 - seuil), 0, 1)
    br = Image.fromarray(np.clip(img * m[..., None], 0, 255).astype(np.uint8))
    img += np.array(br.filter(ImageFilter.GaussianBlur(14)), np.float32) * f1
    img += np.array(br.filter(ImageFilter.GaussianBlur(48)), np.float32) * f2


def rayons(img, x, y, col, n=14, long=900, force=0.10, seed=3, angles=None):
    rnd = random.Random(seed)
    lay = Image.new("L", (img.shape[1], img.shape[0]), 0)
    d = ImageDraw.Draw(lay)
    for i in range(n):
        ang = rnd.uniform(*(angles or (0, 2 * math.pi)))
        lg = long * rnd.uniform(0.5, 1.0)
        da = rnd.uniform(0.02, 0.055)
        d.polygon([(x, y), (x + lg * math.cos(ang - da), y + lg * math.sin(ang - da)),
                   (x + lg * math.cos(ang + da), y + lg * math.sin(ang + da))], fill=int(255 * rnd.uniform(0.5, 1)))
    a = np.array(lay.filter(ImageFilter.GaussianBlur(10)), np.float32) / 255 * force
    img += a[..., None] * np.array(col, np.float32)


def pose(img, lay_hd):
    a = np.array(lay_hd, np.float32)
    al = a[..., 3:4] / 255.0
    img[:] = img * (1 - al) + a[..., :3] * al


def finition(img, vign=0.62, grain=7, seed=1):
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dd = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    img *= (1 - np.clip((dd - 0.5) / 0.95, 0, 1) * vign)[..., None]
    img += np.random.default_rng(seed).normal(0, grain, (h, w, 1)).astype(np.float32)
    return np.clip(img, 0, 255)


# ------------------------------------------------------------------ titre (style Dajjal)
def ligne(txt, taille, coul, contour):
    f = ImageFont.truetype(FONT, taille)
    bb = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), txt, font=f, stroke_width=contour)
    im = Image.new("RGBA", (bb[2] - bb[0] + 20, bb[3] - bb[1] + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - bb[0], 10 - bb[1]), txt, font=f, fill=coul, stroke_width=contour,
                            stroke_fill=NOIR)
    return im


def titre(img_rgba, lignes, cx, bas, chevauche=22):
    ims = [ligne(*l) for l in lignes]
    wmax = max(i.width for i in ims)
    htot = sum(i.height for i in ims) - chevauche * (len(ims) - 1)
    bloc = Image.new("RGBA", (wmax + 80, htot + 80), (0, 0, 0, 0))
    y = 40
    for im in ims:
        bloc.alpha_composite(im, (40 + (wmax - im.width) // 2, y))
        y += im.height - chevauche
    ombre = Image.new("RGBA", bloc.size, (0, 0, 0, 0))
    ombre.putalpha(bloc.getchannel("A").point(lambda v: int(v * 0.8)))
    ombre = ombre.filter(ImageFilter.GaussianBlur(18))
    x0, y0 = int(cx - bloc.width / 2), int(bas - bloc.height + 40)
    img_rgba.alpha_composite(ombre, (x0 + 6, y0 + 16))
    img_rgba.alpha_composite(bloc, (x0, y0))
    return (x0 + 40, y0 + 40, x0 + 40 + wmax, y0 + 40 + htot)


# ------------------------------------------------------------------ A : le tyran (soleil de sang)
def variante_A(lignes):
    cx, sx, sy, R = 292, 292, 112, 106
    pal = [(6, 2, 7), (13, 3, 9), (24, 5, 11), (40, 8, 13), (64, 12, 15), (94, 18, 17), (128, 27, 19),
           (164, 40, 21), (198, 60, 27), (226, 88, 36), (246, 118, 50), (255, 150, 70), (255, 184, 106),
           (255, 214, 150), (255, 236, 196)]
    ds = np.hypot(XX - sx, YY - sy) / R
    ciel = np.clip((YY / 212.0) ** 1.7 * 0.46, 0, 0.46)
    glow = 0.52 * np.exp(-np.clip(ds - 1, 0, None) * 2.6)
    soleil = 0.6 + 0.4 * np.clip(1 - ds, 0, 1) ** 0.55
    champ = np.where(ds < 1, soleil, np.maximum(ciel, glow))
    base = degrade(champ, pal)
    sol = YY >= 212
    base[sol] = degrade(np.clip(1 - (YY - 212) / 58.0, 0, 1) * 0.26, pal)[sol]
    base[(YY >= 211) & (YY <= 212) & (np.abs(XX - sx) < 96)] = (246, 122, 50)
    def pyr(apx, apy, demi, lum_droite):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dd_ = ImageDraw.Draw(lay)
        dd_.polygon([(apx - demi, 212), (apx, apy), (apx + demi, 212)], fill=(24, 6, 9, 255))
        s = 1 if lum_droite else -1
        dd_.polygon([(apx, apy), (apx + s * demi, 212), (apx + s * demi // 3, 212)], fill=(38, 9, 11, 255))
        dd_.line([(apx, apy), (apx + s * demi, 212)], fill=(214, 80, 34, 255))
        colle(base, lay)
    pyr(54, 182, 46, True)
    pyr(152, 156, 68, True)
    pyr(458, 166, 60, False)
    rnd = random.Random(7)
    for _ in range(110):
        x, y = rnd.randrange(0, W), int(rnd.triangular(0, 210, 110))
        base[y, x] = rnd.choice([(255, 150, 60), (255, 196, 110), (255, 120, 50)])
    ox, oy, orr = 86, 116, 17
    orbe(base, ox, oy, orr)
    img = hd(base)
    halo(img, sx * K, sy * K, R * K * 2.0, R * K * 1.7, (255, 70, 30), 0.25)
    halo(img, sx * K, sy * K, R * K * 0.9, R * K * 0.9, (255, 200, 120), 0.18)
    rayons(img, ox * K, oy * K, (255, 236, 190), n=18, long=800, force=0.16)
    halo(img, ox * K, oy * K, 280, 280, (255, 236, 186), 0.55)
    halo(img, ox * K, 214 * K, 320, 44, (255, 220, 160), 0.28)
    pose(img, hd_calque(pharaon(cx)))
    for s in (-1, 1):
        halo(img, (cx + s * 12) * K, 86 * K, 84, 40, (255, 50, 16), 0.9)
    halo(img, cx * K, 86 * K, 220, 70, (255, 40, 10), 0.18)
    bloom(img)
    img = finition(img)
    out = Image.fromarray(img.astype(np.uint8)).convert("RGBA")
    titre(out, lignes, 820, 1012)
    return out


# ------------------------------------------------------------------ B : la mer ouverte (au lever du soleil, 26:60-63)
def interp(pts, x):
    xs, ys = zip(*pts)
    return np.interp(x, xs, ys)


def variante_B(lignes):
    cx = 346
    vx, vy = 128, 104                      # le bout du chemin dans la mer : le lever du soleil
    # ciel de l'aube entre les deux murs
    pal_ciel = [(6, 8, 20), (12, 14, 34), (24, 22, 52), (46, 34, 72), (80, 50, 88), (122, 70, 96), (168, 96, 100),
                (210, 130, 104), (240, 166, 116), (255, 200, 140), (255, 228, 180), (255, 246, 222)]
    dv = np.hypot((XX - vx) / 1.5, (YY - vy) * 1.0) / 110.0
    base = degrade(np.exp(-dv * 1.6), pal_ciel)
    # fond de la mer asséché, en perspective
    sol = YY > vy
    pal_sol = [(8, 7, 10), (16, 13, 15), (28, 22, 23), (46, 34, 31), (74, 54, 42), (112, 82, 58), (164, 122, 84),
               (220, 176, 126)]
    tsol = np.exp(-np.hypot((XX - vx) / 2.4, (YY - vy) * 1.3) / 40.0)
    base[sol] = degrade(tsol, pal_sol)[sol]
    rnd = random.Random(11)
    for _ in range(40):
        y = rnd.randrange(vy + 3, H)
        prof = (y - vy) / (H - vy)
        x = int(vx + rnd.uniform(-1, 1) * (8 + prof * 170))
        lg = int(2 + prof * 16)
        if rnd.random() < 0.55:
            base[y, max(0, x - lg):min(W, x + lg)] = (255, 206, 146) if prof < 0.4 else (170, 120, 90)
        else:
            base[y - 1:y + 1, max(0, x - lg // 2):min(W, x + lg // 2)] = (10, 8, 10)
    # murs d'eau « comme d'énormes montagnes »
    crete_g = [(-10, -8), (36, 14), (74, 40), (100, 64), (114, 80), (121, 92), (124, 100)]
    crete_d = [(133, 100), (136, 92), (150, 78), (178, 56), (226, 30), (286, 6), (340, -12)]
    pal_eau = [(2, 9, 14), (4, 16, 24), (7, 26, 36), (11, 40, 52), (18, 58, 70), (30, 84, 96), (52, 120, 130),
               (96, 168, 172), (160, 214, 210)]
    xf = XX.astype(np.float32)
    def mur(crete, bord_sol, cote):
        top = interp(crete, xf[0])[None, :].repeat(H, 0) if cote < 0 else interp(crete, xf[0])[None, :].repeat(H, 0)
        x_lim = interp(bord_sol, YY.astype(np.float32)[:, 0])[:, None]
        if cote < 0:
            m = (YY >= top) & (XX <= np.maximum(x_lim, crete[-1][0]) ) & (XX <= crete[-1][0])
        else:
            m = (YY >= top) & (XX >= np.minimum(x_lim, crete[0][0])) & (XX >= crete[0][0])
        if cote < 0:
            m &= ~((YY > vy) & (XX > x_lim))
        else:
            m &= ~((YY > vy) & (XX < x_lim))
        prof = np.clip((YY - top) / 46.0, 0, 1)
        pres = np.exp(-np.abs(XX - vx) / 80.0)
        t = 0.6 * (1 - prof) ** 1.3 + 0.36 * pres * (1 - 0.5 * np.clip((YY - vy) / 150.0, 0, 1)) + 0.12
        t += 0.04 * np.sin(YY / 2.6 + np.sin(XX / 11.0) * 2.2)
        base[m] = degrade(t, pal_eau)[m]
        # vagues prises dans le mur (stries ondulées) et bulles
        stries = m & (((YY + (3 * np.sin(XX / 9.0)).astype(int)) % 10) == 0)
        base[stries] = np.clip(base[stries].astype(int) + 30, 0, 255).astype(np.uint8)
        stries2 = m & (((YY + (3 * np.sin(XX / 9.0)).astype(int)) % 10) == 1)
        base[stries2] = (base[stries2].astype(int) * 0.7).astype(np.uint8)
        # écume sur la crête (bord irrégulier)
        bruit = (np.sin(XX * 1.7) * 1.2 + np.sin(XX * 0.43) * 1.5).astype(int)
        ecume = m & (YY - top < 2.2 + bruit.clip(0, None))
        base[ecume] = (224, 244, 240)
        ecume2 = m & ~ecume & (YY - top < 4.5 + bruit.clip(0, None))
        base[ecume2] = (130, 196, 196)
        return m
    mg = mur(crete_g, [(vy, 124), (H, -80)], -1)
    md = mur(crete_d, [(vy, 133), (H, 360)], 1)
    # bulles
    for _ in range(160):
        x, y = rnd.randrange(0, W), rnd.randrange(0, H)
        if (mg[y, x] or md[y, x]) and rnd.random() < 0.8:
            base[y, x] = (120, 186, 190)
    # poissons pris dans les murs (près de la crête, là où l'eau est claire)
    for _ in range(40):
        x = rnd.randrange(4, 120) if rnd.random() < 0.75 else rnd.randrange(140, 300)
        y = int(interp(crete_g if x < 125 else crete_d, x)) + rnd.randrange(10, 60)
        L, s = rnd.randrange(6, 12), rnd.choice((-1, 1))
        if 0 < y < H - 2 and 0 < x < W - 14 and (mg[y, x] or md[y, x]) and (mg[y, x + L] or md[y, x + L]):
            col = (2, 10, 14)
            base[y, x:x + L] = col
            base[y - 1, x + 2:x + L - 2] = col
            base[y + 1, x + 2:x + L - 2] = col
            tx = x + L if s > 0 else x - 1
            base[y - 2:y + 3, tx] = col
    # pied des murs : ligne d'écume au contact du sol
    for (p0, p1) in [((124, vy), (-80, H)), ((133, vy), (360, H))]:
        for i in range(400):
            t = i / 400
            x, y = int(p0[0] + (p1[0] - p0[0]) * t), int(p0[1] + (p1[1] - p0[1]) * t)
            if 0 <= x < W and 0 <= y < H:
                base[y, x] = (190, 226, 222)
    # embruns au-dessus des crêtes
    for _ in range(220):
        crete = crete_g if rnd.random() < 0.5 else crete_d
        x = rnd.uniform(crete[0][0], crete[-1][0])
        y = interp(crete, x) - abs(rnd.gauss(0, 4)) - 1
        if 0 <= int(x) < W and 0 <= int(y) < H:
            base[int(y), int(x)] = (200, 236, 232)
    # les gens qui traversent vers la lumière
    for i in range(16):
        t = rnd.random() ** 0.8
        y = int(vy + 2 + t * 24)
        x = int(vx + rnd.uniform(-1, 1) * (2 + t * 11))
        h = int(2 + t * 5)
        base[y - h:y, x] = (22, 16, 20)
        if h > 4:
            base[y - h + 1:y - 1, x + 1] = (22, 16, 20)
    ox, oy, orr = 112, 136, 11
    orbe(base, ox, oy, orr)
    img = hd(base)
    halo(img, vx * K, vy * K, 300, 170, (255, 206, 150), 0.45)
    rayons(img, vx * K, (vy - 2) * K, (255, 220, 170), n=20, long=1200, force=0.12, seed=5,
           angles=(math.pi * 1.05, math.pi * 1.95))
    halo(img, ox * K, oy * K, 170, 170, (255, 236, 186), 0.5)
    halo(img, cx * K, 100 * K, 520, 420, (70, 140, 150), 0.32)           # brume derrière Pharaon
    pose(img, hd_calque(pharaon(cx, rim_g=(255, 214, 150), rim_d=(96, 196, 200), rim2=(90, 80, 70))))
    for s in (-1, 1):
        halo(img, (cx + s * 12) * K, 86 * K, 84, 40, (255, 50, 16), 0.9)
    halo(img, cx * K, 86 * K, 220, 70, (255, 40, 10), 0.18)
    bloom(img)
    img = finition(img, vign=0.55)
    out = Image.fromarray(img.astype(np.uint8)).convert("RGBA")
    titre(out, lignes, 830, 1012)
    return out


if __name__ == "__main__":
    dossier = sys.argv[1]
    quoi = sys.argv[2] if len(sys.argv) > 2 else "tout"
    lignes = [("MOÏSE", 290, JAUNE, 24), ("CONTRE PHARAON", 132, BLANC, 17)]
    for nom, fn in (("A", variante_A), ("B", variante_B)):
        if quoi not in ("tout", nom):
            continue
        im = fn(lignes).convert("RGB")
        p = os.path.join(dossier, "mini_" + nom + ".jpg")
        im.resize((1280, 720), Image.LANCZOS).save(p, quality=93)
        im.resize((360, 202), Image.LANCZOS).save(os.path.join(dossier, "mini_" + nom + "_tel.png"))
        print("ok", p)
