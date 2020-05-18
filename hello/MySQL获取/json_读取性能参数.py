#!/usr/bin/python
# -*- coding:UTF-8 -*-
import MySQLdb
import MySQLdb.cursors
import json

# 打开连接
db = MySQLdb.connect('192.168.120.104', 'root', 'mysqlmima', 'basedb')
# 获取操作游标
cursor = db.cursor(MySQLdb.cursors.DictCursor)
# 执行SQL语句
cursor.execute('SHOW GLOBAL STATUS ')
# 获取数据
data = cursor.fetchall()

data_json=json.dumps(data)
print data_json

# 关闭连接
db.close()