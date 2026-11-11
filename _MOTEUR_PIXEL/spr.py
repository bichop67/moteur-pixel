# Sprites pixel art : petite toile RGBA, formes au pixel près, contour, ombrage, miroir, agrandissement.
import numpy as np
from PIL import Image

INK = (22, 16, 26, 255)


class Spr:
    def __init__(s, w, h):
        s.w, s.h = w, h
        s.a = np.zeros((h, w, 4), np.uint8)
        s.part = np.zeros((h, w), np.int16)          # numéro de pièce (pour les traits intérieurs)
        s.np = 0

    # ---------- masques
    def m_rect(s, x0, y0, x1, y1):
        m = np.zeros((s.h, s.w), bool)
        m[max(0, y0):max(0, y1 + 1), max(0, x0):max(0, x1 + 1)] = True
        return m

    def m_ell(s, cx, cy, rx, ry):
        yy, xx = np.mgrid[0:s.h, 0:s.w]
        return ((xx - cx) / (rx + 0.01)) ** 2 + ((yy - cy) / (ry + 0.01)) ** 2 <= 1.0

    def m_poly(s, pts):
        from PIL import ImageDraw
        im = Image.new("L", (s.w, s.h), 0)
        ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255)
        return np.array(im) > 0

    def m_line(s, pts, w=1):
        """Trait épais (bras, jambes) le long d'une suite de points."""
        from PIL import ImageDraw
        im = Image.new("L", (s.w, s.h), 0)
        d = ImageDraw.Draw(im)
        d.line([(float(x), float(y)) for x, y in pts], fill=255, width=w, joint="curve")
        r = w / 2.0
        for x, y in pts:
            d.ellipse([x - r + 0.5, y - r + 0.5, x + r - 0.5, y + r - 0.5], fill=255)
        return np.array(im) > 0

    # ---------- peinture
    def paint(s, m, col, newpart=True):
        if newpart:
            s.np += 1
        s.a[m] = (*col, 255) if len(col) == 3 else col
        s.part[m] = s.np
        return m

    def tone(s, m, col):
        """Recolore des pixels déjà peints (ombre/reflet) sans changer de pièce."""
        mm = m & (s.a[..., 3] > 0)
        s.a[mm] = (*col, 255)

    def px(s, x, y, col):
        if 0 <= x < s.w and 0 <= y < s.h:
            s.a[y, x] = (*col, 255) if len(col) == 3 else col

    def pxs(s, pts, col):
        for x, y in pts:
            s.px(x, y, col)

    def shade(s, m, col, dx=-1, dy=0, depth=2):
        """Ombre portée à l'intérieur de la forme, côté opposé à la lumière (lumière venant de (dx,dy) inversé)."""
        inner = m.copy()
        for k in range(1, depth + 1):
            inner &= np.roll(np.roll(m, dx * k, axis=1), dy * k, axis=0)
        s.tone(m & ~inner, col)

    def light(s, m, col, dx=1, dy=1, depth=1):
        s.shade(m, col, dx, dy, depth)

    # ---------- contours
    def outline(s, col=INK):
        """Contour extérieur d'un pixel autour de tout le sprite."""
        o = s.a[..., 3] > 0
        e = o.copy()
        e[1:, :] |= o[:-1, :]; e[:-1, :] |= o[1:, :]; e[:, 1:] |= o[:, :-1]; e[:, :-1] |= o[:, 1:]
        s.a[e & ~o] = col

    def inner_lines(s, pairs, col=INK):
        """Trait sombre là où deux pièces données se touchent (ex. bras devant le torse)."""
        for top, under in pairs:
            t = s.part == top
            u = s.part == under
            edge = u & (np.roll(t, 1, 0) | np.roll(t, -1, 0) | np.roll(t, 1, 1) | np.roll(t, -1, 1))
            s.a[edge] = col

    def sel_out(s, k=0.55):
        """Contour « sélectif » : le contour prend une teinte sombre de la couleur voisine (rendu plus doux)."""
        pass

    # ---------- sortie
    def img(s, scale=1, mirror=False):
        im = Image.fromarray(s.a, "RGBA")
        if mirror:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if scale != 1:
            im = im.resize((s.w * scale, s.h * scale), Image.NEAREST)
        return im


def stamp(sp, rows, pal, x0, y0):
    """Pose une petite carte ASCII (détails du visage, mains…)."""
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch in pal:
                c = pal[ch]
                if c is None:
                    sp.a[y0 + j, x0 + i] = (0, 0, 0, 0)
                else:
                    sp.px(x0 + i, y0 + j, c)
