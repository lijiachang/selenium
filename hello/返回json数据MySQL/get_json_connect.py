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

# 自mysql启动以来，试图连接到(不管是否成功)MySQL服务器的连接数
cursor.execute("show global status like 'Connections';")
connections = cursor.fetchone()[1]

# 自mysql启动以来，试图连接到MySQL服务器而失败的连接数
cursor.execute("show global status like 'Aborted_connects';")
aborted_connects = cursor.fetchone()[1]

# 自mysql启动以来,已经同时使用的连接的最大数量。
cursor.execute("show global status like 'max_used_connections';")
max_used_connections = cursor.fetchone()[1]

# 允许的最大连接
cursor.execute("show variables like 'max_connections';")
max_connections = cursor.fetchone()[1]

# 当前打开的连接的数量
cursor.execute("show  global status like 'Threads_connected';")
threads_connected = cursor.fetchone()[1]

# 剩余可用的连接数
free_connects = str(int(max_connections) - int(threads_connected))

# 线程的使用率 (Threads_connected/max_connections)*100
used_connections_pct = str((float(threads_connected) / float(max_connections)) * 100)

# 当前运行的连接
cursor.execute("show  global status like 'Threads_running';")
threads_running = cursor.fetchone()[1]

# 由服务器错误导致的失败连接数(主机内存不足或是无法开启新的进程)
cursor.execute("show global status like 'Connection_errors_internal';")
connection_errors_internal = cursor.fetchone()[1]

# 由 max_connections 限制导致的失败连接数
cursor.execute(" show  global status like 'Connection_errors_max_connections';")
connection_errors_max_connections = cursor.fetchone()[1]

# 获取所有实例名
cursor.execute("show DATABASES;")
instance = cursor.fetchall()

instance_list = []
get_json=[]
for row in instance:
    instance_list.append("%s"% row)
for row in instance_list:
    get_json.append({'mpoint': db_ip, 'ckbp': row, 'kpis': {'1null': connections,
                                                              'PM-00-03-06-00-23': aborted_connects,
                                                              'PM-40-12-002-07': max_used_connections,
                                                              'CM-00-03-06-00-20': max_connections,
                                                              'PM-00-03-06-00-11': threads_connected,
                                                              '2null': free_connects,
                                                              'PM-00-03-06-00-21': used_connections_pct,
                                                              'PM-00-03-06-00-12': threads_running,
                                                              '3null': connection_errors_internal,
                                                              }}

                   )
print json.dumps(get_json,sort_keys=True)