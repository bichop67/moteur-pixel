# Pièges déjà rencontrés (et la parade)

## Moteur et rendu
- **Vieilles images réutilisées** : un rendu qui reprend d'anciennes images donne une vidéo identique à l'ancienne
  (même taille de fichier au octet près = signe). `tout` vide maintenant le dossier d'images ; si on lance `frames` à
  la main, vider `%TEMP%\ia501\<nom>_frames` d'abord.
- **PC qui rame pendant le rendu** : toujours passer par `tout` (priorité basse automatique) et lancer en arrière-plan.
- **Modifier le moteur** : petits scripts de correction écrits avec l'outil Write puis lancés avec `python` (les
  « heredoc » bash cassent sur les apostrophes françaises). `python sauve_moteur.py avant_<sujet>` AVANT, puis
  `python controle_avant_apres.py` APRÈS (anciens Shorts identiques au pixel près), puis une sauvegarde finale.
- **`controle_vop.py` ne tourne plus** (constaté le 09/11/2026) : il lit `Desktop\VIDEO YOUTUBE\SHORTS VALABLE OU
  PAS\voix\asr_VOP06.json`, et ce dossier n'est plus sur le Bureau. Tant qu'il manque, `controle_avant_apres.py` le
  remplace ; ne jamais écrire « VOP OK » sans l'avoir vu répondre.
- **Un rendu qui échoue (« une partie du rendu a échoué »)** : une seule image qui plante suffit. Relancer avec la
  sortie dans un fichier pour lire l'erreur (`cmd /c "python scenario.py … tout > journal.txt 2>&1"`). Cas du 09/11 :
  une jauge plantait pendant 2 images (rectangle arrondi plus petit que son rayon), invisible sur la planche à
  1 image / s → `python controle_briques.py` dessine chaque brique à 30 images / s.
- **Rendu + autres calculs en même temps** : ne rien lancer d'autre de lourd pendant un rendu (le PC rame, les durées
  doublent).
- **Caractères spéciaux** dans pxv.py (espace insécable des sous-titres) : l'outil Edit peut échouer ; remplacer par
  numéro de ligne dans un petit script.
- **Numérotation Mouslim** de l'outil hadith intégré ≠ sunnah.com (ex. son « Mouslim 132 » = la mort d'Abou Talib).
  sunnah.com bloque la lecture automatique : vérifier dans le Chrome de l'utilisateur.

## Mise en page
- Textes qui se chevauchent (étiquette de démo, source, bandeau d'étape, texte d'un schéma) : regarder la planche aux
  instants où deux éléments arrivent ensemble ; décaler une balise d'un ou deux mots suffit souvent.
- Élément placé en toute fin de phrase : il apparaît sur le dernier mot ; s'il doit rester visible pendant la réaction
  de l'autre, mettre « schéma » dans les didascalies de la réplique suivante.
- Schéma qui s'encombre (3 éléments + flèche) : `{efface}` avant de changer d'idée.
- Démonstration jouée : la règle et son chiffre doivent rester au-dessus des sous-titres ; si un plan reste figé plus
  de 4 s, le moteur rapproche la caméra, sinon ajouter un élément.
- 16:9 : vérifier quelques images (`still`) : les encarts passent sur le côté, le texte du miroir à droite.
- **Source affichée après sa phrase** (corrigé dans le moteur le 01/11/2026) : avant, une `{source}` en fin de
  réplique s'affichait pendant la réplique SUIVANTE (« SELON AN-NAWAWI » sous « Dis je cherche refuge… » qui vient
  de Boukhari) ou disparaissait au changement de décor (« CORAN 19:64 » jamais visible). Maintenant elle couvre sa
  réplique. Toujours vérifier sur la planche que chaque source tombe sous la phrase qu'elle justifie : c'est une
  règle religieuse (attribution), pas un détail.
- **Bandeau d'étape sur une citation ou une source** : le moteur s'en charge (le bandeau s'efface avant la citation,
  la source glisse dessous, aussi dans un schéma) ; vérifier quand même la planche.
- **Guillemet fermant seul en sous-titre** (« … de Moi. » puis « » » seul) : corrigé dans le moteur le 01/11/2026 ;
  les planches ne montrent qu'une image par seconde, donc lire aussi la liste des sous-titres (`VID.subs`) quand une
  réplique contient des « ».
- **Long schéma sans perso** (10-12 s) : le couper avec `nouveau schéma` sur la réplique suivante.
- **Lettres / chiffres en avance sur la voix** : les lettres se calent sur leurs noms entendus ; le chiffre a besoin
  d'≈ 2 s de plan après sa balise (le moteur attend).

- **« Partie 2 », « 1/2 », « 2/2 » à l'écran** (refusé le 01/11/2026 : « ça n'a aucun sens ») : un sujet = un Short
  complet ; le moteur n'affiche plus de numéro dans les bandeaux d'étape.
- **Accroche pas assez percutante** (refusée le 01/11/2026) : la 1re phrase doit choquer (peur, honte, provocation,
  paradoxe), puis la réponse exacte arrive tout de suite.
- **Exemple de hadith trop abstrait** (icônes, flèches) : refusé le 01/11/2026 ; montrer le sens propre du texte
  (écume lavée paquet par paquet, orbes avec les mêmes nuages que le perso, lettres qui donnent « +10 »…).
- **Plusieurs étiquettes sur le même perso** : chaque `{barre}` / `{coche}` ne touche que l'étiquette affichée à ce
  moment (corrigé le 01/11/2026 ; avant, une coche passait sur l'étiquette suivante).
- **Étiquette sur le perso + longue citation en haut** : elles se chevauchent ; décaler l'une des deux d'une réplique.
- **Citation par-dessus « ABONNE-TOI »** : corrigé (la citation s'efface au début de la fin) ; une `{texte}` placée
  après le dernier mot d'une réplique finale n'apparaît donc plus : la mettre sur un mot du début.
- **`DUREE_FIN:` ignoré** jusqu'au 01/11/2026 (l'en-tête avec « _ » n'était pas lu) : corrigé.
- **Persos disproportionnés dans la rue** (01/11/2026 : « les personnages sont disproportionnés par rapport au
  décor ») : dans `rue`, un perso faisait trois étages et la porte lui arrivait à la poitrine → décor `rue_proche`.
  Pour tout nouveau décor : une porte ≈ 1,2 fois la taille d'un perso, et rien au premier plan de plus petit que lui
  (une voiture au premier plan doit être plus grande que les persos, sinon l'enlever).
- **Rocher / grands péchés** : un rivage « tout propre » sans le rocher ferait croire que tous les péchés sont
  effacés (avis minoritaire) : le rocher est visible dès le début et pendant la vague (relecture du 01/11/2026).

## Voix
- **Respiration en début de réplique** (≈ 1 s de blanc) : retirée automatiquement par le moteur (scénarios). Un rire
  `[laughs]` en début de réplique est gardé (c'est voulu).
- **Durée** : la maquette se trompe de quelques secondes ; mesurer avec les vraies voix (fabrique + fin du dernier
  plan) avant le rendu. Changer des didascalies ou des balises ne demande pas de nouvelles voix.

- **Recoller des répliques** (accroche neuve + anciennes répliques) : découper les anciennes comme le moteur
  (`pxv.split` + `pxv.resserre`), 1,6 s de silence entre chaque, volume des neuves aligné sur les anciennes, puis
  `asr` (fait le 01/11/2026 : seules les accroches ont été régénérées, ≈ 360 crédits).

## Dépense (leçons du lot du 08/11/2026 : ≈ 1,6 milliard de tokens pour 9 Shorts)
- **Une animation neuve par Short** (≈ 50 Ko de code chacune, écrite puis corrigée image par image) : c'était la plus
  grosse dépense. Depuis le 09/11 : briques réglées depuis le scénario (`references/catalogue.md`).
- **Notes religieuses dans l'en-tête du scénario** (40 à 100 lignes, relues à chaque ouverture) : elles vont dans
  `sources\fiches\<CODE>.md` ; le scénario garde 3 à 6 lignes.
- **Source revérifiée dans Chrome alors qu'elle l'était déjà** : `python sources.py cherche "…"` d'abord.
- **Une commande par Short et par étape** : `lot.py` fait tout le lot en une commande et un rapport court.
- **Images regardées en série** : une image « controle » par Short, puis seulement les instants signalés.

## Livraison (check-list)
1. `lot.py verifie` sans « ! », image « controle » de chaque Short regardée et corrigée.
2. `lot.py rendu` (ou `controle`) : pas de trou de son, volume OK (−14 LUFS avec voix), aucun passage figé de plus
   de 4 s, planche `_qa.png` regardée.
3. Sources vérifiées, notées dans la fiche et affichées ; pour l'islam, relecture indépendante faite AVANT les voix.
4. Ancienne version gardée en `(vN)` (fait par `lot.py rendu`), jamais écrasée ; rien supprimé hors Corbeille.
5. Si le moteur a changé : `controle_avant_apres.py` OK, `controle_briques.py` OK, `sauve_moteur.py`, LISEZMOI à jour.
6. `lot.py livre` : vidéo, couverture et `.txt` (titre, description) dans `SHORTS A PUBLIER\<date>` ; copie légère
   envoyée (SendUserFile), réponse courte qui dit ce qui reste imparfait.
7. Fin de lot : coût noté dans `_MOTEUR_PIXEL\stats\cout_lots.md`.

## Lot du 09/11/2026 (ISL32 à ISL37, mode autonome) : ce qui a fait perdre du temps
- **Brique citation : 5 lignes de 21 caractères au plus (≈ 100 caractères), titre de 30 caractères au plus.** Au-delà le texte tombe à 26 px, illisible. Une formule longue = plusieurs cartes qui se suivent : chaque nouvelle balise {citation "…"} (sans « + ») REMPLACE la carte précédente ; « + » ajoute une ligne à la carte en cours. Même règle pour la liste (lignes de 24 caractères au plus) ; un titre de grille long devient minuscule.
- **Grand (Quentin) lit la translittération arabe lentement : ≈ 3 syllabes par seconde**, la maquette (15 caractères / s) la sous-estime d'un tiers. Compter 1 s pour 3 syllabes d'arabe AVANT les voix, sinon le Short dépasse 30 s (3 Shorts sur 6 ce jour-là).
- Short trop long après les voix, sans crédit : accélérer la voix sans changer la hauteur (ffmpeg tempo 1,07 à 1,10, original gardé dans oix_xxx\originaux), puis scenario.py … asr. Un soupir [exhales] en début de réplique reste collé à la réplique d'avant et fige l'image : le couper dans le fichier.
- La transcription saute parfois une phrase douce ou de l'arabe (« Calme… dis ça », toute une formule) : le calage tient quand même, mais regarder la planche à ces endroits.
- Pour refiger un texte après avoir retiré une réplique : enlever le code de scenarios\_textes_figes.json, puis lot.py voix sur ce seul scénario.

## Lot du 10/11/2026 (ISL38 à ISL43)
- **Grade d'un hadith hors des deux Sahih : regarder AUSSI l'avis de Chou'ayb al-Arna'out et d'Ahmad Chakir (dorar.net)
  avant d'écrire.** « Hasan (Darussalam) » sur sunnah.com ne suffit pas : Tirmidhi 3563 (dettes) était écrit, fiché et mis
  en planche quand le relecteur a trouvé « chaîne faible » chez ces deux-là → sujet écarté, un Short à refaire.
- **`{citation "…"}` à UN seul texte qui contient le mot « QUI »** (ex. « LA SALETÉ QUI S'Y TROUVE ») : la brique le prend
  pour le titre (« qui parle ») et l'affiche minuscule sur une ligne. Toujours donner deux textes dans ce cas :
  `{citation "LE PROPHÈTE ﷺ A DIT :" "…QUI…"}`. Défaut vu seulement sur la planche `_qa` après le rendu.
- **`{citation qui "LE PROPHÈTE ﷺ A DIT :"}` seul pendant « le Prophète ﷺ a dit »** = une carte presque vide 3-4 s :
  moins bien que la scène. Garder la scène pendant cette phrase, la carte arrive avec la citation.
- **Carte de citation de plus de 5 lignes = petit texte** : remplacer la carte (`{citation "suite"}`) au lieu d'ajouter
  (`{citation + …}`) ; listes : lignes de 18 caractères au plus, ajoutées une à une sur les mots.
- **Bandeau `{texte "…"}` de plus de 4 lignes + attribution de 2 lignes** : il descend sur la tête de Grand (ISL39) →
  passer la phrase en brique citation.
- **La transcription (faster-whisper, français) peut sauter une première réplique courte et remplacer une formule arabe
  par une formule plus connue** (« bismillahirrahmanirrahim » écrit pour « bismillahi awwalahou wa akhirah », ISL39) :
  avant de régénérer une voix, retranscrire le passage seul en arabe ; si la voix est bonne, corriger `asr_CODE.json` à la
  main (mots et temps), en gardant le brut à côté.
- **Volume** : le rendu sort parfois à −15,5 / −16 LUFS (Petit qui crie) : gain simple + limiteur sur le MP4 fini (image
  copiée), puis refaire le contrôle ; pas besoin de refaire le rendu.


## Améliorations du moteur du 11/11/2026 (ce qui change dans la façon de travailler)
- **`lot.py verifie` attrape maintenant avant les planches** ce qui avait coûté 3 à 4 tours de planches par lot : carte ou
  liste au texte trop petit, titre ou note réduits, bandeau `{texte}` trop haut, `{citation qui "…"}` seule, maquette trop
  proche de 30 s, hadith hors des deux Sahih sans l'avis d'al-Arna'out / Ahmad Chakir, réplique mal retrouvée dans la voix.
- **Durée** : la maquette compte le français et l'arabe à part (`estime.py`, vitesses mesurées sur les vraies voix). Elle
  n'est plus « large » de 3 s comme avant : viser 27,5 s ou moins en maquette. `python estime.py mesure` après quelques lots.
- **Titre des cartes de citation** : « LE PROPHÈTE ﷺ A DIT : » passe tout seul sur deux lignes (avant : réduit à 58-78 %).
  Un « QUI » dans le texte cité n'est plus pris pour le mot-clé `qui` (la parade des deux textes n'est plus nécessaire).
- **Volume** : réglé tout seul à −14 LUFS (±0,5) au rendu ; plus de gain à la main sur le MP4.
- **Transcription** : `scenario.py … asr` donne le texte connu en indice ; il affiche « N % du texte retrouvé » par voix.
  Sous 90 % : écouter la voix avant de corriger `asr_CODE.json` à la main.
- **Rendu** : ≈ 3 à 4 min par Short (encodage 4 fois plus rapide, même qualité mesurée).
- **Mesure qui m'a trompé** : sur 6 images isolées, le décor semblait redessiné à chaque image ; en réalité il l'est une
  fois par plan. Toujours mesurer un Short entier (1 image sur 5) avant de conclure sur la vitesse.
