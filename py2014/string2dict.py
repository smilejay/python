'''
Created on Oct 14, 2014

@author: Jay <smile665@gmail.com>
'''

import MySQLdb
import ast
import json


def my_run():
    try:
        m = '{"host":"10.1.77.20", "port":3306, "user":"abc",\
              "passwd":"123", "db":"mydb", "connect_timeout":10}'
        d = ast.literal_eval(m)
        print type(d)
        print d
        d2 = json.loads(m)
        print type(d2)
        MySQLdb.Connect(host=d['host'], port=d['port'], user=d['user'],
                        passwd=d['passwd'], db=d['db'],
                        connect_timeout=d['connect_timeout'])
        print 'right'
    except Exception, e:
        print 'wrong %s' % e


if __name__ == '__main__':
    my_run()
