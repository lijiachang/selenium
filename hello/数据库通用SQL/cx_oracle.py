# coding:utf-8
# 2019.10.12
# install oracle client:https://oracle.github.io/odpi/doc/installation.html
import cx_Oracle
import sys

try:
    hostip = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    servername = sys.argv[5]
    sql = sys.argv[6]
    mpoint = "-".join([hostip, port, servername])
except Exception as e:
    print('Usage:%s Hostip Port Username Password  DatabaseName SQL' % sys.argv[0])
    sys.exit(0)

# hostip = "192.168.180.158"
# port = "1521"
# servername = "nmsdb"
# username = "nms60"
# password = "nms60"
# mpoint = "-".join([hostip, port, servername])
# sql = "SELECT '数据上下文' || RESCLASS  as title, OID as mpoint, KPINO as ckbp, VENDOR as PM02, RESCLASS as PM03  from PM_SNMPOID2KPI"

try:
    if hostip == "0.0.0.0":
        # rac模式参数 ：1数据库ip地址，2数据库唯一标识（自定义），3数据库用户名，4数据库密码，5连接串or服务名
        db = cx_Oracle.connect(username, password, servername, encoding="UTF-8")  # 服务名方式
        mpoint = port
    else:
        db = cx_Oracle.connect(username, password, '{0}:{1}/{2}'.format(hostip, port, servername),
                               encoding="UTF-8")  # 实例名方式,数据库名
except Exception as e:
    print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
    sys.exit(0)
cur = db.cursor()

try:
    cur.execute(sql)
except Exception as e:
    print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
    sys.exit(0)

columns = [i[0] for i in cur.description]  # col整理
columns = [s.lower() for s in columns]
# print(columns)
rows = cur.fetchall()

separator = "||"
for row in rows:
    ckbp = ""
    title = ""
    if "ckbp" in columns:
        ckbp = row[columns.index("ckbp")]
    if "mpoint" in columns:
        mpoint = row[columns.index("mpoint")]
    if "title" in columns:
        title = row[columns.index("title")]
    for column in columns:
        if column.lower() == "ckbp":
            continue
        if column.lower() == "mpoint":
            continue
        if column.lower() == "title":
            continue
        print(separator.join([str(mpoint), str(ckbp), column, str(row[columns.index(column)]), str(title)]))
