#!/usr/bin/python
# coding:utf-8
# 2019.12.16

import requests
from bs4 import BeautifulSoup
import sys
import time
import random

reload(sys)
sys.setdefaultencoding("utf-8")
print("**********************************")
print(u"******** 富贵拍卖-自动出价 ********")
print("**********************************")
print(u"输入帖子链接地址")
PAGE = raw_input("URL:")  # 帖子URL
print(u"输入能接受的最高的价格")
MY_PRICE = int(raw_input("Price:"))  # 能接受的最高价格

#PAGE = "https://www.fglt.net/forum.php?mod=viewthread&tid=4030306"
USER = str()  # 当前登录用户
tid = PAGE.split('&tid=')[1].split('&')[0]  # 帖子tid
formhash = str()  # 提交表格hash值，区别帖子
html_max_bid_user = str()  # 当前最高出价用户
html_max_bid = str()  # 当前最高出价
time_left = 0  # 帖子拍卖剩余时间（倒计时） 单位：秒



# Cookies
cookie_source=open("cookie.txt").readline()
# 处理cookies
cookie = {}  # 传入的cookies参数应该是字典
for line in cookie_source.split(';'):
    name, value = line.strip().split('=', 1)  # 其设置为1就会把字符串拆分成2份
    cookie[name] = value


# 获取拍卖帖，解析，获取具体数据
def update_data():
    global USER, html_max_bid, html_max_bid_user, formhash, time_left  # 函数体内使用全局变量
    html = requests.get(PAGE, cookies=cookie)
    soup = BeautifulSoup(html.text, "html.parser")

    USER = soup.find_all('strong', attrs={'class': 'vwmy qq'})[0].a.get_text()
    print u"登录用户名:", USER

    html_max_bid = soup.find_all('td', attrs={'class': 'list_lt'})[2].get_text()
    # print "当前最高出价：", html_max_bid  # 取到当前的最高出价

    html_max_bid_user = soup.find_all('td', attrs={'class': 'list_lt'})[0].a.get_text()
    print u"当前最高出价用户：", html_max_bid_user, u"当前最高出价：", html_max_bid

    # 根据帖子页面剩余时间，判读出价结束;  根据em标签内unicode值： 结束： \r\n\r\n\u5df2\u7ecf\u7ed3\u675f  未结束：\n
    judge_times_over = soup.find_all('em', attrs={'id': 'timeleft'})[0].get_text()
    if judge_times_over == u"\r\n\r\n\u5df2\u7ecf\u7ed3\u675f":
        time_left = 0
    elif judge_times_over == u"\n":
        time1 = soup.find_all('div', attrs={'class': 'aucdetail'})[
            0].dl.li.script.get_text()  # 获取包含timeleft值的整个javascript
        time_left = int(str(time1).split(";")[0].split("= ")[1])  # 截取出数值
        print u"拍卖剩余时间", time_left, u"秒"
    else:
        print(u"未知错误，不能判断结束。。")

    html_formhash = soup.find_all('input', attrs={'type': 'hidden', 'name': 'formhash'})
    formhash = str(html_formhash[0].get('value'))  # 获取到当前用户的formhash


# 开始出价
def go_bid():
    # 获取出价页面，解析
    bid_page = "".join(['https://www.fglt.net/plugin.php?id=xm_task_20130503:main&tid=', tid, '&operation=join'])
    html_bid_page = requests.get(bid_page, cookies=cookie)
    soup_bid_page = BeautifulSoup(html_bid_page.text, "html.parser")

    bid = str(soup_bid_page.find_all('input', attrs={'type': 'text', 'id': 'price'})[0].get('value'))  # 获取页面系统出价
    print u"将要出价：", bid

    # ##########发送POST请求，进行出价########################

    # 出价请求头
    headers = {'Host': 'www.fglt.net',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',

               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding': 'gzip, deflate, br',
               'Referer': bid_page,
               'Content-Type': 'application/x-www-form-urlencoded',
               'Content-Length': '135',
               'Cookie': cookie_source,
               'DNT': '1',
               'Connection': 'keep-alive',
               'Upgrade-Insecure-Requests': '1',
               'authority': 'www.fglt.net',
                'method': 'POST',
                'path': '/plugin.php?id=xm_task_20130503:main&tid=%s&operation=join' % tid,
                'scheme': 'https',
                'accept': 'text/html,application/xhtml+xml, application/xml;q=0.9, image/webp, image/apng, */*;q=0.8',
                'cache-control': 'max-age=0',
               'origin': 'https://www.fglt.net',
               'upgrade-insecure-requests': '1'
               }

    # 请求主体
    data = {'formhash': formhash, 'price': bid,
            'auc_reply_message': 'zhichi le',
            'confirmsubmit': 'true'}

    # post请求，出价操作，（返回出价成功界面）
    post_page = requests.post(bid_page, headers=headers, data=data)
    #print post_page.text

    # 判断出价成功
    update_data()
    if html_max_bid_user == USER:
        print u"出价成功：", html_max_bid
    else:
        soup_bid = BeautifulSoup(post_page.text, "html.parser")
        print soup_bid.find_all('div', attrs={'class': 'alert_info'})[0].p.get_text()
        print u"出价失败!!!"


update_data()

while time_left > 0:
    update_data()
    if html_max_bid_user != USER and int(html_max_bid) <= MY_PRICE:
        print(u"将开始出价：")
        go_bid()
        time.sleep(time_left - random.randint(60, 120))  # 在拍卖剩余时间里 最后几分钟出价（随机数决定，防止使用固定数太有出价规律）
    elif html_max_bid_user == USER:
        print(u"您已经是最高价~~")
        time.sleep(abs(time_left - 3))  # 在最后3秒内 确认我还是最高价;取绝对值，最后2秒时 防止2-3=-1  sleep(-1)无限时间
        update_data()
        if html_max_bid_user != USER and int(html_max_bid) <= MY_PRICE:
            go_bid()
    else:
        print u"已经超出预算价格，停止出价，当前价格：", str(html_max_bid)
        # break
        time.sleep(time_left + 10)

else:
    # update_data()
    print(u"****拍卖已经结束:")
    print u"****拍得的用户：", html_max_bid_user, u"出价：", html_max_bid
    time.sleep(-1)

# ：：：：：：：：：：暂时用不到的代码：：：：：：：：：：

# # 根据出价界面，判断拍卖是否结束！   暂时不考虑《拍卖未进行》
# auction_is_over = soup_bid_page.find('div', attrs={'id': 'messagetext', 'class': 'alert_error'})
# # print(auction_is_over)
# 输出：最近出价记录
# for item in html_items:
#     print item.get_text()
