#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='172.26.128.141'))
channel = connection.channel()

# 声明一个exchange，广播模式
channel.exchange_declare(exchange='logs',
                         type='fanout')
# 随机取名，Consumer关闭时自动关闭
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# Bindings绑定，建立通道
channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % (body,))


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()

# 此处，必须先运行consumer，建立与两个与exchange相连的队列。
# exchange会向两个channel广播message

