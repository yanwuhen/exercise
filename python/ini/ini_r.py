# IPython log file

import configparser
cf = configparser.ConfigParser()
cf.read('test.ini')
print cf.sections()
print cf.options('cn')
print cf.items('cn')
print cf.get('cn', 'fj')
print cf.getint('cn', 'fj')
