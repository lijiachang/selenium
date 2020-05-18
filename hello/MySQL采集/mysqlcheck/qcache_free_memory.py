#!/usr/bin/env python
# coding=utf-8

import subprocess
import sys

try:
    hostip = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
except:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s ip port user password" % (sys.argv[0], sys.argv[0]))
    sys.exit(0)


###############rebuild a dict rule##########
class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


##################### run a shell in py script###############33
def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    stdos = [line.strip("\n") for line in stdo]
    return stdos


################ sql##############
if password == 'None':

    cmd = "mysql -h" + hostip + " -P" + port + " -u" + username + " -e'show status'"
else:
    cmd = "mysql -h" + hostip + " -P" + port + " -u" + username + " -p" + password + " -e'show status'"
# ps = subprocess.Popen(mysql -uroot -eshow status like 'Open_tables', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
res = outputs(cmd)
try:
    resl = ','.join(res[0].split())
except Exception, e:
    print('||%s||FM-PLUGIN-EXECUTE-FAILED||please check your sql or username/password.' % sys.argv[0])
    sys.exit(0)
names = [x for x in resl.split(',')]
li = []
for i in res:
    i = ','.join(i.split())
    li.append(i)
newli = []
if len(li) >= 2:
    for l in li[1:]:
        l = l.split(',')
        newli.append(l)
else:
    print('||%s||FM-PLUGIN-EXECUTE-FAILED||empty query.' % sys.argv[0])
    sys.exit()

L = [Dict(names, x) for x in newli]
######## monitor keys list#####################
keyl = ['Qcache_free_memory']

######### kpis dict###############

for i in L:
    if i['Variable_name'] in keyl:
        # dickpi[i['Variable_name']]=i['Value']
        res = hostip + '-mysql-' + port + '||""||APM-' + i['Variable_name'] + '||' + i['Value']
        print(res)

