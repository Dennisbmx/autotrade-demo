import asyncio
import time
from pathlib import Path
from typing import List

import os
import time
import asyncio
from pathlib import Path
from typing import List

import os, time, asyncio
from pathlib import Path
from dotenv import load_dotenv

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
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
=======
q7q20a-codex/set-up-demo-auto-trade-application
from pydantic import BaseModel

from autotrade.api.state import STATE
from autotrade.llm.gpt_advisor import ask_gpt
from autotrade.broker.alpaca import get_prices, open_trade, close_trade

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE.parent
load_dotenv(ROOT / '.env')

app = FastAPI(title="AutoTrade 0.6.4")
TEMPLATES = Jinja2Templates(directory=str(BASE / 'web' / 'templates'))
app.mount('/static', StaticFiles(directory=str(BASE / 'web' / 'static')), name='static')


async def summary_loop():
    while True:
        try:
            summary = ask_gpt("Give me a one sentence market brief about US tech stocks")
            if summary:
                STATE['summary'] = summary
                STATE['summary_ts'] = int(time.time())
        except Exception as exc:
            print('Summary update failed:', exc)
        await asyncio.sleep(3600)


@app.on_event('startup')
async def startup_event():
    asyncio.create_task(summary_loop())


@app.get('/')
async def root():
    return "AutoTrade backend OK"


@app.get('/prices')
async def prices(syms: str = 'NVDA,AAPL,MSFT,TSLA'):
    symbols: List[str] = [s.strip() for s in syms.split(',') if s]
    return await asyncio.to_thread(get_prices, symbols)


@app.get('/hourly_summary')
async def hourly_summary():
    return {"summary": STATE['summary'], "ts": STATE['summary_ts']}


class AnalyzeReq(BaseModel):
    capital: int
    risk: str
    lev: int
    inds: List[str] = []


@app.post('/analyze')
async def analyze(req: AnalyzeReq):
    prompt = (
        f"Capital ${req.capital}, Risk {req.risk}, Leverage {req.lev}, "
        f"Indicators: {', '.join(req.inds)}. Give short portfolio advice."
    )
    summary = ask_gpt(prompt)
    if summary:
        STATE['summary'] = summary
        STATE['summary_ts'] = int(time.time())
    return {"summary": summary, "alloc": []}


class TradeOpenReq(BaseModel):
    symbol: str
    qty: int


@app.post('/trade/open')
async def trade_open(req: TradeOpenReq):
    open_trade(req.symbol, req.qty)
    return {"status": "ok"}


class TradeCloseReq(BaseModel):
    symbol: str


@app.post('/trade/close')
async def trade_close(req: TradeCloseReq):
    close_trade(req.symbol)
    return {"status": "ok"}



import yfinance as yf
from alpaca_trade_api import REST
import openai

from .state import STATE
from autotrade.llm.gpt_advisor import ask_gpt
from autotrade.broker.alpaca import open_trade, close_trade
from pydantic import BaseModel

# -----------------------------------------------------------------------------
app = FastAPI(title='AutoTrade 0.6.3 Demo')

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE.parent
load_dotenv(ROOT / ".env")

TEMPLATES = Jinja2Templates(directory=str(BASE / "web" / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE / "web" / "static")), name="static")

ALPACA_KEY    = os.getenv("ALPACA_API_KEY", "")
ALPACA_SECRET = os.getenv("ALPACA_API_SECRET", "")
OPENAI_KEY    = os.getenv("OPENAI_API_KEY", "")
openai.api_key = OPENAI_KEY

# -----------------------------------------------------------------------------
def use_alpaca() -> bool:
    return bool(ALPACA_KEY and ALPACA_SECRET)


async def fetch_prices(symbols: list[str]) -> dict[str, float]:
    prices: dict[str, float] = {}
    if use_alpaca():
        api = REST(ALPACA_KEY, ALPACA_SECRET)
        for s in symbols:
            try:
                bar = api.get_latest_trade(s)
                prices[s] = float(bar.price)
            except Exception:
                prices[s] = 0.0
    else:                                     # fallback — yfinance
        for s in symbols:
            try:
                ticker = yf.Ticker(s)
                info   = ticker.fast_info
                prices[s] = float(info.get("last_price") or 0)
            except Exception:
                prices[s] = 0.0
    return prices


async def generate_summary() -> str:
    if not OPENAI_KEY:
        return "OpenAI disabled."
    prompt = "Provide a short market brief about US tech stocks."
    try:
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        return rsp.choices[0].message["content"].strip()
    except Exception as exc:
        print("GPT error:", exc)
        return STATE["summary"]

# -----------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    async def summary_loop():
        while True:
            try:
                STATE["summary"] = await generate_summary()
                STATE["summary_ts"] = int(time.time())
            except Exception as exc:
                print("Summary update failed:", exc)
            await asyncio.sleep(3600)
    asyncio.create_task(summary_loop())

# -----------------------------------------------------------------------------
@app.get("/prices")
async def prices(syms: str = "NVDA,AAPL,MSFT,TSLA"):
    symbols = [s.strip() for s in syms.split(",") if s]
    STATE["prices"] = await fetch_prices(symbols)
    return STATE["prices"]


@app.get("/hourly_summary")
async def hourly_summary():
    return {"summary": STATE["summary"], "ts": STATE.get("summary_ts", int(time.time()))}

# -----------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>AutoTrade backend OK</h1>"



@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
q7q20a-codex/set-up-demo-auto-trade-application
    return TEMPLATES.TemplateResponse('dashboard.html', {'request': request, 'title': 'Dashboard'})


@app.get('/portfolio', response_class=HTMLResponse)
async def portfolio(request: Request):
    return TEMPLATES.TemplateResponse('portfolio.html', {'request': request, 'title': 'Portfolio'})

    return TEMPLATES.TemplateResponse("dashboard.html", {"request": request, "title": "Dashboard"})


@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio(request: Request):
    return TEMPLATES.TemplateResponse(
        "portfolio.html", {"request": request, "title": "Portfolio"}
    )

    return TEMPLATES.TemplateResponse("portfolio.html", {"request": request, "title": "Portfolio"})

# -----------------------------------------------------------------------------
class AnalyzeReq(BaseModel):
    capital: int
    risk: str
    lev: int
    inds: list[str] = []


@app.post("/analyze")
async def analyze(data: AnalyzeReq):
    prompt = (
        f"Capital ${data.capital}, Risk {data.risk}, "
        f"Leverage {data.lev}, Indicators: {', '.join(data.inds)}."
    )
    summary = ask_gpt(prompt)
    STATE["summary"] = summary
    return {"summary": summary, "alloc": []}

# -----------------------------------------------------------------------------
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

