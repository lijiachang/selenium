# coding=utf-8

import ibm_db
import sys



if len(sys.argv) != 6:
    print("please use parameter:IP Port DataBaseName Username PassWord")
    sys.exit()
else:
    ip = sys.argv[1]
    port = sys.argv[2]
    dataBase = sys.argv[3]
    userName = sys.argv[4]
    passWord = sys.argv[5]

try:
    # ip = "192.168.180.88"
    # port = "50000"
    # dataBase = "SAMPLE"
    # conn = ibm_db.connect("DATABASE=SAMPLE;HOSTNAME=192.168.180.88;PORT=50000;PROTOCOL=TCPIP;UID=db2admin;PWD=ultranms_123", "", "")  # 测试连接
    conn = ibm_db.connect("DATABASE="+dataBase+";HOSTNAME="+ip+";PORT=" +
                          port+";PROTOCOL=TCPIP;UID="+userName+";PWD="+passWord, "", "")
except Exception, e:
    print("DB2数据库连接失败，请检查连接信息!")
    print(e)
    sys.exit()


def sql_execute(sql):
    stmt = ibm_db.exec_immediate(conn, sql)
    data = ibm_db.fetch_both(stmt)
    return data


#  DB2数据库实例
instance_data = sql_execute("select INST_NAME, SERVICE_LEVEL from sysibmadm.env_inst_info;")
mpoint = "-".join([ip, port, "DB2"])
ckbp = ""
separator = "||"
wrap = "\n"

results = separator.join([mpoint, ckbp, "CM-DB2-01-01", instance_data["INST_NAME"]])  # 数据实例名
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-DB2-01-02", instance_data["SERVICE_LEVEL"]])])  # 版本

status_data = sql_execute("select db_status from sysibmadm.snapdb with ur;")
if status_data["DB_STATUS"] == "ACTIVE":
    results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-01-01", "0"])])  # 状态
else:
    results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-01-01", "1"])])  # 状态

# DB2 数据库
data = sql_execute("select db_name,db_path,input_db_alias,db_conn_time from sysibmadm.snapdb with ur")
ckbp = data["DB_NAME"].strip()
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-DB2-02-01", data["DB_NAME"]])])  # 描述信息
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-DB2-02-02", data["INPUT_DB_ALIAS"]])])  # 别名
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-DB2-02-03", data["DB_PATH"]])])  # 路径
DB_CONN_TIME = str(data["DB_CONN_TIME"])[0:19]  # 调整启动时间输出格式
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-DB2-02-04", DB_CONN_TIME])])  # 启动时间
if status_data["DB_STATUS"] == "ACTIVE":
    results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-02-01", "0"])])  # 状态
else:
    results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-02-01", "1"])])  # 状态
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-02-02", "0"])])  # 是否可以连接

data = sql_execute("select APPLS_CUR_CONS,APPLS_IN_DB2,LOCKS_WAITING from sysibmadm.snapdb  with ur")
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-03-01", str(data["APPLS_CUR_CONS"])])])  # 当前连接的应用程序数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-03-02", str(data["APPLS_IN_DB2"])])])  # 当前执行的应用程序数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-03-03", str(data["LOCKS_WAITING"])])])  # 等待锁定的当前代理程序数
if data["APPLS_CUR_CONS"] > 0:
    results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-03-04", str((data["LOCKS_WAITING"] / data["APPLS_CUR_CONS"]) * 100)])])  # 等待锁定的代理程序比例
else:
    results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-03-04", "0"])])  # 等待锁定的代理程序比例

data = sql_execute("select AGENTS_REGISTERED,IDLE_AGENTS,LOCAL_CONS,LOCAL_CONS_IN_EXEC,REM_CONS_IN,REM_CONS_IN_EXEC from sysibmadm.snapdbm")
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-04-01", str(data["AGENTS_REGISTERED"])])])  # 注册的代理程序数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-04-02", str(data["IDLE_AGENTS"])])])         # 空闲的代理程序数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-04-03", str(data["LOCAL_CONS"])])])           # 本地连接数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-04-04", str(data["LOCAL_CONS_IN_EXEC"])])])  # 在数据库管理器中执行的本地连接数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-04-05", str(data["REM_CONS_IN"])])])          # 与数据库管理器的远程连接数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-04-06", str(data["REM_CONS_IN_EXEC"])])])    # 在数据库管理器中执行的远程连接数

data = sql_execute("select DEADLOCKS,LOCK_ESCALS,LOCK_WAITS from sysibmadm.snapdb")
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-05-01", str(data["DEADLOCKS"])])])    # 发生的死锁总数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-05-02", str(data["LOCK_ESCALS"])])])  # 锁定已从若干行锁定升级至表锁定的次数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-05-03", str(data["LOCK_WAITS"])])])   # 当前挂起的锁定数目


# 检测数据数据是否为空，为空返回0
def not_none(test):
    if test == "" or test is None:
        return "0"
    else:
        return test


data = sql_execute("select TOTAL_HIT_RATIO_PERCENT,INDEX_HIT_RATIO_PERCENT,DATA_HIT_RATIO_PERCENT from "
                  "sysibmadm.bp_hitratio where  BP_NAME not in ('IBMSYSTEMBP4K', 'IBMSYSTEMBP8K', 'IBMSYSTEMBP16K', 'IBMSYSTEMBP32K') with ur")
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-07-01", not_none(data["TOTAL_HIT_RATIO_PERCENT"])])])  # 总体读命中率
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-07-02", not_none(data["INDEX_HIT_RATIO_PERCENT"])])])  # 索引读命中率
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-07-03", not_none(data["DATA_HIT_RATIO_PERCENT"])])])   # 数据命中率

data = sql_execute("select PKG_CACHE_LOOKUPS,PKG_CACHE_NUM_OVERFLOWS,CAT_CACHE_LOOKUPS,CAT_CACHE_OVERFLOWS from sysibmadm.snapdb")
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-07-04", str(data["PKG_CACHE_LOOKUPS"])])])           # 程序包高速缓存命中数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-07-05", str(data["PKG_CACHE_NUM_OVERFLOWS"])])])   # 程序包高速缓存溢出数量
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-07-06", str(data["CAT_CACHE_LOOKUPS"])])])         # 目录高速缓存命中数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-07-07", str(data["CAT_CACHE_OVERFLOWS"])])])    # 目录高速缓存溢出数量

data = sql_execute("select  a.DIRECT_READS,a.DIRECT_WRITES,a.DIRECT_READ_REQS,a.DIRECT_WRITE_REQS from sysibmadm.SNAPBP a where  "
                   "BP_NAME not in ('IBMSYSTEMBP4K', 'IBMSYSTEMBP8K', 'IBMSYSTEMBP16K', 'IBMSYSTEMBP32K') with ur")
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-08-01", str(data["DIRECT_READ_REQS"])])])        # 直接读操作请求速率
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-08-02", str(data["DIRECT_READS"])])])           # 直接读操作速率
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-08-03", str(data["DIRECT_WRITE_REQS"])])])    # 直接写操作请求速率
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-08-04", str(data["DIRECT_WRITES"])])])       # 直接写操作速率

data = sql_execute("SELECT A.LOG_UTILIZATION_PERCENT, A.TOTAL_LOG_USED_KB,A.TOTAL_LOG_AVAILABLE_KB,A.TOTAL_LOG_USED_TOP_KB FROM SYSIBMADM.LOG_UTILIZATION A with ur")
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-09-01", str(data["TOTAL_LOG_USED_KB"]/1024)])])         # 使用的总日志空间
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-09-02", str(data["TOTAL_LOG_AVAILABLE_KB"]/1024)])])   # 可用的总日志空间
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-09-03", str(data["LOG_UTILIZATION_PERCENT"])])])       # 总日志空间使用率
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-09-04", str(data["TOTAL_LOG_USED_TOP_KB"]/1024)])])    # 使用的最大总日志空间

# DB2 表空间
ckbp = "ResDB2TableSpace"
data = sql_execute("SELECT TBSP_ID,TBSP_NAME,TBSP_TYPE,TBSP_CONTENT_TYPE FROM SYSIBMADM.TBSP_UTILIZATION")
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-DB2-06-01", str(data["TBSP_ID"])+"-DB2-DATABASE-" + ip + "-" + dataBase])])   # 标识
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-DB2-06-02", data["TBSP_NAME"]])])       # 名称
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-DB2-06-03", data["TBSP_TYPE"]])])         # 类型
results = wrap.join([results, separator.join([mpoint, ckbp, "CM-DB2-06-04", data["TBSP_CONTENT_TYPE"]])])  # 内容类型

data = sql_execute("SELECT TBSP_ID,TBSP_NAME,TBSP_STATE,TBSP_PAGE_SIZE,TBSP_TOTAL_PAGES,TBSP_USABLE_PAGES, \
                  TBSP_USED_PAGES,TBSP_FREE_PAGES,TBSP_CONTENT_TYPE,TBSP_TOTAL_SIZE_KB,TBSP_FREE_SIZE_KB, \
                  TBSP_UTILIZATION_PERCENT FROM SYSIBMADM.TBSP_UTILIZATION")
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-06-01", "0" if data["TBSP_STATE"] == "NORMAL" else "1"])])  # 状态
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-06-02", str(data["TBSP_PAGE_SIZE"])])])  # 页大小
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-06-03", str(data["TBSP_TOTAL_PAGES"])])])  # 总页数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-06-04", str(data["TBSP_USABLE_PAGES"])])])  # 可用页数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-06-05", str(data["TBSP_USED_PAGES"])])])  # 已使用页数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-06-06", str(data["TBSP_FREE_PAGES"])])])  # 空闲页数
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-06-07", str(data["TBSP_TOTAL_SIZE_KB"]/1024)])])  # 总空间(GB)
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-06-08", str(data["TBSP_FREE_SIZE_KB"]/1024)])])  # 可用空间(GB)
results = wrap.join([results, separator.join([mpoint, ckbp, "PM-DB2-06-09", data["TBSP_UTILIZATION_PERCENT"]])])  # 表空间使用率


print(results)

ibm_db.close(conn)
