# coding=utf-8
import threading
import time

print(time.ctime())


def music(name, year):
    for i in range(3):
        print("muisc name is {0}.year is {1}.{2}".format(name, year, time.ctime()))
        time.sleep(2)


def move(name):
    for i in range(5):
        print("move name is {0}.{1}".format(name, time.ctime()))
        time.sleep(2)


def test(name):
    while True:
        print("test")
        time.sleep(1)


threads = []

t1 = threading.Thread(target=music, args=("love", "1995",))  # 注意args后面有（）里面还有逗号,
threads.append(t1)
t2 = threading.Thread(target=move, args=("hit",))
threads.append(t2)
t3 = threading.Thread(target=test, args=("hit",))
threads.append(t3)

if __name__ == '__main__':
    for thread in threads:
        # thread.setDaemon(True)
        thread.start()
    print("program over")
