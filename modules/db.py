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

# ** Database functions **

# Function to update server hosted database
def update_server_hosted_database() -> None:
    global server_hosted_client
    global server_hosted_db
    global settings
    global db_connection

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

# Apply projection for local database
def _apply_projection(docs: list[dict], projection: dict) -> list[dict]:
    if not projection:
        return docs

    include_fields = {k for k, v in projection.items() if v}
    exclude_fields = {k for k, v in projection.items() if not v}

    result = []
    for doc in docs:
        if include_fields:
            filtered = {k: v for k, v in doc.items() if k in include_fields or (k == "_id" and projection.get("_id") != 0)}
        else:
            filtered = {k: v for k, v in doc.items() if k not in exclude_fields}
        result.append(filtered)
    return result

# Find one from database
def find_one(collection:str, filter:dict | None = None, projection:dict | None = None):
    query_filter = filter if filter is not None else {}
    query_projection = projection if projection is not None else {}

    # If it's a local database
    if not db_connection:
        col = local_db[collection]
        doc = col.find_one(query_filter)
        if doc is not None and query_projection:
            return _apply_projection([doc], query_projection)[0]
        return doc
    # If it's a server hosted database
    if server_hosted_db is not None:
        col = server_hosted_db[collection]
        if query_projection:
            return col.find_one(query_filter, projection=query_projection)
        return col.find_one(query_filter)

    return None

# Find all from database
def find_all(collection:str, filter:dict | None = None, projection:dict | None = None):
    query_filter = filter if filter is not None else {}
    query_projection = projection if projection is not None else {}

    # If it's a local database
    if not db_connection:
        col = local_db[collection]
        cursor = col.find(query_filter)
        if query_projection:
            return _apply_projection(list(cursor), query_projection)
        return cursor
    # If it's a server hosted database
    if server_hosted_db is not None:
        col = server_hosted_db[collection]
        if query_projection:
            return col.find(query_filter, projection=query_projection)
        return col.find(query_filter)

    return []

# Insert one into database
def insert_one(collection:str, p_query:dict | None = None):
    query = p_query if p_query is not None else {}
    # If it's a local database
    if not db_connection:
        col = local_db[collection]
    # If it's a server hosted database
    elif server_hosted_db is not None:
        col = server_hosted_db[collection]
    else:
        return None

    col.insert_one(query)

# Delete one from database
def delete_one(collection:str, p_query:dict | None = None):
    query = p_query if p_query is not None else {}

    # If it's a local database
    if not db_connection:
        col = local_db[collection]
    # If it's a server hosted database
    elif server_hosted_db is not None:
        col = server_hosted_db[collection]
    else:
        return None

    col.delete_one(query)

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

    # Update server hosted database connections strings
    update_server_hosted_database()

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

# Load categories
def load_categories() -> list:
    categories = find_all("orders_categories", {}, {"category": 1})
    if categories is None: return []

    categories_list = []
    for category in categories:
        categories_list.append(category["category"])
    return categories_list

# Create new category
def create_new_category(category:str) -> str:
    # Check if category already exists
    if find_one("orders_categories", {"category": category}) != None:
        return "category_already_exists"

    insert_one("orders_categories", {"category": category})
    return "ok"

# Delete category
def delete_category(category:str) -> str:
    delete_one("orders_categories", {"category": category})
    return "ok"
