# Écrire un scénario (scenario.py) — référence complète

Un fichier texte UTF-8 dans `_MOTEUR_PIXEL\scenarios\`. Une ligne = une chose. `#` = commentaire.
Modèle complet et commenté : `scenarios\moche_en_photo.txt`. Autres exemples : `le_passeport_de_papi.txt`
(sketch simple), `demo_dialogue_vivant.txt` (champ / contre-champ, réactions).

## Sommaire
1. En-têtes
2. Décors et options
3. Répliques, actions, didascalies
4. Lignes spéciales (SMS, notification, carton, légende, fin)
5. Balises {…} : schémas, démonstrations, annotations, relances
6. Sous-titres : mots importants
7. Commandes

## 1. En-têtes (au début du fichier)
```
TITRE: Pourquoi on est moche en photo        nom du fichier vidéo (sans apostrophe de préférence)
THEME: sketch                                sketch, valable, neutre, info, histoire, mystere, science, argent, podcast
FORMAT: vertical                             vertical (Short 1080x1920) ou horizontal (16:9 1920x1080)
MUSIQUE: fond_espoir                         fond_espoir, fond_mystere, fond_tension, fond_tristesse, fond_epique,
                                             fond_desert, fond_tempete (dossier _MUSIQUES\FOND) ou « aucune »
PERSONNAGES: ADA, ETUDIANT                   le 1er à gauche, le 2e à droite, le 3e rejoint le 2e
ACCROCHE: BELLE AU MIROIR… / MOCHE EN PHOTO ?!   texte d'accroche visible dès la 1re image (2,6 s)
MINIATURE: BELLE AU MIROIR / MOCHE EN PHOTO ?!   texte de la miniature (sinon le TITRE)
ICONE: question                              icône de la miniature
VOIX: chemin\vers\les\mp3                    (sinon voix_<code> à côté du scénario)
CODE: MOCHE                                  préfixe des fichiers voix (CODE_PERSO.mp3)
DEMO: oui                                    affiche le code de chaque élément (mise au point) ; enlever pour la vraie vidéo
DUREE_FIN: 2.0                               durée du plan « abonne-toi » (2 s par défaut : fin courte)
```

## 2. Décors et options
`== nom_du_decor, options…` ouvre un décor. Liste des décors : `python -c "import sets; print(sorted(sets.DECORS))"`
(71 : salon, cuisine(_soir/_nuit), rue(_soir/_nuit), parc, chambre_ado, classe, couloir_ecole, bureau, snack, metro,
supermarche, hopital, cafe, studio, plateau_tv, voiture, aeroport, avion, stade, marche, prison(_barreaux), desert,
palais, bibliotheque, village, temple, plage, toit, foret, espace, tribunal, tableaux, mosquee, ablutions…).
**Rue : utiliser `rue_proche` (`_soir`, `_nuit`)** : la rue à l'échelle des persos (portes un peu plus hautes qu'eux,
vitrine, grande enseigne ; demandé le 01/11/2026 : dans `rue`, les persos étaient « disproportionnés », trois étages de
haut). `rue` reste pour les anciennes vidéos.
Options : `pluie`, `neige`, `feuilles`, `lucioles`, `voitures`, `passants`, `foule`, `oiseaux`, `feu`,
`1.5s` (plan muet au début), `ensemble (540, 700)` (la caméra s'approche d'un point), `texte "23 H 47"`,
`serre` (plan à deux serré, pas de champ / contre-champ).

## 3. Répliques, actions, didascalies
```
ADA (choc, bulle !) : Comment ça ?!        réplique ; entre parenthèses ce qu'il fait EN la disant
ADA entre à gauche, téléphone              action (au moment où elle est écrite)
ETUDIANT (voix off) : Imagine…             il parle sans être dans le décor (scène d'illustration ailleurs)
```
Visages : content, rit, choc, gêné, malin, blasé, énervé, crie, triste, pleure, peur, suspect, dégoûté, clin d'oeil,
amoureux, émerveillé, dort, fier, calme, honteux.
Gestes (reviennent au repos tout seuls après la réplique) : explique, pointe, index, question, panique, salue, pouce,
facepalm, réfléchit, hausse les épaules, victoire, stop, présente, invoque. Poses tenues : bras croisés, mains sur les
hanches, au téléphone, tape, boit, prie.
Effets : coeurs, colère, idée, zzz, larmes, goutte, étoiles, notes, points, brille.
Objets : téléphone, livre, coran (vert et or), tasse, passeport, valise, sac_courses, micro… ; « tient le coran »,
« donne le passeport à ADA », « range ». Poses photo et selfie : pose="photo", pose="selfie".
Mouvements : entre (à gauche / à droite / par la porte), sort, s'approche, se retourne, apparaît, assis, se lève,
sautille, traverse (passe d'un bord à l'autre, devant les autres, quand ils ont fini de bouger), place 380 (position x
au début du décor).
Bulles / pensées : `bulle !`, `bulle ?`, `bulle …`, `pense à batterie` (n'importe quelle icône).
Plans : `gros plan`, `plan moyen`, `plan large`, `épaule` (champ / contre-champ forcé), `schéma` (la réplique reste
sur le schéma en cours, ex. la réaction pendant que les cercles montrent le détail), `nouveau schéma` (ce schéma ne
prolonge pas celui de la réplique d'avant : on revoit la scène entre les deux). `plan moyen` sur une longue
explication = la caméra se rapproche doucement de celui qui parle (sinon le plan large paraît figé).
Récit en voix off : `{va VOYAGEUR 470}` (il marche jusqu'à x = 470), `{regarde VOYAGEUR bas}` (il baisse les yeux),
placés sur le mot où ça doit arriver.

## 4. Lignes spéciales
```
SMS MAMAN : T'es où ? / > J'arrive          écran de téléphone (« > » = message envoyé)
NOTIF MAMAN : Tu rentres quand ?            notification pendant la réplique suivante
CARTON : LE LENDEMAIN / 8 H 00              carton de temps
LEGENDE : TITRE / texte                     légende de démonstration (le dernier « / » sépare)
FIN                                         tous rient + « ABONNE-TOI POUR LA SUITE » (2,6 s)
```

## 5. Balises {…} dans une réplique (apparaissent pile sur ce mot, ni dites ni sous-titrées)
Plusieurs répliques qui se suivent avec le même genre de balises = un seul plan (le genre change : nouveau plan).

**BRIQUES RÉUTILISABLES (09/11/2026, `briques.py`) — à choisir en premier : aucun code par sujet.** La 1re balise crée
la brique, les suivantes la font évoluer sur un mot ; après un retour à la scène elle reprend où elle en était.
Textes entre guillemets (majuscules automatiques ; « // » = 2e ligne plus petite ; ﷺ écrit en toutes lettres).
- `{liste "A" "B" "C"}` (tableau noir ; `nuit` = fond sombre ; `titre "…"` = le 1er texte est le titre) ·
  `{liste + "D"}` `{liste barre 1 2}` `{liste coche 3}` `{liste or 3}` `{liste efface 1}` `{liste note "…"}`
  (sans numéro = la dernière ligne ; `tout` = toutes).
- `{citation "QUI PARLE :" "« … »"}` (cadre doré, coupée en lignes toute seule) · `{citation + "« … »"}`
  `{citation note "= …"}` ; la source reste `{source "…"}`.
- `{jauge "COLÈRE" 100 -> 35 PETIT %}` (le visage du perso suit le niveau ; `%` affiche la valeur ; `inverse` : haut =
  bien ; `max 40`) · `{jauge -> 0}` `{jauge fin "CALME"}` (`rouge` pour un mauvais résultat).
- `{focus telephone "TON ÉCRAN"}` (une des 74 icônes, un dessin de `OBJETS`, ou un perso : `{focus PETIT triste "TOI"}`)
  · `{focus entoure haut "FENDU"}` (haut, bas, gauche, droite, centre, ou `30 70` en % de l'objet) `{focus ok "…"}`
  `{focus non "…"}` `{focus texte "…"}`.
- `{versus pouce_bas "MAIN GAUCHE" pouce "MAIN DROITE"}` (objet facultatif devant chaque texte ; `titre "…"`) ·
  `{versus non}` `{versus oui}` (+ `gauche` / `droite` pour viser l'autre carte).
- `{bulles PETIT "AL-HAMDOU LILLAH"}` `{bulles GRAND content "YARHAMOUKA ALLAH"}` (chaque balise ajoute une bulle ;
  options `or`, `rouge`, `vide`, un visage ; `nouveau` repart de zéro).
- `{trajet "SA VILLE" -> "LE BON PAYS" PETIT}` (sans perso : un point de lumière ; `titre "…"` ; une icône devant un
  texte change le dessin du bout) · `{trajet avance 45}` `{trajet etape 45 "MI-CHEMIN"}` `{trajet stop "…"}`
  `{trajet arrive}`.
- `{grille 40 "JOURS" "TITRE"}` · `{grille barre 40}` `{grille coche 12}` `{grille vide}` (le compte s'affiche dessous).
- Sur toutes : `{<brique> lueur rouge}` (avertissement, monte du bas), `lueur or` (lumière, descend du haut),
  `lueur vert`, `lueur bleu`, `lueur fin`.
Démo : `scenarios\demo_9_briques.txt`. Un objet qui manque : `@objet("nom")` dans `briques.py`.

**Schéma animé** (la vidéo quitte la scène, décor flou ; 1 élément au centre, 2 côte à côte, 3 en ligne) :
`{perso ADA}` `{perso ADA choc}` · `{miroir ADA}` `{photo ADA}` (+ `grain` : grain de beauté, entouré en rouge par une
double flèche) · `{compare ADA}` · `{icone cerveau}` (74 icônes) · `{chiffre +30 %}` (monte jusqu'à la valeur) ·
`{texte "CE QUE LES AUTRES VOIENT"}` · `{fleche}` `{fleche POURQUOI ?}` `{double-fleche INVERSÉ}` ·
`{distance ADA 1,5 m -> 30 cm}` (version schéma) · `{check}` `{croix}` · `{source "MITA ET AL., 1977"}` ·
`{efface}` (on recommence) · `{fond tableau}`.

**Démonstration jouée** : `{photographe ETUDIANT ADA 30 cm}` (il tient le téléphone devant son visage et prend la
photo : règle au sol, pointillés, écran du téléphone en encart en direct, clic) puis `{recule 1,5 m}` / `{avance 30 cm}`
(il marche sans se retourner, la caméra suit, les deux photos finissent côte à côte) ; `{chiffre +30 %}` s'accroche au
nez de l'encart tant que c'est près, `{check}` sur l'encart quand c'est loin.

**Selfie** : `{selfie ADA}` (bras tendu, l'encart montre le selfie avec son expression, déformé de près).

**Miroir** : `{reflet ADA}` / `{reflet ADA content}` (de dos au premier plan, reflet inversé qui parle et cligne ;
étincelles si content / fier / coeur) ; + `{texte "…"}`, `{source "…"}`.

**Annotations sur la scène** (suivent les persos, la réplique reste en plan large) : `{etiquette ADO "TES POTES"}`,
`{mesure ADA PAPA}`, `{projecteur ADA}`, `{loupe ADA}`.

**Relance** : `{etape "LE MIROIR"}` (bandeau-titre en haut, 2,4 s, whoosh doux). **JAMAIS de numéro** (« 1/2 »,
« PARTIE 2/2 ») : l'utilisateur la refuse (01/11/2026) ; le moteur n'affiche plus que le titre entre guillemets.

**Citation sur la scène** : une réplique qui n'a que `{texte "…"}` et `{source "…"}` les affiche SUR la scène (les persos
restent à l'image) : bandeau sombre doux en haut. `{texte "« CITATION » // explication"}` : l'explication s'ajoute
dessous en jaune (sans voix). Pour forcer un schéma à la place : didascalie « schéma ».

**Pensées noires** : `{pensees PETIT}` (nuages sombres « ? ! » autour de sa tête) puis `{repousse PETIT}` (il fait « stop »,
ils s'envolent).
**Étiquettes barrée / cochée** : `{etiquette ADO "ALLAH M'A OUBLIÉ" rouge}` puis `{barre ADO}` (barrée en rouge au mot) ;
`{etiquette ADA "ALLAH SAIT MIEUX" vert}` + `{coche ADA}` (✓ vert). Couleurs : rouge, vert, bleu, blanc, jaune, orange.
Texte long : deux lignes automatiquement ; jamais coupée par le bord.
**Objets posés par terre** : option de décor `objet trottinette (620)` (aussi : branche, caillou, carton) puis
`{pousse PETIT trottinette}` (il va le pousser hors du chemin et revient ; `continue` = il poursuit sa route et sort ;
`reste`).
**Compteur / chrono / lettres** (schéma) : `{compteur 0 -> 100 "SUBHAN ALLAH WA BIHAMDIH"}`, `{chrono 2:00 "≈ 2 MINUTES"}`
(défile en 1,5 s), `{lettres ا ل م}` (lettres arabes une par une, de droite à gauche, « +10 » chacune, total) ; le plan
reste le temps qu'ils finissent. Les lettres arrivent quand on ENTEND leur nom (« Alif… Lam… Mim… ») après la balise :
mettre la balise juste avant la phrase qui les nomme. `{chiffre ×10}` : le plan attend qu'il ait fini de monter + 1 s.

**Sources** : `{source "BOUKHARI 652"}` s'affiche pendant TOUTE la réplique qui la porte (même balise en fin de phrase),
sur la scène, par-dessus l'épaule et dans le schéma ; glisse sous un bandeau d'étape ; reste sans clignoter si la
réplique suivante a la même source. Une réplique qui cite un texte sans `{source}` n'a rien à l'écran : en mettre une
(ex. « Le Prophète ﷺ a raconté… » doit porter sa source, pas seulement la phrase d'après).
**L'écume de la mer** (décor plage) : `{ecume "TES PÉCHÉS"}` = plan rapproché sur le rivage, écume étiquetée, une vague
l'emporte en scintillant. **Version concrète** (01/11/2026) : `{ecume "TES PÉCHÉS" sale}` = chaque paquet d'écume SALE
est un petit péché (plusieurs marqués « PÉCHÉ »), badge « 100 × SUBHAN ALLAH WA BIHAMDIH » en haut ; `{vague}` (sur le
mot) = des vagues arrivent l'une après l'autre et lavent les paquets UN PAR UN (éclat blanc, étincelles) ; la vague se
brise sur le rocher, qui reste ; réplique suivante en `schéma` : `{propre "PETITS PÉCHÉS : EFFACÉS"}` (vert, coché),
`{rocher "GRANDS PÉCHÉS"}` puis `{rocher "IL FAUT SE REPENTIR"}` (orange) au-dessus du rocher. Mettre le même rocher
dans la vue large dès le début : option de décor `objet rocher (640, 1185)` (x, y).
**Ses péchés sur lui** : `{peches PETIT}` = paquets d'écume sale « PÉCHÉ » autour de lui (même image que le rivage).
**Orbes de lumière** (option de décor, jamais de prophète ni de Compagnon dessiné) : `orbes "DES COMPAGNONS" 3
(355, 1010) pensees` (3 boules bleutées, un nuage noir « ! » au-dessus de chacune, hors du halo, chassé par leur
lumière quand la citation de la réponse arrive) et `orbe "LE PROPHÈTE" (805, 930) dore grand` ; ajouter
`ensemble (560, 990)` pour un rapprochement lent. Jamais de « ? » sur ces nuages (pas du doute : an-Nawawi).
**Coran ouvert** (schéma) : `{coran}` = gros plan sur un Coran ouvert (lignes stylisées), la lumière suit la ligne de
droite à gauche, « +1 » sort de chaque lettre lue ; `{chiffre ×10}` ensuite = les « +1 » deviennent « +10 » + badge
« ×10 » ; légende « EN ARABE · EN PRONONÇANT ». **Téléphone qui défile** (schéma) : `{defile}`.
**Lumière** : `{lumiere VOYAGEUR}` = un faisceau doré descend doucement sur lui (pardon, bénédiction).
**Geste pile sur un mot** : `{geste PETIT invoque}` (tout geste ou visage des didascalies).
**Objets** : `{pousse PETIT trottinette mur}` = il la range contre le mur (le passage est libre) ; `{pousse … 330}` =
jusqu'à x = 330 ; `{va MAMIE 560 devant}` = elle marche jusqu'à 560 en passant devant les autres.

**Radiographie, orteil, arbre, balance** (03/11/2026, Shorts duo sur le modèle de « Tes péchés effacés », LISEZMOI
partie 25, démo `scenarios\demo_5_radio_arbre_balance.txt`, exemples `islam_05_aumones.txt`, `islam_06_orteil.txt`,
`islam_07_monde.txt`) — grands schémas « pleins » :
- `{radio PETIT}` radiographie (squelette, sa casquette, 32 articulations rouges qui battent, « 0 / 360 AUMÔNES ») ;
  `{radio articulations}` (vague + « 360 ARTICULATIONS ») ; `{radio +1 "SOUBHAN ALLAH"}` (une passe au vert, « +1 ») ;
  `{radio reste}` (« ENCORE 357 ! ») ; `{radio tout "2 RAKATS DE DOUHA" "SUNNA // PAS OBLIGATOIRE"}` (toutes au vert,
  « 360 / 360 », « ÇA SUFFIT ! », la note facultative remplace la coche) ;
- `{orteil}` gros plan : le pied s'élance AVANT le mot et se cogne pile sur lui (étoile, orteil rouge, « AÏE ! ») ;
- `{arbre "TES PETITS PÉCHÉS"}` puis `{feuilles}` : 14 feuilles mortes (4 marquées « PÉCHÉ ») tombent une à une ;
- `{balance "LE MONDE ENTIER" "2 RAKATS"}`, `{balance + manette}` (un objet de plus), `{balance pese}` (elle penche
  vers la droite) ; `"A // ligne 2 // ligne 3"` pour une étiquette sur plusieurs lignes ; option `deja manette` quand
  on revient à la balance après la scène (« nouveau schéma »).
Quand une réplique commence par un grand schéma pendant `ACCROCHE:`, il est là dès l'image 0, décalé sous l'accroche.
Éviter un grand schéma figé pendant un ﷺ : commencer la réplique sur la scène (`plan moyen`), schéma après « a dit : ».

**Fièvre, forge, eau glacée, ablutions, cauchemar, gestes** (04/11/2026, `explique_0411.py`, LISEZMOI partie 26, démo
`scenarios\demo_6_fievre_ablutions_cauchemar.txt`, exemples `islam_08_fievre.txt`, `islam_09_eau_glacee.txt`,
`islam_10_cauchemar.txt`) — grands schémas « pleins » :
- `{fievre PETIT}` gros plan : malade sous sa couverture, le thermomètre (en bouche et en grand) monte à 39,5 °C,
  sueur, traits de frisson (accroche) ;
- `{forge "TES PETITS PÉCHÉS // AVIS MAJORITAIRE"}` une forge, le fer couvert de croûtes noires « PÉCHÉ » ;
  `{soufflet}` : 3 coups de soufflet, le feu monte, les croûtes partent en cendres, le fer ressort propre (Mouslim 2575) ;
- `{glace}` gros plan : le robinet givré de la mosquée, l'eau glacée tombe dans sa main, « BRRR ! » (accroche) ;
- `{ablutions PETIT}` puis `{ablutions yeux}` `{ablutions mains}` `{ablutions pieds}` : un voile sombre « PÉCHÉ » autour
  de chaque partie part EN LUMIÈRE quand l'eau coule (eau toujours claire : les péchés ne sont pas des corps, an-Nawawi
  3/133) ; l'eau va jusqu'au coude et au talon (Mouslim 244) ;
- `{cauchemar PETIT}` la nuit, bulle de cauchemar (il tombe dans le vide), il se redresse en sursaut (accroche) ;
- `{gestes PETIT}` assis dans son lit VU DE DOS (sa gauche = la gauche de l'écran) puis `{gestes souffle}` (3 souffles à
  gauche, « 1 2 3 »), `{gestes refuge}` (« A'OUDHOU BILLAHI MINA CH-CHAYTAN / WA MIN CHARRIHA ×3 »), `{gestes tourne}`
  (il se recouche sur le côté), `{gestes chut}` (« NE RACONTE PAS LE RÊVE »), `{gestes protege}` (lumière douce,
  « IL NE TE FERA AUCUN MAL ») — Mouslim 2261 · 2262, Boukhari 7044.
Depuis le 04/11, un schéma n'affiche qu'UNE source à la fois : la suivante remplace la précédente (fondu 0,25 s).

**Cent, chemin, Coran, téléphone, tombe, soleil, Enfer** (04/11/2026 soir, `explique_0411b.py`, LISEZMOI partie 27,
démo `scenarios\demo_7_cent_coran_telephone_tombe_soleil_enfer.txt`, exemples `islam_11_cent.txt` à `islam_16_enfer.txt`)
— grands schémas « pleins », anges en lumières, rien de sanglant :
- `{cent}` accroche : l'homme de dos devant sa ville la nuit, « 100 » rouge ; `{chemin}` la route SA VILLE → LE BON PAYS,
  le savant montre le chemin, puis `{chemin part}` (il marche) `{chemin mort}` `{chemin anges}` `{chemin rapproche}`
  `{chemin mesure}` (« PLUS PROCHE D'UN EMPAN ») `{chemin pardon}` (Boukhari 3470, Mouslim 2766) ;
- `{bute PETIT}` accroche (Coran lu par à-coups, « ? », Petit gêné) ; `{double}` puis `{double lit}` `{double dur}`
  `{double x2}` ; `{double anges}` = la lecture fluide avec les anges nobles (Mouslim 798) ;
- `{ecran}` accroche vue d'en haut : le téléphone tombe entre tes baskets, « CRAC ! » ; `{dua}` le téléphone fendu, puis
  `{dua inna}` `{dua recompense}` (médaille) `{dua mieux}` (cadeau) `{dua iphone}` `{dua choisit}` (Mouslim 918) ;
- `{tombeau}` la tombe en coupe (pas `{tombe}` : c'est déjà la chute des feuilles de l'arbre), puis `{tombeau anges}`
  `{tombeau paradis}` `{tombeau cri}` `{tombeau crie}` (Boukhari 1374) ;
- `{chaleur PETIT}` accroche au stade ; `{soleil}` le soleil qui descend + 4 silhouettes, puis `{soleil mile}`
  `{soleil chevilles|genoux|taille|bouche}` (Mouslim 2864) ; `{soleil ombre}` + `{soleil jeune}` (Boukhari 660) ;
- `{brulure}` accroche (le doigt sur la poêle, « AÏE ! ») ; `{braises}` le moins puni, puis `{braises pense}`
  (Boukhari 6562, Mouslim 213) ; `{datte}` puis `{datte tacos}` `{datte parole}` (Boukhari 1417 · 6540).
Une réplique de 30 s trop longue : la couper en plusieurs lignes du même perso aux « … » (le moteur resserre les
silences, sans nouvelle voix) ; une partie sans balise prend la didascalie « schéma » pour rester sur le schéma.

**Format CONSIGNE : jurer, éternuement, colère, Bismillah, dette, coucher** (07/11/2026, `explique_0611.py` + 6 modules
`explique_0611_serment|eternue|colere|maison|dette|sommeil.py`, LISEZMOI partie 28, démo
`scenarios\demo_8_jurer_eternuement_colere_maison_dette_sommeil.txt`, exemples `islam_17_jurer.txt` à `islam_22_dormir.txt`) :
- `{jure PETIT}` accroche (couloir de lycée, main levée, « SUR LA TÊTE DE MA MÈRE ! », STOP) ; `{serment}` tableau noir,
  puis `{serment pere}` `{serment mere}` (barrés) `{serment allah}` (or) `{serment frere}` (FRÈRE / VIE apparaissent puis
  barrés) `{serment tais}` (« … OU TU TE TAIS ») `{serment vrai}` (Abou Dawoud 3248) ;
- `{atchoum PETIT}` accroche (il éternue dans son coude, « ATCHOUM ! » étouffé) ; `{chaine}` + `{chaine aime}`
  `{chaine hamd}` `{chaine reponse}` `{chaine retour}` `{chaine rien}` (bulles qui se répondent, Boukhari 6223-6224,
  Mouslim 2992) ; `{rhume}` + `{rhume reponse}` `{rhume deux}` `{rhume enrhume}` (Mouslim 2993 ; dou'a à part, en blanc) ;
- `{enerve PETIT}` accroche (télé « PERDU », manette, vapeur) ; `{colere}` jauge « COLÈRE » + `{colere refuge}` (elle
  descend pendant que Petit dit la formule) `{colere fort}` (trophée) `{colere gg}` (« GG EZ », pouce) ;
- `{porte}` accroche vue à ta place (clé, porte, enseigne « CHAMBRE LIBRE ») ; `{maison}` + `{maison entre}`
  `{maison mange}` `{maison pas}` (« PAS DE CHAMBRE / PAS DE DÎNER ») `{maison libre}` (Mouslim 2018, 2e cas exact) ;
- `{sms}` accroche (ton téléphone : Karim réclame ses 5 €, calendrier 3 MOIS) ; `{dette}` + `{dette efface}`
  `{dette reste}` `{dette injustice}` (la liste du martyr, jamais celle de Petit) ; `{carnet}` (Coran 2:282, extrait) ;
- `{lit PETIT}` accroche (la nuit, visage éclairé par le téléphone, 01:12) ; `{sommeil}` + `{sommeil verset}`
  `{sommeil nuit}` `{sommeil reveil}` (couché sur le côté droit, aube SANS soleil, Boukhari 6324, Coran 39:42).
Fin d'un Short : un schéma peut déborder jusqu'à 1,4 s sur « ABONNE-TOI » ; si la dernière carte doit se lire, finir par
une courte réplique en « (schéma) » (ex. Petit : « Bon… je signe ! »).

**VUE SUBJECTIVE — Shorts « … tu fais quoi ? »** (pov.py, 02/11/2026 ; LISEZMOI partie 23). Modèle : EXC 1, le serpent sur
le tapis, le Short qui a le mieux retenu sur TikTok : le spectateur est À LA PLACE de celui qui vit la scène. Décors :
`tapis_pov`, `porte_pov`, `remise_nuit`, `puits`, `chevet_pov(_jour)`, `nuque_nuit` / `nuque_jour`, `chambre_aube`.
Narrateur en voix off : `NARRATEUR (voix off) : …` (sous-titres sans vignette). Toute réplique avec une balise `{pov …}`
= plan en vue subjective jusqu'à la fin du décor :
- `tapis_pov` : `{pov passant}` (il arrive et s'arrête entre toi et ton sac = la soutra), `{pov soutra}`, `{pov repousse}`
  (ta main le repousse), `{pov insiste}`, `{pov repousse fort}`, `{pov demon}` (halo sombre), `{pov contourne}` ;
- `porte_pov` : `{pov chat}` (chat maigre sous la pluie qui vient s'asseoir devant toi), `{pov chat là}`, `{pov miaou}`,
  `{pov gamelle}` (ta main pose une gamelle, il mange, cœurs) ;
- `remise_nuit` : `{pov chatte}` (chat attaché au poteau), `{pov jours}`, `{pov porte}`, `{pov enfer}` (l'image rougit) ;
- `puits` : `{pov chien}`, `{pov botte}` (botte pleine d'eau, il boit), `{pov pardon}` (lumière dorée) ;
- `chevet_pov` : `{pov reveil "05:47"}` (téléphone qui sonne, FAJR), `{pov manque}` (« 3 alarmes manquées ») ;
- `nuque_nuit` / `nuque_jour` : `{pov noeuds}` (3 nœuds + « la nuit est longue… dors »), `{pov defait}` (le suivant se
  défait), `{pov dhikr}` (« الحمد لله » doré), `{pov eau}`, `{pov priere}`, `{pov oreille}` ;
- partout : `{pov label "TEXTE"}` (autocollant au milieu de l'écran, le suivant le remplace), `{pov}` (rien).
En-tête `ACCROCHE_DUREE: 4.2` : l'accroche reste le temps de la question. Exemples : `scenarios\tfq_01_passant.txt`,
`tfq_02_chat.txt`, `tfq_03_fajr.txt`. Toujours regarder les 5 premières secondes (une image toutes les 0,5 s).

Sons automatiques (discrets) : whoosh doux à l'entrée d'un plan d'explication, papier (photo), scintillement (miroir),
tampon (✓ / ✗), petit « ting » (autres éléments, étiquettes), clic d'appareil, pas.

## 6. Sous-titres : mots importants et durée
`*moche*` ou `*trente pour cent*` → en jaune dans les sous-titres (1 par réplique, sur le mot qui compte). Les étoiles
ne sont pas envoyées à ElevenLabs. Nombres en toutes lettres dans le texte dit (« trente centimètres »), en chiffres
dans les schémas (`{chiffre +30 %}`). ﷺ dans le texte : ElevenLabs le lit en entier (≈ 2,5 s) — la maquette en tient
compte ; à l'écran (sous-titres) il devient « (paix et salut sur lui) ». **30 s MAXIMUM, FIN comprise** (règle du
01/11/2026), à revérifier avec les vraies voix.

## 7. Commandes
```
python scenario.py scenarios\x.txt sheet            planche (maquette sans voix tant que les MP3 n'existent pas)
python scenario.py scenarios\x.txt still 12.4 a.png  une image
python scenario.py scenarios\x.txt voix             textes pour ElevenLabs
python scenario.py scenarios\x.txt asr              recale sur les vraies voix
python scenario.py scenarios\x.txt tout             la vidéo (plusieurs cœurs, priorité basse)
python controle_video.py "x.mp4" --leger            son, planche, rythme, copie légère
python miniature.py scenarios\x.txt                 miniature YouTube + couverture de Short
python controle_vop.py                              après une modification du moteur (si le dossier des voix VOP est là)
```
Pour un LOT (une commande pour tous les Shorts, un rapport court) :
```
python lot.py verifie  scenarios\islam_3*.txt       contrôles du texte, sans image : « ! » à corriger, « ? » à regarder
python lot.py planches scenarios\islam_3*.txt       + UNE image par Short (« … - controle.png »)
python lot.py voix     scenarios\islam_3*.txt       coût, textes ElevenLabs dans un seul fichier, textes figés
python lot.py rendu    scenarios\islam_3*.txt       rendu + contrôle final + copie légère (ancienne version en (vN))
python lot.py controle scenarios\islam_3*.txt       contrôle final seul
python lot.py livre    scenarios\islam_3*.txt       vidéo + couverture + .txt (titre, description) dans SHORTS A PUBLIER\<date>
python lot.py deja                                  sujets déjà faits + prochain code libre (réserve : sujets.md)
python sources.py cherche "boukhari 163"            une source déjà vérifiée ? (python sources.py : refait l'index)
python sauve_moteur.py <sujet>                      sauvegarde zip datée du moteur et du skill
python controle_avant_apres.py                      anciens Shorts identiques au pixel près après une modification
python controle_briques.py [planche x.png]          les briques se dessinent toutes (30 images / s)
```
Démo jouée / schéma dans un script Python (sans scénario) : `sc.plan_photo`, `sc.plan_selfie`, `sc.plan_reflet`,
`sc.plan_schema`, `sc.plan_epaule`, `sc.plans_auto(D)`, `sc.etiquette/mesure/projecteur/loupe`, `sc.reactions(D)`
(LISEZMOI parties 14-16).
