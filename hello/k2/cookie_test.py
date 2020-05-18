# coding:utf-8

import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

product_id = "13"  # k2:5  插座:24  秤12 电视盒子13
useVcNum = '29900' # 秤23900  路由16000 电视盒子29900
cookie_init = "_VMC_UID=b3d6ef49d5f0bf1cfd119f3fe3a485b2; __jsluid=16f7e4928b42bd0da401fa1333a992fc; _SID=2d529bb97d800706d8abe1ff9c526c2a; Hm_lvt_c8bb97be004001570e447aa3e00ff0ad=1537844187; UNAME=17611233002; MEMBER_IDENT=4261380; MEMBER_LEVEL_ID=1; CACHE_VARY=e76127a48966f4f17c6d13f3540adbc9-0f063e018c840f8a56946ecec41a6c18; Hm_lpvt_c8bb97be004001570e447aa3e00ff0ad=1537844198"

# 处理cookies
cookie = {}  # 传入的cookies参数应该是字典
for line in cookie_init.split(';'):
    name, value = line.strip().split('=', 1)  # 其设置为1就会把字符串拆分成2份
    cookie[name] = value

MEMBER_IDENT = cookie["MEMBER_IDENT"]  # 用户数字ID
get_image_url = r"https://mall.phicomm.com/vcode-index-passport{0}.html?d=0.6663294782495152".format(MEMBER_IDENT)  # 获取验证码地址
buy_url = r"https://mall.phicomm.com/order-create-is_fastbuy.html"  # 提交订单地址



url = "https://mall.phicomm.com/passport-post_login.html"

# post 请求头
headers = {'Host': 'mall.phicomm.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Accept-Encoding': 'gzip, deflate, br',
           'Referer': 'https://mall.phicomm.com/passport-login.html',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Content-Length': '47',
           'Origin': 'https://mall.phicomm.com',
           'Connection': 'keep-alive',
           'X-Requested-With': 'XMLHttpRequest'
           }


data = {'forward': "", 'uname': "17633228484", 'password': 'tzj871003'}


# 提交订单请求
post_page = requests.post(url, headers=headers, data=data)
print post_page.text.decode("unicode-escape")
print post_page.cookies
print post_page.cookies.get_dict()
