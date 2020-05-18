#!/usr/bin/env python
# coding=utf-8

import requests
import json
import time
import threading
import sys

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

cookie = 'JSESSIONID=538BC602269583E2718D42B12629C128; model=MI+9; brand=Xiaomi; isoffline=1; tkq=BF284B8453A33B31036047D44C194C54; channelid=market_1500; osv=28; v=7.0.5; sts=1569032165266; seq=52; uid=38231579418647; Expires=Mon, 21-Oct-2019 02:16:35 GMT; id58=c5/nR12FkyybAJrKCKZ5Ag==; idzz=c5/nR12FpfCN+Y3qFiIZAg==; t=15; tk=C663312E8A7F1855337A821DF74BC7C4; networktype=4G; zz_t=15; PPU="TT=f1ba6b3b6355989ed1744fb7b6a62a4baab39e2c&UID=38231579418647&SF=ZHUANZHUAN&SCT=1569210305887&V=1&ET=1571798705887"; lat=40.032272; lon=116.416879'
url = 'https://app.zhuanzhuan.com/zz/transfer/getFrontPrice?infoId={0}'.format(infoId)
url_apple_list = "https://app.zhuanzhuan.com/zzopen/ypdeal/getAuctionList?pageNum=1&pageSize=10&cateId=101&businessType=1&auctionType=0&fastSwitchOpt=0&capacityId=&versionId=&oldLevel=&pinpaiId=2101018&sortId=&price=&productTypeOption=&partsOption=&featureOption=&serviceOption="
top_price = 0
top_price_user = ""
bid_is_over = False


# 获取拍卖出价表
def update_bid_list():
    global top_price_user, top_price
    # # get请求头
    # headers = {'Host': 'app.zhuanzhuan.com',
    #            'Connection': 'keep-alive',
    #            'Accept': 'application/json, text/plain, */*',
    #            'Origin': 'https://m.zhuanzhuan.com',
    #            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 8 Build/PKQ1.180729.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36 58ZhuanZhuan',
    #            #  未确定的地址
    #            'Referer': 'https://m.zhuanzhuan.com/u/bmmain/auctionroom/300000000000031624?channel=10000&webview=zzn&metric=9316869dbdb00ff0eb9f43dff9f73532&tt=C663312E8A7F1855337A821DF74BC7C41550141804770&zzv=6.1.0',
    #            'Accept-Encoding': 'gzip, deflate',
    #            'Cookie': cookie,
    #            'X-Requested-With': 'com.wuba.zhuanzhuan'
    #            }

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
    end_minutes = int(end_MilliSecond) / 60000  # 拍卖剩余分钟
    time_now_HM = time.strftime('%H.%M', time.localtime(int(round(time.time() * 1000)) / 1000))  # 现在时间，时分格式 13:24
    end_time = time_now_HM[:3] + str(end_minutes + int(time_now_HM[-2:])) + ".59"


get_end_time()  # 自动获取结束时间
end_time_59 = end_time[:-1] + "9"
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


# 出个目前最高价，检测是否交了保证金 # isJoined=1 需要activityid
# print bid(str(top_price))


# 循环执行获取时间
def update_page():
    now = time.strftime('%H.%M.%S', time.localtime(time.time()))
    # print(now)

    if now == end_time or now == end_time_59:
        update_bid_list()  # 更新出价表
        if bid_is_over:
            update_bid_list()
            time.sleep(-1)  # 拍卖结束
        elif top_price_user != u"不**以然" and top_price < my_top_price:
            print bid(str(top_price + 20))  # 加20 出价
            # update_bid_list()
        else:
            print "未出价！"
            # update_bid_list()
            # time.sleep(-1)

        # update_bid_list()  # 更新出价表

    global timer
    timer = threading.Timer(0.02, update_page)
    timer.start()

    # update_bid_list()  # 更新出价表,要放最后


timer = threading.Timer(0.02, update_page)
timer.start()

