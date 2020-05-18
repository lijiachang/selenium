#!/usr/bin/env python
# coding=utf-8

import requests
import json
import time
import sys

# 2019.04.28
# 目前没有考虑，无人出价的情况   卖价-50利润 -60 = -130

if len(sys.argv) == 2:
    infoId = sys.argv[1]
else:
    infoId = input("InfoId:")


activityId = ""
cookie = 'idzz=c5/nR1y9eBgP8BOiCid0Ag==; v=6.6.0; channelid=market_903; osv=28; model=MI+9; brand=Xiaomi; id58=c5/nR1y9eD4P8BOiCjPdAg==; imei=867252031301210; Version=1; Domain=zhuanzhuan.com; Path=/; ; ab=true; t=15; isGuidExpire=1; JSESSIONID=A359A5BCFA7996CCF98129141B1FF593; tk=C663312E8A7F1855337A821DF74BC7C4; zz_t=15; sts=1556149954331; seq=633; uid=38231579418647; lat=40.03228; lon=116.417034; PPU="TT=88a4ab2d1b95beb49c7238f849cd791a07faf9de&UID=38231579418647&SF=ZHUANZHUAN&SCT=1556177611877&V=1&ET=1558766011877"'
url = 'https://app.zhuanzhuan.com/zz/transfer/getFrontPrice?infoId={0}'.format(infoId)
url_apple_list = "https://app.zhuanzhuan.com/zzopen/ypdeal/getAuctionList?pageNum=1&pageSize=10&cateId=101&businessType=1&auctionType=0&fastSwitchOpt=0&capacityId=&versionId=&oldLevel=&pinpaiId=2101018&sortId=&price=&productTypeOption=&partsOption=&featureOption=&serviceOption="
top_price = 0
top_price_user = ""


# 获取拍卖出价表
def update_bid_list():
    global top_price_user, top_price
    id_page = requests.get(url=url)  # 不使用headers也能获取列表；关闭证书验证（verify=False）
    #print(id_page.text)
    dict_price = json.loads(id_page.text)
    # print dict_price
    # print 'sys time:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(round(time.time() * 1000)) / 1000))  # 现在的时间 格式 2019-04-26 13:24:34
    nowPrice = dict_price["respData"]["nowPrice"]  # 现在的最高价
    price = dict_price["respData"]["priceList"][0]["price"]  # 现在的最高出价
    nickname = dict_price["respData"]["priceList"][0]["nickname"]  # 现在的最高出价人
    timestamp = dict_price["respData"]["priceList"][0]["timestamp"]  # 现在的最高出价 13位时间戳
    top_price_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp) / 1000))
    all = dict_price["respData"]["priceList"]

    print("*********************************")
    for one in all:
        print one["price"], one["nickname"], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(one["timestamp"]) / 1000))
    print("*********************************")

update_bid_list()
