# -*- coding: cp936 -*-
from cashier import *
from commodity import *
import datetime
import random


class Basic:
    conn = None

    # def __init__(self,conn):
    #     self.conn=conn
    @classmethod
    def setConn(cls, conn):  # ok
        Basic.conn = conn

    @classmethod
    def gbk_parsing(cls, rows):
        """解决设置utf8编码后，插入数据库正常，查询数据库乱码的问题"""
        new_list = list()
        for row in rows:
            new_list.append(
                [field.encode('latin-1').decode('gbk') if isinstance(field, str) else field for field in row])
        return new_list

    @classmethod
    def runQuery(cls, sql):  # ok
        with Basic.conn.cursor() as cursor:
            cursor.execute(sql)
            ans = cursor.fetchall()

            return Basic.gbk_parsing(ans)

    @classmethod
    def runModify(cls, sql):  # ok
        with Basic.conn.cursor() as cursor:
            cursor.execute(sql)
            Basic.conn.commit()

    @classmethod
    def query_one_shell(cls, sell_no):
        '''返回列表,没有则返回空列表'''
        sql = "select * from Sell where sell_no='{}'".format(sell_no)
        # print(sql)
        ans = Basic.runQuery(sql)
        if ans != []:
            ans = ans[0]
        return ans

    @classmethod
    def queryOneCommodity(cls, com_num):  # ==queryOneCommodityView
        '''返回列表,没有则返回空列表'''
        sql = "select * from Commodity where commodity_no='{}'".format(com_num)
        # print(sql)
        ans = Basic.runQuery(sql)
        if ans != []:
            ans = ans[0]
        return ans

    @classmethod
    def queryAllCommodity(cls):  # ==queryAllCommodityView
        '''返回列表'''
        sql = "select * from Commodity"
        return Basic.runQuery(sql)

    @classmethod
    def queryOneCashier(cls, cash_num):
        sql = "select * from Cashier where cashier_no='{}'".format(cash_num)
        res = Basic.runQuery(sql)
        if res != []:
            res = res[0]
        return res

    @classmethod
    def queryOnePurchase(cls, pur_num):
        sql = "select * from Purchaser where purchaser_no='{}'".format(pur_num)
        res = Basic.runQuery(sql)
        if res != []:
            res = res[0]
        return res

    @classmethod
    def addOneSell(cls, cashier_no, com_no, sell_no, sell_cnt, sell_rmoney):  # 向支付条目中添加信息
        sql = "insert into Sell values('{}','{}','{}',{},{},'{}')".format(cashier_no, com_no, sell_no, sell_cnt,
                                                                          sell_rmoney, Basic.getNowDateTime())
        print(sql)
        Basic.runModify(sql)

    @classmethod
    def del_one_sell(cls, sell_no):  # 删除一条交易记录
        sql = "delete   from  Sell  where  sell_no='{}'".format(sell_no)
        Basic.runModify(sql)

    @classmethod
    def addOneCommodity(cls, com_no, com_name, com_type, com_size, com_price, com_mdate, com_edate, com_quantity):
        sql = "insert into Commodity values('{}','{}','{}','{}',{},'{}','{}',{})".format(com_no, com_name, com_type,
                                                                                         com_size, com_price, com_mdate,
                                                                                         com_edate, com_quantity)
        print(sql)
        Basic.runModify(sql)

    @classmethod
    def modifyOneCommodity(cls, com_num, com_name, com_type, com_size, com_price, com_mdate, com_edate, com_quantity):
        sql = '''update Commodity
        set Commodity__name='{}',commodity__type1='{}',commodity__size='{}',commodity__sprice={},commodity__mdate='{}',commodity__edate='{}',commodity__quantity={}
        where commodity_no='{}'
        '''.format(com_name, com_type, com_size, com_price, com_mdate, com_edate, com_quantity, com_num)
        Basic.runModify(sql)

    @classmethod
    def addOneCommodityCnt(cls, com_num, com_cnt):
        sql = "update Commodity set commodity__quantity=commodity__quantity +{} where commodity_no='{}'".format(com_cnt,
                                                                                                                com_num)
        Basic.runModify(sql)

    @classmethod
    def addOneCashier(cls, cash_no, cash_name, cash_pwd, cash_sex, cash_age, cash_hourse, cash_salary, cash_phone,
                      cash_entry):
        sql = "insert into Cashier values('{}','{}','{}','{}',{},'{}',{},{},{})".format(cash_no, cash_name, cash_pwd,
                                                                                        cash_sex, cash_age, cash_hourse,
                                                                                        cash_salary, cash_phone,
                                                                                        cash_entry)
        Basic.runModify(sql)

    @classmethod
    def modifyOneCashier(cls, cash_no, cash_name, cash_pwd, cash_sex, cash_age, cash_hourse, cash_salary, cash_phone,
                         cash_entry, cash_edu):
        sql = '''update Cashier set cashier_name='{}',cashier_pwd='{}',cashier_sex='{}',cashier_age={},cashier_hourse='{}',cashier_salary={},cashier_phone={},cashier_entrytime='{}',employee_education_id={} where cashier_no='{}'
'''.format(cash_name, cash_pwd, cash_sex, cash_age, cash_hourse, cash_salary, cash_phone, cash_entry, cash_edu, cash_no)
        Basic.runModify(sql)

    @classmethod
    def addOnePurchaser(cls, pur_no, pur_name, pur_pwd, pur_sex, pur_age, pur_salary, pur_phone, pur_entry, pur_edu):
        sql = "insert into Purchaser values('{}','{}','{}','{}',{},{},{},'{}',{})".format(pur_no, pur_name, pur_pwd,
                                                                                          pur_sex,
                                                                                          pur_age,
                                                                                          pur_salary, pur_phone,
                                                                                          pur_entry,
                                                                                          pur_edu)
        Basic.runModify(sql)

    @classmethod
    def modifyOnePurchaser(cls, pur_no, pur_name, pur_sex, pur_age, pur_salary, pur_phone, pur_entry, pur_edu):
        sql = '''update Purchaser
        set purchaser_name='{}',purchaser_sex='{}',purchaser_age={},purchaser_salary={},purchaser_phone={},purchaser_entrytime='{}',employee_education_id={}
        where purchaser_no='{}'
        '''.format(pur_name, pur_sex, pur_age, pur_salary, pur_phone, pur_entry, pur_edu, pur_no)
        Basic.runModify(sql)

    @classmethod
    def delCommodityCnt(cls, com_num, com_cnt):
        '''删除某一个商品的数量 '''
        sql = "update Commodity set commodity__quantity=commodity__quantity -{} where commodity_no='{}'".format(com_cnt,
                                                                                                                com_num)
        print(sql)
        Basic.runModify(sql)

    @classmethod
    def delOneCashier(cls, cash_no):
        sql = "delete   from  Cashier  where  cashier_no='{}'".format(cash_no)
        Basic.runModify(sql)

    @classmethod
    def delOnePurchase(cls, pur_no):
        sql = "delete  from Purchaser where purchaser_no='{}'".format(pur_no)
        Basic.runModify(sql)

    @classmethod
    def delOneCommodity(cls, com_no):
        sql = "delete from Commodity  where commodity_no='{}'".format(com_no)
        Basic.runModify(sql)

    @classmethod
    def addOneStock(cls, pur_no, com_no, stock_no, com_price, com_cnt, in_date):
        sql = "insert into Stock values('{}','{}','{}',{},{},'{}')".format(pur_no, com_no, stock_no, com_price, com_cnt,
                                                                           in_date)
        print(sql)
        Basic.runModify(sql)

    @classmethod
    def queryAllStock(cls):
        sql = "select * from Stock"
        res = Basic.runQuery(sql)
        return res

    @classmethod
    def queryAllCashier(cls):
        sql = "select c.cashier_no, c.cashier_name,c.cashier_pwd,c.cashier_sex,c.cashier_age,c.cashier_hourse," \
              "c.cashier_salary,c.cashier_phone,e.diploma from Cashier as c, " \
              "EducationInfo as e where c.employee_education_id = e.education_id"
        res = Basic.runQuery(sql)
        return res

    @classmethod
    def queryAllPurchaser(cls):
        sql = "select * from Purchaser"
        sql = "select c.purchaser_no, c.purchaser_name,c.purchaser_pwd,c.purchaser_sex,c.purchaser_age," \
              "c.purchaser_salary,c.purchaser_phone,c.purchaser_entrytime,e.diploma from Purchaser as c, " \
              "EducationInfo as e where c.employee_education_id = e.education_id"
        res = Basic.runQuery(sql)
        return res

    @classmethod
    def queryAllSell(cls):
        sql = "select * from Sell"
        res = Basic.runQuery(sql)
        return res

    @classmethod
    def queryMySell(cls, id):
        sql = "select * from Sell where cashier_no='{}'".format(id)
        res = Basic.runQuery(sql)
        return res

    @classmethod
    def getNowDateTime(cls):
        # return datetime.datetime.now().strftime("%Y-%m-%d")
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def getFlowNum(cls):
        res = datetime.datetime.now().strftime("%Y%m%d") + "%06d" % (random.randint(0, 1000000))
        return res

    @classmethod
    def queryOneSellFlowNum(cls, sell_num):
        sql = "select * from sell where sell_no='{}'".format(sell_num)
        res = cls.runQuery(sql)
        if res != []:
            res = res[0]
        return res

    @classmethod
    def queryOneStockFlowNum(cls, stock_num):
        sql = "select * from stock where stock_no='{}'".format(stock_num)
        res = cls.runQuery(sql)
        if res != []:
            res = res[0]
        return res

    @classmethod
    def queryOneAdmin(cls, admin_no):
        sql = "select * from Administrator where admin_no='{}'".format(admin_no)
        res = cls.runQuery(sql)
        if res != []:
            res = res[0]
        return res


if __name__ == '__main__':
    import pymssql

    con = pymssql.connect(host="127.0.0.1",  # 连接数据库
                          user="zhanglinxin",
                          password="zhanglinxin",
                          database="Supermarket",
                          charset='utf8')
    Basic.setConn(con)
    import json

    # sql = "insert into Commodity values('011','旺仔','饮料','瓶',5.0,'2020-02-02','2022-02-02',0)"
    # Basic.runModify(sql)
    # print('done')
    sql = "select * from Commodity"
    # print(Basic.runQuery(sql.encode('utf8'))[0][1].encode('latin-1').decode('gbk'))
    print(Basic.runQuery(sql))

    admin_no = '001'
    sql = "select * from Administrator where admin_no='{}'".format(admin_no)
    res = Basic.runQuery(sql)
    print(res)
