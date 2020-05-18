#encoding=utf8
from JDPackage import *

#https://github.com/HiddenStrawberry/JDPackage/wiki

a=Account('17600209982', 'lichang1', '944581577', 'lichang1995') #新建账号a
a.login_pc() #账号PC端登录
#a.login()   #账号M端登录

a.get_couponlist() #获取优惠券列表
a.get_msglist() #获取消息列表
a.get_payment() #获取订单列表

# b=Account('#', '#', '#', '#') #新建账号b
# b.login_pc() #账号PC端登录
# b.login()   #账号M端登录
#
# b.get_couponlist() #获取优惠券列表
# b.get_msglist() #获取消息列表
# b.get_payment() #获取订单列表
