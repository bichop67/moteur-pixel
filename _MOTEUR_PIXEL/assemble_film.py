# ASSEMBLAGE D'UN FILM EN PLUSIEURS PARTIES :
#   python assemble_film.py sortie.mp4 partie1.mp4 partie2.mp4 … [--noir 1.0] [--crf 20] [--preset slow] [--leger]
#                                                                [--transition fondu|noir]
# - les parties s'enchaînent par un FONDU ENCHAÎNÉ (xfade fade : la dernière image se fond dans la suivante, sans écran
#   noir) et le son se croise (acrossfade). Décision du 02/11/2026 : le passage au noir entre deux parties (ancienne
#   règle, --transition noir) donnait l'impression d'un film « emboîté », coupé en morceaux ;
# - le son de chaque partie est calé à la durée exacte de son image (aucun décalage qui s'accumule) ;
# - fondu au noir à la fin (image et son) ;
# - tout le film est normalisé à -14 LUFS, crête -1,5 dBTP (loudnorm en deux passes : mesure, puis réglage exact),
#   puis un limiteur à -1,5 dBFS (03/11/2026 : loudnorm avait laissé passer un pic de +2 dBFS dans Moussa « conte ») ;
# - --leger : copie 960x540 (pixels nets) pour regarder sur téléphone ou l'envoyer.
import json
import os
import re
import subprocess
import sys

from pxv import FF, FPS

# Limiteur placé après loudnorm (sortie à 192 kHz : crête quasi « réelle »), retard compensé, sans « niveau auto ».
LIMITEUR = "alimiter=limit=0.8414:attack=1:release=50:level=false:latency=true"


def duree_image(vid):
    """Durée exacte de l'image (nombre d'images / FPS), sans décoder."""
    r = subprocess.run([FF, "-hide_banner", "-i", vid, "-map", "0:v:0", "-c", "copy", "-f", "null", "-"],
                       capture_output=True, text=True, errors="ignore").stderr
    m = re.findall(r"frame=\s*(\d+)", r)
    if not m:
        raise SystemExit(f"illisible : {vid}")
    return int(m[-1]) / FPS


def graphe(durees, noir, fin=1.5, transition="fade"):
    """Filtres image et son : enchaînements (fondu enchaîné, ou au noir), son croisé, fondu final.
    Renvoie (fv, fa, durée totale)."""
    fv, fa = [], []
    for i, d in enumerate(durees):                              # son de chaque partie = durée exacte de son image
        fa.append(f"[{i}:a]aresample=48000,apad,atrim=0:{d:.4f},asetpts=PTS-STARTPTS[s{i}]")
    v, a = "[0:v]", "[s0]"
    t = durees[0]
    for i in range(1, len(durees)):
        fv.append(f"{v}[{i}:v]xfade=transition={transition}:duration={noir}:offset={t - noir:.4f}[v{i}]")
        fa.append(f"{a}[s{i}]acrossfade=d={noir}:c1=tri:c2=tri[a{i}]")
        v, a = f"[v{i}]", f"[a{i}]"
        t += durees[i] - noir
    fv.append(f"{v}fade=t=out:st={t - fin:.4f}:d={fin}[vf]")
    fa.append(f"{a}afade=t=out:st={t - fin:.4f}:d={fin}[af0]")
    return fv, fa, t


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    opt = {}
    for k in ("noir", "crf", "preset", "transition"):
        if f"--{k}" in sys.argv:
            opt[k] = sys.argv[sys.argv.index(f"--{k}") + 1]
            args.remove(opt[k])
    noir = float(opt.get("noir", 1.0))
    transition = "fadeblack" if opt.get("transition", "fondu") in ("noir", "fadeblack") else "fade"
    out, parts = os.path.abspath(args[0]), [os.path.abspath(p) for p in args[1:]]
    durees = [duree_image(p) for p in parts]
    fv, fa, total = graphe(durees, noir, transition=transition)
    print("enchaînements :", "fondu enchaîné (sans écran noir)" if transition == "fade" else "passage au noir", flush=True)
    entrees = sum((["-i", p] for p in parts), [])
    print(f"{len(parts)} partie(s) : " + ", ".join(f"{d:.2f} s" for d in durees) + f" -> {total:.1f} s au total", flush=True)

    # 1re passe : mesure du volume du film entier (son seulement)
    mes = subprocess.run([FF, "-hide_banner", *entrees, "-filter_complex",
                          ";".join(fa) + ";[af0]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[am]",
                          "-map", "[am]", "-f", "null", "-"], capture_output=True, text=True, errors="ignore").stderr
    j = json.loads(mes[mes.rfind("{"):mes.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    print(f"volume mesuré : {j['input_i']} LUFS -> -14 LUFS", flush=True)

    # 2e passe : image + son réglé
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *entrees, "-filter_complex",
                    ";".join(fv + fa) + f";[af0]{ln},{LIMITEUR},aresample=48000[am]",
                    "-map", "[vf]", "-map", "[am]", "-c:v", "libx264", "-preset", opt.get("preset", "slow"),
                    "-crf", opt.get("crf", "20"), "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", out], check=True)
    print("film :", out, f"({os.path.getsize(out) / 1e6:.0f} Mo)", flush=True)
    if "--leger" in sys.argv:
        leger = os.path.splitext(out)[0] + " (leger).mp4"
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", out, "-vf", "scale=960:540:flags=neighbor",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                        "-movflags", "+faststart", leger], check=True)
        print("copie légère :", leger, f"({os.path.getsize(leger) / 1e6:.0f} Mo)", flush=True)


if __name__ == "__main__":
    main()
