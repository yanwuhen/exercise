import os
import csv
import sqlite3

conn = sqlite3.connect('/home/libin/k8m.db')
cursor = conn.cursor()
dr = csv.DictReader(open(output_file, 'r', encoding='utf-8'))
for r in dr:
	cursor.execute('insert into k8m(line,title,author,cited_num,relate,reverse_relate) values(?,?,?,?,?,?)', d)

create table (line VARCHAR(65536), title VARCHAR(65536), author VARCHAR(1024), cited_num VARCHAR(128), relate VARCHAR(128), reverse_relate  VARCHAR(128));
