# **********************************************
# ---------------- 98 SOFTWARES ----------------
# --------------- DATABASE MODULE --------------
# **********************************************

# ** Local databases **
from mongita import MongitaClientDisk
import os

# Session import
from modules.session import session

# Constants import
from modules.constants import DATABASE_DIRECTORY

local_database_file_path = os.path.join(DATABASE_DIRECTORY, "98softwares_db")
local_client = MongitaClientDisk(host=local_database_file_path)
local_db = local_client["98softwares"]

# Function to load settings (use only local database for settings)
def load_settings() -> None:
    settings_dict = {
        "language": "english",
        "style": "dark"
    }

    try:
        settings_collection = local_db["settings"]
        settings = settings_collection.find_one()

        if settings is not None:
            settings.pop("_id", None)
            settings_dict.update(settings)

    except Exception as e:
        print(f"Error on settings load: {e}")

    session.set("settings", settings_dict)

# Write settings (use only local database for settings)
def write_settings(style:str, language:str, db_connection:str, default_printer:str, default_printer_paper_width:int, default_printer_autocut:bool,
                    default_orders_printer:str, default_orders_printer_paper_width:int, default_orders_printer_autocut:bool) -> None:
    settings_collection = local_db["settings"]



    query = {
        "style": style,
        "language": language,
        "db_connection": db_connection,
        "default_printer": default_printer,
        "default_printer_paper_width": default_printer_paper_width,
        "default_printer_autocut": "yes" if default_printer_autocut == True else "no",
        "default_orders_printer": default_orders_printer,
        "default_orders_printer_paper_width": default_orders_printer_paper_width,
        "default_orders_printer_autocut": "yes" if default_orders_printer_autocut == True else "no",
    }

    settings_collection.replace_one({}, query, upsert=True)
