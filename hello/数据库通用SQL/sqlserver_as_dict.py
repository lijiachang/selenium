# coding:utf-8
# 2019.12.18.  15:30
import pymssql
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

try:
    hostip = sys.argv[1].strip()
    port = sys.argv[2].strip()
    username = sys.argv[3]
    password = sys.argv[4]
    servername = sys.argv[5]
    #sql = sys.argv[6]
    mpoint = "-".join([hostip, port, servername])
except Exception as e:
    print('Usage:%s Hostip Port Username Password  DatabaseName SQL' % sys.argv[0])
    sys.exit(0)

sql = u"""select '三亚候鸟--产生告警_PM_YW_SQL_0294' as CKBP,
       count(1) as "PM_YW_SQL_0294",
       case when count(1) =0 then '三亚候鸟没有产生告警' else 
       STUFF(
       (SELECT '*****' + alarm_text FROM f_syhouniao_alarm_detail 
       WHERE DATEDIFF (minute,alarm_time,getdate())<=20 and alarm_tag=1  
       FOR XML PATH('')), 1, 1, '') end as TITLE 
       from f_syhouniao_alarm_detail 
       where DATEDIFF (minute,alarm_time,getdate())<=20 
       and alarm_tag=1
"""

conn = pymssql.connect(hostip + ":" + port, username, password, servername , charset='cp936')  # 获取连接


cursor = conn.cursor()


cursor.execute(sql.encode('cp936'))

columns = [i[0] for i in cursor.description]  # col整理
columns = [s.lower() for s in columns]

rows = cursor.fetchone()

print("中文测试")
print rows
print rows[0]
print rows[0].encode("utf-8")
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
        print(separator.join([str(mpoint), str(ckbp), column, row[columns.index(column)]]))
        print(separator.join([str(mpoint), str(ckbp), column, row[columns.index(column)].encode("utf-8") ]))
