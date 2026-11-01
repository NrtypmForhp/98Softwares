# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ---------------- MAIN MODULE -----------------
# **********************************************

import os

# Constants import
from modules.constants import DATABASE_DIRECTORY

# Session import
from modules.session import session

# Windows Manager import
from modules.windows_manager import windows_manager
from views.main import MainWindow
from views.settings import SettingsWindow

# Database and files import
from modules.db import load_settings
from modules.files_handle import load_messages

# ** On start **
def check_files_and_directories() -> None:
    # Check if database directory exists
    if not os.path.exists(DATABASE_DIRECTORY): os.mkdir(DATABASE_DIRECTORY)

def set_session() -> None:
    session.set("settings", load_settings())
    session.set("msg", load_messages())

def register_windows() -> None:
    windows_manager.register_window("main_window", MainWindow)
    windows_manager.register_window("settings_window", SettingsWindow)
