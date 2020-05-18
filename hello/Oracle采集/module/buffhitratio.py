# coding:utf-8
import cx_Oracle
import sys

"""
By 2019.09.27
"""

try:
    hostip = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    ins = sys.argv[5]
    mpoint = "-".join([hostip, port, ins])
except Exception as e:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s hostip port username password  servername" % (
        sys.argv[0], sys.argv[0]))
    sys.exit(0)

try:
    if hostip == "0.0.0.0":
        db = cx_Oracle.connect(username, password, ins, encoding="UTF-8")  # 服务名方式
    else:
        db = cx_Oracle.connect(username, password, '{0}:{1}/{2}'.format(hostip, port, ins), encoding="UTF-8")  # 实例名方式,数据库名
except Exception as e:
    print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
    sys.exit(0)

def QueryBySqlPlus(sqlComm):
    sqlComm = sqlComm[:-1] if sqlComm.strip()[-1] == ";" else sqlComm  # del ;
    cur = db.cursor()
    try:
        cur.execute(sqlComm)
    except Exception as e:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
        sys.exit(0)
    columns = [i[0] for i in cur.description]  # col整理
    result = cur.fetchall()
    # print(result)
    result = [dict(zip(columns, row)) for row in result]
    if result:
        return result
    else:
        return [dict([(col, "null") for col in columns])]


sqlComm = "select round((1 -(physical.value - direct.value - lobs.value) / logical.value) * 100,2) ratio from V$sysstat physical,V$sysstat direct, V$sysstat lobs, V$sysstat logical where physical.name = 'physical reads' and direct.name = 'physical reads direct' and lobs.name = 'physical reads direct (lob)' and logical.name = 'session logical reads';"
queryresult = QueryBySqlPlus(sqlComm)

ckbp = ""
separator = "||"
wrap = "\n"

results = list()
results.append(separator.join([mpoint, ckbp, "AFM-00-03-01-00-12", str(queryresult[0].get("RATIO"))]))
for r in results:
    print(r)
