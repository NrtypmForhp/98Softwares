# **********************************************
# ---------------- 98 SOFTWARES ----------------
# **********************************************

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase
import sys, os

# Modules import
import modules.main as mm

# Windows Manager import
from modules.windows_manager import windows_manager

# Constants import
from modules.constants import FONTS_DIRECTORY

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

    # Start check and session set
    mm.check_files_and_directories()
    mm.set_session()
    mm.register_windows()

    windows_manager.open_window("main_window")
    sys.exit(app.exec())
