# coding:utf-8
# 2019.09.12
import psycopg2
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

# hostip = "192.168.181.83"
# port = "5432"
# servername = "postgres"
# username = "postgres"
# password = "ultrapower"
# mpoint = "-".join([hostip, port, servername])
# sql = "SELECT id as mpoint, name as ckbp, address as PM02, salary as PM03  from COMPANY"

try:
    conn = psycopg2.connect(database=servername, user=username, password=password, host=hostip, port=port)
except Exception as e:
    print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
    sys.exit(0)
# print "Opened database successfully"

# 查
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
#
# for row in rows:
#     print row
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
