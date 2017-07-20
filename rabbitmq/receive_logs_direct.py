#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='172.26.128.141'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    print >> sys.stderr, "Usage: %s [info] [warning] [error]" % \
                         (sys.argv[0],)
    sys.exit(1)

# 我们将使用log的severity作为routing key，这样Consumer可以针对不同severity的log进行不同的处理。
for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

print (' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print (" [x] %r:%r" % (method.routing_key, body,))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()