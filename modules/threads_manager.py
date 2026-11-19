# **********************************************
# ---------------- 98 SOFTWARES ----------------
# ----------- THREADS MANAGER MODULE -----------
# **********************************************

from typing import Any, Callable, Dict, Optional, Protocol, TypeVar, runtime_checkable
from PySide6.QtCore import QThread, Signal

class _SignalLike(Protocol):
    def connect(self, slot: Callable[..., Any]) -> Any: ...

@runtime_checkable
class SupportsTaskSignals(Protocol):
    succeeded: _SignalLike
    failed: _SignalLike

ThreadType = TypeVar("ThreadType", bound=QThread)

class CallableThread(QThread):
    # End signals
    succeeded = Signal(object)
    failed = Signal(Exception)

    def __init__(self, func: Callable[..., Any], *args: Any, parent = None, **kwargs: Any):
        super().__init__(parent)
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            result = self._func(*self._args, **self._kwargs)
            if not self.isInterruptionRequested(): # Success
                self.succeeded.emit(result)
        except Exception as e:
            if not self.isInterruptionRequested(): # Fail
                self.failed.emit(e)

class ThreadsManager:
    def __init__(self):
        # Register functions or subclasses of threads associated at a name
        self._threads_registry: Dict[str, Callable[..., QThread]] = {}
        # Track instances actually active by name
        self._active_threads: Dict[str, QThread] = {}

    def register_thread(self, name: str, factory: Callable[..., QThread]):
        # Register a function or a class that return a QThread
        self._threads_registry[name] = factory

    def start_thread(self,
        name: str,
        *args,
        on_success: Optional[Callable[[Any], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        on_finished: Optional[Callable[[], None]] = None,
        replace_if_running: bool = False,
        **kwargs
    ) -> QThread:
        # Create and start the thread registered with 'name'
        if name not in self._threads_registry:
            raise ValueError(f"Thread '{name}' not registered on Threads Manager.")

        existing = self._active_threads.get(name)
        if existing is not None and existing.isRunning():
            if replace_if_running:
                self.stop_thread(name)
            else:
                return existing

        factory = self._threads_registry[name]
        thread = factory(*args, **kwargs)
        self._active_threads[name] = thread

        # Connect eventual optional callback if thread expose signals
        if isinstance(thread, SupportsTaskSignals):
            if on_success is not None and hasattr(thread, "succeeded"):
                thread.succeeded.connect(on_success)
            if on_error is not None and hasattr(thread, "failed"):
                thread.failed.connect(on_error)
        if on_finished is not None:
            thread.finished.connect(on_finished)

        # Automatic dictionary cleaning
        thread.finished.connect(lambda t_name=name, t_obj=thread: self._cleanup_thread(t_name, t_obj))
        thread.finished.connect(thread.deleteLater)

        thread.start()
        return thread

    def stop_thread(self, name: str, timeout_ms: int = 3000, force: bool = False):
        # Request thread interrupt and wait for closing
        thread = self._active_threads.get(name)
        if thread is None:
            return

        if thread.isRunning():
            thread.requestInterruption()
            thread.quit()
            if not thread.wait(timeout_ms) and force:
                thread.terminate()
                thread.wait(1000)

        self._cleanup_thread(name, thread)

    def stop_all_threads(self, timeout_ms: int = 3000, force: bool = False):
        # Stop all active threads
        for name in list(self._active_threads.keys()):
            self.stop_thread(name, timeout_ms=timeout_ms, force=force)

    def is_running(self, name: str) -> bool:
        thread = self._active_threads.get(name)
        return thread is not None and thread.isRunning()

    def _cleanup_thread(self, name: str, thread: QThread):
        # Remove only if correspond to actually registered instance (avoid race condition at restart)
        if self._active_threads.get(name) is thread:
            del self._active_threads[name]

threads_manager = ThreadsManager()
