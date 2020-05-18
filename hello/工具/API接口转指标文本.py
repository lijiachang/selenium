# coding:utf-8

import requests
import json

rq = requests.get("http://192.168.95.112:8081/jobmanager/metrics")

results = []
dict_rq = json.loads(rq.text)
for i in dict_rq:
    tmp = "".join(i.values()[0][7:].split("."))
    results.append(tmp[0].lower() + tmp[1:])

# 排序
results.sort()

for i in results:
    print i