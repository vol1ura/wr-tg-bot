"""
ImpulseChallenge
----------------
Supply statistics about Impulse 2022 running challenge
"""
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests


class ImpulseChallenge:
    """
    See https://ihaveimpulse.run/clubs
    """
    __CLUBS_URL = 'https://ihaveimpulse.run/scripts/ajax.php'
    __HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://ihaveimpulse.run',
        'Referer': 'https://ihaveimpulse.run/clubs'
    }
    __COLORS = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#17ceaf'
    ]

    @staticmethod
    def __get_payload(date: datetime.date) -> dict:
        return {
            'func': 'get_Clubs_Year',
            'json_v': [{'arg': {'Week': date.strftime('%V'), 'Year': date.strftime('%Y')}}]
        }

    def __get_tournament_table(self) -> pd.DataFrame:
        payload = self.__get_payload(datetime.date.today())
        page_all_results = requests.post(self.__CLUBS_URL, data=payload, headers=self.__HEADERS)
        club_results = page_all_results.json()[2]
        columns = {
            'Club': [result['Name_Club'] for result in club_results],
            'Dist': [result['Dist_Sum'] for result in club_results],
            'Users': [result['Count_User'] for result in club_results]
        }
        return pd.DataFrame(columns)

    @staticmethod
    def __make_mark(club_name: str, club_users: int) -> str:
        trimmed_club_name = club_name if len(club_name) < 20 else f'{club_name[:18]}...'
        return f'{trimmed_club_name}\n{club_users} участников'

    def make_clubs_bar(self, pic: str):
        """Create bar diagram with Top10 clubs for current moment.

        Parameters
        ----------
        `pic` : str
            Name of file to save diagram

        Returns
        -------
        BufferedReader
            File object with binary data (`png` picture)
        """
        data = self.__get_tournament_table()
        data['mark'] = [self.__make_mark(row.Club, row.Users) for row in data.loc[:, ['Club', 'Users']].itertuples()]
        df = data.sort_values(by=['Dist'], ascending=False).reset_index(
            drop=True).head(10)
        clubs = df['mark']
        vals = df['Dist'].values
        fig = plt.figure(figsize=(6, 6), dpi=150)
        ax = fig.add_subplot()
        plt.xticks(rotation=70)
        plt.bar(clubs, height=vals, color=self.__COLORS)
        for p, label, mark in zip(ax.patches, vals, clubs.values):
            if 'Wake&Run' in mark:
                p.set_facecolor('#9467bd')
            ax.annotate(round(label), (p.get_x() + 0.05, p.get_height()), va='bottom')
        plt.title('Top10 клубов в турнире IMPULSE', fontweight='bold')
        plt.tight_layout()
        plt.savefig(pic)
        return open(pic, 'rb')
