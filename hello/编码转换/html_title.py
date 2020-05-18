# coding=utf-8

"""
题目1
已知列表 urlinfo = ['http://www.sohu.com','http://www.163.com','http://www.sina.com']
用多线程的方式分别打开列表里的URL，
并且输出对应的网页标题和内容。
"""
import urllib
from bs4 import BeautifulSoup
import threading

urlinfo = ['http://www.sohu.com','http://www.163.com','http://www.sina.com']

def open_url(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html,"html.parser")
    print(soup.title.get_text())
    # print(soup.body)  # 输出网页内容，有点多，影响测试

thrs = list()
if __name__ == "__main__":
    for i in xrange(0,len(urlinfo)):
        thr = threading.Thread(target=open_url,args=[urlinfo[i]])
        thr.start()
        print(thr)
        thrs.append(thr)
    for i in thrs:
        i.join()
    print("end!!!")





