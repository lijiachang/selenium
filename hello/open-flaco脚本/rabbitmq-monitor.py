#!/bin/env python
# -*- coding:utf-8 -*-
# 2019.07.04

import urllib2, base64, json
import sys

try:
    ip = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
except:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s ip port username password" % (sys.argv[0], sys.argv[0]))
    sys.exit(0)

step = 60
# ts = int(time.time())
ts = 0
keys = ('messages_ready', 'messages_unacknowledged')
rates = ('ack', 'deliver', 'deliver_get', 'publish')

request = urllib2.Request("http://%s:%s/api/queues" % (ip, port))
# see #issue4
base64string = base64.b64encode('%s:%s' % (username, password))
request.add_header("Authorization", "Basic %s" % base64string)
try:
    result = urllib2.urlopen(request)
except Exception as e:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||%s" % (sys.argv[0], e))
    sys.exit(0)

url_result = result.read()
#print url_result
data = json.loads(url_result)
# data = result.read()[0]
tag = ''
# tag = sys.argv[1].replace('_',',').replace('.','=')

p = []
for queue in data:
    # ready and unack
    msg_total = 0
    for key in keys:
        q = {}
        q["endpoint"] = ip
        q['timestamp'] = ts
        q['step'] = step
        q['counterType'] = "GAUGE"
        q['metric'] = 'rabbitmq.%s' % key
        q['tags'] = 'name=%s,%s' % (queue['name'], tag)
        q['value'] = int(queue[key])
        msg_total += q['value']
        p.append(q)

    # total
    q = {}
    q["endpoint"] = ip
    q['timestamp'] = ts
    q['step'] = step
    q['counterType'] = "GAUGE"
    q['metric'] = 'rabbitmq.messages_total'
    q['tags'] = 'name=%s,%s' % (queue['name'], tag)
    q['value'] = msg_total
    p.append(q)

    # rates
    for rate in rates:
        q = {}
        q["endpoint"] = ip
        q['timestamp'] = ts
        q['step'] = step
        q['counterType'] = "GAUGE"
        q['metric'] = 'rabbitmq.%s_rate' % rate
        q['tags'] = 'name=%s,%s' % (queue['name'], tag)
        try:
            q['value'] = int(queue['message_stats']["%s_details" % rate]['rate'])
        except:
            q['value'] = 0
        p.append(q)


def to_results(data):
    mpoint = "-".join([ip, port, "RabbitMQ"])
    ckbp = ""
    separator = "||"
    wrap = "\n"
    results = list()
    for i in data:
        results.append(separator.join([mpoint, ckbp, "PM-" + i["metric"], str(i["value"])]))
    for r in results:
        print(r)


to_results(p)
