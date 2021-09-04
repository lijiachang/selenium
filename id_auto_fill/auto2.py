import time

from docx import Document  # 操作word文件的库
# selenium介绍 https://www.cnblogs.com/thb-blog/p/7609551.html
# IE 浏览器的配置https://blog.csdn.net/weijiechenlun133/article/details/84247159
from selenium import webdriver  # 该步骤是导入selenium的webdriver包，只有导入selenium包，我们才能使用webdriver API进行自动化脚本的开发
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

path = r"id.docx"  # word文件路径
document = Document(path)  # word文档实例


def gen_ids():
    """生成器：读取word每一行"""
    for paragraph in document.paragraphs:
        if paragraph.text:  # 排除空行
            yield paragraph.text.strip()  # 去除前后空格


if __name__ == '__main__':
    driver = webdriver.Ie()  # 这里将控制webdriver的Ie赋值给driver，通过driver获得浏览器操作对象，后就可以启动浏览器、打开网址、操作对应的页面元素了。
    driver.get("https://ntcekw2.neea.edu.cn/teach/login/index")  # 打开登录界面

    _ = input('请登录后确认回车！')
    driver.get("https://ntcekw2.neea.edu.cn/teach/applicant/checkQuery1")  # 打开输入证件号码的页面

    # driver.implicitly_wait(3)

    # print(driver.page_source)
    log_file_name = '已完成审核记录.txt'  # 记录一下已经审核过的身份证，避免中途退出后，忘记审核到哪里了
    file_handler = open(log_file_name, 'a+')  # 文件对象，a+以追加的方式打开文件

    try:

        for id_card in gen_ids():  # 遍历每一行身份证
            time.sleep(0.3)  # 延迟一下，防止浏览器没反应过来
            driver.find_element_by_id("idCard").send_keys(id_card)  # 在浏览器定位身份证的输入框，然后输入身份证信息
            # driver.find_element_by_class_name("btnOrange").click()  # 点击【下一步】按钮
            driver.find_element_by_class_name("btnOrange").send_keys(Keys.ENTER)

            # print(driver.find_element_by_class_name("btnOrange").text)
            # driver.implicitly_wait(3)
            time.sleep(0.3)
            print(driver.page_source)

            if '没有该考生需要审核' in driver.page_source:
                print('{}：无需审核'.format(id_card))
                time_now = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime())  # 记录一个现在的时间，如2021-09-04 16:30:00
                file_handler.write(id_card + '无需审核  time:' + time_now + '\n')
                driver.get("https://ntcekw2.neea.edu.cn/teach/applicant/checkQuery1")  # 再次打开 输入证件号码的页面
                continue

            # 等待，出现【提交审核】按钮，说明到了审核页面
            element = WebDriverWait(driver, 5, 0.5).until(
                EC.visibility_of_element_located((By.ID, "checkBtn"))
            )  # 20秒内，直到元素在页面中可定位
            # text = element.text
            # print(element.text)
            # element.click()  # 点击

            此版本未完成
            此版本未完成
            此版本未完成
            此版本未完成
            此版本未完成
            此版本未完成

            if element:

                # 审核完毕后，帮忙点击 确定按钮
                WebDriverWait(driver, 600, 0.3).until(EC.alert_is_present())
                for i in range(2):  # 可应对可能出现一个或二个弹窗
                    alert = driver.switch_to.alert
                    print(alert.text)
                    alert.dismiss()  # 去除浏览器警告
                    time.sleep(0.3)

            # 等待用户审核，
            while True:

                try:
                    if '报名信息确认表' in str(driver.page_source):  # 如果有表格存在，说明用户还在审核页面，继续等待
                        pass
                    else:

                        # driver.switch_to.confirm().accept()
                        # driver.switch_to.alert.accept()

                        print('{}：审核完毕'.format(id_card))
                        time_now = time.strftime("%Y-%m-%d %H:%M:%S",
                                                 time.localtime())  # 记录一个现在的时间，如2021-09-04 16:30:00
                        file_handler.write(id_card + '  time:' + time_now + '\n')
                        time.sleep(100)
                        driver.get("https://ntcekw2.neea.edu.cn/teach/applicant/checkQuery1")  # 再次打开 输入证件号码的页面
                        break
                except UnexpectedAlertPresentException:
                    # print("alert处理")
                    try:
                        # driver.find_element_by_class_name("btnOrange").click()  # 点击【提交审核】按钮
                        driver.find_element_by_class_name("btnOrange").send_keys(Keys.ENTER)

                        WebDriverWait(driver, 5).until(EC.alert_is_present())


                        for i in range(2):  # 可应对可能出现一个或二个弹窗
                            alert = driver.switch_to.alert
                            print(alert.text)
                            alert.accept()  # 去除浏览器警告
                            time.sleep(0.3)
                    except NoAlertPresentException:
                        print('no')
                        pass


    except Exception as e:
        raise e
    # finally:
    #     file_handler.close()  # 最后关闭文件句柄
    #     driver.quit()  # 退出并关闭窗口的每一个相关的驱动程序 类似的表弟为 driver.close()
    #     time.sleep(8888)
