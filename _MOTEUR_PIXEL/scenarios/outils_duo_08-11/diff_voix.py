# Compare, pour chaque voix enregistrée, le texte ENVOYÉ à ElevenLabs (texte des transcriptions) et le texte que le
# scénario demande MAINTENANT (même calcul que textes_voix.py). Affiche seulement les différences, mot par mot.
import difflib
import io
import json
import os
import re
import sys

MOT = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL"
sys.path.insert(0, MOT)
import explique  # noqa: E402
import kit  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
LOT = {"ISL23": "islam_23_talons.txt", "ISL24": "islam_24_urine.txt", "ISL25": "islam_25_droite.txt",
       "ISL26": "islam_26_imam.txt", "ISL27": "islam_27_asr.txt", "ISL28": "islam_28_medisance.txt",
       "ISL29": "islam_29_ecoute.txt", "ISL30": "islam_30_horoscope.txt", "ISL31": "islam_31_coucher.txt"}
voix = {v["gen"]: (v["code"], v["perso"]) for v in json.load(open(os.path.join(ICI, "voix_urls.json"), encoding="utf-8"))}
envoye = {}
statut = json.load(open(sys.argv[1], encoding="utf-8"))
for tr in statut["transcripts"]:
    m = re.search(r"content_generation/[^/]+/([^/]+)/content\.mp3", tr["source"]["url"])
    if m and m.group(1) in voix:
        envoye[voix[m.group(1)]] = tr["text"]
for a in sys.argv[2:]:                      # « CODE:PERSO:fichier_texte » pour les voix transcrites à part
    code, perso, f = a.split(":", 2)
    envoye[(code, perso)] = io.open(f, encoding="utf-8").read().strip()


def actuel(code):
    reps = []
    for line in io.open(os.path.join(MOT, "scenarios", LOT[code]), encoding="utf-8"):
        m = re.match(r"^([A-Z_0-9]+)\s*(?:\(([^)]*)\))?\s*:\s*(.+)$", line.strip())
        if m and m.group(1) in ("PETIT", "GRAND"):
            reps.append((m.group(1), re.sub(r"\s+", " ", explique.balises(m.group(3).strip())[0]).strip()))
    return kit.prompts(reps)


for (code, perso), txt in sorted(envoye.items()):
    now = actuel(code).get(perso, "")
    if now == txt:
        print(f"{code}_{perso} : identique")
        continue
    a, b = txt.split(), now.split()
    d = [x for x in difflib.ndiff(a, b) if x[:1] in "+-"]
    print(f"{code}_{perso} : DIFFÉRENT -> " + " ".join(d)[:400])
