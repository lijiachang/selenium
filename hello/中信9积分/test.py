import re
import time
import json
import requests


def get_headers(header_raw):
    """
    通过原生请求头获取请求头字典
    :param header_raw: {str} 浏览器请求头
    :return: {dict} headers
    """
    return dict(line.strip().split(": ", 1) for line in header_raw.split("\n"))


def get_validate(gt, challenge):
    kancloud_api = "http://api.z-fp.com/start_handle"

    data = {'username': '944581577',
            'appkey': '10efd9357c3e9c3c03da06e89ecb6198',
            'gt': gt,  # 这个不变
            'challenge': challenge,
            'referer': 'https://dknp.e-pointchina.com.cn/citiccrd_mall/html/index.html',
            'handle_method': 'three_on'}

    t0 = time.time()
    rep = requests.post(kancloud_api, data=data)
    print(rep.text)
    validate = json.loads(rep.text).get('data').get('validate')
    print('validate: ' + validate)
    print('kancloud_api use time:{}'.format(time.time() - t0))
    return validate


def get_gt_challenge(cookie_):
    headers = """Host: dknp.e-pointchina.com.cn
    Connection: keep-alive
    Content-Length: 0
    Accept: application/json, text/plain, */*
    User-Agent: Mozilla/5.0 (Linux; Android 11; M2011K2C Build/RKQ1.200928.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 DKKJ/8.0.1/[DKKJ_TOWER_1.3] dkkj_channel_id/DKKJ/UnionPay/1.0 DKKJ
    Origin: https://dknp.e-pointchina.com.cn
    X-Requested-With: com.citiccard.mobilebank
    Sec-Fetch-Site: same-origin
    Sec-Fetch-Mode: cors
    Sec-Fetch-Dest: empty
    Referer: https://dknp.e-pointchina.com.cn/citiccrd_mall/html/index.html
    Accept-Encoding: gzip, deflate
    Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
    Cookie: {}"""

    data = {'tag': 'JFXD001',
            'term': '202103',
            'payment_id': 'IP00995',  # 会变动，每个商品对应一个支付ID？
            'item_id': '00000177486be2b90001a701',  # 商品ID
            'serviceMethod': 'createCaptcha',
            'serviceType': 'com.ebuy.citiccrd.mall.web.service.UserOrderService',
            'redirect_url': 'index.html%23%2Fconfirm'}

    url = "https://dknp.e-pointchina.com.cn/citiccrd_mall/cloudDataService.do"
    rep = requests.post(url, data=data, headers=get_headers(headers.format(cookie_)))
    print(rep.text)
    gt = re.search('<gt_id>(.*?)</gt_id>', rep.text).group(1)
    challenge = re.search('<gt_trans>(.*?)</gt_trans>', rep.text).group(1)
    print('gt: ' + gt)
    print('challenge: ' + challenge)
    return gt, challenge


def get_order(cookie_, challenge_, validate_):
    headers = """Host: dknp.e-pointchina.com.cn
                Connection: keep-alive
                Content-Length: 0
                Accept: application/json, text/plain, */*
                User-Agent: Mozilla/5.0 (Linux; Android 11; M2011K2C Build/RKQ1.200928.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 DKKJ/8.0.1/[DKKJ_TOWER_1.3] dkkj_channel_id/DKKJ/UnionPay/1.0 DKKJ
                Origin: https://dknp.e-pointchina.com.cn
                X-Requested-With: com.citiccard.mobilebank
                Sec-Fetch-Site: same-origin
                Sec-Fetch-Mode: cors
                Sec-Fetch-Dest: empty
                Referer: https://dknp.e-pointchina.com.cn/citiccrd_mall/html/index.html
                Accept-Encoding: gzip, deflate
                Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
                Cookie: {}"""

    data = {'tag': 'JFXD001',
            'term': '202103',
            'payment_id': 'IP00995',  # 会变动，每个商品对应一个支付ID？
            'item_id': '00000177486be2b90001a701',  # 商品ID
            'serviceMethod': 'verifyCaptcha',
            'serviceType': 'com.ebuy.citiccrd.mall.web.service.UserOrderService',
            'redirect_url': 'index.html%23%2Fconfirm',
            'address_id': '',
            'gt_server_status': '1',
            'gt_challenge': challenge_,
            'gt_validate': validate_,
            'gt_seccode': validate_ + '%7Cjordan',  # |是否要转义为%7C
            'mobile': ''
            }

    url = "https://dknp.e-pointchina.com.cn/citiccrd_mall/cloudDataService.do"
    rep = requests.post(url, data=data, headers=get_headers(headers.format(cookie_)))
    print(rep.text)  # 正常的响应code应该是000000


if __name__ == '__main__':
    cookie = "utm_source=ctask; uuid=e9428987-ae9d-44d2-820e-d2fd48bb46be; JSESSIONID=1DEBF083720883352605CF376EB6F936; authTicket=citiccrd_mall0000017cd102e8550003dbed4ac9155ac320fa226ab31a0efef529d4; crdcitycode=010; crdgpscitycode=010; Hm_lvt_e78ea3a4bbceabaa52b33ceda4219b55=1635591078,1635592675,1635592778,1635592935; Hm_lpvt_e78ea3a4bbceabaa52b33ceda4219b55=1635594073"
    cookie = "utm_source=ctask; uuid=687f2d4f-61ae-46c3-b94e-cd0cddccf07c; authTicket=citiccrd_mall0000017cd1125df3000020fd6c9ca686e0db7cd25bee9113a19fceb0; JSESSIONID=72764F4DC0F84A4B3644214CAA34EAC1; crdcitycode=010; crdgpscitycode=010; Hm_lvt_e78ea3a4bbceabaa52b33ceda4219b55=1635591078,1635592675,1635592778,1635592935; Hm_lpvt_e78ea3a4bbceabaa52b33ceda4219b55=1635595208"
    gt, challenge = (get_gt_challenge(cookie))  # 获取本次滑块验证码的上下文
    # gt = "9aa006e2fe22b4b1d9c9823147db97e1"
    # challenge = "df37154575845cb3a5ffb9e11646c7fahc"
    validate = get_validate(gt, challenge)  # 滑块打码
    time.sleep(2)
    # 提交订单
    get_order(cookie, challenge, validate)
    # cookie失效：网络繁忙，请稍后再试
