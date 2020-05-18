#!/usr/bin/env python
# -*-coding:utf-8 -*-

import sys, time
import subprocess
import platform
import os


def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    stdos = [line.strip("\n") for line in stdo]
    return stdos


if len(sys.argv) != 3:
    print('error:need 2 paramters,dip and ping count')
    sys.exit()

#Hip = outputs("ip add list|grep global|sed -n 1p|awk -F' ' '{print $2}'|awk -F'/' '{print $1}'")
Hname = outputs("hostname")
curip = ""

def pinger(ip, count):
    if platform.system() == "Linux":

        cmd = "ping -c %s %s" % (count, ip)

        outfile = "/dev/null"
    elif platform.system() == "Windows":

        cmd = "ping -n %s %s" % (count, ip)

        outfile = "ping.temp"
    ret = subprocess.call(cmd, shell=True, stdout=open(outfile, 'w'), stderr=subprocess.STDOUT)
    if ret == 0:
        result = curip + '||' + ip + '-ICMPstatus' + '||APM-LINUX-PORT-01-05||0'

        print result
    else:
        result = curip + '||' + ip + '-ICMPstatus' + '||APM-LINUX-PORT-01-05||1'

        print result


if __name__ == "__main__":
    ip = sys.argv[1]
    count = sys.argv[2]
    pinger(ip, count)
