# coding: utf-8
import sys

a = [1, 2, 3]

try:
    print(a[5])
except Exception as a:
    exc = sys.exc_info()
    print"出现异常", a
    print(exc)
else:
    "如果没有出现异常，就执行："
    print("没有出现异常")
finally:
    "不管是否出现异常，都会执行"
    print("测试")

# 断言,开发时期检查代码的方式，只断言绝对不能出现的错误
# assert 表达式 , 出错后的抛出信息
assert 1 > 4, "出错"
