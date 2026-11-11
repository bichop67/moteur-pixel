# Prépare les temps des mots du lot du 08/11/2026 sans rien recopier à la main :
#   python prepare_asr.py <statut_transcriptions.json> [<url words.json> <CODE> <PERSO>] ...
# Le fichier de statut (réponse de creative_get_flow_run_status enregistrée par l'outil) contient les transcriptions ;
# chacune est rattachée à sa voix par l'identifiant de génération présent dans source.url (voir voix_urls.json).
# Des transcriptions supplémentaires peuvent être données par leur lien words.json. Écrit transcriptions_08-11.json et
# gen_map.json, puis lance asr_shorts_duo.py (qui écrit voix_islNN\asr_ISLNN.json sans jamais réécrire un fichier existant).
import json
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
voix = {v["gen"]: (v["code"], v["perso"]) for v in json.load(open(os.path.join(ICI, "voix_urls.json"), encoding="utf-8"))}

statut = json.load(open(sys.argv[1], encoding="utf-8"))
transcripts, gen_map = [], {}
for tr in statut.get("transcripts", []):
    m = re.search(r"content_generation/[^/]+/([^/]+)/content\.mp3", (tr.get("source") or {}).get("url", ""))
    if not m or m.group(1) not in voix:
        print("transcription sans voix reconnue :", tr.get("generation_id"))
        continue
    code, perso = voix[m.group(1)]
    transcripts.append({"generation_id": tr["generation_id"], "words": tr["words"]})
    gen_map[tr["generation_id"]] = [code, perso]

extra = sys.argv[2:]
os.makedirs(os.path.join(ICI, "brut"), exist_ok=True)
for i in range(0, len(extra), 3):
    url, code, perso = extra[i:i + 3]
    dst = os.path.join(ICI, "brut", f"{code}_{perso}_words.json")
    if not os.path.exists(dst):
        subprocess.run(["curl", "-s", "-L", "-f", "-o", dst, url], check=True)
    d = json.load(open(dst, encoding="utf-8"))
    words = d if isinstance(d, list) else (d.get("words") or (d.get("transcripts") or [{}])[0].get("words"))
    gid = f"extra_{code}_{perso}"
    transcripts.append({"generation_id": gid, "words": words})
    gen_map[gid] = [code, perso]

vus = sorted(f"{c}_{p}" for c, p in gen_map.values())
print(len(vus), "transcriptions :", " ".join(vus))
manque = sorted(f"{c}_{p}" for c, p in voix.values() if f"{c}_{p}" not in vus)
if manque:
    print("MANQUE :", " ".join(manque))
json.dump({"transcripts": transcripts}, open(os.path.join(ICI, "transcriptions_08-11.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(gen_map, open(os.path.join(ICI, "gen_map.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
subprocess.run([sys.executable, os.path.join(ICI, "asr_shorts_duo.py"), os.path.join(ICI, "transcriptions_08-11.json")],
               check=True)
