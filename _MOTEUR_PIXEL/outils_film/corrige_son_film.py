# Son du film « conte » : un pic de +2 dBFS (20 ms, à 8:38) laissé par loudnorm lors de l'assemblage.
# 1. son v2 = son du film passé dans un limiteur à -1,5 dBFS (suréchantillonné x4, retard compensé, sans « niveau auto ») ;
# 2. contrôles : volume intégré inchangé, crête réelle, aucun décalage avec l'image (corrélation avec l'ancien son) ;
# 3. film et copie légère refaits SANS réencoder l'image (la vidéo est copiée telle quelle) -> fichiers « (son v2) ».
# Le remplacement des anciens fichiers (Corbeille puis renommage) se fait à part, après vérification.
import ctypes
import os
import re
import subprocess
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
k32 = ctypes.windll.kernel32
k32.GetCurrentProcess.restype = ctypes.c_void_p
k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
k32.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
h = k32.GetCurrentProcess()
k32.SetPriorityClass(h, 0x40)
k32.SetProcessAffinityMask(h, 0xF00)

sys.path.insert(0, r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL")
import assemble_film as af  # noqa: E402

FF = af.FF
EP = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\FILM\EPISODE 14"
SCR = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.join(EP, "Moussa - le film.mp4")
LEGER = os.path.join(EP, "Moussa - le film (leger).mp4")
SON2 = os.path.join(SCR, "moussa_conte_son_v2.m4a")
FILM2 = os.path.join(EP, "Moussa - le film (son v2).mp4")
LEGER2 = os.path.join(EP, "Moussa - le film (leger) (son v2).mp4")
SR = 48000


def mesure(src):
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", src, "-vn", "-af", "ebur128=peak=true:framelog=verbose",
                        "-f", "null", "-"], capture_output=True, text=True, errors="ignore").stderr
    s = r[r.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+)", s).group(1)
    p = re.search(r"Peak:\s+(-?[\d.]+|-inf)", s).group(1)
    return float(i), float(p)


def lire(src, ss, t):
    raw = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-ss", f"{ss}", "-t", f"{t}", "-i", src, "-vn",
                          "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


for f in (FILM2, LEGER2):
    if os.path.exists(f):
        raise SystemExit(f"existe déjà : {f}")

print("1. son v2 (limiteur -1,5 dBFS)…", flush=True)
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", FILM, "-vn", "-af",
                "aresample=192000,alimiter=limit=0.8414:attack=1:release=50:level=false:latency=true,"
                "aresample=48000", "-c:a", "aac", "-b:a", "192k", "-ac", "1", SON2], check=True)

print("2. contrôles", flush=True)
i1, p1 = mesure(FILM)
i2, p2 = mesure(SON2)
print(f"   avant : {i1} LUFS, crête réelle {p1:+.1f} dBTP ; après : {i2} LUFS, crête réelle {p2:+.1f} dBTP", flush=True)
for t in (60.0, 517.0, 1500.0, 3000.0):
    a, b = lire(FILM, t, 4.0), lire(SON2, t, 4.0)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    lags = range(-480, 481)
    c = [np.dot(a[max(0, k):n + min(0, k)], b[max(0, -k):n - max(0, k)]) for k in lags]
    k = lags[int(np.argmax(c))]
    print(f"   décalage à {t:.0f} s : {k} échantillon(s) ({k / SR * 1000:.2f} ms)", flush=True)
x = lire(SON2, 517.5, 1.0)
print(f"   à 8:38 : crête {20 * np.log10(np.abs(x).max()):+.2f} dBFS", flush=True)
if p2 > -0.5 or abs(i2 - i1) > 0.3:
    raise SystemExit("contrôle du son v2 NON conforme : rien n'est remplacé")

print("3. film et copie légère avec le son v2 (image copiée, pas réencodée)…", flush=True)
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-i", FILM, "-i", SON2, "-map", "0:v:0", "-map", "1:a:0",
                "-c", "copy", "-movflags", "+faststart", FILM2], check=True)
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-i", LEGER, "-i", SON2, "-map", "0:v:0", "-map", "1:a:0",
                "-c", "copy", "-movflags", "+faststart", LEGER2], check=True)
for f in (FILM2, LEGER2):
    r = subprocess.run([FF, "-hide_banner", "-i", f], capture_output=True, text=True, errors="ignore").stderr
    d = re.search(r"Duration: ([\d:.]+)", r).group(1)
    print(f"   {os.path.basename(f)} : {d}, {os.path.getsize(f) / 1e9:.2f} Go", flush=True)
print("terminé", flush=True)
