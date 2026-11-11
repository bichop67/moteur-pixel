# Temps de chaque mot des 10 voix de personnages reprises de l'ancienne version (parties 3 à 6) :
# faster-whisper « medium » sur le processeur (4 cœurs), comme voix.py → asr_reutilisees.json
import json
import os

from faster_whisper import WhisperModel

D = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\FILM\EPISODE 14\voix_conte"
SCR = os.path.dirname(os.path.abspath(__file__))
F = ["E14P3_SERVANTE", "E14P4_PHARAON", "E14P4_GARDE", "E14P4_SERVANTE", "E14P5_CONSEILLERS", "E14P5_PHARAON",
     "E14P5_EGYPTIEN", "E14P6_CONSEILLERS", "E14P6_PHARAON", "E14P6_DELATEUR"]
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
out = {}
for f in F:
    segs, _ = m.transcribe(os.path.join(D, f + ".mp3"), language="fr", word_timestamps=True, vad_filter=False)
    out[f] = [dict(t=w.word.strip(), s=round(w.start, 2), e=round(w.end, 2)) for s in segs for w in s.words]
    print(f, "|", " ".join(w["t"] for w in out[f]), flush=True)
json.dump(out, open(os.path.join(SCR, "asr_reutilisees.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("ok")
