import time
import urllib3
from selenium import webdriver

urllib3.disable_warnings()

# 解析配置文件
with open('profile.ini', 'r', encoding='utf-8') as (f):
    readers = f.readlines()
    main_account_id = readers[0].split('=')[-1].split('#')[0].strip()
    profileDir = readers[1].split('=')[-1].split('#')[0].strip()
    metamask_url = readers[2].split('=')[-1].split('#')[0].strip()
    metamask_password = readers[3].split('=')[-1].split('#')[0].strip()


class FireFoxDriver:
    """MetaMask 10.2.2"""

    def __init__(self):
        profile = webdriver.FirefoxProfile(profileDir)
        self.browser = webdriver.Firefox(profile)
        self.browser.set_page_load_timeout(30)  # 设置页面加载超时
        self.browser.implicitly_wait(16)
        # 若出现浏览器闪退，尝试关闭多余的拓展插件

        # 加载过滤id列表的文件
        self.filter_ids = None
        try:
            with open('abandon_id.txt', 'r') as file:
                self.filter_ids = file.readlines()
        except Exception as e:
            print('load abandon_id.txt failed:{}'.format(e))

    def login(self):
        time.sleep(2)
        self.browser.get(metamask_url)
        elem = self.browser.find_element_by_id("password")
        elem.send_keys(metamask_password)  # 发送到输入框关键词

        # 登录
        click_obj = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/button')
        # 解决连接服务器慢，按钮不能点击：because another element <div class="loading-overlay"> obscures it
        webdriver.ActionChains(self.browser).move_to_element(click_obj).click(click_obj).perform()

    def click_id_wrapper(self):
        """点击右上角头像"""
        click = self.browser.find_element_by_class_name('identicon__address-wrapper')
        click.click()  # 点击右上角头像

    def get_account_list_info(self):
        """点击头像，获取用户信息"""
        self.click_id_wrapper()
        # 获取我的账户列表
        account_list_obj = self.browser.find_element_by_class_name('account-menu__accounts')
        accounts_info = account_list_obj.text
        accounts_info = '   '.join(x for x in accounts_info.split('\n')).split('XDAI')
        print('#' * 20)
        print('XDAI 账户列表：')
        money_total = 0
        for account in accounts_info:
            # 兼容列表中有个多余的 , '   已导入']
            account = account.replace('已导入', '').strip()
            if account:
                account_name, money = account.rsplit(maxsplit=1)
                print(format(account_name.strip(), '<10s'), money)
                money_total += float(money)
        print('XDAI 账户总计:     {}'.format(money_total))
        print('#' * 20)

    def gen_loop_user(self):
        # 账户列表下的子Div，具体账户
        account_nums = self.browser.find_elements_by_xpath(
            '//div[@class="account-menu__account account-menu__item--clickable"]')
        for x in range(len(account_nums)):
            account_list = self.browser.find_elements_by_xpath(
                '//div[@class="account-menu__account account-menu__item--clickable"]')
            account_line = account_list[x]
            account_line.click()
            yield
            time.sleep(0.3)
            self.click_id_wrapper()
            # time.sleep(3)

    def get_current_account_id(self):
        """获取当前账户ID # 0x7f62...9F56"""
        current_account_id = self.browser.find_element_by_xpath('//div[@class="selected-account__address"]').text
        return current_account_id

    def is_main_id(self, current_id_):
        start, end = current_id_.split('...')
        # 如果此Id是主账户ID
        if main_account_id.startswith(start) and main_account_id.endswith(end):
            return True
        # 如果此ID是过滤列表中的ID
        elif self.filter_ids:
            for account_id in self.filter_ids:
                account_id = account_id.strip()
                if account_id.startswith(start) and account_id.endswith(end):
                    return True
        else:
            return False

    def click_send_button(self):
        # 账户主页的[发送]按钮
        account_send_button = self.browser.find_element_by_xpath('//button[@data-testid="eth-overview-send"]')
        account_send_button.click()

    def sana_transfer(self):
        """转账汇入指定账户"""
        # 输入转入的ID
        input_ = self.browser.find_element_by_xpath('//input[@class="ens-input__wrapper__input"]')
        input_.click()
        input_.send_keys(main_account_id)
        #  点击币种下拉框
        _button = self.browser.find_element_by_xpath('//div[@class="send-v2__asset-dropdown__input-wrapper"]')
        _button.click()
        # 选择SANA币
        elements = self.browser.find_elements_by_xpath('//div[@class="send-v2__asset-dropdown__asset"]')
        for element in elements:
            if 'SANA' in element.text:
                # 如果余额是0，则跳过
                if element.text.split('余额 :')[1].split('SANA')[0].strip() == '0':
                    # 使得 页面可点击
                    element.click()
                    # 点击右上角的取消按钮，返回账户主页
                    button_cancel = self.browser.find_element_by_xpath(
                        '//a[@class="button btn-link page-container__header-close-text"]')
                    button_cancel.click()
                    return 0
                element.click()

        # 选择最大数额
        amount_max_button = self.browser.find_element_by_xpath('//button[@class="send-v2__amount-max"]')
        # amount_max_button.click()
        # 解决连接服务器慢，按钮不能点击：because another element <div class="loading-overlay"> obscures it
        webdriver.ActionChains(self.browser).move_to_element(amount_max_button).click(amount_max_button).perform()

        # 点击发送按钮
        next_button = self.browser.find_element_by_xpath(
            '//button[@class="button btn-secondary page-container__footer-button"]')
        next_button.click()
        # 跳转到确认界面，
        # 解析转账金额和手续费xDAI
        amount = self.browser.find_elements_by_xpath(
            '//div[@class="transaction-detail-item__row"]/h6[@class="box box--margin-top-1 box--margin-right-0 box--margin-bottom-1 box--margin-left-0 typography transaction-detail-item__total typography--h6 typography--weight-bold typography--style-normal typography--color-black"]')
        amount = amount[1].text  # 获取总额信息：5 SANA + 0.000094 xDAI
        amount = amount.split('SANA')[0].strip()
        # 点击确认
        next_button = self.browser.find_element_by_xpath(
            '//button[@class="button btn-primary page-container__footer-button"]')
        next_button.click()

        return int(amount)


if __name__ == '__main__':
    browser = FireFoxDriver()
    browser.login()  # 登录
    browser.get_account_list_info()  # 统计账户信息
    total_sana = 0
    print('开始SANA批量汇入主账户: {}'.format(main_account_id))
    for user in browser.gen_loop_user():
        current_id = browser.get_current_account_id()

        if browser.is_main_id(current_id):
            print('{} : 跳过！'.format(current_id))
            continue

        browser.click_send_button()  # 点击账户主页的发送按钮，准备转账
        sana_num = browser.sana_transfer()
        total_sana += sana_num
        print('{} : {} SANA 已汇入主账户！'.format(current_id, sana_num))
    print('操作完成，合计共 {} SANA'.format(total_sana))

time.sleep(8888)
