# coding=utf-8
# 2020.01.10
import winsound
import requests
import json
import time
import sys
import urllib

reload(sys)
sys.setdefaultencoding('utf8')

try:
    key1 = sys.argv[1].decode("GBK").encode("utf-8")
except Exception as e:
    print "大哥输入监测关键词，如：主机"
    sys.exit(0)
key = urllib.quote(key1)
url = "https://bizgw.jd.com/search/v2/searchMixFqy"
query = "query=%7B%22bizType%22%3A%2211%22%2C%22hideC2c%22%3Atrue%2C%22key%22%3A%22" + key + "%22%2C%22pageNo%22%3A1%2C%22sort%22%3A%7B%22order%22%3A%22desc%22%2C%22sortKey%22%3A%22createTime%22%7D%7D&lng=116.423667&log=116.423667&channel=MI&lon=116.423667&clientVersion=2.1.4&m=MI%209&uuid=928049b62a32092b&appVersionCode=201040&idad=&uuid1=00000000-180e-3af1-0033-c5870033c587&macAddress=c29bd7a2dc90&osVersion=Android10&build=201040&client=android&networkType=wifi&brand=Xiaomi&lat=40.097309"
api = "https://sc.ftqq.com/SCU75557Tdd7d69d128ae097811659b73783094135e0ed22e82c37.send"
# api = "https://sc.ftqq.com/SCU75524T15f230221f4fbeabde558cd8f26a4b485e0eb3cc02f3f.send"
start_time = int(time.time())
# start_time = 0
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print u"版本：4.0 开始监测《%s》：" % key1


# print start_time, "start"

def update():
    global start_time
    page = requests.get(url + "?" + query)
    page_dict = json.loads(page.text)
    itemList = page_dict["data"].get("itemList", [])
    # 解决 itemList为空
    if itemList:
        pass
    else:
        print "itemList为空"
        try:
            with open("s.txt", "w") as f:
                f.write(str(page_dict))
        except Exception as e:
            print "日志写入错误"

    for item in itemList:
        if int(item["createTime"]) > start_time:
            print("--------" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "--------")
            print(item["price"][:-3] + "--" + item["title"])
            # 微信通知
            try:
                title = item["price"][:-3] + "." + item["title"]
                content = u"----\n###%s\n###%s\n###https://paipai.m.jd.com/c2c/goodsDetail.html?itemid=%s&shareIndex=1" % (
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), item["price"], item["itemId"])
                data = {
                    "text": title,
                    "desp": content
                }
                req = requests.post(api, data=data)
            except Exception as e:
                print u"微信推送失败！"
                print e
            winsound.PlaySound('2.wav', winsound.SND_FILENAME)
            winsound.PlaySound('2.wav', winsound.SND_FILENAME)
    for item in itemList:
        start_time = int(item["createTime"]) if int(item["createTime"]) > start_time else start_time


error_time = 0
while True:
    try:
        update()
        time.sleep(2)
    except requests.exceptions.ConnectionError:
        print "ConnectionError" + str(error_time)
        error_time += 1
        if error_time == 50:
            print u"累计重连50次，将休息60秒！"
            time.sleep(60)
            error_time = 0
        continue
