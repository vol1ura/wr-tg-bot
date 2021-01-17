import logging
import os
import random
import re
import time

from dotenv import load_dotenv

import telebot
# https://api.telegram.org/{TOKEN}/getMe
from telebot import types

from utils import content, vk, instagram, weather, parkrun, news, search

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN_BOT = os.environ.get('API_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN_BOT)
logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)  # Outputs debug messages to console.

# if message.chat.type == "private":
# 	# private chat message
#
# if message.chat.type == "group":
# 	# group chat message
#
# if message.chat.type == "supergroup":
# 	# supergroup chat message
#
# if message.chat.type == "channel":
# 	# channel message


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, content.start_message, disable_notification=True)


@bot.message_handler(commands=['about', 'оботе'])
@bot.message_handler(regexp=r'(?i)\bбот\b(?=.*о себе)', content_types=['text'])
def about(message):
    bot.send_message(message.chat.id, content.about_message, disable_notification=True)


@bot.message_handler(commands=['admin', 'админ'])
@bot.message_handler(func=lambda message: search.bot_compare(message.text, search.phrases_admin))
def admin(message):
    if message.chat.type == "private":  # private chat message
        bot.send_message(message.chat.id, 'Здесь нет админов, мы все равны.', parse_mode=None)
    else:
        admin = random.choice(bot.get_chat_administrators(message.chat.id)).user.to_dict()
        about_admin = f"\nАдмин @{admin['username']} - {admin['first_name']}  {admin['last_name']}"
        bot.send_message(message.chat.id, random.choice(content.phrases_about_admin) + about_admin, parse_mode=None)


@bot.message_handler(commands=['social', 'соцсети'])
@bot.message_handler(func=lambda message: search.bot_compare(message.text, search.phrases_social))
def social(message):
    bot.send_message(message.chat.id, content.about_social,
                     parse_mode='MarkdownV2', disable_web_page_preview=True, disable_notification=True)


@bot.message_handler(commands=['shedule', 'расписание'])
@bot.message_handler(regexp=r'(?i)\bбот\b(?=.*(\bрасписани\B|когда тренировк\B))', content_types=['text'])
def shedule(message):
    bot.send_message(message.chat.id, content.about_training,
                     parse_mode='MarkdownV2', disable_web_page_preview=True, disable_notification=True)


@bot.message_handler(commands=['help', 'помощь', 'команды', 'справка'])
def commands(message):
    bot.send_message(message.chat.id, """Я понимаю следующие команды:
    📆 /schedule, /расписание - расписание тренировок
    📱 /social, /соцсети - Wake&Run в соцсетях
    👤 /admin, /админ - администраторы чата
    🤖 /about, /оботе - информация о боте
    ❓ /help, /помощь, /справка, /команды - данное сообщение
    Есть inline режим запросов.
    Кроме того, со мной можно просто поболтать.""", disable_notification=True)
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    # itembtn1 = types.KeyboardButton('📆 Расписание')
    # itembtn2 = types.KeyboardButton('📱 Соцсети клуба')
    # itembtn3 = types.KeyboardButton('👤 Администратор')
    # itembtn4 = types.KeyboardButton('🤖 О боте')
    # markup.add(itembtn1, itembtn2, itembtn3, itembtn4)


@bot.message_handler(func=lambda message: search.bot_compare(message.text, search.phrases_to_run))
def ask_to_run(message):
    # if message.chat.type == "private":
    #     print('debug')
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    #     m1 = types.KeyboardButton('My position', request_location=True)
    #     markup.add(m1)
    #     return markup
    #     place = 'Кузьминки'
    # else:
    place = 'Кузьминки'  # TODO how to get user location??? Make check for private chat and implement request
    aq = weather.get_air_quality(place, content.places[place].lat, content.places[place].lon)
    if aq[0] > 3:
        bot.reply_to(message, 'Если вы с Москве, то крайне не рекомендую сейчас бегать, '
                              'показатели загрязнения воздуха высокие. Лучше попозже.')
    elif time.gmtime(time.time()).tm_wday == 3 and time.gmtime(time.time()).tm_hour < 20:
        bot.reply_to(message, 'Сегодня ж четверговая, приходи побегать в компании! '
                              'Информация о тренировках доступна по команде /shedule')
    elif time.gmtime(time.time()).tm_wday == 6 and time.gmtime(time.time()).tm_hour < 9:
        bot.reply_to(message, 'Сегодня ж длительная в парке, приходи на пробежку в компании! '
                              'Информация о тренировках доступна по команде /shedule')
    elif time.gmtime(time.time()).tm_wday == 1 and time.gmtime(time.time()).tm_hour < 19:
        bot.reply_to(message, 'Сегодня ж городская пробежка, приходи! '
                              'Информация о тренировках доступна по команде /shedule')
    else:
        bot.reply_to(message, random.choice(content.phrases_about_running))


@bot.inline_handler(lambda query: 'погода' in query.query)
def query_weather(inline_query):
    try:
        places_weather = [types.InlineQueryResultArticle(
            f'{k}', k, description='погода сейчас',
            input_message_content=types.InputTextMessageContent(weather.get_weather(k, v.lat, v.lon)))
            for k, v in content.places.items()]
        bot.answer_inline_query(inline_query.id, places_weather, cache_time=3000)
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: query.query == 'воздух')
def query_air(inline_query):
    try:
        places_air = [types.InlineQueryResultArticle(
            f'{k}', k, description='качество воздуха',
            input_message_content=types.InputTextMessageContent(weather.get_air_quality(k, v.lat, v.lon)[1]))
            for k, v in content.places.items()]
        bot.answer_inline_query(inline_query.id, places_air, cache_time=3000)
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: 'паркран' in query.query or 'parkrun' in query.query)
def query_parkrun(inline_query):
    try:
        m1 = types.InlineQueryResultArticle(
            f'{1}', 'Где бегали наши одноклубники?', description='перечень паркранов',
            input_message_content=types.InputTextMessageContent(parkrun.get_participants(),
                                                                parse_mode='Markdown', disable_web_page_preview=True))
        m2 = types.InlineQueryResultArticle(
            f'{2}', 'Как установить клуб в parkrun?', description='ссылка на клуб Wake&Run',
            input_message_content=types.InputTextMessageContent(parkrun.get_club(),
                                                                parse_mode='Markdown', disable_web_page_preview=True))
        bot.answer_inline_query(inline_query.id, [m2, m1], cache_time=100000)  # FIXME change time for debug
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: re.search(r'соревнован|старт|забег', query.query))
def query_competitions(inline_query):
    try:
        date = time.gmtime(time.time())
        month, year = date.tm_mon, date.tm_year
        competitions = news.get_competitions(month, year)
        print(len(competitions))
        if len(competitions) < 10:
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
            competitions += news.get_competitions(month, year)

        queries = []
        for i, comp in enumerate(competitions, 1):
            queries.append(types.InlineQueryResultArticle(
                str(i), comp[0], description=comp[1],
                input_message_content=types.InputTextMessageContent(comp[2], parse_mode='html')))
        bot.answer_inline_query(inline_query.id, queries, cache_time=600000)
    except Exception as e:
        print(e)


@bot.message_handler(regexp=r'(?i)бот (паркран|parkrun)', content_types=['text'])
def get_parkrun_picture(message):
    token = os.environ.get('VK_SERVICE_TOKEN')
    bot.send_photo(message.chat.id, vk.get_random_photo(token), disable_notification=True)


@bot.message_handler(func=lambda message: search.bot_compare(message.text, search.phrases_instagram))
def get_instagram_post(message):
    login = os.environ.get('IG_USERNAME')
    password = os.environ.get('IG_PASSWORD')
    user = random.choice(content.instagram_profiles)
    wait_message = bot.reply_to(message, 'Сейчас что-нибудь найду, подождите...', disable_notification=True)
    ig_post = instagram.get_last_post(login, password, user)
    bot.send_photo(message.chat.id, *ig_post, disable_notification=True)
    bot.delete_message(wait_message.chat.id, wait_message.id)


@bot.message_handler(regexp=r'(?i)\bбот\b', content_types=['text'])
def simple_answers(message):
    ans = []
    if 'как' in message.text and re.search('дел|жизнь|сам|поживаешь', message.text, re.I):
        ans = content.phrases_about_myself
    elif re.search('привет|hi|hello|здравствуй', message.text, re.I):
        user = message.from_user.first_name
        ans = [s.format(user) for s in content.greeting]
    elif search.bot_compare(message.text, search.phrases_parkrun):
        ans = content.phrases_about_parkrun

    if ans:
        bot.reply_to(message, random.choice(ans), disable_web_page_preview=True)
        return
    elif 'погода' in message.text:
        ans = ['Информацио о погоде можно получить через inline запрос: в строке сообщений наберите "@имябота погода"']
    elif re.search(r'\bтренировк', message.text):
        ans = [content.about_training]
    # elif 'топ стравы' in message.text:
    #     ans = ['Текст-----------------------------------------']
    else:
        ans = content.phrases_about_running
    bot.send_message(message.chat.id, random.choice(ans), disable_web_page_preview=True)


if __name__ == '__main__':
    # print(os.environ.get('API_BOT_TOKEN'))
    # bot.remove_webhook()
    bot.polling(none_stop=True)
