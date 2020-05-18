#!/usr/bin/python
# coding:utf-8

import json
import urllib2
import time
import sys

results = str()  # 总的返回数据

if len(sys.argv) != 3:
    print("please use parameter:IP Port")
    sys.exit()
else:
    ip = sys.argv[1]
    port = sys.argv[2]

# ip = "192.168.182.141"
# port = "2345"
url_info = "http://" + ip + ":" + port + "/v1.22/info"
url_containers = "http://" + ip + ":" + port + "/v1.22/containers/json?all=true"

print("loading...")
info = json.loads(urllib2.urlopen(url_info).read())
containers = json.loads(urllib2.urlopen(url_containers).read())
# 判断宿主机状态
status = "1" if info is None or info == "" else "0"
# 以下是宿主机信息
results = "".join([ip, "-", port, "-docker||ResDockerHost||CM-docker-01-01||", info["Name"]])
results = "".join([results, "\n", ip, "-", port, "-docker||ResDockerHost||CM-docker-01-02||", ip])
results = "".join([results, "\n", ip, "-", port, "-docker||ResDockerHost||CM-docker-01-03||", port])
results = "".join([results, "\n", ip, "-", port, "-docker||ResDockerHost||CM-docker-01-04||", "http"])
results = "".join([results, "\n", ip, "-", port, "-docker||ResDockerHost||CM-docker-01-05||", info["ServerVersion"]])
results = "".join([results, "\n", ip, "-", port, "-docker||ResDockerHost||CM-docker-01-06||", info["OperatingSystem"]])
results = "".join([results, "\n", ip, "-", port, "-docker||ResDockerHost||CM-docker-01-07||", info["KernelVersion"]])
results = "".join([results, "\n", ip, "-", port, "-docker||ResDockerHost||PM-docker-01-01||", status])  # 状态
results = "".join([results, "\n", ip, "-", port, "-docker||ResDockerHost||PM-docker-01-02||", str(info["Containers"])])
results = "".join(
    [results, "\n", ip, "-", port, "-docker||ResDockerHost||PM-docker-01-03||", str(info["ContainersRunning"])])
results = "".join(
    [results, "\n", ip, "-", port, "-docker||ResDockerHost||PM-docker-01-04||", str(info["ContainersPaused"])])
results = "".join(
    [results, "\n", ip, "-", port, "-docker||ResDockerHost||PM-docker-01-05||", str(info["ContainersStopped"])])


def get_container_ip(n):
    """获取容器ip"""
    networkMode = containers[n]["HostConfig"]["NetworkMode"]
    networkSettings = containers[n]["NetworkSettings"]
    if networkMode[:3] != "con":
        networks = networkSettings["Networks"]
        if networks != "" and networks != None and networks.has_key(networkMode):
            ip_add = networks[networkMode]["IPAddress"]
            if networkMode == "host" and ip_add == "":
                ip_add = ip
        else:
            networkMode = "bridge"
            ip_add = networks[networkMode]["IPAddress"]
    else:
        ip_add = networkMode.replace("container:", "")
    return ip_add


# 时间转换
def get_time(created_time):
    time_format = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_time))
    return time_format


# 判断 单个容器状态
def get_state(container_id_dict):
    # 先看是否是 上面的三个状态，不如不是的话，就找下面的四个，哪个是true
    state = id_dict["State"]
    state_status = state["Status"]
    if state_status == "running":
        result = "0"
    elif state_status == "exited":
        result = "1"
    elif state_status == "created":
        result = "6"
    else:
        if state["Paused"]:  # 对应的值 就是Ture 或者False
            result = "2"
        elif state["Restarting"]:
            result = "3"
        elif state["OOMKilled"]:
            result = "4"
        elif state["Dead"]:
            result = "5"

    return result


# 计算内存利用率
def get_mem_utilization(id_stats_dict):
    usage = id_stats_dict["memory_stats"]["usage"]
    limit = id_stats_dict["memory_stats"]["limit"]
    if usage == 0:
        return "0"
    else:
        mem_utilization = format(float(usage * 100) / float(limit), ".2f")
        return str(mem_utilization)


# 以下是单个容器信息
n = 0
while n < len(containers):
    container_id = containers[n]["Id"]
    url_container_id = "http://" + ip + ":" + port + "/v1.22/containers/" + container_id + "/json"
    id_dict = json.loads(urllib2.urlopen(url_container_id).read())

    # CM 信息
    results = "".join(
        [results, "\n", ip, "-", port, "-docker||ResDockerContainer||CM-docker-02-01||", containers[n]["Names"][0][1:]])
    results = "".join(
        [results, "\n", ip, "-", port, "-docker||ResDockerContainer||CM-docker-02-02||", container_id])
    results = "".join(
        [results, "\n", ip, "-", port, "-docker||ResDockerContainer||CM-docker-02-03||",
         containers[n]["NetworkSettings"]["Networks"].keys()[0]])
    results = "".join(
        [results, "\n", ip, "-", port, "-docker||ResDockerContainer||CM-docker-02-04||", get_container_ip(n)])
    results = "".join(
        [results, "\n", ip, "-", port, "-docker||ResDockerContainer||CM-docker-02-05||",
         get_time(int(containers[n]["Created"]))])
    results = "".join(
        [results, "\n", ip, "-", port, "-docker||ResDockerContainer||CM-docker-02-06||", id_dict["Path"]])
    results = "".join(
        [results, "\n", ip, "-", port, "-docker||ResDockerContainer||CM-docker-02-07||", containers[n]["Image"]])
    results = "".join(
        [results, "\n", ip, "-", port, "-docker||ResDockerContainer||CM-docker-02-08||",
         str(id_dict["HostConfig"]["Memory"])])
    results = "".join(
        [results, "\n", ip, "-", port, "-docker||ResDockerContainer||CM-docker-02-09||",
         "1024" if id_dict["HostConfig"]["CpuShares"] == 0 else str(id_dict["HostConfig"]["CpuShares"])])

    # PM 信息
    url_stats_container_id = "http://" + ip + ":" + port + "/v1.22/containers/" + container_id + "/stats?stream=false"
    id_stats_dict = json.loads(urllib2.urlopen(url_stats_container_id).read())

    results = "".join(
        [results, "\n", ip, "-", port, "-docker||ResDockerContainer||PM-docker-02-01||", get_state(id_dict)])
    results = "".join(
        [results, "\n", ip, "-", port, "-docker||ResDockerContainer||PM-docker-02-02||", str(id_dict["RestartCount"])])
    results = "".join(
        [results, "\n", ip, "-", port, "-docker||ResDockerContainer||PM-docker-02-05||",
         get_mem_utilization(id_stats_dict)])

    # print id_dict
    n = n + 1
print(results)
