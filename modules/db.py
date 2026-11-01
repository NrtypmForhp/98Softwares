# **********************************************
# ---------------- 98 SOFTWARES ----------------
# --------------- DATABASE MODULE --------------
# **********************************************

# ** Local databases **
from mongita import MongitaClientDisk
import os

# Constants import
from modules.constants import DATABASE_DIRECTORY

local_database_file_path = os.path.join(DATABASE_DIRECTORY, "98softwares_db")
local_client = MongitaClientDisk(host=local_database_file_path)
local_db = local_client["98softwares"]

# Function to load settings (use only local database for settings)
def load_settings() -> dict:
    settings_dict = {
        "language": "english"
    }
    settings_collection = local_db["settings"]

    # Get collections list
    existing_collections = local_db.list_collection_names()

    # If settings collections not exists return only a basic language dict (with english as default)
    if "settings" not in existing_collections: return settings_dict

    # If exists load all settings
    settings = settings_collection.find_one({}, {"_id": 0})
    if settings == None: return settings_dict

    settings_dict["language"] = settings["language"]

    return settings_dict
