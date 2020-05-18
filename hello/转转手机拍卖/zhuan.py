#!/usr/bin/env python
# coding=utf-8

import requests
import json
import time
import threading
import sys

# 2020.02.24
# 兼容剩余时间大于1小时的拍卖
# 2019.09.30
# 适配新版有人出价延时15s拍卖
# 2019.08.27
# 新增 1.缴纳保证金判断 2.cookie有效性判断
# 2019.05.14
# 新增无人出价的情况

reload(sys)
sys.setdefaultencoding('utf8')

if len(sys.argv) == 3:
    infoId = sys.argv[1]
    my_top_price = int(sys.argv[2])
else:
    infoId = input("InfoId:")
    my_top_price = input("MyPrice:")

activityId = ""

cookie = 'idzz=c5/nR12V1hJ5nyL5KFBuAg==; id58=c5/nR12V1hJ5nyL5KFC2Ag==; visitSku=5463:1000000004,5463:1000000007; sku=1175963672296849411; channelid=market_903; osv=29; model=MI+9; brand=Xiaomi; networktype=WIFI; isoffline=1; uid=38231579418647; v=7.5.11; JSESSIONID=C310F4B7E83BC58BED4C78A5DE49B21D; t=15; tk=C663312E8A7F1855337A821DF74BC7C4; lat=40.091148; lon=116.417257; PPU="TT=979ec8bfd3805b0d1c16e4e5dbaefc3ced933ccd&UID=38231579418647&SF=ZHUANZHUAN&SCT=1582443109628&V=1&ET=1585031509628"; zz_t=15'
url = 'https://app.zhuanzhuan.com/zz/transfer/getFrontPrice?infoId={0}'.format(infoId)
url_apple_list = "https://app.zhuanzhuan.com/zzopen/ypdeal/getAuctionList?pageNum=1&pageSize=10&cateId=101&businessType=1&auctionType=0&fastSwitchOpt=0&capacityId=&versionId=&oldLevel=&pinpaiId=2101018&sortId=&price=&productTypeOption=&partsOption=&featureOption=&serviceOption="
top_price = 0
top_price_user = ""
bid_is_over = False


# 获取拍卖出价表
def update_bid_list():
    global top_price_user, top_price

    id_page = requests.get(url=url)  # 不使用headers也能获取列表；关闭证书验证（verify=False）
    # print(id_page.text)  # 2019.05.04去掉打印
    dict_price = json.loads(id_page.text)
    # print dict_price
    # print 'sys time:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(round(time.time() * 1000)) / 1000))  # 现在的时间 格式 2019-04-26 13:24:34
    price = dict_price["respData"]["nowPrice"]  # 现在的最高价
    # price = dict_price["respData"]["priceList"][0]["price"]  # 现在的最高人出价
    try:
        nickname = dict_price["respData"]["priceList"][0]["nickname"]  # 现在的最高出价人
        timestamp = dict_price["respData"]["priceList"][0]["timestamp"]  # 现在的最高出价 13位时间戳
    except IndexError:
        print price, "None"
    else:
        top_price_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp) / 1000))
        print price, nickname, top_price_time

        top_price_user = nickname
        top_price = int(price)


#   获取我的参加拍卖表
def get_my_list():
    headers = {'Host': 'app.zhuanzhuan.com',
               'Connection': 'keep-alive',
               'Accept': 'application/json, text/plain, */*',
               'Origin': 'https://m.zhuanzhuan.com',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 9 Build/PKQ1.181121.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36 58ZhuanZhuan',
               #  未确定的地址  试试空的情况！！！！！！
               'Referer': 'https://m.zhuanzhuan.com/u/bmmain/auctionroom/{0}/offer'.format(activityId),
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,en-US;q=0.9',
               'Cookie': cookie,
               'X-Requested-With': 'com.wuba.zhuanzhuan'
               }
    url = "https://app.zhuanzhuan.com/zzopen/ypdeal/getMyAuctionList?pageNum=1&pageSize=10&smark=&init_from=4_1_6069_0&cateId=101&businessType=1"
    page = requests.get(url=url, headers=headers)
    page = json.loads(page.text)
    # print(json.dumps(page, indent=2))  # 易读展示【我参拍的】
    # 判断cookie有效性：
    if page["respCode"] == -2:
        print "Cookie已失效，请检查！！"
        sys.exit(0)
    # 保证金检查：
    respData = page["respData"]
    if not respData:
        print "【我参拍的】列表为空！"
    isJoined = 0
    for data in respData:
        if data["zzItemId"] == infoId:
            isJoined = 1
    if isJoined == 0:
        print "未缴纳 保证金！！！"
        print "未缴纳 保证金！！！"
        print "未缴纳 保证金！！！"


get_my_list()

end_time = "null"


# 获取拍卖倒计时的时间
def get_end_time():
    global end_time
    id_page = requests.get(url=url_apple_list)  # 不使用headers也能获取列表；关闭证书验证（verify=False）
    # print(id_page.text)
    dict_price = json.loads(id_page.text)
    end_MilliSecond = dict_price["respData"][0]["deadlineMilliSecond"]  # 毫秒级剩余时间

    t = time.time()  # 原始时间数据
    haomiao = (int(round(t * 1000))) + int(end_MilliSecond) - 1000  # 毫秒级时间戳 + 毫秒级剩余时间 - 1秒
    timeStamp = float(haomiao / 1000)
    timeArray = time.localtime(timeStamp)
    end_time = time.strftime("%H.%M.%S", timeArray)
    if not end_time.endswith("59"):
        print "时间有误，检查get_end_time()函数！"


get_end_time()  # 自动获取结束时间
# end_time_59 = end_time[:-1] + "9"
print("抢拍时间：" + end_time)


# 进行出价
def bid(offerPrice):
    global bid_is_over
    # get请求头
    headers = {'Host': 'app.zhuanzhuan.com',
               'Connection': 'keep-alive',
               'Accept': 'application/json, text/plain, */*',
               'Origin': 'https://m.zhuanzhuan.com',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 9 Build/PKQ1.181121.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36 58ZhuanZhuan',
               #  未确定的地址  试试空的情况！！！！！！
               'Referer': 'https://m.zhuanzhuan.com/u/bmmain/auctionroom/{0}/offer'.format(activityId),
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,en-US;q=0.9',
               'Cookie': cookie,
               'X-Requested-With': 'com.wuba.zhuanzhuan'
               }
    url = 'https://app.zhuanzhuan.com/zz/transfer/offerPrice?infoId={0}&offerPrice={1}'.format(infoId, offerPrice)
    id_page = requests.get(url=url, headers=headers)
    if u"拍卖已结束" in id_page.text:
        bid_is_over = True
    return id_page.text


update_bid_list()  # 初始化获取出价表


# 循环执行获取时间
def update_page():
    global end_time
    now = time.strftime('%H.%M.%S', time.localtime(time.time()))
    # print(now)

    if now == end_time:
        update_bid_list()  # 更新出价表
        if bid_is_over:
            print "拍卖已结束："
            update_bid_list()
            sys.exit(0)
        elif top_price > my_top_price:
            print "高于我的预期价格："
            update_bid_list()
            sys.exit(0)
        elif top_price_user != u"不**以然" and top_price <= my_top_price:
            print bid(str(top_price + 20))  # 加20 出价
            time.sleep(15)  # 等待15s
            now = time.strftime('%H.%M.%S', time.localtime(time.time()))
            end_time = now  # 立即判断
        else:
            print "未出价！"

    global timer
    timer = threading.Timer(0.02, update_page)
    timer.start()


timer = threading.Timer(0.02, update_page)
timer.start()
