import time
import urllib3
from selenium import webdriver
import selenium

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

    def notifications_do_not_disturb(self):
        """暂停浏览器通知，直到下次打开"""
        self.browser.get('about:preferences#privacy')
        _obj = self.browser.find_element_by_id('notificationsDoNotDisturb')
        _obj.click()

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
        self.enabled_click(click)  # 点击右上角头像

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
            for _ in range(5):  # 重试五次
                try:
                    # 点击一条账户
                    account_line = self.browser.find_element_by_css_selector(
                        'div.account-menu__account:nth-child({})'.format(x + 1))
                    account_line.click()
                    break
                except selenium.common.exceptions.NoSuchElementException:
                    time.sleep(0.5)
                    self.click_id_wrapper()
                    time.sleep(0.5)
            yield
            time.sleep(0.5)
            self.click_id_wrapper()
            time.sleep(0.5)

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

    def enabled_click(self, _button, click=True):
        while True:
            if _button.is_enabled():
                # 此点击方式可以解决： selenium Element is not clickable because another element obscures it
                if click:
                    self.browser.execute_script('arguments[0].click()', _button)
                break
            time.sleep(0.1)

    def waiting_overlay(self):
        """等待模糊图层消失"""
        while True:
            time.sleep(0.1)
            try:
                if self.browser.find_element_by_xpath('//div[@class="loading-overlay"]'):
                    pass
                else:
                    break
            except selenium.common.exceptions.NoSuchElementException:
                break

    def find_network_error(self):
        """出现错误：Gas price estimation failed due to network error."""
        try:
            el = self.browser.find_element_by_xpath('//div[@class="dialog send__error-dialog dialog--error"]')
            if 'network err' in el.text:
                print('find network error.')
                return True
        except selenium.common.exceptions.NoSuchElementException:
            return False
        return False

    def select_sana(self):
        """选择币种SANA，判断是否为0"""
        #  点击币种下拉框
        try:
            _button = self.browser.find_element_by_xpath('//div[@class="send-v2__asset-dropdown__input-wrapper"]')
            self.enabled_click(_button)
        except Exception as e:
            print(e)
            # 跑到了 输入账号窗口？ 重试一次
            input_ = self.browser.find_element_by_xpath('//input[@class="ens-input__wrapper__input"]')
            input_.send_keys(main_account_id)  # 输入账户id
            _button = self.browser.find_element_by_xpath('//div[@class="send-v2__asset-dropdown__input-wrapper"]')
            self.enabled_click(_button)

        time.sleep(1)
        # 选择SANA币
        elements = self.browser.find_elements_by_xpath('//div[@class="send-v2__asset-dropdown__asset"]')
        for element in elements:
            if 'SANA' in element.text:
                # 如果余额是0，则跳过
                while True:
                    try:
                        sana_ = element.text.split('余额 :')[1].split('SANA')[0].strip()
                        if float(sana_) >= 0.0:
                            break
                    except Exception:
                        pass
                    time.sleep(0.1)

                if sana_ == '0':
                    # 使得 页面可点击
                    self.enabled_click(element)

                    # 加载转圈的涂层 //div[@class="loading-overlay"]
                    # self.waiting_overlay()
                    time.sleep(0.3)

                    # 点击右上角的取消按钮，返回账户主页
                    button_cancel = self.browser.find_element_by_xpath(
                        '//a[@class="button btn-link page-container__header-close-text"]')
                    try:
                        self.enabled_click(button_cancel)
                    except selenium.common.exceptions.ElementClickInterceptedException:
                        self.enabled_click(button_cancel)
                    # webdriver.ActionChains(self.browser).move_to_element(button_cancel).click(
                    #    button_cancel).perform()
                    return 0
                # element.click()

                # 非数量0，选择SANA
                self.enabled_click(element)
        return True

    def input_main_account_id(self):
        """在Send to界面确保输入账户id"""
        # self.enabled_click(input_)  # 点击输入框
        while True:
            input_ = self.browser.find_element_by_xpath('//input[@class="ens-input__wrapper__input"]')
            input_.send_keys(main_account_id)  # 输入账户id
            try:
                self.browser.find_element_by_xpath('//div[@class="send-v2__form-label"]')  # 转账界面的[资产]
            except selenium.common.exceptions.NoSuchElementException:
                pass  # 找不到说明没有输入id成功，继续输入
            else:
                break  # 找到了，说明已经到了转账界面
            # 再次点击输入框，准备输入
            input_ = self.browser.find_element_by_xpath('//input[@class="ens-input__wrapper__input"]')
            self.enabled_click(input_)  # 点击输入框

    def sana_transfer(self):
        """转账汇入指定账户"""
        # 输入转入的ID
        self.input_main_account_id()

        # 第一次尝试选择SANA
        try:
            sana_ = self.select_sana()
        except Exception:
            print('err:to send to page, retry: input_main_account_id and select_sana')
            self.input_main_account_id()
            sana_ = self.select_sana()

        if sana_ is True:
            # 数额的单位
            for _ in range(5):  # 重试五次
                time.sleep(0.3)
                try:
                    unit = self.browser.find_element_by_xpath(
                        '/html/body/div[1]/div/div[3]/div/div[3]/div/div[2]/div[2]/div[1]/div/div/div[1]/div').text
                except Exception as e:
                    print('unit e:', e)
                    continue
                if 'SANA' in unit:  # 已经选择了SANA，继续
                    break
                else:
                    print('{} != SANA, retry'.format(unit))
                    sana_ = self.select_sana()  # 没有正确选择SANA，重试
            else:  # 出现了网络错误
                # 点击右上角的取消按钮，返回账户主页
                button_cancel = self.browser.find_element_by_xpath(
                    '//a[@class="button btn-link page-container__header-close-text"]')
                try:
                    self.enabled_click(button_cancel)
                except selenium.common.exceptions.ElementClickInterceptedException:
                    self.enabled_click(button_cancel)
                return 0

        if sana_ == 0:  # SANA数量为0，跳过
            return 0

        # 选择最大数额
        amount_max_button = self.browser.find_element_by_xpath('//button[@class="send-v2__amount-max"]')
        self.enabled_click(amount_max_button)
        # 解决连接服务器慢，按钮不能点击：because another element <div class="loading-overlay"> obscures it
        # webdriver.ActionChains(self.browser).move_to_element(amount_max_button).click(amount_max_button).perform()

        # 点击下一步按钮
        next_button = self.browser.find_element_by_xpath(
            '//button[@class="button btn-secondary page-container__footer-button"]')
        self.enabled_click(next_button)

        # 跳转到确认界面，
        # 解析转账金额和手续费xDAI
        amount = self.browser.find_elements_by_xpath(
            '//div[@class="transaction-detail-item__row"]/h6[@class="box box--margin-top-1 box--margin-right-0 box--margin-bottom-1 box--margin-left-0 typography transaction-detail-item__total typography--h6 typography--weight-bold typography--style-normal typography--color-black"]')
        amount = amount[1].text  # 获取总额信息：5 SANA + 0.000094 xDAI
        amount = amount.split('SANA')[0].strip()
        # 点击确认
        time.sleep(0.5)
        confirm_button = self.browser.find_element_by_xpath(
            '//button[@class="button btn-primary page-container__footer-button"]')
        while True:
            if confirm_button.is_enabled():
                confirm_button.click()
                break
            time.sleep(0.1)
        #

        return float(amount)


if __name__ == '__main__':
    browser = FireFoxDriver()
    browser.notifications_do_not_disturb()  # 禁止通知
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
