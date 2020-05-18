# coding=utf-8

import threading


def printf(p):
    print(p)


ts = list()

for i in xrange(0, 10):
    th = threading.Thread(target=printf(i))
    ts.append(th)

for i in ts:
    i.start()

# for i in ts:
#     i.join()

printf("end !!!")

from time import ctime
import time

printf(ctime())


# 不使用多线程 用时4s
def a():
    print("a bengin")
    time.sleep(2)
    print("a end")


def b():
    print("b bengin")
    time.sleep(2)
    print("b end")


bengin_time = time.time()
a()
b()
print(time.time() - bengin_time)


# 使用多线程 用时2s
def a():
    print("a bengin")
    time.sleep(2)
    print("a end")


def b():
    print("b bengin")
    time.sleep(2)
    print("b end")


bengin_time = time.time()

t = list()
t.append(threading.Thread(target=a))
t.append(threading.Thread(target=b))
for i in t:
    i.start()
for i in t:
    i.join()
print(time.time() - bengin_time)


#协程： yield生成器，包含yield的函数，就是一个可迭代对象
def test():
    i = 0
    a = 4
    while i < a:
        yield i
        i += 1

for i in test():
    print i

