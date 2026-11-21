# **********************************************
# ---------------- 98 SOFTWARES ----------------
# **********************************************

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase
import sys, os

# Constants import
from modules.constants import FONTS_DIRECTORY, DATABASE_DIRECTORY

# Check if database directory exists
os.makedirs(DATABASE_DIRECTORY, exist_ok=True)

# Windows Manager import
from modules.windows_manager import windows_manager
from views.main import MainWindow
from views.settings import SettingsWindow
from views.orders import OrdersWindow

# Threads Manager import
from modules.threads_manager import threads_manager, CallableThread

# Database and files import
from modules.db import load_settings, ping_mongo
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

    # Load session
    load_settings()
    load_messages()

    # Start windows manager
    windows_manager.register_window("main_window", MainWindow)
    windows_manager.register_window("settings_window", SettingsWindow)
    windows_manager.register_window("orders_window", OrdersWindow)

    # Start thread manager
    threads_manager.register_thread(
        "db_ping",
        lambda conn_str, timeout=3000: CallableThread(ping_mongo, conn_str, timeout_ms=timeout)
    )

    windows_manager.open_window("main_window")
    sys.exit(app.exec())
