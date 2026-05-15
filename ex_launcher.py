import os
import subprocess
import sys
import time

LOGO = """\
\u2593\u2588\u2588\u2588\u2588\u2588 \u2592\u2588\u2588   \u2588\u2588\u2592 \u2592\u2588\u2588\u2588\u2588\u2588  \u2593\u2588\u2588\u2588\u2588\u2588\u2584  \u2588    \u2588\u2588   \u2588\u2588\u2588\u2588\u2588\u2588 
\u2593\u2588   \u2580 \u2592\u2592 \u2588 \u2588 \u2592\u2591\u2592\u2588\u2588\u2592  \u2588\u2588\u2592\u2592\u2588\u2588\u2580 \u2588\u2588\u258c \u2588\u2588  \u2593\u2588\u2588\u2592\u2592\u2588\u2588    \u2592 
\u2592\u2588\u2588\u2588   \u2591\u2591  \u2588   \u2591\u2592\u2588\u2588\u2591  \u2588\u2588\u2592\u2591\u2588\u2588   \u2588\u258c\u2593\u2588\u2588  \u2592\u2588\u2588\u2591\u2591 \u2593\u2588\u2588\u2584   
\u2592\u2593\u2588  \u2584  \u2591 \u2588 \u2588 \u2592 \u2592\u2588\u2588   \u2588\u2588\u2591\u2591\u2593\u2588\u2584   \u258c\u2593\u2593\u2588  \u2591\u2588\u2588\u2591  \u2592   \u2588\u2588\u2592
\u2591\u2592\u2588\u2588\u2588\u2588\u2592\u2592\u2588\u2588\u2592 \u2592\u2588\u2588\u2592\u2591 \u2588\u2588\u2588\u2588\u2593\u2592\u2591\u2591\u2592\u2588\u2588\u2588\u2588\u2593 \u2592\u2592\u2588\u2588\u2588\u2588\u2588\u2593 \u2592\u2588\u2588\u2588\u2588\u2588\u2588\u2592\u2592
\u2591\u2591 \u2592\u2591 \u2591\u2592\u2592 \u2591 \u2591\u2593 \u2591\u2591 \u2591\u2592\u2591\u2592\u2591\u2592\u2591  \u2592\u2592\u2593  \u2592 \u2591\u2592\u2593\u2592 \u2592 \u2592 \u2592 \u2592\u2593\u2592 \u2592 \u2591
 \u2591 \u2591  \u2591\u2591\u2591   \u2591\u2592 \u2591  \u2591 \u2592 \u2592\u2591  \u2591 \u2592  \u2592 \u2591\u2591\u2592\u2591 \u2591 \u2591 \u2591 \u2591\u2592  \u2591 \u2591
   \u2591    \u2591    \u2591  \u2591 \u2591 \u2591 \u2592   \u2591 \u2591  \u2591  \u2591\u2591\u2591 \u2591 \u2591 \u2591  \u2591  \u2591  
   \u2591  \u2591 \u2591    \u2591      \u2591 \u2591     \u2591       \u2591           \u2591  
                          \u2591                        """

RED   = '\033[91m'
WHITE = '\033[97m'
DIM   = '\033[2;37m'
RESET = '\033[0m'
INFO1   = "Low resources python DOS/HTTP flood tool" 
SEP      = DIM + "\u2500" * 56 + RESET
INFO_STR = f"{INFO1} by Retribution.          (v1.1)"


def clr():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

clr()    
print(RED + LOGO + RESET)
print(WHITE + "\n" + INFO_STR + RESET)
print('\n', SEP, '\n')

print('Loading dependences')
time.sleep(0.1)
print("Creating Python venv if doesn't exist...")
time.sleep(0.1)
print('Password may be required')
time.sleep(0.5)
subprocess.run('sudo python3 -m venv venv',
    shell=True,
    executable='/bin/bash',)
venv_python = os.path.expanduser("~/venv/bin/python")
print('Python venv Loaded')
base_dir = os.path.dirname(os.path.abspath(__file__))
target_script = os.path.join(base_dir, "exodus_new.py")
print('Loading EXODUS')
time.sleep(0.1)
print('\n Load Complete, launching EXODUS by Retribution')
time.sleep(1)
os.execv(venv_python, [venv_python, target_script] + sys.argv[1:])
