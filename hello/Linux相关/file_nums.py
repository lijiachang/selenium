# coding:utf-8
# 2019.01.29
# 文件个数，支持通配符

import os
import sys
import subprocess


if len(sys.argv) < 2:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please insert the full path of the file." % sys.argv[0])
    sys.exit(0)
else:
    path = sys.argv[1]

dir = os.path.dirname(path)
if not os.path.isdir(dir):
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Path %s not exists." % (sys.argv[0], dir))
    sys.exit(0)


def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stderr = ps.stderr.read()
    stdout = ps.stdout.readlines()
    if stderr:
        print("||%s||FM-PLUGIN-EXECUTE-FAILED||%s" % (sys.argv[0], stderr.strip()))
        sys.exit(0)
    else:
        return stdout


cmd = "ls " + path + "|wc -l"
#print(cmd)

file_nums = outputs(cmd)

Hip = ""

try:
    result = Hip + '||' + path + '||PM-LINUX-LOG-01-05||' + file_nums[0].strip()
    print(result)
except Exception as e:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Error:%s." % (sys.argv[0], e))
    sys.exit(0)
