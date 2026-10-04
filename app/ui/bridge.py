from __future__ import annotations

import json
from PySide6.QtCore import QObject, Signal, Slot


class ChartBridge(QObject):
    marketUpdated = Signal(str)

    @Slot(str)
    def receive(self, message: str) -> None:
        pass

    def publish(self, snapshot: dict, signal: dict) -> None:
        self.marketUpdated.emit(json.dumps({"snapshot": snapshot, "signal": signal}))
