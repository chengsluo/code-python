# coding:UTF-8
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # IPV4, UDP
s.bind(("", 5005))
data, addr = s.recvfrom(1024)          # 缓冲区大小为1024B
print(' received message:%s' % data)
s.close()