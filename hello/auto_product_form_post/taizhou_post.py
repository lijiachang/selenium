# -*- coding:utf-8 -*-
import time
import requests
import re

domain = 'www.taizhou66.com'

common_headers = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: max-age=0
Content-Type: application/x-www-form-urlencoded
Cookie: PHPSESSID=fmjvsmqkeo98g9e405j7l8spmd
Host: {domain}
Origin: http://{domain}
Proxy-Connection: keep-alive
Referer: http://{domain}/index.php?m=site&c=content&a=article_form
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"""

common_form = """timesend: 2021-10-23 17:58:28
access_key: 6173d364eb599
info[title]: 3n鹤岗50子怎么装修设计图
info[seo_title]: n鹤岗50子怎么装修设计图
info[keywords]: n鹤岗,50,子,怎么装修,设计图
info[description]: 欧式简约风格一般就是把设计的元素，色彩，原材料以及照明做到简单化
submit1: ok
info[id]:
is_auto_save: 1
info[status]: 
status: 1
http_referer: http://{}/index.php?m=site&c=content&a=article_index
cat_id[]: 35
cat_id[]: 131
cat_id[]: 245
cat_id[]: 319
copy_id: 
tag_content: ,690,233,194,116,265
info[filename]: 
info[listorder]: 
info[addtimeb]: 
iscopy: 0
content: <p>欧式简约风格一般就是把设计的元素，色彩，原材料以及照明做到简单化，但是对于色彩以及材料的质感要求会比较高。如果说欧式简约风格有什么共同点的话那一定是简洁、直接、功能化且贴近自然，一份宁静的欧洲风情，绝非是蛊惑人心的虚华设计影响。客厅不大，但是收纳功能超级强大，整面的原木书柜，把爱书的家庭收拾地干干净净。清新自然的北欧简约风格，干净的白，素雅的木色，还有强大的墙面收纳，自然而实用。狭小的厨房有着很多零碎的物品，但是北欧人家的厨房看上去总是那么整洁而有序。精心设计的角落让他们的厨房充满温馨的感觉。没有欧洲繁复的床品设计，没有中国传统床品中太多的遮拦，就是简简单单的床和床头柜搭配，北欧经典的简约风就此打造而成，但是细心的你会发现，他们在卧室背景墙上花得功夫可不少哦。</p><p><br/></p>"""


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


# post_url = 'http://{}/index.php?m=site&c=content&a=article_form'.format(domain)
# rep = requests.post(post_url,
#                     headers=get_headers(common_headers.format(domain=domain)),
#                     data=get_form_data(common_form.format(domain)))
# print(rep.text)


class ArticleForm:
    def __init__(self, headers_raw):
        self.headers = get_headers(headers_raw.format(domain=domain))
        self.access_key = self.get_page_access_key()

    def get_page_access_key(self):
        """获取发布页面的access_key值，虽然自己随机一个也能用，但是防止撞库，还是从页面获取值比较好"""
        url = 'http://www.taizhou66.com/index.php?m=site&c=content&a=article_form'
        rep = requests.get(url, headers=self.headers)
        ret = re.search('<input type="hidden" name="access_key" value="(.*?)">', rep.text)
        if ret:
            access_key = ret.group(1)

            return access_key
        return None

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

    def list_remote_images(self):
        """查询空间中的略缩图
        请求 URL: http://www.taizhou66.com/index.php?m=mod&c=thumb&a=picture_list

        page: 2     #该分类下的页码
        cat_id: 2   #分类

        返回图片的ID，文件路径
        {"data":[{"id":2000,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195036_50079.jpg","filesize":120272,"status":1,"status_use":0,"addtime":1551527436},{"id":1999,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195036_89379.jpg","filesize":150505,"status":1,"status_use":0,"addtime":1551527435},{"id":1998,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195036_44823.jpg","filesize":97095,"status":1,"status_use":0,"addtime":1551527436},{"id":1997,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195036_85689.jpg","filesize":86456,"status":1,"status_use":0,"addtime":1551527435},{"id":1996,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195036_26718.jpg","filesize":100938,"status":1,"status_use":1,"addtime":1551527435},{"id":1995,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195035_98170.jpg","filesize":74665,"status":1,"status_use":0,"addtime":1551527435},{"id":1994,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195035_90379.jpg","filesize":85512,"status":1,"status_use":0,"addtime":1551527435},{"id":1993,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195035_58549.jpg","filesize":135324,"status":1,"status_use":0,"addtime":1551527435},{"id":1992,"cat_id":2,"filename":"\/storage\/8603\/imagesclass\/20190302\/20190302195035_83925.jpg","filesize":132173,"status":1,"status_use":0,"addtime":1551527435}]}

        """

    def post_remote_image(self, file_path):
        """上传空间中的略缩图
        请求 URL: http://www.taizhou66.com/index.php?m=mod&c=thumb&a=picture_2_thumb

        data[]: /storage/8603/imagesclass/20190410/8e1c618b31d3a5e1c631392a6c4a1415.gif     上传的是文件路径
        typename: article
        item_id: 0
        access_key: 6173e78beea23

        {"status":1,"msg":"\u5df2\u4e0a\u4f20\u6210\u529f","logo":"\/storage\/article\/20211023\/2021102302912_69427.gif"}

        """
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
                'info[title]': '123利津县115平的房子装修大概多少钱',
                'info[seo_title]': 'new利津县115平的房子装修大概多少钱',
                'info[keywords]': '利津县,115,平,房子,装修,大概,多少钱',
                'info[description]': '前50字符',
                'submit1': 'ok',
                # 'info[id]': '20203',
                'is_auto_save': '1',
                'info[status]:': '',
                'http_referer': 'http://{}/index.php?m=site&c=content&a=article_index'.format(domain),
                'status': '1',
                'cat_id[]': '4',
                'copy_id:': '',
                'tag_content': tag_content,
                'info[filename]:': '',
                'info[listorder]:': '',
                'iscopy': '0',
                'content': '<p>一平方600到1000!也就是7万到12万左右!</p>'}

        url = 'http://www.taizhou66.com/index.php?m=site&c=content&a=article_form'
        rep = requests.post(url, data=form, headers=self.headers)
        return rep.text


article = ArticleForm(common_headers)
ak = article.get_page_access_key()
tag_ids = article.post_tag('设计图,装修')
tag_content = ',' + ','.join(str(tag_in) for tag_in in tag_ids)

print(article.post_article(tag_content))
print()
