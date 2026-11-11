# Textes définitifs (après relecture indépendante du 30/10/2026) des 5 Shorts dialogue.
T = {
 "VOP01": ["PGPGPGPG", [
  "Ma sœur fait ses ablutions avec du vernis… sa prière est valable ?",
  "Non. Le vernis fait une couche : l'eau ne touche pas l'ongle.",
  "Pour un petit ongle ?",
  "Les savants s'appuient sur un hadith : un homme avait laissé sur son pied une partie sèche, grande comme un ongle. Le Prophète ﷺ lui a dit : retourne, et refais bien tes ablutions.",
  "Donc elle doit tout enlever ?",
  "Avant chaque ablution, oui. Ou alors, elle fait ses ablutions d'abord, et elle met le vernis après.",
  "Et elle peut prier avec ?",
  "Tant qu'elle garde ses ablutions, oui. Abonne-toi pour la suite."]],
 "VOP07": ["PGPGPGPGPG", [
  "J'ai éclaté de rire pendant la prière… elle compte encore ?",
  "Si tu as ri avec du bruit, et que tu pouvais te retenir : non, elle est annulée. Tu la recommences.",
  "Tout le monde est d'accord ?",
  "Ibn al-Moundhir rapporte que les savants sont unanimes : le rire avec du bruit annule la prière.",
  "Et si je pouvais pas m'arrêter ?",
  "Beaucoup de savants disent que tu es excusé. Mais ne te laisse pas aller.",
  "Et si j'ai juste souri ?",
  "Le sourire, lui, ne l'annule pas, pour la plupart des savants.",
  "C'est mon pote qui m'a fait rire !",
  "Alors pense à Celui devant qui tu te tiens… et prie loin de lui. Abonne-toi pour la suite."]],
 "VOP04": ["PGPGGPGPG", [
  "Je me suis réveillé après l'heure de la prière… c'est fichu ?",
  "Non. Tu la pries tout de suite, dès que tu te réveilles.",
  "Mais l'heure est passée !",
  "Le Prophète ﷺ a dit : celui qui oublie une prière, ou qui dort et la rate, qu'il la prie dès qu'il s'en souvient.",
  "Et le Prophète ﷺ a dit aussi : il n'y a pas de négligence dans le sommeil.",
  "Donc je peux dormir tranquille ?",
  "La négligence, c'est quand tu es réveillé et que tu laisses passer l'heure. Et pour les savants, celui qui ne prend aucune précaution n'a plus d'excuse.",
  "Donc…",
  "Mets ton réveil. Abonne-toi pour la suite."]],
 "VOP08": ["PGPGPGPG", [
  "Mon pote a un tatouage… sa prière est valable ?",
  "Pour la plupart des savants, oui. L'encre est sous la peau : l'eau des ablutions touche bien sa peau.",
  "Alors il peut en refaire un ?",
  "Non ! Le Prophète ﷺ a dit : Allah a maudit la tatoueuse et celle qui se fait tatouer. Et les savants disent : pareil pour les hommes.",
  "Et celui qu'il a déjà ?",
  "Il se repent sincèrement. Pour les chaféites et d'autres savants, s'il peut l'enlever sans danger, il l'enlève. Si ça abîme sa peau, il n'est pas obligé.",
  "Je lui dis direct.",
  "Avec douceur. Abonne-toi pour la suite."]],
 "VOP09": ["PGPGPGPGPG", [
  "Faux ongles, henné, maquillage… pour les ablutions, c'est valable ou pas ?",
  "Pour les savants, la règle est simple : si l'eau ne touche pas la peau ou l'ongle, les ablutions ne sont pas complètes.",
  "Les faux ongles ?",
  "Pas valable : collés sur l'ongle, l'eau ne passe pas. Il faut les enlever avant les ablutions.",
  "Le henné ?",
  "Valable. C'est une couleur, pas une couche. Enlève juste bien la pâte.",
  "Et le maquillage waterproof ?",
  "Le waterproof fait souvent une couche : on l'enlève avant. Une simple couleur, comme le khôl, ça passe.",
  "Donc la règle…",
  "Couleur : ça passe. Couche : on enlève. Abonne-toi pour la suite."]],
}


def prompts(sk):
    order, texts = T[sk]
    p = [t for w, t in zip(order, texts) if w == "P"]
    g = [t for w, t in zip(order, texts) if w == "G"]
    return " [long pause] ".join(p), " [long pause] ".join(g), order.count("P"), order.count("G")


if __name__ == "__main__":
    import sys
    p, g, np_, ng = prompts(sys.argv[1])
    print(np_, ng); print(p); print(g)
