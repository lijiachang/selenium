# coding=utf-8

import os
import sys

try:
    path = sys.argv[1]
    filename = sys.argv[2]
except:
    print("Please usage:%s Path Filename" % (sys.argv[0]))
    sys.exit(0)

path = path if path[-1] == "/" else path + "/"
if os.path.exists(path + filename):
    print("0")  # 文件存在返回0
else:
    print("1")  # 文件不存在返回1
