import asyncio
import time
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from autotrade.api.state import STATE
from autotrade.broker.alpaca import close_trade, get_prices, open_trade
from autotrade.llm.gpt_advisor import ask_gpt

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE.parent
load_dotenv(ROOT / ".env")

app = FastAPI(title="AutoTrade 0.6.4")
TEMPLATES = Jinja2Templates(directory=str(BASE / "web" / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE / "web" / "static")), name="static")


async def summary_loop():
    while True:
        try:
            summary = ask_gpt(
                "Give me a one sentence market brief about US tech stocks"
            )
            if summary:
                STATE["summary"] = summary
                STATE["summary_ts"] = int(time.time())
        except Exception as exc:
            print("Summary update failed:", exc)
        await asyncio.sleep(3600)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(summary_loop())


@app.get("/")
async def root():
    return "AutoTrade backend OK"


@app.get("/prices")
async def prices(syms: str = "NVDA,AAPL,MSFT,TSLA"):
    symbols: List[str] = [s.strip() for s in syms.split(",") if s]
    return await asyncio.to_thread(get_prices, symbols)


@app.get("/hourly_summary")
async def hourly_summary():
    return {"summary": STATE["summary"], "ts": STATE["summary_ts"]}


class AnalyzeReq(BaseModel):
    capital: int
    risk: str
    lev: int
    inds: List[str] = []


@app.post("/analyze")
async def analyze(req: AnalyzeReq):
    prompt = (
        f"Capital ${req.capital}, Risk {req.risk}, Leverage {req.lev}, "
        f"Indicators: {', '.join(req.inds)}. Give short portfolio advice."
    )
    summary = ask_gpt(prompt)
    if summary:
        STATE["summary"] = summary
        STATE["summary_ts"] = int(time.time())
    return {"summary": summary, "alloc": []}


class TradeOpenReq(BaseModel):
    symbol: str
    qty: int


@app.post("/trade/open")
async def trade_open(req: TradeOpenReq):
    open_trade(req.symbol, req.qty)
    return {"status": "ok"}


class TradeCloseReq(BaseModel):
    symbol: str


@app.post("/trade/close")
async def trade_close(req: TradeCloseReq):
    close_trade(req.symbol)
    return {"status": "ok"}


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return TEMPLATES.TemplateResponse(
        "dashboard.html", {"request": request, "title": "Dashboard"}
    )


@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio(request: Request):
    return TEMPLATES.TemplateResponse(
        "portfolio.html", {"request": request, "title": "Portfolio"}
    )
