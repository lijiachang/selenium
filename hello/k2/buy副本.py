# coding:utf-8

import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import threading
import time

product_id = "13"  # k2:5  插座:24  秤12 电视盒子13
useVcNum = '29900' # 秤23900  路由16000 电视盒子29900
cookie_init = "from_vshopid=null; __jsluid=d0e1c40d96620bafb93f7c66e3197c4c; _VMC_UID=92dd508272f1a4344f89633452269635; _SID=9062d6dfe61ae686637e9a083b8e5434; Hm_lvt_c8bb97be004001570e447aa3e00ff0ad=1539745050; from_vshopid=43105230377; UNAME=15269026760; MEMBER_IDENT=2523347; MEMBER_LEVEL_ID=2; CACHE_VARY=51e487cac03c44768d32a4809acd0cf4-47587e393d1368226b29aa1662628b0a"






# 处理cookies
cookie = {}  # 传入的cookies参数应该是字典
for line in cookie_init.split(';'):
    name, value = line.strip().split('=', 1)  # 其设置为1就会把字符串拆分成2份
    cookie[name] = value

MEMBER_IDENT = cookie["MEMBER_IDENT"]  # 用户数字ID
get_image_url = r"https://mall.phicomm.com/vcode-index-passport{0}.html?d=0.66432973382495195".format(MEMBER_IDENT)  # 获取验证码地址
buy_url = r"https://mall.phicomm.com/order-create-is_fastbuy.html"  # 提交订单地址

# 获取 cart_md5, addr_id
def get_cart_md5():
    id_url = "https://mall.phicomm.com/cart-fastbuy-{0}-1.html?vsid=43105230377".format(product_id)  # 确定商品ID
    referer = 'https://mall.phicomm.com/item-{0}.html'.format(product_id)
    checkout_url = r"https://mall.phicomm.com/checkout-fastbuy.html"   # 订单确认详情

    # get请求头
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'max-age=0',
               'Connection': 'max-age=0',
               'Cookie': cookie_init,
               'Host': 'mall.phicomm.com',
               'Referer': referer,
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
               }

    # 给服务器商品ID
    id_page = requests.get(url=id_url, headers=headers)

    # 获取下单界面详情，以寻找md5 认证串
    checkout_page = requests.get(checkout_url, headers=headers)

    soup = BeautifulSoup(checkout_page.text, "html.parser")
    print soup.text
    inputs_cart_md5 = soup.find_all('input', attrs={'name': 'cart_md5'})
    inputs_addr_id = soup.find_all('input', attrs={'name': 'addr_id', 'type': 'radio', 'class': 'hide dz_hide'})
    cart_md5 = inputs_cart_md5[0].get('value') if inputs_cart_md5 else "not found cart_md5!"
    addr_id = inputs_addr_id[0].get('value') if inputs_addr_id else "not found addr_id!"
    return cart_md5, addr_id

# 获取验证码图片
def get_Vcode():
    iamge_page = requests.get(get_image_url, cookies=cookie)
    image = Image.open(BytesIO(iamge_page.content))
    image.save('Vcode.png')

# post 请求头
headers = {'Host': 'mall.phicomm.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Accept-Encoding': 'gzip, deflate, br',
           'Referer': 'https://mall.phicomm.com/checkout-fastbuy.html',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Content-Length': '186',
           'Cookie': cookie_init,
           'Origin': 'https://mall.phicomm.com',
           'Connection': 'keep-alive',
           'X-Requested-With': 'XMLHttpRequest'
           }

cart_md5, addr_id = get_cart_md5()
#cart_md5, addr_id = "da9cebd8db531f1aa1f73b152ee1d908", "273397"
print cart_md5, addr_id


get_Vcode()
Vcode = raw_input(u"请输入验证码:")


data = {'cart_md5': cart_md5, 'addr_id': addr_id, 'dlytype_id': '1',
        'payapp_id': 'alipay', 'yougouma': '', 'invoice_type': '', 'invoice_title': '', 'useVcNum': useVcNum,
        'need_invoice2': 'on', 'useDdwNum': '0', 'memo': '', 'vcode': Vcode}


# 提交订单请求
def buy():
    post_page = requests.post(buy_url, headers=headers, data=data)
    print post_page.text.decode("unicode-escape")

buy()

# # 多线程提交
# threads = []
# for i in xrange(2):
#     threads.append(threading.Thread(target=buy))
# for thread in threads:
#     thread.start()
#     time.sleep(2)
