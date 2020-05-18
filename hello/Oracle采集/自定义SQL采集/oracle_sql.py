# coding:utf-8
import os
import sys

"""
读取本地文件sql.txt ，执行单条SQL语句，返回执行结果
By 李家昌，2018.04.18
"""


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

    try:
        f = open("sql.txt", "r")
    except IOError:
        print("No such file: sql.txt ; Please write your SQL in sql.txt!")
        sys.exit()

    # 格式处理 ##############################################################
    sql_file = f.readlines()[::-1]  # 倒序读取
    # 默认文件多行取出是list，需要拼接成str
    sql = ""
    for sqls in sql_file:
        sql = sqls + sql
    sql = sql + ";" if sql.strip()[-1] != ";" else sql  # SQL最后自动判断符号; 并追加
    sqlComm = sql.replace("v$", "v\$")  # 符号$ 需要转义,避免多次转义
    #########################################################################

    result = QueryBySqlPlus(sqlComm)
    print(result)

    # # 重新组成字典数据，方便查询
    # values_dict = dict()
    # for i in result:
    #     values_dict.update({i.values()[0]:i.values()[1]})
