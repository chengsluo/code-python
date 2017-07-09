import xlwt
book = xlwt.Workbook()
sheet1 = book.add_sheet('Sheet 1')  #添加一个sheet
sheet2= book.add_sheet('Sheet 2')
sheet2.write(0,0,'已抓取粉丝网页数')   #通过sheet添加cell值
sheet2.write(0,1,'已抓取粉丝数')
sheet2.write(1,0,'1')
sheet2.write(1,1,'0')

firstline=['粉丝id号', '粉丝昵称', '关注他人数', '已有粉丝数', '发布微博数', '地域']
for i in range(0,6):
    sheet1.write(0, i,firstline[i])
book.save('微博粉丝参与记录.xls')
