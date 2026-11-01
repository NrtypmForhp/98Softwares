# **********************************************
# ---------------- 98 SOFTWARES ----------------
# --------------- SETTINGS VIEW ----------------
# **********************************************

from PySide6.QtWidgets import QVBoxLayout, QLabel, QComboBox
from PySide6.QtCore import Qt
import os

# Base window import
from views.base_window import BaseWindow

# Session import
from modules.session import session

# Constants import
from modules.constants import MESSAGES_DIRECTORY

class SettingsWindow(BaseWindow):
    def __init__(self):
        super().__init__(title=session.get("msg")["settings"]["title"])

        # Set main layout
        self.lay = QVBoxLayout(self)
        self.setLayout(self.lay)
        self.lay.setContentsMargins(10, 10, 10, 10)
        self.lay.setSpacing(1)

        # Language
        self.l_language = QLabel(text=session.get("msg")["settings"]["language"])
        self.l_language.setAccessibleName("l_title")
        self.lay.addWidget(self.l_language, alignment=Qt.AlignmentFlag.AlignCenter)

        self.cb_language = QComboBox()
        # Get languages
        languages_list = os.listdir(MESSAGES_DIRECTORY)
        languages_list.sort()
        self.cb_language.addItems(languages_list)
        self.cb_language.setCurrentText(session.get("settings")["language"])
        self.cb_language.currentTextChanged.connect(self.language_change)
        self.lay.addWidget(self.cb_language, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add a flexible space under all the widgets, to push they up
        self.lay.addStretch(1)

    # When language change
    def language_change(self):
        from modules.files_handle import load_messages

        session.set_dict_value("settings", "language", self.cb_language.currentText())
        session.set("msg", load_messages()) # Reload messages

        self.l_language.setText(session.get("msg")["settings"]["language"])
