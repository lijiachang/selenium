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
    sqlComm = """select trannums,max_trans,trannums/max_trans*100 as tran_used_percent,procnums,max_procs, trunc(procnums/max_procs*100,2) as proc_used_percent
                from (select count(*) as trannums from v\$transaction),
                (select value as max_trans from v\$parameter where name='transactions'),
                (select count(*) as procnums from v\$process),
                (select value as max_procs from v\$parameter where name='processes');"""  # 符号$ 需要转义
    result = QueryBySqlPlus(sqlComm)

    mpoint = "-".join([hostip, port, ins])
    ckbp = ""
    separator = "||"
    wrap = "\n"

    results = list()
    results.append(separator.join([mpoint, ckbp, "APM-00-03-01-00-27", result[0].get("TRAN_USED_PERCENT")]))  # 事务数利用率

    for r in results:
        print(r)
