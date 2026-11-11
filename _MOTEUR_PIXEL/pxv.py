# Moteur vidéo PIXEL (dialogue à deux voix, style « Faux Positif ») — 1080x1920, 30 i/s.
# Plans = décor pixel (x4) + persos (échelle entière) + bulles + tableau ; caméra douce ; sous-titres pixel
# avec vignette du perso qui parle ; filtre film (grain, vignette) ; bouches calées sur la voix.
import os, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import sets, duo
from px import Px, TAHOMA
try:
    import lieux                           # nouveaux décors (s'ajoutent à sets.DECORS)
except ImportError:
    lieux = None

W, H, FPS = 1080, 1920, 30
SR = 48000
# BASE = le dossier qui contient _MOTEUR_PIXEL, _MUSIQUES, _BRUITAGES… (11/11/2026 : plus de chemin « C:/Users/… » en
# dur, pour que le moteur marche sur un autre ordinateur ; sur le PC d'origine les chemins sont les mêmes qu'avant)
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
FF = os.path.expanduser("~").replace("\\", "/") + "/AppData/Local/Temp/ia501/bin/ffmpeg.exe"
if not os.path.exists(FF):                 # Windows vide le dossier Temp (fichiers de plus d'une semaine) : copie du paquet Python
    try:
        import imageio_ffmpeg
        FF = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:                      # noqa: BLE001
        import shutil
        FF = shutil.which("ffmpeg") or FF  # sinon un ffmpeg installé sur l'ordinateur (voir INSTALLATION.md)
XF = 0.22                                 # fondu enchaîné entre deux plans (pas de coupe sèche)
SUB_Y = 1465                               # hauteur des sous-titres (au-dessus de la légende TikTok)
SEGOE_BLACK = "C:/Windows/Fonts/seguibl.ttf"

SPEAKER = dict(P=dict(ol=(118, 18, 30), frame=(226, 62, 62), name="P"),
               G=dict(ol=(14, 70, 76), frame=(46, 176, 160), name="G"))


def speaker(who):
    """Couleurs du sous-titre et de la vignette : le duo, puis les personnages du créateur (cast.py)."""
    if who in SPEAKER:
        return SPEAKER[who]
    import cast
    if cast.has(who):
        return cast.speaker(who)
    return dict(ol=(40, 40, 50), frame=(200, 200, 210), name=who, side="right", bg=(50, 50, 60))


class Theme:
    """Habillage d'une chaîne : bandeau, filtre film, sous-titres, appel à s'abonner.
    Theme() sans réglage = l'habillage de « VALABLE OU PAS ? » (identique aux vidéos déjà livrées)."""

    def __init__(s, bandeau="VALABLE OU PAS ?", bandeau_fond=(24, 96, 104), bandeau_accent=(250, 196, 70),
                 bandeau_texte=(255, 255, 255), bandeau_contour=(20, 60, 70), bandeau_xy=(40, 150), grain=5.0,
                 chaleur=(1.02, 1.0, 0.965), vignette=0.38, lignes=True, sous_titres_y=1465,
                 cta=("ABONNE-TOI", "POUR LA SUITE"), cta_couleurs=((255, 255, 255), (120, 20, 30), (255, 214, 90), (90, 40, 10)),
                 cotes=None, etiquette=((30, 22, 30), (250, 240, 220)), carte="carte",
                 format="portrait", ombres=True, lumiere=True, parallaxe=True,
                 film=False, st_maxc=26, st_largeur=16, vignette_st=True, src_droite=False, cinema=0):
        # FILM (film.py, thème « film ») : sous-titres de cinéma (st_maxc lettres par sous-titre, st_largeur par ligne,
        # sans vignette), référence en haut à droite, bandes noires de cinéma (cinema = hauteur d'une bande en px)
        s.film, s.st_maxc, s.st_largeur, s.vignette_st = film, st_maxc, st_largeur, vignette_st
        s.src_droite, s.cinema = src_droite, cinema
        s.carte = carte                    # fond de la carte d'accroche (« carte », « carte_rouge »…)
        s.format = format                  # "portrait" (Shorts 1080x1920) ou "paysage" (vidéos longues 1920x1080)
        s.ombres, s.lumiere, s.parallaxe = ombres, lumiere, parallaxe     # ombres au sol, lumière sur les persos, relief
        if format == "paysage":
            if sous_titres_y == 1465:
                sous_titres_y = 952
            if bandeau_xy == (40, 150):
                bandeau_xy = (40, 40)
        s.bandeau, s.bandeau_fond, s.bandeau_accent = bandeau, bandeau_fond, bandeau_accent
        s.bandeau_texte, s.bandeau_contour, s.bandeau_xy = bandeau_texte, bandeau_contour, bandeau_xy
        s.grain, s.chaleur, s.vignette, s.lignes = grain, chaleur, vignette, lignes
        s.sous_titres_y, s.cta, s.cta_couleurs = sous_titres_y, cta, cta_couleurs
        s.cotes = cotes or {}
        s.etiquette = etiquette

    def band_img(s, k=4):
        if not s.bandeau:
            return None
        a = pixel_text(s.bandeau, s.bandeau_texte, s.bandeau_contour, size=9, k=k)
        pad = 3 * k
        im = Image.new("RGBA", (a.width + 2 * pad, a.height + pad), (*s.bandeau_fond, 240))
        d = ImageDraw.Draw(im); d.rectangle([0, 0, k * 2, im.height], fill=(*s.bandeau_accent, 255))
        im.alpha_composite(a, (pad + k, pad // 2))
        return im

    def side(s, who):
        if who in s.cotes:
            return s.cotes[who]
        sp = speaker(who)
        return sp.get("side") or ("left" if who == "G" else "right")


class Silence:
    """Dialogue sans voix (démo, plan muet) : parle = [(qui, t0, t1)] pour animer les bouches."""

    def __init__(s, dur, parle=()):
        s.dur, s.lines, s.parle, s.tempo = dur, [], list(parle), 1.0
        s.voice = np.zeros(int(dur * SR) + SR, np.float32)
        s.env = {}

    def talking(s, who, t):
        for w, a, b in s.parle:
            if w == who and a <= t < b:
                return (int(t * FPS) // 3) % 3 != 2
        return False

    def chunks(s, maxc=26):
        return []


def _moyenne_glissante(x, k):
    """Moyenne glissante de largeur k, alignée comme np.convolve(x, np.ones(k) / k, mode="same"), mais en O(n)."""
    n = len(x)
    c = np.concatenate(([0.0], np.cumsum(x, dtype=np.float64)))
    i = np.arange(n)
    lo = np.clip(i + (k - 1) // 2 - k + 1, 0, n)
    hi = np.clip(i + (k - 1) // 2 + 1, 0, n)
    return ((c[hi] - c[lo]) / k).astype(x.dtype if x.dtype.kind == "f" else np.float64)


def priorite_basse():
    """Le rendu passe après les applications de l'utilisateur (navigateur, jeux…) : le PC reste fluide."""
    try:
        import ctypes
        k = ctypes.windll.kernel32
        k.SetPriorityClass(k.GetCurrentProcess(), 0x00004000)        # BELOW_NORMAL_PRIORITY_CLASS
    except Exception:
        pass


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * x * (x * (x * 6 - 15) + 10)


# =================================================================== audio
def _couche(spr):
    """Sprite d'un perso étendu au sol : tourné d'un quart de tour (la tête à gauche), posé sur sa ligne la plus basse."""
    im = spr.transpose(Image.ROTATE_90)
    al = np.array(im)[..., 3]
    lignes = np.where(al.max(axis=1) > 0)[0]
    im.info = dict(spr.info)
    im.info.update(foot=int(lignes.max()) + 1 if len(lignes) else im.height, ombre=34)
    return im


def _incline(spr, angle):
    """Perso qui tombe / se relève : penché de `angle` degrés (0 = debout, 90 = étendu comme _couche), tourné autour de
    son centre et posé sur son point le plus bas (le passage debout -> étendu est continu, sans saut)."""
    if angle <= 0.5:
        return spr
    if angle >= 89.5:
        return _couche(spr)
    im = spr.rotate(angle, expand=True, resample=Image.NEAREST)
    al = np.array(im)[..., 3]
    lignes = np.where(al.max(axis=1) > 0)[0]
    im.info = dict(spr.info)
    im.info.update(foot=int(lignes.max()) + 1 if len(lignes) else im.height, ombre=34)
    return im


CHUTE = 0.7                                                         # durée d'une chute / d'un relevé (s)


def _angle_chute(a, u, allonge):
    """Si le perso vient de passer debout <-> étendu (pose « allonge ») il y a moins de CHUTE s : l'angle du moment."""
    if u < CHUTE:
        return None
    if (a.state(u - CHUTE).get("pose") == "allonge") == allonge:
        return None
    lo_, hi_ = u - CHUTE, u                                          # instant du changement de pose (dichotomie)
    for _ in range(12):
        mid_ = (lo_ + hi_) / 2
        if (a.state(mid_).get("pose") == "allonge") == allonge:
            hi_ = mid_
        else:
            lo_ = mid_
    k_ = smooth((u - hi_) / CHUTE)
    return 90.0 * (k_ if allonge else 1.0 - k_)


def _prosterne(spr, angle=75, plie=0.42, coupe=0.50):
    """Prosterné : à genoux (jambes repliées), le buste penché de `angle` degrés vers l'avant, le front vers le sol."""
    a = np.array(spr)
    lignes = np.where((a[..., 3] > 0).any(axis=1))[0]
    if len(lignes) == 0:
        return spr
    top, bot = int(lignes.min()), int(lignes.max())
    hip = top + int((bot - top + 1) * coupe)
    haut, bas = spr.crop((0, top, spr.width, hip)), spr.crop((0, hip, spr.width, bot + 1))
    bas = bas.resize((bas.width, max(1, int(bas.height * plie))), Image.NEAREST)
    w, h = haut.size
    grand = Image.new("RGBA", (w * 3, h * 3), (0, 0, 0, 0))
    grand.paste(haut, (w, h))
    piv = (w + w // 2, h + h)
    tour = grand.rotate(-angle, center=piv, resample=Image.NEAREST)
    can = Image.new("RGBA", (w * 3, h * 3 + bas.height), (0, 0, 0, 0))
    can.alpha_composite(tour, (0, 0))
    can.alpha_composite(bas, (w, piv[1] - 1))
    al = np.array(can)[..., 3] > 0
    r_, c_ = np.where(al.any(axis=1))[0], np.where(al.any(axis=0))[0]
    cx = w + w // 2                                                  # garder le perso centré sur ses genoux
    x0, x1 = int(c_.min()) - 1, int(c_.max()) + 2
    demi = max(cx - x0, x1 - cx)
    can = can.crop((cx - demi, int(r_.min()) - 1, cx + demi, int(r_.max()) + 2))
    can.info = dict(spr.info)
    can.info.update(foot=can.height - 1, ombre=30)
    return can


def load(path):
    r = subprocess.run([FF, "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).copy()


def silences(a, thr=-40.0, min_len=0.28):
    hop = int(0.01 * SR); n = len(a) // hop
    fr = a[:n * hop].reshape(n, hop)
    db = 20 * np.log10(np.maximum(1e-6, np.sqrt((fr ** 2).mean(axis=1))))
    q = db < thr
    out, i = [], 0
    while i < n:
        if q[i]:
            j = i
            while j < n and q[j]:
                j += 1
            if (j - i) * 0.01 >= min_len or i == 0 or j == n:
                out.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    return out


def split(a, n):
    """Coupe un fichier voix en n répliques sur les n-1 plus longs silences intérieurs."""
    sil = silences(a)
    dur = len(a) / SR
    first = sil[0][1] if sil and sil[0][0] <= 0.01 else 0.0
    last = sil[-1][0] if sil and sil[-1][1] >= dur - 0.02 else dur
    inner = [r for r in sil if r[0] > first + 0.05 and r[1] < last - 0.05]
    cuts = sorted(sorted(inner, key=lambda r: r[1] - r[0], reverse=True)[:n - 1])
    segs = []
    for k in range(n):
        s0 = (cuts[k - 1][1] - 0.06) if k else max(0.0, first - 0.06)
        s1 = (cuts[k][0] + 0.10) if k < n - 1 else min(dur, last + 0.12)
        segs.append((s0, s1))
    return segs


def split_texte(a, mots, textes):
    """Coupe un fichier voix en len(textes) répliques d'après le texte : on retrouve dans la transcription horodatée
    (mots) le premier mot de chaque réplique, puis on coupe dans le silence qui le précède. Robuste aux [pause]
    voulues à l'intérieur d'une réplique. Renvoie None si le texte ne se retrouve pas (on revient alors à split)."""
    import difflib, re as _re, unicodedata

    def norm(x):
        x = _re.sub(r"\[[^\]]*\]|\{[^}]*\}", " ", x).replace("ﷺ", " quelapaixetlesalutdallahsoientsurlui ")
        x = unicodedata.normalize("NFD", x.lower())
        return "".join(ch for ch in x if ch.isalnum() and not unicodedata.combining(ch))
    n = len(textes)
    if n <= 1 or not mots:
        return None
    a_chars, a_w = [], []
    for i, w in enumerate(mots):
        for ch in norm(w["t"]):
            a_chars.append(ch); a_w.append(i)
    b_chars, b_line = [], []
    for k, txt in enumerate(textes):
        for ch in norm(txt):
            b_chars.append(ch); b_line.append(k)
    if not a_chars or not b_chars:
        return None
    sm = difflib.SequenceMatcher(None, "".join(a_chars), "".join(b_chars), autojunk=False)
    first = [None] * n
    nb = [0] * n
    for blk in sm.get_matching_blocks():
        for j in range(blk.size):
            k = b_line[blk.b + j]; wi = a_w[blk.a + j]
            nb[k] += 1
            if first[k] is None or wi < first[k]:
                first[k] = wi
    tot = [b_line.count(k) for k in range(n)]
    if any(first[k] is None or nb[k] < 0.4 * tot[k] for k in range(n)):
        return None
    for k in range(1, n):                                    # ordre strict
        if first[k] <= first[k - 1]:
            first[k] = first[k - 1] + 1
        if first[k] >= len(mots):
            return None
    sil = silences(a)
    dur = len(a) / SR
    debut = sil[0][1] if sil and sil[0][0] <= 0.01 else 0.0
    fin = sil[-1][0] if sil and sil[-1][1] >= dur - 0.02 else dur
    coupes = []
    for k in range(1, n):
        e_prev = mots[first[k] - 1]["e"]
        s_cur = mots[first[k]]["s"]
        lo, hi = min(e_prev, s_cur) - 0.15, max(e_prev, s_cur) + 0.15
        cands = [r for r in sil if r[1] > lo and r[0] < hi and r[0] > debut + 0.05 and r[1] < fin - 0.05]
        if cands:
            c = max(cands, key=lambda r: r[1] - r[0])
            coupes.append((c[0] + 0.10, c[1] - 0.06))
        else:
            m = (e_prev + s_cur) / 2
            coupes.append((m, m))
    segs = []
    for k in range(n):
        s0 = coupes[k - 1][1] if k else max(0.0, debut - 0.06)
        s1 = coupes[k][0] if k < n - 1 else min(dur, fin + 0.12)
        if s1 - s0 < 0.1:
            return None
        segs.append((s0, s1))
    return segs


def _fermant(t):
    """Un « mot » qui n'est qu'un signe fermant (» " ) ’ …), éventuellement suivi de ponctuation."""
    t = t.strip()
    return bool(t) and t[0] in "»\")]’”" and not any(ch.isalnum() for ch in t)


def resserre(a, s0, s1, seuil=-30.0, souffle=0.6, ecart=0.2):
    """Retire d'une réplique les respirations (sons faibles et courts, séparés de la parole par un vrai silence)
    au début et à la fin : la réplique commence sur le premier mot et finit sur le dernier (pas de seconde morte)."""
    hop = int(0.01 * SR)
    seg = a[int(s0 * SR):int(s1 * SR)]
    n = len(seg) // hop
    if n < 10:
        return (s0, s1)
    fr = seg[:n * hop].reshape(n, hop)
    db = 20 * np.log10(np.maximum(1e-6, np.sqrt((fr ** 2).mean(axis=1))))
    db = np.convolve(np.pad(db, 2, mode="edge"), np.ones(5) / 5, mode="valid")   # moyenne sur 50 ms (sans effet de bord)
    son = db > -40.0
    runs, i = [], 0                                                  # passages sonores : (début, fin, parole ?)
    while i < n:
        if son[i]:
            j = i
            while j < n and son[j]:
                j += 1
            runs.append((i, j, bool((db[i:j] > seuil).any())))
            i = j
        else:
            i += 1
    if not runs:
        return (s0, s1)
    while (len(runs) > 1 and not runs[0][2] and (runs[0][1] - runs[0][0]) * 0.01 < souffle
           and (runs[1][0] - runs[0][1]) * 0.01 >= ecart):
        runs.pop(0)                                                  # respiration avant le premier mot
    while (len(runs) > 1 and not runs[-1][2] and (runs[-1][1] - runs[-1][0]) * 0.01 < souffle
           and (runs[-1][0] - runs[-2][1]) * 0.01 >= ecart):
        runs.pop()                                                   # respiration / bruit après le dernier mot
    n0 = s0 + max(0.0, runs[0][0] * 0.01 - 0.06)
    n1 = s0 + min(n * 0.01, runs[-1][1] * 0.01 + 0.12)
    return (max(s0, n0), min(s1, n1))


class Dialogue:
    """Enchaîne les répliques des deux voix ; donne les temps de chaque mot et l'enveloppe de chaque voix."""

    def __init__(s, vdir, sk, order, nlines, asr, gaps=None, lead=0.15, tempo=1.0, serre=False, textes=None):
        s.src = {w: load(vdir + f"{sk}_{w}.mp3") for w in nlines}
        s.segs = {}
        for w in nlines:                             # scénarios : découpe d'après le texte (sinon : plus longs silences)
            sg = split_texte(s.src[w], asr.get(w, []), textes[w]) if textes and w in textes else None
            s.segs[w] = sg or split(s.src[w], nlines[w])
        brut = s.segs
        s.serre = serre
        if serre:                                    # sans respirations ni silences en début / fin de réplique
            s.segs = {w: [resserre(s.src[w], a0, a1) for (a0, a1) in brut[w]] for w in brut}
        s.asr = asr
        s.lines = []
        t = lead
        idx = {w: 0 for w in nlines}
        for k, who in enumerate(order):
            i = idx[who]; idx[who] += 1
            a0, a1 = s.segs[who][i]
            d = (a1 - a0) / tempo
            if serre:                                # mots de la réplique d'origine, ramenés dans la partie gardée
                o0, o1 = brut[who][i]
                words = [dict(t=w["t"], s=t + (min(max(w["s"], a0), a1) - a0) / tempo,
                              e=t + (min(max(w["e"], a0), a1) - a0) / tempo)
                         for w in asr[who] if o0 - 0.05 <= w["s"] < o1 - 0.03]
            else:
                words = [dict(t=w["t"], s=t + (w["s"] - a0) / tempo, e=t + (w["e"] - a0) / tempo)
                         for w in asr[who] if a0 - 0.05 <= w["s"] < a1 - 0.03]
            s.lines.append(dict(who=who, a0=a0, a1=a1, t0=t, t1=t + d, words=words, k=k))
            gap = (gaps or {}).get(k, 0.07 if who == "P" else 0.11)
            t += d + gap
        s.dur = t + 0.6
        s.tempo = tempo
        s._build()

    def _build(s):
        n = int(s.dur * SR) + SR
        s.voice = np.zeros(n, np.float32)
        s.env = {w: np.zeros(int(s.dur * FPS) + FPS) for w in s.src}
        for L in s.lines:
            seg = s.src[L["who"]][int(L["a0"] * SR):int(L["a1"] * SR)]
            if s.tempo != 1.0:
                x = np.arange(0, len(seg) - 1, s.tempo)
                seg = np.interp(x, np.arange(len(seg)), seg).astype(np.float32)
            fade = min(len(seg), int(0.012 * SR))
            seg = seg.copy(); seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
            i0 = int(L["t0"] * SR)
            s.voice[i0:i0 + len(seg)] += seg
            hop = SR // FPS
            for f in range(len(seg) // hop):
                e = float(np.sqrt(np.mean(seg[f * hop:(f + 1) * hop] ** 2)))
                fi = int(L["t0"] * FPS) + f
                if fi < len(s.env[L["who"]]):
                    s.env[L["who"]][fi] = e
        for w in s.env:
            m = max(1e-6, np.percentile(s.env[w][s.env[w] > 0], 90) if np.any(s.env[w] > 0) else 1)
            s.env[w] = s.env[w] / m

    def talking(s, who, t):
        f = int(t * FPS)
        e = s.env.get(who)
        if e is None:                                # personnage sans voix dans ce dialogue
            return False
        if f >= len(e) or e[f] < 0.18:
            return False
        return (f // 3) % 3 != 2                     # la bouche s'ouvre / se ferme pendant la parole

    def line(s, k):
        return s.lines[k]

    # ---- bouche et sourcils (personnages du créateur) : forme de bouche d'après les lettres du mot prononcé
    VIS = dict(a="A", o="O", u="O", e="E", i="E", y="E", m="M", b="M", p="M", f="F", v="F")

    def _mot(s, who, t):
        for L in s.lines:
            if L["who"] == who and L["t0"] - 0.05 <= t <= L["t1"] + 0.05:
                for w in L["words"]:
                    if w["s"] <= t < w["e"]:
                        return w
        return None

    def bouche(s, who, t):
        import unicodedata
        w = s._mot(who, t)
        if w is None:
            return None
        txt = unicodedata.normalize("NFD", w["t"].lower())
        letters = [c for c in txt if c.isalpha() and not unicodedata.combining(c)]
        if not letters:
            return None
        p = (t - w["s"]) / max(0.05, w["e"] - w["s"])
        return s.VIS.get(letters[min(len(letters) - 1, int(p * len(letters)))], "parle")

    def accent(s, who, t):
        w = s._mot(who, t)
        if w is None:
            return None
        x = w["t"].strip()
        return "!" if x.endswith("!") or x.endswith("!?") else ("?" if x.endswith("?") else None)

    def at(s, k, needle, default=0.0):
        """Temps absolu du premier mot de la réplique k qui contient needle."""
        for w in s.lines[k]["words"]:
            if needle.lower() in w["t"].lower():
                return w["s"]
        return s.lines[k]["t0"] + default

    def align(s, texts):
        """Remplace les mots transcrits par les mots du script (affichage exact), calés sur les temps de la voix."""
        import difflib, unicodedata

        def norm(x):
            x = unicodedata.normalize("NFD", x.lower())
            return "".join(ch for ch in x if ch.isalnum() and not unicodedata.combining(ch))
        for L, txt in zip(s.lines, texts):
            ws = L["words"]
            if not ws:
                continue
            a_chars, a_time = [], []
            for w in ws:
                for ch in norm(w["t"]):
                    a_chars.append(ch); a_time.append((w["s"], w["e"]))
            toks = []
            for tok in txt.split():                          # ponctuation française collée au mot précédent
                if toks and tok in ("?", "!", ":", "?!", ";", "…", "!?"):
                    toks[-1] = toks[-1] + " " + tok
                else:
                    toks.append(tok)
            b_chars, b_owner = [], []
            for i, tok in enumerate(toks):
                for ch in ("quelapaixetlesalutdallahsoientsurlui" if tok == "ﷺ" else norm(tok)):
                    b_chars.append(ch); b_owner.append(i)
            sm = difflib.SequenceMatcher(None, "".join(a_chars), "".join(b_chars), autojunk=False)
            tmap = {}
            for blk in sm.get_matching_blocks():
                for j in range(blk.size):
                    tmap.setdefault(b_owner[blk.b + j], a_time[blk.a + j][0])
            L["retrouve"] = sum(blk.size for blk in sm.get_matching_blocks()) / max(1, len(b_chars))   # pour lot.py
            starts = []
            for i in range(len(toks)):
                starts.append(tmap.get(i))
            t0, t1 = L["t0"], L["t1"]
            for i in range(len(toks)):                       # mots non retrouvés : interpolation
                if starts[i] is None:
                    prv = next((starts[j] for j in range(i - 1, -1, -1) if starts[j] is not None), t0)
                    nxt = next((starts[j] for j in range(i + 1, len(toks)) if starts[j] is not None), t1 - 0.1)
                    starts[i] = prv + (nxt - prv) * 0.5 if i else t0 + 0.02
            for i in range(1, len(toks)):
                starts[i] = max(starts[i], starts[i - 1] + 0.05)
            ends = starts[1:] + [ws[-1]["e"]]
            L["words"] = [dict(t=tok, s=st, e=en) for tok, st, en in zip(toks, starts, ends)]

    def chunks(s, maxc=26):
        """Sous-titres : groupes de mots coupés à la ponctuation, puis en parts équilibrées (2 lignes max).
        (scénarios) un guillemet ou une parenthèse fermante après la fin d'une phrase reste avec elle (jamais « » » seul)
        et la ferme : le sous-titre suivant ne commence pas par « » » (03/11/2026, « … limites. » Et Allah… »)."""
        colle = getattr(s, "serre", False)
        out = []
        for L in s.lines:
            ws = L["words"]
            phrase = []
            for i, w in enumerate(ws):
                phrase.append(w)
                end = w["t"][-1:] in ",.!?…:" or w["t"] == "ﷺ" or (i + 1 < len(ws) and ws[i + 1]["t"] == "ﷺ") or i == len(ws) - 1
                if colle and not end and _fermant(w["t"]):
                    avant = next((x["t"] for x in reversed(phrase[:-1]) if not _fermant(x["t"])), "")
                    end = avant[-1:] in ".!?…"
                if end and colle and i + 1 < len(ws) and _fermant(ws[i + 1]["t"]):
                    end = False
                if not end:
                    continue
                txt = " ".join(x["t"] for x in phrase).replace("ﷺ", "(paix et salut sur lui)")
                n = max(1, math.ceil(len(txt) / maxc)) if phrase[0]["t"] != "ﷺ" else 1
                tot = len(txt); target = tot / n
                cur, acc, parts = [], 0, []
                for w2 in phrase:
                    cur.append(w2); acc += len(w2["t"]) + 1
                    if len(parts) < n - 1 and acc >= target * (len(parts) + 1) - 2:
                        parts.append(cur); cur = []
                if cur:
                    parts.append(cur)
                if colle and len(parts) > 1 and all(_fermant(x["t"]) for x in parts[-1]):
                    parts[-2].extend(parts.pop())
                for part in parts:
                    out.append(dict(who=L["who"], t0=part[0]["s"], words=part, k=L["k"]))
                phrase = []
        for i, c in enumerate(out):
            nxt = out[i + 1]["t0"] if i + 1 < len(out) else c["words"][-1]["e"] + 0.5
            if i + 1 < len(out) and out[i + 1]["k"] != c["k"]:
                nxt = min(nxt, c["words"][-1]["e"] + 0.45)
            c["t1"] = nxt
            c["txt"] = " ".join(x["t"] for x in c["words"]).replace("ﷺ", "(paix et salut sur lui)")
        return out


# =================================================================== rendu des textes pixel
def pixel_text(txt, col=(255, 255, 255), ol=(20, 20, 30), size=10, font=TAHOMA, k=5, ol2=None):
    """Texte pixel net : rendu sans lissage à petite taille, contour d'un pixel, agrandi xk."""
    f = ImageFont.truetype(font, size)
    d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
    bb = d0.textbbox((0, 0), txt, font=f)
    w, h = bb[2] - bb[0] + 6, bb[3] - bb[1] + 6
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m); d.fontmode = "1"
    d.text((3 - bb[0], 3 - bb[1]), txt, font=f, fill=255)
    a = np.array(m) > 0
    e = a.copy()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        e |= np.roll(np.roll(a, dy, 0), dx, 1)
    out = np.zeros((h, w, 4), np.uint8)
    if ol2 is not None:
        e2 = e.copy()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            e2 |= np.roll(np.roll(e, dy, 0), dx, 1)
        out[e2] = (*ol2, 255)
    out[e] = (*ol, 255)
    out[a] = (*col, 255)
    im = Image.fromarray(out, "RGBA")
    return im.resize((w * k, h * k), Image.NEAREST)


def big_title(lines, size=104):
    """Titre d'accroche (lettres pleines, ombre portée), lignes [(texte, couleur)]."""
    f = ImageFont.truetype(SEGOE_BLACK, size)
    ims = []
    for txt, col in lines:
        d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
        bb = d0.textbbox((0, 0), txt, font=f, stroke_width=8)
        w, h = bb[2] - bb[0] + 30, bb[3] - bb[1] + 30
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.text((15 - bb[0] + 8, 15 - bb[1] + 10), txt, font=f, fill=(8, 20, 24, 200), stroke_width=8, stroke_fill=(8, 20, 24, 200))
        d.text((15 - bb[0], 15 - bb[1]), txt, font=f, fill=col, stroke_width=8, stroke_fill=(16, 28, 34))
        ims.append(im)
    W_ = max(i.width for i in ims); H_ = sum(i.height for i in ims) - 20 * (len(ims) - 1)
    out = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); y = 0
    for im in ims:
        out.alpha_composite(im, ((W_ - im.width) // 2, y)); y += im.height - 20
    return out


def portrait_img(who, face="neutre", talk=False, k=5):
    a = duo.portrait(who, face, talk)
    h, w = a.shape[:2]
    fr = np.zeros((h + 4, w + 4, 4), np.uint8)
    sp = speaker(who)
    fr[:, :] = (*sp["frame"], 255)
    fr[1:-1, 1:-1] = (*duo.INK[:3], 255)
    if who in ("P", "G"):
        fr[2:-2, 2:-2] = (44, 36, 58, 255) if who == "G" else (58, 34, 44, 255)
    else:
        fr[2:-2, 2:-2] = (*sp.get("bg", (50, 44, 56)), 255)
    inner = fr[2:-2, 2:-2]
    msk = a[..., 3] > 0
    inner[msk] = a[msk]
    return Image.fromarray(fr, "RGBA").resize(((w + 4) * k, (h + 4) * k), Image.NEAREST)


def wrap(txt, maxc=17):
    words, lines, cur = [w for w in txt.split(" ") if w], [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxc:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


_SUBC = {}


def _ligne_mots_cles(line, ol, blanc=(255, 255, 255)):
    """Une ligne de sous-titre où les mots entre *étoiles* sont en jaune (mot important)."""
    mots = line.split(" ")
    if not any("*" in m for m in mots):
        return pixel_text(line, blanc, ol, size=10, k=5, ol2=(14, 10, 18))
    ims, hauts, fort = [], [], False
    f10 = ImageFont.truetype(TAHOMA, 10)
    d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
    for m in mots:
        debut = m.lstrip("«\u00a0").startswith("*")
        fin = m.rstrip("?!.,:;\u00a0…»").endswith("*")
        f = fort or debut
        propre = m.replace("*", "")
        if propre:
            ims.append(pixel_text(propre, (255, 214, 70) if f else blanc, ol, size=10, k=5, ol2=(14, 10, 18)))
            hauts.append(d0.textbbox((0, 0), propre, font=f10)[1])     # haut du mot : même ligne de base pour tous
        fort = (fort or debut) and not fin
    esp = 4 * 5
    h0 = min(hauts)
    dy = [(h - h0) * 5 for h in hauts]
    out = Image.new("RGBA", (sum(i.width for i in ims) + esp * (len(ims) - 1) - 6 * 5 * (len(ims) - 1),
                             max(i.height + d for i, d in zip(ims, dy))), (0, 0, 0, 0))
    x = 0
    for i, d in zip(ims, dy):
        out.alpha_composite(i, (x, d))
        x += i.width + esp - 6 * 5
    return out


def subtitle_img(txt, who, side=None, vignette=True, largeur=16, colle=False):
    """Sous-titre : texte (mots clés en jaune) + vignette du perso qui parle. Films : vignette=False, lignes plus
    larges (largeur = lettres par ligne), couleur du texte propre à la voix (la voix du Coran en or pâle)."""
    key = (txt, who, side, vignette, largeur, colle)
    if key in _SUBC:
        return _SUBC[key]
    if side is None:
        side = "left" if who == "G" else "right"
    blanc = speaker(who).get("texte", (255, 255, 255))
    lie = txt.replace(" ?", "\u00a0?").replace(" !", "\u00a0!").replace(" :", "\u00a0:")
    if colle:                                          # vidéos à thème (03/11/2026) : « et » restent collés à
        lie = lie.replace(" »", "\u00a0»").replace("« ", "«\u00a0")   # leurs mots (jamais « » » seul)
    if "*" in txt:                                     # mots clés en jaune (le compte des lettres ignore les étoiles)
        lignes, cur = [], ""
        for w in [w for w in lie.split(" ") if w]:
            if cur and len(cur.replace("*", "")) + 1 + len(w.replace("*", "")) > largeur:
                lignes.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        if cur:
            lignes.append(cur)
        ouvert, lines2 = False, []
        for l in lignes:                              # un *groupe de mots* coupé en deux lignes reste jaune
            ws = l.split(" ")
            if ouvert and ws:
                ws[0] = "*" + ws[0]
            for w in ws:
                if w.lstrip("«\u00a0").startswith("*"):
                    ouvert = True
                if w.rstrip("?!.,:;\u00a0…»").endswith("*"):
                    ouvert = False
            if ouvert and ws:
                ws[-1] = ws[-1] + "*"
            lines2.append(" ".join(ws))
        ims = [_ligne_mots_cles(l, speaker(who)["ol"], blanc) for l in lines2]
    else:
        lines = wrap(lie, largeur)
        ims = [pixel_text(l, blanc, speaker(who)["ol"], size=10, k=5, ol2=(14, 10, 18)) for l in lines]
    tw = max(i.width for i in ims); th = sum(i.height for i in ims) - 14 * (len(ims) - 1)
    tx = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); y = 0
    for im in ims:
        tx.alpha_composite(im, ((tw - im.width) // 2, y)); y += im.height - 14
    if not vignette or who in ("NARRATEUR", "CORAN"):  # films, ou voix sans corps dans un Short : le texte seul
        _SUBC[key] = tx
        return tx
    pt = portrait_img(who)
    gap = 18
    wtot = tx.width + gap + pt.width
    htot = max(tx.height, pt.height)
    out = Image.new("RGBA", (wtot, htot), (0, 0, 0, 0))
    if side == "left":                                 # celui qui explique : vignette à gauche
        out.alpha_composite(pt, (0, (htot - pt.height) // 2)); out.alpha_composite(tx, (pt.width + gap, (htot - tx.height) // 2))
    else:                                              # celui qui demande : vignette à droite
        out.alpha_composite(tx, (0, (htot - tx.height) // 2)); out.alpha_composite(pt, (tx.width + gap, (htot - pt.height) // 2))
    _SUBC[key] = out
    return out


def tag_img(txt, bg=(30, 22, 30), fg=(250, 240, 220), k=4, size=8):
    t = pixel_text(txt, fg, bg, size=size, k=k)
    pad = 2 * k
    im = Image.new("RGBA", (t.width + 2 * pad, t.height + pad), (*bg, 235))
    im.alpha_composite(t, (pad, pad // 2))
    return im


def series_band(k=4):
    a = pixel_text("VALABLE OU PAS ?", (255, 255, 255), (20, 60, 70), size=9, k=k)
    pad = 3 * k
    im = Image.new("RGBA", (a.width + 2 * pad, a.height + pad), (24, 96, 104, 240))
    d = ImageDraw.Draw(im); d.rectangle([0, 0, k * 2, im.height], fill=(250, 196, 70, 255))
    im.alpha_composite(a, (pad + k, pad // 2))
    return im


_ORB_LAB = {}                                         # noms des orbes (film.py), déjà écrits


# =================================================================== plans
class Actor:
    def __init__(s, who, x, y, k=7, mirror=False, state=None, path=None, talk_with=None, breathe=0.0, bob=0.0):
        """state(t) -> dict(pose=, face=, ...) ; path(t) -> (x, y) ; talk_with = voix qui anime la bouche.
        breathe = respiration (px, mouvement lent) ; bob = petits sauts doux (rire)."""
        s.who, s.x, s.y, s.k, s.mirror = who, x, y, k, mirror
        s.breathe, s.bob = breathe, bob
        s.state = state or (lambda t: {})
        s.path = path
        s.talk_with = talk_with if talk_with is not None else (who if (who in ("P", "G") or (who not in ("S", "IMAM") and duo.is_char(who))) else None)


def blink(t, seed=0.0):
    p = (t + seed) % 3.4
    return p < 0.11


class Shot:
    def __init__(s, t0, t1, bg, actors=(), cam=(1.0, 1.0, (540, 960), (540, 960)), blur=0, fg=True,
                 world=None, overlays=None, bubbles=None, board=None, src=None, tags=None, band=True,
                 anims=None, anims_avant=None, effets=None, fond2=None, sons=None, ambiance=None, ecran=None):
        s.t0, s.t1, s.bg, s.actors = t0, t1, bg, list(actors)
        s.cam, s.blur, s.fg = cam, blur, fg   # cam = (z0, z1, c0, c1) ou liste de clés [(u, zoom, (cx, cy)), …]
        s.world = world or []           # images posées dans le décor (photo, titre…) : (img, x, y, t_in)
        s.overlays = overlays or []     # fonctions(img, t) dessinées dans le monde après les persos
        s.bubbles = bubbles or []       # (actor_index, sprite_fn, t_in, t_out, dx, dy)
        s.board = board                 # fonction(Px) qui écrit sur le tableau
        s.src = src
        s.tags = tags or []
        s.band = band
        s.anims = anims or []           # fonctions(img, u) : décor animé DERRIÈRE les persos (passants, vapeur, feu…)
        s.anims_avant = anims_avant or []   # fonctions(img, u) : DEVANT les persos (pluie, neige, voitures, objet lancé…)
        s.effets = effets or []         # (actor_index, fonction(img, u, tête, durée), t_in, t_out) : cœurs, zzz, colère…
        s.fond2 = fond2                 # (décor, u_début, durée) : le décor se change en un autre (lumière qui s'éteint…)
        s.sons = sons or []             # (u, bruitage, gain[, durée max]) : bruitages calés dans le plan
        s.ambiance = ambiance           # (bruitage, gain) : ambiance en boucle pendant le plan
        s.ecran = ecran or []           # fonctions(img, u) dessinées APRÈS la caméra (légendes, notifications, téléphone)
        s.lumieres = []                 # sources de lumière en plus de celles du décor : (x, y, rayon, couleur, force)
        s._bgc = None
        s._bg2 = None
        s._far = None
        s._fgbb = None                  # zone dessinée de l'avant-plan du décor (calculée une fois)

    def background(s, fmt="portrait"):
        if s._bgc is None:
            if fmt == "paysage" and lieux is not None:
                bg, fg = lieux.decor_large(s.bg)                  # 16:9 : décor redessiné plus large (sans doublon)
            else:
                bg, fg = sets.DECORS[s.bg]()
            if s.board:
                s.board(bg)
            im = bg.img(4).convert("RGB")
            if s.blur:
                im = im.filter(ImageFilter.GaussianBlur(s.blur))
            s._bgc = (im, fg.img(4, rgba=True) if (fg is not None and s.fg) else None)
            s._bga = im.convert("RGBA")
            s._far, s._holes = None, None
            lo, cm = getattr(bg, "lointain", None), getattr(bg, "ciel_m", None)
            if lo is not None and cm is not None and cm.any():          # relief : le ciel lointain sur sa propre couche
                if RELIEF_PROLONGE:                                     # films : le ciel lointain est prolongé vers le bas
                    lo = np.array(lo, copy=True)                        # (sinon une ligne noire apparaît sous l'horizon
                    y_bas = int(np.nonzero(cm.any(axis=1))[0].max())    # quand la caméra glisse ou se rapproche)
                    lo[y_bas + 1:] = lo[y_bas]
                far = Image.fromarray(lo).resize((bg.w * 4, bg.h * 4), Image.NEAREST).convert("RGB")
                if s.blur:
                    far = far.filter(ImageFilter.GaussianBlur(s.blur))
                s._far = far.convert("RGBA")
                holes = np.array(s._bga)
                holes[np.repeat(np.repeat(cm, 4, 0), 4, 1), 3] = 0
                s._holes = Image.fromarray(holes, "RGBA")
        return s._bgc

    def background2(s, fmt="portrait"):
        if s._bg2 is None:
            if fmt == "paysage" and lieux is not None:
                bg, fg = lieux.decor_large(s.fond2[0])
            else:
                bg, fg = sets.DECORS[s.fond2[0]]()
            im = bg.img(4).convert("RGB")
            if s.blur:
                im = im.filter(ImageFilter.GaussianBlur(s.blur))
            s._bg2 = (im, fg.img(4, rgba=True) if (fg is not None and s.fg) else None)
        return s._bg2


def cam_keys(keys, u):
    """Caméra à clés : [(u, zoom, (cx, cy)), …] ; mouvement doux (smootherstep) d'une clé à l'autre."""
    keys = sorted(keys, key=lambda k: k[0])
    if u <= keys[0][0]:
        k = keys[0]
        return k[1], k[2][0], k[2][1]
    for a, b in zip(keys, keys[1:]):
        if a[0] <= u < b[0]:
            e = smooth((u - a[0]) / max(1e-6, b[0] - a[0]))
            return a[1] + (b[1] - a[1]) * e, a[2][0] + (b[2][0] - a[2][0]) * e, a[2][1] + (b[2][1] - a[2][1]) * e
    k = keys[-1]
    return k[1], k[2][0], k[2][1]


RELIEF_PROLONGE = False                          # films (scenario.py) : ciel lointain prolongé sous l'horizon
BRUITAGES = BASE + "/_BRUITAGES"
_SONS = {}


def bruitage(nom, prise=None):
    """Son de la bibliothèque _BRUITAGES par son nom (dv_porte_bois, amb_pluie…) ; prise _1/_2 au hasard."""
    if os.path.isabs(nom) and os.path.exists(nom):
        path = nom
    else:
        found = {}
        for root, _, files in os.walk(BRUITAGES):
            for f in files:
                found.setdefault(f, os.path.join(root, f))
        cands = [found[f] for f in (nom + ".mp3", nom + "_1.mp3", nom + "_2.mp3") if f in found]
        if not cands:                                    # sons livrés en .zip pas encore décompressés : on lit dans le zip
            import zipfile, tempfile
            cache = os.path.join(tempfile.gettempdir(), "ia501", "bruitages_zip")
            for zf in [os.path.join(BRUITAGES, f) for f in os.listdir(BRUITAGES) if f.lower().endswith(".zip")]:
                with zipfile.ZipFile(zf) as z:
                    names = {os.path.basename(n): n for n in z.namelist()}
                    for f in (nom + ".mp3", nom + "_1.mp3", nom + "_2.mp3"):
                        if f in names:
                            dst = os.path.join(cache, f)
                            if not os.path.exists(dst):
                                os.makedirs(cache, exist_ok=True)
                                with open(dst, "wb") as out:
                                    out.write(z.read(names[f]))
                            cands.append(dst)
        if not cands:
            raise FileNotFoundError(f"bruitage introuvable : {nom}")
        path = cands[(prise or 0) % len(cands)] if prise is not None else cands[sum(map(ord, nom)) % len(cands)]
    if path not in _SONS:
        _SONS[path] = load(path)
    return _SONS[path]


class Video:
    def __init__(s, dlg, shots, music=None, music_gain=0.10, theme=None, sons=None):
        s.dlg, s.shots = dlg, shots
        s.sons = sons or []                # bruitages globaux : (t, nom, gain[, durée max])
        s.globaux = []                     # dessins d'écran sur toute la vidéo f(img, t) : accroche, étapes…
        s.music, s.music_gain = music, music_gain
        s.theme = theme or Theme()
        s.v2 = theme is not None           # sans thème = rendu d'origine (Shorts VOP déjà livrés, identiques au pixel)
        s.fmt = getattr(s.theme, "format", "portrait") if s.v2 else "portrait"
        s.W, s.H = (1920, 1080) if s.fmt == "paysage" else (W, H)
        s.subs = dlg.chunks(maxc=getattr(s.theme, "st_maxc", 26))
        yy, xx = np.mgrid[0:s.H, 0:s.W]
        r = np.sqrt(((xx - s.W / 2) / (s.W * 0.62)) ** 2 + ((yy - s.H / 2) / (s.H * 0.62)) ** 2)
        s.vig = np.clip(1 - s.theme.vignette * np.clip(r - 0.55, 0, 1) ** 1.6 * 2.2, 0.55, 1.0)[..., None].astype(np.float32)
        s.scan = np.where((yy % 4) == 0, 0.975 if s.theme.lignes else 1.0, 1.0)[..., None].astype(np.float32)
        s.band = series_band() if theme is None else s.theme.band_img()
        s.warm = np.array(s.theme.chaleur, np.float32)
        s.rng = np.random.default_rng(7)
        s._rcache, s._ocache = {}, {}
        if s.v2:                           # filtre film rapide : un seul multiplicateur entier + grain précalculé
            s.mult16 = np.round(s.vig * s.scan * s.warm[None, None, :] * 128).astype(np.uint16)
            g = np.random.default_rng(7)
            s.grains = [np.repeat(np.repeat(np.clip(np.round(g.normal(0, s.theme.grain, (s.H // 2, s.W // 2))), -127, 127)
                                            .astype(np.int8), 2, 0), 2, 1)[..., None] for _ in range(24)]
            s.grains16 = [(gr.astype(np.int16) + 128).astype(np.uint16) for gr in s.grains]
            s._tampon = np.empty((s.H, s.W, 3), np.uint16)
        s.brouillon = False                # True : aperçu rapide (render_brouillon), sans filtre film

    # ---- un plan à l'instant t (temps absolu)
    def render_shot(s, sh, t):
        if s.v2:
            return s.render_shot_v2(sh, t)
        u = t - sh.t0
        D = max(0.01, sh.t1 - sh.t0)
        bg, fg = sh.background()
        img = bg.copy().convert("RGBA")
        if sh.fond2 is not None and u > sh.fond2[1]:                 # le décor se change en un autre (fondu lent)
            k2 = smooth((u - sh.fond2[1]) / max(0.01, sh.fond2[2]))
            bg2, fg2 = sh.background2()
            img = Image.blend(img, bg2.convert("RGBA"), k2)
            if fg is not None and fg2 is not None:
                fg = Image.blend(fg, fg2, k2)
        for (wim, x, y, tin) in sh.world:
            if t >= sh.t0 + tin:
                img.alpha_composite(wim, (int(x - wim.width / 2), int(y)))
        for an in sh.anims:
            an(img, u)
        heads = []
        for a in sh.actors:
            st = dict(a.state(u))
            mir = st.pop("_mirror", a.mirror)
            alpha = st.pop("_alpha", 1.0)
            if alpha <= 0.01:
                heads.append((a.x, -9999, a.k, mir))
                continue
            who = a.who
            if who in ("P", "G", "S"):
                if a.talk_with and s.dlg.talking(a.talk_with, t) and not st.get("mute"):
                    st["talk"] = True
                if st.get("face", "neutre") in ("neutre", "content", "gene", "malin", "blase") and not st.get("noblink") \
                        and blink(t, 0.0 if who == "P" else 1.3) and not st.get("back"):
                    st["face"] = "ferme"
                st.pop("mute", None); st.pop("noblink", None)
            elif duo.is_char(who):                     # personnages du créateur : la bouche suit la voix, ils clignent
                if a.talk_with and s.dlg.talking(a.talk_with, t) and not st.get("mute"):
                    st["talk"] = True
                if not st.get("noblink") and not st.get("back") and blink(t, (sum(map(ord, who)) % 17) / 5.0):
                    st["cligne"] = True
                st.pop("mute", None); st.pop("noblink", None)
            spr = duo.sprite(who, **st) if duo.is_char(who) else duo.sprite(who)
            x, y = a.path(u) if a.path else (a.x, a.y)
            if a.breathe:
                y += a.breathe * math.sin(2 * math.pi * u / 2.8)
            if a.bob:
                y -= a.bob * abs(math.sin(2 * math.pi * u * 1.5))
            im = spr.resize((spr.width * a.k, spr.height * a.k), Image.NEAREST)
            if mir:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            if alpha < 1:
                im = im.copy(); im.putalpha(Image.fromarray((np.array(im)[..., 3] * alpha).astype(np.uint8)))
            foot = spr.info.get("foot", duo.FOOT)
            px0 = int(x - im.width / 2); py0 = int(y - foot * a.k)
            img.alpha_composite(im, (px0, py0)) if 0 <= px0 + im.width and px0 < W * 2 else None
            heads.append((x, py0 + duo.head_top(who, st) * a.k, a.k, mir))
        if fg is not None:
            img.alpha_composite(fg)
        for an in sh.anims_avant:
            an(img, u)
        for (ai, fn, tin, tout, dx, dy) in sh.bubbles:
            if tin <= u < tout:
                hx, hy, k, mir = heads[ai]
                b = fn().img(k)
                al = smooth((u - tin) / 0.12) * (1 - smooth((u - (tout - 0.12)) / 0.12))
                if al < 1:
                    b = b.copy(); b.putalpha(Image.fromarray((np.array(b)[..., 3] * al).astype(np.uint8)))
                img.alpha_composite(b, (int(hx + dx * k - b.width / 2), int(hy + dy * k - b.height)))
        for (ai, fn, tin, tout) in sh.effets:
            if tin <= u < tout and ai < len(heads) and heads[ai][1] > -9000:
                fn(img, u - tin, heads[ai], tout - tin)
        for ov in sh.overlays:
            ov(img, u)
        # caméra : zoom et glissé doux (deux positions, ou une liste de clés)
        if isinstance(sh.cam, list):
            z, cx, cy = cam_keys(sh.cam, u)
        else:
            z0, z1, c0, c1 = sh.cam
            e = smooth(u / D)
            z = z0 + (z1 - z0) * e
            cx = c0[0] + (c1[0] - c0[0]) * e; cy = c0[1] + (c1[1] - c0[1]) * e
        w, h = W / z, H / z
        x0 = min(max(0, cx - w / 2), W - w); y0 = min(max(0, cy - h / 2), H - h)
        if abs(z - 1) > 1e-3 or x0 or y0:
            img = img.crop((x0, y0, x0 + w, y0 + h)).resize((W, H), Image.BILINEAR)
        for ov in sh.ecran:
            ov(img, u)
        return img

    # ---- rendu « v2 » (toutes les nouvelles vidéos) : ombres, lumière, relief, format horizontal, animaux, bouche
    def _sprite_k(s, spr, k, mir):
        key = (id(spr), k, mir)
        im = s._rcache.get(key)
        if im is None:
            if len(s._rcache) > 900:
                s._rcache.clear()
            im = spr.resize((spr.width * k, spr.height * k), Image.NEAREST)
            if mir:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            s._rcache[key] = (im, spr)
            return im
        return im[0]

    def _ombre(s, k, w):
        key = (k, w)
        if key not in s._ocache:
            ww, hh = max(6, int(w)), 4
            a = np.zeros((hh, ww, 4), np.uint8)
            yy, xx = np.mgrid[0:hh, 0:ww]
            m = ((xx + 0.5 - ww / 2) / (ww / 2)) ** 2 + ((yy + 0.5 - hh / 2) / (hh / 2)) ** 2 <= 1.0
            a[m] = (12, 6, 22, 122)
            s._ocache[key] = Image.fromarray(a, "RGBA").resize((ww * k, hh * k), Image.NEAREST)
        return s._ocache[key]

    def _eclaire(s, im, x, y, k, lum):
        """Lumière de la scène sur le perso : ambiance (nuit bleutée, soir orangé) + liseré côté source (feu, lampe)."""
        amb, sources = lum
        arr = np.array(im)
        alpha = arr[..., 3] > 0
        if not alpha.any():
            return im
        rgb = arr[..., :3].astype(np.float32)
        if amb is not None and any(abs(v - 1) > 0.01 for v in amb):
            rgb *= np.array(amb, np.float32)
        for (lx, ly, rad, col, force) in sources:
            cy = y - im.height * 0.45
            d = math.hypot(lx - x, ly - cy)
            if d > rad:
                continue
            w = force * (1 - d / rad) ** 1.3
            rgb += np.array(col, np.float32) * (0.22 * w)                         # lumière d'ambiance de la source
            side = 1 if lx > x else -1                                           # liseré du côté de la source
            sh_ = max(1, k)
            shifted = np.zeros_like(alpha)
            if side > 0:
                shifted[:, :-sh_] = alpha[:, sh_:]
            else:
                shifted[:, sh_:] = alpha[:, :-sh_]
            rim = alpha & ~shifted
            if ly < cy - im.height * 0.2:                                       # source en hauteur : liseré sur le dessus aussi
                top = np.zeros_like(alpha); top[sh_:, :] = alpha[:-sh_, :]
                rim |= alpha & ~top
            rgb[rim] = rgb[rim] * (1 - 0.55 * w) + np.array(col, np.float32) * (0.55 * w)
        arr[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
        return Image.fromarray(arr, "RGBA")

    def lumiere_shot(s, sh, u):
        """Ambiance + sources lumineuses du plan (décor, feu, lampe) ; suit le changement de décor (fond2)."""
        if not s.theme.lumiere or lieux is None:
            return None
        amb, src = lieux.lumiere_de(sh.bg, s.W, s.H, s.fmt)
        if sh.fond2 is not None and u > sh.fond2[1]:
            k2 = smooth((u - sh.fond2[1]) / max(0.01, sh.fond2[2]))
            amb2, src2 = lieux.lumiere_de(sh.fond2[0], s.W, s.H, s.fmt)
            amb = tuple(amb[i] * (1 - k2) + amb2[i] * k2 for i in range(3))
            src = [(a, b, c, d, e * (1 - k2)) for (a, b, c, d, e) in src] + [(a, b, c, d, e * k2) for (a, b, c, d, e) in src2]
        dx = 420 if s.fmt == "paysage" else 0                 # sources ajoutées par la scène : coordonnées du format vertical
        src = list(src) + [(x + dx, y, r, c, f) for (x, y, r, c, f) in (getattr(sh, "lumieres", []) or [])]
        return amb, src

    def render_shot_v2(s, sh, t):
        W_, H_ = s.W, s.H
        u = t - sh.t0
        D = max(0.01, sh.t1 - sh.t0)
        bg, fg = sh.background(s.fmt)
        bg_fg = fg                                       # (pour reconnaître l'avant-plan d'origine, non fondu)
        ox = (sh._bga.width - W) // 2                    # 16:9 : la scène est élargie de 420 px de chaque côté
        relief = s.theme.parallaxe and sh._far is not None and getattr(sh, "relief", True)
        img = (sh._holes if relief else sh._bga).copy()
        if sh.fond2 is not None and u > sh.fond2[1]:
            k2 = smooth((u - sh.fond2[1]) / max(0.01, sh.fond2[2]))
            bg2, fg2 = sh.background2(s.fmt)
            img = Image.blend(sh._bga.copy() if relief else img, bg2.convert("RGBA"), k2)
            relief = False
            if fg is not None and fg2 is not None:
                fg = Image.blend(fg, fg2, k2)
        for (wim, x, y, tin) in sh.world:
            if t >= sh.t0 + tin:
                img.alpha_composite(wim, (int(x + ox - wim.width / 2), int(y)))
        for an in sh.anims:
            an(img, u)
        lum = s.lumiere_shot(sh, u)
        heads, draws = [], []
        for a in sh.actors:
            st = dict(a.state(u))
            mir = st.pop("_mirror", a.mirror)
            alpha = st.pop("_alpha", 1.0)
            if alpha <= 0.01:
                heads.append((a.x, -9999, a.k, mir))
                continue
            who = a.who
            if who in ("P", "G", "S"):
                if a.talk_with and s.dlg.talking(a.talk_with, t) and not st.get("mute"):
                    st["talk"] = True
                if st.get("face", "neutre") in ("neutre", "content", "gene", "malin", "blase") and not st.get("noblink") \
                        and blink(t, 0.0 if who == "P" else 1.3) and not st.get("back"):
                    st["face"] = "ferme"
                st.pop("mute", None); st.pop("noblink", None)
            elif duo.is_char(who):
                if a.talk_with and s.dlg.talking(a.talk_with, t) and not st.get("mute"):
                    st["talk"] = True
                    if hasattr(s.dlg, "bouche"):
                        st["bouche"] = s.dlg.bouche(a.talk_with, t)
                        st["accent"] = s.dlg.accent(a.talk_with, t)
                    st["hoche"] = int(t * 2.4) % 2                     # petit hochement de tête en parlant
                elif st.get("talk"):
                    st["hoche"] = int(t * 2.4) % 2
                if not st.get("noblink") and not st.get("back") and blink(t, (sum(map(ord, who)) % 17) / 5.0):
                    st["cligne"] = True
                st.pop("mute", None); st.pop("noblink", None)
            allonge = st.get("pose") == "allonge"
            prosterne = st.get("pose") == "prosterne"
            chute = None if prosterne else _angle_chute(a, u, allonge)  # il tombe / se relève en ce moment
            if chute is not None:
                allonge = False
            if allonge or prosterne or chute is not None:                # étendu au sol / prosterné, yeux fermés (film)
                st = dict(st, pose="neutre", face="dodo")
                for k_ in ("talk", "hoche", "bouche", "accent", "cligne"):
                    st.pop(k_, None)
            spr = duo.sprite(who, **st) if duo.anime(who) else duo.sprite(who)
            if allonge:
                spr = _couche(spr)
            elif chute is not None:
                spr = _incline(spr, chute)
            elif prosterne:
                spr = _prosterne(spr)
            if spr.info.get("lumineux"):                                 # orbe : jamais en miroir (son nom resterait à l'envers)
                mir = False
            x, y = a.path(u) if a.path else (a.x, a.y)
            x += ox
            ysol = a.sol(u) if getattr(a, "sol", None) else y
            if a.breathe:
                y += a.breathe * math.sin(2 * math.pi * u / 2.8)
            if a.bob:
                y -= a.bob * abs(math.sin(2 * math.pi * u * 1.5))
            if spr.info.get("flotte"):                                   # orbe (film.py) : flotte doucement
                y -= spr.info.get("flotte_amp", 2.2) * a.k * (0.5 + 0.5 * math.sin(2 * math.pi * u / 2.8 + (sum(map(ord, who)) % 7)))
            im = s._sprite_k(spr, a.k, mir)
            if lum is not None and not spr.info.get("lumineux"):         # une orbe garde sa propre lumière
                im = s._eclaire(im, x, y, a.k, lum)
            if alpha < 1:
                im = im.copy(); im.putalpha(Image.fromarray((np.array(im)[..., 3] * alpha).astype(np.uint8)))
            foot = spr.info.get("foot", duo.FOOT)
            px0 = int(x - im.width / 2); py0 = int(y - foot * a.k)
            draws.append((im, px0, py0, x, ysol, a, st, mir, alpha, spr))
            heads.append((x, py0 + duo.head_top(who, st) * a.k, a.k, mir))
        if s.theme.ombres:                                              # ombres au sol, sous tous les persos
            for (im, px0, py0, x, ysol, a, st, mir, alpha, spr) in draws:
                if (st.get("back") and a.k > 11) or spr.info.get("lumineux") or spr.info.get("ombre", 1) == 0:
                    continue
                w = spr.info.get("ombre", 24 if not st.get("assis") else 30)
                dx = 0 if not st.get("assis") else (6 if not mir else -6) * a.k
                o = s._ombre(a.k, w)
                if alpha < 1:
                    o = o.copy(); o.putalpha(Image.fromarray((np.array(o)[..., 3] * alpha).astype(np.uint8)))
                img.alpha_composite(o, (int(x + dx - o.width / 2), int(ysol - o.height * 0.6)))
        for (im, px0, py0, x, ysol, a, st, mir, alpha, spr) in draws:
            if px0 + im.width >= 0 and px0 < W_ * 2:
                img.alpha_composite(im, (px0, py0))
                if spr.info.get("label"):                                # orbe : son nom, petit et net, sous la boule
                    lab = _ORB_LAB.get(spr.info["label"])
                    if lab is None:
                        lab = _ORB_LAB[spr.info["label"]] = pixel_text(spr.info["label"], (255, 255, 255), (24, 18, 30),
                                                                         size=8, k=3)
                    if alpha < 1:
                        lab = lab.copy(); lab.putalpha(Image.fromarray((np.array(lab)[..., 3] * alpha).astype(np.uint8)))
                    img.alpha_composite(lab, (int(x - lab.width / 2), int(py0 + (spr.info["cy"] + spr.info["r"] + 3) * a.k)))
        fg_relief = relief and fg is not None
        if fg is not None and not fg_relief:
            if fg is bg_fg:                                              # avant-plan du décor : seule sa zone dessinée
                bb = sh._fgbb                                            # est posée (identique, plus rapide)
                if bb is None:
                    bb = sh._fgbb = (fg.getbbox() or (0, 0, 1, 1), )
                    sh._fgc = fg.crop(bb[0])
                img.alpha_composite(sh._fgc, bb[0][:2])
            else:
                img.alpha_composite(fg)
        for an in sh.anims_avant:
            an(img, u)
        for (ai, fn, tin, tout, dx, dy) in sh.bubbles:
            if tin <= u < tout:
                hx, hy, k, mir = heads[ai]
                b = fn().img(k)
                al = smooth((u - tin) / 0.12) * (1 - smooth((u - (tout - 0.12)) / 0.12))
                if al < 1:
                    b = b.copy(); b.putalpha(Image.fromarray((np.array(b)[..., 3] * al).astype(np.uint8)))
                img.alpha_composite(b, (int(hx + dx * k - b.width / 2), int(hy + dy * k - b.height)))
        for (ai, fn, tin, tout) in sh.effets:
            if tin <= u < tout and ai < len(heads) and heads[ai][1] > -9000:
                fn(img, u - tin, heads[ai], tout - tin)
        for ov in sh.overlays:
            ov(img, u)
        if isinstance(sh.cam, list):
            z, cx, cy = cam_keys(sh.cam, u)
        else:
            z0, z1, c0, c1 = sh.cam
            e = smooth(u / D)
            z = z0 + (z1 - z0) * e
            cx = c0[0] + (c1[0] - c0[0]) * e; cy = c0[1] + (c1[1] - c0[1]) * e
        cx += ox
        CW, CH = img.width, img.height                       # la scène (1080x1920, ou 1920x1920 en 16:9)

        def cadre(im, zz, ccx, ccy):
            w, h = W_ / zz, H_ / zz
            x0 = min(max(0, ccx - w / 2), CW - w); y0 = min(max(0, ccy - h / 2), CH - h)
            if abs(zz - 1) > 1e-3 or x0 or y0 or (CW, CH) != (W_, H_):
                return im.crop((x0, y0, x0 + w, y0 + h)).resize((W_, H_), Image.BILINEAR)
            return im
        img = cadre(img, z, cx, cy)
        if relief:                                                       # le lointain bouge moins que la scène
            d = 0.3
            far = cadre(sh._far, 1 + (z - 1) * d, CW / 2 + (cx - CW / 2) * d, CH / 2 + (cy - CH / 2) * d)
            far = far.copy(); far.alpha_composite(img); img = far
            if fg_relief:
                d = 1.12
                img.alpha_composite(cadre(fg, 1 + (z - 1) * d, CW / 2 + (cx - CW / 2) * d, CH / 2 + (cy - CH / 2) * d))
        bande = getattr(s.theme, "cinema", 0)                               # film : bandes noires de cinéma
        if bande:
            d_ = ImageDraw.Draw(img)
            d_.rectangle([0, 0, W_, bande], fill=(4, 3, 6, 255))
            d_.rectangle([0, H_ - bande, W_, H_], fill=(4, 3, 6, 255))
        for ov in sh.ecran:
            ov(img, u)
        return img

    def frame(s, t):
        shots = s.shots
        i = max([k for k, sh in enumerate(shots) if sh.t0 <= t] or [0])
        sh = shots[i]
        img = s.render_shot(sh, t)
        if i + 1 < len(shots) and t > shots[i + 1].t0 - XF / 2:
            a = smooth((t - (shots[i + 1].t0 - XF / 2)) / XF)
            img = Image.blend(img, s.render_shot(shots[i + 1], max(t, shots[i + 1].t0)), a)
        elif i > 0 and t < sh.t0 + XF / 2:
            a = smooth((t - (sh.t0 - XF / 2)) / XF)
            img = Image.blend(s.render_shot(shots[i - 1], t), img, a)
        bande = getattr(s.theme, "cinema", 0)                               # (bandes noires : dans render_shot_v2)
        # bandeau de série, sources, étiquettes (écran)
        if sh.band and s.band is not None:
            img.alpha_composite(s.band, s.theme.bandeau_xy)
        y = 236
        for (txt, t_in, t_out) in ([(sh.src, 0, 99)] if sh.src else []) + sh.tags:
            if t_in <= t - sh.t0 < t_out:
                if getattr(s.theme, "src_droite", False):             # film : petite référence en haut à droite
                    tg = pixel_text(txt, (236, 226, 204), (20, 16, 22), size=8, k=3)
                    img.alpha_composite(tg, (s.W - 44 - tg.width, max(26, bande - tg.height // 2 + 4)))
                    continue
                tg = tag_img(txt, bg=s.theme.etiquette[0], fg=s.theme.etiquette[1])
                img.alpha_composite(tg, (40, y)); y += tg.height + 10
        # sous-titre (carton) : vignette + texte
        for c in s.subs:
            if c["t0"] <= t < c["t1"]:
                im = subtitle_img(c["txt"], c["who"], s.theme.side(c["who"]),
                                  vignette=getattr(s.theme, "vignette_st", True), largeur=getattr(s.theme, "st_largeur", 16),
                                  colle=s.v2)
                al = smooth((t - c["t0"]) / 0.08)
                if al < 1:
                    im = im.copy(); im.putalpha(Image.fromarray((np.array(im)[..., 3] * al).astype(np.uint8)))
                img.alpha_composite(im, (int(s.W / 2 - im.width / 2), int(s.theme.sous_titres_y - im.height / 2)))
                break
        for g in getattr(s, "globaux", []):                             # accroche, étapes (toute la vidéo)
            g(img, t)
        if s.v2:                                                         # filtre film rapide (entiers)
            if s.brouillon:                                              # aperçu rapide : sans grain ni vignette
                return img.convert("RGB")
            # (11/11/2026) même calcul qu'avant, au pixel près, mais dans un seul tampon : (image x filtre) / 128 + grain,
            # borné à 0-255 ; le grain est stocké décalé de +128 pour rester en entiers positifs
            b = s._tampon
            np.multiply(np.asarray(img.convert("RGB")), s.mult16, out=b)
            np.right_shift(b, 7, out=b)
            np.add(b, s.grains16[int(round(t * FPS)) % len(s.grains16)], out=b)
            np.clip(b, 128, 383, out=b)
            np.subtract(b, 128, out=b)
            return Image.fromarray(b.astype(np.uint8))
        # filtre film : vignette, lignes très légères, grain, teinte chaude
        a = np.asarray(img.convert("RGB")).astype(np.float32)
        a *= s.vig * s.scan
        a *= s.warm
        g = s.rng.normal(0, s.theme.grain, (H // 2, W // 2)).astype(np.float32)
        a += np.repeat(np.repeat(g, 2, 0), 2, 1)[..., None]
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

    # ---- sorties
    def sheet(s, path, step=1.0, cols=8):
        ts = np.arange(0.05, s.dlg.dur, step)
        tw, th_ = (180, 320) if getattr(s, "fmt", "portrait") == "portrait" else (320, 180)
        cols = cols if tw == 180 else 5
        th = [s.frame(t).resize((tw, th_)) for t in ts]
        rows = (len(th) + cols - 1) // cols
        sh = Image.new("RGB", (cols * tw, rows * th_))
        d = ImageDraw.Draw(sh)
        for i, (t, im) in enumerate(zip(ts, th)):
            sh.paste(im, ((i % cols) * tw, (i // cols) * th_))
            d.text(((i % cols) * tw + 4, (i // cols) * th_ + 4), f"{t:.1f}", fill=(255, 255, 0))
        sh.save(path)

    def bruitages(s, n):
        """Bruitages et ambiances des plans (+ s.sons) mélangés en une piste, discrète sous la voix."""
        evs = list(getattr(s, "sons", None) or [])
        ambs = []
        for sh in s.shots:
            for ev in sh.sons:
                evs.append((sh.t0 + ev[0],) + tuple(ev[1:]))
            if sh.ambiance:
                ambs.append((sh.t0 - XF / 2, sh.t1 + XF / 2) + tuple(sh.ambiance))
        if not evs and not ambs:
            return None
        fx = np.zeros(n, np.float32)
        manquants = set()
        for ev in evs:
            t, nom, gain = ev[0], ev[1], ev[2]
            try:
                a = bruitage(nom).copy()
            except FileNotFoundError:
                manquants.add(nom)
                continue
            if len(ev) > 3 and ev[3]:
                a = a[:int(ev[3] * SR)]
                f = min(len(a), int(0.25 * SR)); a[-f:] *= np.linspace(1, 0, f)
            i0 = max(0, int(t * SR))
            seg = a[:max(0, n - i0)]
            fx[i0:i0 + len(seg)] += seg * gain
        for (t0, t1, nom, gain) in ambs:
            try:
                a = bruitage(nom)
            except FileNotFoundError:
                manquants.add(nom)
                continue
            i0, i1 = max(0, int(t0 * SR)), min(n, int(t1 * SR))
            if i1 <= i0:
                continue
            L = i1 - i0
            loop = np.tile(a, L // len(a) + 1)[:L].copy()
            f = min(L // 2, int(0.4 * SR))
            loop[:f] *= np.linspace(0, 1, f); loop[-f:] *= np.linspace(1, 0, f)
            fx[i0:i1] += loop * gain
        if manquants:
            print("ATTENTION, bruitages introuvables (ignorés) :", ", ".join(sorted(manquants)))
        return fx

    def _emotion(s, v, n):
        """Passages de musique d'émotion : enveloppe e (0-1, fondus 3,5 s / 4,5 s) et piste nasheed calée sur chaque passage."""
        emo = getattr(s, "emotions", None) or []
        if not emo:
            return None, None
        e = np.zeros(n, np.float32)
        piste = np.zeros(n, np.float32)
        for (t0, t1, chemin) in emo:
            a, b = int(t0 * SR), min(n, int((t1 + 4.5) * SR))
            if b <= a:
                continue
            m = load(chemin)
            seg = b - a
            if len(m) < seg:
                m = np.tile(m, seg // len(m) + 1)
            k = np.arange(seg) / SR
            env_ = np.minimum(1.0, k / 3.5) * np.clip((t1 + 4.5 - t0 - k) / 4.5, 0.0, 1.0)
            piste[a:b] += m[:seg] * env_
            e[a:b] = np.maximum(e[a:b], env_)
        return e, piste

    def audio(s, path):
        v = s.dlg.voice.copy()
        n = len(v)
        mix = v.copy()
        e_emo, p_emo = s._emotion(v, n)
        if e_emo is not None:                                # musique d'émotion : plus bas sous la voix, encore plus sous le Coran
            env_e = _moyenne_glissante(np.abs(v), int(0.25 * SR))
            parle = np.clip(env_e / (np.percentile(env_e, 95) + 1e-6), 0, 1)
            duck_e = 1.0 - 0.78 * parle
            coran = np.zeros(n, np.float32)
            for L in s.dlg.lines:
                if L["who"] == "CORAN":
                    coran[int(L["t0"] * SR):int(L["t1"] * SR)] = 1.0
            coran = _moyenne_glissante(coran, int(0.3 * SR))
            duck_e = duck_e * (1.0 - 0.44 * coran)
            mix = mix + p_emo * 0.12 * duck_e
        if s.music:
            m = load(s.music)
            if len(m) < n:
                m = np.tile(m, n // len(m) + 1)
            m = m[:n]
            env = np.abs(v)
            k = int(0.25 * SR)
            env = _moyenne_glissante(env, k)                 # = np.convolve(env, ones(k)/k, "same"), en O(n) (300x plus rapide)
            duck = 1.0 - 0.55 * np.clip(env / (np.percentile(env, 95) + 1e-6), 0, 1)
            fade = np.minimum(1, np.arange(n) / (0.6 * SR)) * np.minimum(1, (n - np.arange(n)) / (1.2 * SR))
            if e_emo is not None:                            # la musique de fond s'efface sous la musique d'émotion
                fade = fade * (1.0 - 0.9 * e_emo)
            mix = mix + m * s.music_gain * duck * fade
        fx = s.bruitages(n)
        if fx is not None:
            if getattr(s.theme, "film", False):                 # films (02/11/2026, « bruitages trop forts ») : -6 dB,
                env_f = _moyenne_glissante(np.abs(v), int(0.25 * SR))   # et encore -6 dB quand la voix parle
                parle_f = np.clip(env_f / (np.percentile(env_f, 95) + 1e-6), 0, 1)
                fx = fx * 0.5 * (1.0 - 0.5 * parle_f)
            mix = mix + fx
        target = -14 if np.abs(v).max() > 1e-4 else -20         # sans voix (démo, maquette) : plus doux
        tmp = path + ".raw.wav"
        import soundfile as sf
        sf.write(tmp, mix, SR)
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", tmp, "-af", f"loudnorm=I={target}:TP=-1.5:LRA=11", "-ar", str(SR), path], check=True)
        os.remove(tmp)
        if getattr(s, "volume_exact", False):
            s.volume = volume_exact(path, target)

    @staticmethod
    def _lufs(path):
        import re
        r = subprocess.run([FF, "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                           capture_output=True, text=True, errors="ignore").stderr
        m = re.search(r"I:\s+(-?[\d.]+) LUFS", r[r.rfind("Summary:"):])
        return float(m.group(1)) if m else None

    def render(s, out_mp4, workdir, parts=1, part=0):
        priorite_basse()
        os.makedirs(workdir, exist_ok=True)
        n = int(s.dlg.dur * FPS)
        for f in range(part, n, parts):
            p = os.path.join(workdir, f"f{f:05d}.jpg")
            if not os.path.exists(p):
                s.frame(f / FPS).save(p, quality=93)

    # ---- APERÇU RAPIDE (« brouillon », 11/11/2026) : voir le film BOUGER, avec le son, avant le vrai rendu.
    # 1 image sur `pas` (10 images/s), demi-taille, sans filtre film, mot BROUILLON incrusté (jamais publiable).
    def render_brouillon(s, workdir, parts=1, part=0, pas=3):
        priorite_basse()
        os.makedirs(workdir, exist_ok=True)
        s.brouillon = True
        marque = pixel_text("BROUILLON", (255, 226, 90), (20, 16, 22), size=8, k=2)
        n = int(s.dlg.dur * FPS)
        for j, f in enumerate(range(0, n, pas)):
            if j % parts != part:
                continue
            p = os.path.join(workdir, f"b{j:05d}.jpg")
            if not os.path.exists(p):
                im = s.frame(f / FPS).reduce(2)
                im.paste(marque, (10, 8), marque)
                im.save(p, quality=84)

    def encode_brouillon(s, out_mp4, workdir, pas=3):
        priorite_basse()
        wav = os.path.join(workdir, "mix.wav")
        s.audio(wav)
        subprocess.run([FF, "-y", "-loglevel", "error", "-framerate", f"{FPS}/{pas}", "-i", os.path.join(workdir, "b%05d.jpg"),
                        "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out_mp4], check=True)

    def encode(s, out_mp4, workdir):
        priorite_basse()                       # ffmpeg hérite de la priorité basse
        wav = os.path.join(workdir, "mix.wav")
        s.audio(wav)
        if getattr(s.theme, "film", False):
            reglage = ("-preset", "veryfast", "-crf", "16")          # film : parties, réencodées au montage
        elif getattr(s, "encodage_rapide", False):                   # Shorts à scénario (scenario.fabrique, 11/11/2026) :
            reglage = ("-preset", "veryfast", "-crf", "18")          # mesuré sur ISL43, 28 s au lieu de 121 s, même
        else:                                                        # fidélité (SSIM 0,970 / 0,969), 142 Mo / 136 Mo
            reglage = ("-preset", "slow", "-crf", "18")
        subprocess.run([FF, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(workdir, "f%05d.jpg"), "-i", wav,
                        "-c:v", "libx264", *reglage,
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", "-movflags", "+faststart", out_mp4], check=True)


def volume_exact(path, cible, tolerance=0.5, essais=3):
    """Ramène un fichier son à `cible` LUFS à `tolerance` près : loudnorm en une passe sort souvent 1,5 à 2 LUFS trop
    bas quand un perso crie (−15,6 mesuré sur ISL43). Gain simple + limiteur à −1,5 dB, mesuré puis corrigé, au plus
    `essais` fois. Renvoie le volume final (LUFS) ; le fichier n'est remplacé que si le résultat est meilleur."""
    lufs = Video._lufs(path)
    if lufs is None:
        return None
    for _ in range(essais):
        if abs(lufs - cible) <= tolerance:
            break
        tmp = path + ".vol.wav"
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", path, "-af",
                        f"volume={cible - lufs:+.2f}dB,alimiter=limit=-1.5dB:level=false:attack=3:release=60",
                        "-ar", str(SR), tmp], check=True)
        neuf = Video._lufs(tmp)
        if neuf is None or abs(neuf - cible) >= abs(lufs - cible):
            os.remove(tmp)
            break
        os.replace(tmp, path)
        lufs = neuf
    return lufs
