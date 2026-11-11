# DÉMONSTRATION EN IMAGE DU 07/11/2026 — Short duo ISL19 « Tu t'énerves ? Dis ça » (format consigne, 30 s).
#   {enerve PETIT}   accroche : sa chambre, le soir ; derrière lui la télé affiche « PERDU » (un match de foot) au-dessus
#                    de la console. Petit debout, en buste très grand, tout rouge, il crie, la manette serrée dans les
#                    mains au premier plan ; une vapeur neutre (gris-rouge) monte de sa tête ; il respire fort.
#   {colere}         à gauche la jauge « COLÈRE » (thermomètre : rouge en haut, orange, vert en bas), pleine ; à droite
#                    Petit debout, énervé, la manette à la main, la vapeur sur la tête ; en haut : rien.
#   {colere refuge}  « A'OÛDHOU BILLÂHI // MINA CH-CHAYTÂNI R-RAJÎM » (voyelles longues) et sa traduction : la jauge
#                    descend en douceur PENDANT qu'il la dit (100 → 25 %), son visage se calme, la vapeur s'arrête
#                    (Boukhari 6115 · Mouslim 2610). Aucun effet « magique » : la jauge descend, c'est tout.
#   {colere fort}    un trophée ; en petit « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : » puis « LE FORT : CELUI QUI // SE
#                    MAÎTRISE DANS LA COLÈRE » (or) ; Petit sourit (Boukhari 6114 · Mouslim 2609).
#   {colere gg}      une notification « GG EZ » glisse en haut : la jauge remonte un peu (45 %) ; il se calme et dit
#                    « A'OÛDHOU BILLÂH » (visage calme, pas malin : la formule n'est pas une vanne), elle redescend
#                    (10 %) ; Petit sourit et fait un POUCE (pas les bras levés en victoire : pas de vantardise).
# Retouches du 07/11/2026 (relecture religieuse) : voyelles longues, attribution au Prophète (paix et salut sur lui)
# et « dans la colère » sur la carte du fort, pouce au lieu de victoire.
# Aucun Chaytan dessiné (le mot n'est écrit que dans la formule), rien de cassé ni de violent ; mouvements doux
# seulement (glissés, fondus, respiration lente). Branché dans explique.Schema par explique_0611.py.
import math
import unicodedata

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import cast
import objets
import pxv
from px import Px, TAHOMA
from pxv import smooth
from explique import _titre, _fade, autocollant, BLANC
from explique_0411b import _Base, _bulle, _translucide, ROUGE, OR_
from explique_0411 import OL, _peau, _sprite, _grand

VAPEUR = (224, 178, 174)                       # la vapeur : neutre, gris-rouge
VAPEUR_OL = (92, 56, 66)
LIQ = dict(rouge=(228, 60, 54), orange=(250, 152, 52), vert=(86, 198, 100))
BOUTONS = ((255, 206, 70), (70, 136, 236), (232, 64, 60), (80, 196, 100))   # jaune, bleu, rouge, vert
ROUGEUR = dict(b=(234, 122, 102), s=(204, 90, 78), d=(158, 62, 56), h=(248, 160, 136))   # la peau, rouge de colère


# ---------------------------------------------------------------- petits outils
def _norm(m):
    """Minuscules sans accents : « Colère » → « colere », « énerve » → « enerve »."""
    return "".join(ch for ch in unicodedata.normalize("NFD", m.lower()) if unicodedata.category(ch) != "Mn")


def _mel(a, b, f):
    return tuple(int(round(x + (y - x) * f)) for x, y in zip(a, b))


def _rougit(a, peau, f):
    """La peau vire au rouge (« rouge de colère ») : f = 0 normal, 1 tout rouge. a = tableau RGBA du dessin."""
    if f <= 0.01:
        return a
    a = a.copy()
    rgb = a[..., :3].copy()
    vis = a[..., 3] > 0
    for k_, c_ in ROUGEUR.items():
        m = vis & np.all(rgb == np.array(peau[k_], np.uint8), axis=-1)
        a[m, :3] = _mel(peau[k_], c_, f)
    return a


def _encre(im):
    """Recadre sur ce qui est dessiné (les titres ont de grandes marges transparentes)."""
    bb = im.getbbox()
    return im.crop(bb) if bb else im


def _pile(ims, ecart=-4):
    """Lignes de texte empilées (recadrées sur l'encre), centrées, serrées."""
    ims = [_encre(i) for i in ims]
    W_ = max(i.width for i in ims)
    out = Image.new("RGBA", (W_, sum(i.height for i in ims) + ecart * (len(ims) - 1)), (0, 0, 0, 0))
    y = 0
    for i in ims:
        out.alpha_composite(i, ((W_ - i.width) // 2, y))
        y += i.height + ecart
    return out


def _sans_accent(txt):
    """« A'OÛDHOU BILLÂHI » → « A'OUDHOU BILLAHI » (même casse)."""
    return "".join(ch for ch in unicodedata.normalize("NFD", txt) if unicodedata.category(ch) != "Mn")


def _ext_haut(txt, size):
    """De combien de pixels les accents d'une ligne (Û, Â, Î, È…) dépassent au-dessus des capitales (police des
    titres, pxv.big_title)."""
    f = ImageFont.truetype(pxv.SEGOE_BLACK, size)
    return max(0, f.getbbox(_sans_accent(txt))[1] - f.getbbox(txt)[1])


def _lignes(lignes, ecart=-4):
    """[(texte, couleur, taille), …] : lignes empilées, centrées et serrées comme _pile, mais l'écart se compte entre
    les CAPITALES : les accents d'une ligne montent dans la marge du bas (ombre) de la ligne du dessus au lieu
    d'écarter les lignes (sinon chaque ligne accentuée prend 13 px de plus)."""
    ims = [_encre(_titre(t_, c_, z_)) for (t_, c_, z_) in lignes]
    ys, y = [], 0
    for j, (im_, (t_, _, z_)) in enumerate(zip(ims, lignes)):
        if j:
            y -= _ext_haut(t_, z_)
        ys.append(y)
        y += im_.height + ecart
    W_ = max(i.width for i in ims)
    out = Image.new("RGBA", (W_, max(y_ + i.height for i, y_ in zip(ims, ys))), (0, 0, 0, 0))
    for i, y_ in zip(ims, ys):                              # dans l'ordre : les accents passent sur l'ombre d'au-dessus
        out.alpha_composite(i, ((W_ - i.width) // 2, y_))
    return out


PERIODE_V = 1.86                               # durée de vie d'une bouffée de vapeur (s)


def _vapeur(im, cx, y0, u, fenetres, px=8, n=3, haut=26, r0=3.0, r1=7.0, ecart=11.0):
    """Vapeur neutre (gris-rouge) qui monte de la tête : des bouffées rondes (pixels de px x px) qui montent, gonflent
    et s'effacent. fenetres = [(debut, fin, opacité, taille)] : une bouffée n'est émise que si elle naît dans une
    fenêtre ; hors fenêtre plus rien ne sort, les dernières finissent de monter (la vapeur « s'arrête », sans effet).
    Rien qui ressemble à un être : seulement des ronds. cx, y0 en pixels d'écran ; haut, r0, r1, ecart en pixels px."""
    W, H = im.width // px + 1, im.height // px + 1
    bouffees = []
    for j in range(n):
        for i in range(3):
            dec = 3 + i * PERIODE_V / 3 + j * 0.37
            v = ((u + dec) % PERIODE_V) / PERIODE_V
            nee = u - v * PERIODE_V
            f_ = next(((a_, k_) for (t0, t1, a_, k_) in fenetres if t0 <= nee < t1), None)
            if f_ is None:
                continue
            a_, k_ = f_
            al = a_ * smooth(v / 0.15) * (1 - smooth((v - 0.5) / 0.5))
            if al < 0.02:
                continue
            x = cx / px + (j - (n - 1) / 2) * ecart * k_ * (1 + 0.5 * v) + 1.4 * math.sin(u * 2.1 + j * 2.0 + i)
            y = y0 / px - 1 - haut * k_ * v
            r = (r0 + (r1 - r0) * v) * k_
            bouffees.append((v, x, y, r, al))
    if not bouffees:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for (v, x, y, r, al) in sorted(bouffees, key=lambda b_: -b_[0]):              # les plus vieilles d'abord
        A = int(205 * al)
        ronds = ((x, y - 0.2 * r, r), (x - 0.62 * r, y + 0.3 * r, 0.64 * r), (x + 0.6 * r, y + 0.34 * r, 0.6 * r))
        for (cx_, cy_, rr) in ronds:                                                # un petit nuage : un seul contour
            d.ellipse([cx_ - rr - 1, cy_ - rr * 0.86 - 1, cx_ + rr + 1, cy_ + rr * 0.86 + 1], fill=(*VAPEUR_OL, A))
        for (cx_, cy_, rr) in ronds:
            d.ellipse([cx_ - rr, cy_ - rr * 0.86, cx_ + rr, cy_ + rr * 0.86], fill=(*VAPEUR, A))
    im.alpha_composite(lay.resize((W * px, H * px), Image.NEAREST).crop((0, 0, im.width, im.height)))


def _chiffre(c, txt, x, y, col):
    """Petits chiffres 3 x 5 (le score à l'écran) ; « - » = un tiret."""
    for ch in txt:
        if ch == "-":
            c.fill(c.mask_rect(x, y + 2, x + 2, y + 3), col)
            x += 3
            continue
        for j, ligne in enumerate(cast.DIGITS.get(ch, [])):
            for i, v in enumerate(ligne):
                if v == "x":
                    c.px(x + i, y + j, col)
        x += 4


# ---------------------------------------------------------------- {enerve PETIT} {colere …}
class Colere(_Base):
    """{enerve PETIT} : accroche, Petit tout rouge crie devant la télé « PERDU », la manette serrée au premier plan,
    la vapeur sur la tête. {colere} : la jauge « COLÈRE » pleine et Petit énervé ; {colere refuge} la formule (voyelles
    longues), la jauge descend pendant qu'il la dit ; {colere fort} « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : » puis
    « LE FORT : CELUI QUI // SE MAÎTRISE DANS LA COLÈRE » ; {colere gg} « GG EZ » : la jauge remonte un peu, il se
    calme, « A'OÛDHOU BILLÂH », elle redescend ; Petit sourit et fait un pouce."""
    ETAPES = ("refuge", "fort", "gg")
    KB = 16                        # accroche : échelle du buste
    KM = 16                        # accroche : échelle de la manette au premier plan
    BX, BBAS = 330, 990            # accroche : milieu du buste, bas du buste (sous le cadre)
    T_PERDU = -0.45                # accroche : l'écran passe à « PERDU » juste avant le mot
    KP = 9                         # jauge : échelle de Petit en entier
    PX_, PIEDS = 772, 950          # jauge : milieu de Petit, ses pieds
    JX, JY = 40, 368               # jauge : coin haut gauche de la jauge (pixels d'écran)
    JW, JH = 50, 98                # jauge : taille du dessin de la jauge (pixels du dessin, x6)
    YN0, YN1 = 76, 6               # jauge : haut du liquide à 0 % et à 100 % (pixels du dessin)

    def __init__(s, cmd, mode="jauge", who="PETIT"):
        super().__init__(cmd)
        s.mode = "enerve" if _norm(str(mode)) in ("enerve", "accroche") else "jauge"
        s.who = who if who in cast.CAST else "PETIT"
        s.negatif = s.mode == "enerve"

    def sons_el(s):
        if s.mode == "enerve":
            return []
        out = []
        for nom, dec, son, g in (("refuge", 0.1, "tr_whoosh_doux", 0.02), ("fort", 0.0, "sa_ting", 0.03),
                                 ("gg", 0.0, "dv_notifications", 0.03)):
            if nom in s.t:
                out.append((s.t[nom] + dec, son, g, None))
        return out

    # ============================================================ l'accroche
    def _chambre(s, perdu):
        """La chambre le soir (bande LED, fenêtre sur la ville, poster), la télé (un match de foot ; perdu : l'écran
        s'assombrit, « PERDU » en rouge) au-dessus du meuble et de la console."""
        cle = ("ch", perdu)
        if cle in s._cache:
            return s._cache[cle]
        W, H = 170, 160
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        mur = c.mask_rect(0, 0, W, 110) & tout_
        c.vgrad(mur, 0, 110, (32, 26, 60), (62, 48, 98), steps=6)
        for x in range(W):                                                         # la bande LED du plafond
            col_ = _mel((255, 70, 200), (70, 220, 255), x / (W - 1))
            c.px(x, 3, col_)
            c.px(x, 4, col_)
        c.glow(85, 4, 120, (180, 100, 255), 0.14, m=mur)
        c.glow(131, 44, 74, (255, 76, 66) if perdu else (90, 220, 150), 0.2, m=mur)   # la lueur de la télé
        fen = c.mask_rect(6, 12, 46, 56)                                          # la fenêtre : la ville la nuit
        c.vgrad(fen, 12, 56, (14, 18, 46), (48, 42, 100), steps=5)
        for (x, y) in ((10, 16), (20, 22), (31, 14), (42, 27), (13, 30), (29, 31), (40, 17)):
            c.px(x, y, (240, 240, 255))
        c.fill(c.mask_ell(37, 21, 4, 4) & ~c.mask_ell(35, 20, 3.4, 3.4), (250, 236, 170))
        rng = np.random.default_rng(7)
        x = 6
        while x < 46:
            w = int(rng.integers(5, 10))
            h = int(rng.integers(9, 21))
            bat = c.mask_rect(x, 56 - h, min(46, x + w), 56)
            c.fill(bat, (24, 20, 48) if (x // 5) % 2 else (30, 26, 58))
            for wy in range(56 - h + 2, 54, 3):
                for wx in range(x + 1, min(46, x + w) - 1, 2):
                    if rng.random() < 0.35:
                        c.px(wx, wy, (250, 214, 110))
            x += w
        c.fill((c.mask_rect(25, 12, 27, 56) | c.mask_rect(6, 33, 46, 35)) & fen, (34, 30, 58))
        c.outline(fen, (18, 14, 30))
        c.shape(c.mask_rect(3, 56, 49, 60), (88, 76, 112), shade=(60, 52, 82), band=1, olcol=OL)
        po = c.mask_rect(56, 12, 84, 46)                                          # le poster (une planète)
        c.fill(po, (26, 32, 78))
        for (x, y) in ((60, 16), (79, 20), (62, 40), (77, 41), (70, 15)):
            c.px(x, y, (230, 230, 255))
        pl = c.mask_ell(70, 29, 8, 8)
        c.shape(pl, (240, 150, 64), shade=(196, 104, 44), light=(255, 200, 120), band=2, olcol=OL)
        c.fill(c.mask_rect(62, 26, 78, 27) & pl, (214, 120, 52))
        anneau = (c.mask_ell(70, 30, 14, 3.2) & ~c.mask_ell(70, 30, 11, 1.8)) & ~(pl & c.mask_rect(0, 0, W, 30))
        c.fill(anneau, (250, 222, 150))
        c.outline(po, OL)
        tv = c.mask_rrect(94, 20, 169, 68, 2)                                     # la télé
        c.shape(tv, (26, 24, 32), shade=(14, 12, 18), light=(62, 60, 76), band=1, olcol=OL)
        ecr = c.mask_rect(97, 23, 166, 64)
        for i, x in enumerate(range(97, 166, 7)):                                 # le terrain de foot
            c.fill(ecr & c.mask_rect(x, 23, x + 7, 64), (62, 150, 72) if i % 2 == 0 else (52, 134, 62))
        bl = (230, 240, 230)
        lignes = (c.mask_rect(99, 27, 164, 28) | c.mask_rect(99, 61, 164, 62) | c.mask_rect(99, 27, 100, 62) |
                  c.mask_rect(163, 27, 164, 62) | c.mask_rect(131, 27, 132, 62))
        lignes |= c.mask_ell(131.5, 44.5, 6, 6) & ~c.mask_ell(131.5, 44.5, 5, 5)
        lignes |= (c.mask_rect(99, 38, 106, 51) & ~c.mask_rect(99, 39, 105, 50)) | \
                  (c.mask_rect(157, 38, 164, 51) & ~c.mask_rect(158, 39, 164, 50))
        c.fill(lignes & ecr, bl)
        for (x, y, eq) in ((112, 34, 0), (121, 49, 0), (139, 40, 0), (149, 33, 0), (108, 45, 1), (126, 39, 1),
                           (144, 52, 1), (155, 44, 1)):
            c.fill(c.mask_rect(x, y + 1, x + 2, y + 4), (232, 66, 60) if eq == 0 else (66, 118, 236))
            c.px(x, y, (224, 166, 124))
            c.px(x + 1, y, (224, 166, 124))
        c.fill(c.mask_rect(151, 43, 153, 45), (252, 252, 252))                     # le ballon
        c.fill(c.mask_rect(98, 24, 112, 32), (16, 16, 24))                         # le score
        _chiffre(c, "1-2", 100, 26, (250, 250, 250))
        if perdu:                                                                  # « PERDU »
            c.tint(ecr, (26, 6, 14), 0.62)
            c.fill(c.mask_rect(97, 37, 166, 52), (60, 10, 20))
            m = c.text((131.5, 44.5), "PERDU", (240, 58, 52), size=16, font=TAHOMA, anchor="mm", ol=(26, 6, 12))
            c.fill(m & ~np.roll(m, 1, axis=0), (255, 150, 140))
        c.fill(c.mask_rect(130, 65, 133, 66), (220, 60, 60) if perdu else (80, 200, 255))   # le voyant
        meuble = c.mask_rect(92, 88, 170, 110) & tout_                            # le meuble télé
        c.shape(meuble, (96, 66, 52), shade=(70, 46, 38), light=(128, 92, 70), band=1, olcol=OL)
        for x0 in (98, 134):
            tiroir = c.mask_rect(x0, 94, x0 + 30, 106)
            c.outline(tiroir, (62, 40, 32))
            c.fill(c.mask_rect(x0 + 13, 99, x0 + 17, 100), (200, 176, 140))
        cons = c.mask_rrect(104, 80, 131, 88, 1)                                  # la console
        c.shape(cons, (34, 34, 44), shade=(20, 20, 28), light=(78, 78, 94), band=1, olcol=OL)
        c.fill(c.mask_rect(108, 84, 126, 85), (80, 170, 255))
        c.px(128, 86, (140, 236, 255))
        jeu = c.mask_rect(135, 81, 141, 88)                                        # une boîte de jeu
        c.shape(jeu, (60, 110, 210), shade=(40, 80, 160), band=1, olcol=OL)
        c.fill(c.mask_rect(136, 83, 140, 85), (240, 240, 250))
        sol = c.mask_rect(0, 110, W, H) & tout_                                   # le sol : lames en perspective
        c.vgrad(sol, 110, H, (52, 40, 60), (84, 64, 78), steps=5)
        for xb in range(-150, W + 160, 26):                                        # les joints filent vers le fond
            c.line(85 + (xb - 85) * 0.32, 111, xb, H - 1, (40, 30, 46))
        for y in (114, 121, 132, 147):                                             # quelques bouts de lames
            for x in range((y * 7) % 52, W, 52):
                c.fill(c.mask_rect(x, y, x + 9, y + 1) & sol, (44, 34, 50))
        c.fill(c.mask_rect(0, 108, W, 110) & tout_, (82, 66, 98))                 # la plinthe
        s._cache[cle] = c.img(s.K, rgba=True)
        return s._cache[cle]

    def _lueur_tv(s):
        """Halo rouge doux autour de l'écran « PERDU » (il respire lentement)."""
        if "lueur" not in s._cache:
            K = s.K
            lay = Image.new("RGBA", (int(100 * K), int(72 * K)), (0, 0, 0, 0))
            ImageDraw.Draw(lay).rounded_rectangle([14 * K, 14 * K, 86 * K, 58 * K], 30, fill=(255, 60, 50, 130))
            lay = lay.filter(ImageFilter.GaussianBlur(26))
            a = np.array(lay)
            a[12 * K:60 * K + 1, 13 * K:88 * K + 1, 3] = 0                          # rien sur la télé : autour seulement
            s._cache["lueur"] = Image.fromarray(a, "RGBA")
        return s._cache["lueur"]

    def _buste0(s):
        """Petit, tête et poitrine (les mains jointes devant lui, cachées par la manette), qui crie, tout rouge, avec
        un liseré rouge du côté de la télé ; petit dessin (pixels du sprite)."""
        if "b0" not in s._cache:
            g = cast.geo(cast.CAST[s.who])
            a = np.array(_sprite(s.who, "priere", "cri", blush=True))
            n = np.array(_sprite(s.who, "neutre", "cri", blush=True))
            y_ = g.top + 7                              # le ventre sans les mains jointes (on le voit entre les poignées)
            a[y_:y_ + 14, 18:30] = n[y_:y_ + 14, 18:30]
            a = _rougit(a, _peau(s.who), 0.55)
            m = a[..., 3] > 0
            bord = m & ~np.roll(m, -1, axis=1)                                     # le contour à droite
            rim = m & ~np.roll(m, -2, axis=1) & ~bord                             # juste à l'intérieur
            a[rim, :3] = (a[rim, :3].astype(float) * 0.5 + np.array((255, 96, 84)) * 0.5).astype(np.uint8)
            haut = int(np.where(m.any(axis=1))[0][0])                              # le haut de la casquette
            a = a[haut:g.top + 20]                                                 # tête et poitrine
            cols = np.where(a[..., 3].max(axis=0) > 0)[0]
            a = a[:, cols[0]:cols[-1] + 1]
            s._cache["b0"] = (Image.fromarray(a, "RGBA"), int(cols[0]))
        return s._cache["b0"]

    def _buste(s, z):
        z = round(z / 0.004) * 0.004
        cle = ("bz", round(z, 3))
        if cle not in s._cache:
            b0, _ = s._buste0()
            k = s.KB * z
            s._cache[cle] = b0.resize((int(round(b0.width * k)), int(round(b0.height * k))), Image.NEAREST)
        return s._cache[cle]

    def _manette_mains(s):
        """Au premier plan : la manette (comme l'icône, en plus grand) serrée dans ses deux poings, les pouces dessus."""
        if "mm" in s._cache:
            return s._cache["mm"]
        p = {k_: _mel(v, ROUGEUR.get(k_, v), 0.55) for k_, v in _peau(s.who).items()}   # rouges, comme son visage
        sw = cast.tons(cast.CAST[s.who]["couleur"])
        W, H = 32, 19

        def miroir(pts):
            return [(W - x, y) for (x, y) in pts]
        c = Px(W, H, alpha=True)
        for x0 in (2, 21):                                                         # les poignets (manches du sweat)
            m = c.mask_rrect(x0, 16, x0 + 9, 24, 2)
            c.shape(m, sw["b"], shade=sw["s"], light=sw["h"], band=1, olcol=OL)
            c.fill(m & c.mask_rect(0, 16, W, 18), sw["s"])
        corps = c.mask_rrect(8, 3, 24, 11, 3)
        poig = (c.mask_poly([(8, 6), (13, 9), (11, 15), (7, 16.5), (5, 15), (6, 9)]) |
                c.mask_poly([(24, 6), (19, 9), (21, 15), (25, 16.5), (27, 15), (26, 9)]))
        c.shape(corps | poig, (50, 50, 62), shade=(30, 30, 40), light=(92, 92, 112), band=1, olcol=OL)
        c.fill(c.mask_rect(9, 6, 12, 7) | c.mask_rect(10, 5, 11, 8), (160, 166, 182))   # la croix
        c.px(10, 6, (120, 126, 142))
        for (bx, by), col_ in zip(((20, 3), (18, 5), (22, 5), (20, 7)), BOUTONS):  # les 4 boutons
            c.fill(c.mask_rect(bx, by, bx + 2, by + 2), col_)
            c.px(bx, by, _mel(col_, (255, 255, 255), 0.5))
        for sx in (13.5, 18.5):                                                    # les deux sticks
            st = c.mask_ell(sx, 9.5, 1.5, 1.5)
            c.fill(st, (88, 88, 104))
            c.px(int(sx) - 1, 8, (140, 140, 160))
        c.fill(c.mask_rect(15, 5, 17, 6), (120, 210, 255))                         # le voyant
        for gauche in (True, False):                                               # les poings serrés sur les poignées
            poing = c.mask_rrect(3, 11, 11, 18, 2) if gauche else c.mask_rrect(W - 11, 11, W - 3, 18, 2)
            c.shape(poing, p["b"], shade=p["s"], light=p["h"], band=1, sdir="right" if gauche else "left",
                    ldir="left" if gauche else "right", olcol=OL)
            for y in (13, 15):                                                     # les doigts repliés
                c.fill((c.mask_rect(3, y, 9, y + 1) if gauche else c.mask_rect(W - 9, y, W - 3, y + 1)) & poing, p["s"])
            for y in (12, 14, 16):                                                 # les jointures
                c.px(4 if gauche else W - 5, y, p["h"])
            pts = [(8.5, 12.5), (8.5, 10), (10.5, 8.2), (12.8, 8.4), (12.6, 10), (10.5, 11.5), (10, 13)]
            pouce = c.mask_poly(pts if gauche else miroir(pts))                    # le pouce, appuyé dessus
            c.shape(pouce, p["b"], shade=p["s"], light=p["h"], band=1, olcol=OL)
            c.px(11 if gauche else W - 12, 9, p["h"])                             # l'ongle
        s._cache["mm"] = c.img(s.KM, rgba=True)
        return s._cache["mm"]

    def _image_enerve(s, u):
        if u < s.T_PERDU + 0.35:
            im = s._chambre(False).copy()
            a = smooth((u - s.T_PERDU) / 0.35)
            if a > 0:                                                              # fondu, seulement là où ça change
                if "zp" not in s._cache:
                    ys, xs = np.where(np.any(np.array(s._chambre(False)) != np.array(s._chambre(True)), axis=-1))
                    s._cache["zp"] = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
                bb = s._cache["zp"]
                im.alpha_composite(_fade(s._chambre(True).crop(bb), a), bb[:2])
        else:
            im = s._chambre(True).copy()
        W_, H_ = im.size
        K = s.K
        a_l = smooth((u - s.T_PERDU) / 0.4) * (0.75 + 0.25 * math.sin(2 * math.pi * u / 1.8))
        if a_l > 0.01:
            lu = s._lueur_tv()
            im.alpha_composite(_fade(lu, a_l), (int(81 * K), int(8 * K)))
        # il respire fort (1,00 → 1,02) et se penche doucement vers toi
        resp = 0.5 - 0.5 * math.cos(2 * math.pi * (u + 0.5) / 1.4)
        z_app = 1.0 + 0.06 * smooth((u + 0.5) / 3.5)
        z = z_app * (1.0 + 0.02 * resp)
        bu = s._buste(z)
        bx, by = int(s.BX - bu.width / 2), int(s.BBAS - bu.height)
        b0, col0 = s._buste0()
        k_ = bu.width / b0.width
        tete_x = bx + (21.5 - col0) * k_                                           # le milieu de sa casquette
        _vapeur(im, tete_x, by + 3 * k_, u, [(-1e9, 1e9, 1.0, 1.0)], px=8)
        im.alpha_composite(bu, (bx, by))
        mm = s._manette_mains()
        z_app = round(z_app / 0.004) * 0.004
        cle = ("mmz", round(z_app, 3))
        if cle not in s._cache:
            s._cache[cle] = mm.resize((int(mm.width * z_app), int(mm.height * z_app)), Image.NEAREST)
        m2 = s._cache[cle]
        my = H_ - 6 - m2.height - 8 * resp                                         # elle monte avec sa poitrine
        im.alpha_composite(m2, (int(s.BX - m2.width / 2), int(my)))
        return im

    # ============================================================ la jauge
    def _niveau(s, u):
        """La colère (0 → 1) : pleine ; {refuge} 100 → 25 % en 2,2 s ; {gg} 25 → 45 % puis → 10 %."""
        n = 1.0
        if "refuge" in s.t:
            n -= 0.75 * smooth((u - s.t["refuge"] - 0.1) / 2.2)
        if "gg" in s.t:
            v = u - s.t["gg"]
            n = min(1.0, n + 0.20 * smooth((v - 0.1) / 0.9)) - 0.35 * smooth((v - 1.2) / 1.3)
        return max(0.04, min(1.0, n))

    def _jauge_fixe(s):
        """Le thermomètre de la colère (sans le liquide) : tube, boule, graduations, zones teintées."""
        if "jf" in s._cache:
            return s._cache["jf"]
        c = Px(s.JW, s.JH, alpha=True)
        tube = c.mask_rrect(18, 2, 34, 79, 8) | c.mask_ell(26, 85, 12, 12)
        c.shape(tube, (234, 240, 250), shade=(184, 196, 218), light=(255, 255, 255), band=2, olcol=OL)
        canal = s._canal(c)
        for (y0, y1, col_) in ((0, 29, (240, 206, 210)), (29, 52, (244, 226, 200)), (52, s.JH, (212, 236, 216))):
            c.fill(canal & c.mask_rect(0, y0, s.JW, y1), col_)
        for i in range(11):                                       # graduations, couleur de leur zone (vert → rouge)
            y = int(round(s.YN0 - i * (s.YN0 - s.YN1) / 10))
            tick = c.mask_rect(37, y - 1, 44 if i % 5 == 0 else 42, y + 1)
            c.shape(tick, LIQ["vert"] if y >= 52 else (LIQ["orange"] if y >= 29 else LIQ["rouge"]), olcol=OL)
        s._cache["jf"] = c.img(s.K, rgba=True)
        return s._cache["jf"]

    def _canal(s, c):
        return c.mask_rrect(22, 6, 30, 82, 4) | c.mask_ell(26, 85, 8, 8)

    def _liquide(s):
        """Le liquide plein (100 %) : vert en bas, orange, rouge en haut (paliers tramés) ; + couleur de chaque rangée."""
        if "liq" in s._cache:
            return s._cache["liq"]
        c = Px(s.JW, s.JH, alpha=True)
        canal = s._canal(c)
        R, O, V = LIQ["rouge"], LIQ["orange"], LIQ["vert"]
        c.fill(canal, V)
        c.fill(canal & c.mask_rect(0, 0, s.JW, 50), O)
        c.vgrad(canal & c.mask_rect(0, 48, s.JW, 55), 48, 55, O, V, steps=4)
        c.fill(canal & c.mask_rect(0, 0, s.JW, 27), R)
        c.vgrad(canal & c.mask_rect(0, 25, s.JW, 32), 25, 32, R, O, steps=4)
        c.tint(canal & c.mask_rect(23, 0, 25, s.JH), (255, 255, 255), 0.35)          # reflet
        c.tint(canal & c.mask_rect(28, 0, 30, s.JH), (0, 0, 0), 0.16)                # ombre
        rang = {}
        for y in range(s.JH):                                                       # couleur et largeur de chaque rangée
            xs = np.where(canal[y])[0]
            if len(xs):
                rang[y] = (tuple(int(v) for v in c.a[y, 26]), int(xs[0]), int(xs[-1]))
        s._cache["liq"] = (c.img(s.K, rgba=True), rang)
        return s._cache["liq"]

    def _petit(s, face, rouge, blush, pose, pose_de=None, mix=0.0):
        """Petit en entier, tourné vers la jauge (retourné), la manette à la main, agrandi xKP."""
        mix = round(mix, 1)
        rouge = round(rouge, 1)
        cle = ("p", face, rouge, blush, pose, pose_de if mix > 0 else None, mix)
        if cle not in s._cache:
            kw = dict(objet="manette", blush=blush)
            if pose_de and mix > 0:
                kw.update(pose_de=pose_de, mix=mix)
            a = np.array(_sprite(s.who, pose, face, **kw))
            a = _rougit(a, _peau(s.who), rouge)
            s._cache[cle] = _grand(Image.fromarray(a, "RGBA").transpose(Image.FLIP_LEFT_RIGHT), s.KP)
        return s._cache[cle]

    def _visages(s):
        """Les visages successifs : (instant, visage, rouge, joues)."""
        ev = [(-1e9, "enerve", 1.0, True)]
        if "refuge" in s.t:
            tr = s.t["refuge"]
            ev += [(tr + 0.55, "blase", 0.45, True), (tr + 1.5, "neutre", 0.0, False)]
        if "fort" in s.t:
            ev.append((s.t["fort"] + 0.1, "content", 0.0, False))
        if "gg" in s.t:
            tg = s.t["gg"]
            # « GG EZ » l'agace ; il se calme (visage calme, pas malin) quand la bulle de la formule arrive ; il sourit
            # avec le pouce
            ev += [(tg + 0.2, "blase", 0.35, True), (tg + 1.1, "neutre", 0.0, False), (tg + 2.1, "content", 0.0, False)]
        return sorted(ev, key=lambda e_: e_[0])

    def _image_jauge(s, u):
        W_, H_ = 1020, 960
        K = s.K
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        tr, tf, tg = s.t.get("refuge"), s.t.get("fort"), s.t.get("gg")
        # -- la jauge « COLÈRE »
        im.alpha_composite(s._jauge_fixe(), (s.JX, s.JY))
        liq, rang = s._liquide()
        niv = s._niveau(u)
        y_n = int(round(s.YN0 - niv * (s.YN0 - s.YN1)))
        part = liq.crop((0, y_n * K, liq.width, liq.height))
        im.alpha_composite(part, (s.JX, s.JY + y_n * K))
        d = ImageDraw.Draw(im)
        if y_n in rang:                                                            # la surface du liquide (plus claire)
            col_, x0_, x1_ = rang[y_n]
            col_ = _mel(col_, (255, 255, 255), 0.45)
            d.rectangle([s.JX + x0_ * K, s.JY + y_n * K, s.JX + (x1_ + 1) * K - 1, s.JY + y_n * K + K - 1],
                        fill=(*col_, 255))
        lab = s._cache.setdefault("lab_col", _encre(_titre("COLÈRE", ROUGE, 54)))
        s._pose(im, lab, s.JX + 26 * K, s.JY - lab.height / 2 - 4, 1.0)
        # -- Petit : visage, pose (la manette à la main ; {gg} : un pouce, la manette le long du corps)
        ev = s._visages()
        i_c = max(i for i, e_ in enumerate(ev) if e_[0] <= u)
        e_f = smooth((u - ev[i_c][0]) / 0.3) if i_c > 0 else 1.0
        pose, pose_de, mix = "tient", None, 0.0
        if tg is not None and u >= tg + 2.0:
            pose, pose_de, mix = "pouce", "tient", 1 - smooth((u - tg - 2.0) / 0.45)
        sx0 = s.PX_ - 23 * s.KP
        sy0 = s.PIEDS - 93 * s.KP
        if "haut" not in s._cache:                                                 # le haut de sa casquette (rangée)
            a_ = np.array(_sprite(s.who, "tient", "neutre", objet="manette"))
            s._cache["haut"] = int(np.where(a_[..., 3].max(axis=1) > 0)[0][0])
        y_tete = sy0 + s._cache["haut"] * s.KP
        ombre = [s.PX_ - 120, s.PIEDS - 12, s.PX_ + 120, s.PIEDS + 12]
        _translucide(im, lambda dd: dd.ellipse(ombre, fill=(10, 8, 20, 90)))
        # la vapeur sur sa tête : plus rien ne sort quand il dit la formule (les dernières bouffées finissent de
        # monter) ; un peu au « GG EZ », puis plus rien
        fen = [(-1e9, tr + 0.25 if tr is not None else 1e9,
                1.0 - (smooth((u - tr - 0.5) / 0.8) if tr is not None else 0.0), 1.0)]
        if tg is not None:
            fen.append((tg + 0.2, tg + 0.8, 0.85 * (1 - smooth((u - tg - 0.95) / 0.5)), 0.75))
        _vapeur(im, sx0 + (46 - 21.5) * s.KP, y_tete + s.KP, u, fen, px=6, n=3, haut=24, r0=2.0, r1=4.6, ecart=8.0)
        # -- {fort} le trophée et son halo, DERRIÈRE Petit (au pouce de {gg}, sa main passe dans le halo : elle reste
        # nette)
        if tf is not None:
            ef = s._e("fort", u, 0.45)
            if ef > 0:
                tro = s._cache.get("tro")
                if tro is None:
                    tro = s._cache["tro"] = autocollant(objets.icone("trophee").img(12), r=5)
                    lay = Image.new("RGBA", (tro.width + 160, tro.height + 160), (0, 0, 0, 0))
                    ImageDraw.Draw(lay).ellipse([40, 40, lay.width - 40, lay.height - 40], fill=(255, 214, 90, 110))
                    s._cache["halo"] = lay.filter(ImageFilter.GaussianBlur(30))
                halo = s._cache["halo"]
                tx, ty = 470, 610 + 8 * math.sin(2 * math.pi * (u - tf) / 2.6)
                im.alpha_composite(_fade(halo, ef), (int(tx - halo.width / 2), int(ty - halo.height / 2)))
                k2 = 0.86 + 0.14 * ef
                cle = ("tro_k", round(k2, 2))
                if cle not in s._cache:
                    s._cache[cle] = tro.resize((int(tro.width * k2), int(tro.height * k2)), Image.LANCZOS)
                t2 = s._cache[cle]
                im.alpha_composite(_fade(t2, ef), (int(tx - t2.width / 2), int(ty - t2.height / 2)))
        for j, i_ in enumerate((i_c - 1, i_c) if e_f < 1 else (i_c,)):
            _, face, rouge, joues = ev[i_]
            sp = s._petit(face, rouge, joues, pose, pose_de, mix)
            im.alpha_composite(sp if (j == 0 or e_f >= 1) else _fade(sp, e_f), (sx0, sy0))
        # -- {refuge} la formule (voyelles longues) et sa traduction, en haut. Les accents grandissent la formule :
        # lignes empilées sur les capitales, bloc collé en haut (y = 2) et traduction serrée dessous (-4), pour que
        # le bas de la traduction reste à ≈ 12 px au-dessus de l'étiquette « COLÈRE »
        if tr is not None:
            a1 = s._a("refuge", u, 0.35, fin=("fort", "gg"))
            a2 = s._a("refuge", u, 0.35, fin=("fort", "gg"), dec=0.4)
            f1 = s._cache.get("formule")
            if f1 is None:
                f1 = s._cache["formule"] = _lignes([("A'OÛDHOU BILLÂHI", OR_, 60),
                                                    ("MINA CH-CHAYTÂNI R-RAJÎM", OR_, 60)])
                s._cache["trad"] = _pile([_titre("JE DEMANDE LA PROTECTION D'ALLAH", BLANC, 44),
                                          _titre("CONTRE LE DIABLE BANNI", BLANC, 44)])
            f2 = s._cache["trad"]
            y1 = 2 + f1.height / 2
            s._pose(im, f1, W_ / 2, y1 + 14 * (1 - smooth((u - tr) / 0.35)), a1)
            s._pose(im, f2, W_ / 2, 2 + f1.height - 4 + f2.height / 2 + 12 * (1 - smooth((u - tr - 0.4) / 0.35)), a2)
        # -- {fort} « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : » puis « LE FORT : CELUI QUI // SE MAÎTRISE DANS LA
        # COLÈRE » (le trophée est dessiné plus haut, derrière Petit)
        if tf is not None:
            at = s._a("fort", u, 0.35, fin="gg", dec=0.25)                         # une fois la formule partie
            if at > 0:
                lf = s._cache.get("lefort")
                if lf is None:                              # qui parle (en petit), puis la parole (Boukhari 6114)
                    lf = s._cache["lefort"] = _lignes([("LE PROPHÈTE (PAIX ET SALUT SUR LUI) :", BLANC, 44),
                                                       ("LE FORT : CELUI QUI", OR_, 68),
                                                       ("SE MAÎTRISE DANS LA COLÈRE", OR_, 62)])
                s._pose(im, lf, W_ / 2, 12 + lf.height / 2 + 14 * (1 - smooth((u - tf - 0.25) / 0.35)), at)
        # -- {gg} la notification « GG EZ », puis « A'OÛDHOU BILLÂH »
        if tg is not None:
            v = u - tg
            if v >= 0:
                no = s._notif()
                e_n = smooth(v / 0.45)
                im.alpha_composite(_fade(no, smooth(v / 0.25)), (int(W_ / 2 - no.width / 2),
                                                                  int(-no.height + (no.height + 12) * e_n)))
            ab = s._e("gg", u, 0.35, dec=1.05)
            if ab > 0:
                b = s._cache.get("bulle_gg")
                if b is None:
                    b = s._cache["bulle_gg"] = _bulle([("A'OÛDHOU BILLÂH", OR_)], fond=(40, 60, 120), size=46, queue=0.8)
                bx = int(s.PX_ - 22 - b.width * 0.8)
                im.alpha_composite(_fade(b, ab), (bx, int(y_tete - 8 - b.height + 12 * (1 - ab))))
        return im

    def _notif(s):
        """La notification grise « GG EZ » (l'appli de jeu)."""
        if "notif" in s._cache:
            return s._cache["notif"]
        tx = _encre(pxv.big_title([("GG EZ", BLANC)], size=74))
        ic = objets.icone("manette").img(5)
        app = Image.new("RGBA", (ic.width + 24, ic.height + 24), (0, 0, 0, 0))
        ImageDraw.Draw(app).rounded_rectangle([0, 0, app.width - 1, app.height - 1], 24, fill=(36, 36, 48, 255),
                                              outline=(255, 255, 255, 255), width=4)
        app.alpha_composite(ic, (12, 12))
        pad = 22
        Wn = pad + app.width + 28 + tx.width + pad + 8
        Hn = max(app.height, tx.height) + 2 * pad
        b = Image.new("RGBA", (Wn + 14, Hn + 16), (0, 0, 0, 0))
        sh = Image.new("RGBA", b.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([10, 14, Wn + 8, Hn + 12], 36, fill=(8, 8, 16, 120))
        b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
        ImageDraw.Draw(b).rounded_rectangle([0, 0, Wn - 1, Hn - 1], 36, fill=(128, 132, 148, 250),
                                            outline=(255, 255, 255, 255), width=6)
        b.alpha_composite(app, (pad, (Hn - app.height) // 2))
        b.alpha_composite(tx, (pad + app.width + 28, (Hn - tx.height) // 2))
        s._cache["notif"] = b
        return b

    def image(s, u):
        return s._image_enerve(u) if s.mode == "enerve" else s._image_jauge(u)


# ---------------------------------------------------------------- branchement dans explique.Schema
CLES = ("enerve", "colere", "colère")


def ordre(schema, t, brut, mots, reste):
    """Appelé (via explique_0611.ordre) par explique.Schema._ordre pour les clés de CLES. Renvoie True si l'ordre a
    été pris en compte. {enerve PETIT} : l'accroche ; {colere} : la jauge ; {colere refuge|fort|gg} : une étape de la
    dernière jauge visible (créée si besoin)."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    qui = mots[1].upper() if len(mots) > 1 else "PETIT"

    def dernier(cls, mode=None):
        return next((it["el"] for it in reversed(schema._visibles(t + 0.01))
                     if isinstance(it["el"], cls) and (mode is None or getattr(it["el"], "mode", None) == mode)), None)

    def u_de(el):
        return t - next(it["t_in"] for it in schema.items if it["el"] is el)

    def etape(cls, nom, mode=None, nouveau=None):
        el = dernier(cls, mode)
        if el is None:
            el = nouveau() if nouveau else cls(brut)
            schema._ajoute(t, el)
        el.t[nom] = u_de(el)

    if k == "enerve":
        schema._ajoute(t, Colere(brut, "enerve", qui if qui in ("PETIT", "GRAND") else "PETIT"))
    elif k == "colere":
        if sous in Colere.ETAPES:
            etape(Colere, sous, "jauge", lambda: Colere(brut, "jauge"))
        else:
            schema._ajoute(t, Colere(brut, "jauge"))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "enerve":
        return t + 1.4
    if k == "colere":
        return t + dict(refuge=2.5, fort=1.0, gg=2.8).get(sous, 0.8)
    return None
