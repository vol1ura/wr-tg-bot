# https://cse.google.com/cse/all
import os
import random
import re
import urllib.parse
from lxml.html import parse
from pprint import pprint

import requests
from dotenv import load_dotenv


def google(phrase):
    search_prase = re.sub(r'бот|\.|,|!', '', phrase, re.I) + ' бег'
    params = {
        "q": f"{search_prase}",
        "key": f"{os.environ.get('GOOGLE_API_KEY')}",
        "cx": f"{os.environ.get('GOOGLE_CX')}"
    }
    values_url = urllib.parse.urlencode(params)
    result = requests.get(f'https://www.googleapis.com/customsearch/v1?' + values_url)
    try:
        res1 = random.choice(result.json()['items'])['htmlSnippet']
    except KeyError:
        return ''
    res2 = re.sub(r'(?im)<b>|</b>|\.\.\.|<br>|&nbsp;|&quot;|\n', '', res1)
    res3 = re.sub(r'Марафорум - форум о любительском беге, тренировках,( соревнованиях.)?', '', res2, re.MULTILINE)
    return re.sub(r'[,\.!?][\w ]+$', '.', res3.strip(), re.MULTILINE)


def bashim(phrase):
    search_prase = re.sub(r'бот|\.|,|!|\?', '', phrase, re.I).strip()
    params = {
        "text": f"{search_prase}"
    }
    values_url = urllib.parse.urlencode(params)
    result = requests.get(f'https://bash.im/search?' + values_url, stream=True)
    result.raw.decode_content = True
    tree = parse(result.raw)
    cites = tree.xpath('//article/div/div')
    if cites:
        for cite in cites:
            cite = re.split(r'[\w\. ]+?:', re.sub(r'\n', '', cite.text_content()))
            [cite.remove(s) for s in list(cite) if s == '']
            print(f'"{cite[0].strip()}",')
    return ''


if __name__ == '__main__':
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    s = bashim('бот, гречка')
    print(s)
