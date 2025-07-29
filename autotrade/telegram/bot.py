import os

import telebot

from autotrade.api.state import STATE

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

bot = telebot.TeleBot(TOKEN) if TOKEN else None
_paused = False


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
    def status(msg):
        text = f"Summary: {STATE['summary']}\nPositions: {STATE['positions']}"
        bot.reply_to(msg, text)

    if CHAT_ID:
        bot.send_message(CHAT_ID, "Bot started")

    bot.infinity_polling()


def send_alert(text: str):
    if bot and CHAT_ID:
        bot.send_message(CHAT_ID, text)
