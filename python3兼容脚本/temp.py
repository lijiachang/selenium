import re

a = "select 'oracle instance' as Pm_01_01,'ok' as pm_01_02,'03' as pm_01_03   from V\$INSTANCE;"
print(a)

b = re.split('[ ,]', a)
print(b)
# 找到所有“as”的位置下标
as_index = [i for i,x in enumerate(b) if x == "as"]
print(as_index)
kpi_list =list()
for a in as_index:
    kpi_list.append(b[a + 1])
print(kpi_list)

c = "123"
print(len(c))

c = c.replace(["1","2"],"")
print(c)