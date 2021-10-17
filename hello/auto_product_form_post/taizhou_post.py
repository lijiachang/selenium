import requests

domain = 'www.taizhou66.com'

common_headers = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Content-Length: 1019
Content-Type: application/x-www-form-urlencoded
Cookie: PHPSESSID=p7dfumfbqsmcg0nopjv5dhcf3l
Host: www.taizhou66.com
Origin: http://{0}
Referer: http://{0}/index.php?m=site&c=content&a=product_form
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"""

common_form = """timesend: 2021-10-12 21:10:03
access_key: 61659685e6e62
info[title]: 3222利津县115平的房子装修大概多少钱
info[seo_title]: 333222利津县115平的房子装修大概多少钱
info[keywords]: 33222利津县,115,平,房子,装修,大概,多少钱
info[description]: 222前50字符
submit1: ok
info[id]: 51
is_auto_save: 1
info[status]: 
http_referer: http://{0}/index.php?m=site&c=content&a=product_index
status: 1
cat_id[]: 4
copy_id: 
tag_content: ,3369,3370,3371,3372,3373,3374,3375
info[filename]: 
info[listorder]: 
iscopy: 0
content: <p>一平方600到1000!也就是7万到12万左右!</p>"""


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


post_url = 'http://{}/index.php?m=site&c=content&a=product_form'.format(domain)
rep = requests.post(post_url,
              headers=get_headers(common_headers.format(domain)),
              data=get_form_data(common_form.format(domain)))
print(rep.text)