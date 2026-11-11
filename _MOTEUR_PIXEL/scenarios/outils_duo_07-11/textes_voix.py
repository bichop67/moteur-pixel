# Textes exacts à envoyer à ElevenLabs pour les 6 Shorts duo du 07/11/2026 (une génération par perso et par Short,
# répliques séparées par [long pause]), calculés comme le moteur (scenario.py : explique.balises + kit.prompts), sans
# fabriquer la vidéo. Signale aussi les didascalies inconnues et donne une durée estimée (15 caractères/s, ﷺ ≈ 2,5 s).
# Usage : python textes_voix.py            -> affiche tout et écrit « Voix ElevenLabs - 6 Shorts duo (07-11).txt »
import io
import os
import re
import sys

MOT = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL"
sys.path.insert(0, MOT)
import explique  # noqa: E402
import kit  # noqa: E402
import scenario  # noqa: E402

FICHIERS = ["islam_17_jurer.txt", "islam_18_eternuement.txt", "islam_19_colere.txt", "islam_20_maison.txt",
            "islam_21_dette.txt", "islam_22_dormir.txt"]
VOIX = {"PETIT": "QEZnlKYcLy9N2ierwPEc (Lucas)", "GRAND": "43TArLZXN5r3L8mJ6AGR (Quentin)"}

sortie = []
total = 0
for f in FICHIERS:
    code, titre, reps = None, None, []
    for n, line in enumerate(io.open(os.path.join(MOT, "scenarios", f), encoding="utf-8"), 1):
        line = line.strip()
        if line.startswith("CODE:"):
            code = line.split(":", 1)[1].strip()
        if line.startswith("TITRE:"):
            titre = line.split(":", 1)[1].strip()
        m = re.match(r"^([A-Z_0-9]+)\s*(?:\(([^)]*)\))?\s*:\s*(.+)$", line)
        if m and m.group(1) in VOIX:
            act = scenario.lire_didascalies(m.group(2) or "")
            for x in act["inconnus"]:
                print(f"!! {f} ligne {n} : didascalie inconnue « {x} »")
            voix_txt = re.sub(r"\s+", " ", explique.balises(m.group(3).strip())[0]).strip()
            reps.append((m.group(1), voix_txt))
    pr = kit.prompts(reps)
    dit = " ".join(re.sub(r"\[[^\]]*\]", "", t) for _, t in reps)
    est = len(dit.replace("ﷺ", "")) / 15 + 2.5 * dit.count("ﷺ") + 0.35 * (len(reps) - 1) + 1.4
    sortie.append(f"===== {code} — {titre} (≈ {est:.1f} s estimées, fin comprise)")
    for who in ("PETIT", "GRAND"):
        if who in pr:
            sortie.append(f"--- {code}_{who} · voix {VOIX[who]} · eleven_v4 · {len(pr[who])} caractères")
            sortie.append(pr[who])
            total += len(pr[who])
    sortie.append("")
sortie.append(f"TOTAL : {total} caractères (≈ {total} crédits ElevenLabs)")
txt = "\n".join(sortie)
print(txt)
io.open(os.path.join(MOT, "scenarios", "Voix ElevenLabs - 6 Shorts duo (07-11).txt"), "w", encoding="utf-8").write(
    "Textes exacts envoyés à ElevenLabs (eleven_v4, une prise) — 6 Shorts duo du 07/11/2026\n\n" + txt + "\n")
