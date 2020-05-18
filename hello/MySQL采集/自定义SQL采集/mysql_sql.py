# coding:utf-8

import subprocess
import sys

"""
读取本地文件sql.txt ，执行单条SQL语句，返回执行结果
使用mysql -h 命令远程采集信息， By 李家昌 最后修改于 2018.04.18
"""


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

    try:
        ip = sys.argv[1]
        port = sys.argv[2]
        user = sys.argv[3]
        password = sys.argv[4]
    except:
        print("Please usage:%s ip port user password db" % sys.argv[0])
        sys.exit(0)

    mpoint = "-".join([ip, port, "MySQL"])
    ckbp = ""
    separator = "||"
    wrap = "\n"


