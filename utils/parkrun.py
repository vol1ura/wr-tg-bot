import pandas as pd
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

parkrun_headers = {"Accept": "text/html",
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


def get_participants():
    result = requests.get('https://www.parkrun.com/results/consolidatedclub/?clubNum=23212',
                          headers=parkrun_headers, stream=True)
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


def get_kuzminki_fans():
    url = 'https://www.parkrun.ru/kuzminki/results/clubhistory/?clubNum=23212'
    page_all_results = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'})
    data = pd.read_html(page_all_results.text)[0]
    data.drop(data.columns[[1, 5, 9, 12]], axis=1, inplace=True)
    data.rename(columns={data.columns[0][0]: 'Участник', data.columns[0][1]: 'W&R'}, inplace=True)
    table = data.drop(data.iloc[:, 1:7], axis=1).\
        drop(data.columns[8], axis=1).\
        sort_values(by=[data.columns[7]], ascending=False).\
        reset_index(drop=True).head(10)
    sportsmens = table[table.columns[0]]
    pr_num = table[table.columns[1]]
    message = 'Наибольшее количество забегов *в Кузьминках*:\n'
    for i, (name, num) in enumerate(zip(sportsmens, pr_num), 1):
        message += f'{i:>2}.\xa0{name:<20}\xa0*{num:<3}*\n'
    return message.rstrip()


def get_wr_purkruners():
    url = 'https://www.parkrun.ru/kuzminki/results/clubhistory/?clubNum=23212'
    page_all_results = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'})
    data = pd.read_html(page_all_results.text)[0]
    data.drop(data.columns[[1, 5, 9, 12]], axis=1, inplace=True)
    data.rename(columns={data.columns[0][0]: 'Участник', data.columns[0][1]: 'W&R'}, inplace=True)
    table = data.drop(data.iloc[:,1:8], axis=1).\
        sort_values(by=[data.columns[8]], ascending=False).\
        reset_index(drop=True).\
        head(10)
    sportsmens = table[table.columns[0]]
    pr_num = table[table.columns[1]]
    message = 'Рейтинг одноклубников по количеству паркранов:\n'
    for i, (name, num) in enumerate(zip(sportsmens, pr_num), 1):
        message += f'{i:>2}.\xa0{name:<20}\xa0*{num:<3}*\n'
    return message.rstrip()


def get_kuzminki_top_results():
    url = 'https://www.parkrun.ru/kuzminki/results/clubhistory/?clubNum=23212'
    page_all_results = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'})
    data = pd.read_html(page_all_results.text)[0]
    data.drop(data.columns[[1, 5, 9, 12]], axis=1, inplace=True)
    data.rename(columns={data.columns[0][0]: 'Участник', data.columns[0][1]: 'W&R'}, inplace=True)
    table = data.drop(data.iloc[:,2:], axis=1).sort_values(by=[data.columns[1]]).reset_index(drop=True).head(10)
    sportsmens = table[table.columns[0]]
    pr_num = table[table.columns[1]]
    message = 'Самые быстрые одноклубники _на паркране Кузьминки_:\n'
    for i, (name, num) in enumerate(zip(sportsmens, pr_num), 1):
        message += f'{i:>2}.\xa0{name:<20}\xa0*{num:<3}*\n'
    return message.rstrip()


def get_club():
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
    mes = get_kuzminki_top_results()
    print(mes)
