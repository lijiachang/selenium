# -*- coding:utf-8 -*-
import os
import random
import requests
import re
from logger import logger
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from collections import namedtuple
from pip._vendor.retrying import retry

################# 配置区 ##############################################################################################
domain = 'www.chuangjiawang.com'  # 网站地址 www.xxx.com
domain_index = 'http://www.chuangjiawang.com/admin/?index.html'  # 管理后台的页面URL
username = 'admin'  # 后台管理用户名
password = 'zgMPGiiYytigU0b'  # 后台管理密码

images_path = '/root/tu01'  # 图片库路径目录
db_file_name = 'inventory_sku_20211106.txt'  # 读取的数据库文件的路径
number_of_domain = 1  # 网站的序号，比如有10个网站，需要挂10个脚本，分别改为1、2、3...10

# 配置定时任务
daily_task = 10  # 每天发布的文章数量
job_time = '02:30'  # 每天的什么时候发布
######################################################################################################################

common_headers = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Connection: keep-alive
Cookie: KT-GUID=KT-69F23C0DF1D726B30D8AB94F81633E2A; KT-ADMIN=admin; security_session_verify=c01aefbdeed31a21ec9bd6f056dcb66e; srcurl=687474703a2f2f7777772e636875616e676a696177616e672e636f6d2f61646d696e2f3f696e6465782d6c6f67696e; security_session_mid_verify=70d96eeba917702efcd3a0a9fb8b404c; KT-ATOKEN={token}
Host: {domain}
Origin: http://{domain}
Referer: http://{domain}/admin/?article/article-create.html
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4621.0 Safari/537.36"""

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


class SingletonATOKEN:
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
            self.token = self.login()
            self.__init_flag = True
        else:
            pass

    def login(self):
        """登录成功后 获取到 KT-GUID=KT-6969005D94A0D1451DC6CCC9AEB768A4  KT-ATOKEN=1-KT187E19B8C8329363D31F06B00CC8434F"""
        headers = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Content-Type: application/x-www-form-urlencoded
Cookie: KT-GUID=KT-69F23C0DF1D726B30D8AB94F81633E2A; KT-ADMIN=admin; security_session_verify=c01aefbdeed31a21ec9bd6f056dcb66e; srcurl=687474703a2f2f7777772e636875616e676a696177616e672e636f6d2f61646d696e2f3f696e6465782d6c6f67696e; security_session_mid_verify=70d96eeba917702efcd3a0a9fb8b404c
Host: {0}
Origin: http://{0}
Proxy-Connection: keep-alive
Referer: http://{0}/admin/?index-login
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4621.0 Safari/537.36"""

        form = {'admin_name': username,
                'admin_pwd': password}

        url = 'http://{}/admin/?index-login'.format(domain)
        rep = requests.post(url, data=form,
                            headers=get_headers(headers.format(domain)), allow_redirects=False)

        re_match = re.match('KT-ATOKEN=(.*?);', rep.headers.get('Set-Cookie'))
        if re_match:
            token = re_match.group(1)
            logger.info('登录成功: KT-ATOKEN=={}'.format(token))
            return token
        else:
            logger.info('登录失败:')
            logger.info(rep.text)
            return False


class ArticleForm:

    def __init__(self, headers_raw, line: LINE):
        self.token = SingletonATOKEN().token
        self.headers = get_headers(headers_raw.format(domain=domain, token=self.token))
        self.city_id_map = self.init_city_id_map()
        self.line = line

    def publish(self):

        # 上传略缩图
        # 随机一个略缩图

        random_image_file_path = random.choice(self.get_raw_file_list(images_path))  # 在目录下随机找一张图片

        # 发布文章
        self.post_article(random_image_file_path)

    """获取文件列表"""

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

    def init_city_id_map(self):
        """获取发布页的 城市和id 映射关系
        http://www.chuangjiawang.com/admin/?block/item-push-article-151.html&MINI=load

        """
        url = 'http://{}/admin/?block/item-push-article-151.html&MINI=load'.format(domain)
        rep = requests.get(url, headers=self.headers)
        # 从推送文章窗口的源码中，解析出id和城市的对应关系。 {'邢台': '1', '天津': '2', '石家庄': '3', '唐山': '4'
        ret = re.findall(
            r'<li style="width:80px;"><label><input type="checkbox" name="data\[city_ids\]\[\d*\]"  value="(\d*)" CK=".*?"/>(.*?)</label></li>',
            rep.text)

        if ret:
            city_id_map = dict((y, x) for x, y in ret)
            # logger.info('get city_id_map :{}'.format(city_id_map))
        else:
            logger.info('get city_id_map err rep.text:{}'.format(rep.text))
            city_id_map = {}

        return city_id_map  # e.g.  {'邢台': '1', '天津': '2', '石家庄': '3', '唐山': '4', '秦皇岛': '5',

    def match_city_id(self, text):
        """从一个文本中，匹配城市ID"""
        for city_name, city_id in self.city_id_map.items():
            if city_name in text:
                return city_id
        else:
            return 0

    def post_article(self, image_file_path):
        """发布文章内容
        请求URL: http://www.chuangjiawang.com/admin/?article/article-create.html

        请求标头
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,zh;q=0.9
        Cache-Control: max-age=0
        Connection: keep-alive
        Content-Length: 2069
        Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryFfVmLB0zKlB89nB1
        Cookie: KT-GUID=KT-69F23C0DF1D726B30D8AB94F81633E2A; KT-ADMIN=admin; PHPSESSID=oaua0npunq1q0nbdtgkahr8e22; KT-ATOKEN=1-KT187E19B8C8329363D31F06B00CC8434F
        Host: www.chuangjiawang.com
        Origin: http://www.chuangjiawang.com
        Referer: http://www.chuangjiawang.com/admin/?article/article-create.html
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4621.0 Safari/537.36

        表单
        MINI: iframe
        data[title]: 标题111
        data[cat_id]: 16
        data[thumb]: （二进制）
        data[desc]: 描述
        data[linkurl]:
        data[content]: 内容
        data[seo_title]: SEO标题
        data[seo_keywords]: SEO关键词
        data[seo_description]: SEO描述：
        data[views]: 1
        data[favorites]: 0
        data[photos]: 0
        data[comments]: 0
        data[ontime]:
        data[orderby]: 50
        data[allow_comment]: 1
        data[hidden]: 0
        data[audit]: 1

        发布成功后，rep.txt 里面有发布成功 提示
        Widget.MsgBox.success("添加文章成功",function(){});

        """
        form = {'MINI': 'iframe',
                'data[title]': self.line.title,
                'data[cat_id]': 16,  # 分类
                # 'data[thumb]': ('001_01.jpg', open('001_01.jpg', 'rb'), 'image/jpeg', {}),  # 二进制的图片
                'data[desc]': self.line.content[:50],
                'data[linkurl]': '',
                'data[content]': self.line.content,
                'data[seo_title]': self.line.title,
                'data[seo_keywords]': self.line.key_words,
                'data[seo_description]': self.line.content[:50],
                'data[views]': 1,
                'data[favorites]': 0,
                'data[photos]': 0,
                'data[comments]': 0,
                'data[ontime]': '',
                'data[orderby]': 50,
                'data[allow_comment]': 1,
                'data[hidden]': 0,
                'data[audit]': 1}
        # 'data[city_ids][97]': 97,  # 推送城市

        # 匹配城市
        city_id = self.match_city_id(self.line.title)
        if city_id:
            form['data[city_ids][{}]'.format(city_id)] = city_id

        url = 'http://{}/admin/?article/article-create.html'.format(domain)
        multipart_form_data = {key: (None, value) for key, value in form.items()}
        multipart_form_data['data[thumb]'] = (image_file_path, open(image_file_path, 'rb'), 'image/jpeg')

        rep = requests.post(url, files=multipart_form_data, headers=self.headers)
        rep_text = rep.text
        if '添加文章成功' in rep_text:
            logger.info('id={} 添加文章成功: {}'.format(self.line.id, self.line.title))
        else:
            logger.info('！！！id={} 发布失败: {}'.format(self.line.id, self.line.title))

        return rep_text


def analysis_line(line: str):
    """line eg.
    397469	2021-11-05 16:43:42	台州装修首付一般付多少	台州装修	台州,装修,首付,一般,付,多少	关键还是看怎么谈，3-6成都有，按进度逐步付款。
    """
    line = line.split()
    id_ = line[0]
    if not id_.isdigit():
        raise Exception('id need be digit')
    create_time = line[1] + '' + line[2]
    title = line[3]
    key_words = line[4]
    tag = line[5]
    content = ' '.join(line[6:])
    if not content:
        raise Exception('cant found content')
    return LINE(id_, create_time, title, key_words, tag, content)


published_titles = {}  # 统计读取到的title和出现的次数


def gen_read_inventory(file_name):
    with open(file_name, 'r', encoding='utf-8') as file_handler:
        while True:
            line = file_handler.readline()
            if line:
                try:
                    line_ = analysis_line(line)  # 提取正确的一行

                    published_titles.setdefault(line_.title, 0)  # 字典key不存在：这时增加key 值为1
                    published_titles[line_.title] += 1

                    if published_titles[line_.title] != number_of_domain:  # 未到自己的编号，跳过
                        continue
                except Exception as e:
                    logger.error('read line err:{}'.format(e))
                    continue
                else:
                    yield line_
            else:
                break


gen_tasks = gen_read_inventory(db_file_name)


# 最开始初始化一次空间略缩图
# ArticleForm(common_headers, '').save_all_remote_images()


# 若出现错误，重试3次，每次间隔1小时
def job():
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
            logger.info('{} 内的文章已经全部发布完成，请更新'.format(db_file_name))
    # 确保下次任务需要先登录
    SingletonATOKEN.__init_flag = False


job()  # 第一次运行的时候，先发布一次

scheduler = BlockingScheduler()
# 在每天2点的25分，运行一次 job 方法
hour = job_time.split(':')[0]
minute = job_time.split(':')[1]
scheduler.add_job(job, 'cron', max_instances=10, hour=hour, minute=minute, misfire_grace_time=3600)
scheduler.start()
