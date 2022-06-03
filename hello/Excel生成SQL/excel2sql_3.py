# coding: utf-8

import sys
import time
from openpyxl import load_workbook

"""
用于Go-agent项目读取excel文件生成sql   Oracle数据库专用
By：李家昌  最后修改：2018.04.18
"""

#######################################################################
data = load_workbook(u"UltraAgent脚本信息集.xlsx")  # 读取excel表
sheet = data[u"MySQL"]                              # 读取表名
file_sql = "mysql_0417_for_oracle.sql"         # 生成的sql文件
#######################################################################

# 计算实际行数real_rows 即非空行
real_rows = 0
for i in sheet["D"]:
    if i.value is not None:
        real_rows += 1
print("非空行数：%s" % real_rows)

monitorType, scriptPath, scriptName, parameterName, parameterDescr, parameterDataType, parameterDataScope, \
isRequired, isEncrypted, defaultValue, execsEquence, note, kpi, scriptId, adaptos, creator, scriptType = [""] * 17


def updata_data(row_index, is_super=1):
    global monitorType, scriptPath, scriptName, parameterName, parameterDescr, parameterDataType, parameterDataScope, isRequired, isEncrypted, defaultValue, execsEquence, note, kpi, scriptId, adaptos, creator, scriptType
    e = sheet[row_index]
    kpi = e[13].value   # 每次循环都更新 kpi内数据 3.19 （解决合并单元格，第二行重复添加 kpi）
    if is_super == 1:
        if e[0].value is not None:
            monitorType = e[0].value
            scriptPath = e[1].value.replace("\\", "/")  # 替换 \  为 /
        scriptName = e[2].value
        #kpi = e[13].value
    else:
        print("is_not_super")

    parameterName = "" if e[4].value is None else str(e[4].value)  # 参数名称
    parameterDescr = "" if e[5].value is None else str(e[5].value)  # 参数描述
    parameterDataType = "" if e[6].value is None else str(e[6].value)  # 参数储存类型
    parameterDataScope = "" if e[7].value is None else str(e[7].value)  # 参数范围
    isRequired = "1" if e[8].value == u"是" else "0"  # 是否必填
    isEncrypted = "1" if e[9].value == u"是" else "0"  # 是否加密
    defaultValue = "" if e[10].value is None else str(e[10].value)  # 默认值
    execsEquence = "" if e[11].value is None else str(e[11].value)  # 执行顺序  直接取到的是float...
    note = "" if e[12].value is None else str(e[12].value)  # 参数说明
    print("scriptPath %s", scriptPath)
    print("scriptName %s", scriptName)
    scriptId = scriptPath + "/" + scriptName   # 替换 \  为 /
    adaptos = "linux"  # 平台，暂时只有Linux
    creator = e[3].value  # 所属用户
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
    updata_data(row_index, is_super=is_super)
    sql_file = open(file_sql, "a")

    createrTime = str(int(round(time.time() * 1000)))  # 毫秒级当前时间戳  创建时间
    updateTime = "0"
    isFormat = "1"

    if is_super == 1:
        sql_file.write(
            "-- DELETE FROM ua_plugin_info WHERE scriptName = '" + scriptName + "' and SCRIPTPATH ='" + scriptPath + "';\n"
            + "INSERT INTO ua_plugin_info(SCRIPTPATH, SCRIPTNAME, SCRIPTID, ADAPTOS, CREATOR, scriptType, createrTime, updateTime, isFormat) VALUES"
            + " ('" + scriptPath + "','" + scriptName + "','" + scriptId + "','" + adaptos + "','" + creator + "','" + scriptType + "','" + createrTime + "','" + updateTime + "','" + isFormat +"');\n")

    # 如果没有<输出pki>和<参数名称>，只要一个ua_plugin_info语句，剩下的跳过
    if kpi is None and parameterName == "":
        return

    # 如果 执行顺序 为空，跳过执行 UA_SCRIPT_PARAM语句
    if execsEquence != "":
        sql_file.write("-- DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = '" + scriptId + "';\n"
                       + "INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDESCR, PARAMETERDATATYPE,"
                       + " PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, "
                       + "VIEWSEQUENCE, NOTE) VALUES" + " ('" + scriptId + "','" + parameterName + "','" + parameterDescr + "','" + parameterDataType + "','"
                       + parameterDataScope + "'," + isRequired + "," + isEncrypted + ",'"
                       + defaultValue + "','" + execsEquence + "','" + execsEquence + "','" + note + "'" + "); \n\n")

    # 如果没有<输出pki>，只要ua_plugin_info和UA_SCRIPT_PARAM 语句，剩下的跳过
    if kpi is None:
        return

    kpis = kpi.split("\n")
    i = 0
    for k in kpis:
        kpi_info = k.split("|")
        kpi_id = kpi_info[0]
        cn_name = kpi_info[1]
        data_type = kpi_info[2]
        unit = kpi_info[3]
        kpi_no = str(int(round(time.time() * 1000)) + i)  # 毫秒级当前时间戳
        sql_file.write("-- DELETE FROM kpi_info WHERE KPI_NO = " + kpi_no + "; \n"
                       + "insert into KPI_INFO (KPI_NO,KBP_CLASS, KPI_ID, KPI_EN_NAME, KPI_CN_NAME, KPI_EN_DESCR, KPI_CN_DESCR, KPI_TYPE, KPI_UNIT,EXT_DATASOURCE)"
                       + " values (" + kpi_no + ", '" + monitorType + "', '" + kpi_id + "', '" + kpi_id + "', '" + cn_name + "', '" + kpi_id + "', '" + cn_name + "', '"
                       + data_type + "','" + unit + "','PATROL'); \n")
        i += 1

    for k in kpis:
        kpi_info = k.split("|")
        kpi_id = kpi_info[0]
        sql_file.write("-- DELETE FROM UA_PLUGIN_KPI WHERE KPIID = '"
                       + kpi_id + "' AND SCRIPTID ='"
                       + scriptId + "'; \n"
                       + "INSERT INTO UA_PLUGIN_KPI(KPIID,SCRIPTID) VALUES"
                       + " ('"
                       + kpi_id + "','" + scriptId + "'); \n")
    sql_file.write("\n")
    sql_file.close()


if __name__ == "__main__":
    f = open(file_sql, "w")  # 清空
    f.close()

    i = 2
    while i <= real_rows:
        if sheet["C"][i - 1].value:
            write_sql(i)

        else:
            write_sql(i, is_super=0)

        i += 1
    else:
        with open(file_sql, "a") as f:
            f.write("commit;")

