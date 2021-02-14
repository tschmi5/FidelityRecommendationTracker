"""
Module To Help Extract Fidelity Research Information
"""
import bs4


class PageParser:
    """
    Object to aid with parsing of fidelity research page
    """
    def __init__(self, file_path):
        """
        :param file_path: Path to Fidelity HTML stock research page
        """
        self.file_path = file_path

        with open(self.file_path, 'r') as page:
            self.file_soup = bs4.BeautifulSoup(page.read(), 'html.parser')

    def get_bearish_technical_events(self):
        """
        Get Bearish technical events and data
        :return: Dict
        """
        return self.__extract_bull_or_bear_table('bear')

    def get_bullish_technical_events(self):
        """
        Get Bullish technical event and data
        :return:
        """
        return self.__extract_bull_or_bear_table('bull')

    def __extract_bull_or_bear_table(self, event_type):
        """
        Helper to extract event details for technical event
        :param event_type:
        :return:
        """
        # Find the tbody of the table for given type
        tbody = self.file_soup.find('div', class_=event_type).findChild('table').findChild("tbody")

        # Extract the rows for this table
        rows = tbody.find_all('td', {"scope": "row"})

        tickers = []
        link_ids = []

        for index, row in enumerate(rows):
            # If even row, extract ticker symbol
            if index % 2 == 0:
                for j in row.find_all('span', recursive=False):
                    tickers.append(j['fmr-param-symbol'])
            # If odd row, extract link to data
            else:
                for j in row.find_all('a', recursive=False):
                    link_ids.append(f'{j["id"]}-content')

        events_data = []
        for ticker, link_id in zip(tickers, link_ids):
            e_d = {'ticker': ticker, **self.__tech_event_table_extraction_helper(link_id)}
            events_data.append(e_d)
        return events_data

    def __tech_event_table_extraction_helper(self, event_id):
        """
        Helper to extract event table data
        :param event_id: id of the corresponding data
        :return: Dict of table values
        """
        event_data = {}

        table = self.file_soup.find('div', attrs={"id": event_id}).findChild('table')
        event_data['event_type'] = " ".join(table
                                            .findChild('thead')
                                            .findChild('tr').findChild('th')
                                            .contents[0]
                                            .split())

        for row in table.findChild('tbody').findChildren('tr'):
            label = '_'.join(str(row.findChild(attrs={"class":"first"}).contents[0])
                             .strip(':')
                             .lower()
                             .split())
            value = ' '.join(str(row.findChild(attrs={"class":"second"}).contents[0]).split())

            if label == 'target_price':
                event_data['lower_target_price'] = float(value.split('-')[0])
                event_data['upper_target_price'] = float(value.split('-')[1])
            elif label == 'volume':
                event_data[label] = int(value.replace(',',''))
            else:
                event_data[label] = " ".join(value.split())

        return event_data

    def get_top_rated_by_sector(self):
        """
        Parse out the top rated by sector
        :return:
        """
        # Grab the sectors
        sectors_html = self.file_soup.find_all('span', attrs={"class": "col-sector"})
        sectors = []
        for sector_html in sectors_html:
            sectors.append(sector_html.findChild('a').contents[0])

        # Grab the Ticker Symbols
        tickers = []
        sector_data = self.file_soup.find('div', attrs={"class":"sector-data"})
        for j in sector_data.find_all('span', recursive=True):
            if j.has_attr('fmr-param-symbol'):
                tickers.append(j['fmr-param-symbol'])

        return [{"ticker": ticker, "sector": sector} for ticker, sector in zip(tickers, sectors)]
