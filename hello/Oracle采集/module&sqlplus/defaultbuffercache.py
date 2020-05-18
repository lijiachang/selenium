#!/usr/bin/env python
# coding:utf-8
import os
import platform
import sys

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
    strCommand = strCommand + 'set term off verify off feedback off tab off \n'
    strCommand = strCommand + 'set numwidth 40\n'
    strCommand = strCommand + sqlCommand + '\n'
    strCommand = strCommand + 'exit\n'
    strCommand = strCommand + '!\n'
    result = os.popen(strCommand)
    list_1 = []
    for line in result:
        list_1.append(line)

    # print(list_1)
    if not list_1:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||table result in null !" % mpoint)  # 空表输出结果
        sys.exit(0)
    if 'sh: sqlplus' in list_1[0]:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, list_1[0].strip()))  # sqlplus: command not found 18.09.12
        sys.exit(0)
    if "unknown" in list_1[0]:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||please check your sql , Error code: %s" % (mpoint, list_1[0]))
        sys.exit(0)
    elif 'ERROR' in list_1[2]:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||please check your sql ,Error infor: %s" % (mpoint, list_1[3]))
        sys.exit(0)
    elif 'ERROR' in list_1[0]:
        if "ORA-12514" in list_1[1]:
            print("%s||||FM-PLUGIN-EXECUTE-FAILED||Error code:ORA-12514, please check servername : %s" % (mpoint, ins))
        elif "ORA-01017" in list_1[1]:
            print("%s||||FM-PLUGIN-EXECUTE-FAILED||Error code:ORA-01017, please check username or password : %s %s" % (
                mpoint, username, password))
        elif "ORA-12541" in list_1[1]:
            print("%s||||FM-PLUGIN-EXECUTE-FAILED||Error code:ORA-12541, please check ip port : %s %s" % (
                mpoint, hostip, port))
        elif "ORA-12543" in list_1[1]:
            print("%s||||FM-PLUGIN-EXECUTE-FAILED||Error code:ORA-12543, please check ip : %s" % (mpoint, hostip))
        else:
            print("%s||||FM-PLUGIN-EXECUTE-FAILED||Unknown Error: %s" % (mpoint, list_1[1]))
        sys.exit(0)
    else:
        return parseQueryResult(list_1)


sqlVersion = "select * from PRODUCT_COMPONENT_VERSION where Product = 'NLSRTL ';"
sqlComm = "select name, round(value / 1024 / 1024) from V$parameter where name = 'log_buffer';"
if model == 'sqlplus':
    queryversion = QueryBySqlPlus(sqlVersion)
elif model == 'module':
    sqlVersion = sqlVersion.replace("v\$", "v$")
    queryversion = QueryByModule(sqlVersion)
else:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||not find sqlplus or python-cx_Oracle" )
    sys.exit(0)

ver = ""
for j in queryversion:
    ver = str(list(j.values())[2])
if ver == "11.2.0.1.0":
    sqlComm = "select component,current_size/1024/1024 cur_size_M  from  V$memory_dynamic_components where component = 'DEFAULT buffer cache';"
else:
    sqlComm = "select component, current_size / 1024 / 1024 cur_size_M from V$sga_dynamic_components where component = 'DEFAULT buffer cache';"

if model == 'sqlplus':
    result = QueryBySqlPlus(sqlComm)
elif model == 'module':
    sqlComm = sqlComm.replace("v\$", "v$")
    sqlComm = sqlComm.replace("V\$", "v$")
    result = QueryByModule(sqlComm)
else:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||not find sqlplus or python-cx_Oracle")
    sys.exit(0)


ckbp = ""
separator = "||"
wrap = "\n"

results = list()
results.append(separator.join([mpoint, ckbp, "ACM-00-03-01-00-46", str(result[0].get("CUR_SIZE_M"))]))

for r in results:
    print(r)
