#!/usr/bin/env python

# li 2019.06.17
import sys
import subprocess
import time


def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    stdos = [line.decode('utf-8').strip("\n") for line in stdo]
    return stdos


if len(sys.argv) != 2:
    print ("||%s||FM-PLUGIN-EXECUTE-FAILED||Usage:%s processname" % (sys.argv[0], sys.argv[0]))
else:
    proname = sys.argv[1]
    pids = "ps aux|awk \'{for(i=2;i<=NF;i++)printf $i \" \";printf\"\\n\"}\'|grep -v grep|grep -v '%s %s'|grep " % (
    sys.argv[0], sys.argv[1]) + proname + "|awk '{print $1}'"
    # print(pids)
    pro_ios = outputs(pids)
    # print pro_ios
    sum_ioin, sum_ioout = 0, 0
    for pro_io in pro_ios:
        ioin = outputs("cat /proc/%s/io|grep read_bytes|awk '{print $2}'" % pro_io)
        ioout = outputs("cat /proc/%s/io|grep -v cancelled_write_bytes|grep write_bytes|awk '{print $2}'" % pro_io)
        #print ioin, ioout
        if ioin:
            sum_ioin += int(ioin[0])
        if ioout:
            sum_ioout += int(ioout[0])
        time.sleep(0.01)
    # print "sum:", sum_ioin, sum_ioout
    try:
        print('||' + proname + '||PM-00-01-01-06-10||' + str(sum_ioin))
        print('||' + proname + '||PM-00-01-01-06-11||' + str(sum_ioout))
    except Exception as e:
        print('||' + proname + '||PM-00-01-01-06-10||' + e.message)
        print('||' + proname + '||PM-00-01-01-06-11||' + e.message)
