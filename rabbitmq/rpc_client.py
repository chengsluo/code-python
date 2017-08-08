#!/usr/bin/env python
import pika
import uuid

# 先声明自己为 consumer ，然后再摇身一变producer，原本的consumer接受应答

# 这个远程调用是阻塞式的，在实际应用中是没人使用的
class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='172.26.128.141'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        # 验证消息身份
        if self.corr_id == props.correlation_id:
            self.response = body
    # delivery_mode: 持久化一个Message（通过设定值为2）。其他任意值都是非持久化。请移步RabbitMQ消息队列（三）：任务分发机制
    # content_type: 描述mime-type 的encoding。比如设置为JSON编码：设置该property为application/json。
    # reply_to: 一般用来指明用于回调的queue（Commonly used to name a callback queue）。
    # correlation_id: 在请求中关联处理RPC响应（correlate RPC responses with requests）。

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print (" [x] Requesting fib(30)")
response = fibonacci_rpc.call(40)
print (" [.] Got %r" % (response,))

'''
当客户端启动时，它创建了匿名的exclusive callback queue.
客户端的RPC请求时将同时设置两个properties： reply_to设置为callback queue；correlation_id设置为每个request一个独一无二的值.
请求将被发送到an rpc_queue queue.
RPC端或者说server一直在等待那个queue的请求。当请求到达时，它将通过在reply_to指定的queue回复一个message给client。
client一直等待callback queue的数据。当message到达时，它将检查correlation_id的值，如果值和它request发送时的一致那么就将返回响应。

'''