from selenium import webdriver

debug = True

web_driver = webdriver.Chrome("/Users/Carlton/chromedriver")
log_path = '/Users/Carlton/Log/taobao_spider.log'


class DB:
    host = 'localhost'
    user_name = 'root'
    password = '123456'
    db_name = 'tb'

