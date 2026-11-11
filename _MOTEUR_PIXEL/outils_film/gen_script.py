"""Fabrique le fichier ElevenLabs de l'épisode 14 à partir de ep14_source.txt (et un résumé des longueurs)."""
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
SRC, OUT = sys.argv[1], sys.argv[2]
VOIX = {"N": "NARRATEUR", "C": "CORAN"}

parts, cur, scene = [], None, None
for raw in io.open(SRC, encoding="utf-8"):
    line = raw.rstrip("\n")
    if not line.strip() or line.startswith("#"):
        continue
    if line.startswith("==="):
        num, titre, mus = [x.strip() for x in line[3:].split("|")]
        cur = dict(num=num, titre=titre, musique=mus, scenes=[])
        parts.append(cur)
        continue
    if line.startswith("@SCENE"):
        scene = dict(nom=line[6:].strip(), image="", son="", lignes=[])
        cur["scenes"].append(scene)
        continue
    if line.startswith("@IMAGE"):
        scene["image"] = line[6:].strip()
        continue
    if line.startswith("@SON"):
        scene["son"] = line[4:].strip()
        continue
    f = [x.strip() for x in line.split("|")]
    qui = VOIX.get(f[0], f[0])
    scene["lignes"].append(dict(qui=qui, txt=f[1], ref=f[2] if len(f) > 2 else ""))


def dit(t):
    """Texte envoyé à ElevenLabs : sans les étoiles des mots en jaune."""
    return t.replace("*", "")


def mots(t):
    """Mots prononcés (sans balises ni étoiles)."""
    t = re.sub(r"\[[^\]]+\]", " ", t.replace("*", ""))
    return len(re.findall(r"[\wÀ-ÿ'’-]+", t))


cpt = {}
for p in parts:
    for s in p["scenes"]:
        for l in s["lignes"]:
            pre = {"NARRATEUR": "N", "CORAN": "C"}.get(l["qui"], l["qui"][:3])
            cpt[pre] = cpt.get(pre, 0) + 1
            l["id"] = f"{pre}{cpt[pre]:02d}"
total_mots = sum(mots(l["txt"]) for p in parts for s in p["scenes"] for l in s["lignes"])
json.dump(parts, open("ep14_parts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

DESC = {
    "NARRATEUR": "ID Qrl71rx6Yg8RvyPYRGCQ, la même voix que les épisodes précédents",
    "CORAN": "ID aQROLel5sQbj1vuIVi6B (Voix Nicolas Petit), la même à chaque épisode : calme, solennelle, lente, [calm] seulement",
    "PHARAON": "homme mûr, voix grave, froide et orgueilleuse",
    "DEVIN": "vieil homme mystérieux, voix rauque et lente",
    "VIEILLARD": "vieil homme des fils d'Israël, voix douce et fatiguée",
    "CONSEILLERS": "notable égyptien, voix assurée et inquiète",
    "SERVANTE": "jeune femme égyptienne, voix vive",
    "GARDE": "homme du palais, voix dure et méfiante",
    "EGYPTIEN": "homme brutal et moqueur",
    "DELATEUR": "homme essoufflé, qui crie",
    "ISRAELITE": "homme effrayé, voix tremblante",
    "MESSAGER": "homme pressé, qui chuchote un avertissement",
    "MAGICIENS": "chef des magiciens (parle au nom de tous), voix grave, d'abord arrogante puis apaisée",
    "HERAUT": "crieur de Pharaon, voix forte",
    "FILS_D_ISRAEL": "un homme du peuple (parle au nom de tous), voix qui change : peur, colère, moquerie, plainte",
    "CROYANT": "homme mûr de la famille de Pharaon, voix posée, sage et courageuse",
    "SAMIRI": "homme maigre, voix insinuante",
    "DEUX_HOMMES": "homme pieux, voix ferme et confiante",
    "QAROUN": "homme riche, voix grasse et méprisante",
    "GENS": "gens du peuple (au nom de tous), voix ordinaire",
    "SAGES": "homme savant, voix calme et grave",
}

o = []
w = o.append
w("L'HISTOIRE DES PROPHÈTES — FILM, ÉPISODE 14")
w("L'HISTOIRE DU PROPHÈTE MOUSSA — du fleuve à la dune rouge (toute l'histoire, du début à la fin)")
w("=" * 78)
w("RÈGLES DE CET ÉPISODE")
w("=" * 78)
for r in [
    "- FORMAT FILM / CONTE (demandes du 01/11/2026 : « raconté vraiment comme une histoire », « cinématique, digne d'un film de cinéma »,",
    "  « toute l'histoire, même si c'est 40 minutes », « des personnages qui parlent entre eux ») : narration au présent, scène par scène,",
    "  sans leçon ni aparté. Les récits des savants d'autrefois (Ibn Kathir, At-Tabari, le long récit d'Ibn 'Abbas rapporté par an-Nasa'i)",
    "  sont racontés comme l'histoire ; une seule phrase d'ouverture le dit ; leur référence s'affiche en haut à droite, jamais lue.",
    "- UN SEUL FILM, TOUTE L'HISTOIRE (« même si le film dure 1 heure ») : de la naissance de Moussa à sa mort, en 24 parties.",
    "- Laissé de côté : la gifle donnée par Moussa à l'ange de la mort (Boukhari 3407, authentique) : elle demande l'explication des savants",
    "  (l'ange était venu sous l'apparence d'un homme) ; le récit garde l'essentiel (le taureau, « et ensuite ? », « alors maintenant »).",
    "- Images : moteur pixel (_MOTEUR_PIXEL), 16:9, scènes animées. Sous-titres oui (mot important en jaune). Pas de titre de chapitre.",
    "- JAMAIS DESSINÉS, JAMAIS DOUBLÉS (orbes avec leur nom) : MOUSSA (bébé, enfant, adulte), HAROUN, la MÈRE de Moussa, sa SŒUR, ASIYA,",
    "  MARYAM (évoquée), le VIEIL HOMME de Madyan (beaucoup disaient que c'était le prophète Chou'ayb), ses DEUX FILLES (dont la future femme",
    "  de Moussa), YAQOUB et YOUSSOUF (souvenir). Leurs paroles du Coran : VOIX DU CORAN ; leurs paroles rapportées par les savants : le narrateur.",
    "  Allah n'est jamais représenté : sur la montagne, on voit seulement l'arbre et sa lumière.",
    "- DOUBLÉS (personnages ordinaires, une voix chacun) : Pharaon, le devin, un vieil homme des fils d'Israël, les conseillers de Pharaon,",
    "  une servante, un garde, l'Égyptien de la bagarre, l'Égyptien qui dénonce, l'homme des fils d'Israël, l'homme qui accourt ;",
    "  puis les magiciens, le crieur, des fils d'Israël, l'homme croyant de la famille de Pharaon, le Samiri, Qaroun, des gens de son",
    "  peuple, les sages. Youcha' (5:23, 18:60-64) est prophète : orbe, jamais doublé ; le verset des deux hommes (5:23) est lu en entier",
    "  par la voix du Coran.",
    "  Leurs répliques viennent du Coran ou des récits des savants (référence affichée) ; aucune parole inventée.",
    "- Ce qui n'est pas montré : aucune mise à mort (fondu, plan de réaction). Aucun détail venu seulement de la Bible.",
    "- Versets : traduction de Hamidullah (quran.com/fr) mot pour mot. Retouches : Moïse → Moussa, Hâmân → Haman, Aaron → Haroun,",
    "  Tuwâ → Touwa ; crochets et parenthèses explicatives retirés, en gardant les mots quand la phrase en a besoin (28:7 « [ceci] » retiré ;",
    "  28:9 « Cet enfant » ; 28:12 « le sein », « Elle dit donc » ; 28:15 « Moussa dit », « du Diable » ; 28:19 et 28:25 « il dit » ;",
    "  28:20 « Quitte la ville » ; 28:21 « ce peuple » ; 28:23 « leurs bêtes » ; 28:24 « les bêtes » ; 28:26 « à ton service » ; 28:27 « dix",
    "  années » ; 28:28 « C'est conclu…, dit Moussa » ; 28:33 « dit Moussa » ; 28:35 « Nos signes » ; 20:14 « divinité véritable », « la prière » ;",
    "  20:18 « les arbres » ; 20:19, 20:21, 20:36 « Allah (lui) dit » ; 20:25 « Moussa dit »). Coquilles de l'édition en ligne corrigées :",
    "  28:10 « devient » → « devint » ; 28:18 « grand cris » → « grands cris » ; 20:14 « laprière » → « la prière ».",
    "  Versets du même moment non lus, pour ne pas répéter la scène : 20:10-11 et 27:7-12 (l'appel est lu avec 28:29-35 et 20:12-36).",
    "  Parties 10 à 24 : mêmes règles (Moïse → Moussa, Aaron → Haroun, Coré → Qaroun, « le Samaritain (Sâmirî) » → « le Samiri » ; crochets et",
    "  parenthèses retirés, mots gardés quand la phrase en a besoin ; « [Moïse] dit » → « Moussa dit », « [Allah] dit » → « Allah dit »).",
    "  Dans les répliques jouées par Pharaon, les incises « dit Pharaon » sont retirées (la voix du Coran ou le narrateur annonce qui parle).",
    "  Coquilles corrigées : 20:59 « matiné » → « matinée » ; 10:90 « inimité » → « inimitié », « je suis nombre » → « je suis du nombre » ;",
    "  18:72 et 18:75 « dis » → « dit » ; 18:73 « prend » → « prends » ; 28:81 « pût » → « put » ; 44:24 « voués » → « vouées ».",
    "  Extraits (coupes) : 2:55, 2:57, 2:60, 2:61, 5:20-21, 7:126, 7:130-131, 7:144-145, 7:155, 20:73, 40:39-41, 40:45, 66:11.",
    "- La formule ﷺ est dite deux fois : à la première mention du Prophète (hadith d'Asiya, P4) et au début de la fin (P24, la dune",
    "  rouge) ; partout ailleurs « le Prophète ».",
    "- Les références ne sont jamais lues : elles s'affichent à l'écran. Colle chaque bloc entre les ===== dans ElevenLabs (Eleven v4) avec la voix",
    "  indiquée, garde les lignes vides entre les répliques ; un fichier MP3 par bloc, avec le nom indiqué.",
]:
    w(r)
w("")
w("CASTING")
voix_cnt = {}
for p in parts:
    for s in p["scenes"]:
        for l in s["lignes"]:
            voix_cnt[l["qui"]] = voix_cnt.get(l["qui"], 0) + 1
import os
CAST = {}
_cj = os.path.join(os.path.dirname(os.path.abspath(OUT)), "_source", "casting.json")
if os.path.exists(_cj):
    CAST = {k: v for k, v in json.load(open(_cj, encoding="utf-8")).items() if not k.startswith("_")}
for v, n in voix_cnt.items():
    vid = f" — voix ElevenLabs : {CAST[v][1]}, ID {CAST[v][0]}" if v in CAST else ""
    w(f"- {v} : {DESC.get(v, '')}{vid} — {n} réplique(s)")
w("")
for p in parts:
    code = "E14" + p["num"]
    blocs = {}
    for s in p["scenes"]:
        for l in s["lignes"]:
            blocs.setdefault(l["qui"], []).append(l)
    for v, ls in blocs.items():
        corps = "\n\n".join(dit(l["txt"]) for l in ls)
        w("=" * 78)
        vid = f" (ID {CAST[v][0]})" if v in CAST else ""
        w(f"VOIX : {v}{vid} — {p['num']} : {p['titre']}   ({len(corps)} caractères)   → fichier : {code}_{v}.mp3")
        w("=" * 78)
        w(corps)
        w("")
w("=" * 78)
w("DÉCOUPAGE DU FILM : SCÈNES, ORDRE DE MONTAGE, SON, RÉFÉRENCES À L'ÉCRAN (pour Claude, ne pas coller dans ElevenLabs)")
w("=" * 78)
for p in parts:
    w("")
    w(f"■■ {p['num']} — {p['titre']}   (musique : {p['musique']})")
    for s in p["scenes"]:
        w(f"■ {s['nom']}")
        w(f"IMAGE : {s['image']}")
        w(f"SON : {s['son']}")
        for l in s["lignes"]:
            w(f"{l['id']} {l['qui']} — {dit(l['txt'])}")
            if l["ref"]:
                w(f"     ÉCRAN : {l['ref']}")
w("")
mn = total_mots / 155
w(f"TOTAL : {sum(voix_cnt.values())} répliques, environ {total_mots} mots de voix, soit environ {mn:.0f} minutes de voix "
  f"(+ plans muets, respirations et fondus : environ {mn * 1.12:.0f} minutes de film).")
io.open(OUT, "w", encoding="utf-8", newline="\r\n").write("\n".join(o) + "\n")

print("mots", total_mots, "= %.1f min de voix" % mn)
for p in parts:
    ls = [l for s in p["scenes"] for l in s["lignes"]]
    m = sum(mots(l["txt"]) for l in ls)
    ch = {}
    for l in ls:
        ch[l["qui"]] = ch.get(l["qui"], 0) + len(dit(l["txt"])) + 2
    print(p["num"], p["titre"], "|", m, "mots = %.1f min" % (m / 155), "|", ", ".join(f"{k}:{v}" for k, v in ch.items()))
tot = {}
for p in parts:
    for s in p["scenes"]:
        for l in s["lignes"]:
            tot[l["qui"]] = tot.get(l["qui"], 0) + len(dit(l["txt"]))
print("caracteres par voix :", tot, "total", sum(tot.values()))
