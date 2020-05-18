#coding:utf-8
import time
import httplib


def get_webtime(host):
    conn = httplib.HTTPConnection(host)
    conn.request("GET", "/")
    r = conn.getresponse()
    ts = r.getheader('date')  # 获取http头date部分
    # 将GMT时间转换成北京时间
    ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    ttime = time.localtime(time.mktime(ltime) + 8 * 60 * 60)
    tm = "%02u:%02u:%02u" % (ttime.tm_hour, ttime.tm_min, ttime.tm_sec)
    return tm

while True:
    print get_webtime("mall.phicomm.com")
    time.sleep(1)