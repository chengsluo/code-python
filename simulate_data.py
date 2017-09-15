#!/usr/bin/env python3
#-- coding:utf-8 --

# pip install mysqlclient

import time
import MySQLdb
import random

conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='12345',
    db='bmr',
    charset='utf8'
)

def insert_data():
    cur = conn.cursor()
    nows = time.time()
    args_array=[]
    adminId="14121257"
    userId="14121257"
    requestReason="我想使用房间"
    for item in range(1,204000):
        requestId=item
        needDate = time.strftime('%Y-%m-%d 00:00:00', time.localtime(nows+item*50000-10000000000))
        needIndex =random.randint(1, 3)
        timestamp =time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(nows+item*50-1000000000))
        # print(timestamp)
        roomId=random.randint(1, 211)
        status=random.randint(1, 5)
        finishTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(nows+item*150-1000000000))
        args_array.append((requestId, adminId, needDate, needIndex, timestamp, requestReason, roomId, status, userId, finishTime))
        
    # print ("insert into Request(requestId, adminId, needDate, needIndex, timestamp, requestReason, roomId, status, userId, finishTime) values{};".format(args_array[0]))
    cur.executemany('insert into Request(requestId, adminId, needDate, needIndex, timestamp, requestReason, roomId, status, userId, finishTime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',args_array)
    conn.commit()

insert_data()
