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
    def __make_mark(club_name: str) -> str:
        return club_name if len(club_name) < 20 else f'{club_name[:18]}...'

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
        data['mark'] = [self.__make_mark(club) for club in data['Club'].values]
        df = data.sort_values(by=['Dist'], ascending=False).reset_index(drop=True).head(10)
        clubs = df['mark']
        vals = [df['Dist'].values, df['Users'].values, df['Dist'].values / df['Users'].values]
        colors = ['#1f77b4', '#ff7f0e', '#bcbd22']
        ylabels = ['Σ, км', 'участников', 'км/чел']
        fig, axs = plt.subplots(3, 1, sharex=True, figsize=(9,16), dpi=300)
        plt.xticks(rotation=70, fontsize=14)
        for ax, val, color, ylabel in zip(axs, vals, colors, ylabels):
            ax.bar(clubs, height=val, color=color)
            ax.set_ylabel(ylabel, fontsize=16, fontweight='bold')
            ax.set_facecolor('0.85')
            for p, label, mark in zip(ax.patches, val, clubs.values):
                if 'Wake&Run' in mark:
                    p.set_facecolor('#9467bd')
                ax.annotate(round(label), (p.get_x()+p.get_width()/2, p.get_height()),
                    va='top', ha='center', fontsize=14, color='white', fontweight='bold')
        axs[0].set_title('Top10 клубов в турнире IMPULSE', fontsize=16, fontweight='bold')
        plt.tight_layout()
        fig.subplots_adjust(hspace=0)
        plt.savefig(pic)
        return open(pic, 'rb')
