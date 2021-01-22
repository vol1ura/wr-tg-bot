import re
import requests
from lxml.html import parse


top_volunteers = """Toп 10 волонтёров parkrun Kuzminki
1. Максим СИЛАЕВ | 156
2. Янчик КРЖИЖАНОВСКАЯ | 125
3. Александр ЩЁЛОКОВ | 119
4. Ольга АКИМОВА | 100
5. Наталия ДУЛЕБЕНЕЦ | 92
6. Андрей ЛЕТУНОВСКИЙ | 84
7. Оксана ГАМЗИНА | 71
8. Анастасия КАЗАНЦЕВА | 69
9. Сергей КОТЛОВ | 58
10. Альфия ЗАЙНУТДИНОВА | 55"""


def get_participants():
    headers = {"Accept": "text/html",
               "Accept-Encoding": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
               "Cache-Control": "max-age=0",
               "Connection": "keep-alive",
               "Host": "www.parkrun.com",
               "Referer": "https://www.parkrun.ru/",
               "Sec-GPC": "1",
               "TE": "Trailers",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
               }
    result = requests.get('https://www.parkrun.com/results/consolidatedclub/?clubNum=23212',
                          headers=headers, stream=True)
    result.raw.decode_content = True
    tree = parse(result.raw)
    head = tree.xpath('//div[@class="floatleft"]/p')[0].text_content()
    data = re.search(r'(\d{4}-\d{2}-\d{2}). Of a total (\d+) members, (\d+) took part', head)
    places = tree.xpath('//div[@class="floatleft"]/h2')
    links_to_results = tree.xpath('//div[@class="floatleft"]/p/a/@href')[1:-1]
    message = f'Паркраны, где побывали наши одноклубники {data.group(1)}:\n'
    for i, (p, l) in enumerate(zip(places, links_to_results), 1):
        p_num = re.search(r'runSeqNumber=(\d+)', l).group(1)
        message += f'{i}. [{p.text_content().strip()}\xa0№{p_num}]({l})\n'
    message += f'\nУчаствовало {data.group(3)} из {data.group(2)} чел.'
    return message


def get_club():
    # headers = {"Accept": "text/html",
    #            "Accept-Encoding": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    #            "Cache-Control": "max-age=0",
    #            "Connection": "keep-alive",
    #            "Host": "www.parkrun.com",
    #            "Sec-GPC": "1",
    #            "TE": "Trailers",
    #            "Upgrade-Insecure-Requests": "1",
    #            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    #            }
    # session = requests.Session()
    # result = session.get('https://www.parkrun.ru/groups/23212/', headers=headers)#, stream=True)
    return '[Установи в профиле клуб Wake&Run, перейдя по ссылке](https://www.parkrun.com/profile/groups#id=23212&q=Wake%26Run)'
    # result.raw.decode_content = True
    # tree = parse(result.raw)
    # with open('parkrun1.html', 'w') as f:
    #     f.write(result.text)
    # n = tree.xpath('//div[@id="vue-public-group"]/p')
    # print(n)

# https://www.parkrun.ru/results/courserecords/


if __name__ == '__main__':
    # mes = get_participants()
    mes = get_club()
    print(mes)
