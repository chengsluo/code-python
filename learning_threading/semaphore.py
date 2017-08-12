import time
from random import random
from threading import Thread, Semaphore
sema = Semaphore(3)
# 信号量同步基于内部计数器，每调用一次acquire()，计数器减1；
# 每调用一次release()，计数器加1.当计数器为0时，acquire()调用被阻塞。

def foo(tid):
    with sema:
        print ('{} acquire sema'.format(tid))
        wt = random() * 2
        time.sleep(wt)
    print ('{} release sema'.format(tid))
threads = []
for i in range(5):
    t = Thread(target=foo, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
