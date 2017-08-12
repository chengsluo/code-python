# coding=utf-8
from urllib import request,error
import socket

try:
    response = request.urlopen('http://chengsluo.cn/index.htm',timeout=0.01)

except error.URLError as e:
	print(type(e.reason))
	if	isinstance(e.reason,socket.timeout): #查看类型后强制抛出异常
		print('TIME	OUT')
except error.HTTPError as e:
    print(e.reason,e.code,e.headers)
except error.URLError as e:
    print(e.reason)
else:
    print('Request Successfully')