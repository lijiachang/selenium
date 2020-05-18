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
    #  获取所有 索引使用空间大小 ，去除第一行标题：
    db_names = multi_rows_outputs("SELECT TABLE_SCHEMA, SUM(index_length) AS 'IndexSize', sum(DATA_LENGTH) AS 'DataSize' FROM information_schema. TABLES GROUP BY TABLE_SCHEMA")[1:]
    for db_name in db_names:
        name = db_name.decode('utf-8').split("\t")[0]
        print(separator.join([mpoint, name, "APM-00-03-06-01-03", db_name.decode('utf-8').split("\t")[1]]))  # 索引使用空间大小
