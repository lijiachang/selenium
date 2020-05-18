#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 定义函数
def my_abs(x):
    """求绝对值,进行参数检查"""
    if not isinstance(x, (int, float)):
        raise TypeError('参数错误！')  # 检查参数，自定义抛出异常
    if x >= 0:
        return x
    else:
        return -x


print "函数介绍：", my_abs.__doc__
print my_abs(120)
print my_abs(-12)


# print my_abs('abc')

# 空函数，还没想好怎么写，先运行起来
def nop():
    pass


# 函数返回多个值
import math


def move(x, y, step):
    nx = x + step
    ny = y + step
    return nx, ny


print move(12, 13, 3)


# 函数默认参数   (必选参数在前，默认参数在后, 只有一个参数可以是默认参数 )
# 计算任意数n次方:
def power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s


print power(5)
print power(5, 3)


# !!!默认参数必须指向不变对象！

# 可变参数 * 传入的多个参数，会变为元组如（1，2,3）
# 可变参数就是传入的参数个数是可变的，可以是1个、2个到任意个，还可以是0个
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum


# 关键字参数 ** 传入的多个参数，会变成字典如city='beijing' 变为 {'city','beijing'}
def person(name, age, **kw):
    print 'name:', name, 'age:', age, 'other:', kw


person('lichang', 22, city='beijing', job='cook')


# 递归函数
# 计算阶乘n! = 1 x 2 x 3 x ... x n，用函数fact(n)表示
def fact(n):
    if n == 1:
        return 1
    else:
        return n * fact(n - 1)


print fact(1)
print fact(5)
