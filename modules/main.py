# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ---------------- MAIN MODULE -----------------
# **********************************************

from PySide6.QtWidgets import QWidget
from modules.files_handle import import_style

# Constants import
from modules.constants import STYLES_DIRECTORY

# Base window class (common settings for all windows)
class BaseWindow(QWidget):
    def __init__(self, title="98Softwares"):
        super().__init__()

        self.setWindowTitle(title)
        self.setMinimumSize(600, 400)
        self.resize(1200, 800)
        try:
          self.setStyleSheet(import_style("dark", STYLES_DIRECTORY))
        except Exception as e:
          print(f"Impossible to load style: {e}")
