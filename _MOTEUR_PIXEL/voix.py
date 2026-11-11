# VOIX : préparer les textes pour ElevenLabs et transcrire les MP3 (temps de chaque mot) pour caler bouches et sous-titres.
#   kit.prompts(REPLIQUES)  -> { "ADO": "réplique 1 [long pause] réplique 2 …", "PAPI": "…" }  (une génération par voix)
#   python voix.py asr "C:/…/voix/" CODE ADO PAPI   -> asr_CODE.json  (faster-whisper medium, sur le processeur)
# Fichiers attendus dans le dossier voix : CODE_ADO.mp3, CODE_PAPI.mp3 … (un fichier par personnage).
import json, os, sys


def _lettres(x):
    import re, unicodedata
    x = re.sub(r"\[[^\]]*\]|\{[^}]*\}", " ", x).replace("ﷺ", " que la paix et le salut d'allah soient sur lui ")
    x = unicodedata.normalize("NFD", x.lower())
    return "".join(ch for ch in x if ch.isalnum() and not unicodedata.combining(ch))


def retrouve(mots, texte):
    """Part du texte prévu (0 à 1) que l'on retrouve dans les mots transcrits."""
    import difflib
    a, b = _lettres(" ".join(w["t"] for w in mots)), _lettres(texte)
    return sum(k.size for k in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks()) / max(1, len(b))


def transcrire(dossier, code, qui, modele="medium", textes=None):
    """textes = {personnage: tout son texte, dans l'ordre} (11/11/2026) : les formules ARABES du texte (repérées par
    estime.arabe) sont données en indice au modèle, qui ne les remplace plus par une formule plus connue ni par de
    l'écriture arabe, et ne saute plus la réplique d'avant. Mesuré : ISL39 80 → 100 % du texte retrouvé, ISL43
    80 → 92 %, ISL32 98 %. Sans arabe dans le texte : écoute simple, comme avant. Si l'indice fait moins bien que
    l'écoute simple, on garde l'écoute simple.
    NE PAS donner tout le texte en indice : essayé, le modèle répète la dernière phrase en boucle (ISL43 : 28 %)."""
    import estime
    from faster_whisper import WhisperModel
    m = WhisperModel(modele, device="cpu", compute_type="int8")
    out = {}

    def ecoute(p, **kw):
        segs, _ = m.transcribe(p, language="fr", word_timestamps=True, vad_filter=False, **kw)
        return [dict(t=w.word.strip(), s=round(w.start, 2), e=round(w.end, 2)) for s in segs for w in s.words]
    for who in qui:
        p = os.path.join(dossier, f"{code}_{who}.mp3")
        prevu = (textes or {}).get(who)
        if prevu:
            arabe = estime.arabe(prevu)[2]
            if arabe:
                out[who] = ecoute(p, initial_prompt="Formules en arabe : " + " ".join(arabe) + ".",
                                  temperature=[0.0], condition_on_previous_text=False)
                part = retrouve(out[who], prevu)
            if not arabe or part < 0.9:                              # pas d'arabe, ou l'indice n'a pas suffi
                simple = ecoute(p)
                if not arabe or retrouve(simple, prevu) > part:
                    out[who], part = simple, retrouve(simple, prevu)
            print("%s : %d %% du texte retrouvé%s" % (who, round(100 * part), "" if part >= 0.85 else
                                                     "  <-- À ÉCOUTER : la voix ne dit peut-être pas tout le texte"),
                  flush=True)
        else:
            out[who] = ecoute(p)
        print(who, " ".join(w["t"] for w in out[who]), flush=True)
    dst = os.path.join(dossier, f"asr_{code}.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False)
    return dst


if __name__ == "__main__":
    if sys.argv[1] == "asr":
        print(transcrire(sys.argv[2], sys.argv[3], sys.argv[4:]))
