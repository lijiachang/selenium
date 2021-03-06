# -*- coding:utf-8 -*-
import json
import os
import random
import requests
import re
from logger import logger
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from collections import namedtuple
from pip._vendor.retrying import retry
from openpyxl import load_workbook

################# 配置区 ##############################################################################################
domain = 'yiyou.01taizhou.com'  # 网站地址 www.xxx.com
domain_index = 'http://yiyou.01taizhou.com/login.php?s=Admin/login'  # 管理后台的页面URL
username = 'adminyiyou'  # 后台管理用户名
password = '8210784124yiyou'  # 后台管理密码

images_path = 'G:\地中海家装案例（70套 1493张 4.04G）\裁剪大小'  # 图片库路径目录
# Excel配置
excel_name = 'lawcdyc2.xlsm'
sheet_name = 'Sheet1'
# 替换的关键字
replace_string = {'需要替换的文字': '替换后的文字', '_x000D_': '', }

# 配置定时任务
daily_task = 2  # 每天发布的文章数量
job_time = '01:10'  # 每天的什么时候发布
delay = 5  # 发布时间间隔的，比如间隔5秒发布一篇, 单位是秒

######################################################################################################################

common_headers = """Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: security_session_verify={security_session_verify}; security_session_mid_verify={security_session_mid_verify}; home_lang=cn; PHPSESSID={PHPSESSID}; admin_lang=cn
Host: {domain}
Origin: http://{domain}
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
X-Requested-With: XMLHttpRequest"""

# 发布的headers样例：
"""Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Connection: keep-alive
Content-Length: 657
Content-Type: application/x-www-form-urlencoded
Cookie: security_session_verify=157a6ddd471ef0b999f7664ca8e96d12; PHPSESSID=nhl6c9c6se7bbnlflq89cvkm0a; admin_lang=cn; home_lang=cn; ENV_UPHTML_AFTER=%7B%22seo_uphtml_after_home%22%3A%221%22%2C%22seo_uphtml_after_channel%22%3A%221%22%2C%22seo_uphtml_after_pernext%22%3A%221%22%7D; users_id=1; admin-arctreeClicked-Arr=null; ENV_GOBACK_URL=%2Flogin.php%3Fm%3Dadmin%26c%3DArchives%26a%3Dindex_archives%26lang%3Dcn; ENV_LIST_URL=%2Flogin.php%3Fm%3Dadmin%26c%3DArchives%26a%3Dindex_archives%26lang%3Dcn; admin-treeClicked-Arr=null; workspaceParam=index%7CArchives; ENV_IS_UPHTML=0
Host: yiyou.01taizhou.com
Origin: http://yiyou.01taizhou.com
Referer: http://yiyou.01taizhou.com/login.php?m=admin&c=Article&a=add&typeid=1&gourl=http%3A%2F%2Fyiyou.01taizhou.com%2Flogin.php%3Fm%3Dadmin%26c%3DArchives%26a%3Dindex_archives%26typeid%3D1%26lang%3Dcn&lang=cn
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"""

LINE = namedtuple('LINE', 'id create_time title key_words tag content')


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


class SingletonPHPSESSID:
    __instance = None
    __init_flag = False  # 是否初始化过

    def __new__(cls, *args, **kwargs):
        if cls.__instance:
            return cls.__instance
        else:
            cls.__instance = object.__new__(cls)
            return cls.__instance

    def __init__(self):
        if not self.__init_flag:
            self.session_id, self.security_session_verify, self.security_session_mid_verify = self.login()
            self.__init_flag = True
        else:
            pass

    def login(self):
        """登录成功后变为有效id"""
        form = {'user_name': username,
                'password': password}
        url = 'http://{domain}/login.php?m=admin&c=Admin&a=login&_ajax=1&lang=cn&t=0.6388018966483218'.format(
            domain=domain)
        _session_id, security_session_verify, security_session_mid_verify = self.get_session_id()
        rep = requests.post(url, data=form,
                            headers=get_headers(common_headers.format(domain=domain, PHPSESSID=_session_id,
                                                                      security_session_verify=security_session_verify,
                                                                      security_session_mid_verify=security_session_mid_verify)))
        if '登录成功' in rep.text:
            logger.info('登录成功: _session_id={}'.format(_session_id))
            return _session_id, security_session_verify, security_session_mid_verify
        else:
            logger.info(rep.text)
            return False, False, False

    def get_cookies(self, url):
        """
        破解云锁服务器安全软件
        来源https://blog.csdn.net/baidu_36146918/article/details/89928154
        """

        resp = requests.get(url, timeout=5)
        cookie = {}
        for key, value in resp.cookies.items():
            cookie[key] = value
            print(f'{key}: {value}')
        security_session_verify = resp.cookies.get('security_session_verify')

        resp = requests.get(
            '{}{}'.format(url, '?security_verify_data=313932302c31303830'),
            cookies=cookie
        )

        for key, value in resp.cookies.items():
            cookie[key] = value
            print(f'{key}: {value}')
        security_session_mid_verify = resp.cookies.get('security_session_mid_verify')
        return security_session_verify, security_session_mid_verify

    def get_session_id(self):
        """获取响应标头里面的id
        Set-Cookie: PHPSESSID=pe9a66n4ffcuiddahf5rj8s4tp; path=/
        """
        headers = """Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: security_session_verify={security_session_verify}; security_session_mid_verify={security_session_mid_verify}; home_lang=cn; admin_lang=cn
Host: {domain}
Origin: http://{domain}
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
X-Requested-With: XMLHttpRequest"""
        url = domain_index
        security_session_verify, security_session_mid_verify = self.get_cookies(url)
        rep = requests.get(url, allow_redirects=False, headers=get_headers(
            headers.format(domain=domain, security_session_verify=security_session_verify,
                           security_session_mid_verify=security_session_mid_verify)))

        PHPSESSID = rep.headers.get('Set-Cookie')  # PHPSESSID=pe9a66n4ffcuiddahf5rj8s4tp; path=/
        logger.info('login get response headers Set-Cookie:{}'.format(PHPSESSID))
        PHPSESSID = PHPSESSID.split(';')[0].split('=')[1]  # pe9a66n4ffcuiddahf5rj8s4tp
        logger.info('login PHPSESSID:{}'.format(PHPSESSID))
        return PHPSESSID, security_session_verify, security_session_mid_verify


class ArticleForm:
    remote_images = []  # 网络空间的略缩图

    def __init__(self, headers_raw, line: LINE):
        self.php_session_id = SingletonPHPSESSID().session_id
        self.security_session_verify = SingletonPHPSESSID().security_session_verify
        self.security_session_mid_verify = SingletonPHPSESSID().security_session_mid_verify

        self.headers = get_headers(headers_raw.format(domain=domain, PHPSESSID=self.php_session_id,
                                                      security_session_verify=self.security_session_verify,
                                                      security_session_mid_verify=self.security_session_mid_verify))
        # self.access_key, self.cat_id_map = self.init_publish_page()
        self.line = line

    def publish(self):
        """发布一篇文章"""

        # 上传略缩图
        # 在目录下随机找一张图片
        random_image_file_path = random.choice(self.get_raw_file_list(images_path))
        # 上传图片到网站
        image_url = self.post_image(random_image_file_path)

        # 发布文章
        publish_result = self.post_article(image_url)

    @staticmethod
    def get_raw_file_list(path):
        """-------------------------
        files,names=getRawFileList(raw_data_dir)
        files: ['datacn/dialog/one.txt', 'datacn/dialog/two.txt']
        names: ['one.txt', 'two.txt']
        ----------------------------"""
        files = []
        # names = []
        for f in os.listdir(path):
            if not f.endswith("~") or not f == "":  # 返回指定的文件夹包含的文件或文件夹的名字的列表
                if f.endswith('jpg'):  # 限制jpg格式图片
                    files.append(os.path.join(path, f))  # 把目录和文件名合成一个路径
                    # names.append(f)
        return files

    def post_image(self, image_path):
        """上传略缩图
        请求 URL: http://yiyou.01taizhou.com/login.php?m=admin&c=Ueditor&a=imageUp&savepath=allimg&pictitle=banner&dir=images&is_water=1&lang=cn

        表单：
        _ajax: 1
        file: （二进制）
        type_id: 0

        响应：
        height: 270
        img_id: "2"
        original: "001_42.JPG"
        path: "images"
        state: "SUCCESS"
        time: 1645107945
        title: "banner"
        url: "/uploads/allimg/20220217/1-22021H22545306.JPG"
        width: 420
        """
        url = 'http://{}/login.php?m=admin&c=Ueditor&a=imageUp&savepath=allimg&pictitle=banner&dir=images&is_water=1&lang=cn'.format(
            domain)
        form = {'_ajax': 1,
                'type_id': 0}
        multipart_form_data = {key: (None, value) for key, value in form.items()}
        multipart_form_data['file'] = (image_path, open(image_path, 'rb'), 'image/jpeg')

        post_images_headers = self.headers.copy()
        del post_images_headers['Content-Type']  # 记得不用填 heads中content-type ，不用传， 不用传 ，不用传, 否则上传不成功， 提示：请检查空间是否开启文件上传功能！

        rep = requests.post(url, files=multipart_form_data, headers=post_images_headers)
        rep_text = rep.text
        if 'SUCCESS' in rep_text:
            print('略缩图上传成功:{}'.format(rep_text))
            image_url = rep.json().get('url')
            return image_url
        else:
            print('略缩图上传失败:{}'.format(rep_text))
            return ''

    def post_article(self, image_url):
        """发布文章内容
        请求URL: http://yiyou.01taizhou.com/login.php?m=admin&c=Article&a=add&lang=cn

        表单
        title: 标题111
        subtitle:
        typeid: 1
        jumplinks:
        tags: TAG标签1,TAG标签2,TAG标签3
        province_id: 0
        city_id:
        area_id:
        litpic_local: /uploads/allimg/210421/thumb_pc_20190314222006_73478.jpg
        litpic_remote:
        restric_type: 0
        arc_level_id: 1
        users_price:
        part_free: 0
        size: 1
        addonFieldExt[content]: <p>内容121</p>
        seo_title: SEO标题 11
        seo_keywords: TAG标签1,TAG标签2,TAG标签3
        seo_description: SEO描述111
        author: adminyiyou
        origin:
        click: 786
        arcrank: 0
        add_time: 2022-02-17 21:50:07
        tempview: view_article.htm
        type_tempview: view_article.htm
        htmlfilename:
        free_content:
        gourl:

        发布成功后，rep.txt 里面有成功发布文档提示
        """
        form = {
            'title': self.line.title,
            'subtitle': '',  # 副标题
            'typeid': 1,
            'jumplinks': '',
            'tags': self.line.tag,
            'province_id': 0,
            'city_id': '',
            'area_id': '',
            'litpic_local': image_url,
            'litpic_remote': '',
            'restric_type': 0,
            'arc_level_id': 1,
            'users_price': '',
            'part_free': 0,
            'size': 1,
            'addonFieldExt[content]': '<p>{}</p>'.format(self.line.content),
            'seo_title': self.line.title,
            'seo_keywords': self.line.tag,
            'seo_description': self.line.content[:50],
            'author': 'adminyiyou',
            'origin': '',
            'click': 786,
            'arcrank': 0,
            'add_time': time.strftime("%Y-%m-%d %H:%M:%S"),
            'tempview': 'view_article.htm',
            'type_tempview': 'view_article.htm',
            'htmlfilename': '',
            'free_content': '',
            'gourl': '', }
        #
        # # 增加cat_id 关联城市
        # for cat_id, city_name in self.cat_id_map.items():
        #     if city_name in self.line.title:
        #         form['cat_id[]'].append(cat_id)  # 在一个post中提交含有多个相同名称的数据

        url = 'http://{}/login.php?m=admin&c=Article&a=add&lang=cn'.format(domain)
        rep = requests.post(url, data=form, headers=self.headers)
        rep_text = rep.text
        if '成功' in rep_text:
            logger.info('id={} 发布成功: {}'.format(self.line.id, self.line.title))
        else:
            logger.info('！！！id={} 发布失败: {}'.format(self.line.id, self.line.title))

        return rep_text


def write_title_to_cache(num):
    """缓存line"""
    with open('cache', 'w') as file_ob:
        file_ob.write(str(num))


def read_title_from_cache():
    """读取缓存line"""
    try:

        with open('cache', 'r') as file_ob:
            num = file_ob.read()
            num = int(num)
    except Exception as e:
        logger.info('no read_index_from_cache:{}'.format(e))
        num = None
    return num


def analysis_line(line):
    """line eg.
    A                   F
    序号	时间	标题	标签	tag	内容
1		台州70平米的服装装修大概多少钱	台州,70,平米,服装,大概,多少钱	台州,70,平米,服装,大概,多少钱	"必要店面现状，大备注，小项目，重整修需求，这个人才多是个人。</p>
<p><p><br/></p><p><img src=""/images/tu01/Image_307.jpg""title=""台州70平米的服装装修大概多少钱""  alt=""台州70平米的服装装修大概多少钱""/></p><p><br/></p><p><strong>台州70平方米装修费用要多少哪里找这么大房子的装修案例？</strong></p><p>服装店</p>
    """

    title = line[2].value  # 标题
    key_words = line[3].value  # 标签
    tag = line[4].value  # tag
    content = line[5].value  # 内容
    if title and key_words and tag and content:
        for string, rep_string in replace_string.items():
            title = title.replace(string, rep_string)
            key_words = key_words.replace(string, rep_string)
            tag = tag.replace(string, rep_string)
            content = content.replace(string, rep_string)

        return LINE('', '', title, key_words, tag, content)
    else:
        raise Exception('单元格内容为空，跳过')


def gen_read_inventory():
    data = load_workbook(excel_name, read_only=True)  # 读取excel表
    sheet = data[sheet_name]  # 读取表名

    cache_row_index = read_title_from_cache()
    gen_sheet = enumerate(sheet)

    next(gen_sheet)  # 跳过第一行： 序号	时间	标题	title	tag	内容

    # 读取到上次暂停处
    if cache_row_index:
        while True:
            row_index, _ = next(gen_sheet)
            if row_index == cache_row_index:
                break

    for row_index, sheet_line in gen_sheet:
        try:
            line_ = analysis_line(sheet_line)  # 提取正确的一行
        except Exception as e:
            logger.error('read line err:{}'.format(e))
            continue
        else:
            write_title_to_cache(row_index)
            yield line_


gen_tasks = gen_read_inventory()


# 最开始初始化一次空间略缩图
# ArticleForm(common_headers, '').save_all_remote_images()


# 若出现错误，重试3次，每次间隔1小时
# @retry(stop_max_attempt_number=3, wait_fixed=1000 * 60 * 60)
def job():
    # 确保下次任务需要先登录
    SingletonPHPSESSID.__init_flag = False
    SingletonPHPSESSID.__instance = None
    SingletonPHPSESSID._SingletonPHPSESSID__instance = None
    for _ in range(daily_task):
        try:
            line_info = next(gen_tasks)

            # 初始化
            article = ArticleForm(common_headers, line_info)
            # 发布一条
            article.publish()

            # 休息1秒，减轻服务器压力
            time.sleep(1)
        except StopIteration:
            logger.info('{} 内的文章已经全部发布完成，请更新'.format(excel_name))

print(111111)
job()  # 第一次运行的时候，先发布一次
print(22222)
job()  # 第一次运行的时候，先发布一次2

scheduler = BlockingScheduler()
# 在每天2点的25分，运行一次 job 方法
hour = job_time.split(':')[0]
minute = job_time.split(':')[1]
scheduler.add_job(job, 'cron', max_instances=10, hour=hour, minute=minute, misfire_grace_time=3600)
scheduler.start()

