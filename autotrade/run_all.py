import os
import asyncio
import threading
from pathlib import Path

from dotenv import load_dotenv
import uvicorn

import autotrade.api.server as srv
from autotrade.telegram.bot import run_bot
from autotrade.llm.gpt_advisor import ask_gpt


async def auto_brief():
    while True:
        srv.STATE["summary"] = ask_gpt("Give me one-sentence market brief")
        await asyncio.sleep(3600)


def start_server():
    uvicorn.run(srv.app, host='0.0.0.0', port=8000, reload=False)


def main():
    load_dotenv(Path(__file__).resolve().parent.parent / '.env')
    asyncio.get_event_loop().create_task(auto_brief())

    enable = os.getenv('ENABLE_TELEGRAM', 'true').lower() == 'true'
    token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    if enable and token:
        threading.Thread(target=run_bot, daemon=True).start()
    else:
        print('Telegram disabled.')

    start_server()


if __name__ == '__main__':
    main()
