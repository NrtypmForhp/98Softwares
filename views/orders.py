# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ---------------- ORDERS VIEW -----------------
# **********************************************

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QLabel, QLineEdit, QPushButton, QDialog, QMessageBox, QHeaderView
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer, Signal
import os

# Base window import
from views.base_window import BaseWindow

# Base dialog import
from views.base_dialog import BaseDialog

# Session import
from modules.session import session

# Database import
from modules.db import load_categories, create_new_category, delete_category

# Components import
from views.components import WrappedLabel, NonScrollingComboBox, InputDialog, ExpandedLineEdit, ExpandedTableWidget

# Constants import
from modules.constants import PICTURES_DIRECTORY

# ** Create or modify product
class CreateModifyProduct(BaseDialog):
    final_product = Signal(dict)

    def __init__(self, category:str, product_data:dict={}, parent=None):
        super().__init__(title=session.get("msg")["orders_view"]["create-modify-product"])

        # Set main layout
        self.lay = self.content_layout

        l_category = WrappedLabel(text=f'{session.get("msg")["orders_view"]["create-modify-product-category"]} {category}')
        l_category.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(l_category)

        self.lay.addSpacing(10)

        l_name_description = WrappedLabel(text=session.get("msg")["orders_view"]["product-name-description"])
        l_name_description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(l_name_description)

        self.le_product_name = ExpandedLineEdit()
        self.le_product_name.setText(product_data.get("product_name", ""))
        self.le_product_name.setPlaceholderText(session.get("msg")["orders_view"]["product-name"])
        self.le_product_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.le_product_name)

        self.lay.addSpacing(10)

        l_product_price = WrappedLabel(text=session.get("msg")["orders_view"]["product-price-description"])
        l_product_price.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(l_product_price)

        self.le_product_price = ExpandedLineEdit()
        if product_data.get("product_price", "") != "":
            product_price = f"{float(product_data['product_price']):.2f}"
        else: product_price = ""
        self.le_product_price.setText(product_price)
        self.le_product_price.setPlaceholderText(session.get("msg")["orders_view"]["product-price"])
        self.le_product_price.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(self.le_product_price)

        self.lay.addSpacing(10)

        l_product_additions = WrappedLabel(text=session.get("msg")["orders_view"]["product-additions"])
        l_product_additions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lay.addWidget(l_product_additions)

        b_new_addition = QPushButton(session.get("msg")["orders_view"]["new-addition"])
        b_new_addition.setAccessibleName("b_main")
        self.lay.addWidget(b_new_addition, alignment=Qt.AlignmentFlag.AlignCenter)

        self.product_additions_table = ExpandedTableWidget(0, 2)
        self.product_additions_table.setHorizontalHeaderLabels([
            session.get("msg")["orders_view"]["addition"],
            session.get("msg")["orders_view"]["product-price"]
        ])
        self.product_additions_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.lay.addWidget(self.product_additions_table)

        self.lay.addStretch() # Push widgets up

# ** Main Window **
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

        b_reprint_receipt = QPushButton(session.get("msg")["orders_view"]["reprint-receipt"])
        b_reprint_receipt.setAccessibleName("b_main")
        f_print_save_receipt_lay.addWidget(b_reprint_receipt)

        f_print_save_receipt_lay.addStretch() # Push widgets to the top

        # Print order and reprint specific order (right third)
        f_print_order = QFrame()
        f_print_order_lay = QVBoxLayout(f_print_order)
        f_print_order_lay.setSpacing(5)
        top_frame_lay.addWidget(f_print_order)

        b_print_order = QPushButton(session.get("msg")["orders_view"]["print-order"])
        b_print_order.setAccessibleName("b_main")
        f_print_order_lay.addWidget(b_print_order)

        b_reprint_order = QPushButton(session.get("msg")["orders_view"]["reprint-order"])
        b_reprint_order.setAccessibleName("b_main")
        f_print_order_lay.addWidget(b_reprint_order)

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
        try:
            categories_list = load_categories()
        except Exception:
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle(session.get("msg")["errors"]["error"])
            error_msg.setText(session.get("msg")["errors"]["db-connection-failed"])
            error_msg.exec()
            QTimer.singleShot(0, self.close)
            return

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

        b_new_product = QPushButton(session.get("msg")["orders_view"]["new-product"])
        b_new_product.setAccessibleName("b_main")
        b_new_product.clicked.connect(self.new_product_button)
        category_lay.addWidget(b_new_product)

        f_products_lay.addLayout(category_lay)

        f_products_lay.addStretch() # Push widgets to the top

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

    def new_category_button(self): # Press on new category button
        dialog = InputDialog(session.get("msg")["orders_view"]["new-category"], session.get("msg")["orders_view"]["new-category-description"], self)
        if dialog.exec() == QDialog.DialogCode.Accepted:

            category = dialog.get_text().strip().upper()
            try:
                response = create_new_category(category)
            except Exception:
                error_msg = QMessageBox(self)
                error_msg.setWindowTitle(session.get("msg")["errors"]["error"])
                error_msg.setText(session.get("msg")["errors"]["db-connection-failed"])
                error_msg.exec()
                return

            if response != "ok": # If category already exists, simply set the combobox text to the existint category
                self.cb_category.setCurrentText(category)
            else:
                self.cb_category.addItem(category)
                self.cb_category.setCurrentText(category)

    def delete_category_button(self): # Press on delete category button
        # Check if a category is selected
        if self.cb_category.currentText() == "":
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle(session.get("msg")["errors"]["warning"])
            error_msg.setText(session.get("msg")["orders_view"]["no-categories-warning"])
            error_msg.exec()
            return

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
            try:
                delete_category(category)
            except Exception:
                error_msg = QMessageBox(self)
                error_msg.setWindowTitle(session.get("msg")["errors"]["error"])
                error_msg.setText(session.get("msg")["errors"]["db-connection-failed"])
                error_msg.exec()
                return
            self.cb_category.removeItem(self.cb_category.currentIndex())

    def new_product_button(self): # Press on new product button
        # Check if a category is selected
        if self.cb_category.currentText() == "":
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle(session.get("msg")["errors"]["warning"])
            error_msg.setText(session.get("msg")["orders_view"]["no-categories-warning"])
            error_msg.exec()
            return

        dialog = CreateModifyProduct(self.cb_category.currentText())
        dialog.exec()
