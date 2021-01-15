# Bot is deployed on Heroku, so it might sleep
# after 30 mins of being inactive but could wake up (big delay around 30 secs)
from flask import Flask, request, abort

from wakeandrunbot import *


app = Flask(__name__)


@app.route('/' + TOKEN_BOT, methods=['POST'])
def get_message():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)
    # bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    # return "!", 200


@app.route(f"/{config.WEBHOOK}")
def webhook():
    bot.remove_webhook()
    # bot.set_webhook(url='127.0.0.1:5000/' + TOKEN_BOT)
    bot.set_webhook(url='https://wakeandrun.pythonanywhere.com/' + TOKEN_BOT)
    return "!", 200


@app.route("/bot")
def bot():
    return "<h1>Привет, вы на странице для администрирования бота</h1>", 200


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'Привет!'


if __name__ == '__main__':
    app.run()
