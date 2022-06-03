# coding: utf-8

import time
from collections import namedtuple

import openpyxl
from openpyxl import load_workbook

"""
用于Go-agent项目读取excel文件生成sql   Oracle数据库专用
By：李家昌  最后修改：2018.04.18
"""

#######################################################################
data = load_workbook("lawcdyc.xlsm")  # 读取excel表
sheet = data["Sheet1"]  # 读取表名
print(type(sheet))
# 计算实际行数real_rows 即非空行
real_rows = 0
for index, line in enumerate(sheet):
    print(index, line[2].value)

LINE = namedtuple('LINE', 'id create_time title key_words tag content')


def write_title_to_cache(line):
    """缓存line"""
    with open('cache', 'w') as file_ob:
        file_ob.write(line)


def read_title_from_cache():
    """读取缓存line"""
    try:

        with open('cache', 'r') as file_ob:
            num = file_ob.read()
            num = int(num)
    except Exception as e:
        logger.info('no read_index_from_cache:{}'.format(e))
        num = None
    return num


def analysis_line(line):
    """line eg.
    A                   F
    序号	时间	标题	标签	tag	内容
1		台州70平米的服装装修大概多少钱	台州,70,平米,服装,大概,多少钱	台州,70,平米,服装,大概,多少钱	"必要店面现状，大备注，小项目，重整修需求，这个人才多是个人。</p>
<p><p><br/></p><p><img src=""/images/tu01/Image_307.jpg""title=""台州70平米的服装装修大概多少钱""  alt=""台州70平米的服装装修大概多少钱""/></p><p><br/></p><p><strong>台州70平方米装修费用要多少哪里找这么大房子的装修案例？</strong></p><p>服装店</p>
    """

    title = line[2].value  # 标题
    key_words = line[3].value  # 标签
    tag = line[4].value  # tag
    content = line[5].value  # 内容
    if title and key_words and tag and content
        return LINE('', '', title, key_words, tag, content)
    else:
        raise Exception('单元格内容为空，跳过')


def gen_read_inventory(file_name):
    cache_row_index = read_title_from_cache()
    gen_sheet = enumerate(sheet)

    # 读取到上次暂停处
    if cache_row_index:
        while True:
            row_index, _ = next(gen_sheet)
            if row_index == cache_row_index:
                break

    for row_index, sheet_line in gen_sheet:
        try:
            line_ = analysis_line(sheet_line)  # 提取正确的一行
        except Exception as e:
            logger.error('read line err:{}'.format(e))
            continue
        else:
            write_title_to_cache(row_index)
            yield line_


monitorType, scriptPath, scriptName, parameterName, parameterDescr, parameterDataType, parameterDataScope, \
isRequired, isEncrypted, defaultValue, execsEquence, note, kpi, scriptId, adaptos, creator, scriptType = [""] * 17


def updata_data(row_index, is_super=1):
    global monitorType, scriptPath, scriptName, parameterName, parameterDescr, parameterDataType, parameterDataScope, isRequired, isEncrypted, defaultValue, execsEquence, note, kpi, scriptId, adaptos, creator, scriptType
    e = sheet[row_index]
    kpi = e[13].value  # 每次循环都更新 kpi内数据 3.19 （解决合并单元格，第二行重复添加 kpi）
    if is_super == 1:
        if e[0].value is not None:
            monitorType = e[0].value
            scriptPath = e[1].value.replace("\\", "/")  # 替换 \  为 /
        scriptName = e[2].value
        # kpi = e[13].value
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
    scriptId = scriptPath + "/" + scriptName  # 替换 \  为 /
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
