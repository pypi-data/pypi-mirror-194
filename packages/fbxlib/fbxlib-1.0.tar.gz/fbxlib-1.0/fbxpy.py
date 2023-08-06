import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
libdir = os.path.join(current_dir, "lib")

os.makedirs(libdir, exist_ok=True)

if not os.path.isfile("./lib/fbx.so"):
    os.system(f'wget --no-check-certificate \'https://docs.google.com/uc?export=download&id=1ZkcpPNOkeRXt4gaYuBP_J3nk0twUUCYQ\' -O {os.path.join(libdir, "fbx.so")}')
    
if not os.path.isfile("./lib/fbxsip.so"):
    os.system(f'wget --no-check-certificate \'https://docs.google.com/uc?export=download&id=1S0fMr28-L2PJZ4mTOXG5BIFylxcIMwWS\' -O {os.path.join(libdir, "fbxsip.so")}')

sys.path.append(libdir)

from fbx import *