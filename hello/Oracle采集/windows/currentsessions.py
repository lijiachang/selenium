# coding:utf-8
import os
import sys

"""
By 李家昌，2018.04.17
windows 环境专用
"""

try:
    username = sys.argv[1]
    password = sys.argv[2]
    hostip = sys.argv[3]
    port = sys.argv[4]
    ins = sys.argv[5]
    gStrConnection = username + '/' + password + '@' + hostip + ':' + port + '/' + ins
except Exception, e:
    print('Usage:%s hostip username password port instanceid' % sys.argv[0])
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
    f = open("tmp.sql", "w+")
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
    print(list1)
    return parseQueryResult(list1)



if __name__ == "__main__":
    sqlComm = """SELECT   resource_name,
                     current_utilization,
                     max_utilization,
                     LIMIT,
                     ROUND (current_utilization / LIMIT * 100) || '%' rate,
                     ROUND (max_utilization / LIMIT * 100) || '%' maxrate
              FROM   (SELECT   resource_name,
                               current_utilization,
                               max_utilization,
                               TO_NUMBER (initial_allocation) LIMIT
                        FROM   v$resource_limit
                       WHERE   resource_name IN ('sessions')
                               AND max_utilization > 0);"""  # 符号$ 需要转义
    result = QueryBySqlPlus(sqlComm)
    print(result)

    mpoint = "-".join([hostip, port, ins])
    ckbp = ""
    separator = "||"
    wrap = "\n"

    # results = list()
    # results.append(separator.join([mpoint, ckbp, "APM-00-03-01-00-26", result[0].get("CURRENT_UTILIZATION")]))  # 当前会话数
    #
    # for r in results:
    #     print(r)
