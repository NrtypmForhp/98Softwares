# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ---------------- ORDERS VIEW -----------------
# **********************************************

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QLabel, QLineEdit, QPushButton, QDialog, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

# Base window import
from views.base_window import BaseWindow

# Session import
from modules.session import session

# Database import
from modules.db import load_categories, create_new_category, delete_category

# Components import
from views.components import WrappedLabel, NonScrollingComboBox, InputDialog

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

        b_customer_table_minus = QPushButton("-")
        b_customer_table_minus.setAccessibleName("b_operation_button_minus")
        b_customer_table_minus.clicked.connect(self.table_button_minus)
        table_controls_lay.addWidget(b_customer_table_minus)

        self.le_customer_table = QLineEdit()
        self.le_customer_table.setAccessibleName("le_operation")
        self.le_customer_table.setText("-1")
        table_controls_lay.addWidget(self.le_customer_table)

        b_customer_table_plus = QPushButton("+")
        b_customer_table_plus.setAccessibleName("b_operation_button_plus")
        b_customer_table_plus.clicked.connect(self.table_button_plus)
        table_controls_lay.addWidget(b_customer_table_plus)

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

        b_receipt_number_minus = QPushButton("-")
        b_receipt_number_minus.setAccessibleName("b_operation_button_minus")
        b_receipt_number_minus.clicked.connect(self.receipt_number_minus)
        receipt_number_lay.addWidget(b_receipt_number_minus)

        self.le_receipt_number = QLineEdit()
        self.le_receipt_number.setAccessibleName("le_operation")
        self.le_receipt_number.setText("1")
        receipt_number_lay.addWidget(self.le_receipt_number)

        b_receipt_number_plus = QPushButton("+")
        b_receipt_number_plus.setAccessibleName("b_operation_button_plus")
        b_receipt_number_plus.clicked.connect(self.receipt_number_plus)
        receipt_number_lay.addWidget(b_receipt_number_plus)

        f_print_order_lay.addLayout(receipt_number_lay)

        b_reprint_receipt = QPushButton(session.get("msg")["orders_view"]["reprint"])
        b_reprint_receipt.setAccessibleName("b_main")
        f_print_order_lay.addWidget(b_reprint_receipt)

        f_print_order_lay.addStretch() # Push widgets to the top

        # ** Bottom Frame **

        # Products (left side)
        f_products = QFrame()
        f_products_lay = QVBoxLayout(f_products)
        bottom_frame_lay.addWidget(f_products)

        bottom_frame_lay.addStretch(1) # Absorbs the space to the rights of products frame

        # Category
        category_lay = QHBoxLayout()
        category_lay.setSpacing(5)
        category_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cb_category = NonScrollingComboBox()
        categories_list = load_categories()
        self.cb_category.addItems(categories_list)
        category_lay.addWidget(self.cb_category)

        b_new_category = QPushButton(session.get("msg")["orders_view"]["new-category"])
        b_new_category.setAccessibleName("b_main")
        b_new_category.clicked.connect(self.new_category_button)
        category_lay.addWidget(b_new_category)

        b_delete_category = QPushButton(session.get("msg")["orders_view"]["delete-category"])
        b_delete_category.setAccessibleName("b_red")
        b_delete_category.clicked.connect(self.delete_category_button)
        category_lay.addWidget(b_delete_category)

        f_products_lay.addLayout(category_lay)

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

    def new_category_button(self): # Press on new category button
        dialog = InputDialog(session.get("msg")["orders_view"]["new-category"], session.get("msg")["orders_view"]["new-category-description"], self)
        if dialog.exec() == QDialog.DialogCode.Accepted:

            category = dialog.get_text().strip().upper()
            response = create_new_category(category)

            if response != "ok": # If category already exists, simply set the combobox text to the existint category
                self.cb_category.setCurrentText(category)
            else:
                self.cb_category.addItem(category)
                self.cb_category.setCurrentText(category)

    def delete_category_button(self): # Press on delete category button
        # Set a confirm message
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(session.get("msg")["orders_view"]["delete-category"])
        msg_box.setText(session.get("msg")["orders_view"]["confirm-delete-category-description"])

        btn_yes = msg_box.addButton(session.get("msg")["main_messages"]["confirm"], QMessageBox.ButtonRole.YesRole)
        btn_no = msg_box.addButton(session.get("msg")["main_messages"]["cancel"], QMessageBox.ButtonRole.NoRole)

        msg_box.setDefaultButton(btn_no) # Default button if you press Enter

        msg_box.exec()

        if msg_box.clickedButton() == btn_yes:
            category = self.cb_category.currentText()
            delete_category(category)
            self.cb_category.removeItem(self.cb_category.currentIndex())
