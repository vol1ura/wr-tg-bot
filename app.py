import logging
import os

from flask import Flask, request

import telebot

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

TOKEN = os.environ.get('API_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет, ' + message.from_user.first_name)


@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id, "🤖 /start - display the keyboard\n"
                                      "☁ /weather - current forecast\n"
                                      "💎 /comm5 - current cryptocurrency\n"
                                      "⌛️ /comm2 - current time\n"
                                      "📊 /comm3 - current stocks prices\n"
                                      "📰 /news - latest bbc article\n"
                                      "🔁 /comm1 - language translator")


@bot.message_handler(commands=['weather'])
def command_weather(message):
    sent = bot.send_message(message.chat.id, "🗺 Enter the City or Country\n🔍 In such format:  Toronto  or  japan")
    bot.register_next_step_handler(sent, send_forecast)


def send_forecast(message):
    # try:
    #     get_forecast(message.text)
    # except pyowm.exceptions.api_response_error.NotFoundError:
    #     bot.send_message(message.chat.id, "❌  Wrong place, check mistakes and try again!")
    # forecast = get_forecast(message.text)
    bot.send_message(message.chat.id, 'forecast')


@bot.message_handler(regexp=r'^Бот\b', content_types=['text'])
def echo_message(message):
    bot.send_message(message.chat.id, 'и вам не хворать!')


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route(f"/{os.environ.get('WEBHOOK')}")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://wr-tg-bot.herokuapp.com/' + TOKEN)
    return "!", 200


@app.route("/")
def webhook():
    return "<h1>Привет, вы на странице для администрирования бота</h1>", 200


if __name__ == '__main__':
    app.run()
