# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ----------------- MAIN VIEW ------------------
# **********************************************

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QMessageBox, QApplication, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QCloseEvent
import os

# Base window import
from views.base_window import BaseWindow

# Windows Manager import
from modules.windows_manager import windows_manager

# Session import
from modules.session import session

# Components import
from views.components import ExpandedFrame, WrappedLabel, ProportionalImageLabel

# Constants import
from modules.constants import PICTURES_DIRECTORY

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__(title=session.get("msg")["main_view"]["title"])

        # Set main layout
        self.lay = self.content_layout

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
        b_settings.setAccessibleName("b_main")
        b_settings.clicked.connect(self.settings_button)
        top_frame_lay.addWidget(b_settings)

        # ** Bottom Frame **

        # Orders
        f_orders = ExpandedFrame()
        f_orders.setAccessibleName("main_view_frame")
        f_orders.setCursor(Qt.CursorShape.PointingHandCursor)
        f_orders_lay = QHBoxLayout(f_orders)
        bottom_frame_lay.addWidget(f_orders)

        # Orders frame
        picture_pixmap = QPixmap(os.path.join(PICTURES_DIRECTORY, "orders_main.png"))
        l_orders_main_logo = ProportionalImageLabel(picture_pixmap)
        f_orders_lay.addWidget(l_orders_main_logo)

        f_orders_lay.addSpacing(20)

        # Orders description
        f_orders_description = ExpandedFrame()
        f_orders_description_lay = QVBoxLayout(f_orders_description)
        f_orders_lay.addWidget(f_orders_description)

        l_orders_description_title = WrappedLabel(text=session.get("msg")["main_view"]["orders-description-title"])
        l_orders_description_title.setAccessibleName("l_title")
        l_orders_description_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_orders_description_lay.addWidget(l_orders_description_title)

        f_orders_description_lay.addSpacing(5)

        l_orders_description = WrappedLabel(text=session.get("msg")["main_view"]["orders-description"])
        l_orders_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_orders_description_lay.addWidget(l_orders_description)

        l_orders_description_tooltip_1 = WrappedLabel(text=session.get("msg")["main_view"]["orders-description-tooltip-1"])
        l_orders_description_tooltip_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_orders_description_lay.addWidget(l_orders_description_tooltip_1)

        f_orders_description_lay.addStretch() # Keep all widgets up

        f_orders_lay.addStretch() # Keep all widgets left

        bottom_frame_lay.addStretch() # Keep all widgets up

    # Settings button
    def settings_button(self):
        windows_manager.open_window("settings_window")

    # Close event
    def closeEvent(self, event: QCloseEvent) -> None:
        # If application is closing programmatically (example on save settings)
        app_instance = QApplication.instance()
        if app_instance is not None:
            if app_instance.property("is_restarting"):
                windows_manager.close_all_windows()
                event.accept()
                return

        # Set a confirm message before application close
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(session.get("msg")["main_view"]["confirm-exit"])
        msg_box.setText(session.get("msg")["main_view"]["confirm-exit-text"])

        btn_yes = msg_box.addButton(session.get("msg")["main_messages"]["confirm"], QMessageBox.ButtonRole.YesRole)
        btn_no = msg_box.addButton(session.get("msg")["main_messages"]["cancel"], QMessageBox.ButtonRole.NoRole)

        msg_box.setDefaultButton(btn_no) # Default button if you press Enter

        msg_box.exec()

        if msg_box.clickedButton() == btn_yes:
            windows_manager.close_all_windows()
            event.accept()
        else:
            event.ignore()
