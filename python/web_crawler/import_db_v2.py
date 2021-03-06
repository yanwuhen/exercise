import os
import csv
import sqlite3
import xlrd

CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS k8m (id INTEGER,'\
                              ' line VARCHAR(65536),'\
							  ' title VARCHAR(65536),'\
							  ' author VARCHAR(1024),'\
							  ' cited_num VARCHAR(128),'\
							  ' relate VARCHAR(128),'\
							  ' reverse_relate  VARCHAR(128));'

conn = sqlite3.connect('/dev/shm/k8m.db')
cursor = conn.cursor()
try:
	cursor.execute(CREATE_TABLE)
except Exception as e:
	print(e)
cursor.execute('delete from k8m')
conn.commit()

def import_output(output_file='output.csv'):
	dr = csv.reader(open(output_file, 'r', encoding='utf-8'))
	for row in dr:
		#cursor.execute('Insert Or Replace Into k8m(line,title,author,cited_num,relate,reverse_relate) values(?,?,?,?,?,?)', row)
		cursor.execute('update k8m set title=?, author=?, cited_num=?, relate=?, reverse_relate=? where line=?', row[1:]+ [row[0]])
		conn.commit()

def update_file(input_file='input.txt', title=''):
	with open(input_file, 'r', encoding='utf-8') as in_f:
		for ln in in_f.readlines():
			cursor.execute('update k8m set title=? where line=?', [title, ln.strip()])
			conn.commit()

def import_file(input_file='input.txt', title=''):
	id = 0
	with open(input_file, 'r', encoding='utf-8') as in_f:
		for ln in in_f.readlines():
			id += 1
			ln = ln.strip()
			if ln is None or ln == '':
				continue
			cursor.execute('insert into k8m(id, line,title,author,cited_num,relate,reverse_relate) values(?,?,?,?,?,?)', [id, ln, title, '', '', '', ''])
			conn.commit()

def import_xls(input_file='k8m.xls'):
	data = xlrd.open_workbook(input_file)
	sheets = data.sheets()
	st = data.sheet_by_name('all publication Feb21')
	keyword_list = st.col_values(3)
	id_list = st.col_values(1)
	for z in zip(id_list[3:], keyword_list[3:]):
		id, ln = z
		ln = ln.strip()
		if ln is None or ln == '':
			continue
		ln = ln.replace('\n', ' ')
		id = int(id)
		cursor.execute('insert into k8m(id, line,title,author,cited_num,relate,reverse_relate) values(?,?,?,?,?,?,?)', [id, ln, '', '', '', '', ''])
		conn.commit()

import_xls()
#import_file()
import_output(output_file='output.csv')
import_output(output_file='./1114/output.csv')
update_file(input_file='./1114/fail.txt', title='fail')
update_file(input_file='./1114/did_not_match_any.txt', title='did_not_match_any')
conn.close()
