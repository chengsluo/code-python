# coding:UTF-8
# when use UTF-8, you should insert a litter'b' into front of strings.
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b"hello world!", ('127.0.0.1', 5005))   # 每次运行时需要修改IP地址
s.close()

