# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ---------------- ORDERS VIEW -----------------
# **********************************************

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

# Base window import
from views.base_window import BaseWindow

# Session import
from modules.session import session

# Modules import
from modules.main import get_printers_dict

# Components import
from views.components import WrappedLabel, NonScrollingComboBox

# Constants import
from modules.constants import PICTURES_DIRECTORY

class OrdersWindow(BaseWindow):
    def __init__(self):
        super().__init__(title=session.get("msg")["orders_view"]["title"])

        # Set main layout
        self.lay = self.content_layout

        # ** Main frames with specific layout **
        top_frame = QFrame()
        top_frame_lay = QHBoxLayout(top_frame)
        self.lay.addWidget(top_frame, stretch=2) # Stretch to 20% of space

        bottom_frame = QFrame()
        bottom_frame_lay = QHBoxLayout(bottom_frame)
        self.lay.addWidget(bottom_frame, stretch=8) # Stretch to 80% of space

        # ** Top Frame **

        # Logo (left side)
        l_logo = QLabel()
        picture_pixmap = QPixmap(os.path.join(PICTURES_DIRECTORY, "logo.png"))
        l_logo.setPixmap(picture_pixmap)
        l_logo.resize(picture_pixmap.width(), picture_pixmap.height())
        top_frame_lay.addWidget(l_logo)

        top_frame_lay.addStretch(1) # Absorbs the space to the right of the logo

        # Customer details (center)
        f_customer_details = QFrame()
        f_customer_details_lay = QGridLayout(f_customer_details)
        top_frame_lay.addWidget(f_customer_details)

        top_frame_lay.addStretch(1) # Absorbs the space between customer and printers

        self.le_customer_name = QLineEdit()
        self.le_customer_name.setPlaceholderText(session.get("msg")["orders_view"]["customer-name"])
        f_customer_details_lay.addWidget(self.le_customer_name, 0, 0, Qt.AlignmentFlag.AlignCenter)

        # Customer table

        l_customer_table = WrappedLabel(text=session.get("msg")["orders_view"]["customer-table-number"])
        f_customer_details_lay.addWidget(l_customer_table, 1, 0, Qt.AlignmentFlag.AlignCenter)

        table_controls_lay = QHBoxLayout()
        table_controls_lay.setSpacing(5)
        table_controls_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.b_customer_table_minus = QPushButton("-")
        self.b_customer_table_minus.setAccessibleName("b_operation_button_minus")
        self.b_customer_table_minus.clicked.connect(self.table_button_minus)
        table_controls_lay.addWidget(self.b_customer_table_minus)

        self.le_customer_table = QLineEdit()
        self.le_customer_table.setAccessibleName("le_operation")
        self.le_customer_table.setText("-1")
        table_controls_lay.addWidget(self.le_customer_table)

        self.b_customer_table_plus = QPushButton("+")
        self.b_customer_table_plus.setAccessibleName("b_operation_button_plus")
        self.b_customer_table_plus.clicked.connect(self.table_button_plus)
        table_controls_lay.addWidget(self.b_customer_table_plus)

        f_customer_details_lay.addLayout(table_controls_lay, 2, 0, Qt.AlignmentFlag.AlignCenter)

        # Print and save receipt (right first)
        f_print_save_receipt = QFrame()
        f_print_save_receipt_lay = QVBoxLayout(f_print_save_receipt)
        f_print_save_receipt_lay.setSpacing(5)
        top_frame_lay.addWidget(f_print_save_receipt)

        b_print_receipt = QPushButton(session.get("msg")["orders_view"]["print-receipt"])
        b_print_receipt.setAccessibleName("b_main")
        f_print_save_receipt_lay.addWidget(b_print_receipt)

        b_save_receipt = QPushButton(session.get("msg")["orders_view"]["save-receipt"])
        b_save_receipt.setAccessibleName("b_main")
        f_print_save_receipt_lay.addWidget(b_save_receipt)

        f_print_save_receipt_lay.addStretch() # Push widgets to the top

        # Print order and reprint specific receipt (right second)
        f_print_order = QFrame()
        f_print_order_lay = QVBoxLayout(f_print_order)
        f_print_order_lay.setSpacing(5)
        top_frame_lay.addWidget(f_print_order)

        b_print_order = QPushButton(session.get("msg")["orders_view"]["print-order"])
        b_print_order.setAccessibleName("b_main")
        f_print_order_lay.addWidget(b_print_order)

        l_reprint_specific_receipt = WrappedLabel(text=session.get("msg")["orders_view"]["reprint-specific-receipt"])
        l_reprint_specific_receipt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_print_order_lay.addWidget(l_reprint_specific_receipt)

        receipt_number_lay = QHBoxLayout()
        receipt_number_lay.setSpacing(5)
        receipt_number_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.b_receipt_number_minus = QPushButton("-")
        self.b_receipt_number_minus.setAccessibleName("b_operation_button_minus")
        self.b_receipt_number_minus.clicked.connect(self.receipt_number_minus)
        receipt_number_lay.addWidget(self.b_receipt_number_minus)

        self.le_receipt_number = QLineEdit()
        self.le_receipt_number.setAccessibleName("le_operation")
        self.le_receipt_number.setText("1")
        receipt_number_lay.addWidget(self.le_receipt_number)

        self.b_receipt_number_plus = QPushButton("+")
        self.b_receipt_number_plus.setAccessibleName("b_operation_button_plus")
        self.b_receipt_number_plus.clicked.connect(self.receipt_number_plus)
        receipt_number_lay.addWidget(self.b_receipt_number_plus)

        f_print_order_lay.addLayout(receipt_number_lay)

        b_reprint_receipt = QPushButton(session.get("msg")["orders_view"]["reprint"])
        b_reprint_receipt.setAccessibleName("b_main")
        f_print_order_lay.addWidget(b_reprint_receipt)

        f_print_order_lay.addStretch() # Push widgets to the top

    def table_button_minus(self): # Reduce the table number by 1
        table_number = self.le_customer_table.text()

        # Check if table number is a number, if not set it to -1
        try:
            int_table_number = int(table_number)
        except ValueError: return self.le_customer_table.setText("-1")

        if int_table_number < -1: return self.le_customer_table.setText("-1")
        if int_table_number > 999: return self.le_customer_table.setText("999")

        if int_table_number > -1: int_table_number -= 1

        self.le_customer_table.setText(str(int_table_number))

    def table_button_plus(self): # Add 1 to the table number
        table_number = self.le_customer_table.text()

        # Check if table number is a number, if not set it to -1
        try:
            int_table_number = int(table_number)
        except ValueError: return self.le_customer_table.setText("-1")

        if int_table_number < -1: return self.le_customer_table.setText("-1")
        if int_table_number > 999: return self.le_customer_table.setText("999")

        if int_table_number < 999: int_table_number += 1

        self.le_customer_table.setText(str(int_table_number))

    def receipt_number_plus(self): # Add 1 to the receipt number
        receipt_number = self.le_receipt_number.text()

        # Check if receipt number is a number, if not set it to 1
        try:
            int_receipt_number = int(receipt_number)
        except ValueError: return self.le_receipt_number.setText("1")

        if int_receipt_number < 1: return self.le_receipt_number.setText("1")
        if int_receipt_number > 999: return self.le_receipt_number.setText("999")

        if int_receipt_number < 999: int_receipt_number += 1

        self.le_receipt_number.setText(str(int_receipt_number))

    def receipt_number_minus(self): # Reduce the receipt number by 1
        receipt_number = self.le_receipt_number.text()

        # Check if receipt number is a number, if not set it to 1
        try:
            int_receipt_number = int(receipt_number)
        except ValueError: return self.le_receipt_number.setText("1")

        if int_receipt_number < 1: return self.le_receipt_number.setText("1")
        if int_receipt_number > 999: return self.le_receipt_number.setText("999")

        if int_receipt_number > 1: int_receipt_number -= 1

        self.le_receipt_number.setText(str(int_receipt_number))
