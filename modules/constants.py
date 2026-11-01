# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ------------- CONSTANTS MODULE ---------------
# **********************************************

import os

# Main directories
CONSTANTS_PATH = os.path.abspath(__file__)
CONSTANTS_DIRECTORY = os.path.dirname(CONSTANTS_PATH)
APP_ROOT = os.path.dirname(CONSTANTS_DIRECTORY) # Root directory (where main.py is located)
STYLES_DIRECTORY = os.path.join(APP_ROOT, "styles")
MODULES_DIRECTORY = os.path.join(APP_ROOT, "modules")
MESSAGES_DIRECTORY = os.path.join(APP_ROOT, "messages")
PICTURES_DIRECTORY = os.path.join(APP_ROOT, "pictures")
RESOURCES_DIRECTORY = os.path.join(APP_ROOT, "resources")
FONTS_DIRECTORY = os.path.join(RESOURCES_DIRECTORY, "fonts")

# Database directory
DATABASE_DIRECTORY = os.path.join(APP_ROOT, "database")
