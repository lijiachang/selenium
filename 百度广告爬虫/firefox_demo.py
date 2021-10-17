import time

import urllib3
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
browser = webdriver.Firefox(firefox_binary=location)

browser.set_page_load_timeout(30)  # 设置页面加载超时
wait = WebDriverWait(browser, 10)
browser.get('http://m.baidu.com')

time.sleep(20)
