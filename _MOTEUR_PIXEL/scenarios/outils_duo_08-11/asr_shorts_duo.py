# Temps de chaque mot des voix ElevenLabs (transcription du flux, 0 crédit) -> asr_CODE.json du moteur
# ({PERSO: [{t, s, e}]}) pour les 9 Shorts duo du 08/11/2026 (ISL23 à ISL31).
# Entrées, à côté de ce fichier : transcriptions_08-11.json (réponse complète des transcriptions : {"transcripts":
# [{"generation_id": …, "words": [{text, start, end, type}]}]}) et gen_map.json ({generation_id: [code, perso]}).
# Balises [..] retirées (même sur deux mots : « [long » « pause] »), ponctuation seule collée au mot voisin,
# ﷺ développé en « que la paix et le salut d'Allah soient sur lui ». Ne réécrit jamais un asr existant.
import json
import os
import re
import sys

SC = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL/scenarios"
ICI = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ICI, "transcriptions_08-11.json")
GEN = json.load(open(os.path.join(ICI, "gen_map.json"), encoding="utf-8"))
SAW = "que la paix et le salut d'Allah soient sur lui".split()
OUVRANTS = "«“(\"‘"


def convertit(words):
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
        s, e = float(w["start"]), float(w["end"])
        if t.startswith("ﷺ"):                                   # « ﷺ » ou « ﷺ, » : développé, ponctuation gardée
            n = len(SAW)
            for i, m in enumerate(SAW):
                out.append(dict(t=m, s=round(s + (e - s) * i / n, 3), e=round(s + (e - s) * (i + 1) / n, 3)))
            if t[1:].strip():
                out[-1]["t"] += t[1:].strip()
            continue
        if not any(ch.isalnum() for ch in t):
            if t[0] in OUVRANTS:
                prefixe += t + " "
            elif out:
                out[-1]["t"] += " " + t if t[0] in "?!:;»”" else t
            continue
        out.append(dict(t=prefixe + t, s=round(s, 3), e=round(e, 3)))
        prefixe = ""
    return out


d = json.load(open(SRC, encoding="utf-8"))
par_code = {}
for tr in d["transcripts"]:
    code, perso = GEN[tr["generation_id"]]
    mots = convertit(tr["words"])
    par_code.setdefault(code, {})[perso] = mots
    print(f"{code} {perso:6s} {len(mots):3d} mots, fin {mots[-1]['e']:.2f} s : " + " ".join(m["t"] for m in mots)[:150])

REFAIRE = [a.upper() for a in sys.argv[2:]]                      # codes à réécrire exprès (ex. ISL22)
for code, dd in sorted(par_code.items()):
    dst = os.path.join(SC, "voix_" + code.lower(), f"asr_{code}.json")
    if os.path.exists(dst) and code not in REFAIRE:
        print("déjà là (non réécrit) :", dst)
        continue
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(dd, f, ensure_ascii=False, indent=1)
    print("écrit :", dst)
