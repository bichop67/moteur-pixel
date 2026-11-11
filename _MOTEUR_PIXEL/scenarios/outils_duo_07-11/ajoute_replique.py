# Ajoute une réplique (générée à part) à la fin de la voix d'un perso : original + 1,2 s de silence + nouvelle réplique,
# et recale les temps des mots dans asr_CODE.json. L'original est gardé dans « originales (avant ajout) ».
#   python ajoute_replique.py CODE PERSO URL_MP3 '[["Bon…", 0.92, 1.36], ["je", 1.68, 1.76], ["signe !", 1.92, 2.72]]'
import json
import os
import shutil
import subprocess
import sys

import imageio_ffmpeg
import numpy as np

FF = imageio_ffmpeg.get_ffmpeg_exe()
SC = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL/scenarios"
SR = 44100
code, perso, url, mots = sys.argv[1], sys.argv[2], sys.argv[3], json.loads(sys.argv[4])
dos = os.path.join(SC, "voix_" + code.lower())
src = os.path.join(dos, f"{code}_{perso}.mp3")
garde = os.path.join(dos, "originales (avant ajout)")
os.makedirs(garde, exist_ok=True)
orig = os.path.join(garde, f"{code}_{perso}.mp3")
if not os.path.exists(orig):
    shutil.copy2(src, orig)
    shutil.copy2(os.path.join(dos, f"asr_{code}.json"), os.path.join(garde, f"asr_{code}.json"))
neuf = os.path.join(garde, f"{code}_{perso}_ajout.mp3")
if not os.path.exists(neuf):
    subprocess.run(["curl", "-s", "-L", "-f", "-o", neuf, url], check=True)


def pcm(p):
    raw = subprocess.run([FF, "-v", "error", "-i", p, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16)


a, b = pcm(orig), pcm(neuf)
pause = np.zeros(int(1.2 * SR), np.int16)
dec = (len(a) + len(pause)) / SR                                   # instant où commence la nouvelle réplique
tout_ = np.concatenate([a, pause, b])
subprocess.run([FF, "-v", "error", "-y", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-i", "-",
                "-c:a", "libmp3lame", "-b:a", "192k", src], input=tout_.tobytes(), check=True)
asr = json.load(open(os.path.join(garde, f"asr_{code}.json"), encoding="utf-8"))
asr[perso] = asr[perso] + [dict(t=t, s=round(s + dec, 3), e=round(e + dec, 3)) for (t, s, e) in mots]
json.dump(asr, open(os.path.join(dos, f"asr_{code}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{code} {perso} : {len(a) / SR:.2f} s + 1,2 s + {len(b) / SR:.2f} s = {len(tout_) / SR:.2f} s ; "
      f"réplique ajoutée à {dec:.2f} s ; derniers mots : {asr[perso][-3:]}")
