# UN LOT DE SHORTS EN UNE COMMANDE (09/11/2026) — pour dépenser moins : une commande par étape pour TOUT le lot, un
# rapport court en texte, et les images à regarder réduites à une par Short.
#   python lot.py verifie  scenarios\islam_3*.txt     contrôles du texte, sans image (instantané) : durée, balises
#                                                     inconnues, citation sans source, accroche, passages sans mouvement
#   python lot.py planches scenarios\islam_3*.txt     verifie + UNE image par Short (« … - controle.png » : les 5
#                                                     premières secondes en détail, puis 1 image / s)
#   python lot.py voix     scenarios\islam_3*.txt     verifie + les textes à envoyer à ElevenLabs dans UN fichier, le
#                                                     coût en caractères, et le texte FIGÉ (toute modification
#                                                     ultérieure d'un mot dit sera signalée par « verifie »)
#   python lot.py rendu    scenarios\islam_3*.txt     rendu de chaque vidéo (l'ancienne version est renommée (vN),
#                                                     jamais écrasée) + contrôle final + copie légère ; à lancer en
#                                                     arrière-plan (≈ 8 min par Short)
#   python lot.py controle scenarios\islam_3*.txt     contrôle final seul, sur les vidéos déjà rendues
#   python lot.py livre    scenarios\islam_3*.txt     pose chaque vidéo finie dans ..\SHORTS A PUBLIER\<AAAA-MM-JJ>\ avec
#                                                     sa couverture et un .txt à côté (titre, description, hashtags,
#                                                     sources), pris dans scenarios\publication\<CODE>.txt ;
#                                                     rien n'est jamais écrasé ( --dossier "X" : un autre dossier )
#   python lot.py deja                                les sujets déjà faits et le prochain code libre (ISLnn)
# Chaque ligne du rapport : [OK] ou [A VOIR] ; « ! » = à corriger, « ? » = à regarder sur la planche.
import filecmp
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
MARQUE = "@@LOT@@"
FIGE = os.path.join(ICI, "scenarios", "_textes_figes.json")
LIVRAISONS = os.path.join(os.path.dirname(ICI), "SHORTS A PUBLIER")      # un sous-dossier par jour : 2026-11-09
PUBLICATION = os.path.join(ICI, "scenarios", "publication")              # <CODE>.txt : titre, description, hashtags
DUREE_MAX = 30.0
MARGE_VOIX = 2.5              # le pire écart « vraies voix − maquette » mesuré sur 42 Shorts (python estime.py mesure)
SCHEMA_DE_BASE = ("perso", "miroir", "photo", "compare", "icone", "chiffre", "texte", "fleche", "double-fleche",
                  "distance", "check", "croix", "source", "efface", "coran", "defile", "fond", "radio", "orteil",
                  "arbre", "feuilles", "balance", "compteur", "chrono", "lettres", "pov", "reflet", "ecume", "écume",
                  "vague", "propre", "rocher", "selfie", "photographe", "recule", "avance")


def _sans_accent(x):
    import unicodedata
    return "".join(ch for ch in unicodedata.normalize("NFD", x.lower()) if not unicodedata.combining(ch))


# ---------------------------------------------------------------- un scénario (dans son propre processus)
def _un(mode, path):
    sys.path.insert(0, ICI)
    os.chdir(ICI)
    import contextlib
    import io
    sys.argv = [os.path.join(ICI, "scenario.py")]
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon):
        import scenario as sc_
        import explique
        import briques
        import estime
        import kit
        head, blocs = sc_.lire(path)
        VID, nom, dossier, code, voix, repliques = sc_.fabrique(path)
    bavard = tampon.getvalue()
    D = VID.dlg
    R = dict(path=path, nom=nom, code=code, dossier=dossier, duree=round(float(D.dur), 1), err=[], voir=[],
             maquette="maquette" in bavard, moteur=[l_ for l_ in bavard.splitlines() if l_.startswith("(ligne")
                                                   or l_.startswith("briques :")])
    R["accroche"] = head.get("ACCROCHE", "")
    R["sources"] = list(dict.fromkeys(x for b in blocs for it in b["items"] if it["type"] == "ligne"
                                      for (_, cmd) in it.get("visuels", []) if cmd.lower().startswith("source")
                                      for x in re.findall(r'"([^"]+)"', cmd)))
    connues = set(SCHEMA_DE_BASE) | set(sc_.ANNOT) | set(sc_.GLOBAL) | set(explique.CLES_0411) \
        | set(explique.CLES_0411B) | set(explique.CLES_0611) | set(explique.CLES_0811) | set(explique.CLES_BRIQUES)
    actions = briques.connues()
    lignes = [it for b in blocs for it in b["items"] if it["type"] == "ligne"]
    R["repliques"] = len(lignes)
    # -- en-têtes
    if not head.get("ACCROCHE"):
        R["voir"].append("pas d'en-tête ACCROCHE (texte d'accroche de la 1re image)")
    if sc_.norm(head.get("DEMO", "")) in ("oui", "yes", "1", "vrai"):
        R["voir"].append("DEMO: oui (à enlever pour la vraie vidéo)")
    acc = (head.get("ACCROCHE", "") + " " + (lignes[0]["texte"] if lignes else "")).lower()
    if re.search(r"tu fais quoi|que fais-tu|tu ferais quoi", acc):
        R["voir"].append("accroche en forme de question : le format qui marche est la CONSIGNE (fais / ne fais jamais / dis ça)")
    # -- balises
    temps_evts, nb_balises, creees = [], 0, set()
    for k, it in enumerate(lignes):
        cles = []
        for (idx, cmd) in it.get("visuels", []):
            mots = cmd.split()
            if not mots:
                continue
            nb_balises += 1
            cle = mots[0].lower()
            cles.append(cle)
            temps_evts.append(float(explique.temps(D, k, idx)))
            if cle not in connues and _sans_accent(cle) not in connues:
                R["err"].append("ligne %d : balise inconnue {%s}" % (it["n"], cmd[:40]))
            if cle in actions:                                    # une brique : création avant toute action
                sous = _sans_accent(re.sub(r'"[^"]*"', " ", cmd[len(mots[0]):]).split()[0]) \
                    if re.sub(r'"[^"]*"', " ", cmd[len(mots[0]):]).split() else ""
                if actions[cle] and sous in actions[cle]:
                    if cle not in creees:
                        R["err"].append("ligne %d : {%s} avant la balise qui crée la brique {%s …}" % (it["n"], cmd[:40], cle))
                else:
                    creees.add(cle)
            if cle in ("etape", "étape") and re.search(r"\d\s*/\s*\d|partie", cmd.lower()):
                R["err"].append("ligne %d : numéro à l'écran interdit {%s}" % (it["n"], cmd[:40]))
            if cle == "texte" and '"' in cmd:                     # bandeau sur la scène : il descend sur les têtes
                principal, _, sous = re.search(r'"(.+)"', cmd).group(1).partition("//")
                n1 = len(explique.coupe(principal.strip(), 26))
                n2 = len(explique.coupe(sous.strip(), 32)) if sous.strip() else 0
                if n1 > 4 or n1 + n2 > 5:
                    R["voir"].append("ligne %d : bandeau {texte} de %d lignes%s : il descend sur la tête des persos → "
                                     "brique {citation …}" % (it["n"], n1, " + %d de sous-texte" % n2 if n2 else ""))
            if cle == "citation" and re.fullmatch(r'citation\s+qui\s+"[^"]*"\s*', cmd, re.I):
                R["voir"].append("ligne %d : {citation qui \"…\"} seule = une carte presque vide ; garder la scène et "
                                 "donner les deux textes dans la balise de la citation" % it["n"])
        if "«" in it["texte"] and "source" not in cles:
            R["voir"].append("ligne %d : citation « » sans {source \"…\"} sur la même réplique" % it["n"])
        if it["texte"].count("*") % 2:
            R["err"].append("ligne %d : une étoile * n'est pas refermée" % it["n"])
    if lignes and not lignes[0].get("visuels"):
        import pov
        if not (blocs and blocs[0]["decor"] in getattr(pov, "DECORS", {})):
            R["voir"].append("1re réplique sans aucune balise : rien de fort à l'image 0 (les 5 premières secondes décident)")
    R["balises"] = nb_balises
    # -- lisibilité des briques (cartes, listes, grilles…) : dessinées une fois ici, avant toute planche
    with contextlib.redirect_stdout(io.StringIO()):
        soucis = briques.controle()
    for grave, msg in soucis:
        R["err" if grave else "voir"].append(msg)
    # -- sources : un hadith hors des deux Sahih sans l'avis d'al-Arna'out / Ahmad Chakir dans la fiche
    try:
        import sources as src_
        R["voir"] += [msg for (_, msg) in src_.grades(code)]
    except Exception as e:                                        # la base des sources ne doit jamais bloquer un lot
        R["moteur"].append("sources.py grades : " + str(e)[:80])
    # -- voix : répliques mal retrouvées dans la transcription (calage des mots approximatif à cet endroit)
    for L_ in D.lines:
        if L_.get("retrouve") is not None and L_["retrouve"] < 0.5 and L_["k"] < len(lignes) \
                and len(lignes[L_["k"]]["texte"].split()) >= 4:      # une réplique de 2-3 mots se cale bien toute seule
            R["voir"].append("ligne %d : la transcription n'a retrouvé que %d %% de cette réplique (calage approximatif : "
                             "regarder la planche ici, ou refaire `asr`)" % (lignes[L_["k"]]["n"], int(100 * L_["retrouve"])))
    # -- durée, rythme (estimation : plans + balises ; le contrôle final mesure l'image réelle)
    court = getattr(VID, "fmt", "portrait") == "portrait" and not R["nom"].lower().startswith("demo")
    if R["duree"] > DUREE_MAX and court:
        R["err"].append("durée %.1f s : plus de %d s (resserrer le texte)" % (R["duree"], DUREE_MAX))
    elif R["maquette"] and court and R["duree"] > DUREE_MAX - MARGE_VOIX:
        R["voir"].append("durée estimée %.1f s : les vraies voix peuvent ajouter jusqu'à %.1f s → viser %.1f s ou moins "
                         "avant de payer les voix" % (R["duree"], MARGE_VOIX, DUREE_MAX - MARGE_VOIX))
    arabe_ = sum(estime.arabe(it["texte"])[0] for it in lignes)
    if arabe_:
        R["moteur"].append("arabe repéré : %d syllabes (comptées à part dans la durée)" % arabe_)
    evts = sorted(set([0.0] + [round(float(sh.t0), 2) for sh in VID.shots] + [round(t, 2) for t in temps_evts]
                      + [R["duree"]]))
    R["calmes"] = []                                             # information seulement : une balise peut s'animer seule
    for a, b in zip(evts, evts[1:]):
        if b - a > 6.0:
            R["voir"].append("%.1f → %.1f s : ni nouveau plan ni balise pendant %.1f s (passage figé ?)" % (a, b, b - a))
        elif b - a > 4.0:
            R["calmes"].append("%.1f→%.1f" % (a, b))
    # -- texte dit : coût des voix, texte figé
    dit = {}
    for b in blocs:
        for it in b["items"]:
            if it["type"] == "ligne":
                dit.setdefault(it["qui"], []).append(it.get("texte_voix", it["texte"]))
    R["caracteres"] = {q: sum(len(x) for x in v) + 13 * max(0, len(v) - 1) for q, v in dit.items()}
    R["empreinte"] = hashlib.sha1(json.dumps(dit, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    figes = json.load(open(FIGE, encoding="utf-8")) if os.path.exists(FIGE) else {}
    if code in figes and figes[code]["empreinte"] != R["empreinte"]:
        R["err"].append("le texte DIT a changé depuis qu'il a été figé le %s : voix à refaire, ou remettre l'ancien texte"
                        % figes[code]["date"])
    if mode == "voix":
        R["prompts"] = kit.prompts(repliques)
        R["voix"] = voix
    if mode == "planches":
        from PIL import Image, ImageDraw
        port = getattr(VID, "fmt", "portrait") == "portrait"
        tw, th = (144, 256) if port else (288, 162)
        n_acc = 10 if port else 5
        acc_ = [VID.frame(min(D.dur - 0.05, 0.05 + 0.5 * i)).resize((tw, th)) for i in range(n_acc)]
        tw2, th2, cols = (180, 320, 8) if port else (288, 162, 5)
        ts = [0.05 + i for i in range(int(D.dur) + 1) if 0.05 + i < D.dur]
        ims = [VID.frame(t).resize((tw2, th2)) for t in ts]
        rows = (len(ims) + cols - 1) // cols
        W = max(n_acc * tw, cols * tw2)
        pl = Image.new("RGB", (W, th + 26 + rows * th2), (0, 0, 0))
        d = ImageDraw.Draw(pl)
        for i, im in enumerate(acc_):
            pl.paste(im, (i * tw, 0))
            d.text((i * tw + 4, 4), "%.1f" % (0.05 + 0.5 * i), fill=(255, 255, 0))
        d.text((6, th + 6), "^ DEBUT : 0 a 5 s (2 images / s)        v TOUTE LA VIDEO (1 image / s)", fill=(255, 255, 255))
        for i, (t, im) in enumerate(zip(ts, ims)):
            pl.paste(im, ((i % cols) * tw2, th + 26 + (i // cols) * th2))
            d.text(((i % cols) * tw2 + 4, th + 30 + (i // cols) * th2), "%.1f" % t, fill=(255, 255, 0))
        R["planche"] = os.path.join(dossier, nom + " - controle.png")
        pl.save(R["planche"])
    print(MARQUE + json.dumps(R, ensure_ascii=False))


# ---------------------------------------------------------------- le lot
def _fichiers(args):
    out = []
    for a in args:
        trouve = sorted(glob.glob(a)) or sorted(glob.glob(os.path.join(ICI, a)))
        out += [os.path.abspath(f) for f in trouve if f.lower().endswith(".txt")]
    return list(dict.fromkeys(out))


def _lance(mode, path):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "_un", mode, path], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env, cwd=ICI)
    ligne = next((l_ for l_ in r.stdout.splitlines() if l_.startswith(MARQUE)), None)
    if ligne is None:
        fin = (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or ["erreur inconnue"])[-1]
        return dict(path=path, nom=os.path.basename(path), code="?", duree=0.0, repliques=0, balises=0, maquette=True,
                    err=["le moteur refuse ce scénario : " + fin[:200]], voir=[], moteur=[], caracteres={})
    return json.loads(ligne[len(MARQUE):])


def _affiche(R, extra=""):
    ok = not R["err"] and not R["voir"]
    car = " / ".join("%s %d c." % (q, n) for q, n in R.get("caracteres", {}).items())
    print("[%s] %-6s %-44s %5.1f s  %2d répliques  %2d balises  voix : %s  %s%s"
          % ("OK    " if ok else "A VOIR", R["code"], R["nom"][:44], R["duree"], R["repliques"], R["balises"],
             "maquette" if R["maquette"] else "vraies", car, extra))
    for x in R["err"]:
        print("     ! " + x)
    for x in R["voir"]:
        print("     ? " + x)
    for x in R.get("moteur", []):
        print("     · " + x)
    if R.get("calmes"):
        print("     · 4 à 6 s sans nouveau plan ni balise (à l'œil sur la planche) : " + ", ".join(R["calmes"]))


def _controle_video(vid, maquette):
    """Contrôle final d'une vidéo rendue → (ligne de résumé, liste des problèmes)."""
    sys.path.insert(0, ICI)
    import controle_video as cv
    d, (w, h), lufs, pic = cv.infos(vid)
    trous = cv.trous(vid, d)
    calmes, chg, dd = cv.rythme(vid)
    png = cv.planche(vid, w, h)
    out, mo = cv.leger(vid, d)
    pb = []
    cible = -20.0 if maquette else -14.0
    if h > w and d > DUREE_MAX + 0.05 and not os.path.basename(vid).lower().startswith("demo"):
        pb.append("durée %.1f s : plus de %d s" % (d, DUREE_MAX))
    if lufs is not None and abs(lufs - cible) > 2.0:
        pb.append("volume %.1f LUFS (cible %.0f)" % (lufs, cible))
    if trous and not maquette:                                    # une maquette sans voix a forcément des silences
        pb.append("%d trou(s) de son : %s" % (len(trous), trous[:8]))
    if calmes:
        pb.append("passages figés de plus de 4 s : %s" % calmes)
    return ("%.1f s, %s LUFS, %.1f changements d'image / s, copie légère %.1f Mo\n       planche : %s\n       légère  : %s"
            % (d, lufs, chg / max(1.0, dd), mo, png, out)), pb


def _copie(src, dst):
    """Copie sans jamais écraser : si un fichier différent porte déjà ce nom, la copie s'appelle « … (2) », « … (3) »."""
    if os.path.exists(dst):
        if filecmp.cmp(src, dst, shallow=False):
            return dst
        base, ext = os.path.splitext(dst)
        n = 2
        while os.path.exists("%s (%d)%s" % (base, n, ext)):
            n += 1
        dst = "%s (%d)%s" % (base, n, ext)
    shutil.copy2(src, dst)
    return dst


def _livre(R, f, dest):
    """Pose la vidéo finie, sa couverture et son texte de publication dans le dossier du jour."""
    vid = os.path.join(R.get("dossier", ""), R["nom"] + ".mp4")
    if R["err"] or not os.path.exists(vid):
        R["err"].append("pas livré : " + ("scénario à corriger" if R["err"] else "vidéo introuvable (%s)" % vid))
        return
    base = "%s - %s" % (R["code"], R["nom"])
    poses = [_copie(vid, os.path.join(dest, base + ".mp4"))]
    couv = os.path.join(os.path.dirname(f), R["nom"] + " - couverture short.jpg")
    if os.path.exists(couv):
        poses.append(_copie(couv, os.path.join(dest, base + " - couverture.jpg")))
    src = os.path.join(PUBLICATION, R["code"] + ".txt")
    sources = "\n\nSOURCES (affichées dans la vidéo) :\n" + " · ".join(R.get("sources", [])) if R.get("sources") else ""
    if os.path.exists(src):
        texte = open(src, encoding="utf-8-sig").read().rstrip() + sources + "\n"
    else:
        texte = ("TITRE :\n%s\n\nDESCRIPTION :\n(à écrire)\n\nHASHTAGS :\n(à écrire)%s\n"
                 % (R.get("accroche", "").replace(" / ", " ") or R["nom"], sources))
        R["voir"].append("texte de publication absent (scenarios\\publication\\%s.txt) : un modèle à remplir est posé" % R["code"])
    tmp = os.path.join(dest, "_" + base + ".tmp")
    open(tmp, "w", encoding="utf-8-sig").write(texte)             # avec BOM : le Bloc-notes affiche bien les accents
    poses.append(_copie(tmp, os.path.join(dest, base + ".txt")))
    os.remove(tmp)
    R.setdefault("moteur", []).append("posé : " + " | ".join(os.path.basename(p) for p in poses))


def _deja():
    """Les sujets déjà faits (un par ligne) et le prochain code libre : pour ne jamais refaire un sujet."""
    vus, maxi = [], 0
    for f in sorted(glob.glob(os.path.join(ICI, "scenarios", "*.txt"))):
        info = {}
        for l_ in open(f, encoding="utf-8-sig", errors="replace"):
            if l_.startswith("=="):
                break
            m = re.match(r"^(CODE|TITRE|ACCROCHE)\s*:\s*(.+)$", l_.strip())
            if m:
                info.setdefault(m.group(1), m.group(2).strip())
        code = info.get("CODE", "")
        if not code or not info.get("TITRE") or code.upper().startswith("DEMO"):
            continue
        m = re.match(r"([A-Za-z]+)(\d+)", code)
        vus.append(((m.group(1).upper(), int(m.group(2))) if m else (code.upper(), 0), code, info["TITRE"],
                    info.get("ACCROCHE", "")))
        if m and m.group(1).upper() == "ISL":
            maxi = max(maxi, int(m.group(2)))
    for _, code, titre, acc in sorted(vus):
        print("%-7s %-46s %s" % (code, titre[:46], acc[:60]))
    print("DÉJÀ FAITS : %d sujets — PROCHAIN CODE LIBRE : ISL%d" % (len(vus), maxi + 1))


def main():
    if len(sys.argv) >= 4 and sys.argv[1] == "_un":
        return _un(sys.argv[2], sys.argv[3])
    if len(sys.argv) >= 2 and sys.argv[1] == "deja":
        return _deja()
    if len(sys.argv) < 3 or sys.argv[1] not in ("verifie", "planches", "voix", "rendu", "controle", "livre"):
        raise SystemExit("python lot.py verifie | planches | voix | rendu | controle | livre  scenarios\\a.txt "
                         "scenarios\\b*.txt …   (ou : python lot.py deja)")
    mode, fichiers = sys.argv[1], _fichiers(sys.argv[2:])
    if not fichiers:
        raise SystemExit("aucun scénario trouvé")
    dest = None
    if mode == "livre":
        a = sys.argv[2:]
        dest = os.path.abspath(a[a.index("--dossier") + 1]) if "--dossier" in a and a.index("--dossier") + 1 < len(a) \
            else os.path.join(LIVRAISONS, time.strftime("%Y-%m-%d"))
        os.makedirs(dest, exist_ok=True)
    print("LOT : %d scénario(s) — %s" % (len(fichiers), mode))
    a_voir, total_car = 0, 0
    prompts = []
    figes = json.load(open(FIGE, encoding="utf-8")) if os.path.exists(FIGE) else {}
    for f in fichiers:
        R = _lance("planches" if mode == "planches" else "voix" if mode == "voix" else "verifie", f)
        extra = ""
        if mode in ("rendu", "controle") and not R["err"]:
            vid = os.path.join(R["dossier"], R["nom"] + ".mp4")
            if mode == "rendu":
                if os.path.exists(vid):                              # jamais d'écrasement d'une version déjà faite
                    n = 1
                    while os.path.exists(os.path.join(R["dossier"], "%s (v%d).mp4" % (R["nom"], n))):
                        n += 1
                    os.rename(vid, os.path.join(R["dossier"], "%s (v%d).mp4" % (R["nom"], n)))
                    extra = "  (ancienne version gardée : (v%d))" % n
                t0 = time.time()
                r = subprocess.run([sys.executable, os.path.join(ICI, "scenario.py"), f, "tout"], cwd=ICI,
                                   capture_output=True, text=True, errors="replace")
                if r.returncode or not os.path.exists(vid):
                    R["err"].append("le rendu a échoué : " + (r.stderr.strip().splitlines() or ["?"])[-1][:200])
                else:
                    extra += "  rendu en %d min" % round((time.time() - t0) / 60)
            if os.path.exists(vid) and not R["err"]:
                resume, pb = _controle_video(vid, R["maquette"])
                R["err"] += pb
                R.setdefault("moteur", []).append(resume)
            elif not R["err"]:
                R["err"].append("vidéo introuvable : " + vid)
        if mode == "livre":
            _livre(R, f, dest)
        _affiche(R, extra)
        if mode == "planches" and R.get("planche"):
            print("     image à regarder : " + R["planche"])
        if mode == "voix" and not R["err"]:
            figes[R["code"]] = dict(empreinte=R["empreinte"], date=time.strftime("%d/%m/%Y"), scenario=os.path.basename(f))
            for q, p in R.get("prompts", {}).items():
                prompts.append("===== %s — %s — %d caractères → %s\n%s\n" % (R["code"], q, len(p),
                               os.path.join(R["voix"], "%s_%s.mp3" % (R["code"], q)), p))
                total_car += len(p)
        a_voir += 1 if (R["err"] or R["voir"]) else 0
    if mode == "voix" and prompts:
        out = os.path.join(ICI, "scenarios", "Voix ElevenLabs - lot du %s.txt" % time.strftime("%d-%m-%Y"))
        open(out, "w", encoding="utf-8").write("\n".join(prompts))
        json.dump(figes, open(FIGE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("VOIX : %d générations, %d caractères (≈ %d crédits ElevenLabs) — textes : %s" % (len(prompts), total_car,
                                                                                                 total_car, out))
        print("       textes FIGÉS : toute modification d'un mot dit sera signalée par « python lot.py verifie ».")
    if mode == "livre":
        print("DOSSIER DU JOUR : " + dest)
    print("BILAN : %d sur %d à voir" % (a_voir, len(fichiers)) if a_voir else "BILAN : tout est OK (%d)" % len(fichiers))


if __name__ == "__main__":
    main()
