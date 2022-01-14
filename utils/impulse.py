import matplotlib.pyplot as plt
import pandas as pd
import requests

IMPULSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://ihaveimpulse.run',
    'Referer': 'https://ihaveimpulse.run/clubs'
}


def get_tournament_table():
    url = 'https://ihaveimpulse.run/scripts/ajax.php'
    page_all_results = requests.post(url,
        data={'func': 'get_Clubs_Year', 'json_v': [{'arg': {'Week': '02','Year': '2022'}}]},
        headers=IMPULSE_HEADERS)
    club_results = page_all_results.json()[2]
    columns = {
        'Club': [result['Name_Club'] for result in club_results],
        'Dist': [result['Dist_Sum'] for result in club_results],
        'Users': [result['Count_User'] for result in club_results]
    }
    return pd.DataFrame(columns)


def make_clubs_bar(pic: str):
    data = get_tournament_table()
    df = data.sort_values(by=[data.columns[1]], ascending=False).reset_index(drop=True).head(10)
    clubs = df[data.columns[0]]
    vals = df[data.columns[1]].values

    fig = plt.figure(figsize=(6, 6), dpi=150)
    ax = fig.add_subplot()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#17ceaf']
    plt.xticks(rotation=70)
    plt.bar(clubs, height=vals, color=colors)
    for p, label, mark in zip(ax.patches, vals, clubs.values):
        if mark == 'Wake&Run':
            p.set_facecolor('#9467bd')
        ax.annotate(round(label), (p.get_x()+0.05, p.get_height()), va='bottom')
    plt.title('Top10 клубов в турнире IMPULSE', fontweight='bold')
    plt.tight_layout()
    plt.savefig(pic)
    return open(pic, 'rb')
