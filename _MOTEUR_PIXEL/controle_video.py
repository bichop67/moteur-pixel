# CONTRÔLE FINAL d'une vidéo rendue : python controle_video.py video.mp4 [autre.mp4 …] [--leger]
#   durée, volume (LUFS, crête), trous de son, planche 1 image / seconde (… _qa.png à côté de la vidéo)
#   --leger : fait aussi une copie légère (… (leger).mp4, moins de 10 Mo environ) pour l'envoyer ou la regarder sur téléphone
import sys, subprocess, re, os
import numpy as np
from pxv import FF


def infos(vid):
    r = subprocess.run([FF, "-hide_banner", "-i", vid, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, errors="ignore").stderr
    tail = r[r.rfind("Summary:"):]
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r)
    d = int(dur.group(1)) * 3600 + int(dur.group(2)) * 60 + float(dur.group(3))
    taille = re.search(r"Stream.*Video.*?(\d{3,4})x(\d{3,4})", r)
    lufs = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
    pic = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
    return d, (int(taille.group(1)), int(taille.group(2))), float(lufs.group(1)) if lufs else None, \
        float(pic.group(1)) if pic else None


def trous(vid, d, seuil_db=-60.0):
    """Tranches de 0,5 s presque silencieuses (hors 0,5 s de début et de fin)."""
    raw = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-i", vid, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = 4000
    out = []
    for i in range(1, int(len(a) / n) - 1):
        rms = float(np.sqrt(np.mean(a[i * n:(i + 1) * n] ** 2)) + 1e-9)
        if 20 * np.log10(rms) < seuil_db:
            out.append(i * 0.5)
    return out


def rythme(vid, fps=4, seuil=1.2, mini=4.0):
    """Repère les passages sans changement visible à l'image pendant plus de `mini` secondes (l'attention décroche).
    Mesure : différence moyenne entre deux images successives (réduites et floutées : le grain du film est ignoré)."""
    w, h = 72, 128
    raw = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-i", vid, "-vf",
                          f"fps={fps},scale={w}:{h}:flags=area,boxblur=1:1", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         capture_output=True).stdout
    n = len(raw) // (w * h)
    a = np.frombuffer(raw[:n * w * h], np.uint8).reshape(n, h, w).astype(np.float32)
    diff = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    calmes, debut = [], None
    for i, d in enumerate(list(diff) + [99]):
        if d < seuil:
            debut = i if debut is None else debut
        else:
            if debut is not None and (i - debut) / fps >= mini:
                calmes.append((round(debut / fps, 1), round(i / fps, 1)))
            debut = None
    changements = int((diff >= seuil * 4).sum())
    return calmes, changements, n / fps


def planche(vid, w, h):
    port = h > w
    tile, cols = ("180:320", 12) if port else ("320:180", 8)
    d = infos(vid)[0]
    rows = int(np.ceil(d / cols))
    png = os.path.splitext(vid)[0] + "_qa.png"
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", vid, "-vf",
                    f"fps=1,scale={tile},tile={cols}x{rows}", "-frames:v", "1", png], check=True)
    return png


def leger(vid, d, mo=9.5):
    out = os.path.splitext(vid)[0] + " (leger).mp4"
    kbps = max(300, int(mo * 8 * 1024 / d) - 112 - 20)
    log = os.path.join(os.environ.get("TEMP", "."), "ia501", "leger2pass")
    base = [FF, "-hide_banner", "-loglevel", "error", "-y", "-i", vid, "-c:v", "libx264", "-preset", "slow", "-b:v", f"{kbps}k",
            "-pix_fmt", "yuv420p", "-passlogfile", log]
    subprocess.run(base + ["-pass", "1", "-an", "-f", "mp4", os.devnull], check=True)
    subprocess.run(base + ["-pass", "2", "-c:a", "aac", "-b:a", "112k", "-movflags", "+faststart", out], check=True)
    return out, os.path.getsize(out) / 1e6


if __name__ == "__main__":
    vids = [v for v in sys.argv[1:] if not v.startswith("--")]
    for vid in vids:
        d, (w, h), lufs, pic = infos(vid)
        t = trous(vid, d)
        print(f"{os.path.basename(vid)} : {d:.1f} s, {w}x{h}, {lufs} LUFS, crête {pic} dBFS, "
              + (f"{len(t)} tranche(s) silencieuse(s) : {t[:12]}" if t else "aucun trou de son"))
        print("  planche :", planche(vid, w, h))
        calmes, chg, dd = rythme(vid)
        print(f"  rythme : {chg} changements nets d'image ({chg / max(1, dd):.1f} par seconde) ; "
              + (f"passages figés de plus de 4 s : {calmes}" if calmes else "aucun passage figé de plus de 4 s"))
        if "--leger" in sys.argv:
            out, mb = leger(vid, d)
            print(f"  copie légère : {out} ({mb:.1f} Mo)")
