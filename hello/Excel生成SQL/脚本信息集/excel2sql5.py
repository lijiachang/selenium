# coding:utf-8

import sys
import time
from openpyxl import load_workbook
reload(sys)
sys.setdefaultencoding('utf-8')


#######################################################################
data = load_workbook(u"UltraAgent脚本信息集-模板.xlsx")  # 读取excel表
sheet = data[u"模板"]                              # 读取表名
file_sql = "test_0515_for_oracle.sql"         # 生成的sql文件
#######################################################################
title_list = list()
for i in sheet[1]:
    title_list.append(i.value)

print title_list.index(u"脚本名")


# 计算实际行数real_rows 即非空行
real_rows = 0
for i in sheet["I"]:
    if i.value is not None:
        real_rows += 1
print("非空行数：%s" % real_rows)

mpointClass, scriptPath, scriptName, scriptNote, parameterName, parameterDescr, parameterDataType, parameterDataScope, \
isRequired, isEncrypted, defaultValue, execsEquence, note, kpi, scriptId, adaptos, creator, scriptType = [""] * 18


def update_data(row_index, is_super=1):
    global mpointClass, scriptPath, scriptName, scriptNote, parameterName, isEncrypted, execsEquence, note, scriptId, adaptos, scriptType
    e = sheet[row_index]

    if is_super == 1:
        if e[title_list.index(u"监控类型")].value is not None:
            mpointClass = e[title_list.index(u"监控类型")].value.strip()  # 监控类型
        scriptName = e[title_list.index(u"脚本名")].value.strip()  # 脚本名
        scriptNote = e[title_list.index(u"脚本说明")].value.strip()  # 脚本说明
    else:
        print("is_not_super")

    adaptos = adaptos if e[title_list.index(u"操作系统")].value is None else str(e[title_list.index(u"操作系统")].value).strip()   # 操作系统
    scriptPath = e[title_list.index(u"脚本路径")].value.replace("\\", "/").strip() if e[title_list.index(u"脚本路径")].value is not None else scriptPath  # 脚本路径
    parameterName = "" if e[title_list.index(u"参数名称")].value is None else str(e[title_list.index(u"参数名称")].value).strip()  # 参数名称
    isEncrypted = "1" if str(e[title_list.index(u"是否加密")].value).strip() == u"是" else "0"  # 是否加密
    execsEquence = "" if e[title_list.index(u"执行顺序")].value is None else str(e[title_list.index(u"执行顺序")].value).strip()  # 执行顺序  直接取到的是float...
    note = "" if e[title_list.index(u"参数说明")].value is None else str(e[title_list.index(u"参数说明")].value).strip()  # 参数说明
    scriptId = scriptPath + "/" + scriptName   # 替换 \  为 /




    # 脚本类型判断:
    if scriptName.split(".")[1] == "sh":
        scriptType = "shell"
    elif scriptName.split(".")[1] == "py":
        scriptType = "python"
    elif scriptName.split(".")[1] == "ps1":
        scriptType = "powershell"
    else:
        scriptType = "Unknown"



def write_sql(row_index, is_super=1, file_sql=file_sql):
    update_data(row_index, is_super=is_super)
    sql_file = open(file_sql, "a")

    createrTime = str(int(round(time.time() * 1000)))  # 毫秒级当前时间戳  创建时间
    updateTime = "0"
    isFormat = "1"

    if is_super == 1:
        sql_file.write(
            "-- DELETE FROM ua_plugin_info WHERE scriptName = '" + scriptName + "' and SCRIPTPATH ='" + scriptPath + "';\n"
            + "INSERT INTO ua_plugin_info(MPOINTCLASS, SCRIPTPATH, SCRIPTNAME, SCRIPTNOTE, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES"
            + " ('" + mpointClass + "','" + scriptPath + "','" + scriptName + "','" + scriptNote + "','" + scriptId + "','" + adaptos + "','"
            + creator + "','" + scriptType + "','" + createrTime + "','" + updateTime + "','" + isFormat + "');\n")

    # 如果没有<输出pki>和<参数名称>，只要一个ua_plugin_info语句，剩下的跳过
    if parameterName == "":
        return

    # 如果 执行顺序 为空，跳过执行 UA_SCRIPT_PARAM语句
    if execsEquence != "":
        sql_file.write("-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = '" + scriptId + "';\n"
                       + "INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE,"
                       + " PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, "
                       + "VIEWSEQUENCE, NOTE) VALUES" + " ('" + scriptId + "','" + parameterName + "','" + parameterDescr + "','" + parameterDataType + "','"
                       + parameterDataScope + "','" + isRequired + "'," + isEncrypted + ",'"
                       + defaultValue + "','" + execsEquence + "','" + execsEquence + "','" + note + "'" + "); \n\n")

    # 如果没有<输出pki>，只要ua_plugin_info和UA_SCRIPT_PARAM 语句，剩下的跳过


if __name__ == "__main__":
    f = open(file_sql, "w")  # 清空
    f.close()

    with open(file_sql, "a") as f:
        f.write("set define off\n")

    i = 2
    while i <= real_rows:
        if sheet["D"][i - 1].value:
            write_sql(i)

        else:
            write_sql(i, is_super=0)

        i += 1
    else:
        print("End：以上输出信息仅供调试bug，请忽略")
        with open(file_sql, "a") as f:
            f.write("commit;")
