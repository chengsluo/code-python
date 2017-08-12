#coding =utf-8
from urllib import parse

#解析
result=parse.urlparse('http://www.baidu.com/index.html;user?id=5#comment')
print(type(result),result,sep='\n')
print(result.scheme,result[2],result.netloc,result[4],sep='\n')

#打包，必须要有6个参数
data=['http','www.baidu.com','index.html','user','a=6','comment']
print(parse.urlunparse(data))
#http://www.baidu.com/index.html;user?a=6#comment

#解析无path
result=parse.urlsplit('http://www.baidu.com/index.html;user?id=5#comment')
print(result)
#打包，参数为5，同上
data	=	['http',	'www.baidu.com',	'index.html',	'a=6',	'comment']
print(parse.urlunsplit(data))

#url连接
print(parse.urljoin('http://www.baidu.com',	'FAQ.html'))
print(parse.urljoin('http://www.baidu.com',	'https://cuiqingcai.com/FAQ.html'))
print(parse.urljoin('http://www.baidu.com/about.html',	'https://cuiqingcai.com/FAQ.html'))
print(parse.urljoin('http://www.baidu.com/about.html',	'https://cuiqingcai.com/FAQ.html?question=2'))
print(parse.urljoin('http://www.baidu.com?wd=abc',	'https://cuiqingcai.com/index.php'))
print(parse.urljoin('http://www.baidu.com',	'?category=2#comment'))
print(parse.urljoin('www.baidu.com',	'?category=2#comment'))
print(parse.urljoin('www.baidu.com#comment',	'?category=2'))