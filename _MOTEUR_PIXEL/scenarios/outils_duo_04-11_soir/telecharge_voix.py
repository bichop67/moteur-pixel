# Télécharge les 12 voix ElevenLabs des 6 Shorts duo du 04/11/2026 (soir) dans scenarios\voix_islNN\CODE_PERSO.mp3.
# Flux ElevenLabs « Shorts duo islam 04-11 soir (cent, coran, telephone, tombe, soleil, enfer) » (19YCz4hsVZHurRdqf62r).
# Ne réécrit jamais un fichier existant.
import os
import subprocess

SC = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL/scenarios"
BASE = "https://elevenlabsusercontent.com/database/workspace/4af90bdbfe834541ace57a9dac8d2dd1/content_generation/"
FIN = "/content.mp3?Expires=1793836800&KeyName=assets-cdn-key-1&Signature="

VOIX = [  # (code, perso, session, génération, signature)
    ("ISL11", "PETIT", "MeD4OAn8e0BzcZLgf4It", "CHDLBe4PBlll6Yi3pFrb", "GPamRIPs7T0tZ5vrEYoqImLQEsU="),
    ("ISL11", "GRAND", "8lBUxSMe0DbeSelKwuUo", "r7nyeS8IFDuwEF4RAImQ", "QytjPQa-96SoVbETBbOqA11MCzw="),
    ("ISL12", "PETIT", "am44A14dYYsUlre8fazV", "Tw0HKWuH4YraA2ICF8MA", "bmkEM-lxkeR9H3aLh6rBQYm5CmU="),
    ("ISL12", "GRAND", "gHZKWGPMZSQ8J7v1egAs", "qMvG8u5ecHhICSjnlVZb", "RzbKgYabE8nc5h02oQVKpq_tqsA="),
    ("ISL13", "PETIT", "nhw3kLY6hMYxjHuCeitk", "eZofR0PztPrk1tdNmu6S", "f2mcnHE0LndQZ4rZYD4DK7xCVKM="),
    ("ISL13", "GRAND", "Ug4DtFltxJo2qVX6F4ap", "qixczGayiG3bF521IjXK", "TLr9lljCXvJxdCVQbC4F5a_2gz0="),
    ("ISL14", "PETIT", "m6PhY6P9JoyghDIgrSHb", "dAaMBML9m5LbZQguilF8", "JZMTZYrkqU3QTlHdsif1fn_kdow="),
    ("ISL14", "GRAND", "EPPTNIeyDLhs7PoPMZ5Q", "97wLgAoCywmj2uSLeHUa", "Bu-B5Cqhgj_Eenoz4RUi8r1asMo="),
    ("ISL15", "PETIT", "ElhRJeBZvjJq8bT3vQ2S", "jS9Hy8VQLpnKzhzb0baA", "bNzFDmtADAGitKpYXa3s9i9n2PA="),
    ("ISL15", "GRAND", "2B3j8S6Ybd8SabzCRyy2", "vnrUgZDXHicqwEvN5Raq", "ECO5xAkt09ao5B3xsvlUYlnjF0o="),
    ("ISL16", "PETIT", "w7IgcBWEvoicZ0m1km80", "C2KcOfAm5M0qjPOkhJzs", "9uv8HNlSljMVgbvVm6qUhjZVTKc="),
    ("ISL16", "GRAND", "cpaMq65v0fBJpzeDwmnN", "MqvpxfxCyY4b8vKmFvAE", "cmNhGJytbDF7YW5SffZ85QJiIWA="),
]

for (code, perso, sess, gen, sig) in VOIX:
    dossier = os.path.join(SC, "voix_" + code.lower())
    os.makedirs(dossier, exist_ok=True)
    dst = os.path.join(dossier, f"{code}_{perso}.mp3")
    if os.path.exists(dst):
        print("déjà là :", dst)
        continue
    r = subprocess.run(["curl", "-s", "-L", "-f", "-o", dst, BASE + f"{sess}/{gen}" + FIN + sig])
    if r.returncode != 0 or not os.path.exists(dst):
        raise SystemExit(f"téléchargement impossible : {code} {perso}")
    print(f"{code} {perso} : {os.path.getsize(dst) / 1024:.0f} Ko -> {dst}")
