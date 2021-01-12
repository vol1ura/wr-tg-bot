import os
from dotenv import load_dotenv

import telebot


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

bot = telebot.TeleBot(os.environ.get('API_BOT_TOKEN'))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(regexp=r'^Бот\b')
def handle_message(message):
    bot.reply_to(message, message.text)


bot.polling()
