# Rassemble les transcriptions ElevenLabs (0 crédit) des voix du lot du 08/11/2026 pour asr_shorts_duo.py.
# Entrée, à côté de ce fichier : transcriptions_urls.json = [{"generation_id": "...", "code": "ISL23", "perso": "PETIT",
# "url": "<words_download_url ou content_url>"}, ...] (on peut l'allonger au fur et à mesure).
# Sortie : transcriptions_08-11.json ({"transcripts": [{"generation_id", "words": [...]}]}) et gen_map.json
# ({generation_id: [code, perso]}). Les fichiers bruts téléchargés sont gardés dans brut\ (jamais réécrits).
import json
import os
import subprocess

ICI = os.path.dirname(os.path.abspath(__file__))
BRUT = os.path.join(ICI, "brut")
os.makedirs(BRUT, exist_ok=True)

entrees = json.load(open(os.path.join(ICI, "transcriptions_urls.json"), encoding="utf-8"))
transcripts, gen_map = [], {}
for e in entrees:
    dst = os.path.join(BRUT, f"{e['code']}_{e['perso']}_{e['generation_id']}.json")
    if not os.path.exists(dst):
        r = subprocess.run(["curl", "-s", "-L", "-f", "-o", dst, e["url"]])
        if r.returncode != 0:
            raise SystemExit(f"téléchargement impossible : {e['code']} {e['perso']}")
    brut = open(dst, encoding="utf-8").read()
    try:
        d = json.loads(brut)
    except json.JSONDecodeError:
        raise SystemExit(f"pas du JSON : {dst} (début : {brut[:120]!r})")
    if isinstance(d, dict):
        words = d.get("words") or (d.get("transcripts") or [{}])[0].get("words") or d.get("segments")
    else:
        words = d
    if not words:
        raise SystemExit(f"aucun mot trouvé dans {dst} : clés {list(d)[:10] if isinstance(d, dict) else type(d)}")
    transcripts.append({"generation_id": e["generation_id"], "words": words})
    gen_map[e["generation_id"]] = [e["code"], e["perso"]]
    print(f"{e['code']} {e['perso']:6s} {len(words):4d} éléments")

json.dump({"transcripts": transcripts}, open(os.path.join(ICI, "transcriptions_08-11.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(gen_map, open(os.path.join(ICI, "gen_map.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("écrit : transcriptions_08-11.json et gen_map.json")
