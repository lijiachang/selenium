# coding:utf-8

import rk
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import threading
import time
import sys
from random import choice


headers = {'Accept': '*/*',
           'Connection': 'keep-alive',
           'Host': 'tz01.yangxiantc.com',
           'Referer' : 'http://tz01.yangxiantc.com/index.php?g=Wap&m=Voteimg&a=popup_view&token=yciipo1542811095&id=16954&item_id=1907122&td_channelid=110114000000',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
           'X-Requested-With': 'XMLHttpRequest',
           'Cookie': 'PHPSESSID=i8frqj2pbtiop6ne0g3tghu3f6; UM_distinctid=167bbed204f536-0bcd92cf4-6a3f0723-1fa400-167bbed2050715; CNZZDATA1271442956=1492746847-1545043001-%7C1545043001; Hm_lvt_f5df380d5163c1cc4823c8d33ec5fa49=1545046139; Hm_lpvt_f5df380d5163c1cc4823c8d33ec5fa49=1545046238',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.901.400 QQBrowser/9.0.2524.400'
           }

checkout_page = requests.get("http://tz01.yangxiantc.com/index.php?g=Wap&m=Voteimg&a=vote&td_channelid=110114000000&ADTAG=110114000000&vote_id=16954&token=yciipo1542811095&id=1907122&zb=null", headers=headers)

soup = BeautifulSoup(checkout_page.text, "html.parser")
print soup.text