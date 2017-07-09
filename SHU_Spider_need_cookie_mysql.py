# -*- coding: utf-8 -*-
import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
import tablib
import MySQLdb as mdb

from lxml import etree
import traceback


class weibo:
    cookie = {"Cookie": "_T_WM=ca1745569c5bd12e9c2f4dcf89d72af4; ALF=1489561698; SCF=AvHAOognUUQd006WHQR3aCw9y0Z_Pxtg4UfdxwXEy-NUTo6lmJJlgsMNbkDoPM4pK7JJbBn4909HlSOrzTvp_vs.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFvUWMOwVLeOW_8ycw.LzOI5JpX5o2p5NHD95Qf1KqNe0zE1Kz0Ws4DqcjSKJvEdg8VTH5Eehq71Btt; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174; H5_INDEX=1; H5_INDEX_TITLE=%E6%98%8C%E6%B4%A5%E7%9C%A8%E6%98%8C; SUB=_2A251pdhODeRxGeBO6VUT-SfJyTuIHXVXafgGrDV6PUJbkdBeLWSlkW1dSUZODyfdtm3Vt-ULip_rcUMtqg..; SUHB=0ebdBMwQlLe_Oz; SSOLoginState=1486989342"}  # 将your cookie替换成自己的cookie

    # weibo类初始化
    def __init__(self, user_id, filter=0):
        self.user_id = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = 0  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.userName = ''  # 用户名，如“Dear-迪丽热巴”
        self.weiboNum = 0  # 用户全部微博数
        self.weiboGetNum = 0  # 爬取到的微博数
        self.following = 0  # 用户关注数
        self.followers = 0  # 用户粉丝数
        self.MId=[]#微博消息标识
        self.content = []  # 微博内容
        self.link=[] #微博配图链接
        self.num_like = []  # 微博对应的点赞数
        self.num_transmit = []  # 微博对应的转发数
        self.num_comment = []  # 微博对应的评论数

    # 获取目标基本信息
    def getBasicInfo(self):
        try:
            #用户昵称
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            url = 'http://weibo.cn/%d/info' % (self.user_id)
            html = requests.get(url, cookies=weibo.cookie).content
            selector = etree.HTML(html)
            userName = selector.xpath("//title/text()")[0]
            self.userName = userName[:-3].encode('utf-8')
            print '用户昵称：' + self.userName

            url = 'http://weibo.cn/u/%d?filter=%d&page=1' % (self.user_id, self.filter)
            html = requests.get(url, cookies=weibo.cookie).content
            selector = etree.HTML(html)
            pattern = r"\d+\.?\d*"

            # 微博数
            str_wb = selector.xpath("//div[@class='tip2']/span[@class='tc']/text()")[0]
            guid = re.findall(pattern, str_wb, re.S | re.M)
            for value in guid:
                num_wb = int(value)
                break
            self.weiboNum = num_wb
            print '微博数: ' + str(self.weiboNum)

            # 关注数
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)
            self.following = int(guid[0])
            print '关注数: ' + str(self.following)

            # 粉丝数
            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)
            self.followers = int(guid[0])
            print '粉丝数: ' + str(self.followers)
            print "===================================="
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    # 获取用户前200粉丝
    def getFans(self):
        try:
            idList = []
            for index in range(1,21):
                url = 'http://weibo.cn/%s/fans?page=%d'%(self.user_id,index)
                html = requests.get(url, cookies=weibo.cookie).content
                #   print re.findall(r"http://weibo.cn/u/\d{10}", html)
                soup = BeautifulSoup(html.decode("utf-8", 'ignore'), "lxml")
                fans=soup.find_all(href=re.compile("http://weibo.cn/u/(\d{10})"))
                pattern=re.compile(r"\d{10}")
                for item in fans:
                    newid=pattern.search(str(item),0).group(0)
                    idList.append(newid)
            idList = list(set(idList))
            #   print   idList
            try:
                # 打开数据库连接
                db = mdb.connect("182.254.246.75", "testuser", "mysqltest", "test_spider")
                # 使用cursor()方法获取操作游标
                cur= db.cursor()
                # SQL 插入语句
                insertSQL= "INSERT INTO test_spider.fans(id_fans) VALUES(%s)"
                cur.executemany(insertSQL,idList)
                # 关闭数据库连接
                db.commit()
                cur.close()
                db.close()
            except mdb.Error, e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            print len(idList)

        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    #获取SHU每条微博的详细信息,例如文字内容、图片连接、评论数、点赞数、转发数、评论人、点赞人、转发人
    def getItemsDetail(self):
        try:
            url = 'http://weibo.cn/u/%d?filter=%d&page=1' % (self.user_id, self.filter)
            html = requests.get(url, cookies=weibo.cookie).content
            selector = etree.HTML(html)
            if selector.xpath('//input[@name="mp"]') == []:
                pageNum = 1
            else:
                pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
            pattern = r"\d+"
            print "微博消息总页数："+str(pageNum)
            oldPage = 0
            for page in range(1,pageNum+1):
                url2 = 'http://weibo.cn/u/%d?filter=%d&page=%d' % (self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=weibo.cookie).content

                r0 = re.findall(r'<div class="c" id="M_[a-zA-Z0-9]{9}"', html2)
                r1 = re.findall(r'M_[a-zA-Z0-9]{9}', str(r0))
                for item in r1:
                    self.MId.append(str(item)[2:])

                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                # print len(info)
                if len(info) > 3:
                    for i in range(0, len(info) - 2):
                        self.weiboGetNum = self.weiboGetNum + 1
                        # 微博内容
                        str_t = info[i].xpath("div/span[@class='ctt']")
                        weibos = str_t[0].xpath('string(.)').encode('utf-8', 'ignore')
                        self.content.append(weibos)
                        # print '微博内容：'+ weibos
                        # 微博图片链接
                        str_href = info[i].xpath("div/a/@href")[0]
                        if 'pic' not in str_href:
                            str_href = ""
                        self.link.append(str(str_href))
                        # print '图片链接：' + str_href
                        # 点赞数
                        str_zan = info[i].xpath("div/a/text()")[-4]
                        guid = re.findall(pattern, str_zan, re.M)
                        num_zan = int(guid[0])
                        self.num_like.append(num_zan)
                        # print '点赞数: ' + str(num_zan)
                        # 转发数
                        forwarding = info[i].xpath("div/a/text()")[-3]
                        guid = re.findall(pattern, forwarding, re.M)
                        num_forwarding = int(guid[0])
                        self.num_transmit.append(num_forwarding)
                        # print '转发数: ' + str(num_forwarding)
                        # 评论数
                        comment = info[i].xpath("div/a/text()")[-2]
                        guid = re.findall(pattern, comment, re.M)
                        num_comment = int(guid[0])
                        self.num_comment.append(num_comment)
                        # print '评论数: ' + str(num_comment)
                if page % 4 == 0:
                    print page
                    param = []
                    for i in range(oldPage, self.weiboGetNum):
                        param.append(
                            [self.MId[i], self.content[i], self.link[i], self.num_like[i], self.num_comment[i],
                             self.num_transmit[i]])
                    try:
                        # 打开数据库连接
                        db = mdb.connect("182.254.246.75", "testuser", "mysqltest", "test_spider", charset='utf8')
                        # 使用cursor()方法获取操作游标
                        cur = db.cursor()
                        # SQL 插入语句
                        insertSQL = "INSERT IGNORE INTO test_spider.news(newsid,content,piclink,attinum,cmtnum,repostnum) VALUES(%s,%s,%s,%s,%s,%s)"
                        cur.executemany(insertSQL, param)
                        # 关闭数据库连接
                        db.commit()
                        cur.close()
                        db.close()
                        print "插入成功"
                        oldPage = self.weiboGetNum
                    except mdb.Error, e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            param = []
            for i in range(oldPage, self.weiboGetNum):
                param.append(
                    [self.MId[i], self.content[i], self.link[i], self.num_like[i], self.num_comment[i],
                     self.num_transmit[i]])
            try:
                # 打开数据库连接
                db = mdb.connect("182.254.246.75", "testuser", "mysqltest", "test_spider", charset='utf8')
                # 使用cursor()方法获取操作游标
                cur = db.cursor()
                # SQL 插入语句
                insertSQL = "INSERT IGNORE INTO test_spider.news(newsid,content,piclink,attinum,cmtnum,repostnum) VALUES(%s,%s,%s,%s,%s,%s)"
                cur.executemany(insertSQL, param)
                # 关闭数据库连接
                db.commit()
                cur.close()
                db.close()
                print "插入成功"
                oldPage = self.weiboGetNum
            except mdb.Error, e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            if self.filter == 0:
                print '共' + str(self.weiboNum) + '条微博,抓取到' + str(self.weiboGetNum) + '条微博'
            param=[]
            ct=0
            for mid in self.MId:
                ct+=1
                #param 存放id和相关类型，用于插入related表
                #类型1，评论
                #类型2，转发
                #类型3，点赞
                self.weiboGetNum = self.weiboGetNum + 1
                # 获取此消息的评论用户id
                cmturl="http://weibo.cn/comment/" + mid +"?&page=" +'1'
                cmthtml = requests.get(cmturl, cookies=weibo.cookie).content
                # print cmthtml
                cmtnum = 1
                cmtstat=0
                r0 = re.findall(r'1/\d+页', cmthtml)
                if r0 != []:
                    r1 = re.findall(r'\d+', str(r0))
                    cmtnum = int(r1[1])
                #print "评论页"+str(cmtnum)
                r0 = re.findall(r'/attitude/[^/]*/update\?object_type=comment&amp;uid=\d{10}&', cmthtml)
                r1 = re.findall(r'\d{10}', str(r0))
                for item in r1:
                    cmtstat += 1
                    param.append([mid,item,'1'])
                if cmtnum>1:
                    for i in range(2,cmtnum+1):
                        cmturl = "http://weibo.cn/comment/" + mid +"?&page=" + str(i)
                        cmthtml = requests.get(cmturl, cookies=weibo.cookie).content
                        r0 = re.findall(r'/attitude/[^/]*/update\?object_type=comment&amp;uid=\d{10}&', cmthtml)
                        r1 = re.findall(r'\d{10}', str(r0))
                        for item in r1:
                            cmtstat += 1
                            param.append([mid,item,'1'])
                # print "评论数："+str(cmtstat)

                # 获取此消息的转发用户id
                reposturl = "http://weibo.cn/repost/" + mid +"?&page=" + "1"
                reposthtml = requests.get(reposturl, cookies=weibo.cookie).content
                repostnum = 1
                repoststat=0
                r0 = re.findall(r'1/\d+页', reposthtml)
                if r0 != []:
                    r1 = re.findall(r'\d+', str(r0))
                    repostnum = int(r1[1])
                #print "转发页"+str(repostnum)
                r0 = re.findall(r'<a href=\"/u/\d{10}\">', reposthtml)
                r1 = re.findall(r'\d{10}', str(r0))
                repostlen = len(r1)
                for item in range(1, repostlen):
                    param.append([mid,r1[item],'2'])
                    repoststat+=1
                if repostnum > 1:
                    for i in range(2, repostnum + 1):
                        reposturl = "http://weibo.cn/repost/" + mid +"?&page=" + str(i)
                        reposthtml = requests.get(reposturl, cookies=weibo.cookie).content
                        r0 = re.findall(r'<a href=\"/u/\d{10}\">', reposthtml)
                        r1 = re.findall(r'\d{10}', str(r0))
                        for item in r1:
                            param.append([mid,item, '2'])
                            repoststat += 1

                # print "转发数："+str(repoststat)

                # 获取此消息的点赞用户id
                atturl="http://weibo.cn/attitude/"+mid+"?&page="+'1'
                atthtml = requests.get(atturl, cookies=weibo.cookie).content
                attnum = 1
                attstat=0
                r0 = re.findall(r'1/\d+页', atthtml)
                if r0 != []:
                    r1 = re.findall(r'\d+', str(r0))
                    attnum = int(r1[1])
                #print "点赞页"+str(attnum)
                r0 = re.findall(r'<a href=\"/u/\d{10}\">', atthtml)
                r1 = re.findall(r'\d{10}', str(r0))
                attlen = len(r1)
                for item in range(1, attlen):
                    attstat+=1
                    param.append([mid,r1[item], '3'])
                if attnum>1:
                    for i in range(2,attnum+1):
                        atturl = "http://weibo.cn/attitude/" + mid +"?&page=" + str(i)
                        atthtml = requests.get(atturl, cookies=weibo.cookie).content
                        r0 = re.findall(r'<a href=\"/u/\d{10}\">', atthtml)
                        r1 = re.findall(r'\d{10}', str(r0))
                        for item in r1:
                            attstat += 1
                            param.append([mid,item, '3'])
                # print "点赞数："+str(attstat)
                # print "=================="

                if ct%4 == 0:
                    try:
                        # 打开数据库连接
                        db = mdb.connect("182.254.246.75", "testuser", "mysqltest", "test_spider",charset='utf8')
                        # 使用cursor()方法获取操作游标
                        cur = db.cursor()
                        # SQL 插入语句
                        insertSQL = "INSERT IGNORE INTO test_spider.related(newsid,userid,type) VALUES(%s,%s,%s)"
                        cur.executemany(insertSQL, param)
                        # 关闭数据库连接
                        db.commit()
                        cur.close()
                        db.close()
                        print "插入成功"
                        param = []
                    except mdb.Error, e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            try:
                # 打开数据库连接
                db = mdb.connect("182.254.246.75", "testuser", "mysqltest", "test_spider", charset='utf8')
                # 使用cursor()方法获取操作游标
                cur = db.cursor()
                # SQL 插入语句
                insertSQL = "INSERT IGNORE INTO test_spider.related(newsid,userid,type) VALUES(%s,%s,%s)"
                cur.executemany(insertSQL, param)
                # 关闭数据库连接
                db.commit()
                cur.close()
                db.close()
                print "插入成功"
                param = []
            except mdb.Error, e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            if self.filter == 0:
                print '共抓取到'+str(len(self.MId))+'条微博,抓取到' + str(ct) + '条微博详细条目'

        except Exception, e:
            print "Error: ", e
            traceback.print_exc()
    # 获取用户微博内容、图片链接、对应的点赞数、转发数、评论数
    def getWeiboItems(self):
        try:
            url = 'http://weibo.cn/u/%d?filter=%d&page=1' % (self.user_id, self.filter)
            html = requests.get(url, cookies=weibo.cookie).content
            selector = etree.HTML(html)
            if selector.xpath('//input[@name="mp"]') == []:
                pageNum = 1
            else:
                pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
            pattern = r"\d+"
            print "微博消息总页数："+str(pageNum)
            oldPage=0
            for page in range(1,pageNum+1):
                url2 = 'http://weibo.cn/u/%d?filter=%d&page=%d' % (self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=weibo.cookie).content

                r0 = re.findall(r'<div class="c" id="M_[a-zA-Z0-9]{9}"', html2)
                r1 = re.findall(r'M_[a-zA-Z0-9]{9}', str(r0))
                for item in r1:
                    # print item
                    self.MId.append(str(item))

                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                # print len(info)
                if len(info) > 3:
                    for i in range(0, len(info) - 2):
                        self.weiboGetNum = self.weiboGetNum + 1
                        # 微博内容
                        str_t = info[i].xpath("div/span[@class='ctt']")
                        weibos = str_t[0].xpath('string(.)').encode('utf-8', 'ignore')
                        self.content.append(weibos)
                        #print '微博内容：'+ weibos
                        # 微博图片链接
                        str_href = info[i].xpath("div/a/@href")[0]
                        if 'pic' not in str_href:
                            str_href=""
                        self.link.append(str(str_href))
                        #print '图片链接：' + str_href
                        # 点赞数
                        str_zan = info[i].xpath("div/a/text()")[-4]
                        guid=[]
                        guid = re.findall(pattern, str_zan, re.M)
                        num_zan = int(guid[0])
                        self.num_like.append(num_zan)
                        #print '点赞数: ' + str(num_zan)
                        # 转发数
                        forwarding = info[i].xpath("div/a/text()")[-3]
                        guid = re.findall(pattern, forwarding, re.M)
                        num_forwarding = int(guid[0])
                        self.num_transmit.append(num_forwarding)
                        #print '转发数: ' + str(num_forwarding)
                        # 评论数
                        comment = info[i].xpath("div/a/text()")[-2]
                        guid = re.findall(pattern, comment, re.M)
                        num_comment = int(guid[0])
                        self.num_comment.append(num_comment)
                        # print '评论数: ' + str(num_comment)
                if page%2 == 0:
                    print page
                    param=[]
                    for i in range(oldPage,self.weiboGetNum):
                        param.append([self.MId[i],self.content[i],self.link[i],self.num_like[i],self.num_comment[i],self.num_transmit[i]])
                    try:
                        # 打开数据库连接
                        db = mdb.connect("182.254.246.75", "testuser", "mysqltest", "test_spider",charset='utf8')
                        # 使用cursor()方法获取操作游标
                        cur = db.cursor()
                        # SQL 插入语句
                        insertSQL = "INSERT INTO test_spider.news(id_news,words,picture,like_num,mark_num,transmit_num) VALUES(%s,%s,%s,%s,%s,%s)"
                        cur.executemany(insertSQL, param)
                        # 关闭数据库连接
                        db.commit()
                        cur.close()
                        db.close()
                        print "插入成功"
                        oldPage=self.weiboGetNum
                    except mdb.Error, e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            if self.filter == 0:
                print '共'+str(self.weiboNum)+'条微博,抓取到' + str(self.weiboGetNum) + '条微博'
            else:
                print '共' + str(self.weiboNum) + '条微博，其中' + str(self.weiboNum2) + '条为原创微博'
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    # 主程序
    def start(self):
        try:
            weibo.getBasicInfo(self)
            #weibo.getWeiboItems(self)
            weibo.getItemsDetail(self)
            print '==============================\n信息抓取完毕'
        except Exception, e:
            print "Error: ", e


# 使用实例,输入一个用户id，所有信息都会存储在wb实例中
user_id =3243026514#2711257087 可以改成任意合法的用户id（爬虫的微博id除外）
wb = weibo(user_id, filter)  # 调用weibo类，创建微博实例wb
wb.start()  # 爬取微博信息
