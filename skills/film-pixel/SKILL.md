---
name: film-pixel
description: Faire les FILMS IslamArcade « L'histoire des prophètes » (épisodes d'environ 25 min et films hors-série) en PIXEL ART avec le moteur maison _MOTEUR_PIXEL et la stratégie d'attention des Shorts — histoire RACONTÉE par un seul conteur et vérifiée (Coran Hamidullah, hadiths authentiques, récits des savants d'autrefois), voix ElevenLabs (conteur, personnages ; temps des mots par la transcription ElevenLabs), scènes 16:9 animées qui MONTRENT ce que dit la voix, rendu sur le PC, contrôle image par image, miniature, livraison dans FILM\EPISODE N, publication YouTube et Shorts de 30 s tirés du film. À utiliser pour tout nouvel épisode ou hors-série — « la prochaine histoire de prophète », « l'épisode de Moussa », « fais le film », « continue la série », « l'histoire de Dawoud » — même si l'utilisateur ne dit pas « pixel ». Fusion des skills video-pixel et islamarcade-film (01/11/2026).
---

# Films « L'histoire des prophètes » en pixel art

Toujours parler français à l'utilisateur. Ce skill est la fusion demandée le 01/11/2026 (« avec ce nouveau moteur et cette nouvelle strat… fusionne un nouveau skill, celui-ci avec celui des films, pour créer la prochaine histoire de prophète ») de :
- **video-pixel** : le moteur `_MOTEUR_PIXEL`, les scénarios texte, les explications MONTRÉES, le kit pour garder l'attention, le contrôle image par image ;
- **islamarcade-film** : la série, le format conte, les règles religieuses des films, les voix, la livraison et la publication.

Il les remplace pour tout nouveau film. **Charger aussi islamarcade-shorts** : sa section 0 (vérification religieuse, règle absolue) et sa section 3 (son) s'appliquent sans exception. Pour une balise ou une commande du moteur absente d'ici : skill **video-pixel** (`references/balises.md`) et `Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL\LISEZMOI_MOTEUR.txt`.

Références de ce skill (les lire au moment de l'étape) :
- `references/script-conte.md` — écrire le script : conte, attention, clarté, émotion, limites religieuses, fichier ElevenLabs, casting ;
- `references/scenario-film.md` — du script au film pixel 16:9 : parties, décors, orbes, ce qu'on montre, commandes ;
- `references/publication.md` — titre, description, chapitres, miniatures, réglages, Shorts tirés du film, après la sortie.

## 0. Ce que l'utilisateur veut (prioritaire sur tout le reste)

1. **Un vrai film de cinéma, avec TOUTE l'histoire** (01/11/2026 : « cinématique, digne d'un film de cinéma », « je veux toute l'histoire, même si c'est 40 minutes », « du début à la fin ») : la durée que l'histoire demande (≈ 155 mots de voix par minute), sans rien résumer. Une très grande histoire reste UN SEUL film, du début à la fin, même s'il dure une heure (décision du 01/11/2026 pour Moussa : « Non, je ne veux pas que le film s'arrête à l'appel de Pharaon… même si le film dure 1 heure » ; résultat : 49 min 35 en 24 parties assemblées). Mesurer la durée avec les vraies voix avant le rendu.
2. **Une histoire RACONTÉE par une seule personne, pas un cours ni un rappel** (décision du 02/11/2026, qui remplace l'ancien format « narration au présent + voix du Coran » : « je n'ai pas envie des paroles du Coran, je veux que ça soit une histoire racontée par une personne, du genre tu sais Moussa à ce moment a fait ça, du coup il a fait ça, alors il… », « je ne veux pas deux voix qui expliquent », « je ne veux pas faire de rappel, je veux raconter une histoire ») : UN conteur, au passé oral (« Alors Moussa a dit… », « Et là… », « du coup », « tu sais »), phrases courtes ; les versets sont dits par le conteur en mots simples, au plus près du sens de Hamidullah (paroles d'Allah, de Moussa et des figures vénérées rapportées : « Allah lui a dit : « … » ») ; plus de VOIX DU CORAN ; pas de leçon, pas de rappel, pas d'aparté de savant ; les récits des savants racontés comme l'histoire, sans nom de savant dans la voix (la référence s'affiche en haut à droite). Modèle : `_MOTEUR_PIXEL\scenarios\film\ep14_conte\p01.txt` … `p24.txt`.
2 bis. **Des personnages qui se parlent** (01/11/2026 : « fais parler d'autres gens… des conversations… que ça soit un film ») : chaque personnage ordinaire (roi, conseillers, devins, gardes, servantes, passants, bergers…) a sa propre voix et joue ses scènes ; le contenu de chaque réplique vient du Coran ou des récits des savants (référence affichée), jamais inventé. Prophètes et figures vénérées restent des orbes non doublées (section 3).
3. **Personne ne s'ennuie** (la stratégie des Shorts, 31/10 et 01/11/2026, appliquée au film) : première phrase CHOQUANTE (exacte, et le sens arrive tout de suite) ; à l'image, un changement utile toutes les 2 à 4 s, jamais un plan figé plus de 4 s ; des questions ouvertes et des relances ; tout ce que dit la voix est MONTRÉ (les persos font l'action ; une explication devient une carte, un compteur, une démonstration jouée — jamais un décor immobile sous une voix) ; sous-titres avec le mot important en jaune.
4. **Rendu pro, mouvements doux, caméra calme** : glissements lents et fondus ; jamais de secousse, de flash ni de coupe sèche (l'utilisateur a la nausée). « Trop de zooms inutiles » (02/11/2026) : en-tête `CAMERA: calme` — la caméra ne bouge que sur les moments clés (`{cadre X}`, `{gros X}`, `{large}`, 1 toutes les 15-30 s, jamais deux à moins de 7 s ; vérifier avec `_source\outils\debug_camera.py N`). Un décor dédié à chaque lieu et à l'époque ; persos à l'échelle du décor (une porte ≈ 1,2 fois un perso). Graphismes soignés : la mer ouverte « c'est quoi cette daube » a été refaite (decors_mer.py) — tout effet spectaculaire se vérifie en image avant le rendu.
4 bis. **Le bâton de Moussa toujours avec lui dès qu'il est berger** (02/11/2026) : en-tête `BATON_MOUSSA: oui` (le bâton suit l'orbe partout ; option de décor `sans_baton` pour une scène où il ne l'a pas). Même logique pour l'objet propre à un prophète dans les prochains films.
4 ter. **Sous-titres calés au mot près** (« lors de la révélation les sous-titres ne sont pas raccordés au texte », 02/11/2026) : temps des mots donnés par ElevenLabs (section 6) et contrôle `controle_soustitres.py` sur plusieurs parties rendues.
5. **Clair pour un enfant de 10 ans** : on sait toujours qui fait quoi, pourquoi, où et quand ; ce qui peut être mal compris est dit en une phrase.
6. **Un film finit comme un film** : pas de « dans le prochain épisode », pas d'« abonne-toi » à la voix, aucune image d'un autre épisode ; dernière phrase forte, dernière image tenue, fondu au noir d'environ 5 s, musique qui s'éteint.
7. **Qualité avant délai** : planches regardées, contrôle 1 image par seconde, voix vérifiées ; toute nouveauté du moteur se montre d'abord dans une vidéo démo légendée.
8. **Claude génère les voix lui-même** (autorisation permanente) en annonçant le coût, et prévient avant d'épuiser les crédits.
9. Ne jamais publier, programmer, modifier, passer en privé ou supprimer une vidéo sans demande explicite. Label IA toujours « Non ». Jamais de Short dans une playlist. Supprimer seulement vers la Corbeille ; ne jamais écraser une version déjà envoyée (renommer l'ancienne en « (vN) »).

## 1. La série

| # | Épisode | YouTube |
|---|---|---|
| 1 | Adam et Iblis | rxRjFW6eAZ0 |
| 2 | Qabil et Habil | vu7AXoGLgCE |
| 3 | Nouh et le déluge | KkO8Lxo0YzA |
| 4 | Houd et le peuple de 'Ad | lHRmd3tmISE |
| 5 | Salih et la chamelle | E4sehGQ-gyU |
| 6-7 | Ibrahim (1) et (2) | jqZPFUVRG28 · CheZYAccTkk |
| 8 | Lout | — |
| 9-10 | Youssouf (1) « et le puits » et (2) « et la coupe du roi » (+ « L'histoire complète », 48 min) | 20gsp2TFDRg · X2HcE5niRtg (· Z_t3w_nUpIQ) |
| 11 | Ayyoub (format conte HD) | ngMr7PdZ3NE |
| 12 | Chou'ayb | -QPbx-kVU7g |
| 13 | Younous (finissait sur l'annonce de Moussa : « un petit panier qui flotte sur le Nil, droit vers le palais de Pharaon ») ; depuis le 03/11/2026 : écran de fin (20 dernières s) = le film de Moussa + S'abonner, et 1re ligne de la description « ▶ La suite : MOÏSE CONTRE PHARAON LE FILM → lien » | KejFwjjqrgo |
| 14 | Moussa, le film — publié le 03/11/2026 sous « MOÏSE CONTRE PHARAON LE FILM » (titre choisi par l'utilisateur), 52 min 34, playlist, test A/B des 2 miniatures, écran de fin playlist + S'abonner sur les 6 dernières s (après la dernière phrase) | bMfjM2jflW4 |
| HS | Dajjal, le film | 13kuXDvwmaE |
| HS | Gog et Magog, le film (pixel, 10/11/2026 : 9 parties, ≈ 10 min 40 ; Coran + hadiths authentiques seulement ; dossier `FILM\HORS SERIE - GOG ET MAGOG\`, scénarios `scenarios\film\gog\`, moteur `decors_gog.py` + `decors_gog2.py`, LISEZMOI partie 30) | — (pas encore publié) |

Playlist « L'histoire des prophètes » : `https://www.youtube.com/playlist?list=PLBHtqZ6DZ_vU` (films seulement, triée de la plus ancienne à la plus récente).

Les épisodes 1 à 13 sont en illustration HD peinte (moteur cloud, skill islamarcade-film). **À partir de l'épisode 14 : moteur pixel** (ce skill). Relever les ID manquants dans Studio quand on y passe.

**Épisode 14 = Moussa, toute l'histoire en UN SEUL film** (décision du 01/11/2026 : « même si le film dure 1 heure ») :
de la naissance à la mort de Moussa, en 24 parties. 1re version (narration au présent + voix du Coran, 49 min 35)
assemblée le 02/11/2026 puis REFAITE le même jour en version « conte » à la demande de l'utilisateur (section 0) :
scénarios `_MOTEUR_PIXEL\scenarios\film\ep14_conte\p01.txt` … `p24.txt`, voix `FILM\EPISODE 14\voix_conte\`,
outils `FILM\EPISODE 14\_source\outils\` (file_rendu, planches_conte, asr_conte, assemble_conte…). L'ancienne version
et ses voix ont été mises à la Corbeille (place disque). Version conte assemblée et contrôlée le 03/11/2026 :
`FILM\EPISODE 14\Moussa - le film.mp4` (52 min 33, 12,4 Go, −14,6 LUFS) + `(leger)`, chapitres dans
`Film Episode 14 - Moussa description chapitres.txt`, extrait téléphone envoyé (la révélation, 2 min 04). Reste connu :
19 sous-titres sur 2 240 avec un « » » mal placé (parties 3, 4, 5, 7, 8, 9, 10, 13, 17, 22, 24 ; moteur corrigé le
03/11 ; refaire ces parties + l'assemblage ≈ 6 h de PC, seulement si l'utilisateur le veut). Ensuite (à confirmer avec l'utilisateur) : Dawoud et
Souleymane · Zakariya, Yahya et Maryam · 'Issa · Mouhammad ﷺ.

**Ménage du 03/11/2026 (place disque, demande de l'utilisateur)** : tous les fichiers des films (dossier `FILM` en
entier : vidéos, parties rendues, voix, textes, miniatures) ont quitté le PC. Le film de Moussa n'existe plus que sur
YouTube : un Short tiré du film demande donc de nouvelles voix. Restent : les scénarios
`_MOTEUR_PIXEL\scenarios\film\ep14_conte\p01.txt` … `p24.txt` et les outils du film rangés dans
`_MOTEUR_PIXEL\outils_film\` (assemble_conte, file_rendu, planches_conte, asr_conte, controle_final_conte,
mini_pharaon, publication_ep14_modele.txt…). Le prochain film recrée `FILM\EPISODE N\`.

Dossier de chaque film : `Desktop\VIDEO YOUTUBE\FILM\EPISODE N\` (hors-série : `FILM\HORS SERIE - <NOM>\`). Rythme : un épisode tous les deux jours au plus ; mieux vaut décaler un épisode que sauter la vérification.

## 2. Les étapes (faire une liste de tâches)

1. **Recherche et plan** : versets, hadiths, récits des savants ; liste des scènes (lieu, moment, ce qu'on y voit) ; 2 à 4 moments forts.
2. **Script** au format ElevenLabs (`references/script-conte.md`) dans `FILM\EPISODE N\Film - Episode NN - <Nom> - ElevenLabs.txt`.
3. **Vérification religieuse + relecture indépendante** (agent séparé) AVANT les voix ; corriger, puis envoyer le script à l'utilisateur avec ce qui a été corrigé.
4. **Moteur** : construire les décors, persos, objets et démonstrations qui manquent ; les montrer dans une vidéo démo légendée ; lancer `python controle_moteur.py` AVANT et APRÈS (96 images de référence sans voix, identiques au pixel près ; `controle_vop.py` ne tourne plus) ; zip daté dans `_MOTEUR`.
5. **Voix** : coût annoncé, puis génération par Claude (section 6) ; durée réelle mesurée.
6. **Scénario pixel** : un fichier par partie (`references/scenario-film.md`) ; planches regardées et corrigées.
7. **Rendu** des parties en arrière-plan ; contrôle de chaque partie ; assemblage du film.
8. **Contrôle final** : planche 1 image/s regardée en entier, rythme, volume, transcription du début et de la fin, durée.
9. **Livraison** dans le dossier du film (section 8) ; chapitres relevés sur le rendu final.
10. **Shorts de 30 s** tirés du film (section 9), proposés à l'utilisateur.
11. **Publication** seulement sur demande (`references/publication.md`).

## 3. Règles religieuses (le détail est dans islamarcade-shorts, section 0)

- **Versets** : traduction de Hamidullah mot pour mot (quran.com/fr ; outil `get_quran_verse` en « french »). Retouches permises : les coupes (référence « EXTRAIT »), la forme arabe des noms (Moïse → Moussa, Pharaon reste Pharaon), les crochets et parenthèses explicatives retirés (ElevenLabs lirait un crochet comme une balise). Toute retouche est notée dans les règles de l'épisode. Ne jamais « moderniser » un mot.
- **Hadiths** : seuls les hadiths authentiques (sahih) ou bons (hasan) sont attribués au Prophète ﷺ ; grade vérifié ; numéro vérifié page par page sur sunnah.com dans le Chrome de l'utilisateur (sunnah.com bloque la lecture automatique ; l'outil hadith intégré numérote Mouslim autrement). Un récit d'un Compagnon (ex. Ibn 'Abbas) reste attribué à lui, jamais au Prophète ﷺ.
- **Format conte** : chaque détail se trouve vraiment chez un savant ancien (Ibn Kathir, At-Tabari, Al-Baghawi, Al-Qurtubi, Ibn 'Abbas, As-Souddi, Wahb ibn Mounabbih…) et sa référence s'affiche en haut à droite ; rien d'inventé : ni parole, ni pensée, ni geste d'un prophète, ni heure, ni lieu, ni nombre — ni dans la voix, ni dans les lignes IMAGE ; rien qui n'existe que dans la Bible ; on laisse de côté ce qui avilit un prophète et que beaucoup de savants rejettent.
- **Qui est dessiné, qui parle** : prophètes, anges, figures vénérées ou de la famille d'un prophète (Asiya, la mère et la sœur de Moussa, Hajar, Maryam, Al-Khidr, les filles du vieil homme de Madyan…) et Compagnons : jamais dessinés (orbe lumineuse avec leur nom), jamais doublés ; toutes leurs paroles (Coran ou savants) sont rapportées par le conteur (format conte du 02/11/2026 : plus de VOIX DU CORAN). Allah n'est jamais représenté : ni lumière qui « parle », ni feu ou arbre animé sur sa parole (la lueur de l'arbre de Touwa reste régulière). Au moindre doute sur un personnage, demander à l'utilisateur.
- Les autres (Pharaon, Haman, soldats, gens du peuple, bergers…) sont dessinés et doublés, une voix chacun, avec leurs paroles du Coran ; une réplique venue d'un commentateur est introduite par le narrateur (« racontent les anciens »). Iblis : toujours la même voix, jamais en monstre.
- Une mise à mort n'est jamais montrée (fondu, réaction, ombre) ; rien de gore, rien de suggestif.
- **Relecture indépendante obligatoire** (outil Agent, sans le contexte de la rédaction) du script entier AVANT les voix, puis de chaque ajout fait après coup. Consigne : « Tu es un étudiant en sciences islamiques très critique. Trouve toute erreur de sens, d'attribution, de grade de hadith, de numéro de référence, toute retouche d'un verset par rapport à Hamidullah, tout détail du conte introuvable chez le savant cité, toute parole ou geste inventé pour un prophète. Cite tes sources. »

## 4. Le script (détail : `references/script-conte.md`)

- **Ouverture choc (20 à 40 s)** : le moment le plus fort ou le plus mystérieux de l'épisode, et une première phrase qui choque (ex. Moussa : « Une mère jette son bébé dans le fleuve. »), tout de suite expliquée (« … parce qu'Allah le lui a ordonné. Pour le sauver. »). Puis « Comment en est-on arrivé là ? » et « Voici son histoire, telle que la racontaient les savants d'autrefois. » La boucle se referme plus tard sur la même image.
- **Rappel** de 3 à 5 phrases simples quand l'épisode continue une histoire (les spectateurs arrivent souvent par un Short).
- **5 à 8 parties** de 3 à 4 minutes (une partie = un fichier de scénario), chacune finit sur une phrase qui donne envie de voir la suite ; à l'intérieur, une relance toutes les une à deux minutes (une question, « mais… », un nouveau lieu, un nouveau danger).
- **2 à 4 moments forts** développés : phrases très courtes, [pause], silence, musique d'émotion, image lente ; l'émotion naît de la scène elle-même (pas de « Imagine… » adressé au spectateur).
- **Raconté au passé oral par un seul conteur** (section 0.2), scène par scène, phrases courtes, mots simples ; chaque changement de lieu ou de temps annoncé ; chaque personnage présenté à sa première apparition ; une parole du Coran = « X lui a dit : « … » » en mots simples, au plus près du sens de Hamidullah, référence affichée.
- **Scènes dialoguées** : quand une source rapporte ce que des gens se sont dit (un roi et ses conseillers, des devins, des gardes, une servante…), on joue la scène avec leurs voix ; le narrateur ne fait que relier. Une réplique = le contenu de la source, dit simplement ; rien d'ajouté « pour faire vivant ».
- **ﷺ** à voix haute seulement à la première mention du Prophète et une fois au début de la fin ; ailleurs « le Prophète » sans ﷺ.
- **Fin** : une phrase forte qui referme l'histoire (ou ouvre sur la suite par un fait du récit, jamais par une annonce), puis fondu au noir.

## 5. Les images : le moteur pixel en 16:9 (détail : `references/scenario-film.md`)

- Moteur : `Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL\` ; `FORMAT: horizontal` (1920 x 1080, 30 images/s) ; un scénario texte par partie, rendu séparément puis assemblé.
- **Montrer ce que dit la voix** : les persos jouent l'action au mot près (marcher, se retourner, tendre, porter, fuir, abreuver…) ; les orbes se déplacent, brillent, pâlissent ; le décor vit (eau, roseaux, feu, foule, troupeaux, oiseaux, lumière qui change). Une explication devient une image concrète : carte qui trace le trajet, compteur d'années, démonstration jouée (ex. dix bergers qui peinent sur la pierre que l'orbe de Moussa soulève seule).
- **Plans** : plan d'ensemble qui se resserre, plan moyen, gros plan, par-dessus l'épaule pour un échange, réaction de ceux qui écoutent ; glissements lents seulement ; fondu entre deux plans et entre deux parties. Aucun plan figé plus de 4 s (`controle_video.py` le mesure).
- **Texte à l'écran** : les sous-titres (mot important en jaune), la petite référence en haut à droite pendant la phrase qu'elle justifie, le nom sous une orbe, et au besoin le nom des lieux sur une carte. Pas d'encadré, pas de bulle d'information, pas de « À SAVOIR », pas de titre de chapitre (« les gens ne lisent pas, ça brise le graphisme »).
- Les décors, persos et objets propres à l'époque qui manquent sont ajoutés au moteur (`lieux.py`, `troupe.py`/`cast.py`, `objets.py`, `scene.py`), montrés dans une démo, puis notés dans `references/scenario-film.md` et dans le LISEZMOI. Les vidéos déjà livrées ne doivent pas changer : `python controle_moteur.py` après chaque modification (rendu d'origine des VOP, Shorts, Moussa, Gog ; `enregistre` seulement après un changement voulu et regardé).

## 6. Les voix

| Rôle | Voix ElevenLabs | Réglages |
|---|---|---|
| NARRATEUR | ID `Qrl71rx6Yg8RvyPYRGCQ` (affichée « Olivier - Narration » ou « Guillaume - Narrator » : l'ID fait foi), la même dans toute la série | eleven_v4, vitesse 1.00, stabilité 52 %, similarité 53 % |
| VOIX DU CORAN | ID `aQROLel5sQbj1vuIVi6B` (Voix Nicolas Petit) — **plus utilisée depuis le format conte du 02/11/2026** (garder l'ID seulement si l'utilisateur la redemande) | balise [calm] seulement |
| Personnages | une voix par personnage, différente du narrateur et des autres ; casting déjà utilisé dans `references/script-conte.md` (à réutiliser pour les mêmes rôles) | |

- Génération par Claude avec le connecteur ElevenLabs : `creative_create_flow` (un flux par épisode, ou le flux des films `r3QWBUamaM0CEof3l6jd`), `creative_generate_speech` (eleven_v4, `generations_count: 1`, `estimate_only: true` d'abord pour annoncer le coût ≈ 1 crédit par caractère), `creative_get_flow_run_status` → `content_url` → téléchargement direct avec `curl` (ça marche depuis le PC).
- **Une génération par voix et par partie** (moins de 4 300 caractères, sinon deux moitiés A/B recollées avec 1 s de silence : `_source\outils\recolle_ab.py`), répliques séparées par `[long pause]` : c'est le format qu'attend le moteur (`python scenario.py <partie> voix` donne les textes exacts). Fichiers : `<CODE>_<PERSO>.mp3` dans le dossier voix de la partie.
- **Temps de chaque mot = transcription ElevenLabs, PAS faster-whisper sur le PC** (02/11/2026 : Whisper prenait jusqu'à 44 min par partie et rendait le PC inutilisable) : `creative_transcribe_audio` (eleven_scribe_v1, même flow, `connect_from` = node de la voix) → 0 crédit, texte exact, débuts de mots à ±50 ms ; statut avec `creative_get_flow_run_status` (enregistré dans un fichier quand il est gros) puis `_source\outils\asr_conte.py` écrit `asr_<CODE>.json` (balises et ponctuation seule retirées, ﷺ développé, moitié B décalée). Seule une voix réutilisée d'un ancien flux (sans node) passe par `asr_reutilisees.py` (faster-whisper).
- Ne jamais relancer une génération « pour réessayer » sans raison (ça repaye) ; réutiliser une réplique déjà enregistrée quand le texte est identique.

## 7. Le son

- Voix nettement au-dessus : musique environ 18 dB sous la voix quand elle parle, bruitages environ 17 dB sous la voix ; final à −14 LUFS. « Les bruitages sont trop forts » (02/11/2026) : en film, le moteur les divise par deux et les baisse encore sous la voix (ducking) — ne pas les remonter.
- Une ambiance sous presque chaque décor (fleuve, vent, ville, palais, troupeau…) et un son ponctuel doux calé sur l'image toutes les 8 à 15 s ; jamais un son sur chaque titre ni sur chaque sous-titre.
- Bruitages : uniquement `Desktop\VIDEO YOUTUBE\_BRUITAGES` (voir `CATALOGUE.txt` ; ne jamais modifier ce dossier). Son manquant : ElevenLabs Sound Effects (skill islamarcade-shorts, section 3).
- Musique de fond par humeur (`_MUSIQUES\FOND` : fond_desert, fond_mystere, fond_tension, fond_tristesse, fond_epique, fond_espoir, fond_tempete) ; nasheed d'émotion (`_MUSIQUES`) en fondu sur les moments touchants ; jamais de musique du commerce ni de son pris sur internet.

## 8. Rendu, contrôle, livraison

- **Le PC doit rester utilisable** (02/11/2026 : « j'arrive plus à utiliser mon ordinateur ») : TOUT le travail lourd sur 4 processeurs logiques sur 12, priorité faible (`_source\outils\basse.py "cmd"` : masque 0xF00), un seul gros travail à la fois.
- **Une seule commande pour tout le film (11/11/2026)** : `python fais_film.py <dossier des scénarios p01.txt…> <commande> [parties]` remplace les scripts recopiés à chaque film. Commandes : `etat` (voix, calage, durée, rendue ou à refaire), `voix` (textes + crédits → `voix\textes\voix.json`), `asr statut.json` (transcriptions ElevenLabs reconnues par leur texte → `asr_<CODE>.json`), `verifie` (foules, animations et persos dessinés HORS de l'image), `planches [--pas 4] [--de 20 --a 40]`, `brouillon`, `rendu` (file à priorité basse, 4 processus, saute les parties à jour, journal `_source\rendu.log`), `assemble` (garde l'ancienne version sous « (vN) », réglage 23, copie légère), `controle` (durée, volume, crête, silences, `chapitres.txt`, planches), `tout`. En-têtes de scénario : `FILM:` (titre du film entier) et `CHAPITRE:` (titre du chapitre YouTube).
- **Voir le film BOUGER avant le vrai rendu (11/11/2026)** : `python fais_film.py <dossier> brouillon` (ou `python scenario.py <partie> brouillon`) : 10 images/s, demi-taille, avec le son, mot BROUILLON incrusté ; ≈ 2 min par partie au lieu de 6, ≈ 7 Mo par partie, donc envoyable sur le téléphone de l'utilisateur. À REGARDER et à lui envoyer AVANT de lancer le rendu complet : le film Gog a été livré sans avoir été vu en mouvement, c'est ce que ce mode évite.
- **Planche de chaque partie AVANT son rendu** (`fais_film.py … planches` ; avant : `_source\outils\planches_conte.py` : une image toutes les 5 s, pages de 30) et la regarder ; puis la file `file_rendu.py` rend les parties une par une (elle attend la planche validée `planches\pNN.ok`, refait une partie dont le scénario a changé, supprime les ~4 Go d'images temporaires après chaque partie, s'arrête s'il reste moins de 9 Go). Une partie ≈ 25 min, ≈ 58 Mb/s (grain du filtre film) : prévoir ~1,5 Go par partie et ~15 Go pour le film final.
- Rendu d'une partie seule : `python scenario.py <partie> tout 3` ; repart toujours d'images neuves.
- Contrôle de chaque partie : `python controle_video.py "<partie>.mp4" --leger` (durée, volume, trous de son, rythme, planche `_qa.png` à REGARDER).
- Assemblage des parties en un film (fondus entre parties, son normalisé à −14 LUFS, fondu au noir final) : voir `references/scenario-film.md`.
- Contrôle final : planche 1 image par seconde regardée en entier (chevauchements, persos qui flottent, membres qui traversent, texte coupé, sous-titre sur un visage, orbe sans nom), transcription du début et de la fin (formule ﷺ à la première mention, rien après la dernière phrase), durée.
- **Livraison en qualité pleine, jamais recompressée** (« tu compresses rien du tout ») dans `FILM\EPISODE N\` : `L'histoire du prophete <Nom>.mp4`, les 2 miniatures (sombres, qui font peur : section 10), `Film Episode N - Titre description chapitres.txt` (chapitres relevés sur le rendu final), le script ElevenLabs, les scénarios des parties. Une copie légère (< 10 Mo, quelques minutes choisies) peut être envoyée avec SendUserFile pour que l'utilisateur la regarde sur son téléphone.
- Sauvegarder le moteur en zip daté dans `VIDEO YOUTUBE\_MOTEUR\` après chaque modification validée ; mettre à jour le LISEZMOI et ce skill.

## 9. Shorts tirés du film (règles des Shorts du 01/11/2026)

- **30 s MAXIMUM**, fin comprise ; **un moment = un Short complet** (jamais de « partie 2 », jamais de « 1/2 » ni de numéro à l'écran) ; **première phrase choquante** + le même choc écrit à l'écran dès la 1re image (`ACCROCHE:`).
- Fabriqués avec le même moteur : la scène du film rendue en **vertical** (`FORMAT: vertical`, mêmes voix découpées, même mise en scène resserrée), zones sûres de TikTok respectées ; fin « Abonne-toi pour la suite » courte (`DUREE_FIN: 2.0`).
- Un moment fort par Short, posé comme un choc ou une question, sans raconter tout l'épisode ; titre court ; 4 hashtags ; sur YouTube, « Vidéo similaire » = l'épisode dès la publication ; jamais dans une playlist ; relecture indépendante du texte et des titres.

## 10. Publication (détail : `references/publication.md`)

**Titre accrocheur + miniature qui fait peur** (décision du 02/11/2026, sur le modèle du film Dajjal qui a marché : 3 450 vues et 226 h en 3 jours, 69 % du trafic par l'accueil) : le nom français connu et un conflit (« MOÏSE CONTRE PHARAON, le film : le roi qui se disait dieu 👑 », accroche sourcée), le nom arabe dans le titre ou la description ; miniature sombre en pixel dessinée en code (pas d'image IA) — détail dans `references/publication.md` ; description avec chapitres relevés sur le rendu final et sources, pas conçue pour les enfants, catégorie Éducation, langue française, IA = Non, playlist « L'histoire des prophètes » (les films seulement). Programmation à l'heure donnée par l'utilisateur, heure de Paris, vérifiée avant de valider.

## 11. Pièges

- **Leçons du film Gog et Magog (10/11/2026)** : (1) cache des décors : depuis le 11/11/2026 tous les `decors_*.py` comptent d'office dans `egypte._empreinte` (nommer un nouveau fichier de décors `decors_<film>.py`, sinon le cache garde l'ancienne image) ; (2) la fenêtre visible d'un décor de film va de y ≈ 116 à 354 : les foules et objets du premier plan se dessinent entre 300 et 354 — `python controle_cadre.py <partie>` (ou `fais_film.py … verifie`) signale maintenant ce qui est dessiné hors de l'image ; (3) `creative_get_flow_run_status` avec les 14 sessions de voix renvoie ~45 000 caractères dans la conversation : demander les statuts par petits lots, ou seulement quand le total dépasse la limite (les transcriptions, elles, partent d'office dans un fichier) ; (4) le texte des scénarios vit dans UN script (`_source\outils\ecrit_scenarios.py`) qui réécrit les 9 fichiers : on corrige là, jamais dans les fichiers générés ; (5) un grand silence avant un moment fort = un nouveau bloc avec « 7s » et l'animation en option de bloc (`effondre`), pas une annotation ; (6) relecture indépendante : elle a trouvé 9 points à corriger (sujet / complément inversés dans un hadith, « aujourd'hui » du Prophète pris pour notre époque, avis d'exégète présenté comme le verset…) — toujours la faire avant les voix ; (7) hadith disputé (ex. « ils creusent chaque jour », Tirmidhi 3153) : laissé de côté et noté dans les règles du film.

- **Les épisodes 1 à 13 ne sont pas en pixel** : les spectateurs remarqueront le changement de style ; garder la même voix de narrateur, la même voix du Coran et la même structure pour que la série reste reconnaissable.
- **Orbe et prophète** : jamais de silhouette, de main ou d'ombre de prophète ; le bébé Moussa aussi est une orbe (petite).
- **Texte qui prend le dessus** : en film, pas de bandeau d'étape `{etape}`, pas d'étiquette d'explication ; la relance passe par la voix et par l'image.
- **Caméra** : l'utilisateur avait demandé une caméra fixe sur les films peints (« le décor bouge, ça donne le tournis », 20/10/2026), puis trouvé « trop de zooms inutiles » sur le Moussa pixel (02/11/2026) : `CAMERA: calme`. Revers : une longue narration sans balise reste un plan figé (2 min sur la révélation, vu sur la planche) — poser `{cadre X}` / `{large}` aux moments clés, à plus de 7 s du début du décor et les unes des autres.
- **Planches** : défauts vus le 02/11/2026 et à chercher à chaque fois — persos prosternés qui se chevauchent (les espacer de ~210), orbe collée sur un perso (étiquettes qui se recouvrent), un groupe qui « supplie » placé loin de celui qu'il supplie, adorateurs prosternés tournés vers le mauvais côté, petit trait noir droit sur une crête de colline (vide entre le bas des montagnes et le creux de la colline : prolonger les montagnes plus bas, corrigé dans collines_madyan le 02/11/2026) — zoomer sur l'image en taille réelle au moindre doute.
- **Durée** : la maquette se trompe de quelques secondes par partie ; mesurer avec les vraies voix avant le rendu.
- **Crête du son du film** (03/11/2026) : loudnorm, à l'assemblage, avait laissé un pic de +2 dBFS (20 ms) absent des parties ; `assemble_film.py` / `assemble_conte.py` ajoutent maintenant un limiteur à −1,5 dBFS. Toujours mesurer la crête réelle du film fini (`_source\outils\controle_final_conte.py` : volume, crête, silences, planches début / fin / raccords / 1 image toutes les 30 s, transcription du début et de la fin) : sous −0,5 dBTP. Pour corriger un son après coup sans réencoder l'image : `corrige_son_film.py` (son limité, remis sur la vidéo copiée telle quelle, vérif du décalage = 0).
- **Guillemets des sous-titres** : avant le 03/11/2026, un « » » pouvait ouvrir le sous-titre suivant ou rester seul sur la 2e ligne ; corrigé dans pxv.py (vidéos à thème). `_source\outils\guillemets_st.py N` les compte sur un scénario.
- **Extrait pour le téléphone** : couper le son dans un creux de la voix ET l'image avant l'apparition du sous-titre suivant (jamais un sous-titre affiché dont la voix est coupée : c'est exactement le défaut que l'utilisateur déteste) ; image noire tant que le sous-titre de la phrase d'avant est encore affiché ; ne jamais figer une image prise pendant un fondu entre deux plans (double orbe) ; image et son en deux entrées séparées pour tenir la dernière image (`extrait_revelation.py`).
- **Source au bon moment** : la référence s'affiche pendant la phrase qu'elle justifie (c'est une règle religieuse d'attribution) ; vérifier sur les planches.
- Pièges du moteur et des Shorts : skill video-pixel, `references/pieges.md`.
