# **********************************************
# ---------------- 98 SOFTWARES ----------------
# --------------- SESSION MODULE ---------------
# **********************************************

from typing import Any

class AppSession:
    _instance = None
    _data: dict

    # Singleton pattern for use it in whole app
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppSession, cls).__new__(cls)
            cls._instance._data = {}
        return cls._instance

    def set(self, key:str, value:Any) -> None:
        self._data[key] = value

    def set_dict_value(self, key:str, dict_key:str, value:str) -> None:
        if key in self._data and isinstance(self._data[key], dict):
            self._data[key][dict_key] = value

    def get(self, key:str, default: Any = None) -> Any:
        return self._data.get(key, default)

session = AppSession()
