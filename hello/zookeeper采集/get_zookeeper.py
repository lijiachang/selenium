#!/usr/bin/python
# coding:utf-8
# 2019.06.25

import sys
import commands
import socket

localIP = socket.gethostbyname(socket.gethostname())  # Linux获取本地ip

if len(sys.argv) != 3:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s ip port [password]" % (sys.argv[0], sys.argv[0]))
    sys.exit(0)
else:
    zk_ip = sys.argv[1]
    zk_port = sys.argv[2]

mntr = commands.getoutput('echo mntr | nc ' + zk_ip + ' ' + zk_port)
conf = commands.getoutput('echo conf | nc ' + zk_ip + ' ' + zk_port)
cons = commands.getoutput('echo cons | nc ' + zk_ip + ' ' + zk_port)
envi = commands.getoutput('echo envi | nc ' + zk_ip + ' ' + zk_port)
srvr = commands.getoutput('echo srvr | nc ' + zk_ip + ' ' + zk_port)


# 从mntr命令中获取返回值
def getmntr(res, attribute_name):
    if not res:
        print("||%s||FM-PLUGIN-EXECUTE-FAILED||No data" % (sys.argv[0]))
        sys.exit(0)
    attributes = res.replace(',', '').split('\n')
    for attribute in attributes:
        if (attribute_name == attribute.split('\t')[0]):
            return attribute.split('\t')[1]


# 从conf命令中获取返回值
def getconf(res, attribute_name):
    if not res:
        print("||%s||FM-PLUGIN-EXECUTE-FAILED||No data" % (sys.argv[0]))
        sys.exit(0)
    attributes = res.split('\n')
    for attribute in attributes:
        if (attribute_name == attribute.split('=')[0]):
            return attribute.split('=')[1]


# 从srvr命令中获取返回值
def getsrvr(res, attribute_name):
    if not res:
        print("||%s||FM-PLUGIN-EXECUTE-FAILED||No data" % (sys.argv[0]))
        sys.exit(0)
    attributes = res.replace(',', '').split('\n')
    for attribute in attributes:
        if (attribute_name == attribute.split(':')[0]):
            return attribute.split(':')[1]


# 从envi命令中获取返回值
def getenvi(res, attribute_name):
    if not res:
        print("||%s||FM-PLUGIN-EXECUTE-FAILED||No data" % (sys.argv[0]))
        sys.exit(0)
    attributes = res.replace(',', '').split('\n')
    del attributes[0]  # 删除第一行的 Environment:
    for attribute in attributes:
        if (attribute_name == attribute.split('=')[0]):
            return attribute.split('=')[1]


results = str()
results = "".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-000-01||" + getconf(conf, "clientPort")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-000-02||" + getconf(conf, "tickTime")])
results = "\n".join(
    [results,
     zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-000-03||" + getconf(conf, "minSessionTimeout")])
results = "\n".join(
    [results,
     zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-000-04||" + getconf(conf, "maxSessionTimeout")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-000-05||" + getconf(conf, "syncLimit")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-000-06||" + getconf(conf, "maxClientCnxns")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-000-09||" + getconf(conf, "serverId")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-000-11||" + getmntr(mntr, "zk_version")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-000-12||" + getenvi(envi, "host.name")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-000-13||" + getenvi(envi, "os.name")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-001-10||" + getmntr(mntr, "zk_server_state")])
results = "\n".join([results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||PM-40-10-000-08||" + "0"])
results = "\n".join(
    [results,
     zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-001-02||" + getmntr(mntr, "zk_packets_received")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-001-03||" + getmntr(mntr, "zk_packets_sent")])
results = "\n".join(
    [results,
     zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-001-04||" + getmntr(mntr, "zk_num_alive_connections")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-001-05||" + getmntr(mntr, "zk_avg_latency")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-001-06||" + getmntr(mntr, "zk_max_latency")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-001-07||" + getmntr(mntr, "zk_min_latency")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-001-08||" + getmntr(mntr, "zk_znode_count")])
results = "\n".join(
    [results,
     zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-001-09||" + getmntr(mntr, "zk_outstanding_requests")])
results = "\n".join(
    [results, zk_ip + "-" + zk_port + "-zookeeper||ResZooKeeper||CM-40-10-001-11||" + getmntr(mntr, "zk_watch_count")])

print results
