
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

        events_data = []
        for ticker, link_id in zip(tickers, link_ids):
            e_d = {'ticker': ticker, **self.__tech_event_table_extraction_helper(link_id)}
            events_data.append(e_d)
        return events_data

    def __tech_event_table_extraction_helper(self, id):
        table = self.file_soup.find('div', attrs={"id": id}).findChild('table')
        event_type = table.findChild('thead').findChild('tr').findChild('th').contents

        event_data = {}

        for row in table.findChild('tbody').findChildren('tr'):
            label = '_'.join(str(row.findChild(attrs={"class":"first"}).contents[0]).strip(':').lower().split())
            value = ' '.join(str(row.findChild(attrs={"class":"second"}).contents[0]).split())

            if label == 'target_price':
                event_data['lower_target_price'] = float(value.split('-')[0])
                event_data['upper_target_price'] = float(value.split('-')[1])
            elif label == 'volume':
                event_data[label] = int(value.replace(',',''))
            else:
                event_data[label] = value

        return event_data

