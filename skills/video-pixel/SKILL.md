---
name: video-pixel
description: Fabriquer une vidéo en PIXEL ART avec le moteur maison _MOTEUR_PIXEL (Shorts / TikTok / Reels 9:16 et vidéos 16:9) — sketch ou dialogue entre persos écrit comme un scénario texte, explications MONTRÉES (démonstrations jouées, miroir, selfie, schémas animés calés sur les mots, étiquettes, règle, loupe), règles pour garder l'attention (accroche, rythme, relances, mots en jaune, zones sûres), voix ElevenLabs, rendu, contrôle qualité, miniature et publication ; règles IslamArcade pour les vidéos islam. À utiliser pour toute nouvelle vidéo pixel, toute idée de vidéo à produire avec ce moteur (y compris « propose-moi des idées de vidéos »), toute retouche d'une vidéo pixel ou toute amélioration du moteur — même si l'utilisateur dit juste « fais la vidéo », « un sketch », « un Short », « VOP », « le moteur ». « Fais 3 Shorts pour aujourd'hui » lance le mode autonome (tout faire seul, sans confirmation). Pas pour le format « flat » (skill short-histoire) ni le Stick néon (skill stick-video).
---

# Vidéos pixel art (moteur _MOTEUR_PIXEL)

Toujours parler français à l'utilisateur. Il veut un rendu professionnel, des explications **montrées pour de vrai** (jamais un perso qui parle devant un décor fixe), des vidéos où personne ne s'ennuie, et **le moins de tokens possible**. Il juge sur la vidéo : chaque nouveauté se livre en vidéo rendue et contrôlée. S'il demande « fais N Shorts » sans autre précision : **mode autonome, section 7** (tout faire seul, sans poser une seule question).

Moteur : `C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL\` (Python, Windows). Persos IslamArcade : `PETIT` (sweat rouge, casquette) et `GRAND` (qamis, gilet vert, kufi). Short duo modèle : `scenarios\islam_13_telephone.txt`.

Ne lire un fichier de référence que quand l'étape en a besoin, et y CHERCHER le mot (Grep) plutôt que le lire en entier :

| Besoin | Où |
|---|---|
| Comment montrer : briques, outils, animations déjà faites | `references/catalogue.md` |
| Écrire un scénario : en-têtes, décors, didascalies, balises | `references/balises.md` |
| Quels sujets et quelles accroches ont fait des vues | `references/resultats.md` |
| Quels sujets ont DÉJÀ été faits (registre à tenir à jour) | `references/sujets_faits.md` |
| Garder l'attention, plan d'un Short de 30 s | `references/attention.md` |
| Erreurs déjà faites, check-list de livraison | `references/pieges.md` |
| Une commande ou une balise absente d'ici | `LISEZMOI_MOTEUR.txt` du moteur |
| Une source religieuse déjà vérifiée | `python sources.py cherche "boukhari 163"` |

## 1. Dépenser peu (règle de l'utilisateur, 08/11/2026)

Le lot de 9 Shorts du 08/11 a coûté ≈ 1,6 milliard de tokens : 113 agents, une animation neuve de ≈ 50 Ko de code par Short, plusieurs relectures par Short, des textes changés après les voix, 750 000 tokens d'historique. Chaque action relit toute la conversation : le coût, c'est la longueur de la conversation multipliée par le nombre d'actions. Donc :

1. **Une conversation neuve par lot** (9 Shorts au plus) ; ne pas enchaîner dans une session déjà longue.
2. **Aucun code nouveau par Short** : les briques de `references/catalogue.md` se règlent depuis le scénario. Une animation neuve seulement pour une accroche, avec l'accord de l'utilisateur et le coût annoncé avant, une par lot au plus.
3. **Une commande par étape pour tout le lot** (`lot.py`, section 3). Regarder UNE image par Short, plus un `still` aux instants signalés ; jamais des images en série.
4. **Claude écrit les textes lui-même.** Un seul agent par lot : la relecture religieuse (il lit les fiches de sources). Un autre seulement pour relever les vues TikTok.
5. **Sources** : `python sources.py cherche "…"` avant d'ouvrir Chrome ; ne vérifier dans le navigateur que ce qui manque. Dès que la fiche est écrite, `python sources.py grades <CODE>` : un hadith hors de Boukhari et Mouslim doit avoir l'avis d'al-Arna'out ou d'Ahmad Chakir AVANT qu'on écrive le scénario.
6. **Textes figés avant les voix** : `lot.py voix` les fige, `lot.py verifie` signale ensuite tout mot dit modifié.
7. **Deux passes de correction au plus par Short** ; au-delà, s'arrêter et dire à l'utilisateur ce qui bloque.
8. À la fin du lot, noter le coût dans `_MOTEUR_PIXEL\stats\cout_lots.md` (tokens de la session, agents, Shorts).

La vérification religieuse et le contrôle de la vidéo finale restent obligatoires.

## 2. Ce qu'un Short doit être

- **30 s maximum, fin comprise** (`DUREE_FIN: 1.5` à `2.0`), revérifié avec les vraies voix : sur TikTok, c'est le temps de visionnage qui compte. Un sujet = UN Short complet : jamais de « partie 2 », de « 1/2 » ni d'autre numéro à l'écran ; si c'est trop long, resserrer (règle + source + nuance indispensable).
- **Le sujet d'abord : trois questions, trois oui** (lecture des vues TikTok du 09/11/2026, `references/resultats.md`, à revoir à chaque relevé). Est-ce que ça ARRIVE au spectateur sans qu'il l'ait choisi (cauchemar, orteil cogné, téléphone cassé) ? Est-ce que ça pique (douleur, perte, peur) ? Est-ce que la réponse soulage ou fait gagner (« bonne nouvelle », « dis ça », gros gain pour un petit geste) ? Sinon changer de sujet : une routine sans émotion, un reproche sur ce qu'il fait, une réponse qui fait peur ou l'histoire de quelqu'un d'autre sont restés autour de 1 000 vues.
- **Format consigne** : le titre, l'accroche et la 1re phrase donnent un ORDRE qui répond à cet incident (« Ton téléphone est cassé ? Dis ça », « Ton petit orteil ? Bonne nouvelle »), pas une question au spectateur ni un reproche (« Tu fais X ? Arrête ») : l'ordre seul n'a pas suffi, c'est l'incident qui portait la vidéo. « JAMAIS » seulement si l'interdit surprend (raconter son cauchemar : oui ; jurer sur sa mère : non, tout le monde le sait). La 1re phrase doit choquer par l'incident lui-même (la douleur, la perte, la frayeur), en restant exacte et vite corrigée ; la peur du châtiment et l'avertissement vont au milieu, jamais dans l'accroche ni dans le titre.
- **Niveau religieux exact** : « sinon c'est un péché » seulement pour une obligation ou un interdit ; une sunna = « fais ça, tu gagnes… » ; un acte déconseillé = « évite ça ».
- **Les 5 premières secondes décident** (50 % des gens partis à 5 s le 02/11 ; objectif : 70 % encore là). Image 0 vue à la place du spectateur, le sujet en grand qui bouge vers lui, l'ordre avant 4 s, la réponse vers 5 s. Jamais un plan large de persos qui discutent au début. C'est le seul endroit où le sur-mesure vaut son prix.
- **Ensuite** : l'enjeu, une objection ou un malentendu drôle du perso naïf, le texte MONTRÉ au sens propre (concret, jamais des icônes abstraites), un procédé différent à chaque passage, une chute qui redonne la consigne. En duo : Petit vit la situation, Grand donne l'ordre dès la 2e réplique.

## 3. Fabriquer un lot (une commande par étape, dans le dossier du moteur)

1. **Sujets et textes.** Vérifier d'abord dans `references/sujets_faits.md` que le sujet n'a jamais été fait (les vidéos et les scénarios peuvent avoir été supprimés du PC). Proposer (section 6), l'utilisateur choisit. Écrire chaque scénario dans `scenarios\<nom>.txt` avec un en-tête de 3 à 6 lignes de commentaire seulement (les notes longues vont dans la fiche de sources). Écrire en même temps le texte de publication `scenarios\publication\<CODE>.txt` : `TITRE :`, `DESCRIPTION :`, `HASHTAGS :` (règles du skill islamarcade-shorts ; les sources s'y ajoutent toutes seules à la livraison).
2. **Islam : vérifier avant tout le reste.** Charger le skill **islamarcade-shorts** : sa section 0 s'applique sans exception (sens selon les tafsirs, grade des hadiths, numéros sunnah.com vérifiés dans le Chrome de l'utilisateur, Hamidullah mot pour mot, rien d'inventé). Chercher d'abord dans la base (`sources.py cherche`). Écrire une fiche par Short, `sources\fiches\<CODE>.md` (texte exact, grade, date de vérification, décisions), puis `python sources.py`. Sujet de foi, de fiqh ou débattu : relecture par UN agent séparé pour tout le lot, sans le contexte de la rédaction, AVANT les voix. L'outil hadith intégré numérote Mouslim autrement que sunnah.com : ne jamais recopier ses numéros.
3. `python lot.py verifie scenarios\islam_3*.txt` : corriger tout « ! » (durée, balise inconnue, citation sans source…). Depuis le 11/11/2026 il signale aussi, sans planche : une carte ou une liste au texte trop petit (la couper en deux cartes), un titre ou une note réduits, un bandeau `{texte}` trop haut, une maquette au-dessus de 27,5 s (les vraies voix peuvent ajouter 2,5 s : resserrer AVANT les voix ; l'arabe translittéré est compté à part), un hadith hors des deux Sahih sans l'avis d'al-Arna'out ou d'Ahmad Chakir dans la fiche, une réplique mal retrouvée dans la voix. Régler ces « ? » ici évite un tour de planches.
4. `python lot.py planches …` : regarder l'image « … - controle.png » de chaque Short (les 5 premières secondes en détail, puis 1 image / s) : chevauchements, texte coupé ou sous l'interface TikTok, perso hors champ, moment vide. Un détail : `python scenario.py scenarios\x.txt still 12.4 a.png`.
5. **Voix** (payant : seulement quand la mise en scène est validée). `python lot.py voix …` donne le coût et UN fichier de textes ; annoncer le coût (≈ 1 crédit par caractère) et attendre l'accord. Claude génère ensuite avec le connecteur ElevenLabs : P = Lucas `QEZnlKYcLy9N2ierwPEc`, G = Quentin `43TArLZXN5r3L8mJ6AGR`, modèle eleven_v4, une génération par perso et par Short (`generations_count: 1`) : `creative_create_flow`, `creative_generate_speech`, `creative_get_flow_run_status` → `content_url` → `curl` vers le fichier `CODE_PERSO.mp3` indiqué. Puis `python scenario.py … asr` pour chaque Short et de nouveau `lot.py verifie` (30 s avec les vraies voix).
6. `python lot.py rendu …` en arrière-plan (≈ 3 à 4 min par Short depuis le 11/11/2026, rien d'autre de lourd en même temps). Il garde l'ancienne version en `(vN)`, contrôle chaque vidéo (durée, volume −14 LUFS réglé tout seul à 0,5 près, trous de son, passages figés de plus de 4 s) et fait la copie légère (< 10 Mo).
7. Regarder la planche `_qa.png` de chaque vidéo, envoyer la copie légère (SendUserFile), dire ce qui reste imparfait.
8. **Miniature** : `python miniature.py scenarios\<nom>.txt` (en-têtes `MINIATURE:` et `ICONE:`).
9. **Dossier du jour** (règle de l'utilisateur, 09/11/2026) : `python lot.py livre …` pose chaque vidéo finie dans `VIDEO YOUTUBE\SHORTS A PUBLIER\<AAAA-MM-JJ>\`, avec sa couverture et un `.txt` du même nom à côté (titre, description, hashtags, sources). Rien n'y est jamais écrasé. Donner ce dossier dans la réponse finale.
   **Registre (règle de l'utilisateur, 10/11/2026)** : tout de suite après, ajouter une ligne par vidéo finie dans `references/sujets_faits.md` du skill (code, sujet, titre, date). L'utilisateur supprime les vidéos une fois postées : ce registre est la seule mémoire sûre des sujets faits, il se remplit dans la même session, jamais « plus tard ». Quand l'utilisateur dit qu'une vidéo est postée (ou quand Claude la publie), mettre `oui (date)` dans la colonne « Publié ».
10. **Publication** : seulement sur demande explicite, avec les règles des skills islamarcade-shorts / islamarcade-youtube (label IA « Non », jamais de Short dans une playlist, envoi via Chrome, ne jamais appuyer sur Échap dans la fenêtre d'envoi, pas « Histoire fictive » dans les titres).

## 4. Modifier le moteur

- Avant, et après toute grosse modification validée : `python sauve_moteur.py <sujet>` (zip daté dans `VIDEO YOUTUBE\_MOTEUR\`, le plus récent fait foi si le dossier est abîmé).
- Les Shorts **VOP** (`vop06.py`, `vop_suite.py`, `serie.py`, `textes_suite.py`) ne se modifient pas : des Shorts publiés en dépendent. Une nouveauté ne s'active que par un thème ou une balise nouvelle.
- Après toute modification : `python controle_avant_apres.py` (d'anciens Shorts doivent sortir identiques au pixel près) et, si `briques.py` a changé, `python controle_briques.py`. `python controle_moteur.py` (11/11/2026, sans aucune voix : VOP d'origine, démos, Shorts, films ; « OK : N images identiques au pixel près ») remplace `controle_vop.py`, qui ne peut plus tourner depuis que le dossier `SHORTS VALABLE OU PAS\voix` a quitté le Bureau ; `enregistre` seulement après un changement voulu et regardé.
- Une autre session peut modifier le moteur en même temps (films) : ne jamais réécrire un fichier du moteur en entier, seulement des remplacements ciblés, et regarder les dates des fichiers avant de commencer.
- Une nouveauté se montre dans une vidéo démo, puis s'ajoute à `references/catalogue.md`, à `references/balises.md` et au LISEZMOI.
- Supprimer uniquement vers la Corbeille (jamais `rm` sur un fichier de l'utilisateur).
- **Plusieurs ordinateurs (11/11/2026)** : le moteur, ses sons et les skills sont sur le dépôt GitHub `bichop67/moteur-pixel`, PUBLIC depuis le 11/11/2026 à la demande de l'utilisateur (donc : jamais de clé, de mot de passe, d'adresse ni de musique d'un label dans ces dossiers) (le dossier `VIDEO YOUTUBE` est le dépôt ; les vidéos, `FILM`, `SHORTS A PUBLIER` et `_MOTEUR` n'y vont pas). Au début d'une session sur un ordinateur : `powershell -ExecutionPolicy Bypass -File moteur.ps1 recois` ; à la fin d'un lot ou d'une modification du moteur : `… moteur.ps1 envoie` (il range aussi ce skill dans le dépôt, donc le registre des sujets faits). Nouvel ordinateur : une commande dans PowerShell, `irm https://raw.githubusercontent.com/bichop67/moteur-pixel/main/demarre.ps1 | iex` (essayée pour de vrai sur le PC Shadow le 11/11/2026 : « MOTEUR-PIXEL : TERMINE »). Ne jamais piloter le Shadow au clavier depuis le portable (computer use) : la frappe y colle le presse-papiers du Shadow, pas le texte voulu ; donner la commande à l'utilisateur. Aucun chemin `C:/Users/…` en dur dans le code : `pxv.BASE`.

## 5. Avant de livrer

L'utilisateur préfère attendre une vidéo juste. Image de contrôle regardée, aucun passage figé, aucun texte sous l'interface TikTok (haut ≈ 200 px, bas 20 %, droite ≈ 150 px), aucun chevauchement de textes, chaque source affichée sous la phrase qu'elle justifie, contrôles du moteur faits s'il a changé. Check-list complète : `references/pieges.md`. Dire honnêtement ce qui reste imparfait.

## 6. Proposer des idées de vidéos

Partir de `references/resultats.md`. Pour chaque idée : l'incident du quotidien et ses trois questions (oui / non ; dire franchement quand un sujet n'a pas ses trois oui), le titre-consigne (1re phrase = un ordre, avec son niveau religieux : obligatoire, recommandé, interdit ou déconseillé), 3 accroches possibles, le déroulé en 3 à 5 passages avec pour chacun la brique ou l'outil du catalogue, la chute, la durée visée, les sources (déjà dans la base, ou « à vérifier ») et les risques (religieux, faits à vérifier, objet à dessiner). Proposer, ne pas produire : la vidéo se fait quand l'utilisateur en choisit une (sauf en mode autonome, section 7). Les idées gardées pour plus tard vont dans `_MOTEUR_PIXEL\sujets.md`.

## 7. Mode autonome : « fais N Shorts pour aujourd'hui » (règle de l'utilisateur, 09/11/2026)

Quand l'utilisateur demande N Shorts sans autre précision, Claude fait TOUT seul, du choix des sujets aux vidéos finies, sans poser de question ni demander d'accord, et répond une seule fois à la fin. Cette demande vaut accord pour choisir les sujets, dépenser les crédits ElevenLabs des voix et lancer les rendus. Ce qui remplace les questions :

- **Sujets** : `references/sujets_faits.md` du skill (registre des sujets déjà faits : il fait foi, même si les fichiers ont été supprimés ; prochain code = plus grand numéro + 1) et `python lot.py deja` en complément, puis les N premières lignes `à faire` de `_MOTEUR_PIXEL\sujets.md`. S'il en manque, en trouver avec les trois questions de la section 2. Seulement des actes et des invocations sans désaccord connu : jamais une ligne `avec accord`, un sujet de foi, de fiqh débattu ou une polémique.
- **Sources** : la base d'abord, sinon Chrome, comme toujours ; la relecture par UN agent reste obligatoire. Une source introuvable ou faible, ou un doute du relecteur qui ne se règle pas en corrigeant le texte : écarter CE sujet, le noter dans `sujets.md` (`écarté (raison)`) et prendre le suivant. Jamais de texte non vérifié.
- **Image** : briques, outils et animations déjà faites seulement ; aucune animation neuve (au plus un petit `@objet`).
- **Voix** : générées sans annoncer le coût avant. Plafonds : 700 caractères par Short, une seule régénération par voix. Ne jamais acheter de crédits ni changer d'abonnement : si les crédits manquent, livrer en maquette et le dire.
- **Corrections** : deux passes par Short, puis livrer avec le défaut signalé ; écarter le Short s'il est faux sur le fond.
- **Toujours sur demande explicite seulement** : publier, supprimer, modifier le moteur au-delà d'un `@objet`.

Déroulé : la section 3, étapes 1 à 9, d'une traite, jusqu'au dossier du jour. Réponse finale : le dossier du jour, puis pour chaque Short le titre, la durée, la copie légère envoyée, les sources, ce qui reste imparfait (le titre et la description sont dans le `.txt` à côté de la vidéo) ; puis les crédits de voix dépensés et les sujets écartés avec la raison. Mettre à jour `references/sujets_faits.md` du skill (une ligne par Short fini), `sujets.md` (`fait (ISLnn)`) et `stats\cout_lots.md`.

Les fenêtres d'autorisation de l'application (outils, sites) ne dépendent pas de ce skill : si l'une d'elles bloque, continuer ce qui peut l'être et le dire à la fin.
