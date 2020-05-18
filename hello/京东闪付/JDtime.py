# coding=utf-8
import http.client
import time
import os


def get_webtime(host):
    conn = http.client.HTTPConnection(host)
    conn.request("GET", "/")
    r = conn.getresponse()
    # r.getheaders() #获取所有的http头
    ts = r.getheader('date')  # 获取http头date部分
    # 将GMT时间转换成北京时间
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    ttime=time.localtime(time.mktime(ltime)+8*60*60)
    tm="%02u:%02u:%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
    print (tm)




get_webtime('www.baidu.com')
print(time.strftime('%H:%M:%S', time.localtime(time.time())))