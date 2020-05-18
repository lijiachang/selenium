# coding:utf-8

import requests
import threading
import _thread
import time
import datetime
import itchat
import re
from datetime import datetime, time
import random
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 需要抓包
JSESSIONID_OAUTH = "4A80081F98141C521D650F569266C22D"
citicbank_cookie = '!fpVM2HGUYQiK1z27WDSPiZPLSyIDtN9CkbWZT+3H80o/FTQNd+UH4m1qo6N6saGKjkOKEUqFDbPvUYs'
unionidSrc_self = "CgGAJjLUjnRJGbEw04PXbiYrq64ounOOL8bWn7R1JagJyOxRVj/wsc93DdQux/M1OoV7zX1lU/uNfrQXDwxBMSlYBRvJeoWdO6TSUTlOj2XnEh+dehQ4ZvWhoOFoPF8lE65BeTrYZDalyEEphTWrKsm2ZRC3Cw/vMDI5I9zOZH4T5DVLgC6ZfYO+ycpJZYJS6z5JwY6QUKWACLGWa2S0sF9cUwOE8uMaQE8LsRhewEixjpwYn0G/4gZK1mp+0dQKo4qmzHnGNeqC5lV2Nw1N5yuO4IZMvvLiake1+iSWDlO2UkSsaUDNvhbv2Hy/JoZAxRzweryTWJWHGpPw"

DAY_START = time(9, 5)
DAY_END = time(9, 30)
# 需要大于10
WAIT_TIME = 60 * 2

SUCCESS_RET_CODE = '000000'
COOKIE_FAILED = '000004'

needCoin = 0
totalCoin = 0
currentValue = 0
rhizomysId = 0

# feed number
bambooNum = 0
chiliNum = 0
cornNum = 0
blindBoxNum = 0
variationFeedNum = 0

proxy_dict = {
    # "http": "http://127.0.0.1:8888",
    # "https": "http://127.0.0.1:8888",
}

cookie = "JSESSIONID_OAUTH=" + JSESSIONID_OAUTH + "; Domain=.creditcard.ecitic.com; Path=/;citicbank_cookie=" + citicbank_cookie + "; path=/;"
userAgent = "Mozilla/5.0 (Linux; Android 5.0.2; SM-G9200 Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36 MicroMessenger/7.0.9.1560(0x2700099B) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64"

header = {
    "Content-Type": "application/json;charset=utf-8",
    "Cookie": cookie,
    'User-Agent': userAgent,
}

bankSession = requests.session()

chat_login = False
fout = open('log.txt', 'w', encoding='utf8')


# write log to file
def bank_log(msg):
    print(msg)
    log_file = True
    if log_file:
        fout.write(msg + "\n")
        fout.flush()


# send to chat
def send_msg_chat(msg):
    if chat_login:
        itchat.send(msg, 'filehelper')


# 登录
def nopwdlogin():
    # 无法实现 无法得到code iv encryptedData 如果可以得到就可以设置JSESSIONID_OAUTH
    return
    data_send = {"code": "",
                 "encryptedData": "",
                 "iv": "",
                 "channel": "WeChatMini",
                 "activity": "summer",
                 "toMini": "3",
                 "loginType": 0
                 }

    bank_log(str(datetime.today()) + ": login")
    postUrl = "https://uc.creditcard.ecitic.com/citiccard/newucwap/wx/nopwdLogin.do"
    responseRes = bankSession.post(postUrl, headers=header, json=data_send, proxies=proxy_dict, verify=False)
    bank_log(f"statusCode = {responseRes.status_code}")
    json_obj = responseRes.json()
    bank_log(responseRes.text)
    # {"authKey":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX","resultCode":"0000000","resultDesc":"操作成功"}
    bank_log(json_obj['retCode'])
    return json_obj['retCode']


# 登录
def login():
    # 无法实现
    return
    data_send = {
        "wx_code": " ",
        "encryptedData": "",
        "iv": "",
        "wx_header": "https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJQjJicuBaUoibcTAgvgneFneGe78u5FDAYUV35QBFibwHJ97x2Nv0O5rQDGX8dwH3tmDlwas0REJLYQ/132",
        "wx_nickname": "XXX",
        "sex": "1",
        "loginType": 0
    }
    bank_log(str(datetime.today()) + ": login")
    postUrl = "https://mcs.creditcard.ecitic.com/citiccard/gwapi/uc/market/user/login"
    responseRes = bankSession.post(postUrl, headers=header, json=data_send, proxies=proxy_dict, verify=False)
    bank_log(f"statusCode = {responseRes.status_code}")
    json_obj = responseRes.json()
    bank_log(responseRes.text)
    bank_log(json_obj['retCode'])
    return json_obj['retCode']


# 获取game信息
def game_init():
    bank_log(str(datetime.today()) + ": game_init")
    # data_send ={"rhizomysId":rhizomysId,"timesPropId":"WRR_BAMBOO","timesPropNumber":1,"loginType":0}
    data_send = {"combine": 1, "loginType": 0}
    postUrl = "https://mcs.creditcard.ecitic.com/citiccard/gwapi/uc/market/game/gamePageinit"
    responseRes = bankSession.post(postUrl, headers=header, json=data_send, proxies=proxy_dict, verify=False)
    bank_log(f"statusCode = {responseRes.status_code}")

    json_obj = responseRes.json()

    if json_obj['retCode'] == '000000':
        global needCoin
        global totalCoin
        global currentValue
        global rhizomysId
        needCoin = json_obj['data']['levelCoin']['levelRes'][0]['needCoin']
        totalCoin = json_obj['data']['levelCoin']['totalCoin']
        currentValue = json_obj['data']['currentValue']
        rhizomysId = json_obj['data']['rhizomys'][0]['rhizomysId']
        bank_log("升级需要金币: " + str(needCoin))
        bank_log("当前金币总数: " + str(totalCoin))
        bank_log("可收获成长值: " + str(currentValue))

        global bambooNum
        global chiliNum
        global cornNum
        global blindBoxNum
        global variationFeedNum
        for prop in json_obj['data']['propInfo']:
            if prop['propParentKey'] == 'WRR_BAMBOO':
                bambooNum = prop['propNum']
                bank_log("竹子:" + str(prop['propNum']))
            elif prop['propParentKey'] == 'WRR_CHILI':
                chiliNum = prop['propNum']
                bank_log("辣椒:" + str(prop['propNum']))
            elif prop['propParentKey'] == 'WRR_CORN':
                cornNum = prop['propNum']
                bank_log("玉米" + str(prop['propNum']))
            elif prop['propParentKey'] == 'WRR_BLIND_BOX':
                blindBoxNum = prop['propNum']
                bank_log("盲盒:" + str(prop['propNum']))
            elif prop['propParentKey'] == 'WRR_VARIATION_FEED':
                variationFeedNum = prop['propNum']
                bank_log("饲料:" + str(prop['propNum']))
            else:
                bank_log(prop['propParentKey'] + str(prop['propNum']))
    elif json_obj['retCode'] == COOKIE_FAILED:
        bank_log(json_obj)
    else:
        bank_log(json_obj)

    return json_obj['retCode']


# 获取可收获成长值
def getHarvestGrowth():
    bank_log(str(datetime.today()) + ": getHarvestGrowth")
    data_send = {"rhizomysId": rhizomysId, "growthValue": 1367, "loginType": 0}
    postUrl = "https://mcs.creditcard.ecitic.com/citiccard/gwapi/uc/market/game/harvestGrowth"
    responseRes = bankSession.post(postUrl, headers=header, json=data_send, proxies=proxy_dict, verify=False)
    bank_log(f"statusCode = {responseRes.status_code}")
    json_obj = responseRes.json()
    if json_obj['retCode'] == SUCCESS_RET_CODE:
        bank_log("收取成长值成功:" + str(json_obj['data']['coin']))
    elif json_obj['retCode'] == COOKIE_FAILED:
        bank_log(responseRes.text)
        login()
    else:
        bank_log(responseRes.text)

    return json_obj['retCode']


# 每日运势
def fortuneLottery():
    bank_log(str(datetime.today()) + ": fortuneLottery")
    data_send = {"rhizomysId": rhizomysId, "loginType": 0}
    postUrl = "https://mcs.creditcard.ecitic.com/citiccard/gwapi/uc/market/lottery/fortuneLottery"
    responseRes = bankSession.post(postUrl, headers=header, json=data_send, proxies=proxy_dict, verify=False)
    bank_log(f"statusCode = {responseRes.status_code}")

    json_obj = responseRes.json()
    if json_obj['retCode'] == SUCCESS_RET_CODE:
        bank_log(json_obj['data'])
        send_msg_chat(u'每日运势:' + json_obj['data'])
    elif json_obj['retCode'] == COOKIE_FAILED:
        bank_log(responseRes.text)
        login()
    else:
        bank_log(responseRes.text)
        # send_msg_chat(responseRes.text)
    return json_obj['retCode']


# 升级
def rhizomysLevelUp():
    bank_log(str(datetime.today()) + ": rhizomysLevelUp")
    data_send = {"rhizomysId": rhizomysId, "totalCoin": totalCoin, "needCoin": needCoin, "loginType": 0}
    postUrl = "https://mcs.creditcard.ecitic.com/citiccard/gwapi/uc/market/game/rhizomysLevelUp"
    responseRes = bankSession.post(postUrl, headers=header, json=data_send, proxies=proxy_dict, verify=False)
    bank_log(f"statusCode = {responseRes.status_code}")

    json_obj = responseRes.json()
    if json_obj['retCode'] == SUCCESS_RET_CODE:
        bank_log(responseRes.text)
        send_msg_chat("升级成功" + responseRes.text)
    elif json_obj['retCode'] == COOKIE_FAILED:
        bank_log(responseRes.text)
        login()
    else:
        bank_log(responseRes.text)
    return json_obj['retCode']


# 我的奖品
def lotteryAndRewards():
    bank_log(str(datetime.today()) + ": lotteryAndRewards")
    data_send = {"lotteryPageSize": 5, "lotteryPageNo": 1, "loginType": 0}
    postUrl = "https://mcs.creditcard.ecitic.com/citiccard/gwapi/uc/market/lottery/lotteryAndRewards"
    responseRes = bankSession.post(postUrl, headers=header, json=data_send, proxies=proxy_dict, verify=False)
    bank_log(f"statusCode = {responseRes.status_code}")

    json_obj = responseRes.json()
    if json_obj['retCode'] == SUCCESS_RET_CODE:
        bank_log(json_obj['data'])
    elif json_obj['retCode'] == COOKIE_FAILED:
        bank_log(responseRes.text)
        login()
    else:
        bank_log(responseRes.text)
    return json_obj['retCode']


# 我的邀请 我觉得可以不需要
def assistance_query():
    bank_log(str(datetime.today()) + ": assistance_query")
    data_send = {
        "unionidDst": "",
        "pageNum": 1,
        "pageSize": 5,
        "loginType": 0
    }
    postUrl = "https://mcs.creditcard.ecitic.com/citiccard/gwapi/nouc/market/assistance/query"
    responseRes = bankSession.post(postUrl, headers=header, json=data_send, proxies=proxy_dict, verify=False)
    bank_log(f"statusCode = {responseRes.status_code}")
    json_obj = responseRes.json()
    if json_obj['retCode'] == SUCCESS_RET_CODE:
        bank_log(str(json_obj['data']))
    elif json_obj['retCode'] == COOKIE_FAILED:
        bank_log(responseRes.text)
        login()
    else:
        bank_log(responseRes.text)
    return json_obj['retCode']


# 加油
def assistance_enjoy(unionidDst):
    bank_log(str(datetime.today()) + ": 加油")
    data_send = {
        "unionidSrc": unionidSrc_self,
        "nickName": "whoareyou",
        "imageUrl": "https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJQjJicuBaUoibcTAgvgneFneGe78u5FDAYUV35QBFibwHJ97x2Nv0O5rQDGX8dwH3tmDlwas0REJLYQ/132",
        "unionidDst": unionidDst,
        "loginType": 0
    }

    postUrl = "https://mcs.creditcard.ecitic.com/citiccard/gwapi/market/assistance/enjoy"
    responseRes = bankSession.post(postUrl, headers=header, json=data_send, proxies=proxy_dict, verify=False)
    bank_log(f"statusCode = {responseRes.status_code}")

    json_obj = responseRes.json()
    if json_obj['retCode'] == SUCCESS_RET_CODE:
        bank_log('助力加油成功:' + json_obj)
        send_msg_chat(u'助力加油成功')
    elif json_obj['retCode'] == COOKIE_FAILED:
        bank_log(responseRes.text)
        login()
    else:
        bank_log(responseRes.text)
        # send_msg_chat(u'助力加油失败' )

    return json_obj['retCode']


# 喂东西，道具
'''
propParentKey=WRR_CHILI 辣椒
propParentKey=WRR_BLIND_BOX 盲盒
propParentKey=WRR_BAMBOO 竹子
propParentKey=WRR_CORN           玉米
propParentKey=WRR_VARIATION_FEED 饲料
'''


def feedRhizomys(timesPropId, timesPropNumber):
    bank_log(str(datetime.today()) + ": feedRhizomys")

    if timesPropNumber >= 10:
        timesPropNumber = 10
    if timesPropNumber < 10 and timesPropNumber >= 1:
        timesPropNumber = 1

    if timesPropId == 'WRR_BAMBOO':
        bank_log("喂竹子:" + str(timesPropNumber))
    elif timesPropId == 'WRR_CHILI':
        bank_log("喂辣椒:" + str(timesPropNumber))
    elif timesPropId == 'WRR_CORN':
        bank_log("喂玉米" + str(timesPropNumber))
    elif timesPropId == 'WRR_BLIND_BOX':
        bank_log("喂盲盒:" + str(timesPropNumber))
    elif timesPropId == 'WRR_VARIATION_FEED':
        bank_log("喂饲料:" + str(timesPropNumber))
    else:
        bank_log(timesPropId + str(timesPropNumber))

    data_send = {"rhizomysId": rhizomysId, "timesPropId": timesPropId, "timesPropNumber": timesPropNumber,
                 "loginType": 0}
    postUrl = "https://mcs.creditcard.ecitic.com/citiccard/gwapi/uc/market/game/feedRhizomys"
    responseRes = bankSession.post(postUrl, headers=header, json=data_send, proxies=proxy_dict, verify=False)
    bank_log(f"statusCode = {responseRes.status_code}")

    json_obj = responseRes.json()
    if json_obj['retCode'] == SUCCESS_RET_CODE:
        bank_log(responseRes.text)
        send_msg_chat("喂成功" + responseRes.text)
    elif json_obj['retCode'] == COOKIE_FAILED:
        bank_log(responseRes.text)
        login()
    else:
        bank_log(responseRes.text)
    return json_obj['retCode']


def heart_beat():
    retCode = game_init()
    if retCode == SUCCESS_RET_CODE:
        fortuneLottery()
        if currentValue > 0:
            getHarvestGrowth()

        # 每天 定时的
        current_time = datetime.now().time()
        running = False

        if DAY_START <= current_time <= DAY_END:
            running = True

        if totalCoin > needCoin and running:
            rhizomysLevelUp()

        if running:
            # 竹子
            if bambooNum > 0:
                feedRhizomys("WRR_BAMBOO", bambooNum)
            # 辣椒
            if chiliNum > 0:
                feedRhizomys("WRR_CHILI", chiliNum)
            # 玉米
            if cornNum > 0:
                feedRhizomys('WRR_CORN', cornNum)
            # 盲盒
            if blindBoxNum > 0:
                feedRhizomys("WRR_VARIATION_FEED", blindBoxNum)
            # 饲料
            # if variationFeedNum > 0:
            # feedRhizomys("WRR_VARIATION_FEED", variationFeedNum)

        rand_int_sleep = random.randint(-5, 5)
        threading.Timer(WAIT_TIME + rand_int_sleep, heart_beat).start()
    else:
        bank_log("退出程序： " + str(datetime.today()))


@itchat.msg_register(itchat.content.SHARING, isFriendChat=False, isGroupChat=True, )
def share_msg(msg):
    # bank_log(msg['Text'])
    if msg['Text'].find('鼠') >= 0:
        console_text = msg['Content']
        bank_log("为好友 " + msg['ActualNickName'] + " 助力:")
        matchObj = re.match('.*&unionid=(.*?)&', console_text, re.DOTALL)
        if matchObj:
            unionid = matchObj.group(1).strip()
            # bank_log("unionid:",unionid)
            assistance_enjoy(unionid)
        else:
            bank_log("Can't found unionid")


def open_chat():
    itchat.auto_login(hotReload=True)
    global chat_login
    chat_login = True
    itchat.run()


if __name__ == '__main__':
    # 创建两个线程
    try:
        # 如果你不需要微信可以注销
        _thread.start_new_thread(open_chat, ())
        _thread.start_new_thread(heart_beat, ())
    except:
        bank_log("Error: 无法启动线程")

    while 1:
        pass
