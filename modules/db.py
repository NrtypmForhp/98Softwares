# **********************************************
# ---------------- 98 SOFTWARES ----------------
# --------------- DATABASE MODULE --------------
# **********************************************

# ** Local databases **
from mongita import MongitaClientDisk
import os

# ** Server hosted databases **
from pymongo import MongoClient

# Session import
from modules.session import session

# Constants import
from modules.constants import DATABASE_DIRECTORY

local_database_file_path = os.path.join(DATABASE_DIRECTORY, "98softwares_db")
local_client = MongitaClientDisk(host=local_database_file_path)
local_db = local_client["98softwares"]

settings = session.get("settings") or {}
db_connection = (settings.get("db_connection") or "").strip()

server_hosted_client = (
    MongoClient(db_connection, serverSelectionTimeoutMS=3000)
    if db_connection
    else None
)
server_hosted_db = (
    server_hosted_client["98softwares"]
    if server_hosted_client is not None
    else None
)

# Find one from database
def find_one(collection:str, filter:dict = {}, projection:dict = {}):
    # If it's a local database
    if session.get("settings")["db_connection"] == "":
        col = local_db[collection]
    # If it's a server hosted database
    else:
        col = server_hosted_db[collection]

    return col.find_one(filter, projection)

# Insert one into database
def insert_one(collection:str, query:dict):
    # If it's a local database
    if session.get("settings")["db_connection"] == "":
        col = local_db[collection]
    # If it's a server hosted database
    else:
        col = server_hosted_db[collection]

    col.insert_one(query)

# Function to ping mongodb (only for server hosted database)
def ping_mongo(db_connections_string: str, timeout_ms: int = 3000) -> bool:
    client = MongoClient(db_connections_string, serverSelectionTimeoutMS=timeout_ms)
    try:
        client.admin.command("ping")
        return True
    finally:
        client.close()

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
def write_settings(style:str, language:str, header:str, db_connection:str, default_printer:str, default_printer_paper_width:int, default_printer_autocut:bool,
                    default_orders_printer:str, default_orders_printer_paper_width:int, default_orders_printer_autocut:bool) -> None:
    settings_collection = local_db["settings"]



    query = {
        "style": style,
        "language": language,
        "header": header,
        "db_connection": db_connection,
        "default_printer": default_printer,
        "default_printer_paper_width": default_printer_paper_width,
        "default_printer_autocut": "yes" if default_printer_autocut == True else "no",
        "default_orders_printer": default_orders_printer,
        "default_orders_printer_paper_width": default_orders_printer_paper_width,
        "default_orders_printer_autocut": "yes" if default_orders_printer_autocut == True else "no",
    }

    settings_collection.replace_one({}, query, upsert=True)

# ** Orders **

# Create new category
def create_new_category(category:str) -> str:
    # Check if category already exists
    if find_one("orders", {"category": category}) != None:
        return "category_already_exists"

    insert_one("orders", {"category": category})
    return "ok"
