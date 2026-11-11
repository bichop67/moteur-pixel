# CONTRÔLE DU CADRE AVANT LE RENDU (11/11/2026) : ce qui est dessiné HORS de l'image sans que rien ne le signale.
#   python controle_cadre.py scenarios\film\gog\p06.txt [autre.txt …]
# Dans un film 16:9, la scène fait 1920 x 1920 mais l'image n'en montre qu'une fenêtre de 1920 x 1080 (moins les bandes
# noires). Pendant le film Gog et Magog, des foules entières ont été dessinées sous cette fenêtre : la planche montrait
# un décor vide et il fallait deviner pourquoi. Ce contrôle le dit tout de suite :
#   - une ANIMATION (foule, pluie, objet…) dont moins d'un quart du dessin tombe dans l'image, à tous les instants testés ;
#   - un PERSONNAGE (ou une orbe) qui n'entre jamais dans l'image pendant toute une scène (même décor d'affilée).
# Il ne change rien au rendu. Utilisable depuis un autre outil : controle_cadre.examine(VID) -> liste de messages.
import io
import os
import sys
import contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SEUIL_ANIM = 0.25            # part minimale du dessin d'une animation qui doit tomber dans l'image
SEUIL_PERSO = 0.30           # part minimale du corps d'un personnage dans l'image pour le compter « visible »


def _fenetre(vid, sh, u):
    """Fenêtre visible de la scène à l'instant u du plan (x0, y0, x1, y1, en pixels de la scène), bandes noires retirées."""
    import pxv
    D = max(0.01, sh.t1 - sh.t0)
    CW, CH = sh._bga.size
    ox = (CW - pxv.W) // 2
    if isinstance(sh.cam, list):
        z, cx, cy = pxv.cam_keys(sh.cam, u)
    else:
        z0, z1, c0, c1 = sh.cam
        e = pxv.smooth(u / D)
        z = z0 + (z1 - z0) * e
        cx = c0[0] + (c1[0] - c0[0]) * e
        cy = c0[1] + (c1[1] - c0[1]) * e
    cx += ox
    w, h = vid.W / z, vid.H / z
    x0 = min(max(0, cx - w / 2), CW - w)
    y0 = min(max(0, cy - h / 2), CH - h)
    bande = getattr(vid.theme, "cinema", 0) / z
    return x0, y0 + bande, x0 + w, y0 + h - bande, ox


def _boite_perso(a, u, ox):
    """Boîte (x0, y0, x1, y1) du corps dessiné d'un personnage à l'instant u, ou None s'il est invisible (alpha 0)."""
    import duo
    st = dict(a.state(u))
    st.pop("_mirror", None)
    if st.pop("_alpha", 1.0) <= 0.01:
        return None
    for k_ in ("mute", "noblink"):
        st.pop(k_, None)
    try:
        spr = duo.sprite(a.who, **st) if duo.anime(a.who) else duo.sprite(a.who)
        bb = spr.getbbox() or (0, 0, spr.width, spr.height)
        foot = spr.info.get("foot", duo.FOOT)
        larg = spr.width
    except Exception:                                    # noqa: BLE001 (pose inconnue ici : boîte approximative)
        bb, foot, larg = (8, 0, 40, 80), 80, 48
    x, y = a.path(u) if a.path else (a.x, a.y)
    x += ox
    return (x - larg * a.k / 2 + bb[0] * a.k, y - foot * a.k + bb[1] * a.k,
            x - larg * a.k / 2 + bb[2] * a.k, y - foot * a.k + bb[3] * a.k)


def _part(b, f):
    """Part de la boîte b qui tombe dans la fenêtre f."""
    w = max(0.0, min(b[2], f[2]) - max(b[0], f[0]))
    h = max(0.0, min(b[3], f[3]) - max(b[1], f[1]))
    aire = max(1.0, (b[2] - b[0]) * (b[3] - b[1]))
    return w * h / aire


def _temps(t):
    return "%d:%02d" % (int(t) // 60, int(t) % 60)


def examine(vid):
    """Liste de messages (vide = tout ce qui est dessiné se voit)."""
    import numpy as np
    from PIL import Image
    if not getattr(vid, "v2", False):
        return []
    out = []
    scenes = []                                          # plans d'affilée dans le même décor
    for sh in vid.shots:
        if scenes and scenes[-1][-1].bg == sh.bg:
            scenes[-1].append(sh)
        else:
            scenes.append([sh])
    for plans in scenes:
        vus = {}                                         # personnage -> meilleure part visible sur toute la scène
        for sh in plans:
            sh.background(vid.fmt)
            D = max(0.05, sh.t1 - sh.t0)
            us = [D * (i + 0.5) / n for n in [min(8, max(2, int(D / 1.5)))] for i in range(n)]
            for a in sh.actors:
                for u in us:
                    try:
                        b = _boite_perso(a, u, _fenetre(vid, sh, u)[4])
                    except Exception:                    # noqa: BLE001
                        b = None
                    if b is None:
                        continue
                    vus[a.who] = max(vus.get(a.who, 0.0), _part(b, _fenetre(vid, sh, u)[:4]))
            for genre, liste in (("derrière les persos", sh.anims), ("devant les persos", sh.anims_avant),
                                 ("posée sur la scène", sh.overlays)):
                for i, an in enumerate(liste):
                    meilleur, dessine, zone = 0.0, False, None
                    for u in us:
                        lay = Image.new("RGBA", sh._bga.size, (0, 0, 0, 0))
                        try:
                            with contextlib.redirect_stdout(io.StringIO()):
                                an(lay, u)
                        except Exception:                # noqa: BLE001 (animation qui a besoin du décor : ignorée)
                            dessine = False
                            break
                        al = np.asarray(lay.getchannel("A").reduce(4)) > 0
                        tot = int(al.sum())
                        if not tot:
                            continue
                        dessine = True
                        x0, y0, x1, y1, _ = _fenetre(vid, sh, u)
                        dedans = int(al[int(y0 / 4):int(y1 / 4) + 1, int(x0 / 4):int(x1 / 4) + 1].sum())
                        if dedans / tot >= meilleur:
                            ys = np.nonzero(al.any(axis=1))[0]
                            meilleur, zone = dedans / tot, (int(ys.min()) * 4, int(ys.max()) * 4, int(y0), int(y1))
                    if dessine and meilleur < SEUIL_ANIM:
                        nom = getattr(an, "__qualname__", getattr(an, "__name__", "animation")).split(".<locals>")[0]
                        out.append("%s, décor %s : l'animation %s (%s) dessine entre y = %d et %d, l'image montre y = %d à %d "
                                   "→ %d %% visible au mieux" % (_temps(sh.t0), sh.bg, nom, genre, zone[0], zone[1], zone[2],
                                                                 zone[3], int(100 * meilleur)))
        for who, part in vus.items():
            if part < SEUIL_PERSO:
                out.append("%s à %s, décor %s : %s n'entre jamais dans l'image (%d %% visible au mieux)"
                           % (_temps(plans[0].t0), _temps(plans[-1].t1), plans[0].bg, who, int(100 * part)))
    return list(dict.fromkeys(out))


def examine_fichier(chemin):
    import scenario
    with contextlib.redirect_stdout(io.StringIO()):
        vid = scenario.fabrique(os.path.abspath(chemin))[0]
    return examine(vid)


if __name__ == "__main__":
    os.chdir(HERE)
    if len(sys.argv) < 2:
        raise SystemExit("python controle_cadre.py scenario.txt [autre.txt …]")
    total = 0
    for f in sys.argv[1:]:
        msgs = examine_fichier(f)
        total += len(msgs)
        print(os.path.basename(f), ":", "tout ce qui est dessiné se voit" if not msgs else "")
        for m in msgs:
            print("   ", m)
    sys.exit(1 if total else 0)
