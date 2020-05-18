#!/usr/bin/python
# -*- coding:UTF-8 -*-
import MySQLdb

# 打开连接
db = MySQLdb.connect('192.168.120.104', 'root', 'mysqlmima', 'basedb')
# 获取操作游标
cursor = db.cursor()
# 执行SQL语句
cursor.execute('SHOW GLOBAL STATUS ')
# 获取数据
data = cursor.fetchall()
for row in data:
    name=row[0]
    value=row[1]
    print '%s   %s' %  (name,value)

print data

# 关闭连接
db.close()
