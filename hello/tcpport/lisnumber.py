#!/usr/bin/env python

import sys, os
import subprocess


def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    stdos = [line.strip("\n") for line in stdo]
    return stdos


if len(sys.argv) != 2:
    print("need 1 paramter,insert one port number.")
    sys.exit()
portnum = sys.argv[1]

cmd = 'lsof -i:%s|grep LISTEN|wc -l' % portnum

lisnum = outputs(cmd)

#Hip = outputs("ip add list|grep global|sed -n 1p|awk -F' ' '{print $2}'|awk -F'/' '{print $1}'")
Hip = ""
try:
    result = Hip + '||' + portnum + '-liscount' + '||APM-LINUX-PORT-01-01||' + lisnum[0]
    print result
except Exception, e:
    print(e)
