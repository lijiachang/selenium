#!/usr/bin/env python
# -*- coding:utf-8 -*-

'my first test moudle'

__author__ = 'lijiachang'

import sys

print sys.path


def test():
    args = sys.argv  # argv变量，用list存储了命令行的所有参数
    if len(args) == 1:
        print 'hello word!'
    elif len(args) == 2:
        print 'hell', args[1]
    else:
        print 'too many args'


if __name__ == '__main__':
    test()

# 别名：
# 导入模块时，还可以使用别名，这样，可以在运行时根据当前环境选择最合适的模块
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

    # Python标准库一般会提供StringIO和cStringIO两个库，这两个库的接口和功能是一样的，但是cStringIO是C写的，速度更快

a = "-bash: mysql: mysql: [Warning] Using a password on the command line interface can be insecure."

if "12" in a:
    print("YES")
elif "-bash: mysql:" in a:
    print("YES2")
