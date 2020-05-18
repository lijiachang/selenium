# coding:utf-8

import requests
from bs4 import BeautifulSoup


# DC1 24
# w3  197
def get_cart_md5():
    product_id = "24"
    id_url = "https://mall.phicomm.com/cart-fastbuy-{0}-1.html?vsid=43105230377".format(product_id)
    referer = 'https://mall.phicomm.com/item-{0}.html'.format(product_id)

    buy_url = r"https://mall.phicomm.com/checkout-fastbuy.html"
    cookie_init = "_VMC_UID=73a11f5bafa1f75ef1430a793112c49e; __jsluid=d1dc9fcbf7be9f60ddd6f5e78e03f5f0; _SID=032b033d7e2fdf947f6848f62d0299d4; Hm_lvt_c8bb97be004001570e447aa3e00ff0ad=1537407253,1537408291; c_dizhi=611816; c_peisong=1; c_zhifu=alipay; from_vshopid=43105230377; UNAME=18854831825; MEMBER_IDENT=3054837; MEMBER_LEVEL_ID=1; CACHE_VARY=f19d975b1edbcefe1553d7f59e3294bc-0f063e018c840f8a56946ecec41a6c18; Hm_lpvt_c8bb97be004001570e447aa3e00ff0ad=1537419922"
    # cookie_init = "_VMC_UID=73a11f5bafa1f75ef1430a793112c49e; __jsluid=d1dc9fcbf7be9f60ddd6f5e78e03f5f0"

    # 请求头
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'max-age=0',
               'Connection': 'max-age=0',
               'Cookie': cookie_init,
               'Host': 'mall.phicomm.com',
               'Referer': referer,
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
               }

    # 给服务器商品ID
    post_page1 = requests.get(url=id_url, headers=headers)

    # 获取下单界面详情，以寻找md5 认证串
    post_page2 = requests.get(buy_url, headers=headers)
    print post_page2.text
    soup = BeautifulSoup(post_page2.text, "html.parser")


    inputs_cart_md5 = soup.find_all('input', attrs={'name': 'cart_md5'})
    inputs_addr_id = soup.find_all('input', attrs={'name': 'addr_id', 'type': 'radio', 'class': 'hide dz_hide'})
    cart_md5 = inputs_cart_md5[0].get('value') if inputs_cart_md5 else "not found cart_md5!"
    addr_id = inputs_addr_id[0].get('value') if inputs_addr_id else "not found addr_id!"
    return cart_md5, addr_id


a,b = get_cart_md5()
print a
print b
