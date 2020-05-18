# coding:utf-8
# 2019.09.18
import pymssql
import sys
import platform

pythonver=platform.python_version()
if pythonver.startswith('2'):
    reload(sys)
    sys.setdefaultencoding('utf-8')


try:
    hostip = sys.argv[1].strip()
    port = sys.argv[2].strip()
    username = sys.argv[3]
    password = sys.argv[4]
    servername = sys.argv[5]
    sql = sys.argv[6]
    sql = unicode(sql, "utf-8")
    mpoint = "-".join([hostip, port, servername])
except Exception as e:
    print('Usage:%s Hostip Port Username Password  DatabaseName SQL' % sys.argv[0])
    sys.exit(0)



# hostip = "192.168.180.88"
# port = "1433"
# username = "sa"
# password = "Ultrapower_123"
# servername = "master"
# mpoint = "-".join([hostip, port, servername])
# sql = "SELECT id as mpoint, name as ckbp, salesrep as PM02, addr as PM03  from persons"

try:
    conn = pymssql.connect(hostip + ":" + port, username, password, servername,charset="cp936")  # 获取连接
except Exception as e:
    print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
    sys.exit(0)

cursor = conn.cursor()
try:
    cursor.execute(sql.encode('cp936'))
except Exception as e:
    print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
    sys.exit(0)

columns_des = [i[0] for i in cursor.description]  # col整理
columns = [s.lower() for s in columns_des]
##print(columns_des)

rows = cursor.fetchall()
# print rows
conn.close()

separator = "||"
for row in rows:
    ckbp = ""
    title = ""
    if "ckbp" in [s.lower() for s in columns]:
        ckbp = row[columns.index("ckbp")]
    if "mpoint" in [s.lower() for s in columns]:
        mpoint = row[columns.index("mpoint")]
    if "title" in columns:
        title = row[columns.index("title")]
        ##title = title.decode("utf8")
    for column in columns_des:
        if column.lower() == "ckbp":
            continue
        if column.lower() == "mpoint":
            continue
        if column.lower() == "title":
            continue
        ##print(separator.join([str(mpoint), str(ckbp), column, str(row[columns.index(column).lower()])]))
        print(separator.join([str(mpoint), str(ckbp), column, str(row[columns.index(column.lower())]), str(title)]))
