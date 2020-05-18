# 最近有个需求就是页面上执行shell命令，第一想到的就是os.system，
# 复制代码 代码如下:
import os
os.system('cat /proc/cpuinfo')

# 但是发现页面上打印的命令执行结果 0或者1，当然不满足需求了。
# 尝试第二种方案 os.popen()
# 复制代码 代码如下:

output = os.popen('cat /proc/cpuinfo')
print output.read()

# 通过 os.popen() 返回的是 file read 的对象，对其进行读取 read() 的操作可以看到执行的输出。但是无法读取程序执行的返回值）
# 尝试第三种方案 commands.getstatusoutput() 一个方法就可以获得到返回值和输出，非常好用。
# 复制代码 代码如下:
import commands
(status, output) = commands.getstatusoutput('cat /proc/cpuinfo')
print status, output
'''
Python Document 中给的一个例子，
复制代码 代码如下:

>>> import commands
>>> commands.getstatusoutput('ls /bin/ls')
(0, '/bin/ls')
>>> commands.getstatusoutput('cat /bin/junk')
(256, 'cat: /bin/junk: No such file or directory')
>>> commands.getstatusoutput('/bin/junk')
(256, 'sh: /bin/junk: not found')
>>> commands.getoutput('ls /bin/ls')
'/bin/ls'
>>> commands.getstatus('/bin/ls')
'-rwxr-xr-x 1 root 13352 Oct 14 1994 /bin/ls'

最后页面上还可以根据返回值来显示命令执行结果。
'''