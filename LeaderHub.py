import os
import time
import random

# Terminal colors
G = "\033[92m"
R = "\033[91m"
C = "\033[96m"
Y = "\033[93m"
W = "\033[97m"
RESET = "\033[0m"

os.system("clear")

# Banner
print(G + """
██╗   ██╗██╗████████╗██╗  ██╗██╗   ██╗
██║   ██║██║╚══██╔══╝██║  ██║██║   ██║
╚██╗ ██╔╝██║   ██║   ███████║██║   ██║
 ╚████╔╝ ██║   ██║   ██╔══██║╚██████╔╝
  ╚═══╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝

          V I T H U   D E V
""" + RESET)

print(C + "[+] Initializing VITHU DEV..." + RESET)
time.sleep(1)

# Fake demo logs
logs = [
    "Loading Python modules",
    "Initializing system",
    "Checking environment",
    "Loading LeaderHub components",
    "Connecting local runtime",
    "Preparing terminal interface",
    "System initialization completed"
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

print("\n" + C + "========== OUTPUT ==========" + RESET)
print(G + "Hello" + RESET)
print(C + "============================" + RESET)
print(Y + "Powered by VITHU DEV" + RESET)
