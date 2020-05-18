#!/usr/bin/env python

import sys, os
import subprocess


def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    stdos = [line.strip("\n") for line in stdo]
    return stdos


if len(sys.argv) != 3:
    print('need 2 paramters,insert dip and dport.')

    sys.exit()
else:
    dip = sys.argv[1]
    dport = sys.argv[2]
    cmd = 'netstat -ant|awk ' + "'" + '$5==' + '"' + dip + ':' + dport + '"' + "'" + '|wc -l'

    tcplisnum = outputs(cmd)

#Hip = outputs("ip add list|grep global|sed -n 1p|awk -F' ' '{print $2}'|awk -F'/' '{print $1}'")
Hip = ""

try:
    result = Hip + '||' + dip + '-' + dport + '-tcpliscount' + '||APM-LINUX-PORT-01-03||' + tcplisnum[0]
    print result
except Exception, e:
    print(e)
