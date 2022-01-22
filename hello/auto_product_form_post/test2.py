import requests

common_headers = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Connection: keep-alive
Content-Length: 738
Content-Type: application/x-www-form-urlencoded
Cookie: security_session_verify=95ae91ad67b94034c35081f516c1d7fb; security_session_mid_verify=c9a505fda0f2278f86619680041ba8ca; home_lang=cn; PHPSESSID=4kc8bfuedeso6v60a5f8lnlekb; admin_lang=cn;
Host: yiyou.yueshengj.com
Origin: http://yiyou.yueshengj.com
Referer: http://yiyou.yueshengj.com/login.php?m=admin&c=Article&a=add&typeid=1&gourl=http%3A%2F%2Fyiyou.yueshengj.com%2Flogin.php%3Fm%3Dadmin%26c%3DArchives%26a%3Dindex_archives%26typeid%3D1%26lang%3Dcn&lang=cn
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"""


def get_headers(header_raw):
    """
    通过原生请求头获取请求头字典
    :param header_raw: {str} 浏览器请求头
    :return: {dict} headers
    """
    return dict(line.strip().split(": ", 1) for line in header_raw.split("\n"))


def get_form_data(data_raw):
    """
    """
    tmp_list = []
    for line in data_raw.split("\n"):
        line_s = line.strip().split(": ", 1)
        tmp_list.append(line_s if len(line_s) == 2 else line_s + [''])
    return dict(tmp_list)


data_raw = """title: 标题33
subtitle: 副标题11
typeid: 1
is_litpic: 1
jumplinks: 
tags: 标签1,标签2,标签3
province_id: 0
city_id: 
area_id: 
litpic_local: /uploads/allimg/20220109/1-220109162GK07.jpg
litpic_remote: 
restric_type: 0
arc_level_id: 1
users_price: 
part_free: 0
size: 1
addonFieldExt[content]: <p>内容1&nbsp;</p>
seo_title: SEO标题 11
seo_keywords: 标签1,标签2,标签3
seo_description: SEO描述11
author: adminyiyou
origin: 
click: 531
arcrank: 0
add_time: 2022-01-09 16:24:33
tempview: view_article.htm
type_tempview: view_article.htm
htmlfilename: 
free_content: 
gourl: """

url = 'http://yiyou.yueshengj.com/login.php?m=admin&c=Article&a=add&lang=cn'
rep = requests.post(url, data=get_form_data(data_raw), headers=get_headers(common_headers))
print(rep.text)
print(rep.status_code)
