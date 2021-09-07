# encoding: utf-8
# @Date    : 2021-09-04
# @Author  : author
# @Version : log_ip v1.0
# @Email   :


import sys
import importlib

importlib.reload(sys)

import re
import time
import requests

time1 = time.time()


######函数功能:能够提取ip地址，并且去重################
def read_file(input_file_name, output_file_name):
    _fLog = open(input_file_name)
    sep = '\n'
    ip_list = []
    # print(_fLog)
    for each in _fLog:
        # print(each)
        # 取出()内的分组内容
        match = re.match(r'.*view neiwang: (\S*)', each)
        # print(match)
        if match:
            print(match.group(1))
            ip_list.append(match.group(1))

    ids = list(set(ip_list))
    print("共解析个数:%s " % len(ids))  ##写出数据到本地
    out = open(output_file_name, "a")
    # out.write("ip" + sep)
    for each in ids:
        print(each)
        out.write(each + sep)  ##关闭连接 out.close()
    _fLog.close()
    print("ip提取完毕~~")


####主函数################
if __name__ == '__main__':
    input_file_name = "_2021-09-02~00_07_57_15.log"
    output_file_name = "myjob.txt"
    read_file(input_file_name, output_file_name)
    time2 = time.time()
    print(u'总共耗时：' + str(time2 - time1) + 's')
