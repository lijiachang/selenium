# coding:utf-8
# 2019.10.11

import pymysql
import sys

################################################
stdi, stdo, stde = sys.stdin, sys.stdout, sys.stderr
reload(sys)
sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
sys.setdefaultencoding('utf-8')
################################################

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

# ip = "192.168.120.104"
# port = "3306"
# mpoint = "-".join([ip, port, "MySQL"])
# conn = pymysql.connect(host="192.168.120.104", port=3306, user="root", passwd="mysqlmima", db="basedb", charset='utf8')
# sql = "SELECT DBFIELDNAME  as ckbp , MIBOID as PM_01, MIBNAME as PM_02  from collect_oids;"

try:
    conn = pymysql.connect(host=hostip, port=int(port), user=username, passwd=password, db=servername, charset='utf8')
except Exception as e:
    print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
    sys.exit(0)

cur = conn.cursor()
try:
    cur.execute(sql)
except Exception as e:
    print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
    sys.exit(0)
# print cur.rowcount  # 数据行数

columns = [i[0] for i in cur.description]  # col整理
columns = [s.lower() for s in columns]

rows = cur.fetchall()

conn.close()

separator = "||"
for row in rows:
    ckbp = ""
    if "ckbp" in [s.lower() for s in columns]:
        ckbp = row[columns.index("ckbp")]
    if "mpoint" in [s.lower() for s in columns]:
        mpoint = row[columns.index("mpoint")]
    for column in columns:
        if column.lower() == "ckbp":
            continue
        if column.lower() == "mpoint":
            continue
        print(separator.join([str(mpoint), str(ckbp), column, str(row[columns.index(column)])]))
