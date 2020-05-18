#!/usr/bin/python
# coding: utf-8

# 面向对象 Class


class myclass(object):
    a = 123  # a是myclass的属性

    """
    第一个参数必须是self，self意思是对象本身
    """
    def __init__(self, var1):  # __init__是 class的构造方法
        self.var1 = var1  # var1就可以在整个类里面使用了

    def get(self):  # get是myclass的方法
        return self.var1

    def __del__(self):  # 析构方法：销毁的方法，一般用不到
        del self.var1


t = myclass("i am li")  # t是类myclass的一个实例

print t.a
print t.get()

print not (True and False)

a ="12345"
print(a[1:])

a = '"'
print(a)
