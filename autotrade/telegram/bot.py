import os
import telebot

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
ENABLE = os.getenv('ENABLE_TELEGRAM', 'true').lower() == 'true'

bot = telebot.TeleBot(TOKEN) if TOKEN and ENABLE else None


def run_bot():
    if not bot:
        print('Telegram disabled.')
        return

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
