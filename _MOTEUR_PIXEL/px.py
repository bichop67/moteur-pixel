# Moteur PIXEL ART « à la main » : on dessine directement à la résolution pixel (270x480 pour les décors),
# sans lissage, avec contours, ombres en aplats, tramage (dithering). Couche RGB + masque alpha (avant-plans).
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PW, PH = 270, 480
OUT = (34, 22, 34)
INK = (22, 16, 26)
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
TAHOMA = "C:/Windows/Fonts/tahomabd.ttf"
VERDANA = "C:/Windows/Fonts/verdanab.ttf"


class Px:
    def __init__(s, w=PW, h=PH, bg=(0, 0, 0), alpha=False):
        s.w, s.h = w, h
        s.a = np.zeros((h, w, 3), np.uint8); s.a[:] = bg
        s.al = np.zeros((h, w), bool) if alpha else np.ones((h, w), bool)
        s.yy, s.xx = np.mgrid[0:h, 0:w]

    # ---------- masques
    def mask_rect(s, x0, y0, x1, y1):
        m = np.zeros((s.h, s.w), bool)
        m[max(0, int(y0)):max(0, int(y1)), max(0, int(x0)):max(0, int(x1))] = True
        return m

    def mask_ell(s, cx, cy, rx, ry):
        return ((s.xx + 0.5 - cx) / rx) ** 2 + ((s.yy + 0.5 - cy) / ry) ** 2 <= 1.0

    def mask_poly(s, pts):
        im = Image.new("L", (s.w, s.h), 0)
        ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255)
        return np.array(im) > 0

    def mask_rrect(s, x0, y0, x1, y1, r):
        m = s.mask_rect(x0 + r, y0, x1 - r, y1) | s.mask_rect(x0, y0 + r, x1, y1 - r)
        for cx, cy in ((x0 + r, y0 + r), (x1 - r, y0 + r), (x0 + r, y1 - r), (x1 - r, y1 - r)):
            m |= s.mask_ell(cx, cy, r, r)
        return m

    def mask_arch(s, x0, x1, y_top, y_bot, pointed=0.0):
        """Arc (plein cintre ou brisé) : rectangle + demi-ellipse ; pointed>0 = arc brisé."""
        cx = (x0 + x1) / 2; r = (x1 - x0) / 2
        m = s.mask_rect(x0, y_top + r, x1, y_bot)
        if pointed > 0:
            yy, xx = s.yy + 0.5, s.xx + 0.5
            for sgn in (-1, 1):
                ccx = cx - sgn * r * pointed
                rr = r * (1 + pointed)
                m |= (((xx - ccx) ** 2 + (yy - (y_top + r)) ** 2) <= rr ** 2) & (yy <= y_top + r) & \
                     ((xx - cx) * sgn >= -0.01) & (xx >= x0) & (xx <= x1)
        else:
            m |= s.mask_ell(cx, y_top + r, r, r) & s.mask_rect(x0, y_top, x1, y_top + r + 1)
        return m

    # ---------- remplissages
    def fill(s, m, col):
        s.a[m] = col; s.al[m] = True

    def outline(s, m, col=OUT):
        e = m.copy()
        e[1:, :] |= m[:-1, :]; e[:-1, :] |= m[1:, :]; e[:, 1:] |= m[:, :-1]; e[:, :-1] |= m[:, 1:]
        s.fill(e & ~m, col)

    def edge(s, m, col, side="bottom", n=1):
        """Bande sur un bord de la forme (ombre / reflet en aplat)."""
        dx, dy = dict(bottom=(0, -1), top=(0, 1), left=(1, 0), right=(-1, 0))[side]
        inner = m.copy()
        for k in range(1, n + 1):
            inner &= np.roll(np.roll(m, dx * k, axis=1), dy * k, axis=0)
        s.fill(m & ~inner, col)

    def shape(s, m, col, shade=None, light=None, ol=True, sdir="right", band=2, ldir="left", lband=1, olcol=OUT):
        s.fill(m, col)
        if shade is not None:
            s.edge(m, shade, sdir, band)
            if sdir in ("right", "left"):
                s.edge(m, shade, "bottom", max(1, band // 2))
        if light is not None:
            s.edge(m, light, ldir, lband)
            s.edge(m, light, "top", 1)
        if ol:
            s.outline(m, olcol)

    def dither(s, m, col, k=0.5):
        """Tramage : couvre une fraction k des pixels du masque (motif de Bayer)."""
        s.fill(m & (BAYER[s.yy % 4, s.xx % 4] < k), col)

    def vgrad(s, m, y0, y1, top, bot, steps=6):
        """Dégradé vertical tramé dans un masque."""
        top, bot = np.array(top, float), np.array(bot, float)
        t = np.clip((s.yy - y0) / max(1, y1 - y0), 0, 1) * (steps - 1)
        lo = np.floor(t); f = t - lo
        q = np.where(BAYER[s.yy % 4, s.xx % 4] < f, lo + 1, lo) / (steps - 1)
        col = top[None, None, :] + (bot - top)[None, None, :] * q[..., None]
        s.a[m] = col[m].astype(np.uint8); s.al[m] = True

    def rgrad(s, m, cx, cy, r, inner, outer, steps=6):
        inner, outer = np.array(inner, float), np.array(outer, float)
        d = np.sqrt((s.xx - cx) ** 2 + ((s.yy - cy)) ** 2) / r
        t = np.clip(d, 0, 1) * (steps - 1)
        lo = np.floor(t); f = t - lo
        q = np.where(BAYER[s.yy % 4, s.xx % 4] < f, lo + 1, lo) / (steps - 1)
        col = inner[None, None, :] + (outer - inner)[None, None, :] * q[..., None]
        s.a[m] = col[m].astype(np.uint8); s.al[m] = True

    def glow(s, cx, cy, r, col, k=0.5, m=None, levels=3):
        """Halo lumineux en paliers nets (style pixel art) ; damier 50 % seulement sur la frontière des paliers."""
        d = np.sqrt((s.xx - cx) ** 2 + ((s.yy - cy) * 1.0) ** 2) / r
        a = np.clip(1 - d, 0, 1) ** 1.2 * k                      # 0..k
        q = a / max(k, 1e-6) * levels                            # 0..levels
        lvl = np.floor(q)
        frac = q - lvl
        chk = ((s.xx + s.yy) % 2 == 0)
        lvl = np.where((frac > 0.82) & chk, lvl + 1, lvl)        # bord tramé d'un pixel environ
        lvl = np.clip(lvl, 0, levels)
        w = (lvl / levels) * k
        on = w > 0
        if m is not None:
            on &= m
        out = s.a.astype(float) * (1 - w[..., None]) + np.array(col, float)[None, None, :] * w[..., None]
        s.a[on] = out[on].astype(np.uint8)

    def tint(s, m, col, k=0.3):
        s.a[m] = (s.a[m].astype(float) * (1 - k) + np.array(col) * k).astype(np.uint8)

    def line(s, x0, y0, x1, y1, col):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for k in range(n):
            t = k / max(1, n - 1)
            s.px(round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t), col)

    def px(s, x, y, col):
        x, y = int(x), int(y)
        if 0 <= x < s.w and 0 <= y < s.h:
            s.a[y, x] = col; s.al[y, x] = True

    def sprite(s, rows, pal, x0, y0, mirror=False):
        for j, r in enumerate(rows):
            if mirror:
                r = r + r[::-1]
            for i, ch in enumerate(r):
                if ch != "." and ch in pal:
                    s.px(x0 + i, y0 + j, pal[ch])

    def paste(s, img_rgba, x0, y0):
        """Colle une image RGBA (sprite) en pixels pleins."""
        a = np.array(img_rgba)
        h, w = a.shape[:2]
        for j in range(h):
            yy = y0 + j
            if not 0 <= yy < s.h:
                continue
            for i in range(w):
                xx = x0 + i
                if 0 <= xx < s.w and a[j, i, 3] > 127:
                    s.a[yy, xx] = a[j, i, :3]; s.al[yy, xx] = True

    def text(s, xy, txt, col, size=10, font=TAHOMA, anchor="la", ol=None):
        """Texte pixel (sans anticrénelage), contour optionnel d'un pixel."""
        f = ImageFont.truetype(font, size)
        im = Image.new("L", (s.w, s.h), 0); d = ImageDraw.Draw(im); d.fontmode = "1"
        d.text(xy, txt, font=f, fill=255, anchor=anchor)
        m = np.array(im) > 0
        if ol is not None:
            s.outline(m, ol)
        s.fill(m, col)
        return m

    # ---------- sortie
    def img(s, k=1, rgba=False):
        if rgba:
            arr = np.dstack([s.a, (s.al * 255).astype(np.uint8)])
            im = Image.fromarray(arr, "RGBA")
        else:
            im = Image.fromarray(s.a)
        return im.resize((s.w * k, s.h * k), Image.NEAREST) if k != 1 else im
