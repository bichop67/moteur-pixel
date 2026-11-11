# BASE DES SOURCES DÉJÀ VÉRIFIÉES (09/11/2026) — pour ne JAMAIS revérifier dans Chrome un hadith ou un verset déjà
# contrôlé pour un autre Short (la vérification dans le navigateur est ce qui coûte le plus cher après les animations).
#   python sources.py                       refait sources\sources_verifiees.md (index) et les fiches manquantes
#   python sources.py cherche "boukhari 163"    où cette source a déjà été vérifiée, avec les lignes de la fiche
#   python sources.py grades [ISL44]            hadiths hors des deux Sahih sans l'avis d'al-Arna'out / Ahmad Chakir
# Une FICHE par Short : sources\fiches\<CODE>.md (texte exact, grade, date de vérification, décisions religieuses,
# relectures). Pour les Shorts d'avant le 09/11, la fiche est la copie de l'en-tête du scénario (1re ligne
# « copie automatique ») ; pour les nouveaux, Claude écrit la fiche à la main et le scénario ne garde que 3 à 6 lignes
# d'en-tête. Le relecteur religieux lit la fiche ; la fabrication ne lit que le scénario.
import glob
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER = os.path.join(ICI, "sources")
FICHES = os.path.join(DOSSIER, "fiches")
INDEX = os.path.join(DOSSIER, "sources_verifiees.md")
AUTO = "<!-- copie automatique de l'en-tête du scénario : ne pas modifier ici, modifier le scénario -->"
NOMS = [("Boukhari", r"boukhari|bukhari"), ("Mouslim", r"mouslim|muslim"),
        ("Abou Dawoud", r"abou\s+dawoud|abu\s*dawud|abudawud"), ("Tirmidhi", r"(?:at-)?tirmidhi"),
        ("Nasa'i", r"nasa['’]?i"), ("Ibn Majah", r"ibn\s*majah"), ("Ahmad", r"ahmad"),
        ("Mouwatta", r"mouwatta|muwatta"), ("Riyad as-Salihin", r"riyad\s+as-salihin|riyadussalihin"),
        ("Coran", r"coran|quran")]
REF = re.compile(r"(?<!charh )\b(%s)\s*:?\s*((?:\d+(?::\d+)?[a-z]?(?:-\d+)?)(?!\s*/)(?:\s*,\s*\d+[a-z]?(?![\d/:]))*)"
                 % "|".join(p for _, p in NOMS), re.I)


def _nom(brut):
    for nom, p in NOMS:
        if re.fullmatch(p, brut.strip(), re.I):
            return nom
    return brut.title()


def _refs(texte):
    out = set()
    for m in REF.finditer(texte):
        for num in re.split(r"\s*,\s*", m.group(2)):
            out.add((_nom(m.group(1)), num.lower()))
    return out


def _entete(path):
    """(code, titre, lignes de commentaire du début du scénario, sans le « # »)."""
    code = titre = None
    notes = []
    debut = True
    for raw in open(path, encoding="utf-8-sig"):
        l_ = raw.rstrip("\n")
        if debut and l_.startswith("#"):
            notes.append(l_[1:].strip() if l_[1:2] != " " else l_[2:].rstrip())
            continue
        if l_.strip():
            debut = False
        m = re.match(r"^(CODE|TITRE)\s*:\s*(.+)$", l_.strip())
        if m and m.group(1) == "CODE":
            code = m.group(2).strip()
        elif m:
            titre = m.group(2).strip()
        if l_.startswith("=="):
            break
    return code, titre, notes


def _cle_num(n):
    m = re.match(r"(\d+)(?::(\d+))?", n)
    return (int(m.group(1)), int(m.group(2) or 0), n) if m else (10 ** 9, 0, n)


def refait():
    os.makedirs(FICHES, exist_ok=True)
    neuves = 0
    for path in sorted(glob.glob(os.path.join(ICI, "scenarios", "*.txt"))):
        code, titre, notes = _entete(path)
        if not code or not re.search(r"sunnah\.com|v[ée]rifi", "\n".join(notes), re.I):
            continue
        fiche = os.path.join(FICHES, code + ".md")
        if os.path.exists(fiche) and AUTO not in open(fiche, encoding="utf-8").read(300):
            continue                                              # fiche écrite à la main : on n'y touche pas
        open(fiche, "w", encoding="utf-8").write("%s\n# %s — %s\nScénario : scenarios\\%s\n\n%s\n"
                                                 % (AUTO, code, titre or "", os.path.basename(path), "\n".join(notes)))
        neuves += 1
    index = {}
    for fiche in sorted(glob.glob(os.path.join(FICHES, "*.md"))):
        code = os.path.splitext(os.path.basename(fiche))[0]
        txt = open(fiche, encoding="utf-8").read()
        d = re.search(r"v[ée]rifi[^\n]*?(\d{2}/\d{2}/\d{4})", txt, re.I)
        for ref in _refs(txt):
            index.setdefault(ref, []).append("%s (%s)" % (code, d.group(1) if d else "date ?"))
    lignes = ["# Sources déjà vérifiées (index)", "",
              "Refait par `python sources.py` à partir des fiches `sources\\fiches\\<CODE>.md`. AVANT de vérifier une",
              "source dans Chrome : `python sources.py cherche \"boukhari 163\"`. Si elle est ici, lire la fiche (texte",
              "exact, grade, décisions) et ne vérifier dans le navigateur QUE ce qui manque. Une source reprise d'une",
              "fiche garde sa date de vérification ; un texte NOUVEAU tiré de la même source se vérifie quand même.", ""]
    for nom, _ in NOMS:
        refs = sorted((r for r in index if r[0] == nom), key=lambda r: _cle_num(r[1]))
        if refs:
            lignes.append("## " + nom)
            lignes += ["- %s %s : %s" % (nom, n, ", ".join(sorted(set(index[(nom, n)])))) for (_, n) in refs]
            lignes.append("")
    open(INDEX, "w", encoding="utf-8").write("\n".join(lignes))
    print("OK : %d fiches (%d refaites), %d sources dans l'index -> %s"
          % (len(glob.glob(os.path.join(FICHES, "*.md"))), neuves, len(index), INDEX))


HORS_SAHIH = ("Abou Dawoud", "Tirmidhi", "Nasa'i", "Ibn Majah", "Ahmad", "Mouwatta")
AVIS = re.compile(r"arna['’ʾ]?o?u[tṭ]|chakir|shakir", re.I)


def grades(code=None):
    """Hadiths hors de Boukhari et Mouslim dont la fiche ne donne l'avis NI d'al-Arna'out NI d'Ahmad Chakir.
    Leçon du 10/11/2026 (Tirmidhi 3563, « hasan (Darussalam) » sur sunnah.com, chaîne faible chez ces deux-là : Short
    écrit puis écarté). À lancer AVANT d'écrire le scénario. Renvoie [(code, message)] ; code=None : toutes les fiches
    écrites à la main."""
    out = []
    for fiche in sorted(glob.glob(os.path.join(FICHES, "*.md"))):
        c = os.path.splitext(os.path.basename(fiche))[0]
        if code and c.upper() != code.upper():
            continue
        txt = open(fiche, encoding="utf-8").read()
        if AUTO in txt[:300] and not code:
            continue                                              # copie d'un ancien en-tête : pas une fiche de travail
        refs = sorted(r for r in _refs(txt) if r[0] in HORS_SAHIH)
        if refs and not AVIS.search(txt):
            out.append((c, "%s : hors des deux Sahih, et la fiche ne donne l'avis ni d'al-Arna'out ni d'Ahmad Chakir "
                           "(dorar.net) → à regarder avant d'écrire, puis à noter dans sources\\fiches\\%s.md"
                        % (", ".join("%s %s" % r for r in refs), c)))
    return out


def cherche(quoi):
    cibles = _refs(quoi)
    if not cibles:
        raise SystemExit("écrire par exemple : python sources.py cherche \"boukhari 163\"")
    trouve = False
    for fiche in sorted(glob.glob(os.path.join(FICHES, "*.md"))):
        txt = open(fiche, encoding="utf-8").read()
        if not (cibles & _refs(txt)):
            continue
        trouve = True
        lignes = txt.splitlines()
        print("=== %s  (%s)" % (os.path.basename(fiche), lignes[1][2:] if len(lignes) > 1 else ""))
        vus = set()
        for i, l_ in enumerate(lignes):
            if cibles & _refs(l_):
                for j in range(i, min(len(lignes), i + 3)):       # la ligne et les 2 suivantes (le texte continue souvent)
                    if j not in vus:
                        vus.add(j)
                        print("  " + lignes[j][:420])
    if not trouve:
        print("pas encore vérifiée : à vérifier dans Chrome (sunnah.com), puis à noter dans la fiche du Short")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "cherche":
        cherche(" ".join(sys.argv[2:]))
    elif len(sys.argv) > 1 and sys.argv[1] == "grades":
        manque = grades(sys.argv[2] if len(sys.argv) > 2 else None)
        for c, msg in manque:
            print("? %s — %s" % (c, msg))
        print("%d fiche(s) à compléter" % len(manque) if manque else "OK : chaque hadith hors des deux Sahih a son avis")
    else:
        refait()
        for c, msg in grades():
            print("? %s — %s" % (c, msg))
