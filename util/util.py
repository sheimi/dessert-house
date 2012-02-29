from datetime import datetime as dt

def str2date(time):
    '''the format of time is mm/dd/yyyy'''
    time = [int(x) for x in time.split('/')]
    return dt(time[2], time[0], time[1])

def date2str(time):
    '''the format of time is mm/dd/yyyy'''
    year, month, day = str(time.year), str(time.month), str(time.day)
    month = month if len(month) == 2 else '0' + month
    day = day if len(day) == 2 else '0' + day
    return '%s/%s/%s' % (month, day, year)
    
