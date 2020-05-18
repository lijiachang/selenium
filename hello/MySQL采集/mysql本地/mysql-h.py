# coding:utf-8

import subprocess
import sys

"""
使用mysql -h 命令远程采集信息， 
By 李家昌 最后修改于 2018.04.19
"""

try:
    ip = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
except:
    print("Please usage:%s ip port user password" % sys.argv[0])
    sys.exit(0)

# ip = "192.168.120.104"
# port = "3306"
# user = "root"
# password = "mysqlmima"
# mysql -h 192.168.120.104 -P 3306 -u root -APMysqlmima -e "select version();"

mpoint = "-".join([ip, port, "MySQL"])
ckbp = ""
separator = "||"
wrap = "\n"


def output(sql):
    command = 'mysql -h ' + ip + ' -P ' + port + ' -u '+ user + ' -p' + password + ' -e "' + sql + '"'
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout = ps.stdout.readlines()
    return stdout[1].strip()   # 原始格式：['version()\n', '5.7.18-log\n']


def outputs(sql):
    command = 'mysql -h ' + ip + ' -P ' + port + ' -u ' + user + ' -p' + password + ' -e "' + sql + '"'
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout = ps.stdout.readlines()
    return stdout[1].split("\t")[1].strip()  # 原始格式：['Variable_name\tValue\n', 'character_set_database\tutf8\n']


def multi_rows_outputs(sql):
    command = 'mysql -h ' + ip + ' -P ' + port + ' -u ' + user + ' -p' + password + ' -e "' + sql + '"'
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout = ps.stdout.readlines()
    return stdout  # 原始格式示例：['TABLE_SCHEMA\tIndexSize\tDataSize\n', 'agentdb\t16384\t294912\n', 'basedb\t8290304\t27508736\n']


if __name__ == '__main__':

    results = list()
    results.append(separator.join([mpoint, ckbp, "ACM-00-03-06-00-02", output("select version();")]))
    results.append(separator.join([mpoint, ckbp, "ACM-00-03-06-00-03", output("select @@basedir as basePath from dual")]))
    results.append(separator.join([mpoint, ckbp, "ACM-00-03-06-00-04", outputs("show variables like 'character_set_database'")]))
    results.append(separator.join([mpoint, ckbp, "ACM-00-03-06-00-10", outputs("show variables WHERE Variable_name = 'query_cache_size'")]))
    results.append(separator.join([mpoint, ckbp, "ACM-00-03-06-00-13", outputs("SHOW GLOBAL STATUS like 'Innodb_page_size'")]))
    results.append(separator.join([mpoint, ckbp, "ACM-00-03-06-00-14", outputs("show variables like 'innodb%pool_size%'")]))
    results.append(separator.join([mpoint, ckbp, "ACM-00-03-06-00-20", outputs("show variables like 'max_connections'")]))
    results.append(separator.join([mpoint, ckbp, "ACM-00-03-06-01-15", ip]))

    # 当前打开的连接的数量
    threads_connected = outputs("show global status like 'Threads_connected'")
    # 允许的最大连接
    max_connections = outputs("show variables like 'max_connections'")
    # 线程的使用率 (Threads_connected/max_connections)*100
    used_connections_pct = str((float(threads_connected) / float(max_connections)) * 100)

    # # 自mysql启动以来,insert,update,delete语句执行的次数
    # com_insert = outputs("SHOW GLOBAL STATUS LIKE 'Com_insert'")
    # com_update = outputs("SHOW GLOBAL STATUS LIKE 'Com_update'")
    # com_delete = outputs("SHOW GLOBAL STATUS LIKE 'Com_delete'")
    # # 自mysql启动以来,写入执行的次数 Writes = Com_insert + Com_update + Com_delete
    # writes = str(int(com_insert) + int(com_update) + int(com_delete))

    results.append(separator.join([mpoint, ckbp, "APM-00-03-06-00-11", threads_connected]))
    results.append(separator.join([mpoint, ckbp, "APM-00-03-06-00-12", outputs("show  global status like 'Threads_running'")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-03-06-00-17", outputs("show status like 'innodb_data_writes'")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-03-06-00-21", used_connections_pct]))
    results.append(separator.join([mpoint, ckbp, "APM-00-03-06-00-23", outputs("show global status like 'Aborted_connects'")]))
    results.append(separator.join([mpoint, ckbp, "APM-40-12-002-07", outputs("show global status like 'max_used_connections'")]))

    # 以下是 MySql数据库 信息：

    #   获取所有数据库名，去除第一行标题：
    db_names = multi_rows_outputs("select * from information_schema.schemata")[1:]
    for db_name in db_names:
        name = db_name.split("\t")[1]
        results.append(separator.join([mpoint, name, "ACM-00-03-06-01-01", name]))

    #  获取所有 已用数据库空间 ，去除第一行标题：
    db_names = multi_rows_outputs("SELECT TABLE_SCHEMA, SUM(index_length) AS 'IndexSize', sum(DATA_LENGTH) AS 'DataSize' FROM information_schema. TABLES GROUP BY TABLE_SCHEMA")[1:]
    for db_name in db_names:
        name = db_name.split("\t")[0]
        results.append(separator.join([mpoint, name, "APM-00-03-06-01-02", db_name.split("\t")[2].strip()]))

    #  获取所有 索引使用空间大小 ，去除第一行标题：
    for db_name in db_names:
        name = db_name.split("\t")[0]
        results.append(separator.join([mpoint, name, "APM-00-03-06-01-03", db_name.split("\t")[1]]))

    for result in results:
        print(result)
