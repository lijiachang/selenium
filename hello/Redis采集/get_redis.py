# /bin/usr/python
# coding:utf-8

import redis  # 需要安装redis模块
import sys

try:
    import json
except ImportError:
    import simplejson as json

if len(sys.argv) != 4:
    print("please use parameter:IP Port RedisPassword")
    sys.exit()
else:
    ip = sys.argv[1]
    port = sys.argv[2]
    password = sys.argv[3]

# ip = '192.168.95.113'
# port = "56379"
# password = "sigmam1611"
redis_service = 'SIGMAM'

r = redis.Redis(host=ip, port=port, password=password)
redis_info = r.info()
# print(redis_info)

mpoint = "-".join([ip, port, "zookeeper"])
ckbp = "ResRedisSentinel"
separator = "||"
wrap = "\n"

results = separator.join([mpoint, ckbp, "CM-Redis-Sentinel-01-01", 'SentinelName'])  # 代理名称(描述信息)
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Sentinel-01-02", ip])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Sentinel-01-03", str(redis_info["tcp_port"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Sentinel-01-04", redis_service])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Sentinel-01-05", 'SentinelStatus'])])   # 代理状态

ckbp = "ResRedisServer"
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-01-01", 'resDescr'])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-01-02", ip])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-01-03", str(redis_info["tcp_port"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-01-04", redis_service])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-01-05", redis_info["redis_version"]])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-01-06", redis_info["redis_mode"]])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-01-07", redis_info["os"]])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-01-08", redis_info["gcc_version"]])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-01-09", str(redis_info["uptime_in_seconds"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-01-10", str(redis_info["uptime_in_days"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-01-11", 'ServiceStatus'])])

results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-02-01", redis_info["role"]])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-02-02", "MasterOrSlave"])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-03-01", str(redis_info["connected_clients"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-03-02", str(redis_info["blocked_clients"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-03-03", "Newconnection"])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-04-01", redis_info["used_memory_human"]])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-04-02", redis_info["used_memory_peak_human"]])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-05-01", "QPS"])])
# keyspace_hits/（单位keyspace_hits+单位keyspace_misses）
if (redis_info["keyspace_hits"] + redis_info["keyspace_misses"]) == 0:
    keyspaceShooting = 0
else:
    keyspaceShooting = float(redis_info["keyspace_hits"]) / float(
        (redis_info["keyspace_hits"] + redis_info["keyspace_misses"])) * 100
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-05-02", str(round(keyspaceShooting, 2))])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-05-03", str(redis_info["db0"]["keys"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-05-04", str(redis_info["pubsub_channels"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-05-05", str(redis_info["pubsub_patterns"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-06-01", redis_info["rdb_last_bgsave_status"]])])
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-Redis-Server-06-02", str(redis_info["rdb_last_save_time"])])])

# 从指标模型中新增 PM-40-14-002-XX
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-40-14-002-01", str(redis_info["used_cpu_sys"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-40-14-002-02", str(redis_info["used_cpu_user"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-40-14-002-03", str(redis_info["used_cpu_sys_children"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-40-14-002-04", str(redis_info["used_cpu_user_children"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-40-14-002-05", str(redis_info["mem_fragmentation_ratio"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-40-14-002-06", 'responseAvgTime'])])
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-40-14-002-07", str(redis_info["instantaneous_ops_per_sec"])])])
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-40-14-002-08", 'keyPercent'])])
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-40-14-002-09", 'keyExpiresPercent'])])


print(results)
