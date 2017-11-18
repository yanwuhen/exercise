import xlrd, xlsxwriter
from xlutils.copy import copy
TEST_XLS = '/home/libin/libin.xls'
DST_XLS = '/home/libin/taget.xls'

# data = xlrd.open_workbook(TEST_XLS)
# sheets = data.sheets()
# st = data.sheet_by_name('all publication Feb21')
# for i in (0..6135)

# xlsw = xlsxwriter.Workbook(TEST_XLS)
# xlsw.add_worksheet


 
rb = xlrd.open_workbook(TEST_XLS) 
rs = rb.sheet_by_index(1)
authors = rs.col_values(0)

wb = copy(rb) 
ws = wb.get_sheet(1)

tmp_autor  = ''
try:
    for row in range(0,61355):
        value = authors[row]
        if type(value) != str or '(' in value or \
           '（' in value or value.strip() == '':
            ws.write(row, 0, tmp_autor)
        else:
            tmp_autor = value
except Exception as e:
    print('row is %d, value is %s' % (row, value))
    print(e)
 
wb.save(TEST_XLS)   