# ISL28 — « Tu parles dans son dos ? Arrête ! » (la médisance)

Scénario : `scenarios\islam_28_medisance.txt` · module : `explique_0811_medisance.py` (clés `ghiba`, `chair` ; écrit le
08/11, corrigé après la 2e relecture, planche de contrôle refaite) · décor `couloir_ecole` · musique `fond_tension` ·
icône `interdit` · durée estimée **28,0 s** fin comprise · empreinte du texte dit **9479cfdd720729e5** (437 caractères
ElevenLabs : PETIT 111, GRAND 326).
Révisée le 08/11/2026 après la 1re relecture, après la 2e relecture (religieuse + format), puis après la 3e relecture
(contre-vérification) : voir §9.
**Voix** : les voix ISL28 du 08/11 (06:06) ont été faites sur l'ancienne réplique 1 (« Yanis, il pue ! ») et l'ancienne
réplique 3 (« Mais c'est vrai ! ») → **refaire seulement la voix de PETIT** (111 caractères, texte du 08/11 après la 3e
relecture) ; celle de GRAND est inchangée mot pour mot (aucune réplique de GRAND n'a changé, vérifié dans
asr_ISL28.json par la contre-vérification). Ensuite : renommer l'ancien `voix_isl28\ISL28_PETIT.mp3` en « (v1) » sans
le supprimer, relancer `python scenario.py scenarios\islam_28_medisance.txt asr`, vérifier que « Arrête ! » commence
avant ≈ 3 s (avec l'ancienne voix de PETIT, la réplique 1 était étirée jusqu'à 4,09 s et « Arrête ! » tombait à 4,2 s),
puis recaler D_TAPE / T_ENVOI (§8).

## 1. Sources vérifiées (08/11/2026, revérifiées page par page sur sunnah.com après la 2e relecture)

**Coran 49:12** — https://quran.com/fr/49/12 (Hamidullah, identique à l'outil Coran « french »)
« وَلَا يَغْتَب بَّعْضُكُم بَعْضًا ۚ أَيُحِبُّ أَحَدُكُمْ أَن يَأْكُلَ لَحْمَ أَخِيهِ مَيْتًا فَكَرِهْتُمُوهُ ۚ وَٱتَّقُوا۟ ٱللَّهَ ۚ إِنَّ ٱللَّهَ تَوَّابٌ رَّحِيمٌ »
Hamidullah, mot pour mot : « … Et n'espionnez pas; et ne médisez pas les uns des autres. L'un de vous aimerait-il
manger la chair de son frère mort ? (Non !) vous en aurez horreur. Et craignez Allah. Car Allah est Grand Accueillant au
repentir, Très Miséricordieux. » → à l'écran, toujours **« CORAN 49:12 · EXTRAIT »** (comme ISL29).
**Correction du brief** : Hamidullah écrit « (Non !) vous en **aurez** horreur », pas « vous en auriez horreur ».
Sens (Ibn Kathir, Qurtubi) : comparaison (tachbîh) — « comme tu as horreur de manger la chair d'un mort par nature, aie
horreur de la médisance par la religion » (Ibn Kathir) ; « mort » car l'absent ne peut pas se défendre.

**Mouslim 2589** — https://sunnah.com/muslim:2589 (livre 45, hadith 91 ; le chapitre où il se trouve s'intitule
« باب تحريم الغيبة », titre posé par an-Nawawi), Abou Hourayra :
« أَتَدْرُونَ مَا الْغِيبَةُ » . قَالُوا اللَّهُ وَرَسُولُهُ أَعْلَمُ . قَالَ « ذِكْرُكَ أَخَاكَ بِمَا يَكْرَهُ » . قِيلَ أَفَرَأَيْتَ إِنْ كَانَ فِي أَخِي
مَا أَقُولُ قَالَ « إِنْ كَانَ فِيهِ مَا تَقُولُ فَقَدِ اغْتَبْتَهُ وَإِنْ لَمْ يَكُنْ فِيهِ فَقَدْ بَهَتَّهُ »
Traduction : « Savez-vous ce qu'est la médisance ? » Ils dirent : « Allah et Son Messager savent mieux. » Il dit :
« C'est que tu évoques ton frère par ce qu'il déteste. » On lui demanda : « Et si ce que je dis est vraiment en mon
frère ? » Il dit : « Si ce que tu dis est en lui, tu as médit de lui ; et si ce n'est pas en lui, tu l'as calomnié. »
Sahih (Mouslim).

**Abou Dawoud 4878** — https://sunnah.com/abudawud:4878 (livre 43, hadith 106 ; « باب في الغيبة »), Anas ibn Mâlik :
« لَمَّا عُرِجَ بِي مَرَرْتُ بِقَوْمٍ لَهُمْ أَظْفَارٌ مِنْ نُحَاسٍ يَخْمِشُونَ وُجُوهَهُمْ وَصُدُورَهُمْ فَقُلْتُ مَنْ هَؤُلاَءِ يَا جِبْرِيلُ قَالَ
هَؤُلاَءِ الَّذِينَ يَأْكُلُونَ لُحُومَ النَّاسِ وَيَقَعُونَ فِي أَعْرَاضِهِمْ »
Traduction : « Quand je fus élevé au ciel, je suis passé près de gens qui avaient des ongles de cuivre ; ils se
griffaient le visage et la poitrine. J'ai dit : “Qui sont-ils, Jibril ?” Il a dit : “Ce sont ceux qui mangent la chair
des gens et s'attaquent à leur honneur.” » **Grade affiché sur sunnah.com : Sahih (al-Albani).** Abou Dawoud ajoute
(« حَدَّثَنَاهُ يَحْيَى بْنُ عُثْمَانَ عَنْ بَقِيَّةَ لَيْسَ فِيهِ أَنَسٌ ») qu'une autre chaîne (Yahya ibn 'Uthman, de Baqiyya) ne
mentionne pas Anas ; mais juste après, **n° 4879** (https://sunnah.com/abudawud:4879, livre 43, hadith 107), il cite la
transmission d'Abou l-Moughira « كَمَا قَالَ ابْنُ الْمُصَفَّى » (comme Ibn al-Musaffa, donc avec Anas). → « SAHIH
(AL-ALBANI) » à l'écran, la remarque complète dans la description. Le texte ne dit pas « en Enfer » : on ne le dit pas.

**Tirmidhi 1931** — https://sunnah.com/tirmidhi:1931 (livre 27, hadith 37 ; « باب ما جاء في الذب عن عرض المسلم »),
Abou d-Darda' : « مَنْ رَدَّ عَنْ عِرْضِ أَخِيهِ رَدَّ اللَّهُ عَنْ وَجْهِهِ النَّارَ يَوْمَ الْقِيَامَةِ »
Traduction : « Celui qui défend l'honneur de son frère, Allah repousse le Feu de son visage le Jour de la
Résurrection. » At-Tirmidhi : « هَذَا حَدِيثٌ حَسَنٌ » ; sunnah.com : Hasan (Darussalam). C'est une **promesse pour le Jour
de la Résurrection** → dans la voix, futur « Allah protégera ton visage du Feu » (ni dou'a, ni protection immédiate).

**Écouter la médisance** — an-Nawawi, Riyâd as-Sâlihîn, chapitre 255 (https://sunnah.com/riyadussalihin:1528) :
« باب تحريم سماع الغيبة وأمر من سمع غيبة محرمة بردها والإنكار على قائلها فإن عجز أو لم يقبل منه فارق ذلك المجلس إن
أمكنه » : écouter est INTERDIT ; il faut la repousser, sinon quitter l'assemblée si on le peut.

**Exceptions** — an-Nawawi, Riyâd as-Sâlihîn, chapitre 256 « باب ما يباح من الغيبة » (titre vérifié sur
https://sunnah.com/riyadussalihin:1532) : six cas permis par nécessité. Le 1er (التظلم) : « فيجوز للمظلوم أن يتظلم إلى
السلطان والقاضي وغيرهما ممن له ولاية أو قدرة على إنصافه » = la plainte de l'opprimé **auprès de qui a l'autorité ou le
pouvoir de lui rendre justice** (pas « le raconter à tout le monde ») ; puis aide pour faire cesser un mal, demande
d'avis religieux, mise en garde, celui qui affiche son péché, surnom connu. L'introduction du chapitre n'est pas
affichée sur sunnah.com : citée d'après le livre.

**Repentir de la médisance** — Ibn Kathir sur 49:12 (outil tafsir, relu le 08/11 après la 2e relecture) : pour la
majorité, c'est cesser en ayant l'intention de ne pas recommencer ; divergence sur le regret et sur le fait de demander
pardon à la personne ; certains disent de ne pas le lui dire si ça doit la blesser davantage, mais de dire du bien
d'elle dans les assemblées où on a médit et de la défendre autant qu'on peut, en compensation. **Ibn Kathir ne parle pas
de dou'a** (retiré de la description). An-Nawawi (Riyâd as-Sâlihîn, introduction du chapitre du repentir : « وإن كانت
غيبة استحله منها ») en fait une condition (cité d'après le livre).

## 2. Niveau religieux

**Interdit (harâm)** : le Coran l'interdit (49:12, « ne médisez pas »), le chapitre de Mouslim s'intitule
« l'interdiction de la médisance » (titre d'an-Nawawi), et an-Nawawi (al-Adhkâr) comme Ibn Kathir rapportent l'accord
des savants sur l'interdiction. → « Arrête ! » et « péché » sont permis. « **Grand péché** » : al-Qurtubi rapporte qu'il
n'y a pas de divergence pour en faire un grand péché ; d'autres savants l'ont classée autrement → « grand péché selon
beaucoup de savants », seulement dans la description (pas dans la voix).
La médisance compte aussi **par écrit et par signe** (an-Nawawi, al-Adhkâr) : un message dans un groupe en est bien une.
Écouter la médisance sans la refuser est aussi **interdit** (an-Nawawi, Riyâd as-Sâlihîn, ch. 255) : dans la description.

## 3. L'avertissement exact

- « L'un de vous aimerait-il manger la chair de son frère mort ? » (Coran 49:12) : comparaison voulue par Allah.
- Lors de l'ascension, le Prophète ﷺ a vu des gens aux ongles de cuivre qui se griffaient le visage et la poitrine :
  « ceux qui mangent la chair des gens et s'attaquent à leur honneur » (Abou Dawoud 4878, sahih selon al-Albani).
- Même si c'est vrai, c'est de la médisance ; si c'est faux, c'est de la calomnie (Mouslim 2589).
Remède : arrêter, se repentir (description), défendre l'honneur de son frère : Allah repousse le Feu de son visage le
Jour de la Résurrection (Tirmidhi 1931).

## 4. Nuances indispensables

- « Ce qu'il déteste » : son corps, sa religion, son caractère, sa famille, ses habits… (an-Nawawi) ; « vrai » ne
  l'excuse pas, c'est justement la définition.
- Exceptions (§1) : **à l'écran** trois lignes courtes « SE PLAINDRE D'UNE INJUSTICE / À QUI PEUT T'AIDER ? / PERMIS SI
  NÉCESSAIRE (AN-NAWAWI) » (un élève harcelé ou témoin doit comprendre qu'il peut le signaler à un adulte, pas le
  raconter à tout le monde) ; la liste dans la description ; le rappel dans la légende TikTok.
- Repentir : divergence dite dans la description (§1).
- « Tu manges la chair de ton frère mort » (voix) = l'image du verset, sous CORAN 49:12 · EXTRAIT, verset exact à
  l'écran ; gardé par les trois relectures (le hadith lui-même dit « ceux qui mangent la chair des gens »).
- Jibril n'est nommé que sur la carte écrite (jamais dessiné) ; à l'oral Grand donne seulement la réponse.
- **Chaque source sous la phrase qu'elle justifie** : la carte du verset n'est plus à l'écran pendant « Le Prophète ﷺ
  dit : » (nouveau plan, Grand en plan moyen, source MOUSLIM 2589) ; la blague « Je coupe mes ongles ! » est dans son
  propre plan, SANS aucune source (la source d'Abou Dawoud est en tête de la réplique 5 pour ne pas déborder dessus).
- **Pas de prénom** : « le nouveau » ne vise personne (un prénom très courant comme Yanis pouvait servir à se moquer
  de vrais Yanis : la vidéo aurait servi la moquerie qu'elle interdit, Coran 49:11).

## 5. Texte dit (pour la relecture)

| # | Perso | Texte | Plan / source à l'écran |
|---|---|---|---|
| 1 | PETIT | [laughs] Le nouveau *pue* ! | `{ghiba PETIT}` — aucune source (mêmes mots que le message tapé) |
| 2 | GRAND | Arrête ! Tu manges la chair de ton frère *mort* ! | `{ghiba stop}` puis `{chair}`, `{chair cloche}` — CORAN 49:12 · EXTRAIT |
| 3 | PETIT | [annoyed] Ben c'est *vrai* ! (l'OBJECTION du hadith, ton de protestation, pas un « beurk ») | `{chair beurk}` — (« CORAN 49:12 · EXTRAIT » DESSINÉ sous le bandeau du verset) |
| 4 | GRAND | Le Prophète ﷺ dit : si c'est vrai, c'est *ça*, la médisance ! | **nouveau schéma** : plan moyen de Grand pendant le ﷺ, puis `{chair vrai}`, `{chair calomnie}` sur « c'est ça » — MOUSLIM 2589 |
| 5 | GRAND | Il a vu des gens aux ongles de *cuivre* se griffer le visage : ceux qui mangent la chair des gens ! | `{chair ongles}` + ABOU DAWOUD 4878 · SAHIH (AL-ALBANI) **en tête de réplique**, `{chair ceux}` |
| 6 | PETIT | Je coupe mes *ongles* ! | **nouveau schéma** `{chair efface}` — aucune source (la blague) |
| 7 | GRAND | Défends-le : Allah protégera ton *visage* du Feu ! | `{chair defend}` — TIRMIDHI 1931 · HASAN (aussi DESSINÉ sous la carte finale) |

## 6. Spécification visuelle (pour la personne qui dessine)

Règles pour tout le module : mouvements DOUX (glissements, fondus de 0,3 à 0,6 s, apparitions en montée douce), jamais
de secousse, de flash, de zoom brusque ni de coupe sèche. Rien de gore : AUCUNE chair, viande, sang, blessure, visage
griffé, cadavre ni squelette. Aucun prophète, ange (Jibril), Compagnon ni Chaytan dessiné ; Allah jamais représenté ;
jamais d'auréole ni d'anneau de lumière autour d'une tête. Textes à l'écran en MAJUSCULES, dans la zone sûre (rien
d'important au-dessus de y ≈ 200 px, au-dessous de y ≈ 1450 px — les sous-titres sont à y = 1465 — ni à droite de
x ≈ 930 entre y ≈ 840 et 1450). Chaque carte laisse la place de la source en bas du schéma. Les paroles du Prophète ﷺ
sont toujours entre guillemets « … », suivies de « — LE PROPHÈTE (PAIX ET SALUT SUR LUI) ». Aucun prénom nulle part.

### `{ghiba PETIT}` — accroche, image 0 (réplique 1, ≈ 0-1,5 s, puis tenue pendant le début de la réplique 2)
- **Vue à ta place** : TON téléphone en très grand (≈ 80 % de la largeur), tenu par deux mains vues de face (sweat
  rouge de Petit aux poignets), légèrement incliné, qui **monte doucement vers le spectateur** (léger rapprochement
  continu, ≈ 8 % sur 2 s). Fond : le couloir du lycée flou.
- **« Dans son dos » sans lire** : au fond flou du couloir, derrière le téléphone, un garçon **vu de dos** (sac à dos,
  sweat gris) qui s'éloigne doucement sans rien savoir : c'est le nouveau. Étiquette « HORS DU GROUPE ».
- Écran : application de messages, en-tête **« LA CLASSE (SANS LE NOUVEAU) »** (« 27 MEMBRES » retiré : illisible, il
  touchait « LA CLASSE »). Des bulles grises d'autres élèves montent vite une à une : « 😂😂😂 », « MDR LE NOUVEAU »,
  « 😂 », « T'AS VU SES BASKETS 😂 » (pas de 💀) ; petits « ding » doux.
- Le pouce de Petit tape dans la zone de saisie « LE NOUVEAU PUE 🤮 » (lettres une par une en 1,0 s, calées sur « Le
  nouveau pue » ; deux espaces avant l'émoji pour que « PUE » se lise en entier), puis ENVOIE à 1,2 s : la bulle
  verte part (glissé).
- Sur « Arrête ! » (réplique 2, balise `{ghiba stop}`) : la main de Grand (manche verte, gilet) entre doucement par la
  droite en geste STOP devant l'écran ; le téléphone s'immobilise ; panneau doux « STOP » rouge (fondu, pas de flash),
  posé sur les messages moqueurs (420, 630) : il ne cache plus « (SANS LE NOUVEAU) » (vérifié en image, 3e relecture).
- L'en-tête ACCROCHE (« TU PARLES DANS SON DOS ? / ARRÊTE ! ») est au-dessus : le téléphone se décale vers le bas pour
  ne pas le toucher.
- **Couverture du Short et miniature** : jamais « LE NOUVEAU PUE » lisible (prendre une image où le message n'est pas
  encore tapé, ou flouter la zone de saisie).

### `{chair}` — la carte du verset (réplique 2, sur « Tu manges »)
- Carte parchemin vert sombre et or au centre, qui monte doucement : en petit en haut « ALLAH DIT : » ; en grand :
  « … ET NE MÉDISEZ PAS LES UNS DES AUTRES. L'UN DE VOUS AIMERAIT-IL MANGER LA CHAIR DE SON FRÈRE MORT ? (NON !) VOUS
  EN AUREZ HORREUR. » (Hamidullah exact ; « … » au début = extrait). « LA CHAIR DE SON FRÈRE MORT » en jaune. Ne rien
  changer à ce texte.
- Source du moteur : CORAN 49:12 · EXTRAIT. La carte ne doit pas toucher l'ACCROCHE (affichée jusqu'à 3,0 s).

### `{chair cloche}` / `{chair beurk}` — le plat sous cloche (fin de la réplique 2, puis réplique 3 de Petit)
- La carte du verset se réduit et remonte en bandeau (texte toujours lisible, plus petit) ; **sous le bandeau, la
  référence dessinée « CORAN 49:12 · EXTRAIT »** (la réplique 3 n'a pas de source moteur).
- Au centre, une table de cantine, une assiette avec une **cloche argentée froide et FERMÉE** (on ne voit jamais ce qu'il
  y a dessous) ; **pas de vapeur** ; une étiquette posée sur la cloche : « LE NOUVEAU » (écrite en grand, lisible) ;
  au-dessus en grand : **« TU AIMERAIS ? »**.
- Réplique 3 (« Ben c'est vrai ! », dit en protestant, balise `{chair beurk}` en tête) : petit encart du visage de Petit, dégoûté (« BEURK »
  en vert pâle au-dessus de lui), qui repousse le plateau du bout des doigts : la cloche glisse de 40 px vers la
  droite. La cloche ne s'ouvre JAMAIS.

### Réplique 4 — « Le Prophète ﷺ dit : » (nouveau schéma)
- La réplique commence sur la scène (plan moyen de Grand, qui bouge), source MOUSLIM 2589 ; **plus rien du verset à
  l'écran** (sinon le verset paraîtrait sourcé « Mouslim 2589 »). Le tableau n'arrive qu'après « dit : ».

### `{chair vrai}` — « MAIS C'EST VRAI ! » → « = MÉDISANCE » (réplique 4, sur « si c'est vrai »)
- Tableau en deux colonnes, style ping-pong : à gauche une bulle de Petit **« MAIS C'EST VRAI ! »** (rouge) ; une
  flèche douce part vers la droite et dépose **« = MÉDISANCE »** (orange, gros).
- Sous le tableau, en blanc : « LA MÉDISANCE ? « C'EST QUE TU ÉVOQUES TON FRÈRE PAR CE QU'IL DÉTESTE. » » et en petit
  « — LE PROPHÈTE (PAIX ET SALUT SUR LUI) » (y = 712 : ne touche plus « PAR CE QU'IL DÉTESTE »).
- **Exception, dès l'arrivée du tableau**, tout en bas, plus petit, en vert pâle, trois lignes (y = 850) :
  « SE PLAINDRE D'UNE INJUSTICE » / « À QUI PEUT T'AIDER ? » / « PERMIS SI NÉCESSAIRE (AN-NAWAWI) ».

### `{chair calomnie}` — « SINON = CALOMNIE » (réplique 4, sur « c'est ça », montré sans être dit)
- Deuxième ligne du ping-pong : bulle « ET SI C'EST FAUX ? » (gris) → flèche → **« = CALOMNIE »** (rouge foncé, gros),
  glissé doux de 0,3 s. Avancée sur « c'est ça » : lisible ≈ 1,7 s (au lieu de 0,5 s).
- Le tableau reste pendant la pause jusqu'à `{chair ongles}` (en tête de la réplique 5), puis fondu de 0,4 s.

### `{chair ongles}` — les ongles de cuivre (réplique 5, dès « Il a vu »)
- Nuit très sombre (bleu-noir), étoiles fines : bandeau en haut « LORS DE L'ASCENSION (AL-MI'RÂJ), LE PROPHÈTE (PAIX ET
  SALUT SUR LUI) A VU : » qui arrive sur « Il a vu », **en même temps que la source ABOU DAWOUD** (en tête de réplique).
- Au centre, dans l'ombre : **seulement des mains / ongles** — des ongles longs couleur cuivre (reflet qui glisse
  lentement EN CONTINU, petite lueur), qui sortent de manches sombres sans corps visible, levés vers le HAUT et qui
  **s'arrêtent avant tout contact**. AUCUN visage, aucune poitrine, aucune trace, aucun sang.
- Texte : « « … DES GENS QUI AVAIENT DES ONGLES DE CUIVRE ; ILS SE GRIFFAIENT LE VISAGE ET LA POITRINE. » » (blanc),
  « CUIVRE » en couleur cuivre. Fondu vers `{chair ceux}` avant 4 s de plan.

### `{chair ceux}` — la réponse (réplique 5, sur « ceux qui mangent »)
- Les ongles reculent dans l'ombre (fondu) ; « « QUI SONT-ILS, JIBRIL ? » » puis, en grand : **« JIBRIL : « CE SONT
  CEUX QUI MANGENT LA CHAIR DES GENS ET S'ATTAQUENT À LEUR HONNEUR. » »** (« LA CHAIR DES GENS » en jaune). Jibril
  seulement nommé par le texte, jamais dessiné ni représenté par une lumière qui parle.

### `{chair efface}` — Petit efface (réplique 6, **nouveau schéma**, la BLAGUE, sans aucune source)
- Le téléphone revient, plus petit et à droite (échelle 4, x = 420) : le pouce tremble un peu (lent, 2 px) ; la bulle
  « LE NOUVEAU PUE 🤮 » se dissout doucement en poussière grise → « MESSAGE SUPPRIMÉ ».
- À gauche, **sans toucher le téléphone** : Petit (buste agrandi ×10, goutte de sueur) regarde ses deux mains levées
  devant sa poitrine, ongles normaux couleur peau (jamais en cuivre), le coupe-ongles du côté gauche (loin du téléphone).
- **Aucune carte de verset ni de source** sur ce plan (le repentir et 49:12 entier sont dans la description).

### `{chair defend}` — le remède (réplique 7, dernier plan, peut déborder 1,4 s sur « ABONNE-TOI »)
- Le téléphone : le pouce de Petit écrit et envoie **« LAISSEZ LE NOUVEAU TRANQUILLE ✋ »** (bulle verte) ; une bulle
  d'un élève : « OK… 👍 ».
- Encart : Petit apaisé, une lumière douce venue d'en haut et un **bouclier de lumière DEVANT son visage** (plus visible
  après la 2e relecture), **aucun anneau autour de la tête** ; derrière, une lueur orangée (plus nette) qui **recule et
  sort du cadre, sans s'éteindre** ; jamais de flammes sur lui.
- Texte : « « CELUI QUI DÉFEND L'HONNEUR DE SON FRÈRE, ALLAH REPOUSSE LE FEU DE SON VISAGE LE JOUR DE LA
  RÉSURRECTION. » » (« SON VISAGE » en jaune) puis « — LE PROPHÈTE (PAIX ET SALUT SUR LUI) » ; **sous la carte, la
  référence dessinée « TIRMIDHI 1931 · HASAN »**.

Interdits pour TOUT le module : montrer de la chair, de la viande, un corps mort, un visage griffé, du sang ; dessiner
Jibril, le Prophète ﷺ ou un Compagnon ; auréole ; flash, secousse, coupe sèche ; un prénom ; « LE NOUVEAU PUE » sur la
couverture ou la miniature ; une source affichée sous une phrase qu'elle ne justifie pas.

## 7. Publication

**Titre (YouTube et TikTok, 52 caractères)** : Tu parles dans son dos ? ARRÊTE ! Ongles de cuivre 😨

**Description YouTube** :
Allah dit : « … et ne médisez pas les uns des autres. L'un de vous aimerait-il manger la chair de son frère mort ?
(Non !) vous en aurez horreur. Et craignez Allah. Car Allah est Grand Accueillant au repentir, Très Miséricordieux »
(Coran 49:12, traduction Hamidullah, extrait). Le Prophète ﷺ a dit : « Savez-vous ce qu'est la médisance ? » Ils
dirent : « Allah et Son Messager savent mieux. » Il dit : « C'est que tu évoques ton frère par ce qu'il déteste. » On
lui demanda : « Et si ce que je dis est vraiment en mon frère ? » Il dit : « Si ce que tu dis est en lui, tu as médit
de lui ; et si ce n'est pas en lui, tu l'as calomnié » (Mouslim 2589). Il a dit aussi : « Quand je fus élevé au ciel,
je suis passé près de gens qui avaient des ongles de cuivre ; ils se griffaient le visage et la poitrine. J'ai dit :
“Qui sont-ils, Jibril ?” Il a dit : “Ce sont ceux qui mangent la chair des gens et s'attaquent à leur honneur” » (Abou
Dawoud 4878, authentique selon al-Albani ; Abou Dawoud signale une chaîne sans Anas, puis en cite une autre qui confirme
celle avec Anas, n° 4879). Et : « Celui qui défend l'honneur de son frère, Allah repousse le Feu de son visage le Jour
de la Résurrection » (Tirmidhi 1931, hasan selon at-Tirmidhi). La médisance est interdite par l'accord des savants, et
un grand péché selon beaucoup d'entre eux ; elle compte aussi par écrit (un message, une story) et par signe (an-Nawawi,
al-Adhkâr). Rire ou écouter sans rien dire est aussi interdit : défends ton frère, sinon quitte la discussion si tu peux
(an-Nawawi, Riyâd as-Sâlihîn, chapitre de l'interdiction d'écouter la médisance). Quelques cas sont permis par
nécessité, et seulement dans la mesure du besoin : se plaindre d'une injustice auprès de qui peut t'aider, demander de
l'aide pour faire cesser un mal (par exemple signaler un harcèlement à un adulte), demander un avis religieux, mettre
quelqu'un en garde (an-Nawawi, Riyâd as-Sâlihîn, chapitre de ce qui est permis de la médisance). Tu l'as fait ? Arrête,
regrette, demande pardon à Allah et ne recommence pas. Pour beaucoup de savants, tu dois aussi lui demander pardon
(an-Nawawi, Riyâd as-Sâlihîn) ; pour d'autres, ne le lui dis pas si ça doit le blesser davantage : dis du bien de lui
là où tu l'as rabaissé et défends-le (avis rapportés par Ibn Kathir, tafsir de 49:12).

Abonne-toi pour la suite 🕹️
#islam #rappel #hadith #medisance

**Légende TikTok** : Tu parles dans son dos ? ARRÊTE ! Ongles de cuivre 😨 (Te plaindre d'une injustice à qui peut
t'aider : permis.) #islam #rappel #hadith #medisance

## 8. Points à regarder sur la vidéo (planche du module refaite le 08/11 après la 2e relecture)

- Les balises `{ghiba stop}` (réplique 2) et `{chair beurk}` (réplique 3) sont dans le scénario : la main STOP et
  l'encart BEURK doivent apparaître.
- Chronologie : 4 plans (0 → fin de la réplique 3 ; réplique 4 = scène puis tableau ; réplique 5 ; réplique 6-7),
  enchaînés en fondu, sans éclair. Vérifier image par image : **aucune source sous la blague**, aucune carte du verset
  sous « MOUSLIM 2589 ».
- La carte du verset ne touche pas l'ACCROCHE (jusqu'à 3,0 s) ; la cloche reste fermée, sans vapeur ; les ongles ne
  touchent rien ; aucune lumière « qui parle » pour Jibril ; bouclier devant le visage, jamais d'auréole.
- Réplique 4 : le plan moyen de Grand pendant le ﷺ (≈ 3 s) doit bouger ; réplique 5 : reflet du cuivre en continu et
  fondu vers la réponse avant 4 s (attend_figes.py / controle_video.py).
- Le typage « LE NOUVEAU PUE » (1,0 s, envoi à 1,2 s) est calé sur l'estimation : le recaler sur la vraie voix de PETIT
  (D_TAPE / T_ENVOI dans le module) si l'envoi tombe après « Arrête ! ».
- Durée à remesurer avec les vraies voix (estimation 28,0 s ; l'ancienne version mesurait ≈ 23,9 s). Seulement s'il
  reste de la place (vraies voix < 27,5 s) : « [amused] Non… » en tête de la réplique 7 (+0,4 s, voix de GRAND à
  refaire alors).

## 9. Décisions de relecture (08/11/2026)

1re relecture :
- Plus de `{source "CORAN 49:12"}` ni de carte du repentir sous « Je coupe mes ongles ! » ; variante « Repens-toi… »
  écartée (29,5 s estimées).
- « CORAN 49:12 · EXTRAIT » partout ; références dessinées dans les cartes (bandeau du verset, carte finale).
- « protège » → « protégera » (promesse du Jour de la Résurrection) ; « a dit » → « dit ».
- Exception à l'écran + légende TikTok ; divergence sur le repentir et écoute de la médisance dans la description.
- Bouclier devant le visage au lieu du halo ; lueur qui recule sans s'éteindre ; cloche froide sans vapeur ; paroles
  du Prophète ﷺ entre guillemets ; réponse attribuée à Jibril ; titre du chapitre de Mouslim attribué à an-Nawawi.
- Format : accroche « TU PARLES DANS SON DOS ? / ARRÊTE ! » (TITRE: « Tu parles dans son dos arrete ») ; titre avec la
  peur du hadith ; garçon vu de dos à l'image 0.

2e relecture (religieuse + format ; sources revérifiées sur sunnah.com : abudawud:4878 et 4879, muslim:2589,
tirmidhi:1931, riyadussalihin:1528 et 1532 ; tafsir d'Ibn Kathir sur 49:12 relu) :
- **Attribution à l'écran** : « nouveau schéma » sur les répliques 4 et 6 ; source d'Abou Dawoud en tête de la
  réplique 5 ; `{chair calomnie}` avancé sur « c'est ça » (même hadith).
- `{ghiba stop}` et `{chair beurk}` ajoutés (ils manquaient : la main STOP et l'encart BEURK n'apparaissaient jamais).
- Exception précisée comme an-Nawawi : « À QUI PEUT T'AIDER ? ».
- **Prénom Yanis remplacé par « le nouveau »** (voix, écran du module, cloche, messages) ; pour garder 28,0 s estimées,
  réplique 3 « Mais c'est vrai ! » → « C'est vrai ! » (la bulle du tableau garde « MAIS C'EST VRAI ! »). Seule la voix
  de PETIT est à refaire. Empreinte 13676b2b83355e21 → dbc217984069f367.
- Description : « fais des dou'as pour lui » retiré (Ibn Kathir ne le dit pas) ; écouter la médisance « aussi
  interdit… si tu peux » ; remarque sur Abou Dawoud complétée par le n° 4879.
- Module : « PUE » lisible (deux espaces avant l'émoji) ; « 27 MEMBRES » retiré ; « — LE PROPHÈTE » à y = 712 et
  exception à y = 850 ; plan de la blague recomposé (téléphone ×4 à droite, Petit ×10 à gauche, mains devant la
  poitrine, coupe-ongles loin du téléphone) ; bouclier et lueur du Feu plus visibles ; étiquette de la cloche écrite
  en grand.
- Non retenu : « C'est manger la chair de ton frère mort ! » (aucune marge de durée ; le texte actuel n'est pas une
  erreur : c'est l'image du verset, verset exact à l'écran).

3e relecture (contre-vérification indépendante ; muslim:2589 relu page par page sur sunnah.com : livre 45, hadith 91,
chapitre « باب تحريم الغيبة », objection « قِيلَ أَفَرَأَيْتَ إِنْ كَانَ فِي أَخِي مَا أَقُولُ ») :
- **Réplique 3 (importante, format)** : « [disgusted] C'est vrai ! », dit pendant « TU AIMERAIS ? » et l'encart BEURK,
  s'entendait comme un accord (« beurk, c'est vrai ») et non comme l'objection du hadith à laquelle répond « si c'est
  vrai… ». → **« [annoyed] Ben c'est *vrai* ! »** (protestation nette ; [annoyed] déjà utilisé dans ISL13 pour Petit).
  « Mais c'est vrai ! » (variante proposée) aurait donné 28,3 s estimées (> 28 s) ; pour garder **28,0 s**, réplique 1
  « Le nouveau, il pue ! » → **« Le nouveau *pue* ! »** (-4 signes ; mêmes mots que le message tapé « LE NOUVEAU PUE »)
  et « Ben » (+4). La bulle du tableau garde « MAIS C'EST VRAI ! » (résumé écrit de l'objection, sens identique).
  Empreinte dbc217984069f367 → **9479cfdd720729e5** ; PETIT 113 → 111 caractères ; GRAND inchangé mot pour mot.
- **Voix de PETIT (mineure, fabrication)** : l'ancienne voix (« Yanis, il pue ! / Mais c'est vrai ! ») étirait la
  réplique 1 jusqu'à 4,09 s (« Arrête ! » à 4,2 s). Marche à suivre en tête de fiche (renommer en « (v1) », relancer
  asr, « Arrête ! » avant ≈ 3 s, recaler D_TAPE / T_ENVOI).
- **Panneau STOP (mineure, image)** : il cachait « (SANS LE NOUVEAU) » ≈ 0,4 s → descendu sur les messages
  (`_colle(im, pk, 420, 630, ep_)` dans `_img_tel`) ; image vérifiée à 0,7 et 1,2 s après « Arrête ! » : l'en-tête
  « LA CLASSE (SANS LE NOUVEAU) » reste lisible, le panneau couvre la bulle moqueuse « T'AS VU SES BASKETS ».
- Rien de religieux à corriger (le contre-vérificateur non plus) : sources, niveau religieux et images inchangés.
