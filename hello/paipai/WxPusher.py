# coding=gbk

import winsound
import requests
import json
import time
import sys
import urllib

api = "http://wxpusher.zjiecode.com/api/send/message"
a = "8801667"
content = u"2575.00\n\n优胜美电 六核i5 9400/16G专业平面设计师美工专用台式电脑主机家用办公DIY组装机图形工作站 升级配置/i5 9400/16"


uids = ["UID_KyiycPUC76jLyU7QXj4mvhwGT1Ah"]
body = {
    "appToken": "AT_epdwTPm1PeboDE0Ix8VWczRgqpsuDrjq",
    "content": content,
    "contentType": 1,
    "uids": uids,
    "url":"https://paipai.m.jd.com/c2c/goodsDetail.html?itemid=8801767&shareIndex=1"
}
# 以json格式发送post请求,
headers = {'Content-Type': 'application/json'}
data = json.dumps(body)
req = requests.post(api, headers=headers, data=data)

print req.text

if "1111" not in req.text:
    print "shibai"



