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

    cookie = "__jdu=1611668680086733123997; shshshfpa=36fcbb31-f7f4-11e4-487a-b069741c5a93-1611668681; shshshfpb=zmpHpg7kc3jL40tjLN%2FGtGg%3D%3D; shshshfp=7061a8b6fac251ab3055f7be87b8b48b; mba_muid=1611668680086733123997; qd_ad=-%7C-%7C-%7C-%7C0; qd_uid=KLWANMLS-VC7GN5XA8NKZA7M6RMNM; qd_fs=1614948527148; TrackerID=hCOei84DQqxSHUrOiL09EUSP6_hNOXGI4pKHl7oFWflVgzWlFiD7A4sE9v5qsB_DQwvZ0mP4ywkWl3c97kFp9E6i7a3Uloy-BOeJwxcazzM; pt_key=AAJgQijhADCJGTTAWd0hPhHyxwSKnfDKHB5lFBfjfCUS_4SyGI7_oScuShgQBzlETvFTfrPQ5jg; pt_pin=jd_76ab57cdbf964; pt_token=wcotda5f; pwdt_id=jd_76ab57cdbf964; sfstoken=tk01mc1a61cbba8sMSsyeDF4MSsxYH11jz0WrlU9NFCGGvpxL0rmtgDzIYi8/zjS7uxnC1GOuyGMHxgMKG/xQ79cydmT; __jda=122270672.1611668680086733123997.1611668680.1614948528.1615031896.5; __jdv=122270672|baidu|-|organic|%25E4%25BA%25AC%25E4%25B8%259C%25E6%2597%25B6%25E9%2597%25B4|1615031895514; areaId=1; ipLoc-djd=1-2953-0-0; 3AB9D23F7A4B3C9B=QIPHWURKRGQN7YRARJGLLDFVQUPC3G2K5SXOOEYMOPRRUJT5G44FT5BU6MHCZGCAKOEGMSXRGD64F4BID43WNVSLHY; qd_ls=1615032166727; qd_ts=1615097555285; qd_sq=3; qd_sid=KLWANMLS-VC7GN5XA8NKZA7M6RMNM-3"
    plus = JRplus(cookie)
    plus.getInfo()
    plus.dotask()
