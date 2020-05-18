#!/bin/env python
# -*- coding:utf-8 -*-
# 2019.06.25
# 可远程采集redis

import time
import os
import re
import sys
import commands

try:
    ip = sys.argv[1]
    port = sys.argv[2]
except:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s ip port [password]" % (sys.argv[0], sys.argv[0]))
    sys.exit(0)

try:
    password = sys.argv[3]  # 可以为空
except:
    password = None


class RedisStats:
    # 自动寻找redis-cli路径 2019.06.13
    _pid = (commands.getoutput("ps -e|grep redis-server|awk '{print $1}'"))  # redis-server pid
    pwdx = (commands.getoutput("pwdx %s" % _pid))
    path_regex = re.findall(r"\S*:\s(.*)", pwdx)
    raw_data = ""

    # 如果你是自己编译部署到redis，请将下面的值替换为你到redis-cli路径
    # _redis_cli = '/opt/ultrapower/sigmamcloud/middleware/redis-4.0.12/src/redis-cli'
    _redis_cli = path_regex[0] + "/redis-cli"
    _stat_regex = re.compile(ur'(\w+):([0-9]+\.?[0-9]*)\r')

    def __init__(self, port='58946', password='mima', host='127.0.0.1'):
        self._cmd = '%s -h %s -p %s info' % (self._redis_cli, host, port)
        if password not in ['', None, 'None']:
            self._cmd = '%s -h %s -p %s -a %s info' % (self._redis_cli, host, port, password)
        # print self._cmd

    def stats(self):
        ' Return a dict containing redis stats '
        info = commands.getoutput(self._cmd)
        # print(info)  # 原始数据
        self.raw_data = info
        return dict(self._stat_regex.findall(info))


def main():
    global p
    # ip = socket.gethostname()
    timestamp = int(time.time())
    step = 60
    # inst_list中保存了redis配置文件列表，程序将从这些配置中读取port和password，建议使用动态发现的方法获得，如：
    # inst_list = [ i for i in commands.getoutput("find  /etc/ -name 'redis*.conf'" ).split('\n') ]
    insts_list = ['/etc/redis/redis.conf']
    p = []

    monit_keys = [
        ('connected_clients', 'GAUGE'),
        ('blocked_clients', 'GAUGE'),
        ('used_memory', 'GAUGE'),
        ('used_memory_rss', 'GAUGE'),
        ('mem_fragmentation_ratio', 'GAUGE'),
        ('total_commands_processed', 'COUNTER'),
        ('rejected_connections', 'COUNTER'),
        ('expired_keys', 'COUNTER'),
        ('evicted_keys', 'COUNTER'),
        ('keyspace_hits', 'COUNTER'),
        ('keyspace_misses', 'COUNTER'),
        ('keyspace_hit_ratio', 'GAUGE'),
    ]

    for inst in insts_list:
        # port = commands.getoutput("sed -n 's/^port *\([0-9]\{4,5\}\)/\\1/p' %s" % inst)
        # passwd = commands.getoutput("sed -n 's/^requirepass *\([^ ]*\)/\\1/p' %s" % inst)
        metric = "redis"
        endpoint = ip
        tags = 'port=%s' % port

        try:
            conn = RedisStats(port, password, ip)
            stats = conn.stats()
            # print stats
        except Exception as e:
            print(e)
            continue

        # 结果为空时，打印FM输出错误原始内容
        if not stats:
            raw_data2 = conn.raw_data.replace(
                "Warning: Using a password with '-a' option on the command line interface may not be safe.\n", "")
            print("-".join([ip, port, "redis"]) + '||' + sys.argv[0] + '||FM-PLUGIN-EXECUTE-FAILED||' + raw_data2)
            sys.exit(0)

        for key, vtype in monit_keys:
            # 一些老版本的redis中info输出的信息很少，如果缺少一些我们需要采集的key就跳过
            if key not in stats.keys():
                continue
            # 计算命中率
            if key == 'keyspace_hit_ratio':
                try:
                    value = float(stats['keyspace_hits']) / (
                            int(stats['keyspace_hits']) + int(stats['keyspace_misses']))
                except ZeroDivisionError:
                    value = 0
            # 碎片率是浮点数
            elif key == 'mem_fragmentation_ratio':
                value = float(stats[key])
            else:
                # 其他的都采集成counter，int
                try:
                    value = int(stats[key])
                except:
                    continue

            i = {
                'Metric': '%s.%s' % (metric, key),
                'Endpoint': endpoint,
                'Timestamp': timestamp,
                'Step': step,
                'Value': value,
                'CounterType': vtype,
                'TAGS': tags
            }
            p.append(i)
    # print(json.dumps(p, sort_keys=True, indent=4))


def to_results():
    mpoint = "-".join([ip, port, "redis"])
    ckbp = ""
    separator = "||"
    wrap = "\n"
    results = list()
    for i in p:
        results.append(separator.join([mpoint, ckbp, "PM-" + i["Metric"], str(i["Value"])]))
    for r in results:
        print(r)


if __name__ == '__main__':
    proc = commands.getoutput(' ps -ef|grep %s|grep -v grep|wc -l ' % os.path.basename(sys.argv[0]))
    sys.stdout.flush()
    if int(proc) < 5:
        main()
        to_results()
