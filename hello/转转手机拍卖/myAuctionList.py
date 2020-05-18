#!/usr/bin/env python
# coding=utf-8

import requests
import json
import time
import sys

# 2019.08.27
# 新增 1.缴纳保证金判断 2.cookie有效性判断
# 2019.05.14
# 新增无人出价的情况

reload(sys)
sys.setdefaultencoding('utf8')


activityId = ""

cookie = 'osv=28; model=MI+9; brand=Xiaomi; uid=38231579418647; idzz=c5/nR11WEtBMO2zRcR5PAg==; id58=c5/nR11WEtBMO2zRcR6SAg==; isoffline=1; firstSourceId=2; secondSourceId=biz_10005; bizResourceId=; v=6.13.3; channelid=market_1500; JSESSIONID=9EA3C9818F792AF4396B8B56AC0CC216; networktype=WIFI; t=15; tk=C663312E8A7F1855337A821DF74BC7C4; lat=40.091342; lon=116.414514; zz_t=15; PPU="TT=ceb2dc2ac36e9f67e794a4356881cb58112447b0&UID=38231579418647&SF=ZHUANZHUAN&SCT=1566574492416&V=1&ET=1569162892416"'
url_apple_list = "https://app.zhuanzhuan.com/zzopen/ypdeal/getAuctionList?pageNum=1&pageSize=10&cateId=101&businessType=1&auctionType=0&fastSwitchOpt=0&capacityId=&versionId=&oldLevel=&pinpaiId=2101018&sortId=&price=&productTypeOption=&partsOption=&featureOption=&serviceOption="
top_price = 0
top_price_user = ""
bid_is_over = False


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

    # 判断cookie有效性：
    if page["respCode"] == -2:
        print "Cookie已失效，请检查！！"
        sys.exit(0)
    print(json.dumps(page, indent=2).decode('unicode-escape'))  # 易读展示【我参拍的】


get_my_list()
