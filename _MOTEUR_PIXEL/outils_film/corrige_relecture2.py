"""Corrections de la 2e relecture indépendante (parties 10 à 24), 01/11/2026."""
import io
import sys

P = sys.argv[1]
s = io.open(P, encoding="utf-8").read()
n_ok = 0


def rep(old, new, n=1):
    global s, n_ok
    assert s.count(old) == n, (old[:90], s.count(old))
    s = s.replace(old, new)
    n_ok += 1


# ---------------------------------------------------------------- ERREUR : Youcha' (prophète) ne doit pas être doublé
rep("@IMAGE Au bord d'une terre verte et fertile, au loin des murailles ; l'orbe de Moussa face au peuple ; deux hommes s'avancent du groupe ; le peuple, lui, recule et s'assoit par terre.",
    "@IMAGE Au bord d'une terre verte et fertile, au loin des murailles ; l'orbe de Moussa face au peuple ; deux hommes s'avancent du groupe : l'orbe de YOUCHA' et un homme pieux (dessiné) ; le peuple, lui, recule et s'assoit par terre.")
rep("DEUX_HOMMES | [calm] Entrez chez eux par la porte ; puis, quand vous y serez entrés, vous serez les vainqueurs. Et c'est en Allah qu'il faut avoir confiance, si vous êtes croyants. | CORAN 5:23",
    "C | Deux hommes d'entre ceux qui craignaient Allah et qui étaient comblés par Lui de bienfaits dirent : « Entrez chez eux par la porte ; puis, quand vous y serez entrés, vous serez les vainqueurs. Et c'est en Allah qu'il faut avoir confiance, si vous êtes croyants. » | CORAN 5:23")

# ---------------------------------------------------------------- À REVOIR : la foudre, l'invocation, puis la résurrection
rep("C | Alors la foudre vous saisit tandis que vous regardiez. Puis Nous vous ressuscitâmes après votre mort afin que vous soyez reconnaissants. | CORAN 2:55-56\n",
    "C | Alors la foudre vous saisit tandis que vous regardiez. | CORAN 2:55 (EXTRAIT)\n")
rep("Pardonne-nous et fais-nous miséricorde, car Tu es le Meilleur des pardonneurs ! » | CORAN 7:155 (EXTRAIT)\n",
    "Pardonne-nous et fais-nous miséricorde, car Tu es le Meilleur des pardonneurs ! » | CORAN 7:155 (EXTRAIT)\n"
    "C | Puis Nous vous ressuscitâmes après votre mort afin que vous soyez reconnaissants. | CORAN 2:56\n")

# ---------------------------------------------------------------- À REVOIR : les douze sources, pendant les quarante ans (P16 -> P21)
bloc_sources = s[s.index("@SCENE LES DOUZE SOURCES\n"):s.index("\n=== P17 |")]
assert bloc_sources.count("\n") >= 7
s = s.replace(bloc_sources, "", 1).replace("\n\n\n=== P17 |", "\n\n=== P17 |")
bloc_sources = bloc_sources.rstrip("\n") + "\n"
old_n174 = "N | [warmly] Un rocher qu'ils emportent avec eux. À chaque halte, Moussa le frappe… et l'eau jaillit. | TAFSIR IBN KATHIR (5:26)\n"
assert bloc_sources.count(old_n174) == 1
bloc_sources = bloc_sources.replace(old_n174, "N | [warmly] Ils emportent avec eux un rocher, porté par une bête. À chaque halte, Moussa le frappe… et l'eau jaillit. | TAFSIR IBN KATHIR (5:26 · 2:60)\n")
old_c79 = "C | Et quand Moussa demanda de l'eau"
assert bloc_sources.count(old_c79) == 1
bloc_sources = bloc_sources.replace(old_c79, "N | [warmly] Et pourtant, même dans ce désert, Allah ne les abandonne pas. | TAFSIR IBN KATHIR (2:57)\n" + old_c79)
bloc_sources = bloc_sources.replace("@IMAGE Le désert brûlant ; le peuple assoiffé ;", "@IMAGE Les années d'errance, le désert brûlant ; le peuple assoiffé ;")
rep("N | [sad] Quarante ans. Chaque matin, ils se mettent en marche. Et chaque soir, ils ne sont arrivés nulle part. | TAFSIR IBN KATHIR (5:26, IBN 'ABBAS)\n",
    "N | [sad] Quarante ans. Chaque matin, ils se mettent en marche. Et chaque soir, ils ne sont arrivés nulle part. | TAFSIR IBN KATHIR (5:26, IBN 'ABBAS)\n" + bloc_sources)

# ---------------------------------------------------------------- À REVOIR : 'Achoura (Boukhari 3397)
rep("N | [warmly] Ce jour-là, Moussa jeûna pour remercier Allah. Des siècles plus tard, à Médine, le Prophète jeûnera ce même jour, et dira : « Nous sommes plus proches de Moussa. » C'est le jour de 'Achoura. | BOUKHARI 2004",
    "N | [warmly] Ce jour-là, Moussa jeûna pour remercier Allah. Des siècles plus tard, à Médine, le Prophète trouvera les juifs en train de jeûner ce jour-là. Il dira : « Je suis plus proche de Moussa qu'eux. » Et il jeûnera, lui aussi. C'est le jour de 'Achoura. | BOUKHARI 3397")

# ---------------------------------------------------------------- À REVOIR : « Il a donc oublié » expliqué
rep("FILS_D_ISRAEL | [excited] C'est votre divinité et la divinité de Moussa ! Il a donc oublié ! | CORAN 20:88\n",
    "FILS_D_ISRAEL | [excited] C'est votre divinité et la divinité de Moussa ! Il a donc oublié ! | CORAN 20:88\n"
    "N | [calm] Moussa, disent-ils, a oublié son dieu ici… et il est parti le chercher ailleurs. | TAFSIR IBN KATHIR (20:88, IBN 'ABBAS)\n")

# ---------------------------------------------------------------- À REVOIR : le garçon (18:82)
rep("Je ne l'ai d'ailleurs pas fait de mon propre chef. Voilà l'interprétation de ce que tu n'as pas pu endurer avec patience. » | CORAN 18:78-82\n",
    "Je ne l'ai d'ailleurs pas fait de mon propre chef. Voilà l'interprétation de ce que tu n'as pas pu endurer avec patience. » | CORAN 18:78-82\n"
    "N | [calm] Al-Khidr n'a rien fait de lui-même : c'est Allah qui le lui avait ordonné. | TAFSIR IBN KATHIR (18:82)\n")

# ---------------------------------------------------------------- À REVOIR : contexte avant l'invocation (10:88)
rep("@SON Nuit, fleuve ; musique grave.\nC | Et Moussa dit : « Ô notre Seigneur ! Tu as accordé à Pharaon",
    "@SON Nuit, fleuve ; musique grave.\n"
    "N | [calm] Pharaon et ses notables ont vu tous les signes… et ils refusent toujours. Moussa sait maintenant qu'il n'y a plus rien de bon à attendre d'eux. | TAFSIR IBN KATHIR (10:88)\n"
    "C | Et Moussa dit : « Ô notre Seigneur ! Tu as accordé à Pharaon")

# ---------------------------------------------------------------- DÉTAILS
rep("C | Moussa dit : « Ô Pharaon ! Je suis un Messager de la part du Seigneur de l'Univers,",
    "C | Et Moussa dit : « Ô Pharaon ! Je suis un Messager de la part du Seigneur de l'Univers,")
rep("N | [warmly] Pendant ce temps, en Égypte, Allah inspire à Haroun d'aller à la rencontre de son frère.",
    "N | [warmly] Pendant ce temps, en Égypte, Allah révèle à Haroun qu'il doit aller à la rencontre de son frère.")
rep("Et ce qu'ils viennent de voir… ce n'est pas de la magie. | TAFSIR IBN KATHIR (20:70)",
    "Et ce qu'ils viennent de voir… ce n'est pas de la magie. | TAFSIR IBN KATHIR (20:69-70)")
rep("N | [warmly] Et elle voyait déjà, racontent les anciens, sa maison au Paradis.",
    "N | [warmly] Et déjà, elle voyait sa maison au Paradis.")
rep("N | [dark] Pendant ce temps, au camp, un homme appelé le Samiri rassemble les bijoux d'or emportés d'Égypte. Il les jette dans le feu… et en fait sortir un veau. Un veau d'or… qui mugit. | CORAN 20:87-88",
    "N | [dark] Pendant ce temps, au camp, un homme appelé le Samiri leur fait rassembler les bijoux emportés d'Égypte. On les jette dans le feu… et il en fait sortir un veau. Un veau d'or… qui mugit. | CORAN 20:87-88 · TAFSIR IBN KATHIR (20:96, 'IKRIMA)")
rep("@IMAGE Au camp : un homme (LE SAMIRI) rassemble les bijoux des femmes, les jette dans un grand feu ;",
    "@IMAGE Au camp : un homme (LE SAMIRI) fait rassembler les bijoux ; on les jette dans un grand feu ;")
rep("Allah le lui reproche : il aurait dû dire qu'Allah seul sait.",
    "Allah le lui reproche, car il aurait dû répondre : « Allah sait mieux. »")
rep("« Retourne vers ton Seigneur, et demande-Lui d'alléger : ta communauté n'en sera pas capable. » | BOUKHARI 349",
    "« Retourne vers ton Seigneur, et demande-Lui d'alléger : ta communauté n'en sera pas capable. » | MOUSLIM 162")
rep("L'homme qui a parlé à son Seigneur… et fendu la mer. | CORAN 28:7 · 20:39",
    "L'homme qui a parlé à son Seigneur… et devant qui la mer s'est ouverte. | CORAN 28:7 · 20:39")
# voir Allah : une phrase pour qu'aucun enfant ne comprenne « personne ne verra jamais Allah »
rep("Lorsqu'il se fut remis, il dit : « Gloire à Toi ! À Toi je me repens ; et je suis le premier des croyants. » | CORAN 7:143\n",
    "Lorsqu'il se fut remis, il dit : « Gloire à Toi ! À Toi je me repens ; et je suis le premier des croyants. » | CORAN 7:143\n"
    "N | [calm] Dans cette vie, personne ne peut voir Allah. Au Paradis, les croyants Le verront. | TAFSIR IBN KATHIR (7:143)\n")

# ---------------------------------------------------------------- IMAGE / SON
rep("@IMAGE Au lever du soleil : l'armée de Pharaon, des chars à perte de vue, soulève un nuage de poussière.",
    "@IMAGE Au lever du soleil : l'armée de Pharaon, des cavaliers à perte de vue, soulève un nuage de poussière.")
rep("@SON Grondement des chars, chevaux, trompes ; vagues ; cris.", "@SON Galop, chevaux, trompes ; vagues ; cris.")
rep("@IMAGE Pharaon lance ses chars dans les chemins de la mer ; toute l'armée s'y engouffre.",
    "@IMAGE Pharaon, à cheval, hésite au bord de la mer, puis son cheval s'élance dans les chemins de la mer ; toute l'armée s'y engouffre.")
rep("@SON Chars, puis un fracas d'eau immense, puis le silence des vagues.",
    "@SON Galop, puis un fracas d'eau immense, puis le silence des vagues.")
rep("au bout de la rue, un vieux mur penché qui va s'écrouler ; l'orbe verte le redresse pierre par pierre.",
    "au bout de la rue, un vieux mur penché qui va s'écrouler ; l'orbe verte s'en approche, et le mur se redresse, de bas en haut.")
rep("@IMAGE Le désert, un soir : la petite tente de Haroun ; son orbe s'éteint doucement ; l'orbe de Moussa près de lui ; le peuple en silence.",
    "@IMAGE Au flanc d'une montagne, un soir : l'orbe de Haroun s'éteint doucement ; l'orbe de Moussa près de lui.")

io.open(P, "w", encoding="utf-8").write(s)
print("corrections appliquées :", n_ok, "+ scène des douze sources déplacée en P21")
