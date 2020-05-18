#!/usr/bin/python
# coding:utf-8
# 2019.12.30

import requests
from bs4 import BeautifulSoup
import time

import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
import sys

reload(sys)
sys.setdefaultencoding('utf8')

PAGE = "http://shop.cgbchina.com.cn/mall/goods/03140714143403208122?itemCode=03140714143403208122"


def update():
    html = requests.get(PAGE, allow_redirects=False)  # 默认allow_redirects=True是启动重定向
    soup = BeautifulSoup(html.text, "html.parser")
    icon_sold_out = soup.find_all('div', attrs={'class': 'icon-item-state icon-sold-out stock-zero-img'})

    # print icon_sold_out

    if icon_sold_out:
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "没货"
    else:
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "------有货"
        email()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "邮件已发送"
        time.sleep(1800)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "继续监测"


def email():
    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = 'diy_admin@126.com'
    password = 'diydiy123'
    # 收信方邮箱
    # to_addr = '123123@qq.com'
    # 抄送

    # 发信服务器
    smtp_server = 'smtp.126.com'

    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL()
    server.connect(smtp_server)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 整理接收人
    adds = []
    with open('email_addrs.txt', 'r') as addrs:
        for addr in addrs:
            adds.append(addr.strip())

    # 126免费邮箱每次只能发40收件人，分39人为一组
    # 优雅地将list分组
    addrs_groups = [adds[i:i + 39] for i in xrange(0, len(adds), 39)]

    # 39人一组，分别发送
    for one_addrs in addrs_groups:
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText(
            'DIY有货了，兑换地址：http://shop.cgbchina.com.cn/mall/goods/03140714143403208122?itemCode=03140714143403208122',
            'plain', 'utf-8')
        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['Cc'] = Header(from_addr)
        msg['Subject'] = Header('>>>>DIY签账额----有货<<<<', 'utf-8')
        # msg['Subject'] = Header('测试的，忽略', 'utf-8')
        msg['To'] = ','.join(one_addrs)

        # 发送邮件
        try:
            server.sendmail(from_addr, msg['To'].split(','), msg.as_string())
        except Exception as e:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "email发送失败：", one_addrs
            print e

            # 解决多次发送。连接被关闭问题
            if "Connection unexpectedly closed" in e:
                i = 0
                while True:
                    i += 1
                    if i == 20:
                        print "重连20次都是失败！"
                        break
                    server = smtplib.SMTP_SSL()
                    server.connect(smtp_server)
                    server.login(from_addr, password)
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "server服务已重连！"
                    time.sleep(1)
                    # 再次发送
                    try:
                        server.sendmail(from_addr, msg['To'].split(','), msg.as_string())
                        print time.strftime('%Y-%m-%d %H:%M:%S',
                                            time.localtime(time.time())), "---email发送成功！！！：", one_addrs
                        break
                    except Exception as e:
                        print "再次发送失败...."
                        print e
                        continue


        else:
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "---email发送成功！！！：", one_addrs

        time.sleep(1)

    # 关闭服务器
    server.quit()


while True:
    update()
    time.sleep(10)
