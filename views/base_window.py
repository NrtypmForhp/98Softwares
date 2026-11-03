# **********************************************
# ---------------- 98 SOFTWARES ----------------
# -------------- BASE WINDOW VIEW --------------
# **********************************************

from PySide6.QtWidgets import QWidget, QPushButton, QComboBox
from PySide6.QtCore import Qt
from modules.files_handle import import_style

# Session import
from modules.session import session

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
          self.setStyleSheet(import_style(session.get("settings")["style"], STYLES_DIRECTORY))
        except Exception as e:
          print(f"Impossible to load style: {e}")

    def showEvent(self, event):
        super().showEvent(event)
        # Set all Buttons and Combobox to use a pointer cursor
        for widget_type in (QPushButton, QComboBox):
            for widget in self.findChildren(widget_type):
                widget.setCursor(Qt.CursorShape.PointingHandCursor)
