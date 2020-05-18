#!/usr/bin/env python
import time
import sys,os
import subprocess


def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    stdos = [line.decode('utf-8').strip("\n") for line in stdo]
    return stdos

cpucount=float(outputs('cat /proc/cpuinfo|grep processor|wc -l')[0])
if len(sys.argv)!=2:
    print ("||%s||FM-PLUGIN-EXECUTE-FAILED||Usage:%s processname" % (sys.argv[0], sys.argv[0]))
else:
    proname=sys.argv[1]
    exist_pro="ps aux|awk \'{for(i=2;i<=NF;i++)printf $i \" \";printf\"\\n\"}\'|grep -v grep|grep "+proname+"|wc -l"
    proexist=outputs(exist_pro)
    com_pro_cpu="ps aux|awk \'{for(i=2;i<=NF;i++)printf $i \" \";printf\"\\n\"}\'|grep -v grep|grep "+proname+"|awk \'BEGIN{total=0}{total+=$2}END{print total}\'"
    com_pro_mem="ps aux|awk \'{for(i=2;i<=NF;i++)printf $i \" \";printf\"\\n\"}\'|grep -v grep|grep "+proname+"|awk \'BEGIN{total=0}{total+=$3}END{print total}\'"
    if proexist[0]=='1':
        print("||%s||FM-PLUGIN-EXECUTE-FAILED||no such process found,please check your process name." % (sys.argv[1]))
        sys.exit(0)
    else:
        pro_cpu=outputs(com_pro_cpu)
        pro_mem=outputs(com_pro_mem)
        try:
            print('||'+proname+'||PM-00-01-01-06-09||'+str(round(float(pro_cpu[0])/float(cpucount),5)))
        except Exception:
            print('||'+proname+'||PM-00-01-01-06-09||'+e.message)
        try:
            print('||'+proname+'||PM-00-01-01-06-01||'+str(pro_mem[0]))
        except Exception:
            print('||'+proname+'||PM-00-01-01-06-01||'+e.message)
