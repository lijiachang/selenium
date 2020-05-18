# /bin/usr/python
# coding:utf-8

# 需要安装模块MySQLdb  （python2.6 以下需要安装simplejson）

import MySQLdb

try:
    import json
except ImportError:
    import simplejson as json

db_ip="192.168.120.104" #raw_input("MySQL ip：")
# db_user=raw_input("user:")
# db_pw=raw_input("password:")
# db_instance=raw_input("instance:")

db = MySQLdb.connect(db_ip, "root", "mysqlmima", "basedb")
cursor = db.cursor()

# 自mysql启动以来,已经发送给服务器的查询的个数(包含增删查)
cursor.execute("SHOW GLOBAL STATUS LIKE 'Questions';")
questions=cursor.fetchone()[1]

# 自mysql启动以来,select语句执行的次数
cursor.execute('SHOW GLOBAL STATUS LIKE "Com_select";')
com_select=cursor.fetchone()[1]

# 自mysql启动以来,insert语句执行的次数
cursor.execute('SHOW GLOBAL STATUS LIKE "Com_insert";')
com_insert=cursor.fetchone()[1]

# 自mysql启动以来,update语句执行的次数
cursor.execute('SHOW GLOBAL STATUS LIKE "Com_update";')
com_update=cursor.fetchone()[1]

# 自mysql启动以来,delete语句执行的次数
cursor.execute('SHOW GLOBAL STATUS LIKE "Com_delete";')
com_delete=cursor.fetchone()[1]

# 自mysql启动以来,写入执行的次数 Writes = Com_insert + Com_update + Com_delete
writes=str(int(com_insert)+int(com_update)+int(com_delete))

# 获取所有实例名
cursor.execute("show DATABASES;")
instance = cursor.fetchall()

instance_list = []
get_json=[]
for row in instance:
    instance_list.append("%s"% row)
for row in instance_list:
    get_json.append({'mpoint': db_ip, 'ckbp': row, 'kpis': {'1null': questions,
                                                              '2null': com_select,
                                                              '3null': com_insert,
                                                              '4null': com_update,
                                                              '5null': com_delete,
                                                              'PM-00-03-06-00-17': writes,
                                                              }}

                   )
print json.dumps(get_json,sort_keys=True)