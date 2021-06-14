# coding=utf-8
# 生产者：采集分析
import threading
import inspect
import time

domains = [p for p in xrange(5)]

def get_title(x):
    time.sleep(1)
    print inspect.stack()[0][3], '-->', x


def domain_crawl(d, sss):
    for x in d:
        print inspect.stack()[0][3], '-->', x

        t_get_title = threading.Thread(target=get_title, args=(x,))
        t_get_title.start()

        time.sleep(2)

        t_get_title.join()


def domain_crawl2(d):
    for x in d:
        print inspect.stack()[0][3], '---->', x
        time.sleep(3)

s = '123'

t1 = threading.Thread(target=domain_crawl, args=(domains, s))
t1.start()

# 消费者：记录符合的域名
t2 = threading.Thread(target=domain_crawl2, args=(domains,))
t2.start()
