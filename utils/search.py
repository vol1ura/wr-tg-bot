# https://cse.google.com/cse/all
import os
import random
import re
import urllib.parse
from lxml.html import parse

import requests


def google(phrase):
    search_phrase = re.sub(r'(?i)бот|\.|,|!', '', phrase).strip()
    params = {
        "q": f"{search_phrase}",
        "key": f"{os.environ.get('GOOGLE_API_KEY')}",
        "cx": f"{os.environ.get('GOOGLE_CX')}"
    }
    values_url = urllib.parse.urlencode(params)
    result = requests.get(f'https://www.googleapis.com/customsearch/v1?{values_url}')
    try:
        res1 = random.choice(result.json()['items'])['htmlSnippet']
    except(KeyError, TypeError):
        return ''
    res2 = re.sub(r'(?im)<b>|</b>|\.\.\.|<br>|&nbsp;|&quot;|\n', '', res1)
    res3 = re.sub(r'Марафорум - форум о любительском беге, тренировках,( соревнованиях.)?', '', res2, re.MULTILINE)
    res4 = re.sub(r' Сейчас этот раздел просматривают:.*', '.', res3, re.MULTILINE)
    res5 = re.sub(r'Сообщение Добавлено: \w{,2} \d{,2} \w+ \d{2,4}, \d\d:\d\d', '', res4)
    res6 = re.sub(r'\d{1,2} \w+ \d{2,4}|\d\d\.\d\d\.\d{4} \d\d:\d\d', '', res5)
    res7 = re.sub(r'Марафорум|» Соревнования|» Кроссы, трейлы\.|Часовой пояс:|UTC\.|Кто сейчас на форуме\.*', '', res6)
    res8 = re.sub(r'Последний раз редактировалось .*, \d\d:\d\d, всего', '', res7)
    res9 = re.sub(r'Клубные дела IRC|»|Обсуждение клубных дел IRC|irc', '', res8, re.I)
    return re.sub(r'[,.!?][\w ]+$', '.', res9.strip(), re.MULTILINE)


def bashim(phrase):
    search_phrase = re.sub(r'(?i)\bбот\b|\.|,|!|\?', '', phrase).strip()
    params = {
        "text": f"{search_phrase}"
    }
    values_url = urllib.parse.urlencode(params)
    result = requests.get(f'https://bash.im/search?{values_url}', stream=True)
    result.raw.decode_content = True
    tree = parse(result.raw)
    cites = tree.xpath('//article/div/div')
    if cites:
        for cite in cites:
            cite = re.split(r'[\w. ]+?:', re.sub(r'\n', '', cite.text_content()))
            [cite.remove(s) for s in list(cite) if s == '']
            print(f'"{cite[0].strip()}",')
    return ''
