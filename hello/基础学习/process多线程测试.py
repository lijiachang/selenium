# coding=utf-8
# 1.默认情况，Python只能用到一个线程
# from threading import Thread
#
#
# def loop():
#     while True:
#         pass
#
#
# for i in range(12):
#     print "id:", i
#     th = Thread(target=loop)
#     th.start()

# 2.使用multiprocessing模块，利用到多线程,CPU利用率瞬间百分百

from multiprocessing import Process


def loop():
    while True:
        pass


if __name__ == '__main__':
    for i in range(12):
        print "id:", i
        th = Process(target=loop)
        th.start()
