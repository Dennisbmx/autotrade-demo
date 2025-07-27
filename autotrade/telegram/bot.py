
import os, telebot

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN','')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID','')

bot = telebot.TeleBot(TOKEN) if ':' in TOKEN else None

def run_bot():
    if not bot:
        print('Telegram disabled.')
        return
    @bot.message_handler(commands=['ping'])
    def _ping(m):
        bot.reply_to(m,'pong')
    bot.send_message(CHAT_ID or m.chat.id,'Bot started')
    bot.infinity_polling()

if __name__=='__main__':
    run_bot()
