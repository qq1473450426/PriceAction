from __future__ import annotations

import asyncio
import math
import time
from dataclasses import asdict
from threading import Thread
from typing import Optional

from app.strategies.liquidity_hunter import LiquidityHunter, MarketSnapshot


class RuntimeController:
    def __init__(self, window) -> None:
        self.window = window
        self.strategy = LiquidityHunter()
        self._thread: Optional[Thread] = None
        self._stop_event = False
        self._last_price = 100000.0
        self._step = 0

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event = False
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event = True
        if self._thread:
            self._thread.join(timeout=1.0)

    def _run(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._pump())
        loop.close()

    async def _pump(self) -> None:
        while not self._stop_event:
            self._step += 1
            self._last_price += math.sin(self._step / 17.0) * 2.5
            snapshot = MarketSnapshot(
                symbol="BTC-USDT-SWAP",
                timestamp=time.time(),
                price=self._last_price,
                delta=math.sin(self._step / 9.0) * 140.0,
                orderbook_imbalance=math.sin(self._step / 13.0) * 0.75,
                liquidity_distance=0.0015 + abs(math.sin(self._step / 21.0)) * 0.004,
                sweep_strength=max(0.0, math.sin(self._step / 15.0)),
                absorption_strength=max(0.0, math.cos(self._step / 18.0)),
                reclaim_strength=max(0.0, math.sin(self._step / 11.0)),
            )
            signal = self.strategy.evaluate(snapshot)
            self.window.push_market(asdict(snapshot), asdict(signal))
            await asyncio.sleep(0.25)
