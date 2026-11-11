# Rend les Shorts du lot du 08/11/2026 l'un après l'autre, en priorité basse (le PC reste utilisable), puis lance
# controle_video.py --leger sur chacun. Écrit tout dans rendu_0811.log et affiche à la fin un résumé COURT par Short.
#   python rendu_lot.py ISL23 ISL24 ...        (codes du lot ; « tous » = les 9)
import ctypes
import io
import os
import re
import subprocess
import sys
import time

MOT = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL"
ICI = os.path.dirname(os.path.abspath(__file__))
LOT = {"ISL23": "islam_23_talons.txt", "ISL24": "islam_24_urine.txt", "ISL25": "islam_25_droite.txt",
       "ISL26": "islam_26_imam.txt", "ISL27": "islam_27_asr.txt", "ISL28": "islam_28_medisance.txt",
       "ISL29": "islam_29_ecoute.txt", "ISL30": "islam_30_horoscope.txt", "ISL31": "islam_31_coucher.txt"}
codes = list(LOT) if sys.argv[1:] == ["tous"] else sys.argv[1:]

k32 = ctypes.windll.kernel32
k32.GetCurrentProcess.restype = ctypes.c_void_p
k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
k32.SetPriorityClass(k32.GetCurrentProcess(), 0x40)          # priorité « faible », héritée par les rendus

log = io.open(os.path.join(ICI, "rendu_0811.log"), "a", encoding="utf-8")


def lance(args):
    t0 = time.time()
    log.write(time.strftime("%H:%M:%S") + " -> " + " ".join(args) + "\n")
    log.flush()
    r = subprocess.run([sys.executable] + args, cwd=MOT, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    log.write(r.stdout[-6000:] + r.stderr[-3000:] + f"\n{time.strftime('%H:%M:%S')} fin ({r.returncode}) en "
              f"{(time.time() - t0) / 60:.1f} min\n")
    log.flush()
    return r


resume = []
for c in codes:
    f = LOT[c]
    titre = next(l.split(":", 1)[1].strip() for l in io.open(os.path.join(MOT, "scenarios", f), encoding="utf-8")
                 if l.startswith("TITRE:"))
    if not os.path.exists(os.path.join(MOT, "scenarios", "voix_" + c.lower(), f"asr_{c}.json")):
        lance(["scenario.py", "scenarios/" + f, "asr"])
    r = lance(["scenario.py", "scenarios/" + f, "tout", "8"])
    if r.returncode != 0:
        resume.append(f"{c} : RENDU EN ERREUR (voir rendu_0811.log) : {r.stderr.strip()[-200:]}")
        continue
    mp4 = f"scenarios/{titre}.mp4"
    q = lance(["controle_video.py", mp4, "--leger"])
    out = q.stdout
    m = re.search(r": ([\d.]+) s, (\d+x\d+), (-?[\d.]+) LUFS.*?(\d+) tranche", out)
    fige = "aucun passage figé" in out
    resume.append(f"{c} {titre} : " + (f"{m.group(1)} s, {m.group(3)} LUFS, {m.group(4)} tranches silencieuses, "
                                       if m else "contrôle illisible, ") +
                  ("rythme OK" if fige else "PASSAGE FIGÉ > 4 s") +
                  (" | " + re.search(r"(passage figé[^\n]*|figé[^\n]*)", out).group(1)[:120]
                   if not fige and re.search(r"figé", out) else ""))
print("\n".join(resume))
log.write("\n".join(resume) + "\n")
