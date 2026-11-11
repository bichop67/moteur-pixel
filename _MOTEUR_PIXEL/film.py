# FILM : ce qu'il faut au moteur pour les films « L'histoire des prophètes » (16:9, voix off, orbes qui jouent).
#
#  - ORBES : les prophètes et les figures vénérées ne sont JAMAIS dessinés. Ici, chacun est une boule de lumière qui
#    joue comme un personnage (place, va, apparaît, disparaît, champ / contre-champ…), avec son nom dessous.
#      orbe("MOUSSA", "MOUSSA", couleur="or")           puis, dans un scénario : MOUSSA place 600 / {va MOUSSA 820}
#    Poses : neutre, pale (lumière faible : peur, chagrin, faim), intense (lumière forte : joie, révélation).
#  - VOIX SANS CORPS : NARRATEUR et CORAN (toujours en voix off ; sous-titres sans vignette).
#  - THÈME « film » (kit.THEMES["film"]) : pas de bandeau, pas d'« abonne-toi », sous-titres de cinéma (une ligne
#    longue, sans vignette), référence en haut à droite, bandes noires de cinéma.
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import pxv

# ---------------------------------------------------------------- orbes
TONS = dict(
    or_=((255, 204, 104), (255, 250, 228)),        # prophètes
    bleu=((160, 208, 255), (240, 250, 255)),       # figures vénérées (mère, sœur…)
    rose=((255, 176, 196), (255, 240, 246)),
    blanc=((232, 238, 255), (255, 255, 255)),      # anges (petites orbes)
    vert=((150, 230, 180), (240, 255, 246)),
    ambre=((255, 186, 120), (255, 244, 226)),
)
ORBES = {}


def orbe(nom, label=None, couleur="or_", r=7, hauteur=40):
    """Déclare une orbe-personnage. r = rayon de la boule (pixels du dessin, x7 à l'écran) ; hauteur = hauteur du
    centre de la boule au-dessus du sol (40 ≈ la poitrine d'un adulte ; 22 pour un bébé dans un coffre)."""
    col, clair = TONS[couleur] if isinstance(couleur, str) else couleur
    ORBES[nom] = dict(label=(label if label is not None else nom), col=col, clair=clair, r=r, hauteur=hauteur)


def has(nom):
    return nom in ORBES or nom in VOIX_SEULES or nom in OBJETS_FILM


_FONT = "C:/Windows/Fonts/tahomabd.ttf"
_CACHE = {}


def _texte_1x(txt, col=(255, 255, 255), ol=(24, 18, 30), size=7):
    """Petit texte pixel (taille du dessin) avec contour, pour le nom sous l'orbe."""
    f = ImageFont.truetype(_FONT, size)
    d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
    bb = d0.textbbox((0, 0), txt, font=f)
    w, h = bb[2] - bb[0] + 4, bb[3] - bb[1] + 4
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    d.fontmode = "1"
    d.text((2 - bb[0], 2 - bb[1]), txt, font=f, fill=255)
    a = np.array(m) > 0
    e = a.copy()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        e |= np.roll(np.roll(a, dy, 0), dx, 1)
    out = np.zeros((h, w, 4), np.uint8)
    out[e] = (*ol, 235)
    out[a] = (*col, 255)
    return Image.fromarray(out, "RGBA")


def image(nom, pose="neutre", **_):
    """Sprite de l'orbe (taille du dessin ; le moteur l'agrandit x k). Le bas du sprite = le sol."""
    if nom in VOIX_SEULES:
        im = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        im.info.update(foot=1, ombre=0, lumineux=True)
        return im
    key = (nom, pose)
    if key in _CACHE:
        return _CACHE[key]
    if nom in OBJETS_FILM:
        _CACHE[key] = _OBJETS_DESSIN[nom](pose)
        return _CACHE[key]
    o = ORBES[nom]
    r, col, clair = o["r"], o["col"], o["clair"]
    force = dict(pale=0.45, intense=1.35).get(pose, 1.0)
    halo = int(r * (1.9 if pose == "intense" else 1.55))
    w = 2 * (r + halo) + 3
    cy = r + halo + 1                                       # centre de la boule
    h = cy + o["hauteur"]
    a = np.zeros((h, w, 4), np.float32)
    yy, xx = np.mgrid[0:h, 0:w]
    cx = (w - 1) / 2
    d = np.hypot(xx - cx, yy - cy)
    for k_, al in ((halo, 0.10), (halo * 0.72, 0.18), (halo * 0.48, 0.30)):      # halo en paliers (style pixel)
        m = (d <= r + k_)
        a[m, :3] = clair if k_ < halo * 0.5 else col
        a[m, 3] = np.maximum(a[m, 3], 255 * al * force)
    boule = d <= r
    t = np.clip(np.hypot(xx - (cx - r * 0.3), yy - (cy - r * 0.35)) / (r * 1.3), 0, 1)
    t = np.floor(t * 5) / 5                                   # dégradé en 5 paliers
    for c in range(3):
        a[..., c] = np.where(boule, clair[c] * (1 - t) + col[c] * t, a[..., c])
    a[boule, 3] = 255 * min(1.0, 0.55 + 0.45 * force)
    bord = boule & (d > r - 1)
    a[bord, :3] = [v * 0.78 for v in col]
    hl = np.hypot(xx - (cx - r * 0.38), yy - (cy - r * 0.42)) <= max(1.2, r * 0.22)
    a[hl, :3] = (255, 255, 255)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")
    # le nom est écrit à part, en petit et net, sous la boule (pxv.render_shot_v2)
    im.info.update(foot=h, ombre=0, lumineux=True, flotte=True, label=o["label"], cy=cy, r=r)
    _CACHE[key] = im
    return im


# ---------------------------------------------------------------- objets qui jouent comme des persos (film)
# COFFRE : le coffre de Moussa sur le Nil. Poses : neutre (fermé, une lueur dorée filtre sous le couvercle),
# ouvert (couvercle relevé : la petite orbe du bébé brille sur un lit de tissu), vide (fermé, sans lueur).
# Dans un scénario : COFFRE place 300 1180 / {va COFFRE 900} / COFFRE ouvert. Il flotte en tanguant à peine.
OBJETS_FILM = {"COFFRE", "BERCEAU", "PLATEAU", "BRAISE", "PIERRE", "SEAU", "BATON", "VEAU", "TABLETTES", "ROCHER", "PANIER", "BATEAU", "CLES", "CLES2", "CLES3", "TRESOR"}
_OBJETS_DESSIN = dict(COFFRE=lambda p: _coffre(p), BERCEAU=lambda p: _berceau(p), PLATEAU=lambda p: _plateau(p),
                      BRAISE=lambda p: _braise(p), PIERRE=lambda p: _pierre(p), SEAU=lambda p: _seau(p),
                      BATON=lambda p: _baton(p), VEAU=lambda p: _veau(p), TABLETTES=lambda p: _tablettes(p),
                      ROCHER=lambda p: _rocher(p), PANIER=lambda p: _panier(p), BATEAU=lambda p: _bateau(p),
                      CLES=lambda p: _cles(p), CLES2=lambda p: _cles(p), CLES3=lambda p: _cles(p),
                      TRESOR=lambda p: _tresor(p))


def _coffre(pose):
    W_, H_ = 34, 30
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    def rect(x0, y0, x1, y1):
        return (xx >= x0) & (xx <= x1) & (yy >= y0) & (yy <= y1)
    def put(m, c, al=255):
        a[m] = (*c, al)
    bois, sombre, clair = (128, 88, 52), (82, 54, 32), (170, 122, 74)
    or_ = (255, 214, 120)
    x0, x1, yb0, yb1 = 6, 27, 18, 25                       # caisse
    if pose == "ouvert":                                   # couvercle relevé vers l'arrière
        put(rect(x0 + 1, 9, x1 - 1, 12), sombre)
        put(rect(x0 + 2, 10, x1 - 2, 11), bois)
        put(rect(x0 + 1, 13, x1 - 1, 17), (232, 226, 210))          # le tissu, en plis
        put(rect(x0 + 1, 13, x1 - 1, 13), (250, 248, 240))
        for x in range(x0 + 3, x1 - 1, 4):
            put(rect(x, 14, x, 16), (204, 196, 180))
        cx, cy, r = 16.5, 13.5, 3.2                                  # la petite orbe du bébé (jamais un bébé dessiné)
        d = np.hypot(xx - cx, yy - cy)
        for rr, al in ((r + 5, 60), (r + 3, 110)):
            m = (d <= rr) & (a[..., 3] < 200)
            put(m, (255, 236, 170), al)
        put(d <= r, or_)
        put(np.hypot(xx - (cx - 1), yy - (cy - 1)) <= 1.1, (255, 255, 240))
    put(rect(x0, yb0, x1, yb1), bois)                                # caisse en planches
    for y in (20, 23):
        put(rect(x0, y, x1, y), sombre)
    put(rect(x0, yb0, x1, yb0), clair)
    for x in (x0 + 4, x1 - 4):                                       # liens de corde
        put(rect(x, yb0, x, yb1), (196, 170, 112))
    put(rect(x0, yb0, x0, yb1), sombre); put(rect(x1, yb0, x1, yb1), sombre)
    if pose != "ouvert":
        put(rect(x0 - 1, 14, x1 + 1, 17), bois)                      # couvercle bombé
        put(rect(x0, 13, x1, 13), clair)
        put(rect(x0 - 1, 17, x1 + 1, 17), sombre)
        if pose != "vide":                                           # lueur dorée sous le couvercle entrouvert
            put(rect(x0 + 2, 18, x1 - 2, 18), or_)
            d_ = ((xx - 16.5) / 13.0) ** 2 + ((yy - 18) / 5.0) ** 2
            for lim, al in ((1.0, 34), (0.55, 60)):
                m = (d_ <= lim) & (a[..., 3] < al)
                put(m, (255, 222, 150), al)
    eau = pose in ("neutre", "corde")                               # sur l'eau ; sinon posé au sol (ferme, ouvert, vide) ou porté
    if eau:
        for y, w_, al in ((26, 0, 150), (27, 3, 110), (28, 6, 70)):  # rides de l'eau autour du coffre
            put(rect(x0 - 2 - w_, y, x0 + 1 - w_ + 3, y) | rect(x1 - 1 + w_ - 3, y, x1 + 2 + w_, y), (220, 236, 246), al)
        put(rect(x0, 26, x1, 26), (40, 70, 96), 120)                 # ombre de la caisse dans l'eau
    contour = (a[..., 3] == 255)
    e = contour.copy()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        e |= np.roll(np.roll(contour, dy, 0), dx, 1)
    bord = e & ~contour & (yy < 26) & (a[..., 3] < 60)
    a[bord] = (34, 22, 16, 255)
    if pose == "corde":                                              # corde NON attachée : elle traîne dans l'eau
        m_ = 13                                                      # (marge des deux côtés : le coffre reste centré)
        b = np.zeros((H_, W_ + 2 * m_, 4), np.uint8)
        b[:, m_:m_ + W_] = a
        a = b
        for i in range(14):
            x, y = m_ + x0 - 1 - i, min(27, 21 + (i + 1) // 2)
            a[y, x] = (206, 178, 118, 255) if y < 26 else (176, 152, 104, 170)
            if y >= 26:
                a[y - 1, x] = (150, 170, 190, 90)
    im = Image.fromarray(a, "RGBA")
    if eau:
        im.info.update(foot=27, ombre=0, flotte=True, flotte_amp=0.45)
    elif pose == "porte":                                            # porté à hauteur des mains : 22 lignes vides dessous,
        b = Image.new("RGBA", (im.width, im.height + 22), (0, 0, 0, 0))   # placé juste devant les porteurs (y + 2)
        b.paste(im, (0, 0))
        im = b
        im.info.update(foot=26 + 22, ombre=0)
    else:                                                            # posé au sol
        im.info.update(foot=26, ombre=30)
    return im


def _contour(a, yy, limite_y=None):
    """Contour sombre d'un pixel autour des parties opaques (style du moteur)."""
    plein = (a[..., 3] == 255)
    e = plein.copy()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        e |= np.roll(np.roll(plein, dy, 0), dx, 1)
    bord = e & ~plein & (a[..., 3] < 60)
    if limite_y is not None:
        bord &= yy < limite_y
    a[bord] = (34, 22, 16, 255)


def _orbe_bebe(a, xx, yy, cx, cy, r=3.2):
    """La petite orbe dorée du bébé (jamais un bébé dessiné), avec son halo."""
    d = np.hypot(xx - cx, yy - cy)
    for rr, al in ((r + 5, 60), (r + 3, 110)):
        m = (d <= rr) & (a[..., 3] < 200)
        a[m] = (255, 236, 170, al)
    a[d <= r] = (255, 214, 120, 255)
    a[np.hypot(xx - (cx - 1), yy - (cy - 1)) <= 1.1] = (255, 255, 240, 255)


def _berceau(pose):
    """Couffin d'osier posé au sol, un tissu blanc ; pose neutre : la petite orbe du bébé dedans ; vide : sans l'orbe."""
    W_, H_ = 38, 26
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    cx = 18.5
    osier, sombre, clair = (200, 162, 98), (142, 108, 62), (228, 198, 138)
    corps = (((xx - cx) / 15.0) ** 2 + ((yy - 15) / 8.0) ** 2 <= 1) & (yy >= 15)
    corps |= (xx >= cx - 15) & (xx <= cx + 15) & (yy >= 15) & (yy <= 17)
    a[corps] = (*osier, 255)
    for x in range(int(cx - 14), int(cx + 15), 3):                    # tressage
        a[corps & (xx == x)] = (*sombre, 255)
    for y in (18, 21):
        a[corps & (yy == y) & ((xx // 2) % 2 == 0)] = (*clair, 255)
    a[corps & (yy >= 22)] = (*sombre, 255)
    if pose not in ("vide", "porte_vide"):                            # le tissu, puis l'orbe du bébé
        tissu = ((((xx - cx) / 12.5) ** 2 + ((yy - 14) / 2.6) ** 2) <= 1)
        a[tissu] = (238, 232, 218, 255)
        a[tissu & (yy <= 12)] = (252, 250, 244, 255)
        _orbe_bebe(a, xx, yy, cx, 10.5)
    bord = (((xx - cx) / 16.0) ** 2 + ((yy - 15) / 2.2) ** 2 <= 1) & ~((((xx - cx) / 13.5) ** 2 + ((yy - 14.6) / 1.4) ** 2) <= 1)
    a[bord & (yy >= 14)] = (*clair, 255)
    a[bord & (yy < 14)] = (*osier, 255)
    _contour(a, yy, limite_y=24)
    im = Image.fromarray(a, "RGBA")
    if pose in ("porte", "porte_vide"):                                # porté à hauteur des mains (placé juste devant les porteurs)
        b = Image.new("RGBA", (im.width, im.height + 22), (0, 0, 0, 0))
        b.paste(im, (0, 0))
        im = b
        im.info.update(foot=24 + 22, ombre=0)
        return im
    im.info.update(foot=24)
    return im


def _plateau(pose):
    """Plateau doré posé sur un petit pied : deux perles qui brillent, deux braises rouges ; pose « prise » : une braise
    a été prise (il n'en reste qu'une)."""
    W_, H_ = 40, 24
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    cx = 20.0
    pied = (xx >= cx - 3) & (xx <= cx + 3) & (yy >= 15) & (yy <= 21)
    a[pied] = (176, 130, 50, 255)
    a[(xx >= cx - 6) & (xx <= cx + 6) & (yy >= 20) & (yy <= 21)] = (150, 108, 40, 255)
    dessus = (((xx - cx) / 17.0) ** 2 + ((yy - 13) / 3.6) ** 2) <= 1
    a[dessus] = (226, 182, 82, 255)
    a[dessus & (yy >= 15)] = (176, 130, 50, 255)
    a[dessus & (((xx - cx) / 14.5) ** 2 + ((yy - 12.6) / 2.4) ** 2 <= 1)] = (246, 214, 120, 255)
    for px_ in (cx - 10, cx - 5):                                     # deux perles
        d = np.hypot(xx - px_, yy - 11.5)
        a[d <= 2.0] = (236, 236, 244, 255)
        a[(d <= 2.0) & (yy >= 12.5)] = (190, 192, 206, 255)
        a[np.hypot(xx - (px_ - 0.6), yy - 10.8) <= 0.8] = (255, 255, 255, 255)
    braises = (cx + 5, cx + 10) if pose != "prise" else (cx + 10,)
    for bx in braises:                                                # braises : noir rougeoyant, cœur orange
        d = np.hypot(xx - bx, (yy - 11.5) * 1.2)
        for rr, al in ((5.0, 50), (3.6, 90)):
            m = (d <= rr) & (a[..., 3] < 200)
            a[m] = (255, 120, 50, al)
        a[d <= 2.2] = (110, 30, 24, 255)
        a[d <= 1.4] = (236, 86, 34, 255)
        a[np.hypot(xx - bx, yy - 11.2) <= 0.7] = (255, 214, 120, 255)
    _contour(a, yy, limite_y=22)
    im = Image.fromarray(a, "RGBA")
    im.info.update(foot=22, lumineux=True)
    return im


def _pierre(pose):
    """La grosse pierre ronde qui ferme le puits de Madyan (vue de biais) : PIERRE place 440 1226 (sur la bouche)."""
    W_, H_ = 52, 18
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    dessus = ((xx - 25.5) / 24.0) ** 2 + ((yy - 7) / 6.0) ** 2 <= 1
    flanc = (((xx - 25.5) / 24.0) ** 2 + ((yy - 11) / 6.0) ** 2 <= 1) | ((np.abs(xx - 25.5) <= 24) & (yy >= 7) & (yy <= 11))
    a[flanc] = (112, 104, 96, 255)
    a[flanc & (yy >= 13)] = (88, 82, 76, 255)
    a[dessus] = (156, 148, 136, 255)
    a[dessus & (((xx - 21) / 15.0) ** 2 + ((yy - 5.5) / 3.0) ** 2 <= 1)] = (178, 170, 156, 255)
    for (x0, y0, x1, y1) in ((14, 6, 22, 9), (30, 4, 36, 8), (36, 8, 42, 7)):
        for t in np.linspace(0, 1, 12):
            a[int(round(y0 + (y1 - y0) * t)), int(round(x0 + (x1 - x0) * t))] = (110, 102, 94, 255)
    _contour(a, yy)
    im = Image.fromarray(a, "RGBA")
    im.info.update(foot=17, ombre=40)
    return im


def _seau(pose):
    """Le seau de cuir et de bois qu'on remonte du puits, avec sa corde."""
    W_, H_ = 14, 26
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    a[(xx == 7) & (yy <= 12)] = (196, 170, 112, 255)
    corps = (yy >= 13) & (yy <= 23) & (np.abs(xx - 7) <= 4 + (23 - yy) * 0.15)
    a[corps] = (130, 92, 56, 255)
    a[corps & ((yy == 15) | (yy == 21))] = (86, 60, 36, 255)
    a[(yy == 13) & (np.abs(xx - 7) <= 5)] = (100, 150, 176, 255)
    _contour(a, yy)
    im = Image.fromarray(a, "RGBA")
    im.info.update(foot=24, ombre=0)
    return im


def _baton(pose):
    """Le bâton de berger de Moussa (bois clair, poignée recourbée), debout : BATON place x y (à côté de l'orbe)."""
    W_, H_ = 12, 50
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    bois, sombre = (150, 108, 64), (100, 70, 40)
    a[(xx >= 5) & (xx <= 6) & (yy >= 6) & (yy <= 48)] = (*bois, 255)
    a[(xx == 6) & (yy >= 6) & (yy <= 48)] = (*sombre, 255)
    for (x, y) in ((5, 5), (5, 4), (6, 3), (7, 2), (8, 2), (9, 3), (9, 4), (9, 5), (8, 6)):
        a[y, x] = (*bois, 255)
    a[(yy == 30) & (xx >= 5) & (xx <= 6)] = (*sombre, 255)
    _contour(a, yy)
    im = Image.fromarray(a, "RGBA")
    im.info.update(foot=49, ombre=8)
    return im


def _veau(pose):
    """La statue du veau d'or sur son socle de pierre (une idole : on la montre pour ce qu'elle est)."""
    import animaux
    sp, _o = animaux.vache((226, 182, 70))
    v = sp.img()
    a = np.array(v)
    m = a[..., 3] > 0
    g = a[..., :3].astype(np.float32).mean(axis=-1)
    a[m, 0] = np.clip(120 + g[m] * 0.6, 0, 255)                     # tout en or, reflets
    a[m, 1] = np.clip(84 + g[m] * 0.5, 0, 255)
    a[m, 2] = np.clip(20 + g[m] * 0.15, 0, 255)
    v = Image.fromarray(a, "RGBA")
    W_, H_ = v.width, v.height + 14
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    im.alpha_composite(v, (0, 0))
    soc = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    bloc = (xx >= 10) & (xx <= W_ - 12) & (yy >= v.height - 2) & (yy <= H_ - 2)
    soc[bloc] = (150, 140, 128, 255)
    soc[bloc & (yy <= v.height)] = (186, 176, 160, 255)
    soc[bloc & (yy >= H_ - 4)] = (110, 102, 94, 255)
    s_ = Image.fromarray(soc, "RGBA")
    s_.alpha_composite(im)
    im = s_
    im.info.update(foot=H_ - 2, ombre=40, lumineux=True)
    return im


def _tablettes(pose):
    """Les Tables : deux tablettes de pierre claire au sommet arrondi, couvertes de lignes, entourées d'une lueur douce ;
    portées à hauteur des mains (comme le coffre « porte ») ; pose « sol » : posées par terre."""
    W_, H_ = 30, 26
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    d = np.hypot(xx - 15, (yy - 12) * 1.1)
    for rr, al in ((14, 40), (11, 70)):
        a[(d <= rr)] = (255, 244, 210, al)
    for x0 in (6, 16):
        t = ((xx >= x0) & (xx <= x0 + 8) & (yy >= 8) & (yy <= 22)) | (np.hypot(xx - (x0 + 4), yy - 8) <= 4.2)
        a[t] = (226, 220, 206, 255)
        a[t & (xx == x0 + 8)] = (180, 172, 160, 255)
        for y in range(10, 21, 2):
            a[t & (yy == y) & (xx >= x0 + 2) & (xx <= x0 + 6)] = (150, 142, 132, 255)
    _contour(a, yy)
    im = Image.fromarray(a, "RGBA")
    if pose == "sol":
        im.info.update(foot=23, ombre=20, lumineux=True)
        return im
    b = Image.new("RGBA", (W_, H_ + 22), (0, 0, 0, 0))
    b.paste(im, (0, 0))
    b.info.update(foot=23 + 22, ombre=0, lumineux=True)
    return b


def _panier(pose):
    """Le panier d'osier du voyage (18:61) : un poisson dedans (sa queue dépasse) ; « vide » : sans le poisson ;
    « porte » : porté à hauteur des mains (à côté de l'orbe de Youcha')."""
    W_, H_ = 24, 16
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    corps = (((xx - 11.5) / 10.5) ** 2 + ((yy - 9) / 6.5) ** 2 <= 1) & (yy >= 6)
    osier, sombre = (186, 140, 84), (130, 92, 52)
    a[corps] = (*osier, 255)
    a[corps & (((xx + yy) // 2) % 2 == 0)] = (*sombre, 255)
    a[corps & (yy == 6)] = (210, 170, 110, 255)
    if pose not in ("vide", "porte_vide"):
        queue = ((xx >= 16) & (xx <= 20) & (yy >= 1) & (yy <= 6) & (np.abs(xx - 18) <= (6 - yy) * 0.6 + 0.5))
        a[queue] = (176, 190, 204, 255)
        a[(xx >= 6) & (xx <= 15) & (yy == 5)] = (196, 208, 220, 255)
    _contour(a, yy)
    im = Image.fromarray(a, "RGBA")
    if pose in ("porte", "porte_vide"):
        b = Image.new("RGBA", (W_, H_ + 22), (0, 0, 0, 0))
        b.paste(im, (0, 0))
        b.info.update(foot=H_ - 1 + 22, ombre=0)
        return b
    im.info.update(foot=H_ - 1, ombre=18)
    return im


def _bateau(pose):
    """Le petit bateau des pêcheurs pauvres (18:71) : coque de planches, un mât court, un filet ; « breche » : une
    planche arrachée sur le flanc, l'eau qui entre. Il flotte (tangue à peine) ; le bas de l'image = la ligne d'eau."""
    W_, H_ = 84, 46
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    from PIL import ImageDraw
    m = Image.new("L", (W_, H_), 0)
    ImageDraw.Draw(m).polygon([(2, 28), (82, 28), (74, 42), (12, 42)], fill=255)
    coque = np.array(m) > 0
    bois, sombre, clair = (132, 90, 56), (92, 60, 38), (168, 122, 80)
    a[coque] = (*bois, 255)
    for y in (31, 35, 39):
        a[coque & (yy == y)] = (*sombre, 255)
    a[coque & (yy <= 29)] = (*clair, 255)
    mat = (xx >= 40) & (xx <= 41) & (yy >= 4) & (yy <= 28)
    a[mat] = (110, 76, 46, 255)
    voile = (xx >= 42) & (xx <= 47) & (yy >= 6) & (yy <= 22) & (xx - 42 <= (yy - 6) * 0.45 + 1)
    a[voile] = (226, 214, 186, 255)
    filet = (xx >= 10) & (xx <= 26) & (yy >= 23) & (yy <= 28) & ((xx + yy) % 3 == 0)
    a[filet] = (150, 140, 120, 255)
    if pose == "breche":                                                       # la planche arrachée, l'eau qui entre
        trou = (xx >= 50) & (xx <= 62) & (yy >= 33) & (yy <= 37)
        a[trou & coque] = (40, 26, 18, 255)
        a[(xx >= 50) & (xx <= 62) & (yy == 38) & coque] = (110, 170, 214, 255)
        eau = (xx >= 14) & (xx <= 70) & (yy >= 26) & (yy <= 27)
        a[eau] = (110, 170, 214, 255)
    _contour(a, yy)
    im = Image.fromarray(a, "RGBA")
    im.info.update(foot=40, ombre=0, flotte=True, flotte_amp=0.8)
    return im


def _cles(pose):
    """Un énorme trousseau de clés de fer (28:76 : les clés pesaient lourd à toute une bande d'hommes forts) : un gros
    anneau et de longues clés qui pendent en éventail ; « porte » : tenu à hauteur des mains."""
    W_, H_ = 26, 30
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    fer, clair, sombre = (112, 112, 120), (176, 176, 186), (74, 74, 82)
    d = np.hypot(xx - 13, yy - 6)
    a[(d <= 5.6) & (d >= 3.6)] = (*fer, 255)                                  # l'anneau
    a[(d <= 5.6) & (d >= 4.6) & (yy <= 5)] = (*clair, 255)
    for ang in (-0.42, -0.21, 0.0, 0.21, 0.42):                                # les clés qui pendent
        x0_, y0_ = 13 + 5 * math.sin(ang), 10
        for t in range(16):
            x_ = int(round(x0_ + t * math.sin(ang)))
            y_ = int(round(y0_ + t * math.cos(ang)))
            if 0 <= x_ < W_ - 1 and 0 <= y_ < H_:
                a[y_, x_] = (*fer, 255)
                a[y_, x_ + 1] = (*(clair if t < 3 else sombre), 255)
        xb, yb = int(round(x0_ + 15 * math.sin(ang))), int(round(y0_ + 15 * math.cos(ang)))
        for (dx, dy) in ((2, 0), (3, 0), (2, -2), (3, -2)):                    # le panneton (les dents)
            if 0 <= xb + dx < W_ and 0 <= yb + dy < H_:
                a[yb + dy, xb + dx] = (*fer, 255)
    _contour(a, yy)
    im = Image.fromarray(a, "RGBA")
    if pose != "porte":
        im.info.update(foot=H_ - 1, ombre=16)
        return im
    b = Image.new("RGBA", (W_, H_ + 14), (0, 0, 0, 0))
    b.paste(im, (0, 0))
    b.info.update(foot=H_ + 13, ombre=0)
    return b


def _tresor(pose):
    """Un coffre plein d'or (le trésor caché sous le mur, 18:82)."""
    W_, H_ = 30, 22
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    corps = (xx >= 2) & (xx <= 27) & (yy >= 9) & (yy <= 20)
    a[corps] = (120, 74, 44, 255)
    a[corps & (yy == 9)] = (156, 104, 62, 255)
    for x in (5, 24):
        a[corps & (xx >= x) & (xx <= x + 1)] = (90, 90, 96, 255)
    a[(xx >= 13) & (xx <= 16) & (yy >= 11) & (yy <= 13)] = (236, 192, 72, 255)
    tas = (((xx - 14.5) / 12.5) ** 2 + ((yy - 9) / 5) ** 2 <= 1) & (yy <= 9)
    a[tas] = (236, 192, 72, 255)
    a[tas & ((xx * 7 + yy * 3) % 5 == 0)] = (255, 232, 140, 255)
    _contour(a, yy)
    im = Image.fromarray(a, "RGBA")
    im.info.update(foot=H_ - 1, ombre=24, lumineux=False)
    return im


def _rocher(pose):
    """Le rocher des douze sources (2:60) : un bloc de pierre carré, gris, posé au sol (le même que sur le dos de l'âne,
    en plus grand). ROCHER place x 1250 : son sommet arrive à hauteur des jets de {sources x 1240}."""
    W_, H_ = 34, 24
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    from PIL import ImageDraw
    m = Image.new("L", (W_, H_), 0)
    ImageDraw.Draw(m).polygon([(4, 4), (26, 2), (31, 6), (31, 21), (6, 22), (2, 19), (2, 7)], fill=255)
    roc = np.array(m) > 0
    a[roc] = (150, 144, 136, 255)
    a[roc & (yy <= 7)] = (186, 180, 170, 255)                                  # le dessus, plus clair
    a[roc & (xx >= 26)] = (116, 110, 104, 255)                                 # le flanc à l'ombre
    for (x0, y0, x1, y1) in ((11, 9, 15, 15), (19, 12, 21, 19)):               # fissures
        n_ = max(abs(x1 - x0), abs(y1 - y0)) + 1
        for i in range(n_):
            x_, y_ = round(x0 + (x1 - x0) * i / (n_ - 1)), round(y0 + (y1 - y0) * i / (n_ - 1))
            if roc[y_, x_]:
                a[y_, x_] = (104, 98, 92, 255)
    _contour(a, yy)
    im = Image.fromarray(a, "RGBA")
    im.info.update(foot=H_ - 1, ombre=30)
    return im


def _braise(pose):
    """Une braise seule (rougeoie, petit halo) : à faire glisser du plateau jusqu'à l'enfant ({derive BRAISE x y 2s})."""
    W_, H_ = 14, 14
    a = np.zeros((H_, W_, 4), np.uint8)
    yy, xx = np.mgrid[0:H_, 0:W_]
    d = np.hypot(xx - 7, (yy - 7) * 1.15)
    for rr, al in ((6.0, 50), (4.2, 100)):
        a[d <= rr] = (255, 120, 50, al)
    a[d <= 2.3] = (110, 30, 24, 255)
    a[d <= 1.5] = (236, 86, 34, 255)
    a[np.hypot(xx - 7, yy - 6.6) <= 0.7] = (255, 214, 120, 255)
    im = Image.fromarray(a, "RGBA")
    im.info.update(foot=10, ombre=0, lumineux=True, flotte=True, flotte_amp=0.3)
    return im


# ---------------------------------------------------------------- voix sans corps (narrateur, voix du Coran)
VOIX_SEULES = {"NARRATEUR", "CORAN"}
pxv.SPEAKER.setdefault("NARRATEUR", dict(ol=(26, 22, 32), frame=(220, 220, 230), name="NARRATEUR"))
pxv.SPEAKER.setdefault("CORAN", dict(ol=(70, 48, 8), frame=(250, 220, 140), name="CORAN", texte=(255, 234, 168)))


# ---------------------------------------------------------------- les orbes de l'histoire de Moussa (épisode 14)
# tailles pensées pour les décors du film (persos à l'échelle k = 4) ; « or_ » = prophètes
orbe("MOUSSA", "MOUSSA", "or_", r=10, hauteur=42)
orbe("HAROUN", "HAROUN", "or_", r=10, hauteur=42)
orbe("MOUSSA_ENFANT", "MOUSSA", "or_", r=8, hauteur=28)
orbe("MOUSSA_BEBE", "MOUSSA", "or_", r=6, hauteur=12)
orbe("HAROUN_BEBE", "HAROUN", "or_", r=6, hauteur=12)
orbe("SA_MERE", "SA MÈRE", "bleu", r=9, hauteur=40)
orbe("SA_SOEUR", "SA SŒUR", "rose", r=8, hauteur=32)
orbe("ASIYA", "ASIYA", "ambre", r=9, hauteur=40)
orbe("MARYAM", "MARYAM", "blanc", r=9, hauteur=40)
orbe("VIEIL_HOMME", "LE VIEIL HOMME", "vert", r=10, hauteur=40)   # le Coran ne le nomme pas (avis divergents)
orbe("FILLE_1", "LA FILLE", "rose", r=8, hauteur=36)     # celle qui vient chercher Moussa (puis SA_FEMME)
orbe("FILLE_2", "SA SŒUR", "rose", r=8, hauteur=36)
orbe("SA_FEMME", "SA FEMME", "rose", r=8, hauteur=36)
orbe("YAQOUB", "YAQOUB", "or_", r=9, hauteur=40)
orbe("YOUSSOUF", "YOUSSOUF", "or_", r=9, hauteur=40)
orbe("KHIDR", "AL-KHIDR", "vert", r=10, hauteur=42)                # statut discuté : orbe, jamais dessiné
orbe("YOUCHA", "YOUCHA", "or_", r=8, hauteur=38)
orbe("ANGE_MORT", "L'ANGE", "blanc", r=6, hauteur=40)                     # l'ange de la mort (Boukhari 3407)                    # le jeune compagnon de Moussa (nommé dans Boukhari 3401)
orbe("PROPHETE", "LE PROPHÈTE", "or_", r=10, hauteur=42)          # Mouhammad (ﷺ jamais écrit à l'écran)
orbe("ANGE_1", "LES ANGES", "blanc", r=5, hauteur=30)                 # anges : jamais dessinés, petites orbes blanches
orbe("ANGE_2", "", "blanc", r=5, hauteur=30)
orbe("ANGE_3", "", "blanc", r=5, hauteur=30)
orbe("ANGE_4", "", "blanc", r=5, hauteur=30)
