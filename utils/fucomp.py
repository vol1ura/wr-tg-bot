import re
from fuzzywuzzy import process, fuzz


def compare(user_phrase, dictionary: list) -> bool:
    return process.extractOne(user_phrase, dictionary)[1] >= 70


def bot_compare(user_phrase, dictionary: list) -> bool:
    accost_bot = re.compile(r'\bбот\b', re.I)
    user_str = str(user_phrase)
    if accost_bot.search(user_str):
        return process.extractOne(accost_bot.sub('', user_str), dictionary, scorer=fuzz.token_sort_ratio)[1] >= 70
    else:
        return False


# ======================= DICTIONARIES TO COMPARE =======================================================
phrases_instagram = [
    'инстаграм бег', 'instagram', 'пишут спортсмены', 'пишут спортивные каналы', 'статья о беге',
    'новость бег', 'последн публикаци', 'беговой блог', 'новость в каналах', 'новости спорта'
]

phrases_admin = [
    'админ', 'тут главный в чате', 'админ чата', 'администратор', 'кто начальник чата', 'контакт админа',
    "позови админа"
]

phrases_social = [
    'соцсети клуба', 'ссылки на клуб', 'клуб в интернете', 'информация о клубе', 'клуб в vk', "клуб в фейсбук",
    'клуб в страве'
]

phrases_weather = [
    'погода на улице', 'информация о погоде', 'прогноз погоды'
]

phrases_to_run = [
    'где бегать', 'бег на улице', 'хочу побегать', 'с кем бегать', "можно бегать", "тренировка на улице"
]

phrases_parkrun = [
    "расскажи о паркран", "новости о паркран", "что известно о паркран", "когда откроют паркран"
]

phrases_schedule = [
    "расписание", "тренировки клуба", "четверговые", "длительная тренировка"
]

# ===================== TESTING =============================
if __name__ == '__main__':
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
