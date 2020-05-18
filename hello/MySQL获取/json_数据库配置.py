#!/usr/bin/python
# -*- coding:UTF-8 -*-
import MySQLdb
import MySQLdb.cursors
import json


db = MySQLdb.connect('192.168.120.104', 'root', 'mysqlmima', 'basedb')
cursor = db.cursor(MySQLdb.cursors.DictCursor)

cursor.execute("select * from information_schema.schemata")

data = cursor.fetchall()
data_json=json.dumps(data)

print data_json

# a ="我".decode('utf-8')
# print a,len(a)

# 关闭连接
db.close()