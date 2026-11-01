# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ----------------- MAIN VIEW ------------------
# **********************************************

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os

# Base window import
from views.base_window import BaseWindow

# Windows Manager import
from modules.windows_manager import windows_manager

# Session import
from modules.session import session

# Constants import
from modules.constants import PICTURES_DIRECTORY

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__(title=session.get("msg")["main_view"]["title"])

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

        # Center empty stretch to move the settings button to right
        top_frame_lay.addStretch()

        # Settings button (right side)
        b_settings = QPushButton(session.get("msg")["main_messages"]["settings"])
        b_settings.setAccessibleName("b_yellow")
        b_settings.clicked.connect(self.settings_button)
        top_frame_lay.addWidget(b_settings)

    # Settings button
    def settings_button(self):
        windows_manager.open_window("settings_window")
