# **********************************************
# ---------------- 98 SOFTWARES ----------------
# --------------- SETTINGS VIEW ----------------
# **********************************************

from PySide6.QtWidgets import QVBoxLayout, QPushButton, QComboBox, QLineEdit, QMessageBox, QApplication
from PySide6.QtCore import Qt
import os, sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Base window import
from views.base_window import BaseWindow

# Components import
from views.components import WrappedLabel, ExpandedLineEdit

# Session import
from modules.session import session

# Modules import
from modules.main import get_printers_dict
from modules.db import write_settings

# Constants import
from modules.constants import MESSAGES_DIRECTORY, STYLES_DIRECTORY

class SettingsWindow(BaseWindow):
    def __init__(self):
        super().__init__(title=session.get("msg")["settings"]["title"])

        # Set main layout
        self.lay = QVBoxLayout(self)
        self.setLayout(self.lay)
        self.lay.setContentsMargins(10, 10, 10, 10)
        self.lay.setSpacing(5)

        # Style
        self.l_style = WrappedLabel(text=session.get("msg")["settings"]["style"])
        self.l_style.setAccessibleName("l_title")
        self.l_style.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.l_style)

        self.l_style_description = WrappedLabel(text=session.get("msg")["settings"]["style-description"])
        self.l_style_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.l_style_description)

        self.cb_styles = QComboBox()
        # Get styles
        styles_list = os.listdir(STYLES_DIRECTORY)

        # Remove .txt
        new_styles_list = [style.replace(".txt", "") for style in styles_list]

        new_styles_list.sort()

        self.cb_styles.addItems(new_styles_list)
        if "style" in session.get("settings") and session.get("settings")["style"] in new_styles_list:
            self.cb_styles.setCurrentText(session.get("settings")["style"])
        self.lay.addWidget(self.cb_styles, alignment=Qt.AlignmentFlag.AlignCenter)

        self.lay.addSpacing(20)

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
        if session.get("settings")["language"] in languages_list:
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
        if "db_connection" in session.get("settings"):
            self.le_db_connection.setText(session.get("settings")["db_connection"])
        self.le_db_connection.setPlaceholderText(session.get("msg")["settings"]["database-connection-title"])
        self.lay.addWidget(self.le_db_connection)

        self.lay.addSpacing(20)

        # Default printer selection
        self.l_default_printer_title = WrappedLabel(text=session.get("msg")["settings"]["default-printer-title"])
        self.l_default_printer_title.setAccessibleName("l_title")
        self.l_default_printer_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.l_default_printer_title)

        self.l_default_printer_selection_description = WrappedLabel(text=session.get("msg")["settings"]["default-printer-selection-description"])
        self.l_default_printer_selection_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.l_default_printer_selection_description)

        self.printers_dict = get_printers_dict()
        printers_list = []
        for printer in self.printers_dict:
            printers_list.append(self.printers_dict[printer])
        self.cb_printers_list = QComboBox()
        self.cb_printers_list.addItem("") # First item blank
        self.cb_printers_list.addItems(printers_list)
        if "default_printer" in session.get("settings") and session.get("settings")["default_printer"] in printers_list:
            self.cb_printers_list.setCurrentText(session.get("settings")["default_printer"])
        self.lay.addWidget(self.cb_printers_list, alignment=Qt.AlignmentFlag.AlignCenter)

        # Printer paper width
        self.l_default_printer_paper_width_description = WrappedLabel(text=session.get("msg")["settings"]["default-printer-paper-width-description"])
        self.l_default_printer_paper_width_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.l_default_printer_paper_width_description)

        self.le_default_printer_paper_width = QLineEdit()
        if "default_printer_paper_width" in session.get("settings"):
            self.le_default_printer_paper_width.setText(str(session.get("settings")["default_printer_paper_width"]))
        self.le_default_printer_paper_width.setPlaceholderText(session.get("msg")["settings"]["default-printer-paper-width-placeholder"])
        self.lay.addWidget(self.le_default_printer_paper_width, alignment=Qt.AlignmentFlag.AlignCenter)

        self.lay.addSpacing(20)

        # Confirm button
        self.l_confirm_restart_warning = WrappedLabel(text=session.get("msg")["settings"]["confirm-restart-warning"])
        self.l_confirm_restart_warning.setAccessibleName("red")
        self.l_confirm_restart_warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.l_confirm_restart_warning)

        self.b_confirm = QPushButton(session.get("msg")["main_messages"]["confirm"])
        self.b_confirm.setAccessibleName("b_main")
        self.b_confirm.clicked.connect(self.confirm)
        self.lay.addWidget(self.b_confirm, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add a flexible space under all the widgets, to push they up
        self.lay.addStretch()

    # When language change
    def language_change(self):
        from modules.files_handle import load_messages

        session.set_dict_value("settings", "language", self.cb_language.currentText().lower())
        load_messages() # Reload messages

        self.l_style.setText(session.get("msg")["settings"]["style"])
        self.l_style_description.setText(session.get("msg")["settings"]["style-description"])
        self.l_language.setText(session.get("msg")["settings"]["language"])
        self.l_db_connection_title.setText(session.get("msg")["settings"]["database-connection-title"])
        self.l_db_connection_description.setText(session.get("msg")["settings"]["database-connection-description"])
        self.l_db_connection_local_warning.setText(session.get("msg")["settings"]["database-connection-local-warning"])
        self.le_db_connection.setPlaceholderText(session.get("msg")["settings"]["database-connection-title"])
        self.l_default_printer_title.setText(session.get("msg")["settings"]["default-printer-title"])
        self.l_default_printer_selection_description.setText(session.get("msg")["settings"]["default-printer-selection-description"])
        self.l_default_printer_paper_width_description.setText(session.get("msg")["settings"]["default-printer-paper-width-description"])
        self.le_default_printer_paper_width.setPlaceholderText(session.get("msg")["settings"]["default-printer-paper-width-placeholder"])
        self.l_confirm_restart_warning.setText(session.get("msg")["settings"]["confirm-restart-warning"])
        self.b_confirm.setText(session.get("msg")["main_messages"]["confirm"])

    # Press confirm button
    def confirm(self):
        # Get fields
        style = self.cb_styles.currentText().lower()
        language = self.cb_language.currentText().lower()
        db_connection = self.le_db_connection.text()
        default_printer = next((k for k, v in self.printers_dict.items() if v == self.cb_printers_list.currentText()), "")
        default_printer_paper_width = self.le_default_printer_paper_width.text()

        # Check
        if db_connection != "":
            # Test database connection
            client = MongoClient(db_connection, ServerSelectionTimeoutMS = 3000)

            try:
                client.admin.command("ping")
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                error_msg = QMessageBox(self)
                error_msg.setWindowTitle(session.get("msg")["errors"]["error"])
                error_msg.setText(session.get("msg")["errors"]["db-connection-failed"])
                return error_msg.exec()

        if default_printer == "":
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle(session.get("msg")["errors"]["error"])
            error_msg.setText(session.get("msg")["errors"]["mandatory-printer-select"])
            return error_msg.exec()

        if default_printer_paper_width == "":
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle(session.get("msg")["errors"]["error"])
            error_msg.setText(session.get("msg")["errors"]["printer-paper-width"])
            return error_msg.exec()

        try:
            numeric_default_printer_paper_width = int(default_printer_paper_width)
        except:
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle(session.get("msg")["errors"]["error"])
            error_msg.setText(session.get("msg")["errors"]["printer-paper-width"])
            return error_msg.exec()

        self.b_confirm.setEnabled(False)

        # Write settings to local database
        write_settings(style, language, db_connection, default_printer, numeric_default_printer_paper_width)

        # Flag application to close programmatically
        app_instance = QApplication.instance()
        if app_instance is not None:
            app_instance.setProperty("is_restarting", True)

        # Close settings window
        from PySide6.QtCore import QProcess
        QProcess.startDetached(sys.executable, sys.argv)
        QApplication.quit()
