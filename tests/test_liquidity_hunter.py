from app.strategies.liquidity_hunter import LiquidityHunter, MarketSnapshot


def test_liquidity_hunter_returns_signal():
    strategy = LiquidityHunter()
    snapshot = MarketSnapshot("BTC-USDT-SWAP", 0.0, 100000.0, 100.0, 0.8, 0.002, 1.0, 1.0, 1.0)
    signal = strategy.evaluate(snapshot)
    assert signal.side == "LONG"
    assert signal.score > 70
