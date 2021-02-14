
import glob
import re
import bs4
from Scripts.PageParser import PageParser

pages = glob.glob('./HTML/*.html', recursive=False)

pp = PageParser(pages[0])


pp.get_bearish_tech_events()

pp.get_bullish_tech_event()




# bs4.BeautifulSoup.find_all(class_="bearish", pages[0])
