# coding:utf-8

import rk
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import threading
import time
import sys
from random import choice

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


##  试试用手机web界面
product_id = "13"  # k2:5  插座:24  秤12 电视盒子13
useVcNum = '29900' # 秤23900  路由16000 电视盒子29900
cookie_init = "__jsluid=ea019bef88ca17477600625ceb312d89; _VMC_UID=f47ff553d611ab7090158c643b58038d; _SID=27ecdb48361e5a3aefd7e4cbf4d22304; from_vshopid=43105230377; __jsl_clearance=1542941832.991|0|rPfR6YkUtwRWgyFWRJfljKqiH0M%3D; CACHE_VARY=6f8fb63e2a9b34f841787535ed557205-f97d48f7d515cde89d08f67a90635a23; UNAME=15269026760; MEMBER_IDENT=2523347; MEMBER_LEVEL_ID=2"





# 处理cookies
cookie = {}  # 传入的cookies参数应该是字典
for line in cookie_init.split(';'):
    name, value = line.strip().split('=', 1)  # 其设置为1就会把字符串拆分成2份
    cookie[name] = value

# 生成随机数，用于获取验证码的网址
random_num=""
for x in range(14):
    random_num =random_num + str(choice(range(10)))

MEMBER_IDENT = cookie["MEMBER_IDENT"]  # 用户数字ID
get_image_url = r"https://mall.phicomm.com/vcode-index-passport{0}.html?d=0.48{1}".format(MEMBER_IDENT, random_num)  # 获取验证码地址
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
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
               }

    # 给服务器商品ID
    id_page = requests.get(url=id_url, headers=headers)

    # 获取下单界面详情，以寻找md5 认证串
    checkout_page = requests.get(checkout_url, headers=headers)

    soup = BeautifulSoup(checkout_page.text, "html.parser")
    #print soup.text
    inputs_cart_md5 = soup.find_all('input', attrs={'name': 'cart_md5'})
    inputs_addr_id = soup.find_all('input', attrs={'name': 'addr_id', 'type': 'radio', 'class': 'hide dz_hide'})
    cart_md5 = inputs_cart_md5[0].get('value') if inputs_cart_md5 else "not found cart_md5!"
    addr_id = inputs_addr_id[0].get('value') if inputs_addr_id else "not found addr_id!"
    return cart_md5, addr_id



# 获取验证码图片
def get_Vcode():
    referer = "https://mall.phicomm.com/checkout-fastbuy.html"
    get_Vcode_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control' : 'max-age=0',
               'Connection': 'keep-alive',
               'Cookie': cookie_init,
               'Host': 'mall.phicomm.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
               }
    #iamge_page = requests.get(get_image_url, cookies=cookie)
    iamge_page = requests.get(get_image_url, headers=get_Vcode_headers)
    print iamge_page  #  验证码返回状态
    image = Image.open(BytesIO(iamge_page.content))
    image.save('Vcode.png')

# post 请求头
headers = {'Host': 'mall.phicomm.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
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


cart_md5 = "not found cart_md5"
#cart_md5, addr_id = "cbffc16a4a9249d6747302b6309bfe00", "273397"
while "not" in cart_md5:
    cart_md5, addr_id = get_cart_md5()
    print cart_md5, addr_id
print cart_md5, addr_id



get_Vcode()
#Vcode = raw_input(u"请输入验证码:")

rc = rk.RClient('944581577', 'lichang1995', '112258', '6ff5e81e204f4c4f8da9dfb1c068e98e')
im = open('Vcode.png', 'rb').read()
rc_result = rc.rk_create(im, 4030)  # 4030  三位纯汉字  花费30快豆=大约1分钱
#print rc_result
print "识别的验证码为：" + rc_result["Result"]

Vcode = rc_result["Result"]

data = {'cart_md5': cart_md5, 'addr_id': addr_id, 'dlytype_id': '1',
        'payapp_id': 'alipay', 'yougouma': '', 'invoice_type': '', 'invoice_title': '', 'useVcNum': useVcNum,
        'need_invoice2': 'on', 'useDdwNum': '0', 'memo': '', 'vcode': Vcode}


# 提交订单请求
def buy():
    code = 0
    while code == 0:
        post_page = requests.post(buy_url, headers=headers, data=data)
        post_page_result = post_page.text.decode("unicode-escape")
        print post_page_result
        if "Time-out" in post_page_result:
            code = 0
        else:
            code = 1




buy()

# # 多线程提交
# threads = []
# for i in xrange(2):
#     threads.append(threading.Thread(target=buy))
# for thread in threads:
#     thread.start()
#     time.sleep(2)
