# Compare l'empreinte du texte dit au moment où il a été figé (résultats de contre-vérification dans le journal du
# workflow) à l'empreinte actuelle (textes_voix.py). Sortie courte : code, figé, actuel, durée estimée, caractères.
import io
import json
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
JOURNAL = (r"C:\Users\abdellah\.claude\projects\C--WINDOWS-system32\bd815e4d-ef87-4d31-bd4c-2de9422f0326"
           r"\subagents\workflows\wf_88b5d2e0-e7f\journal.jsonl")
figees = {}
for line in io.open(JOURNAL, encoding="utf-8"):
    try:
        j = json.loads(line)
    except json.JSONDecodeError:
        continue
    r = j.get("result")
    if j.get("type") == "result" and isinstance(r, dict) and r.get("marqueur_pose") and r.get("empreinte"):
        figees[r["code"]] = r["empreinte"]

out = subprocess.run([sys.executable, os.path.join(ICI, "textes_voix.py")], capture_output=True, text=True,
                     encoding="utf-8").stdout
for m in re.finditer(r"===== (ISL\d+) — .*?\(≈ ([\d.]+) s .*?empreinte du texte dit : (\w+)", out):
    code, est, emp = m.groups()
    chars = sum(int(c) for c in re.findall(rf"--- {code}_\w+ · .*?· (\d+) caractères", out))
    etat = "OK" if figees.get(code) == emp else ("PAS FIGÉ" if code not in figees else "DIFFÉRENT")
    print(f"{code}  figé={figees.get(code, '-'):16s} actuel={emp}  {etat:9s}  ≈{est} s  {chars} car.")
for l in out.splitlines():
    if l.startswith("!!") or l.startswith("TOTAL"):
        print(l)
