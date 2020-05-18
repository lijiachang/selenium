#!/usr/bin/python
# coding:utf-8


import redis  # 需要安装redis模块

try:
    import json
except ImportError:
    import simplejson as json


# ip = '192.168.95.113'
# redis_service = 'SIGMAM'
# r = redis.Redis(host=ip, port=56379, password="sigmam1611")
#
# redis_info = r.info()


def get_sentinel_kpis(ip, redis_info):
    redis_service = 'SIGMAM'
    sentinel = dict()
    sentinel.update({'CM-Redis-Sentinel-01-01': 'SentinelName'})
    sentinel.update({'CM-Redis-Sentinel-01-02': ip})
    sentinel.update({'CM-Redis-Sentinel-01-03': redis_info["tcp_port"]})
    sentinel.update({'CM-Redis-Sentinel-01-04': redis_service})
    sentinel.update({'PM-Redis-Sentinel-01-05': 'SentinelStatus'})
    return sentinel

def get_server_kpis(ip, redis_info):
    redis_service = 'SIGMAM'
    server = dict()
    server.update({'CM-Redis-Server-01-01': 'resDescr'})
    server.update({'CM-Redis-Server-01-02': ip})
    server.update({'CM-Redis-Server-01-03': redis_info["tcp_port"]})
    server.update({'CM-Redis-Server-01-04': redis_service})
    server.update({'CM-Redis-Server-01-05': redis_info["redis_version"]})
    server.update({'CM-Redis-Server-01-06': redis_info["redis_mode"]})
    server.update({'CM-Redis-Server-01-07': redis_info["os"]})
    server.update({'CM-Redis-Server-01-08': redis_info["gcc_version"]})
    server.update({'CM-Redis-Server-01-09': redis_info["uptime_in_seconds"]})
    server.update({'CM-Redis-Server-01-10': redis_info["uptime_in_days"]})
    server.update({'CM-Redis-Server-01-11': 'ServiceStatus'})

    server.update({'CM-Redis-Server-02-01': redis_info["role"]})
    server.update({'CM-Redis-Server-02-02': "MasterOrSlave"})
    server.update({'CM-Redis-Server-03-01': redis_info["connected_clients"]})
    server.update({'CM-Redis-Server-03-02': redis_info["blocked_clients"]})
    server.update({'CM-Redis-Server-03-03': "Newconnection"})
    server.update({'CM-Redis-Server-04-01': redis_info["used_memory_human"]})
    server.update({'CM-Redis-Server-04-02': redis_info["used_memory_peak_human"]})
    server.update({'CM-Redis-Server-05-01': "QPS"})
    # keyspace_hits/（单位keyspace_hits+单位keyspace_misses）
    if (redis_info["keyspace_hits"] + redis_info["keyspace_misses"]) == 0:
        keyspaceShooting = 0
    else:
        keyspaceShooting = float(redis_info["keyspace_hits"]) / float(
            (redis_info["keyspace_hits"] + redis_info["keyspace_misses"])) * 100
    server.update({'CM-Redis-Server-05-02': round(keyspaceShooting, 2)})
    server.update({'CM-Redis-Server-05-03': redis_info["db0"]["keys"]})
    server.update({'CM-Redis-Server-05-04': redis_info["pubsub_channels"]})
    server.update({'CM-Redis-Server-05-05': redis_info["pubsub_patterns"]})
    server.update({'CM-Redis-Server-06-01': redis_info["rdb_last_bgsave_status"]})
    server.update({'CM-Redis-Server-06-02': redis_info["rdb_last_save_time"]})
    #从指标模型中新增 PM-40-14-002-XX
    server.update({'PM-40-14-002-01': redis_info["used_cpu_sys"]})
    server.update({'PM-40-14-002-02': redis_info["used_cpu_user"]})
    server.update({'PM-40-14-002-03': redis_info["used_cpu_sys_children"]})
    server.update({'PM-40-14-002-04': redis_info["used_cpu_user_children"]})
    server.update({'PM-40-14-002-05': redis_info["mem_fragmentation_ratio"]})
    server.update({'PM-40-14-002-06': 'responseAvgTime'})
    server.update({'PM-40-14-002-07': redis_info["instantaneous_ops_per_sec"]})
    server.update({'PM-40-14-002-08': 'keyPercent'})
    server.update({'PM-40-14-002-09': 'keyExpiresPercent'})

    return server


results = []
ip_all = ["192.168.95.111", "192.168.95.112", "192.168.95.113"]
for i in ip_all:
    r = redis.Redis(host=i, port=56378)
    redis_info = r.info()
    results.append({'mpoint': 'Redis-' + i + '-56378', 'ckbp': 'null', 'kpis': get_sentinel_kpis(i, redis_info)})

    r = redis.Redis(host=i, port=56379, password="sigmam1611")
    redis_info = r.info()
    results.append({'mpoint': 'Redis-' + i + '-56379', 'ckbp': 'null', 'kpis': get_server_kpis(i, redis_info)})

    r = redis.Redis(host=i, port=56380, password="sigmam1611")
    redis_info = r.info()
    results.append({'mpoint': 'Redis-' + i + '-56380', 'ckbp': 'null', 'kpis': get_server_kpis(i, redis_info)})

print json.dumps(results, sort_keys=True)
