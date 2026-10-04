from __future__ import annotations

from dataclasses import dataclass

from app.strategies.base import BaseStrategy, Signal


@dataclass
class MarketSnapshot:
    symbol: str
    timestamp: float
    price: float
    delta: float
    orderbook_imbalance: float
    liquidity_distance: float
    sweep_strength: float
    absorption_strength: float
    reclaim_strength: float


class LiquidityHunter(BaseStrategy):
    name = "liquidity_hunter"

    def evaluate(self, snapshot: MarketSnapshot) -> Signal:
        long_score = (
            25.0 * max(0.0, snapshot.orderbook_imbalance)
            + 25.0 * snapshot.sweep_strength
            + 25.0 * snapshot.absorption_strength
            + 25.0 * snapshot.reclaim_strength
        )
        short_score = (
            25.0 * max(0.0, -snapshot.orderbook_imbalance)
            + 25.0 * max(0.0, -snapshot.sweep_strength)
            + 25.0 * max(0.0, -snapshot.absorption_strength)
            + 25.0 * max(0.0, -snapshot.reclaim_strength)
        )
        if long_score >= short_score:
            side, score = "LONG", long_score
            reason = "下方流动性候选：盘口偏多 + 扫损/吸收/回收评分"
        else:
            side, score = "SHORT", short_score
            reason = "上方流动性候选：盘口偏空 + 扫损/吸收/回收评分"
        confidence = min(0.99, 0.5 + abs(long_score - short_score) / 200.0)
        return Signal(side, round(score, 2), round(confidence, 4), snapshot.price, reason)
