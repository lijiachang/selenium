
import time

import urllib3
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


urllib3.disable_warnings()

options = webdriver.ChromeOptions()
options.add_argument('-ignore-certificate-errors')
options.add_argument('-ignore -ssl-errors')
options.add_argument('--disable-software-rasterizer')

# 初始化手机信息
# 指定了宽度、高度、分辨率以及ua标识
options.add_experimental_option('mobileEmulation',
    {'deviceMetrics':{'width': 360,
                      'height': 640,
                      'piexelRatio': 3.0,
                      'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
                      }
    }
    )

browser = webdriver.Chrome(options=options)
browser.set_page_load_timeout(30)  # 设置页面加载超时
wait = WebDriverWait(browser, 10)
browser.get('http://m.baidu.com')

time.sleep(1)
elem = browser.find_element_by_id("index-kw")  # 输入框内的id   index-kw
elem.send_keys("蔬菜")  # 发送到输入框关键词
time.sleep(1)
click = browser.find_element_by_id("index-bn")  # 百度一下的 id  index-bn
click.click()  # 模拟点击
time.sleep(20)
