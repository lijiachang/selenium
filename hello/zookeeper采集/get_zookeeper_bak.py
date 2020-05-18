#!/usr/bin/python
# coding:utf-8

# 仅支持Linux本地运行
import commands

# # 获取方法1
# mntr1 = os.popen('echo mntr | nc 192.168.95.114 52181')
# print mntr1.read()
# # 获取方法2
# mntr = commands.getoutput('echo mntr | nc 192.168.95.114 52181')
# print mntr


mntr = commands.getoutput('echo mntr | nc 192.168.95.114 52181')
conf = commands.getoutput('echo conf | nc 192.168.95.114 52181')
cons = commands.getoutput('echo cons | nc 192.168.95.114 52181')
envi = commands.getoutput('echo envi | nc 192.168.95.114 52181')
srvr = commands.getoutput('echo srvr | nc 192.168.95.114 52181')


# 从mntr命令中获取返回值
## 将str以换行符分割成list，.replace先把逗号去掉，因为逗号也被分割？
def getmntr(mntr, attribute_name):
    attributes = mntr.replace(',', '').split('\n')
    for attribute in attributes:
        if (attribute_name == attribute.split('\t')[0]):
            return attribute.split('\t')[1]


print getmntr(mntr, 'zk_version')


# 从conf命令中获取返回值
def getconf(mntr, attribute_name):
    attributes = mntr.split('\n')
    for attribute in attributes:
        if (attribute_name == attribute.split('=')[0]):
            return attribute.split('=')[1]


print getconf(conf, 'dataDir')


# 从srvr命令中获取返回值
def getsrvr(mntr, attribute_name):
    attributes = mntr.replace(',', '').split('\n')
    for attribute in attributes:
        if (attribute_name == attribute.split(':')[0]):
            return attribute.split(':')[1]


print getsrvr(srvr, 'Sent')


# 从envi命令中获取返回值
def getenvi(mntr, attribute_name):
    attributes = mntr.replace(',', '').split('\n')
    del attributes[0]  # 删除第一行的 Environment:
    for attribute in attributes:
        if (attribute_name == attribute.split('=')[0]):
            return attribute.split('=')[1]


print getenvi(envi, 'java.home')

results = str()
results = "".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-000-01||" + getconf(conf, "clientPort")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-000-02||" + getconf(conf, "tickTime")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-000-03||" + getconf(conf, "minSessionTimeout")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-000-04||" + getconf(conf, "maxSessionTimeout")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-000-05||" + getconf(conf, "syncLimit")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-000-06||" + getconf(conf, "maxClientCnxns")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-000-09||" + getconf(conf, "serverId")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-000-11||" + getmntr(mntr, "zk_version")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-000-12||" + getenvi(envi, "host.name")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-000-13||" + getenvi(envi, "os.name")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-001-10||" + getmntr(mntr, "zk_server_state")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||PM-40-10-000-08||" +"state!!" ])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-001-02||" + getmntr(mntr, "zk_packets_received")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-001-03||" + getmntr(mntr, "zk_packets_sent")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-001-04||" + getmntr(mntr, "zk_num_alive_connections")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-001-05||" + getmntr(mntr, "zk_avg_latency")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-001-06||" + getmntr(mntr, "zk_max_latency")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-001-07||" + getmntr(mntr, "zk_min_latency")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-001-08||" + getmntr(mntr, "zk_znode_count")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-001-09||" + getmntr(mntr, "zk_outstanding_requests")])
results = "\n".join([results, "192.168.95.114-52181-zookeeper||null||CM-40-10-001-11||" + getmntr(mntr, "zk_watch_count")])

print results
