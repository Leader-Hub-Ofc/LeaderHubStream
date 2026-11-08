import os
import time
import random
import subprocess
import platform
import getpass

# Terminal colors
G = "\033[92m"
R = "\033[91m"
C = "\033[96m"
Y = "\033[93m"
W = "\033[97m"
RESET = "\033[0m"

PASSWORD = "vithu2008"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def getprop(prop):
    try:
        return subprocess.check_output(
            ["getprop", prop],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip() or "Unknown"
    except:
        return "Not available"

clear()

# VITHU DEV Banner
print(G + """
██╗   ██╗██╗████████╗██╗  ██╗██╗   ██╗
██║   ██║██║╚══██╔══╝██║  ██║██║   ██║
╚██╗ ██╔╝██║   ██║   ███████║██║   ██║
 ╚████╔╝ ██║   ██║   ██╔══██║╚██████╔╝
  ╚═══╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝

          V I T H U   D E V
""" + RESET)

print(C + "\n[+] Initializing VITHU DEV..." + RESET)
time.sleep(1)

logs = [
    "Loading Python modules",
    "Checking environment",
    "Loading LeaderHub components",
    "Preparing terminal interface",
    "Initialization completed"
]

for log in logs:
    print(G + "[SUCCESS] " + W + log + RESET)
    time.sleep(0.5)

# Coding animation
print(Y + "\n[+] Starting animation...\n" + RESET)

chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ#$@"

for i in range(20):
    line = "".join(random.choice(chars) for _ in range(55))
    print(G + line + RESET)
    time.sleep(0.08)

# Password screen
print(C + "\n================================" + RESET)
print(G + "          SECURITY LOGIN" + RESET)
print(C + "================================" + RESET)

entered = getpass.getpass(Y + "\nEnter Password: " + RESET)

if entered != PASSWORD:
    print(R + "\n[ACCESS DENIED] Wrong Password!" + RESET)
    raise SystemExit

print(G + "\n[ACCESS GRANTED] Welcome VITHU DEV!" + RESET)
time.sleep(1)

clear()

# Mobile Information
print(G + """
================================
       VITHU DEV
     MOBILE INFORMATION
================================
""" + RESET)

print(C + "\n[ DEVICE INFORMATION ]" + RESET)

print(W + "Device Model : " +
      getprop("ro.product.model"))

print("Manufacturer : " +
      getprop("ro.product.manufacturer"))

print("Brand        : " +
      getprop("ro.product.brand"))

print("Android      : " +
      getprop("ro.build.version.release"))

print("SDK Version  : " +
      getprop("ro.build.version.sdk"))

print("Device Name  : " +
      getprop("ro.product.device"))

print(C + "\n[ SYSTEM INFORMATION ]" + RESET)

print("Architecture : " + platform.machine())
print("Python       : " + platform.python_version())
print("System       : " + platform.system())

try:
    kernel = subprocess.check_output(
        ["uname", "-r"], text=True
    ).strip()
    print("Kernel       : " + kernel)
except:
    print("Kernel       : Unknown")

print(C + "\n================================" + RESET)
print(G + "      VITHU DEV SYSTEM READY" + RESET)
print(C + "================================" + RESET)

print(Y + "\nPowered by VITHU DEV" + RESET)
