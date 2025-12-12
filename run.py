import os
import subprocess
import sys
import time

BANNER = r"""
============================================================
                 PROJECT INITIALIZER v1.0
               Powered by Ciel — System Module
------------------------------------------------------------
   • Checking environment
   • Installing dependencies
   • Initializing runtime
   • Launching main application
============================================================
"""

CREDITS = r"""
------------------------------------------------------------
                   DEVELOPMENT CREDITS
------------------------------------------------------------
   Project Owner   : Hillorius
   Core Developer  : Hillorius
   Environment     : Python {py}
------------------------------------------------------------
""".format(py=sys.version.split()[0])


def run_command(cmd):
    """Run a shell command safely and stream output."""
    process = subprocess.Popen(cmd, shell=True)
    process.communicate()

    if process.returncode != 0:
        print(f"[ERROR] Command failed: {cmd}")
        sys.exit(process.returncode)


def install_requirements():
    """Install packages from requirements.txt if available."""
    req_file = "requirements.txt"

    if not os.path.exists(req_file):
        print("[INFO] No requirements.txt found. Skipping installation.")
        return

    print("[SETUP] Installing dependencies...")
    run_command(f"{sys.executable} -m pip install -r {req_file}")


def launch_main():
    """Start main.py with the current Python interpreter."""
    if not os.path.exists("main.py"):
        print("[ERROR] main.py not found.")
        return

    print("\n[BOOT] Launching main.py...\n")
    time.sleep(0.6)
    run_command(f"{sys.executable} main.py")


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)
    time.sleep(0.5)

    print(CREDITS)
    time.sleep(0.5)

    install_requirements()
    launch_main()


if __name__ == "__main__":
    main()