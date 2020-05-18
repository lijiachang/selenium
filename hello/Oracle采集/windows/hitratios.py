# coding:utf-8
import os
import sys

"""
By 李家昌，2018.04.16
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
    sqlComm = """select a.cache_hit_percent, e.rowcache_hitratio, d.get_ratio_percent
              from (SELECT ROUND((1 - ((s1.VALUE - s4.VALUE - s5.VALUE) /
                                 (s2.VALUE + s3.VALUE - s4.VALUE - s5.VALUE))) * 100,
                                 2) cache_hit_percent
                      FROM v\$sysstat s1,
                           v\$sysstat s2,
                           v\$sysstat s3,
                           v\$sysstat s4,
                           v\$sysstat s5
                     WHERE s1.NAME = 'physical reads'
                       AND s2.NAME = 'consistent gets'
                       AND s3.NAME = 'db block gets'
                       AND s4.NAME = 'physical reads direct (lob)'
                       AND s5.NAME = 'physical reads direct') a,
                   (select round(100 * (1 - sum(misses) / sum(gets)), 2) latch_ratio_percent
                      from v\$latch) b,
                   (select round(100 * (a.get_ratio / b.total), 2) get_ratio_percent
                      from (select sum(gethitratio) get_ratio from v\$LIBRARYCACHE) a,
                           (select count(*) total from v\$LIBRARYCACHE) b) d,
                   (select round(100 * (1 - sum(getmisses) / sum(gets)), 2) rowcache_hitratio
                      from v\$rowcache) e,
                   (SELECT round(100 * s1.VALUE / (s2.VALUE + s1.VALUE), 2) mem_sort_percent
                      FROM v\$sysstat s1, v\$sysstat s2
                     WHERE s1.NAME = 'sorts (memory)'
                       AND s2.NAME = 'sorts (disk)') f;"""  # 符号$ 需要转义
    result = QueryBySqlPlus(sqlComm)

    mpoint = "-".join([hostip, port, ins])
    ckbp = ""
    separator = "||"
    wrap = "\n"
    results = list()
    results.append(separator.join([mpoint, ckbp, "APM-00-03-01-00-08", result[0].get("CACHE_HIT_PERCENT")]))  # 缓冲池命中率
    results.append(separator.join([mpoint, ckbp, "APM-00-03-01-00-09", result[0].get("ROWCACHE_HITRATIO")]))  # 数据字典命中率
    results.append(separator.join([mpoint, ckbp, "APM-00-03-01-00-34", result[0].get("GET_RATIO_PERCENT")]))  # 库缓存命中率

    for r in results:
        print(r)
