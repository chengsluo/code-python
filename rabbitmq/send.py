#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='172.26.128.141'))
channel = connection.channel()

# 创建名字为hello的queue
channel.queue_declare(queue='hello',auto_delete=True)

# Producer只能发送到exchange，它是不能直接发送到queue的
# 现在我们使用默认的exchange（名字是空字符）。
# 这个默认的exchange允许我们发送给指定的queue。
# routing_key就是指定的queue名字。
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print (" [x] Sent 'Hello World!'")

connection.close()