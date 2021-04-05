import pymssql
import generaloperat
from basic import Basic
from frontdesk import FrontDesk
from purchasemanage import PurchaseManage
from adminmanage import AdminManage
from logo import logo_str
import os


def link():
    con = pymssql.connect(host="127.0.0.1",  # 连接数据库
                          user="zhanglinxin",
                          password="zhanglinxin",
                          database="Supermarket",
                          charset='utf8')
    return con


def meta():
    while True:
        os.system("cls")
        print(logo_str)
        print("------------------------------------------------")
        print("1: 销售员界面")  # 售货
        print("2: 采购员界面")  # 进货
        print("3: 管理员界面")
        print("                                     其他任意输入退出")
        print("------------------------------------------------")
        cmd = input("请输入选项:").strip()
        if cmd == "1":
            front_desk = FrontDesk()
            front_desk.meta()
        elif cmd == "2":
            purchase_manage = PurchaseManage()
            purchase_manage.meta()
        elif cmd == "3":
            admin_manage = AdminManage()
            admin_manage.meta()
        else:
            break
        os.system("pause")


if __name__ == '__main__':
    try:
        conn = link()
        Basic.setConn(conn)
        meta()
    except Exception as e:
        print("出现错误，原因：", e)

