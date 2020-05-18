# coding:utf-8

import subprocess
import sys

# 兼容Python3
# 通用mysql采集
# 读取参数sql，执行单条SQL语句，返回执行结果
# 使用mysql -h 命令远程采集信息， By 李家昌 最后修改于 2018.08.16


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
    command = 'mysql -h ' + ip + ' -P ' + port + ' -u '+ user + ' -p' + password + ' ' + database + ' -e "' + sql + '"'
    #print(command)
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
    # print(results)
    results0_lower = results[0].lower()  # 解决大小写问题
    list_results0_lower = results0_lower.decode("utf-8").strip().split("\t")

    if "ckbp" in list_results0_lower and "kpi" in list_results0_lower and "value" in list_results0_lower:
        index_ckbp = list_results0_lower.index("ckbp")
        index_kpi = list_results0_lower.index("kpi")
        index_value = list_results0_lower.index("value")
    else:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||SQL should include :'ckbp' 'kpi' 'value'" % mpoint)
        sys.exit(0)

    for r in results[1:]:
        if "mkbp" in list_results0_lower:
            mpoint = r.decode("utf-8").split("\t")[list_results0_lower.index("mkbp")].strip()
        else:
            mpoint = "-".join([ip, port, database])
        ckbp = r.decode("utf-8").split("\t")[index_ckbp].strip()
        kpi = r.decode("utf-8").split("\t")[index_kpi].strip()
        value = r.decode("utf-8").split("\t")[index_value].strip()

        ckbp = "" if ckbp.lower() == "null" else ckbp
        kpi = "kpi is null" if kpi == "" or kpi.lower() == "null" else kpi  # kpi 和value为"" 或者为 "null"时 输出提示 is null
        value = "value is null" if value == "" or value.lower() == "null" else value

        print(separator.join([mpoint, ckbp, kpi, value]))
