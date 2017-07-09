#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 对于特殊字符难以识别和支持
import tablib

headers = ('area', 'user', 'recharge')
data = [
    ('1', 'Rooney', 20),
    ('2', 'John', 30),
]
data = tablib.Dataset(*data, headers=headers)

# 然后就可以通过下面这种方式得到各种格式的数据了。
data.xlsx
data.xls
data.ods
data.json
data.yaml
data.csv
data.tsv
data.html

# 增加行
data.append(['3', 'Keven', 18])
# 增加列
data.append_col([22, 20, 13], header='Age')
print data.csv

# 删除行
del data[1:3]
# 删除列
del data['Age']
print data.csv

#导出excel表
open('xxx.xls', 'wb').write(data.xls)

#注意，因为excel表有二进制数据，所以必须要用二进制模式打开文件，即'wb'。

#多个sheet的excel表
book = tablib.Databook((data, data, data))
book.xls
