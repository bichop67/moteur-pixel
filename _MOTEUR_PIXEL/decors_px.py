# Décors pixel art dessinés à la résolution pixel (270x480).
import math
import numpy as np
from px import Px, OUT, BAYER

K = OUT

# carreau de zellige 12x12 (étoile à 8 branches), dessiné à la main
TILE = [
    "wwwwwgwwwwww",
    "wwwwgggwwwww",
    "wwwgbbbgwwww",
    "wwgbbybbgwww",
    "wgbbyyybbgww",
    "ggbyyyyybggw",
    "wgbbyyybbgww",
    "wwgbbybbgwww",
    "wwwgbbbgwwww",
    "wwwwgggwwwww",
    "wwwwwgwwwwww",
    "wwwwwwwwwwww",
]
TPAL = dict(w=(236, 232, 220), g=(24, 128, 120), b=(36, 82, 150), y=(232, 186, 70))


def floor_persp(c, y0, cx=135, col1=(232, 218, 192), col2=(170, 120, 92), tile=1.0, fog=(200, 186, 160)):
    """Sol en damier vu en perspective (calcul pixel par pixel, tramage au loin)."""
    for y in range(y0, c.h):
        z = 60.0 / (y - y0 + 6)
        for x in range(c.w):
            xw = (x - cx) * z / 30.0
            on = (math.floor(xw / tile) + math.floor(z * 2.2 / tile)) % 2
            col = col1 if on else col2
            f = min(1.0, z / 9.0)
            if f > 0.75 and BAYER[y % 4, x % 4] < (f - 0.75) * 2:
                col = fog
            c.a[y, x] = col


def mgrad(c, m, y0, y1, top, bot, steps=6):
    """Dégradé tramé limité à un masque."""
    top, bot = np.array(top, float), np.array(bot, float)
    yy, xx = np.mgrid[0:c.h, 0:c.w]
    t = np.clip((yy - y0) / max(1, y1 - y0), 0, 1) * (steps - 1)
    lo = np.floor(t); f = t - lo
    q = np.where(BAYER[yy % 4, xx % 4] < f, lo + 1, lo) / (steps - 1)
    col = top[None, None, :] + (bot - top)[None, None, :] * q[..., None]
    c.a[m] = col[m].astype(np.uint8)


def ablutions(c):
    """Salle d'ablutions : mur enduit + fenêtres en arc, frise de zellige, rebord en pierre, robinets, sol en damier."""
    c.vgrad(0, 0, c.w, 236, (250, 226, 186), (232, 200, 156), steps=7)
    # fenêtres en arc, lumière du jour
    for wx in (30, 135, 240):
        m = c.mask_rect(wx - 22, 70, wx + 22, 190) | c.mask_ell(wx, 70, 22, 24)
        mgrad(c, m, 46, 190, (226, 246, 255), (140, 200, 238))
        for gx in (wx - 8, wx + 8):
            c.fill(c.mask_rect(gx - 1, 50, gx + 1, 190) & m, (120, 80, 50))
        c.fill(c.mask_rect(wx - 22, 128, wx + 22, 130) & m, (120, 80, 50))
        c.outline(m)
        c.fill(c.mask_rect(wx - 26, 190, wx + 26, 196), (210, 176, 132)); c.outline(c.mask_rect(wx - 26, 190, wx + 26, 196))
        c.glow(wx, 140, 70, (255, 246, 214), 0.35)
    # lanterne en laiton
    c.line(135, 0, 135, 30, (120, 84, 40))
    lan = c.mask_poly([(127, 30), (143, 30), (147, 44), (135, 58), (123, 44)])
    c.shape(lan, (232, 182, 70), (176, 120, 40), (252, 226, 140), band=3, dith=False)
    c.glow(135, 46, 40, (255, 220, 140), 0.45)
    # frise de zellige
    y0 = 236
    for ty in range(y0, y0 + 96, 12):
        for tx in range(0, c.w, 12):
            c.sprite(TILE, TPAL, tx, ty)
    c.fill(c.mask_rect(0, y0 - 6, c.w, y0), (24, 128, 120)); c.outline(c.mask_rect(0, y0 - 6, c.w, y0))
    for x in range(0, c.w, 6):
        c.px(x, y0 - 3, (232, 186, 70))
    # robinets
    for k, x in enumerate(range(22, c.w, 45)):
        pipe = c.mask_rect(x - 2, 262, x + 3, 272) | c.mask_rect(x - 8, 268, x + 3, 273)
        c.shape(pipe, (200, 206, 214), (140, 146, 160), (250, 250, 252), band=1, dith=False)
        knob = c.mask_ell(x + 1, 260, 3, 3); c.shape(knob, (210, 60, 60), (150, 30, 30), band=1, dith=False)
        if k % 2 == 1:
            for yy in range(274, 334):
                c.px(x - 6, yy, (170, 220, 250)); c.px(x - 5, yy, (220, 244, 255) if yy % 5 else (170, 220, 250))
    # rebord en pierre + rigole d'eau
    ledge = c.mask_rect(0, 332, c.w, 344); c.shape(ledge, (206, 196, 180), (160, 148, 132), (232, 226, 214), dir=(0, 1), band=3)
    c.fill(c.mask_rect(0, 344, c.w, 350), (92, 160, 210))
    for x in range(0, c.w, 7):
        c.px(x, 346, (210, 240, 255)); c.px(x + 1, 346, (210, 240, 255))
    floor_persp(c, 350)
    # tabourets en pierre
    for x in (40, 130, 220):
        t = c.mask_rrect(x - 16, 356, x + 16, 366, 3); c.shape(t, (196, 186, 170), (150, 140, 124), (226, 220, 206), dir=(0, 1), band=3)
        p = c.mask_rect(x - 9, 366, x + 9, 382); c.shape(p, (176, 166, 150), (130, 120, 106), band=3)
