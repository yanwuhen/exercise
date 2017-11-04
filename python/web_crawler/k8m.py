import os
import sys
import csv
import requests
from bs4 import BeautifulSoup
if sys.version > '3':
    import urllib.parse as parse
else:
    import urllib as parse

def clean_text(txt):
    return txt

def get_data(keyword):
    q_str = parse.urlencode({'q': keyword})
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
            cited_num = n.contents[0][9:]
    return clean_text(title), clean_text(author), cited_num

def calc_relate(title, line):
    t_list = title.strip.split(' ')
    l_line = line.strip.split(' ')
    cnt = 0
    reverse_cnt = 0
    for t in t_list:
        if t in l_line:
            cnt += 1
    relate = "%02.2f%%" % ((cnt * 100.0) / len(l_line))
    for l in l_line:
        if l in t_list:
            reverse_cnt += 1
    reverse_relate = "%02.2f%%" % ((reverse_cnt * 100.0) / len(t_list))
    return relate, reverse_relate

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('usage: xxx your_input_file')
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        raise Exception('error: file no exist.')
    if os.path.exists('output.cvs'):
        raise Exception('error: output.cvs aleady exist.')
    else:
        writer = csv.writer(open('output.cvs', 'w'))
    with open(input_file, 'r') as in_f:
        for line in in_f.readlines():
            title, author, cited_num = get_data(line.strip())
            relate, reverse_relate = calc_relate(title, line)
            writer.writerow([line, title, author, cited_num, relate, reverse_relate])
