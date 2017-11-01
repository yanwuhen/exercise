import os
import requests
import urllib
from bs4 import BeautifulSoup

def get_data(keyword):
    q_str = urllib.parse.urlencode({'q': keyword})
    #参数：hl=zh-CN 指定语言；as_sdt=20051008 日期；
    rsp = requests.get(url='https://scholar.google.com/scholar?hl=en-US&as_sdt=0%2C5&'+ q_str)
    html_txt = rsp.text
    bs = BeautifulSoup(html_txt, "lxml")
    gs_ri = bs.find('div', class_='gs_ri')
    gs_rt = gs_ri.find("h3", class_='gs_rt')
    title = gs_rt.find('a').contents[0]
    gs_a = gs_ri.find("div", class_="gs_a")
    author_nodes = gs_a.findAll("a")
    author = [a.contents[0] for a in author_nodes]
    cited_node = gs_ri.find("div", class_="gs_fl")
    cited_num = 0
    for n in cited_node.findAll("a"):
        if 'Cited by' in n.contents[0]:
            cited_num = n.contents[0]
    return title, author, cited_num

def handle(input_file):
    if not os.path.exists(input_file):
        print('error: file no exist.')
    with open(input_file, 'r') as in_f:
        for l in in_f.readlines():
            get_data(l.strip())