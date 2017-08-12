#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
在python2.7中测试通过
'''

import cookielib
import time
import re
import sys
import requests
import MySQLdb as mdb
try:
    from PIL import Image
except:
    pass
import threading

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': agent
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar('weibo_cookies.txt')

# 访问 初始页面带上 cookie
index_url = "http://weibo.com/"
try:
    session.get(index_url, headers=headers, timeout=2)
except:
    session.get(index_url, headers=headers)


def open_img(image_name):
    """打开图片
    :param image_name: 图片的路径
    :return:
    """
    im = Image.open(image_name)
    im.show()
    im.close()


def login():
    """登录主函数
    :return:
    """
    image_name, qrcode_qrid = get_qrcode()
    try:
        # 用此方法打开图片不会退出，可以直接命令行用open打开，粗暴简单.
        thread = threading.Thread(target=open_img, name="open", args=(image_name,))
        thread.start()
        print(u"请用手机微博扫描二维码"
              u"微博二维码扫描在主页右上角!")
    except:
        print(u"请到当前目录下，打开二维码后用手机微博扫描二维码"
              u"微博二维码扫描在主页右上角!")
    # 下面判断是否已经扫描了二维码
    statu = 0
    while not statu:
        qrcode_check_page = scan_qrcode(qrcode_qrid, str(long(time.time() * 10000)))
        if "50114002" in qrcode_check_page:
            statu = 1
            print(u"---成功扫描，请在手机点击确认以登录---")
        time.sleep(2)

    # 下面判断是否已经点击登录,并获取alt的内容
    while statu:
        qrcode_click_page = scan_qrcode(qrcode_qrid, str(long(time.time() * 100000)))
        if "succ" in qrcode_click_page:
            # 登录成功后显示的是如下内容,需要获取到alt的内容
            # {"retcode":20000000,"msg":"succ","data":{"alt":"ALT-MTgxODQ3MTYyMQ==-sdfsfsdfsdfsfsdf-39A12129240435A0D"}}
            statu = 0
            alt = re.search(r'"alt":"(?P<alt>[\w\-\=]*)"', qrcode_click_page).group("alt")
            print(u"---登录成功---")
        time.sleep(2)

    # 下面是登录请求获取登录的跨域请求
    params = {
        "entry": "weibo",
        "returntype": "TEXT",
        "crossdomain": 1,
        "cdult": 3,
        "domain": "weibo.com",
        "alt": alt,
        "savestate": 30,
        "callback": "STK_" + str(long(time.time() * 100000))
    }
    login_url_list = "http://login.sina.com.cn/sso/login.php"
    login_list_page = session.get(login_url_list, params=params, headers=headers)
    # 返回的数据如下所示，需要提取出4个url
    # STK_145809336258600({"retcode":"0","uid":"1111111","nick":"*****@sina.cn","crossDomainUrlList":
    # ["http:***************","http:\/\***************","http:\/\/***************","http:\/\/***************"]});
    url_list = [i.replace("\/", "/") for i in login_list_page.content.split('"') if "http" in i]
    for i in url_list:
        session.get(i, headers=headers)
        time.sleep(0.5)
    session.cookies.save(ignore_discard=True, ignore_expires=True)


def get_qrcode():
    """获取二维码图片以及二维码编号
    :return: qrcode_image, qrcode_qrid
    """
    qrcode_before = "http://login.sina.com.cn/sso/qrcode/image?entry=weibo&size=180&callback=STK_" + str(
        long(time.time() * 10000))
    qrcode_before_page = session.get(qrcode_before, headers=headers)
    if qrcode_before_page.status_code != 200:
        sys.exit(u"可能微博改了接口!请联系作者修改")
    qrcode_before_data = qrcode_before_page.content
    qrcode_image = re.search(r'"image":"(?P<image>.*?)"', qrcode_before_data).group("image").replace("\/", "/")
    qrcode_qrid = re.search(r'"qrid":"(?P<qrid>[\w\-]*)"', qrcode_before_data).group("qrid")
    cha_page = session.get(qrcode_image, headers=headers)
    image_name = u"cha." + cha_page.headers['content-type'].split("/")[1]
    with open(image_name, 'wb') as f:
        f.write(cha_page.content)
        f.close()
    return image_name, qrcode_qrid


def scan_qrcode(qrcode_qrid, _time):
    """判断是否扫码等需要
    :param qrcode_qrid:
    :return: html
    """
    params = {
        "entry": "weibo",
        "qrid": qrcode_qrid,
        "callback": "STK_" + _time
    }
    qrcode_check = "http://login.sina.com.cn/sso/qrcode/check"
    return session.get(qrcode_check, params=params, headers=headers).content


def is_login():
    """判断是否登录成功
    :return: 登录成功返回True，失败返回False
    """
    try:
        session.cookies.load("weibo_cookies.txt",ignore_discard=True, ignore_expires=True)
    except:
        print(u"没有检测到cookie文件")
        return False
    url = "http://weibo.com/"
    my_page = session.get(url, headers=headers)
    if "我的首页" in my_page.content:
        return True
    else:
        return False

if __name__ == '__main__':
    login()
    if is_login():
        print "登录成功！"
    else:
        print "登录失败！"
    url = "http://weibo.com/"
    my_page = session.get(url, headers=headers).content
    r0=re.findall(r"CONFIG\[\'uid\'\]=\'\d{10}",my_page)
    r1=re.findall(r"\d{10}",str(r0))
    uid=r1[0]
    url = "http://weibo.com/%s/fans"%(uid)
    html=session.get(url, headers=headers).content
    #   print html
    r0_for_page=re.findall(r"page=\d*",html)
    r1_for_page=re.findall(r"\d*",str(r0_for_page))
    maxpage=1
    for item in r1_for_page:
        if  item.isdigit() and int(item)>maxpage:
            maxpage=int(item)
    print "粉丝最大页数："+ str(maxpage)

    param=[]
    sum=0
    for index in range(1, maxpage+1):
        url = "http://weibo.com/%s/fans?cfs=600&relate=fans&t=1&f=1&type=&Pl_Official_RelationFans__88_page=%d#Pl_Official_RelationFans__88"%(uid,index)
        html = session.get(url, headers=headers).content
        #print html
        r0=re.findall(r'/\d{10}\\/fans\?current=fans\\" >\d+<', html)
        r1=re.findall("\d{10}",str(r0))
        #print r1
        r2=re.findall(r">\d+",str(r0))
        r3 = re.findall(r"\d+", str(r2))
        #print r3
        for i in range(0,len(r1)):
            param.append([r1[i],r3[i]])
        sum+=len(r1)
    try:
        # 打开数据库连接
        db = mdb.connect("182.254.246.75", "testuser", "mysqltest", "test_spider")
        # 使用cursor()方法获取操作游标
        cur = db.cursor()
        # SQL 插入语句
        insertSQL = "INSERT INTO test_spider.fans(id_fans,follow_num) VALUES(%s,%s)"
        cur.executemany(insertSQL, param)
    except mdb.Error, e:
        cur.close()
        db.close()
        print "数据库操作失败,请重试！如有重复数据,请利用代码中的数据库账号和密码删除重复数据后再试！"
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    else:
        # 关闭数据库连接
        db.commit()
        cur.close()
        db.close()
        print "获取粉丝总数："+str(sum)
        print "完成数据获取,顺利退出程序"
    # print session.cookies
