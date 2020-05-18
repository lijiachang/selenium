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
    print(separator.join([mpoint, ckbp, "APM-00-18-03-08-03", outputs("show global status like 'Connection_errors_max_connections';")]))  # 由 max_connections 限制导致的失败连接数

