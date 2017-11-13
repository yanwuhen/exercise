import os
import csv
import sqlite3

conn = sqlite3.connect('k8m.db')
cursor = conn.cursor()
dr = csv.reader(open('output.csv', 'r', encoding='utf-8'))
p_same = a_same = 0
for row in dr:
	line = row[0]
	cursor.execute('select line,title,author,cited_num,relate,reverse_relate from k8m where line=?', [line])
	ret = cursor.fetchall()
	if len(ret) >= 1:
		if ret[0][1] != row[1] or ret[0][2] != row[2] or ret[0][3] != row[3] or ret[0][4] != row[4] or ret[0][5] != row[5]:
			p_same += 1
			print('line is same, and other is diff: %s' % line)
		else:
			a_same += 1
	cursor.execute('insert into k8m(line,title,author,cited_num,relate,reverse_relate) values(?,?,?,?,?,?)', row)
print('p_same is %d, a_same is %d' % (p_same, a_same))
#create sql
#create table k8m (line VARCHAR(65536), title VARCHAR(65536), author VARCHAR(1024), cited_num VARCHAR(128), relate VARCHAR(128), reverse_relate  VARCHAR(128));create table k8m (line VARCHAR(65536), title VARCHAR(65536), author VARCHAR(1024), cited_num VARCHAR(128), relate VARCHAR(128), reverse_relate  VARCHAR(128));
