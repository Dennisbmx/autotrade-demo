import os
import random
from typing import Dict, List

import yfinance as yf
from alpaca_trade_api import REST

from autotrade.api.state import STATE

ALPACA_KEY = os.getenv("ALPACA_API_KEY", "")
ALPACA_SECRET = os.getenv("ALPACA_API_SECRET", "")
BASE_URL = "https://paper-api.alpaca.markets"

_client = (
    REST(ALPACA_KEY, ALPACA_SECRET, base_url=BASE_URL)
    if ALPACA_KEY and ALPACA_SECRET
    else None
)


def use_real() -> bool:
    return _client is not None


def open_trade(symbol: str, qty: int):
    if use_real():
        _client.submit_order(
            symbol=symbol,
            qty=qty,
            side="buy",
            type="market",
            time_in_force="gtc",
        )
    else:
        STATE["log"].append(f"MOCK BUY {qty} {symbol}")
    pos = STATE["positions"].setdefault(symbol, {"qty": 0, "avg": 0})
    pos["qty"] += qty


def close_trade(symbol: str):
    if symbol in STATE["positions"]:
        if use_real():
            try:
                _client.close_position(symbol)
            except Exception:
                pass
        else:
            STATE["log"].append(f"MOCK SELL ALL {symbol}")
        STATE["positions"].pop(symbol, None)


def get_prices(symbols: List[str]) -> Dict[str, float]:
    prices: Dict[str, float] = {}
    if use_real():
        for s in symbols:
            try:
                trade = _client.get_latest_trade(s)
                prices[s] = float(trade.price)
            except Exception:
                prices[s] = 0.0
    else:
        for s in symbols:
            try:
                prices[s] = float(yf.Ticker(s).fast_info.last_price)
            except Exception:
                prices[s] = round(random.uniform(10, 1000), 2)
    return prices
