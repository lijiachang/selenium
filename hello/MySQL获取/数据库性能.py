#/usr/bin/python
#-*- coding:UTF-8 -*-

import MySQLdb

db=MySQLdb.connect('192.168.120.104','root','mysqlmima','basedb')
cursor=db.cursor()
cursor.execute("SELECT TABLE_SCHEMA,SUM(index_length) as 'IndexSize',sum(DATA_LENGTH) as 'DataSize' FROM information_schema.TABLES group by TABLE_SCHEMA")
data=cursor.fetchall()

for row in data:
    print '%s %s %s' %(row[0],row[1],row[2])

db.close()
