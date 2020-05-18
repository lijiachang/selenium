# coding:utf-8
import os
import sys

"""
By 李家昌，2018.04.17
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


if __name__ == "__main__":
    sqlComm = """SELECT 'Short to Long Full Table Scans' "Ratio",
                       ROUND((SELECT SUM(value)
                                FROM v\$SYSSTAT
                               WHERE name = 'table scans (short tables)') /
                             (SELECT SUM(value)
                                FROM v\$SYSSTAT
                               WHERE name IN ('table scans (short tables)',
                                      'table scans (long  tables)')) * 100,
                             2) || '%' "Percentage"
                  FROM DUAL
                UNION
                SELECT 'Short Table Scans ' "Ratio",
                       ROUND((SELECT SUM(value)
                                FROM v\$SYSSTAT
                               WHERE name = 'table scans (short tables)') /
                             (SELECT SUM(value)
                                FROM v\$SYSSTAT
                               WHERE name IN
                                     ('table scans (short tables)',
                                      'table scans (long tables)', 'table fetch by rowid')) * 100,
                             2) || '%' "Percentage"
                  FROM DUAL
                UNION
                SELECT 'Long Table Scans ' "Ratio",
                       ROUND((SELECT SUM(value)
                                FROM v\$SYSSTAT
                               WHERE name = 'table scans (long tables)') /
                             (SELECT SUM(value)
                                FROM v\$SYSSTAT
                               WHERE name IN
                                     ('table scans (short tables)',
                                      'table scans (long  tables)', 'table fetch by rowid')) * 100,
                             2) || '%' "Percentage"
                  FROM DUAL
                UNION
                SELECT 'Table by Index ' "Ratio",
                       ROUND((SELECT SUM(value)
                                FROM v\$SYSSTAT
                               WHERE name = 'table fetch by rowid') /
                             (SELECT SUM(value)
                                FROM v\$SYSSTAT
                               WHERE name IN
                                     ('table scans (short tables)',
                                      'table scans (long  tables)', 'table fetch by rowid')) * 100,
                             2) || '%' "Percentage"
                  FROM DUAL
                UNION
                SELECT 'Efficient Table Access ' "Ratio",
                       ROUND((SELECT SUM(value)
                                FROM v\$SYSSTAT
                               WHERE name IN
                                     ('table scans (short tables)', 'table fetch by rowid')) /
                             (SELECT SUM(value)
                                FROM v\$SYSSTAT
                               WHERE name IN
                                     ('table scans (short tables)',
                                      'table scans (long  tables)', 'table fetch by rowid')) * 100,
                             2) || '%' "Percentage"
                  FROM DUAL;"""  # 符号$ 需要转义
    result = QueryBySqlPlus(sqlComm)

    # 重新组成字典数据，方便查询
    values_dict = dict()
    for i in result:
        values_dict.update({i.values()[1]:i.values()[0]})

    mpoint = "-".join([hostip, port, ins])
    ckbp = ""
    separator = "||"
    wrap = "\n"

    results = list()
    results.append(separator.join([mpoint, ckbp, "APM-00-03-01-00-12", values_dict.get("Long Table Scans")]))  # 全表扫描百分比(%)LongScanRatio

    for r in results:
        print(r)
