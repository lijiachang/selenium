# coding:utf-8


import os
import sys
import subprocess

if len(sys.argv) < 3:
    print("输入：RPM包名  挂载目录")
    sys.exit(0)
else:
    path = sys.argv[1]

dir = os.path.dirname(path)
if not os.path.isdir(dir):
    print("Path %s not exists." % dir)
    sys.exit(0)


def check_and_ensure_rpmpackage(RPM, PATH):
    cmd = "rpm -qa|grep %s" % RPM
    ps = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stderr = ps.stderr.read()
    stdout = ps.stdout.readlines()
    if stderr:
        print("unknown error when installing %s" % RPM)
    if stdout:
        print("%s already installd" % RPM)
    else:
        # 开始安装
        # 接下来思路：1 find命令先找到挂载目录中是否含有 所需包 2 rpm -ivh 包名，安装包
        pass

