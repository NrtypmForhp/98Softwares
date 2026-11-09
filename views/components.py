# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ----------------- COMPONENTS -----------------
# **********************************************

from PySide6.QtWidgets import QLabel, QSizePolicy, QLineEdit, QFrame
from PySide6.QtCore import Qt

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

class ExpandedFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Enable expand to occupy all the space
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

class ProportionalImageLabel(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.original_pixmap = pixmap
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.original_pixmap.isNull():
            # Resize pixmap to adapt original height
            scaled = self.original_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.setPixmap(scaled)
