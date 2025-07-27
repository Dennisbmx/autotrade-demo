import os
import time
import asyncio
from pathlib import Path

from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import yfinance as yf
from alpaca_trade_api import REST
import openai

app = FastAPI(title='AutoTrade 0.6.3 Demo')

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE.parent
load_dotenv(ROOT / '.env')
TEMPLATES = Jinja2Templates(directory=str(BASE / 'web' / 'templates'))
app.mount('/static', StaticFiles(directory=str(BASE / 'web' / 'static')), name='static')

ALPACA_KEY = os.getenv('ALPACA_API_KEY', '')
ALPACA_SECRET = os.getenv('ALPACA_API_SECRET', '')
OPENAI_KEY = os.getenv('OPENAI_API_KEY', '')

STATE = {
    'prices': {},
    'summary': 'No analysis yet.',
    'summary_ts': int(time.time())
}


def use_alpaca() -> bool:
    return bool(ALPACA_KEY and ALPACA_SECRET)


async def fetch_prices(symbols):
    prices = {}
    if use_alpaca():
        api = REST(ALPACA_KEY, ALPACA_SECRET)
        for s in symbols:
            try:
                bar = api.get_latest_trade(s)
                prices[s] = float(bar.price)
            except Exception:
                prices[s] = 0.0
    else:
        for s in symbols:
            try:
                ticker = yf.Ticker(s)
                info = ticker.fast_info
                prices[s] = float(info.get('last_price') or 0)
            except Exception:
                prices[s] = 0.0
    return prices


async def generate_summary() -> str:
    if not OPENAI_KEY:
        return 'OpenAI disabled.'
    openai.api_key = OPENAI_KEY
    prompt = 'Provide a short market brief about US tech stocks.'
    try:
        resp = await openai.ChatCompletion.acreate(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        print('GPT error:', exc)
        return STATE['summary']


async def summary_loop():
    while True:
        try:
            STATE['summary'] = await generate_summary()
            STATE['summary_ts'] = int(time.time())
        except Exception as e:
            print('Summary update failed:', e)
        await asyncio.sleep(3600)


@app.on_event('startup')
async def startup_event():
    asyncio.create_task(summary_loop())


@app.get('/prices')
async def prices(syms: str = 'NVDA,AAPL,MSFT,TSLA'):
    symbols = [s.strip() for s in syms.split(',') if s]
    STATE['prices'] = await fetch_prices(symbols)
    return STATE['prices']


@app.get('/hourly_summary')
async def hourly():
    return {'summary': STATE['summary'], 'ts': STATE['summary_ts']}


@app.get('/', response_class=HTMLResponse)
async def root():
    return '<h1>AutoTrade backend OK</h1>'


@app.get('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request):
    return TEMPLATES.TemplateResponse('dashboard.html', {'request': request, 'title': 'Dashboard'})


@app.get('/portfolio', response_class=HTMLResponse)
async def portfolio(request: Request):
    return TEMPLATES.TemplateResponse('portfolio.html', {'request': request, 'title': 'Portfolio'})
