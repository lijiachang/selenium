import time

from docx import Document  # 操作word文件的库
# selenium介绍 https://www.cnblogs.com/thb-blog/p/7609551.html
# IE 浏览器的配置https://blog.csdn.net/weijiechenlun133/article/details/84247159
from selenium import webdriver  # 该步骤是导入selenium的webdriver包，只有导入selenium包，我们才能使用webdriver API进行自动化脚本的开发
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

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
            driver.find_element_by_id("idCard").send_keys(id_card)  # 在浏览器定位身份证的输入框，然后输入身份证信息
            # driver.find_element_by_class_name("btnOrange").click()  # 点击【下一步】按钮
            driver.find_element_by_class_name("btnOrange").send_keys(Keys.ENTER)

            # print(driver.find_element_by_class_name("btnOrange").text)
            # driver.implicitly_wait(3)
            time.sleep(0.3)
            # print(driver.page_source)

            # 等待用户审核，
            while True:
                if '报名信息确认表' in driver.page_source:  # 如果有表格存在，说明用户还在审核页面，继续等待
                    pass
                else:
                    print('{}：审核完毕'.format(id_card))
                    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 记录一个现在的时间，如2021-09-04 16:30:00
                    file_handler.write(id_card + '  time:' + time_now + '\n')
                    driver.get("https://ntcekw2.neea.edu.cn/teach/applicant/checkQuery1")  # 再次打开 输入证件号码的页面
                    break
    except Exception:
        raise
    finally:
        file_handler.close()  # 最后关闭文件句柄
        driver.quit()  # 退出并关闭窗口的每一个相关的驱动程序 类似的表弟为 driver.close()
        time.sleep(8888)
