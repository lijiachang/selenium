#!/usr/bin/env python
# coding=utf-8

import sys,time
import subprocess


def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    stdos = [line.strip("\n") for line in stdo]
    return stdos


if len(sys.argv) == 3:
    dip = sys.argv[1]
    dport = sys.argv[2]
    cmd='netstat -an|grep ESTABLISHED|awk '+"'"+'$5=='+'"'+dip+':'+dport+'"'+"'"+'|wc -l'
elif len(sys.argv) == 2:
    dip = sys.argv[1]
    dport = ""
    cmd = 'netstat -an|grep ESTABLISHED|awk ' + "'" + '$5~' + '"' + dip + ':"' + "'" + '|wc -l'
elif len(sys.argv) == 1:
    cmd = 'netstat -an|grep ESTABLISHED|wc -l'
else:
    print("Up to two parameters!")
    sys.exit(0)

esbnum=outputs(cmd)

Hip = ""
Hname=outputs("hostname")
try:
    result=Hip+'||'+dip+'-'+dport+'-esbcount'+'||APM-LINUX-PORT-01-02||'+esbnum[0]
    print result
except Exception,e:
    print('Error:%s.' %e)


