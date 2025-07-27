
import threading, time, uvicorn
from autotrade.api.server import app

def run_server():
    uvicorn.run(app, host='0.0.0.0', port=8000)

if __name__=='__main__':
    threading.Thread(target=run_server, daemon=True).start()
    while True:
        time.sleep(3600)
