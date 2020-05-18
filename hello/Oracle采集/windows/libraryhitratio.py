# coding:utf-8
import os
import sys

"""
By 李家昌，2018.04.27
windows 专用
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
        sys.exit(1)
    elif 'ERROR' in list1[0]:
        print("ERROR")
        sys.exit(1)
    else:
        return parseQueryResult(list1)


if __name__ == "__main__":
    sqlComm = """select '' as mkbp, '' as ckbp ,'APM-LibraryHitRatio' as kpi,round(sum(pins - reloads) / sum(pins) * 100, 2) as value from v$librarycache;"""  # windows中不需要转义
    result = QueryBySqlPlus(sqlComm)

    mpoint = "-".join([hostip, port, ins])
    ckbp = ""
    separator = "||"
    wrap = "\n"

    results = list()
    results.append(separator.join([mpoint, ckbp, result[0].values()[-1], result[0].values()[0]]))  # 库缓存命中率

    for r in results:
        print(r)
