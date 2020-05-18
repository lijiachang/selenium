# coding:utf-8
import os
import sys


# By li 2018.09.12
# support python3
# Oracle Status
# 	0 正常
# 	1 服务名错误
# 	2 用户名密码错误
# 	3 IP端口错误


"""
By 2018.10.14
support python3
"""

try:
    hostip = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    ins = sys.argv[5]
    mpoint = "-".join([hostip, port, ins])
    gStrConnection = username + '/' + password + '@' + hostip + ':' + port + '/' + ins
    if hostip == "0.0.0.0":
        mpoint = port
        gStrConnection = username + '/' + password + "@'" + ins + "'"

except Exception as e:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s hostip port username password  servername" % (
        sys.argv[0], sys.argv[0]))
    sys.exit(0)

try:
    import cx_Oracle
except ImportError as e:
    model = 'sqlplus'
else:
    model = 'module'
# model = 'sqlplus'



def QueryByModule(sqlComm):
    sqlComm = sqlComm[:-1] if sqlComm.strip()[-1] == ";" else sqlComm  # del ;

    try:
        if hostip == "0.0.0.0":
            db = cx_Oracle.connect(username, password, ins, encoding="UTF-8")  # 服务名方式
        else:
            db = cx_Oracle.connect(username, password, '{0}:{1}/{2}'.format(hostip, port, ins),
                                   encoding="UTF-8")  # 实例名方式,数据库名
    except Exception as e:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
        sys.exit(0)
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

def parseQueryResult(listQueryResult):
    listResult = []
    if len(listQueryResult) < 4:
        return listResult
    listStrTmp = listQueryResult[2].split(' ')
    listIntWidth = []
    listStrFieldName = []
    iLastIndex = 0
    lineFieldNames = listQueryResult[1]
    for oneStr in listStrTmp:
        listIntWidth.append(len(oneStr))
    listIntWidth[-1] += 10  # 180730解决中文显示
    for iWidth in listIntWidth:
        strFieldName = lineFieldNames[iLastIndex:iLastIndex + iWidth]
        strFieldName = strFieldName.strip()
        listStrFieldName.append(strFieldName)
        iLastIndex = iLastIndex + iWidth + 1
    for i in range(3, len(listQueryResult)):
        oneLiseResult = listQueryResult[i]
        # oneLiseResult = unicode(listQueryResult[i], 'UTF-8') # 180730解决中文显示
        fieldMap = {}
        iLastIndex = 0
        for j in range(len(listIntWidth)):
            strFieldValue = oneLiseResult[iLastIndex:iLastIndex + listIntWidth[j]]
            strFieldValue = strFieldValue.strip()
            fieldMap[listStrFieldName[j]] = strFieldValue
            iLastIndex = iLastIndex + listIntWidth[j] + 1
        listResult.append(fieldMap)
    return listResult


def QueryBySqlPlus(sqlCommand):
    global gStrConnection
    strCommand = 'sqlplus -S %s 2>&1 <<!\n' % gStrConnection  # 错误输出重定向到标准输出2>&1  18.09.12
    strCommand = strCommand + 'set linesize 32767\n'
    strCommand = strCommand + 'set pagesize 9999\n'
    strCommand = strCommand + 'col KPI format a40;\n'
    strCommand = strCommand + 'col CKBP format a40;\n'
    # strCommand = strCommand + 'col VALUE format a40;\n'
    strCommand = strCommand + 'set term off verify off feedback off tab off \n'
    strCommand = strCommand + 'set numwidth 40\n'
    strCommand = strCommand + sqlCommand + '\n'
    strCommand = strCommand + 'exit\n'
    strCommand = strCommand + '!\n'
    result = os.popen(strCommand)
    list_1 = []
    for line in result:
        list_1.append(line)

    if not list_1:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||table result in null !" % mpoint)  # 空表输出结果
        sys.exit(0)
    if 'sh: sqlplus' in list_1[0]:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, list_1[0].strip()))  # sqlplus: command not found 18.09.12
        sys.exit(0)
    if 'sh: sqlplus' in list_1[0]:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, list_1[0].strip()))  # sqlplus: command not found 18.09.12
        sys.exit(0)
    if 'ERROR' in list_1[0]:
        if "ORA-12514" in list_1[1]:
            print("%s||||PM-oracle-status||1" % mpoint)
        elif "ORA-01017" in list_1[1]:
            print("%s||||PM-oracle-status||2" % mpoint)
        elif "ORA-12541" in list_1[1]:
            print("%s||||PM-oracle-status||3" % mpoint)
        elif "ORA-12543" in list_1[1]:
            print("%s||||PM-oracle-status||3" % mpoint)
        elif "ORA-12545" in list_1[1] or "ORA-12154" in list_1[1]:
            print("%s||||PM-oracle-status||3" % mpoint)
        else:
            print("%s||||FM-PLUGIN-EXECUTE-FAILED||Unknown Error:%s" % (mpoint, list_1[1]))
        sys.exit(0)
    else:
        return parseQueryResult(list_1)


if __name__ == "__main__":
    separator = "||"
    ckbp = ""
    sqlComm = "select status from v\$instance;"

    if model == 'sqlplus':
        result = QueryBySqlPlus(sqlComm)
    elif model == 'module':
        sqlComm = sqlComm.replace("v\$", "v$")
        result = QueryByModule(sqlComm)
    else:
        result = []


    if "unknown" in result[0]:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||please check your sql, unknown error!" % mpoint)
        sys.exit(0)

    status = result[0].get("STATUS")
    if status in "OPEN MIGRATE":
        result = "0"
    elif status in "STARTED":
        result = "5"
    elif status in "MOUNTED":
        result = "6"

    print(separator.join([mpoint, ckbp, "PM-oracle-status", result]))

# 5: STARTED已启动/不装载（NOMOUNT）。启动实例，但不装载数据库。
# 该模式用于重新创建控制文件，对控制文件进行恢复或重新创建数据库。
# 6: MOUNTED已装载（MOUNT）。装载数据库，但不打开数据库。
# 该模式用于更改数据库的归档模式或执行恢复操作，数据文件的恢复。
