# coding:utf-8

import re

pattern = "yue"  # 普通字符作为原子
string = "this is xiao yue yue"
res = re.search(pattern, string)
print res