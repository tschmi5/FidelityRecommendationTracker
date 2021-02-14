
import glob
import re
import bs4
from Scripts.PageParser import PageParser

pages = glob.glob('./HTML/*.html', recursive=False)

pp = PageParser(pages[0])


pp.get_bearish_technical_events()

pp.get_bullish_technical_events()




# bs4.BeautifulSoup.find_all(class_="bearish", pages[0])
