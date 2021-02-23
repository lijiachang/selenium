# coding=utf-8
# 2020.04.10  增加代理功能
import winsound
import requests
import json
import time
import sys
import urllib

reload(sys)
sys.setdefaultencoding('utf8')

key1 = '手机'
key = urllib.quote(key1)

url = "https://bizgw.jd.com/search/v2/searchMixFqy"
query = "query=%7B%22bizType%22%3A%2211%22%2C%22hideC2c%22%3Atrue%2C%22key%22%3A%22" + key + "%22%2C%22pageNo%22%3A1%2C%22sort%22%3A%7B%22order%22%3A%22desc%22%2C%22sortKey%22%3A%22createTime%22%7D%7D&lng=116.423667&log=116.423667&channel=MI&lon=116.423667&clientVersion=2.1.4&m=MI%209&uuid=928049b62a32092b&appVersionCode=201040&idad=&uuid1=00000000-180e-3af1-0033-c5870033c587&macAddress=c29bd7a2dc90&osVersion=Android10&build=201040&client=android&networkType=wifi&brand=Xiaomi&lat=40.097309"

proxy = "218.60.8.83:3129"
proxies = {
    "https": proxy,
}
page = requests.get(url + "?" + query, proxies=proxies)

print page.text