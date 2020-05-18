#!/usr/bin/env python
# coding=utf-8

import requests
import json


# 不方便放到requests的header中
# 方法用python把他变成字典形式;
def parse_fidder_cookie(cookie):
    itemDict = {}
    items = cookie.split('\n')
    for item in items:
        key = item.split(':')[0].strip()
        if key:
            value = item.split(':')[1].strip()
            itemDict[key] = value
    return itemDict


headers = """Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Length: 1662
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: ASP.NET_SessionId=taxbhkhngcpvfjxm3f5pmf3j; SERVERID=208fec25b20334ee39adbd1e8a5ee230|1561539571|1561537910
Host: exhibitor.fia-china.com
Origin: http://exhibitor.fia-china.com
Referer: http://exhibitor.fia-china.com/fia2019/zh-CN
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
X-Requested-With: XMLHttpRequest"""



data = """draw: 39
columns[0][data]: 0
columns[0][name]: 
columns[0][searchable]: true
columns[0][orderable]: false
columns[0][search][value]: 
columns[0][search][regex]: false
columns[1][data]: 1
columns[1][name]: 
columns[1][searchable]: true
columns[1][orderable]: true
columns[1][search][value]: 
columns[1][search][regex]: false
columns[2][data]: StandNoStr
columns[2][name]: 
columns[2][searchable]: true
columns[2][orderable]: true
columns[2][search][value]: 
columns[2][search][regex]: false
columns[3][data]: CountryChs
columns[3][name]: 
columns[3][searchable]: true
columns[3][orderable]: true
columns[3][search][value]: 
columns[3][search][regex]: false
columns[4][data]: ProductCategoryChs
columns[4][name]: 
columns[4][searchable]: true
columns[4][orderable]: false
columns[4][search][value]: 
columns[4][search][regex]: false
columns[5][data]: 5
columns[5][name]: 
columns[5][searchable]: true
columns[5][orderable]: false
columns[5][search][value]: 
columns[5][search][regex]: false
order[0][column]: 1
order[0][dir]: asc
start: 600
length: 100
search[value]: 
search[regex]: false
fn: getExhibitor
orderfields: ["","ExhibitorNameChs","StandNoStr","CountryEn",""]
filter[country]: 47
filter[productcategory]: 
filter[businessnature]: 
filter[exhibitortype]: 
filter[fairlocation]: 
dt: 1
FairID: 55"""
url = 'http://exhibitor.fia-china.com/api'



data2 = (parse_fidder_cookie(data))
headers2 = parse_fidder_cookie(headers)
print data2
print headers2

id_page = requests.post(url=url, headers=headers2, data=data2)

all_data=json.loads(id_page.text)["data"]

for one in all_data:
    print one["ExhibitorNameChs"]
