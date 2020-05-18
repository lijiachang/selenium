# -_-!  coding:utf-8 -_-!

# 系统自带读写文件
d = open('test.txt', 'w')
d.write('ni hao!\nthis is test!')  # 使用write写文件
print >> d, "use print !"  # 使用重定向>>写文件
d.close()

d = open('test.txt', 'r')
print d.readline()  # 读取一行
print d.readline()  # 继续读取一行

d.seek(0)  # 游标归位

print d.read(1000)

d.seek(0)  # 游标归位
print d.readlines()
d.close()

# 使用linecache读取文件
print "***********使用linecache读取文件************"
import linecache

print linecache.getline("test.txt", 1)  # 参数 文件名，读取的第几行
print linecache.getline("test.txt", 2)
list = linecache.getlines("test.txt")
print list
