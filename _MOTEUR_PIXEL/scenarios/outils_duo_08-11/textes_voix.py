# Textes exacts à envoyer à ElevenLabs pour les 9 Shorts duo du 08/11/2026 (une génération par perso et par Short,
# répliques séparées par [long pause]), calculés comme le moteur (scenario.py : explique.balises + kit.prompts), sans
# fabriquer la vidéo. Signale les didascalies inconnues, donne une durée estimée (15 caractères/s, ﷺ ≈ 2,5 s) et une
# EMPREINTE du texte dit (sha256) : elle ne doit pas changer quand on ne touche qu'aux didascalies, balises ou décors.
# Usage : python textes_voix.py [islam_23_talons.txt …]   -> affiche (tous les fichiers du lot si aucun n'est donné)
#         python textes_voix.py --ecrire                  -> écrit aussi « Voix ElevenLabs - 9 Shorts duo (08-11).txt »
import hashlib
import io
import os
import re
import sys

MOT = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL"
sys.path.insert(0, MOT)
import explique  # noqa: E402
import kit  # noqa: E402
import scenario  # noqa: E402

LOT = ["islam_23_talons.txt", "islam_24_urine.txt", "islam_25_droite.txt", "islam_26_imam.txt", "islam_27_asr.txt",
       "islam_28_medisance.txt", "islam_29_ecoute.txt", "islam_30_horoscope.txt", "islam_31_coucher.txt"]
VOIX = {"PETIT": "QEZnlKYcLy9N2ierwPEc (Lucas)", "GRAND": "43TArLZXN5r3L8mJ6AGR (Quentin)"}

args = [a for a in sys.argv[1:] if not a.startswith("--")]
fichiers = [os.path.basename(a) for a in args] or LOT
sortie = []
total = 0
for f in fichiers:
    p = os.path.join(MOT, "scenarios", f)
    if not os.path.exists(p):
        sortie.append(f"===== {f} : PAS ENCORE ÉCRIT")
        continue
    code, titre, reps = None, None, []
    for n, line in enumerate(io.open(p, encoding="utf-8"), 1):
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
    emp = hashlib.sha256("\n".join(f"{w}|{t}" for w, t in reps).encode("utf-8")).hexdigest()[:16]
    sortie.append(f"===== {code} — {titre} (≈ {est:.1f} s estimées, fin comprise) — empreinte du texte dit : {emp}")
    for who in ("PETIT", "GRAND"):
        if who in pr:
            sortie.append(f"--- {code}_{who} · voix {VOIX[who]} · eleven_v4 · {len(pr[who])} caractères")
            sortie.append(pr[who])
            total += len(pr[who])
    sortie.append("")
sortie.append(f"TOTAL : {total} caractères (≈ {total} crédits ElevenLabs)")
txt = "\n".join(sortie)
print(txt)
if "--ecrire" in sys.argv:
    io.open(os.path.join(MOT, "scenarios", "Voix ElevenLabs - 9 Shorts duo (08-11).txt"), "w", encoding="utf-8").write(
        "Textes exacts envoyés à ElevenLabs (eleven_v4, une prise) — 9 Shorts duo du 08/11/2026\n\n" + txt + "\n")
