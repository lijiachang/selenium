#!/usr/bin/env python
# coding:utf-8

import sys,time
import subprocess


def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    stdos = [line.decode('utf-8').strip("\n") for line in stdo]
    return stdos


if len(sys.argv) != 3:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||error:need 2 paramters,dip and dport." % sys.argv[0])
    sys.exit(0)
else:
    dip=sys.argv[1]
    dport=sys.argv[2]

    if dip == "None" or dip.strip() == "":
        if dport == "None" or dport.strip() == "":
            cmd = 'netstat -an|grep ESTABLISHED|wc -l'  # 都是空
        else:
            cmd = 'netstat -an|grep ESTABLISHED|awk ' + "'" + '$5~' + '":' + dport + '"' + "'" + '|wc -l' # dip空 dport非空
    elif dport == "None" or dport.strip() == "":
        cmd = 'netstat -an|grep ESTABLISHED|awk ' + "'" + '$5~' + '"' + dip + ':"' + "'" + '|wc -l' # dip非空 dport空
    else :
        cmd = 'netstat -an|grep ESTABLISHED|awk ' + "'" + '$5==' + '"' + dip + ':' + dport + '"' + "'" + '|wc -l' # 都不是空

esbnum=outputs(cmd)
#Hip=outputs("ip add list|grep global|sed -n 1p|awk -F' ' '{print $2}'|awk -F'/' '{print $1}'")
Hip = ""
Hname=outputs("hostname")
try:
    result=Hip+'||'+dip+'-'+dport+'||APM-LINUX-CONNPORT-01-02||'+esbnum[0]
    print(result)
except Exception as e:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Error:%s." % (sys.argv[0], e))
    sys.exit(0)
