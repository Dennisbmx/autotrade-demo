import os
import random
from typing import Dict, List

from alpaca_trade_api import REST

ALPACA_API_KEY = os.getenv('ALPACA_API_KEY', '')
ALPACA_API_SECRET = os.getenv('ALPACA_API_SECRET', '')

class AlpacaBroker:
    """Simple wrapper around Alpaca API with a mock fallback."""

    def __init__(self):
        self.use_real = bool(ALPACA_API_KEY and ALPACA_API_SECRET)
        if self.use_real:
            self.client = REST(ALPACA_API_KEY, ALPACA_API_SECRET)
        else:
            self.client = None

    def buy(self, symbol: str, qty: int):
        if self.use_real:
            return self.client.submit_order(symbol=symbol, qty=qty,
                                            side='buy', type='market',
                                            time_in_force='gtc')
        print(f"[MOCK] Buy {qty} {symbol}")
        return {'symbol': symbol, 'qty': qty, 'side': 'buy', 'mock': True}

    def sell(self, symbol: str, qty: int):
        if self.use_real:
            return self.client.submit_order(symbol=symbol, qty=qty,
                                            side='sell', type='market',
                                            time_in_force='gtc')
        print(f"[MOCK] Sell {qty} {symbol}")
        return {'symbol': symbol, 'qty': qty, 'side': 'sell', 'mock': True}

    def get_prices(self, symbols: List[str]) -> Dict[str, float]:
        prices: Dict[str, float] = {}
        if self.use_real:
            for sym in symbols:
                try:
                    trade = self.client.get_latest_trade(sym)
                    prices[sym] = float(trade.price)
                except Exception:
                    prices[sym] = 0.0
        else:
            for sym in symbols:
                prices[sym] = round(random.uniform(10, 1000), 2)
        return prices
