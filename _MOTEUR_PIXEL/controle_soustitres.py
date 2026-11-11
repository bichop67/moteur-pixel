# CONTRÔLE DES SOUS-TITRES (02/11/2026, après « les sous-titres ne sont pas raccordés au texte » sur le film de Moussa) :
# compare l'instant où chaque mot s'affiche (calage du moteur) à l'instant où il est VRAIMENT dit dans la vidéo rendue
# (transcription faster-whisper du son final).
#   python controle_soustitres.py scenarios\film\ep14_conte\p15.txt "<partie>.mp4"
# Résultat : écart médian, liste des répliques où des mots s'affichent trop tôt / trop tard (> 0,45 s), et un verdict.
import difflib
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

SEUIL = 0.45


def norm(x):
    x = x.replace("ﷺ", " quelapaixetlesalutdallahsoientsurlui ")
    x = unicodedata.normalize("NFD", x.lower())
    return "".join(ch for ch in x if ch.isalnum() and not unicodedata.combining(ch))


def mots_du_moteur(scenario):
    ici = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, ici)
    old = sys.argv
    sys.argv = [os.path.join(ici, "scenario.py")]
    try:
        import scenario as sc_
        VID = sc_.fabrique(os.path.abspath(scenario))[0]
    finally:
        sys.argv = old
    out = []
    for k, L in enumerate(VID.dlg.lines):
        for w in L["words"]:
            out.append(dict(t=w["t"], s=float(w["s"]), k=k, who=L["who"]))
    return out, VID.dlg


def transcription(video):
    import pxv
    wav = os.path.join(tempfile.gettempdir(), "ctrl_st_" + str(os.getpid()) + ".wav")
    subprocess.run([pxv.FF, "-hide_banner", "-loglevel", "error", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000",
                    wav], check=True)
    from faster_whisper import WhisperModel
    modele = os.environ.get("CTRL_ST_MODELE", "small")              # « small » suffit pour les temps (3x plus rapide)
    m = WhisperModel(modele, device="cpu", compute_type="int8", cpu_threads=4)
    segs, _ = m.transcribe(wav, language="fr", word_timestamps=True, vad_filter=False)
    mots = [dict(t=w.word.strip(), s=float(w.start)) for s in segs for w in s.words]
    os.remove(wav)
    return mots


def compare(moteur, asr):
    a_chars, a_t = [], []
    for w in asr:
        for ch in norm(w["t"]):
            a_chars.append(ch); a_t.append(w["s"])
    b_chars, b_i = [], []
    for i, w in enumerate(moteur):
        for ch in norm(w["t"]):
            b_chars.append(ch); b_i.append(i)
    sm = difflib.SequenceMatcher(None, "".join(a_chars), "".join(b_chars), autojunk=False)
    t_dit = {}
    for blk in sm.get_matching_blocks():
        for j in range(blk.size):
            t_dit.setdefault(b_i[blk.b + j], a_t[blk.a + j])
    return t_dit


def main():
    scenario, video = sys.argv[1], sys.argv[2]
    moteur, D = mots_du_moteur(scenario)
    print(f"{len(moteur)} mots affichés ; transcription de la vidéo…", flush=True)
    asr = transcription(video)
    t_dit = compare(moteur, asr)
    ecarts = [(i, moteur[i]["s"] - t_dit[i]) for i in t_dit]
    if not ecarts:
        raise SystemExit("aucun mot retrouvé dans la transcription")
    absd = sorted(abs(e) for _, e in ecarts)
    med = absd[len(absd) // 2]
    trouves = len(t_dit) / max(1, len(moteur))
    par_ligne = {}
    for i, e in ecarts:
        if abs(e) > SEUIL:
            par_ligne.setdefault(moteur[i]["k"], []).append((moteur[i]["t"], e))
    print(f"mots retrouvés à l'oral : {trouves:.0%} ; écart médian affichage / voix : {med:.2f} s")
    for k in sorted(par_ligne):
        L = D.lines[k]
        mauvais = par_ligne[k]
        n_l = sum(1 for w in moteur if w["k"] == k)
        if len(mauvais) < max(2, 0.25 * n_l):                     # un ou deux mots isolés : bruit de transcription
            continue
        txt = " ".join(w["t"] for w in L["words"])[:110]
        moy = sum(e for _, e in mauvais) / len(mauvais)
        print(f"  réplique {k + 1} ({L['who']}, {L['t0']:.1f} s) : {len(mauvais)}/{n_l} mots décalés "
              f"({'trop tôt' if moy < 0 else 'trop tard'} de {abs(moy):.2f} s en moyenne) — « {txt} »")
    graves = [k for k in par_ligne if len(par_ligne[k]) >= max(2, 0.25 * sum(1 for w in moteur if w["k"] == k))]
    print("VERDICT :", "OK, sous-titres calés sur la voix" if (med < 0.25 and not graves and trouves > 0.85)
          else f"À REVOIR ({len(graves)} réplique(s) décalée(s))")


if __name__ == "__main__":
    main()
