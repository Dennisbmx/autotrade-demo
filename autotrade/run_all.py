import os
import threading
from pathlib import Path

from dotenv import load_dotenv
import uvicorn

from autotrade.api.server import app
from autotrade.telegram.bot import run_bot


def start_server():
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=False)


def main():
    load_dotenv(Path(__file__).resolve().parent.parent / '.env')

    enable = os.getenv('ENABLE_TELEGRAM', 'true').lower() == 'true'
    token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    if enable and token:
        threading.Thread(target=run_bot, daemon=True).start()
    else:
        print('Telegram disabled.')

    start_server()


if __name__ == '__main__':
    main()
