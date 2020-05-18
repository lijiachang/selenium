# coding: utf-8

import sys
import xlrd
import time
from openpyxl import load_workbook

"""
用于Go-agent项目读取excel文件生成sql  ~~~MySQL专用~~~
"""
reload(sys)
sys.setdefaultencoding("utf-8")

data = load_workbook(u"falcon agent检查项2.xlsx")
sheet = data[u"脚本定义"]

# 计算实际行数real_rows 即非空行
real_rows = 0
for i in sheet["D"]:
    if i.value is not None:
        real_rows += 1
print(real_rows)

monitorType, scriptPath, scriptName, parameterName, parameterDataType, parameterDataScope, \
isRequired, isEncrypted, defaultValue, execsEquence, note, kpi, scriptId = [""] * 13


def updata_data(row_index, is_super=1):
    global monitorType, scriptPath, scriptName, parameterName, parameterDataType, parameterDataScope, isRequired, isEncrypted, defaultValue, execsEquence, note, kpi, scriptId
    e = sheet[row_index]
    if is_super == 1:
        if e[0].value is not None:
            monitorType = e[0].value
        scriptPath = e[1].value
        scriptName = e[2].value
        kpi = e[13].value
        print(kpi)
    else:
        print("is 000000000000")

    parameterName = e[5].value
    parameterDataType = e[6].value
    parameterDataScope = str(e[7].value)
    isRequired = "1" if e[8].value == u"是" else "0"
    isEncrypted = "1" if e[9].value == u"是" else "0"
    defaultValue = str(e[10].value)
    execsEquence = str(e[11].value)  # 直接取到的是float...
    note = str(e[12].value)
    print("scriptPath %s", scriptPath)
    print("scriptName %s", scriptName)
    scriptId = scriptPath + "\\" + scriptName


def write_sql(row_index, is_super=1, file_sql="agentCheck2.sql"):
    updata_data(row_index, is_super=is_super)
    sql_file = open(file_sql, "a")
    if is_super == 1:
        sql_file.write(
            "### DELETE FROM ua_plugin_info WHERE scriptName = '" + scriptName + "' and SCRIPTPATH ='" + scriptPath + "';\n"
            + "INSERT INTO ua_plugin_info(SCRIPTPATH, SCRIPTNAME, SCRIPTID) VALUES"
            + " ('" + scriptPath + "','" + scriptName + "','" + scriptId + "');\n")

    sql_file.write("### DELETE FROM UA_SCRIPT_PARAM WHERE SCRIPTID = '" + scriptId + "';\n"
                   + "INSERT INTO UA_SCRIPT_PARAM(SCRIPTID,PARAMETERNAME, PARAMETERDATATYPE,"
                   + " PARAMETERDATASCOPE, ISREQUIRED, ISENCRYPTED, DEFAULTVALUE, EXECSEQUENCE, "
                   + " NOTE) VALUES" + " ('" + scriptId + "','" + parameterName + "','" + parameterDataType + "','"
                   + parameterDataScope + "'," + isRequired + "," + isEncrypted + ",'"
                   + defaultValue + "'," + execsEquence + ",'" + note + "'" + "); \n\n")

    kpis = kpi.split("\n")
    i = 0
    for k in kpis:
        kpi_info = k.split("|")
        kpi_id = kpi_info[0]
        cn_name = kpi_info[1]
        data_type = kpi_info[2]
        unit = kpi_info[3]
        kpi_no = str(int(round(time.time() * 1000)) + i)  # 毫秒级当前时间戳
        sql_file.write("### DELETE FROM kpi_info WHERE KPI_NO = " + kpi_no + "; \n"
                       + "insert into KPI_INFO (KPI_NO,KBP_CLASS, KPI_ID, KPI_EN_NAME, KPI_CN_NAME, KPI_EN_DESCR, KPI_CN_DESCR, KPI_TYPE, KPI_UNIT,EXT_DATASOURCE)"
                       + " values (" + kpi_no + ", '" + monitorType + "', '" + kpi_id + "', '" + kpi_id + "', '" + cn_name + "', '" + kpi_id + "', '" + cn_name + "', '"
                       + data_type + "','" + unit + "','PATROL'); \n")
        i += 1

    for k in kpis:
        kpi_info = k.split("|")
        kpi_id = kpi_info[0]
        sql_file.write("### DELETE FROM UA_PLUGIN_KPI WHERE KPIID = '"
                       + kpi_id + "' AND SCRIPTID ='"
                       + scriptId + "'; \n"
                       + "INSERT INTO UA_PLUGIN_KPI(KPIID,SCRIPTID) VALUES"
                       + " ('"
                       + kpi_id + "','" + scriptId + "'); \n")
    sql_file.write("\n")
    sql_file.close()


if __name__ == "__main__":
    f = open("agentCheck2.sql", "w")  # 清空
    f.close()

    i = 2
    while i <= real_rows:
        if sheet["C"][i - 1].value:
            write_sql(i)


        else:
            write_sql(i, is_super=0)

        i += 1
