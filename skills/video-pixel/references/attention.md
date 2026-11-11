# Kit TikTok / Shorts : garder l'attention

Recherche du 31/10/2026. La plupart des chiffres qui circulent (« 70 % de rétention à 3 s »…) viennent d'agences sans
source vérifiable : on garde les RÈGLES sur lesquelles toutes les sources s'accordent, pas leurs pourcentages.

**Avant les règles, le sujet** : ce qui a fait des vues sur le compte est dans `references/resultats.md` (relevé
TikTok du 09/11/2026 : 8 vidéos sur 71 font ≈ 79 % des vues). Trois questions, trois oui : ça ARRIVE au spectateur sans
qu'il l'ait choisi ? ça pique ? la réponse soulage ou fait gagner ?

## Les règles
1. **Accroche CHOQUANTE dans les 1 à 3 premières secondes.** Phrase choc dès le 1er mot (règle de l'utilisateur ; le
   01/11/2026 : « pas assez percutante… mets une phrase d'accroche qui est choquante » : peur, honte, provocation,
   paradoxe — « je suis devenu mécréant ?! », « ils me cracheraient dessus », « ça sert à rien »), image qui
   bouge, texte d'accroche à l'écran dès la 1re image (`ACCROCHE:`). TikTok (guide officiel des créations) : annoncer le
   sujet dans les 3 premières secondes, construire l'accroche avec le suspense ou la surprise.
   **Depuis le 06/11/2026 : une CONSIGNE, pas une question.** « Ton téléphone est cassé ? Dis ça » marche (« les ordres,
   ça marche »), les vidéos bâties sur une question au spectateur non (« elles work pas ») : titre et 1re phrase = fais /
   ne fais jamais / dis ça. **Nuance du relevé du 09/11/2026** : l'ordre a percé quand il répondait à un INCIDENT qui
   arrive au spectateur (cauchemar 50 K, téléphone cassé 33 K) ; en reproche sur une habitude ou un péché, il est resté
   sous 3,5 K, et la peur du châtiment en accroche aussi (`references/resultats.md`). Niveau religieux exact : « sinon c'est un péché » seulement pour une obligation ou un
   interdit ; une sunna = « fais ça, tu gagnes… » ; un acte déconseillé = « évite ça ».
2. **Un changement d'image toutes les 2 à 4 s, mais utile** : une preuve, un contraste, une nouvelle question, un
   autre plan — pas de la décoration. Aucun plan figé de plus de 4 s (`controle_video.py` les signale). Les changements
   restent doux (glissements, fondus) : l'utilisateur ne supporte pas les secousses ni les flashs.
3. **L'enjeu tout de suite, la preuve ensuite** (ce que tu gagnes ou risques en suivant la consigne), **relances au
   milieu** (une objection ou un malentendu du perso naïf, « Et le pire… », un nouveau décor). **JAMAIS de numérotation à l'écran** (« 1/2 », « 2/2 », « PARTIE ») :
   l'utilisateur la refuse (« ça n'a aucun sens ») ; le moteur ne l'affiche plus (`{etape "TITRE"}` = titre seul).
4. **Sous-titres** avec les mots importants en jaune (`*mot*`). Étude Verizon Media / Publicis Media 2019 : 80 % des
   sondés disent finir plus souvent une vidéo sous-titrée ; 69 % regardent sans le son dans les lieux publics.
   TikTok conseille 5 à 10 mots par seconde pour un texte à l'écran.
5. **Montrer** : une façon différente à chaque passage (démonstration jouée, miroir, schéma, étiquette, voix off
   ailleurs…), des visages et des émotions (TikTok conseille de montrer des personnes).
6. **Zones sûres** (1080x1920) : rien d'important en haut (≈ 200 px : onglets, recherche, LIVE), en bas (≈ 20 % :
   légende, pseudo, musique) ni à droite (≈ 150 px à partir de ≈ 840 px de haut : boutons). Sous-titres du moteur à
   y = 1465 : dans la zone permise.
7. **Fin courte** : la chute puis « ABONNE-TOI POUR LA SUITE » (2 s, `DUREE_FIN: 2.0`) ; pas de longue conclusion.
   Une boucle (dernière image qui rejoint la première) marche surtout pour les vidéos très courtes (7-20 s).
8. **30 s MAXIMUM** (règle de l'utilisateur, 01/11/2026 : « le plus important sur TikTok c'est le watch time, il
   faut que les gens restent sur la vidéo »). Plus la vidéo est courte, plus la part regardée jusqu'au bout est
   haute. Couper ce qui n'est pas indispensable. **Un sujet = UN seul Short complet** : JAMAIS de « partie 2 » (refusé
   le 01/11/2026 : « je veux que ce soit des parties 1 complètes… un short maximum ») ; si c'est trop long, resserrer
   le texte (garder règle + source + nuance indispensable) jusqu'à 30 s. Pas de seconde morte : le moteur retire
   les respirations des voix ; chaque ﷺ (≈ 2,5 s) doit tomber sur un plan qui bouge ou un élément qui arrive.
9. **Mesurer sur ses propres chiffres**, pas sur ceux des agences : YouTube Studio → contenu → Shorts → « Combien ont
   choisi de regarder » (regardé / balayé) + courbe de rétention ; TikTok → rétention et durée moyenne. Comparer les
   vidéos entre elles, changer une seule chose à la fois (l'accroche d'abord).

## Structure type d'un Short de 30 s maximum (sketch explicatif)
| Temps | Contenu | Outil |
|---|---|---|
| 0-3 s | situation + ORDRE (« … dis ça ! ») + image forte + texte d'accroche | `ACCROCHE:`, `{selfie …}`, `{pensees …}`, gros plan, choc |
| 3-7 s | objection du perso naïf, l'enjeu | `plan moyen`, scène d'illustration en voix off |
| 7-12 s | point 1, montré | schéma / miroir / démonstration |
| ~12 s | réaction du perso naïf | champ / contre-champ, `schéma` |
| 12-22 s | relance + point 2, autre façon de montrer | malentendu du perso, `nouveau schéma`, voix off ailleurs |
| 22-26 s | chute drôle qui redonne la consigne | rapprochement automatique sur la chute |
| 26-28 s | fin courte | `FIN` (`DUREE_FIN: 2.0`) |

Exemple réel (01/11/2026, « Lire le Coran sans comprendre », ≤ 30 s) : accroche provocante 0-3 s → GRAND → Coran ouvert
où chaque lettre lue donne « +1 » puis « +10 » → lettres ا ل م calées sur la voix + « = 30 » → réaction → téléphone qui
défile → il prend le Coran + citation sourcée → fin. Un changement toutes les 2 à 5 s, chaque hadith MONTRÉ en image
concrète.

Modèle CONSIGNE (04/11/2026, « Ton téléphone est cassé ? Dis ça », `scenarios\islam_13_telephone.txt`, celui que les
gens « aiment trop ») : accroche « TON TÉLÉPHONE EST CASSÉ ? / DIS ÇA ! » + le téléphone qui tombe vu d'en haut →
Petit « Noooon ! Mon téléphone ! » → Grand « Dis vite : inna lillahi » → « Pour un téléphone ?! » → la dua montrée
ligne par ligne (Mouslim 918) → « Le dernier iPhone ?! » → « Mieux… c'est Allah qui choisit. Patiente ! ».

## Sources
- TikTok, Creative best practices for performance ads : https://ads.tiktok.com/help/article/creative-best-practices?lang=en
- YouTube Help, Understand your content performance : https://support.google.com/youtube/answer/12220281
- Verizon Media & Publicis Media 2019 (via 3Play Media) : https://www.3playmedia.com/blog/verizon-media-and-publicis-media-find-viewers-want-captions/
- Zones sûres (estimations, à vérifier sur téléphone) : https://reap.video/blog/short-form-video-safe-zones
- Principes (chiffres non sourcés) : https://www.grow-it.se/en/resources/short-form-video-retention-benchmarks ,
  https://www.gofaceless.ai/en/blog/optimize-video-engagement-pattern-breaks , https://socialk.it/en/blog/tiktok-storytelling-guide
