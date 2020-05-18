#!/usr/bin/python
# coding:utf-8

"""
while 基本组成：
    1 break    结束整个while
    2 continue 跳过以后的代码，但不结束while
    3 else     正常结束while以后执行，里面有break，else里面内容不执行
"""

a = 1
while a < 5:
    a += 1
    print a
    if a >= 20:
        break
else:
    print "while is end"

"""
for 基本组成：
    1 break    结束整个for循环
    2 continue 跳过以后的代码，但不结束for循环
    3 else     正常结束for循环以后执行，如果for里面有break，else里面内容不执行
"""

for x in "i am a student":
    print x
else:
    print "for is end"

print x  #注意：for的的最后一个迭代值将会保留

print "my" is "my"

a = [{'S1.VALUE/S2.VALUE*100': u'.027976792033984463886017472462776836233', 'KPI': u'', 'VALUE': u'', 'CKB': u'aaa'}]

print("KP" in a[0])


ip = list()
ip = ip if ip else [""]
print(ip)


