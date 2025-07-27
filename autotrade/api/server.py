
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import time, json

app = FastAPI(title='AutoTrade 0.6.3 Demo')

BASE = Path(__file__).resolve().parent.parent
TEMPLATES = Jinja2Templates(directory=str(BASE / 'web' / 'templates'))
app.mount('/static', StaticFiles(directory=str(BASE / 'web' / 'static')), name='static')

STATE = {'prices': {'NVDA': 900, 'AAPL': 200, 'MSFT': 420, 'TSLA': 250},
         'summary': 'No analysis yet.'}

@app.get('/prices')
async def prices(syms: str = 'NVDA,AAPL,MSFT,TSLA'):
    symbols = syms.split(',')
    return {s: STATE['prices'].get(s, 0) for s in symbols}

@app.get('/hourly_summary')
async def hourly():
    return {'summary': STATE['summary'], 'ts': int(time.time())}

@app.get('/', response_class=HTMLResponse)
async def root():
    return '<h1>AutoTrade backend OK</h1>'

@app.get('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request):
    return TEMPLATES.TemplateResponse('dashboard.html', {'request': request, 'title': 'Dashboard'})
