# Recolle E14P4_NARRATEUR_A + _B et E14P9_NARRATEUR_A + _B (1 s de silence entre les deux) en un seul MP3,
# puis mesure où commence B dans le fichier final (pour décaler les mots de sa transcription).
import json
import os
import subprocess

import numpy as np

FF = r"C:\Users\abdellah\AppData\Local\Temp\ia501\bin\ffmpeg.exe"
D = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\FILM\EPISODE 14\voix_conte"
SCR = os.path.dirname(os.path.abspath(__file__))
SR = 44100
GAP = 1.0


def lit(p):
    r = subprocess.run([FF, "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).copy()


out = {}
dst_json = os.path.join(SCR, "decalages_ab.json")
if os.path.exists(dst_json):
    out = json.load(open(dst_json, encoding="utf-8"))
for code in ("E14P4", "E14P9"):
    a = lit(os.path.join(D, f"{code}_NARRATEUR_A.mp3"))
    b = lit(os.path.join(D, f"{code}_NARRATEUR_B.mp3"))
    dst = os.path.join(D, f"{code}_NARRATEUR.mp3")
    if not os.path.exists(dst):
        x = np.concatenate([a, np.zeros(int(GAP * SR), np.float32), b])
        subprocess.run([FF, "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                        "-c:a", "libmp3lame", "-b:a", "192k", dst], input=x.tobytes(), check=True)
    y = lit(dst)
    attendu = len(a) + int(GAP * SR)
    ref = b[:SR * 3]                                          # 3 premières secondes de B
    best, off = -1.0, attendu
    for d in range(-2000, 2001, 1):                           # cherche le décalage réel à ± 45 ms près
        i = attendu + d
        seg = y[i:i + len(ref)]
        if len(seg) < len(ref):
            continue
        c = float(np.dot(seg, ref) / (np.linalg.norm(seg) * np.linalg.norm(ref) + 1e-9))
        if c > best:
            best, off = c, i
    out[code] = dict(debut_B=off / SR, attendu=attendu / SR, correlation=round(best, 4),
                     duree_A=len(a) / SR, duree_B=len(b) / SR, duree_totale=len(y) / SR)
    print(code, out[code], flush=True)
json.dump(out, open(dst_json, "w", encoding="utf-8"), indent=1)
