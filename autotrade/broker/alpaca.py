from autotrade.api.state import STATE


def open_trade(symbol: str, qty: int):
    STATE["log"].append(f"MOCK BUY {qty} {symbol}")
    pos = STATE["positions"].setdefault(symbol, {"qty": 0, "avg": 0})
    pos["qty"] += qty
    # real Alpaca REST call would go here


def close_trade(symbol: str):
    if symbol in STATE["positions"]:
        STATE["log"].append(f"MOCK SELL ALL {symbol}")
        STATE["positions"].pop(symbol)
    # real Alpaca REST call would go here
