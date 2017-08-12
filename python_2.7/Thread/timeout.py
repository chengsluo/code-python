import threading
import time
def func1(x, y):
    for i in range(x,y):
        print (i)
    # time.sleep(10)

t1=threading.Thread(target=func1,args=(100,200)) # 线程定义
t1.start() # 线程启动
# t1.join(5) #阻塞当前线程，等待线程结束或超时返回
t2=threading.Thread(target=func1, args=(5,50))
t2.start()
t2.join()
print('t1',t1.isAlive())
print('t2',t2.isAlive())