# li coding=utf=8 li
# 2018.08.14
import subprocess
import sys

try:
    process = sys.argv[1]
except:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s ProcessName" % (sys.argv[0], sys.argv[0]))
    sys.exit(0)

cmd = "tasklist|findstr " + process
ps = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

if ps.stdout:
    stdout = ps.stdout.readlines()
    result = '||' + process + '||' + 'APM-00-01-01-06-02||' + str(len(stdout))
    print(result)
    # for line in stdout:
    # print(line)
    # number = number + 1 if line[:26].strip() == "services.exe" else number + 0
elif ps.stderr:
    print('||' + sys.argv[0] + '||FM-PLUGIN-EXECUTE-FAILED||' + ps.stderr.read())
else:
    print('||' + sys.argv[0] + '||FM-PLUGIN-EXECUTE-FAILED||No result')
