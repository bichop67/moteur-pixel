"""Télécharge les voix ElevenLabs listées dans un fichier « nom url » vers FILM\\EPISODE 14\\voix (sans écraser)."""
import io
import os
import sys
import urllib.request

DST = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\FILM\EPISODE 14\voix"
ok, ko = 0, []
for ligne in io.open(sys.argv[1], encoding="utf-8"):
    ligne = ligne.strip()
    if not ligne:
        continue
    nom, url = ligne.split(" ", 1)
    out = os.path.join(DST, nom)
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        continue
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            data = r.read()
        if len(data) < 1000 or not (data[:3] == b"ID3" or data[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")):
            raise ValueError(f"réponse inattendue ({len(data)} octets)")
        io.open(out, "wb").write(data)
        ok += 1
    except Exception as e:  # noqa: BLE001
        ko.append((nom, str(e)[:80]))
print(f"{ok} fichier(s) téléchargé(s) ; échecs : {ko}")
print(len([f for f in os.listdir(DST) if f.endswith('.mp3')]), "MP3 dans le dossier voix")
