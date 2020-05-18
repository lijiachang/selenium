#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 迭代：
# dic的迭代，默认迭代的是key
dic = {'name': 'li', 'age': 22, 'job': 'wocker'}
for k in dic:
    print k
print type(dic)
# 想要迭代value的话,好像用dic.values()也可以
for k in dic.itervalues():
    print k

# 整数不可以迭代，也不可以切片，str可以切片
print str(1234)[-1]

# 下标循环
a = ['A', 'B', 'C']
for i, value in enumerate(a):
    print i, value

# 列表生成式range
print range(1, 5)  # 生成1到5列表，默认步长1
# 列表生成式xrange
x = xrange(1, 10, 1)  # 生成1到10列表，步长1  生成的是xrange对象
print x
print x[0]  # 调用的时候和range一样

# 两者的区别：
# range ：直接生成一个列表对象
# xrange：生成一个xrange对象
# xrange的用法：1.当操作一个非常庞大的数据，而且内存比较紧。可以用来节省内存
#               2.xrange一般用在循环里面，只需要操作部分数据的时候使用

# 列表推导式
print [x * x for x in range(10)]  # 返回1-10的所有值的平方列表
print ["my name is %d" % x for x in range(10)]  # 生成字符串的列表
print [(x, y) for x in range(2) for y in range(2)]  # 生成元组的列表
print dict([(x, y) for x in range(2) for y in range(2)])  # 生成字典的列表 由于key的唯一性，有些会覆盖
print range(2)
print "********列表推导式*************"
print [x for x in xrange(101)]

# 提取list中的数字
list1 = "abs123df44yui789"
print "".join([s for s in list1 if s.isdigit()])

# 输出不是数字的部分
a = "aAsmr3idd4bgs7Dlsf9eAF"
a = "".join([x for x in a if not x.isdigit()])
print(a)
