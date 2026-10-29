# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ----------------- MAIN VIEW ------------------
# **********************************************

from pydoc import text

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QCursor
import os

# Modules import
import modules.main as mm

# Constants import
from modules.constants import MSG, PICTURES_DIRECTORY

class MainWindow(mm.BaseWindow):
    def __init__(self):
        super().__init__(title=MSG["main_view"]["title"])

        # Set main layout
        self.lay = QVBoxLayout(self)
        self.setLayout(self.lay)
        self.lay.setContentsMargins(10, 10, 10, 10)
        self.lay.setSpacing(1)

        # ** Main frames with specific layout **
        top_frame = QFrame()
        top_frame_lay = QHBoxLayout(top_frame)
        self.lay.addWidget(top_frame, stretch=2) # Stretch to 20% of space

        bottom_frame = QFrame()
        bottom_frame_lay = QVBoxLayout(bottom_frame)
        self.lay.addWidget(bottom_frame, stretch=8) # Stretch to 80% of space

        # ** Top Frame **

        # Logo (left side)
        l_logo = QLabel()
        picture_pixmap = QPixmap(os.path.join(PICTURES_DIRECTORY, "logo.png"))
        l_logo.setPixmap(picture_pixmap)
        l_logo.resize(picture_pixmap.width(), picture_pixmap.height())
        top_frame_lay.addWidget(l_logo)

        # Center empty stretch to move the options button to right
        top_frame_lay.addStretch()

        # Options button (right side)
        b_options = QPushButton(MSG["main_messages"]["options"])
        b_options.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        top_frame_lay.addWidget(b_options)
