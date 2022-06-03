# -*- coding:utf-8 -*-
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
domain = 'www.taizhou66.com'  # 网站地址 www.xxx.com
domain_index = 'http://www.taizhou66.com/admin974.php'  # 管理后台的页面URL
username = 'admin846pjw'  # 后台管理用户名
password = '1Ny0Io7WdLR1mUow'  # 后台管理密码

# Excel配置
excel_name = 'lawcdyc2.xlsm'
sheet_name = 'Sheet1'
# 替换的关键字
replace_string = {'需要替换的文字': '替换后的文字', '_x000D_': '', }


# 配置定时任务
daily_task = 50  # 每天发布的文章数量
job_time = '03:30'  # 每天的什么时候发布
delay = 5  # 发布时间间隔的，比如间隔5秒发布一篇, 单位是秒
######################################################################################################################

common_headers = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: max-age=0
Content-Type: application/x-www-form-urlencoded
Cookie: security_session_verify={security_session_verify}; security_session_mid_verify={security_session_mid_verify}; PHPSESSID={php_session_id}
Host: {domain}
Origin: http://{domain}
Proxy-Connection: keep-alive
Referer: http://{domain}/index.php?m=site&c=content&a=article_form
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"""

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
        headers = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Cookie: security_session_verify={security_session_verify}; security_session_mid_verify={security_session_mid_verify}; PHPSESSID={session_id}
Host: {domain}
Origin: http://{domain}
Referer: http://{domain}/index.php?m=site&c=index&a=login
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"""
        form = {'username': username,
                'password': password}
        url = 'http://www.taizhou66.com/index.php?m=site&c=index&a=login'
        _session_id, security_session_verify, security_session_mid_verify = self.get_session_id()
        rep = requests.post(url, data=form,
                            headers=get_headers(headers.format(domain=domain, session_id=_session_id,
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
        headers = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Connection: keep-alive
Host: {domain}
Cookie: security_session_verify={security_session_verify}; security_session_mid_verify={security_session_mid_verify}
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"""

        url = domain_index
        security_session_verify, security_session_mid_verify = self.get_cookies(url)
        logger.info(f'security_session_verify:{security_session_verify}, security_session_mid_verify:{security_session_mid_verify}')
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
        self.headers = get_headers(headers_raw.format(domain=domain, php_session_id=self.php_session_id,
                                                      security_session_verify=self.security_session_verify,
                                                      security_session_mid_verify=self.security_session_mid_verify))
        self.access_key, self.cat_id_map = self.init_publish_page()
        self.line = line

    def publish(self):
        # 上传tag
        tag_ids = self.post_tag(self.line.tag.strip())
        tag_content = ',' + ','.join(str(tag_in) for tag_in in tag_ids)

        # 上传略缩图
        # 随机一个网络略缩图
        random_image = random.choice(self.remote_images)
        # {'id': 1869, 'cat_id': 20, 'filename': '/storage/8603/imagesclass/20190302/005_271.jpg', 'filesize': 40775, 'status': 1, 'status_use': 0, 'addtime': 1551527430}
        image_path = random_image['filename']
        self.post_remote_image(image_path)

        # 发布文章
        publish_result = self.post_article(tag_content)

    def init_publish_page(self):
        """1.获取发布页面的access_key值，虽然自己随机一个也能用，但是防止撞库，还是从页面获取值比较好
           2.获取发布页的 城市和id 映射关系"""
        url = 'http://www.taizhou66.com/index.php?m=site&c=content&a=article_form'
        rep = requests.get(url, headers=self.headers)
        ret = re.search('<input type="hidden" name="access_key" value="(.*?)">', rep.text)
        access_key = None
        if ret:
            access_key = ret.group(1)
            logger.info('get access_key:{}'.format(access_key))
        else:
            logger.info('get access_key err rep.text:{}'.format(rep.text))
        cat_ids = self.get_cat_ids_by_text(rep.text)
        return access_key, cat_ids

    @staticmethod
    def get_cat_ids_by_text(text):
        """从发布页的源码中，解析出id和城市的对应关系"""
        p = '<input id="cat_id" lay-skin="primary" type="checkbox"  name="cat_id\[\]" value="(\d+)"  title="(.*?)">'
        ret = re.findall(p, text)
        return dict(r for r in ret)  # e.g. {'119': '抚顺', '120': '阜新', '121': '阜阳', '122': '广安'}

    def post_tag(self, tag_str):
        """
        发布标签关键词，返回每个关键词的数据标签
        请求 URL: http://www.taizhou66.com/index.php?m=mod&c=tag_article&a=ajax_form&tag_str=n%E9%B9%A4%E5%B2%97,50,%E5%AD%90,%E6%80%8E%E4%B9%88%E8%A3%85%E4%BF%AE,%E8%AE%BE%E8%AE%A1%E5%9B%BE
        表单：
        m: mod
        c: tag_article
        a: ajax_form
        tag_str: n鹤岗,50,子,怎么装修,设计图

        {"status":0,"names":["n\u9e64\u5c97","50","\u5b50","\u600e\u4e48\u88c5\u4fee","\u8bbe\u8ba1\u56fe"],"ids":["3376",233,194,116,265]}

        :param tag_str: 多个标签请用英文逗号（,）分开 eg.鹤岗,50,子,怎么装修,设计图
        :return:
        """

        form = {'m': 'mod',
                'c': 'tag_article',
                'a': 'ajax_form',
                'tag_str': tag_str}
        url = 'http://www.taizhou66.com/index.php'
        rep = requests.post(url, data=form, headers=self.headers)
        ids = rep.json().get('ids')
        return ids

    def post_image(self):
        """上传略缩图 
        请求 URL: http://www.taizhou66.com/index.php?m=mod&c=thumb&a=thumb_upload
        表单：
        logo: (二进制)
        typename: article
        item_id: 20203
        access_key: 6173e1d669410
        响应：
        上传第一个图 {"status":1,"msg":"\u5df2\u4e0a\u4f20\u6210\u529f","logo":"\/storage\/article\/20211023\/20211023182059_77963.jpg","id":"1122"}
        上传第二个图 {"status":1,"msg":"\u5df2\u4e0a\u4f20\u6210\u529f","logo":"\/storage\/article\/20211023\/20211023183010_42588.jpg","id":"1123"}
        """

    def list_remote_images(self, cat_id, page):
        """查询空间中的略缩图
        请求 URL: http://www.taizhou66.com/index.php?m=mod&c=thumb&a=picture_list

        page: 2     #该分类下的页码
        cat_id: 2   #分类

        返回图片的ID，文件路径
        {"data":[{"id":2000,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195036_50079.jpg","filesize":120272,"status":1,"status_use":0,"addtime":1551527436},{"id":1999,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195036_89379.jpg","filesize":150505,"status":1,"status_use":0,"addtime":1551527435},{"id":1998,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195036_44823.jpg","filesize":97095,"status":1,"status_use":0,"addtime":1551527436},{"id":1997,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195036_85689.jpg","filesize":86456,"status":1,"status_use":0,"addtime":1551527435},{"id":1996,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195036_26718.jpg","filesize":100938,"status":1,"status_use":1,"addtime":1551527435},{"id":1995,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195035_98170.jpg","filesize":74665,"status":1,"status_use":0,"addtime":1551527435},{"id":1994,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195035_90379.jpg","filesize":85512,"status":1,"status_use":0,"addtime":1551527435},{"id":1993,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195035_58549.jpg","filesize":135324,"status":1,"status_use":0,"addtime":1551527435},{"id":1992,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195035_83925.jpg","filesize":132173,"status":1,"status_use":0,"addtime":1551527435}]}

        """
        url = "http://www.taizhou66.com/index.php?m=mod&c=thumb&a=picture_list"

        form = {'page': page,
                'cat_id': cat_id}
        rep = requests.post(url, data=form, headers=self.headers)
        logger.info(rep.json()['data'])
        return rep.json()['data']

    def save_all_remote_images(self):
        """爬取所有的网络略缩图, 大约有2000多个"""
        logger.info('开始采集网络略缩图：')
        remote_images = []
        for cat_id in range(21):  # 21 分类：无分组、微信采集、001、002、003......
            for page in range(100):  # 页码：
                res = self.list_remote_images(cat_id, page)
                if res:
                    remote_images += res
                else:
                    break
        logger.info('共采集网络略缩图：{}'.format(len(remote_images)))
        # {'id': 1869, 'cat_id': 20, 'filename': '/storage/8603/imagesclass/20190302/005_271.jpg', 'filesize': 40775, 'status': 1, 'status_use': 0, 'addtime': 1551527430}
        remote_images = [image for image in remote_images if image.get('filename').endswith('jpg')]
        logger.info('收集到jpg略缩图：{}'.format(len(remote_images)))
        ArticleForm.remote_images = remote_images

    def post_remote_image(self, file_path):
        """上传空间中的略缩图
        请求 URL: http://www.taizhou66.com/index.php?m=mod&c=thumb&a=picture_2_thumb

        data[]: /storage/8603/imagesclass/20190410/8e1c618b31d3a5e1c631392a6c4a1415.gif     上传的是文件路径
        typename: article
        item_id: 0
        access_key: 6173e78beea23

        {"status":1,"msg":"\u5df2\u4e0a\u4f20\u6210\u529f","logo":"\/storage\/article\/20211023\/2021102302912_69427.gif"}

        """
        logger.info('使用空间略缩图: {}'.format(file_path))
        form = {'data[]': file_path,
                'typename': 'article',
                'item_id': 0,
                'access_key': self.access_key}
        url = 'http://www.taizhou66.com/index.php?m=mod&c=thumb&a=picture_2_thumb'
        rep = requests.post(url, data=form, headers=self.headers)
        return rep.text

    def check_image(self):
        """查询略缩图
        请求 URL: http://www.taizhou66.com/index.php?m=mod&c=thumb&a=thumb_list

        item_type: 2
        item_id: 20203

        展示两个图 {"data":[{"id":1122,"uid":1,"item_type":2,"item_id":20203,"file_name":"001_51.jpg","file_location":"\/storage\/article\/20211023\/20211023182059_77963.jpg","add_time":1634984459,"access_key":"6173e1d669410","thumb":"\/storage\/article\/20211023\/thumb_pc_20211023182059_77963.jpg","status":1,"listorder":0},{"id":1123,"uid":1,"item_type":2,"item_id":20203,"file_name":"1 (9).jpg","file_location":"\/storage\/article\/20211023\/20211023183010_42588.jpg","add_time":1634985010,"access_key":"6173e1d669410","thumb":"\/storage\/article\/20211023\/thumb_pc_20211023183010_42588.jpg","status":1,"listorder":0}]}
        """

    def post_article(self, tag_content):
        """发布文章内容
        请求URL: http://www.taizhou66.com/index.php?m=site&c=content&a=article_form

        表单
        timesend: 2021-10-23 18:20:06
        access_key: 6173e1d669410
        info[title]: 中国鹤岗50子怎么装修设计图
        info[seo_title]: n鹤岗50子怎么装修设计图
        info[keywords]: n鹤岗,50,子,怎么装修,设计图
        info[description]: 欧式简约风格一般就是把设计的元素，色彩，原材料以及照明做到简单化
        submit1: ok
        info[id]: 20203  # 这个id是上传略缩图后的关联作用
        is_auto_save: 1
        info[status]: 1
        status: 1
        http_referer: http://www.taizhou66.com/index.php?m=site&c=content&a=article_index
        cat_id[]: 35  # 发布勾选的分类，每个数字对应一个城市，可以在发布页面源码中找到
        cat_id[]: 131 # 发布勾选的分类，每个数字对应一个城市，可以在发布页面源码中找到
        cat_id[]: 319
        copy_id:
        tag_content: ,3376,233,194,116,265
        info[filename]: 3nhg50zzmzxsjt20203
        info[listorder]: 0
        info[addtimeb]: 2021-10-23 18:09:46
        iscopy: 0
        content: <p>欧式简约风格<a data-mid="5586" href="/a/13987.html">一般</a>就是把<a data-mid="5742" href="/a/14115.html">设计</a>的元素，色彩，原材料以及照明做到<a data-mid="5516" href="/a/14009.html">简单</a>化，但是对于色彩以及材料的质感要求会比较高。如果说欧式简约风格有<a data-mid="5563" href="/a/13995.html">什么</a>共同点的话那一定是简洁、直接、功能化且贴近自然，一份宁静的欧洲风情，绝非是蛊惑人心的虚华设计影响。<a data-mid="5555" href="/a/13997.html">客厅</a>不大，但是收纳功能超级强大，整面的原木书柜，把爱书的<a data-mid="5574" href="/a/13991.html">家庭</a>收拾地干干净净。清新自然的北欧简约风格，干净的白，素雅的木色，还有强大的墙面收纳，自然而实用。狭小的厨房有着很多零碎的物品，但是北欧人家的厨房看上去总是那么整洁而有序。精心设计的角落让他们的厨房充满温馨的感觉。没有欧洲繁复的床品设计，没有中国传统床品中太多的遮拦，就是简简单单的床和床头柜搭配，北欧经典的简约风就此打造而成，但是细心的你会发现，他们在卧室背景墙上花得功夫可不少哦。</p><p><br/></p>

        发布成功后，rep.txt 里面有发布成功 提示
        """
        form = {'timesend': time.strftime("%Y-%m-%d %H:%M:%S"),
                'access_key': self.access_key,
                'info[title]': self.line.title,
                'info[seo_title]': self.line.title,
                'info[keywords]': self.line.key_words,
                'info[description]': self.line.content[:50],
                'submit1': 'ok',
                # 'info[id]': '20203', # 这个id是手动上传略缩图后的关联作用
                'is_auto_save': '1',
                'info[status]:': '',
                'http_referer': 'http://{}/index.php?m=site&c=content&a=article_index'.format(domain),
                'status': '1',
                'cat_id[]': ['35'],  # 装修问答 是必选的分类 todo 如果没有其他分类，这样列表是否能正常识别
                'copy_id:': '',
                'tag_content': tag_content,
                'info[filename]:': '',
                'info[listorder]:': '',
                'iscopy': '0',
                'content': '<p>{}</p>'.format(self.line.content)}
        # 增加cat_id 关联城市
        for cat_id, city_name in self.cat_id_map.items():
            if city_name in self.line.title:
                form['cat_id[]'].append(cat_id)  # 在一个post中提交含有多个相同名称的数据

        url = 'http://www.taizhou66.com/index.php?m=site&c=content&a=article_form'
        rep = requests.post(url, data=form, headers=self.headers)
        rep_text = rep.text
        if '发布成功' in rep_text:
            logger.info('id={} 发布成功: {}'.format(self.line.id, self.line.title))
        else:
            logger.info('！！！id={} 发布失败: {}'.format(self.line.id, self.line.title))

        return rep_text

    def get_cat_ids(self):
        """根据title 返回符合的cat_id列表"""
        # return [cat_id for cat_id in cat_id_maps if cat_id in self.line.title]

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
ArticleForm(common_headers, '').save_all_remote_images()


# 若出现错误，重试3次，每次间隔1小时
#@retry(stop_max_attempt_number=3, wait_fixed=1000 * 60 * 60)
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
            logger.info('{} 内的文章已经全部发布完成，请更新'.format(excel_name))
    # 确保下次任务需要先登录
    SingletonPHPSESSID.__init_flag = False


job()  # 第一次运行的时候，先发布一次

scheduler = BlockingScheduler()
# 在每天2点的25分，运行一次 job 方法
hour = job_time.split(':')[0]
minute = job_time.split(':')[1]
scheduler.add_job(job, 'cron', max_instances=10, hour=hour, minute=minute, misfire_grace_time=3600)
scheduler.start()

