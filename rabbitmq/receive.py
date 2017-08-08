#!/usr/bin/env python
import pika

# 创建connection
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='172.26.128.141'))
# 创建channel
channel = connection.channel()
# 创建queue
channel.queue_declare(queue='hello',auto_delete=True)

print (' [*] Waiting for messages. To exit press CTRL+C')

# 订阅前声明回调函数

def callback(ch, method, properties, body):
    print (" [x] Received %r" % (body,))
    connection.close()

# 订阅
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

channel.start_consuming()

