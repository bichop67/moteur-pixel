# Catalogue : comment MONTRER (du moins cher au plus cher)

Ordre de choix pour chaque passage d'un Short :
1. une **brique** (partie A) : une ligne de scénario, aucun code ;
2. un **outil de base** (partie B) ;
3. une **animation déjà faite** pour un ancien sujet, si le nouveau sujet s'y prête vraiment (partie C) ;
4. une animation NEUVE : seulement pour l'accroche (les 3 à 5 premières secondes), avec l'accord de l'utilisateur et le
   coût annoncé avant (≈ 50 Ko de code + mises au point). Jamais pour le milieu de la vidéo.

À chaque passage un procédé DIFFÉRENT du précédent. Les balises s'écrivent dans la réplique, à l'endroit du mot où
l'élément doit apparaître. Mouvements doux et fondus seulement : jamais de secousse, de flash ni de coupe sèche.

## A. Les 8 briques (briques.py, 09/11/2026 ; démo : `scenarios\demo_9_briques.txt`)

La 1re balise CRÉE la brique avec son contenu, les suivantes la font évoluer sur un mot. Après un retour à la scène,
la brique reprend où elle en était. Textes entre guillemets (majuscules automatiques, « // » = 2e ligne plus petite).

| Besoin | Brique | Balises |
|---|---|---|
| Ce qui est permis / interdit, une liste qui se barre | **liste** (tableau noir ; `nuit` = fond sombre) | `{liste titre "TU JURES SUR…" "TON PÈRE" "TA MÈRE" "ALLAH"}` · `{liste barre 1 2}` `{liste coche 3}` `{liste or 3}` `{liste efface 1}` `{liste + "TA VIE"}` `{liste note "… OU TU TE TAIS"}` |
| Une parole citée (hadith, verset) | **citation** (cadre doré, coupée seule) | `{citation "LE PROPHÈTE ﷺ A DIT :" "« … »"}` · `{citation + "« … »"}` `{citation note "= …"}` + `{source "MOUSLIM 243"}` |
| Quelque chose qui monte ou descend (colère, foi, fièvre) | **jauge** | `{jauge "COLÈRE" 100 -> 35 PETIT %}` · `{jauge -> 0}` `{jauge fin "CALME"}` ; options `inverse` (haut = bien), `max 40` |
| Un objet ou un visage en gros plan, un endroit précis | **focus** (74 icônes, dessins de `OBJETS`, ou un perso) | `{focus telephone "TON ÉCRAN"}` · `{focus PETIT triste "TOI"}` · `{focus entoure haut "FENDU"}` (haut, bas, gauche, droite, centre ou `30 70`) `{focus ok "…"}` `{focus non "…"}` `{focus texte "…"}` |
| Le mauvais geste contre le bon | **versus** | `{versus titre "TU MANGES AVEC…" pouce_bas "LA MAIN GAUCHE" pouce "LA MAIN DROITE"}` · `{versus non}` `{versus oui}` |
| Des formules qui se répondent | **bulles** | `{bulles PETIT "AL-HAMDOU LILLAH"}` `{bulles GRAND content "YARHAMOUKA ALLAH"}` ; options `or`, `vide`, `rouge`, `nouveau` |
| Un voyage, une journée, une vie (frise) | **trajet** | `{trajet titre "LE VOYAGE" "SA VILLE" -> "LE BON PAYS" PETIT}` · `{trajet avance 45}` `{trajet etape 45 "MI-CHEMIN"}` `{trajet stop "…"}` `{trajet arrive}` |
| Compter pour de vrai (40 jours, 5 prières, 3 fois) | **grille** | `{grille 40 "JOURS" "TA PRIÈRE"}` · `{grille barre 40}` `{grille coche 12}` `{grille vide}` |
| Un avertissement / un pardon, sur n'importe quelle brique | **lueur** | `{citation lueur rouge}` (monte du bas) · `{focus lueur or}` (descend du haut) · `vert`, `bleu`, `fin` |

Icônes pour focus / versus / trajet : `python -c "import objets; print(sorted(objets.ICONES))"` (telephone, livre, lune,
soleil, maison, coeur, feu, horloge, argent, bouclier, pouce, pouce_bas, interdit, check, croix…). Un objet qui manque =
une petite fonction `@objet("nom")` dans `briques.py` (30 à 80 lignes) : c'est le SEUL code qu'un sujet peut demander.
Objets maison déjà faits : `goutte`, `chien` (09/11/2026 : `{focus chien "OUAF ! OUAF !"}`), `mouche` (10/11/2026 :
`{versus titre "LE DIABLE DEVIENT…" maison "COMME UNE MAISON" mouche "COMME UNE MOUCHE"}` ; dans versus, « // » ne coupe
pas les étiquettes : textes courts).
Détail de chaque option : en-tête de `briques.py`.

Anciennes animations refaites en brique : serments → liste ; colère → jauge ; éternuement → bulles ; route du
repentant → trajet ; talon sec, écran cassé → focus ; main droite, maison avec / sans Bismillah → versus ; 40 nuits,
360 articulations → grille ; invocation ligne par ligne, verset → citation.

## B. Outils de base

| Besoin | Outil | Exemple |
|---|---|---|
| Accroche vue à la place du spectateur | vue subjective | `{pov …}` et décors `tapis_pov`, `porte_pov`… (LISEZMOI partie 23) |
| Accroche : le perso se voit | selfie raté en encart | `ADA (degoute) : {selfie ADA} Pourquoi je suis moche en photo ?!` |
| Une action, une mesure | démonstration jouée | `{photographe ETUDIANT ADA 30 cm}` … `{recule 1,5 m}` |
| Le perso face à lui-même | miroir | `{reflet ADA content}` |
| Comparer deux images | schéma | `{miroir ADA grain}` `{photo ADA grain}` `{double-fleche INVERSÉ}` |
| Une idée abstraite | icônes + chiffre | `{icone cerveau}` `{chiffre +30 %}` |
| Désigner quelqu'un dans la scène | étiquette, projecteur, loupe, règle | `{etiquette ADO "TES POTES"}` `{projecteur ADA}` `{loupe ADA}` `{mesure ADA PAPA}` |
| Idée fausse / juste sur un perso | étiquette barrée / cochée | `{etiquette ADO "…" rouge}` `{barre ADO}` · `{coche ADA}` |
| Illustrer ailleurs pendant qu'il parle | nouveau décor + voix off | `== couloir_ecole` puis `ETUDIANT (voix off) : …` |
| Relancer au milieu | bandeau-titre (JAMAIS de numéro) | `{etape "TON TÉLÉPHONE"}` |
| Une preuve | source à l'écran (toute la réplique) | `{source "BOUKHARI 652"}` |
| Une citation sur la scène | bandeau sombre en haut | `{texte "« … » // explication"}` |
| Pensées qui envahissent | nuages de pensées | `{pensees PETIT}` … `{repousse PETIT}` |
| Un geste à imiter, dégager le passage | objet à pousser | option `objet trottinette (620)` + `{pousse PETIT trottinette mur}` `{va MAMIE 560 devant}` |
| Compter, durer | compteur, chrono | `{compteur 0 -> 100 "…"}` `{chrono 2:00 "≈ 2 MINUTES"}` |
| Lettres arabes une par une | lettres | `{lettres ا ل م}` |
| Prophète / Compagnons (jamais dessinés) | orbes de lumière | option `orbes "DES COMPAGNONS" 3 (355, 1010) pensees`, `orbe "LE PROPHÈTE" (805, 930) dore grand` |
| Pardon, bénédiction sur un perso | lumière douce | `{lumiere VOYAGEUR}` |
| Un geste pile sur un mot | geste | `{geste PETIT invoque}` |
| Scroller | téléphone qui défile | `{defile}` |

## C. Animations déjà faites pour un sujet (à reprendre telles quelles si le sujet revient)

Syntaxe et étapes de chacune : chercher sa clé dans `references/balises.md` ou dans `LISEZMOI_MOTEUR.txt`.

| Sujet | Balises | Date |
|---|---|---|
| Petits péchés lavés un par un | `{ecume "TES PÉCHÉS" sale}` `{vague}` `{propre "…"}` `{rocher "…"}` · `{peches PETIT}` | 01/11 |
| « Chaque lettre lue » | `{coran}` … `{chiffre ×10}` | 01/11 |
| 360 aumônes, douleur qui efface, balance | `{radio …}` · `{orteil}` `{arbre "…"}` `{feuilles}` · `{balance "A" "B"}` | 03/11 |
| Fièvre, eau glacée, ablutions, cauchemar | `{fievre PETIT}` `{forge "…"}` `{soufflet}` · `{glace}` `{ablutions …}` · `{cauchemar PETIT}` `{gestes …}` | 04/11 |
| 100 meurtres, Coran difficile, téléphone cassé, tombe, soleil, Enfer | `{cent}` `{chemin …}` · `{bute}` `{double …}` · `{ecran}` `{dua …}` · `{tombeau …}` · `{chaleur}` `{soleil …}` · `{brulure}` `{braises …}` `{datte …}` | 04/11 soir |
| Jurer, éternuer, colère, rentrer chez soi, dette, coucher | `{jure}` `{serment …}` · `{atchoum}` `{chaine …}` `{rhume …}` · `{enerve}` `{colere …}` · `{porte}` `{maison …}` · `{sms}` `{dette …}` `{carnet}` · `{lit}` `{sommeil …}` | 07/11 |
| Talons, urine, main droite, imam, Asr, médisance, écouter aux portes, horoscope, coucher du soleil | `{talon}` `{talons …}` · `{gouttes}` `{tombes …}` · `{repas}` `{maindroite …}` · `{imam}` `{ane …}` · `{soleilbas}` `{asr …}` · `{ghiba}` `{chair …}` · `{oreille}` `{plomb …}` · `{astro}` `{quarante …}` · `{coucher}` `{crepuscule …}` | 08/11 |

## D. Mise en scène

- Le moteur choisit seul les plans entre les balises (plan large, glissement vers celui qui parle, rapprochement,
  champ / contre-champ, réactions). Une longue explication en plan large paraît figée : mettre `plan moyen`, alterner
  scène et schéma (`nouveau schéma`), et prévoir un élément juste avant ou après chaque ﷺ (≈ 2,5 s à l'oral).
- Proportions : une porte ≈ 1,2 fois un perso. Rue : `rue_proche` (`_soir`, `_nuit`), jamais `rue`.
- Hadith / verset : l'image montre le sens propre du texte (concret), jamais des icônes abstraites.
- Jamais de prophète, d'ange, de Compagnon ni de figure vénérée dessinés (orbe de lumière avec un nom si besoin).
- Zones sûres TikTok : rien d'important en haut (≈ 200 px), en bas (20 %) ni à droite (≈ 150 px, sous 840 px de haut).
