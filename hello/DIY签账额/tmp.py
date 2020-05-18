
# coding:utf-8
# 2019.12.19

import requests
from bs4 import BeautifulSoup
import time

# 126免费邮箱每次只能发40收件人
import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
import sys

reload(sys)
sys.setdefaultencoding('utf8')
adds = []

with open('email_addrs.txt', 'r') as addrs:
    for addr in addrs:
        adds.append(addr.strip())

# for s in adds:
#     print s
#
#
# a=adds
# for i in range(0,len(a),39):
#     b=a[i:i+39]
#     print b
# # 优雅地将list分组
# print [a[i:i+39] for i in xrange(0,len(a),39)]

msg = MIMEText(
        'DIY有货了，兑换地址：http://shop.cgbchina.com.cn/mall/goods/03140714143403208122?itemCode=03140714143403208122',
        'plain', 'utf-8')
msg['To'] = ','.join(adds)
print msg

msg = MIMEText(
    'DIY有货了，兑换地址：http://shop.cgbchina.com.cn/mall/goods/03140714143403208122?itemCode=03140714143403208122',
    'plain', 'utf-8')
msg['To'] = ','.join(adds)
print msg