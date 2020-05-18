# /bin/usr/python
# coding:utf-8

# 需要安装模块MySQLdb  （python2.6 以下需要安装simplejson）
import MySQLdb
import sys

try:
    import json
except ImportError:
    import simplejson as json

try:
    ip = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    db = sys.argv[5]
except:
    print("Please usage:%s ip port user password db" % sys.argv[0])
    sys.exit(0)

# ip = "192.168.120.104"
# port = "3306"
# conn = MySQLdb.connect(host="192.168.120.104", port=3306, user="root", passwd="mysqlmima", db="basedb")

conn = MySQLdb.connect(host=ip, port=int(port), user=user, passwd=password, db=db)
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)


def query(sql):
    cursor.execute(sql)
    data = cursor.fetchone()
    return data.values()[0]


mpoint = "-".join([ip, port, "MySQL"])
ckbp = "ResMySQL"
separator = "||"
wrap = "\n"

results = separator.join([mpoint, ckbp, "CM-00-03-06-00-02", query("select version();")])
results = wrap.join(
    [results, separator.join([mpoint, ckbp, "CM-00-03-06-00-03", query("select @@basedir as basePath from dual")])])
results = wrap.join([results, separator.join(
    [mpoint, ckbp, "CM-00-03-06-00-04", query("show variables like 'character_set_database'")])])
results = wrap.join([results, separator.join(
    [mpoint, ckbp, "CM-00-03-06-00-10", query("show variables WHERE Variable_name = 'query_cache_size'")])])
results = wrap.join(
    [results, separator.join([mpoint, ckbp, "CM-00-03-06-00-13", query("SHOW GLOBAL STATUS like 'Innodb_page_size'")])])
results = wrap.join(
    [results, separator.join([mpoint, ckbp, "CM-00-03-06-00-14", query("show variables like 'innodb%pool_size%'")])])
results = wrap.join(
    [results, separator.join([mpoint, ckbp, "CM-00-03-06-00-20", query("show variables like 'max_connections'")])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-00-03-06-01-15", ip])])

# 连接

# 当前打开的连接的数量
threads_connected = query("show global status like 'Threads_connected'")
# 允许的最大连接
max_connections = query("show variables like 'max_connections'")
# 线程的使用率 (Threads_connected/max_connections)*100
used_connections_pct = str((float(threads_connected) / float(max_connections)) * 100)

# 自mysql启动以来,insert,update,delete语句执行的次数
com_insert = query("SHOW GLOBAL STATUS LIKE 'Com_insert'")
com_update = query("SHOW GLOBAL STATUS LIKE 'Com_update'")
com_delete = query("SHOW GLOBAL STATUS LIKE 'Com_delete'")
# 自mysql启动以来,写入执行的次数 Writes = Com_insert + Com_update + Com_delete
writes = str(int(com_insert) + int(com_update) + int(com_delete))

results = wrap.join(
    [results, separator.join([mpoint, ckbp, "PM-00-03-06-00-23", query("show global status like 'Aborted_connects'")])])
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-00-03-06-00-11", threads_connected])])
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-00-03-06-00-21", used_connections_pct])])
results = wrap.join(
    [results, separator.join([mpoint, ckbp, "PM-00-03-06-00-12", query("show  global status like 'Threads_running'")])])
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-00-03-06-00-17", writes])])
results = wrap.join([results, separator.join(
    [mpoint, ckbp, "PM-40-12-002-07", query("show global status like 'max_used_connections'")])])

conn.close()
print(results)
