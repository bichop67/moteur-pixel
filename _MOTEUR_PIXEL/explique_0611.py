# DÉMONSTRATIONS EN IMAGE DU 07/11/2026 — 6 Shorts duo au format « consigne » (un ordre dès le début) :
#   explique_0611_serment.py  {jure PETIT} (accroche) · {serment pere|mere|allah|frere|tais|vrai}      (ISL17, jurer)
#   explique_0611_eternue.py  {atchoum PETIT} · {chaine aime|hamd|reponse|retour|rien} · {rhume …}    (ISL18, éternuement)
#   explique_0611_colere.py   {enerve PETIT} · {colere refuge|fort|gg}                                 (ISL19, colère)
#   explique_0611_maison.py   {porte} · {maison entre|mange|pas|libre}                                 (ISL20, Bismillah)
#   explique_0611_dette.py    {sms} · {dette efface|reste|injustice} · {carnet}                        (ISL21, dette)
#   explique_0611_sommeil.py  {lit PETIT} · {sommeil verset|nuit|reveil}                               (ISL22, coucher)
# Chaque élément vit dans son module ; ce fichier les réunit pour explique.Schema._ordre (import tardif) et
# scenario._fin_anim, comme explique_0411b. Mêmes règles : mouvements doux, aucun prophète, ange, Compagnon ni Chaytan
# dessiné (seulement du texte ou des lumières neutres), Allah jamais représenté, rien de gore.
import explique_0611_serment as _serment
import explique_0611_eternue as _eternue
import explique_0611_colere as _colere
import explique_0611_maison as _maison
import explique_0611_dette as _dette
import explique_0611_sommeil as _sommeil

MODULES = (_serment, _eternue, _colere, _maison, _dette, _sommeil)
CLES = tuple(k for m in MODULES for k in m.CLES)


def _module(cle):
    cle = cle.lower()
    for m in MODULES:
        if cle in m.CLES:
            return m
    return None


def ordre(schema, t, brut, mots, reste):
    """Appelé par explique.Schema._ordre pour les clés de CLES. Renvoie True si l'ordre a été pris en compte."""
    m = _module(mots[0])
    return bool(m and m.ordre(schema, t, brut, mots, reste))


def fin_anim(t, mots):
    """Fin de l'animation d'un ordre (pour que le plan de schéma dure assez) ; None = rien à attendre."""
    m = _module(mots[0])
    return m.fin_anim(t, mots) if m else None
