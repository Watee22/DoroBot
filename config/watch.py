from __future__ import annotations
import os
import threading
import time
from typing import Callable, List

Callback = Callable[[], None]

class ConfigWatcher:
    def __init__(self, path: str, interval: float = 1.0):
        self.path = path
        self.interval = interval
        self._callbacks: List[Callback] = []
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._last_mtime = None

    def subscribe(self, cb: Callback) -> None:
        self._callbacks.append(cb)

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._last_mtime = os.path.getmtime(self.path) if os.path.exists(self.path) else None
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                if os.path.exists(self.path):
                    mtime = os.path.getmtime(self.path)
                    if self._last_mtime is None:
                        self._last_mtime = mtime
                    elif mtime != self._last_mtime:
                        self._last_mtime = mtime
                        for cb in list(self._callbacks):
                            try:
                                cb()
                            except Exception:
                                pass
            except Exception:
                pass
            time.sleep(self.interval)