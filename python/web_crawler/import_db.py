import os
import csv
import sqlite3

#create sql
#create table k8m (line VARCHAR(65536), title VARCHAR(65536), author VARCHAR(1024), cited_num VARCHAR(128), relate VARCHAR(128), reverse_relate  VARCHAR(128));create table k8m (line VARCHAR(65536), title VARCHAR(65536), author VARCHAR(1024), cited_num VARCHAR(128), relate VARCHAR(128), reverse_relate  VARCHAR(128));

conn = sqlite3.connect('k8m.db')
cursor = conn.cursor()

def check_line_exist(line):
	cursor.execute('select line,title,author,cited_num,relate,reverse_relate from k8m where line=?', [line])
	ret = cursor.fetchall()
	if len(ret) >= 1:
		return True
	else:
		return False

def import_output(output_file='output.csv'):
	dr = csv.reader(open(output_file, 'r', encoding='utf-8'))
	cnt = p_same = a_same = 0
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
			continue
		cursor.execute('insert into k8m(line,title,author,cited_num,relate,reverse_relate) values(?,?,?,?,?,?)', row)
		conn.commit()
		#cnt += 1
		#if cnt % 1000 == 0:
		#	print(cnt)
	print('p_same is %d, a_same is %d' % (p_same, a_same))

def import_file(input_file='input.txt', title='', check=True):
	with open(input_file, 'r', encoding='utf-8') as in_f:
		for ln in in_f.readlines():
			ln = ln.strip()
			if check and not check_line_exist(ln):
				cursor.execute('insert into k8m(line,title,author,cited_num,relate,reverse_relate) values(?,?,?,?,?,?)', [ln, title, '', '', '', ''])
				conn.commit()
				
import_output(output_file='output.csv')
import_output(output_file='./1114/output.csv')
import_file(input_file='./1114/fail.txt', title='fail', check=False)
import_file(input_file='./1114/did_not_match_any.txt', title='did_not_match_any', check=False)
import_file()
