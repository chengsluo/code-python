from urllib import robotparser

rb=robotparser.RobotFileParser(url='')
rb.set_url('http://www.baidu.com/robots.txt')
rb.read() #必须先调用read()表示读取分析
