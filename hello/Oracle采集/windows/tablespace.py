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
    sqlComm = """SELECT D.TABLESPACE_NAME TSNAME,
                   SPACE TSSIZE,
                   SPACE - NVL (FREE_SPACE, 0) TSUSED,
                   ROUND ( (1 - NVL (FREE_SPACE, 0) / SPACE) * 100, 2) USERATIO,
                   FREE_SPACE FREESPACE,
                   AUTOEXTENSIBLE AUTOEXTENSIBLE,
                   BLOCKS MAXBLOCK
              FROM (  SELECT TABLESPACE_NAME,
                             ROUND (SUM (BYTES) / (1024 * 1024), 2) SPACE,
                             MAX (BLOCKS) BLOCKS,
                             DECODE (SUM (DECODE (autoextensible, 'NO', 0, 1)), 0, 'NO','YES') AUTOEXTENSIBLE
                        FROM DBA_DATA_FILES
                    GROUP BY TABLESPACE_NAME
                    having tablespace_name not like 'UNDOTBS%') D,
                   (  SELECT TABLESPACE_NAME,
                             ROUND (SUM (BYTES) / (1024 * 1024), 2) FREE_SPACE
                        FROM DBA_FREE_SPACE
                    GROUP BY TABLESPACE_NAME
                    having tablespace_name not like 'UNDOTBS%') F
             WHERE D.TABLESPACE_NAME = F.TABLESPACE_NAME(+)
            UNION ALL                                                          
            SELECT D.TABLESPACE_NAME TSNAME,
                   SPACE TSSIZE,
                   USED_SPACE TSUSED,
                   ROUND (NVL (USED_SPACE, 0) / SPACE * 100, 2) USERATIO,
                   NVL (FREE_SPACE, 0) FREESPACE,
                   AUTOEXTENSIBLE AUTOEXTENSIBLE,
                   BLOCKS MAXBLOCK
              FROM (  SELECT TABLESPACE_NAME,
                             ROUND (SUM (BYTES) / (1024 * 1024), 2) SPACE,
                             MAX (BLOCKS) BLOCKS,
                             DECODE (SUM (DECODE (autoextensible, 'NO', 0, 1)), 0, 'NO', 'YES') AUTOEXTENSIBLE
                        FROM DBA_TEMP_FILES
                    GROUP BY TABLESPACE_NAME) D,
                   (  SELECT TABLESPACE_NAME,
                             ROUND (SUM (BYTES_USED) / (1024 * 1024), 2) USED_SPACE,
                             ROUND (SUM (BYTES_FREE) / (1024 * 1024), 2) FREE_SPACE
                        FROM v\$TEMP_SPACE_HEADER
                    GROUP BY TABLESPACE_NAME) F
             WHERE D.TABLESPACE_NAME = F.TABLESPACE_NAME(+)
            ORDER BY 4 DESC;"""  # 符号$ 需要转义
    result = QueryBySqlPlus(sqlComm)

    mpoint = "-".join([hostip, port, ins])
    ckbp = ""
    separator = "||"
    wrap = "\n"
    results = list()

    for row in result:
        ckbp = row.get("TSNAME")
        results.append(separator.join([mpoint, ckbp, "ACM-00-03-04-01-01", ckbp]))  # 表空间名称
        results.append(separator.join([mpoint, ckbp, "ACM-00-03-04-01-02", row.get("TSSIZE")]))  # 表空间大小
        # results.append(separator.join([mpoint, ckbp, "", row.get("TSUSED")]))  # 对应kpi信息未找到
        results.append(separator.join([mpoint, ckbp, "APM-00-03-01-00-28", row.get("USERATIO")]))  # 表空间利用率
        results.append(separator.join([mpoint, ckbp, "APM-00-03-04-01-05", row.get("FREESPACE")]))  # 表空间空闲空间
        results.append(separator.join([mpoint, ckbp, "ACM-00-03-04-01-03", row.get("AUT")]))  # 表空间是否自动扩展（AUTOEXTENSIBLE）
        # results.append(separator.join([mpoint, ckbp, "", row.get("MAXBLOCK")]))  # 对应kpi信息未找到

    for r in results:
        print(r)
