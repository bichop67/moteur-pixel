# VOP06 « J'ai lâché un prout pendant la prière » — dialogue des deux frères, style pixel « Faux Positif ».
# python vop06.py sheet | frames i n | video
import sys, os, json, math
import numpy as np
from PIL import Image, ImageDraw
import pxv, duo, sets
from pxv import Shot, Actor, smooth, W, H
from px import Px, TAHOMA

V = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/SHORTS VALABLE OU PAS/voix/"
OUT = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/SHORTS VALABLE OU PAS/"
WORK = "C:/Users/abdellah/AppData/Local/Temp/ia501/vop06_frames"
MUSIC = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MUSIQUES/FOND/fond_espoir.mp3"

ORDER = ["P", "G", "P", "G", "P", "G", "G", "P", "G", "P", "G", "G"]
TEXTS = ["J'ai lâché un prout pendant la prière… elle compte encore ?",
         "Non, elle est annulée. Un gaz, même sans bruit, casse tes ablutions.",
         "Mais tout le monde va savoir !",
         "Le Prophète ﷺ a prévu le cas : tiens-toi le nez, et sors.",
         "Le nez ?!",
         "D'après les savants, on croira que tu saignes du nez.",
         "Tu refais tes ablutions, puis ta prière. Si l'imam prie encore, tu le rejoins.",
         "Et si c'est juste un doute ?",
         "Le hadith dit : qu'il ne parte pas, tant qu'il n'entend pas un bruit, ou ne sent pas une odeur.",
         "Donc si ça sent…",
         "Ça peut être le voisin ! Si t'es sûr que c'est toi : le nez, et tu sors.",
         "Abonne-toi pour la suite."]

asr = json.load(open(V + "asr_VOP06.json", encoding="utf-8"))
D = pxv.Dialogue(V, "VOP06", ORDER, dict(P=5, G=7), asr)
D.dur -= 0.2
D.align(TEXTS)
L = D.lines
t = lambda k: L[k]["t0"]
te = lambda k: L[k]["t1"]
at = D.at

CHALK = (238, 238, 226)
CHALK2 = (196, 214, 200)


# ------------------------------------------------------------------ tableaux (écrits à la craie)
def board_annulee(c):
    c.text((135, 84), "SANS ABLUTIONS", CHALK, size=15, anchor="ma")
    c.text((135, 106), "=", (250, 214, 110), size=15, anchor="ma")
    c.text((135, 126), "PRIÈRE PAS", CHALK, size=15, anchor="ma")
    c.text((135, 146), "ACCEPTÉE", (250, 214, 110), size=15, anchor="ma")
    for x in range(80, 192):
        if x % 7 != 0:
            c.px(x, 166, CHALK2)
    c.text((135, 182), "UN GAZ, MÊME SANS", CHALK, size=11, anchor="ma")
    c.text((135, 196), "BRUIT, CASSE", CHALK, size=11, anchor="ma")
    c.text((135, 210), "TES ABLUTIONS", CHALK, size=11, anchor="ma")
    plate = c.mask_rect(84, 230, 186, 244); c.fill(plate, (26, 22, 30))
    c.text((135, 232), "SRC  BOUKHARI 135", (250, 240, 220), size=8, anchor="ma")


def board_doute(c):
    c.text((135, 76), "UN DOUTE ?", (250, 214, 110), size=15, anchor="ma")
    for x0, icon, lab in ((40, "oreille", "UN BRUIT ?"), (150, "nez", "UNE ODEUR ?")):
        ic = duo.icone(icon).img(3)
        c.paste(ic, x0 + 18, 100)
        c.text((x0 + 38, 146), lab, CHALK, size=11, anchor="ma")
    c.text((135, 172), "SINON :", CHALK, size=13, anchor="ma")
    c.text((135, 190), "TU RESTES", (250, 214, 110), size=15, anchor="ma")
    plate = c.mask_rect(68, 211, 188, 225); c.fill(plate, (26, 22, 30))
    c.text((128, 213), "SRC  BOUKHARI 137 · MOUSLIM 362", (250, 240, 220), size=8, anchor="ma")


# ------------------------------------------------------------------ la photo d'accroche (polaroid + pince)
def polaroid():
    bg, _ = sets.mosquee()
    m = bg.img(1).crop((96, 200, 174, 278))                        # 78x78
    p = duo.sprite("P", pose="panique", face="choc", sweat=True, blush=True)
    head = p.crop((6, duo.FOOT - 66, 40, duo.FOOT - 34)).resize((68, 64), Image.NEAREST)
    m = m.convert("RGBA"); m.alpha_composite(head, (5, 14))
    fr = Image.new("RGBA", (90, 104), (248, 246, 240, 255))
    d = ImageDraw.Draw(fr)
    d.rectangle([0, 0, 89, 103], outline=(30, 22, 30, 255))
    fr.alpha_composite(m, (6, 6))
    d.rectangle([5, 5, 84, 84], outline=(30, 22, 30, 255))
    for y in range(90, 100, 3):                                     # reflet/texture du bas
        d.line([(10, y), (80, y)], fill=(236, 232, 224, 255))
    pin = Image.new("RGBA", (12, 22), (0, 0, 0, 0)); dp = ImageDraw.Draw(pin)
    dp.rectangle([3, 0, 8, 21], fill=(198, 150, 92, 255), outline=(30, 22, 30, 255))
    dp.line([(5, 2), (5, 19)], fill=(226, 186, 128, 255)); dp.rectangle([2, 9, 9, 12], fill=(160, 120, 60, 255), outline=(30, 22, 30, 255))
    out = Image.new("RGBA", (90, 116), (0, 0, 0, 0))
    out.alpha_composite(fr.rotate(-3, resample=Image.NEAREST, expand=False), (0, 12))
    out.alpha_composite(pin, (39, 0))
    return out.resize((90 * 6, 116 * 6), Image.NEAREST)


TITLE = pxv.big_title([("UN PROUT PENDANT", (255, 255, 255)), ("LA PRIÈRE ?", (255, 210, 70))], size=92)


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


def splash(img, u):
    """Eau qui tombe sur les mains + gouttes (pixels de 4)."""
    d = ImageDraw.Draw(img)
    for y in range(1200, 1250, 4):
        d.rectangle([590, y, 601, y + 3], fill=(150, 210, 248, 255))
        d.rectangle([594, y, 597, y + 3], fill=(236, 248, 255, 255))
    rnd = np.random.default_rng(int(u * 12))
    for _ in range(12):
        x = 596 + int(rnd.integers(-40, 40)); y = 1250 + int(rnd.integers(-14, 26))
        d.rectangle([x, y, x + 3, y + 3], fill=(206, 238, 252, 255))


# ------------------------------------------------------------------ acteurs
def P(x, y, k=7, mirror=False, **st):
    return Actor("P", x, y, k, mirror, state=lambda u, st=st: st)


def G(x, y, k=7, mirror=True, **st):
    return Actor("G", x, y, k, mirror, state=lambda u, st=st: st)


def rows(front_y=1770, front_k=6, with_p=None, imam=True, gap=None):
    """Rangées de fidèles vus de dos (+ l'imam devant)."""
    acts = []
    if imam:
        acts.append(Actor("IMAM", 540, 1262, 4))
    for i, x in enumerate((150, 300, 450, 630, 780, 930)):
        acts.append(Actor(f"F{i % 4}", x, 1352, 4))
    for i, x in enumerate((90, 330, 750, 990)):
        acts.append(Actor(f"F{(i + 2) % 4}", x, 1540, 5))
    xs = (200, 540, 880)
    for i, x in enumerate(xs):
        if with_p is not None and i == 1:
            acts.append(with_p)
        elif gap == i:
            acts.append(Actor("F0", -9999, front_y, front_k))
        else:
            acts.append(Actor(f"F{(i + 1) % 4}", x, front_y, front_k))
    return acts


shots = []
S = shots.append
T_HOOK = 1.85
# 1. accroche : carte titre + photo
S(Shot(0.0, T_HOOK, "carte", cam=(1.0, 1.04, (540, 900), (540, 930)), band=False,
       world=[(TITLE, 540, 200, 0.0), (polaroid(), 540, 520, 0.0)]))
# 1b. dans la mosquée : le petit frère dans le rang (de dos)
S(Shot(T_HOOK, te(0) + 0.05, "mosquee", rows(with_p=Actor("P", 540, 1770, 6, state=lambda u: dict(back=True))),
       cam=(1.05, 1.16, (540, 1250), (540, 1380)),
       bubbles=[(12, lambda: duo.bulle("!"), 0.15, 9, 0, -2)]))
# 2. salon : « Non, elle est annulée. »
S(Shot(t(1), at(1, "Un"), "salon", [P(300, 1340, pose="neutre", face="choc"), G(780, 1340, pose="the", face="blase")],
       cam=(1.0, 1.05, (540, 1100), (560, 1080))))
# 2b. tableau : sans ablutions = prière pas acceptée
S(Shot(at(1, "Un"), te(1) + 0.08, "tableau", [P(230, 1380, pose="question", face="neutre"), G(850, 1380, pose="pointe", face="neutre")],
       cam=(1.0, 1.04, (540, 820), (540, 780)), board=board_annulee))
# 3. gros plan : « Mais tout le monde va savoir ! »
S(Shot(t(2), te(2) + 0.06, "mosquee", [Actor("P", 560, 1830, 18, False, state=lambda u: dict(pose="panique", face="choc", sweat=True, blush=True), breathe=6)],
       cam=(1.0, 1.04, (540, 900), (540, 880)), blur=4))
# 4. gros plan grand frère : « Le Prophète ﷺ a prévu le cas : »
S(Shot(t(3), at(3, "tiens-toi"), "salon", [Actor("G", 520, 1900, 17, True, state=lambda u: dict(pose="explique", face="neutre"), breathe=5)],
       cam=(1.0, 1.04, (540, 880), (520, 860)), blur=4, fg=False))
# 4b. mosquée : il sort en se tenant le nez
walk = Actor("P", 0, 0, 8, True, state=lambda u: dict(pose="nez", face="gene", sweat=True, step=int(u / 0.16) % 4),
             path=lambda u: (1010 - 250 * min(1, u / 1.9), 1720))
S(Shot(at(3, "tiens-toi"), te(3) + 0.08, "mosquee", rows(gap=2) + [walk], cam=(1.0, 1.03, (540, 1300), (520, 1320)),
       src="SRC  ABOU DAWOUD 1114 · IBN MAJAH 1222"))
# 5. gros plan : « Le nez ?! »
S(Shot(t(4), te(4) + 0.08, "mosquee", [Actor("P", 520, 1830, 18, False, state=lambda u: dict(pose="nez", face="choc", sweat=True), breathe=6)],
       cam=(1.0, 1.05, (540, 900), (560, 880)), blur=4,
       bubbles=[(0, lambda: duo.bulle("?!"), 0.0, 9, 10, -2)]))
# 6. les gens croient qu'il saigne du nez
S(Shot(t(5), te(5) + 0.08, "mosquee",
       rows(gap=0) + [Actor("P", 0, 0, 8, True, state=lambda u: dict(pose="nez", face="gene", step=int(u / 0.16) % 4),
                       path=lambda u: (330 - 260 * min(1, u / 2.4), 1720))],
       cam=(1.0, 1.04, (560, 1240), (600, 1260)), src="SRC  AL-KHATTABI, MA'ALIM AS-SOUNAN",
       tags=[("PAS UN MENSONGE : DE LA PUDEUR", 0.6, 99)],
       bubbles=[(12, duo.pensee_saigne, 0.35, 9, 3, -2)]))
# 7. ablutions puis retour dans le rang (l'imam prie encore)
S(Shot(t(6), at(6, "Si"), "ablutions", [P(482, 1470, pose="ablution", face="content")],
       cam=(1.45, 1.52, (580, 1150), (590, 1150)), overlays=[splash]))
S(Shot(at(6, "Si"), te(6) + 0.08, "mosquee", rows(with_p=Actor("P", 540, 1770, 6, state=lambda u: dict(back=True))),
       cam=(1.12, 1.22, (540, 1300), (540, 1260))))
# 8. gros plan : « Et si c'est juste un doute ? »
S(Shot(t(7), te(7) + 0.08, "salon", [Actor("P", 540, 1830, 18, False, state=lambda u: dict(pose="neutre", face="gene"), breathe=6)],
       cam=(1.0, 1.04, (540, 900), (520, 900)), blur=4, fg=False,
       bubbles=[(0, lambda: duo.bulle("?"), 0.2, 9, 12, -2)]))
# 9. tableau : un bruit ? une odeur ? sinon tu restes
S(Shot(t(8), te(8) + 0.08, "tableau", [P(230, 1380, pose="question", face="neutre"), G(850, 1380, pose="pointe", face="neutre")],
       cam=(1.0, 1.05, (540, 800), (540, 760)), board=board_doute))
# 10. gros plan : « Donc si ça sent… »
S(Shot(t(9), te(9) + 0.08, "salon", [Actor("P", 540, 1830, 18, False, state=lambda u: dict(pose="neutre", face="malin"), breathe=6)],
       cam=(1.0, 1.05, (540, 900), (560, 880)), blur=4, fg=False))
# 11. salon : « Ça peut être le voisin ! … le nez, et tu sors. »
S(Shot(t(10), te(10) + 0.08, "salon", [Actor("P", 300, 1340, 7, False, state=lambda u: dict(pose="neutre", face="choc" if u < 1.6 else "content")),
                                     G(780, 1340, pose="explique", face="blase")],
       cam=(1.0, 1.06, (540, 1080), (520, 1060))))
# 12. fin : abonne-toi
S(Shot(t(11), D.dur, "salon", [Actor("P", 300, 1340, 7, False, state=lambda u: dict(pose="neutre", face="rire", mute=True), bob=9), G(780, 1340, pose="the", face="content")],
       cam=(1.06, 1.09, (540, 1080), (540, 1080)), overlays=[cta_overlay]))

VID = pxv.Video(D, shots, music=MUSIC, music_gain=0.10)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "sheet":
        VID.sheet(sys.argv[2], step=float(sys.argv[3]) if len(sys.argv) > 3 else 1.0)
    elif cmd == "still":
        VID.frame(float(sys.argv[2])).save(sys.argv[3])
    elif cmd == "frames":
        VID.render(None, WORK, parts=int(sys.argv[3]), part=int(sys.argv[2]))
    elif cmd == "video":
        VID.encode(OUT + "VOP06 - Un prout pendant la priere.mp4", WORK)
    elif cmd == "subs":
        for c in VID.subs:
            print(f'{c["t0"]:.2f}-{c["t1"]:.2f} {c["who"]} {c["txt"]}')
        print("durée", D.dur)
