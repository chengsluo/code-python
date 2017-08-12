#coding:UTF-8
# 3.x python
import urllib.request
f = urllib.request.urlopen('http://www.baidu.com')
print(f.read())
f.close()

