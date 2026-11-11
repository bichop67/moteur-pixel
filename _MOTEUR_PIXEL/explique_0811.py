# DÉMONSTRATIONS EN IMAGE DU 08/11/2026 — 9 Shorts duo au format « consigne + avertissement » (un ordre dès le début,
# puis ce qui arrive, selon un texte authentique, à celui qui ne le fait pas) :
#   explique_0811_talons.py      {talon PETIT} (accroche) · {talons …}       (ISL23, laver ses talons aux ablutions)
#   explique_0811_urine.py       {gouttes PETIT} (accroche) · {tombes …}     (ISL24, se protéger de l'urine)
#   explique_0811_droite.py      {repas PETIT} (accroche) · {maindroite …}   (ISL25, manger de la main droite)
#   explique_0811_imam.py        {imam} (accroche) · {ane …}                 (ISL26, ne pas devancer l'imam)
#   explique_0811_asr.py         {soleilbas} (accroche) · {asr …}            (ISL27, ne pas rater l'Asr)
#   explique_0811_medisance.py   {ghiba} (accroche) · {chair …}              (ISL28, la médisance)
#   explique_0811_ecoute.py      {oreille PETIT} (accroche) · {plomb …}      (ISL29, écouter en cachette)
#   explique_0811_horoscope.py   {astro} (accroche) · {quarante …}           (ISL30, devins et horoscope)
#   explique_0811_coucher.py     {coucher} (accroche) · {crepuscule …}       (ISL31, rentrer au coucher du soleil)
# Chaque module est chargé seulement quand une de ses clés sert (import tardif) : un module en travaux ne gêne pas les
# autres. Branché comme explique_0611 dans explique.Schema._ordre et scenario._fin_anim. Mêmes règles : mouvements
# doux, aucun prophète, ange, Compagnon ni Chaytan dessiné (seulement du texte, des lumières ou une ombre neutre),
# Allah jamais représenté, rien de gore.
import importlib

MODS = {
    "explique_0811_talons": ("talon", "talons"),
    "explique_0811_urine": ("gouttes", "tombes"),
    "explique_0811_droite": ("repas", "maindroite"),
    "explique_0811_imam": ("imam", "ane", "âne"),
    "explique_0811_asr": ("soleilbas", "asr"),
    "explique_0811_medisance": ("ghiba", "chair"),
    "explique_0811_ecoute": ("oreille", "plomb"),
    "explique_0811_horoscope": ("astro", "quarante"),
    "explique_0811_coucher": ("coucher", "crepuscule", "crépuscule"),
}
CLES = tuple(k for ks in MODS.values() for k in ks)
_charges = {}


def _module(cle):
    cle = cle.lower()
    for nom, ks in MODS.items():
        if cle in ks:
            if nom not in _charges:
                _charges[nom] = importlib.import_module(nom)
            return _charges[nom]
    return None


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique.Schema._ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
    m = _module(mots[0])
    return bool(m and m.ordre(schema, t, brut, mots, reste))


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    m = _module(mots[0])
    return m.fin_anim(t, mots) if m else None
