import io, os, re, subprocess, imageio_ffmpeg
SC = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL\scenarios"
DUO = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\SHORTS DUO"
DEST = os.path.join(DUO, "A METTRE EN LIGNE - 9 Shorts du 08-11")
LEG = os.path.join(DUO, "copies legeres (pour le telephone)")
FICH = ["islam_23_talons", "islam_24_urine", "islam_25_droite", "islam_26_imam", "islam_27_asr",
        "islam_28_medisance", "islam_29_ecoute", "islam_30_horoscope", "islam_31_coucher"]
FF = imageio_ffmpeg.get_ffmpeg_exe()
os.makedirs(DEST, exist_ok=True); os.makedirs(LEG, exist_ok=True)
fiche = ["9 SHORTS DUO DU 08/11/2026 — titres et descriptions (voir aussi les fiches détaillées dans _MOTEUR_PIXEL\\scenarios\\outils_duo_08-11\\fiches)\n"]
for i, f in enumerate(FICH, 1):
    titre = next(l.split(":", 1)[1].strip() for l in io.open(os.path.join(SC, f + ".txt"), encoding="utf-8") if l.startswith("TITRE:"))
    src, srcl = os.path.join(SC, titre + ".mp4"), os.path.join(SC, titre + " (leger).mp4")
    dst = os.path.join(DEST, f"{i} - {titre}.mp4")
    if os.path.exists(src) and not os.path.exists(dst):
        os.rename(src, dst)
    if os.path.exists(srcl):
        os.rename(srcl, os.path.join(LEG, f"08-11 - {i} - {titre} (leger).mp4"))
    r = subprocess.run([FF, "-i", dst], capture_output=True, text=True, errors="replace").stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r)
    d = float(m.group(3)) + 60 * int(m.group(2)) if m else 0
    print(f"{i} - {titre} : {d:.1f} s")
    code = "ISL%d" % (22 + i)
    fp = os.path.join(SC, "outils_duo_08-11", "fiches", code + ".md")
    fiche.append(f"\n{'=' * 50}\n{i} - {titre}.mp4  ({d:.1f} s)\n{'=' * 50}\n")
    fiche.append(io.open(fp, encoding="utf-8").read() if os.path.exists(fp) else "(fiche manquante)\n")
io.open(os.path.join(DEST, "Titres et descriptions.txt"), "w", encoding="utf-8").write("".join(fiche))
