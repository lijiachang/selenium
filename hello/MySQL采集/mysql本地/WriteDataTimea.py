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


def outputs(sql):
    command = 'mysql -h ' + ip + ' -P ' + port + ' -u '+ user + ' -p' + password + ' -e "' + sql + '"'
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stderr = ps.stderr.read()
    stdout = ps.stdout.readlines()
    if "ERROR" in stderr:
        print('||'+sys.argv[0]+'||FM-PLUGIN-EXECUTE-FAILED||' + stderr)
        sys.exit(0)
    return stdout[1].split("\t")[1].strip()


if __name__ == '__main__':
    print(separator.join([mpoint, ckbp, "APM-00-03-06-00-17", outputs("show status like 'innodb_data_writes'")]))  # 写数据次数

