
import bs4
import pandas as pd
import numpy as np


class PageParser:
    def __init__(self, file_path):
        self.file_path = file_path

        with open(self.file_path, 'r') as p:
            self.file_soup = bs4.BeautifulSoup(p.read(), 'html.parser')

    def get_bearish_tech_events(self):
        return self.__extract_bull_or_bear_table('bear')

    def get_bullish_tech_event(self):
        return self.__extract_bull_or_bear_table('bull')

    def __extract_bull_or_bear_table(self, type):

        # Find the tbody of the table for given type
        tbody = self.file_soup.find('div', class_=type).findChild('table').findChild("tbody")

        # Extract the rows for this table
        rows = tbody.find_all('td', {"scope": "row"})


        tickers = []
        link_ids = []

        for i, r in enumerate(rows):
            # If even row, extract ticker symbol
            if i % 2 == 0:
                for j in r.find_all('span', recursive=False):
                    tickers.append(j['fmr-param-symbol'])
            # If odd row, extract link to data
            else:
                for j in r.find_all('a', recursive=False):
                    link_ids.append(f'{j["id"]}-content')

        for id in link_ids:
            self.__tech_event_table_extraction_helper(id)

        table = np.empty([len(tickers), 3])
        df = pd.DataFrame(
            table,
            columns=['Ticker','Price','Something'],
            index=tickers
        )

        # print(df)


        return 0

    def __tech_event_table_extraction_helper(self, id):
        thing = self.file_soup.find('div', attrs={"id": id})
        print(thing)