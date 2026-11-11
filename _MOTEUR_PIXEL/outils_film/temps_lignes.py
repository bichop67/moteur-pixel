"""Minutage de chaque réplique et de chaque {annotation} d'un scénario : python temps_lignes.py scenario.txt"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MOTEUR = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
sys.path.insert(0, MOTEUR)
os.chdir(MOTEUR)
scen = os.path.abspath(sys.argv[1])
sys.argv = ["scenario.py"]
import scenario  # noqa: E402

_orig = scenario.plans_du_bloc


def _espion(b, D, *a, **k):
    print(f"== bloc {b['t0']:.1f} -> {b['t1']:.1f}")
    for it in b["items"]:
        if it["type"] == "ligne":
            print(f"  {it['t0']:6.1f}-{it['t1']:6.1f} {it['qui']}: {it['texte'][:60]}")
            for (t, c) in it.get("annot", []):
                print(f"        {t:6.1f}  {{{c}}}")
    return _orig(b, D, *a, **k)


scenario.plans_du_bloc = _espion
V = scenario.fabrique(scen)[0]
print("durée", round(V.D.dur if hasattr(V, "D") else 0, 1))
