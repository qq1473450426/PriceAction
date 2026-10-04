from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QMainWindow, QPlainTextEdit, QPushButton, QSplitter, QVBoxLayout, QWidget

from app.ui.bridge import ChartBridge


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PriceAction · AI Liquidity Trading Terminal")
        self.resize(1500, 920)
        self.bridge = ChartBridge()
        self._build()

    def _build(self) -> None:
        root = QWidget()
        root.setStyleSheet("""
        QWidget { background:#0f1115; color:#e7eaf0; font-size:13px; }
        QFrame#panel { background:#161a20; border:1px solid #262c35; border-radius:10px; }
        QPushButton { background:#232a33; border:1px solid #353d48; border-radius:7px; padding:8px 14px; }
        QPushButton:hover { background:#2d3642; }
        QPlainTextEdit { background:#0b0d10; border:0; }
        QLabel#title { font-size:18px; font-weight:700; }
        QLabel#status { color:#6ee7b7; font-weight:600; }
        """)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(12, 12, 12, 12)

        bar = QHBoxLayout()
        title = QLabel("PriceAction · Liquidity Hunter")
        title.setObjectName("title")
        status = QLabel("● PAPER / CONNECTING")
        status.setObjectName("status")
        bar.addWidget(title)
        bar.addStretch()
        for text in ("▶ 启动", "⏸ 暂停", "⚡ 实盘", "⚙ 参数"):
            bar.addWidget(QPushButton(text))
        bar.addWidget(status)
        layout.addLayout(bar)

        splitter = QSplitter(Qt.Horizontal)
        chart = QWebEngineView()
        chart.setMinimumWidth(800)
        channel = QWebChannel(chart.page())
        channel.registerObject("bridge", self.bridge)
        chart.page().setWebChannel(channel)
        html = Path(__file__).resolve().parents[2] / "web" / "index.html"
        chart.setUrl(html.as_uri())
        splitter.addWidget(chart)

        right = QFrame()
        right.setObjectName("panel")
        right_layout = QVBoxLayout(right)
        self.signal_label = QLabel("等待信号…")
        self.signal_label.setWordWrap(True)
        self.signal_label.setStyleSheet("font-size:16px; font-weight:700;")
        right_layout.addWidget(self.signal_label)
        right_layout.addWidget(QLabel("Liquidity / Order Flow / RL / Risk"))
        right_layout.addStretch()
        splitter.addWidget(right)
        splitter.setSizes([1100, 360])
        layout.addWidget(splitter, 1)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(190)
        layout.addWidget(self.log)
        self.setCentralWidget(root)

    def bind_runtime(self, runtime) -> None:
        self.runtime = runtime

    def push_market(self, snapshot: dict, signal: dict) -> None:
        self.bridge.publish(snapshot, signal)
        self.signal_label.setText(
            f"{signal['side']} · Score {signal['score']:.1f} · Confidence {signal['confidence']:.0%}\n"
            f"Price {signal['price']:.2f}\n{signal['reason']}"
        )
        self.log.appendPlainText(
            f"{snapshot['timestamp']:.3f} | {signal['side']} | {signal['score']:.1f} | {signal['reason']}"
        )
