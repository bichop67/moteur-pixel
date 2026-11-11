# Planches de contrôle AVANT rendu : une image toutes les 5 s de chaque partie (pages de 30 vignettes 384x216).
#   python planches_conte.py                 -> toutes les parties de la file (refait celles dont le scénario a changé)
#   python planches_conte.py une 7           -> une seule partie (sous-processus)
import json
import os
import subprocess
import sys
import time

MOTEUR = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
SC = os.path.join(MOTEUR, "scenarios", "film", "ep14_conte")
SCR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCR, "planches")
PAS, COLS, ROWS, TW, TH = 5.0, 5, 6, 384, 216


def a_jour(num):
    scen = os.path.join(SC, f"p{num:02d}.txt")
    p = os.path.join(OUT, f"p{num:02d}_1.png")
    return os.path.exists(p) and os.path.getmtime(p) > os.path.getmtime(scen)


def une(num):
    sys.path.insert(0, MOTEUR)
    os.chdir(MOTEUR)
    import numpy as np
    from PIL import Image, ImageDraw
    import scenario
    VID, nom, dossier, code, voix, repliques = scenario.fabrique(os.path.join(SC, f"p{num:02d}.txt"))
    dur = VID.dlg.dur
    ts = list(np.arange(0.5, dur, PAS))
    os.makedirs(OUT, exist_ok=True)
    par_page = COLS * ROWS
    for pg in range(0, len(ts), par_page):
        lot = ts[pg:pg + par_page]
        rows = (len(lot) + COLS - 1) // COLS
        sh = Image.new("RGB", (COLS * TW, rows * TH))
        d = ImageDraw.Draw(sh)
        for i, t in enumerate(lot):
            im = VID.frame(float(t)).convert("RGB").resize((TW, TH))
            x, y = (i % COLS) * TW, (i // COLS) * TH
            sh.paste(im, (x, y))
            d.rectangle((x, y, x + 52, y + 16), fill=(0, 0, 0))
            d.text((x + 4, y + 3), f"{t:.0f} s", fill=(255, 255, 0))
        sh.save(os.path.join(OUT, f"p{num:02d}_{pg // par_page + 1}.png"))
    json.dump(dict(duree=dur, pages=(len(ts) + par_page - 1) // par_page),
              open(os.path.join(OUT, f"p{num:02d}.json"), "w"))
    print(f"p{num:02d} : {dur:.1f} s, {len(ts)} vignettes", flush=True)


if __name__ == "__main__":
    if sys.argv[1:2] == ["une"]:
        une(int(sys.argv[2]))
        sys.exit(0)
    ordre = json.load(open(os.path.join(SCR, "file_rendu_ordre.json"), encoding="utf-8"))
    for num in ordre:
        if num in (1, 15) or a_jour(num):
            continue
        t = time.time()
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "une", str(num)])
        print(time.strftime("%H:%M:%S"), f"planche p{num:02d} : code {r.returncode} ({(time.time() - t) / 60:.1f} min)",
              flush=True)
