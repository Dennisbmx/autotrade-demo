
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'web', 'templates'))

app = FastAPI(title='AutoTrade Minimal')

_PRICES = {
    'AAPL': 200,
    'GOOG': 150,
    'TSLA': 50,
}


@app.get('/', response_class=PlainTextResponse)
async def root() -> str:
    """Health-check endpoint."""
    return 'AutoTrade backend OK'


@app.get('/prices')
async def prices(syms: str):
    symbols = [s.strip().upper() for s in syms.split(',') if s.strip()]
    return {s: _PRICES.get(s, 0) for s in symbols}


@app.get('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse('dashboard.html', {
        'request': request,
        'prices': _PRICES,
    })
