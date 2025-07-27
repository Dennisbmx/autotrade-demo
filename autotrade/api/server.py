
from fastapi import FastAPI
app = FastAPI(title='AutoTrade Minimal')

@app.get('/')
async def root():
    return {'msg':'AutoTrade API alive'}
