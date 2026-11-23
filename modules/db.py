# **********************************************
# ---------------- 98 SOFTWARES ----------------
# --------------- DATABASE MODULE --------------
# **********************************************

from PySide6.QtWidgets import QMessageBox

# ** Local databases **
from mongita import MongitaClientDisk
import os

# ** Server hosted databases **
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Session import
from modules.session import session

# Constants import
from modules.constants import DATABASE_DIRECTORY

# ** Database functions **

class RemoteDatabaseError(Exception):
    """Error during operation on remote database."""

# Global database variables
_local_client: MongitaClientDisk | None = None
_local_db = None

_cached_remote_uri: str | None = None
_remote_client: MongoClient | None = None
_remote_db = None

# Function to get cached local db
def _get_local_db():
    global _local_client, _local_db

    if _local_client is None:
        local_database_file_path = os.path.join(DATABASE_DIRECTORY, "98softwares_db")
        _local_client = MongitaClientDisk(host=local_database_file_path)
        _local_db = _local_client["98softwares"]

    return _local_db

# Function to close remote client
def _close_remote_client() -> None:
    global _cached_remote_uri, _remote_client, _remote_db

    if _remote_client is not None:
        _remote_client.close()

    _cached_remote_uri = None
    _remote_client = None
    _remote_db = None

# Function to get the correct database (local or server hosted), return True if is local, False if is server hosted
def _get_current_db(force_local:bool = False, check_remote: bool = True):
    local_db = _get_local_db()

    if force_local:
        return local_db, True

    settings = session.get("settings") or {}
    db_connection = (settings.get("db_connection") or "").strip()

    if not db_connection:
        _close_remote_client()
        return local_db, True

    # If URI is changed or not exists
    if db_connection != _cached_remote_uri or _remote_client is None:
        _close_remote_client()
        client = MongoClient(db_connection, serverSelectionTimeoutMS=3000)
        try:
            if check_remote:
                client.admin.command("ping")
        except PyMongoError as exc:
            client.close()
            raise RemoteDatabaseError(
                f"Impossible to reach remote database: {exc}"
            ) from exc

        globals()["_remote_client"] = client
        globals()["_cached_remote_uri"] = db_connection
        globals()["_remote_db"] = client["98softwares"]

    return _remote_db, False

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

    db, is_local = _get_current_db()

    if db is None:
        raise RemoteDatabaseError("Connection to remote database failed!")

    try:
        # If it's a local database
        if is_local:
            col = db[collection]
            doc = col.find_one(query_filter)
            if doc is not None and query_projection:
                return _apply_projection([doc], query_projection)[0]
            return doc
        # If it's a server hosted database
        else:
            col = db[collection]
            if query_projection:
                return col.find_one(query_filter, query_projection)
            return col.find_one(query_filter)
    except PyMongoError as exc:
        if not is_local:
            raise RemoteDatabaseError(
                f"Impossible to connect to remote database: {exc}"
            ) from exc
        raise

# Find all from database
def find_all(collection:str, filter:dict | None = None, projection:dict | None = None):
    query_filter = filter if filter is not None else {}
    query_projection = projection if projection is not None else {}

    db, is_local = _get_current_db()

    if db is None:
        raise RemoteDatabaseError("Connection to remote database failed!")

    try:
        # If it's a local database
        if is_local:
            col = db[collection]
            cursor = col.find(query_filter)
            if query_projection:
                return _apply_projection(list(cursor), query_projection)
            return cursor
        # If it's a server hosted database
        else:
            col = db[collection]
            if query_projection:
                return col.find(query_filter, query_projection)
            return col.find(query_filter)
    except PyMongoError as exc:
        if not is_local:
            raise RemoteDatabaseError(
                f"Impossible to connect to remote database: {exc}"
            ) from exc
        raise

# Insert one into database
def insert_one(collection:str, p_query:dict | None = None):
    query = p_query if p_query is not None else {}

    db, is_local = _get_current_db()

    if db is None:
        raise RemoteDatabaseError("Connection to remote database failed!")

    try:
        col = db[collection]

        col.insert_one(query)
    except PyMongoError as exc:
        if not is_local:
            raise RemoteDatabaseError(
                f"Impossible to connect to remote database: {exc}"
            ) from exc
        raise

# Delete one from database
def delete_one(collection:str, p_query:dict | None = None):
    query = p_query if p_query is not None else {}

    db, is_local = _get_current_db()

    if db is None:
        raise RemoteDatabaseError("Connection to remote database failed!")

    try:
        col = db[collection]

        col.delete_one(query)
    except PyMongoError as exc:
        if not is_local:
            raise RemoteDatabaseError(
                f"Impossible to connect to remote database: {exc}"
            ) from exc
        raise

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
        db, is_local = _get_current_db(True)
        if db is None:
            raise RemoteDatabaseError("Connection to remote database failed!")

        settings_collection = db["settings"]
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

    db, is_local = _get_current_db(True)

    if db is None:
        raise RemoteDatabaseError("Connection to remote database failed!")

    settings_collection = db["settings"]

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
def load_categories() -> list[str]:
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
