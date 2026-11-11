# Extrait léger (< 10 Mo) du film « conte » pour le téléphone : la révélation (partie 9), de « Moussa s'est approché »
# jusqu'à la main blanche (« Pas une maladie : une lumière. »). Pris dans le film assemblé, 640x360, x264 deux passes.
# Coupes calées sur les sous-titres ET sur les creux de la voix (03/11/2026) :
#   - début : l'image reste noire tant que le sous-titre de la phrase d'avant est affiché (jusqu'à 23,73 s) ;
#   - fin : son coupé dans le creux après « une lumière. » (146,55 -> 146,88), image arrêtée avant le sous-titre
#     suivant (146,92), dernière image tenue 1 s puis fondu au noir.
import ctypes
import glob
import os
import re
import subprocess
import sys

k32 = ctypes.windll.kernel32
k32.GetCurrentProcess.restype = ctypes.c_void_p
k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
k32.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
h = k32.GetCurrentProcess()
k32.SetPriorityClass(h, 0x40)
k32.SetProcessAffinityMask(h, 0xF00)

ENGINE = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
EP = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\FILM\EPISODE 14"
SCR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ENGINE)
import assemble_film as af  # noqa: E402

FF = af.FF
FILM = os.path.join(EP, "Moussa - le film.mp4")
SORTIE = os.path.join(EP, "Moussa conte - extrait (la révélation, leger).mp4")
FPS, FADE = 30, 30
DEBUT = 23.40            # (temps de la partie 9) creux avant « Moussa s'est approché » (voix à 23,68)
IMAGE_VISIBLE = 23.73    # sous-titre « Moussa s'est approché. » (le précédent reste noir)
FIN_VOIX = 146.55        # fin de « une lumière. »
FIN = 146.88             # avant le sous-titre « Et Allah lui a dit : » (146,92)
FIN_IMAGE = 146.70       # dernière image nette : le fondu vers le plan suivant commence vers 146,78
TENUE = 1.0              # dernière image tenue, puis fondu au noir


def parties():
    d = {}
    for p in glob.glob(ENGINE + r"\scenarios\film\ep14_conte\Moussa conte - partie *.mp4"):
        nom = os.path.basename(p)
        if "(v" in nom or "(leger" in nom:
            continue
        m = re.match(r"Moussa conte - partie (\d+) - ", nom)
        if m:
            d[int(m.group(1))] = p
    return [d[i] for i in range(1, 25)]


if os.path.exists(SORTIE) and "--essai" not in sys.argv:
    raise SystemExit("l'extrait existe déjà : je ne l'écrase pas")
nb = [round(af.duree_image(p) * FPS) for p in parties()]
debut9 = (sum(nb[:8]) - FADE * 8) / FPS
ss, t = debut9 + DEBUT, FIN - DEBUT
total = t + TENUE
print(f"partie 9 dans le film : {debut9:.2f} s ; extrait {ss:.2f} s + {t:.2f} s (+ {TENUE} s tenue)", flush=True)
# image et son lus séparément (deux entrées) : l'image s'arrête à FIN_IMAGE puis la dernière image est tenue
# (tpad) jusqu'au fondu au noir ; le son s'arrête à FIN puis silence jusqu'à la fin.
vf = (f"[0:v]scale=640:360:flags=area,format=yuv420p,fade=t=in:st={IMAGE_VISIBLE - DEBUT:.2f}:d=0.4,"
      f"tpad=stop_mode=clone:stop_duration={total - (FIN_IMAGE - DEBUT):.3f},"
      f"fade=t=out:st={total - 1.2:.2f}:d=1.2,trim=end={total:.3f}[v]")
af_ = (f"[1:a]afade=t=in:st=0:d=0.25,afade=t=out:st={FIN_VOIX - DEBUT:.2f}:d={FIN - FIN_VOIX:.2f},"
       f"apad=whole_dur={total:.3f},atrim=end={total:.3f}[a]")
journal = os.path.join(SCR, "extrait_2passes")
entrees = [FF, "-hide_banner", "-loglevel", "error", "-y",
           "-ss", f"{ss:.3f}", "-t", f"{FIN_IMAGE - DEBUT:.3f}", "-i", FILM,
           "-ss", f"{ss:.3f}", "-t", f"{t:.3f}", "-i", FILM]
video = ["-c:v", "libx264", "-preset", "slow", "-b:v", "520k", "-maxrate", "800k", "-bufsize", "1600k",
         "-threads", "4", "-passlogfile", journal]
if "--essai" in sys.argv:                 # vérification rapide des durées, sans les deux passes
    essai = os.path.join(SCR, "essai_extrait.mp4")
    subprocess.run(entrees + ["-filter_complex", vf + ";" + af_, "-map", "[v]", "-map", "[a]", "-c:v", "libx264",
                              "-preset", "ultrafast", "-crf", "30", "-c:a", "aac", "-b:a", "80k", essai], check=True)
    print("essai :", essai, f"image {af.duree_image(essai):.2f} s / attendu {total:.2f} s", flush=True)
    sys.exit(0)
subprocess.run(entrees + ["-filter_complex", vf, "-map", "[v]"] + video + ["-pass", "1", "-an", "-f", "null", "NUL"],
               check=True)
subprocess.run(entrees + ["-filter_complex", vf + ";" + af_, "-map", "[v]", "-map", "[a]"] + video +
               ["-pass", "2", "-c:a", "aac", "-b:a", "80k", "-ac", "1", "-movflags", "+faststart", SORTIE], check=True)
print(f"extrait : {SORTIE} ({os.path.getsize(SORTIE) / 1e6:.1f} Mo)", flush=True)
