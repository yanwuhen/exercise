# IPython log file
import configparser
cf_w = configparser.ConfigParser()
cf_w.add_section('cn')
cf_w.add_section('us')
cf_w.add_section('to_delete')
cf_w.set('cn', 'fj', 'nice')
cf_w.set('us', 'a', 'b')
cf_w.remove_section('to_delete')
cf_w.remove_option('us', 'a')
with open('test.ini', 'w') as fp:
    cf_w.write(fp)
    
