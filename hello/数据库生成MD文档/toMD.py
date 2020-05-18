# coding:utf-8

import cx_Oracle
import sys



ip = "192.168.180.158"
port = "1521"
username = "pasm"
password = "pasm"
sid = "pasm5"

db = cx_Oracle.connect(username+"/"+password+"@"+ip+":"+port+"/"+sid)
cursor = db.cursor()
cursor.execute("select 'TX-TXTXTX1' AS kbp,to_char(sysdate,'yyyy-mm-dd hh24:mi:ss')AS time,'888' as value from dual")
data = cursor.fetchone()
print(data)

cursor.close
db.close
