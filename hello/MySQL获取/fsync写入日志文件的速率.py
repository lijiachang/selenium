#!/usr/bin/python
# -*- coding:UTF-8 -*-
import MySQLdb

# 打开连接
db = MySQLdb.connect('192.168.120.104', 'root', 'mysqlmima', 'basedb')
# 获取操作游标
cursor = db.cursor()
# 执行SQL语句
cursor.execute("show status like 'Innodb_os_log_fsyncs'")
# 获取数据
data = cursor.fetchall()
for row in data:
    name=row[0]
    value=row[1]
    print '%s   %s' %  (name,value)



# 关闭连接
db.close()
