import re
import time
from datetime import date, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import requests
from lxml.html import parse, fromstring
from matplotlib.colors import Normalize
from matplotlib.ticker import MultipleLocator
from urllib.parse import urlencode

parkrun_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"}

CLUB_NAME = 'Wake&Run'
CLUB_ID = 23212
CLUB_LINK = f"https://www.parkrun.com/profile/groups#{urlencode({'id': CLUB_ID, 'q': CLUB_NAME})}"
CLUB_INFO = f'[Установи в профиле клуб Wake&Run, перейдя по ссылке]({CLUB_LINK})'
VOLUNTEERS_FILE = 'static/kuzminki_full_stat.txt'


def get_html_tree(url):
    result = requests.get(url, headers=parkrun_headers, stream=True)
    result.raw.decode_content = True
    return parse(result.raw)


def add_volunteers(start, stop):
    url = 'https://www.parkrun.ru/kuzminki/results/weeklyresults/?runSeqNumber='
    for parkrun_number in range(start, stop+1):
        time.sleep(1.11)
        tree = get_html_tree(url + str(parkrun_number))
        volunteers = tree.xpath('//*[@class="paddedt left"]/p[1]/a')
        with open(VOLUNTEERS_FILE, 'a') as f:
            for volunteer in volunteers:
                volunteer_name = volunteer.text_content()
                volunteer_id = re.search(r'\d+', volunteer.attrib['href'])[0]
                f.write(f'kuzminki\t{parkrun_number}\tA{volunteer_id} {volunteer_name}\n')


def get_volunteers():
    url = 'https://www.parkrun.ru/kuzminki/results/latestresults/'
    tree = get_html_tree(url)
    parkrun_number = int(tree.xpath('//div[@class="Results"]/div/h3/span[3]/text()')[0][1:])
    with open(VOLUNTEERS_FILE) as f:
        all_stat = f.readlines()
    last_parkrun_db = int(all_stat[-2].split()[1])
    if last_parkrun_db < parkrun_number:
        add_volunteers(last_parkrun_db + 1, parkrun_number)
        with open(VOLUNTEERS_FILE) as f:
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
    tree = get_html_tree('https://www.parkrun.com/results/consolidatedclub/?clubNum=23212')
    head = tree.xpath('//div[@class="floatleft"]/p')[0].text_content()
    data = re.search(r'(\d{4}-\d{2}-\d{2}). Of a total (\d+) members', head)
    info_date = date.fromisoformat(data.group(1))
    message = add_relevance_notification(info_date)
    places = tree.xpath('//div[@class="floatleft"]/h2')
    results_tables = tree.xpath('//table[contains(@id, "results")]')
    counts = [len(table.xpath('.//tr/td[4]//*[not(contains(text(), "Unattached"))]')) for table in results_tables]
    links_to_results = tree.xpath('//div[@class="floatleft"]/p/a/@href')[1:-1]
    message += f'Паркраны, где побывали наши одноклубники {data.group(1)}:\n'
    for i, (p, l, count) in enumerate(zip(places, links_to_results, counts), 1):
        p_num = re.search(r'runSeqNumber=(\d+)', l).group(1)
        message += f"{i}. [{re.sub('parkrun', '', p.text_content()).strip()}\xa0№{p_num}]({l}) ({count}\xa0чел.)\n"
    message += f'\nУчаствовало {sum(counts)} из {data.group(2)} чел.'
    return message


def add_relevance_notification(content_date: date) -> str:
    notification = 'Извините, но результаты в системе parkrun ещё не обновились 😿 ' \
                   'Всё, что могу предложить на данный момент - результаты за прошлую неделю.\n'
    return notification if date.today() > content_date + timedelta(6) else ''


def get_club_table():
    url = 'https://www.parkrun.ru/kuzminki/results/clubhistory/?clubNum=23212'
    page_all_results = requests.get(url, headers=parkrun_headers)
    data = pd.read_html(page_all_results.text)[0]
    data.drop(data.columns[[1, 5, 9, 12]], axis=1, inplace=True)
    return data


def get_kuzminki_fans():
    data = get_club_table()
    table = data.sort_values(by=[data.columns[7]], ascending=False).head(10)
    sportsmens = table[table.columns[0]]
    pr_num = table[table.columns[7]]
    message = 'Наибольшее количество забегов _в Кузьминках_:\n'
    for i, (name, num) in enumerate(zip(sportsmens, pr_num), 1):
        message += f'{i:>2}.\xa0{name:<20}\xa0*{num}*\n'
    return message.rstrip()


def get_wr_parkruners():
    data = get_club_table()
    table = data.sort_values(by=[data.columns[8]], ascending=False).head(10)
    sportsmens = table[table.columns[0]]
    pr_num = table[table.columns[8]]
    message = 'Рейтинг одноклубников _по количеству паркранов_:\n'
    for i, (name, num) in enumerate(zip(sportsmens, pr_num), 1):
        message += f'{i:>2}.\xa0{name:<20}\xa0*{num:<3}*\n'
    return message.rstrip()


def get_kuzminki_top_results():
    data = get_club_table()
    table = data.sort_values(by=[data.columns[1]]).head(10)
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
    table = data.sort_values(by=[data.columns[7]], ascending=False).head(10)
    parkrun = table[table.columns[0]]
    result = table[table.columns[7]]
    message = '*10 самых медленных паркранов:*\n'
    for i, (name, num) in enumerate(zip(parkrun, result), 1):
        message += f'{i:>2}.\xa0{name:<25}\xa0*{num:<3}*\n'
    return message.rstrip()


def get_latest_results_df():
    url = 'https://www.parkrun.ru/kuzminki/results/latestresults/'
    page_all_results = requests.get(url, headers=parkrun_headers)
    html_page = page_all_results.text
    tree = fromstring(html_page)
    parkrun_date = tree.xpath('//span[@class="format-date"]/text()')[0]
    df = pd.read_html(html_page)[0]
    number_runners = len(df)
    df = df.dropna(thresh=3)
    df['Время'] = df['Время'].dropna() \
        .transform(lambda s: re.search(r'^(\d:)?\d\d:\d\d', s)[0]) \
        .transform(time_to_float)
    return df, number_runners, parkrun_date


def make_latest_results_diagram(pic: str, name=None, turn=0):
    df, number_runners, parkrun_date = get_latest_results_df()

    plt.figure(figsize=(5.5, 4), dpi=300)
    ax = df['Время'].hist(bins=32, color='darkolivegreen')
    ptchs = ax.patches
    med = df['Время'].median()
    m_height = 0
    personal_y_mark = 0

    norm = Normalize(0, med)

    if name:
        personal_res = df[df['Участник'].str.contains(name.upper())].reset_index(drop=True)
        if personal_res.empty:
            raise AttributeError
        personal_name = re.search(r'([^\d]+)\d.*', personal_res["Участник"][0])[1]
        personal_name = ' '.join(n.capitalize() for n in personal_name.split())
        personal_time = personal_res['Время'][0]
    else:
        personal_time = 0
        personal_name = ''

    for ptch in ptchs:
        ptch_x = ptch.get_x()
        color = plt.cm.viridis(norm(med - abs(med - ptch_x)))
        ptch.set_facecolor(color)
        if ptch_x <= med:
            m_height = ptch.get_height() + 0.3
        if ptch_x <= personal_time:
            personal_y_mark = ptch.get_height() + 0.3

    med_message = f'Медиана {float_to_time(med)}'
    ax.annotate(med_message, (med - 0.5, m_height + 0.2), rotation=turn)
    plt.plot([med, med], [0, m_height], 'b')

    ldr_time = ptchs[0].get_x()
    ldr_y_mark = ptchs[0].get_height() + 0.3
    ldr_message = f'Лидер {float_to_time(ldr_time)}'
    ax.annotate(ldr_message, (ldr_time - 0.5, ldr_y_mark + 0.2), rotation=90)
    plt.plot([ldr_time, ldr_time], [0, ldr_y_mark], 'r')

    lst_time = ptchs[-1].get_x() + ptchs[-1].get_width()
    lst_y_mark = ptchs[-1].get_height() + 0.3
    ax.annotate(f'Всего участников {number_runners}', (lst_time - 0.5, lst_y_mark + 0.2), rotation=90)
    plt.plot([lst_time, lst_time], [0, lst_y_mark], 'r')

    if name and personal_time:
        ax.annotate(f'{personal_name}\n{float_to_time(personal_time)}',
                    (personal_time - 0.5, personal_y_mark + 0.2),
                    rotation=turn, color='red', size=12, fontweight='bold')
        plt.plot([personal_time, personal_time], [0, personal_y_mark], 'r')

    ax.set_xlabel("Результаты участников (минуты)")
    ax.set_ylabel("Результатов в диапазоне")
    plt.title(f'Результаты паркрана Кузьминки {parkrun_date}', size=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(pic)
    return open(pic, 'rb')


def make_clubs_bar(pic: str):
    df, _, parkrun_date = get_latest_results_df()

    clubs = df['Клуб'].value_counts()
    x = clubs.index
    colors = [('blueviolet' if item == 'Wake&Run' else 'darkkhaki') for item in x]

    fig = plt.figure(figsize=(6, 6), dpi=300)
    ax = fig.add_subplot()
    ax.grid(False, axis='x')
    ax.grid(True, axis='y')
    ax.yaxis.set_major_locator(MultipleLocator(base=2))
    plt.xticks(rotation=80, size=8)
    plt.bar(x, clubs.values, color=colors)
    plt.title(f'Клубы на паркране Кузьминки {parkrun_date}', size=14, fontweight='bold')
    plt.ylabel('Количество участников')
    plt.tight_layout()
    plt.savefig(pic)
    return open(pic, 'rb')


def time_to_float(h_mm_ss):
    return sum(x * float(t) for x, t in zip([1 / 60, 1, 60], h_mm_ss.split(':')[::-1]))


def float_to_time(mins):
    secs = round(mins * 60)
    return f'{secs // 60}:{secs % 60}'
