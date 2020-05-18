# coding=utf-8
# 2020.01.10
import winsound
import requests
import json
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

url = "https://app.zhuanzhuan.com/zzopen/ypdeal/getAuctionList?pageNum=1&pageSize=50&cateId=101&businessType=1&auctionType=0&fastSwitchOpt=0&capacityId=&versionId=&oldLevel=&pinpaiId=2101018&xinghaoId=2101018010&sortId=&price=&productTypeOption=&partsOption=&featureOption=&serviceOption="

print u"开始"
while True:
    now = time.strftime('%M:%S', time.localtime(time.time()))
    # print now
    if now == "00:00":
        id_page = requests.get(url=url)  # 不使用headers也能获取列表；关闭证书验证（verify=False）
        dict_price = json.loads(id_page.text)
        items = dict_price["respData"]

        if items:
            winsound.PlaySound('2.wav', winsound.SND_FILENAME)
            winsound.PlaySound('2.wav', winsound.SND_FILENAME)
        else:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + u"  本场无商品")
        time.sleep(10)
    time.sleep(0.5)
