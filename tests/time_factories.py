from datetime import datetime


def minute(minute_string):
    return hour('00:' + minute_string)


def hour(hour_string):
    return datetime.strptime('2019-01-01 %s' % hour_string, '%Y-%m-%d %H:%M:%S')
