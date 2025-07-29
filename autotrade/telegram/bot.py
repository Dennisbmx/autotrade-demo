import os
import telebot

from autotrade.api.state import STATE

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

bot = telebot.TeleBot(TOKEN) if TOKEN else None
_paused = False
import threading
import time
import telebot
from autotrade.api.state import STATE

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

bot = telebot.TeleBot(TOKEN) if TOKEN else None
_paused = False

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

bot = telebot.TeleBot(TOKEN) if TOKEN else None
_paused = False

import telebot

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
ENABLE = os.getenv('ENABLE_TELEGRAM', 'true').lower() == 'true'

bot = telebot.TeleBot(TOKEN) if TOKEN and ENABLE else None


def run_bot():
    if not bot:
        print("Telegram disabled.")
        return

    @bot.message_handler(commands=["start"])
    def start(msg):
        bot.reply_to(msg, "AutoTrade 0.6.4 online")

    @bot.message_handler(commands=["ping"])
    def ping(msg):
        bot.reply_to(msg, "pong")

    @bot.message_handler(commands=["pause"])
    def pause(msg):
        global _paused
        _paused = True
        bot.reply_to(msg, "paused")

    @bot.message_handler(commands=["resume"])
    def resume(msg):
        global _paused
        _paused = False
        bot.reply_to(msg, "resumed")

    @bot.message_handler(commands=["status"])


    @bot.message_handler(commands=['start'])
    def start(msg):
        bot.reply_to(msg, 'AutoTrade 0.6.4 online')

    @bot.message_handler(commands=['ping'])
    def ping(msg):
        bot.reply_to(msg, 'pong')

    @bot.message_handler(commands=['pause'])
    def pause(msg):
        global _paused
        _paused = True
        bot.reply_to(msg, 'paused')

    @bot.message_handler(commands=['resume'])
    def resume(msg):
        global _paused
        _paused = False
        bot.reply_to(msg, 'resumed')

    @bot.message_handler(commands=['status'])
    def status(msg):
        text = f"Summary: {STATE['summary']}\nPositions: {STATE['positions']}"
        bot.reply_to(msg, text)

    if CHAT_ID:
        bot.send_message(CHAT_ID, "Bot started")


        bot.send_message(CHAT_ID, 'Bot started')

    @bot.message_handler(commands=['ping'])
    def _ping(message):
        bot.reply_to(message, 'pong')

    if CHAT_ID:
        bot.send_message(CHAT_ID, 'Bot started')
    else:
        print('CHAT_ID not set; bot running without alerts.')


    bot.infinity_polling()


def send_alert(text: str):
    if bot and CHAT_ID:
        bot.send_message(CHAT_ID, text)



if __name__ == '__main__':
    run_bot()
