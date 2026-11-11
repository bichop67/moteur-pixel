# BRIQUES RÉUTILISABLES (09/11/2026) — des démonstrations en image RÉGLÉES DEPUIS LE SCÉNARIO : un nouveau sujet
# s'écrit en texte, sans nouveau code. À préférer à une animation sur mesure (une animation sur mesure = 600 à 900
# lignes de code par Short ; une brique = une ligne de scénario). Le sur-mesure reste permis pour l'ACCROCHE.
#
# Règle commune : la 1re balise CRÉE la brique avec son contenu ; les suivantes ({brique action …}) la font évoluer
# pile sur le mot. Si on revient sur le schéma après un retour à la scène, la brique reprend où elle en était.
# Textes : écrits entre guillemets, mis en majuscules tout seuls ; « // » = 2e ligne plus petite ; ﷺ est écrit en
# toutes lettres. Tous les mouvements sont doux (fondus, glissés) : aucune secousse, aucun flash.
#
#   LISTE     {liste "SUR TON PÈRE" "SUR TA MÈRE" "PAR ALLAH"}      lignes au tableau noir ({liste nuit …} : fond sombre)
#             {liste titre "LES SERMENTS" "A" "B"}                  le 1er texte est le titre (jaune)
#             {liste + "SUR TA VIE"}  {liste barre 1 2}  {liste coche 3}  {liste or 3}  {liste efface 1}
#             {liste note "… OU TU TE TAIS"}                        (sans numéro = la dernière ligne ; « tout » = toutes)
#   CITATION  {citation "LE PROPHÈTE ﷺ A DIT :" "« MALHEUR AUX TALONS… À CAUSE DU FEU ! »"}   cadre doré, coupée seule
#             {citation + "« RETOURNE ET FAIS BIEN TES ABLUTIONS »"}  {citation note "= LAVE TOUT LE PIED"}
#             (la source reste la balise {source "MOUSLIM 243"} habituelle)
#   JAUGE     {jauge "COLÈRE" 100 -> 0}        un tube qui se vide / se remplit ; + PETIT : son visage suit le niveau
#             {jauge -> 40}  {jauge fin "CALME"}     options : % (affiche la valeur), inverse (haut = bien), max 40
#   FOCUS     {focus telephone "TON ÉCRAN"}    gros plan sur un objet (74 icônes, dessins de OBJETS, ou un perso :
#             {focus PETIT triste "TOI"})  ;  {focus entoure bas "SEC"} (haut, bas, gauche, droite, centre ou 30 70)
#             {focus ok "LAVÉ"}  {focus non "INTERDIT"}  {focus texte "…"}
#   VERSUS    {versus pouce_bas "MAIN GAUCHE" pouce "MAIN DROITE"}   deux cartes côte à côte (objet facultatif)
#             {versus non}  {versus oui}       (+ gauche / droite pour viser l'autre carte ; + titre "…" à la création)
#   BULLES    {bulles PETIT "AL-HAMDOU LILLAH"}  {bulles GRAND "YARHAMOUKA ALLAH"}   formules qui se répondent
#             options : or (la bonne formule), vide (pas de réponse), un visage (content…), nouveau (repart de zéro)
#   TRAJET    {trajet "SA VILLE" -> "LE BON PAYS" PETIT}     une route, quelqu'un qui avance (ou un point lumineux)
#             {trajet avance 50}  {trajet etape 30 "DHUHR"}  {trajet stop "IL MEURT ICI"}  {trajet arrive}
#   GRILLE    {grille 40 "JOURS"}              N cases à compter pour de vrai (40 jours, 5 prières, 3 fois…)
#             {grille coche 3}  {grille barre 40}  {grille vide}
#   + sur TOUTES les briques : {<brique> lueur rouge} (avertissement, monte du bas), {… lueur or} (lumière, descend
#     du haut), {… lueur vert}, {… lueur fin}
#
# Ajouter un OBJET (pour focus / versus / trajet) : une petite fonction qui renvoie un dessin Px, décorée par
# @objet("nom") — voir « goutte » plus bas. C'est le seul code qu'un nouveau sujet peut demander (30 à 80 lignes).
# Branché dans explique.Schema._ordre (CLES_BRIQUES) et scenario._fin_anim. Les VOP n'utilisent aucune de ces clés.
import math
import re
import unicodedata

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import cast
import objets
import pxv
from px import Px
from pxv import smooth
from explique import _titre, _fade, autocollant, coupe, BLANC, JAUNE
from explique_0411 import OL, _buste, _grand, _sprite, _goutte
from explique_0411b import _Base, _bulle, _translucide, ROUGE, ORANGE, OR_, VERT

MAXW = 880                                       # largeur maximale d'un texte (loin des bords et des boutons TikTok)
LUEURS = dict(rouge=((255, 72, 40), "bas"), orange=((255, 150, 60), "bas"), vert=((110, 226, 130), "bas"),
              bleu=((130, 190, 255), "haut"), **{"or": ((255, 214, 110), "haut")})


def _norm(m):
    m = unicodedata.normalize("NFD", m.lower())
    return "".join(ch for ch in m if not unicodedata.combining(ch))


def _propre(txt):
    """Texte d'écran : ﷺ en toutes lettres (la police des titres ne l'a pas), majuscules."""
    return txt.replace("ﷺ", "(paix et salut sur lui)").upper().strip()


def _jetons(reste):
    """Le contenu d'une balise, dans l'ordre : ("t", texte entre guillemets) ou ("m", mot)."""
    return [("t", m.group(1)) if m.group(0).startswith('"') else ("m", m.group(0))
            for m in re.finditer(r'"([^"]*)"|[^\s"]+', reste)]


def _nombre(m):
    try:
        return float(m.replace(",", "."))
    except ValueError:
        return None


def _mel(a, b, f):
    return tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))


def _clair(c, k=0.35):
    return tuple(int(v + (255 - v) * k) for v in c)


def _degrade(mauvais):
    """Vert (0) → jaune (0,5) → rouge (1)."""
    if mauvais < 0.5:
        return _mel((96, 214, 124), (255, 214, 70), mauvais * 2)
    return _mel((255, 214, 70), (240, 76, 66), (mauvais - 0.5) * 2)


# ---------------------------------------------------------------- objets (dessins maison, en plus des 74 icônes)
OBJETS = {}


def objet(nom):
    """Décorateur : enregistre un dessin (fonction sans argument → image RGBA en pixels du dessin, non agrandie)."""
    def pose(f):
        OBJETS[_norm(nom)] = f
        return f
    return pose


@objet("goutte")
def _obj_goutte():
    return _goutte((120, 190, 255), k=1, w=9, h=13)


@objet("chien")
def _obj_chien():
    """Un chien debout, de profil (le sprite d'animaux.py) : {focus chien "OUAF ! OUAF !"} (ISL36, 09/11/2026)."""
    import animaux
    return animaux.chien(robe=(104, 78, 60), pose="debout")[0].img()


@objet("mouche")
def _obj_mouche():
    """Une mouche vue de dessus : {versus … mouche "COMME UNE MOUCHE"} (ISL40, 10/11/2026)."""
    lignes = [
        "...a.......a...",
        "....a.rnr.a....",
        ".....rnnnr.....",
        ".a...nnnnn...a.",
        "..aannnnnnnaa..",
        "..wwnnnnnnnww..",
        ".wwwwnnnnnwwww.",
        "wwwwwnnnnnwwwww",
        "wwwwwannnawwwww",
        ".wwwa.nnn.awww.",
        "..wa...n...aw..",
        "..a.........a..",
    ]
    pal = {"n": (38, 40, 50, 255), "a": (20, 20, 26, 255), "r": (176, 44, 44, 255), "w": (200, 226, 246, 200)}
    im = Image.new("RGBA", (len(lignes[0]), len(lignes)), (0, 0, 0, 0))
    for y, ligne in enumerate(lignes):
        for x, c in enumerate(ligne):
            if c in pal:
                im.putpixel((x, y), pal[c])
    return im


def est_objet(nom):
    return _norm(nom) in OBJETS or _norm(nom) in objets.ICONES or nom.upper() in cast.CAST


def objet_img(nom, face="neutre"):
    n = _norm(nom)
    if n in OBJETS:
        return OBJETS[n]()
    if n in objets.ICONES:
        return objets.icone(n).img(1)
    if nom.upper() in cast.CAST:
        return _buste(nom.upper(), face if face in FACES() else "neutre")[0]
    return None


def FACES():
    import explique
    return explique.cast_faces()


def _agrandi(im, haut, large):
    k = max(1, min(int(haut // im.height), int(large // im.width)))
    return im.convert("RGBA").resize((im.width * k, im.height * k), Image.NEAREST)


def _icone(nom, k=5, r=4):
    return autocollant(objets.icone(nom).img(k), r=r, ombre=False)


# ---------------------------------------------------------------- fonds (pixel art, agrandis x6)
def _fond_nuit(W, H):
    c = Px(W, H, alpha=True)
    m = c.mask_rrect(1, 1, W - 1, H - 1, 6)
    c.vgrad(m, 1, H - 1, (42, 46, 90), (20, 20, 46), steps=7)
    c.fill(m & ~c.mask_rrect(3, 3, W - 3, H - 3, 5), (96, 106, 176))
    c.outline(m, OL)
    return c.img(6, rgba=True)


def _fond_cadre(W, H):
    c = Px(W, H, alpha=True)
    m = c.mask_rrect(1, 1, W - 1, H - 1, 6)
    c.vgrad(m, 1, H - 1, (48, 38, 76), (22, 18, 42), steps=7)
    c.fill(m & ~c.mask_rrect(3, 3, W - 3, H - 3, 5), (218, 174, 80))                     # cadre doré
    c.fill(c.mask_rrect(5, 5, W - 5, H - 5, 4) & ~c.mask_rrect(6, 6, W - 6, H - 6, 3), (128, 98, 52))
    for (x, y) in ((8, 8), (W - 9, 8), (8, H - 9), (W - 9, H - 9)):                      # clous des coins
        c.fill(c.mask_rect(x - 1, y - 1, x + 2, y + 2), (246, 214, 130))
    c.outline(m, OL)
    return c.img(6, rgba=True)


def _fond_tableau(W, H):
    """Le tableau noir de la classe (même dessin que le tableau des serments du 07/11)."""
    c = Px(W, H, alpha=True)
    yb = H - 9
    tout_ = c.mask_rrect(1, 1, W - 1, H - 3, 4)
    c.shape(tout_, (150, 104, 66), shade=(110, 74, 46), light=(186, 138, 94), band=2, olcol=OL)
    for y in range(6, H - 4, 7):                                                         # le grain du bois
        c.fill(c.mask_rect(1, y, W - 1, y + 1) & tout_ & ~c.mask_rect(4, 4, W - 4, yb + 1), (136, 94, 58))
    tab = c.mask_rect(4, 4, W - 4, yb)
    c.vgrad(tab, 4, yb, (44, 70, 62), (32, 54, 48), steps=5)
    for (x, y, rx, ry) in ((34, 24, 26, 4), (132, 60, 24, 3), (46, H - 42, 30, 4), (128, H - 24, 22, 3)):
        c.dither(c.mask_ell(x, y, rx, ry) & tab, (52, 80, 71), 0.16)                     # traces de craie effacée
    c.fill(c.mask_rect(4, 4, W - 4, 5), (24, 40, 36))
    c.fill(c.mask_rect(4, 4, 5, yb), (24, 40, 36))
    auget = c.mask_rect(2, yb, W - 2, yb + 5)
    c.shape(auget, (160, 112, 72), shade=(116, 78, 48), light=(196, 146, 100), band=1, sdir="bottom", olcol=OL)
    c.shape(c.mask_rect(124, yb - 3, 132, yb), (244, 244, 234), shade=(206, 206, 196), band=1, olcol=OL)
    c.shape(c.mask_rect(24, yb - 5, 40, yb), (178, 150, 110), shade=(140, 116, 82), band=1, olcol=OL)
    c.fill(c.mask_rect(24, yb - 2, 40, yb), (70, 76, 96))
    return c.img(6, rgba=True)


FONDS = dict(nuit=_fond_nuit, cadre=_fond_cadre, tableau=_fond_tableau)
_FONDS = {}


# ---------------------------------------------------------------- socle commun
class _Brique(_Base):
    PW_, PH_ = 170, 150                          # x6 = 1020 x 900 pixels d'écran
    ACTIONS = ("lueur",)
    AUTO = False                                 # True : pas de balise de création (chaque balise ajoute quelque chose)
    FOND = "nuit"

    def __init__(s, cmd, textes=(), mots=(), jetons=()):
        super().__init__(cmd)
        s.fond = next((m for m in map(_norm, mots) if m in FONDS), s.FOND)
        s.lueurs = []                            # (u, couleur ou None)
        s._sons = []

    # -- événements ({brique action …} sur un mot) ; u < 0 : déjà fait avant ce plan
    def evt(s, u, action, textes, mots):
        if action == "lueur":
            m = [_norm(x) for x in mots]
            s.lueurs.append((u, None if any(x in ("fin", "stop") for x in m)
                             else next((x for x in m if x in LUEURS), "rouge")))
            return True
        return False

    def reprise(s):
        """La brique revient après un retour à la scène : ses animations d'ouverture sont déjà faites."""

    def son(s, u, nom, g=0.03):
        if u >= 0:
            s._sons.append((u, nom, g, None))

    def sons_el(s):
        return list(s._sons)

    # -- petits outils d'image
    @staticmethod
    def _av(t0, u, d=0.35, dec=0.0):
        """Avancement doux 0 → 1 depuis l'instant t0 (None : jamais ; négatif : déjà fait)."""
        if t0 is None:
            return 0.0
        if t0 < 0:
            return 1.0
        return smooth((u - t0 - dec) / d) if u >= t0 + dec else 0.0

    def _bloc(s, lignes, col=BLANC, size=48):
        cle = ("bloc", tuple(lignes), col, size)
        if cle not in s._cache:
            s._cache[cle] = autocollant(pxv.big_title([(l_, col) for l_ in lignes], size=size), r=3, ombre=False)
        return s._cache[cle]

    def _mets(s, im, lab, x, y, a=1.0, maxw=MAXW):
        """Colle lab centré en (x, y), réduit s'il est trop large, sans sortir du cadre ; renvoie (x0, y0, w, h)."""
        if lab.width > maxw:
            s._retreci = min(getattr(s, "_retreci", 1.0), maxw / lab.width)     # pour controle() : texte trop long
            cle = ("r", id(lab), int(maxw))
            if cle not in s._cache:
                k_ = maxw / lab.width
                s._cache[cle] = lab.resize((int(lab.width * k_), max(1, int(lab.height * k_))), Image.LANCZOS)
            lab = s._cache[cle]
        x0 = int(max(10, min(im.width - lab.width - 10, x - lab.width / 2)))
        y0 = int(max(6, min(im.height - lab.height - 6, y - lab.height / 2)))
        if a > 0.01:
            im.alpha_composite(_fade(lab, a), (x0, y0))
        return x0, y0, lab.width, lab.height

    def _ic(s, nom, k=5, r=4, ombre=False):
        cle = ("ic", nom, k, r, ombre)
        if cle not in s._cache:
            s._cache[cle] = autocollant(objets.icone(nom).img(k), r=r, ombre=ombre)
        return s._cache[cle]

    def _halo(s, w, h, col, al=150, flou=34):
        cle = ("halo", int(w), int(h), col, al)
        if cle not in s._cache:
            lay = Image.new("RGBA", (int(w + 4 * flou), int(h + 4 * flou)), (0, 0, 0, 0))
            ImageDraw.Draw(lay).ellipse([2 * flou, 2 * flou, 2 * flou + w, 2 * flou + h], fill=(*col, al))
            s._cache[cle] = lay.filter(ImageFilter.GaussianBlur(flou))
        return s._cache[cle]

    def _pose_halo(s, im, x, y, w, h, col, a, al=150):
        if a > 0.01:
            lay = s._halo(w, h, col, al)
            x0, y0 = int(x - lay.width / 2), int(y - lay.height / 2)
            box = (max(0, -x0), max(0, -y0), min(lay.width, im.width - x0), min(lay.height, im.height - y0))
            if box[2] > box[0] and box[3] > box[1]:
                im.alpha_composite(_fade(lay.crop(box), a), (max(0, x0), max(0, y0)))

    def _image_fond(s):
        cle = (s.fond, s.PW_, s.PH_)
        if cle not in _FONDS:
            _FONDS[cle] = FONDS[s.fond](s.PW_, s.PH_)
        return _FONDS[cle]

    def _lueur(s, im, u):
        """{… lueur rouge} : une lumière douce qui monte du bas (avertissement) ou descend du haut (or : pardon)."""
        if not s.lueurs:
            return
        cur, a = None, 0.0
        for (t0, nom) in s.lueurs:
            if t0 > u:
                break
            if nom is None:
                a = a * (1 - s._av(t0, u, 0.6))
            else:
                cur, a = nom, s._av(t0, u, 0.8)
        if cur is None or a <= 0.01:
            return
        cle = ("lueur", cur)
        if cle not in s._cache:
            col, cote = LUEURS[cur]
            W, H = im.size
            yy = np.linspace(0.0, 1.0, H)[:, None]
            f = (yy if cote == "bas" else 1 - yy) ** 2.2
            arr = np.zeros((H, W, 4), np.uint8)
            arr[..., :3] = col
            arr[..., 3] = (f * 170 * (np.array(s._image_fond())[..., 3] / 255.0)).astype(np.uint8)
            s._cache[cle] = Image.fromarray(arr, "RGBA")
        im.alpha_composite(_fade(s._cache[cle], a * (0.84 + 0.16 * math.sin(2 * math.pi * u / 2.8))))

    def dessine(s, im, u):
        pass

    def image(s, u):
        im = s._image_fond().copy()
        s.dessine(im, u)
        s._lueur(im, u)
        return im

    @classmethod
    def duree(cls, action, textes, mots):
        return 1.0


# ---------------------------------------------------------------- {liste …}
class Liste(_Brique):
    ACTIONS = ("+", "barre", "coche", "or", "efface", "note", "lueur")
    FOND = "tableau"
    COUPE = None                                 # nombre de caractères avant de couper une ligne (None : jamais)
    COL_TITRE, K_TITRE = JAUNE, 0.92
    T0, ECART = 0.15, 0.12                       # les lignes de départ arrivent l'une après l'autre
    PAS = 1.72                                   # écart entre deux lignes (en tailles de lettres)

    def __init__(s, cmd, textes=(), mots=(), jetons=()):
        super().__init__(cmd, textes, mots, jetons)
        textes = [_propre(x) for x in textes]
        s.titre = None
        if "titre" in map(_norm, mots) and textes:
            s.titre, textes = textes[0], textes[1:]
        s.lignes = []
        s.note = None                            # (texte, u)
        s._mots = [_norm(m) for m in mots]       # les mots HORS guillemets (un « QUI » dans le texte cité n'en est pas un)
        s._depart(textes)

    def _depart(s, textes):
        for x in textes:
            s._plus(x, None)

    def _plus(s, txt, u):
        """Ajoute une ligne (u = None : ligne de départ ; u < 0 : déjà là ; sinon elle arrive à l'instant u)."""
        for l_ in (coupe(txt, s.COUPE) if s.COUPE else [txt]):
            n = len(s.lignes)
            if u is None:
                t, o = s.T0 + s.ECART * n, None
            elif u < 0:
                t, o = -9.0, None
            else:
                t, o = u + 0.15 * sum(1 for L in s.lignes if L["o"] == u), u
            s.lignes.append(dict(txt=l_, t=t, o=o, barre=None, coche=None, or_=None, efface=None))

    def reprise(s):
        for L in s.lignes:
            L["t"] = -9.0

    def _cibles(s, mots):
        m = [_norm(x) for x in mots]
        if "tout" in m or "toutes" in m:
            return list(range(len(s.lignes)))
        out = [int(x) - 1 for x in m if x.isdigit() and 1 <= int(x) <= len(s.lignes)]
        return out or ([len(s.lignes) - 1] if s.lignes else [])

    def evt(s, u, action, textes, mots):
        if action == "+":
            for x in textes:
                s._plus(_propre(x), u)
            s.son(u, "sa_ting", 0.025)
        elif action in ("barre", "coche", "or", "efface"):
            cle = "or_" if action == "or" else action
            for j, i in enumerate(s._cibles(mots)):
                s.lignes[i][cle] = (u + 0.25 * j) if u >= 0 else -9.0
                s.son(u + 0.25 * j, "imp_tampon" if action == "barre" else "sa_scintillement" if action == "or"
                      else "sa_ting", 0.02 if action == "barre" else 0.035)
        elif action == "note":
            s.note = (_propre(textes[0]) if textes else "", u)
        else:
            return super().evt(u, action, textes, mots)
        return True

    @staticmethod
    def _poids(L):
        return 1 + 0.7 * L["txt"].count("//")                       # « A // b » : une 2e ligne plus petite

    TITRE_2_LIGNES = False                       # True : un titre trop long passe sur deux lignes au lieu d'être réduit
    PLUS_TITRE = 0.55                            # place de la 2e ligne du titre (en écarts de lignes)

    def _taille_pour(s, plus=0.0):
        n = sum(s._poids(L) for L in s.lignes) + (1.1 if s.titre else 0) + (1.15 if s.note else 0) + plus
        size = 86 if n <= 3 else 78 if n <= 4.2 else 72 if n <= 5.2 else 66 if n <= 6.3 else 60 if n <= 7.3 \
            else 54 if n <= 8.3 else 46
        haut = s.PH_ * 6 - (150 if s.fond == "tableau" else 130)
        while size > 26 and size * s.PAS * n > haut:
            size -= 2
        large = max([s._lab(L["txt"], BLANC, size).width for L in s.lignes] or [0])
        if large > MAXW:
            size = max(26, int(size * MAXW / large) - 1)
        return size

    def _taille(s):
        """Taille des lettres : la plus grande qui tient (en hauteur et en largeur), la même pour toutes les lignes."""
        if "taille" not in s._cache:
            size = s._taille_pour()
            s._cache["titre_l"] = [s.titre] if s.titre else []
            if s.titre and s.TITRE_2_LIGNES \
                    and s._lab(s.titre, s.COL_TITRE, int(size * s.K_TITRE)).width * TROP_REDUIT > MAXW:
                i = s.titre.find(")")                                   # « LE PROPHÈTE (PAIX ET SALUT SUR LUI) / A DIT : »
                deux = [s.titre[:i + 1].strip(), s.titre[i + 1:].strip()] if 0 < i < len(s.titre) - 2 \
                    else coupe(s.titre, len(s.titre) // 2 + 3)
                if len(deux) == 2 and all(deux):
                    s._cache["titre_l"] = deux
                    size = s._taille_pour(s.PLUS_TITRE)
            s._cache["taille"] = size
        return s._cache["taille"]

    def _places(s, u):
        """Milieu de chaque ligne à l'instant u : la place d'une ligne ajoutée s'ouvre en douceur juste avant son
        mot, et le bloc reste centré (glissés doux, jamais de saut)."""
        pas = s._taille() * s.PAS
        y, ys = 0.0, []
        y_titre = None
        if s.titre:
            y_titre, y = pas * 0.5, pas * 1.1
            if len(s._cache.get("titre_l", ())) == 2:                   # titre sur deux lignes
                y_titre, y = y_titre + pas * s.PLUS_TITRE / 2, y + pas * s.PLUS_TITRE
        for L in s.lignes:
            o = 1.0 if (L["o"] is None or L["o"] < 0) else smooth((u - L["o"] + 0.3) / 0.4)
            h = pas * s._poids(L)
            ys.append(y + h * 0.5 * o)
            y += h * o
        y_note = None
        if s.note:
            o = 1.0 if s.note[1] < 0 else smooth((u - s.note[1] + 0.3) / 0.4)
            y_note = y + pas * 0.62 * o
            y += pas * 1.15 * o
        y0 = s.PH_ * 3 - (18 if s.fond == "tableau" else 0) - y / 2
        return (None if y_titre is None else y0 + y_titre), [y0 + v for v in ys], (None if y_note is None else y0 + y_note)

    def dessine(s, im, u):
        size, xc = s._taille(), im.width / 2
        y_titre, ys, y_note = s._places(u)
        if s.titre:
            tl = s._cache.get("titre_l", ())
            s._mets(im, s._bloc(tl, s.COL_TITRE, int(size * s.K_TITRE)) if len(tl) == 2
                    else s._lab(s.titre, s.COL_TITRE, int(size * s.K_TITRE)), xc, y_titre, smooth(u / 0.35))
        for L, y in zip(s.lignes, ys):
            a_in = s._av(L["t"], u, 0.3)
            if a_in <= 0.01:
                continue
            a = a_in * (1 - s._av(L["efface"], u, 0.5))
            p = s._av(L["barre"], u, 0.3)
            a *= 1 - 0.32 * s._av(L["barre"], u, 0.3, dec=0.3)          # une ligne barrée s'estompe un peu
            dore = s._av(L["or_"], u, 0.45)
            x = xc - 26 * (1 - a_in)
            lab = s._lab(L["txt"], BLANC, size)
            if dore > 0.01:                                             # la bonne réponse : en or, avec une lueur douce
                s._pose_halo(im, x, y, min(MAXW, lab.width) * 0.9, size * 1.5, (255, 210, 90),
                             a * dore * (0.82 + 0.18 * math.sin(2 * math.pi * u / 2.6)))
            x0, y0, w, h = s._mets(im, lab, x, y, a * (1 - dore))
            if dore > 0.01:
                s._mets(im, s._lab(L["txt"], OR_, size), x, y, a * dore)
            if p > 0.01 and a > 0.01:                                   # le trait rouge, un peu penché, comme à la main
                k_ = w / max(1, lab.width)
                xa, xb, ym = x0 + 24 * k_, x0 + w - 24 * k_, y0 + h * 0.56
                xe, ye = xa + (xb - xa) * p, ym + 5 - 10 * p
                d = ImageDraw.Draw(im)
                d.line([(xa, ym + 10), (xe, ye + 5)], fill=(16, 12, 24, 255), width=10)
                d.line([(xa, ym + 5), (xe, ye)], fill=(*ROUGE, 255), width=11)
            ac = s._av(L["coche"], u, 0.3) * a
            if ac > 0.01:
                ic = s._ic("check", 5)
                s._mets(im, ic, max(60, x0 - ic.width * 0.42), y, ac)
        if s.note and y_note is not None:
            s._mets(im, s._lab(s.note[0], JAUNE, int(size * 0.9)), xc, y_note, s._av(s.note[1], u, 0.4))

    @classmethod
    def duree(cls, action, textes, mots):
        if action == "":
            return cls.T0 + cls.ECART * len(textes) + 0.9
        n = max(1, sum(1 for m in mots if m.isdigit()))
        return dict(barre=0.9, coche=0.8, efface=0.9, note=1.1).get(action, 0.9) + 0.25 * (n - 1)


# ---------------------------------------------------------------- {citation …}
class Citation(Liste):
    """Une parole citée, dans un cadre doré : le 1er texte (s'il y en a plusieurs) dit QUI parle, les suivants sont
    la citation, coupée en lignes toute seule. La source reste la balise {source "…"}."""
    FOND = "cadre"
    PH_ = 112                                    # une carte moins haute (672 pixels)
    COUPE = 21
    COL_TITRE, K_TITRE = OR_, 0.74
    TITRE_2_LIGNES = True                        # 11/11/2026 : « LE PROPHÈTE ﷺ A DIT : » ne sort plus minuscule
    T0, ECART = 0.25, 0.16

    def _depart(s, textes):
        if (len(textes) > 1 or "qui" in s._mots) and s.titre is None and textes:     # 11/11/2026 : plus s.cmd.split()
            s.titre, textes = textes[0], textes[1:]
        for x in textes:
            s._plus(x, None)


# ---------------------------------------------------------------- {jauge …}
class Jauge(_Brique):
    ACTIONS = ("->", "fin", "lueur")

    def __init__(s, cmd, textes=(), mots=(), jetons=()):
        super().__init__(cmd, textes, mots, jetons)
        s.lab_ = _propre(textes[0]) if textes else ""
        m = [_norm(x) for x in mots]
        s.inverse, s.pct = "inverse" in m, "%" in m
        s.who = next((x.upper() for x in mots if x.upper() in cast.CAST), None)
        s.max, nums, i = None, [], 0
        while i < len(m):
            if m[i] == "max" and i + 1 < len(m) and _nombre(m[i + 1]) is not None:
                s.max = _nombre(m[i + 1])
                i += 2
                continue
            if _nombre(m[i]) is not None:
                nums.append(_nombre(m[i]))
            i += 1
        s.pts = [(0.0, nums[0] if nums else 100.0, 0.0)]            # (instant, valeur visée, durée)
        if "->" in m and len(nums) > 1:
            s.pts.append((0.55, nums[1], 1.5))
        s.max = s.max or max([100.0] + nums)
        s.fin = None                                                # (u, texte, couleur)

    def reprise(s):
        s.pts = [(t0 if i == 0 else -9.0, v, d) for i, (t0, v, d) in enumerate(s.pts)]

    def evt(s, u, action, textes, mots):
        if action == "->":
            v = next((_nombre(x) for x in mots if _nombre(x) is not None), None)
            if v is not None:
                s.pts.append((u if u >= 0 else -9.0, v, 1.1))
                s.max = max(s.max, v)
                s.son(u, "tr_whoosh_doux", 0.025)
        elif action == "fin":
            rouge = "rouge" in map(_norm, mots)
            s.fin = (u, _propre(textes[0]) if textes else "", ROUGE if rouge else VERT)
            s.son(u, "sa_scintillement", 0.04)
        else:
            return super().evt(u, action, textes, mots)
        return True

    def _niveau(s, u):
        v = s.pts[0][1]
        for (t0, cible, d) in s.pts[1:]:
            if t0 < 0:
                v = cible
            elif u > t0:
                v = v + (cible - v) * smooth((u - t0) / d)
        return v

    def _buste_img(s, face):
        cle = ("buste", face)
        if cle not in s._cache:
            s._cache[cle] = _grand(_buste(s.who, face)[0], 12)
        return s._cache[cle]

    def dessine(s, im, u):
        W = im.width
        d = ImageDraw.Draw(im)
        cx, lw = (236, 150) if s.who else (W // 2, 190)
        x0, x1, y0, y1 = cx - lw // 2, cx + lw // 2, 176, 716
        s._mets(im, s._lab(s.lab_, JAUNE, 66), W / 2, 86, smooth(u / 0.35))
        v = s._niveau(u)
        r = max(0.0, min(1.0, v / s.max))
        mauvais = (1 - r) if s.inverse else r
        col = _degrade(mauvais)
        d.rounded_rectangle([x0 - 14, y0 - 14, x1 + 14, y1 + 14], 34, fill=(*OL, 255))
        d.rounded_rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], 28, fill=(232, 236, 250, 255))
        d.rounded_rectangle([x0, y0, x1, y1], 20, fill=(26, 26, 54, 255))
        yl = y1 - (y1 - y0) * r
        if y1 - yl > 6:
            ray = min(20, int((y1 - yl) / 2) - 2)                   # (un rayon trop grand pour la hauteur fait planter PIL)
            if ray >= 3:
                d.rounded_rectangle([x0, yl, x1, y1], ray, fill=(*col, 255))
            else:
                d.rectangle([x0 + 6, yl, x1 - 6, y1], fill=(*col, 255))
            if y1 - yl > 26:
                d.rectangle([x0 + 12, yl + 6, x1 - 12, yl + 12], fill=(*_clair(col), 255))
            if y1 - yl > 90:                                        # petites bulles qui montent : la jauge vit
                for j in range(3):
                    ph = (u / (2.4 + 0.5 * j) + 0.37 * j) % 1.0
                    bx, by = x0 + 34 + j * (lw - 80) / 2, y1 - 18 - ph * (y1 - yl - 50)
                    d.rectangle([bx, by, bx + 10, by + 10], fill=(*_clair(col, 0.5), 255))
        for f in (0.25, 0.5, 0.75):                                 # graduations
            yg = y1 - (y1 - y0) * f
            d.rectangle([x1 - 46, yg - 3, x1 - 10, yg + 3], fill=(232, 236, 250, 255))
        _translucide(im, lambda dd: dd.rounded_rectangle([x0 + 14, y0 + 16, x0 + 32, y1 - 16], 9,
                                                         fill=(255, 255, 255, 44)))
        if s.pct:
            lab = s._lab("%d %%" % round(v), BLANC, 58)
            s._mets(im, lab, x1 + 118, max(y0 + 34, min(y1 - 34, yl)), smooth(u / 0.4))
        if s.who:
            faces = ("content", "neutre", "triste") if s.inverse else ("content", "neutre", "enerve")
            b = s._buste_img(faces[2] if mauvais > 0.66 else faces[1] if mauvais > 0.33 else faces[0])
            bx, by = 726 - b.width // 2, int(446 - b.height / 2 + 4 * math.sin(2 * math.pi * u / 3.2))
            s._pose_halo(im, 726, 446, b.width * 0.9, b.height * 0.8, col, 0.55 * smooth(u / 0.5), 90)
            im.alpha_composite(_fade(b, smooth(u / 0.35)), (bx, by))
        if s.fin:
            a = s._av(s.fin[0], u, 0.4)
            x0_, y0_, w_, h_ = s._mets(im, s._lab(s.fin[1], s.fin[2], 62), W / 2 + 30, 806, a, maxw=760)
            if s.fin[2] == VERT:
                ic = s._ic("check", 5)
                s._mets(im, ic, x0_ - ic.width * 0.4, 806, a)

    @classmethod
    def duree(cls, action, textes, mots):
        return 2.5 if (action == "" and "->" in mots) else 1.6 if action == "->" else 1.0


# ---------------------------------------------------------------- {focus …}
class Focus(_Brique):
    ACTIONS = ("entoure", "ok", "non", "texte", "lueur")
    CX, CY, HAUT, LARGE = 510, 392, 430, 640
    ZONES = dict(haut=(0, -0.27), bas=(0, 0.27), gauche=(-0.27, 0), droite=(0.27, 0), centre=(0, 0))

    def __init__(s, cmd, textes=(), mots=(), jetons=()):
        super().__init__(cmd, textes, mots, jetons)
        noms = [x for x in mots if est_objet(x)]
        s.nom = noms[0] if noms else None
        s.face = next((x for x in map(_norm, mots) if x in FACES()), "neutre")
        s.lab_ = [(0.0, _propre(textes[0]), BLANC)] if textes else []      # (u, texte, couleur) : le dernier gagne
        s.marques = []                                                       # (u, dx, dy, texte) en fractions de l'objet
        s.tampon = None                                                      # (u, icône)

    def reprise(s):
        s.lab_ = [(-9.0, t, c) for (_, t, c) in s.lab_]

    def evt(s, u, action, textes, mots):
        m = [_norm(x) for x in mots]
        txt = _propre(textes[0]) if textes else None
        if action == "entoure":
            nums = [_nombre(x) for x in m if _nombre(x) is not None]
            if len(nums) >= 2:
                dx, dy = nums[0] / 100 - 0.5, nums[1] / 100 - 0.5
            else:
                dx = sum(s.ZONES[x][0] for x in m if x in s.ZONES)
                dy = sum(s.ZONES[x][1] for x in m if x in s.ZONES)
            s.marques.append((u, dx, dy, txt))
            s.son(u, "sa_ting", 0.03)
        elif action in ("ok", "non"):
            s.tampon = (u, "check" if action == "ok" else "interdit")
            if txt:
                s.lab_.append((u, txt, VERT if action == "ok" else ROUGE))
            s.son(u, "sa_scintillement" if action == "ok" else "imp_tampon", 0.035 if action == "ok" else 0.025)
        elif action == "texte":
            if txt:
                s.lab_.append((u, txt, JAUNE))
        else:
            return super().evt(u, action, textes, mots)
        return True

    def _objet(s):
        if "objet" not in s._cache:
            im = objet_img(s.nom, s.face) if s.nom else None
            s._cache["objet"] = _agrandi(im, s.HAUT, s.LARGE) if im is not None else None
        return s._cache["objet"]

    def dessine(s, im, u):
        obj = s._objet()
        a_in = smooth(u / 0.35)
        dy = 6 * math.sin(2 * math.pi * u / 3.4)
        ow, oh = (obj.width, obj.height) if obj is not None else (420, 300)
        if obj is not None:
            s._pose_halo(im, s.CX, s.CY, ow + 120, oh + 90, (255, 240, 190),
                         a_in * (0.8 + 0.2 * math.sin(2 * math.pi * u / 3.0)), 84)
            s._pose_halo(im, s.CX, s.CY + oh / 2 + 30, ow * 0.7, 26, (0, 0, 0), a_in, 130)       # ombre au sol
            im.alpha_composite(_fade(obj, a_in), (int(s.CX - ow / 2), int(s.CY - oh / 2 + dy)))
        r0 = max(74, 0.25 * min(ow, oh))
        for (t0, fx, fy, txt) in s.marques:                          # cercles pointillés jaunes qui tournent lentement
            a = s._av(t0, u, 0.35)
            if a <= 0.01:
                continue
            mx, my = s.CX + fx * ow, s.CY + fy * oh + dy
            r = r0 * (1 + 0.03 * math.sin(2 * math.pi * u / 1.6))
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            n = 16
            for (ep, col) in ((18, (16, 12, 24, 255)), (10, (*JAUNE, 255))):
                for i in range(n):
                    a0 = 360.0 * i / n + u * 22
                    dl.arc([mx - r, my - r, mx + r, my + r], a0, a0 + 360.0 / n * 0.56, fill=col, width=ep)
            im.alpha_composite(_fade(lay, a))
            if txt:
                bas = fy > 0.1
                s._mets(im, s._lab(txt, JAUNE, 54), mx, my + (r + 50 if bas else -r - 50), a, maxw=520)
        if s.tampon and obj is not None:
            a = s._av(s.tampon[0], u, 0.3)
            st = s._ic(s.tampon[1], 13, 5, True)
            s._mets(im, st, s.CX + ow / 2 - st.width * 0.2, s.CY - oh / 2 + st.height * 0.2 + dy, a)
        for i, (t0, txt, col) in enumerate(s.lab_):                 # le texte du bas (le dernier remplace le précédent)
            a = s._av(t0, u, 0.35) if i else (1.0 if t0 < 0 else a_in)
            if i + 1 < len(s.lab_):
                a *= 1 - s._av(s.lab_[i + 1][0], u, 0.25)
            y = (s.CY + oh / 2 + 110) if obj is not None else s.CY
            s._mets(im, s._lab(txt, col, 62 if obj is not None else 84), s.CX, min(820, y), a)

    @classmethod
    def duree(cls, action, textes, mots):
        return dict(entoure=1.2).get(action, 0.9)


# ---------------------------------------------------------------- {versus …}
class Versus(_Brique):
    ACTIONS = ("non", "oui", "lueur")
    LW, LH, Y0 = 452, 590, 150

    def __init__(s, cmd, textes=(), mots=(), jetons=()):
        super().__init__(cmd, textes, mots, jetons)
        s.titre, s.cotes, obj, face = None, [], None, "neutre"
        titre = "titre" in map(_norm, mots)
        for (g, v) in jetons:
            if g == "m":
                if est_objet(v):
                    obj = v
                elif _norm(v) in FACES():
                    face = _norm(v)
            elif titre and s.titre is None:
                s.titre = _propre(v)
            elif len(s.cotes) < 2:
                s.cotes.append(dict(obj=obj, face=face, txt=_propre(v)))
                obj, face = None, "neutre"
        while len(s.cotes) < 2:
            s.cotes.append(dict(obj=None, face="neutre", txt=""))
        s.marques = [None, None]                                     # (u, "non" | "oui")
        s.t_in = [0.0, 0.3]

    def reprise(s):
        s.t_in = [-9.0, -9.0]

    def evt(s, u, action, textes, mots):
        if action in ("non", "oui"):
            m = [_norm(x) for x in mots]
            i = 0 if "gauche" in m else 1 if "droite" in m else (0 if action == "non" else 1)
            s.marques[i] = (u, action)
            s.son(u, "imp_tampon" if action == "non" else "sa_scintillement", 0.025 if action == "non" else 0.04)
            return True
        return super().evt(u, action, textes, mots)

    def _carte(s, i):
        """Le contenu fixe d'une carte (objet + légende), sans son cadre."""
        cle = ("carte", i)
        if cle not in s._cache:
            c = s.cotes[i]
            lay = Image.new("RGBA", (s.LW, s.LH), (0, 0, 0, 0))
            im = objet_img(c["obj"], c["face"]) if c["obj"] else None
            lignes = coupe(c["txt"], 13) if c["txt"] else []
            if im is not None:
                o = _agrandi(im, 270, s.LW - 90)
                lay.alpha_composite(o, (int(s.LW / 2 - o.width / 2), int(206 - o.height / 2)))
            if lignes:
                lab = s._bloc(lignes, BLANC, 50 if im is not None else 62)
                if lab.width > s.LW - 36:
                    k_ = (s.LW - 36) / lab.width
                    lab = lab.resize((int(lab.width * k_), int(lab.height * k_)), Image.LANCZOS)
                yc = 462 if im is not None else s.LH / 2
                lay.alpha_composite(lab, (int(s.LW / 2 - lab.width / 2), int(min(s.LH - lab.height - 10, yc - lab.height / 2))))
            s._cache[cle] = lay
        return s._cache[cle]

    def dessine(s, im, u):
        W = im.width
        if s.titre:
            s._mets(im, s._lab(s.titre, JAUNE, 60), W / 2, 80, smooth(u / 0.35))
        for i in (0, 1):
            a_in = s._av(s.t_in[i], u, 0.35)
            if a_in <= 0.01:
                continue
            x0 = (36 if i == 0 else W - 36 - s.LW) + (1 - a_in) * (-30 if i == 0 else 30)
            y0 = s.Y0 if s.titre else s.Y0 - 30
            mq = s.marques[i]
            e = s._av(mq[0], u, 0.4) if mq else 0.0
            non = bool(mq) and mq[1] == "non"
            bord = _mel((150, 160, 214), ROUGE if non else VERT, e)
            if mq and not non:
                s._pose_halo(im, x0 + s.LW / 2, y0 + s.LH / 2, s.LW * 0.9, s.LH * 0.9, (110, 226, 130),
                             a_in * e * (0.8 + 0.2 * math.sin(2 * math.pi * u / 2.6)), 110)
            lay = Image.new("RGBA", (s.LW, s.LH), (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            dl.rounded_rectangle([0, 0, s.LW - 1, s.LH - 1], 30, fill=(*OL, 255))
            dl.rounded_rectangle([6, 6, s.LW - 7, s.LH - 7], 26, fill=(*bord, 255))
            dl.rounded_rectangle([16, 16, s.LW - 17, s.LH - 17], 18,
                                 fill=(*_mel((30, 32, 64), (64, 26, 34) if non else (26, 58, 44), e), 255))
            lay.alpha_composite(s._carte(i))
            im.alpha_composite(_fade(lay, a_in * (1 - 0.28 * e if non else 1)), (int(x0), int(y0)))
            if mq:
                st = s._ic("croix" if non else "check", 11, 5, True)
                s._mets(im, st, x0 + s.LW - st.width * 0.36, y0 + st.height * 0.3, e * a_in)
        a_vs = s._av(s.t_in[1], u, 0.35, dec=0.15)
        if a_vs > 0.01:
            s._mets(im, s._lab("VS", JAUNE, 58), W / 2, (s.Y0 if s.titre else s.Y0 - 30) + s.LH / 2 - 60, a_vs)


# ---------------------------------------------------------------- {bulles …}
class Bulles(_Brique):
    AUTO = True
    ACTIONS = ()
    BAS, ECART = 838, 30
    FONDS_B = ((40, 60, 120), (30, 98, 86))                         # celui de gauche, celui de droite

    def __init__(s, cmd, textes=(), mots=(), jetons=()):
        super().__init__(cmd)
        s.msgs = []                                                  # dict(u, who, cote, img)
        s.cotes = {}

    def evt(s, u, action, textes, mots):
        m = [_norm(x) for x in mots]
        if m and m[0] == "lueur":
            return super().evt(u, "lueur", textes, mots[1:])
        who = next((x.upper() for x in mots if x.upper() in cast.CAST), None)
        face = next((x for x in m if x in FACES()), "neutre")
        cote = s.cotes.setdefault(who, len(s.cotes) % 2)
        vide = "vide" in m or not textes
        txt = "…" if vide else _propre(textes[0])
        fond = (70, 72, 92) if vide else (124, 88, 18) if "or" in m else (120, 40, 44) if "rouge" in m else s.FONDS_B[cote]
        col = (190, 192, 206) if vide else JAUNE if "or" in m else BLANC
        b = _bulle([(l_, col) for l_ in coupe(txt, 15)], fond=fond, size=46, queue=0.13 if cote == 0 else 0.87)
        b = b.crop(b.getbbox())
        if b.width > 640:
            b = b.resize((640, int(b.height * 640 / b.width)), Image.LANCZOS)
        tete = None
        if who:
            tete = _grand(_buste(who, face)[0], 6)
            if cote == 1:
                tete = tete.transpose(Image.FLIP_LEFT_RIGHT)
        h = max(b.height, tete.height if tete is not None else 0)
        lay = Image.new("RGBA", (980, h), (0, 0, 0, 0))
        if cote == 0:
            if tete is not None:
                lay.alpha_composite(tete, (0, h - tete.height))
            lay.alpha_composite(b, (186, (h - b.height) // 2))
        else:
            if tete is not None:
                lay.alpha_composite(tete, (980 - tete.width, h - tete.height))
            lay.alpha_composite(b, (980 - 186 - b.width, (h - b.height) // 2))
        s.msgs.append(dict(u=u, img=lay, h=h))
        s.son(u, "sa_ting", 0.025)
        return True

    def dessine(s, im, u):
        # les bulles forment un bloc centré ; quand il ne tient plus, il reste calé en bas et les plus anciennes sortent
        tot = sum((M["h"] + s.ECART) * s._av(M["u"], u, 0.4) for M in s.msgs) - s.ECART
        haut = min(s.PH_ * 3 - tot / 2, s.BAS - tot)
        for i, M in enumerate(s.msgs):
            a = s._av(M["u"], u, 0.3)
            if a <= 0.01:
                continue
            y = haut + sum((N["h"] + s.ECART) * s._av(N["u"], u, 0.4) for N in s.msgs[:i]) + 26 * (1 - a)
            if y < 30:                                               # les plus anciennes s'effacent en haut
                a *= max(0.0, 1 - (30 - y) / 90)
            if a > 0.01 and y > -M["h"]:
                img = M["img"]
                y0 = int(y)
                if y0 < 0:
                    img, y0 = img.crop((0, -y0, img.width, img.height)), 0
                im.alpha_composite(_fade(img, a), (20, y0))


# ---------------------------------------------------------------- {trajet …}
class Trajet(_Brique):
    ACTIONS = ("avance", "stop", "arrive", "etape", "lueur")
    PH_ = 130                                                        # 780 pixels de haut
    XA, XB, ROUTE = 170, 836, 500                                    # bouts de la route, haut de la route

    def __init__(s, cmd, textes=(), mots=(), jetons=()):
        super().__init__(cmd, textes, mots, jetons)
        s.who = next((x.upper() for x in mots if x.upper() in cast.CAST), None)
        s.titre, bouts, obj = None, [], None
        titre = "titre" in map(_norm, mots)
        for (g, v) in jetons:
            if g == "m":
                if _norm(v) in objets.ICONES or _norm(v) in OBJETS:
                    obj = _norm(v)
            elif titre and s.titre is None:
                s.titre = _propre(v)
            elif len(bouts) < 2:
                bouts.append((obj, _propre(v)))
                obj = None
        while len(bouts) < 2:
            bouts.append((None, ""))
        s.bouts = [(bouts[0][0] or "maison", bouts[0][1]), (bouts[1][0] or "drapeau", bouts[1][1])]
        s.pts = [(0.0, 0.0, 0.0)]                                    # (instant, avancement visé 0..1, durée)
        s.etapes, s.stop, s.arrive = [], None, None

    def evt(s, u, action, textes, mots):
        nums = [_nombre(x) for x in mots if _nombre(x) is not None]
        txt = _propre(textes[0]) if textes else ""
        if action == "avance":
            s.pts.append((u if u >= 0 else -9.0, max(0.0, min(1.0, (nums[0] if nums else 50) / 100)), 1.3))
        elif action == "arrive":
            s.pts.append((u if u >= 0 else -9.0, 1.0, 1.3))
            s.arrive = (u + 1.3) if u >= 0 else -9.0
            s.son(u + 1.3, "sa_scintillement", 0.04)
        elif action == "stop":
            s.stop = (u, txt)
            s.son(u, "tr_whoosh_doux", 0.03)
        elif action == "etape":
            s.etapes.append((u, max(0.0, min(1.0, (nums[0] if nums else 50) / 100)), txt))
            s.son(u, "sa_ting", 0.025)
        else:
            return super().evt(u, action, textes, mots)
        return True

    def _p(s, u):
        v, bouge = s.pts[0][1], False
        for (t0, cible, d) in s.pts[1:]:
            if t0 < 0:
                v = cible
            elif u > t0:
                v = v + (cible - v) * smooth((u - t0) / d)
                bouge = bouge or (u < t0 + d and abs(cible - v) > 1e-3)
        return v, bouge

    def _decor(s):
        if "decor" not in s._cache:
            lay = Image.new("RGBA", (s.PW_ * 6, s.PH_ * 6), (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            rng = np.random.default_rng(7)
            for _ in range(26):                                      # quelques étoiles
                x, y = int(rng.integers(40, 980)), int(rng.integers(130, 380))
                d.rectangle([x, y, x + 5, y + 5], fill=(214, 220, 255, int(rng.integers(70, 170))))
            y = s.ROUTE
            d.rounded_rectangle([64, y - 6, 956, y + 62], 20, fill=(*OL, 255))
            d.rounded_rectangle([70, y, 950, y + 56], 16, fill=(64, 60, 92, 255))
            for x in range(100, 930, 64):
                d.rectangle([x, y + 25, x + 30, y + 31], fill=(120, 118, 150, 255))
            for i, (ico, txt) in enumerate(s.bouts):
                o = autocollant(objets.icone(ico).img(8) if ico in objets.ICONES else
                                _agrandi(OBJETS[ico](), 130, 130), r=4, ombre=False)
                xc = 96 if i == 0 else 930
                lay.alpha_composite(o, (int(xc - o.width / 2), int(y - 14 - o.height)))
            s._cache["decor"] = lay
        return s._cache["decor"]

    def dessine(s, im, u):
        W = im.width
        a_in = smooth(u / 0.35)
        im.alpha_composite(_fade(s._decor(), a_in))
        if s.titre:
            s._mets(im, s._lab(s.titre, JAUNE, 58), W / 2, 76, a_in)
        y = s.ROUTE
        p, bouge = s._p(u)
        x = s.XA + (s.XB - s.XA) * p
        d = ImageDraw.Draw(im)
        if x - s.XA > 4:                                             # le chemin déjà fait
            d.rectangle([s.XA - 4, y + 20, x + 4, y + 36], fill=(16, 12, 24, 255))
            d.rectangle([s.XA, y + 24, x, y + 32], fill=(*JAUNE, 255))
        arrive = s._av(s.arrive, u, 0.5)
        for i, (ico, txt) in enumerate(s.bouts):                     # les noms des deux bouts, sous la route
            if txt:
                col = OR_ if (i == 1 and arrive > 0.5) else BLANC
                s._mets(im, s._bloc(coupe(txt, 13), col, 46), 200 if i == 0 else W - 200, y + 196, a_in, maxw=380)
        for j, (t0, pe, txt) in enumerate(s.etapes):                 # les étapes : un fanion sur la route + son nom
            a = s._av(t0, u, 0.35)
            if a <= 0.01:
                continue
            xe = s.XA + (s.XB - s.XA) * pe
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            dl.rectangle([xe - 5, y - 50, xe + 5, y + 8], fill=(16, 12, 24, 255))
            dl.rectangle([xe - 2, y - 47, xe + 2, y + 5], fill=(236, 238, 250, 255))
            dl.polygon([(xe + 3, y - 50), (xe + 46, y - 36), (xe + 3, y - 22)], fill=(16, 12, 24, 255))
            dl.polygon([(xe + 3, y - 45), (xe + 36, y - 36), (xe + 3, y - 27)], fill=(*ORANGE, 255))
            im.alpha_composite(_fade(lay, a))
            if txt:
                s._mets(im, s._bloc(coupe(txt, 12), JAUNE, 40), xe, y - 262 - 66 * (j % 2), a, maxw=300)
        if s.who:                                                    # celui qui marche (ses pieds sur la route)
            cle = ("marche", int(u * 9) % 8 if bouge else -1)
            if cle not in s._cache:
                spr = _sprite(s.who, step=cle[1]) if bouge else _sprite(s.who)
                bb = spr.getbbox()
                s._cache[cle] = _grand(spr.crop(bb), 3)
            sp = s._cache[cle]
            im.alpha_composite(_fade(sp, a_in), (int(x - sp.width / 2), int(y + 30 - sp.height)))
        else:                                                        # sinon : un point de lumière
            s._pose_halo(im, x, y + 28, 60, 60, (255, 226, 140), a_in * (0.85 + 0.15 * math.sin(2 * math.pi * u / 1.8)), 200)
            d = ImageDraw.Draw(im)
            d.ellipse([x - 20, y + 8, x + 20, y + 48], fill=(*OL, 255))
            d.ellipse([x - 15, y + 13, x + 15, y + 43], fill=(255, 236, 170, 255))
        if s.stop:                                                   # sous la route, à l'endroit où il s'est arrêté
            xs = s.XA + (s.XB - s.XA) * s._p(max(0.0, s.stop[0]))[0]
            s._mets(im, s._lab(s.stop[1], ROUGE, 50), xs, y + 106, s._av(s.stop[0], u, 0.35), maxw=560)
        if arrive > 0.01:
            ic = s._ic("check", 7)
            s._mets(im, ic, 930, y - 204, arrive)

    @classmethod
    def duree(cls, action, textes, mots):
        return dict(avance=1.8, arrive=2.2, stop=1.0, etape=0.8).get(action, 0.9)


# ---------------------------------------------------------------- {grille …}
class Grille(_Brique):
    ACTIONS = ("coche", "barre", "vide", "lueur")

    def __init__(s, cmd, textes=(), mots=(), jetons=()):
        super().__init__(cmd, textes, mots, jetons)
        nums = [_nombre(x) for x in mots if _nombre(x) is not None]
        s.n = int(max(1, min(120, nums[0] if nums else 5)))
        s.lab_ = _propre(textes[0]) if textes else ""
        s.titre = _propre(textes[1]) if len(textes) > 1 else None
        s.evts = []                                                  # (u, "coche" | "barre" | "vide", jusqu'où)

    def evt(s, u, action, textes, mots):
        if action in ("coche", "barre", "vide"):
            m = [_norm(x) for x in mots]
            nums = [_nombre(x) for x in m if _nombre(x) is not None]
            n = s.n if (action == "vide" or "tout" in m or not nums) else int(max(0, min(s.n, nums[0])))
            s.evts.append((u, action, n))
            s._cache.pop("etats", None)
            s.son(u, "imp_tampon" if action == "barre" else "sa_ting", 0.02 if action == "barre" else 0.03)
            return True
        return super().evt(u, action, textes, mots)

    def _etats(s):
        """Pour chaque case : la liste (instant, état) de ses changements (les cases changent l'une après l'autre)."""
        if "etats" not in s._cache:
            et = [[(-9.0, "vide")] for _ in range(s.n)]
            for (u, kind, n) in s.evts:
                neuves = [i for i in range(n) if et[i][-1][1] != kind]
                dt = min(0.12, 1.2 / max(1, len(neuves)))
                for j, i in enumerate(neuves):
                    et[i].append(((u + j * dt) if u >= 0 else -9.0, kind))
            s._cache["etats"] = et
        return s._cache["etats"]

    def dessine(s, im, u):
        W = im.width
        a_in = smooth(u / 0.35)
        if s.titre:
            s._mets(im, s._lab(s.titre, JAUNE, 58), W / 2, 80, a_in)
        n = s.n
        cols = n if n <= 5 else 5 if n <= 10 else 6 if n <= 24 else 8 if n <= 40 else 10 if n <= 60 else 12
        rows = int(math.ceil(n / cols))
        c = int(min(176, 860 / cols, (500 if s.titre else 560) / rows))
        gap = max(4, c // 8)
        cote = c - gap
        gx, gy = W / 2 - (cols * c - gap) / 2, (420 if s.titre else 390) - (rows * c - gap) / 2
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        et = s._etats()
        compte = {"coche": 0, "barre": 0}
        rad = max(3, cote // 6)
        for i in range(n):
            x0, y0 = gx + (i % cols) * c, gy + (i // cols) * c
            avant, cur, f = "vide", "vide", 1.0
            for (t0, kind) in et[i]:
                if t0 <= u:
                    avant, cur, f = cur, kind, (1.0 if t0 < 0 else smooth((u - t0) / 0.25))
            if cur in compte and f > 0.5:
                compte[cur] += 1
            cols_ = dict(vide=((44, 48, 92), (112, 122, 192)), coche=((52, 160, 92), VERT), barre=((150, 48, 54), ROUGE))
            fond, bord = _mel(cols_[avant][0], cols_[cur][0], f), _mel(cols_[avant][1], cols_[cur][1], f)
            d.rounded_rectangle([x0, y0, x0 + cote, y0 + cote], rad, fill=(*OL, 255))
            ep = max(2, cote // 14)
            d.rounded_rectangle([x0 + ep, y0 + ep, x0 + cote - ep, y0 + cote - ep], max(2, rad - ep), fill=(*bord, 255))
            d.rounded_rectangle([x0 + 2 * ep, y0 + 2 * ep, x0 + cote - 2 * ep, y0 + cote - 2 * ep], max(1, rad - 2 * ep),
                                fill=(*fond, 255))
            if cur != "vide" and f > 0.3 and cote >= 40:
                e, tr = cote * 0.26, max(4, cote // 9)
                xm, ym = x0 + cote / 2, y0 + cote / 2
                if cur == "coche":
                    d.line([(xm - e, ym), (xm - e * 0.25, ym + e * 0.7), (xm + e, ym - e * 0.7)], fill=(255, 255, 255, 255),
                           width=tr, joint="curve")
                else:
                    d.line([(xm - e, ym - e), (xm + e, ym + e)], fill=(255, 255, 255, 255), width=tr)
                    d.line([(xm - e, ym + e), (xm + e, ym - e)], fill=(255, 255, 255, 255), width=tr)
        im.alpha_composite(_fade(lay, a_in))
        quoi = "barre" if (compte["barre"] and not compte["coche"]) else "coche"
        txt = "%d / %d %s" % (compte[quoi], n, s.lab_)
        col = ROUGE if quoi == "barre" and compte["barre"] else (VERT if compte["coche"] == n else BLANC)
        s._mets(im, s._lab(txt.strip(), col, 62), W / 2, 806, a_in)

    @classmethod
    def duree(cls, action, textes, mots):
        return 2.0 if action in ("coche", "barre") else 0.9


# ---------------------------------------------------------------- branchement (explique.Schema, scenario._fin_anim)
BRIQUES = dict(liste=Liste, citation=Citation, jauge=Jauge, focus=Focus, versus=Versus, bulles=Bulles,
               trajet=Trajet, grille=Grille)
CLES = tuple(BRIQUES)
_MEMO = {}                    # clé → ce qu'il faut pour refaire la brique dans un autre plan (création + événements)
CREEES = []                   # toutes les briques créées par le scénario en cours (pour controle())


def _lit(cls, reste):
    jet = _jetons(reste)
    textes = [v for (g, v) in jet if g == "t"]
    mots = [v for (g, v) in jet if g == "m"]
    sous = _norm(mots[0]) if mots else ""
    if cls.AUTO:
        return jet, textes, mots, "", True
    return jet, textes, mots, sous, sous in cls.ACTIONS


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique.Schema._ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
    k = _norm(mots[0])
    cls = BRIQUES.get(k)
    if cls is None:
        return False
    jet, textes, autres, sous, est_evt = _lit(cls, reste)
    if cls.AUTO and autres and _norm(autres[0]) == "nouveau":        # {bulles nouveau PETIT "…"} : on repart de zéro
        _MEMO.pop(k, None)
        autres = autres[1:]
        for it in schema._visibles(t + 0.01):
            if type(it["el"]) is cls:
                it["t_out"] = t
    if not est_evt:                                                  # création
        el = cls(brut, textes, autres, jet)
        CREEES.append(el)
        schema._ajoute(t, el)
        _MEMO[k] = dict(args=(brut, textes, autres, jet), sigs=[], evts=[])
        return True
    el = next((it["el"] for it in reversed(schema._visibles(t + 0.01)) if type(it["el"]) is cls), None)
    memo = _MEMO.setdefault(k, dict(args=(brut, [], [], []), sigs=[], evts=[])) if cls.AUTO else _MEMO.get(k)
    sig = " ".join(brut.split())
    if el is None:
        if memo is None:
            print("briques : {%s} sans brique à modifier (il manque la balise de création)" % brut)
            return True
        el = cls(*memo["args"])                                      # autre plan : la brique reprend où elle en était
        CREEES.append(el)
        el.reprise()
        n = memo["sigs"].index(sig) if sig in memo["sigs"] else len(memo["sigs"])
        for (a_, tx_, mo_) in memo["evts"][:n]:
            el.evt(-9.0, a_, tx_, mo_)
        schema._ajoute(t, el)
    u = t - next(it["t_in"] for it in schema.items if it["el"] is el)
    args = (sous, textes, autres if cls.AUTO else autres[1:])
    el.evt(max(0.0, u), *args)
    if sig not in memo["sigs"]:
        memo["sigs"].append(sig)
        memo["evts"].append(args)
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    cls = BRIQUES.get(_norm(mots[0]))
    if cls is None:
        return None
    jet, textes, autres, sous, est_evt = _lit(cls, " ".join(mots[1:]))
    return t + cls.duree(sous if est_evt else "", textes, [_norm(x) for x in autres])


def connues():
    """Pour la vérification des scénarios (lot.py) : clé → actions permises."""
    return {k: tuple(a for a in c.ACTIONS) for k, c in BRIQUES.items()}


# ---------------------------------------------------------------- contrôle de lisibilité (lot.py verifie, 11/11/2026)
PETIT_TEXTE = 46              # en dessous, une carte ou une liste se lit mal sur téléphone (26 = illisible)
TROP_REDUIT = 0.8             # un texte réduit à moins de 80 % de sa taille pour tenir en largeur


def controle():
    """Après scenario.fabrique : dessine une fois chaque brique du scénario dans son état final et signale les textes
    trop petits AVANT les planches. Renvoie [(grave ?, message)] sans doublon. Ne change rien au rendu."""
    out = []
    for el in CREEES:
        cmd = " ".join(str(getattr(el, "cmd", "")).split())[:46]
        try:
            el.image(60.0)
        except Exception as e:                                       # une brique qui plante : le rendu échouerait
            out.append((True, "{%s} : la brique plante (%s)" % (cmd, str(e)[:80])))
            continue
        if isinstance(el, Liste) and el.lignes:
            size = el._taille()
            if size < PETIT_TEXTE:
                n = len(el.lignes)
                long_ = max(len(L["txt"]) for L in el.lignes)
                quoi = "%d lignes" % n if n > 5 else "une ligne de %d caractères" % long_
                out.append((size < 38, "{%s} : texte à %d px (%s) → couper en deux cartes : une nouvelle balise sans "
                                       "« + » remplace la carte" % (cmd, size, quoi)))
        r = getattr(el, "_retreci", 1.0)
        if r < 0.74:                                                  # (un titre sur deux lignes à 78 % se lit bien)
            quoi = "un texte"
            if isinstance(el, Liste):                                 # titre ou note : les lignes, elles, sont réglées
                size = el._taille()
                if el.note and el._lab(el.note[0], JAUNE, int(size * 0.9)).width > MAXW:
                    quoi = "la note « %s… » (%d caractères)" % (el.note[0][:24], len(el.note[0]))
                elif el.titre:
                    quoi = "le titre « %s… »" % el.titre[:30]
            out.append((r < 0.6, "{%s} : %s est réduit à %d %% de sa taille pour tenir en largeur (trop long)"
                        % (cmd, quoi, int(r * 100))))
    return list(dict.fromkeys(out))
