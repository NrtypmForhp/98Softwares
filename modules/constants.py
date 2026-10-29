# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ------------- CONSTANTS MODULE ---------------
# **********************************************

import os

from modules.files_handle import load_messages

# Main directories
CONSTANTS_PATH = os.path.abspath(__file__)
CONSTANTS_DIRECTORY = os.path.dirname(CONSTANTS_PATH)
APP_ROOT = os.path.dirname(CONSTANTS_DIRECTORY) # Root directory (where main.py is located)
STYLES_DIRECTORY = os.path.join(APP_ROOT, "styles")
MODULES_DIRECTORY = os.path.join(APP_ROOT, "modules")
MESSAGES_DIRECTORY = os.path.join(APP_ROOT, "messages")
PICTURES_DIRECTORY = os.path.join(APP_ROOT, "pictures")

# Messages dict
MSG = load_messages(MESSAGES_DIRECTORY)
