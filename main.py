
import glob
import re
import bs4
from Modules.PageParser import PageParser

pages = glob.glob('./HTML/*.html', recursive=False)

pp = PageParser(pages[0])


print(pp.get_bearish_technical_events())

print(pp.get_bullish_technical_events())

print(pp.get_top_rated_by_sector())
