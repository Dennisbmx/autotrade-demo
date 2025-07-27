
import threading, uvicorn, time
from autotrade.api.server import app

def run_server():
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=False)

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        pass
