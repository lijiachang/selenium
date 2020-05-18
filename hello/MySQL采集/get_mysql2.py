# /bin/usr/python
# coding:utf-8

# 需要安装模块MySQLdb
# 本脚本采集的是 ：没有输出KPI，有SQL语句能查到的监控指标

import MySQLdb
import sys

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
#
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

results = separator.join([mpoint, ckbp, "PM-00-18-03-08-01", query("show global status like 'Connections';")])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-02", query("show global status like 'Connection_errors_internal';")])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-03", query("show global status like 'Connection_errors_max_connections';")])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-04", query("SHOW GLOBAL STATUS LIKE 'Questions';")])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-05", query("SHOW GLOBAL STATUS LIKE 'Com_select';")])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-06", query("SHOW GLOBAL STATUS LIKE 'Com_insert';")])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-07", query("SHOW GLOBAL STATUS LIKE 'Com_update';")])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-08", query("SHOW GLOBAL STATUS LIKE 'Com_delete';")])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-09", query("SHOW GLOBAL STATUS LIKE 'Slow_queries';")])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-10", query("SHOW GLOBAL STATUS LIKE 'Innodb_row_lock_waits';")])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-11", query("show global status like 'Innodb_buffer_pool_pages_total';")])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-12", query("show global status like 'innodb_page_size';")])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-13", query("show variables like 'Innodb_buffer_pool_size';")])])

# MyISAM缓冲池使用率key_blocks_usage = Key_blocks_used/(Key_blocks_unused +Key_blocks_used)
Key_blocks_used = query("show global status like 'Key_blocks_used';")
Key_blocks_unused = query("show global status like 'Key_blocks_unused';")
key_blocks_usage = float(Key_blocks_used)/(float(Key_blocks_unused) + float(Key_blocks_used)) * 100
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-14", Key_blocks_unused])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-15", Key_blocks_used])])
results = wrap.join([results,separator.join([mpoint, ckbp, "PM-00-18-03-08-16", str(key_blocks_usage)])])

conn.close()
print(results)
