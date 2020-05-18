# coding:utf-8

import subprocess
import sys

# 兼容Python3
# 通用mysql采集
#  By 李家昌 最后修改于 2019.01.31


try:
    ip = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    database = sys.argv[5]
    sql = sys.argv[6]
    mpoint = "-".join([ip, port, database])
except:
    print("Please usage:%s ip port user password database sql" % sys.argv[0])
    sys.exit(0)


def output(sql):
    command = 'mysql -h ' + ip + ' -P ' + port + ' -u ' + user + ' -p' + password + ' ' + database + ' -e "' + sql + '"'
    # print(command)
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stderr = ps.stderr.read()
    stdout = ps.stdout.readlines()
    if b"ERROR" in stderr:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, stderr))
        sys.exit(0)
    else:
        return stdout


if __name__ == '__main__':
    separator = "||"
    if sql[0] == '"':
        sql = sql[1:-1]  # 判断有引号，去掉两个引号
    results = output(sql)

    if not results:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||table result in null !" % mpoint)  # 空表输出结果
        sys.exit(0)
    #print(results)
    results0_lower = results[0]  # 解决大小写问题
    list_results0_lower = results0_lower.decode("utf-8").strip().split("\t")

    for r in results[1:]:

        for title in list_results0_lower:
            # dict_tmp = {}
            # dict_tmp.update({title: r.decode("utf-8").split("\t")[list_results0_lower.index(title)]})
            if title != "ckbp":
                ckbp = r.decode("utf-8").split("\t")[list_results0_lower.index("ckbp")] if "ckbp".encode() in results0_lower else ""
                ckbp = "" if ckbp.lower() == "null" else ckbp
                kpi = title
                value = r.decode("utf-8").split("\t")[list_results0_lower.index(title)].strip()
                value = "value is null" if value == "" or value.lower() == "null" else value
                if value != "value is null": # value 空值不输出
                    print(separator.join([mpoint, ckbp, kpi, value]))

