# Lance une ou plusieurs commandes en priorité « faible » sur 8 des 12 processeurs logiques (le PC reste utilisable).
#   python basse.py "cmd 1" "cmd 2" …      (les commandes s'enchaînent ; arrêt à la première erreur)
import ctypes
import subprocess
import sys
import time

k32 = ctypes.windll.kernel32
k32.GetCurrentProcess.restype = ctypes.c_void_p
k32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
k32.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
h = k32.GetCurrentProcess()
if not (k32.SetPriorityClass(h, 0x40) and k32.SetProcessAffinityMask(h, 0xF00)):   # 4 processeurs sur 12 (02/11 :
    #                                                                     « j'arrive plus à utiliser mon ordinateur »)
    print("ATTENTION : priorité faible / cœurs non réglés", flush=True)
for cmd in sys.argv[1:]:
    t = time.time()
    print(time.strftime("%H:%M:%S"), ">>", cmd, flush=True)
    r = subprocess.run(cmd, shell=True)
    print(time.strftime("%H:%M:%S"), f"fin ({(time.time() - t) / 60:.1f} min, code {r.returncode})", flush=True)
    if r.returncode:
        sys.exit(r.returncode)
