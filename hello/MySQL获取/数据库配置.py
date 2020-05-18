#!/usr/bin/python
#-*- conding:UTF-8 -*-

import MySQLdb

db =MySQLdb.connect('192.168.120.104','root','mysqlmima','basedb')
cursor=db.cursor()
cursor.execute('select * from information_schema.schemata')
data=cursor.fetchall()

for row in data:
    print '%s %s %s %s %s' %(row[0],row[1],row[2],row[3],row[4])

# DATABASE_CM
db.close()