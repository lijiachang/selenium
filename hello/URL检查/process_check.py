# coding=utf-8

import subprocess
import sys

# 检查进程是否存在 2018.08.10
try:
    process_name = sys.argv[1]
except:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s process_name" % (sys.argv[0], sys.argv[0]))
    sys.exit(0)


command = "ps -e | grep " + process_name + " | grep -v 'grep'|awk '{print $4}'"
ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
stderr = ps.stderr.read()
stdout = ps.stdout.readlines()

num = 0
if stdout:
    for r in stdout:
        num += 1 if process_name == r.strip() else num + 0
    print(num)
    if num > 0:
        print("||||PM-Process-status||" + "0")
    else:
        print("||||PM-Process-status||" + "1")

else:
    print("||||PM-Process-status||" + "1")

