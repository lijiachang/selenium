# coding:utf-8

import re

# 匹配电话号码
a = re.match(r"^\d{3}-\d{3,8}$", "010-123456711111d11")
print(a)

if a:
    print("正则成功匹配")
else:
    print("未匹配")

# 分割
b = "a  b     c"
print(b.split(" "))
print(b.split())
c = "1aaa2bbb3ccc123abc"
pattern = r"\d+"
print(re.split(pattern, c))

# 分组
m = re.match(r"^(\d{3})-(\d{3,8})$", "010-4571668")
print(m.group(0))
print(m.group(1))
print(m.group(2))
print(m.group())  # 不填写参数时，返回group(0)

# 贪婪匹配
# 由于\d+采用贪婪匹配，直接把后面的0全部匹配了，结果0*只能匹配空字符串了（没作用了）
t = re.match(r"^(\d+)(0*)$", "10230000")
print(u"贪婪匹配")
print(t.groups())

# 非贪婪匹配，尽可能少匹配
t = re.match(r"^(\d+?)(0*)$", "10230000")
print(u"非贪婪匹配")
print(t.groups())

# re.match 和 re.search 区别
print("########re.match 和 re.search 区别##########")
pattern = re.compile(r"world")  # 将正则表达式编译成Pattern对象
m = re.match(pattern, "hello world!")
print(m)
m = re.search(pattern, "hello world!")
print(m)
"""search方法与match方法极其类似，区别在于match()函数只检测re是不是在string的开始位置匹配，
search()会扫描整个string查找匹配，match（）只有在0位置匹配成功的话才有返回，如果不是开始位置
匹配成功的话，match()就返回None。同样，search方法的返回对象同样match()返回对象的方法和属性。"""

# r.findall 搜索string，以列表形式返回全部能匹配的子串。
pattern = re.compile(r"\d+")
print(re.findall(pattern,c))