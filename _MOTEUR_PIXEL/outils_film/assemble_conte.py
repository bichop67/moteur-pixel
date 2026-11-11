# Assemblage LÉGER du film de Moussa : mêmes enchaînements que assemble_film.py (fondu enchaîné d'1 s entre les parties,
# son croisé, fondu final, -14 LUFS), mais SANS ouvrir les 24 parties en même temps (l'ancienne méthode prenait 9 Go de
# RAM et tout le processeur). Ici : 2 parties lues à la fois, images envoyées une par une à UN seul encodeur.
# Le PC reste utilisable : priorité « faible » et 3 cœurs sur 6 (processeurs logiques 6 à 11) pour tout le travail.
#   python assemble_flux.py            -> film complet + copie légère
#   python assemble_flux.py --test     -> 5 s autour du 1er raccord, pour vérifier couleurs et calage
import ctypes
import glob
import json
import os
import re
import subprocess
import sys
import time
from collections import deque

import numpy as np

# --- priorité faible + 3 cœurs (hérités par tous les ffmpeg lancés ensuite) ---
k32 = ctypes.windll.kernel32
k32.GetCurrentProcess.restype = ctypes.c_void_p                  # sans ces déclarations, l'appel échoue sans rien dire
k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
k32.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
h = k32.GetCurrentProcess()
if not (k32.SetPriorityClass(h, 0x40)                            # IDLE_PRIORITY_CLASS (« Faible »)
        and k32.SetProcessAffinityMask(h, 0xF00)):               # 4 processeurs logiques sur 12 (02/11 : PC utilisable)
    print("ATTENTION : priorité faible / cœurs non réglés", flush=True)

ENGINE = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
EP = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\FILM\EPISODE 14"
SCRATCH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ENGINE)
import assemble_film as af                                       # noqa: E402  (graphe() et duree_image())

FF = af.FF
W, H, FPS, FADE = 1920, 1080, 30, 30
FS = W * H * 3 // 2                                              # une image yuv420p
TEST = "--test" in sys.argv


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def parties():
    d = {}
    for p in glob.glob(ENGINE + r"\scenarios\film\ep14_conte\Moussa conte - partie *.mp4"):
        nom = os.path.basename(p)
        if "(v" in nom or "(leger" in nom:
            continue
        m = re.match(r"Moussa conte - partie (\d+) - ", nom)
        if m:
            d[int(m.group(1))] = p
    manque = [i for i in range(1, 25) if i not in d]
    if manque:
        raise SystemExit(f"parties manquantes : {manque}")
    return [d[i] for i in range(1, 25)]


def images(path, ss=None, t=None):
    """Images d'une partie, une par une (yuv420p, plage « tv » comme la sortie de l'ancien assemblage)."""
    cmd = [FF, "-hide_banner", "-loglevel", "error", "-threads", "2"]
    if ss is not None:
        cmd += ["-ss", f"{ss:.4f}"]
    cmd += ["-i", path]
    if t is not None:
        cmd += ["-t", f"{t:.4f}"]
    cmd += ["-map", "0:v:0", "-fps_mode", "passthrough", "-pix_fmt", "yuvj420p", "-f", "rawvideo", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=FS * 2)
    try:
        while True:
            b = p.stdout.read(FS)
            if not b:
                break
            if len(b) < FS:
                raise RuntimeError(f"image incomplète dans {os.path.basename(path)}")
            yield b
    finally:
        p.stdout.close()
        p.wait()


def melange(a, b, k):
    """Fondu enchaîné : image k (0..29) du raccord, 0 = image A pure."""
    a = np.frombuffer(a, np.uint8).astype(np.uint16)
    b = np.frombuffer(b, np.uint8).astype(np.uint16)
    return ((a * (FADE - k) + b * k + FADE // 2) // FADE).astype(np.uint8).tobytes()


def encodeur(sortie, audio, total):
    cmd = [FF, "-hide_banner", "-loglevel", "error", "-y",
           "-f", "rawvideo", "-pix_fmt", "yuvj420p", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if audio:
        cmd += ["-i", audio, "-map", "0:v", "-map", "1:a", "-c:a", "copy"]
    if total:
        cmd += ["-vf", f"fade=t=out:st={total - 1.5:.4f}:d=1.5"]
    cmd += ["-c:v", "libx264", "-preset", "faster", "-crf", "20", "-threads", "4", "-pix_fmt", "yuvj420p",
            "-colorspace", "bt470bg", "-movflags", "+faststart", sortie]           # comme les parties et la v1
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, bufsize=FS * 2)


def son(liste, durees, sortie):
    """Son du film : mêmes réglages que assemble_film.py (son croisé, fondu final, -14 LUFS en deux passes)."""
    _, fa, _ = af.graphe(durees, 1.0, transition="fade")
    entrees = sum((["-i", p] for p in liste), [])
    mes = subprocess.run([FF, "-hide_banner", *entrees, "-filter_complex",
                          ";".join(fa) + ";[af0]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[am]",
                          "-map", "[am]", "-f", "null", "-"], capture_output=True, text=True, errors="ignore").stderr
    j = json.loads(mes[mes.rfind("{"):mes.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    log(f"son : volume mesuré {j['input_i']} LUFS -> -14 LUFS")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *entrees, "-filter_complex",
                    ";".join(fa) + f";[af0]{ln},{af.LIMITEUR},aresample=48000[am]", "-map", "[am]",
                    "-c:a", "aac", "-b:a", "192k", sortie], check=True)


liste = parties()
if TEST:
    n1 = af.duree_image(liste[0])
    log(f"test : partie 1 = {n1:.2f} s")
    sortie = os.path.join(SCRATCH, "test_raccord.mp4")
    enc = encodeur(sortie, None, None)
    plan = [(liste[0], dict(ss=n1 - 3.0)), (liste[1], dict(t=3.0))]
else:
    durees = [af.duree_image(p) for p in liste]
    nb = [round(d * FPS) for d in durees]
    total_img = sum(nb) - FADE * (len(liste) - 1)
    total = total_img / FPS
    log(f"24 parties, {total_img} images -> {int(total // 60)} min {total % 60:04.1f} s")
    audio = os.path.join(SCRATCH, "moussa_conte_son.m4a")
    son(liste, durees, audio)
    sortie = os.path.join(EP, "Moussa - le film.mp4")
    enc = encodeur(sortie, audio, total)
    plan = [(p, {}) for p in liste]

ecrit, t0 = 0, time.time()


def ecrire(b):
    global ecrit
    enc.stdin.write(b)
    ecrit += 1
    if ecrit % (FPS * 60) == 0:
        v = ecrit / (time.time() - t0)
        reste = ((total_img if not TEST else 150) - ecrit) / max(v, 0.1)
        log(f"{ecrit // (FPS * 60)} min de film faites ({v:.1f} images/s), fin dans ~{reste / 60:.0f} min")


comptes = []
it, lues = images(plan[0][0], **plan[0][1]), 0
for i in range(len(plan)):
    queue = deque()
    for b in it:
        lues += 1
        queue.append(b)
        if len(queue) > FADE:
            ecrire(queue.popleft())
    comptes.append(lues)
    if i == len(plan) - 1:
        for b in queue:
            ecrire(b)
        break
    suite, lues = images(plan[i + 1][0], **plan[i + 1][1]), 0
    for k in range(FADE):
        b = next(suite)
        lues += 1
        ecrire(melange(queue[k], b, k))
    it = suite

enc.stdin.close()
if enc.wait() != 0:
    raise SystemExit("échec de l'encodage")
log(f"images écrites : {ecrit} en {(time.time() - t0) / 60:.1f} min ({ecrit / (time.time() - t0):.1f} images/s)")

if TEST:
    log("test :", sortie)
    sys.exit(0)

ecarts = [(i + 1, c, n) for i, (c, n) in enumerate(zip(comptes, nb)) if c != n]
log("images par partie :", "toutes conformes" if not ecarts else f"ÉCARTS {ecarts}")
if ecrit != total_img:
    log(f"ATTENTION : {ecrit} images écrites au lieu de {total_img}")
log("film :", sortie, f"({os.path.getsize(sortie) / 1e9:.2f} Go)")

leger = os.path.join(EP, "Moussa - le film (leger).mp4")
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", sortie, "-vf", "scale=960:540:flags=neighbor",
                "-c:v", "libx264", "-preset", "faster", "-crf", "27", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", leger], check=True)
log("copie légère :", leger, f"({os.path.getsize(leger) / 1e6:.0f} Mo)")
log("terminé")
