import os
import csv
import sqlite3

conn = sqlite3.connect('k8m.db')
cursor = conn.cursor()
unh = []
with open('input.txt', 'r') as f:
	for l in f.readlines():
		l_clear = l.strip()
		cursor.execute('select line,title,author,cited_num,relate,reverse_relate from k8m where line=?', [l_clear])
		ret = cursor.fetchall()
		if len(ret) >= 1:
			continue
		unh.append(l)

with open('unh.txt', 'w') as of:
	of.writelines(unh)
