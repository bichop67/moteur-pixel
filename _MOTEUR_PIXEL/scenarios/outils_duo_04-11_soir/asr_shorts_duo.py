# Temps de chaque mot des voix ElevenLabs (transcription du flux, 0 crédit) -> asr_CODE.json du moteur
# ({PERSO: [{t, s, e}]}) pour les 6 Shorts duo du 04/11/2026 soir (ISL11 à ISL16).
# Flux ElevenLabs « Shorts duo islam 04-11 soir » (19YCz4hsVZHurRdqf62r). La réponse complète de la transcription
# (12 voix) est gardée à côté : transcriptions_04-11_soir.json.
# Balises [..] retirées (même sur deux mots : « [long » « pause] »), ponctuation seule collée au mot voisin,
# ﷺ développé en « que la paix et le salut d'Allah soient sur lui ».
import json
import os
import re
import sys

SC = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL/scenarios"
ICI = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ICI, "transcriptions_04-11_soir.json")
SAW = "que la paix et le salut d'Allah soient sur lui".split()
OUVRANTS = "«“(\"‘"

GEN = {  # génération de la transcription -> (code, perso)
    "qPPd9KM3Aqe1KcA1TROe": ("ISL11", "PETIT"), "drTL6HBDDT8SJstgLV9n": ("ISL11", "GRAND"),
    "clwIFPeOsQ58wCtRZnXw": ("ISL12", "PETIT"), "ozTM5ZaZB2HlTV20WQQK": ("ISL12", "GRAND"),
    "I443HAQiYgdyAy19t58X": ("ISL13", "PETIT"), "Rd1bXEq2XKgUb8woX7al": ("ISL13", "GRAND"),
    "JWWL18oAK4w5OYDzm1gy": ("ISL14", "PETIT"), "DX6GU1JV6NdLhYj84xXo": ("ISL14", "GRAND"),
    "p7SIwpSt1z6iSIHg984g": ("ISL15", "PETIT"), "OEQNBYoWc1tmZMHs14US": ("ISL15", "GRAND"),
    "5MnJdi1wP6YoIq6KIkdt": ("ISL16", "PETIT"), "gcNRv6H5tPdvanTwphZo": ("ISL16", "GRAND"),
}


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
        if t == "ﷺ":
            n = len(SAW)
            for i, m in enumerate(SAW):
                out.append(dict(t=m, s=round(s + (e - s) * i / n, 3), e=round(s + (e - s) * (i + 1) / n, 3)))
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
    print(f"{code} {perso:6s} {len(mots):3d} mots, fin {mots[-1]['e']:.2f} s : " + " ".join(m["t"] for m in mots)[:140])

for code, dd in sorted(par_code.items()):
    dst = os.path.join(SC, "voix_" + code.lower(), f"asr_{code}.json")
    if os.path.exists(dst):
        print("déjà là (non réécrit) :", dst)
        continue
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(dd, f, ensure_ascii=False, indent=1)
    print("écrit :", dst)
