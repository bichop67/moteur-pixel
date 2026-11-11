# Voix refaites le 08/11/2026 (texte final après la dernière relecture) : à partir du statut des transcriptions
# (fichier enregistré par l'outil), télécharge chaque nouvelle voix depuis source.url (CODE_PERSO.mp3, jamais par-dessus
# un fichier existant), ajoute ses mots aux transcriptions déjà faites (les voix inchangées gardent les leurs), puis
# réécrit les asr des Shorts touchés.   python integre_nouvelles_voix.py <statut.json>
import json
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
SC = os.path.dirname(ICI)
nouv = {v["gen"]: (v["code"], v["perso"]) for v in json.load(open(os.path.join(ICI, "voix_urls2.json"), encoding="utf-8"))}
tr_all = json.load(open(os.path.join(ICI, "transcriptions_08-11.json"), encoding="utf-8"))
gen_map = json.load(open(os.path.join(ICI, "gen_map.json"), encoding="utf-8"))

statut = json.load(open(sys.argv[1], encoding="utf-8"))
touches = set()
for tr in statut.get("transcripts", []):
    url = (tr.get("source") or {}).get("url", "")
    m = re.search(r"content_generation/[^/]+/([^/]+)/content\.mp3", url)
    if not m or m.group(1) not in nouv:
        print("transcription non reconnue :", tr.get("generation_id"))
        continue
    code, perso = nouv[m.group(1)]
    dst = os.path.join(SC, "voix_" + code.lower(), f"{code}_{perso}.mp3")
    if os.path.exists(dst):
        raise SystemExit("existe déjà (rien n'est écrasé) : " + dst)
    subprocess.run(["curl", "-s", "-L", "-f", "-o", dst, url], check=True)
    print(f"{code} {perso} : {os.path.getsize(dst) // 1024} Ko")
    # on retire l'ancienne transcription de cette voix, on met la nouvelle
    for gid in [g for g, cp in gen_map.items() if cp == [code, perso]]:
        del gen_map[gid]
        tr_all["transcripts"] = [t for t in tr_all["transcripts"] if t["generation_id"] != gid]
    tr_all["transcripts"].append({"generation_id": tr["generation_id"], "words": tr["words"]})
    gen_map[tr["generation_id"]] = [code, perso]
    touches.add(code)

json.dump(tr_all, open(os.path.join(ICI, "transcriptions_08-11.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(gen_map, open(os.path.join(ICI, "gen_map.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Shorts touchés :", " ".join(sorted(touches)))
subprocess.run([sys.executable, os.path.join(ICI, "asr_shorts_duo.py"), os.path.join(ICI, "transcriptions_08-11.json")]
               + sorted(touches), check=True)
