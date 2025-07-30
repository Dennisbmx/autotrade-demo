from typing import List, Dict
from autotrade.brokers.alpaca_client import AlpacaBroker

class TradeEngine:
    def __init__(self):
        self.broker = AlpacaBroker()

    def buy(self, symbol: str, qty: int):
        return self.broker.buy(symbol, qty)

    def sell(self, symbol: str, qty: int):
        return self.broker.sell(symbol, qty)

    def get_prices(self, symbols: List[str]) -> Dict[str, float]:
        return self.broker.get_prices(symbols)
