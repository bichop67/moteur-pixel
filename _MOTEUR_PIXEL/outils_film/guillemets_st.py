"""Sous-titres du film « conte » : où un guillemet est-il mal placé ?
 (a) sous-titre qui commence par un signe fermant (« » Et Allah leur a répondu : ») ;
 (b) ligne faite seulement d'un signe fermant (« » » seul sur la 2e ligne) ;
 (c) ligne ou sous-titre qui finit par « « » (le guillemet ouvrant séparé de ses mots).
python guillemets_st.py [parties…]   (sans argument : les 24)"""
import contextlib
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
MOTEUR = r"C:\Users\abdellah\Desktop\VIDEO YOUTUBE\_MOTEUR_PIXEL"
sys.path.insert(0, MOTEUR)
os.chdir(MOTEUR)
sys.argv, nums = ["scenario.py"], [int(a) for a in sys.argv[1:]] or list(range(1, 25))
import pxv  # noqa: E402
import scenario  # noqa: E402

FERM = "»\")]’”"
COLLE = "--avant" not in sys.argv          # --avant : règle d'avant le 03/11 (sans guillemets collés)
sys.argv = [a for a in sys.argv if a != "--avant"]


def fermant(w):
    w = w.strip()
    return bool(w) and w[0] in FERM and not any(ch.isalnum() for ch in w)


def lignes(txt, largeur):
    t = txt.replace(" ?", "\u00a0?").replace(" !", "\u00a0!").replace(" :", "\u00a0:")
    if COLLE:
        t = t.replace(" \u00bb", "\u00a0\u00bb").replace("\u00ab ", "\u00ab\u00a0")
    out, cur = [], ""
    for w in [w for w in t.split(" ") if w]:
        if cur and len(cur.replace("*", "")) + 1 + len(w.replace("*", "")) > largeur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


total = 0
for n in nums:
    path = os.path.join(MOTEUR, "scenarios", "film", "ep14_conte", f"p{n:02d}.txt")
    with contextlib.redirect_stdout(io.StringIO()):
        V = scenario.fabrique(path)[0]
    larg = getattr(V.theme, "st_largeur", 16)
    pb = []
    for c in V.subs:
        mots = c["txt"].split()
        ls = lignes(c["txt"], larg)
        if mots and fermant(mots[0]):
            pb.append(("a", c))
        elif any(all(fermant(w) for w in l.replace("\u00a0", " ").split()) for l in ls[1:]):
            pb.append(("b", c))
        elif any(l.rstrip().endswith("«") for l in ls) or c["txt"].rstrip().endswith("«"):
            pb.append(("c", c))
    total += len(pb)
    print(f"p{n:02d} : {len(V.subs)} sous-titres, {len(pb)} à revoir", flush=True)
    for k, c in pb:
        print(f"   ({k}) {c['t0']:7.1f} s  {' / '.join(lignes(c['txt'], larg))}", flush=True)
print("TOTAL à revoir :", total)
