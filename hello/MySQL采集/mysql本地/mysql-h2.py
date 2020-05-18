# coding:utf-8

import subprocess
import sys

"""
使用mysql -h 命令远程采集信息， By 李家昌 最后修改于 2018.04.13
本脚本采集的是 ：没有输出KPI（KPI信息在NMS的指标模型中找不到），有SQL语句能查到的监控指标
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


if __name__ == '__main__':

    results = list()
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-01", outputs("show global status like 'Connections';")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-02", outputs("show global status like 'Connection_errors_internal';")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-03", outputs("show global status like 'Connection_errors_max_connections';")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-04", outputs("SHOW GLOBAL STATUS LIKE 'Questions';")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-05", outputs("SHOW GLOBAL STATUS LIKE 'Com_select';")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-06", outputs("SHOW GLOBAL STATUS LIKE 'Com_insert';")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-07", outputs("SHOW GLOBAL STATUS LIKE 'Com_update';")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-08", outputs("SHOW GLOBAL STATUS LIKE 'Com_delete';")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-09", outputs("SHOW GLOBAL STATUS LIKE 'Slow_queries';")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-10", outputs("SHOW GLOBAL STATUS LIKE 'Innodb_row_lock_waits';")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-11", outputs("show global status like 'Innodb_buffer_pool_pages_total';")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-12", outputs("show global status like 'innodb_page_size';")]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-13", outputs("show variables like 'Innodb_buffer_pool_size';")]))

    # MyISAM缓冲池使用率key_blocks_usage = Key_blocks_used/(Key_blocks_unused +Key_blocks_used)
    Key_blocks_used = outputs("show global status like 'Key_blocks_used';")
    Key_blocks_unused = outputs("show global status like 'Key_blocks_unused';")
    key_blocks_usage = float(Key_blocks_used) / (float(Key_blocks_unused) + float(Key_blocks_used)) * 100

    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-14", Key_blocks_unused]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-15", Key_blocks_used]))
    results.append(separator.join([mpoint, ckbp, "APM-00-18-03-08-16", str(key_blocks_usage)]))

    for result in results:
        print(result)
