# -*- coding: utf-8 -*-


# 有道云笔记自动登陆签到看广告获取空间，配合腾讯云函数python3.6
import requests
# server酱开关，填0不开启(默认)，填1只开启cookie失效通知，填2同时开启cookie失效通知和签到成功通知
sever = '0'
# 填写server酱sckey,不开启server酱则不用填
sckey = ''
# 填入有道云笔记客户端抓包的cookie
cookie = '_ntes_nnid=69465d7f8b4cda9a06b9364e4fb2a3a2,1586678492225; OUTFOX_SEARCH_USER_ID_NCOO=322168544.8140284; OUTFOX_SEARCH_USER_ID="-1583303755@10.108.160.18"; JSESSIONID=aaa-0YHKhOuXV7eCeWgix; Hm_lpvt_30b679eb2c90c60ff8679ce4ca562fcc=1589261661; Hm_lvt_30b679eb2c90c60ff8679ce4ca562fcc=1589261661; __yadk_uid=CmtysvAUOVCGsI1II65YOYoPNpbpk7Ut; _ga=GA1.2.191706967.1589261668; _gid=GA1.2.792780996.1589261668; _gat=1; YNOTE_SESS=v2|eoI-7nklLyOE0HUW6LOMRezhMQL0HY50gFn4PBnLpS0gFhfTBhLJz0Qz64QLkLJyReL0fzMhfJLRkGnfgZOfQZ0QyhMzE0HlER; YNOTE_PERS=v2|urstoken||YNOTE||web||-1||1589261675017||221.217.51.17||m15269026760_1@163.com||zMkfOW6LqB0zERHe4hHguRQFk4JFn4wF0gF0MPLnMOl06FhfqzhHlE0zYOMqunfTBRQunMQFkMTS0Ym64UfOLQB0; YNOTE_LOGIN=3||1589261675026; YNOTE_CSTK=kZ1R8aJf'

def start():
  ad=0
  payload = 'yaohuo:id34976'
  headers = {'Cookie': cookie}
  re = requests.request("POST", "https://note.youdao.com/yws/api/daupromotion?method=sync", headers=headers, data = payload)
  if 'error' not in re.text:
    res = requests.request("POST", "https://note.youdao.com/yws/mapi/user?method=checkin", headers=headers, data = payload)
    for i in range(3):
      resp = requests.request("POST", "https://note.youdao.com/yws/mapi/user?method=adRandomPrompt", headers=headers, data = payload)
      ad += resp.json()['space'] // 1048576
      print(re.text, res.text, resp.text)
    if sever == '2':
      if 'reward' in re.text:
        sync = re.json()['rewardSpace'] // 1048576
        checkin = res.json()['space'] // 1048576
        requests.get('https://sc.ftqq.com/' + sckey + '.send?text=有道云笔记签到成功共获得空间' + str(sync + checkin + ad) + 'M')
  else:
    if sever != '0':
      requests.get('https://sc.ftqq.com/' + sckey + '.send?text=有道云笔记签到cookie失效请更新')


def main_handler(event, context):
  return start()

if __name__ == '__main__':
  start()

"""
(u'{"rewardTime":1589261744293,"rewardSpace":1048576,"totalRewardSpace":11534336,"continuousDays":1,"accept":true}', u'{"total":65011712,"success":1,"time":1589261744526,"space":3145728}', u'{"isReachLimit":false,"secondNotChosenSpace":8388608,"success":true,"firstNotChosenSpace":2097152,"todayCount":1,"space":3145728,"adSpaceTotal":3145728}')
(u'{"rewardTime":1589261744293,"rewardSpace":1048576,"totalRewardSpace":11534336,"continuousDays":1,"accept":true}', u'{"total":65011712,"success":1,"time":1589261744526,"space":3145728}', u'{"isReachLimit":false,"secondNotChosenSpace":9437184,"success":true,"firstNotChosenSpace":2097152,"todayCount":2,"space":4194304,"adSpaceTotal":7340032}')
(u'{"rewardTime":1589261744293,"rewardSpace":1048576,"totalRewardSpace":11534336,"continuousDays":1,"accept":true}', u'{"total":65011712,"success":1,"time":1589261744526,"space":3145728}', u'{"isReachLimit":true,"secondNotChosenSpace":7340032,"success":true,"firstNotChosenSpace":1048576,"todayCount":3,"space":3145728,"adSpaceTotal":10485760}')

"""