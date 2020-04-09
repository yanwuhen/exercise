import os
import sys
import requests
from requests_html import HTMLSession,AsyncHTMLSession
from bs4 import BeautifulSoup
import bs4
if sys.version > '3':
    import urllib.parse as parse
else:
    import urllib as parse

def get_btdoor_data(keyword):
    q_str = parse.urlencode({'q': keyword})
    url="https://btdoor.cc/query?word=%s" % q_str
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    session = HTMLSession()
    r = session.get(url, headers={'user-agent': ua})
    r.html.render()