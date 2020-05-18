# coding:utf-8

import subprocess
import sys

"""

By 李家昌 最后修改于 2018.0507
"""

try:
    ip = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
except:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s ip port user password" % (sys.argv[0], sys.argv[0]))
    sys.exit(0)

mpoint = "-".join([ip, port, "MySQL"])
ckbp = ""
separator = "||"
wrap = "\n"

def multi_rows_outputs(sql):
    command = 'mysql -h ' + ip + ' -P ' + port + ' -u ' + user + ' -p' + password + ' -e "' + sql + '"'
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stderr = ps.stderr.read()
    stdout = ps.stdout.readlines()
    if "ERROR" in stderr:
        print('||'+sys.argv[0]+'||FM-PLUGIN-EXECUTE-FAILED||' + stderr)
        sys.exit(0)
    return stdout


if __name__ == '__main__':
    #   获取所有数据库名，去除第一行标题：
    db_names = multi_rows_outputs("select * from information_schema.schemata")[1:]
    for db_name in db_names:
        ckbp = db_name.split("\t")[1]
        print(separator.join([mpoint, ckbp, "ACM-00-03-06-01-01", ckbp]))   # 数据库名
