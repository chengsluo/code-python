# !/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='172.26.128.141'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')
for i in range(0,1000):
    message = "string"+"  %s" % i
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body=message)
    print(" [x] Sent %r" % (message,))
connection.close()
