# coding:utf-8

import subprocess
import sys

"""
By   2018.08.01
"""

try:
    ip = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    database = sys.argv[5]
except:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s ip port user password servername" % (sys.argv[0], sys.argv[0]))
    sys.exit(0)

mpoint = "-".join([ip, port, database])
ckbp = ""
separator = "||"
wrap = "\n"

def multi_rows_outputs(sql):
    command = 'mysql -h ' + ip + ' -P ' + port + ' -u ' + user + ' -p' + password + ' -e "' + sql + '"'
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stderr = ps.stderr.read()
    stdout = ps.stdout.readlines()
    if b"ERROR" in stderr:
        print('||'+sys.argv[0]+'||FM-PLUGIN-EXECUTE-FAILED||' + stderr)
        sys.exit(0)
    return stdout


if __name__ == '__main__':
    #  获取所有 已用数据库空间 ，去除第一行标题：
    db_names = multi_rows_outputs("SELECT TABLE_SCHEMA, SUM(index_length) AS 'IndexSize', sum(DATA_LENGTH) AS 'DataSize' FROM information_schema. TABLES GROUP BY TABLE_SCHEMA")[1:]
    for db_name in db_names:
        ckbp = db_name.decode('utf-8').split("\t")[0]
        print(separator.join([mpoint, ckbp, "APM-00-03-06-01-02", db_name.decode('utf-8').split("\t")[2].strip()]))  # 已用数据库空间
