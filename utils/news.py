import re
import time

import requests
from lxml.html import parse


def get_competitions(month, year):
    payload = f'year={year}&mes={month}&distselect=000&oblselect=000&fedselect=%D6%E5%ED%F2%F0&' \
              f'%F1select=%D0%EE%F1%F1%E8%FF&datenum=000&datemon=000&np=YES&' \
              f'fedokr=&countr=&Vidp=0&oblsubmit=%E2%FB%E1%F0%E0%F2%FC'
    headers = {"Accept": "text/html",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "ru-RU",
               "Connection": "keep-alive",
               "Content-Type": "application/x-www-form-urlencoded",
               "Cookie": "hotlog=1",
               "Host": "probeg.org",
               "Origin": "https://probeg.org",
               "Referer": "https://probeg.org/kalend/kalend.php",
               "Sec-GPC": "1",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
               }
    result = requests.post('https://probeg.org/kalend/kalend.php', data=payload, headers=headers, stream=True)
    result.raw.decode_content = True
    tree = parse(result.raw)
    rows = tree.xpath('//table[@class="textU"]/tr')[1:]
    competitions = []
    from_date = time.localtime(time.time()).tm_mday
    for row in rows:
        cells = row.xpath('.//td')
        when = cells[2].text_content().strip()
        day = int(when[:2])
        if day < from_date:
            continue
        where = cells[1].text_content()
        if 'отменен' in where.lower() or 'Воронеж' in where or 'Рязань' in where or 'Смоленск' in where or \
                'Костром' in where or 'Калуж' in where:
            continue
        kontacts = cells[5].text_content()
        if 'Скоблина' in kontacts or 'alleviate@yandex' in kontacts:
            continue
        title = cells[0].text_content().strip()
        url = cells[0].xpath('.//b/a/@href')[0].strip()
        dist = ', '.join(re.findall(r'\d+ [а-я]+', cells[3].text_content()))
        description = f'✏️<a href="{url}">{title}</a>' \
                      f'\n🕒\xa0<b>Дата</b>: {when}\xa0| 📌\xa0{where}' \
                      f'\n➡️ <b>Дистанции</b>: {dist}'
        competitions.append((title, when, description))
    return competitions


if __name__ == '__main__':
    a = get_competitions(1, 2021)
    # print(a)
