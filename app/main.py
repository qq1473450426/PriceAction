from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow
from app.services.runtime import RuntimeController


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    runtime = RuntimeController(window)
    window.bind_runtime(runtime)
    window.show()
    runtime.start()
    exit_code = app.exec()
    runtime.stop()
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
