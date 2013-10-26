#!/usr/bin/python

'''
Created on Sep 20, 2013
@summary: some of the methods to handle date calculation
@author: Jay <smilejay.com>
'''

import datetime
import calendar

def get_a_month_val(year, month, day=1):
    day = datetime.datetime(year, month, day)
    print day
    last_day_of_previous_month = day.replace(day=1) - datetime.timedelta(days=1)
    last_day_of_this_month = day.replace(day=calendar.monthrange(year, month)[1])
    print last_day_of_previous_month
    print last_day_of_this_month

if __name__ == '__main__':
    get_a_month_val(2013, 10, 20)
