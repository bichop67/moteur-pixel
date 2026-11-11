# Contrôle final du film « conte » assemblé (épisode 14) :
#   1. son : volume intégré (cible -14 LUFS), crête, silences de plus de 2 s ;
#   2. images : début et fin du film (pleine qualité), milieu de chaque raccord entre parties, 1 image toutes les 30 s ;
#   3. transcription des 40 premières et 40 dernières secondes (faster-whisper medium, processeur).
# Priorité « faible » et 4 processeurs logiques sur 12 : le PC reste utilisable.
import ctypes
import glob
import io
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
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
OUT = os.path.join(SCR, "controle_conte")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, ENGINE)
import assemble_film as af  # noqa: E402

FF = af.FF
FILM = os.path.join(EP, "Moussa - le film.mp4")
LEGER = os.path.join(EP, "Moussa - le film (leger).mp4")
FPS, FADE = 30, 30
POLICE = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 18)


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


def hms(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02d}"


def image(src, t, w=320, h=180):
    r = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1",
                        "-vf", f"scale={w}:{h}", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    if not r.stdout:
        return Image.new("RGB", (w, h), (255, 0, 255))
    return Image.open(io.BytesIO(r.stdout)).convert("RGB")


def planche(tuiles, cols, nom):
    w, h = tuiles[0][0].size
    rows = (len(tuiles) + cols - 1) // cols
    pl = Image.new("RGB", (cols * (w + 4), rows * (h + 4)), (40, 40, 40))
    d = ImageDraw.Draw(pl)
    for i, (im, lab) in enumerate(tuiles):
        x, y = (i % cols) * (w + 4), (i // cols) * (h + 4)
        pl.paste(im, (x, y))
        d.rectangle([x, y, x + 9 * len(lab) + 8, y + 22], fill=(0, 0, 0))
        d.text((x + 4, y + 2), lab, font=POLICE, fill=(255, 255, 0))
    p = os.path.join(OUT, nom)
    pl.save(p)
    print("planche :", p, flush=True)


def son():
    r = subprocess.run([FF, "-hide_banner", "-nostats", "-i", FILM, "-vn", "-af",
                        "ebur128=peak=true:framelog=verbose,silencedetect=n=-45dB:d=2", "-f", "null", "-"],
                       capture_output=True, text=True, errors="ignore").stderr
    resume = r[r.rfind("Summary:"):]
    for cle in ("I:", "LRA:", "Peak:"):
        m = re.search(re.escape(cle) + r"\s+(-?[\d.]+|-inf)\s+(\w+)", resume)
        if m:
            print(f"son {cle} {m.group(1)} {m.group(2)}", flush=True)
    sil = re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", r)
    print(f"silences de plus de 2 s : {len(sil)}", flush=True)
    for a, b, d in sil:
        print(f"   {hms(float(a))} -> {hms(float(b))} ({float(d):.1f} s)", flush=True)


def transcrire(total):
    from faster_whisper import WhisperModel
    m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
    for nom, ss in (("debut", 0.0), ("fin", total - 40.0)):
        wav = os.path.join(OUT, f"{nom}.wav")
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{ss:.2f}", "-t", "40", "-i", FILM,
                        "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
        segs, _ = m.transcribe(wav, language="fr", vad_filter=False)
        print(f"--- transcription {nom} ({hms(ss)} -> {hms(ss + 40)}) ---", flush=True)
        for s in segs:
            print(f"   [{hms(ss + s.start)}] {s.text.strip()}", flush=True)


liste = parties()
nb = [round(af.duree_image(p) * FPS) for p in liste]
debuts = [0]
for n in nb[:-1]:
    debuts.append(debuts[-1] + n - FADE)
total = (sum(nb) - FADE * (len(nb) - 1)) / FPS
print(f"durée attendue : {hms(total)} ({total:.2f} s)", flush=True)

if "--son" in sys.argv or len(sys.argv) == 1:
    son()

if "--images" in sys.argv or len(sys.argv) == 1:
    ts = [0.5, 3, 8, 15, 25, 36, total - 30, total - 15, total - 8, total - 4, total - 1.5, total - 0.1]
    planche([(image(FILM, t, 640, 360), hms(t) if t < total - 1 else f"{t:.1f} s") for t in ts], 3,
            "debut_fin.png")
    planche([(image(LEGER, (debuts[i] + FADE // 2) / FPS), f"p{i}>p{i + 1} {hms((debuts[i] + 15) / FPS)}")
             for i in range(1, 24)], 6, "raccords.png")
    tous = [(image(LEGER, t), hms(t)) for t in range(15, int(total), 30)]
    for k in range(0, len(tous), 36):
        planche(tous[k:k + 36], 6, f"film_30s_{k // 36 + 1}.png")

if "--transcrire" in sys.argv or len(sys.argv) == 1:
    transcrire(total)
print("contrôle terminé", flush=True)
