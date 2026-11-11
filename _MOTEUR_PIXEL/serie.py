# Outils communs de la série « VALABLE OU PAS ? » (dialogue des deux frères) : accroche, plans types, tableau.
import json, math
import numpy as np
from PIL import Image, ImageDraw
import pxv, duo, sets
from pxv import Shot, Actor, smooth

V = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/SHORTS VALABLE OU PAS/voix/"
OUT = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/SHORTS VALABLE OU PAS/"
MUSIC = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MUSIQUES/FOND/fond_espoir.mp3"
CHALK = (238, 238, 226)
YEL = (250, 214, 110)
T_HOOK = 1.85


def acteur(who, x, y, k=7, mirror=None, breathe=0.0, bob=0.0, **st):
    if mirror is None:
        mirror = who == "G"
    return Actor(who, x, y, k, mirror, state=lambda u, st=st: dict(st), breathe=breathe, bob=bob)


def polaroid(bg="mosquee", crop=(96, 200, 174, 278), who="P", **st):
    b, _ = sets.DECORS[bg]()
    m = b.img(1).crop(crop).resize((78, 78), Image.NEAREST)
    p = duo.sprite(who, **st)
    top = duo.HEAD_TOP.get(who, duo.FOOT - 73)
    head = p.crop((6, top - 2, 40, top + 30)).resize((68, 64), Image.NEAREST)
    m = m.convert("RGBA"); m.alpha_composite(head, (5, 14))
    fr = Image.new("RGBA", (90, 104), (248, 246, 240, 255)); d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, 89, 103], outline=(30, 22, 30, 255)); fr.alpha_composite(m, (6, 6))
    d.rectangle([5, 5, 84, 84], outline=(30, 22, 30, 255))
    pin = Image.new("RGBA", (12, 22), (0, 0, 0, 0)); dp = ImageDraw.Draw(pin)
    dp.rectangle([3, 0, 8, 21], fill=(198, 150, 92, 255), outline=(30, 22, 30, 255))
    dp.rectangle([2, 9, 9, 12], fill=(160, 120, 60, 255), outline=(30, 22, 30, 255))
    out = Image.new("RGBA", (90, 116), (0, 0, 0, 0))
    out.alpha_composite(fr.rotate(-3, resample=Image.NEAREST), (0, 12)); out.alpha_composite(pin, (39, 0))
    return out.resize((540, 696), Image.NEAREST)


def board(lines=(), icons=(), src=None):
    """lines : (y, texte, taille, jaune?) ; icons : (nom, x, y, échelle) ; src en étiquette au bas du tableau."""
    def draw(c):
        for y, txt, size, yel in lines:
            c.text((135, y), txt, YEL if yel else CHALK, size=size, anchor="ma")
        for name, x, y, k in icons:
            sp = duo.icone2(name) if name in duo.ICONS2 else duo.icone(name)
            c.paste(sp.img(k), x, y)
        if src:
            w = min(200, 8 + len(src) * 5)
            c.fill(c.mask_rect(135 - w // 2, 211, 135 + w // 2, 225), (26, 22, 30))
            c.text((135, 213), src, (250, 240, 220), size=8, anchor="ma")
    return draw


def cta_overlay(img, u):
    if u < 0.2:
        return
    a = pxv.pixel_text("ABONNE-TOI", (255, 255, 255), (120, 20, 30), size=13, k=5, ol2=(14, 10, 18))
    b = pxv.pixel_text("POUR LA SUITE", (255, 214, 90), (90, 40, 10), size=11, k=5, ol2=(14, 10, 18))
    al = smooth((u - 0.2) / 0.25)
    for im, y in ((a, 330), (b, 430)):
        if al < 1:
            im = im.copy(); im.putalpha(Image.fromarray((np.array(im)[..., 3] * al).astype(np.uint8)))
        img.alpha_composite(im, (int(540 - im.width / 2), y))


def rows(front_y=1770, front_k=6, with_p=None, imam=True, gap=None):
    acts = []
    if imam:
        acts.append(Actor("IMAM", 540, 1262, 4))
    for i, x in enumerate((150, 300, 450, 630, 780, 930)):
        acts.append(Actor(f"F{i % 4}", x, 1352, 4))
    for i, x in enumerate((90, 330, 750, 990)):
        acts.append(Actor(f"F{(i + 2) % 4}", x, 1540, 5))
    for i, x in enumerate((200, 540, 880)):
        if with_p is not None and i == 1:
            acts.append(with_p)
        elif gap == i:
            acts.append(Actor("F0", -9999, front_y, front_k))
        else:
            acts.append(Actor(f"F{(i + 1) % 4}", x, front_y, front_k))
    return acts


# ------------------------------------------------------------------ plans types
def duo_shot(t0, t1, p=None, g=None, bg="salon", extra=(), cam=(1.0, 1.05, (540, 1080), (540, 1060)), **kw):
    acts = [acteur("P", 300, 1340, **(p or dict(pose="neutre", face="neutre"))),
            acteur("G", 780, 1340, **(g or dict(pose="the", face="blase")))] + list(extra)
    return Shot(t0, t1, bg, acts, cam=cam, **kw)


def close(t0, t1, who, bg="salon", bubble=None, **st):
    a = acteur(who, 540 if who == "P" else 520, 1830 if who != "G" else 1900, k=18 if who != "G" else 17, breathe=6, **st)
    return Shot(t0, t1, bg, [a], cam=(1.0, 1.05, (540, 900), (530, 880)), blur=4, fg=False,
                bubbles=[(0, (lambda b=bubble: duo.bulle(b)), 0.15, 9, 12, -2)] if bubble else [])


def board_shot(t0, t1, drawfn, p=None, g=None):
    return Shot(t0, t1, "tableau", [acteur("P", 230, 1380, **(p or dict(pose="question", face="neutre"))),
                                     acteur("G", 850, 1380, **(g or dict(pose="pointe", face="neutre")))],
                cam=(1.0, 1.04, (540, 820), (540, 780)), board=drawfn)


def hook(title_lines, pol):
    return Shot(0.0, T_HOOK, "carte", cam=(1.0, 1.04, (540, 900), (540, 930)), band=False,
                world=[(pxv.big_title(title_lines, size=88), 540, 200, 0.0), (pol, 540, 520, 0.0)])


def end_shot(t0, t1):
    return duo_shot(t0, t1, p=dict(pose="neutre", face="rire", mute=True, bob=9), g=dict(pose="the", face="content"),
                    cam=(1.06, 1.09, (540, 1080), (540, 1080)), overlays=[cta_overlay])


def dialogue(sk, order, nlines, texts):
    asr = json.load(open(V + f"asr_{sk}.json", encoding="utf-8"))
    D = pxv.Dialogue(V, sk, order, nlines, asr)
    D.dur -= 0.2
    D.align(texts)
    return D


def main(VID, D, sk, title):
    import sys
    cmd = sys.argv[1]
    work = f"C:/Users/abdellah/AppData/Local/Temp/ia501/{sk}_frames"
    if cmd == "sheet":
        VID.sheet(sys.argv[2], step=1.0)
    elif cmd == "frames":
        VID.render(None, work, parts=int(sys.argv[3]), part=int(sys.argv[2]))
    elif cmd == "video":
        VID.encode(OUT + f"{sk} - {title}.mp4", work)
    elif cmd == "info":
        for L in D.lines:
            print(L["k"], L["who"], f'{L["t0"]:.2f}-{L["t1"]:.2f}', " ".join(w["t"] for w in L["words"])[:60])
        print("durée", round(D.dur, 2))
