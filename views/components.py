# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ----------------- COMPONENTS -----------------
# **********************************************

from PySide6.QtWidgets import QLabel, QSizePolicy, QLineEdit, QComboBox
from PySide6.QtGui import QPalette, QColor

class WrappedLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        # Enable word wrap
        self.setWordWrap(True)

        # Enable expand to occupy all the space neccessary
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

class ExpandedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Enable expand to occupy all the space
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
