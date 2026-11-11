# ISL31 — « Soleil couché ? Rentre les petits, les démons sortent » (rentrer les enfants au coucher du soleil, fermer la porte en disant Bismillah)

Scénario : `scenarios\islam_31_coucher.txt` · module à dessiner : `explique_0811_coucher.py` (clés `coucher`, `crepuscule`)
Durée estimée (textes_voix.py) : **≈ 27,1 s fin comprise** · empreinte du texte dit : **402c6946534e00f6** (révisée le 08/11 après
relecture : seule la réplique 1 change ; ancienne empreinte 15a1d6ad6bf237df caduque ; INCHANGÉE après la 2e relecture : seules
des balises et le module bougent) · 433 caractères ElevenLabs · aucune didascalie inconnue.

### Contre-vérification (08/11/2026) — ce qui a changé (aucun mot dit, empreinte 402c6946534e00f6 conservée, voix valables)
- Bandeau final : « APRÈS LE DÉBUT DE LA NUIT, » se lisait « une fois la nuit commencée » (l'inverse du texte) →
  **« QUAND LE DÉBUT DE LA NUIT EST PASSÉ, »** (Boukhari 3304 « فَإِذَا ذَهَبَ سَاعَةٌ مِنَ اللَّيْلِ فَحُلُّوهُمْ », Mouslim 2013a
  « حَتَّى تَذْهَبَ فَحْمَةُ الْعِشَاءِ », Mouslim 2012e, relus sur sunnah.com ; réduit automatiquement à 760 px de large).
- Bandeau en fondu **dès le début** de `{crepuscule nuit}` (`smooth(u / 0.3)`) : ≈ 0,4 s de lecture en plus (avec les vraies voix,
  il n'était lisible qu'≈ 1,7 s).
- Plantage du rendu corrigé : `_panneau` ne dessine plus de battant de moins d'1 px (Pillow levait « x1 must be greater than or equal
  to x0 » au tout début de chaque fermeture de porte).
- Ballon de l'accroche : 3 tours au lieu de 3,2 → il s'arrête sur le motif classique (phase 0), plus sur un motif à « visage ».

### 2e relecture (08/11/2026) — ce qui a changé (aucun mot dit)
- Bandeau final : « PLUS TARD DANS LA NUIT » → « APRÈS LE DÉBUT DE LA NUIT, » (remplacé ensuite, voir ci-dessus) (Boukhari 3304 « فَإِذَا ذَهَبَ سَاعَةٌ مِنَ اللَّيْلِ »,
  Mouslim 2013 « حَتَّى تَذْهَبَ فَحْمَةُ الْعِشَاءِ » ; an-Nawawi 13/185 : le noir du DÉBUT de la nuit), relus sur sunnah.com.
- Bandeau final : lignes limitées à **760 px** et 3e ligne **« CONSEIL : SUNNA (AVIS MAJORITAIRE) »** → texte entre x 188 et x 900
  (y 966-1212, mesuré avec le moteur) : plus rien sous les boutons (avant : jusqu'à x ≈ 1002). La 3e ligne est GARDÉE (nuance
  obligatoire, seul endroit où elle se lit longtemps).
- `{crepuscule}` posé au **début** de la réplique 3 (le schéma bouge pendant le ﷺ : nuit qui tombe, enfants qui rentrent, brume
  sans légende) + nouvelle sous-clé **`{crepuscule tombe}`** qui cale « QUAND LA NUIT TOMBE… / RETENEZ VOS ENFANTS / SUNNA (AVIS
  MAJORITAIRE) » sur les mots → la menace se voit vers ≈ 4,5 s au lieu de ≈ 8 s.
- Brume : texture interpolée (glissé continu, plus de saut 4 fois par seconde). `{crepuscule claque}` : glissé de caméra 0,9 s
  (au lieu de 0,7 s), sautillé de Petit 3 px à 4 rebonds/s (au lieu de 5 px à 5).

## 1. Sources vérifiées (sunnah.com, navigateur intégré, 08/11/2026, page par page — revérifiées après relecture)

| Réf. | URL | Narrateur | Grade |
|---|---|---|---|
| Boukhari 3304 | https://sunnah.com/bukhari:3304 | Jâbir ibn 'Abdillah | sahih (Boukhari) |
| Boukhari 5623 | https://sunnah.com/bukhari:5623 | Jâbir ibn 'Abdillah (même texte, + outres, récipients, lampes) | sahih |
| Mouslim 2012e | https://sunnah.com/muslim:2012e | Jâbir (même chaîne Ibn Jourayj ← 'Atâ' ← Jâbir) | sahih (Mouslim) |
| Mouslim 2013a | https://sunnah.com/muslim:2013a | Jâbir (Abou z-Zoubayr) | sahih (Mouslim) |
| Mouslim 2012a | https://sunnah.com/muslim:2012 | Jâbir (Abou z-Zoubayr) | sahih |
| Boukhari 3280 | https://sunnah.com/bukhari:3280 | Jâbir | sahih — autre version, SANS « porte fermée » |

**Boukhari 3304 (texte cité dans le Short)** :
« إِذَا كَانَ جُنْحُ اللَّيْلِ ـ أَوْ أَمْسَيْتُمْ ـ فَكُفُّوا صِبْيَانَكُمْ، فَإِنَّ الشَّيَاطِينَ تَنْتَشِرُ حِينَئِذٍ، فَإِذَا ذَهَبَ سَاعَةٌ مِنَ اللَّيْلِ فَحُلُّوهُمْ، وَأَغْلِقُوا الأَبْوَابَ، وَاذْكُرُوا اسْمَ اللَّهِ، فَإِنَّ الشَّيْطَانَ لاَ يَفْتَحُ بَابًا مُغْلَقًا »
Traduction fidèle : « Quand vient l'obscurité de la nuit (ou, selon un doute du rapporteur : quand vous êtes au soir), retenez vos
enfants, car les démons se répandent à ce moment-là. Quand un moment de la nuit est passé, laissez-les aller. Fermez les portes et
citez le nom d'Allah, car le Chaytan n'ouvre pas une porte fermée. »
(Mouslim 2012e : identique, avec « الشَّيْطَانَ يَنْتَشِرُ » au singulier et « فَخَلُّوهُمْ ».)

**Mouslim 2013a (lien avec le coucher du soleil ; base de la réplique 1)** :
« لاَ تُرْسِلُوا فَوَاشِيَكُمْ وَصِبْيَانَكُمْ إِذَا غَابَتِ الشَّمْسُ حَتَّى تَذْهَبَ فَحْمَةُ الْعِشَاءِ فَإِنَّ الشَّيَاطِينَ تَنْبَعِثُ إِذَا غَابَتِ الشَّمْسُ حَتَّى تَذْهَبَ فَحْمَةُ الْعِشَاءِ »
« Ne laissez pas sortir vos bêtes et vos enfants quand le soleil se couche, jusqu'à ce que passe le noir du début de la nuit, car les
démons sortent quand le soleil se couche, jusqu'à ce que passe le noir du début de la nuit. » (تَنْبَعِثُ ; anglais sunnah.com : « is let loose »)

**Mouslim 2012a** : « … فَإِنَّ الشَّيْطَانَ لاَ يَحُلُّ سِقَاءً وَلاَ يَفْتَحُ بَابًا وَلاَ يَكْشِفُ إِنَاءً » (le Chaytan ne dénoue pas une outre,
n'ouvre pas une porte, ne découvre pas un récipient).

### Corrections du brief
- **Boukhari 3280 ne contient PAS « le Chaytan n'ouvre pas une porte fermée »** (il a « أَغْلِقْ بَابَكَ وَاذْكُرِ اسْمَ اللَّهِ » et
  « سَاعَةٌ مِنَ الْعِشَاءِ ») → il n'est pas affiché ; source à l'écran : **BOUKHARI 3304 · MOUSLIM 2012** (texte exact = 3304 = 5623 = 2012e).
- **Le lien avec le coucher du soleil vient de Mouslim 2013**, pas de 3304 ; Ibn Hajar (Fath al-Bari 6/341) : جُنْح الليل = l'arrivée
  de la nuit après le coucher du soleil. La réplique 1 (« Rentre ! Les démons sortent ! ») porte donc **{source "MOUSLIM 2013"}**.
- **Le texte vise les enfants (صِبْيَان)** : l'accroche dit **« RENTRE LES PETITS ! »** ; dans la scène, Grand dit « rentre ! » à son
  petit frère (un enfant), ce qui est le texte.

## 2. Niveau religieux : RECOMMANDÉ (sunna, conseil de protection) selon LA PLUPART des savants
- **Preuve du niveau** : Fatâwâ al-Lajna ad-Dâ'ima 26/317 : « هذه الأوامر الواردة في الحديث محمولة على الندب والإرشاد عند أكثر العلماء »,
  citant Ibn Mouflih (al-Fouroû' 1/132) et Ibn Hajar (Fath al-Bari 11/87) — lu sur islamqa.info/ar/answers/125922 le 08/11/2026.
  Ce n'est pas unanime (« عند أكثر العلماء ») → dit À L'ÉCRAN et dans la description.
- **Correction de relecture** : le titre du chapitre n'est pas de Mouslim mais d'an-Nawawi, et en arabe il dit « باب الأَمْرِ… وَكَفِّ
  الصِّبْيَانِ وَالْمَوَاشِي بَعْدَ الْمَغْرِبِ » (« l'ORDRE de… ») ; le « It is recommended » vient seulement de la traduction anglaise de
  sunnah.com et ne compte PAS comme preuve.
- An-Nawawi (Charh Mouslim 13/185) : « فكفوا صبيانكم : أي امنعوهم من الخروج ذلك الوقت » ; ces gestes sont des causes de protection
  contre la nuisance du Chaytan (il ne peut ni découvrir un récipient, ni dénouer une outre, ni ouvrir une porte) ; on craint pour les
  enfants à ce moment-là parce que les démons sont nombreux. Il rappelle aussi le hadith de celui qui NOMME Allah en entrant chez lui
  (le Chaytan dit : « pas de gîte ») : citer le nom d'Allah = le DIRE.
- Donc : « fais ça », jamais « péché », jamais « obligatoire ». À l'écran : « SUNNA (AVIS MAJORITAIRE) ».

## 3. L'avertissement exact
« Les démons sortent » quand le soleil se couche (Mouslim 2013, réplique 1, ≈ 0-2 s) puis « les démons se répandent à ce moment-là »
(Boukhari 3304 · Mouslim 2012, réplique 3). Rien de plus : le Short ne dit pas ce qu'ils font, ne promet aucun malheur, ne parle ni de
possession ni d'Enfer. Le remède = le même texte : enfants à l'intérieur, porte fermée en citant le nom d'Allah, « le Chaytan n'ouvre
pas une porte fermée ».

## 4. Nuances indispensables (toutes à l'écran)
1. Ce n'est **pas toute la nuit** (« فَإِذَا ذَهَبَ سَاعَةٌ مِنَ اللَّيْلِ فَحُلُّوهُمْ ») → **bandeau final SANS guillemets** pendant la chute
   (répliques 6-7 en « schéma », plan serré sur la porte, sans brume dans le cadre), lisible ≥ 2 s :
   « QUAND LE DÉBUT DE LA NUIT EST PASSÉ, LES ENFANTS PEUVENT RESSORTIR » (blanc) // « CONSEIL : SUNNA (AVIS MAJORITAIRE) » (jaune).
   Jamais « LÂCHEZ-LES » (se lirait « lâchez les démons »). Plus aucune carte pendant « Bismillah ! ».
2. **Sunna (avis majoritaire)**, pas obligation : petit et blanc sous « RETENEZ VOS ENFANTS » dans `{crepuscule}` + 2e ligne du bandeau
   final + description.
3. **Bismillah = une parole** (« وَاذْكُرُوا اسْمَ اللَّهِ ») : bulle de parole « BISMILLAH ! » + « = AU NOM D'ALLAH » ; JAMAIS écrit sur la
   porte (pas d'image d'inscription qui protège, de talisman).
4. Le hadith concerne **les enfants** : on n'ajoute RIEN sur les adultes (ni « ils ne risquent rien », ni l'inverse) ; la brume ne
   touche jamais Grand ni personne.

## 5. Texte dit (empreinte 402c6946534e00f6)
| # | Perso | Texte | Balises |
|---|---|---|---|
| 1 | GRAND (stop) | [firm] Rentre ! Les démons *sortent* ! | `{coucher PETIT}` (image 0) · source MOUSLIM 2013 |
| 2 | PETIT (énervé, bulle ?) | [annoyed] Je suis plus un *bébé* ! | — (scène, rue du soir) |
| 3 | GRAND (explique, plan moyen) | [serious] Le Prophète ﷺ a dit : « Quand la nuit tombe, retenez vos enfants… car les démons se *répandent* à ce moment-là. » | `{crepuscule}` au début de la réplique (avant « Le Prophète »), `{crepuscule tombe}` après « a dit : », `{crepuscule repandent}` avant « car » · source BOUKHARI 3304 · MOUSLIM 2012 |
| 4 | GRAND (index, nouveau schéma) | [firm] « Fermez les portes, citez le nom d'Allah… car le Chaytan n'ouvre pas une porte *fermée*. » | ≈ 1 s sur le visage de Grand, `{crepuscule porte}` après « Fermez les portes, », `{crepuscule fermee}` avant « car » · même source |
| 5 | PETIT (panique, sort à droite, schéma) | [panicked] *Bismillah* ! | `{crepuscule claque}` · même source |
| 6 | GRAND (choc, bulle !, schéma) | [surprised] Et *moi* ?! | `{crepuscule nuit}` (Grand de dos devant la porte fermée + bandeau final) · même source |
| 7 | PETIT (voix off, schéma) | [mischievously] T'es plus un *bébé* ! | reste sur `{crepuscule nuit}` (bandeau lisible) · même source, puis FIN |

## 6. SPÉCIFICATION VISUELLE (pour `explique_0811_coucher.py`)
Règles communes : mouvements DOUX seulement (glissés, fondus ≥ 0,3 s ; jamais de secousse, de flash, de coupe sèche, de porte qui
« claque » avec tremblement) ; AUCUN Chaytan dessiné ni suggéré : la brume n'a NI forme, NI visage, NI yeux, NI mains, NI griffes, NI
cornes, NI silhouette, NI ombre humanoïde, NI sourire, et ne touche jamais un personnage ; rien de gore ; Allah jamais représenté ;
aucun prophète, ange ou Compagnon. **Aucun texte écrit sur une porte** (le nom d'Allah est DIT, en bulle de parole). **Lampadaires
stables** pendant la brume (elle n'agit sur rien) : la rue s'assombrit uniquement avec la tombée de la nuit dans `{crepuscule}`, AVANT
la brume. Textes à l'écran en MAJUSCULES, pixel art du moteur, dans la zone sûre (pas dans les 200 px du haut, ni sous y ≈ 1450 où vont
les sous-titres, ni sur la bande droite x > 930 au-dessous de y ≈ 840). Palette du soir : ciel orange → rouge → violet, immeubles en
contre-jour violet sombre, lampadaires jaune chaud. Personnages à l'échelle (une porte ≈ 1,2 × un perso).
Les modes `porte`, `fermee`, `claque`, `nuit` doivent pouvoir partir SANS l'état du mode précédent (la réplique 4 est un « nouveau
schéma ») : chacun redessine la rue de nuit, les trois maisons et la brume au sol, loin des persos.

### `{coucher PETIT}` — accroche, image 0 (≈ 0-3 s, sous l'ACCROCHE « LE SOLEIL SE COUCHE ? / RENTRE LES PETITS ! »)
- Vue À TA PLACE, debout au bout de la rue (décor rue_proche_soir, cadrage plein écran).
- Au fond, au centre : un GRAND soleil rouge-orangé (**≈ 420 px de diamètre**) qui descend lentement derrière la ligne des immeubles
  (au bout de 3 s il n'en reste qu'une moitié) ; le ciel passe doucement de l'orange au rouge. Rien sur le soleil qui ressemble à des
  yeux, des cornes ou une silhouette.
- Au milieu de la rue : Petit (sweat rouge, casquette), content, qui tire dans son ballon ; le ballon roule VERS TOI et grossit
  (**≈ 60 → ≈ 320 px**) et s'arrête au-dessus de y ≈ 1400 (hors des sous-titres).
- Les ombres (Petit, lampadaires, poteaux) s'allongent lentement vers le bas de l'écran, vers toi ; lampadaires allumés en fondu.
- Pas de brume, pas de texte en plus de l'accroche (la source MOUSLIM 2013 du moteur ne doit pas chevaucher l'accroche : à vérifier
  sur la planche).

### `{crepuscule}` — la nuit tombe (dès le DÉBUT de la réplique 3, ≈ 4,1 s, pendant « Le Prophète ﷺ a dit : »)
- Le schéma n'est pas figé pendant le ﷺ : tombée de la nuit (1,4 s), enfants vert et bleu qui rentrent, brume sans légende qui
  naît à u = 0,4. Les trois textes ci-dessous n'arrivent qu'avec **`{crepuscule tombe}`** (sur « Quand la nuit tombe »,
  décalés de 0,1 / 0,85 / 1,1 s).
- Grand schéma plein : la même rue vue un peu de haut, le soleil a disparu (un fil rouge à l'horizon), ciel violet-bleu sombre.
- Trois maisons basses avec leur porte éclairée ; trois enfants (silhouettes simples) encore dehors : Petit (sweat rouge, casquette),
  un enfant au **sweat bleu**, un enfant au sweat vert.
- Texte en haut (≈ y 300) : « QUAND LA NUIT TOMBE… » ; ≈ 1 s après, en dessous : « RETENEZ VOS ENFANTS » (jaune), et dessous, petit
  et blanc : « SUNNA (AVIS MAJORITAIRE) ». L'enfant vert et l'enfant bleu marchent tranquillement vers leur maison ; Petit reste
  dehors, au milieu.
- **La brume naît déjà, SANS légende**, tout au fond de la rue (fine bande au ras du sol, très loin des enfants) : l'avertissement se
  voit avant d'être nommé.

### `{crepuscule repandent}` — l'avertissement (sur « car les démons se répandent à ce moment-là »)
- La BRUME sombre (gris-violet très foncé, semi-transparente, bords flous, aucune forme reconnaissable) s'étale lentement au ras du sol
  et le long des murs (≈ 2 s pour couvrir la moitié de la rue). Lampadaires inchangés.
- Grand texte (≈ y 420) : « LES DÉMONS SE RÉPANDENT » (blanc, contour rouge sombre), petit texte dessous « (CHAYÂTÎN) » et
  « À CE MOMENT-LÀ ».
- La brume s'ARRÊTE à bonne distance de Petit (≈ 150 px) : elle ne le touche pas, ne l'entoure pas. Petit a l'air inquiet (goutte).
- INTERDIT : yeux brillants dans la brume, visages, mains, silhouettes, rires, flash, « jump scare ».

### `{crepuscule porte}` — le remède (réplique 4, après « Fermez les portes, » ; avant : ≈ 1 s sur le visage de Grand)
- Rue de nuit redessinée (nouveau schéma) ; rapprochement lent (≈ 0,8 s) sur la porte de l'enfant au **sweat bleu** (on le voit de dos
  dans l'encadrement éclairé). **Petit reste dehors**, petit, au milieu de la rue au second plan, et regarde la brume (goutte) ; la brume
  est au sol, loin de lui et de la porte.
- La porte se ferme doucement (≈ 1 s, sans rebond). **Pendant qu'elle se ferme, une BULLE DE PAROLE « BISMILLAH ! » sort de
  l'entrebâillement** (dite par l'enfant qui ferme) ; dessous, petit et blanc : « = AU NOM D'ALLAH ». La bulle s'efface quand la porte
  est fermée. **Rien d'écrit sur la porte.** Texte en haut : « FERMEZ LES PORTES ».

### `{crepuscule fermee}` — la porte tient (sur « car le Chaytan n'ouvre pas une porte fermée »)
- La porte fermée vue de dehors, **nue, sans aucun texte** ; un liseré de lumière dorée douce apparaît autour du cadre **là où était la
  bulle** (lié à la parole), sans éclair.
- La brume glisse jusqu'au seuil et S'ARRÊTE au liseré ; elle ne passe pas, ne monte pas sur la porte, rien ne touche la poignée.
- Grand texte : « LE CHAYTAN N'OUVRE PAS / UNE PORTE FERMÉE » (blanc, « FERMÉE » en jaune) + une coche verte douce.
- INTERDIT : une main, une griffe ou une ombre sur la poignée, une forme qui gratte la porte.

### `{crepuscule claque}` — Petit rentre (réplique 5, Petit : « Bismillah ! »)
- La caméra glisse doucement (0,9 s) vers la maison de **Petit** (une AUTRE porte que celle de l'enfant bleu). Petit (sweat rouge,
  casquette) court vers elle (glissé rapide mais fluide, sautillé de 3 px seulement) ; son trajet reste dégagé : la brume est DERRIÈRE lui, au sol, et ne le touche jamais. Il entre, la porte se ferme vite
  mais sans tremblement (petit « clac » discret).
- Bulle depuis la fenêtre éclairée : « BISMILLAH ! ».
- **Aucune carte, aucun autre texte** (l'ancienne carte « LÂCHEZ-LES » est supprimée).

### `{crepuscule nuit}` — la chute (répliques 6-7, jusqu'à FIN)
- Plan serré sur la porte fermée de Petit et sa fenêtre éclairée, ciel de nuit (pas de retour à la rue orange) ; **la brume est hors du
  cadre** (restée loin dans la rue : la caméra est simplement plus proche, elle ne disparaît pas).
- Grand (qamis, gilet vert, kufi) arrive DE DOS à pas lents devant la porte déjà fermée, s'arrête, petite bulle « ! » au-dessus de lui :
  le gag « porte fermée au nez de Grand » se voit sans le son.
- **Bandeau** en fondu de 0,3 s dès le début du plan (≈ y 1250, au-dessus des sous-titres, fond sombre doux), du début de la réplique 6
  jusqu'à FIN (≈ 2 s de voix + jusqu'à 1,4 s sur « ABONNE-TOI ») : « QUAND LE DÉBUT DE LA NUIT EST PASSÉ, / LES ENFANTS PEUVENT RESSORTIR » (blanc) // « CONSEIL : SUNNA
  (AVIS MAJORITAIRE) » (jaune). SANS guillemets. Chaque ligne ≤ 760 px → texte entre x 188 et x 900 de l'écran (y 966-1212), hors
  des boutons. **La ligne jaune reste** même si la planche paraît chargée (décision de relecture : c'est la nuance obligatoire et,
  dans `{crepuscule}`, elle ne se lit qu'≈ 1-1,5 s).
- Aucun texte ni signe sur les adultes.

Durées : `fin_anim` de chaque mode ≈ 2,5-3 s (ballon et soleil 3 s ; brume 2 s ; porte 1 s ; claque 1,2 s ; nuit : arrivée de Grand
≈ 1 s, bandeau en fondu 0,3 s dès u = 0 puis fixe). Ballon de l'accroche : exactement 3 tours (s'arrête sur le motif classique).

## 7. Publication
- **Titre** (55 caractères) : `Soleil couché ? Rentre les petits, les démons sortent 😨`
- **Description YouTube** :

```
Le Prophète ﷺ a dit : « Quand vient l'obscurité de la nuit (ou, selon un doute du rapporteur : quand vous êtes au soir), retenez vos enfants, car les démons se répandent à ce moment-là. Quand un moment de la nuit est passé, laissez-les aller. Fermez les portes et citez le nom d'Allah, car le Chaytan n'ouvre pas une porte fermée. » (Boukhari 3304 · Mouslim 2012)
Et dans Mouslim (2013) : « Ne laissez pas sortir vos bêtes et vos enfants quand le soleil se couche, jusqu'à ce que passe le noir du début de la nuit, car les démons sortent quand le soleil se couche, jusqu'à ce que passe le noir du début de la nuit. »
Selon la plupart des savants, c'est un conseil recommandé (sunna) pour protéger les enfants et la maison, pas une obligation. Ce n'est pas toute la nuit : seulement le début, après le coucher du soleil. Dire « Bismillah » en fermant la porte, c'est citer le nom d'Allah.
Abonne-toi pour la suite 🕹️
#islam #rappel #hadith #maghrib
```

- **Légende TikTok** : `Soleil couché ? Rentre les petits, les démons sortent 😨 #islam #rappel #hadith #maghrib`
- L'en-tête `TITRE:` du scénario (nom de fichier vidéo) reste `Le soleil se couche rentre les petits`.

## 8. Points à relire (planche)
- 1 image/s, et toutes les 0,5 s pour les 5 premières secondes : ballon et soleil en grand dès l'image 0, la source MOUSLIM 2013 ne
  chevauche pas l'accroche.
- Rien qui ressemble à une silhouette, des cornes ou des yeux, ni dans la brume ni sur le soleil couchant ; aucun contact de la brume
  (surtout pendant la course de Petit et l'arrivée de Grand) ; porte qui se ferme sans rebond ; aucune inscription sur une porte.
- « QUAND LA NUIT TOMBE… » arrive bien sur les mots (`{crepuscule tombe}`) ; la brume glisse sans saccade ; passage claque → nuit
  sans coupe sèche.
- Le bandeau final se lit au moins 2 s ; aucun texte dans les 200 px du haut, sous y ≈ 1450 ni à droite de x 930 au-dessous de y 840.
- Petit n'entre qu'une fois (réplique 5) ; la porte de la réplique 4 est celle de l'enfant au sweat bleu.
- « Chaytan » : prononciation ElevenLabs (déjà utilisé dans ISL20).
- Même risque possible dans ISL20 (signalé par la relecture) : vérifier que « BISMILLAH » n'y est pas montré comme une inscription
  qui protège la porte (ISL20 n'est pas modifié ici).
