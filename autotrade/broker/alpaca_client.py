import os
import random
from typing import Dict, List

import yfinance as yf
from alpaca_trade_api import REST

from autotrade.api.state import STATE


class AlpacaBroker:
    def __init__(self) -> None:
        key = os.getenv("ALPACA_API_KEY", "")
        secret = os.getenv("ALPACA_API_SECRET", "")
        self._client = (
            REST(key, secret, base_url="https://paper-api.alpaca.markets")
            if key and secret
            else None
        )

    def use_real(self) -> bool:
        return self._client is not None

    def buy(self, symbol: str, qty: int) -> None:
        if self.use_real():
            self._client.submit_order(
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

    def sell(self, symbol: str) -> None:
        if symbol in STATE["positions"]:
            if self.use_real():
                try:
                    self._client.close_position(symbol)
                except Exception:
                    pass
            else:
                STATE["log"].append(f"MOCK SELL ALL {symbol}")
            STATE["positions"].pop(symbol, None)

    def get_prices(self, symbols: List[str]) -> Dict[str, float]:
        prices: Dict[str, float] = {}
        if self.use_real():
            for s in symbols:
                try:
                    trade = self._client.get_latest_trade(s)
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


broker = AlpacaBroker()
