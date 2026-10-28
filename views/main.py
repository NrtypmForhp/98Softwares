# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ----------------- MAIN VIEW ------------------
# **********************************************

# Modules import
import modules.main as mm

# Constants import
from modules.constants import MSG

class MainWindow(mm.BaseWindow):
    def __init__(self):
        super().__init__(title=MSG["main_view"]["title"])
