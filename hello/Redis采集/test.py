#!/usr/bin/python
# coding:utf-8


import redis  # 需要安装redis模块

try:
    import json
except ImportError:
    import simplejson as json

ip = '192.168.95.110'
redis_service = 'SIGMAM'
r = redis.Redis(host=ip, port=56389)
redis_info = r.info()

for r in redis_info:
    print "%s  %s" % (r, redis_info[r])

# kpis.update({'CM-Redis-Service-01-01':'ServiceName'})
# kpis.update('PM-Redis-Service-01-02','ServiceStatus')
# kpis.update('CM-Redis-Sentinel-01-01','SentinelName')
# kpis.update('CM-Redis-Sentinel-01-02','IP')
# kpis.update('CM-Redis-Sentinel-01-03','tcpPort')
# kpis.update('CM-Redis-Sentinel-01-04','redisservice')
# kpis.update('CM-Redis-Sentinel-01-05','SentinelStatus')
# kpis.update('CM-Redis-Sentinel-01-02','IP')

# server = dict()
# server.update({'CM-Redis-Server-01-01': 'resDescr'})
# server.update({'CM-Redis-Server-01-02': ip})
# server.update({'CM-Redis-Server-01-03': redis_info["tcp_port"]})
# server.update({'CM-Redis-Server-01-04': redis_service})
# server.update({'CM-Redis-Server-01-05': redis_info["redis_version"]})
# server.update({'CM-Redis-Server-01-06': redis_info["redis_mode"]})
# server.update({'CM-Redis-Server-01-07': redis_info["os"]})
# server.update({'CM-Redis-Server-01-08': redis_info["gcc_version"]})
# server.update({'CM-Redis-Server-01-09': redis_info["uptime_in_seconds"]})
# server.update({'CM-Redis-Server-01-10': redis_info["uptime_in_days"]})
# server.update({'CM-Redis-Server-01-11': 'ServiceStatus'})
#
# server.update({'CM-Redis-Server-02-01': redis_info["role"]})
# server.update({'CM-Redis-Server-02-02': "MasterOrSlave"})
# server.update({'CM-Redis-Server-03-01': redis_info["connected_clients"]})
# server.update({'CM-Redis-Server-03-02': redis_info["blocked_clients"]})
# server.update({'CM-Redis-Server-03-03': "Newconnection"})
# server.update({'CM-Redis-Server-04-01': redis_info["used_memory_human"]})
# server.update({'CM-Redis-Server-04-02': redis_info["used_memory_peak_human"]})
# server.update({'CM-Redis-Server-05-01': "QPS"})
# # keyspace_hits/（单位keyspace_hits+单位keyspace_misses）
# if (redis_info["keyspace_hits"] + redis_info["keyspace_misses"]) == 0:
#     keyspaceShooting = 0
# else:
#     keyspaceShooting = float(redis_info["keyspace_hits"]) / float(
#         (redis_info["keyspace_hits"] + redis_info["keyspace_misses"])) * 100
# server.update({'CM-Redis-Server-05-02': round(keyspaceShooting, 2)})
# server.update({'CM-Redis-Server-05-03': redis_info["db0"]["keys"]})
# server.update({'CM-Redis-Server-05-04': redis_info["pubsub_channels"]})
# server.update({'CM-Redis-Server-05-05': redis_info["pubsub_patterns"]})
# server.update({'CM-Redis-Server-06-01': redis_info["rdb_last_bgsave_status"]})
# server.update({'CM-Redis-Server-06-02': redis_info["rdb_last_save_time"]})
#
# print server
