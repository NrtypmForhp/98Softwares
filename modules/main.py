# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ---------------- MAIN MODULE -----------------
# **********************************************

import os
from PySide6.QtWidgets import QWidget

# Constants import
from modules.constants import STYLES_DIRECTORY

# Function to import style
def import_style(filename:str) -> str:
    # Add .txt if is not present in filename add it to filename string
    if ".txt" not in filename: filename = f"{filename}.txt"

    file_path = os.path.join(STYLES_DIRECTORY, filename)

    # Check if file exists, if not return an empty string
    if not os.path.exists(file_path): return ""

    # Load style
    with open(file_path, "r") as f:
        file_content = f.read().strip()

    return file_content

# Base window class (common settings for all windows)
class BaseWindow(QWidget):
    def __init__(self, title="98Softwares"):
        super().__init__()

        self.setWindowTitle(title)
        self.showMaximized()
        try:
          self.setStyleSheet(import_style("dark"))
        except Exception as e:
          print(f"Impossible to load style: {e}")
