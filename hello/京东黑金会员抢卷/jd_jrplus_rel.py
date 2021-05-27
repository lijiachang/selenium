#!usr/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import urllib3

urllib3.disable_warnings()


class JRplus(object):
    def __init__(self, key):
        self.session = requests.Session()
        self.cookie = key

    def getInfo(self):
        url = 'https://ms.jr.jd.com/gw/generic/hy/h5/m/queryNewRightsDetail?reqData={"appCode":"jr-vip","rid":"158"}'
        headers = {
            'Host': 'ms.jr.jd.com',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; BAC-TL00 Build/HUAWEIBAC-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.0.9) WindVane/8.3.0 1080X1812',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://h5.m.jd.com',
            'Referer': 'https://ms.jr.jd.com/gw/generic/hy/h5/m/drawNewMemberRights1?reqData={"appCode":"jr-vip","rid":159,"hasReadParam":"301,302,305,310,350,351,352","drawEnv":"JR_APP"}',
            'Cookie': self.cookie
        }
        response = self.session.get(url, headers=headers, verify=False).json()
        listinfo = response.get('resultData', '').get('data', '').get('subRightsList1', '')
        # print(response.get('resultData','').get('data','').get('subRightsList1',''))
        for i in listinfo:
            print(i['rightsId'] + '-' + i['name'])
        listinfo = response.get('resultData', '').get('data', '').get('subRightsList2', '')
        # print(response.get('resultData','').get('data','').get('subRightsList1',''))
        for i in listinfo:
            print(i['rightsId'] + '-' + i['name'])

    def quan1(self, key):
        url = 'https://ms.jr.jd.com/gw/generic/hy/h5/m/drawNewMemberRights1?reqData={"appCode":"jr-vip","rid":' + str(key) + ',"hasReadParam":"301,302,305,310,350,351,352","drawEnv":"JR_APP"}'
        headers = {
            'Host': 'ms.jr.jd.com',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; BAC-TL00 Build/HUAWEIBAC-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.0.9) WindVane/8.3.0 1080X1812',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://h5.m.jd.com',
            'Referer': 'https://ms.jr.jd.com/gw/generic/hy/h5/m/drawNewMemberRights1?reqData={"appCode":"jr-vip","rid":159,"hasReadParam":"301,302,305,310,350,351,352","drawEnv":"JR_APP"}',
            'Cookie': self.cookie
        }

        response = self.session.get(url, headers=headers, verify=False).json()
        print(response)
        print(response.get('resultData', '')['success'])
        if (response.get('resultData', '')['success'] != False):
            print(str(key) + ' 抢到了')

    def dotask(self):
        choice_2 = input('请输入要抢权益编码，如159, :')
        self.quan1(choice_2)
        i = 20
        while i > 0:
            i = i - 1
            self.quan1(choice_2)
            print("尝试第" + str(20 - i) + "次")
            time.sleep(0.1)


##
if __name__ == '__main__':

    cookie = "__jdu=1611668680086733123997; shshshfpa=36fcbb31-f7f4-11e4-487a-b069741c5a93-1611668681; shshshfpb=zmpHpg7kc3jL40tjLN%2FGtGg%3D%3D; mba_muid=1611668680086733123997; qd_uid=KLWANMLS-VC7GN5XA8NKZA7M6RMNM; qd_fs=1614948527148; whwswswws=; qd_ts=1615097555285; qd_ls=1615032166727; qd_sq=3; webp=1; visitkey=38577976860161798; ipLoc-djd=1-2953-54047-0; wxa_level=1; retina=0; cid=9; jxsid=16206515067588103213; __jdv=122270672%7Cdirect%7C-%7Cnone%7C-%7C1620651506998; __jda=122270672.1611668680086733123997.1611668680.1618651016.1620651506.12; __jdc=122270672; autoOpenApp_downCloseDate_auto=1620651508068_10800000; 3AB9D23F7A4B3C9B=QIPHWURKRGQN7YRARJGLLDFVQUPC3G2K5SXOOEYMOPRRUJT5G44FT5BU6MHCZGCAKOEGMSXRGD64F4BID43WNVSLHY; jcap_dvzw_fp=EfNMZ-S1xNmMSAGMQpCv5DOG-Hxj11Ne2PJ1mYvjP64hbN-gae37OgLYix7VRuILECivcA==; TrackerID=GmEGWd9PjADy8ESWMURcReSqoDJUzQKXMqbJurh1Z73UIWYDMZHbikFS-cjYqzjRX1iEuF59L6aAzW-D-wGOVkYPV70-Fkemd-yAl1jsBxU; pt_key=AAJgmS4OADAw6IbEMqBv--VJGFa208FA9VBFXXZhMp-WugBJFu9dH7Rad_PNhFKWl4KqNg1PGe4; pt_pin=jd_76ab57cdbf964; pt_token=xo2i5jx2; pwdt_id=jd_76ab57cdbf964; sfstoken=tk01mb5a31c3ba8sMngxMXVJYjV6wF0wyWxX/nS4eTUJL1HYUdJGnHZaa/bUX1g12ijaPQFJfY0ateo5J3jwgq8pG9Zv; wqmnx1=MDEyNjM2MXQvbW9kb3RjbGM4NjF6NWkgLldwYjMoLCApbTAuYTUxcjdVNDRXT0hIKSk%3D; __jdb=122270672.3.1611668680086733123997|12.1620651506; mba_sid=16206515070003171802797303782.3; __wga=1620651529348.1620651529348.1616760408255.1616760408255.1.2; PPRD_P=UUID.1611668680086733123997; jxsid_s_t=1620651529423; jxsid_s_u=https%3A//home.m.jd.com/myJd/newhome.action; sc_width=1920; shshshfp=e1ffa240d5bf77828585f9ee6205a3f6; shshshsID=0baa3bd3e0bcc532fc8efcb51fe03ec3_2_1620651529927"
    plus = JRplus(cookie)
    plus.getInfo()
    plus.dotask()
