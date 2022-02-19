import requests

header = """Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary21m6eVoo8F04iAXm
Cookie: security_session_verify=29fd5fd0b92a905571978c45fb629652; PHPSESSID=9pb2lhbovt61e87nvl5ah7dgod; admin_lang=cn; home_lang=cn; ENV_UPHTML_AFTER=%7B%22seo_uphtml_after_home%22%3A%221%22%2C%22seo_uphtml_after_channel%22%3A%221%22%2C%22seo_uphtml_after_pernext%22%3A%221%22%7D; users_id=1; workspaceParam=index%7CArchives; admin-arctreeClicked-Arr=null; ENV_GOBACK_URL=%2Flogin.php%3Fm%3Dadmin%26c%3DArchives%26a%3Dindex_archives%26lang%3Dcn; ENV_LIST_URL=%2Flogin.php%3Fm%3Dadmin%26c%3DArchives%26a%3Dindex_archives%26lang%3Dcn; ENV_IS_UPHTML=0; img_id_upload=
Host: yiyou.yueshengj.com
Origin: http://yiyou.yueshengj.com
Referer: http://yiyou.yueshengj.com/login.php?m=admin&c=Uploadimgnew&a=get_upload_list&info=eyJudW0iOjEsInNpemUiOjUyNDI4ODAwLCJpbnB1dCI6IiIsImZ1bmMiOiJpbWdfY2FsbF9iYWNrIiwicGF0aCI6ImFsbGltZyIsImlzX3dhdGVyIjoxfQ%3D%3D&lang=cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
X-Requested-With: XMLHttpRequest"""

def get_headers(header_raw):
    """
    通过原生请求头获取请求头字典
    :param header_raw: {str} 浏览器请求头
    :return: {dict} headers
    """
    return dict(line.strip().split(": ", 1) for line in header_raw.split("\n"))

domain = 'yiyou.yueshengj.com'  # 网站地址 www.xxx.com

url = 'http://{}/login.php?m=admin&c=Ueditor&a=imageUp&savepath=allimg&pictitle=banner&dir=images&is_water=1&lang=cn'.format \
    (domain)
form = {'_ajax': 1,
        'type_id': 0}
multipart_form_data = {key: (None, value) for key, value in form.items()}
multipart_form_data['file'] = ('001_01.jpg', open('001_01.jpg', 'rb'), 'image/jpeg')  # todo 临时hack

# files = {
#     "file": (image_path, open(image_path, 'rb'), "image/jpeg")
# }
rep = requests.post(url, files=multipart_form_data, headers=get_headers(header))
rep_text = rep.text
print(rep_text)
# 请检查空间是否开启文件上传功能！