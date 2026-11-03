# **********************************************
# ---------------- 98 SOFTWARES ----------------
# **********************************************

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase
import sys, os

# Session import
from modules.session import session

# Modules import
import modules.main as mm

# Windows Manager import
from modules.windows_manager import windows_manager
from views.main import MainWindow
from views.settings import SettingsWindow

# Constants import
from modules.constants import FONTS_DIRECTORY, DATABASE_DIRECTORY

# Database and files import
from modules.db import load_settings
from modules.files_handle import load_messages

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load Kode Mono font
    font_path = os.path.join(FONTS_DIRECTORY, "KodeMono-Variable.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)

    # Get font family, and set it globally for all application
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            custom_font_family = font_families[0]
            global_font = QFont(custom_font_family, 10)
            global_font.setWeight(QFont.Weight.Normal)
            app.setFont(global_font)
    else:
        print("Warning! Error on loading custom font! Default font will be used.")

    # Check if database directory exists
    if not os.path.exists(DATABASE_DIRECTORY): os.mkdir(DATABASE_DIRECTORY)

    # Load session
    load_settings()
    load_messages()

    # Start windows manager
    windows_manager.register_window("main_window", MainWindow)
    windows_manager.register_window("settings_window", SettingsWindow)

    windows_manager.open_window("main_window")
    sys.exit(app.exec())
