# Temps de chaque mot des voix ElevenLabs (transcription du flux, 0 crédit) -> asr_CODE.json du moteur
# ({PERSO: [{t, s, e}]}) pour les 3 Shorts duo du 04/11/2026 (ISL8 fièvre, ISL9 eau glacée, ISL10 cauchemar).
# Flux ElevenLabs « Shorts duo islam 04-11 (fievre, eau glacee, cauchemar) » (Cg9mrhtypYiEN3eVgP80).
# Balises [..] retirées (même sur deux mots : « [long » « pause] »), ponctuation seule collée au mot voisin,
# ﷺ développé en « que la paix et le salut d'Allah soient sur lui ».
import json
import os
import re
import subprocess

SC = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL/scenarios"
BASE = "https://elevenlabsusercontent.com/database/workspace/4af90bdbfe834541ace57a9dac8d2dd1/content_generation/"
SAW = "que la paix et le salut d'Allah soient sur lui".split()
OUVRANTS = "«“(\"‘"

VOIX = [  # (code, perso, session, génération, signature)
    ("ISL8", "PETIT", "F8flTT4YMORFKMbkD6mT", "dV65gOW1PQHwuB4usONi", "56NKeXdAaY_2yhR2HvE1tHH_Zv8="),
    ("ISL8", "GRAND", "LaugakeFz0IpOTAfNQhH", "iuXveL7NQKsSsMdKtXHl", "ZJuIdB9UJtBkmgSY17a724lBJSs="),
    ("ISL9", "PETIT", "Ufqf0nlUYYMEwTEcQ5UB", "46cKXzYLY7ZMV2qpB8Ou", "R2EufB7Jj3TVdJyTp2vQZU--wsI="),
    ("ISL9", "GRAND", "kQf0X47T3bb92ECiL8SD", "Jf3pdzNYuWefysbEq1tc", "uhhkR0Be9QCHiXqwya1bbzC43DU="),
    ("ISL10", "PETIT", "5qSrvsyQju3vrvGj4AAX", "NuLp1WAEUcCEqEzY31Qv", "c9S-oMppC2X2c78Nv2GGA_1MrdM="),
    ("ISL10", "GRAND", "W4vNcfkpjT5INzSRewJy", "QzG39RvTkPW28Y7A8T4c", "vEGj39CmYS9VHmAFr19EQPC_3yY="),
]


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


par_code = {}
for (code, perso, sess, gen, sig) in VOIX:
    url = (BASE + f"{sess}/{gen}/words.json?response-content-disposition=attachment%3B%20filename%3D%22transcript-{gen}"
           f"-words.json%22&Expires=1793768400&KeyName=assets-cdn-key-1&Signature={sig}")
    r = subprocess.run(["curl", "-s", "-L", "-f", url], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"téléchargement impossible : {code} {perso}")
    d = json.loads(r.stdout.decode("utf-8"))
    ws = d.get("words", d) if isinstance(d, dict) else d
    mots = convertit(ws)
    par_code.setdefault(code, {})[perso] = mots
    print(f"{code} {perso:6s} {len(mots):3d} mots, fin {mots[-1]['e']:.2f} s : " + " ".join(m["t"] for m in mots)[:150])

for code, d in par_code.items():
    dst = os.path.join(SC, "voix_" + code.lower(), f"asr_{code}.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print("écrit :", dst)
