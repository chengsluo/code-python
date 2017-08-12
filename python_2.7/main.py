# coding=utf-8
import socket
from urllib import request, parse, error
from http import cookiejar

try:
    # HelloSpider
    response = request.urlopen('http://chengsluo.cn/blog')  # 请求构造方式，注意协议，IP都要一致
    response = request.urlopen('http://www.baidu.com')
    #print(response.read().decode('utf-8'))
    print(type(response))
    # print(response.read().decode('utf-8'))
    print(response.status)
    print(response.getheaders())
    print(response.getheader('Server'))

    # POST
    data = bytes(parse.urlencode({'word': 'Hello'}), encoding='utf8')
    response = request.urlopen('http://httpbin.org/post', data=data, timeout=1)
    print(response.read().decode('utf-8'))

    # #GET
    # response = request.urlopen('http://httpbin.org/get',timeout=10)
    # print(response.read(),decode('utf-8'))

    # 加入Header的写法
    url = 'http://httpbin.org/post'
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        'Host': 'httpbin.org'
    }
    dict = {
        'name': 'Germey'
    }
    data = bytes(parse.urlencode(dict), encoding='utf8')
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    print(response.read().decode('utf-8'))
    # req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')

    # #高级写法
    # auth_handler = request.HTTPBasicAuthHandler()
    # auth_handler.add_password(realm='PDQ Application',
    #                           uri='https://mahler:8092/site-updates.py',
    #                           user = 'klem',
    #                           passwd = 'kadidd!ehopper')
    # opener = request.build_opener(auth_handler)
    # request.install_opener(opener)
    # request.urlopen('http://www.example.com/login.html')

    # #添加代理
    # proxy_handler = request.ProxyHandler({
    #     'http': 'http://218.202.111.10:80',
    #     'https': 'https://180.250.163.34:8888'
    # })
    # opener = request.build_opener(proxy_handler)
    # response = opener.open('https://www.baidu.com')
    # print(response.read())

    # Cookie
    # 获取cookie,它是一个本地的变量，会随着访问而改变
    #打印cookie
    cookie = cookiejar.CookieJar()
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    response = opener.open('http://www.baidu.com')
    for item in cookie:
        print(item.name + "=" + item.value)
    #Cookie文件保存
    filename='cookie.txt'
    cookie=cookiejar.MozillaCookieJar(filename=filename) #为了将cookie保存成Mozilla型格式
    handler=request.HTTPCookieProcessor(cookie) #构建handler
    opener=request.build_opener(handler) #利用handler构建opener
    response=opener.open('http://www.baidu.com')
    cookie.save(ignore_discard=True,ignore_expires=True)
    #加载Cookie
    cookie=cookiejar.MozillaCookieJar()
    cookie.load('cookie.txt',ignore_discard=True,ignore_expires=True)
    handler=request.HTTPCookieProcessor(cookie)
    opener=request.build_opener(handler)
    response=opener.open('http://www.baidu.com')
    print(response.read().decode('utf-8'))

except error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print('TIME OUT')
