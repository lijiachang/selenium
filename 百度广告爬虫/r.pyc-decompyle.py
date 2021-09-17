import sys

import parsel
import random
import re

import pyautogui
import requests
import sqlite3
import time
from hashlib import md5
from itertools import cycle

import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# from fake_useragent import UserAgent

urllib3.disable_warnings()


def get_random_ua():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
    ]
    UserAgent = random.choice(user_agent_list)
    return UserAgent


class Spider:

    def __init__(self):
        with open(u'\u914d\u7f6e\u6587\u4ef6.ini', 'r', encoding='utf-8') as (f):
            readers = f.readlines()
            path = readers[0].split('=')[-1].split('#')[0].strip()
            self.t_min = int(readers[1].split('=')[-1].split('#')[0].strip())
            self.t_max = int(readers[2].split('=')[-1].split('#')[0].strip())
            self.keyword = readers[3].split('=')[-1].split('#')[0].strip()
            self.keywords = re.split(r'[,，]', self.keyword)

            self.n = int(readers[4].split('=')[-1].split('#')[0].strip())
            self.db = readers[5].split('=')[-1].split('#')[0].strip()
            self.table = readers[6].split('=')[-1].split('#')[0].strip()
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        # 随机ua对象
        # self.ua = UserAgent()

        try:
            self.cursor.execute(
                u'create table {}(id varchar(20) primary key,\u6807\u9898 varchar(20),\u7f51\u5740 varchar(100))'.format(
                    self.table))
        except:
            pass

        self.s = set()
        self.num = 1

        self.init_browser()

        start_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.f = open('{}.txt'.format(start_time), 'a+', buffering=1, encoding='utf-8-sig', newline='')

    def init_browser(self, proxy=None):
        """

        :param proxy: 202.20.16.82:10152
        """
        options = webdriver.ChromeOptions()
        options.add_argument('-ignore-certificate-errors')
        options.add_argument('-ignore -ssl-errors')
        options.add_argument('--disable-software-rasterizer')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        # 设置代理
        if proxy:
            options.add_argument("--proxy-server={}".format(proxy))
            # 一定要注意，=两边不能有空格

        # 设置随机User-Agent
        # user_agent = self.ua.random
        user_agent = get_random_ua()
        print(f'random user_agent=={user_agent}')
        options.add_argument('user-agent={}'.format(user_agent))

        self.browser = webdriver.Chrome(options=options)
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': "\n                    Object.defineProperty(navigator, 'webdriver', {\n                      get: () => undefined\n                    })\n                  "})
        # self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 10)
        url = 'https://www.baidu.com/'
        self.browser.get(url)

    def parse(self):
        html = self.browser.page_source
        response = parsel.Selector(text=html)
        lis = response.xpath('.//div[@id="content_left"]/div')
        i = 1
        for li in lis:
            if li.xpath('.//div[contains(@class,"c-span12")]/div'):
                divs = li.xpath('.//div[contains(@class,"c-span12")]/div')
                for div in divs:
                    name = ''
                    if div.xpath('string(.//h3/div/a)'):
                        name = div.xpath('string(.//h3/div/a)').extract_first()
                    else:
                        if div.xpath('string(.//h3/a)'):
                            name = div.xpath('string(.//h3/a)').extract_first()
                    if name:
                        href = div.xpath('.//h3//a/@data-landurl').extract_first()
                        id = md5(href.encode('utf-8')).hexdigest()
                        dic = {'id': id,
                               u'\u6807\u9898': name,
                               u'\u7f51\u5740': href}
                        print(i, dic)
                        i += 1
                        keys = ','.join(dic.keys())
                        values = ','.join(['?'] * len(dic))
                        sql = ('REPLACE INTO {table} ({keys}) VALUES ({values})').format(table=self.table, keys=keys,
                                                                                         values=values)
                        d = tuple(dic.values())
                        try:
                            if self.cursor.execute(sql, d):
                                print(u'\u63d2\u5165\u6210\u529f')
                                self.conn.commit()
                        except:
                            print(u'\u63d2\u5165\u5931\u8d25')
                            self.conn.rollback()

            else:
                name = ''
                if li.xpath('string(.//h3/a)'):
                    name = li.xpath('string(.//h3/a)').extract_first().strip()
                if name:
                    href = li.xpath('.//h3/a/@href').extract_first()
                    if 'http:' not in href:
                        href = ' https://www.baidu.com' + href
                    href = self.get_real(href)
                    id = md5(href.encode('utf-8')).hexdigest()
                    dic = {'id': id,
                           u'\u6807\u9898': name,
                           u'\u7f51\u5740': href}
                    print(i, dic)
                    i += 1
                    keys = ','.join(dic.keys())
                    values = ','.join(['?'] * len(dic))
                    sql = ('REPLACE INTO {table} ({keys}) VALUES ({values})').format(table=self.table, keys=keys,
                                                                                     values=values)
                    d = tuple(dic.values())
                    try:
                        if self.cursor.execute(sql, d):
                            print(u'\u63d2\u5165\u6210\u529f')
                            self.conn.commit()
                    except:
                        print(u'\u63d2\u5165\u5931\u8d25')
                        self.conn.rollback()

    def get_real(self, o_url):
        """
        获取重定向url指向的网址
        """
        print(o_url)
        try:
            r = requests.get(o_url, allow_redirects=False)
            o_url = r.headers['Location']
            return o_url
        except:
            pass

        return o_url

    def get_page(self):
        i = 1
        while i < 4:
            self.parse()
            try:
                self.browser.execute_script('window.scrollTo(0,10000)')
                self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'n'))).click()
                time.sleep(random.uniform(self.t_min, self.t_max))
                i += 1
            except:
                print(u'\u6ca1\u6709\u4e0b\u4e00\u9875\u4e86')
                return

    def r(self, keyword):
        """输入关键词搜索"""
        input = self.wait.until(EC.presence_of_element_located((By.ID, 'kw')))
        input.click()
        input.clear()
        input.send_keys(keyword)
        self.wait.until(EC.presence_of_element_located((By.ID, 'su'))).click()
        time.sleep(self.t_min)
        self.get_page()

    @staticmethod
    def get_proxies():
        with open('proxy10.txt', 'r') as f:
            proxys = f.readlines()

        return [':'.join(re.split(r'[: ]', proxy)) for proxy in proxys]

    def run(self):
        print(u'\u5f00\u59cb\u81ea\u52a8\u5904\u7406')

        # 获取本地存储的代理
        # proxies_cycle = cycle(self.get_proxies())

        j = 1
        while j < self.n:
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(u'\u5f00\u59cb\u91c7\u96c6\u7b2c{}\u6b21'.format(j))
            self.conn = sqlite3.connect(self.db)
            self.cursor = self.conn.cursor()
            try:
                self.cursor.execute(
                    u'create table {}(id varchar(20) primary key,\u6807\u9898 varchar(50),\u7f51\u5740 varchar(200))'.format(
                        self.table))
            except:
                pass

            # 支持多个关键词搜索
            try:
                for keyword in self.keywords:
                    self.r(keyword)  # 搜索采集
            except Exception as e:
                print('pass for:{}'.format(e))
            else:
                # 清理cookie
                cookies = self.browser.get_cookies()
                print(f'''清理前cookies = {cookies}''')
                print(u'\u5220\u9664\u5f53\u524dcookies')
                self.browser.delete_all_cookies()
                cookies = self.browser.get_cookies()
                print(f'''清理后cookies = {cookies}''')

            # 退出浏览器
            self.browser.quit()

            # 配置代理
            # 更换user-agent
            # ，打开新的浏览器
            while True:
                # proxy = next(proxies_cycle)
                proxy = ProxyPool.get_proxy()  # 从代理池获取一个代理IP，如114.96.167.66:4280
                print(f'''更换proxy = {proxy}''')
                try:

                    # AutoSwitchDynProxy().re_connect_proxy()  # 更换全局代理,使用【百万动态客户端】

                    self.init_browser(proxy=proxy)
                    break
                except Exception as e:
                    # 退出浏览器
                    self.browser.quit()
                    print(e)
                    if 'This version of' in e.__repr__():  # 浏览器和chromeDriver不匹配，退出！
                        sys.exit(0)
                    print(f'''当前proxy = {proxy} 可能失效，跳过！''')

            self.cursor.close()
            self.conn.close()
            j += 1


class AutoSwitchDynProxy:
    """点击动态客户端工具，注意要用管理员方式运行Python，才有点击的权限"""

    @staticmethod
    def click_connect_button():
        pyautogui.moveTo(x=1703, y=952)  # 【连接】按钮

        # 鼠标当前位置0.5s间隔双击
        # pyautogui.doubleClick()
        pyautogui.doubleClick(x=None, y=None, interval=0.5, button='left', duration=0.0, tween=pyautogui.linear)
        print('click [connect] button')

    @staticmethod
    def click_close_button():
        pyautogui.moveTo(x=1852, y=958)  # 【断开】按钮

        # 鼠标当前位置0.5s间隔双击
        # pyautogui.doubleClick()
        pyautogui.doubleClick(x=None, y=None, interval=0.5, button='left', duration=0.0, tween=pyautogui.linear)
        print('click [close] button')

    def re_connect_proxy(self):
        self.click_close_button()
        time.sleep(1.5)
        self.click_connect_button()
        time.sleep(4)


class ProxyPool:
    """网络代理池https://zhimahttp.com/getapi/#obtain_ip"""

    @staticmethod
    def get_proxy():
        """num	int	是	提取IP数量
            pro	int	否	省份，默认全国
            city	int	否	城市，默认全国
            regions	int	否	全国混拨地区
            yys	int	是	0:不限 100026:联通 100017:电信
            port	int	是	IP协议 1:HTTP 2:SOCK5 11:HTTPS
            time	int	按次提取必填	稳定时长 1:5-25min 2:25min-3h 3:3-6h 4:6-12h
            type	int	否	数据格式：1:TXT 2:JSON 3:html
            pack	int	否	用户套餐ID
            ts	int	否	是否显示IP过期时间: 1显示 2不显示
            ys	int	否	是否显示IP运营商: 1显示
            cs	int	否	否显示位置: 1显示
            lb	int	否	分隔符(1:\r\n 2:/br 3:\r 4:\n 5:\t 6 :自定义)
            sb	string	否	自定义分隔符
            mr	int	否	去重选择（1:360天去重 2:单日去重 3:不去重）
            pb	int	否	端口位数（4:4位端口 5:5位端口）"""

        url = 'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
        rep = requests.get(url)
        return rep.text


if __name__ == '__main__':
    start = time.time()
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))
    print(u'\u811a\u672c\u542f\u52a8\u5f00\u59cb\u65f6\u95f4: {}'.format(start_time))
    s = Spider()
    s.run()
    finish = time.time()
    finish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(finish))
    Total_time = finish - start
    m, s = divmod(Total_time, 60)
    h, m = divmod(m, 60)
    print(u'\u5f00\u59cb\u65f6\u95f4:', start_time)
    print(u'\u7ed3\u675f\u65f6\u95f4:', finish_time)
    print('Total_time', u'\u5171\u8017\u65f6===>%d\u65f6:%02d\u5206:%02d\u79d2' % (h, m, s))
