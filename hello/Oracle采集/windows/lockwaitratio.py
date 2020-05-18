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
    sqlComm = """select 'prf_' || translate(NAME,' ','_'),
                VALUE
                from V\$SYSSTAT
                where NAME in ('background checkpoints completed',
                               'consistent changes',
                               'consistent gets',
                               'db block changes',
                               'db block gets',
                               'execute count',
                               'recursive calls',
                               'sorts (disk)',
                               'sorts (memory)',
                               'sorts (rows)',
                               'table fetch continued row',
                               'table fetch by rowid',
                               'table scan rows gotten',
                               'user calls',
                               'user commits',
                               'user rollbacks',
                               'DBWR make free requests',
                               'DBWR free buffers found',
                               'DBWR lru scans',
                               'DBWR summed scan depth',
                               'DBWR buffers scanned',
                               'DBWR checkpoints',
                               'DBWR cross instance writes',
                               'DBWR forced writes',
                               'DBWR timeouts',
                               'enqueue requests',
                               'enqueue waits',
                               'enqueue conversions',
                              'enqueue deadlocks',
                               'enqueue releases',
                               'enqueue timeouts');"""  # 符号$ 需要转义
    result = QueryBySqlPlus(sqlComm)
    # 重新组成字典数据，方便查询
    values_dict = dict()
    for i in result:
        values_dict.update({i.values()[0]:i.values()[1]})

    # 算法: enqueue waits的值/enqueue requests的值 变成百分比
    prf_enqueue_waits = values_dict.get("prf_enqueue_waits")
    prf_enqueue_requests = values_dict.get("prf_enqueue_requests")
    lockWaitRatio = float(prf_enqueue_waits) * 100 / float(prf_enqueue_requests)

    mpoint = "-".join([hostip, port, ins])
    ckbp = ""
    separator = "||"
    wrap = "\n"

    results = list()
    results.append(separator.join([mpoint, ckbp, "APM-00-03-01-00-16", str(lockWaitRatio)]))  # 锁请求等待比例 LockWaitRatio
    for r in results:
        print(r)
