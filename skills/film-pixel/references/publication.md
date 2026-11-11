# Publier un film et ses Shorts

Ne rien publier, programmer ni modifier sans demande explicite de l'utilisateur. Label IA toujours « Non ».

## 1. Le fichier `Film Episode N - Titre description chapitres.txt`

- **TITRE** (décision du 02/11/2026, remplace celle du 26/10) : ACCROCHEUR, sur le modèle du film Dajjal (« Dajjal, le
  film : quand viendra-t-il et que fera-t-il ? 👁️ » : 3 450 vues, 226 h et +30 abonnés en 3 jours). Le nom français
  connu + le conflit, puis une accroche exacte et sourcée : « MOÏSE CONTRE PHARAON, le film : le roi qui se disait dieu
  👑 » (79:24, 28:38). Le nom arabe (Moussa) dans une variante du titre ou dans la description ; environ 60 caractères ;
  sans numéro d'épisode. Proposer 2-3 variantes. Ancienne règle (« L'HISTOIRE DU PROPHÈTE MOUSSA ») abandonnée.
- **DESCRIPTION** : une phrase d'accroche ; ce qu'on voit dans le film ; « Les références (Coran, hadiths et récits des
  savants d'autrefois) s'affichent à l'écran. » ; CHAPITRES ; sources principales ; liens des épisodes précédents ;
  « Abonne-toi pour ne pas rater la suite 🕹️ » (l'appel à s'abonner est ici, jamais dans la voix) ; 3-4 hashtags.
- **CHAPITRES** (description seulement, jamais à l'écran) : horodatages relevés sur le rendu final (début de chaque
  partie : l'assemblage les donne), le premier à 0:00, au moins 3, chacun d'au moins 10 secondes.
- **RÉGLAGES** : pas conçue pour les enfants · promotion rémunérée Non · contenu modifié / IA Non · catégorie
  Éducation · langue française · playlist « L'histoire des prophètes » (films seulement) · écran de fin vers l'épisode
  précédent ou la playlist.

## 2. Miniatures

- **« Un truc badass qui fait peur »** (décision du 02/11/2026, modèle : `FILM\HORS SERIE - LE DAJJAL\Film Hors-serie -
  Le Dajjal - Miniature.jpg`) : image SOMBRE, une silhouette géante et menaçante à contre-jour (le tyran, le méchant de
  l'histoire), les yeux qui brillent, un grand halo de lumière derrière elle (soleil de sang, lune) ; le prophète =
  une orbe de lumière face à elle (jamais dessiné). Titre énorme en bas : un mot jaune (255, 212, 72) + une ligne
  blanche, très gros contour noir, police Segoe UI Black ; rien d'important en bas à droite (la durée s'y affiche).
- Le texte = le nom français connu + le conflit (« MOÏSE / CONTRE PHARAON »), pas le nom arabe seul.
- Pixel art dessiné en code, pas d'image générée par IA (refusée pour la monétisation, 30/10/2026). Modèle :
  `_MOTEUR_PIXEL\outils_film\mini_pharaon.py` (480 x 270 agrandi x4, halos, bloom, grain ; Pharaon géant
  réutilisable ; variantes soleil de sang / mer ouverte). Deux variantes pour Test & Compare, enregistrées sous de
  nouveaux noms (jamais par-dessus une miniature déjà envoyée). Les regarder en taille téléphone (360 px) avant d'envoyer.

## 3. Envoi et programmation (YouTube Studio, Chrome de l'utilisateur)

- Le fichier du film est trop lourd pour l'outil d'envoi : l'utilisateur choisit le fichier dans Studio (brouillon),
  Claude remplit le reste. Ne jamais appuyer sur Échap dans la fenêtre d'envoi.
- Programmation : à l'heure donnée par l'utilisateur, fuseau « (UTC+01:00) Paris » choisi dans la liste, heure choisie
  dans la liste (pas tapée) ; vérifier date + heure + fuseau + miniature avant de valider, puis la confirmation.
- « Programme les autres » = le jour même, étalé (au moins 2 h d'écart), sauf indication contraire.

## 4. Shorts tirés du film

- 30 s maximum, un moment fort complet, première phrase choquante + texte d'accroche dès la 1re image, jamais de
  « partie 2 » ni de numéro, fin courte « Abonne-toi pour la suite ».
- Rendus en vertical avec le moteur (mêmes voix découpées) : voir `scenario-film.md`, section 6.
- Fichiers : `Short Film NN - <titre>.mp4` + `Short Film NN - Titres et descriptions.txt` dans le dossier du film ;
  copie légère < 10 Mo pour l'envoi par Chrome.
- Publication : titre court (≈ 60 caractères), légende TikTok = titre + 4 hashtags en gras (choisir la suggestion pour
  chaque tag, vérifier au zoom), « Vérification de contenu simple » désactivée ; YouTube : « Vidéo similaire » =
  l'épisode, jamais de playlist, catégorie Éducation ; Instagram : Reel, ne pas appuyer sur Échap. Jamais deux Shorts
  à la même minute. Sur TikTok, l'heure d'une vidéo programmée ne se change plus : vérifier avant de valider.
- Relecture indépendante des textes lus, des textes à l'écran, des titres et des descriptions avant la livraison.

## 5. Après la sortie

- Ajouter l'épisode à la playlist ; mettre le lien de la suite dans la description de l'épisode précédent.
- À J+2 ou J+3 dans Studio : rétention (surtout la première minute et les endroits où l'on décroche), durée moyenne
  regardée, part du trafic venue des Shorts. Proposer d'ajouter à ce skill chaque leçon tirée des chiffres.
- Correction d'un épisode en ligne, seulement avec l'accord de l'utilisateur : lui montrer les horodatages exacts, puis
  couper le passage avec l'éditeur de Studio plutôt que supprimer ou passer en privé (les heures de visionnage
  disparaîtraient).
