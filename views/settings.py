# **********************************************
# ---------------- 98 SOFTWARES ----------------
# --------------- SETTINGS VIEW ----------------
# **********************************************

from PySide6.QtWidgets import QVBoxLayout, QLabel, QComboBox, QLineEdit
from PySide6.QtCore import Qt
import os

# Base window import
from views.base_window import BaseWindow

# Components import
from views.components import WrappedLabel, ExpandedLineEdit

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
        self.lay.setSpacing(5)

        # Language
        self.l_language = WrappedLabel(text=session.get("msg")["settings"]["language"])
        self.l_language.setAccessibleName("l_title")
        self.l_language.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.l_language)

        self.cb_language = QComboBox()
        # Get languages
        languages_list = os.listdir(MESSAGES_DIRECTORY)
        languages_list.sort()
        self.cb_language.addItems(languages_list)
        self.cb_language.setCurrentText(session.get("settings")["language"])
        self.cb_language.currentTextChanged.connect(self.language_change)
        self.lay.addWidget(self.cb_language, alignment=Qt.AlignmentFlag.AlignCenter)

        self.lay.addSpacing(20)

        # Database connection
        self.l_db_connection_title = WrappedLabel(text=session.get("msg")["settings"]["database-connection-title"])
        self.l_db_connection_title.setAccessibleName("l_title")
        self.l_db_connection_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.l_db_connection_title)

        self.l_db_connection_description = WrappedLabel(text=session.get("msg")["settings"]["database-connection-description"])
        self.l_db_connection_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.l_db_connection_description)

        self.l_db_connection_local_warning = WrappedLabel(text=session.get("msg")["settings"]["database-connection-local-warning"])
        self.l_db_connection_local_warning.setAccessibleName("red")
        self.l_db_connection_local_warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.l_db_connection_local_warning)

        self.le_db_connection = ExpandedLineEdit()
        self.le_db_connection.setPlaceholderText(session.get("msg")["settings"]["database-connection-title"])
        self.lay.addWidget(self.le_db_connection)

        # Add a flexible space under all the widgets, to push they up
        self.lay.addStretch()

    # When language change
    def language_change(self):
        from modules.files_handle import load_messages

        session.set_dict_value("settings", "language", self.cb_language.currentText())
        session.set("msg", load_messages()) # Reload messages

        self.l_language.setText(session.get("msg")["settings"]["language"])
        self.l_db_connection_title.setText(session.get("msg")["settings"]["database-connection-title"])
        self.l_db_connection_description.setText(session.get("msg")["settings"]["database-connection-description"])
        self.l_db_connection_local_warning.setText(session.get("msg")["settings"]["database-connection-local-warning"])
        self.le_db_connection.setPlaceholderText(session.get("msg")["settings"]["database-connection-title"])
