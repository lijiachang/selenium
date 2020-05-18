#!/usr/bin/python
# coding:utf-8

import urllib2
import json
import sys

results = str()  # 总的返回数据
# ip = "192.168.95.111"
# port = "58087"
try:
    ip = sys.argv[1]
    port = sys.argv[2]
except IndexError:
    print("please use parameter:ip port")
    sys.exit(0)

# Storm 服务监控
cluster_configuration = "".join(["http://", ip, ":", port, "/api/v1/cluster/configuration"])
cluster_summary = "".join(["http://", ip, ":", port, "/api/v1/cluster/summary"])
# storm控制节点监控
nimbus_summary = "".join(["http://", ip, ":", port, "/api/v1/nimbus/summary"])
# storm工作节点监控
supervisor_summary = "".join(["http://", ip, ":", port, "/api/v1/supervisor/summary"])
# storm拓扑监控
topology_summary = "".join(["http://", ip, ":", port, "/api/v1/topology/summary"])

# 服务监控
json_cluster_configuration = urllib2.urlopen(cluster_configuration).read()
dict_cluster_configuration = json.loads(json_cluster_configuration)
# print(dict_cluster_configuration)
json_cluster_summary = urllib2.urlopen(cluster_summary).read()
dict_cluster_summary = json.loads(json_cluster_summary)


# print(dict_cluster_summary)

# 获取zookeeper地址
def get_zookeeperAddr():
    zk_port = dict_cluster_configuration["storm.zookeeper.port"]
    zk_ips = dict_cluster_configuration["storm.zookeeper.servers"]
    zookeeperAddr = str()
    if zk_ips != "" and zk_ips != None:
        for zk_ip in zk_ips:
            zookeeperAddr = "".join([zookeeperAddr, str(zk_ip), ":", str(zk_port), ","])
    return zookeeperAddr[:-1]


ip_port = "-".join([ip, port])

results = "".join([ip_port + "-storm||ResStormService||CM-storm-01-01||" +
                   "serviceName"])  # 未知
results = "\n".join([results, ip_port + "-storm||ResStormService||CM-storm-01-02||" +
                     "descr"])  # 未知
results = "\n".join([results, ip_port + "-storm||ResStormService||CM-storm-01-03||" +
                     dict_cluster_summary['stormVersion']])
results = "\n".join([results, ip_port + "-storm||ResStormService||CM-storm-01-04||" +
                     get_zookeeperAddr()])  # 1.0:未知  2.0:用函数计算
results = "\n".join([results, ip_port + "-storm||ResStormService||CM-storm-01-05||" +
                     str(len(dict_cluster_configuration["nimbus.seeds"]))])  # 1.0：计算nimbus.seeds的数量 来推算nimbusNum 2.0：同
results = "\n".join([results, ip_port + "-storm||ResStormService||CM-storm-01-06||" +
                     str(dict_cluster_summary['supervisors'])])
results = "\n".join([results, ip_port + "-storm||ResStormService||PM-storm-01-01||" +
                     "0"])  # 1.0:未知   2.0:能采集到上面的数据，说明正常 0
results = "\n".join([results, ip_port + "-storm||ResStormService||PM-storm-01-02||" +
                     str(dict_cluster_summary['slotsUsed'])])
results = "\n".join([results, ip_port + "-storm||ResStormService||PM-storm-01-03||" +
                     str(dict_cluster_summary['slotsFree'])])
results = "\n".join([results, ip_port + "-storm||ResStormService||PM-storm-01-04||" +
                     str(dict_cluster_summary['slotsTotal'])])
results = "\n".join([results, ip_port + "-storm||ResStormService||PM-storm-01-05||" +
                     str(dict_cluster_summary['executorsTotal'])])
results = "\n".join([results, ip_port + "-storm||ResStormService||PM-storm-01-06||" +
                     str(dict_cluster_summary['tasksTotal'])])

# 控制节点监控,返回两组
json_nimbus_summary = urllib2.urlopen(nimbus_summary).read()
dict_nimbus_summary = json.loads(json_nimbus_summary)
# print(dict_nimbus_summary)
n = 0
while n < len(dict_nimbus_summary['nimbuses']):
    results = "\n".join([results, ip_port + "-storm||ResStormNimbus||CM-storm-02-01||" +
                         dict_nimbus_summary['nimbuses'][n]['host']])
    results = "\n".join([results, ip_port + "-storm||ResStormNimbus||CM-storm-02-02||" +
                         str(dict_nimbus_summary['nimbuses'][n]['port'])])
    results = "\n".join([results, ip_port + "-storm||ResStormNimbus||CM-storm-02-03||" +
                         (u"是" if dict_nimbus_summary['nimbuses'][n]['status'] == "Leader" else u"否")])
    # 1.0:isLeader属性在json里面没有找到，可用status属性代替?  2.0:参考java代码，根据status判断
    results = "\n".join([results, ip_port + "-storm||ResStormNimbus||PM-storm-02-01||" +
                         dict_nimbus_summary['nimbuses'][n]['status']])
    n = n + 1

# 工作节点监控返回要求的格式
json_supervisor_summary = urllib2.urlopen(supervisor_summary).read()
dict_supervisor_summary = json.loads(json_supervisor_summary)
results = "\n".join([results, ip_port + "-storm||ResStormSupervisor||CM-storm-03-01||" +
                     dict_supervisor_summary['supervisors'][0]['host']])
results = "\n".join([results, ip_port + "-storm||ResStormSupervisor||CM-storm-03-02||" +
                     dict_supervisor_summary['supervisors'][0]['id']])
results = "\n".join([results, ip_port + "-storm||ResStormSupervisor||PM-storm-03-01||" +
                     "0"])  # 1.0 status属性在json里面没有找到，后续处理  2.0 参考java代码，写死"0"
results = "\n".join([results, ip_port + "-storm||ResStormSupervisor||PM-storm-03-02||" +
                     str(dict_supervisor_summary['supervisors'][0]['slotsUsed'])])
results = "\n".join([results, ip_port + "-storm||ResStormSupervisor||PM-storm-03-03||" +
                     str(dict_supervisor_summary['supervisors'][0]['slotsTotal'])])
results = "\n".join([results, ip_port + "-storm||ResStormSupervisor||PM-storm-03-04||" +
                     str(dict_supervisor_summary['supervisors'][0]['usedMem'])])

# 获取拓扑监控topology的json，会返回三组数据！
json_topology_summary = urllib2.urlopen(topology_summary).read()
dict_topology_summary = json.loads(json_topology_summary)  # 解析成字典，方便获取
numbers = (len(dict_topology_summary['topologies']))  # 返回了几组数据 （一般是三组）
# 输出三组 拓扑监控topology 的要求返回格式
n = 1
while n <= numbers:
    results = "\n".join([results, ip_port + "-storm||ResStormTopology||CM-storm-04-01||" +
                         dict_topology_summary['topologies'][n - 1]['name']])
    results = "\n".join([results, ip_port + "-storm||ResStormTopology||CM-storm-04-02||" +
                         dict_topology_summary['topologies'][n - 1]['id']])
    results = "\n".join([results, ip_port + "-storm||ResStormTopology||PM-storm-04-01||" +
                         dict_topology_summary['topologies'][n - 1]['status']])
    results = "\n".join([results, ip_port + "-storm||ResStormTopology||PM-storm-04-02||" +
                         str(dict_topology_summary['topologies'][n - 1]['workersTotal'])])
    results = "\n".join([results, ip_port + "-storm||ResStormTopology||PM-storm-04-03||" +
                         str(dict_topology_summary['topologies'][n - 1]['executorsTotal'])])
    results = "\n".join([results, ip_port + "-storm||ResStormTopology||PM-storm-04-04||" +
                         str(dict_topology_summary['topologies'][n - 1]['tasksTotal'])])
    results = "\n".join([results, ip_port + "-storm||ResStormTopology||PM-storm-04-05||" +
                         str(dict_topology_summary['topologies'][n - 1]['assignedTotalMem'])])
    n = n + 1

print(results)

# # 输出所有返回的json
# get_all_json = list()
# all_url = [cluster_configuration, cluster_summary, nimbus_summary, supervisor_summary, topology_summary]
# for url in all_url:
#     get_all_json.append(urllib2.urlopen(url).read())
# print(get_all_json)
