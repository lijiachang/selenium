#!/usr/bin/env python
# -*- coding:utf-8 -*-
# haproxymon通过Haproxy的stats socket来采集Haproxy基础状态信息
#
# 找到haproxy的stats文件
# 默认位置在： /var/lib/haproxy/stats
# 实际位置在haproxy的配置文件中可以看到 /etc/haproxy/haproxy.cfg

import os
import sys
import stat
import socket

try:
    stats_path = sys.argv[1]
except:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s haproxy_stats_path" % (sys.argv[0], sys.argv[0]))
    sys.exit(0)


class HaproxyStats(object):
    def __init__(self, conf):
        self.StatsFile = conf["stats_file"]
        self.Debug = conf["debug_level"]
        self.BufferSize = conf["buffer_size"]
        self.MetricPrefix = conf["metric_prefix"]
        self.Metrics = conf["metrics"]
        self._status = True
        self.socket_ = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if conf["endpoint_type"] == "hostname":
            self.EndpointName = socket.gethostname()
        else:
            self.EndpointName = self.get_local_ip()

    def __del__(self):
        self.socket_.close()

    def connect(self):
        try:
            if os.path.exists(self.StatsFile) and stat.S_ISSOCK(os.stat(self.StatsFile).st_mode):
                self.socket_.connect(self.StatsFile)
            else:
                print("||%s||FM-PLUGIN-EXECUTE-FAILED||SOCK file:  %s dont exist" % (sys.argv[0], sys.argv[1]))
                sys.exit(0)
                # print >> sys.stderr, "-- SOCK file: " + self.StatsFile + " dont exist"
                # self._status = False
        except socket.error, msg:
            print >> sys.stderr, msg
            self._status = False

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            (addr, port) = s.getsockname()
            s.close()
            return addr
        except socket.error:
            return socket.gethostbyname(socket.gethostname())

    def get_ha_stats(self):
        try:
            HS = []
            COMMAND = 'show stat\n'
            # import pdb;pdb.set_trace()
            if self._status:
                self.socket_.send(COMMAND)
                data = self.socket_.recv(self.BufferSize)
                if self.Debug >= 3:
                    print "-- orgi stat info:\n", data, "\n"
                data = data.split("\n")
                for line in data:
                    Status = line.split(',')
                    # For Compatibility older versions
                    if len(Status) < 2:
                        continue
                    if Status[32] == 'type':
                        Status[0] = Status[0].replace('#', '').strip()
                        Title = Status[0:-1]
                    else:
                        HS.append(Status)
                if self.Debug >= 3:
                    print '-- stat info array:\n', HS, "\n"
                NewHS = []
                for MS in HS:
                    metric = {}
                    for header in Title:
                        i = Title.index(header)
                        metric[header] = 0 if len(str(MS[i])) == 0 else MS[i]
                    NewHS.append(metric)
                if self.Debug >= 3:
                    print "-- stst info array by title:\n", NewHS, "\n"
            return NewHS
        except Exception, msg:
            print >> sys.stderr, msg
            return False

    def get_ha_info(self):
        try:
            COMMAND = 'show info\n'
            if self._status:
                self.socket_.send(COMMAND)
                data = self.socket_.recv(8192)
                return data
            else:
                self._status = False
        except socket.error, msg:
            print >> sys.stderr, msg

    def getMetric(self):
        UploadMetric = []
        # upload_ts = int(time.time())
        upload_ts = 0
        self.connect()
        if self._status:
            MyStats = self.get_ha_stats()
            if MyStats:
                StatusCnt = 0
                for MS in MyStats:
                    Tag = 'pxname=' + MS['pxname'] + ',svname=' + MS['svname']
                    for key, value in MS.iteritems():
                        if key not in self.Metrics:
                            continue
                        MetricName = self.MetricPrefix + key
                        if key == 'status':
                            if value == 'DOWN':
                                MetricValue = 1
                            else:
                                MetricValue = 0
                        else:
                            MetricValue = value
                        UploadMetric.append(
                            {"endpoint": self.EndpointName, "metric": MetricName, "tags": Tag, "timestamp": upload_ts,
                             "value": MetricValue, "step": 60, "counterType": "GAUGE"})
                getStatsFile = 0
            else:
                getStatsFile = 1
        else:
            getStatsFile = 2
        UploadMetric.append({"endpoint": self.EndpointName, "metric": self.MetricPrefix + 'getstats',
                             "tags": 'filename=' + self.StatsFile, "timestamp": upload_ts, "value": getStatsFile,
                             "step": 60, "counterType": "GAUGE"})
        return UploadMetric

    def sendData(self):
        haproxy_metric = self.getMetric()
        # print haproxy_metric # 原始数据


def to_results(data):
    # mpoint = "-".join(["ip", "port", "Haproxy"])
    mpoint = "-".join([ip, "Haproxy"])
    ckbp = ""
    separator = "||"
    wrap = "\n"
    results = list()
    for i in data:
        results.append(separator.join([mpoint, ckbp, "PM-" + i["tags"] + "-" + i["metric"], str(i["value"])]))
    for r in results:
        print(r)


if __name__ == "__main__":
    conf = {
        "debug_level": 2,
        "endpoint_type": "ip",
        "metric_prefix": "haproxy_",
        "metrics": ['qcur', 'scur', 'rate', 'status', 'ereq', 'drep', 'act', 'bck', 'qtime', 'ctime', 'rtime', 'ttime'],
        "stats_file": "%s" % stats_path,
        "buffer_size": 8192,
    }
    hs = HaproxyStats(conf)
    ip = hs.get_local_ip()
    to_results(hs.getMetric())
