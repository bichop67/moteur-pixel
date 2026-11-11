# Lance des commandes du moteur l'une après l'autre en priorité « faible » sur 4 processeurs logiques (0xF00) :
# le PC reste utilisable. Les processus lancés héritent des cœurs (et de la priorité basse).
#   python lance_bas.py "scenario.py|scenarios/x.txt|sheet" "scenario.py|scenarios/y.txt|tout|4"
import ctypes
import os
import subprocess
import sys
import time

k32 = ctypes.windll.kernel32
k32.GetCurrentProcess.restype = ctypes.c_void_p
k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
k32.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
h = k32.GetCurrentProcess()
if not (k32.SetPriorityClass(h, 0x40) and k32.SetProcessAffinityMask(h, 0xF00)):
    print("ATTENTION : priorité / cœurs non réglés", flush=True)

ENGINE = "C:/Users/abdellah/Desktop/VIDEO YOUTUBE/_MOTEUR_PIXEL"
ok = True
for arg in sys.argv[1:]:
    cmd = [sys.executable] + arg.split("|")
    t0 = time.time()
    print(time.strftime("%H:%M:%S"), "→", " ".join(cmd[1:]), flush=True)
    r = subprocess.run(cmd, cwd=ENGINE)
    print(time.strftime("%H:%M:%S"), f"fin ({r.returncode}) en {(time.time() - t0) / 60:.1f} min", flush=True)
    ok = ok and r.returncode == 0
sys.exit(0 if ok else 1)
