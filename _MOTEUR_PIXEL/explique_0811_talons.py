# DÉMONSTRATION EN IMAGE DU 08/11/2026 — Short ISL23 « Tu fais tes ablutions ? Lave tes talons ! » (format consigne +
# avertissement). Même principe que explique_0611_dette.py : le sens propre du hadith, montré en grand, avec des
# mouvements doux (jamais de secousse, de flash ni de coupe sèche). Personne de vénéré n'est dessiné : la parole du
# Prophète (paix et salut sur lui) n'est que du texte. Le Feu n'est qu'une LUEUR derrière le talon (aucune flamme sur la
# peau, aucune brûlure, aucune blessure) ; la peau du talon ne change jamais de couleur à cause d'elle.
# Code couleur de la peau (partout) : partie SÈCHE = un ton plus pâle, MATE, sans aucun reflet ; partie MOUILLÉE = un
# ton plus foncé, reflets qui glissent, gouttes. Ce qui montre le sec : le cercle pointillé jaune et le mot « SEC ».
#   {talon PETIT} / {talon}   accroche, vue à ta place : TON pied nu sur le rebord de la salle d'ablutions, le robinet
#                             coule sur les orteils et le dessus du pied, le TALON reste sec (pâle, mat) ; le cercle
#                             pointillé jaune se dessine (0,6 s) avec « SEC » ; tout se rapproche doucement (×1,08 en
#                             3 s) ; ta main fait « c'est bon » (pouce levé), le pied se retire de l'eau (1,8 s) : le
#                             talon n'a jamais été touché.
#   {talons}                  le pied de profil (talon à gauche), talon sec dans le cercle, « DES TALONS // RESTÉS
#                             SECS » ; la carte-parchemin : « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : » dès le 1er mot,
#                             puis « « MALHEUR AUX TALONS… » » mot par mot ;
#                             {talons feu} la carte se complète « À CAUSE DU FEU ! » » (FEU rouge-orangé), une lueur
#                             rouge-orangé monte du sol DERRIÈRE le talon, des braises flottent à distance, « LE FEU »
#                             sous le pied ; {talons crie} « IL L'A CRIÉ 2 OU 3 FOIS » (Boukhari 163) sous la carte.
#   {talons ongle}            le pied vu de dessus, tout mouillé, un seul coin sec grand comme un ongle sur le
#                             cou-de-pied (même taille que l'ongle du gros orteil) ; la loupe glisse dessus ;
#                             « UN COIN SEC GRAND COMME / UN ONGLE / SUR TON PIED » (Mouslim 243, pas de Feu ici) ;
#                             {talons refais} le bandeau sombre : « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : »
#                             « « RETOURNE ET FAIS BIEN TES ABLUTIONS. » » mot par mot, la flèche ↻ fait un tour
#                             autour du coin sec, puis « UNE PARTIE SÈCHE = ABLUTIONS PAS VALABLES », « LAVE LA PARTIE
#                             SÈCHE (OU REFAIS TOUT), PUIS PRIE ✓ » et « (LES AVIS DIFFÈRENT : VOIR LA DESCRIPTION) ».
#   {talons ponce}            la chute drôle : Petit (buste, paniqué, en sueur) frotte son talon des deux mains (2,5
#                             allers-retours par seconde, petite amplitude, caméra fixe), la mousse blanche grossit, le
#                             chrono défile de 0:00 à 10:00, puis « 10 MINUTES… » (aucune râpe, aucune rougeur).
#   {talons eau}              le remède : le pied de profil avec la lueur allumée ; l'eau du robinet avance des orteils
#                             au talon puis monte jusqu'aux chevilles, ta main passe UNE fois sur le talon ; la lueur
#                             s'éteint (0,8 s), petite lumière blanche sur le talon LAVÉ, le ✓ vert ; le robinet
#                             s'efface, « TOUT LE PIED, / TALON COMPRIS » (vert) et « « … ET LAVEZ-VOUS LES PIEDS /
#                             JUSQU'AUX CHEVILLES » » (CORAN 5:6, EXTRAIT).
# Zones sûres (1080 x 1920) : le grand schéma est posé de y ≈ 288 à 1248 (x + 30) ; tout ce qui compte reste à x < 870
# du dessin (x < 900 à l'écran), rien sous les sous-titres.
# Branché par explique_0811.py (import tardif dans explique.Schema._ordre et scenario._fin_anim).
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from px import Px, TAHOMA
from pxv import smooth
from explique import _titre, _fade, BLANC, JAUNE
from explique_0411 import OL, _peau, _buste, _grand, _robinet
from explique_0411b import _Base, _translucide
from explique_0611_dette import _texte_px, _lignes, _colle, _etincelle

K = 6
W, H = 170, 160                                   # le dessin (×6 = 1020 x 960)
CX = 450                                          # centre des textes (pixels d'écran du schéma) : loin des boutons
MAXW = 820
VERT = (120, 226, 132)
FEU = (255, 120, 40)
FEU_ENCRE = (214, 72, 24)
ENCRE = (62, 42, 34)
ENCRE_P = (98, 70, 52)
PAPIER = (244, 232, 200)
GRIS = (206, 208, 218)
EAU_C, EAU_M, EAU_F = (226, 242, 255), (164, 210, 248), (104, 160, 222)


def _mix(a, b, k):
    return tuple(int(x + (y - x) * k) for x, y in zip(a, b))


PEAU = _peau("PETIT")
NORM = (PEAU["b"], PEAU["s"], PEAU["h"])
SEC = (_mix(PEAU["b"], (232, 226, 216), 0.5), _mix(PEAU["s"], (204, 196, 186), 0.45))     # pâle, mat
_mo = _mix(PEAU["b"], PEAU["s"], 0.5)
MOUILLE = (_mix(_mo, (70, 110, 170), 0.12), _mix(_mix(PEAU["s"], PEAU["d"], 0.5), (60, 96, 160), 0.14),
           _mix(PEAU["h"], (220, 236, 255), 0.35))
REFLET = (250, 252, 255)
JEAN = ((62, 96, 166), (44, 70, 128), (96, 132, 200))
ROUGE_M = ((200, 50, 50), (150, 34, 40), (232, 92, 84))       # la manche du sweat de Petit

# le pied de profil (talon à gauche, orteils à droite), avant décalage / échelle
PROFIL = [(70, 92), (80, 97), (92, 102), (106, 108), (120, 113), (132, 117), (140, 121), (144, 126), (144, 131),
          (141, 135), (136, 137), (124, 138), (110, 138), (100, 136), (88, 134), (74, 134), (62, 136), (56, 138),
          (44, 138), (38, 135), (35, 129), (34, 121), (36, 113), (39, 106), (41, 96), (40, 70), (38, 40), (76, 40),
          (73, 70)]
JEAN_P = [(32, -260), (82, -260), (81, 50), (82, 58), (31, 58), (33, 50)]
Y_PIED = 95                                       # au-dessus : la jambe ; en dessous : le pied
X_TALON = 62                                      # à gauche : le talon
TALON_C = (50, 124)                               # centre du talon (cercle)
X_EAU = 118                                       # la colonne d'eau du robinet (accroche, remède)


# ---------------------------------------------------------------- petits outils
def _ligne_mots(mots, size, k, bord=None, pad=3):
    """Une ligne de texte pixel net, mot par mot : [(mot, couleur)] → [(image, x)] (x depuis le bord gauche de la
    ligne) et la largeur totale. La ligne entière est rendue d'un seul coup (espaces exacts), puis découpée en
    morceaux, un par mot (chacun dans sa couleur)."""
    f = ImageFont.truetype(TAHOMA, size)
    asc, desc = f.getmetrics()
    txt = " ".join(m for m, _ in mots)
    h = pad + asc + desc + 1 + pad

    def masque(t):                                                   # le vrai rendu bitmap (plus large que getlength)
        m = Image.new("L", (int(f.getlength(t) * 1.6) + 2 * pad + 20, h), 0)
        d = ImageDraw.Draw(m)
        d.fontmode = "1"
        d.text((pad, pad), t, font=f, fill=255, anchor="la")
        return m

    plein = masque(txt)
    bb = plein.getbbox() or (0, 0, 1, 1)
    w = bb[2] + pad
    a = np.array(plein.crop((0, 0, w, h))) > 0
    fins = [(masque(" ".join(mm for mm, _ in mots[:i + 1])).getbbox() or (0, 0, pad, 1))[2] for i in range(len(mots))]
    pleins = {}
    for _, col in mots:
        if col not in pleins:
            o = np.zeros((h, w, 4), np.uint8)
            o[a] = (*col, 255)
            pleins[col] = Image.fromarray(o, "RGBA").resize((w * k, h * k), Image.NEAREST)
    out = []
    for i, (m, col) in enumerate(mots):
        xa = 0 if i == 0 else (fins[i - 1] + 1) * k
        xb = w * k if i == len(mots) - 1 else (fins[i] + 1) * k
        out.append((pleins[col].crop((xa, 0, xb, h * k)), xa))
    return out, w * k


def _pointilles(d, cx, cy, r, a, p=1.0, ep=9, n=22):
    """Cercle en pointillés jaunes (bordés de sombre) ; p = part déjà dessinée (0 → 1, depuis le haut)."""
    A = int(255 * max(0.0, min(1.0, a)))
    if A <= 0 or p <= 0:
        return
    bb = [cx - r, cy - r, cx + r, cy + r]
    m = max(1, int(math.ceil(n * min(1.0, p))))
    for i in range(m):
        a0 = -90 + i * 360 / n
        d.arc(bb, a0 - 1.5, a0 + 360 / n * 0.55 + 1.5, fill=(20, 16, 30, A), width=ep + 8)
    for i in range(m):
        a0 = -90 + i * 360 / n
        d.arc([bb[0] + 4, bb[1] + 4, bb[2] - 4, bb[3] - 4], a0, a0 + 360 / n * 0.55, fill=(*JAUNE, A), width=ep)


def _coche(taille, col=VERT):
    """Le ✓ vert (tampon doux) : trait épais bordé de sombre, sur fond transparent."""
    t = taille
    im = Image.new("RGBA", (t + 40, t + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(20 + t * 0.08, 20 + t * 0.55), (20 + t * 0.38, 20 + t * 0.85), (20 + t * 0.95, 20 + t * 0.15)]
    d.line(pts, fill=(20, 16, 30, 255), width=int(t * 0.24), joint="curve")
    for p_ in (pts[0], pts[-1]):
        r = t * 0.12
        d.ellipse([p_[0] - r, p_[1] - r, p_[0] + r, p_[1] + r], fill=(20, 16, 30, 255))
    d.line(pts, fill=(*col, 255), width=int(t * 0.15), joint="curve")
    for p_ in (pts[0], pts[-1]):
        r = t * 0.075
        d.ellipse([p_[0] - r, p_[1] - r, p_[0] + r, p_[1] + r], fill=(*col, 255))
    return im


def _halo_doux(w, h, col, al, flou):
    m = int(flou * 2.5)
    lay = Image.new("RGBA", (int(w) + 2 * m, int(h) + 2 * m), (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([m, m, m + int(w), m + int(h)], fill=(*col, al))
    return lay.filter(ImageFilter.GaussianBlur(flou))


# ---------------------------------------------------------------- le pied de profil
class _Pied:
    """Le pied de profil (masques au dessin, 170 x 160) et son rendu selon la partie mouillée : mouillé si x >= fx et
    y >= fy (fx, fy en pixels du dessin)."""

    def __init__(s, ox=0.0, oy=0.0, e=1.0):
        c = Px(W, H, alpha=True)
        s.ox, s.oy, s.e = ox, oy, e
        P = s.P
        s.tout = c.mask_poly([P(*p) for p in PROFIL])
        s.jean = c.mask_poly([P(*p) for p in JEAN_P])
        ycut = oy + Y_PIED * e
        s.peau = s.tout & ~s.jean
        s.jambe = s.peau & (c.yy < ycut)
        s.pied = s.peau & (c.yy >= ycut)
        s.yy, s.xx = c.yy, c.xx
        m = s.tout
        s.bas2 = m & ~(np.roll(m, -1, 0) & np.roll(m, -2, 0))
        s.haut1 = m & ~np.roll(m, 1, 0)
        s.prof = np.zeros_like(m)                                     # à moins de 4 pixels du dessus (les reflets)
        for k_ in range(1, 5):
            s.prof |= m & ~np.roll(m, k_, 0)
        s.droite1 = m & ~np.roll(m, -1, 1)
        s.gauche1 = m & ~np.roll(m, 1, 1)
        top = np.where(m.any(axis=0), m.argmax(axis=0), H)
        s.top = top
        mx, my = P(57, 91)                                           # la malléole (petite bosse de la cheville)
        r1 = c.mask_ell(mx, my, 5 * e, 4 * e)
        r2 = c.mask_ell(mx, my, 6 * e, 5 * e)
        s.malleole = r2 & ~r1 & (c.yy >= my - 1) & (c.xx >= mx - 3 * e) & s.peau
        s.orteils = []
        for x in (127, 132, 137):                                    # les séparations des orteils
            xs = int(round(ox + x * e))
            y0 = int(top[xs]) if 0 <= xs < W else H
            s.orteils.append((xs, y0 + 1, y0 + 1 + max(2, int(3 * e))))
        xa, xb = int(round(ox + 139 * e)), int(round(ox + 143 * e))
        s.ongle = [(x, int(top[x]) + 1) for x in range(xa, xb) if 0 <= x < W and top[x] < H]
        rng = np.random.default_rng(23)
        s.gouttes = []
        ys, xs_ = np.where(s.peau & ~s.prof)
        for i in rng.choice(len(xs_), 26, replace=False):
            s.gouttes.append((int(xs_[i]), int(ys[i])))
        s._base = {}

    def P(s, x, y):
        return (s.ox + x * s.e, s.oy + y * s.e)

    def sur(s, x):
        """Le haut du pied (pixels du dessin) dans la colonne x, ou None."""
        x = int(round(x))
        if 0 <= x < W and s.top[x] < H:
            return int(s.top[x])
        return None

    def _statique(s, fx, fy):
        cle = (int(round(fx)), int(round(fy)))
        if cle in s._base:
            return s._base[cle]
        c = Px(W, H, alpha=True)
        mouille = s.peau & (s.xx >= cle[0]) & (s.yy >= cle[1])
        sec = s.pied & ~mouille
        norm = s.jambe & ~mouille
        for zone, (b, sh, li) in ((norm, NORM), (mouille, MOUILLE)):
            c.fill(zone, b)
            c.fill(zone & (s.bas2 | s.droite1), sh)
            c.fill(zone & s.haut1 & ~s.jean, li)
            c.fill(zone & s.gauche1 & (s.yy < s.oy + Y_PIED * s.e), li)
        c.fill(sec, SEC[0])                                          # le sec : pâle, mat, sans reflet
        c.fill(sec & s.bas2, SEC[1])
        c.dither(sec & ~s.bas2, _mix(SEC[0], (246, 242, 234), 0.5), 0.12)
        for zone, col in ((mouille, MOUILLE[1]), (norm, NORM[1]), (sec, SEC[1])):
            c.fill(s.malleole & zone, col)
        for (x, y0, y1) in s.orteils:
            for y in range(y0, y1):
                if 0 <= y < H and s.peau[y, x]:
                    c.px(x, y, MOUILLE[1] if mouille[y, x] else (SEC[1] if sec[y, x] else NORM[1]))
        for (x, y) in s.ongle:                                       # l'ongle du gros orteil
            c.px(x, y, (240, 204, 194))
            c.px(x, y + 1, (226, 182, 170))
        c.fill(s.jean, JEAN[0])
        c.fill(s.jean & s.droite1, JEAN[1])
        c.fill(s.jean & s.gauche1, JEAN[2])
        y_rev0, y_rev1 = s.oy + 47 * s.e, s.oy + 58 * s.e            # le bas retroussé
        rev = s.jean & (s.yy >= y_rev0) & (s.yy < y_rev1)
        c.fill(rev, JEAN[2])
        c.fill(rev & (s.yy < y_rev0 + 1), JEAN[1])
        c.fill(rev & s.droite1, (70, 104, 170))
        c.outline(s.tout, OL)
        s._base[cle] = (c.a.copy(), c.al.copy(), mouille)
        return s._base[cle]

    def rendu(s, fx, fy, u, sens=1.0):
        """Image (×6) du pied à l'instant u : reflets qui glissent (sens +1 : vers les orteils) sur le mouillé."""
        a, al, mouille = s._statique(fx, fy)
        c = Px(W, H, alpha=True)
        c.a[:] = a
        c.al[:] = al
        bande = ((s.xx * 1.0 - s.yy * 0.55 - 24.0 * u * sens) % 19.0) < 1.6
        c.fill(mouille & s.prof & bande, REFLET)
        c.fill(mouille & s.haut1 & (((s.xx + int(u * 9)) % 7) < 3), (214, 234, 252))
        for i, (x, y) in enumerate(s.gouttes):
            if mouille[y, x]:
                c.px(x, y, (236, 246, 255))
                c.px(x, y + 1, MOUILLE[1])
        return c.img(K, rgba=True)


# ---------------------------------------------------------------- l'élément
class Talon(_Base):
    """{talon PETIT} : accroche, vue à ta place : ton pied sous le robinet, le talon reste sec. {talons} / {talons feu} /
    {talons crie} : le talon sec de profil, la carte « MALHEUR AUX TALONS… À CAUSE DU FEU ! », la lueur derrière le
    talon. {talons ongle} / {talons refais} : le coin sec grand comme un ongle sous la loupe, « RETOURNE ET FAIS BIEN
    TES ABLUTIONS. ». {talons ponce} : Petit ponce son talon dix minutes. {talons eau} : l'eau couvre tout le pied
    jusqu'aux chevilles, la main passe une fois, la lueur s'éteint, ✓."""
    ETAPES = ("feu", "crie", "refais")
    MODES = ("accroche", "profil", "dessus", "ponce", "eau")
    # accroche
    T_CERCLE = 0.6                      # le cercle pointillé se dessine (0,6 s)
    T_POUCE = 1.15                      # la main « c'est bon »
    T_RETIRE = 1.8                      # le pied se retire de l'eau
    # profil
    Y_CARTE = 6
    T_MOTS = (0.0, 0.42, 0.72)          # « MALHEUR », « AUX », « TALONS… » (depuis {talons})
    T_FEU_MOTS = (0.0, 0.12, 0.42, 0.58, 0.85)   # « À », « CAUSE », « DU », « FEU », « ! » » (depuis {talons feu})
    T_LUEUR = 0.45                      # la lueur commence à monter (après {talons feu}), en 0,8 s
    # dessus
    T_LOUPE, D_LOUPE = 0.2, 0.85
    COIN = (78, 62)                     # le coin sec (dessin)
    T_QUOTE = (0.0, 0.55, 0.72, 0.98, 1.25, 1.45)   # « RETOURNE ET FAIS BIEN TES ABLUTIONS. »
    # remède
    T_FX = (0.05, 0.5)                  # l'eau avance des orteils au talon
    T_FY = (0.45, 0.85)                 # puis monte jusqu'aux chevilles
    T_MAIN = (0.15, 0.8)                # la main passe une fois sur le talon
    T_OK = 0.85                         # ✓, la lueur s'éteint (0,8 s)

    def __init__(s, cmd, mode="profil", who="PETIT"):
        super().__init__(cmd)
        s.mode = mode if mode in s.MODES else "profil"
        s.who = "PETIT"

    # ------------------------------------------------------------ sons (discrets)
    def sons_el(s):
        if s.mode == "profil":
            return [(s.t["feu"] + s.T_LUEUR, "imp_grondement", 0.03, None)] if "feu" in s.t else []
        if s.mode == "dessus":
            out = [(s.T_LOUPE, "tr_whoosh_doux", 0.03, None)]
            if "refais" in s.t:
                out.append((s.t["refais"] + 0.85, "sa_ting", 0.03, None))
            return out
        if s.mode == "eau":
            return [(s.T_OK, "sa_scintillement", 0.04, None)]
        return []

    def image(s, u):
        return getattr(s, "_image_" + s.mode)(u)

    # ------------------------------------------------------------ fonds
    def _fond_profil(s):
        """La salle d'ablutions de côté : mur carrelé (assombri en haut), frise verte, rebord carrelé, rigole."""
        if "fprof" in s._cache:
            return s._cache["fprof"]
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        mur = c.mask_rect(0, 0, W, 98) & tout_
        c.fill(mur, (122, 146, 158))
        for x in range(0, W, 12):
            c.fill(mur & c.mask_rect(x, 0, x + 1, 98), (100, 122, 136))
        for y in range(4, 98, 12):
            c.fill(mur & c.mask_rect(0, y, W, y + 1), (100, 122, 136))
        for x in range(2, W, 12):                                     # petit reflet sur chaque carreau
            for y in range(6, 96, 12):
                c.fill(mur & c.mask_rect(x + 1, y + 1, x + 4, y + 2), (140, 164, 176))
        fr = c.mask_rect(0, 62, W, 69) & tout_
        c.fill(fr, (42, 112, 98))
        for x in range(0, W, 6):
            c.fill(fr & c.mask_rect(x + 2, 64, x + 4, 67), (190, 214, 200))
        rebord = c.mask_rect(0, 98, W, 148) & tout_
        c.vgrad(rebord, 98, 148, (128, 122, 118), (150, 142, 134), steps=5)
        for y in (106, 118, 134):
            c.fill(rebord & c.mask_rect(0, y, W, y + 1), (110, 104, 100))
        for j, (y0, y1) in enumerate(((98, 106), (106, 118), (118, 134), (134, 148))):
            pas = (14, 18, 24, 30)[j]
            for x in range(-40 + 7 * j, W + 40, pas):
                xb = x + (x - 85) * 0.08 * j
                c.fill(rebord & c.mask_rect(xb, y0, xb + 1, y1), (110, 104, 100))
        c.fill(c.mask_rect(0, 98, W, 99) & tout_, (88, 84, 82))
        face = c.mask_rect(0, 148, W, 153) & tout_
        c.fill(face, (96, 90, 86))
        rig = c.mask_rect(0, 153, W, H) & tout_
        c.fill(rig, (40, 58, 72))
        for x in range(6, W, 23):
            c.fill(rig & c.mask_rect(x, 155, x + 6, 156), (110, 160, 200))
        c.outline(tout_, OL)
        im = c.img(K, rgba=True)
        a = np.array(im).astype(float)                               # le haut s'assombrit (les textes s'y lisent)
        f = np.clip(0.42 + 0.58 * (np.arange(im.height) / (im.height * 0.55)), 0, 1)
        a[..., :3] *= f[:, None, None]
        im = Image.fromarray(a.astype(np.uint8), "RGBA")
        s._cache["fprof"] = im
        return im

    def _fond_dessus(s):
        """Le sol carrelé vu d'en haut (pour le pied vu de dessus), bords assombris."""
        if "fdes" in s._cache:
            return s._cache["fdes"]
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        c.fill(tout_, (120, 132, 142))
        c.dither(tout_, (128, 140, 150), 0.3)
        for x in range(3, W, 15):
            c.fill(tout_ & c.mask_rect(x, 0, x + 1, H), (96, 108, 118))
        for y in range(5, H, 15):
            c.fill(tout_ & c.mask_rect(0, y, W, y + 1), (96, 108, 118))
        rig = c.mask_rect(0, 146, W, 154) & tout_
        c.fill(rig, (44, 60, 74))
        for x in range(4, W, 19):
            c.fill(rig & c.mask_rect(x, 149, x + 5, 150), (110, 160, 200))
        c.outline(tout_, OL)
        im = c.img(K, rgba=True)
        a = np.array(im).astype(float)
        yy, xx = np.mgrid[0:im.height, 0:im.width]
        v = 1 - 0.45 * np.clip(((xx - 480) / 620.0) ** 2 + ((yy - 430) / 560.0) ** 2, 0, 1)
        a[..., :3] *= v[..., None]
        s._cache["fdes"] = Image.fromarray(a.astype(np.uint8), "RGBA")
        return s._cache["fdes"]

    def _robinet_img(s):
        if "rob" not in s._cache:
            c = Px(W, H, alpha=True)
            s._cache["rob_pt"] = _robinet(c, 86, 30)
            s._cache["rob"] = c.img(K, rgba=True)
        return s._cache["rob"], s._cache["rob_pt"]

    def _eau(s, im, pied, dx, u, a=1.0, fx=None):
        """Le filet d'eau du robinet jusqu'au pied (ou jusqu'au rebord), éclaboussures douces. dx = décalage du pied
        (pixels du dessin)."""
        if a <= 0.01:
            return
        _, (wx, wy) = s._robinet_img()
        x0 = int(wx) - 1
        imp = pied.sur(x0 + 1 - dx)
        y_imp = imp if imp is not None and imp > wy else 147
        c = Px(W, H, alpha=True)
        for x in range(x0 - 1, x0 + 3):
            col = EAU_F if x in (x0 - 1, x0 + 2) else EAU_M
            c.fill(c.mask_rect(x, int(wy), x + 1, y_imp + 1), col)
        for y in range(int(wy), y_imp + 1):                          # les paquets d'eau qui descendent
            if ((y - 42.0 * u) % 7.0) < 2.0:
                c.px(x0, y, EAU_C)
                c.px(x0 + 1, y, EAU_C)
        for j in range(8):                                           # gouttes qui rebondissent (douces)
            ph = (u * 1.4 + j / 8.0) % 1.0
            sg = -1 if j % 2 else 1
            gx = x0 + 0.5 + sg * (2 + 9 * ph + (j % 3))
            gy = y_imp - 7 * math.sin(math.pi * ph) - (j % 2)
            c.px(gx, gy, EAU_C if j % 3 else EAU_M)
        for j in range(5):                                           # le film d'eau qui file vers les orteils
            ph = (u * 0.9 + j / 5.0) % 1.0
            gx = x0 + 3 + 24 * ph
            gy = pied.sur(gx - dx)
            if gy is not None and gy < 150:
                c.px(gx, gy, EAU_C)
                c.px(gx + 1, gy, EAU_M)
        lay = c.img(K, rgba=True)
        im.alpha_composite(_fade(lay, a))

    # ------------------------------------------------------------ accroche
    def _pouce(s):
        """Ta main (vue à ta place) : poing fermé, pouce levé (« c'est bon »), manche du sweat rouge qui sort par le
        bas à droite."""
        if "pouce" in s._cache:
            return s._cache["pouce"]
        c = Px(36, 46, alpha=True)
        b, sh, li = NORM
        manche = c.mask_poly([(10, 32), (25, 30), (36, 42), (36, 46), (14, 46)])
        c.shape(manche, ROUGE_M[0], shade=ROUGE_M[1], light=ROUGE_M[2], band=2, olcol=OL)
        for j in range(4):
            c.fill(c.mask_rect(13 + 3 * j, 33 + j // 2, 14 + 3 * j, 38) & manche, ROUGE_M[1])
        poing = c.mask_rrect(6, 16, 26, 33, 4)
        c.shape(poing, b, shade=sh, light=li, band=1, olcol=OL)
        for y in (20, 24, 28):                                        # les doigts repliés
            c.fill(c.mask_rect(8, y, 20, y + 1) & poing, sh)
        pouce = c.mask_rrect(16, 3, 23, 19, 3)
        c.shape(pouce, b, shade=sh, light=li, band=1, olcol=OL)
        c.fill(c.mask_rrect(17, 4, 22, 8, 2), (246, 216, 198))
        s._cache["pouce"] = c.img(K, rgba=True)
        return s._cache["pouce"]

    def _image_accroche(s, u):
        if "pied" not in s._cache:
            s._cache["pied"] = _Pied()
        pied = s._cache["pied"]
        im = s._fond_profil().copy()
        rob, _ = s._robinet_img()
        im.alpha_composite(rob)
        r = smooth((u - s.T_RETIRE) / 0.9)                           # le pied se retire de l'eau (sans avoir lavé
        dx, dy = -9.0 * r, -2.0 * r                                  # le talon)
        pim = pied.rendu(X_TALON + 2, Y_PIED, u)
        im.alpha_composite(pim, (int(dx * K), int(dy * K)))
        s._eau(im, pied, dx, u)
        tcx, tcy = (TALON_C[0] + dx) * K, (TALON_C[1] + dy) * K       # le cercle pointillé + « SEC »
        p = smooth((u - s.T_CERCLE) / 0.6)
        pulse = 0.82 + 0.18 * math.sin(2 * math.pi * (u - s.T_CERCLE))
        if p > 0:
            _translucide(im, lambda d: _pointilles(d, tcx, tcy, 132, pulse, p))
            s._pose(im, s._lab("SEC", JAUNE, 58), tcx + 6, tcy - 190, smooth((u - s.T_CERCLE - 0.3) / 0.4) * pulse)
        e = smooth((u - s.T_POUCE) / 0.45)                           # « c'est bon »
        if e > 0.01:
            po = s._pouce()
            im.alpha_composite(_fade(po, e), (640, int(960 - po.height + 10 + 70 * (1 - e))))
        z = 1 + 0.08 * smooth(u / 3.0)                               # tout se rapproche doucement
        if z > 1.001:
            big = im.resize((int(im.width * z), int(im.height * z)), Image.LANCZOS)
            cx_, cy_ = 430 * z, 640 * z
            x0, y0 = int(cx_ - 430), int(cy_ - 640)
            im = big.crop((x0, y0, x0 + im.width, y0 + im.height))
        return im

    # ------------------------------------------------------------ profil : la parole et le Feu
    def _carte(s):
        if "carte" in s._cache:
            return s._cache["carte"]
        c = Px(146, 42, alpha=True)
        feuille = c.mask_rect(7, 2, 139, 40)
        c.fill(feuille, PAPIER)
        c.dither(feuille, (234, 218, 182), 0.16)
        c.edge(feuille, (226, 206, 166), "bottom", 2)
        c.edge(feuille, (252, 244, 222), "top", 1)
        c.outline(feuille, OL)
        for x0 in (1, 138):                                           # les deux rouleaux
            r = c.mask_rrect(x0, 0, x0 + 7, 42, 3)
            c.shape(r, (216, 188, 138), shade=(172, 142, 98), light=(238, 218, 176), band=2, olcol=OL)
        s._cache["carte"] = c.img(K, rgba=True)
        return s._cache["carte"]

    def _mots(s, nom, mots, size, k, bord=None):
        cle = ("mots", nom)
        if cle not in s._cache:
            s._cache[cle] = _ligne_mots(mots, size, k, bord)
        return s._cache[cle]

    def _ecrit(s, im, nom, mots, temps, t0, u, y, size=13, k=4, bord=None, cx=CX):
        """Une ligne qui s'écrit mot par mot (temps = instants des mots depuis t0), centrée en cx, haut en y."""
        if t0 is None:
            return
        imgs, lw = s._mots(nom, mots, size, k, bord)
        x0 = cx - lw / 2
        for (w_, xo), tm in zip(imgs, temps):
            a = smooth((u - t0 - tm) / 0.25)
            if a > 0.01:
                im.alpha_composite(_fade(w_, a), (int(x0 + xo), int(y + 8 * (1 - a))))

    def _lueur(s, im, cx, cy, a, u):
        """La lueur rouge-orangé qui monte du sol DERRIÈRE le talon (la peau n'en est jamais touchée) et ses braises,
        qui flottent loin du talon."""
        if a <= 0.01:
            return
        if "lueurs" not in s._cache:
            s._cache["lueurs"] = (_halo_doux(560, 420, (220, 50, 30), 150, 55), _halo_doux(360, 300, FEU, 170, 40))
        l1, l2 = s._cache["lueurs"]
        pulse = 0.85 + 0.15 * math.sin(2 * math.pi * u / 1.8)
        _colle(im, l1, cx, cy, a * pulse)
        _colle(im, l2, cx, cy + 30, a * (0.9 + 0.1 * math.sin(2 * math.pi * u / 1.8 + 1.0)))
        braises = []
        for j in range(12):                                          # braises : à gauche et à droite du talon
            ph = (u / 3.2 + j / 12.0) % 1.0
            cote = -1 if j % 2 else 1
            bx = cx + cote * (190 + 45 * (j % 3)) + 14 * math.sin(2 * math.pi * (u / 2.6 + j * 0.37))
            by = cy + 150 - 380 * ph
            ba = a * smooth(ph / 0.15) * (1 - smooth((ph - 0.6) / 0.4))
            if ba > 0.02:
                braises.append((bx, by, ba, j))

        def dessin(d):
            for (bx, by, ba, j) in braises:
                r = 6 if j % 3 else 9
                col = (255, 210, 90) if j % 2 else FEU
                d.rectangle([bx - r - 3, by - r - 3, bx + r + 3, by + r + 3], fill=(120, 30, 20, int(120 * ba)))
                d.rectangle([bx - r, by - r, bx + r, by + r], fill=(*col, int(255 * ba)))
        _translucide(im, dessin)

    def _image_profil(s, u):
        if "pied" not in s._cache:
            s._cache["pied"] = _Pied()
        pied = s._cache["pied"]
        im = s._fond_profil().copy()
        tf = s.t.get("feu")
        tcx, tcy = TALON_C[0] * K, TALON_C[1] * K
        a_l = smooth((u - tf - s.T_LUEUR) / 0.8) if tf is not None else 0.0
        if a_l > 0:                                                  # la lueur monte du sol (derrière le pied)
            s._lueur(im, tcx, tcy + 120 * (1 - a_l), a_l, u)
        im.alpha_composite(pied.rendu(X_TALON + 2, Y_PIED, u))
        pulse = 0.82 + 0.18 * math.sin(2 * math.pi * u)
        p = smooth(u / 0.5)
        _translucide(im, lambda d: _pointilles(d, tcx, tcy, 128, pulse, p))
        s._pose(im, s._lab("SEC", JAUNE, 50), 96, tcy + 30, smooth((u - 0.25) / 0.4) * pulse)
        lab = s._cache.get("lab_secs")
        if lab is None:
            lab = s._cache["lab_secs"] = _lignes(["DES TALONS", "RESTÉS SECS"], BLANC, 50, serre=34)
        s._pose(im, lab, 330, 530, smooth((u - 0.35) / 0.4), maxw=560)
        if a_l > 0:
            s._pose(im, s._lab("LE FEU", FEU, 60), 300, 905, smooth((u - tf - s.T_LUEUR - 0.3) / 0.5), maxw=420)
        # la carte : qui parle (dès le 1er mot), puis la parole mot par mot
        carte = s._carte()
        im.alpha_composite(carte, (CX - carte.width // 2, s.Y_CARTE))
        y0 = s.Y_CARTE
        s._ecrit(im, "pro", [(m, ENCRE_P) for m in "LE PROPHÈTE (PAIX ET SALUT SUR LUI) :".split()],
                 [0.0] * 7, 0.0, u, y0 + 30, size=8, k=4)
        s._ecrit(im, "l1", [(m, ENCRE) for m in ("«", "MALHEUR", "AUX", "TALONS…")], (0.0,) + s.T_MOTS,
                 0.0, u, y0 + 84, size=13, k=4)
        s._ecrit(im, "l2", [("À", ENCRE), ("CAUSE", ENCRE), ("DU", ENCRE), ("FEU", FEU_ENCRE), ("! »", ENCRE)],
                 s.T_FEU_MOTS, tf, u, y0 + 154, size=13, k=4)
        tc = s.t.get("crie")
        if tc is not None:
            e = smooth((u - tc) / 0.45)
            s._pose(im, s._lab("IL L'A CRIÉ 2 OU 3 FOIS", GRIS, 40), CX, 292 + 12 * (1 - e), e, maxw=MAXW)
        return im

    # ------------------------------------------------------------ dessus : le coin sec grand comme un ongle
    def _pied_dessus(s):
        """Le pied vu de dessus (orteils à droite), tout mouillé, sauf un coin sec grand comme l'ongle du gros orteil
        sur le cou-de-pied ; renvoie (couleurs, opacité, masque mouillé, masque du dessus) au dessin."""
        if "pdes" in s._cache:
            return s._cache["pdes"]
        c = Px(W, H, alpha=True)
        oy = -10

        def P(x, y):
            return (x, y + oy)
        corps = c.mask_poly([P(*p) for p in ((36, 64), (58, 61), (76, 58), (96, 55), (112, 52), (118, 54), (119, 111),
                                             (112, 116), (96, 116), (76, 113), (58, 110), (36, 107))])
        doigts = [(127, 58, 11, 6.5), (125, 71, 8.5, 5), (122, 82, 7.5, 4.6), (119, 92, 6.5, 4.2), (115, 102, 5.5, 3.8)]
        ongles = [(132, 58, 3, 2.6), (130, 71, 2.4, 2), (126.5, 82, 2, 1.7), (123, 92, 1.7, 1.5), (118.5, 102, 1.4, 1.3)]
        b, sh, li = MOUILLE
        tout = corps.copy()
        c.fill(corps, b)
        for (x, y, rx, ry) in doigts:
            tout |= c.mask_ell(x, y + oy, rx, ry)
        bas = tout & ~(np.roll(tout, -1, 0) & np.roll(tout, -2, 0) & np.roll(tout, -3, 0))
        for (x, y, rx, ry) in doigts:                                 # chaque orteil, bordé d'ombre
            m = c.mask_ell(x, y + oy, rx, ry)
            c.fill(m, b)
            c.outline(m, sh)
            c.fill(m & ~np.roll(m, 1, 0), li)
        c.fill(corps & ~tout, b)
        c.fill(corps, b)
        c.fill(bas & corps, sh)
        c.fill(corps & ~np.roll(corps, 1, 0), li)
        for (x0, y0, x1, y1) in ((52, 78, 112, 60), (54, 84, 112, 72), (56, 90, 110, 84), (56, 96, 108, 94)):
            c.line(x0, y0 + oy, x1, y1 + oy, _mix(b, li, 0.45))      # les tendons, discrets
        for (x, y, rx, ry) in ongles:
            m = c.mask_ell(x, y + oy, rx, ry)
            c.fill(m, (238, 202, 192))
            c.px(int(x), int(y + oy - ry + 1), (255, 240, 236))
        sec = c.mask_ell(s.COIN[0], s.COIN[1], 3.6, 3.0)
        c.fill(sec, SEC[0])
        c.dither(sec, _mix(SEC[0], (246, 242, 234), 0.5), 0.12)
        jean = c.mask_rrect(4, 40, 50, 112, 12)
        c.fill(jean, JEAN[0])
        c.fill(jean & ~np.roll(jean, -3, 0), JEAN[1])
        c.fill(jean & ~np.roll(jean, 2, 1), JEAN[2])
        c.dither(jean, (54, 86, 152), 0.22)                           # la toile du jean
        rev = jean & ~c.mask_rrect(9, 45, 45, 107, 9)
        c.fill(rev, JEAN[2])
        c.fill(rev & ~np.roll(rev, -1, 1) & (c.xx > 30), (70, 104, 170))
        couture = c.mask_rrect(12, 48, 42, 104, 7) & ~c.mask_rrect(13, 49, 41, 103, 6)
        c.fill(couture & (((c.xx + c.yy) % 4) < 2), (150, 176, 220))  # la couture en pointillés
        for (x0, y0, x1, y1) in ((16, 60, 24, 66), (18, 84, 28, 88), (30, 70, 38, 78)):
            c.line(x0, y0, x1, y1, JEAN[1])                          # quelques plis
        c.outline(tout | jean, OL)
        mouille = tout & ~sec & ~jean
        dessus = mouille & ~bas
        s._cache["pdes"] = (c.a.copy(), c.al.copy(), mouille, dessus)
        return s._cache["pdes"]

    def _pied_dessus_img(s, u):
        a, al, mouille, dessus = s._pied_dessus()
        c = Px(W, H, alpha=True)
        c.a[:] = a
        c.al[:] = al
        bande = (((c.xx * 1.0 + c.yy * 0.4 - 20.0 * u) % 21.0) < 1.2) & (((c.yy + c.xx // 7) % 9) < 3)
        c.fill(dessus & bande, REFLET)                               # petits reflets en tirets qui glissent
        rng = np.random.default_rng(5)
        ys, xs = np.where(dessus)
        for i in rng.choice(len(xs), 30, replace=False):
            x, y = int(xs[i]), int(ys[i])
            if abs(x - s.COIN[0]) > 6 or abs(y - s.COIN[1]) > 5:
                c.px(x, y, (236, 246, 255))
                c.px(x, y + 1, MOUILLE[1])
        return c.img(K, rgba=True)

    def _loupe(s, im, src, cx, cy, a, kz=2, R=120):
        """La loupe : la scène dessous, agrandie ×2 dans un rond, cerclée de métal, manche en bas à droite."""
        if a <= 0.01:
            return
        r0 = R // kz
        box = (int(cx - r0), int(cy - r0), int(cx + r0), int(cy + r0))
        zone = src.crop(box).resize((2 * R, 2 * R), Image.NEAREST)
        if "masque_loupe" not in s._cache:
            m = Image.new("L", (2 * R, 2 * R), 0)
            ImageDraw.Draw(m).ellipse([0, 0, 2 * R - 1, 2 * R - 1], fill=255)
            s._cache["masque_loupe"] = m
        lens = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0))
        lens.paste(zone, (0, 0), s._cache["masque_loupe"])

        def dessin(d):
            A = int(255 * a)
            ux, uy = math.cos(math.radians(45)), math.sin(math.radians(45))
            hx0, hy0 = cx + ux * (R + 8), cy + uy * (R + 8)
            hx1, hy1 = cx + ux * (R + 150), cy + uy * (R + 150)
            d.line([(hx0, hy0), (hx1, hy1)], fill=(20, 16, 30, A), width=46)
            d.line([(hx0, hy0), (hx1, hy1)], fill=(110, 70, 44, A), width=32)
            d.line([(hx0 - 6, hy0 + 6), (hx1 - 6, hy1 + 6)], fill=(150, 104, 70, A), width=8)
            d.ellipse([cx - R - 16, cy - R - 16, cx + R + 16, cy + R + 16], outline=(20, 16, 30, A), width=26)
            d.ellipse([cx - R - 10, cy - R - 10, cx + R + 10, cy + R + 10], outline=(186, 194, 206, A), width=14)
            d.arc([cx - R - 10, cy - R - 10, cx + R + 10, cy + R + 10], 200, 260, fill=(246, 250, 255, A), width=8)
        _translucide(im, dessin)
        im.alpha_composite(_fade(lens, a), (int(cx - R), int(cy - R)))
        lay = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0))         # reflet du verre
        ImageDraw.Draw(lay).arc([18, 18, 2 * R - 18, 2 * R - 18], 205, 245, fill=(255, 255, 255, int(110 * a)), width=10)
        im.alpha_composite(lay, (int(cx - R), int(cy - R)))

    def _fleche_tour(s, im, cx, cy, r, p, a=1.0):
        """La flèche circulaire ↻ qui fait un tour autour du coin sec (p : 0 → 1)."""
        if p <= 0.01 or a <= 0.01:
            return
        A = int(255 * a)
        a0, a1 = -100, -100 + 310 * p
        bb = [cx - r, cy - r, cx + r, cy + r]

        def dessin(d):
            d.arc(bb, a0, a1, fill=(20, 16, 30, A), width=22)
            d.arc(bb, a0, a1, fill=(*JAUNE, A), width=12)
            t = math.radians(a1)
            px_, py_ = cx + r * math.cos(t), cy + r * math.sin(t)
            tx, ty = -math.sin(t), math.cos(t)                       # sens de la flèche
            nx, ny = math.cos(t), math.sin(t)
            pts = [(px_ + tx * 30, py_ + ty * 30), (px_ + nx * 22 - tx * 6, py_ + ny * 22 - ty * 6),
                   (px_ - nx * 22 - tx * 6, py_ - ny * 22 - ty * 6)]
            d.polygon(pts, fill=(*JAUNE, A), outline=(20, 16, 30, A))
        _translucide(im, dessin)

    def _image_dessus(s, u):
        im = s._fond_dessus().copy()
        im.alpha_composite(s._pied_dessus_img(u))
        ccx, ccy = s.COIN[0] * K + 3, s.COIN[1] * K + 3
        pulse = 0.82 + 0.18 * math.sin(2 * math.pi * u)
        _translucide(im, lambda d: _pointilles(d, ccx, ccy, 46, pulse, smooth((u - 0.1) / 0.5), ep=6, n=14))
        tr = s.t.get("refais")
        a_haut = smooth(u / 0.3) * (1 - (s._e("refais", u, 0.3) if tr is not None else 0.0))
        if a_haut > 0.01:                                            # « UN COIN SEC GRAND COMME / UN ONGLE / SUR TON PIED »
            s._pose(im, s._lab("UN COIN SEC GRAND COMME", BLANC, 50), CX, 52, a_haut, maxw=MAXW)
            s._pose(im, s._lab("UN ONGLE", JAUNE, 66), CX, 134, a_haut * smooth((u - 0.25) / 0.35), maxw=MAXW)
            s._pose(im, s._lab("SUR TON PIED", BLANC, 46), CX, 210, a_haut * smooth((u - 0.45) / 0.35), maxw=MAXW)
        e = smooth((u - s.T_LOUPE) / s.D_LOUPE)                      # la loupe glisse sur le coin sec
        lx, ly = 760 + (ccx - 760) * e, 640 + (ccy - 640) * e
        src = im.copy()
        s._loupe(im, src, lx, ly, smooth((u - s.T_LOUPE + 0.1) / 0.3))
        if tr is None:
            return im
        v = u - tr
        s._fleche_tour(im, lx, ly, 96, smooth((v - 0.1) / 0.8))
        ab = smooth(v / 0.3)                                         # le bandeau sombre de la citation
        if ab > 0.01:
            _translucide(im, lambda d: d.rounded_rectangle([CX - 430, 6, CX + 430, 236], 28,
                                                            fill=(18, 16, 34, int(215 * ab)),
                                                            outline=(255, 255, 255, int(200 * ab)), width=5))
        s._ecrit(im, "q0", [(m, (220, 214, 236)) for m in "LE PROPHÈTE (PAIX ET SALUT SUR LUI) :".split()],
                 [0.0] * 7, tr, u, 30, size=8, k=4)
        mots = [("«", BLANC), ("RETOURNE", BLANC), ("ET", BLANC), ("FAIS", BLANC), ("BIEN", BLANC)]
        s._ecrit(im, "q1", mots, (0.0,) + s.T_QUOTE[:4], tr, u, 84, size=13, k=4)
        s._ecrit(im, "q2", [("TES", BLANC), ("ABLUTIONS.", BLANC), ("»", BLANC)],
                 (s.T_QUOTE[4], s.T_QUOTE[5], s.T_QUOTE[5] + 0.3), tr, u, 156, size=13, k=4)
        la = s._cache.get("la")
        if la is None:
            la = s._cache["la"] = (_lignes(["UNE PARTIE SÈCHE =", "ABLUTIONS PAS VALABLES"], JAUNE, 34, serre=66),
                                   _lignes(["LAVE LA PARTIE SÈCHE", "(OU REFAIS TOUT), PUIS PRIE"], JAUNE, 34, serre=66),
                                   _titre("(LES AVIS DIFFÈRENT : VOIR LA DESCRIPTION)", GRIS, 24))
        l1, l2, l3 = la
        e1, e2, e3 = (smooth((v - d_) / 0.4) for d_ in (0.4, 0.8, 1.15))
        s._pose(im, l1, CX, 702 + 10 * (1 - e1), e1, maxw=MAXW)
        s._pose(im, l2, CX - 30, 812 + 10 * (1 - e2), e2, maxw=MAXW - 60)
        if e2 > 0.01:
            ck = s._cache.get("coche_p")
            if ck is None:
                ck = s._cache["coche_p"] = _coche(50)
            _colle(im, ck, CX - 30 + min(MAXW - 60, l2.width) / 2 - 4, 836, e2)
        s._pose(im, l3, CX, 900, e3, maxw=MAXW)
        return im

    # ------------------------------------------------------------ ponce : dix minutes de frottage
    def _image_ponce(s, u):
        if "pied_p" not in s._cache:
            s._cache["pied_p"] = _Pied(6, 30, 0.8)
        pied = s._cache["pied_p"]
        im = s._fond_profil().copy()
        im.alpha_composite(pied.rendu(0, 0, u * 0.6))
        hx, hy = pied.P(*TALON_C)                                    # le talon (dessin)
        osc = 2.0 * math.sin(2 * math.pi * 2.5 * u)                  # 2,5 allers-retours par seconde, petite amplitude
        c = Px(W, H, alpha=True)
        n = int(46 * smooth(u / 1.8))                                # la mousse grossit doucement
        rng = np.random.default_rng(31)
        pts = [(float(rng.uniform(-1, 1)), float(rng.uniform(-1, 1)), float(rng.uniform(1.6, 3.4))) for _ in range(46)]
        for i, (px_, py_, r) in enumerate(pts[:n]):
            rr = 9.5 * min(1.0, 0.45 + 0.55 * smooth(u / 1.8))
            x, y = hx + px_ * rr, hy + py_ * rr * 0.8
            m = c.mask_ell(x, y, r, r)
            c.fill(m, (250, 252, 255))
            c.edge(m, (206, 214, 228), "bottom", 1)
            c.px(x - r * 0.4, y - r * 0.4, (255, 255, 255))
        for j in range(6):                                           # des bulles qui montent lentement
            ph = (u / 2.4 + j / 6.0) % 1.0
            if n > 10:
                x, y = hx - 8 + 4 * j + 2 * math.sin(6 * ph + j), hy - 8 - 26 * ph
                m = c.mask_ell(x, y, 1.6, 1.6)
                c.outline(m, (230, 240, 252))
        for k_, (dxm, dym, ys) in enumerate(((-9, -2, 104), (6, 2, 124))):   # les deux avant-bras (ils entrent par la
            mx, my = hx + dxm + osc * (1 if k_ else -1), hy + dym            # gauche), les mains sur le talon
            manche = c.mask_poly([(-2, ys - 6), (-2, ys + 6), (mx - 5, my + 4), (mx - 5, my - 4)])
            c.shape(manche, ROUGE_M[0] if k_ else ROUGE_M[1], shade=ROUGE_M[1], light=ROUGE_M[2], band=1, olcol=OL)
            poignet = c.mask_poly([(mx - 9, my - 4), (mx - 5, my - 4), (mx - 5, my + 4), (mx - 9, my + 4)]) & manche
            c.fill(poignet, ROUGE_M[2])                                  # le bord de la manche
            main = c.mask_ell(mx, my, 5.5, 4.5)
            c.shape(main, NORM[0], shade=NORM[1], light=NORM[2], band=1, olcol=OL)
            for j in range(3):
                c.px(mx - 2 + 2 * j, my + 2, NORM[1])
        im.alpha_composite(c.img(K, rgba=True))
        bu = s._cache.get("buste")                                   # Petit en médaillon : paniqué, en sueur
        if bu is None:
            b0 = _grand(_buste("PETIT", "peur", sweat=True)[0], 10)
            cad = Image.new("RGBA", (b0.width + 40, b0.height + 30), (0, 0, 0, 0))
            dc = ImageDraw.Draw(cad)
            dc.rounded_rectangle([0, 0, cad.width - 1, cad.height - 1], 26, fill=(20, 16, 30, 255))
            dc.rounded_rectangle([7, 7, cad.width - 8, cad.height - 8], 20, fill=(236, 226, 196, 255))
            cad.alpha_composite(b0, (20, cad.height - b0.height - 7))
            m = Image.new("L", cad.size, 0)
            ImageDraw.Draw(m).rounded_rectangle([7, 7, cad.width - 8, cad.height - 8], 20, fill=255)
            bord = Image.new("RGBA", cad.size, (0, 0, 0, 0))
            ImageDraw.Draw(bord).rounded_rectangle([0, 0, cad.width - 1, cad.height - 1], 26, outline=(20, 16, 30, 255),
                                                    width=8)
            out = Image.new("RGBA", cad.size, (0, 0, 0, 0))
            out.paste(cad, (0, 0), m)
            out.alpha_composite(bord)
            bu = s._cache["buste"] = out
        im.alpha_composite(bu, (548, 20 + int(4 * math.sin(2 * math.pi * u / 1.4))))
        v = 600 * smooth(min(1.0, u / 1.6))                          # le chrono : 0:00 → 10:00
        txt = "%d:%02d" % (int(v // 60), int(v % 60))
        _translucide(im, lambda d: d.rounded_rectangle([560, 392, 770, 486], 18, fill=(18, 16, 34, 225),
                                                       outline=(255, 255, 255, 220), width=5))
        ch = s._cache.get(("chrono", txt))
        if ch is None:
            ch = s._cache[("chrono", txt)] = _texte_px(txt, BLANC, 15, k=5, pad=1)
        im.alpha_composite(ch, (int(665 - ch.width / 2), int(439 - ch.height / 2)))
        s._pose(im, s._lab("10 MINUTES…", JAUNE, 50), 665, 548, smooth((u - 1.65) / 0.4), maxw=380)
        return im

    # ------------------------------------------------------------ eau : le remède
    def _main_passe(s):
        """Ta main de profil, doigts vers la droite (elle passe une fois sur le talon), manche rouge à gauche."""
        if "mainp" in s._cache:
            return s._cache["mainp"]
        c = Px(62, 22, alpha=True)
        b, sh, li = NORM
        manche = c.mask_poly([(0, 3), (24, 5), (25, 19), (0, 21)])
        c.shape(manche, ROUGE_M[0], shade=ROUGE_M[1], light=ROUGE_M[2], band=1, olcol=OL)
        c.fill(c.mask_rect(20, 4, 25, 20) & manche, ROUGE_M[1])
        main = c.mask_poly([(24, 7), (40, 6), (52, 8), (60, 11), (59, 14), (48, 16), (36, 18), (24, 18)])
        c.shape(main, b, shade=sh, light=li, band=1, olcol=OL)
        for y in (11, 14):
            c.fill(c.mask_rect(42, y, 58, y + 1) & main, sh)
        pouce = c.mask_poly([(30, 7), (40, 2), (45, 3), (38, 9)])
        c.shape(pouce, b, shade=sh, light=li, band=1, olcol=OL)
        s._cache["mainp"] = c.img(K, rgba=True)
        return s._cache["mainp"]

    def _image_eau(s, u):
        if "pied" not in s._cache:
            s._cache["pied"] = _Pied()
        pied = s._cache["pied"]
        im = s._fond_profil().copy()
        tcx, tcy = TALON_C[0] * K, TALON_C[1] * K
        ok = smooth((u - s.T_OK) / 0.8)                              # la lueur s'éteint en douceur
        s._lueur(im, tcx, tcy, 1 - ok, u + 3.0)
        e_x = smooth((u - s.T_FX[0]) / (s.T_FX[1] - s.T_FX[0]))
        e_y = smooth((u - s.T_FY[0]) / (s.T_FY[1] - s.T_FY[0]))
        fx = (X_TALON + 2) + (30 - (X_TALON + 2)) * e_x              # l'eau avance jusqu'au talon…
        fy = Y_PIED + (80 - Y_PIED) * e_y                            # … puis monte jusqu'aux chevilles
        im.alpha_composite(pied.rendu(fx, fy, u, sens=-1.0 if e_x < 1 else 1.0))
        a_rob = 1 - smooth((u - s.T_OK - 0.1) / 0.4)                 # le robinet se ferme et s'efface
        if a_rob > 0.01:
            rob, _ = s._robinet_img()
            im.alpha_composite(_fade(rob, a_rob))
            s._eau(im, pied, 0, u, a_rob)
        m0, m1 = s.T_MAIN                                            # la main passe UNE fois sur le talon
        if m0 - 0.2 < u < m1 + 0.4:
            f = smooth((u - m0) / (m1 - m0))
            am = smooth((u - m0 + 0.2) / 0.25) * (1 - smooth((u - m1) / 0.35))
            mp = s._main_passe()
            mx = -60 + 230 * f
            my = tcy - 70 + 25 * math.sin(math.pi * f)
            im.alpha_composite(_fade(mp, am), (int(mx), int(my)))
        if ok > 0.01:                                                # le talon LAVÉ : petite lumière blanche douce
            if "blanc" not in s._cache:
                s._cache["blanc"] = _halo_doux(170, 130, (255, 255, 240), 45, 30)
            _colle(im, s._cache["blanc"], tcx, tcy, ok * (0.8 + 0.2 * math.sin(2 * math.pi * u / 1.6)))
            etoiles = [(tcx - 50, tcy - 40, 5, 0.0), (tcx + 40, tcy - 10, 4, 0.33), (tcx - 10, tcy + 40, 4, 0.66)]
            _translucide(im, lambda d: [_etincelle(d, x_, y_, r_, ok * (0.7 + 0.3 * math.sin(
                2 * math.pi * (u / 1.6 + ph_)))) for (x_, y_, r_, ph_) in etoiles])
            ck = s._cache.get("coche")
            if ck is None:
                ck = s._cache["coche"] = _coche(130)
            e = smooth((u - s.T_OK) / 0.45)
            ck_ = ck.resize((int(ck.width * (1.15 - 0.15 * e)), int(ck.height * (1.15 - 0.15 * e))), Image.LANCZOS)
            _colle(im, ck_, 130, 560, e)
        et = smooth((u - s.T_OK - 0.1) / 0.4)
        if et > 0.01:
            ti = s._cache.get("titre_eau")
            if ti is None:
                ti = s._cache["titre_eau"] = _lignes(["TOUT LE PIED,", "TALON COMPRIS"], VERT, 62, serre=34)
            s._pose(im, ti, CX, 310 + 14 * (1 - et), et, maxw=MAXW)   # sous « ABONNE-TOI » (fin)
        ec = smooth((u - s.T_OK - 0.35) / 0.4)
        if ec > 0.01:
            ci = s._cache.get("cite_eau")
            if ci is None:
                ci = s._cache["cite_eau"] = _lignes(["« … ET LAVEZ-VOUS LES PIEDS", "JUSQU'AUX CHEVILLES »"], BLANC, 38,
                                                    serre=28)
            s._pose(im, ci, CX, 474, ec, maxw=MAXW)
            s._pose(im, s._lab("(CORAN 5:6, EXTRAIT)", GRIS, 30), CX, 560, ec, maxw=MAXW)
        return im


# ---------------------------------------------------------------- branchement (via explique_0811.py)
CLES = ("talon", "talons")


def _norm(m):
    return m.lower().replace("é", "e").replace("è", "e").replace("ê", "e")


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique_0811.ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""

    def dernier(mode):
        return next((it["el"] for it in reversed(schema._visibles(t + 0.01))
                     if isinstance(it["el"], Talon) and it["el"].mode == mode), None)

    def u_de(el):
        return t - next(it["t_in"] for it in schema.items if it["el"] is el)

    def etape(nom, mode):
        el = dernier(mode)
        if el is None:
            el = Talon(brut, mode)
            schema._ajoute(t, el)
        el.t[nom] = u_de(el)

    if k == "talon":
        schema._ajoute(t, Talon(brut, "accroche"))
    elif k == "talons":
        if sous in ("feu", "crie"):
            etape(sous, "profil")
        elif sous == "refais":
            etape("refais", "dessus")
        elif sous == "ongle":
            schema._ajoute(t, Talon(brut, "dessus"))
        elif sous == "ponce":
            schema._ajoute(t, Talon(brut, "ponce"))
        elif sous == "eau":
            schema._ajoute(t, Talon(brut, "eau"))
        else:
            schema._ajoute(t, Talon(brut, "profil"))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "talon":
        return t + 3.0
    if k == "talons":
        return t + dict(feu=1.6, crie=1.2, ongle=1.4, refais=1.6, ponce=2.0, eau=2.2).get(sous, 1.5)
    return None
