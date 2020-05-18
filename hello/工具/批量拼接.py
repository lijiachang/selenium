# coding:utf-8

results = str()
i = 0

kpi = open("kpi.txt", "r").readlines()
name = open("name.txt", "r").readlines()

for k in kpi:
    results = "\n".join([results, "|".join([k[:-1], name[i][:-1], k[0:2],""])])
    i += 1

# with open("kpi.txt", "r") as kpi:
#     with open("name.txt", "r") as name:
#         while i < le:
#             results = "".join([results, "\n",("|".join([kpi.readline()[:-1], name.readline()[:-1], kpi.readline()[0:2]]))])
#             i+=1

print results
