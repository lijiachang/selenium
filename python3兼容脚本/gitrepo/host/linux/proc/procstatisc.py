#!/usr/bin/env python

import sys,os
import subprocess


def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    stdos = [line.decode('utf-8').strip("\n") for line in stdo]
    return stdos

#ip = outputs("ip add list|grep global|sed -n 1p|awk -F' ' '{print $2}'|awk -F'/' '{print $1}'")

dictsp={}
dictp={}
com_pro_wait = "ps aux|awk '$8=="+'"'+"S"+'"'+"'|wc -l"

com_pro_dead = "ps aux|awk '$8=="+'"'+"Z"+'"'+"'|wc -l"

com_pro_active = "ps aux|awk '$8=="+'"'+"R"+'"'+"'|wc -l"

com_pro_user = "ps aux|awk '$1!="+'"'+"root"+'"'+"'|wc -l"

reswait=outputs(com_pro_wait)
resdead=outputs(com_pro_dead)
resactive=outputs(com_pro_active)
resuser=outputs(com_pro_user)
try:
    a='||'+'""'+'||'+'APM-00-01-01-06-05'+'||'+reswait[0]
    b='||'+'""'+'||'+'APM-00-01-01-06-06'+'||'+resdead[0]
    c='||'+'""'+'||'+'APM-00-01-01-06-08'+'||'+resactive[0]
    d='||'+'""'+'||'+'APM-00-01-01-06-07'+'||'+resuser[0]
    print(a+'\n'+b+'\n'+c+'\n'+d)
except Exception:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Error:%s." % (sys.argv[0], sys.argv[0]))

