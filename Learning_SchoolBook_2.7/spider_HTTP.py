# 2.7.x python
import urllib
proxies = {'http': 'http://proxy.example.com:8080/'}
opener = urllib.FancyURLopener(proxies)
f = opener.open('http://www.python.org')
print (f.read())