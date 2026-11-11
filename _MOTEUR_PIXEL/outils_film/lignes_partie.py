"""Sort les répliques d'une partie du script (source maître) au format scénario, pour écrire pNN.txt :
python lignes_partie.py 3  ->  lignes_P3.txt (scènes, IMAGE et SON en commentaires, répliques prêtes à placer)."""
import io
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
n = int(sys.argv[1])
src = io.open(os.path.join(ICI, "ep14_source_complet.txt"), encoding="utf-8").read().splitlines()
out, dedans = [], False
for ligne in src:
    if ligne.startswith("=== P"):
        dedans = ligne.startswith(f"=== P{n} |")
        if dedans:
            out.append("# " + ligne)
        continue
    if not dedans or not ligne.strip():
        continue
    if ligne.startswith("@SCENE"):
        out += ["", "# " + ligne[1:]]
    elif ligne.startswith("@IMAGE") or ligne.startswith("@SON"):
        out.append("#   " + ligne[1:])
    elif "|" in ligne:
        parts = [p.strip() for p in ligne.split("|")]
        qui, txt = parts[0], parts[1]
        ref = parts[2] if len(parts) > 2 else ""
        qui = {"N": "NARRATEUR (voix off)", "C": "CORAN (voix off)"}.get(qui, qui)
        out.append(f"{qui} : {txt}" + (f' {{source "{ref}"}}' if ref else ""))
io.open(os.path.join(ICI, f"lignes_P{n}.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("ok", len(out))
