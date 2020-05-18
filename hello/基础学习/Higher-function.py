#!/usr/bin/env python
# -*- coding: utf-8 -*-

#高阶函数的抽象能力是非常强大的，而且，核心代码可以保持得非常简洁。

#变量可以指向函数
a=abs  #不要带括号
print a(-12)

#序列[1, 3, 5, 7, 9]变换成字符串
li=[1,3,5,7,9]
print map(str,li)


# 传入函数
def add(x,y,f):
    return f(x)+f(y)

x=int(raw_input('请输入变量x：'))
y=int(raw_input('请输入变量y：'))
#f=raw_input('请输入函数名：')
print add(x,y,abs)

#filter()函数用于过滤序列。
def is_odd(n):
    return n%2==1  #判断是不是奇数，奇数返回true

num=[1,2,3,4,5,6,7,8]
print filter(is_odd,num)

# 序列中的空字符串删掉
none=['A', '', 'B', None, 'C', '  ']

def noempty(s):
    return s and s.strip()
    #and 从左到右计算表达式，若所有值均为真，则返回最后一个值，若存在假，返回第一个假值。
    #and: 与运算，0、''、[]、()、{}、None 在布尔上下文中为假；其它任何东西都为真,都是真的话，返回最后一个值
print filter(noempty,none)

##
##排序算法

##Python内置的sorted()函数就可以升序
num=[3,5,4,9,9,7,1]
print '升序：',sorted(num)

#倒序排序，我们就可以自定义一个reversed_cmp函数
def re(x,y):
    if x>y:
        return -1
    if x<y:
        return 1
    return 0
#sorted()函数也是一个高阶函数，它还可以接收一个比较函数来实现自定义的排序
print '倒序：',sorted(num,re)

#匿名函数
print map(lambda x:x*x,[1,2,3,4])

f=lambda x:x*x
print f(2)


def xx(x,y):
    return lambda x,y:x*x+y*y

# 偏函数
import functools
int2 =functools.partial(int,base=2)
int2('1010101')


