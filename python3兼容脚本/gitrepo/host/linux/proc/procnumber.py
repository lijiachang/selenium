#!/usr/bin/env python
import time
import sys, os
import subprocess


def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    stdos = [line.decode('utf-8').strip("\n") for line in stdo]
    return stdos


if len(sys.argv) != 2:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||error,use processname" % sys.argv[0])
    sys.exit(0)
else:
    proname = sys.argv[1]
    #ip = outputs("ip add list|grep global|sed -n 1p|awk -F' ' '{print $2}'|awk -F'/' '{print $1}'")
    dctime = int(round(time.time() * 1000))

    dictsp = {}
    dictp = {}
    #com_pro = "ps aux|awk \'$11~\"" + proname + "\"\'|grep -v " + sys.argv[0] + "|wc -l"
    com_pro = "ps aux|awk \'{for(i=11;i<=NF;i++)printf $i \" \";printf\"\\n\"}\'|grep -v "+sys.argv[0]+"|grep "+proname+"|grep -v grep|wc -l"

    res = outputs(com_pro)

    if len(res) == 0:
        print("||%s||FM-PLUGIN-EXECUTE-FAILED||Result is empty. this command get nothing" % sys.argv[0])
    else:
        result = '||' + proname + '||' + 'APM-00-01-01-06-02||' + res[0]
        print(result)
    
