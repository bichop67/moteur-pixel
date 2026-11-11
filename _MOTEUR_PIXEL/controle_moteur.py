# CONTRÔLE DU MOTEUR, SANS AUCUNE VOIX (11/11/2026) — remplace controle_vop.py, qui ne tourne plus depuis que les voix
# des VOP ont quitté le PC. À lancer AVANT et APRÈS toute modification du moteur :
#   python controle_moteur.py                 compare aux empreintes enregistrées : OK, ou liste des images qui ont changé
#                                             (+ planche controle_moteur_ecarts.png : référence à gauche, maintenant à droite)
#   python controle_moteur.py verifie gog     seulement les scènes dont le nom contient « gog »
#   python controle_moteur.py enregistre      (seulement après un changement VOULU et regardé) nouvelles empreintes
#   python controle_moteur.py liste           les scènes de référence
# Principe : des scènes de référence (rendu d'origine des VOP, Shorts en scénario, films) sont fabriquées en MAQUETTE
# (durées estimées d'après le texte, même si les voix existent) ; quelques images de chacune sont comparées au pixel près.
import hashlib
import io
import json
import os
import sys
import time
import contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
REF = os.path.join(HERE, "controle_moteur.json")
VIGNETTES = os.path.join(HERE, "controle_moteur_ref")
ECARTS = os.path.join(HERE, "controle_moteur_ecarts.png")
FRACTIONS = (0.06, 0.24, 0.43, 0.62, 0.81, 0.96)

# scènes de référence : (nom court, fichier de scénario) ; « @vop » = le rendu d'origine (sans thème), construit ici
SCENES = [
    ("vop_origine", "@vop"),
    ("demo_dialogue", "scenarios/demo_dialogue_vivant.txt"),
    ("demo_briques", "scenarios/demo_9_briques.txt"),
    ("demo_explique", "scenarios/demo_8_jurer_eternuement_colere_maison_dette_sommeil.txt"),
    ("short_tombe", "scenarios/islam_14_tombe.txt"),
    ("short_droite", "scenarios/islam_25_droite.txt"),
    ("short_coucher", "scenarios/islam_31_coucher.txt"),
    ("short_vent", "scenarios/islam_35_vent.txt"),
    ("moussa_p01", "scenarios/film/ep14_conte/p01.txt"),
    ("moussa_p06", "scenarios/film/ep14_conte/p06.txt"),
    ("moussa_p12", "scenarios/film/ep14_conte/p12.txt"),
    ("moussa_p17", "scenarios/film/ep14_conte/p17.txt"),
    ("gog_p03", "scenarios/film/gog/p03.txt"),
    ("gog_p06", "scenarios/film/gog/p06.txt"),
    ("gog_p07", "scenarios/film/gog/p07.txt"),
    ("gog_p09", "scenarios/film/gog/p09.txt"),
]


def _vop():
    """Le rendu d'origine (Video sans thème) : un plan à deux et un gros plan, bouches animées, sans voix."""
    import kit
    import pxv
    plans = [kit.duo_plan(0.0, 4.0, "salon", "P", "G", g=dict(pose="question"), d=dict(pose="explique")),
             kit.gros_plan(4.0, 8.0, "P", "salon", face="choc", bulle="?")]
    return pxv.Video(pxv.Silence(8.0, parle=[("G", 0.4, 3.4), ("P", 4.3, 7.0)]), plans)


def video(source):
    """La vidéo d'une scène de référence, toujours en maquette (aucune voix lue)."""
    import kit
    if source == "@vop":
        return _vop()
    import scenario
    vrai = kit.dialogue
    # maquette à 15 caractères par seconde, toujours : les empreintes ne dépendent ni des voix présentes sur le PC, ni
    # des vitesses de voix mesurées (estime.py), qui changent quand on les remesure
    kit.dialogue = lambda voix, code, repliques, gaps=None, avant=None, serre=False, **_: kit.Maquette(repliques, avant=avant)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return scenario.fabrique(os.path.join(HERE, source))[0]
    finally:
        kit.dialogue = vrai


def images(filtre=""):
    """{« scène@instant » : image} pour toutes les scènes de référence présentes sur le disque."""
    for nom, source in SCENES:
        if filtre and not any(f in nom for f in filtre.split(",")):       # « gog » ou « demo,short »
            continue
        if source != "@vop" and not os.path.exists(os.path.join(HERE, source)):
            print(f"  ({nom} : scénario absent, ignoré : {source})", flush=True)
            continue
        t0 = time.time()
        vid = video(source)
        for f in FRACTIONS:
            t = round(vid.dlg.dur * f, 2)
            yield f"{nom}@{t}", vid.frame(t).convert("RGB")
        print(f"  {nom} : {time.time() - t0:.0f} s", flush=True)


def _vignette(cle):
    return os.path.join(VIGNETTES, cle.replace("@", "_").replace(".", "-") + ".jpg")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "verifie"
    filtre = sys.argv[2] if len(sys.argv) > 2 else ""
    if mode == "liste":
        for nom, source in SCENES:
            print(f"{nom:16s} {source}")
        return 0
    from PIL import Image
    ref = json.load(open(REF, encoding="utf-8")) if os.path.exists(REF) else {}
    cur, change = {}, []
    os.makedirs(VIGNETTES, exist_ok=True)
    for cle, im in images(filtre):
        cur[cle] = hashlib.md5(im.tobytes()).hexdigest()
        if mode == "enregistre":
            im.resize((480, 480 * im.height // im.width), Image.BILINEAR).save(_vignette(cle), quality=88)
        elif cle in ref and ref[cle] != cur[cle]:
            change.append((cle, im.resize((480, 480 * im.height // im.width), Image.BILINEAR)))
    if mode == "enregistre":
        ref.update(cur)
        json.dump(ref, open(REF, "w", encoding="utf-8"), indent=1, sort_keys=True)
        print(f"empreintes enregistrées : {len(cur)} images ({len(ref)} au total)")
        return 0
    nouvelles = [k for k in cur if k not in ref]
    perdues = [k for k in ref if k not in cur and (not filtre or any(f in k.split("@")[0] for f in filtre.split(",")))]
    if nouvelles:
        print("sans référence (lancer « enregistre ») :", ", ".join(nouvelles))
    if perdues:
        print("ATTENTION, images de référence qui n'existent plus (durée changée ?) :", ", ".join(perdues))
    if not change and not perdues:
        print(f"OK : {len(cur) - len(nouvelles)} images identiques au pixel près")
        if os.path.exists(ECARTS):
            os.remove(ECARTS)
        return 0
    if change:
        print("ATTENTION, images changées :", ", ".join(k for k, _ in change))
        lignes = change[:40]
        h = max(im.height for _, im in lignes)
        g = Image.new("RGB", (480 * 2 + 12, (h + 6) * len(lignes)), (30, 30, 30))
        for i, (cle, im) in enumerate(lignes):
            if os.path.exists(_vignette(cle)):
                g.paste(Image.open(_vignette(cle)).convert("RGB"), (0, i * (h + 6)))
            g.paste(im, (492, i * (h + 6)))
        g.save(ECARTS)
        print("planche des écarts (référence à gauche, maintenant à droite) :", ECARTS)
    return 1


if __name__ == "__main__":
    sys.exit(main())
