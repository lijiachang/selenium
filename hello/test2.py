# coding:utf-8

import requests

headers_str = """Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Cookie: bid=-6gENow_E0c; __utmz=30149280.1614418005.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%23%E5%90%B4%E5%AD%9F%E8%BE%BE%E5%8E%BB%E4%B8%96%23; ap_v=0,6.0; __utma=30149280.2026197266.1611584998.1614418005.1614690806.4; __utmc=30149280; __utmt=1; __utmb=30149280.1.10.1614690806
Host: m.douban.com
Origin: https://www.douban.com
Referer: https://www.douban.com/gallery/topic/27196/?qq-pf-to=pcqq.c2c
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"""


def get_headers(header_raw):
    """
    通过原生请求头获取请求头字典
    :param header_raw: {str} 浏览器请求头
    :return: {dict} headers
    """
    return dict(line.strip().split(": ", 1) for line in header_raw.split("\n"))


url = 'https://m.douban.com/rexxar/api/v2/gallery/topic/27196/items?from_web=1&sort=hot&start=0&count=20&status_full_text=1&guest_only=0&ck=null'

res = requests.get(url, headers=get_headers(headers_str))
print res.content.decode('unicode-escape')
