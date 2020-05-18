# coding:utf-8
import os
import sys

"""
oracle 通用脚本，参数传入SQL
By 李家昌，2018.05.04
"""

try:
    hostip = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    ins = sys.argv[5]
    sql = sys.argv[6]
    gStrConnection = username + '/' + password + '@' + hostip + ':' + port + '/' + ins
    print(gStrConnection)
    print(sql)
except Exception, e:
    print('Usage:%s hostip port username password  servername' % sys.argv[0])
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
    strCommand = 'sqlplus -S %s <<!\n' % gStrConnection
    strCommand = strCommand + 'set linesize 32767\n'
    strCommand = strCommand + 'set pagesize 9999\n'
    strCommand = strCommand + 'set term off verify off feedback off tab off \n'
    strCommand = strCommand + 'set numwidth 40\n'
    strCommand = strCommand + sqlCommand + '\n'
    strCommand = strCommand + 'exit\n'
    strCommand = strCommand + '!\n'
    result = os.popen(strCommand)
    list = []
    for line in result:
        list.append(line)
    if 'ERROR' in list[2]:
        print(list[3])
        sys.exit(1)
    elif 'ERROR' in list[0]:
        print(list[1])
        sys.exit(1)
    else:
        return parseQueryResult(list)


# if __name__ == "__main__":
#     sqlComm = "select sum(w.count) wait from v\$waitstat w  ;"  # 符号$需要转义
#     wait = QueryBySqlPlus(sqlComm)
#     sqlComm = "select sum(s.value)  read  from v\$sysstat s where s.name='session logical reads';"  # 符号$需要转义
#     read = QueryBySqlPlus(sqlComm)
#     result = float(wait[0].values()[0]) / float(read[0].values()[0]) * 100 # 保留两位小数
#
#     mpoint = "-".join([hostip, port, ins])
#     ckbp = ""
#     separator = "||"
#     wrap = "\n"
#     results = separator.join([mpoint, ckbp, "APM-00-03-01-00-07", str(result)])  # 缓冲池繁忙率
#     print(results)