#!/usr/bin/env python3
#-- coding:utf-8 --

# pip install mysqlclient

import time
import MySQLdb

conn = MySQLdb.connect(
    host='115.29.146.79',
    port=3306,
    user='yahaa',
    passwd='Asd147258',
    db='webService',
)

def fix_msg():
    cur = conn.cursor()
    nows = time.time()
    args_array=[]
    for item in range(1,1000):
        tr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(nows+item))
        args_array.append((tr,item))

    cur.executemany('update msg set time=%s where msg_id=%s;',args_array)
    conn.commit()

def fix_inverter_data():
    cur = conn.cursor()
    nows = time.time()
    args_array=[]
    for item in range(1,89000):
        tr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(nows+item))
        args_array.append((tr,item))

    cur.executemany('update inverter_data set the_current_time_of_the_inverter=%s where id=%s;',args_array)
    conn.commit()
def fix_weather_meter_data():
    cur = conn.cursor()
    nows = time.time()
    args_array=[]
    for item in range(8000,11000):
        tr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(nows+item))
        args_array.append((tr,item))

    cur.executemany('update weather_meter_data set time=%s where id=%s;',args_array)
    conn.commit()


fix_weather_meter_data()
