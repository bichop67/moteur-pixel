# DURÉE ESTIMÉE D'UNE RÉPLIQUE AVANT LES VOIX (11/11/2026) — pour que la maquette annonce la bonne durée du Short.
# L'ancienne règle (15 caractères par seconde pour tout) se trompait dans les deux sens : ≈ 3 s de trop sur un Short
# ordinaire, ≈ 3 s de moins quand Grand dit une longue formule en arabe (3 Shorts sur 6 au-dessus de 30 s le 09/11).
# Ici : le français et l'arabe translittéré sont comptés à part, avec les vitesses MESURÉES sur les vraies voix
# (Lucas = PETIT, Quentin = GRAND). Refaire la mesure après quelques lots : python estime.py mesure
#   estime.duree("GRAND", "Dis : « Bismillahi awwalahou wa akhirah ».")  -> secondes, ou None (voix inconnue)
#   estime.arabe("…")  -> (syllabes d'arabe, caractères du reste, mots d'arabe repérés)
import re
import unicodedata

# vitesses mesurées le 11/11/2026 sur 263 répliques de 42 Shorts (voix non accélérées) : voir `python estime.py mesure`
VITESSES = dict(GRAND=dict(car=19.0, syl=3.6, fixe=0.45), PETIT=dict(car=17.5, syl=4.6, fixe=0.45))
SON = 0.5                                        # un [laughs] / [gasps] / [sighs]… en plus du texte
MARGE = 1.5                                      # incertitude sur un Short entier (secondes) : voir lot.py verifie

_ELISION = re.compile(r"^(l|d|j|n|s|t|qu|c|m|jusqu|lorsqu|puisqu|aujourd)['’]")
_PARTICULES = set("wa la bi min fi ma ya an inna illa li ila lam wala houwa anta kulli koulli ala anna in man "
                  "ilaha lahou lak laka lah".split())
_MARQUE = re.compile(r"llah|kh|dh|gh|aa|ou[a-z]*ou|"
                     r"(ahou|ihi|ika|ouka|ouna|ina|oun|ati|atou|ani|anna|ouhou|aka|iya|awa|ayka|ihim|ahoum|akoum|"
                     r"ikoum|ih|ah|an|ou)$|^(al|ach|as|ar|an|at|adh|az|ad|ch|r|t|s|n|l)-")
_FRANCAIS = set("""le les un une des de du et ou a au aux en dans sur sous pour par avec sans que qui quoi dont ce cet
cette ces il elle on nous vous ils elles je tu me te se ne pas plus est es suis sont as ai ont dis dit fais fait mon ton
son ta sa mes tes ses si mais donc car ni comme tout tous toute quand alors oui non ca c y tres bien meme prophete
dire cela ici voila apres avant jamais toujours encore deja aussi rien peut peux doit dois faut va vas vais main mains
dieu nom chaque fois jour nuit bouche homme femme coeur ame porte toi moi lui eux leur leurs notre votre nos vos ah oh
maman papa plan dedans ou vraiment maintenant pourtant tant autant avant devant pendant enfant grand quand comment
sinon pardon cadeau cou fou sou chou genou bijou hibou trou bout debout beaucoup coup loup nous vous tout partout
surtout sais""".split())


def _plat(x):
    x = unicodedata.normalize("NFD", x.lower())
    return "".join(ch for ch in x if not unicodedata.combining(ch))


def _mots(txt):
    txt = re.sub(r"\[[^\]]*\]|\{[^}]*\}", " ", txt).replace("*", "").replace("ﷺ", " ")
    return re.findall(r"[^\s«»\"“”.,;:!?…()/]+", txt)


def _genre(mot):
    """'A' : arabe sûr ; 'p' : petit mot arabe (wa, la, bi…) ; 'F' : français ; '?' : on ne sait pas."""
    p = _plat(mot).strip("'’-")
    if not p or p.isdigit():
        return "F"
    if p in _PARTICULES:
        return "p"
    if re.search(r"[éèêçàùœ]", mot.lower()) or _ELISION.match(_plat(mot)) or p in _FRANCAIS:
        return "F"
    if "'" in p or "’" in p or _MARQUE.search(p):
        return "A"
    return "?"


def arabe(txt):
    """Repère les passages d'arabe translittéré : au moins deux mots sûrs qui se suivent (petits mots et un mot
    inconnu isolé permis entre eux). Renvoie (syllabes d'arabe, caractères du reste, mots repérés)."""
    ms = _mots(txt)
    g = [_genre(m) for m in ms]
    n = len(ms)
    pris = [False] * n
    i = 0
    while i < n:
        if g[i] not in "Ap":
            i += 1
            continue
        j, dernier, surs = i, None, 0
        while j < n:
            if g[j] == "A":
                surs += 1
                dernier = j
            elif g[j] == "p":
                pass
            elif g[j] == "?" and j + 1 < n and g[j + 1] in "Ap" and j > i:
                pass
            else:
                break
            j += 1
        if surs >= 2:
            for k in range(i, dernier + 1):           # jusqu'au dernier mot sûr (pas le « wa », « an » qui traîne)
                pris[k] = True
            i = j
        else:
            i += 1
    syl = sum(max(1, len(re.findall(r"[aeiouy]+", _plat(m)))) for m, a in zip(ms, pris) if a)
    reste = sum(len(m) + 1 for m, a in zip(ms, pris) if not a)
    return syl, reste, [m for m, a in zip(ms, pris) if a]


def _voix(who):
    w = str(who).upper()
    return VITESSES.get(w)


def duree(who, texte, texte_voix=None):
    """Durée probable de la réplique dite par `who`, ou None si on ne connaît pas la vitesse de cette voix."""
    v = _voix(who)
    if v is None:
        return None
    syl, reste, _ = arabe(texte)
    reste += texte.count("ﷺ") * 45                # ﷺ est lu en entier par ElevenLabs
    sons = len(re.findall(r"\[(?:laughs|gasps|sighs|exhales|chuckles|clears throat|crying|sobbing)[^\]]*\]",
                          texte_voix or ""))
    return max(0.8, v["fixe"] + reste / v["car"] + syl / v["syl"] + SON * sons)


# ------------------------------------------------------------------ mesure sur les vraies voix
def _mesure():
    """Relit tous les Shorts qui ont de vraies voix et compare : ancienne règle, règle actuelle, meilleur réglage."""
    import contextlib
    import glob
    import io
    import json
    import os
    import subprocess
    import sys
    ici = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) > 2 and sys.argv[2] == "_un":
        path = sys.argv[3]
        sys.argv = [os.path.join(ici, "scenario.py")]
        tampon = io.StringIO()
        with contextlib.redirect_stdout(tampon):
            import scenario as sc
            head, blocs = sc.lire(path)
            VID, nom, dossier, code, voix, repliques = sc.fabrique(path)
        if "maquette" in tampon.getvalue() or os.path.isdir(os.path.join(voix, "originaux")):
            return                                # pas de vraies voix, ou voix accélérées après coup : pas une mesure
        dits = [(it["qui"], it.get("texte_voix", it["texte"]), it["texte"]) for b in blocs for it in b["items"]
                if it["type"] == "ligne"]
        print("@@" + json.dumps([dict(code=code, who=L["who"], dur=round(L["t1"] - L["t0"], 3), voix=v, txt=t)
                                 for L, (_, v, t) in zip(VID.dlg.lines, dits)], ensure_ascii=False))
        return
    import numpy as np
    from concurrent.futures import ThreadPoolExecutor

    def un(f):
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "mesure", "_un", f], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", cwd=ici,
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        l_ = next((x for x in r.stdout.splitlines() if x.startswith("@@")), None)
        return json.loads(l_[2:]) if l_ else []
    with ThreadPoolExecutor(5) as ex:
        rows = [x for res in ex.map(un, sorted(glob.glob(os.path.join(ici, "scenarios", "islam_*.txt")))) for x in res]
    print("%d répliques de %d Shorts (vraies voix, non accélérées)" % (len(rows), len({r["code"] for r in rows})))
    if "--voir" in sys.argv:
        for r in rows:
            a = arabe(r["txt"])[2]
            if a:
                print("  %-6s %-5s %4.1f s | %s" % (r["code"], r["who"], r["dur"], " ".join(a)))
    for who in sorted({r["who"] for r in rows}):
        R = [r for r in rows if r["who"] == who]
        y = np.array([r["dur"] for r in R])
        vieux = np.array([max(0.8, (len(r["txt"].replace("*", "")) + r["txt"].count("ﷺ") * 45) / 15.0) for r in R])
        neuf = np.array([duree(who, r["txt"], r["voix"]) or 0.0 for r in R])
        A = np.array([[arabe(r["txt"])[1] + r["txt"].count("ﷺ") * 45, arabe(r["txt"])[0], 1.0] for r in R])
        sol = np.linalg.lstsq(A, y, rcond=None)[0]
        print("%-6s %3d répliques | ancienne règle : %+.2f s en moyenne, écart %.2f | règle actuelle : %+.2f, écart %.2f"
              " | meilleur réglage : car=%.1f syl=%.1f fixe=%.2f"
              % (who, len(R), (vieux - y).mean(), np.abs(vieux - y).mean(), (neuf - y).mean(), np.abs(neuf - y).mean(),
                 1 / sol[0], (1 / sol[1]) if sol[1] > 1e-6 else 0.0, sol[2]))
    par = {}
    for r in rows:
        v = par.setdefault(r["code"], [0.0, 0.0, 0.0])
        v[0] += r["dur"]
        v[1] += max(0.8, (len(r["txt"].replace("*", "")) + r["txt"].count("ﷺ") * 45) / 15.0)
        v[2] += duree(r["who"], r["txt"], r["voix"]) or 0.0
    e_v = np.array([v[1] - v[0] for v in par.values()])
    e_n = np.array([v[2] - v[0] for v in par.values()])
    print("par Short : ancienne règle %+.1f s en moyenne (de %+.1f à %+.1f) | règle actuelle %+.1f s (de %+.1f à %+.1f)"
          % (e_v.mean(), e_v.min(), e_v.max(), e_n.mean(), e_n.min(), e_n.max()))


if __name__ == "__main__":
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] == "mesure":
        _mesure()
    else:
        for _t in _sys.argv[1:]:
            print(arabe(_t), {w: round(duree(w, _t), 1) for w in VITESSES})
