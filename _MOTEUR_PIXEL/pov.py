# POV : plans en VUE SUBJECTIVE pour les Shorts « … tu fais quoi ? » (02/11/2026).
# Modèle : EXC 1 « Un serpent pendant ta prière… tu fais quoi ? », le Short qui a le mieux retenu sur TikTok : le
# spectateur est À LA PLACE de celui qui vit la scène (ses pieds sur le tapis), le sujet est en grand et bouge vers lui
# dès la 1re image, la question est posée en 3-4 s et la réponse arrive vers 5 s.
#
# DÉCORS (pixel 270x480, x4) : tapis_pov (tes pieds sur le tapis, un sac posé devant = la soutra), porte_pov (sur le
#   pas de ta porte la nuit), remise_nuit (remise sombre, poteau, gamelle vide), puits (désert, puits de pierre),
#   chevet_pov / chevet_pov_jour (vu depuis l'oreiller), nuque_nuit / nuque_jour (il dort, vu de dos),
#   chambre_aube (lever du soleil, tapis de prière déroulé : on peut y placer des persos).
# BALISES (dans une réplique, sur le mot ; jamais dites ni sous-titrées) : toujours {pov …}
#   tapis_pov   : {pov passant} quelqu'un arrive et s'arrête devant toi · {pov repousse} ta main le repousse ·
#                 {pov insiste} il revient · {pov repousse fort} · {pov demon} halo sombre · {pov contourne} il passe
#                 derrière le sac (la soutra) · {pov soutra} étiquette « TA SOUTRA »
#   porte_pov   : {pov chat} un chat maigre arrive sous la pluie et s'assoit devant toi · {pov miaou} ·
#                 {pov gamelle} ta main pose une gamelle pleine, il mange (cœurs)
#   remise_nuit : {pov chatte} la chatte attachée au poteau · {pov jours} les jours passent (traits au mur) ·
#                 {pov porte} la lumière sous la porte s'éteint · {pov enfer} l'image rougit
#   puits       : {pov chien} un chien assoiffé lèche le sable mouillé · {pov botte} une botte pleine d'eau, il boit ·
#                 {pov pardon} une lumière dorée descend sur lui
#   chevet_pov  : {pov reveil "05:47"} le téléphone sonne (FAJR) · {pov manque} « 3 alarmes manquées »
#   nuque_nuit  : {pov noeuds} trois nœuds sombres sur la nuque (« la nuit est longue… dors ») · {pov defait} le
#                 nœud suivant se défait · {pov dhikr} « الحمد لله » doré · {pov eau} gouttes d'ablutions ·
#                 {pov priere} lumière chaude · {pov oreille} ombre près de l'oreille (jour)
#   partout     : {pov label "TEXTE"} autocollant en haut · {pov} rien (garde le plan en vue subjective)
# Les {texte "…"} et {source "…"} d'un passage en vue subjective s'affichent aussi (scenario.py).
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import pxv, lieux, sets
from px import Px, OUT
from spr import Spr, INK
from pxv import Shot, smooth

K = 4                                                           # taille d'un pixel du décor à l'écran
SONS_POV = pxv.BASE + "/SHORTS TU FAIS QUOI/bruitages/"


def _son(nom):
    """Bruitage propre à ces Shorts (hors _BRUITAGES) s'il existe, sinon None."""
    for f in (nom + ".mp3", nom + "_1.mp3"):
        if os.path.exists(SONS_POV + f):
            return SONS_POV + f
    return None


# =================================================================== DÉCORS
def _diamants(c, m, c1, c2, pas=40):
    for y in range(-pas, c.h + pas, pas):
        for x in range(-pas, c.w + pas, pas):
            ox = pas // 2 if (y // pas) % 2 else 0
            pm = c.mask_poly([(x + ox, y), (x + ox + pas / 2, y + pas / 2), (x + ox, y + pas), (x + ox - pas / 2, y + pas / 2)])
            c.fill(pm & m, c1 if ((x + y) // pas) % 2 else c2)


def _mes_pieds(c, y, chaussons=False):
    """Tes deux pieds vus d'en haut (orteils vers le haut) et ton jean qui vient vers toi jusqu'en bas de l'image."""
    for fx in (104, 166):
        jean = c.mask_poly([(fx - 18, y + 28), (fx + 18, y + 28), (fx + 36, 480), (fx - 36, 480)])
        c.shape(jean, (48, 66, 112), (34, 48, 84), (66, 88, 142), band=2)
        if chaussons:
            p = c.mask_ell(fx, y, 16, 28) | c.mask_rect(fx - 16, y, fx + 16, y + 30)
            c.shape(p, (150, 56, 64), (112, 38, 46), (182, 80, 86), band=2)
            c.fill(c.mask_ell(fx, y - 12, 11, 10), (172, 72, 80))
            c.fill(c.mask_rect(fx - 13, y + 2, fx + 13, y + 5), (120, 42, 50))
        else:
            p = c.mask_ell(fx, y, 14, 26) | c.mask_rect(fx - 14, y, fx + 14, y + 30)
            c.shape(p, (92, 94, 110), (68, 70, 86), (116, 118, 134), band=2)
            for dx in (-9, -3, 3, 9):
                c.fill(c.mask_ell(fx + dx, y - 22 + abs(dx) * 0.4, 3.2, 3.6), (104, 106, 122))
        ourlet = c.mask_rect(fx - 20, y + 26, fx + 20, y + 33)
        c.shape(ourlet, (58, 78, 126), (40, 56, 96), band=1)


def tapis_pov(heure="soir"):
    """Vue subjective : debout sur ton tapis de prière, tu regardes tes pieds ; un sac posé devant (la soutra)."""
    c = Px()
    tout = c.mask_rect(0, 0, 270, 480)
    c.vgrad(tout, 0, 480, (128, 96, 82), (102, 74, 66), steps=6)
    _diamants(c, tout, (120, 89, 78), (112, 82, 72))
    c.shape(c.mask_rect(0, 0, 270, 14), (80, 60, 56), (62, 46, 44), band=2, sdir="bottom")      # plinthe
    x0, y0, x1, y1 = 62, 168, 208, 446                                    # le tapis de prière
    for x in range(x0 + 3, x1 - 2, 5):                                    # franges
        c.fill(c.mask_rect(x, y0 - 6, x + 2, y0), (236, 222, 190))
    mat = c.mask_rect(x0, y0, x1, y1)
    c.shape(mat, (30, 98, 74), (22, 76, 58), (44, 120, 92), band=2)
    bord = (c.mask_rect(x0 + 5, y0 + 5, x1 - 5, y0 + 7) | c.mask_rect(x0 + 5, y1 - 7, x1 - 5, y1 - 5)
            | c.mask_rect(x0 + 5, y0 + 5, x0 + 7, y1 - 5) | c.mask_rect(x1 - 7, y0 + 5, x1 - 5, y1 - 5))
    c.fill(bord, (214, 170, 80))
    arc = c.mask_arch(x0 + 22, x1 - 22, y0 + 16, y0 + 136)
    c.shape(arc, (150, 38, 46), (112, 26, 34), (178, 60, 64), band=2, olcol=(214, 170, 80))
    c.fill(c.mask_rect(134, y0 + 34, 136, y0 + 54), (214, 170, 80))       # lampe du mihrab
    c.fill(c.mask_poly([(129, y0 + 54), (141, y0 + 54), (135, y0 + 66)]), (240, 200, 90))
    for k in range(4):                                                    # motifs du bas
        yy = y0 + 160 + k * 18
        c.fill(c.mask_rect(x0 + 14, yy, x1 - 14, yy + 1), (60, 140, 106))
    c.fill(c.mask_ell(135, 146, 26, 4), (88, 62, 56))                     # ombre du sac
    sac = c.mask_rrect(113, 92, 157, 144, 9)                              # le sac à dos (la soutra)
    c.shape(sac, (52, 78, 128), (36, 54, 92), (72, 102, 158), band=2)
    poche = c.mask_rrect(119, 116, 151, 141, 5)
    c.shape(poche, (64, 94, 150), (44, 66, 110), band=1)
    c.fill(c.mask_rect(122, 122, 148, 123), (36, 50, 84))
    c.fill(c.mask_rect(133, 120, 136, 125), (220, 200, 120))
    c.fill(c.mask_rect(125, 84, 145, 93) & ~c.mask_rect(129, 87, 141, 93), (40, 58, 96))   # poignée
    _mes_pieds(c, 404)
    lieux.teinte(c, heure, interieur=True)
    c.glow(36, 30, 130, (255, 206, 140), 0.18)
    return c, None


def porte_pov(heure="nuit"):
    """Vue subjective : sur le pas de ta porte, la nuit ; la rue mouillée dehors, tes chaussons en bas."""
    c = Px()
    facade = c.mask_rect(0, 0, 270, 112)
    c.vgrad(facade, 0, 112, (26, 30, 52), (36, 40, 66), steps=5)
    for i in range(6):
        for j in range(2):
            x, y = 14 + i * 44, 12 + j * 48
            f = c.mask_rect(x, y, x + 22, y + 30)
            c.fill(f, (236, 192, 110) if (i * 7 + j * 3) % 4 == 0 else (50, 56, 84))
            c.outline(f, (18, 16, 28))
    c.fill(c.mask_rect(0, 108, 270, 116), (70, 74, 96))
    rue = c.mask_rect(0, 116, 270, 300)
    c.vgrad(rue, 116, 300, (40, 46, 70), (60, 64, 88), steps=6)
    for k in range(10):                                                   # reflets du lampadaire
        y = 132 + k * 16
        c.fill(c.mask_rect(26 + (k % 3) * 2, y, 44 - (k % 2) * 3, y + 1), (150, 140, 120))
    lieux.lampadaire(c, 34, 116, h=96, on=True)
    c.tint(c.mask_poly([(30, 300), (240, 300), (262, 150), (8, 150)]), (255, 196, 120), 0.26)    # lumière de la maison
    for (xa, xb) in ((0, 22), (248, 270)):                               # encadrement de la porte
        c.shape(c.mask_rect(xa, 0, xb, 310), (96, 66, 46), (70, 46, 32), (124, 88, 60), band=2)
    c.shape(c.mask_rect(0, 298, 270, 312), (150, 142, 132), (118, 110, 102), band=2, sdir="bottom")  # seuil
    sol = c.mask_rect(0, 312, 270, 480)                                  # dedans : parquet chaud
    c.vgrad(sol, 312, 480, (150, 104, 70), (124, 84, 56), steps=5)
    for y in range(326, 480, 16):
        c.fill(c.mask_rect(0, y, 270, y + 1), (112, 76, 50))
    tapis = c.mask_rect(56, 318, 214, 374)
    c.fill(tapis, (150, 110, 60)); c.dither(tapis, (120, 86, 46), 0.5); c.outline(tapis, (90, 64, 36))
    _mes_pieds(c, 410, chaussons=True)
    c.glow(135, 476, 170, (255, 210, 150), 0.22)
    return c, None


def remise_nuit(heure="nuit"):
    """Une remise sombre, la nuit : murs de planches, un poteau, une lucarne de lune, une porte fermée, une gamelle vide."""
    c = Px()
    mur = c.mask_rect(0, 0, 270, 252)
    c.vgrad(mur, 0, 252, (46, 40, 54), (34, 30, 42), steps=6)
    for x in range(0, 270, 18):
        c.fill(c.mask_rect(x, 0, x + 1, 252), (26, 22, 32))
        for y in range(8 + (x * 7) % 30, 252, 46):
            c.px(x + 6, y, (56, 50, 64)); c.px(x + 7, y, (56, 50, 64))
    sol = c.mask_rect(0, 252, 270, 480)
    c.vgrad(sol, 252, 480, (60, 48, 42), (36, 28, 26), steps=6)
    rng = np.random.default_rng(3)
    for _ in range(90):                                                   # paille
        x, y = int(rng.uniform(0, 266)), int(rng.uniform(258, 476))
        c.line(x, y, x + int(rng.uniform(-6, 6)), y + int(rng.uniform(-3, 3)), (118, 98, 60))
    luc = c.mask_rect(186, 36, 236, 76)                                   # lucarne
    c.vgrad(luc, 36, 76, (92, 112, 162), (62, 78, 122), steps=3)
    c.fill(c.mask_ell(223, 48, 6, 6) & luc, (232, 236, 250))
    for x in (198, 211, 224):
        c.fill(c.mask_rect(x, 36, x + 2, 76), (30, 26, 34))
    c.outline(luc, (22, 18, 26))
    c.tint(c.mask_poly([(186, 76), (236, 76), (210, 400), (100, 400)]), (150, 166, 220), 0.14)
    porte = c.mask_rect(214, 96, 262, 254)                                # porte fermée
    c.shape(porte, (70, 52, 40), (50, 36, 28), (92, 70, 52), band=2)
    for y in (140, 190, 230):
        c.fill(c.mask_rect(214, y, 262, y + 1), (46, 34, 26))
    c.fill(c.mask_rect(218, 172, 222, 178), (180, 160, 100))
    poteau = c.mask_rect(60, 40, 80, 334)                                 # le poteau
    c.shape(poteau, (104, 78, 54), (76, 56, 38), (130, 100, 70), band=2)
    c.fill(c.mask_rect(58, 290, 82, 296), (176, 150, 100))               # anneau de corde
    c.outline(c.mask_rect(58, 290, 82, 296), (90, 70, 46))
    gam = c.mask_ell(206, 322, 20, 7)                                     # gamelle vide, fêlée
    c.shape(gam, (124, 124, 134), (92, 92, 102), (154, 154, 164), band=1)
    c.fill(c.mask_ell(206, 320, 15, 4), (70, 70, 80))
    c.line(196, 318, 202, 324, (40, 40, 48))
    c.glow(223, 54, 60, (200, 210, 250), 0.2)
    return c, None


def puits(heure="jour"):
    """Désert en plein soleil, il y a très longtemps : un puits de pierre, un palmier, du sable mouillé près du puits."""
    c = Px()
    ciel_ = c.mask_rect(0, 0, 270, 230)
    c.vgrad(ciel_, 0, 230, (120, 180, 230), (238, 224, 192), steps=6)
    c.glow(214, 40, 46, (255, 250, 220), 0.55)
    c.fill(c.mask_ell(214, 40, 12, 12), (255, 250, 232))
    lieux.dune(c, 214, 12, 90, 0.4, (228, 188, 130), y1=480)
    lieux.dune(c, 232, 10, 70, 1.6, (218, 174, 114), y1=480)
    sable = c.mask_rect(0, 252, 270, 480)
    c.vgrad(sable, 252, 480, (226, 184, 124), (204, 160, 102), steps=5)
    lieux.palmier(c, 236, 262, h=150, lean=-10, seed=2)
    corps = c.mask_rect(40, 222, 142, 292)                                # le puits
    c.shape(corps, (176, 156, 126), (140, 122, 96), (200, 182, 150), band=3)
    for i, y in enumerate(range(230, 292, 10)):
        c.fill(c.mask_rect(40, y, 142, y + 1), (140, 122, 96))
        for x in range(40 + (i % 2) * 12, 142, 24):
            c.fill(c.mask_rect(x, y, x + 1, y + 10), (140, 122, 96))
    c.shape(c.mask_ell(91, 222, 54, 10), (160, 140, 112), (128, 110, 86), (190, 172, 140), band=2)
    c.fill(c.mask_ell(91, 222, 44, 6), (40, 52, 64))
    for x in (46, 136):
        c.shape(c.mask_rect(x - 3, 160, x + 3, 222), (120, 86, 54), (90, 62, 38), band=1)
    c.shape(c.mask_rect(38, 156, 144, 163), (120, 86, 54), (90, 62, 38), band=1)
    c.fill(c.mask_rect(90, 163, 91, 190), (170, 140, 90))
    c.shape(c.mask_poly([(83, 190), (99, 190), (97, 204), (85, 204)]), (130, 96, 60), (96, 70, 44), band=1)
    mouille = c.mask_ell(178, 318, 40, 9)                                 # le sable mouillé (le chien le lèche)
    c.fill(mouille, (188, 148, 98)); c.dither(mouille & c.mask_ell(178, 318, 30, 6), (172, 132, 86), 0.5)
    return c, None


def chevet_pov(heure="nuit"):
    """Vue subjective depuis l'oreiller : la table de chevet (le téléphone y est posé), un verre d'eau, la chambre."""
    c = Px()
    nuit = heure == "nuit"
    mur = c.mask_rect(0, 0, 270, 300)
    c.vgrad(mur, 0, 300, (30, 34, 60) if nuit else (238, 224, 198), (22, 24, 44) if nuit else (222, 204, 176), steps=5)
    fen = c.mask_rect(24, 34, 120, 166)
    lieux.ciel(c, fen, 34, 166, "nuit" if nuit else "jour", seed=4, astre=(92, 66))
    c.fill(c.mask_rect(70, 34, 73, 166) | c.mask_rect(24, 98, 120, 101), (58, 50, 62) if nuit else (244, 240, 230))
    c.outline(fen, (20, 16, 26))
    if not nuit:
        c.tint(c.mask_poly([(24, 166), (120, 166), (200, 300), (96, 300)]), (255, 238, 186), 0.26)
    lit = c.mask_rect(0, 300, 270, 480)                                    # le lit (sous la table et autour)
    c.vgrad(lit, 300, 480, (44, 52, 92) if nuit else (196, 204, 230), (30, 36, 66) if nuit else (170, 180, 210), steps=4)
    dessus = c.mask_poly([(34, 252), (270, 238), (270, 304), (20, 318)])  # dessus de la table (perspective)
    c.shape(dessus, (124, 86, 58), (96, 64, 42), (152, 110, 76), band=2)
    face = c.mask_poly([(20, 318), (270, 304), (270, 392), (26, 406)])
    c.shape(face, (100, 68, 46), (76, 50, 34), band=2)
    c.fill(c.mask_rect(116, 342, 176, 346), (70, 46, 30))
    verre = c.mask_rect(216, 206, 236, 258)                               # verre d'eau
    c.fill(verre, (176, 200, 228) if not nuit else (86, 104, 146))
    c.fill(c.mask_rect(217, 226, 235, 257), (120, 170, 220) if not nuit else (58, 86, 136))
    c.outline(verre, (40, 50, 70))
    oreiller = c.mask_ell(76, 474, 132, 76)                               # oreiller au premier plan
    c.shape(oreiller, (206, 210, 232) if not nuit else (110, 118, 160), (170, 176, 204) if not nuit else (84, 92, 132), band=3)
    c.shape(c.mask_poly([(150, 480), (270, 418), (270, 480)]), (90, 110, 170), (70, 86, 140), band=2)
    if nuit:
        c.glow(72, 100, 74, (180, 190, 240), 0.2)
    return c, None


def nuque(heure="nuit"):
    """Il dort : sa tête vue de dos sur l'oreiller, la nuque au-dessus de la couverture."""
    c = Px()
    nuit = heure == "nuit"
    fond = c.mask_rect(0, 0, 270, 480)
    c.vgrad(fond, 0, 480, (40, 44, 74) if nuit else (234, 218, 190), (28, 30, 52) if nuit else (216, 198, 170), steps=6)
    c.shape(c.mask_rrect(16, 118, 254, 330, 34), (146, 154, 194) if nuit else (238, 238, 246),
            (114, 122, 164) if nuit else (208, 208, 224), band=3)
    peau, peau_s = ((122, 90, 80), (98, 72, 64)) if nuit else ((182, 132, 102), (150, 106, 80))
    for ox in (74, 196):                                                  # oreilles
        c.shape(c.mask_ell(ox, 232, 9, 16), peau, peau_s, band=1)
    c.shape(c.mask_ell(135, 220, 62, 68), (44, 32, 30), (30, 22, 22), (66, 50, 46), band=3)   # cheveux
    for k in range(9):
        x = 96 + k * 9
        c.line(x, 168 + abs(k - 4) * 3, x + 2, 270, (58, 44, 40))
    c.shape(c.mask_poly([(98, 268), (172, 268), (186, 336), (84, 336)]), peau, peau_s, band=2)   # la nuque
    c.fill(c.mask_poly([(98, 268), (172, 268), (168, 280), (102, 280)]), (44, 32, 30))
    for x in range(104, 168, 6):
        c.px(x, 281, (44, 32, 30)); c.px(x + 2, 282, (44, 32, 30))
    couv = c.mask_poly([(0, 322), (60, 312), (135, 330), (210, 310), (270, 322), (270, 480), (0, 480)])
    c.shape(couv, (70, 90, 150) if nuit else (90, 120, 180), (54, 70, 120) if nuit else (70, 96, 150), band=3)
    for (xa, ya, xb, yb) in ((40, 366, 120, 424), (160, 356, 230, 436), (90, 446, 200, 472)):
        c.line(xa, ya, xb, yb, (50, 64, 110) if nuit else (70, 96, 150))
    if nuit:
        c.glow(204, 56, 130, (160, 170, 230), 0.16)
    else:
        c.glow(222, 36, 170, (255, 236, 180), 0.28)
    return c, None


def chambre_aube(heure="jour"):
    """Une chambre au lever du soleil : grande fenêtre dorée, tapis de prière déroulé, lumière chaude."""
    c = Px()
    mur = c.mask_rect(0, 0, 270, 312)
    c.vgrad(mur, 0, 312, (250, 216, 172), (236, 198, 152), steps=6)
    fen = c.mask_rect(66, 46, 204, 214)
    lieux.ciel(c, fen, 46, 214, "soir", seed=6, astre=(135, 196))
    c.fill(c.mask_rect(133, 46, 137, 214) | c.mask_rect(66, 128, 204, 132), (244, 230, 204))
    c.outline(fen, (90, 60, 40))
    c.shape(c.mask_rect(58, 214, 212, 222), (222, 198, 162), (192, 168, 132), band=1)
    sol = c.mask_rect(0, 312, 270, 480)
    c.vgrad(sol, 312, 480, (196, 150, 104), (170, 126, 86), steps=5)
    for y in range(326, 480, 16):
        c.fill(c.mask_rect(0, y, 270, y + 1), (160, 118, 80))
    tapis = c.mask_poly([(78, 372), (192, 372), (206, 444), (64, 444)])
    c.shape(tapis, (30, 98, 74), (22, 76, 58), band=2)
    c.fill(c.mask_poly([(112, 376), (158, 376), (162, 398), (108, 398)]), (150, 38, 46))
    c.tint(c.mask_poly([(66, 214), (204, 214), (252, 480), (18, 480)]), (255, 220, 150), 0.2)
    c.glow(135, 130, 130, (255, 210, 140), 0.32)
    return c, None


DECORS = dict(tapis_pov=tapis_pov, porte_pov=porte_pov, remise_nuit=remise_nuit, puits=puits,
              chevet_pov=chevet_pov, chevet_pov_jour=lambda: chevet_pov("jour"),
              nuque_nuit=nuque, nuque_jour=lambda: nuque("jour"), chambre_aube=chambre_aube)
lieux.DECORS.update(DECORS)
sets.DECORS.update(DECORS)
for _n in DECORS:
    lieux.SPOTS[_n] = dict(gauche=(300, 1340), droite=(780, 1340), k=7, opts={})


# =================================================================== SPRITES (pixel, même contour que le moteur)
_SP = {}


def _cache(key, fn):
    if key not in _SP:
        _SP[key] = fn()
    return _SP[key]


def _jambes(pose):
    """Jambes d'un passant vues d'en haut (jean + baskets) : elles montent jusqu'au haut de l'image. 48x170.
    pose : a / b (il marche vers la gauche), arret (face à toi)."""
    sp = Spr(48, 170)
    jean, js, jl = (60, 74, 116), (44, 56, 90), (84, 100, 150)
    off = dict(a=(-6, 5), b=(5, -6), arret=(0, 0))[pose]
    for i, (x, o) in enumerate(((15, off[0]), (32, off[1]))):
        m = sp.m_poly([(x - 8, 0), (x + 8, 0), (x + 6 + o, 150), (x - 6 + o, 150)])
        sp.paint(m, jean if i == 0 else js)
        sp.tone(sp.m_poly([(x - 8, 0), (x - 6, 0), (x - 5 + o, 150), (x - 6 + o, 150)]) & m, jl)
        sp.paint(sp.m_rect(x - 7 + o, 146, x + 7 + o, 151), (40, 50, 80))
        if pose == "arret":                                         # baskets tournées vers toi
            b = sp.m_ell(x + o, 158, 7, 10)
            sp.paint(b, (238, 238, 244))
            sp.tone(sp.m_rect(x - 7 + o, 164, x + 7 + o, 168) & b, (210, 60, 60))
            sp.pxs([(x - 2 + o, 154), (x + 2 + o, 154), (x - 2 + o, 157), (x + 2 + o, 157)], (150, 150, 160))
        else:                                                       # baskets tournées vers la gauche (il marche)
            b = sp.m_ell(x - 4 + o, 158, 10, 6.5)
            sp.paint(b, (238, 238, 244))
            sp.tone(sp.m_rect(x - 14 + o, 162, x + 6 + o, 164) & b, (210, 60, 60))
            sp.pxs([(x - 6 + o, 156), (x - 3 + o, 155), (x + o, 156)], (150, 150, 160))
    sp.outline()
    return sp.img(K)


def _bras(img, MAIN, xh, yh, a=1.0):
    """Ta main (bout des doigts en yh) et ton bras en perspective : étroit au poignet, large en bas (près de toi)."""
    if yh >= img.height:
        return
    yb = int(yh + MAIN.height - 40)
    H_ = img.height
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    al = int(255 * a)
    pts = [(xh - 56, yb), (xh + 56, yb), (xh + 150, H_ + 60), (xh - 150, H_ + 60)]
    d.polygon(pts, fill=(22, 16, 26, al))                                  # contour
    pts2 = [(xh - 50, yb), (xh + 50, yb), (xh + 142, H_ + 60), (xh - 142, H_ + 60)]
    d.polygon(pts2, fill=(120, 126, 142, al))                              # la manche
    d.polygon([(xh + 26, yb), (xh + 50, yb), (xh + 142, H_ + 60), (xh + 80, H_ + 60)], fill=(100, 104, 120, al))
    for k in range(1, 4):                                                  # plis de la manche
        y = yb + (H_ - yb) * k / 4
        e = (y - yb) / max(1, H_ + 60 - yb)
        w = 50 + 92 * e
        d.line([(xh - w + 14, y), (xh + w * 0.3, y + 10)], fill=(96, 100, 116, al), width=4)
    d.rectangle([xh - 52, yb - 4, xh + 52, yb + 16], fill=(96, 100, 116, al))   # poignet de la manche
    img.alpha_composite(lay)
    _colle(img, MAIN, xh, yh + MAIN.height, a)


def _main():
    """Ta main vue de dessus (dos de la main, doigts vers le haut) au bout de ta manche. 32x60."""
    sp = Spr(32, 60)
    peau, ps, pl = (206, 156, 120), (170, 122, 92), (226, 184, 150)
    for i, x in enumerate((7, 12, 17, 22)):                          # doigts
        h = (6, 2, 3, 7)[i]
        sp.paint(sp.m_rect(x, h, x + 3, 22), peau)
        sp.tone(sp.m_rect(x + 3, h, x + 3, 22), ps)
        sp.px(x + 1, h + 1, pl)
    pa = sp.m_rrect(6, 18, 27, 40, 5) if hasattr(sp, "m_rrect") else sp.m_rect(6, 18, 27, 40)
    sp.paint(pa, peau)
    sp.tone(sp.m_rect(24, 18, 27, 40) & pa, ps)
    for x in (9, 14, 19, 24):
        sp.px(x, 21, ps)
    sp.paint(sp.m_poly([(26, 24), (31, 20), (31, 26), (27, 36)]), peau)   # pouce
    sp.paint(sp.m_rect(6, 38, 27, 43), (220, 168, 132))                    # poignet
    manche = sp.m_rect(3, 42, 30, 59)
    sp.paint(manche, (120, 126, 142))
    sp.tone(sp.m_rect(3, 42, 30, 45), (96, 100, 116))
    sp.tone(sp.m_rect(27, 46, 30, 59) & manche, (100, 104, 120))
    sp.outline()
    return sp.img(K)


def _gamelle(pleine=True):
    sp = Spr(32, 12)
    b = sp.m_ell(16, 7, 14, 4.6)
    sp.paint(b, (200, 62, 62))
    sp.tone(sp.m_rect(0, 8, 31, 11) & b, (160, 44, 44))
    if pleine:
        for (x, y) in ((8, 4), (11, 3), (14, 4), (17, 3), (20, 4), (23, 4), (12, 5), (18, 5), (15, 2)):
            sp.paint(sp.m_rect(x, y, x + 1, y + 1), (140, 92, 52))
    else:
        sp.paint(sp.m_ell(16, 5, 10, 2), (90, 40, 40))
    sp.outline()
    return sp.img(K)


GRIS = dict(b=(150, 142, 134), s=(116, 108, 102), d=(88, 82, 78), h=(186, 178, 170), ventre=(206, 198, 188),
            rayure=(112, 104, 98))


def _chat_face(pose="assis", maigre=True):
    """Chat assis vu de face, grands yeux (gros plan en vue subjective). 48x58. Poses : assis, miaou, mange, heureux."""
    P = GRIS
    sp = Spr(48, 58)
    q = sp.m_line([(36, 52), (43, 44), (42, 34), (39, 30)], 3)      # queue
    sp.paint(q, P["s"])
    corps = sp.m_ell(24, 41, 10 if maigre else 12.5, 14)
    sp.paint(corps, P["b"])
    sp.tone(sp.m_ell(24, 44, 6 if maigre else 8, 9) & corps, P["ventre"])
    sp.shade(corps, P["s"], dx=-1, dy=0, depth=2)
    if maigre:                                                      # côtes visibles
        for y in (36, 40, 44):
            sp.tone(sp.m_rect(15, y, 17, y) | sp.m_rect(31, y, 33, y), P["d"])
    for x in (17, 27):                                              # pattes avant
        pa = sp.m_rect(x, 44, x + 4, 55)
        sp.paint(pa, P["b"]); sp.tone(sp.m_rect(x + 4, 44, x + 4, 55), P["s"])
        sp.paint(sp.m_ell(x + 2, 55, 3, 2), P["h"])
    hy = 28 if pose == "mange" else 19                              # la tête
    tete = sp.m_ell(24, hy, 13, 11)
    sp.paint(tete, P["b"])
    sp.shade(tete, P["s"], dx=-1, dy=-1, depth=1)
    for (a, b_, cx_) in ((11, 20, 14), (37, 28, 34)):               # oreilles
        o = sp.m_poly([(a, hy - 5), (b_, hy - 8), (cx_, hy - 18)])
        sp.paint(o, P["b"], newpart=False)
        sp.tone(sp.m_poly([(a + 2 if a < 24 else a - 2, hy - 6), (b_ - 2 if a < 24 else b_ + 2, hy - 8), (cx_, hy - 15)]),
                (230, 150, 160))
    for x in (19, 24, 29):                                          # rayures du front
        sp.tone(sp.m_rect(x, hy - 10, x, hy - 7) & tete, P["rayure"])
    if pose in ("mange", "heureux"):                                # yeux fermés (contents)
        for ex in (18, 30):
            sp.pxs([(ex - 2, hy), (ex - 1, hy - 1), (ex, hy - 1), (ex + 1, hy - 1), (ex + 2, hy)], (40, 34, 40))
    else:                                                           # grands yeux qui supplient
        for ex in (18, 30):
            sp.paint(sp.m_ell(ex, hy, 3.6, 4.2), (196, 216, 92), newpart=False)
            sp.paint(sp.m_ell(ex, hy + 0.5, 1.8, 3.4), (24, 22, 30), newpart=False)
            sp.px(ex - 1, hy - 2, (255, 255, 255)); sp.px(ex + 1, hy + 2, (255, 255, 255))
            sp.px(ex - 4, hy - 4, P["d"]); sp.px(ex - 3, hy - 5, P["d"])          # sourcils tristes
    sp.paint(sp.m_poly([(22, hy + 4), (26, hy + 4), (24, hy + 6)]), (232, 140, 150), newpart=False)   # nez
    if pose == "miaou":
        sp.paint(sp.m_ell(24, hy + 9, 3, 3), (110, 36, 48), newpart=False)
        sp.paint(sp.m_ell(24, hy + 10.5, 2, 1.2), (226, 120, 136), newpart=False)
    else:
        sp.pxs([(23, hy + 7), (22, hy + 8), (25, hy + 7), (26, hy + 8)], (60, 46, 50))
    for (x0, y0, x1, y1) in ((14, hy + 6, 4, hy + 4), (14, hy + 8, 4, hy + 9), (34, hy + 6, 44, hy + 4), (34, hy + 8, 44, hy + 9)):
        sp.paint(sp.m_line([(x0, y0), (x1, y1)], 1), (226, 226, 230), newpart=False)
    sp.outline()
    return sp.img(1)


def _chat_couche():
    """La chatte attachée, couchée sur le flanc, maigre, les yeux mi-clos. 56x26."""
    P = GRIS
    sp = Spr(56, 26)
    sp.paint(sp.m_line([(4, 20), (10, 21), (14, 21)], 2), P["s"])
    corps = sp.m_ell(27, 17, 15, 5.4)
    sp.paint(corps, P["b"])
    sp.shade(corps, P["s"], dx=-1, dy=-1, depth=1)
    for x in (22, 26, 30):                                          # côtes
        sp.tone(sp.m_rect(x, 14, x, 17), P["d"])
    sp.paint(sp.m_rect(38, 20, 47, 22), P["h"])                     # pattes avant sous la tête
    tete = sp.m_ell(46, 16, 6.4, 5.6)
    sp.paint(tete, P["b"])
    sp.shade(tete, P["s"], dx=-1, dy=-1, depth=1)
    sp.paint(sp.m_poly([(41, 13), (44, 11), (42, 7)]), P["b"], newpart=False)
    sp.paint(sp.m_poly([(47, 11), (51, 12), (50, 7)]), P["b"], newpart=False)
    sp.pxs([(44, 16), (45, 16), (49, 16), (50, 16)], (40, 34, 40))      # yeux mi-clos
    sp.px(47, 18, (232, 140, 150))
    sp.paint(sp.m_rect(39, 13, 40, 19), (176, 150, 100), newpart=False)  # le collier de corde
    sp.outline()
    return sp.img(1)


def _chien(pose="halete"):
    """Chien maigre et assoiffé, de profil, tourné vers la gauche. 60x42. Poses : halete, lape."""
    sp = Spr(60, 42)
    b, s, d, h = (200, 164, 114), (166, 132, 90), (130, 100, 66), (226, 196, 150)
    sp.paint(sp.m_line([(48, 18), (55, 22), (57, 28)], 2), s)        # queue basse
    corps = sp.m_ell(34, 20, 15, 6)
    sp.paint(corps, b)
    sp.shade(corps, s, dx=-1, dy=-1, depth=1)
    for x in (30, 34, 38):
        sp.tone(sp.m_rect(x, 17, x, 21), d)
    for i, x in enumerate((22, 26, 40, 44)):                         # pattes
        far = i in (1, 3)
        sp.paint(sp.m_rect(x, 23, x + 2, 38), s if far else b)
        sp.paint(sp.m_rect(x - 1, 37, x + 2, 38), d)
    if pose == "lape":
        hx, hy = 13, 28
        cou = sp.m_poly([(22, 15), (26, 18), (17, 30), (12, 27)])
    else:
        hx, hy = 15, 12
        cou = sp.m_poly([(22, 15), (27, 19), (20, 18), (14, 14)])
    sp.paint(cou, b)
    tete = sp.m_ell(hx, hy, 6.5, 5.5)
    sp.paint(tete, b)
    sp.paint(sp.m_rect(hx - 11, hy, hx - 4, hy + 3), b)              # museau
    sp.px(hx - 11, hy, (40, 30, 30)); sp.px(hx - 11, hy + 1, (40, 30, 30))
    sp.paint(sp.m_poly([(hx + 1, hy - 5), (hx + 6, hy - 4), (hx + 5, hy + 4)]), s, newpart=False)   # oreille tombante
    sp.px(hx - 3, hy - 2, (30, 26, 30))
    langue = sp.m_rect(hx - 8, hy + 4, hx - 6, hy + 8 if pose == "halete" else hy + 6)
    sp.paint(langue, (232, 120, 136), newpart=False)
    sp.outline()
    return sp.img(1)


def _botte():
    """La botte de cuir (khuff) remplie d'eau. 22x26."""
    sp = Spr(22, 26)
    c_, cs = (130, 84, 48), (100, 62, 36)
    sp.paint(sp.m_rect(5, 3, 14, 19), c_)
    sp.tone(sp.m_rect(12, 3, 14, 19), cs)
    sp.paint(sp.m_rect(2, 17, 19, 24), c_)
    sp.tone(sp.m_rect(2, 22, 19, 24), cs)
    sp.paint(sp.m_rect(6, 2, 13, 4), (110, 180, 230), newpart=False)   # l'eau
    sp.px(8, 2, (240, 250, 255)); sp.px(9, 2, (240, 250, 255))
    sp.outline()
    return sp.img(1)


def _noeud(defait=False):
    """Un nœud sombre (violet-noir). 18x16."""
    sp = Spr(18, 16)
    c_, h = (44, 26, 60), (104, 72, 136)
    if defait:
        sp.paint(sp.m_line([(1, 9), (5, 6), (9, 9), (13, 6), (17, 9)], 2), c_)
    else:
        sp.paint(sp.m_ell(6, 7, 4.5, 4.5) & ~sp.m_ell(6, 7, 2, 2), c_)
        sp.paint(sp.m_ell(12, 7, 4.5, 4.5) & ~sp.m_ell(12, 7, 2, 2), c_)
        sp.paint(sp.m_line([(8, 9), (4, 14)], 2) | sp.m_line([(10, 9), (14, 14)], 2), c_)
        sp.pxs([(5, 3), (11, 3), (9, 7)], h)
    sp.outline()
    return sp.img(1)


def _px_scale(im, k):
    return im.resize((max(1, int(round(im.width * k))), max(1, int(round(im.height * k)))), Image.NEAREST)


def _colle(img, im, x, y, a=1.0, ancre="bas"):
    """Colle un sprite : (x, y) = milieu du bas (ancre bas) ou centre (ancre centre)."""
    if a <= 0.01:
        return
    if a < 1:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    if ancre == "bas":
        img.alpha_composite(im, (int(round(x - im.width / 2)), int(round(y - im.height))))
    else:
        img.alpha_composite(im, (int(round(x - im.width / 2)), int(round(y - im.height / 2))))


def _halo(img, x, y, r, col, a):
    """Halo doux (lumière) — en paliers nets comme les lueurs du moteur."""
    if a <= 0.01:
        return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for k, al in ((1.0, 0.18), (0.72, 0.26), (0.46, 0.34)):
        d.ellipse([x - r * k, y - r * k, x + r * k, y + r * k], fill=(*col, int(255 * al * a)))
    img.alpha_composite(lay)


def _etincelles(img, x, y, u, a=1.0, n=6, col=(255, 248, 210), haut=120, seed=1):
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(img)
    for i in range(n):
        e = (u * 0.7 + rng.uniform(0, 1)) % 1.0
        sx = x + rng.uniform(-70, 70)
        sy = y - haut * e
        z = 6 * (1 - e) + 2
        al = int(230 * a * math.sin(math.pi * e))
        d.rectangle([sx - z / 2, sy - z * 1.6, sx + z / 2, sy + z * 1.6], fill=(*col, al))
        d.rectangle([sx - z * 1.6, sy - z / 2, sx + z * 1.6, sy + z / 2], fill=(*col, al))


def _coeur(img, x, y, z, a):
    d = ImageDraw.Draw(img)
    c = (240, 90, 120, int(255 * a))
    for (dx, dy, w, h) in ((-2, -1, 2, 2), (1, -1, 2, 2), (-2, 0, 5, 2), (-1, 2, 3, 1), (0, 3, 1, 1)):
        d.rectangle([x + dx * z, y + dy * z, x + (dx + w) * z - 1, y + (dy + h) * z - 1], fill=c)


def _texte_pixel(txt, col=(255, 255, 255), ol=(22, 16, 26), size=9, k=4):
    return pxv.pixel_text(txt, col, ol, size=size, k=k)


def _arabe(txt, taille=96, col=(255, 222, 120)):
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        t = get_display(arabic_reshaper.reshape(txt))
    except Exception:
        t = txt
    police = next((p for p in ("C:/Windows/Fonts/trado.ttf", "C:/Windows/Fonts/arabtype.ttf", "C:/Windows/Fonts/tahomabd.ttf",
                               "C:/Windows/Fonts/arial.ttf") if os.path.exists(p)), "C:/Windows/Fonts/arial.ttf")
    f = ImageFont.truetype(police, taille)
    d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
    bb = d0.textbbox((0, 0), t, font=f, stroke_width=6)
    im = Image.new("RGBA", (bb[2] - bb[0] + 40, bb[3] - bb[1] + 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((20 - bb[0], 20 - bb[1]), t, font=f, fill=col, stroke_width=6, stroke_fill=(60, 36, 10))
    return im


def _auto(txt, col=(255, 255, 255), size=52, maxc=20):
    """Autocollant (même style que les étiquettes du moteur), coupé en lignes de ~maxc caractères."""
    import explique
    return explique.autocollant(pxv.big_title([(l_, col) for l_ in explique.coupe(txt, maxc)], size=size), r=3,
                                ombre=False)


# =================================================================== LE PLAN EN VUE SUBJECTIVE
BALISES = ("pov",)


def _evts(evts):
    """[(u, "pov chat"), …] -> [(u, mot, reste)] (les {texte}/{source} sont gérés par scenario.py)."""
    out = []
    for (u, c) in evts:
        m = c.split()
        if not m or m[0].lower() != "pov":
            continue
        mot = m[1].lower() if len(m) > 1 else ""
        reste = c.split(None, 2)[2] if len(m) > 2 else ""
        out.append((u, mot, reste))
    return out


def _quand(ev, mot, defaut=None):
    return next((u for (u, m, _) in ev if m == mot), defaut)


def _tous(ev, mot):
    return [u for (u, m, _) in ev if m == mot]


def plan(sc, debut, fin, evts, band=True):
    """Construit le plan en vue subjective du décor courant (sc.bg) ; evts = [(u depuis le début du plan, commande)]."""
    ev = _evts(evts)
    D = fin - debut
    bg = sc.bg
    anims, avant, ecran, sons = [], [], [], []
    amb = None
    cam = [(0.0, 1.0, (540, 960)), (D, 1.05, (540, 930))]               # lente avancée : jamais un plan figé

    for (u, m, reste) in ev:                                         # autocollants « {pov label "…"} »
        if m == "label" and '"' in reste:
            txt = reste.split('"')[1]
            if not txt.strip():                                      # {pov label ""} : efface l'autocollant en cours
                continue
            im = _auto(txt.upper(), (255, 214, 70) if "jaune" in reste else (255, 255, 255))
            nxt = [u2 for (u2, m2, _) in ev if m2 == "label" and u2 > u]
            u_fin = (nxt[0] - 0.2) if nxt else D

            def lab(img, uu, im=im, u0=u, u1=u_fin):
                if uu < u0 or uu > u1 + 0.4:
                    return
                a = smooth((uu - u0) / 0.35) * (1 - smooth((uu - u1) / 0.4))
                _colle(img, im, img.width / 2, img.height * 0.42, a, ancre="centre")
            ecran.append(lab)

    if bg.startswith("tapis_pov"):
        t_pass = _quand(ev, "passant", 0.0)
        t_rep = _tous(ev, "repousse")
        t_ins = _tous(ev, "insiste")
        t_dem = _quand(ev, "demon")
        t_con = _quand(ev, "contourne")
        forts = [u for (u, m, r) in ev if m == "repousse" and "fort" in r]
        J = {p: _cache(("jambes", p), lambda p=p: _jambes(p)) for p in ("a", "b", "arret")}
        MAIN = _cache("main", _main)
        y_arret = 158 * K                                              # pieds du passant : entre le sac et le tapis

        def pos_passant(u):
            """(x, y des pieds, marche ?) du passant à l'instant u."""
            x, y, marche = 1060.0, y_arret, False
            if u >= t_pass:                                            # il arrive de la droite (déjà visible à 0 s)
                e = smooth((u - t_pass) / 1.7)                          # et s'arrête devant toi
                x = 1060 + (470 - 1060) * e
                marche = e < 0.97
            for ta in _tous(ev, "avance"):                             # {pov avance} : il fait un pas de plus vers toi
                if u >= ta:
                    y += 40 * smooth((u - ta) / 0.6)
                    marche = marche or (u - ta) < 0.6
            for tr in t_rep:                                           # repoussé : il recule (vers le haut)
                if u >= tr + 0.35:
                    k_ = 1.6 if tr in forts else 1.0
                    y -= 90 * k_ * smooth((u - tr - 0.35) / 0.5)
            for ti in t_ins:                                           # il revient
                if u >= ti:
                    y += 90 * smooth((u - ti) / 0.7)
                    marche = marche or (u - ti) < 0.7
            if t_con is not None and u >= t_con:                       # il passe DERRIÈRE le sac et s'en va
                e = smooth((u - t_con) / 2.2)
                y = y - (y - 40) * min(1.0, e * 2.0)
                x = 470 + (-400 - 470) * smooth(max(0.0, (u - t_con - 0.6) / 2.0))
                marche = True
            return x, y, marche

        def passant(img, u):
            x, y, marche = pos_passant(u)
            if x > 1500 or x < -300:
                return
            if t_dem is not None and t_dem <= u < t_dem + 3.4:         # « ce n'est qu'un diable » : halo sombre
                a = smooth((u - t_dem) / 0.6) * (1 - smooth((u - t_dem - 2.5) / 0.8))
                _halo(img, x, y - 230, 260, (30, 8, 20), 0.9 * a)
                _halo(img, x, y - 230, 170, (90, 10, 30), 0.35 * a)
            im = J[("a" if int(u * 4) % 2 == 0 else "b")] if marche else J["arret"]
            _colle(img, im, x, y)

        def main(img, u):
            for tr in t_rep:                                           # ta main sort du bas de l'image et repousse
                if tr - 0.1 <= u < tr + 1.6:
                    fort = tr in forts
                    v = u - tr
                    e = smooth(v / 0.35) * (1 - smooth((v - 1.05) / 0.5))
                    xh = 500
                    yh = 1920 + 60 - (1920 + 60 - (y_arret + (60 if not fort else 20))) * e
                    if fort and 0.3 < v < 0.6:                         # poussée plus forte : petites lignes de mouvement
                        d = ImageDraw.Draw(img)
                        for k_ in range(3):
                            yy = yh - 30 - k_ * 26
                            d.rectangle([xh - 150, yy, xh - 100, yy + 6], fill=(255, 255, 255, 170))
                            d.rectangle([xh + 100, yy, xh + 150, yy + 6], fill=(255, 255, 255, 170))
                    _bras(img, MAIN, xh, yh)
        anims += [passant]
        avant += [main]
        if t_pass is not None:
            sons.append((t_pass, "dv_pas_pierre", 0.10, 2.0))
        for ta in _tous(ev, "avance"):
            sons.append((ta, "dv_pas_pierre", 0.07, 0.8))
        for tr in t_rep:
            sons.append((tr + 0.3, "tr_whoosh_doux", 0.06, None))
        if t_con is not None:
            sons.append((t_con, "dv_pas_pierre", 0.08, 2.0))
        u_sou = _quand(ev, "soutra")
        if u_sou is not None:
            im_s = _auto("TA SOUTRA", (255, 214, 70), size=46)

            def sou(img, u, im=im_s, u0=u_sou):
                if u0 <= u < u0 + 4.2:                                 # « TA SOUTRA » le temps de la question
                    a = smooth((u - u0) / 0.35) * (1 - smooth((u - u0 - 3.8) / 0.4))
                    _colle(img, im, 540 + 236, 118 * K, a, ancre="centre")
            avant.append(sou)
        cam = [(0.0, 1.0, (540, 960))]                                 # la caméra va vers ce qui se passe
        if u_sou is not None:
            cam.append((u_sou + 0.3, 1.12, (540, 760)))
        if t_rep:
            cam.append((t_rep[0] - 0.1, 1.18, (520, 780)))
        if t_dem is not None:
            cam.append((t_dem + 0.8, 1.12, (520, 820)))
            cam.append((t_dem + 2.4, 1.04, (540, 900)))
        if t_con is not None:
            cam.append((t_con + 0.4, 1.0, (540, 940)))
        cam.append((D, 1.04, (540, 930)))
        cam = sorted(cam, key=lambda k_: k_[0])
        amb = ("amb_grillons_nuit", 0.06)

    elif bg.startswith("porte_pov"):
        t_chat = _quand(ev, "chat", 0.0)
        t_chat = 0.0 if t_chat < 0.6 else t_chat                       # au début du plan : visible dès l'image 0
        deja = any(set(r.lower().split()) & {"la", "là"} for (u, m, r) in ev if m == "chat")   # {pov chat là} : déjà assis
        t_miaous = _tous(ev, "miaou")
        t_gam = _quand(ev, "gamelle")
        CH = {p: _cache(("chatf", p), lambda p=p: _chat_face(p, maigre=True)) for p in ("assis", "miaou", "mange", "heureux")}
        GAM = _cache("gamelle", lambda: _gamelle(True))
        MAIN = _cache("main", _main)
        y_fin, k_fin = 302 * K, 7.0

        def chat(img, u):
            if u < t_chat and not deja:
                return
            e = 1.0 if deja else smooth((u - t_chat) / 2.0)
            x = 640 + (540 - 640) * e
            y = 186 * K + (y_fin - 186 * K) * e
            k = 3.0 + (k_fin - 3.0) * e
            sway = math.sin((u - t_chat) * 7.0) * 10 * (1 - e)          # il trottine vers toi (balancement)
            pose = "assis"
            if any(tm <= u < tm + 0.9 for tm in t_miaous):
                pose = "miaou"
            if t_gam is not None and u >= t_gam + 1.1:
                pose = "mange" if int((u - t_gam) * 2.2) % 3 else "heureux"
            im = CH[pose]
            if e >= 0.999:
                im = _cache(("chatf_k", pose), lambda im=im: _px_scale(im, k_fin))
            else:
                im = _px_scale(im, k)
            _colle(img, im, x + sway, y)
            if any(tm <= u < tm + 0.9 for tm in t_miaous):           # « MIAOU »
                tm = next(tm for tm in t_miaous if tm <= u < tm + 0.9)
                bul = _cache("miaou_txt", lambda: _auto("MIAOU…", (255, 255, 255), size=40))
                _colle(img, bul, x + 230, y - im.height + 30, smooth((u - tm) / 0.2) * (1 - smooth((u - tm - 0.6) / 0.3)),
                       ancre="centre")
            if t_gam is not None and u >= t_gam + 1.4:                # des cœurs : il est content
                for i in range(3):
                    p = ((u - t_gam - 1.4) * 0.5 + i / 3) % 1.0
                    _coeur(img, x - 120 + i * 120, y - im.height - 20 - 160 * p, 6, math.sin(math.pi * p))

        def gamelle(img, u):
            if t_gam is None or u < t_gam:
                return
            e = smooth((u - t_gam) / 0.9)
            r = smooth((u - t_gam - 1.0) / 0.6)
            yg = 1980 + (y_fin + 34 - 1980) * e
            if r < 1:                                                  # ta main pose la gamelle puis repart
                _bras(img, MAIN, 560, yg - 20 + 900 * r)
            _colle(img, GAM, 540, yg)
        anims += [chat]
        avant += [gamelle]

        def pluie(img, u):                                           # la pluie, seulement dehors
            d = ImageDraw.Draw(img)
            rng = np.random.default_rng(4)
            for i in range(70):
                x0 = rng.uniform(90, 990)
                v = rng.uniform(900, 1300)
                y = (rng.uniform(0, 1200) + u * v) % 1200
                if y > 1180:
                    continue
                d.rectangle([x0, y, x0 + 3, y + 26], fill=(176, 196, 226, 120))
        anims.insert(0, pluie)
        amb = ("amb_pluie", 0.10)
        s_m = _son("chat_miaou")
        for tm in t_miaous:
            if s_m:
                sons.append((tm, s_m, 0.22, None))
        s_r = _son("chat_ronron")
        if t_gam is not None:
            sons.append((t_gam, "dv_clic", 0.05, None))
            if s_r:
                sons.append((t_gam + 1.2, s_r, 0.18, 3.0))
        if deja:
            cam = [(0.0, 1.16, (540, 1040))]
            if t_gam is not None:
                cam.append((t_gam + 0.2, 1.08, (540, 1080)))
            cam.append((D, 1.16, (540, 1050)))
        else:
            cam = [(0.0, 1.0, (540, 960)), (2.3, 1.16, (540, 1040)), (D, 1.20, (540, 1040))]

    elif bg.startswith("remise"):
        t_ch = _quand(ev, "chatte", 0.0)
        t_jours = _quand(ev, "jours")
        t_porte = _quand(ev, "porte")
        t_enfer = _quand(ev, "enfer")
        CC = _cache("chat_couche", lambda: _px_scale(_chat_couche().transpose(Image.FLIP_LEFT_RIGHT), 7))

        def remise(img, u):
            d = ImageDraw.Draw(img)
            if t_porte is None or u < t_porte + 0.8:                    # lumière sous la porte (quelqu'un est là)
                a = 1.0 if t_porte is None else 1 - smooth((u - t_porte) / 0.8)
                d.rectangle([214 * K, 251 * K, 262 * K, 253 * K], fill=(255, 210, 140, int(230 * a)))
            if t_jours is not None and u >= t_jours:                    # les jours passent : traits gravés au mur
                n = min(13, int((u - t_jours) / 0.32) + 1)
                for i in range(n):
                    g, j = divmod(i, 5)
                    x = (100 + g * 32) * K
                    if j < 4:
                        d.rectangle([x + j * 5 * K, 112 * K, x + j * 5 * K + K - 1, 136 * K], fill=(186, 176, 186, 255))
                    else:
                        d.line([(x - 2 * K, 132 * K), (x + 18 * K, 116 * K)], fill=(186, 176, 186, 255), width=K)
            if u >= t_ch:                                               # le chat attaché au poteau
                a = smooth((u - t_ch) / 0.5)
                xc, yc = 150 * K, 320 * K
                _colle(img, CC, xc, yc + (K if int(u * 1.2) % 2 else 0), a)       # il respire à peine
                col_x, col_y = xc - CC.width / 2 + 16 * 7, yc - CC.height + 15 * 7
                d.line([(80 * K, 293 * K), (col_x, col_y)], fill=(176, 150, 100, int(255 * a)), width=K)
        anims += [remise]
        if t_enfer is not None:
            def enfer(img, u):
                if u < t_enfer:
                    return
                a = smooth((u - t_enfer) / 0.9)
                lay = Image.new("RGBA", img.size, (150, 16, 20, int(95 * a)))
                img.alpha_composite(lay)
            ecran.append(enfer)
        if t_porte is not None:
            sons.append((t_porte, "dv_porte_bois", 0.10, None))
        amb = ("amb_vent_doux", 0.05)
        cam = [(0.0, 1.06, (560, 1000)), (D, 1.30, (580, 1150))]

    elif bg.startswith("puits"):
        t_chien = _quand(ev, "chien", 0.0)
        t_botte = _quand(ev, "botte")
        t_par = _quand(ev, "pardon")
        CHN = {p: _cache(("chien", p), lambda p=p: _px_scale(_chien(p), 6)) for p in ("halete", "lape")}
        BOT = _cache("botte", lambda: _px_scale(_botte(), 6))

        def scene_puits(img, u):
            xd, yd = 196 * K, 326 * K
            if t_botte is not None and u >= t_botte:                    # la botte d'eau posée devant lui
                a = smooth((u - t_botte) / 0.5)
                _colle(img, BOT, xd - 150, yd, a)
            if t_botte is not None and u >= t_botte + 0.7:
                pose = "lape"
            else:
                pose = "halete" if int(u * 3) % 4 else "lape"           # il halète, lèche le sable mouillé
            _colle(img, CHN[pose], xd, yd)
            if t_par is not None and u >= t_par:                        # la lumière du pardon
                a = smooth((u - t_par) / 0.8)
                lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
                dl = ImageDraw.Draw(lay)
                for k_, al in ((150, 0.10), (100, 0.16), (60, 0.22)):
                    dl.polygon([(xd - k_, 0), (xd + k_, 0), (xd + k_ * 1.6, yd), (xd - k_ * 1.6, yd)],
                               fill=(255, 226, 150, int(255 * al * a)))
                img.alpha_composite(lay)
                _etincelles(img, xd, yd - 120, u, a, n=8, seed=3)
        anims += [scene_puits]
        s_h = _son("chien_halete")
        if s_h:
            sons.append((t_chien, s_h, 0.14, 2.5))
        if t_par is not None:
            sons.append((t_par, "sa_scintillement", 0.06, None))
        amb = ("amb_vent_desert", 0.05)
        cam = [(0.0, 1.0, (540, 960))]
        if t_botte is not None:
            cam.append((t_botte + 0.3, 1.14, (680, 1120)))
        cam.append((D, 1.18, (700, 1110)))

    elif bg.startswith("chevet_pov"):
        t_rev = [(0.0 if u < 0.6 else u, r) for (u, m, r) in ev if m == "reveil"]   # il sonne dès l'image 0
        t_man = _quand(ev, "manque")
        heure = t_rev[0][1].split('"')[1] if t_rev and '"' in t_rev[0][1] else "05:47"
        jour = bg.endswith("jour")

        def tel_img(sonne, manque):
            key = ("tel", sonne, manque, heure)
            def f():
                c = Px(80, 50, alpha=True)
                corps = c.mask_poly([(6, 2), (74, 2), (78, 46), (2, 46)])
                c.shape(corps, (30, 30, 40), (20, 20, 28), band=1)
                ecr = c.mask_poly([(10, 6), (70, 6), (73, 42), (7, 42)])
                if manque:
                    c.vgrad(ecr, 6, 42, (40, 40, 56), (24, 24, 36), steps=3)
                    c.text((40, 9), "08:43", (230, 230, 240), size=12, anchor="ma")
                    c.fill(c.mask_rect(10, 27, 70, 38), (200, 40, 50))
                    c.text((40, 28), "3 ALARMES", (255, 255, 255), size=8, anchor="ma")
                else:
                    c.vgrad(ecr, 6, 42, (90, 70, 200), (40, 30, 110), steps=3)
                    c.text((40, 7), "FAJR", (255, 214, 70), size=8, anchor="ma")
                    c.text((40, 16), heure, (255, 255, 255), size=16, anchor="ma")
                    c.fill(c.mask_rrect(14, 34, 36, 40, 2), (220, 60, 70)); c.fill(c.mask_rrect(44, 34, 66, 40, 2), (120, 120, 140))
                return c.img(K, rgba=True)
            return _cache(key, f)

        def tel(img, u):
            sonne = bool(t_rev) and t_rev[0][0] <= u and (t_man is None or u < t_man)
            manque = t_man is not None and u >= t_man
            im = tel_img(sonne, manque)
            x, y = 136 * K, 300 * K
            if sonne:
                v = u - t_rev[0][0]
                x += (K if int(v * 24) % 2 else -K) if (v % 1.2) < 0.8 else 0      # il vibre (un pixel)
                d = ImageDraw.Draw(img)
                for i in range(3):                                     # ondes de la sonnerie
                    p = (v * 1.2 + i / 3) % 1.0
                    rr = 190 + 120 * p
                    al = int(200 * (1 - p))
                    d.arc([x - rr, y - 100 - rr * 0.5, x + rr, y - 100 + rr * 0.5], 200, 340, fill=(255, 230, 160, al), width=K)
                _halo(img, x, y - 100, 260, (150, 130, 255), 0.25)
            _colle(img, im, x, y)
        anims += [tel]
        if t_rev:
            sons.append((t_rev[0][0], "dv_sonnerie_telephone", 0.10, (t_man or D) - t_rev[0][0]))
        amb = None if jour else ("amb_grillons_nuit", 0.05)
        cam = [(0.0, 1.12, (540, 1080)), (D, 1.26, (550, 1110))]

    elif bg.startswith("nuque"):
        t_n = _quand(ev, "noeuds")
        t_def = sorted(_tous(ev, "defait"))
        t_dh = _quand(ev, "dhikr")
        t_eau = _quand(ev, "eau")
        t_pri = _quand(ev, "priere")
        t_or = _quand(ev, "oreille")
        N = _cache("noeud", lambda: _px_scale(_noeud(False), 6))
        ND = _cache("noeud_d", lambda: _px_scale(_noeud(True), 6))
        xs = [(108 * K, 304 * K), (135 * K, 310 * K), (162 * K, 304 * K)]
        chuch = _cache("chuchote", lambda: _texte_pixel("« LA NUIT EST LONGUE… DORS. »", (226, 216, 255), (30, 20, 50), size=10, k=4))

        def noeuds(img, u):
            if t_n is None or u < t_n:
                return
            for i, (x, y) in enumerate(xs):
                ta = t_n + i * 0.7
                if u < ta:
                    continue
                a = smooth((u - ta) / 0.45)
                td = t_def[i] if i < len(t_def) else None
                if td is not None and u >= td:
                    e = smooth((u - td) / 0.7)
                    _colle(img, ND, x, y, (1 - e), ancre="centre")
                    _etincelles(img, x, y - 20, u - td, 1 - e, n=4, seed=i + 2, haut=90)
                    continue
                _halo(img, x, y, 70, (60, 20, 90), 0.5 * a)
                _colle(img, N, x, y, a, ancre="centre")
            t_chu = _quand(ev, "chuchote")                             # {pov chuchote} : pile sur le chuchotement de la voix
            fin_ch = (t_chu + 2.2) if t_chu is not None else (t_n + 3.0)   # un seul texte, puis il s'efface
            if t_n <= u < fin_ch + 0.35:
                a = smooth((u - t_n) / 0.25) * (1 - smooth((u - fin_ch) / 0.35))
                pulse = 0.85 + 0.15 * math.sin((u - t_n) * 2 * math.pi / 0.7)    # il revient avec chaque nœud
                _colle(img, chuch, 540, xs[1][1] - 134, a * pulse, ancre="centre")
        anims += [noeuds]

        def actions(img, u):
            if t_dh is not None and t_dh <= u < t_dh + 2.0:              # « الحمد لله » doré qui monte
                im = _cache("dhikr", lambda: _arabe("الحمد لله"))
                a = smooth((u - t_dh) / 0.4) * (1 - smooth((u - t_dh - 1.5) / 0.5))
                _halo(img, 540, 760 - 40 * (u - t_dh), 260, (255, 220, 140), 0.35 * a)
                _colle(img, im, 540, 760 - 40 * (u - t_dh), a, ancre="centre")
            if t_eau is not None and t_eau <= u < t_eau + 2.0:             # gouttes d'eau (ablutions)
                d = ImageDraw.Draw(img)
                rng = np.random.default_rng(9)
                a = 1 - smooth((u - t_eau - 1.5) / 0.5)
                for i in range(26):
                    x = rng.uniform(300, 780)
                    y = 500 + ((u - t_eau) * rng.uniform(700, 1000) + rng.uniform(0, 600)) % 800
                    d.rectangle([x, y, x + K, y + 3 * K], fill=(150, 210, 255, int(220 * a)))
                    d.rectangle([x - K, y + K, x + 2 * K, y + 2 * K], fill=(110, 180, 240, int(200 * a)))
            if t_pri is not None and u >= t_pri:                          # la prière : une lumière chaude
                a = smooth((u - t_pri) / 0.8)
                _halo(img, 540, 900, 700, (255, 210, 140), 0.45 * a)
            if t_or is not None and u >= t_or:                            # près de l'oreille : une ombre
                a = smooth((u - t_or) / 0.8)
                _halo(img, 196 * K, 232 * K, 120, (30, 20, 40), 0.7 * a)
        avant += [actions]
        if t_n is not None:
            sons.append((t_n, "tr_whoosh_doux", 0.05, None))
        for td in t_def:
            sons.append((td, "sa_scintillement", 0.05, None))
        if t_eau is not None:
            sons.append((t_eau, "amb_source_eau", 0.08, 1.6))
        amb = ("amb_grillons_nuit", 0.05) if bg.endswith("nuit") else None
        cam = [(0.0, 1.0, (540, 960))]
        if t_n is not None:
            cam.append((t_n + 2.2, 1.16, (540, 1130)))
        if t_pri is not None:
            cam.append((t_pri + 1.0, 1.06, (540, 1000)))
        cam.append((D, 1.10, (540, 1040)))
        cam = sorted(cam, key=lambda k_: k_[0])

    sh = Shot(debut, fin, bg, [], cam=cam, fg=False, anims=anims, anims_avant=avant, ecran=ecran,
              sons=sons, ambiance=amb, band=band)
    sh.lumieres = list(getattr(sc, "lumieres", []))
    return sh
