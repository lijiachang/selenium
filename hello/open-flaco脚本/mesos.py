#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019.07.22

import urllib2
import sys

try:
    ip = sys.argv[1]
    port = sys.argv[2]

except:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s ip port" % (sys.argv[0], sys.argv[0]))
    sys.exit(0)

ts = 0
raw = {}

try:
    info = urllib2.Request('http://%s:%s/metrics/snapshot' % (ip, port))
    info = urllib2.urlopen(info, timeout=5).read()
    # print result
    raw.update(eval(info))
except Exception as e:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||%s" % (sys.argv[0], e))
    sys.exit(0)

result = []
for k, v in raw.iteritems():
    result.append({
        "metric": "mesos.%s" % k.replace('\/', '.'),
        "timestamp": ts,
        "step": 30,
        "value": v,
    })


def to_results(data):
    mpoint = "-".join([ip, port, "Mesos"])
    ckbp = ""
    separator = "||"
    wrap = "\n"
    results = list()
    for i in data:
        results.append(separator.join([mpoint, ckbp, "PM-" + i["metric"], str(i["value"])]))
    for r in results:
        print(r)


to_results(result)
