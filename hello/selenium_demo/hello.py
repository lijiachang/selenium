
#coding:utf-8
from selenium import webdriver

wd = webdriver.Chrome(r"D:\Chrome\chromedriver.exe")
wd.get("https://www.baidu.com")


print wd.find_elements_by_id("qrcode")[0].text

pass