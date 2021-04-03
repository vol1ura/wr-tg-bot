import matplotlib.pyplot as plt
import pandas as pd
import re
import requests
from lxml.html import parse, fromstring

parkrun_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}

club_link = '[Установи в профиле клуб Wake&Run, перейдя по ссылке](https://www.parkrun.com/profile/groups#id=23212&q=Wake%26Run)'


def add_volunteers(start, stop):
    url = 'https://www.parkrun.ru/kuzminki/results/weeklyresults/?runSeqNumber='
    parkrun_number = start
    while parkrun_number <= stop:
        result = requests.get(url + str(parkrun_number), headers=parkrun_headers, stream=True)
        result.raw.decode_content = True
        tree = parse(result.raw)
        volunteers = tree.xpath('//*[@class="paddedt left"]/p[1]/a')
        with open('static/kuzminki_full_stat.txt', 'a') as f:
            for volunteer in volunteers:
                volunteer_name = volunteer.text_content()
                volunteer_id = re.search(r'\d+', volunteer.attrib['href'])[0]
                f.write(f'kuzminki\t{parkrun_number}\tA{volunteer_id} {volunteer_name}\n')
        parkrun_number += 1


def get_volunteers():
    url = f'https://www.parkrun.ru/kuzminki/results/latestresults/'
    result = requests.get(url, headers=parkrun_headers, stream=True)
    result.raw.decode_content = True
    tree = parse(result.raw)
    parkrun_number = int(tree.xpath('//div[@class="Results"]/div/h3/span[3]/text()')[0][1:])
    with open('static/kuzminki_full_stat.txt', 'r') as f:
        all_stat = f.readlines()
    last_parkrun_db = int(all_stat[-2].split()[1])
    if last_parkrun_db < parkrun_number:
        add_volunteers(last_parkrun_db + 1, parkrun_number)
        with open('static/kuzminki_full_stat.txt', 'r') as f:
            all_stat = f.readlines()
    volunteers = {}
    for line in all_stat:
        name = line.split(maxsplit=3)[-1].strip()
        volunteers[name] = volunteers.setdefault(name, 0) + 1

    top_volunteers = sorted(volunteers.items(), key=lambda v: v[1], reverse=True)[:10]
    result = '*Toп 10 волонтёров parkrun Kuzminki*\n'
    for i, volunteer in enumerate(top_volunteers, 1):
        result += f'{i}. {volunteer[0]} | {volunteer[1]}\n'

    return result.strip()


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


def get_club_table():
    url = 'https://www.parkrun.ru/kuzminki/results/clubhistory/?clubNum=23212'
    page_all_results = requests.get(url, headers=parkrun_headers)
    data = pd.read_html(page_all_results.text)[0]
    data.drop(data.columns[[1, 5, 9, 12]], axis=1, inplace=True)
    return data


def get_kuzminki_fans():
    data = get_club_table()
    data.rename(columns={data.columns[0][0]: 'Участник', data.columns[0][1]: 'W&R'}, inplace=True)
    table = data.drop(data.iloc[:, 1:7], axis=1).\
        drop(data.columns[8], axis=1).\
        sort_values(by=[data.columns[7]], ascending=False).\
        reset_index(drop=True).head(10)
    sportsmens = table[table.columns[0]]
    pr_num = table[table.columns[1]]
    message = 'Наибольшее количество забегов _в Кузьминках_:\n'
    for i, (name, num) in enumerate(zip(sportsmens, pr_num), 1):
        message += f'{i:>2}.\xa0{name:<20}\xa0*{num:<3}*\n'
    return message.rstrip()


def get_wr_purkruners():
    data = get_club_table()
    data.rename(columns={data.columns[0][0]: 'Участник', data.columns[0][1]: 'W&R'}, inplace=True)
    table = data.drop(data.iloc[:, 1:8], axis=1).\
        sort_values(by=[data.columns[8]], ascending=False).\
        reset_index(drop=True).\
        head(10)
    sportsmens = table[table.columns[0]]
    pr_num = table[table.columns[1]]
    message = 'Рейтинг одноклубников _по количеству паркранов_:\n'
    for i, (name, num) in enumerate(zip(sportsmens, pr_num), 1):
        message += f'{i:>2}.\xa0{name:<20}\xa0*{num:<3}*\n'
    return message.rstrip()


def get_kuzminki_top_results():
    data = get_club_table()
    data.rename(columns={data.columns[0][0]: 'Участник', data.columns[0][1]: 'W&R'}, inplace=True)
    table = data.drop(data.iloc[:, 2:], axis=1).sort_values(by=[data.columns[1]]).reset_index(drop=True).head(10)
    sportsmens = table[table.columns[0]]
    result = table[table.columns[1]]
    message = 'Самые быстрые одноклубники _на паркране Кузьминки_:\n'
    for i, (name, num) in enumerate(zip(sportsmens, result), 1):
        message += f'{i:>2}.\xa0{name:<20}\xa0*{num:<3}*\n'
    return message.rstrip()


def most_slow_parkruns():
    url = 'https://www.parkrun.ru/results/courserecords/'
    page_all_results = requests.get(url, headers=parkrun_headers)
    data = pd.read_html(page_all_results.text)[0]
    data.drop(data.columns[[1, 5]], axis=1, inplace=True)
    data.rename(columns={data.columns[0][0]: 'Parkrun'}, inplace=True)
    table = data.drop(data.iloc[:, 1:5], axis=1)\
        .drop(data.columns[6], axis=1)\
        .sort_values(by=[data.columns[5]], ascending=False)\
        .reset_index(drop=True)\
        .head(10)
    parkrun = table[table.columns[0]]
    result = table[table.columns[1]]
    message = '*10 самых медленных паркранов:*\n'
    for i, (name, num) in enumerate(zip(parkrun, result), 1):
        message += f'{i:>2}.\xa0{name:<25}\xa0*{num:<3}*\n'
    return message.rstrip()


def make_latest_results_diagram(pic: str):
    url = f'https://www.parkrun.ru/kuzminki/results/latestresults/'
    page_all_results = requests.get(url, headers=parkrun_headers)
    html_page = page_all_results.text
    tree = fromstring(html_page)
    parkrun_date = tree.xpath('//span[@class="format-date"]/text()')[0]
    data = pd.read_html(html_page)[0]
    data = data.dropna(thresh=3)
    data[data.columns[5]] = data[data.columns[5]].dropna().transform(lambda s: re.search(r'^(\d:)?\d\d:\d\d', s)[0])
    plt.figure(figsize=(16, 7))
    ax = data['Время'] \
        .transform(lambda time: sum(x * int(t) for x, t in zip([1 / 60, 1, 60], time.split(':')[::-1]))) \
        .hist(bins=32, color='darkolivegreen')
    ax.set_xlabel("Результаты участников (минуты)", size=12)
    ax.set_ylabel("Результатов в диапазоне", size=12)
    plt.title(f'Результаты паркрана Кузьминки {parkrun_date}', size=16)
    plt.savefig(pic)
    return open(pic, 'rb')


def make_clubs_bar(pic: str):
    url = f'https://www.parkrun.ru/kuzminki/results/latestresults/'
    page_all_results = requests.get(url, headers=parkrun_headers)
    html_page = page_all_results.text
    tree = fromstring(html_page)
    parkrun_date = tree.xpath('//span[@class="format-date"]/text()')[0]
    data = pd.read_html(html_page)[0]
    data = data.dropna(thresh=3)

    clubs = data['Клуб'].value_counts()
    x = clubs.index
    colors = [('blueviolet' if item == 'Wake&Run' else 'darkkhaki') for item in x]
    plt.figure(figsize=(16, 7))
    plt.xticks(rotation=20)
    plt.bar(x, clubs.values, color=colors)
    plt.title(f'Количество участников из клубов на паркране Кузьминки {parkrun_date}', size=16)
    plt.savefig(pic)
    return open(pic, 'rb')


if __name__ == '__main__':
    # mes = get_participants()
    # mes = most_slow_parkruns()
    # print(mes)
    # get_latest_results_diagram()
    # make_latest_results_diagram('../utils/results.png').close()
    # add_volunteers(204, 204)
    make_clubs_bar('../utils/clubs.png').close()
