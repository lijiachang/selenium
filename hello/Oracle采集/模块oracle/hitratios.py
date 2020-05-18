# coding:utf-8
import cx_Oracle
import sys

"""
By 2019.09.27
"""

try:
    hostip = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    ins = sys.argv[5]
    mpoint = "-".join([hostip, port, ins])
except Exception as e:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please usage:%s hostip port username password  servername" % (
        sys.argv[0], sys.argv[0]))
    sys.exit(0)

try:
    if hostip == "0.0.0.0":
        db = cx_Oracle.connect(username, password, ins, encoding="UTF-8")  # 服务名方式
    else:
        db = cx_Oracle.connect(username, password, '{0}:{1}/{2}'.format(hostip, port, ins),
                               encoding="UTF-8")  # 实例名方式,数据库名
except Exception as e:
    print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
    sys.exit(0)


def QueryBySqlPlus(sqlComm):
    sqlComm = sqlComm.strip()[:-1] if sqlComm.strip()[-1] == ";" else sqlComm  # del ;
    cur = db.cursor()
    try:
        cur.execute(sqlComm)
    except Exception as e:
        print("%s||||FM-PLUGIN-EXECUTE-FAILED||%s" % (mpoint, e))
        sys.exit(0)
    columns = [i[0] for i in cur.description]  # col整理
    result = cur.fetchall()
    # print(result)
    result = [dict(zip(columns, row)) for row in result]
    if result:
        return result
    else:
        return [dict([(col, "null") for col in columns])]


if __name__ == "__main__":
    sqlComm = """select a.cache_hit_percent, e.rowcache_hitratio, d.get_ratio_percent
              from (SELECT ROUND((1 - ((s1.VALUE - s4.VALUE - s5.VALUE) /
                                 (s2.VALUE + s3.VALUE - s4.VALUE - s5.VALUE))) * 100,
                                 2) cache_hit_percent
                      FROM V$sysstat s1,
                           V$sysstat s2,
                           V$sysstat s3,
                           V$sysstat s4,
                           V$sysstat s5
                     WHERE s1.NAME = 'physical reads'
                       AND s2.NAME = 'consistent gets'
                       AND s3.NAME = 'db block gets'
                       AND s4.NAME = 'physical reads direct (lob)'
                       AND s5.NAME = 'physical reads direct') a,
                   (select round(100 * (1 - sum(misses) / sum(gets)), 2) latch_ratio_percent
                      from V$latch) b,
                   (select round(100 * (a.get_ratio / b.total), 2) get_ratio_percent
                      from (select sum(gethitratio) get_ratio from V$LIBRARYCACHE) a,
                           (select count(*) total from V$LIBRARYCACHE) b) d,
                   (select round(100 * (1 - sum(getmisses) / sum(gets)), 2) rowcache_hitratio
                      from V$rowcache) e,
                   (SELECT round(100 * s1.VALUE / (s2.VALUE + s1.VALUE), 2) mem_sort_percent
                      FROM V$sysstat s1, V$sysstat s2
                     WHERE s1.NAME = 'sorts (memory)'
                       AND s2.NAME = 'sorts (disk)') f;"""
    result = QueryBySqlPlus(sqlComm)

    mpoint = "-".join([hostip, port, ins])
    ckbp = ""
    separator = "||"
    wrap = "\n"
    results = list()
    results.append(separator.join([mpoint, ckbp, "APM-00-03-01-00-08", str(result[0].get("CACHE_HIT_PERCENT"))]))  # 缓冲池命中率
    results.append(separator.join([mpoint, ckbp, "APM-00-03-01-00-09", str(result[0].get("ROWCACHE_HITRATIO"))]))  # 数据字典命中率
    results.append(separator.join([mpoint, ckbp, "APM-00-03-01-00-34", str(result[0].get("GET_RATIO_PERCENT"))]))  # 库缓存命中率

    for r in results:
        print(r)
