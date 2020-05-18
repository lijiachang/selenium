# coding=utf-8

import http.client
import requests
import sys
import time
import random

reload(sys)
sys.setdefaultencoding("utf-8")
print("**********************************")
print(u"******** 京东闪付-5元低保 ********")
print("**********************************")

PAGE10 = r"https://pa.jd.com/prize/center/h5/draw?entranceKey=b183f8bdcc5077fe87d813847047e95b"
PAGE14 = r"https://pa.jd.com/prize/center/h5/draw?entranceKey=8581c41185dbd6e9e8c13a2c744d4636"
PAGE20 = r"https://pa.jd.com/prize/center/h5/draw?entranceKey=f513f407cdb3a7b675f2ac13b00b56a2"

def get_webtime(host):
    conn = http.client.HTTPConnection(host)
    conn.request("GET", "/")
    r = conn.getresponse()
    ts = r.getheader('date')  # 获取http头date部分
    # 将GMT时间转换成北京时间
    ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    ttime = time.localtime(time.mktime(ltime) + 8 * 60 * 60)
    tm = "%02u:%02u:%02u" % (ttime.tm_hour, ttime.tm_min, ttime.tm_sec)
    return tm


print(u"京东时间" + get_webtime('www.jd.com'))
print(u"本机时间" + time.strftime('%H:%M:%S', time.localtime(time.time())))

# Cookies
try:
    cookie_source = open("cookie.txt").readline()
    # 处理cookies
    cookie = {}
    for line in cookie_source.split(';'):
        name, value = line.strip().split('=', 1)
        cookie[name] = value
except:
    print(u"请检查Cookie.txt文件！")
    time.sleep(-1)


def update_data(PAGE):
    html = requests.get(PAGE, cookies=cookie)
    return html.text
    # soup = BeautifulSoup(html.text, "html.parser")
    # return soup.text

if "-99999" in update_data(PAGE10):
    print(u"Cookie无效或过期，请检查！")
    time.sleep(-1)
else:
    print(u"Cookie检查：OK")


while True:
    now = time.strftime('%H.%M', time.localtime(time.time()))
    #print(now)
    if now == "10.00":
        result = update_data(PAGE10)
        if "今日已领取" in result:
            print(u"10.00 领取成功！")
            time.sleep(60)
        if "登录后才可以领奖" in result:
            print(u"Cookie 已失效，请重新提取！")
            time.sleep(60)
    if now == "14.00":
        result = update_data(PAGE14)
        if "今日已领取" in result:
            print(u"14.00 领取成功！")
            time.sleep(60)
        if "登录后才可以领奖" in result:
            print(u"Cookie 已失效，请重新提取！")
            time.sleep(60)
    if now == "20.00":
        result = update_data(PAGE20)
        if "今日已领取" in result:
            print(u"20.00 领取成功！")
            time.sleep(60)
        if "登录后才可以领奖" in result:
            print(u"Cookie 已失效，请重新提取！")
            time.sleep(60)

    time.sleep(1)
