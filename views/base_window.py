# **********************************************
# ---------------- 98 SOFTWARES ----------------
# -------------- BASE WINDOW VIEW --------------
# **********************************************

from PySide6.QtWidgets import QWidget, QPushButton, QComboBox, QVBoxLayout, QScrollArea
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

        # ** Scroll area **
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        main_layout.addWidget(self.scroll_area)

        # Inside container for children widgets
        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)

        # Internal layout for subclasses
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(5)

    def showEvent(self, event):
        super().showEvent(event)
        # Set all Buttons and Combobox to use a pointer cursor
        for widget_type in (QPushButton, QComboBox):
            for widget in self.findChildren(widget_type):
                widget.setCursor(Qt.CursorShape.PointingHandCursor)
