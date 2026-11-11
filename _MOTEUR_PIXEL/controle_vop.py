# (11/11/2026) NE TOURNE PLUS : les voix des VOP ont quitté le PC (il manque asr_VOP06.json). Utiliser à la place
#   python controle_moteur.py     (scènes de référence sans aucune voix, dont le rendu d'origine des VOP)
# CONTRÔLE après toute modification du moteur : les Shorts VOP déjà livrés doivent sortir identiques au pixel près.
#   python controle_vop.py          -> compare aux empreintes enregistrées (OK ou liste des images qui ont changé)
#   python controle_vop.py enregistre   -> (seulement si un changement voulu a été validé) enregistre de nouvelles empreintes
import sys, os, io, json, runpy, hashlib, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
REF = os.path.join(HERE, "controle_vop.json")
CASES = [("vop06.py", None, [0.5, 3.0, 8.0, 15.0, 30.0]), ("vop_suite.py", "VOP09", [0.5, 4.0, 12.0, 25.0]),
         ("vop_suite.py", "VOP04", [1.0, 9.0, 31.0])]


def empreintes():
    out = {}
    for script, sk, ts in CASES:
        sys.argv = [script] + ([sk, "info"] if sk else [])
        with contextlib.redirect_stdout(io.StringIO()):
            g = runpy.run_path(script, run_name="controle")
        for t in ts:
            a = np.asarray(g["VID"].frame(t).convert("RGB"))
            out[f"{sk or 'VOP06'}@{t}"] = hashlib.md5(a.tobytes()).hexdigest()
    return out


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "verifie"
    cur = empreintes()
    if mode == "enregistre":
        json.dump(cur, open(REF, "w"), indent=1)
        print("empreintes enregistrées :", len(cur))
    else:
        ref = json.load(open(REF))
        bad = [k for k in ref if ref[k] != cur.get(k)]
        print("OK : les VOP sont identiques" if not bad else "ATTENTION, images changées : " + ", ".join(bad))
