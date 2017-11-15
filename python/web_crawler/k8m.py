import os
import sys
import csv
import copy
import requests
from bs4 import BeautifulSoup
import bs4
if sys.version > '3':
    import urllib.parse as parse
else:
    import urllib as parse
debug=False
#debug=True

def clean_text(contents_list):
    try:
        if type(contents_list) in (str, bs4.element.NavigableString):
            return contents
        ret = []
        for node in contents_list:
            if type(node) in (str, bs4.element.NavigableString):
                ret.append(node)
            else:
                ret.append(clean_text(node))
        return ''.join(ret)
    except Exception as e:
        return str(contents_list)

def get_data(keyword):
    q_str = parse.urlencode({'q': keyword})
    rsp = requests.get(url='https://scholar.google.com/scholar?hl=en-US&as_sdt=0%2C5&'+ q_str)
    html_txt = rsp.text
    if 'did not match any articles' in html_txt:
        return 'did_not_match_any', None, None
    if debug:
        #k_file = keyword[:50].replace('\\','').replace("'", '').replace("/", "") + '.html'
        k_file = 'test.html'
        with open(k_file, 'w', encoding='utf-8') as tmp_f:
            if sys.version > '3':
                f_txt = html_txt
            else:
                f_txt = html_txt.encode('utf-8')
            tmp_f.write(f_txt)
    if 'not a robot' in html_txt:
        return 'not_a_robot', None, None

    bs = BeautifulSoup(html_txt, "lxml")
    gs_ri = bs.find('div', class_='gs_ri')
    gs_rt = gs_ri.find("h3", class_='gs_rt')
    title = gs_rt.find('a')
    if title:
        title = title.contents
    else:
        title = gs_rt.text
    title = clean_text(title)

    gs_a = gs_ri.find("div", class_="gs_a")
    author_nodes = gs_a.findAll("a")
    if author_nodes is None:
        author_nodes = gs_a.text
    else:
        author = [clean_text(a.contents) for a in author_nodes]
        author = ','.join(author)

    cited_node = gs_ri.find("div", class_="gs_fl")
    cited_num = 0
    for n in cited_node.findAll("a"):
        if 'Cited by' in n.contents[0]:
            cited_num = n.contents[0][9:]
    return title, author, cited_num

def calc_relate(title, line):
    t_list = title.strip().split(' ')
    l_line = line.strip().split(' ')
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
    output_file = 'output.csv'
    if os.path.exists(output_file):
        writer = csv.writer(open(output_file, 'a', encoding='utf-8'))
    else:
        writer = csv.writer(open(output_file, 'w', encoding='utf-8'))
        writer.writerow(['line', 'title', 'author', 'cited_num', 'relate', 'reverse_relate'])

    with open(input_file, 'r', encoding='utf-8') as in_f:
        all_keyword = in_f.readlines()
        copy_keywork = copy.deepcopy(all_keyword)
    for line_org in all_keyword:
        line = line_org.strip()
        if line is None or line == '':
            continue
        try:
            title, author, cited_num = get_data(line)
        except Exception as e:
            if debug:
                import traceback
                print(line)
                print(traceback.format_exc())
            with open('fail.txt', 'a', encoding='utf-8') as fail_f:
                fail_f.writelines(line + '\n')
            #raise e
        if title == 'not_a_robot' and author is None and cited_num is None:
             print('robot detection')
             raise
        if title == 'did_not_match_any' and author is None and cited_num is None:
            with open('did_not_match_any.txt', 'a', encoding='utf-8') as dnma:
                dnma.writelines(line+'\n')
        else:
            relate, reverse_relate = calc_relate(title, line)
            writer.writerow([line, title, author, cited_num, relate, reverse_relate])
        with open(input_file, 'w', encoding='utf-8') as unh_f:
            copy_keywork.remove(line_org)
            unh_f.writelines(copy_keywork)
