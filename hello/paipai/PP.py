# coding=utf-8
# 2020.04.10  增加代理功能
# 2021.02.21  从代理池服务中获取代理IP。 使用集合判断新商品
import winsound
import requests
import json
import time
import sys
import urllib
import webbrowser

reload(sys)
sys.setdefaultencoding('utf8')

# 代理
proxy = False
proxy_server_url = 'http://192.168.2.190:5010'

try:
    # key1 = sys.argv[1].decode("GBK").encode("utf-8")
    key1 = '主机'
except Exception as e:
    print u"大哥输入监测关键词，如：主机"
    sys.exit(0)

key = urllib.quote(key1)
url = "https://bizgw.jd.com/search/v2/searchMixFqy"
query = "query=%7B%22bizType%22%3A%2211%22%2C%22hideC2c%22%3Atrue%2C%22key%22%3A%22" + key + "%22%2C%22pageNo%22%3A1%2C%22sort%22%3A%7B%22order%22%3A%22desc%22%2C%22sortKey%22%3A%22createTime%22%7D%7D&lng=116.423667&log=116.423667&channel=MI&lon=116.423667&clientVersion=2.1.4&m=MI%209&uuid=928049b62a32092b&appVersionCode=201040&idad=&uuid1=00000000-180e-3af1-0033-c5870033c587&macAddress=c29bd7a2dc90&osVersion=Android10&build=201040&client=android&networkType=wifi&brand=Xiaomi&lat=40.097309"
api = "http://wxpusher.zjiecode.com/api/send/message"
uids = ["UID_GN1WpBU7xOzZKhTlk3k0S0gEs4aS"]
goods_init = set()
# start_time = int(time.time())
# start_time = 0
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
print u"版本：7.0 开始监测《%s》：" % key1


def get_proxy():
    return requests.get(proxy_server_url + "/get/").json()


def delete_proxy(proxy):
    requests.get(proxy_server_url + "/delete/?proxy={}".format(proxy))


def get_itemIds_by_itemList(itemList):
    return [item['itemId'] for item in itemList]


def get_item_from_itemList_by_itemId(tiemId, itemList):
    for item in itemList:
        if item['itemId'] == tiemId:
            return item


# print start_time, "start"

def update():
    global goods_init
    print goods_init
    if proxy:
        proxy_ = get_proxy().get("proxy")
        proxies = {
            "https": proxy_,
            "http": proxy_
        }
        try:
            page = requests.get(url + "?" + query, proxies=proxies, timeout=5)
        except Exception as e:
            print proxy_, ' not ok ', e
            delete_proxy(proxy_)

        # print u"使用代理"
    else:
        page = requests.get(url + "?" + query)
        # print u"未使用"
    page_dict = json.loads(page.text)
    # print page_dict
    itemList = page_dict["data"].get("itemList", [])

    # 解决 itemList为空
    if itemList:
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), itemList
        pass
    else:
        print "itemList为空"
        try:
            with open("s.txt", "a+") as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "\n" + str(page_dict) + "\n")
        except Exception as e:
            print "日志写入错误"

    # 第一次的初始化
    if not goods_init:
        goods_init = set(get_itemIds_by_itemList(itemList))

    new_goods = set(get_itemIds_by_itemList(itemList)) - goods_init

    if new_goods:
        for item_id in new_goods:
            item = get_item_from_itemList_by_itemId(item_id, itemList)
            # print 'int(item["createTime"]):',int(item["createTime"])
            print("--------" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "--------")
            print(item["price"][:-3] + "--" + item["title"])
            good_url = "https://paipai.m.jd.com/c2c/goodsDetail.html?itemid=%s&shareIndex=1" % item["itemId"]

            # 打开浏览器
            webbrowser.open(good_url)

            # 微信通知
            try:
                content = u"%s\n\n%s\n%s" % (
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), item["price"], item["title"])

                body = {
                    "appToken": "AT_epdwTPm1PeboDE0Ix8VWczRgqpsuDrjq",
                    "content": content,
                    "contentType": 1,
                    "uids": uids,
                    "url": good_url
                }
                # 以json格式发送post请求,
                headers = {'Content-Type': 'application/json'}
                data = json.dumps(body)
                req = requests.post(api, headers=headers, data=data)
                if "处理成功" not in req.text:
                    print req.text
            except Exception as e:
                print u"微信推送失败！"
                print e
            winsound.PlaySound('2.wav', winsound.SND_FILENAME)
            winsound.PlaySound('2.wav', winsound.SND_FILENAME)

        goods_init = goods_init | new_goods


error_time = 0
while True:
    try:
        update()
        time.sleep(0.3)
    except requests.exceptions.ConnectionError:
        print "ConnectionError" + str(error_time)
        error_time += 1
        if error_time == 50:
            print u"累计重连50次，将休息60秒！"
            time.sleep(60)
            error_time = 0
        continue
    except UnboundLocalError:
        continue
