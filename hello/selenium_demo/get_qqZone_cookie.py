
#coding:utf-8
from selenium import webdriver
import time
import json

driver = webdriver.Firefox()
driver.get(r"https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=手机QQ空间&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=https%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html&pt_no_auth=0")

button = driver.find_element_by_class_name("face")
# print(button)
button.click()

time.sleep(5)
print(driver.current_url)
text = driver.page_source
cookie = driver.get_cookies()
print(cookie)
jsonCookies = json.dumps(cookie)
with open('qqhomepage.json', 'w') as f:
    f.write(jsonCookies)
