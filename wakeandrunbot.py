import logging
import os
import random
import re
import time

import telebot
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
# https://api.telegram.org/{TOKEN}/getMe
from telebot import types

from utils import content, vk, instagram, weather, chat_gpt, news, fucomp, search, impulse

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

TOKEN_BOT = os.environ.get('API_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN_BOT)
logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)  # Outputs WARNING messages to log and console.


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, content.start_message, disable_notification=True)


@bot.message_handler(commands=['about', 'оботе'])
@bot.message_handler(regexp=r'(?i)^бот\b(?=.*о себе)', content_types=['text'])
def about(message):
    bot.send_message(message.chat.id, content.about_message,
                     disable_notification=True, parse_mode='html', disable_web_page_preview=True)


@bot.message_handler(commands=['admin', 'админ'])
@bot.message_handler(func=lambda message: fucomp.bot_compare(message.text, fucomp.phrases_admin))
def admin_info(message):
    if message.chat.type == "private":  # private chat message
        bot.send_message(message.chat.id, 'Здесь нет админов, мы все равны.')
    else:
        admin = random.choice(bot.get_chat_administrators(message.chat.id)).user.to_dict()
        about_admin = f"\nАдмин @{admin['username']} - {admin['first_name']}  {admin['last_name']}"
        bot.send_message(message.chat.id, random.choice(content.phrases_about_admin) + about_admin)


@bot.message_handler(commands=['social', 'соцсети'])
@bot.message_handler(func=lambda message: fucomp.bot_compare(message.text, fucomp.phrases_social))
def social(message):
    bot.send_message(message.chat.id, content.about_social,
                     parse_mode='Markdown', disable_web_page_preview=True, disable_notification=True)


@bot.message_handler(commands=['schedule', 'расписание'])
@bot.message_handler(func=lambda message: fucomp.bot_compare(message.text, fucomp.phrases_schedule))
def schedule(message):
    bot.send_message(message.chat.id, content.about_training,
                     parse_mode='Markdown', disable_web_page_preview=True, disable_notification=True)


@bot.message_handler(commands=['help', 'помощь'])
def commands(message):
    bot_nick = bot.get_me().to_dict()["username"]
    bot.send_message(message.chat.id, f"""Я понимаю следующие команды:
    📆 /schedule, /расписание - расписание тренировок
    📱 /social, /соцсети - Wake&Run в соцсетях
    👤 /admin, /админ - администраторы чата
    🤖 /about, /оботе - информация о боте
    ❓ /help, /помощь - _данное сообщение_
    Есть *inline* режим запросов - наберите в поле ввода сообщения @{bot_nick} <запрос> (примеры):
    @{bot_nick} погода
    @{bot_nick} воздух
    @{bot_nick} старты
    Через пару секунд появится меню, из которого можно выбрать нужный вариант информации.
    Про погоду и воздух можно также спросить напрямую, например, _Бот, погода Москва Кузьминки_, либо
    _Бот, воздух Кисловодск_.
    Если отправлять сообщения _Бот суббота_,  _Бот, инстаграм_, бот будет находить картинки или новости.
    Бот _не чувствителен_ к знакам пунктуации, регистру букв, и, в большинстве случаев, к порядку фраз.
    Кроме того, с ботом можно просто поболтать - отправьте сообщение, начинающееся словом *бот*.""",
                     disable_notification=True, parse_mode='Markdown')


@bot.message_handler(regexp=r'(?i)бот,? (?:покажи )?(погод\w|воздух)( \w+,?){1,3}$')
def ask_weather(message):
    match = re.search(r'бот,? (?:покажи )?(погод\w|воздух) ([\w, ]+)', message.text, re.I)
    if match:
        place = re.sub(r' в\b', '', match.group(2).strip())
        app = Nominatim(user_agent="wr-tg-bot")
        try:
            location = app.geocode(place).raw
        except AttributeError:
            return bot.reply_to(message, f'Есть такой населённый пункт {place}? ...не знаю. Введите запрос в в формате '
                                         '"Бот, погода Город" или "Бот, воздух Название Область".')
        if match.group(1).startswith('погод'):
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, weather.get_weather(place, location['lat'], location['lon']))
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, weather.get_air_quality(place, location['lat'], location['lon'])[1])


@bot.inline_handler(lambda query: 'погода' in query.query)
def query_weather(inline_query):
    try:
        places_weather = [types.InlineQueryResultArticle(
            f'{k}', k, description='погода сейчас',
            input_message_content=types.InputTextMessageContent(weather.get_weather(k, v.lat, v.lon)))
            for k, v in content.places.items()]
        bot.answer_inline_query(inline_query.id, places_weather, cache_time=3000)
    except Exception as e:
        logger.error(e)


@bot.inline_handler(lambda query: 'воздух' in query.query)
def query_air(inline_query):
    try:
        places_air = [types.InlineQueryResultArticle(
            f'{k}', k, description='качество воздуха',
            input_message_content=types.InputTextMessageContent(weather.get_air_quality(k, v.lat, v.lon)[1]))
            for k, v in content.places.items()]
        bot.answer_inline_query(inline_query.id, places_air, cache_time=3000)
    except Exception as e:
        logger.error(e)


# @bot.inline_handler(lambda query: 'паркран' in query.query or 'parkrun' in query.query)
# def query_parkrun(inline_query):
#     try:
#         pattern = '⏳ Получение данных '
#         m1 = types.InlineQueryResultArticle(
#             f'{1}', 'Где бегали наши соклубники?', description='перечень паркранов',
#             input_message_content=types.InputTextMessageContent(pattern + 'об участии...'),
#             thumb_url='https://raw.githubusercontent.com/vol1ura/wr-tg-bot/master/static/pics/1.jpg',
#             thumb_width=48, thumb_height=48)
#         m2 = types.InlineQueryResultArticle(
#             f'{2}', 'Как установить наш клуб в parkrun?', description='ссылка на клуб Wake&Run',
#             input_message_content=types.InputTextMessageContent(parkrun.CLUB_INFO,
#                                                                 parse_mode='Markdown', disable_web_page_preview=True),
#             thumb_url='https://raw.githubusercontent.com/vol1ura/wr-tg-bot/master/static/pics/2.jpg',
#             thumb_width=48, thumb_height=48)
#         m3 = types.InlineQueryResultArticle(
#             f'{3}', 'Топ 10 волонтёров', description='на паркране Кузьминки',
#             input_message_content=types.InputTextMessageContent(pattern + 'о волонтёрах.', parse_mode='Markdown'),
#             thumb_url='https://raw.githubusercontent.com/vol1ura/wr-tg-bot/master/static/pics/3.jpg',
#             thumb_width=48, thumb_height=48)
#         m4 = types.InlineQueryResultArticle(
#             f'{4}', 'Топ 10 wakeandrunцев по числу забегов', description='на паркране Кузьминки',
#             input_message_content=types.InputTextMessageContent(pattern + 'о количестве стартов в Кузьминках...'),
#             thumb_url='https://raw.githubusercontent.com/vol1ura/wr-tg-bot/master/static/pics/4.jpg',
#             thumb_width=48, thumb_height=48)
#         m5 = types.InlineQueryResultArticle(
#             f'{5}', 'Топ 10 wakeandrunцев по количеству паркранов', description='по всем паркранам',
#             input_message_content=types.InputTextMessageContent(pattern + 'о количестве всех стартов...'),
#             thumb_url='https://raw.githubusercontent.com/vol1ura/wr-tg-bot/master/static/pics/5.jpg',
#             thumb_width=48, thumb_height=48)
#         m6 = types.InlineQueryResultArticle(
#             f'{6}', 'Топ 10 результатов соклубников', description='на паркране Кузьминки',
#             input_message_content=types.InputTextMessageContent(pattern + 'о рекордах...'),
#             thumb_url='https://raw.githubusercontent.com/vol1ura/wr-tg-bot/master/static/pics/6.jpg',
#             thumb_width=48, thumb_height=48)
#         m7 = types.InlineQueryResultArticle(
#             f'{7}', 'Самые медленные паркраны России', description='по мужским результатам',
#             input_message_content=types.InputTextMessageContent(pattern + 'о российских паркранах'),
#             thumb_url='https://raw.githubusercontent.com/vol1ura/wr-tg-bot/master/static/pics/7.jpg',
#             thumb_width=48, thumb_height=48)
#         m8 = types.InlineQueryResultArticle(
#             f'{8}', 'Гистограмма с последними результатами', description='на паркране Кузьминки',
#             input_message_content=types.InputTextMessageContent(pattern + 'и расчёт диаграммы...'),
#             thumb_url='https://raw.githubusercontent.com/vol1ura/wr-tg-bot/master/static/pics/8.jpg',
#             thumb_width=48, thumb_height=48)
#         m9 = types.InlineQueryResultArticle(
#             f'{9}', 'Диаграмма с распределением по клубам', description='на паркране Кузьминки',
#             input_message_content=types.InputTextMessageContent(pattern + 'о клубах...'),
#             thumb_url='https://raw.githubusercontent.com/vol1ura/wr-tg-bot/master/static/pics/9.jpg',
#             thumb_width=48, thumb_height=48)
#         bot.answer_inline_query(inline_query.id, [m1, m3, m8, m9, m4, m5, m6, m7, m2], cache_time=36000)
#     except Exception as e:
#         logger.error(e)


# @bot.message_handler(regexp='⏳ Получение данных', content_types=['text'])
# def post_parkrun_info(message):
#     bot.send_chat_action(message.chat.id, 'typing')
#     if 'об участии' in message.text:
#         bot.send_message(message.chat.id,
#                          parkrun.get_participants(),
#                          parse_mode='Markdown',
#                          disable_web_page_preview=True)
#     elif 'диаграммы' in message.text:
#         pic = parkrun.make_latest_results_diagram('results.png')
#         if os.path.exists("results.png"):
#             bot.send_photo(message.chat.id, pic)
#             pic.close()
#         else:
#             logger.error('File results.png not found! Or the picture wasn\'t generated.')


@bot.inline_handler(lambda query: re.search(r'соревнован|старт|забег|competition|event', query.query))
def query_competitions(inline_query):
    try:
        date = time.gmtime(time.time())
        month, year = date.tm_mon, date.tm_year
        competitions = news.get_competitions(month, year)
        logger.info(str(len(competitions)))
        if len(competitions) < 10:
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
            competitions += news.get_competitions(month, year)
        queries = [types.InlineQueryResultArticle(
            '111', 'Google-таблица стартов и одноклубников', description='Показать ссылку',
            input_message_content=types.InputTextMessageContent(news.club_calendar(), parse_mode='html'))]
        for i, comp in enumerate(competitions, 1):
            queries.append(types.InlineQueryResultArticle(
                str(i), comp[0], description=comp[1],
                input_message_content=types.InputTextMessageContent(comp[2], parse_mode='html')))
        bot.answer_inline_query(inline_query.id, queries, cache_time=30000)
    except Exception as e:
        logger.error(e)


@bot.message_handler(regexp=r'(?i)^бот[, \w]*(impulse|импульс)')
def parkrun_impulse_club_diagram(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        pic = impulse.ImpulseChallenge().make_clubs_bar('impulse.png')
        bot.send_photo(message.chat.id, pic)
        pic.close()
    except Exception as e:
        logger.error(f'Attempt to generate Impulse diagram failed. Query: {message.text}. Error: {e}')
        bot.reply_to(message, 'Что-то пошло не так. Не удалось построить диаграмму')


@bot.message_handler(regexp=r'(?i)бот,? (суббота|5km|9am|5\s?км\b)', content_types=['text'])
def get_parkrun_picture(message):
    token = os.environ.get('VK_SERVICE_TOKEN')
    bot.send_photo(message.chat.id, vk.get_random_photo(token), disable_notification=True)


@bot.message_handler(regexp=r'(?i)бот[, \w]* календарь', content_types=['text'])
def get_parkrun_picture(message):

    bot.reply_to(message, news.club_calendar(), disable_web_page_preview=True, parse_mode='html')


@bot.message_handler(func=lambda message: fucomp.bot_compare(message.text, fucomp.phrases_instagram))
def get_instagram_post(message):
    login = os.environ.get('IG_USERNAME')
    password = os.environ.get('IG_PASSWORD')
    user = random.choice(content.instagram_profiles)
    wait_message = bot.reply_to(message, 'Сейчас что-нибудь найду, подождите...', disable_notification=True)
    ig_post = instagram.get_last_post(login, password, user)
    bot.send_photo(message.chat.id, *ig_post, disable_notification=True)
    bot.delete_message(wait_message.chat.id, wait_message.id)


@bot.message_handler(regexp=r'(?i)^бот\b', content_types=['text'])
@bot.message_handler(func=lambda mes: mes.reply_to_message and mes.reply_to_message.from_user.is_bot)
def simple_answers(message):
    if 'как' in message.text and re.search(r'\bдела\b|жизнь|\bсам\b|поживаешь', message.text, re.I):
        ans = content.phrases_about_myself
    elif re.search(r'привет|\bhi\b|hello|здравствуй', message.text, re.I):
        user = message.from_user.first_name
        ans = [s.format(user) for s in content.greeting]
    elif fucomp.bot_compare(message.text, fucomp.phrases_parkrun):
        ans = content.phrases_about_parkrun
    elif 'Петрищев' in message.text:
        ans = [fucomp.best_answer(message.text, fucomp.petristchev)]
    elif 'погода' in message.text:
        bot_nick = bot.get_me().to_dict()["username"]
        ans = [f'Информацию о погоде можно получить через inline запрос: в строке сообщений наберите "@{bot_nick} '
               'погода". Либо, набрав сообщение, "Бот, погода Населённый пункт", например, '
               '"Бот, погода Кузьминки Москва".']
    elif re.search(r'GRUT|ГРУТ', message.text, re.I):
        ans = content.phrases_grut
    elif re.search(r'\bгречк|\bгречневая', message.text, re.I):
        ans = content.phrases_grechka
    else:
        ans = None

    if not ans:
        ans = [chat_gpt.ask(message.text)]
    if not ans:
        bot.send_chat_action(message.chat.id, 'typing')
        ans_variant = random.randrange(2021) % 3
        if ans_variant == 0:
            ans = [search.google(message.text)]
            if not ans[0]:
                ans = [random.choice(content.phrases_about_running)]
        elif ans_variant == 1:
            ans = [fucomp.best_answer(message.text, fucomp.message_base_wr)]
        else:
            ans = [fucomp.best_answer(message.text, fucomp.message_base_m)]
    bot.reply_to(message, random.choice(ans), disable_web_page_preview=True, disable_notification=True)


@bot.message_handler(func=lambda m: random.randrange(100) < 20 and m.text.endswith('?') and len(m.text) > 35)
def random_answer(message):
    response = chat_gpt.ask(message.text)
    if response:
        bot.reply_to(message, response, disable_web_page_preview=True, disable_notification=True)

if __name__ == '__main__':  # pragma: no cover
    # bot.remove_webhook()
    bot.polling(none_stop=True)
