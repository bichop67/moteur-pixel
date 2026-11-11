# UN FILM EN PLUSIEURS PARTIES, UNE SEULE COMMANDE (11/11/2026) — remplace la dizaine de petits scripts recopiés et
# adaptés à chaque film (asr_gog.py, planches_gog.py, file_rendu_gog.py, controle_final_gog.py…).
#
#   python fais_film.py <dossier des scénarios> <commande> [parties…] [options]
#
# Le dossier contient p01.txt, p02.txt… (un scénario par partie). Tout le reste se lit dans leurs en-têtes :
#   FILM: Gog et Magog                    titre du film entier (sinon : le début commun des TITRE)
#   CHAPITRE: La sortie de Gog et Magog   titre du chapitre YouTube (sinon : la fin du TITRE)
#   VOIX: FILM/<film>/voix                dossier des voix, à partir du dossier qui contient _MOTEUR_PIXEL (ou un
#                                         chemin complet) ; le dossier du film est son parent (livraison, planches)
#
# Commandes (sans numéro de partie : toutes les parties ; « 6 4 1 » : ces parties, dans cet ordre) :
#   etat          où en est chaque partie : voix, calage des mots, durée, rendue ou à refaire
#   voix          textes à générer sur ElevenLabs → voix\textes\voix.json + nombre de caractères (≈ crédits)
#   asr F.json…   transcriptions ElevenLabs (statut enregistré dans un fichier) → voix\asr_<CODE>.json
#                 (chaque transcription est reconnue par son texte : plus de table d'identifiants à tenir)
#   verifie       contrôle du cadre : foules, animations et personnages dessinés hors de l'image
#   planches      planche d'images de chaque partie avant le rendu   [--pas 4] [--de 20 --a 40]
#   brouillon     aperçu rapide qui bouge, avec le son, de chaque partie, puis du film entier
#   rendu         rendu des parties à la file (priorité basse, 4 processus) ; une partie déjà rendue et à jour est
#                 sautée sauf si on la nomme ; journal dans <film>\_source\rendu.log   [--coeurs 4]
#   assemble      film entier + copie légère   [--crf 23]
#   controle      durée, volume, crête, silences, chapitres (écrits dans <film>\chapitres.txt), planches du film
#   tout          verifie → rendu → assemble → controle
import contextlib
import ctypes
import difflib
import glob
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SAW = "que la paix et le salut d'Allah soient sur lui".split()
OUVRANTS = "«“(\"‘"
CRF_FILM = "23"              # mesuré le 11/11/2026 sur la scène la plus chargée de Gog et Magog (voir LISEZMOI, section 31)


# ---------------------------------------------------------------- le film : ses parties, ses dossiers
class Film:
    def __init__(s, dossier):
        import scenario
        s.scenarios = os.path.abspath(dossier)
        s.parties = []
        for p in sorted(glob.glob(os.path.join(s.scenarios, "p[0-9]*.txt"))):
            head = scenario.lire(p)[0]
            titre = head.get("TITRE", os.path.splitext(os.path.basename(p))[0])
            nom = "".join(ch for ch in unicodedata.normalize("NFD", titre) if not unicodedata.combining(ch))
            nom = re.sub(r"\s+", " ", re.sub(r"[^\w \-']", "", nom)).strip()      # même règle que scenario.fabrique
            code = head.get("CODE") or (re.sub(r"\W", "", nom.upper())[:10] or "SCENE")
            s.parties.append(dict(n=int(re.search(r"p(\d+)", os.path.basename(p)).group(1)), txt=p, titre=titre, nom=nom,
                                  code=code, voix=head.get("VOIX"), film=head.get("FILM"),
                                  chapitre=head.get("CHAPITRE") or titre.rsplit(" - ", 1)[-1],
                                  mp4=os.path.join(s.scenarios, nom + ".mp4")))
        if not s.parties:
            raise SystemExit(f"aucun scénario p01.txt, p02.txt… dans {s.scenarios}")
        s.titre = next((p["film"] for p in s.parties if p["film"]), None) \
            or re.split(r"\s+-\s+partie", os.path.commonprefix([p["titre"] for p in s.parties]))[0].strip(" -") or "Film"
        import pxv
        for p in s.parties:                              # « VOIX: FILM/<film>/voix » : à partir du dossier pxv.BASE
            if p["voix"] and not os.path.isabs(p["voix"]):
                p["voix"] = os.path.join(pxv.BASE, p["voix"])
        v = next((p["voix"] for p in s.parties if p["voix"]), None)
        s.voix = os.path.abspath(v) if v else os.path.join(s.scenarios, "voix")
        s.dossier = os.path.dirname(s.voix) if v else s.scenarios           # dossier de livraison du film
        s.sortie = os.path.join(s.dossier, f"{s.titre} - le film.mp4")
        s.source = os.path.join(s.dossier, "_source")

    def choisies(s, nums):
        if not nums:
            return list(s.parties)
        par_n = {p["n"]: p for p in s.parties}
        manque = [n for n in nums if n not in par_n]
        if manque:
            raise SystemExit(f"partie(s) inconnue(s) : {manque}")
        return [par_n[n] for n in nums]

    def fabrique(s, p):
        import scenario
        with contextlib.redirect_stdout(io.StringIO()):
            return scenario.fabrique(p["txt"])


def _signature(p):
    """Empreinte de ce qui fait la partie : le texte du scénario, ses voix et le calage de leurs mots."""
    import hashlib
    h = hashlib.sha1(open(p["txt"], "rb").read())
    if p["voix"]:
        for f in sorted(glob.glob(os.path.join(p["voix"], p["code"] + "_*.mp3"))
                        + glob.glob(os.path.join(p["voix"], "asr_" + p["code"] + ".json"))):
            h.update(f"{os.path.basename(f)}:{os.path.getsize(f)}".encode("utf-8"))
    return h.hexdigest()[:16]


def _a_jour(p):
    """La partie est rendue, et rien n'a changé depuis (scénario, voix). Une partie rendue avant ce suivi (sans trace
    à côté d'elle) est comparée par dates : un scénario réécrit à l'identique la fait passer pour « à refaire »."""
    if not os.path.exists(p["mp4"]):
        return False
    trace = p["mp4"][:-4] + ".rendu.txt"
    if os.path.exists(trace):
        return open(trace, encoding="utf-8").read().strip() == _signature(p)
    t = os.path.getmtime(p["mp4"])
    sources = [p["txt"]] + (glob.glob(os.path.join(p["voix"], p["code"] + "_*.mp3")) if p["voix"] else [])
    return all(os.path.getmtime(f) <= t for f in sources)


def _duree(vid):
    import assemble_film
    return assemble_film.duree_image(vid)


def _temps(t):
    return "%d:%02d" % (int(t) // 60, int(t) % 60)


def _priorite_basse(coeurs=4):
    """Priorité basse et `coeurs` processeurs seulement (les derniers) : le PC reste utilisable pendant le rendu."""
    try:
        k32 = ctypes.windll.kernel32
        k32.GetCurrentProcess.restype = ctypes.c_void_p
        k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        k32.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
        h = k32.GetCurrentProcess()
        k32.SetPriorityClass(h, 0x4000)                  # « inférieure à la normale » (0x40 = « inactive » : le rendu
        #                                                  n'avançait plus du tout dès qu'un autre rendu tournait)
        n = os.cpu_count() or 4
        coeurs = max(1, min(coeurs, n))
        k32.SetProcessAffinityMask(h, ((1 << coeurs) - 1) << (n - coeurs))
    except Exception:                                    # noqa: BLE001 (pas Windows : priorité normale)
        pass


def _journal(film, msg):
    os.makedirs(film.source, exist_ok=True)
    msg = time.strftime("%H:%M:%S ") + msg
    print(msg, flush=True)
    with open(os.path.join(film.source, "rendu.log"), "a", encoding="utf-8") as f:
        f.write(msg + "\n")


# ---------------------------------------------------------------- etat
def etat(film, parties, opt):
    print(f"FILM « {film.titre} » — {len(film.parties)} parties — livraison : {film.dossier}")
    total = 0.0
    for p in parties:
        VID, _, _, code, voix, repliques = film.fabrique(p)
        qui = list(dict.fromkeys(w for w, _ in repliques))
        v = voix if voix.endswith(("/", "\\")) else voix + "/"
        mp3 = [w for w in qui if os.path.exists(v + f"{code}_{w}.mp3")]
        asr = os.path.exists(v + f"asr_{code}.json")
        vraies = len(mp3) == len(qui) and asr
        total += VID.dlg.dur
        suivi = os.path.exists(p["mp4"][:-4] + ".rendu.txt")
        rendu_ = "rendue" if _a_jour(p) else "pas rendue" if not os.path.exists(p["mp4"]) else \
            ("À REFAIRE (scénario ou voix changés)" if suivi else "à vérifier (fichiers plus récents que le rendu)")
        print(f"  partie {p['n']:2d}  {code:8s} voix {len(mp3)}/{len(qui)}  mots {'oui' if asr else 'NON'}  "
              f"{VID.dlg.dur:6.1f} s{'' if vraies else ' (estimée)'}  {rendu_:12s}  {p['chapitre']}")
    print(f"  durée des parties choisies : {_temps(total)} (moins 1 s de fondu par enchaînement)")


# ---------------------------------------------------------------- voix : textes pour ElevenLabs
def voix(film, parties, opt):
    import kit
    out, total = {}, 0
    for p in parties:
        _, _, _, code, _, repliques = film.fabrique(p)
        for w, txt in kit.prompts(repliques).items():
            out[f"{code}_{w}"] = txt
            total += len(txt)
            print(f"  {code}_{w:16s} {len(txt):5d} caractères" + ("   ATTENTION : plus de 4 300, à couper en deux moitiés A/B"
                                                                  if len(txt) > 4300 else ""))
    d = os.path.join(film.voix, "textes")
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, "voix.json")
    ancien = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
    ancien.update(out)
    json.dump(ancien, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(out)} générations, {total} caractères (≈ {total} crédits ElevenLabs) → {f}")


# ---------------------------------------------------------------- asr : transcriptions ElevenLabs → asr_<CODE>.json
def _norm(x):
    x = re.sub(r"\[[^\]]*\]", " ", x).replace("ﷺ", " " + " ".join(SAW) + " ")
    x = unicodedata.normalize("NFD", x.lower())
    return "".join(ch for ch in x if ch.isalnum() and not unicodedata.combining(ch))


def _convertit(words):
    """Mots d'ElevenLabs → mots du moteur : balises [dark] retirées, ponctuation recollée, ﷺ développé."""
    out, dans_balise, prefixe = [], False, ""
    for w in words:
        if w.get("type", "word") != "word":
            continue
        t = w["text"].strip()
        if not t:
            continue
        if dans_balise:
            if "]" in t:
                dans_balise = False
                t = t.split("]", 1)[1].strip()
            if not t:
                continue
        t = re.sub(r"\[[^\]]*\]", "", t).strip()
        if "[" in t:
            dans_balise = True
            t = t.split("[", 1)[0].strip()
        if not t:
            continue
        s_, e_ = float(w["start"]), float(w["end"])
        if t == "ﷺ":
            n = len(SAW)
            for i, m in enumerate(SAW):
                out.append(dict(t=m, s=round(s_ + (e_ - s_) * i / n, 3), e=round(s_ + (e_ - s_) * (i + 1) / n, 3)))
            continue
        if not any(ch.isalnum() for ch in t):
            if t[0] in OUVRANTS:
                prefixe += t + " "
            elif out:
                out[-1]["t"] += " " + t if t[0] in "?!:;»”" else t
            continue
        out.append(dict(t=prefixe + t, s=round(s_, 3), e=round(e_, 3)))
        prefixe = ""
    return out


def _mots(tr):
    ws = tr.get("words") or []
    if len(ws) < (tr.get("word_count") or 0) and tr.get("words_download_url"):
        r = subprocess.run(["curl", "-s", "-L", "-f", tr["words_download_url"]], capture_output=True)
        d = json.loads(r.stdout.decode("utf-8"))
        ws = d.get("words", d) if isinstance(d, dict) else d
    return ws


def _charge(f):
    brut = open(f, encoding="utf-8").read()
    try:
        d = json.loads(brut)
    except ValueError:
        d = json.loads(brut[brut.index("{"):brut.rindex("}") + 1])
    if isinstance(d, list):                              # enveloppe [{type: text, text: "..."}]
        d = json.loads(d[0]["text"])
    return d


def asr(film, parties, opt):
    f = os.path.join(film.voix, "textes", "voix.json")
    if not os.path.exists(f):
        raise SystemExit("lancer d'abord « voix » (il manque voix\\textes\\voix.json)")
    attendu = {k: _norm(v) for k, v in json.load(open(f, encoding="utf-8")).items()}
    conv = {}
    for fichier in opt["fichiers"]:
        d = _charge(fichier)
        if not d.get("all_completed") or d.get("has_failures"):
            print("ATTENTION : statut incomplet dans", fichier)
        for tr in d.get("transcripts", []):
            ws = _convertit(_mots(tr))
            dit = _norm(" ".join(w["t"] for w in ws))
            if not dit:
                continue
            # la transcription est reconnue par son texte : celle des voix attendues qui lui ressemble le plus
            pres = sorted(attendu, key=lambda k: abs(len(attendu[k]) - len(dit)))[:6]
            nom, r = max(((k, difflib.SequenceMatcher(None, dit, attendu[k], autojunk=False).ratio()) for k in pres),
                         key=lambda x: x[1])
            if r < 0.9:
                print(f"transcription non reconnue (meilleure ressemblance {r:.2f} avec {nom}) : « {dit[:60]}… »")
                continue
            msg = [] if dit == attendu[nom] else [f"texte {r:.3f}"]
            if any(ws[i]["s"] < ws[i - 1]["s"] - 0.001 for i in range(1, len(ws))):
                msg.append("temps non croissants")
            conv[nom] = ws
            print(f"  {nom:24s} {len(ws):4d} mots  fin {ws[-1]['e']:7.2f} s  " + ("; ".join(msg) or "ok"))
    for p in parties:
        code = p["code"]
        qui = sorted(k[len(code) + 1:] for k in attendu if k.startswith(code + "_"))
        cible = os.path.join(film.voix, f"asr_{code}.json")
        deja = json.load(open(cible, encoding="utf-8")) if os.path.exists(cible) else {}
        deja.update({v: conv[f"{code}_{v}"] for v in qui if f"{code}_{v}" in conv})
        manque = [v for v in qui if v not in deja]
        if manque:
            print(f"  {code} : il manque la transcription de {', '.join(manque)}")
            continue
        if any(f"{code}_{v}" in conv for v in qui):
            json.dump(deja, open(cible, "w", encoding="utf-8"), ensure_ascii=False)
            print(f"  {code} : asr écrit ({', '.join(qui)})")


# ---------------------------------------------------------------- verifie : contrôle du cadre
def verifie(film, parties, opt):
    import controle_cadre
    soucis = 0
    for p in parties:
        VID = film.fabrique(p)[0]
        msgs = controle_cadre.examine(VID)
        soucis += len(msgs)
        print(f"partie {p['n']} ({VID.dlg.dur:.0f} s) :", "tout ce qui est dessiné se voit" if not msgs else "", flush=True)
        for m in msgs:
            print("   ", m)
    return soucis


# ---------------------------------------------------------------- planches
def planches(film, parties, opt):
    from PIL import Image, ImageDraw, ImageFont
    pas, t_min, t_max = float(opt.get("pas", 4.0)), float(opt.get("de", 0.0)), float(opt.get("a", 1e9))
    police = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 18)
    os.makedirs(os.path.join(film.dossier, "planches"), exist_ok=True)
    for p in parties:
        V = film.fabrique(p)[0]
        fin = min(t_max, V.shots[-1].t1)
        ts, t = [], max(t_min, 0.4)
        while t < fin:
            ts.append(t)
            t += pas
        larg, haut, col = (640, 360, 3) if V.W > V.H else (270, 480, 6)
        g = Image.new("RGB", (col * larg, ((len(ts) + col - 1) // col) * haut), (0, 0, 0))
        for i, t in enumerate(ts):
            im = V.frame(t).convert("RGB").resize((larg, haut), Image.LANCZOS)
            ImageDraw.Draw(im).text((8, 4), f"{t:.1f} s", fill=(255, 255, 0), font=police, stroke_width=2, stroke_fill=(0, 0, 0))
            g.paste(im, ((i % col) * larg, (i // col) * haut))
        out = os.path.join(film.dossier, "planches",
                           f"p{p['n']:02d}" + ("" if t_min == 0 and t_max > 1e8 else f"_{int(t_min)}") + ".png")
        g.save(out)
        print(f"partie {p['n']} : {V.shots[-1].t1:.1f} s, {len(ts)} images → {out}", flush=True)


# ---------------------------------------------------------------- brouillon, rendu
def _lance(film, parties, mode, coeurs):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    faits = []
    for p in parties:
        t = time.time()
        sig = _signature(p)                              # relevée AVANT le rendu (une retouche pendant le rendu se verra)
        _journal(film, f"partie {p['n']} : {mode}, début")
        r = subprocess.run([sys.executable, "scenario.py", p["txt"], mode, str(coeurs)], cwd=HERE, env=env,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        fin = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][-2:]
        _journal(film, f"partie {p['n']} : fin en {(time.time() - t) / 60:.1f} min, code {r.returncode} | " + " | ".join(fin))
        for d in glob.glob(os.path.join(os.environ.get("TEMP", "."), "ia501", p["nom"].replace(" ", "_") + "_frames")):
            shutil.rmtree(d, ignore_errors=True)         # images temporaires de la partie (plusieurs Go)
        if r.returncode:
            raise SystemExit(f"partie {p['n']} : échec, voir {os.path.join(film.source, 'rendu.log')}")
        if mode == "tout":                               # trace du rendu : de quoi la partie a été faite
            open(p["mp4"][:-4] + ".rendu.txt", "w", encoding="utf-8").write(sig)
        faits.append(p)
    return faits


def brouillon(film, parties, opt):
    import pxv
    coeurs = int(opt.get("coeurs", 4))
    _priorite_basse(coeurs)
    _lance(film, parties, "brouillon", coeurs)
    vids = [os.path.join(film.scenarios, p["nom"] + " (brouillon).mp4") for p in parties]
    if len(vids) > 1:                                    # le film entier, parties bout à bout (coupes franches : brouillon)
        liste = os.path.join(film.source, "brouillon.txt")
        open(liste, "w", encoding="utf-8").write("".join("file '%s'\n" % v.replace("\\", "/").replace("'", "'\\''") for v in vids))
        out = os.path.join(film.dossier, f"{film.titre} - le film (brouillon).mp4")
        subprocess.run([pxv.FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", liste,
                        "-c", "copy", "-movflags", "+faststart", out], check=True)
        print(f"film en brouillon : {out} ({os.path.getsize(out) / 1e6:.0f} Mo, {_temps(_duree(out) * 3)})")
    else:
        print("brouillon :", vids[0])


def rendu(film, parties, opt):
    coeurs = int(opt.get("coeurs", 4))
    _priorite_basse(coeurs)
    if not opt["nums"]:                                  # tout le film : on ne refait pas ce qui est à jour
        saute = [p["n"] for p in parties if _a_jour(p)]
        parties = [p for p in parties if p["n"] not in saute]
        if saute:
            print("déjà rendues et à jour (sautées) :", saute)
    _lance(film, parties, "tout", coeurs)
    _journal(film, "file terminée")


# ---------------------------------------------------------------- assemble, controle
def assemble(film, parties, opt):
    manque = [p["n"] for p in film.parties if not os.path.exists(p["mp4"])]
    vieux = [p["n"] for p in film.parties if os.path.exists(p["mp4"]) and not _a_jour(p)]
    if manque:
        raise SystemExit(f"parties pas encore rendues : {manque}")
    if vieux:
        print("ATTENTION, parties rendues AVANT la dernière retouche de leur scénario ou de leurs voix :", vieux)
    if os.path.exists(film.sortie):                      # jamais d'écrasement d'une version déjà livrée
        n = 1
        while os.path.exists(film.sortie[:-4] + f" (v{n}).mp4"):
            n += 1
        os.rename(film.sortie, film.sortie[:-4] + f" (v{n}).mp4")
        leger = film.sortie[:-4] + " (leger).mp4"
        if os.path.exists(leger):
            os.rename(leger, film.sortie[:-4] + f" (v{n}) (leger).mp4")
        print(f"l'ancienne version est gardée sous « (v{n}) »")
    _priorite_basse(int(opt.get("coeurs", 4)))
    subprocess.run([sys.executable, "assemble_film.py", film.sortie] + [p["mp4"] for p in film.parties]
                   + ["--crf", str(opt.get("crf", CRF_FILM)), "--leger"], cwd=HERE, check=True,
                   env=dict(os.environ, PYTHONIOENCODING="utf-8"))


def controle(film, parties, opt):
    import pxv
    from PIL import Image, ImageDraw, ImageFont
    V = film.sortie
    if not os.path.exists(V):
        raise SystemExit("le film n'est pas assemblé : " + V)
    t, chap = 0.0, []
    for p in film.parties:
        chap.append(f"{_temps(t)} {p['chapitre']}")
        t += _duree(p["mp4"]) - 1.0
    total = _duree(V)
    print(f"durée du film : {int(total) // 60} min {int(total) % 60:02d} s ({os.path.getsize(V) / 1e6:.0f} Mo, "
          f"{os.path.getsize(V) * 8 / total / 1e6:.1f} Mbit/s)")
    print("\n".join(chap))
    open(os.path.join(film.dossier, "chapitres.txt"), "w", encoding="utf-8").write("\n".join(chap) + "\n")
    r = subprocess.run([pxv.FF, "-hide_banner", "-nostats", "-i", V, "-map", "0:a", "-af",
                        "ebur128=peak=true,silencedetect=noise=-45dB:d=2.5", "-f", "null", "-"],
                       capture_output=True, text=True, errors="ignore").stderr
    print("volume :", re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1], "LUFS ; crête réelle :",
          re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1], "dBTP")
    print("silences > 2,5 s :", [(round(float(a), 1), round(float(b), 1)) for a, b in
                                 zip(re.findall(r"silence_start: ([\d.]+)", r), re.findall(r"silence_end: ([\d.]+)", r))])
    police = ImageFont.truetype("C:/Windows/Fonts/tahomabd.ttf", 15)
    os.makedirs(os.path.join(film.dossier, "planches"), exist_ok=True)
    ts = [0.3 + 6 * i for i in range(int(total // 6) + 1)] + [total - 8, total - 5, total - 3, total - 1.6, total - 0.4]
    tmp = os.path.join(os.environ.get("TEMP", "."), "film_qa.png")
    col, larg, haut, par_page = 6, 320, 180, 60
    for pg in range((len(ts) + par_page - 1) // par_page):
        lot = ts[pg * par_page:(pg + 1) * par_page]
        g = Image.new("RGB", (col * larg, ((len(lot) + col - 1) // col) * haut))
        for i, tt in enumerate(lot):
            subprocess.run([pxv.FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{max(0, tt):.2f}", "-i", V,
                            "-frames:v", "1", "-vf", f"scale={larg}:{haut}", tmp])
            im = Image.open(tmp).convert("RGB")
            ImageDraw.Draw(im).text((4, 2), _temps(tt), fill=(255, 255, 0), font=police, stroke_width=2, stroke_fill=(0, 0, 0))
            g.paste(im, ((i % col) * larg, (i // col) * haut))
        out = os.path.join(film.dossier, "planches", f"film_final_{pg + 1}.png")
        g.save(out)
        print("planche :", out)


def tout(film, parties, opt):
    if verifie(film, film.parties, opt):
        raise SystemExit("des éléments sont dessinés hors de l'image : corriger, ou lancer « rendu » pour passer outre")
    rendu(film, film.parties, dict(opt, nums=[]))
    assemble(film, film.parties, opt)
    controle(film, film.parties, opt)


COMMANDES = dict(etat=etat, voix=voix, asr=asr, verifie=verifie, planches=planches, brouillon=brouillon, rendu=rendu,
                 assemble=assemble, controle=controle, tout=tout)


def main():
    if len(sys.argv) < 3 or sys.argv[2] not in COMMANDES:
        raise SystemExit("python fais_film.py <dossier des scénarios> " + " | ".join(COMMANDES) + " [parties…] [--pas 4] "
                         "[--de 20 --a 40] [--coeurs 4] [--crf 23]")
    dossier, cmd, reste = sys.argv[1], sys.argv[2], sys.argv[3:]
    opt, nums, fichiers = {}, [], []
    i = 0
    while i < len(reste):
        if reste[i].startswith("--") and i + 1 < len(reste):
            opt[reste[i][2:]] = reste[i + 1]
            i += 2
            continue
        (nums if reste[i].isdigit() else fichiers).append(int(reste[i]) if reste[i].isdigit() else reste[i])
        i += 1
    opt.update(nums=nums, fichiers=fichiers)
    os.chdir(HERE)
    sys.argv = [os.path.join(HERE, "scenario.py")]
    film = Film(dossier)
    r = COMMANDES[cmd](film, film.choisies(nums), opt)
    sys.exit(1 if (cmd == "verifie" and r) else 0)


if __name__ == "__main__":
    main()
