# coding=gbk

import winsound
import requests
import json
import time
import sys
import urllib

api = "http://wxpusher.zjiecode.com/api/send/message"
a = "8801667"
content = u"2575.00\n\n��ʤ���� ����i5 9400/16Gרҵƽ�����ʦ����ר��̨ʽ�����������ð칫DIY��װ��ͼ�ι���վ ��������/i5 9400/16"


uids = ["UID_KyiycPUC76jLyU7QXj4mvhwGT1Ah"]
body = {
    "appToken": "AT_epdwTPm1PeboDE0Ix8VWczRgqpsuDrjq",
    "content": content,
    "contentType": 1,
    "uids": uids,
    "url":"https://paipai.m.jd.com/c2c/goodsDetail.html?itemid=8801767&shareIndex=1"
}
# ��json��ʽ����post����,
headers = {'Content-Type': 'application/json'}
data = json.dumps(body)
req = requests.post(api, headers=headers, data=data)

print req.text

if "1111" not in req.text:
    print "shibai"



