# coding:utf-8
import os
import sys
import re

# By lijiachang，2019.10.14
# Oracle sql通用脚本


try:
    hostip = sys.argv[1].strip()
    port = sys.argv[2].strip()
    username = sys.argv[3].strip()
    password = sys.argv[4].strip()
    servername = sys.argv[5].strip()
    sql = sys.argv[6].strip()
    mpoint = "-".join([hostip, port, servername])
    gStrConnection = username + '/' + password + '@' + hostip + ':' + port + '/' + servername

    if hostip == "0.0.0.0":
        mpoint = port
        gStrConnection = username + '/' + password + "@'" + servername + "'"
except Exception as e:
    print('Usage:%s hostip port username password  servername sql' % sys.argv[0])
    sys.exit(0)

# sql语句解析，找出as后的kpi
sql_lists = re.split(r'[,\s]\s*', sql)
# 找到所有“as”的位置下标
as_index = [i for i, x in enumerate(sql_lists) if x == "as"]
kpi_list = list()
for a in as_index:
    if (not sql_lists[a - 1].isdigit()) and ("count" not in sql_lists[a - 1]):
        kpi_list.append(sql_lists[a + 1].replace("'", "").replace('"', ''))
    # as前为纯数字的KPI不能设置a60，否则####


# print(kpi_list)


def parseQueryResult(listQueryResult):
    listResult = []
    if len(listQueryResult) < 4:
        return listResult
    listStrTmp = listQueryResult[2].split(' ')
    listIntWidth = []
    listStrFieldName = []
    iLastIndex = 0
    lineFieldNames = listQueryResult[1]
    for oneStr in listStrTmp:
        listIntWidth.append(len(oneStr))
    listIntWidth[-1] += 10  # 180730解决中文显示
    for iWidth in listIntWidth:
        strFieldName = lineFieldNames[iLastIndex:iLastIndex + iWidth]
        strFieldName = strFieldName.strip()
        listStrFieldName.append(strFieldName)
        iLastIndex = iLastIndex + iWidth + 1
    for i in range(3, len(listQueryResult)):
        oneLiseResult = listQueryResult[i]
        # oneLiseResult = unicode(listQueryResult[i], 'UTF-8') # 180730解决中文显示
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
    strCommand = 'sqlplus -S %s 2>&1 <<!\n' % gStrConnection  # 错误输出重定向到标准输出2>&1  18.09.12
    for kpi_name in kpi_list:
        # if "pm" not in kpi_name.lower():
        strCommand = strCommand + 'col {0} for a60\n'.format(kpi_name)
    strCommand = strCommand + 'set linesize 32767\n'
    strCommand = strCommand + 'set pagesize 9999\n'
    strCommand = strCommand + 'col CKBP format a100;\n'
    strCommand = strCommand + 'set term off verify off feedback off tab off \n'
    strCommand = strCommand + 'set numwidth 40\n'
    strCommand = strCommand + sqlCommand + '\n'
    strCommand = strCommand + 'exit\n'
    strCommand = strCommand + '!\n'
    # print(strCommand)
    result = os.popen(strCommand, "r")
    # result = subprocess.Popen(strCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # result = result.stdout.readlines()
    list_1 = []
    for line in result:
        list_1.append(line)

    if not list_1:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||table result in null !" % mpoint)  # 空表输出结果
        sys.exit(0)
    if 'sh: sqlplus' in list_1[0]:
        print("%s||||PM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, list_1[0].strip()))  # sqlplus: command not found 18.09.12
        sys.exit(0)
    if "unknown" in list_1[0]:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||please check your sql , Error code: %s" % (mpoint, list_1[0]))
        sys.exit(0)
    elif 'ERROR' in list_1[2]:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||please check your sql ,Error infor: %s" % (mpoint, list_1[3]))
        sys.exit(0)
    elif 'ERROR' in list_1[0]:
        if "ORA-12514" in list_1[1]:
            print("%s||||FM-PLUGIN-EXECUTE-FAILED||Error code:ORA-12514, please check servername : %s" % (
                mpoint, servername))
        elif "ORA-01017" in list_1[1]:
            print("%s||||FM-PLUGIN-EXECUTE-FAILED||Error code:ORA-01017, please check username or password : %s %s" % (
                mpoint, username, password))
        elif "ORA-12541" in list_1[1]:
            print("%s||||FM-PLUGIN-EXECUTE-FAILED||Error code:ORA-12541, please check ip port : %s %s" % (
                mpoint, hostip, port))
        elif "ORA-12543" in list_1[1]:
            print("%s||||FM-PLUGIN-EXECUTE-FAILED||Error code:ORA-12543, please check ip : %s" % (mpoint, hostip))
        else:
            print("%s||||FM-PLUGIN-EXECUTE-FAILED||Unknown Error: %s" % (mpoint, list_1[1]))
        sys.exit(0)
    else:
        return parseQueryResult(list_1)


if __name__ == "__main__":
    separator = "||"
    sqlComm = sql.replace("v$", "v\$").replace("V$", "V\$")  # 转义
    if sqlComm[0] == '"':
        sqlComm = sqlComm[1:-1]  # 判断有引号，去掉两个引号
    sqlComm = sqlComm + ";" if sqlComm.strip()[-1] != ";" else sqlComm  # SQL最后自动判断符号; 并追加
    result = QueryBySqlPlus(sqlComm)
    # print(result)
    # oracle返回sql执行结果时，不必大小写问题，SQL语句是小写，返回的结果也是大写，（mysql会返回小写）

    if "unknown" in result[0]:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||please check your sql, unknown error!" % mpoint)
        sys.exit(0)

    # 解决kpi大小写问题
    sql_lower = sql.lower()
    kpi_dict = {}
    for key in result[0].keys():
        a = sql_lower.index(key.lower())  # 起始位置
        b = a + len(key)  # 结束位置
        # print(sql[a:b])
        kpi_dict.update({key: sql[a:b]})

    for r in result:
        # print r
        if "CKBP" in r:
            ckbp = r.get("CKBP")
            del r["CKBP"]
        elif "ckbp" in r:
            ckbp = r.get("ckbp")
            del r["ckbp"]
        else:
            ckbp = ""
        if "MPOINT" in r:
            mpoint = r.get("MPOINT")
            del r["MPOINT"]
        elif "mpoint" in r:
            mpoint = r.get("mpoint")
            del r["mpoint"]
        for key in r.keys():
            kpi = kpi_dict[key]
            value = r[key]
            value = "value is null" if value == "" else value
            value = "0" + value if value[0] == "." else value  # 小数点前面自动加0
            if value != "value is null":  # value 空值不输出
                print(separator.join([mpoint, ckbp, kpi, value]))
