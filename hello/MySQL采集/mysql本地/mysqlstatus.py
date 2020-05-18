# coding:utf-8

import subprocess
import sys

"""
by lijiachang, 2018.07.30
状态说明：
	0 正常
	1 服务名错误
	2 用户名密码错误
	3 IP端口错误
"""
try:
    ip = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    database = sys.argv[5]
    mpoint = "-".join([ip, port, database])
    ckbp = ""
except:
    print("Please usage:%s ip port user password servername" % sys.argv[0])
    sys.exit(0)


def output(sql):
    command = 'mysql -h ' + ip + ' -P ' + port + ' -u ' + user + ' -p' + password + ' ' + database + ' -e "' + sql + '"'
    # print(command)
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stderr = ps.stderr.read()
    stdout = ps.stdout.readlines()
    if "Unknown database" in stderr:
        print(separator.join([mpoint, ckbp, "PM-mysql-status", "1"]))
    elif "ERROR 1045 (28000)" in stderr:
        print(separator.join([mpoint, ckbp, "PM-mysql-status", "2"]))
    elif "ERROR 2003 (HY000)" in stderr or "ERROR 2005" in stderr:
        print(separator.join([mpoint, ckbp, "PM-mysql-status", "3"]))
    elif "ERROR" in stderr or "command not" in stderr:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, stderr))
        sys.exit(0)
    else:
        return stdout


if __name__ == '__main__':
    separator = "||"
    sql = "select @@basedir as basePath from dual;"
    results = output(sql)
    if results:
        if "basePath" in results[0]:
            print(separator.join([mpoint, ckbp, "PM-mysql-status", "0"]))
