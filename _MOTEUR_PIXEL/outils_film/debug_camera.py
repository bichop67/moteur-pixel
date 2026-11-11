# Affiche, plan par plan, les balises de caméra et les clés de caméra calculées (pour comprendre un plan figé).
#   python debug_camera.py 9
import os
import sys

MOTEUR = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
sys.path.insert(0, MOTEUR)
os.chdir(MOTEUR)
import scenario  # noqa: E402

orig = scenario.camera_film


def dbg(sc, b, roles, t0):
    cam0 = sc.camera

    def cam(keys):
        print(f"--- plan {sc.bg} t0={t0:.1f} durée={b['t1'] - b['t0']:.1f} roles={list(roles)}")
        for it in [i for i in b["items"] if i["type"] == "ligne"]:
            an = [(round(t - t0, 1), c) for (t, c) in it.get("annot", []) if c.split()[0].lower() in ("cadre", "large", "gros")]
            if an:
                print("   ligne", round(it["t0"] - t0, 1), "->", round(it["t1"] - t0, 1), an)
        print("   clés :", [(round(k[0], 1), round(k[1], 2), round(k[2][0])) for k in keys])
        return cam0(keys)
    sc.camera = cam
    return orig(sc, b, roles, t0)


scenario.camera_film = dbg
num = int(sys.argv[1])
scenario.fabrique(os.path.join(MOTEUR, "scenarios", "film", "ep14_conte", f"p{num:02d}.txt"))
