# DÉMONSTRATION EN IMAGE DU 08/11/2026 — Short ISL30 « Tu lis ton horoscope ? ARRÊTE ! » (consigne + avertissement).
# Même principe que les modules du 07/11 (explique_0611_dette.py) : le sens propre du hadith, montré en grand, avec des
# mouvements doux (glissés, fondus, échelles lentes ; jamais de secousse, de flash ni de coupe sèche). AUCUN devin,
# voyante, sorcier, djinn, Chaytan, prophète, ange ni Compagnon dessiné ; Allah jamais représenté ; pas de signe
# ésotérique mis en valeur ; la boule de cristal et la carte de tarot restent petites, floues et VIDES.
#   {astro PETIT}      accroche, vue à ta place : chambre d'ado le soir (floue, lampe chaude) ; TON téléphone dans tes
#                      mains (manches rouges de Petit) MONTE vers toi (85 % → 100 %) ; l'appli violette « TON HOROSCOPE
#                      DU JOUR » défile : « TON HOROSCOPE : » / « TU SERAS RICHE ! » + sac d'argent, « ♥ 12 K » (aucun
#                      signe réel nommé) ; sur le bureau, petites et floues : une carte de tarot retournée (dos à
#                      étoiles, aucune figure) et une boule de cristal au reflet FIXE (rien dedans)
#   {quarante}         ciel de nuit ; la carte « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : » / « CELUI QUI VA VOIR UN DEVIN
#                      ET L'INTERROGE SUR QUELQUE CHOSE… » ; dessous, toute la réplique : « LIRE TON HOROSCOPE =
#                      INTERROGER UN DEVIN » / « (SELON DE NOMBREUX SAVANTS) » ; 40 croissants gris foncé (8 × 5) ; le
#                      compteur « RÉCOMPENSE : 0 » ; le tapis de prière vide, vert et or, vu de trois quarts
#   {quarante lunes}   les 40 nuits passent une à une (gris foncé → gris clair, 0,2 s chacune, de gauche à droite et de
#                      haut en bas), un petit ✓ blanc sur chaque nuit et « ✓ PRIÈRE FAITE » sur le tapis ; le compteur
#                      RESTE à 0 et pâlit ; le tapis se désature (60 %) ; la carte s'achève : « AUCUNE PRIÈRE NE LUI EST
#                      ACCEPTÉE PENDANT QUARANTE NUITS. » » ; à la fin « 40 NUITS » en grand (Mouslim 2230)
#   {quarante arrete}  la bulle de pensée de Petit (le tapis qu'on roule) et un grand « ? » orange ; rien d'autre ne bouge
#   {quarante prie}    la bulle est barrée d'une croix rouge douce puis s'efface ; le tampon orange « VALABLE, MAIS //
#                      SANS RÉCOMPENSE » descend (0,35 s, ×1,15 → ×1, −6°, sans rebond) ; le bandeau vert « ✓ TU DOIS
#                      QUAND MÊME PRIER » ; en bas, en gris : « ELLE COMPTE : TU NE LA REFAIS PAS » / « (EXPLICATION
#                      D'AN-NAWAWI) » ; le tapis RESTE gris, sans halo, les lunes et le compteur ne changent pas
#   {quarante avenir}  fondu de tout le ciel (lunes, tapis et compteur partent avec lui, jamais avant) vers un nouveau
#                      ciel étoilé : l'étiquette verte « TON SIGNE : MUSULMAN ✓ » glisse en haut ; le parchemin « QUI
#                      CONNAÎT TON AVENIR ? » / « NUL DE CEUX QUI SONT DANS LES CIEUX ET SUR LA TERRE NE CONNAÎT
#                      L'INCONNAISSABLE, À PART ALLAH. » (Coran 27:65, Hamidullah, EXTRAIT ; « ALLAH » seul en or) ; en
#                      bas à gauche, l'icône violette de l'appli avec un « ? » gris
#   {quarante supprime} le parchemin s'efface ; le téléphone (vue à ta place) remonte : « SUPPRIMER « HOROSCOPE » ? » →
#                      « OUI » se coche ✓ vert ; l'icône glisse dans la corbeille en rapetissant (fondu, pas
#                      d'explosion) ; au-dessus : « REPENS-TOI : » / « « C'EST LUI QUI AGRÉE DE SES SERVITEURS LE
#                      REPENTIR » (EXTRAIT) » (Coran 42:25). Les lunes ne reviennent pas (rien n'« efface » les 40 nuits).
#   {quarante repens}  (2e relecture du 08/11) dernière réplique de Grand « Et repens-toi ! » : rien de nouveau ne
#                      s'ajoute ; « REPENS-TOI » et la citation s'effacent T_REPENS_OUT s plus tard, pour ne jamais se
#                      mêler à « ABONNE-TOI POUR LA SUITE » quand le schéma déborde sur la fin (à recaler sur la voix).
# 2e relecture du 08/11 : sous « 40 NUITS », « (= 40 JOURS DE PRIÈRES) » ; à {quarante prie}, le bandeau vert prend la
# place du compteur « RÉCOMPENSE : 0 » (qui s'efface dessous) au lieu de cacher la 4e rangée de lunes ; boîte
# « SUPPRIMER ? » plus longue (le « OUI ✓ » reste ≈ 0,4 s).
# Planche du Short (08/11, maquette) : le tampon a une carte sombre derrière l'encre et monte à y = 380 (il se lisait mal
# sur les lunes) ; à {quarante avenir}, « TON SIGNE : MUSULMAN » entre dès 0 s (le schéma commence avec « Musulman ! ») ;
# le téléphone de l'accroche part de 85 % (au lieu de 80 %).
# Branché par explique_0811.py (import tardif dans explique.Schema._ordre et scenario._fin_anim).
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from px import Px, TAHOMA
from pxv import smooth
from explique import _titre, _fade, BLANC
from explique_0411 import OL
from explique_0411b import _Base, _translucide, OR_
from explique_0611_dette import Dette, _texte_px, _lignes, _halo, _tourne_net, _colle, _etincelle

VIOLET = (78, 44, 132)
VIOLET_C = (150, 110, 214)
NUIT_H, NUIT_B = (8, 12, 40), (26, 32, 82)
ENCRE = (52, 36, 30)
ORANGE = (236, 128, 30)
VERT = (44, 156, 84)
VERT_C = (176, 238, 176)
GRIS_T = (196, 198, 212)
LUNE_S = (56, 60, 86)                 # croissant d'une nuit pas encore passée (gris foncé)
LUNE_L = (206, 210, 222)              # nuit passée (gris clair)
CARTE_L1 = "LE PROPHÈTE (PAIX ET SALUT SUR LUI) :"
CARTE_A = ("« CELUI QUI VA VOIR UN DEVIN", "ET L'INTERROGE SUR QUELQUE CHOSE,")
CARTE_B = ("AUCUNE PRIÈRE NE LUI EST ACCEPTÉE", "PENDANT QUARANTE NUITS. »")
VERSET = ("« NUL DE CEUX QUI SONT DANS", "LES CIEUX ET SUR LA TERRE", "NE CONNAÎT L'INCONNAISSABLE,")
REPENTIR = ("« C'EST LUI QUI AGRÉE DE SES", "SERVITEURS LE REPENTIR »  (EXTRAIT)")


def _coche(col=(255, 255, 255), k=5, bord=OL):
    """Petite coche ✓ pixel (bordée de sombre : lisible sur tout fond)."""
    c = Px(11, 9, alpha=True)
    m = c.mask_poly([(1, 4), (3, 4), (4.5, 6), (8.5, 1), (10, 1), (4.5, 8.3), (1, 5.5)])
    c.fill(m, col)
    c.outline(m, bord)
    return c.img(k, rgba=True)


def _desature(im, f):
    """Désature une image RGBA (f = 0 : couleurs, f = 1 : gris)."""
    a = np.array(im).astype(np.float32)
    g = (0.30 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2])[..., None]
    a[..., :3] = a[..., :3] * (1 - f) + g * f
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")


def _cote(ims, ecart=10):
    """Colle des images côte à côte, centrées en hauteur."""
    W_ = sum(i.width for i in ims) + ecart * (len(ims) - 1)
    H_ = max(i.height for i in ims)
    out = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    x = 0
    for i in ims:
        out.alpha_composite(i, (x, int((H_ - i.height) / 2)))
        x += i.width + ecart
    return out


class Horoscope(_Base):
    """{astro PETIT} : accroche, vue à ta place (le téléphone et l'appli « TON HOROSCOPE DU JOUR »). {quarante} et ses
    étapes lunes, arrete, prie, avenir, supprime : les 40 nuits sans récompense (Mouslim 2230, explication
    d'an-Nawawi), « tu dois quand même prier », Coran 27:65 et 42:25 (voir l'en-tête du module)."""
    ETAPES = ("lunes", "arrete", "prie", "avenir", "supprime", "repens")
    PW_, PH_ = 170, 160                 # 1020 × 960 à l'écran
    TEL = (45, 10)                      # coin haut-gauche du téléphone (pixels du dessin, ×6)
    TW, TH = 80, 150
    # la scène des 40 nuits (pixels d'écran)
    Y_CARTE = 8                         # haut de la carte du hadith
    Y_ASSIM = (306, 396)                # « LIRE TON HOROSCOPE = INTERROGER UN DEVIN » / « (SELON DE NOMBREUX SAVANTS) »
    GRILLE = (159, 448, 78, 45)         # centre de la 1re lune (x, y), pas en x, pas en y (10 × 4)
    Y_COMPTEUR = 656
    Y_BANDEAU = 650                     # « ✓ TU DOIS QUAND MÊME PRIER » : à la place du compteur (sous les lunes)
    Y_TAPIS = 696                       # haut du tapis
    T_LUNE0, DT_LUNE = 0.15, 0.06       # 1re nuit, écart entre deux nuits (40 nuits en ≈ 2,6 s)
    T_40 = 2.75                         # « 40 NUITS »
    T_CARTE_B = 0.25                    # la fin de la carte
    # {quarante prie}
    T_TAMPON, T_DOIS, T_GRIS = 0.35, 0.6, 0.95
    # {quarante supprime}
    T_DIALOGUE, T_OUI, T_JETTE = 0.2, 0.6, 1.0
    T_REPENS_OUT = 0.6                  # {quarante repens} : « REPENS-TOI » et la citation s'effacent (0,35 s) après
    #                                     (contre-vérification du 08/11 : 1,5 → 0,6 ; fondu fini à + 0,95 s, avant
    #                                     « ABONNE-TOI », quelle que soit la durée de « Et repens-toi ! »)

    def __init__(s, cmd, mode="quarante", who="PETIT"):
        super().__init__(cmd)
        s.mode = mode
        s.who = who if who in ("PETIT", "GRAND") else "PETIT"
        s.negatif = mode == "astro"

    def sons_el(s):
        if s.mode == "astro":
            return [(0.0, "sa_scintillement", 0.025, None)]
        out = [(0.0, "tr_whoosh_doux", 0.03, None)]
        t = s.t
        if "lunes" in t:
            out += [(t["lunes"] + 0.1, "tr_whoosh_doux", 0.025, None), (t["lunes"] + s.T_40, "sa_ting", 0.03, None)]
        if "arrete" in t:
            out.append((t["arrete"] + 0.1, "tr_whoosh_doux", 0.02, None))
        if "prie" in t:
            out.append((t["prie"] + s.T_TAMPON, "imp_tampon", 0.03, None))
        if "avenir" in t:
            out += [(t["avenir"], "tr_whoosh_doux", 0.03, None), (t["avenir"] + 0.4, "sa_ting", 0.025, None)]
        if "supprime" in t:
            out += [(t["supprime"] + s.T_OUI, "dv_clic", 0.04, None),
                    (t["supprime"] + s.T_JETTE + 0.1, "tr_whoosh_doux", 0.025, None)]
        return out

    def image(s, u):
        if s.mode == "astro":
            return s._image_astro(u)
        return s._image_quarante(u)

    # ------------------------------------------------------------ petits outils
    def _txt(s, nom, *a, **kw):
        cle = ("txt", nom)
        if cle not in s._cache:
            s._cache[cle] = _texte_px(*a, **kw)
        return s._cache[cle]

    def _c(s, cle, f):
        if cle not in s._cache:
            s._cache[cle] = f()
        return s._cache[cle]

    def _zoomk(s, im, k, cle):
        k = round(k, 2)
        cle = ("z", cle, k)
        if cle not in s._cache:
            s._cache[cle] = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        return s._cache[cle]

    def _cadre(s, im):
        """Coins arrondis du panneau (comme le décor de {sms})."""
        m = s._c("cadre", lambda: Image.fromarray(
            (Px(s.PW_, s.PH_, alpha=True).mask_rrect(0, 0, s.PW_, s.PH_, 6) * 255).astype(np.uint8))
            .resize((s.PW_ * s.K, s.PH_ * s.K), Image.NEAREST))
        a = np.array(im)
        a[..., 3] = np.minimum(a[..., 3], np.array(m))
        return Image.fromarray(a, "RGBA")

    # ============================================================ le téléphone (accroche et {quarante supprime})
    def _corps(s):
        """Le corps du téléphone et le masque de son écran (pixels d'écran)."""
        if "corps" in s._cache:
            return s._cache["corps"]
        W, H = s.TW, s.TH
        c = Px(W, H, alpha=True)
        corps = c.mask_rrect(0, 0, W, H + 10, 10)
        c.shape(corps, (42, 42, 54), shade=(24, 24, 32), light=(100, 100, 118), band=2, olcol=OL)
        ecran = c.mask_rrect(4, 5, W - 4, H + 6, 7)
        c.fill(ecran, (12, 10, 24))
        m = Image.fromarray((ecran[5:H, 4:W - 4] * 255).astype(np.uint8)).resize(((W - 8) * s.K, (H - 5) * s.K),
                                                                                    Image.NEAREST)
        s._cache["corps"] = (c.img(s.K, rgba=True), m)
        return s._cache["corps"]

    def _couche_tel(s, ecran):
        """Le téléphone avec son écran et tes mains (vue à ta place), recadré : (image, (x, y) dans le panneau)."""
        K = s.K
        body, m = s._corps()
        lay = Image.new("RGBA", (s.PW_ * K, s.PH_ * K), (0, 0, 0, 0))
        x0, y0 = s.TEL[0] * K, s.TEL[1] * K
        lay.alpha_composite(body, (x0, y0))
        scr = ecran.copy()
        a = np.array(scr)
        a[..., 3] = np.minimum(a[..., 3], np.array(m))
        lay.alpha_composite(Image.fromarray(a, "RGBA"), (x0 + 4 * K, y0 + 5 * K))
        d = ImageDraw.Draw(lay)
        d.rounded_rectangle([x0 + 31 * K, y0 + 7 * K, x0 + 49 * K, y0 + 11 * K], 2 * K, fill=(8, 8, 14, 255))
        main, (mx, my) = Dette._main(s)                                             # (les mains du module du 07/11)
        lay.alpha_composite(main, (mx, my))
        bb = (x0 - 12 * K, y0, s.PW_ * K, s.PH_ * K)
        return lay.crop(bb), bb[:2]

    def _barre_etat(s, c, W):
        """L'heure et la batterie (blocs), sur un écran Px de largeur W (pixels du dessin)."""
        for x in (5, 8, 12, 15):
            c.fill(c.mask_rect(x, 2, x + 2, 6), (230, 226, 244))
        c.px(10, 3, (230, 226, 244))
        c.px(10, 5, (230, 226, 244))
        c.fill(c.mask_rect(W - 12, 2, W - 5, 6), (230, 226, 244))
        c.fill(c.mask_rect(W - 5, 3, W - 4, 5), (230, 226, 244))

    def _logo(s, k=6, r=6):
        """Le logo rond de l'appli (une étoile dorée sur violet : simple logo, aucun signe réel)."""
        cle = ("logo", k, r)
        if cle not in s._cache:
            n = 2 * r + 2
            c = Px(n, n, alpha=True)
            rond = c.mask_ell(n / 2, n / 2, r, r)
            c.shape(rond, VIOLET_C, shade=VIOLET, light=(196, 170, 240), band=1, olcol=OL)
            cx, cy = n / 2, n / 2 + 0.3
            pts = []
            for i in range(10):
                ang = -math.pi / 2 + i * math.pi / 5
                rr = (r * 0.68) if i % 2 == 0 else (r * 0.3)
                pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
            et = c.mask_poly(pts)
            c.fill(et, (255, 214, 90))
            c.fill(et & c.mask_rect(0, cy, n, n), (226, 168, 40))
            s._cache[cle] = c.img(k, rgba=True)
        return s._cache[cle]

    def _sac(s):
        """Le sac d'argent pixel (« € » dessiné en blocs)."""
        if "sac" not in s._cache:
            c = Px(16, 17, alpha=True)
            sac = c.mask_ell(8, 11, 7, 5.6) | c.mask_poly([(5, 6), (11, 6), (9.5, 8), (6.5, 8)])
            c.shape(sac, (196, 150, 82), shade=(150, 108, 52), light=(226, 190, 120), band=2, olcol=OL)
            noeud = c.mask_rect(5, 4, 11, 6)
            c.shape(noeud, (150, 108, 52), band=1, olcol=OL)
            c.fill(c.mask_poly([(4, 1), (7, 4), (9, 4), (12, 1), (9, 2.5), (7, 2.5)]), (196, 150, 82))
            c.outline(c.mask_poly([(4, 1), (7, 4), (9, 4), (12, 1), (9, 2.5), (7, 2.5)]), OL)
            c.text((8, 6), "€", (255, 226, 110), size=10, font=TAHOMA, anchor="ma")
            s._cache["sac"] = c.img(5, rgba=True)
        return s._cache["sac"]

    def _coeur(s):
        if "coeur" not in s._cache:
            c = Px(9, 8, alpha=True)
            m = c.mask_ell(2.6, 2.6, 2.4, 2.4) | c.mask_ell(6.4, 2.6, 2.4, 2.4) | c.mask_poly([(0.4, 3), (8.6, 3),
                                                                                              (4.5, 7.6)])
            c.fill(m, (240, 80, 120))
            c.outline(m, OL)
            s._cache["coeur"] = c.img(4, rgba=True)
        return s._cache["coeur"]

    def _ecran_fond(s):
        """L'écran de l'appli (sans le fil) : violet nuit étoilé, barre d'état, en-tête « TON HOROSCOPE / DU JOUR »."""
        if "efond" in s._cache:
            return s._cache["efond"]
        K = s.K
        W, H = s.TW - 8, s.TH - 5
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rect(0, 0, W, H)
        c.vgrad(tout_, 0, H, (40, 22, 82), (74, 40, 118), steps=6)
        rng = np.random.default_rng(11)
        for _ in range(34):
            c.px(int(rng.integers(1, W - 1)), int(rng.integers(30, H - 1)), (196, 180, 236))
        haut = c.mask_rect(0, 0, W, 29)
        c.fill(haut, (26, 14, 56))
        c.fill(c.mask_rect(0, 29, W, 30), (110, 80, 170))
        s._barre_etat(c, W)
        im = c.img(K, rgba=True)
        lg = s._logo(5, 6)
        im.alpha_composite(lg, (4 * K, int(19 * K - lg.height / 2)))
        t1 = _texte_px("TON HOROSCOPE", BLANC, 11, k=3, pad=0, gras=True)
        t2 = _texte_px("DU JOUR", (255, 214, 90), 11, k=3, pad=0, gras=True)
        im.alpha_composite(t1, (18 * K, 10 * K))
        im.alpha_composite(t2, (18 * K, 10 * K + t1.height - 6))
        s._cache["efond"] = im
        return im

    def _fil(s):
        """Le fil de l'appli : la carte « TON HOROSCOPE : » / « TU SERAS » / « RICHE ! » + sac, « ♥ 12 K », puis le
        haut d'une 2e carte (des traits pâles : rien d'autre à lire)."""
        if "fil" in s._cache:
            return s._cache["fil"]
        K = s.K
        W = s.TW - 8
        c = Px(W, 112, alpha=True)
        carte = c.mask_rrect(3, 0, W - 3, 76, 4)
        c.shape(carte, (58, 32, 110), shade=(44, 24, 88), light=(96, 64, 160), band=1, olcol=(150, 116, 214))
        c.fill(c.mask_rect(8, 60, W - 8, 61), (96, 70, 150))
        c2 = c.mask_rrect(3, 84, W - 3, 140, 4)
        c.shape(c2, (58, 32, 110), shade=(44, 24, 88), light=(96, 64, 160), band=1, olcol=(150, 116, 214))
        for j, y in enumerate((92, 98, 104)):
            c.fill(c.mask_rect(9, y, 9 + (44, 52, 30)[j], y + 2), (110, 86, 164))
        im = c.img(K, rgba=True)
        l0 = _texte_px("TON HOROSCOPE :", (196, 180, 236), 10, k=4, pad=0)
        im.alpha_composite(l0, (9 * K, 4 * K))
        l1 = _texte_px("TU SERAS", BLANC, 12, k=5, pad=0, gras=True)
        im.alpha_composite(l1, (9 * K, 16 * K))
        l2 = _texte_px("RICHE !", (255, 214, 90), 12, k=5, pad=1, gras=True, bord=(70, 34, 10))
        im.alpha_composite(l2, (9 * K - 5, 31 * K))
        sac = s._sac()
        im.alpha_composite(sac, (int(9 * K + l2.width + 4), int(31 * K + l2.height / 2 - sac.height / 2) - 6))
        cr = s._coeur()
        im.alpha_composite(cr, (10 * K, 65 * K))
        l3 = _texte_px("12 K", (236, 220, 250), 10, k=4, pad=0)
        im.alpha_composite(l3, (10 * K + cr.width + 10, int(65 * K + cr.height / 2 - l3.height / 2)))
        s._cache["fil"] = im
        return im

    def _ecran_astro(s, u):
        K = s.K
        e = s._ecran_fond().copy()
        fil = s._fil()
        off = 70 * (1 - smooth((u + 0.3) / 2.6))                                   # le fil défile doucement vers le haut
        y_fil = int(35 * K + off)
        clip = Image.new("RGBA", e.size, (0, 0, 0, 0))
        clip.alpha_composite(fil, (0, y_fil))
        clip = clip.crop((0, 30 * K, e.width, e.height))
        e.alpha_composite(clip, (0, 30 * K))
        return e

    # ============================================================ l'accroche : la chambre floue
    def _chambre(s):
        """La chambre d'ado le soir, floue : mur bleu nuit, fenêtre (ciel de nuit), étagère, poster de foot, lampe
        chaude ; le bureau en bas avec la carte de tarot retournée et la petite boule de cristal (vides)."""
        if "chambre" in s._cache:
            return s._cache["chambre"]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rect(0, 0, W, H)
        c.vgrad(tout_, 0, 116, (40, 36, 74), (78, 58, 96), steps=6)
        fen = c.mask_rect(6, 10, 50, 66)                                            # la fenêtre
        c.shape(fen, (120, 92, 70), shade=(90, 66, 50), band=2, olcol=OL)
        vitre = c.mask_rect(9, 13, 47, 63)
        c.vgrad(vitre, 13, 63, (14, 18, 52), (44, 46, 96), steps=5)
        for (x, y) in ((14, 20), (24, 30), (38, 18), (42, 40), (18, 48), (30, 54)):
            c.px(x, y, (220, 220, 250))
        c.fill(c.mask_rect(27, 13, 29, 63), (120, 92, 70))
        c.fill(c.mask_rect(9, 37, 47, 39), (120, 92, 70))
        poster = c.mask_rect(116, 12, 146, 52)                                      # un poster de foot (sans texte)
        c.shape(poster, (60, 140, 80), shade=(44, 110, 60), band=1, olcol=OL)
        c.fill(c.mask_rect(119, 31, 143, 32), (230, 240, 230))
        c.fill(c.mask_ell(131, 31.5, 5, 5) & ~c.mask_ell(131, 31.5, 4, 4), (230, 240, 230))
        c.fill(c.mask_ell(126, 22, 3, 3), (250, 250, 250))
        eta = c.mask_rect(84, 66, 156, 70)                                          # l'étagère et ses livres
        c.shape(eta, (130, 94, 66), shade=(96, 66, 46), band=1, olcol=OL)
        x = 88
        for j, (w_, h_, col) in enumerate(((5, 14, (190, 60, 60)), (4, 11, (60, 110, 190)), (6, 15, (230, 180, 60)),
                                           (4, 12, (90, 170, 110)), (5, 13, (170, 90, 170)))):
            c.shape(c.mask_rect(x, 66 - h_, x + w_, 66), col, band=1, olcol=OL)
            x += w_ + 1
        pied = c.mask_rect(154, 82, 157, 112)                                       # la lampe
        c.fill(pied, (60, 56, 70))
        abat = c.mask_poly([(146, 72), (164, 72), (168, 84), (142, 84)])
        c.shape(abat, (250, 210, 120), shade=(220, 168, 80), light=(255, 236, 170), band=2, olcol=OL)
        bureau = c.mask_rect(0, 112, W, H)                                          # le bureau
        c.fill(bureau, (118, 80, 56))
        c.dither(bureau, (104, 70, 50), 0.25)
        c.fill(c.mask_rect(0, 112, W, 114), (156, 112, 78))
        c.fill(c.mask_rect(0, 114, W, 115), (80, 52, 38))
        # la carte de tarot, retournée (dos violet à petites étoiles, AUCUNE figure)
        tarot = c.mask_poly([(2, 121), (21, 118), (25, 131), (5, 135)])
        c.shape(tarot, (96, 56, 150), shade=(70, 40, 116), light=(130, 92, 190), band=1, olcol=OL)
        c.outline(c.mask_poly([(4, 122), (20, 119.5), (23.5, 130), (6, 133.5)]) & tarot, (220, 190, 110))
        for (x, y) in ((10, 124), (16, 127), (12, 130)):
            c.px(x, y, (255, 226, 140))
        # la petite boule de cristal sur son socle (reflet FIXE, rien dedans)
        socle = c.mask_poly([(10, 152), (32, 152), (29, 146), (13, 146)])
        c.shape(socle, (120, 84, 56), shade=(86, 58, 40), light=(156, 112, 76), band=1, olcol=OL)
        boule = c.mask_ell(21, 138, 10, 9.5)
        c.shape(boule, (130, 170, 220), shade=(84, 118, 176), light=(176, 206, 240), sdir="right", band=3, olcol=OL)
        c.fill(c.mask_ell(16.5, 133, 2.6, 1.8), (236, 246, 255))
        im = c.img(s.K, rgba=True).convert("RGB").filter(ImageFilter.GaussianBlur(7))
        im = im.convert("RGBA")
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))                              # pénombre sur les bords
        ImageDraw.Draw(lay).rectangle([0, 0, im.width, im.height], fill=(10, 6, 20, 96))
        trou = Image.new("L", im.size, 0)
        ImageDraw.Draw(trou).ellipse([170, 40, 900, 1000], fill=255)
        trou = trou.filter(ImageFilter.GaussianBlur(100))
        a = np.array(lay)
        a[..., 3] = (a[..., 3].astype(float) * (1 - np.array(trou) / 255.0)).astype(np.uint8)
        im.alpha_composite(Image.fromarray(a, "RGBA"))
        _colle(im, _halo(300, 260, (255, 196, 110), 60), 930, 470, 0.32)          # la lueur chaude de la lampe
        s._cache["chambre"] = s._cadre(im)
        return s._cache["chambre"]

    def _image_astro(s, u):
        im = s._chambre().copy()
        tel, (lx, ly) = s._couche_tel(s._ecran_astro(u))
        e = smooth((u + 0.3) / 1.5)                                                 # il monte vers toi (85 % → 100 %)
        z = 0.85 + 0.15 * e                                                         # (planche du 08/11 : plus grand dès l'image 0)
        dx = 2.0 * math.sin(2 * math.pi * u / 3.4)                                 # puis il respire
        dy = 4.0 * math.sin(2 * math.pi * u / 2.6) * e
        if z < 0.999:
            tel = tel.resize((int(tel.width * z), int(tel.height * z)), Image.BILINEAR)
        X1, Y1 = s.PW_ * s.K, s.PH_ * s.K                                          # ancré en bas à droite (la manche)
        x = X1 - (X1 - lx) * z
        y = Y1 - (Y1 - ly) * z + 30 * (1 - e)
        _colle(im, _halo(tel.width * 0.7, 160, (8, 4, 14), 36), x + tel.width * 0.45, Y1 - 40, 0.55)
        im.alpha_composite(tel, (int(x + dx), int(y + dy)))
        return s._cadre(im)

    # ============================================================ {quarante} : les 40 nuits
    def _ciel(s, n=0):
        """Ciel de nuit, étoiles fixes (n = 1 : le ciel du parchemin, un peu plus clair)."""
        cle = ("ciel", n)
        if cle in s._cache:
            return s._cache[cle]
        W, H = s.PW_, s.PH_
        c = Px(W, H, alpha=True)
        tout_ = c.mask_rrect(0, 0, W, H, 6)
        h_, b_ = (NUIT_H, NUIT_B) if n == 0 else ((20, 16, 54), (52, 40, 100))
        c.vgrad(tout_, 0, H, h_, b_, steps=7)
        rng = np.random.default_rng(21 + n)
        for _ in range(70):
            c.px(int(rng.integers(2, W - 2)), int(rng.integers(2, H - 2)), (150, 156, 196))
        for _ in range(14):
            x, y = int(rng.integers(3, W - 3)), int(rng.integers(3, H - 3))
            c.fill(c.mask_rect(x, y, x + 1, y + 1) | c.mask_rect(x, y, x + 1, y + 1), (226, 228, 255))
        s._cache[cle] = c.img(s.K, rgba=True)
        return s._cache[cle]

    def _scintille(s, im, u, n=0):
        """Quelques étoiles qui brillent lentement (période 3 à 5 s : aucun clignotement)."""
        rng = np.random.default_rng(31 + n)
        pts = [(int(rng.integers(20, 1000)), int(rng.integers(20, 940)), float(rng.uniform(3, 5)),
                float(rng.uniform(0, 6.3))) for _ in range(9)]

        def des(d):
            for (x, y, p, ph) in pts:
                a = 0.25 + 0.45 * (0.5 + 0.5 * math.sin(2 * math.pi * u / p + ph))
                _etincelle(d, x, y, 2, a, coeur=(236, 238, 255), bord=(110, 120, 190))
        _translucide(im, des)

    def _carte(s):
        """La carte du hadith (bandeau sombre) : la 1re partie seulement ; la fin est posée à part."""
        if "carte" in s._cache:
            return s._cache["carte"]
        W_ = 1000
        lig = [_texte_px(CARTE_L1, (230, 206, 140), 11, k=3, pad=0)]
        lig += [_texte_px(t_, BLANC, 12, k=3, pad=0, gras=True) for t_ in CARTE_A + CARTE_B]
        H_ = 16 + lig[0].height - 2 + 4 * (lig[1].height - 5) + 16
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 18, fill=(14, 12, 32, 236), outline=(110, 96, 168, 255), width=6)
        ys = [16]
        ys.append(ys[0] + lig[0].height - 2)
        for _ in range(3):
            ys.append(ys[-1] + lig[1].height - 5)
        for j in (0, 1, 2):
            im.alpha_composite(lig[j], (int(W_ / 2 - lig[j].width / 2), ys[j]))
        s._cache["carte"] = im
        s._cache["carte_b"] = [(lig[j], int(W_ / 2 - lig[j].width / 2), ys[j]) for j in (3, 4)]
        return im

    def _lune(s, allumee):
        cle = ("lune", allumee)
        if cle not in s._cache:
            c = Px(15, 14, alpha=True)
            m = c.mask_ell(6.5, 7, 6, 6) & ~c.mask_ell(9.6, 5.6, 5, 5)
            if allumee:
                c.shape(m, LUNE_L, shade=(170, 176, 196), light=(240, 242, 250), band=1, olcol=(40, 44, 70))
            else:
                c.fill(m, LUNE_S)
                c.outline(m, (128, 134, 162))
            s._cache[cle] = c.img(4, rgba=True)
        return s._cache[cle]

    def _tapis(s, f=0.0):
        """Le tapis de prière vide, vert et or, vu de trois quarts (le haut, plus étroit, vers la qibla) ; f = gris."""
        cle = ("tapis", round(f, 2))
        if cle in s._cache:
            return s._cache[cle]
        if "tapis0" not in s._cache:
            c = Px(86, 30, alpha=True)
            tap = c.mask_poly([(15, 1), (71, 1), (85, 29), (1, 29)])
            c.shape(tap, (40, 130, 74), shade=(30, 100, 58), light=(70, 160, 98), band=1, olcol=OL)
            bord = tap & ~c.mask_poly([(18, 3), (68, 3), (80, 27), (6, 27)])
            c.fill(bord, (214, 170, 60))
            c.fill(c.mask_poly([(21, 5), (65, 5), (76, 25), (10, 25)]) & ~c.mask_poly([(22, 6), (64, 6),
                                                                                      (74.5, 24), (11.5, 24)]),
                   (190, 150, 50))
            arc = c.mask_poly([(36, 21), (36, 12), (39, 8), (43, 6), (47, 8), (50, 12), (50, 21)])
            c.fill(arc, (30, 104, 60))
            c.outline(arc, (214, 170, 60))
            c.fill(c.mask_ell(43, 4, 1.4, 1.2), (240, 200, 90))
            for x in range(3, 84, 3):                                               # les franges du bas
                c.fill(c.mask_rect(x, 29, x + 1, 30), (236, 224, 190))
            s._cache["tapis0"] = c.img(5, rgba=True)
        s._cache[cle] = _desature(s._cache["tapis0"], f) if f > 0.005 else s._cache["tapis0"]
        return s._cache[cle]

    def _bulle(s):
        """La bulle de pensée de Petit : le tapis qu'on roule (un rouleau vert et or)."""
        if "bulle" in s._cache:
            return s._cache["bulle"]
        c = Px(48, 42, alpha=True)
        m = (c.mask_ell(24, 15, 18, 12) | c.mask_ell(12, 18, 10, 9) | c.mask_ell(36, 18, 10, 9)
             | c.mask_ell(18, 8, 9, 7) | c.mask_ell(31, 8, 9, 7))
        c.shape(m, (238, 238, 248), shade=(196, 198, 216), light=(255, 255, 255), band=1, olcol=OL)
        for (x, y, r) in ((14, 31, 3.2), (9, 37, 2.2)):
            p = c.mask_ell(x, y, r, r)
            c.shape(p, (238, 238, 248), shade=(196, 198, 216), band=1, olcol=OL)
        rou = c.mask_rrect(11, 12, 37, 21, 4)
        c.shape(rou, (40, 130, 74), shade=(30, 100, 58), light=(76, 166, 104), sdir="bottom", band=2, ldir="top",
                lband=1, olcol=OL)
        for x in (17, 23, 29):
            c.fill(c.mask_rect(x, 13, x + 1, 20) & rou, (214, 170, 60))
        bout = c.mask_ell(37, 16.5, 3, 4.5)
        c.shape(bout, (214, 170, 60), shade=(170, 130, 40), band=1, olcol=OL)
        c.fill(c.mask_ell(37, 16.5, 1.2, 2), (30, 100, 58))
        s._cache["bulle"] = c.img(5, rgba=True)
        return s._cache["bulle"]

    def _tampon(s):
        """Le tampon orange à deux lignes « VALABLE, MAIS » / « SANS RÉCOMPENSE », penché de −6°."""
        if "tampon" in s._cache:
            return s._cache["tampon"]
        from PIL import ImageFont
        f1 = ImageFont.truetype(TAHOMA, 14)
        W, H = int(f1.getlength("SANS RÉCOMPENSE")) + 22, 42
        c = Px(W, H, alpha=True)
        cadre = c.mask_rrect(0, 0, W, H, 3) & ~c.mask_rrect(2, 2, W - 2, H - 2, 2)
        cadre |= c.mask_rrect(4, 4, W - 4, H - 4, 1) & ~c.mask_rrect(5, 5, W - 5, H - 5, 1)
        c.fill(cadre, ORANGE)
        c.text((W / 2, 19), "VALABLE, MAIS", ORANGE, size=14, font=TAHOMA, anchor="ms")
        c.text((W / 2, 35), "SANS RÉCOMPENSE", ORANGE, size=14, font=TAHOMA, anchor="ms")
        encre = c.al.copy()
        rng = np.random.default_rng(9)
        c.fill(encre & (rng.random((H, W)) < 0.10), (206, 100, 20))
        c.outline(encre, (255, 244, 230))
        enc = c.img(4, rgba=True)
        # (planche du 08/11 : posé sur les lunes, il se lisait mal → une carte sombre derrière l'encre)
        fond = Image.new("RGBA", (enc.width + 24, enc.height + 24), (0, 0, 0, 0))
        ImageDraw.Draw(fond).rounded_rectangle([0, 0, fond.width - 1, fond.height - 1], 18, fill=(16, 12, 30, 225))
        fond.alpha_composite(enc, (12, 12))
        s._cache["tampon"] = _tourne_net(fond, -6)
        return s._cache["tampon"]

    def _bandeau(s, txt, size=46, fond=VERT, coche=True):
        cle = ("bandeau", txt, size)
        if cle in s._cache:
            return s._cache[cle]
        t_ = _titre(txt, BLANC, size)
        ims = ([_coche(BLANC, 5)] if coche else []) + [t_]
        row = _cote(ims, 4)
        W_, H_ = row.width + 44, row.height + 4
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 6, W_ - 1, H_ - 7], 22, fill=(*OL, 255))
        d.rounded_rectangle([6, 12, W_ - 7, H_ - 13], 17, fill=(*fond, 255))
        d.rounded_rectangle([6, 12, W_ - 7, 22], 8, fill=tuple(min(255, v + 34) for v in fond) + (255,))
        im.alpha_composite(row, (22, 2))
        s._cache[cle] = im
        return im

    def _scene_nuits(s, u):
        """Le ciel des 40 nuits (tout ce qui part avec lui à {quarante avenir})."""
        K = s.K
        im = s._ciel(0).copy()
        s._scintille(im, u, 0)
        tl = s.t.get("lunes")
        ta, tp = s.t.get("arrete"), s.t.get("prie")
        prog = 0.0                                                                  # part des nuits passées
        if tl is not None:
            prog = min(1.0, max(0.0, (u - tl - s.T_LUNE0) / (39 * s.DT_LUNE + 0.2)))
        # la carte du hadith (et sa fin), puis la ligne « LIRE TON HOROSCOPE = INTERROGER UN DEVIN »
        carte = s._carte()
        e0 = smooth(u / 0.5)
        im.alpha_composite(_fade(carte, e0), (10, int(s.Y_CARTE + 20 * (1 - e0))))
        if tl is not None:
            eb = smooth((u - tl - s.T_CARTE_B) / 0.4)
            for (l_, x, y) in s._cache["carte_b"]:
                if eb > 0.01:
                    im.alpha_composite(_fade(l_, eb), (10 + x, int(s.Y_CARTE + y + 10 * (1 - eb))))
        ea = smooth((u - 0.25) / 0.45)
        sa = 1.0 if tp is None else 1 - smooth((u - tp) / 0.35)                   # (réplique 2 finie : place au tampon)
        assim = s._c("assim", lambda: _lignes(["LIRE TON HOROSCOPE =", "INTERROGER UN DEVIN"], BLANC, 42, serre=38))
        s._pose(im, assim, 510, s.Y_ASSIM[0] + 14 * (1 - ea), ea * sa, maxw=980)
        nb = s._lab("(SELON DE NOMBREUX SAVANTS)", (214, 216, 232), 30)
        s._pose(im, nb, 510, s.Y_ASSIM[1] + 10 * (1 - ea), smooth((u - 0.45) / 0.45) * sa, maxw=900)
        # les 40 nuits
        x0, y0, px_, py_ = s.GRILLE
        sombre, claire, ch = s._lune(False), s._lune(True), s._c("ch", lambda: _coche(BLANC, 3))
        el = smooth((u - 0.15) / 0.5)
        for i in range(40):
            cx, cy = x0 + px_ * (i % 10), y0 + py_ * (i // 10) + 12 * (1 - el)
            f = 0.0 if tl is None else smooth((u - tl - s.T_LUNE0 - i * s.DT_LUNE) / 0.2)
            if f < 0.999:
                _colle(im, sombre, cx, cy, el)
            if f > 0.01:
                _colle(im, claire, cx, cy, f)
                fc = smooth((u - tl - s.T_LUNE0 - i * s.DT_LUNE - 0.1) / 0.25)
                _colle(im, ch, cx + 15, cy + 4 - 4 * (1 - fc), fc)
        # « RÉCOMPENSE : 0 » (il reste à 0 et pâlit)
        ec = smooth((u - 0.35) / 0.45)
        if tp is not None:                                                          # le bandeau vert prend sa place
            ec *= 1 - smooth((u - tp - s.T_DOIS + 0.1) / 0.35)
        rc = s._lab("RÉCOMPENSE : 0", OR_, 46)
        rg = s._lab("RÉCOMPENSE : 0 ", (150, 146, 128), 46)
        s._pose(im, rc, 510, s.Y_COMPTEUR, ec * (1 - 0.75 * prog), maxw=700)
        s._pose(im, rg, 510, s.Y_COMPTEUR, ec * 0.75 * prog, maxw=700)
        # le tapis (il se désature à 60 % avec les nuits, et le reste)
        tap = s._tapis(round(0.6 * prog, 2))
        et = smooth((u - 0.2) / 0.5)
        im.alpha_composite(_fade(tap, et), (int(510 - tap.width / 2), int(s.Y_TAPIS + 16 * (1 - et))))
        if tl is not None:                                                          # « ✓ PRIÈRE FAITE » sur le tapis
            ep = smooth((u - tl - s.T_LUNE0) / 0.35)
            pf = s._c("pfaite", lambda: _cote([_coche(BLANC, 5), _titre("PRIÈRE FAITE", BLANC, 36)], 2))
            s._pose(im, pf, 510, s.Y_TAPIS + 92 - 8 * ep, ep, maxw=420)
            e40 = smooth((u - tl - s.T_40) / 0.45)                                  # « 40 NUITS »
            if tp is not None:
                e40 *= 1 - smooth((u - tp) / 0.35)
            if e40 > 0.01:
                t40 = s._lab("40 NUITS", BLANC, 104)
                s._pose(im, s._zoomk(t40, 0.9 + 0.1 * e40, "t40"), 510, 516, e40)
                j40 = s._lab("(= 40 JOURS DE PRIÈRES)", BLANC, 30)                # pas seulement les prières de nuit
                s._pose(im, j40, 510, 598 + 6 * (1 - e40), e40, maxw=700)
        # {quarante arrete} : la bulle de Petit et le « ? » ; {quarante prie} : barrée puis effacée
        if ta is not None or tp is not None:
            t_b = ta if ta is not None else tp
            eb = smooth((u - t_b) / 0.35)
            if tp is not None:
                eb *= 1 - smooth((u - tp - 0.9) / 0.4)
            if eb > 0.01:
                bu = s._bulle()
                bx, by = 136, 776
                _colle(im, bu, bx, by + 14 * (1 - smooth((u - t_b) / 0.35)), eb)
                q = s._lab("?", (255, 150, 40), 96)
                _colle(im, q, 60, 680 - 10 * (1 - smooth((u - t_b - 0.15) / 0.35)), eb * smooth((u - t_b - 0.15) / 0.3))
                if tp is not None:                                                  # la croix rouge, tracée doucement
                    v = u - tp
                    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
                    d = ImageDraw.Draw(lay)
                    for j, (a0, a1) in enumerate((((36, 690), (236, 864)), ((236, 690), (36, 864)))):
                        p = smooth((v - 0.05 - 0.2 * j) / 0.25)
                        if p > 0.01:
                            xe, ye = a0[0] + (a1[0] - a0[0]) * p, a0[1] + (a1[1] - a0[1]) * p
                            d.line([a0, (xe, ye)], fill=(*OL, 255), width=26)
                            d.line([a0, (xe, ye)], fill=(226, 56, 56, 255), width=16)
                    im.alpha_composite(_fade(lay, eb))
        if tp is not None:                                                          # le tampon, le bandeau, la ligne grise
            v = u - tp
            f = smooth((v - s.T_TAMPON + 0.35) / 0.35)
            if f > 0.01:
                tb = s._tampon()
                tb_ = s._zoomk(tb, 1.15 - 0.15 * f, "tampon") if f < 0.999 else tb
                _colle(im, tb_, 510, 380 - 44 * (1 - f), min(1.0, f * 1.6))        # (sur la place libérée par « LIRE… »)
            ed = smooth((v - s.T_DOIS) / 0.4)
            s._pose(im, s._bandeau("TU DOIS QUAND MÊME PRIER"), 510, s.Y_BANDEAU + 14 * (1 - ed), ed, maxw=990)
            eg = smooth((v - s.T_GRIS) / 0.4)
            g1 = s._lab("ELLE COMPTE : TU NE LA REFAIS PAS", GRIS_T, 30)
            g2 = s._lab("(EXPLICATION D'AN-NAWAWI)", (170, 172, 190), 26)
            s._pose(im, g1, 510, 870, eg, maxw=900)
            s._pose(im, g2, 510, 914, eg, maxw=700)
        return im

    # ============================================================ {quarante avenir} : le parchemin (Coran 27:65)
    def _parchemin(s):
        if "parch" in s._cache:
            return s._cache["parch"]
        K = s.K
        W, H = 160, 92
        c = Px(W, H, alpha=True)
        X0, X1 = 14, 146
        feuille = c.mask_rect(X0, 7, X1, H - 7)
        c.fill(feuille, (244, 232, 200))
        c.dither(feuille, (234, 218, 182), 0.16)
        c.edge(feuille, (226, 206, 166), "right", 2)
        c.edge(feuille, (252, 244, 222), "left", 1)
        c.outline(feuille, OL)
        for (y0, y1) in ((1, 12), (H - 12, H - 1)):
            r = c.mask_rrect(X0 - 7, y0, X1 + 7, y1, 5)
            c.shape(r, (216, 188, 138), shade=(172, 142, 98), light=(238, 218, 176), sdir="bottom", band=3, ldir="top",
                    lband=2, olcol=OL)
            for xb in (X0 - 11, X1 + 5):
                bout = c.mask_rrect(xb, y0 + 2, xb + 6, y1 - 2, 2)
                c.shape(bout, (150, 98, 60), shade=(112, 70, 42), light=(184, 130, 84), band=1, olcol=OL)
        im = c.img(K, rgba=True)
        cx = W * K / 2
        ti = _texte_px("QUI CONNAÎT TON AVENIR ?", (206, 96, 18), 13, k=4, pad=0, gras=True)
        im.alpha_composite(ti, (int(cx - ti.width / 2), 16 * K))
        y = 16 * K + ti.height + 14
        for t_ in VERSET:
            l_ = _texte_px(t_, ENCRE, 12, k=3, pad=0, gras=True)
            im.alpha_composite(l_, (int(cx - l_.width / 2), y))
            y += l_.height + 2
        a1 = _texte_px("À PART ", ENCRE, 12, k=3, pad=1, gras=True)                 # « ALLAH » seul en or
        a2 = _texte_px("ALLAH", (232, 170, 30), 12, k=3, pad=1, gras=True, bord=(96, 56, 14))
        a3 = _texte_px(". »", ENCRE, 12, k=3, pad=1, gras=True)
        ww = a1.width + a2.width + a3.width - 12
        x = int(cx - ww / 2)
        im.alpha_composite(a1, (x, y - 3))
        im.alpha_composite(a2, (x + a1.width - 6, y - 3))
        im.alpha_composite(a3, (x + a1.width + a2.width - 12, y - 3))
        ex = _texte_px("(EXTRAIT)", (120, 92, 70), 10, k=3, pad=0)
        im.alpha_composite(ex, (int(X1 * K - ex.width - 30), int((H - 12) * K - ex.height - 12)))
        s._cache["parch"] = im
        return im

    def _icone_appli(s):
        if "icone" not in s._cache:
            lg = s._logo(7, 7)
            q = _titre("?", (176, 178, 192), 70)
            s._cache["icone"] = _cote([lg, q], 4)
        return s._cache["icone"]

    def _scene_avenir(s, im, u):
        ta, ts = s.t["avenir"], s.t.get("supprime")
        v = u - ta
        sortie = 1.0 if ts is None else 1 - smooth((u - ts) / 0.3)                 # {quarante supprime} : tout s'efface
        # (0,3 s : le parchemin 27:65 est parti quand l'étiquette passe à « CORAN 42:25 » et avant « REPENS-TOI »)
        if sortie <= 0.01:
            return
        # (planche du 08/11 : le schéma démarre avec « Musulman ! » → l'étiquette entre tout de suite, sinon ≈ 0,5 s vide)
        ep = smooth((v - 0.3) / 0.5)
        pa = s._parchemin()
        _colle(im, pa, 510, 520 + 20 * (1 - ep), ep * sortie)
        es = smooth(v / 0.4)                                                        # « TON SIGNE : MUSULMAN ✓ »
        lab = s._c("signe", lambda: s._bandeau("TON SIGNE : MUSULMAN", 40, coche=False))
        lab2 = s._c("signe2", lambda: _cote([lab, _coche((120, 240, 140), 6)], 0))
        s._pose(im, lab2, 510, 130 + 40 * (1 - es), es * sortie, maxw=900)
        ei = smooth((v - 1.0) / 0.5)
        ic = s._icone_appli()
        _colle(im, ic, 150, 872 + 10 * (1 - ei), ei * sortie)

    # ============================================================ {quarante supprime} : l'appli à la corbeille
    def _ecran_accueil(s):
        """L'écran d'accueil (fond bleu nuit, quelques applis sans nom) ; l'icône « HOROSCOPE » et la corbeille sont
        posées à part."""
        if "accueil" in s._cache:
            return s._cache["accueil"]
        W, H = s.TW - 8, s.TH - 5
        c = Px(W, H, alpha=True)
        c.vgrad(c.mask_rect(0, 0, W, H), 0, H, (20, 34, 70), (36, 70, 110), steps=6)
        s._barre_etat(c, W)
        for j, (x, y, col) in enumerate(((7, 12, (60, 170, 90)), (29, 12, (60, 120, 210)), (51, 12, (240, 150, 50)),
                                         (7, 36, (220, 70, 80)), (51, 36, (80, 190, 200)))):
            ic = c.mask_rrect(x, y, x + 15, y + 15, 4)
            c.shape(ic, col, shade=tuple(int(v * 0.75) for v in col), light=tuple(min(255, v + 40) for v in col),
                    band=1, olcol=OL)
            c.fill(c.mask_rrect(x + 4, y + 4, x + 11, y + 11, 2), tuple(min(255, v + 70) for v in col))
        s._cache["accueil"] = c.img(s.K, rgba=True)
        return s._cache["accueil"]

    def _icone_horo(s):
        """L'icône de l'appli sur l'écran d'accueil, avec son nom « HOROSCOPE »."""
        if "ihoro" not in s._cache:
            c = Px(17, 17, alpha=True)
            ic = c.mask_rrect(1, 1, 16, 16, 4)
            c.shape(ic, VIOLET_C, shade=VIOLET, light=(196, 170, 240), band=1, olcol=OL)
            im = c.img(6, rgba=True)
            lg = s._logo(5, 6)
            im.alpha_composite(lg, (int(im.width / 2 - lg.width / 2), int(im.height / 2 - lg.height / 2)))
            nom = _texte_px("HOROSCOPE", BLANC, 9, k=3, pad=1, bord=OL)
            out = Image.new("RGBA", (max(im.width, nom.width), im.height + nom.height), (0, 0, 0, 0))
            out.alpha_composite(im, (int(out.width / 2 - im.width / 2), 0))
            out.alpha_composite(nom, (int(out.width / 2 - nom.width / 2), im.height))
            s._cache["ihoro"] = out
        return s._cache["ihoro"]

    def _corbeille(s, ouvert):
        cle = ("corb", round(ouvert, 1))
        if cle not in s._cache:
            c = Px(20, 24, alpha=True)
            cuve = c.mask_poly([(3, 8), (17, 8), (15.5, 23), (4.5, 23)])
            c.shape(cuve, (186, 192, 206), shade=(140, 146, 164), light=(220, 224, 236), band=1, olcol=OL)
            for x in (7, 10, 13):
                c.fill(c.mask_rect(x, 10, x + 1, 21), (130, 136, 154))
            dy = -2.5 * ouvert
            cou = c.mask_rrect(1, 4 + dy, 19, 7 + dy, 1) | c.mask_rect(8, 2 + dy, 12, 4 + dy)
            c.shape(cou, (200, 206, 220), shade=(150, 156, 174), band=1, olcol=OL)
            s._cache[cle] = c.img(5, rgba=True)
        return s._cache[cle]

    def _dialogue(s, oui):
        cle = ("dial", round(oui, 1))
        if cle in s._cache:
            return s._cache[cle]
        W_, H_ = 400, 250
        im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 24, fill=(*OL, 255))
        d.rounded_rectangle([5, 5, W_ - 6, H_ - 6], 20, fill=(246, 244, 252, 255))
        l1 = _texte_px("SUPPRIMER", (40, 34, 60), 11, k=4, pad=0, gras=True)
        l2 = _texte_px("« HOROSCOPE » ?", VIOLET, 11, k=4, pad=0, gras=True)
        im.alpha_composite(l1, (int(W_ / 2 - l1.width / 2), 22))
        im.alpha_composite(l2, (int(W_ / 2 - l2.width / 2), 22 + l1.height + 2))
        for j, (txt, fond) in enumerate((("NON", (200, 202, 214)), ("OUI", (220, 64, 64)))):
            x0 = 30 + j * 180
            col = fond if j == 0 else tuple(int(a + (b - a) * oui) for a, b in zip(fond, VERT))
            d.rounded_rectangle([x0, 160, x0 + 160, 226], 14, fill=(*OL, 255))
            d.rounded_rectangle([x0 + 4, 164, x0 + 156, 222], 11, fill=(*col, 255))
            t_ = _texte_px(txt, BLANC if j else (60, 60, 76), 11, k=4, pad=0, gras=True)
            xt = x0 + 80 - t_.width / 2 - (18 * oui if j else 0)
            im.alpha_composite(t_, (int(xt), int(193 - t_.height / 2)))
            if j and oui > 0.01:
                im.alpha_composite(_fade(_coche(BLANC, 4), oui), (int(xt + t_.width + 6), 176))
        s._cache[cle] = im
        return im

    def _scene_supprime(s, im, u):
        K = s.K
        v = u - s.t["supprime"]
        e = smooth((v - 0.05) / 0.5)
        if e <= 0.01:
            return
        ecran = s._ecran_accueil().copy()
        # l'icône « HOROSCOPE » glisse vers la corbeille en rapetissant, puis disparaît en fondu
        ih = s._icone_horo()
        g = smooth((v - s.T_JETTE) / 0.6)
        x_i, y_i = 216 + 0 * g, 270 + (560 - 270) * g
        ki = 1 - 0.6 * g
        ai = 1 - smooth((v - s.T_JETTE - 0.4) / 0.4)
        ouv = smooth((v - s.T_JETTE) / 0.3) * (1 - smooth((v - s.T_JETTE - 0.8) / 0.3))
        cb = s._corbeille(ouv)
        ac = smooth((v - 0.6) / 0.3)
        ecran.alpha_composite(_fade(cb, ac), (int(216 - cb.width / 2), int(600 - cb.height / 2)))
        if ai > 0.01:
            ih_ = s._zoomk(ih, ki, "ihoro") if ki < 0.999 else ih
            ecran.alpha_composite(_fade(ih_, ai), (int(x_i - ih_.width / 2), int(y_i - ih_.height / 2)))
        ed = smooth((v - s.T_DIALOGUE) / 0.25) * (1 - smooth((v - s.T_JETTE) / 0.25))
        if ed > 0.01:
            voile = Image.new("RGBA", ecran.size, (6, 6, 16, int(120 * ed)))
            ecran.alpha_composite(voile)
            dl = s._dialogue(smooth((v - s.T_OUI) / 0.2))
            ecran.alpha_composite(_fade(dl, ed), (int(216 - dl.width / 2), int(300 - dl.height / 2)))
        tel, (lx, ly) = s._couche_tel(ecran)
        z = 0.74
        tel = tel.resize((int(tel.width * z), int(tel.height * z)), Image.BILINEAR)
        X1, Y1 = s.PW_ * K, s.PH_ * K
        x = X1 - (X1 - lx) * z - 60
        y = Y1 - (Y1 - ly) * z + 300 * (1 - e)
        im.alpha_composite(_fade(tel, min(1.0, 1.6 * e)), (int(x), int(y)))
        er = smooth((v - 0.25) / 0.4)                                               # « REPENS-TOI : … » (Coran 42:25)
        tr = s.t.get("repens")                                                      # avant « ABONNE-TOI » : tout s'efface
        out = 1.0 if tr is None else 1 - smooth((u - tr - s.T_REPENS_OUT) / 0.35)
        if out <= 0.01:
            return
        rp = s._lab("REPENS-TOI :", (110, 230, 130), 52)
        s._pose(im, rp, 450, 74 + 12 * (1 - er), er * out, maxw=800)
        cit = s._c("repentir", lambda: _lignes(list(REPENTIR), VERT_C, 34, serre=24))
        s._pose(im, cit, 450, 168 + 12 * (1 - er), smooth((v - 0.35) / 0.4) * out, maxw=860)

    def _image_quarante(s, u):
        ta = s.t.get("avenir")
        if ta is None:
            return s._cadre(s._scene_nuits(u))
        im = s._ciel(1).copy()                                                      # le nouveau ciel, dessous
        s._scintille(im, u, 1)
        a1 = 0.0 if ta <= 0.05 else 1 - smooth((u - ta) / 0.5)                     # tout le ciel des nuits part ensemble
        if a1 > 0.01:
            im.alpha_composite(_fade(s._scene_nuits(u), a1))
        if u >= ta:
            s._scene_avenir(im, u)
        if "supprime" in s.t and u >= s.t["supprime"]:
            s._scene_supprime(im, u)
        return s._cadre(im)


# ---------------------------------------------------------------- branchement (via explique_0811.py)
CLES = ["astro", "quarante"]


def _norm(m):
    return m.lower().replace("é", "e").replace("è", "e").replace("ê", "e")


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique_0811.ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    qui = mots[1].upper() if len(mots) > 1 else "PETIT"

    def dernier(cls, mode=None):
        return next((it["el"] for it in reversed(schema._visibles(t + 0.01))
                     if isinstance(it["el"], cls) and (mode is None or getattr(it["el"], "mode", None) == mode)), None)

    def u_de(el):
        return t - next(it["t_in"] for it in schema.items if it["el"] is el)

    if k == "astro":
        schema._ajoute(t, Horoscope(brut, "astro", qui if qui in ("PETIT", "GRAND") else "PETIT"))
    elif k == "quarante":
        if sous in Horoscope.ETAPES:
            el = dernier(Horoscope, "quarante")
            if el is None:
                el = Horoscope(brut, "quarante")
                schema._ajoute(t, el)
            el.t[sous] = u_de(el)
        else:
            schema._ajoute(t, Horoscope(brut, "quarante"))
    else:
        return False
    return True


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    k = _norm(mots[0])
    sous = _norm(mots[1]) if len(mots) > 1 else ""
    if k == "astro":
        return t + 2.0
    if k == "quarante":
        return t + dict(lunes=3.3, arrete=1.0, prie=1.6, avenir=2.2, supprime=2.1, repens=1.0).get(sous, 0.9)
    return None
