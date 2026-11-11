# Convertit les transcriptions ElevenLabs (temps de chaque mot des voix) au format du moteur : asr_E14PN.json
#   {VOIX: [{t, s, e}, ...]} — balises [..] retirées, ponctuation seule collée au mot voisin, ﷺ développé,
#   moitié B des parties 4 et 9 décalée à sa place dans le fichier recollé. Les voix réutilisées (parties 3 à 6)
#   viennent de asr_reutilisees.json (faster-whisper sur le PC) quand il existe.
#   python asr_conte.py <statut1.json> <statut2.json> ...
import difflib
import json
import os
import re
import subprocess
import sys
import unicodedata

D = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\FILM\EPISODE 14\voix_conte"
SC = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL\scenarios\film\ep14_conte"
SCR = os.path.dirname(os.path.abspath(__file__))
ENT = {"TITRE", "CODE", "THEME", "FORMAT", "CAMERA", "MUSIQUE", "VOIX", "PERSONNAGES", "QUEUE", "DUREE_FIN"}
SAW = "que la paix et le salut d'Allah soient sur lui".split()
OUVRANTS = "«“(\"‘"

sess = {}
for line in open(os.path.join(SCR, "sessions_asr.txt"), encoding="utf-8"):
    p = line.split()
    if len(p) == 2 and not line.startswith("#"):
        sess[p[1]] = p[0]
dec = json.load(open(os.path.join(SCR, "decalages_ab.json"), encoding="utf-8"))
attendu = {g["fichier"][:-4]: g["texte"] for g in json.load(open(os.path.join(SCR, "liste_voix.json"), encoding="utf-8"))}


def norm(x):
    x = re.sub(r"\[[^\]]*\]", " ", x).replace("ﷺ", " " + " ".join(SAW) + " ")
    x = unicodedata.normalize("NFD", x.lower())
    return "".join(ch for ch in x if ch.isalnum() and not unicodedata.combining(ch))


def convertit(words):
    out, dans_balise, prefixe = [], False, ""
    for w in words:
        if w.get("type", "word") != "word":
            continue
        t = w["text"].strip()
        if not t:
            continue
        if dans_balise:                                       # suite d'une balise sur plusieurs mots : [long pause]
            if "]" in t:
                dans_balise = False
                t = t.split("]", 1)[1].strip()
            if not t:
                continue
        t = re.sub(r"\[[^\]]*\]", "", t).strip()             # balises entières : [calm], [pause]…
        if "[" in t:
            dans_balise = True
            t = t.split("[", 1)[0].strip()
        if not t:
            continue
        s, e = float(w["start"]), float(w["end"])
        if t == "ﷺ":                                          # formule dite en entier par la voix
            n = len(SAW)
            for i, m in enumerate(SAW):
                out.append(dict(t=m, s=round(s + (e - s) * i / n, 3), e=round(s + (e - s) * (i + 1) / n, 3)))
            continue
        if not any(ch.isalnum() for ch in t):                 # ponctuation seule
            if t[0] in OUVRANTS:
                prefixe += t + " "
            elif out:
                out[-1]["t"] += " " + t if t[0] in "?!:;»”" else t
            continue
        out.append(dict(t=prefixe + t, s=round(s, 3), e=round(e, 3)))
        prefixe = ""
    return out


def lit_mots(tr):
    ws = tr.get("words") or []
    if len(ws) < (tr.get("word_count") or 0) and tr.get("words_download_url"):
        r = subprocess.run(["curl", "-s", "-L", "-f", tr["words_download_url"]], capture_output=True)
        d = json.loads(r.stdout.decode("utf-8"))
        ws = d.get("words", d) if isinstance(d, dict) else d
    return ws


conv, brut = {}, {}
for f in sys.argv[1:]:
    d = json.load(open(f, encoding="utf-8"))
    if not d.get("all_completed") or d.get("has_failures"):
        print("ATTENTION : statut incomplet dans", f)
    for tr in d.get("transcripts", []):
        s = tr["download_url"].split("/content_generation/")[1].split("/")[0]
        nom = sess.get(s)
        if not nom:
            print("session inconnue", s)
            continue
        ws = lit_mots(tr)
        brut[nom] = " ".join(w["text"] for w in ws)
        conv[nom] = convertit(ws)

# contrôles : texte identique à celui envoyé, même nombre de répliques, temps croissants
for nom, ws in sorted(conv.items()):
    att = attendu.get(nom)
    msg = []
    if att is not None:
        a, b = norm(" ".join(w["t"] for w in ws)), norm(att)
        if a != b:
            msg.append(f"texte {difflib.SequenceMatcher(None, a, b, autojunk=False).ratio():.3f}")
        if brut[nom].count("[long pause]") != att.count("[long pause]"):
            msg.append(f"répliques {brut[nom].count('[long pause]') + 1} au lieu de {att.count('[long pause]') + 1}")
    if any(ws[i]["s"] < ws[i - 1]["s"] - 0.001 for i in range(1, len(ws))):
        msg.append("temps non croissants")
    print(f"{nom:24s} {len(ws):4d} mots  fin {ws[-1]['e'] if ws else 0:7.2f} s  " + ("; ".join(msg) or "ok"))

reut = {}
p_reut = os.path.join(SCR, "asr_reutilisees.json")
if os.path.exists(p_reut):
    reut = json.load(open(p_reut, encoding="utf-8"))

manque_tout = []
for num in list(range(3, 15)) + list(range(16, 25)):
    code = f"E14P{num}"
    voix = []
    for line in open(os.path.join(SC, f"p{num:02d}.txt"), encoding="utf-8"):
        m = re.match(r"^([A-Z_0-9]+)\s*(?:\(([^)]*)\))?\s*:\s*(.+)$", line.strip())
        if m and m.group(1) not in ENT and m.group(1) not in voix:
            voix.append(m.group(1))
    asr, manque = {}, []
    for v in voix:
        k = f"{code}_{v}"
        if k in conv:
            asr[v] = conv[k]
        elif f"{k}_A" in conv and f"{k}_B" in conv:
            off = dec[code]["debut_B"]
            asr[v] = conv[f"{k}_A"] + [dict(t=w["t"], s=round(w["s"] + off, 3), e=round(w["e"] + off, 3))
                                        for w in conv[f"{k}_B"]]
        elif k in reut:
            asr[v] = reut[k]
        else:
            manque.append(k)
    if manque:
        json.dump(asr, open(os.path.join(SCR, f"asr_partiel_{code}.json"), "w", encoding="utf-8"), ensure_ascii=False)
        print(code, "MANQUE :", ", ".join(manque))
        manque_tout += manque
    else:
        json.dump(asr, open(os.path.join(D, f"asr_{code}.json"), "w", encoding="utf-8"), ensure_ascii=False)
        print(code, "asr écrit :", ", ".join(f"{v} ({len(asr[v])})" for v in voix))
json.dump(manque_tout, open(os.path.join(SCR, "asr_manquants.json"), "w", encoding="utf-8"))
