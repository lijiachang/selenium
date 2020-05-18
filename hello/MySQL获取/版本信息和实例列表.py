#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import MySQLdb.cursors  #11.28 增加获取MySQL字段，使用DictCursor

# 打开数据库连接
db = MySQLdb.connect("192.168.120.104", "root", "mysqlmima", "basedb")

# 使用cursor() 方法获取操作游标
cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor) #输出加上字段

# 使用execute方法执行SQL语句
cursor.execute("select version();")

# 使用fetchone()方法获取数据
data = cursor.fetchone()

print "数据库版本：%s" % data

#print type(dblist)  查询了类型是<type 'tuple'>

cursor.execute("show DATABASES;")
dblist = cursor.fetchall()
print "数据库实例列表：",
for name in dblist:
    print "%s "%name,

print   #换行

#使用json输出
import json
data_json=json.dumps(data)
print data_json

dblist_json=json.dumps(dblist)
print dblist_json

# 最后关闭数据库连接
db.close()
