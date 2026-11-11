# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ----------------- COMPONENTS -----------------
# **********************************************

from PySide6.QtWidgets import QLabel, QSizePolicy, QLineEdit, QTextEdit, QFrame, QComboBox
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QMouseEvent

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

class ExpandedTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Enable expand to occupy all the space
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

class ExpandedFrame(QFrame):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Enable expand to occupy all the space
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def mousePressEvent(self, event:QMouseEvent):
        # Emit signal for left button
        if event.button() == Qt.MouseButton.LeftButton: # LeftButton
            self.clicked.emit()
        super().mousePressEvent(event)

class NonScrollingComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, event):
        event.ignore()

class ProportionalImageLabel(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.original_pixmap = pixmap
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    def sizeHint(self):
        if self.original_pixmap.isNull():
            return super().sizeHint()

        # Calculate the proportional width based on the current height of the widget
        current_height = self.height() if self.height() > 0 else 130
        aspect_ratio = self.original_pixmap.width() / self.original_pixmap.height()
        calculated_width = int(current_height * aspect_ratio)

        return QSize(calculated_width, current_height)

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
