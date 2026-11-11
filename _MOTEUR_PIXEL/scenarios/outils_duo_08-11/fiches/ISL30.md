# ISL30 — « Tu lis ton horoscope ? ARRÊTE ! » (devins, voyants, tarot, horoscope)

Scénario : `_MOTEUR_PIXEL\scenarios\islam_30_horoscope.txt` · module de dessin : `_MOTEUR_PIXEL\explique_0811_horoscope.py`
(clés `astro`, `quarante` ; sous-clé `quarante repens` ajoutée à la 2e relecture) · durée estimée par `textes_voix.py` :
**27,6 s fin comprise** · empreinte du texte dit : **999da9e450185305** (remplace 438b8a897aa69ad1 puis 7f71796b7fd28fc0) ·
456 caractères (≈ 456 crédits ElevenLabs) · 8 répliques · décor `chambre_ado` · musique `fond_mystere`.

### Contre-vérification indépendante (08/11/2026) — corrections appliquées (texte dit inchangé)
Revérifié moi-même : sunnah.com muslim:2230 (texte et chapitre « تحريم الكهانة » conformes) et abudawud:3905
(« … زَادَ مَا زَادَ », Hasan, al-Albani), dans mon propre onglet du navigateur intégré, fermé ensuite ; Hamidullah 27:65 et
42:25 (`get_quran_verse`, french) : extraits affichés exacts ; islamweb 234760 relu : Dar al-Ifta n° 16019
« أما مجرد القراءة للتلهي فهو مكروه », et n° 3671 « عامة المسلمين … لا يجوز لهم … النظر في كتب العرافين وأهل التنجيم ».
- **Important — référence coranique** : « Je supprime ! » n'avait pas de `{source}`, donc l'étiquette « CORAN 27:65 »
  restait sous la citation de 42:25 (≈ 0,45 s). → `{source "CORAN 42:25"}` ajoutée sur « Je supprime ! » (une source
  s'affiche dès le début de sa réplique : scenario.py, ligne 1009). « Et repens-toi ! » garde la même source. Ajout de ma
  part : le parchemin 27:65 et « TON SIGNE : MUSULMAN » s'effacent en 0,3 s au lieu de 0,4 s (`_scene_avenir`), pour être
  partis quand l'étiquette passe à 42:25 (fondu 0,25 s) et avant l'entrée de « REPENS-TOI » (même zone en haut).
  Remarque : dans un schéma, deux `{source}` identiques de suite font un léger creux d'opacité (≈ 65 % pendant ≈ 0,3 s,
  explique.py ne fusionne pas les doublons) ; pas un clignotement, à regarder sur la planche.
- **Moyen — « ABONNE-TOI » sur la citation** : `T_REPENS_OUT` 1,5 → **0,6** (fondu fini à « repens » + 0,95 s) ;
  « REPENS-TOI » entre à + 0,25 s (fondu 0,4 s) et la citation à + 0,35 s (au lieu de 0,5 et 0,65) : lisible ≈ 1,2 s
  sous « CORAN 42:25 ». Si la vraie voix de « Et repens-toi ! » dépasse 1,1 s, prendre `T_REPENS_OUT` = durée − 0,35 s.
- **Mineur — hadith sans numéro** : réplique 4 → `{source "MOUSLIM 2230 · AN-NAWAWI, CHARH MOUSLIM"}` (la carte du hadith
  reste à l'écran pendant les répliques 4 et 5).
- **Mineur — description** : « une fatwa de Dar al-Ifta d'Égypte juge la simple lecture… makrouh » (une autre, n° 3671,
  l'interdit aux gens du commun) ; Abou Dawoud 3905 cité en entier (« … : plus il en prend, plus il en prend »), et
  « (l'astrologie) » sorti des guillemets (ce n'était pas dans le hadith).
- **Rétention 3-6 s** : aucun changement (conforme à balises.md « schéma après « a dit : » ») ; remesurer avec
  `controle_video.py` après les voix (aucun passage figé > 4 s).
- **Voix** : les MP3 de `voix_isl30` (06:06) viennent d'un texte plus ancien (GRAND n'a que 3 répliques) : **refaire au
  moins GRAND** avant toute planche ou tout rendu (sinon kit.dialogue les charge et cale mal les répliques).

### Décisions de la 2e relecture (religion + format, 08/11/2026)
- Réplique 2 : `(stop, plan moyen, nouveau schéma)` : sans « nouveau schéma », `{astro}` restait figé ≈ 4 s sous « Arrête !
  Le Prophète ﷺ a dit : ». On voit maintenant Grand faire « stop » et la caméra s'approcher pendant le ﷺ ; `{quarante}`
  arrive après « a dit : » (balises.md : « schéma après « a dit : » », comme islam_16_enfer ; testé sur planche par la
  relecture religieuse). La proposition format (`{quarante}` juste après « Arrête ! ») n'est **pas** retenue : grand schéma
  figé pendant le ﷺ.
- Fin : `{source "CORAN 42:25"}` n'est plus sous « Je supprime ! » ; nouvelle réplique courte de Grand
  « Et *repens-toi* ! » avec la source. `{quarante repens}` efface « REPENS-TOI » et la citation 1,5 s après le début de la
  réplique (fondu 0,35 s), pour qu'ils ne se mêlent jamais à « ABONNE-TOI POUR LA SUITE ».
- Réplique 6 : `[amused]` seulement sur « Musulman ! », `[calm]` sur « Ton avenir, Allah seul le connaît. ».
- Module : sous « 40 NUITS », « (= 40 JOURS DE PRIÈRES) » ; à `{quarante prie}`, le bandeau vert se pose à y = 650, à la
  place du compteur « RÉCOMPENSE : 0 » qui s'efface dessous (il le cachait à moitié, et le bandeau cachait la 4e rangée
  de lunes) ; boîte « SUPPRIMER ? » : T_DIALOGUE 0,2 · T_OUI 0,6 · T_JETTE 1,0 (« OUI ✓ » lisible ≈ 0,4 s).
- Gardés : « Mon horoscope : je serai riche ! » (le téléphone, sujet en grand qui bouge, reste sous toute l'accroche) ;
  « Je supprime ! » sans ajout (sinon > 28 s) ; le compteur reste sans mention « (SENS : AN-NAWAWI) » (an-Nawawi est
  nommé à l'écran quelques secondes plus tard, à `{quarante prie}`).
- Titre plus inquiétant, fidèle au hadith : « Ta prière, 40 nuits… » (jamais « perdue » ni « refusée »).

## 0. Corrections apportées au brief

1. **Abou Dawoud 3904 ne dit PAS « a mécru »** : son texte est « فَقَدْ بَرِئَ مِمَّا أَنْزَلَ اللَّهُ عَلَى مُحَمَّدٍ » (« il s'est
   désavoué de ce qu'Allah a fait descendre sur Mouhammad ») ; « فَصَدَّقَهُ بِمَا يَقُولُ » (« et le croit ») n'est que dans la
   version de Moussa ibn Isma'il. Le mot « كَفَرَ » (« a mécru ») est dans **Tirmidhi 135** (même chaîne), SANS « et le
   croit ». Le hadith joint aussi deux autres actes (rapport pendant les règles, par voie anale).
2. **Son authenticité est discutée** : sahih selon al-Albani (AD 3904), hasan selon Darussalam (Tirmidhi 135), mais
   at-Tirmidhi écrit : « وَضَعَّفَ مُحَمَّدٌ هَذَا الْحَدِيثَ مِنْ قِبَلِ إِسْنَادِهِ » (al-Boukhari a jugé sa chaîne faible) ; et
   « مَعْنَى هَذَا عِنْدَ أَهْلِ الْعِلْمِ عَلَى التَّغْلِيظِ » (sens de menace sévère selon les savants). → **Retiré du texte dit** ;
   il reste dans la description avec son grade discuté. « Y croire » est traité dans la vidéo par le **Coran 27:65**
   (certain) : le parchemin « QUI CONNAÎT TON AVENIR ? » + le verset.
3. **Abou Dawoud 3905** (astrologie = branche de magie) : bon (hasan, al-Albani ; Ibn Majah 3726 hasan, Darussalam) →
   description seulement.
4. **Horoscope = divination** : Comité permanent (Fatawa al-Lajna ad-Dâ'ima **1/203**, tel que cité sur islamqa.info
   n° 336588, relu le 08/11/2026 ; signé Bakr Abou Zayd, 'Abd al-'Aziz Âl ach-Cheikh, al-Fawzan, Ibn Ghoudayyan, Ibn Baz) :
   « (أبراج الحظ) يحرم نشرها، والنظر فيها، وترويجها بين الناس، ولا يجوز تصديقهم، بل هو من شعب الكفر » (il est interdit de les
   publier, de les regarder et de les diffuser ; y croire est une branche de mécréance). Ce texte **ne cite pas les 40
   nuits**. islamqa 336588 conclut seulement : « قراءة كلام الكهان والعرافين محرم، وهو قريب من سؤالهم » (lire = interdit, et
   PROCHE de les interroger). En revanche islamqa 147232 (relu le 08/11/2026) dit que celui qui lit l'horoscope « for fun »
   pèche et qu'« Allah will not accept any prayer from him for forty days ». → Appliquer les 40 nuits à la simple lecture
   = **avis de nombreux savants, pas unanime** : à l'écran « (SELON DE NOMBREUX SAVANTS) », nuance dans la description.
   Ibn Taymiyya **rapporte** (« qad qîla », « on a dit ») que 'arrâf englobe le devin (kâhin), l'astrologue (mounajjim),
   le géomancien… (**réf. à revérifier** : Majmou' al-Fatawa 35/173 selon alsunna.net ; dorar.net donne d'autres
   renvois) → ni ce numéro ni « Ibn Taymiyya dit » nulle part avant vérification. Avis plus souple chez quelques
   savants : **Dar al-Ifta d'Égypte, fatwa n° 16019 du 17/03/2011** (citée par islamweb n° 234760) : « أما مجرد القراءة
   للتلهي فهو مكروه » (la simple lecture pour s'amuser, sans y croire, est **déconseillée, makrouh**) ; mais une autre fatwa
   de Dar al-Ifta (n° 3671, 11/02/2009, même page) l'**interdit** aux gens du commun. Signalé dans la description.
   **Preuves de « selon de nombreux savants »** (relues le 08/11/2026) :
   - islamweb n° 408259 (02/12/2019) : « فلا تجوز قراءة الأبراج لمعرفة الصفات الشخصية، ولا غيرها، وهذا يدخل في حكم إتيان
     العرافين وسؤالهم » ; et « عدم قبول الصلاة … ليس معناه بطلانها، أو وجوب إعادتها، وإنما معناه عدم ثوابها » ;
   - islamweb n° 234760 (02/01/2014) : « قراءة الأبراج دون اعتقاد فيها فهو كسؤال الكهان دون تصديق » ; y sont cités :
     **Ibn 'Uthaymin** (al-Qawl al-moufid : la simple interrogation du 'arrâf est interdite, « فإثبات العقوبة على سؤاله يدل
     على تحريمه »), **al-Fawzan** (I'ânat al-moustafid : les 40 jours pour la simple venue, même sans y croire ; « ولا ثواب له
     عند الله فيها، وإن كان لا يؤمر بالإعادة » ; version « أربعين يوماً وليلة ») ;
   - islamqa n° 147232 (lecture « pour s'amuser » : 40 jours) ;
   - avis divergent : **al-Qari** (Mirqât) : « فسأله عن شيء أي على وجه التصديق » (seulement s'il le croit), et Dar al-Ifta
     16019 ci-dessus.
   → « (SELON DE NOMBREUX SAVANTS) » reste à l'écran.

## 1. Sources vérifiées sur sunnah.com (navigateur intégré, 08/11/2026 ; Mouslim 2230, Mouslim 537a, Abou Dawoud 3904 et 3905 relus une 2e fois page par page à la 2e relecture)

| Réf. | URL | Arabe (extrait exact) | Traduction fidèle | Narrateur | Grade |
|---|---|---|---|---|---|
| Mouslim 2230 | https://sunnah.com/muslim:2230 | « مَنْ أَتَى عَرَّافًا فَسَأَلَهُ عَنْ شَىْءٍ لَمْ تُقْبَلْ لَهُ صَلاَةٌ أَرْبَعِينَ لَيْلَةً » — chapitre : « بَابُ تَحْرِيمِ الْكِهَانَةِ وَإِتْيَانِ الْكُهَّانِ » | « Celui qui va voir un devin ('arrâf) et l'interroge sur quelque chose, aucune prière ne lui est acceptée pendant quarante nuits. » Chapitre : « Interdiction de la divination et d'aller voir les devins » | Safiyya (bint Abi 'Oubayd), d'une des épouses du Prophète ﷺ | Sahih (Mouslim) |
| Mouslim 537a | https://sunnah.com/muslim:537a | « وَإِنَّ مِنَّا رِجَالاً يَأْتُونَ الْكُهَّانَ . قَالَ « فَلاَ تَأْتِهِمْ » » | « Parmi nous, des hommes vont voir les devins. » Il dit : « Ne va pas les voir. » | Mou'awiya ibn al-Hakam as-Soulami | Sahih (Mouslim) |
| Abou Dawoud 3904 (description seulement) | https://sunnah.com/abudawud:3904 | « مَنْ أَتَى كَاهِنًا » — قَالَ مُوسَى : « فَصَدَّقَهُ بِمَا يَقُولُ » — « … فَقَدْ بَرِئَ مِمَّا أَنْزَلَ اللَّهُ عَلَى مُحَمَّدٍ » | « Celui qui va voir un devin (kâhin) — et le croit dans ce qu'il dit (version de Moussa) — … s'est désavoué de ce qu'Allah a fait descendre sur Mouhammad. » | Abou Hourayra | Sahih (al-Albani), chaîne critiquée par al-Boukhari (cf. Tirmidhi 135) → **discuté** |
| Tirmidhi 135 (description seulement) | https://sunnah.com/tirmidhi:135 | « مَنْ أَتَى حَائِضًا أَوِ امْرَأَةً فِي دُبُرِهَا أَوْ كَاهِنًا فَقَدْ كَفَرَ بِمَا أُنْزِلَ عَلَى مُحَمَّدٍ » + « وَضَعَّفَ مُحَمَّدٌ هَذَا الْحَدِيثَ مِنْ قِبَلِ إِسْنَادِهِ » | « … ou va voir un devin, a mécru en ce qui a été révélé à Mouhammad. » At-Tirmidhi : al-Boukhari l'a jugé faible par sa chaîne ; les savants le comprennent comme une menace sévère. | Abou Hourayra | Hasan (Darussalam) ; faible selon al-Boukhari → **discuté** |
| Abou Dawoud 3905 (description seulement) | https://sunnah.com/abudawud:3905 | « قَالَ رَسُولُ اللَّهِ صلى الله عليه وسلم مَنِ اقْتَبَسَ عِلْمًا مِنَ النُّجُومِ اقْتَبَسَ شُعْبَةً مِنَ السِّحْرِ زَادَ مَا زَادَ » (chapitre « بَابٌ فِي النُّجُومِ ») | « Celui qui puise une science dans les étoiles puise une branche de la magie : plus il en prend, plus il en prend. » | Ibn 'Abbas | Hasan (al-Albani) — revu le 08/11/2026 |
| Ibn Majah 3726 (même texte) | https://sunnah.com/ibnmajah:3726 | idem | idem | Ibn 'Abbas | Hasan (Darussalam) |

Versets (Hamidullah, outil `get_quran_verse` en « french », revus le 08/11/2026) :
- **Coran 27:65** (à l'écran, EXTRAIT) : « Dis : "Nul de ceux qui sont dans les cieux et sur la Terre ne connaît
  l'Inconnaissable, à part Allah." Et ils ne savent pas quand ils seront ressuscités ! » → affiché : « NUL DE CEUX QUI
  SONT DANS LES CIEUX ET SUR LA TERRE NE CONNAÎT L'INCONNAISSABLE, À PART ALLAH. »
- **Coran 42:25** (à l'écran à la fin, EXTRAIT, et description) : « Et c'est Lui qui agrée de Ses serviteurs le
  repentir, pardonne les méfaits et sait ce que vous faites. » → affiché : « C'EST LUI QUI AGRÉE DE SES SERVITEURS LE
  REPENTIR ».

Commentaire (relu sur shamela.ws, al-Arba'oun al-'aqadiyya 1/93, https://shamela.ws/book/192/83, qui cite an-Nawawi,
Charh Mouslim sur le hadith 2230) : « وأما عدم قبول صلاته فمعناه أنه لا ثواب له فيها، وإن كانت مُجْزئة في سقوط الفرض عنه، ولا
يحتاج معها إلى إعادة … فإن العلماء متفقون على أنه لا يلزم من أتى العرَّاف إعادةُ صلواتِ أربعينَ ليلةً ».

Fatwas (relues le 08/11/2026) : https://www.islamweb.net/ar/fatwa/408259/ · https://www.islamweb.net/ar/fatwa/234760/
(Dar al-Ifta d'Égypte 16019 et 3671, Ibn 'Uthaymin, al-Fawzan, al-Qari, al-Khatib al-Baghdadi : astronomie permise —
qibla, heures de prière — et astrologie interdite) · islamqa.info n° 147232 et 336588.

## 2. Sens selon les commentaires

- **'arrâf / kâhin** : celui qui prétend connaître l'inconnu (l'avenir, les choses cachées). Ibn Taymiyya rapporte
  (« qad qîla ») que 'arrâf englobe l'astrologue (réf. à revérifier). L'horoscope = un astrologue qui annonce ton
  avenir → **selon de nombreux savants**, le lire revient à interroger le devin (islamqa 147232) ; pour d'autres, c'est
  interdit et « proche » de l'interroger (islamqa 336588).
- **« Aucune prière ne lui est acceptée quarante nuits »** : an-Nawawi : pas de récompense pour ces prières, mais elles
  sont valables, l'obligation est acquittée, on ne les refait pas, et les savants sont d'accord là-dessus. → Grand :
  « Tu dois quand même prier ! » (OBLIGATOIRE dans le Short : sinon on pousserait à abandonner la prière, péché bien
  plus grave). « Quarante nuits » = quarante jours de prières (les Arabes comptent par les nuits ; al-Fawzan cite
  « أربعين يوماً وليلة ») → « (= 40 JOURS DE PRIÈRES) » sous « 40 NUITS ».
- **Étoiles** : al-Khatib al-Baghdadi (cité par islamweb 234760) distingue la science des astres permise (orientation,
  qibla, heures de prière) de l'astrologie (prédire l'avenir) : AD 3905 vise l'astrologie → « (l'astrologie) » dans la
  description. Continuer à prier ne fait **pas** revenir la récompense
  de ces 40 nuits (aucun texte ne le dit) → le tapis reste gris à l'image.
- **Deux cas** (Ibn Hajar, Fath al-Bari 10/217, d'après al-Qourtoubi, cité de seconde main par hadithprophet.com) :
  interroger sans croire (Mouslim 2230) et croire le devin (AD 3904, plus grave). Al-Khattabi : la mécréance tient à
  croire que le devin partage la science de l'inconnu d'Allah. Rien de cela n'est dit en voix (« Même pour rigoler »
  écarté : il faudrait une source à l'écran).

## 3. Niveau religieux de la consigne

- **Interdit** : aller voir / consulter un devin, voyant, tarot ; lire, regarder et diffuser les horoscopes (chapitre de
  Mouslim « تحريم », Mouslim 537 « ne va pas les voir », Comité permanent 1/203). → « Arrête ! » permis ; « péché » non
  dit (la menace du texte suffit), mais il serait permis.
- **Les 40 nuits pour la simple lecture** : avis de nombreux savants, pas unanime → « SELON DE NOMBREUX SAVANTS » écrit.
- **Y croire** : plus grave (branche de mécréance selon le Comité permanent ; contraire à 27:65). Jamais « tu es
  mécréant » ni « l'Enfer » dans le Short.
- **La prière reste obligatoire** pendant les 40 nuits (an-Nawawi).
- **Remède** : arrêter, supprimer l'appli, se repentir (Coran 42:25, à l'écran et dans la description ; islamqa 336588 :
  « فتوبي إلى الله واستغفريه، ولا تعودي لمثله أبدا », sans refaire les prières), continuer à prier.

## 4. L'avertissement exact (dit dans la vidéo)

GRAND : « Arrête ! Le Prophète ﷺ a dit : qui interroge un devin, sa prière n'est pas acceptée quarante nuits. » —
source à l'écran **MOUSLIM 2230** ; condensé de « celui qui va voir un devin et l'interroge sur quelque chose » : la
carte à l'écran donne le texte complet et fidèle (« AUCUNE PRIÈRE NE LUI EST ACCEPTÉE ») ; le lien avec l'horoscope est
ÉCRIT (« LIRE TON HOROSCOPE = INTERROGER UN DEVIN (SELON DE NOMBREUX SAVANTS) »), pas dit.
GRAND : « Non ! Tu dois quand même prier ! » — source **MOUSLIM 2230 · AN-NAWAWI, CHARH MOUSLIM** (la carte du hadith
est encore à l'écran ; la phrase est l'explication d'an-Nawawi, pas une parole du Prophète ﷺ).
GRAND : « Musulman ! Ton avenir, Allah seul le connaît. » — phrase de Grand appuyée sur **CORAN 27:65**, dont l'extrait
exact s'affiche (`[amused]` sur « Musulman ! » seulement, `[calm]` sur la phrase de foi).
PETIT : « Je supprime ! » — source **CORAN 42:25** (contre-vérification) ; l'appli part à la corbeille ; « REPENS-TOI : »
et l'extrait de 42:25 apparaissent (+ 0,25 / + 0,35 s), sous l'étiquette 42:25.
GRAND : « Et repens-toi ! » — source **CORAN 42:25** (sous la phrase qu'elle justifie) ; le texte se lit seul sous sa voix.

## 5. Spécification visuelle (pour le dessin de `explique_0811_horoscope.py`)

Sous-clés réellement utilisées : `astro` ; `quarante`, `quarante lunes`, `quarante arrete`, `quarante prie`,
`quarante avenir`, `quarante supprime`, `quarante repens` (plus de `{quarante rigole}` ni de réplique « Pour rigoler »).

Règles communes : pixel art du moteur ; **mouvements doux seulement** (glissés, fondus 0,3-0,5 s, échelles lentes ;
jamais de secousse, de flash, de coupe sèche, de clignotement rapide) ; **jamais** le Prophète ﷺ, un ange, un
Compagnon, un djinn, le Chaytan ni un « voyant » / sorcier / devin dessiné (ni main, ni silhouette, ni yeux dans la boule) ;
Allah jamais représenté ; pas de signe ésotérique mis en valeur (pas de pentagramme, d'œil, de main de Fatma) ; rien de
gore. Textes en MAJUSCULES, police du moteur, hors zones interdites (haut 200 px, bas 20 %, droite 150 px sous
840 px). Timings indicatifs (estimation, à recaler sur les vraies voix) : réplique 1 ≈ 0-2,6 s · 2 ≈ 2,9-12 s
(« Arrête ! » ≈ 2,9 s, PLAN MOYEN « nouveau schéma » : Grand main levée, la caméra s'approche pendant le ﷺ ; {quarante}
≈ 7 s après « a dit : », menace ≈ 8,8-11,9 s) · 3 ≈ 12,3-14,4 s · 4 ≈ 14,7-16,9 s · 5 ≈ 17,2-18,4 s · 6 ≈ 18,7-21,9 s ·
7 ≈ 22,2-23,3 s · 8 (« Et repens-toi ! ») ≈ 23,6-24,6 s · fin 1,4 s → ≈ 27,6 s. Rien de figé plus de 4 s (pendant la
longue réplique 2, le plan moyen puis la carte et les lunes avancent sans arrêt).

### `{astro PETIT}` — accroche, image 0 (pendant « Mon horoscope : je serai riche ! », ≈ 2,6 s, sous l'ACCROCHE)
- **Vue à ta place** (comme `{sms}` / `{porte}`) : chambre d'ado le soir (lampe chaude, fond `chambre_ado` flou), deux
  mains (manches de sweat ROUGE = Petit) tiennent un téléphone qui MONTE vers le spectateur (échelle 80 % → 100 % en
  1,2 s, très doux), il occupe ≈ 60 % de la hauteur sous l'accroche. **Tout le mouvement va au téléphone.**
- Écran du téléphone : appli violet nuit avec étoiles ; en-tête « TON HOROSCOPE DU JOUR » avec un petit logo rond
  (étoile ou ♈ dessiné en pixels, comme simple logo d'appli) ; carte qui défile lentement vers le haut (comme
  `{defile}`) : « TON HOROSCOPE : » puis « TU SERAS RICHE ! 💰 » (sac d'argent pixel). **Aucun signe réel nommé**
  (pas de « BÉLIER », pas d'étoiles de « CHANCE » : on ne publie la prédiction de personne). Un petit « ❤ 12 K » à côté.
- Sur le bureau, devant, **petits et flous** au premier plan : une **carte de tarot** retournée (dos violet à étoiles,
  aucune figure) et une petite **boule de cristal** bleutée sur socle, avec un **reflet FIXE** (pas de rotation ; aucun
  visage, aucune forme dedans).
- L'accroche « TU LIS TON HOROSCOPE ? / ARRÊTE ! » en haut ; le dessin est décalé sous l'accroche. À ≈ 2,6 s (« Arrête ! »
  de Grand) : la scène redevient le plan moyen (Grand fait « stop ») — assuré par « nouveau schéma » sur la réplique 2.

### `{quarante}` — mise en place (sur « qui interroge un devin », ≈ 7,2 s)
- Ciel de nuit bleu profond, étoiles fixes discrètes ; en bas au centre, un **tapis de prière** vert et or vu de
  trois quarts (vide, personne dessus), orienté vers le haut. Au-dessus du tapis, un petit compteur doré
  « RÉCOMPENSE : 0 ».
- Au-dessus, **40 petits croissants de lune** gris foncé (contour gris clair), en arc ou en grille de 5 × 8, identiques.
- Carte de texte en haut (bandeau sombre, texte blanc) : petite ligne « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : » puis
  « « CELUI QUI VA VOIR UN DEVIN ET L'INTERROGE SUR QUELQUE CHOSE… » ».
- Juste sous la carte, **en blanc, assez gros et lisible** : « LIRE TON HOROSCOPE = INTERROGER UN DEVIN » et dessous,
  plus petit : « (SELON DE NOMBREUX SAVANTS) ». Cette ligne **reste affichée pendant toute la réplique** (elle ne
  s'efface pas à `{quarante lunes}`).
- Entrée : fondu + glissé doux du bas vers le haut (0,5 s).

### `{quarante lunes}` — « sa prière n'est pas acceptée quarante nuits » (≈ 3 s, puis tient)
- Les 40 croissants passent **un par un** du gris foncé au gris clair (une nuit qui passe : montée d'opacité 0,2 s,
  sans flash, de gauche à droite et de haut en bas). À chaque nuit, un petit ✓ blanc « PRIÈRE FAITE » apparaît
  doucement sur le tapis, mais le compteur « RÉCOMPENSE » **reste figé à « 0 »** et pâlit doucement. Le tapis se
  désature à 60 % (gris), sans disparaître. **Aucun chiffre de prières** (pas de « 200 » : le texte n'en donne pas).
- À la fin : « 40 NUITS » en grand (blanc, contour sombre), et dessous, petit : « (= 40 JOURS DE PRIÈRES) » ; la suite de la carte s'ajoute :
  « … AUCUNE PRIÈRE NE LUI EST ACCEPTÉE PENDANT QUARANTE NUITS. » » ; la caméra dérive lentement vers le compteur.

### `{quarante arrete}` — Petit : « Quarante nuits ?! J'arrête de prier ?! » (≈ 2 s)
- Même ciel ; une petite bulle de pensée de Petit (sa vignette du moteur ou une bulle simple) avec le tapis
  qu'on roule ; un grand « ? » orange au-dessus. Rien d'autre ne change (lunes, tapis gris, compteur à 0).

### `{quarante prie}` — Grand : « Non ! Tu dois quand même prier ! » (≈ 2,2 s, puis tient)
- La bulle « tapis roulé » est **barrée** d'une croix rouge douce (comme `{barre}`) puis s'efface.
- Le tapis **RESTE désaturé** (gris), **sans halo** ; les 40 lunes restent telles quelles ; le compteur reste à 0.
- Tampon doux (descente 0,35 s, échelle 1,15 → 1,0, angle −6°, sans rebond) en orange : « VALABLE, MAIS SANS
  RÉCOMPENSE » ; dessous, grand bandeau VERT avec coche ✓ : « TU DOIS QUAND MÊME PRIER », posé à y = 650 à la place du
  compteur « RÉCOMPENSE : 0 », qui s'efface dessous (le tampon dit déjà « SANS RÉCOMPENSE ») ; la 4e rangée de lunes
  reste visible.
- Petite ligne grise en bas du schéma : « ELLE COMPTE : TU NE LA REFAIS PAS · EXPLICATION D'AN-NAWAWI ».

### `{quarante avenir}` — Grand : « Musulman ! Ton avenir, Allah seul le connaît. » (≈ 3,2 s)
- Changement de plan en fondu vers un nouveau ciel étoilé (les lunes, le tapis et le compteur s'effacent **avec tout
  le ciel**, jamais avant ; le tapis ne se rallume jamais). Au centre, un **parchemin** clair (comme `{carnet}` / le
  parchemin de ISL21), titre orange en haut : « QUI CONNAÎT TON AVENIR ? » ; texte noir :
  « NUL DE CEUX QUI SONT DANS LES CIEUX ET SUR LA TERRE NE CONNAÎT L'INCONNAISSABLE, À PART ALLAH. » ; en bas à droite
  « (EXTRAIT) ». Le mot « ALLAH » en or, rien d'autre de doré ; **aucune représentation** (ni lumière « personnifiée »,
  ni main, ni œil).
- Au début de la réplique, sur « Musulman ! » : une petite étiquette joyeuse verte « TON SIGNE : MUSULMAN ✓ » glisse
  au-dessus du parchemin (≈ 1 s) puis reste, petite.
- Dans un coin, l'icône de l'appli horoscope (ronde, violette) apparaît en petit, avec un « ? » gris.

### `{quarante supprime}` — Petit : « Je supprime ! » (≈ 1,1 s + débord sur la fin de 1,4 s)
- Le parchemin 27:65 **s'efface** en 0,3 s (une seule source à l'écran : CORAN 42:25, portée par cette réplique).
- Le téléphone (vue à ta place, comme l'accroche) revient en bas ; l'icône violette « HOROSCOPE » glisse doucement
  vers une **corbeille** pixel ; boîte de dialogue : « SUPPRIMER « HOROSCOPE » ? » (dès 0,2 s) → bouton « OUI » qui se
  coche ✓ vert (0,6 s ; lisible ≈ 0,4 s) ; à 1,0 s l'icône rapetisse et disparaît en fondu (pas d'explosion).
- Petite ligne verte au-dessus du téléphone : « REPENS-TOI : « C'EST LUI QUI AGRÉE DE SES SERVITEURS LE REPENTIR »
  (EXTRAIT) ».
- Ne pas laisser entendre que supprimer l'appli ou se repentir « efface » les 40 nuits (aucun texte ne le dit) : les
  lunes ne reviennent pas à l'image.

### `{quarante repens}` — Grand : « Et repens-toi ! » (≈ 1 s, dernière réplique, en « schéma »)
- Rien de nouveau ne s'ajoute : « REPENS-TOI : » et l'extrait de 42:25 se lisent seuls sous sa voix (source CORAN 42:25
  sous cette réplique).
- 0,6 s après la balise (`T_REPENS_OUT`, 1,5 avant la contre-vérification ; à recaler sur la vraie voix : durée − 0,35 s
  si elle dépasse 1,1 s), « REPENS-TOI » et la citation s'effacent en 0,35 s : ils ne se mêlent jamais à « ABONNE-TOI
  POUR LA SUITE » quand le schéma déborde sur la fin.

**Interdit partout** : dessiner un devin, une voyante, un sorcier, une main qui lit les cartes, un djinn, le Chaytan,
une figure de tarot (Mort, Diable…), des yeux dans la boule ; écrire « MÉCRÉANT », « ENFER », « PÉCHÉ » ou un chiffre de
fatwa ; flash, secousse. À vérifier sur la planche (1 image/s, et 0,5 s sur les 5 premières secondes) : rien dans la
boule ni sur la carte de tarot, le tapis reste gris, les lunes ne reviennent pas, textes hors des zones interdites,
chaque source sous sa phrase.

## 6. Publication

**Titre** (53 caractères) : `Tu lis ton horoscope ? ARRÊTE ⚠️ Ta prière, 40 nuits…`
(jamais « prière perdue » ni « prière refusée » : la prière reste valable. L'en-tête `TITRE:` du fichier ne change pas :
« Tu lis ton horoscope arrete ».)

**Description YouTube** :

Le Prophète ﷺ a dit : « Celui qui va voir un devin et l'interroge sur quelque chose, aucune prière ne lui est acceptée pendant quarante nuits » (Mouslim 2230). Selon an-Nawawi, cela veut dire qu'il n'a pas la récompense de ces prières, mais elles restent obligatoires et valables : tu dois quand même prier. Et à un homme qui disait « certains d'entre nous vont voir les devins », il a répondu : « Ne va pas les voir » (Mouslim 537). Selon de nombreux savants (dont le Comité permanent : Ibn Baz, al-Fawzan…), l'horoscope entre dans la divination : il est interdit de le lire et de le diffuser ; beaucoup disent que le lire, même pour s'amuser, revient à interroger le devin (pour d'autres, c'est interdit et « proche » de l'interroger ; une fatwa de Dar al-Ifta d'Égypte juge la simple lecture, sans y croire, seulement déconseillée (makrouh)). Et y croire est encore plus grave, car « Nul de ceux qui sont dans les cieux et sur la Terre ne connaît l'Inconnaissable, à part Allah » (Coran 27:65). Le Prophète ﷺ a dit aussi, à propos de l'astrologie : « Celui qui puise une science dans les étoiles puise une branche de la magie : plus il en prend, plus il en prend » (Abou Dawoud 3905, bon selon al-Albani). Un autre hadith dit que celui qui va voir un devin et le croit « s'est désavoué de ce qu'Allah a révélé à Mouhammad » (Abou Dawoud 3904, authentique selon al-Albani ; al-Boukhari a jugé sa chaîne faible, son authenticité est donc discutée). Tu en as déjà lu ? Arrête, repens-toi et continue de prier : « C'est Lui qui agrée de Ses serviteurs le repentir » (Coran 42:25).

Abonne-toi pour la suite 🕹️
#islam #rappel #hadith #horoscope

**Légende TikTok** : `Tu lis ton horoscope ? ARRÊTE ⚠️ Ta prière, 40 nuits… #islam #rappel #hadith #horoscope`

## 7. Points à relire

- « Qui interroge un devin » (texte dit) condense « celui qui va voir un devin et l'interroge sur quelque chose » ; la
  carte à l'écran donne le texte entier, avec « LE PROPHÈTE (PAIX ET SALUT SUR LUI) : ».
- Le lien horoscope = devin n'est plus dit en voix (« C'est un devin ! » retiré) : il est ÉCRIT en gros, avec « SELON
  DE NOMBREUX SAVANTS » (islamqa 147232 pour les 40 nuits ; 336588 / Comité 1/203 pour l'interdiction, sans les 40 nuits).
- Ibn Taymiyya : référence 35/173 non vérifiée dans le recueil → ne l'écrire nulle part en chiffres.
- Durée estimée 27,6 s (8 répliques, empreinte 999da9e450185305) ; carte et lunes vers ≈ 7 s, menace dite vers
  ≈ 9-12 s (le ﷺ dure ≈ 2,5 s, sur le plan moyen qui s'approche) : à remesurer avec les vraies voix.
- Module `explique_0811_horoscope.py` écrit et retouché (2e relecture) ; planche de contrôle du schéma `{quarante}`
  (images isolées, sans voix) : bandeau, « (= 40 JOURS DE PRIÈRES) », « OUI ✓ », effacement de « REPENS-TOI » corrects.
  Planche complète du Short (1 image/s, 0,5 s sur les 5 premières s) à refaire après les voix (GRAND à refaire : ses
  MP3 actuels datent d'un texte plus ancien) : vérifier que l'étiquette passe à « CORAN 42:25 » avant la citation, que
  « ABONNE-TOI » arrive sur un écran propre (`T_REPENS_OUT` = 0,6) et que la carte du hadith a « MOUSLIM 2230 » en
  étiquette pendant les répliques 4 et 5.
- `textes_voix.py` plante dans la console Windows (cp1252) sur « ≈ » : le lancer avec `PYTHONIOENCODING=utf-8`.
