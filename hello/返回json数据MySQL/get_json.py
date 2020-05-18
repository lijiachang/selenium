# /bin/usr/python
# coding:utf-8

# 需要安装模块MySQLdb  （python2.6 以下需要安装simplejson）
import socket
import MySQLdb

try:
    import json
except ImportError:
    import simplejson as json

localIP = socket.gethostbyname(socket.gethostname())  # Linux获取本地ip
# print localIP

# mpoint = {'mpoint': localIP}
db = MySQLdb.connect(host="192.168.120.104", user="root", passwd="mysqlmima", db="basedb", port=3306)
cursor = db.cursor()
cursor.execute('show DATABASES;')

instance = cursor.fetchall()
# print instance

instance_list = []
for row in instance:
    instance_list.append('%s' % row)

# print instance_list

# ckbp = {'ckbp': instance_list[0]}

# print json.dumps([mpoint, ckbp])

# MySQL版本
cursor.execute('select version();')
version = '%s' % cursor.fetchone()

# kpis = {'kpis': {'CM-00-03-06-00-02': version}}

# 安装目录
cursor.execute('select @@basedir as basePath from dual')
PATH = '%s' % cursor.fetchone()

# 数据库当前字符集
cursor.execute("show variables like 'character_set_database'")
NLS = cursor.fetchone()[1]

# 查询缓存空间大小
cursor.execute("show variables WHERE Variable_name = 'query_cache_size'")
QueryCacheSize = cursor.fetchone()[1]

# Innodb页大小
cursor.execute("SHOW GLOBAL STATUS like 'Innodb_page_size'")
InnodbPage = cursor.fetchone()[1]

# Innodb缓存池大小
# InnoDB_buffer_pool_size:用于设置InnoDB缓存池(InnoDB_buffer_pool)的大小。
cursor.execute("show variables like 'innodb%pool_size%'")
InnodbPool = cursor.fetchone()[1]

# 最大允许连接数
cursor.execute("show variables like 'max_connections'")
MaxConnections = cursor.fetchone()[1]

# print json.dumps([{'mpoint': localIP,'ckbp': instance_list[0],'kpis': {'CM-00-03-06-00-02': version}}])
json_son = []
for row in instance_list:
    json_son.append({'mpoint': localIP, 'ckbp': row, 'kpis': {'CM-00-03-06-00-02': version,
                                                              'CM-00-03-06-00-03': PATH,
                                                              'CM-00-03-06-00-04': NLS,
                                                              'CM-00-03-06-00-06': 'DESCR',
                                                              'CM-00-03-06-00-10': QueryCacheSize,
                                                              'CM-00-03-06-00-13': InnodbPage,
                                                              'CM-00-03-06-00-14': InnodbPool,
                                                              'CM-00-03-06-00-20': MaxConnections,
                                                              'CM-00-03-06-01-15': localIP,
                                                              }})

print json.dumps(json_son, sort_keys=True)
