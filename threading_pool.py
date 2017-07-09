#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from threading import Thread
import subprocess
from queue import Queue
import re

num_ping_threads = 2
num_arp_threads = 2
in_queue = Queue()
out_queue = Queue()
ips = ["10.0.1.1","10.0.1.2","10.0.1.3","10.0.1.4"]

def ping(i,iq,oq):
    while True:
        ip = iq.get()
        print ("Thread %d: Pinging %s" % (i,ip))
        ret = subprocess.call("ping -c 1 %s " % ip,shell=True,stdout=open("/dev/null","w"),stderr=subprocess.STDOUT)

        if ret == 0:
            oq.put(ip)
        else:
            print("%s : did not respond " %ip)
        iq.task_done()

def arp(i,oq):
    while True:
        ip = oq.get()
        p = subprocess.call("ping -c 1 %s " % ip,shell=True,stdout=subprocess.PIPE)

        out = p.stdout.read()

        result = out.split()
        pattern = re.compile(":")
        mac_addr = None
        for item in result:
            if re.search(pattern, item):
                mac_addr = item

        print("IP Address: %s | Mac Address: %s" %(ip ,mac_addr))
        oq.task_done()

for ip in ips:
    in_queue.put(ip)

for i in range(num_ping_threads):
    worker = Thread(target=ping,args=(i,in_queue,out_queue))
    worker.setDaemon(True)
    worker.start()

for i in range(num_arp_threads):
    worker = Thread(target=arp,args=(i,out_queue))
    worker.setDaemon(True)
    worker.start()

print("Main Thread Waiting!")

in_queue.join()
out_queue.join()

print("done")
