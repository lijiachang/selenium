#!/usr/bin/env python
# -*- coding: utf-8 -*-

#第一种

print "%s is a %s" %('I','boy')

#第二种 前面用key站位，后面用字典的形式，常用于数据库

print "%(who)s is a %(gender)s" %{'who':'I','gender':'girl'}

#第三种，官方推荐,清晰

print "{who} is a {gender}".format(who='I',gender='boy')

ls = list()
print(ls[0] is None)