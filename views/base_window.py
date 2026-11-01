# **********************************************
# ---------------- 98 SOFTWARES ----------------
# -------------- BASE WINDOW VIEW --------------
# **********************************************

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from modules.files_handle import import_style

# Constants import
from modules.constants import STYLES_DIRECTORY

# Base window class (common settings for all windows)
class BaseWindow(QWidget):
    def __init__(self, title="98Softwares"):
        super().__init__()

        # Destroy window from memory when closed
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        self.setWindowTitle(title)
        self.setMinimumSize(600, 400)
        self.resize(1200, 800)
        try:
          self.setStyleSheet(import_style("dark", STYLES_DIRECTORY))
        except Exception as e:
          print(f"Impossible to load style: {e}")
