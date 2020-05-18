#!/usr/bin/python
# coding:utf-8

# str字符串反转排序
a = "abcdefg"
print a[::-1]  # 步进
print a[::-2]  # 反转输出，奇数位

# sorted 方法
a = "aAsmr3idd4bgs7Dlsf9eAF"
print sorted(a,reverse=True)  # 排序 并反转

# 列表b根据列表a排序 list.sort
a = "asdfghjqwert"
b = "adefg"
b_list = list(b)
b_list.sort(key=list(a).index)
print b_list

# 数据结构------排序

a = range(1, 10, 2)
print a

print sorted(a, reverse=True)  # reverse参数 反排序
print sorted(a, key=int)  # 根据int数字类型排序，可以根据string字符串
a.sort(reverse=True)  # sorted和sort区别，list中自带方法sort是操作原数据

# list内2元组排序
b = [('a', 1), ('b', 2), ('c', 3)]  # 根据元组内第二个数字排序
b.sort(key=lambda x: x[1], reverse=True)
print b

# list内3元组排序 根据第二三位数字联合排序,先排序第二位，再根据第三位排序
c = [(1, 2, 3), (2, 3, 4), (3, 2, 1)]
import operator

c.sort(key=operator.itemgetter(1, 2))  # 下标就是 1 2，
print c
