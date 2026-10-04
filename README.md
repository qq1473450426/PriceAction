# PriceAction

OKX Liquidity Hunter AI Trading Terminal. V0.1 is the desktop foundation for a Python-first trading system.

## Architecture

OKX WebSocket/REST -> market data -> feature engine -> strategies -> risk -> execution -> UI.
The first strategy is a deterministic Liquidity Hunter candidate-signal engine. Reinforcement learning is isolated behind a model interface and can be added after paper-trading data is available.

## V0.1 scope

- PySide6 Windows desktop shell
- Embedded Lightweight Charts frontend
- Local Python-to-chart bridge
- Mock market feed for offline UI testing
- Strategy interface and explainable Liquidity Hunter score
- Structured logs
- Paper/live mode placeholders

## Run

Python 3.11+

    pip install -r requirements.txt
    python -m app.main

The current UI uses a deterministic mock stream, so no exchange credentials are required for the first development milestone.
