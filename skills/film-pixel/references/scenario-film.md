# Du script au film pixel 16:9 (moteur _MOTEUR_PIXEL)

État au 02/11/2026 : tout ce qui servait au film « Moussa » (épisode 14, 24 parties) est construit et documenté
dans `_MOTEUR_PIXEL\LISEZMOI_MOTEUR.txt`, parties 21 (FILMS) et 22 (décors, objets, animaux, persos, annotations,
options de bloc, outils). Ce qui suit résume l'essentiel ; en cas de doute, le LISEZMOI fait foi.

## 1. Organisation des fichiers

- Un scénario par partie du film : `_MOTEUR_PIXEL\scenarios\film\ep14\p01_<nom>.txt`, `p02_…` (3 à 4 min chacun).
  Une partie se corrige, se revoit et se rend seule ; l'assemblage colle les parties.
- En-têtes de chaque partie :
  ```
  TITRE: Moussa 1 - p01 ouverture
  CODE: E14P1                      préfixe des voix : E14P1_NARRATEUR.mp3, E14P1_CORAN.mp3, E14P1_PHARAON.mp3…
  THEME: film                      pas de bandeau, pas de fin « abonne-toi », référence en haut à droite
  FORMAT: horizontal
  MUSIQUE: fond_mystere
  VOIX: C:\Users\abdellah\Desktop\VIDEO YOUTUBE\FILM\EPISODE 14\voix\p01
  ```
- Les répliques ont EXACTEMENT le texte du fichier ElevenLabs (sous-titres et calage en dépendent).

## 2. Qui parle

```
NARRATEUR (voix off) : [dark] Une mère jette son bébé dans le fleuve. {source "CORAN 28:7"}
CORAN (voix off) : Et Nous révélâmes à la mère de Moussa : … {source "CORAN 28:7"}
PHARAON (arrogant) : …          un perso dessiné qui parle (bouche, regards, champ / contre-champ automatiques)
```
NARRATEUR et CORAN sont des voix sans corps (sous-titres sans vignette, la voix du Coran en or pâle).
Les balises v4 ([dark], [pause]…) restent dans le texte pour ElevenLabs et ne s'affichent pas.

## 3. Montrer ce que dit la voix

- Le décor s'ouvre avec ses persos placés (`PHARAON place 960`, `COFFRE place 330 1150, ouvert`), puis les actions
  s'écrivent au mot près dans la réplique : `{va X 700 [6s]}`, `{derive X x y Ns}` (glisse), `{court X x}`,
  `{apparait X [Ns]}`, `{disparait X [Ns]}`, `{geste X pose}`, `{regarde X droite}`, `{devient decor N}` (un seul par
  plan), `{cadre X}` `{gros X}` `{large}` (cadrages doux), `{souvenir X decor dx dy Ns}` (vignette d'un lieu),
  `{tableau nom Ns}` (tableau net à l'écran pour une explication), `{noir 3s}` (rien n'est montré, l'image revient).
- Orbes (prophètes, figures vénérées, anges) : jouent comme des persos (place, derive, apparait, poses pale / intense) ;
  jamais dessinés. Chute en douceur : `{geste X allonge}` (0,7 s), relevé : `{geste X debout}`.
- Le décor vit : options de bloc (`emotion`, `oiseaux`, `etoiles`, `armee`, `mur`, `demeure`, `lueur`, `echelle`,
  `cendres`, `noir t d`…) et effets sur un mot (`{sources}`, `{manne}`, `{nuage}`, `{cailles}`, `{poisson}`,
  `{mur redresse}`, `{engloutit}`, `{foudre}`, `{vagues}`, `{serpent}`, `{fleau}`…).
- Rythme : quelque chose bouge au moins toutes les 4 s ; pour une longue réplique (verset), changer de cadrage
  ({cadre}/{large}/{gros}) toutes les 4 à 6 s et ajouter des souvenirs. `controle_video.py` signale les passages
  figés mais ne voit pas les glissés de caméra : regarder la planche.
- Objets posés / portés : garder la pose « porte » et glisser y de 88 pour poser ou reprendre en douceur (pas de saut).
- Sous-titres : ils cachent environ 35 px du bas ; poser les objets vers y 1284-1290 et les corps étendus vers y 1282.

## 4. Décors, persos et objets de l'époque

Décors : `egypte.py`, `decors_film.py` à `decors_film5.py`, `decors_madyan.py` (liste dans le LISEZMOI, partie 22).
Nouveau décor : une fonction qui renvoie (toile, premier plan) + `egypte.enregistre(...)` avec `sol_haut` ; ajouter le
fichier à l'empreinte du cache (`egypte._empreinte`). Toujours vérifier : pas de zone noire (ciel jusqu'au sol), pas de
bande parasite, proportions (une porte ≈ 1,2 fois un perso).
Persos de l'époque : `troupe_egypte.py` (nouveau(...) ; enfants : taille="enfant"). Objets : `film.py` (OBJETS_FILM).
Animaux : `animaux.py` (ANIMAUX). Un nom = un seul rôle par bloc (CLES, CLES2, CLES3 pour trois trousseaux).

## 5. Commandes

```
python scenario.py scenarios\film\ep14\p01_ouverture.txt sheet     planche (maquette tant qu'il n'y a pas de voix)
python scenario.py … voix                                           textes à générer (une génération par voix)
python scenario.py … asr                                            calage sur les vraies voix
python scenario.py … tout                                           rendu de la partie (arrière-plan)
python controle_video.py "<partie>.mp4" --leger                     contrôle
python assemble_film.py "<film>.mp4" p01.mp4 … p24.mp4 [--leger]   assemble : fondus au noir de 1 s, −14 LUFS,
                                        fondu final ; chapitres = début de chaque partie (durées − 1 s par fondu)
```

## 6. Shorts tirés du film

Copier la scène choisie dans un scénario `FORMAT: vertical` avec `ACCROCHE:` et `FIN` (`DUREE_FIN: 2.0`), réutiliser les
voix déjà enregistrées (recollage comme pour les Shorts islam du 01/11/2026 : `pxv.split` + `pxv.resserre`), 30 s
maximum, zones sûres TikTok.
