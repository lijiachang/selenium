# coding:utf-8
import os
import sys
import subprocess

"""
By 李家昌，2018.04.27
windows 环境专用
"""

try:
    hostip = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    ins = sys.argv[5]
    gStrConnection = username + '/' + password + '@' + hostip + ':' + port + '/' + ins
except Exception, e:
    print('Usage:%s hostip port username password servername' % sys.argv[0])
    sys.exit(0)



def parseQueryResult(listQueryResult):
    listResult = []
    if len(listQueryResult) < 4:
        return listResult
    listStrTmp = listQueryResult[2].split(' ')
    listIntWidth = []
    for oneStr in listStrTmp:
        listIntWidth.append(len(oneStr))
        listStrFieldName = []
        iLastIndex = 0
        lineFieldNames = listQueryResult[1]
    for iWidth in listIntWidth:
        strFieldName = lineFieldNames[iLastIndex:iLastIndex + iWidth]
        strFieldName = strFieldName.strip()
        listStrFieldName.append(strFieldName)
        iLastIndex = iLastIndex + iWidth + 1
    for i in range(3, len(listQueryResult)):
        oneLiseResult = unicode(listQueryResult[i], 'UTF-8')
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
    f = open("tmp.sql", "w")
    f.write("set linesize 32767\n")
    f.write("set pagesize 9999\n")
    f.write("set numwidth 40\n")
    f.write(sqlCommand + "\n")
    f.write("exit")
    f.close()

    strCommand = "sqlplus -S %s @tmp.sql" % gStrConnection
    result = os.popen(strCommand)
    list1 = []
    for line in result:
        list1.append(line)
    if 'ERROR' in list1[2]:
        print("ERROR")
        sys.exit(0)
    elif 'ERROR' in list1[0]:
        print("ERROR")
        sys.exit(0)
    else:
        return parseQueryResult(list1)



if __name__ == "__main__":
    sqlComm = "select sum(w.count) wait from v$waitstat w  ;"  # 符号$需要转义
    wait = QueryBySqlPlus(sqlComm)
    sqlComm = "select sum(s.value)  read  from v$sysstat s where s.name='session logical reads';"  # 符号$需要转义
    read = QueryBySqlPlus(sqlComm)
    result = float(wait[0].values()[0]) / float(read[0].values()[0]) * 100  # 保留两位小数

    mpoint = "-".join([hostip, port, ins])
    ckbp = ""
    separator = "||"
    wrap = "\n"
    results = separator.join([mpoint, ckbp, "APM-00-03-01-00-07", str(result)])  # 缓冲池繁忙率
    print(results)
