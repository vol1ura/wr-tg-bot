import re
from fuzzywuzzy import process, fuzz
import pickle


def compare(user_phrase, dictionary: list) -> bool:
    return process.extractOne(user_phrase, dictionary)[1] >= 70


def bot_compare(user_phrase, dictionary: list) -> bool:
    accost_bot = re.compile(r'(?i)\bбот\b')
    user_str = str(user_phrase)
    if accost_bot.search(user_str):
        return process.extractOne(accost_bot.sub('', user_str), dictionary, scorer=fuzz.token_sort_ratio)[1] >= 70
    else:
        return False


def best_answer(user_phrase, dictionary: list) -> str:
    return process.extractOne(re.sub(r'(?i)\bбот\b,?', '', user_phrase).strip(), dictionary,
                              scorer=fuzz.token_set_ratio)[0]


# ======================= DICTIONARIES TO COMPARE =======================================================
phrases_instagram = [
    'инстаграм бег', 'instagram', 'пишут спортсмены', 'пишут спортивные каналы', 'статья о беге',
    'новость бег', 'последн публикаци', 'беговой блог', 'новость в каналах', 'новости спорта'
]

phrases_admin = [
    'админ', 'тут главный в чате', 'админ чата', 'администратор', 'кто начальник чата', 'контакт админа',
    "позови админа", 'модератор', "модератор чата"
]

phrases_social = [
    'соцсети клуба', 'ссылки на клуб', 'клуб в интернете', 'информация о клубе', 'клуб в vk', "клуб в фейсбук",
    'клуб в страве'
]

phrases_weather = [
    'погода на улице', 'информация о погоде', 'прогноз погоды', "какая погода"
]

phrases_parkrun = [
    "расскажи о паркран", "новости о паркран", "что известно о паркран", "когда откроют паркран"
]

phrases_schedule = [
    "расписание", "тренировки клуба", "четверговые", "длительная тренировка", "расписание тренировок",
    "когда тренировка"
]

petristchev = [
    "Одна семья - одна команда", "А Петрищев молодец - марафон за 2:50:40. Так-то!", "Петрищев... хм )))",
    "Куда пропал этот парень? Максим Петрищев из Wake&Run с надписью на футболке) веселый!!!",
    "Помню, помню, было эпично - Петрищев в трусах с топором в Кузминках... а с другой стороны Моторный "
    "в зеленых лосинах... это невозможно развидеть.", "Петрищев в трусах - это вообще святое!",
    "Всё жду, когда мой друг Максим Петрищев - чемпион - будет волонтером в Кузьминках",
    "Почему Петрищев часто бывает девочкой на забегах? 😃 Всё дело в перерегистрации!!!", "Сложно, если ты не Петрищев",
    "Петрищев вообще когда нибудь пешком ходит?😅", "А как бежит Петрищев хз",
    "Петрищев одно время больше всех кричал, что никогда трейлы бегать не будет, и где он теперь???",
    "Петрищев всегда с нами! 🔥🔥🔥", "Куролесит у нас Петрищев)))", "Голый Петрищев великолепен!!!"
]

with open('utils/message_base_wr.pkl', 'rb') as f:
    message_base_wr = pickle.load(f)

with open('utils/message_base_meschch.pkl', 'rb') as f:
    message_base_m = pickle.load(f)

message_base_wr += petristchev

# ===================== TESTING =============================
if __name__ == '__main__':
    with open('message_base_wr.pkl', 'rb') as f:
        message_base_wr = pickle.load(f)
    print(best_answer('бот, знаешь девиз?', message_base_wr))

    phrase1 = 'бот, покажи статью о беге'
    phrase2 = 'Бот, позови администратора'
    phrase3 = 'Бот, покажи ссылки на клуб'
    phrase4 = 'бот, когда откроют паркраны?'
    test_phrases = [phrase1, phrase2, phrase3, phrase4]

    compare1 = list(map(lambda p: bot_compare(p, phrases_instagram), test_phrases))
    compare2 = list(map(lambda p: bot_compare(p, phrases_admin), test_phrases))
    compare3 = list(map(lambda p: bot_compare(p, phrases_social), test_phrases))
    compare4 = list(map(lambda p: bot_compare(p, phrases_parkrun), test_phrases))

    print(compare1)
    print(compare2)
    print(compare3)
    print(compare4)
