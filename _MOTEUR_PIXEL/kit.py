# KIT DE PLANS : tout ce qu'il faut pour monter un Short « duo » avec n'importe quels personnages, décors et chaîne.
#   import kit
#   plans = [kit.accroche(["TITRE", "CHOC ?"], kit.photo("rue", "ADO", face="choc"), theme),
#            kit.duo_plan(t0, t1, "rue_nuit", "ADO", "PAPI", g=dict(pose="question"), d=dict(pose="explique")),
#            kit.gros_plan(t0, t1, "ADO", "rue_nuit", face="choc", bulle="?"),
#            kit.tableau_plan(t0, t1, kit.ecrit([(90, "TEXTE", 15, True)], [("argent", 100, 130, 5)], style="craie")),
#            kit.fin(t0, t1, "rue_nuit", "ADO", "PAPI", theme)]
#   VID = pxv.Video(dialogue, plans, music=..., theme=theme) ; kit.rendu(VID, "nom", dossier)
# Voir LISEZMOI_MOTEUR.txt pour la procédure complète (voix, alignement, rendu, contrôle).
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
import pxv, duo, sets, lieux, cast, objets
from pxv import Shot, Actor, smooth, Theme, Silence, W, H

T_HOOK = 1.85
CHALK, YEL = (238, 238, 226), (250, 214, 110)

# =================================================================== thèmes de chaîne
THEMES = dict(
    valable=Theme(),
    neutre=Theme(bandeau=None),
    sketch=Theme(bandeau=None, grain=4.0, carte="carte_noire"),
    info=Theme(bandeau="L'INFO EN 30 S", bandeau_fond=(190, 30, 46), bandeau_accent=(255, 255, 255), bandeau_contour=(90, 10, 20),
               chaleur=(1.0, 1.0, 1.0), grain=3.0, carte="carte_rouge", cta=("ABONNE-TOI", "POUR L'INFO")),
    histoire=Theme(bandeau="IL ÉTAIT UNE FOIS", bandeau_fond=(110, 70, 36), bandeau_accent=(230, 190, 100), bandeau_contour=(60, 36, 16),
                   chaleur=(1.06, 1.0, 0.9), grain=6.0, vignette=0.48, carte="carte_sepia", etiquette=((70, 46, 26), (250, 236, 200))),
    mystere=Theme(bandeau="AFFAIRE NON RÉSOLUE", bandeau_fond=(50, 24, 70), bandeau_accent=(180, 120, 255), bandeau_contour=(30, 10, 40),
                  chaleur=(0.95, 0.98, 1.06), vignette=0.55, grain=7.0, carte="carte_violette"),
    science=Theme(bandeau="LE SAVAIS-TU ?", bandeau_fond=(20, 80, 160), bandeau_accent=(120, 230, 255), bandeau_contour=(10, 40, 90),
                  chaleur=(0.98, 1.0, 1.04), carte="carte_bleue"),
    argent=Theme(bandeau="ARGENT : VRAI OU FAUX ?", bandeau_fond=(30, 110, 60), bandeau_accent=(250, 210, 70), bandeau_contour=(10, 50, 26),
                 carte="carte_verte"),
    podcast=Theme(bandeau="LE PODCAST", bandeau_fond=(140, 40, 120), bandeau_accent=(120, 230, 255), bandeau_contour=(70, 16, 60),
                  carte="carte_noire"),
    # FILM (« L'histoire des prophètes », film.py) : pas de bandeau ni d'« abonne-toi », sous-titres de cinéma,
    # référence en haut à droite, bandes noires, grain et chaleur de pellicule
    film=Theme(bandeau=None, grain=4.5, chaleur=(1.04, 1.0, 0.95), vignette=0.5, lignes=False, cta=None,
               film=True, st_maxc=44, st_largeur=34, vignette_st=False, src_droite=True, cinema=64, format="paysage"),
)


# =================================================================== personnages
def acteur(who, x, y, k=7, mirror=None, breathe=0.0, bob=0.0, **st):
    """Un personnage fixe. mirror=None : il regarde vers le centre de l'image."""
    if mirror is None:
        mirror = x > W / 2
    return Actor(who, x, y, k, mirror, state=lambda u, st=st: dict(st), breathe=breathe, bob=bob)


def spot(bg):
    return lieux.SPOTS.get(bg, dict(gauche=(300, 1340), droite=(780, 1340), k=7, opts={}))


def tete(who, assis=False):
    """Haut du crâne (sans chapeau) sur la toile du sprite."""
    if who in ("P", "G", "S", "IMAM") or (who.startswith("F") and who[1:].isdigit()):
        return duo.HEAD_TOP.get(who, duo.FOOT - 73)
    return cast.geo(cast.CAST[who], assis).y0


def pied(who):
    return duo.sprite(who).info.get("foot", duo.FOOT)


# =================================================================== plans
def duo_plan(t0, t1, bg, gauche, droite, g=None, d=None, cam=None, bulles=None, **kw):
    """Plan large : deux personnages aux places conseillées du décor (debout, ou assis dans la voiture / le studio)."""
    sp = spot(bg)
    opts = sp.get("opts", {})
    a = acteur(gauche, *sp["gauche"], k=sp["k"], mirror=False, **{**opts, **(g or {})})
    b = acteur(droite, *sp["droite"], k=sp["k"], mirror=True, **{**opts, **(d or {})})
    cam = cam or (1.0, 1.05, (540, 1080), (540, 1060))
    return Shot(t0, t1, bg, [a, b], cam=cam, bubbles=bulles or [], **kw)


def solo(t0, t1, who, bg, x=540, k=None, cam=None, bulle=None, **st):
    sp = spot(bg)
    opts = sp.get("opts", {})
    y = sp["gauche"][1]
    a = acteur(who, x, y, k=k or sp["k"], mirror=st.pop("mirror", False), **{**opts, **st})
    return Shot(t0, t1, bg, [a], cam=cam or (1.0, 1.06, (540, 1080), (540, 1040)),
                bubbles=[(0, (lambda b=bulle: duo.bulle(b)), 0.15, 9, 12, -2)] if bulle else [])


def gros_plan(t0, t1, who, bg="salon", k=17, tete_y=690, x=540, mirror=None, bulle=None, pensee=None, blur=4, **st):
    """Gros plan (comme dans VALABLE OU PAS ?) : fond flou, respiration lente, bulle '!' '?' ou pensée (icône)."""
    assis = st.get("assis", False)
    y = tete_y + (pied(who) - tete(who, assis)) * k
    a = acteur(who, x, y, k=k, mirror=mirror if mirror is not None else False, breathe=6, **st)
    bubbles = []
    if bulle:
        bubbles.append((0, (lambda b=bulle: duo.bulle(b)), 0.15, 9, 12, -2))
    if pensee:
        bubbles.append((0, (lambda p=pensee: objets.pensee(p)), 0.2, 9, 14, -2))
    return Shot(t0, t1, bg, [a], cam=(1.0, 1.05, (540, 900), (530, 880)), blur=blur, fg=False, bubbles=bubbles)


def marche(t0, t1, who, bg, x0, x1, y=None, k=None, cam=None, **st):
    """Un personnage traverse le décor en marchant (mouvement lent et doux)."""
    sp = spot(bg)
    y = y or sp["gauche"][1]
    D = max(0.01, t1 - t0)
    a = Actor(who, x0, y, k or sp["k"], x1 < x0,
              state=lambda u, st=st: dict(st, step=(int(u * 12) % 8) if who in cast.CAST else (int(u * 6) % 4)),
              path=lambda u: (x0 + (x1 - x0) * smooth(u / D), y))
    return Shot(t0, t1, bg, [a], cam=cam or (1.02, 1.05, (540, 1080), (540, 1060)))


def ecrit(lignes=(), icones=(), src=None, style="craie"):
    """Ce qui est écrit sur le tableau. lignes : (y, texte, taille, accent?) ; icônes : (nom, x, y, échelle).
    style : craie (tableau vert), feutre (tableau_blanc), ecran (ecran_info), parchemin (tableau_parchemin)."""
    col, acc = dict(craie=(CHALK, YEL), feutre=((40, 50, 74), (210, 40, 50)), ecran=((240, 246, 255), (90, 200, 255)),
                    parchemin=((76, 50, 30), (160, 40, 30)))[style]

    def draw(c):
        for y, txt, size, yel in lignes:
            c.text((135, y), txt, acc if yel else col, size=size, anchor="ma")
        for name, x, y, kk in icones:
            c.paste(objets.icone(name).img(kk), x, y)
        if src:
            w = min(200, 8 + len(src) * 5)
            c.fill(c.mask_rect(135 - w // 2, 211, 135 + w // 2, 225), (26, 22, 30))
            c.text((135, 213), src, (250, 240, 220), size=8, anchor="ma")
    return draw


TABLEAU_DE = dict(craie="tableau", feutre="tableau_blanc", ecran="ecran_info", parchemin="tableau_parchemin")


def tableau_plan(t0, t1, dessin, bg="tableau", gauche="P", droite="G", g=None, d=None):
    acts = []
    if gauche:
        acts.append(acteur(gauche, 230, 1380, mirror=False, **(g or dict(pose="question", face="neutre"))))
    if droite:
        acts.append(acteur(droite, 850, 1380, mirror=True, **(d or dict(pose="pointe", face="neutre"))))
    return Shot(t0, t1, bg, acts, cam=(1.0, 1.04, (540, 820), (540, 780)), board=dessin)


def photo(bg, who, crop=(96, 200, 174, 278), **st):
    """Polaroïd (photo épinglée) avec la tête d'un personnage devant un bout de décor."""
    b, _ = sets.DECORS[bg]()
    m = b.img(1).crop(crop).resize((78, 78), Image.NEAREST)
    p = duo.sprite(who, **st)
    top = duo.HEAD_TOP.get(who, duo.FOOT - 73)
    head = p.crop((6, top - 2, 40, top + 30)).resize((68, 64), Image.NEAREST)
    m = m.convert("RGBA"); m.alpha_composite(head, (5, 14))
    fr = Image.new("RGBA", (90, 104), (248, 246, 240, 255)); dd = ImageDraw.Draw(fr)
    dd.rectangle([0, 0, 89, 103], outline=(30, 22, 30, 255)); fr.alpha_composite(m, (6, 6))
    dd.rectangle([5, 5, 84, 84], outline=(30, 22, 30, 255))
    pin = Image.new("RGBA", (12, 22), (0, 0, 0, 0)); dp = ImageDraw.Draw(pin)
    dp.rectangle([3, 0, 8, 21], fill=(198, 150, 92, 255), outline=(30, 22, 30, 255))
    dp.rectangle([2, 9, 9, 12], fill=(198, 50, 60, 255), outline=(30, 22, 30, 255))
    out = Image.new("RGBA", (90, 116), (0, 0, 0, 0))
    out.alpha_composite(fr.rotate(-3, resample=Image.NEAREST), (0, 12)); out.alpha_composite(pin, (39, 0))
    return out.resize((540, 696), Image.NEAREST)


def accroche(titre, pol, theme=None, t1=T_HOOK, couleurs=((255, 255, 255), (255, 210, 70))):
    """Carte d'accroche (0 à 1,85 s) : titre choc + photo. titre = ["LIGNE 1", "LIGNE 2"]."""
    lines = [(txt, couleurs[min(i, len(couleurs) - 1)]) for i, txt in enumerate(titre)]
    bg = (theme.carte if theme is not None else "carte")
    return Shot(0.0, t1, bg, cam=(1.0, 1.04, (540, 900), (540, 930)), band=False,
                world=[(pxv.big_title(lines, size=88), 540, 200, 0.0), (pol, 540, 520, 0.0)])


def cta(theme=None):
    th = theme or Theme()
    l1, l2 = th.cta
    c1, o1, c2, o2 = th.cta_couleurs

    def overlay(img, u):
        if u < 0.2:
            return
        a = pxv.pixel_text(l1, c1, o1, size=13, k=5, ol2=(14, 10, 18))
        b = pxv.pixel_text(l2, c2, o2, size=11, k=5, ol2=(14, 10, 18))
        al = smooth((u - 0.2) / 0.25)
        for im, y in ((a, img.height * 0.172), (b, img.height * 0.224)):
            if al < 1:
                im = im.copy(); im.putalpha(Image.fromarray((np.array(im)[..., 3] * al).astype(np.uint8)))
            img.alpha_composite(im, (int(img.width / 2 - im.width / 2), int(y)))
    return overlay


def fin(t0, t1, bg, gauche, droite, theme=None, g=None, d=None):
    """Dernier plan : les deux rient / sourient, « ABONNE-TOI POUR LA SUITE » apparaît en fondu (fixe à l'écran)."""
    return duo_plan(t0, t1, bg, gauche, droite, g=g or dict(pose="neutre", face="rire", mute=True),
                    d=d or dict(pose="neutre", face="content"), cam=(1.06, 1.09, (540, 1080), (540, 1080)),
                    ecran=[cta(theme)])


# =================================================================== dialogue : vraies voix ou maquette
PONCT = ("?", "!", ":", "?!", ";", "…", "!?")


def _longueur(txt):
    """Longueur « dite » d'un texte pour estimer sa durée : ﷺ est lu en entier par ElevenLabs
    (« que la paix et le salut d'Allah soient sur lui »), les *étoiles* des mots clés ne se disent pas."""
    return len(txt.replace("*", "")) + txt.count("ﷺ") * 45


class Maquette(pxv.Dialogue):
    """Dialogue SANS voix : durées estimées d'après la longueur du texte (environ 15 caractères par seconde).
    Sert à caler la mise en scène et à vérifier la planche AVANT de générer (et payer) les voix."""

    def __init__(s, repliques, cps=15.0, lead=0.15, avant=None, durees=None):
        s.lines, s.tempo = [], 1.0
        t = lead
        for k, (who, txt) in enumerate(repliques):
            t += (avant or {}).get(k, 0.0)                  # silence voulu avant cette réplique (plan muet, SMS…)
            toks = []
            for tok in txt.split():
                if toks and tok in PONCT:
                    toks[-1] = toks[-1] + " " + tok
                else:
                    toks.append(tok)
            d = max(0.8, _longueur(txt) / cps)
            if durees and durees[k]:                        # durée mesurée sur les vraies voix (estime.py, 11/11/2026)
                d = durees[k]
            tot = sum(_longueur(x) + 1 for x in toks)
            words, acc = [], 0.0
            for tok in toks:
                w0 = t + d * acc / tot
                acc += _longueur(tok) + 1
                words.append(dict(t=tok, s=w0, e=t + d * acc / tot))
            s.lines.append(dict(who=who, a0=0.0, a1=d, t0=t, t1=t + d, words=words, k=k))
            t += d + (0.07 if k % 2 == 0 else 0.11)
        s.dur = t + 0.6
        s.voice = np.zeros(int(s.dur * pxv.SR) + pxv.SR, np.float32)
        s.env = {}
        for w in dict.fromkeys(who for who, _ in repliques):
            e = np.zeros(int(s.dur * pxv.FPS) + pxv.FPS)
            for L in s.lines:
                if L["who"] == w:
                    e[int(L["t0"] * pxv.FPS):int(L["t1"] * pxv.FPS)] = 1.0
            s.env[w] = e


class Calee(Maquette):
    """Dialogue SANS voix dont chaque réplique tombe à l'instant choisi (démos, plans muets avec sous-titres) :
    Calee([(qui, texte, début, durée ou None), …], durée_totale). La bouche suit quand même les lettres des mots."""

    def __init__(s, repliques, dur, cps=15.0):
        s.lines, s.tempo = [], 1.0
        for k, (who, txt, t, d) in enumerate(repliques):
            toks = []
            for tok in txt.split():
                if toks and tok in PONCT:
                    toks[-1] = toks[-1] + " " + tok
                else:
                    toks.append(tok)
            d = d or max(0.8, len(txt) / cps)
            tot = sum(_longueur(x) + 1 for x in toks)
            words, acc = [], 0.0
            for tok in toks:
                w0 = t + d * acc / tot
                acc += _longueur(tok) + 1
                words.append(dict(t=tok, s=w0, e=t + d * acc / tot))
            s.lines.append(dict(who=who, a0=0.0, a1=d, t0=t, t1=t + d, words=words, k=k))
        s.dur = dur
        s.voice = np.zeros(int(s.dur * pxv.SR) + pxv.SR, np.float32)
        s.env = {}
        for w in dict.fromkeys(L["who"] for L in s.lines):
            e = np.zeros(int(s.dur * pxv.FPS) + pxv.FPS)
            for L in s.lines:
                if L["who"] == w:
                    e[int(L["t0"] * pxv.FPS):int(L["t1"] * pxv.FPS)] = 1.0
            s.env[w] = e


def dialogue(voix, code, repliques, gaps=None, avant=None, serre=False, durees=None):
    """Les vraies voix si CODE_QUI.mp3 et asr_CODE.json existent dans le dossier voix, sinon une Maquette.
    avant = {numéro de réplique: secondes de silence avant elle} (pour un plan muet, un écran de SMS…).
    serre = on retire les respirations et silences en début / fin de chaque réplique (scénarios ; pas les VOP).
    durees = durée estimée de chaque réplique pour la maquette (None : 15 caractères par seconde)."""
    import json
    voix = voix if voix.endswith(("/", "\\")) else voix + "/"
    order = [w for w, _ in repliques]
    nlines = {w: order.count(w) for w in dict.fromkeys(order)}
    ok = all(os.path.exists(voix + f"{code}_{w}.mp3") for w in nlines) and os.path.exists(voix + f"asr_{code}.json")
    if not ok:
        print("(maquette : voix absentes, durées estimées)")
        return Maquette(repliques, avant=avant, durees=durees)
    asr = json.load(open(voix + f"asr_{code}.json", encoding="utf-8"))
    g = dict(gaps or {})
    for k, sec in (avant or {}).items():                    # « avant la réplique k » = « après la réplique k-1 »
        if k == 0:
            continue
        g[k - 1] = g.get(k - 1, 0.07 if order[k - 1] == "P" else 0.11) + sec
    textes = {w: [t for (w2, t) in repliques if w2 == w] for w in nlines} if serre else None
    D = pxv.Dialogue(voix, code, order, nlines, asr, gaps=g, lead=0.15 + (avant or {}).get(0, 0.0), serre=serre,
                     textes=textes)
    D.dur -= 0.2
    D.align([t for _, t in repliques])
    return D


def allonge(D, sec):
    """Ajoute `sec` secondes de silence à la fin (dernier plan plus long, le temps de lire « abonne-toi »)."""
    D.dur += sec
    D.voice = np.concatenate([D.voice, np.zeros(int(sec * pxv.SR) + 1, np.float32)])
    for w in list(D.env):
        D.env[w] = np.concatenate([D.env[w], np.zeros(int(sec * pxv.FPS) + 1)])
    return D


def prompts(repliques):
    """Textes à donner à ElevenLabs : une génération par personnage, répliques séparées par [long pause]."""
    out = {}
    for who, txt in repliques:
        out.setdefault(who, []).append(txt.replace("*", ""))      # *mots clés* : seulement pour les sous-titres
    return {w: " [long pause] ".join(v) for w, v in out.items()}


# =================================================================== rendu (mêmes commandes que les VOP)
def vide_images(work, motif="f*.jpg"):
    """Efface les images d'un rendu précédent (dossier temporaire du moteur) avant un rendu complet
    (motif « b*.jpg » : celles d'un brouillon)."""
    import glob
    for f in glob.glob(os.path.join(work, motif)) + glob.glob(os.path.join(work, "mix.wav")):
        os.remove(f)


def rendu(VID, nom, dossier, work=None, code=None, voix=None, repliques=None):
    """python mon_short.py sheet [planche.png] | still 3.5 image.png | frames i n | video | voix | asr"""
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    work = work or os.path.join(os.environ.get("TEMP", "."), "ia501", nom.replace(" ", "_") + "_frames")
    if cmd == "voix" and repliques:
        for w, p in prompts(repliques).items():
            print(f"===== {w} ({len(p)} caractères)\n{p}\n")
        return
    if cmd == "asr" and repliques:
        import voix as vx
        textes = {}
        for w, t in repliques:                              # le texte connu de chaque voix : indice pour la transcription
            textes[w] = (textes.get(w, "") + " " + t).strip()
        print(vx.transcrire(voix, code, list(textes), textes=textes))
        return
    if cmd == "tout":                                     # toutes les images (plusieurs cœurs, priorité basse) + montage
        import subprocess
        pxv.priorite_basse()
        vide_images(work)                                 # jamais d'images d'un ancien rendu (script modifié depuis)
        n = int(sys.argv[2]) if len(sys.argv) > 2 else max(2, min(8, (os.cpu_count() or 4) - 4))
        procs = [subprocess.Popen([sys.executable, sys.argv[0], "frames", str(i), str(n)]) for i in range(n)]
        if any(p.wait() for p in procs):
            raise SystemExit("une partie du rendu a échoué")
        VID.encode(os.path.join(dossier, nom + ".mp4"), work)
        print("vidéo :", os.path.join(dossier, nom + ".mp4"))
        return
    if cmd == "sheet":
        VID.sheet(sys.argv[2] if len(sys.argv) > 2 else os.path.join(dossier, nom + " - planche.png"), step=1.0)
    elif cmd == "still":
        VID.frame(float(sys.argv[2])).save(sys.argv[3])
    elif cmd == "frames":
        VID.render(None, work, parts=int(sys.argv[3]), part=int(sys.argv[2]))
    elif cmd == "brouillon_images":                       # (lancé par « scenario.py x.txt brouillon »)
        VID.render_brouillon(work[:-len("_frames")] + "_brouillon", parts=int(sys.argv[3]), part=int(sys.argv[2]))
    elif cmd == "video":
        VID.encode(os.path.join(dossier, nom + ".mp4"), work)
