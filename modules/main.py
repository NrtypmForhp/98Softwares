# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ---------------- MAIN MODULE -----------------
# **********************************************

import subprocess
from sys import platform

# Constants import
from modules.constants import DATABASE_DIRECTORY

# Session import
from modules.session import session

# Windows Manager import
from modules.windows_manager import windows_manager

# Get printer dict
def get_printers_dict() -> dict:
    printers_list = []
    printers_dict = {}

    # Linux OS
    if platform in ["linux", "linux2"]:
        printers_list = subprocess.check_output(["lpstat", "-e"], encoding="utf-8")
        printers_list = printers_list.split("\n")[:-1]
        for printer in printers_list:
            printers_dict[printer] = printer.upper()

    # Windows OS
    if platform == "win32":
        list_count = 0
        printers = subprocess.check_output(["wmic", "printer", "get", "name"], encoding="utf-8")
        for line in printers.splitlines():
            line = line.strip()
            if len(line) > 0 and list_count !=0: printers_list.append(line)
            list_count += 1
        for printer in printers_list:
            printers_dict[printer] = printer.upper()

    return printers_dict
