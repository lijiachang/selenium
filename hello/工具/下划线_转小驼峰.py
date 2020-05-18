# coding:utf-8

# http://www.bejson.com/convert/camel_underscore/

results = str()
i = 01

kpi = open("EngishName.txt", "r")

res = kpi.readlines()

for k in res:
    i = "0" + str(i) if i < 10 else i
    print k.strip() + "(" + str(i) + ")",
    i = int(i)
    i+=1

# with open("kpi.txt", "r") as kp

kpi.close()
