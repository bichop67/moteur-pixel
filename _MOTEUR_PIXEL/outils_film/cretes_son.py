# Où sont les crêtes du son du film « conte » ? (ebur128 : crête réelle +2,1 dBFS)
# Lit le son du film en flottants, crête par tranche de 0,1 s, puis crête « réelle » (suréchantillonnée x4)
# autour des tranches les plus fortes.
import ctypes
import os
import subprocess
import sys

import numpy as np
from scipy.signal import resample_poly

k32 = ctypes.windll.kernel32
k32.GetCurrentProcess.restype = ctypes.c_void_p
k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
k32.SetPriorityClass(k32.GetCurrentProcess(), 0x40)

sys.path.insert(0, r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL")
import assemble_film as af  # noqa: E402

SRC = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\FILM\EPISODE 14\Moussa - le film.mp4"
SR = 48000
raw = subprocess.run([af.FF, "-hide_banner", "-loglevel", "error", "-i", SRC, "-vn", "-ac", "1", "-ar", str(SR),
                      "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.float32)
print(f"{len(x) / SR:.1f} s de son", flush=True)
win = SR // 10
n = len(x) // win
pk = np.abs(x[:n * win].reshape(n, win)).max(axis=1)
db = 20 * np.log10(np.maximum(pk, 1e-9))
print(f"crête d'échantillon max : {db.max():+.2f} dBFS", flush=True)
for seuil in (0.0, -1.0, -1.5, -3.0):
    print(f"tranches de 0,1 s au-dessus de {seuil:+.1f} dBFS : {(db > seuil).sum()}", flush=True)


def hms(t):
    return f"{int(t) // 60}:{t % 60:04.1f}"


ordre = np.argsort(-pk)
vus = []
for i in ordre:
    t = i / 10
    if any(abs(t - v) < 2 for v in vus):
        continue
    vus.append(t)
    a, b = max(0, (i - 2) * win), min(len(x), (i + 3) * win)
    tp = np.abs(resample_poly(x[a:b].astype(np.float64), 4, 1)).max()
    print(f"  {hms(t)} : crête {db[i]:+.2f} dBFS, crête réelle {20 * np.log10(tp):+.2f} dBTP", flush=True)
    if len(vus) >= 15:
        break
