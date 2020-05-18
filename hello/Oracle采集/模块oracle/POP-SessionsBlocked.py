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
        db = cx_Oracle.connect(username, password, '{0}:{1}/{2}'.format(hostip, port, ins),
                               encoding="UTF-8")  # 实例名方式,数据库名
except Exception as e:
    print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
    sys.exit(0)


def QueryBySqlPlus(sqlComm):
    sqlComm = sqlComm.strip()[:-1] if sqlComm.strip()[-1] == ";" else sqlComm  # del ;
    cur = db.cursor()
    try:
        cur.execute(sqlComm)
    except Exception as e:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
        sys.exit(0)
    columns = [i[0] for i in cur.description]  # col整理
    result = cur.fetchall()
    result = [dict(zip(columns, row)) for row in result]
    if result:
        return result
    else:
        return [dict([(col, "null") for col in columns])]


if __name__ == "__main__":
    sqlComm = """select (select username from V$session where sid = b.sid) blocked,
       b.sid  SID_BLOCKED,
             a.sid SID_BLOCKER
  from gV$lock a, gV$lock b
 where a.block >0
   and b.request > 0
   and a.id1 = b.id1
   and a.id2 = b.id2;"""
    result = QueryBySqlPlus(sqlComm)
    # print(result)

    mpoint = "-".join([hostip, port, ins])
    ckbp = ""
    separator = "||"
    wrap = "\n"
    results = list()

    for row in result:
        results.append(
            separator.join([mpoint, ckbp, "PM-ORACLE-PERFORMANCE-SessionsBlocked", str(row.get("BLOCKED"))]))

    for r in range(len(results)):
        print(results[r])
