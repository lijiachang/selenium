# coding=utf-8

import cx_Oracle
import sys

if len(sys.argv) != 6:
    print("please use parameter:Username Password IP Port Sid")
    sys.exit()
else:
    username = sys.argv[1]
    password = sys.argv[2]
    ip = sys.argv[3]
    port = sys.argv[4]
    sid = sys.argv[5]

db = cx_Oracle.connect(username+"/"+password+"@"+ip+":"+port+"/"+sid)
cursor = db.cursor()
cursor.execute("select 'TX-TXTXTX1' AS kbp,to_char(sysdate,'yyyy-mm-dd hh24:mi:ss')AS time,'888' as value from dual")
data = cursor.fetchone()
print(data)

cursor.close
db.close

