# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ---------- WINDOWS MANAGER MODULE ------------
# **********************************************

from typing import Callable, Dict, List, Optional
from PySide6.QtWidgets import QWidget

class WindowsManager:
    def __init__(self):
        self._windows_registry: Dict[str, Callable[..., QWidget]] = {}
        self._active_windows: Dict[str, QWidget] = {}

    # Register window class on registry
    def register_window(self, name:str, window_class: Callable[..., QWidget]):
        self._windows_registry[name] = window_class

    # Create, show and memorize a new window on PySide6
    def open_window(self, name:str, *args, **kwargs) -> QWidget:
        if name not in self._windows_registry:
            raise ValueError(f"Window '{name}' not registered on Windows Manager.")

        # If window exists show it

        active_window: Optional[QWidget] = self._active_windows.get(name)
        if active_window is not None and active_window:
            # If it's minimized restore it
            if active_window.isMinimized():
                active_window.showNormal()

            active_window.raise_()
            active_window.activateWindow()
            return active_window

        # If window not exists create it

        window_factory = self._windows_registry[name]
        window = window_factory(*args, **kwargs)
        self._active_windows[name] = window

        # When window will be destroied delete it from memory
        window.destroyed.connect(lambda: self._cleanup_window(name))

        window.show()

        return window

    # Remove window from memory when it's destroyed
    def _cleanup_window(self, name:str):
        if name in self._active_windows:
            del self._active_windows[name]

    # Close all windows except the main window
    def close_all_windows(self):
        for name, window in list(self._active_windows.items()):
            if name != "main_window":
                window.close()

windows_manager = WindowsManager()
