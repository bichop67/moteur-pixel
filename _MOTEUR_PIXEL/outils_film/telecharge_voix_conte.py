# Télécharge les 43 voix de la version « conte » (parties 3-14, 16-24) dans voix_conte, sans jamais écraser un fichier.
#   python telecharge_voix.py <résultat_lot1.json>
import json
import os
import subprocess
import sys

D = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\FILM\EPISODE 14\voix_conte"
SCR = os.path.dirname(os.path.abspath(__file__))
BASE = ("https://elevenlabsusercontent.com/database/workspace/4af90bdbfe834541ace57a9dac8d2dd1/content_generation/"
        "{s}/{g}/content.mp3?Expires=1793653200&KeyName=assets-cdn-key-1&Signature={sig}")

fic = {}                                                     # session -> nom de fichier
for line in open(os.path.join(SCR, "sessions_voix.txt"), encoding="utf-8"):
    p = line.split()
    if len(p) == 3 and p[0].endswith(".mp3"):
        fic[p[2]] = p[0]

urls = {}
for f in sys.argv[1:]:                                       # lot 1 : résultat complet enregistré par l'outil
    d = json.load(open(f, encoding="utf-8"))
    for g in d["generations"]:
        s = g["content_url"].split("/content_generation/")[1].split("/")[0]
        urls[s] = g["content_url"]

LOTS_2_3 = [                                                 # lots 2 et 3 : (session, génération, signature)
    ("nF1hhUB5LjKiYh37PcBi", "phPZaJw3uq0E8GbvTdZE", "5PhpJvL19xGw4RTk3ulN8xWdXME="),
    ("3BH8MJbKnQAj1DsbYLH3", "2kMTQvCv7YkwbidtvtBW", "2R8lZSVSSuKKRjGKOXmYId5pXf0="),
    ("Xc2OedtL5UsRXmjxqrNK", "hWp5J0eKfw3ENhGG4E5k", "wEWtYg_2_RAnQ5oojD2udlX3up0="),
    ("wPe3mUWpIVuijcGZvjPj", "hlhzqc2hjtBwAgwkIeKw", "lgqzSdTgKCq9T3yN0dmiPrNEI1w="),
    ("rBmrIVr6no1t1SuwmHoy", "txktY4rht57M0dhqELyp", "MiZw5YeEG_yllExT9LHKNXoaroU="),
    ("094Ims1ze9v3gbobxQkl", "Cw9oWYz1yjwgaSQ0tNfo", "FB_YTVpCAdbISvuY0_yWah-vN2E="),
    ("3JeiFBLJdEgygfOSv2z4", "cFqaS8PZ45rMBlYNwTy4", "5yA_vhQCKJz66bmnl2xkdJ28RX0="),
    ("MezA9VtduTtxcyDjAxcW", "h30BZPNw8PxSRpsYERpo", "HEMR8h7YRjTNDclM4M1vZGLCsYE="),
    ("erZWGySRF5WZmHBL65sp", "fPqt8djelt3dYHfS2R0U", "GM5m7Tyq13QgYN6GzcJ-m5myC1k="),
    ("DwD1VEfHJpJRophVQAtB", "NtVjl6huo5ovxQf3OFBZ", "gcYFwjaZ-6G_u3u4ECEWlMfXsuw="),
    ("6fDPxvV2VyIUoOn0vibF", "drzKwbhhdabS4xamfalf", "ol-4tJO4XToSrgDged1wlSvdpls="),
    ("1fRmHsKgc2R6A8m86KE7", "8yatNLohgqQHvKcXPAVj", "e0jgicDEjnYzKH3RCfPGnBVE2Ac="),
    ("egEsdPyuL2ayrIGdUtbC", "HuNQyQtTWCufF5GKy2gk", "S3boC5-xl9SnbIGqzGaW7ZlSbH4="),
    ("WbwEpZK1VRoRDhbpPdBd", "SYB4cJ3Ja5AdbZTnifEa", "vDXfJdKvvmbutqhIfoTfQyZa6Pg="),
    ("u0C5xvoPlDDjXJZ0yqT6", "YfFfTAFNxvOBAQw1tYtO", "687viMFoEc8PhYQI44oK3p8PQt8="),
    ("aXPnUtW1cyjoV71gUnmc", "QxSJWxjALx5R8qwKwiX7", "z2LpvtB9RziIlz9xBRva6yUqx_0="),
    ("osDfibDhiG7qVfZeG57S", "NndiSOAAIE4JsTNpUfOL", "kxth6wZ9aMobatiAocWaf2_YHB8="),
    ("eFCId0tDS2dt4HqNPZcB", "MQVEssokaqgbrQr512N6", "J4rQs7VunLeYWTb-t7lciFDlcMA="),
    ("w7MO4veoOsCnWqKyFS6W", "pFT1W5Z1SLbEjfYcgcYn", "HREx5lCs2Poo4VrEs7wlp20PSW8="),
    ("FAyS4gWHt7OCFlr8R6KW", "AqVfJ67j38p0M70938CZ", "Js1WQ6z2vbkjakxRVQZmUQjdqqc="),
    ("bF67cb7DCP6Wzclzf55n", "DFF9ybWV4zXsoeEhwkbE", "JvbmLyfGo_Mz22gSVtN9Ezze7U8="),
    ("duWzKrRFttqe5cZSL3Z1", "q6iY7gRlQCrJvPueg9od", "hMxF3GCky9qKV5bvBEzg6PHOTUY="),
    ("uty8kZwv0J0UmFJoReOP", "wtSFBtFtgZ3Pafb1yKNU", "QdcumI0wJ_SYlNZlM1ibXZCIC1Q="),
    ("f7f5ZB9UdBtVnWFd4sve", "gfXiHwYSRd8jRq0IYzJk", "tyysgVemTc6MIxKfxGDTydE3noM="),
    ("mhEsdCYhGaKApDYWAKot", "N3pWdO0Haj06rwg9wGUN", "cXAhTeuIIY6nmzPcwbT5f9UgrHw="),
    ("uj5Ifa2aK4TtIygzkwZn", "NX01fIJPhDj0mmq06JOa", "kndJWRSl6fcpG3aA3a2SkeGRdjE="),
    ("uZ9XCpAYv1xUrUoqn4E3", "OmYTsMvcqQLBndN93kjk", "zzNs-jc7mE7a5Vo3m6DXezSumKo="),
    ("acAcnOaoqNPCL6tPTOjp", "6vT0VeQ9YlShtjoJNsXC", "8zlL4yG5mSmRdgJo1xtcYNh-pjk="),
]
for s, g, sig in LOTS_2_3:
    urls.setdefault(s, BASE.format(s=s, g=g, sig=sig))

print("sans lien :", [f for s, f in fic.items() if s not in urls])
ok_n = 0
for s, nom in fic.items():
    if s not in urls:
        continue
    dst = os.path.join(D, nom)
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        print("déjà là :", nom)
        ok_n += 1
        continue
    r = subprocess.run(["curl", "-s", "-L", "-f", "--retry", "2", "-o", dst, urls[s]])
    taille = os.path.getsize(dst) if os.path.exists(dst) else 0
    ok = r.returncode == 0 and taille > 1000
    ok_n += ok
    print(("OK     " if ok else "ÉCHEC  ") + nom, f"{taille / 1e6:.2f} Mo", flush=True)
print(f"{ok_n}/{len(fic)} fichiers présents")
