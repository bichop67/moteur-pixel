# Télécharge les voix ElevenLabs des 6 Shorts duo du 07/11/2026 dans scenarios\voix_islNN\CODE_PERSO.mp3.
# Flux ElevenLabs « Shorts duo islam 07-11 (consignes : …) » (5ZF98cbHA05qS9lOZLdM).
# Les liens (content_url) sont dans voix_urls.json, à côté de ce fichier : [{"code": "ISL17", "perso": "PETIT",
# "url": "https://…"}, …]. Ne réécrit jamais un fichier existant.
import json
import os
import subprocess

SC = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL/scenarios"
ICI = os.path.dirname(os.path.abspath(__file__))

for v in json.load(open(os.path.join(ICI, "voix_urls.json"), encoding="utf-8")):
    code, perso = v["code"], v["perso"]
    dossier = os.path.join(SC, "voix_" + code.lower())
    os.makedirs(dossier, exist_ok=True)
    dst = os.path.join(dossier, f"{code}_{perso}.mp3")
    if os.path.exists(dst):
        print("déjà là :", dst)
        continue
    r = subprocess.run(["curl", "-s", "-L", "-f", "-o", dst, v["url"]])
    if r.returncode != 0 or not os.path.exists(dst):
        raise SystemExit(f"téléchargement impossible : {code} {perso}")
    print(f"{code} {perso} : {os.path.getsize(dst) / 1024:.0f} Ko -> {dst}")
