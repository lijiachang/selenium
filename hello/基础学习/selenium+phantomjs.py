# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# driver = webdriver.PhantomJS(executable_path=r"C:\Python27\phantomjs.exe")
# driver.get("http://www.qq.com")
# data = driver.title
# driver.save_screenshot('qq.png')  # 网页截图
# print data

firefox = webdriver.Firefox(executable_path=r"C:\Python27\geckodriver.exe")
firefox.get("http://www.baidu.com")
elem = firefox.find_element_by_name("wd")  # 可以通过审查元素查看输入框的name="wd"
elem.send_keys("python")
elem.send_keys(Keys.RETURN)
firefox.save_screenshot("baidu.png")
