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


def outputs(sql):
    command = 'mysql -h ' + ip + ' -P ' + port + ' -u ' + user + ' -p' + password + ' ' + database + ' -e "' + sql + '"'
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stderr = ps.stderr.read()
    stdout = ps.stdout.readlines()
    if b"ERROR" in stderr:
        print('||'+sys.argv[0]+'||FM-PLUGIN-EXECUTE-FAILED||' + stderr)
        sys.exit(0)
    return stdout[1].decode('utf-8').split("\t")[1].strip()


if __name__ == '__main__':
    # 当前打开的连接的数量
    threads_connected = outputs("show global status like 'Threads_connected'")
    # 允许的最大连接
    max_connections = outputs("show variables like 'max_connections'")
    # 线程的使用率 (Threads_connected/max_connections)*100
    used_connections_pct = str((float(threads_connected) / float(max_connections)) * 100)

    print(separator.join([mpoint, ckbp, "APM-00-03-06-00-21", used_connections_pct]))  # 线程的使用率

