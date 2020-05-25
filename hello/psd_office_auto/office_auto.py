# coding:utf-8
import os
import sys
import shutil
from time import sleep

# from collections import OrderedDict

# original_path = raw_input(u"请输入源文件路径：")
# out_put_path = raw_input(u"请输入【全国考区资料】所在路径：")
reload(sys)
sys.setdefaultencoding('utf8')

original_path = r'C:\Users\li\Desktop\源'
original_path_u = unicode(original_path, "utf-8")  # 处理中文目录问题
file_list = os.listdir(original_path_u)


def copmulu(path, path1):  # path原文件地址，path1指定地址
    s = path.split("\\")  # 获得以原路径按“/”切割的字符串，取最后一个s[-1]得到文件名
    newpath = os.path.join(path1, s[-1])  # 更新新路径
    os.makedirs(newpath)  # 创建目录
    lt = os.listdir(path)  # 获得老目录下的信息

    for i in lt:
        if os.path.isdir(os.path.join(path, i)):  # 如果是目录就调用函数进行递归
            copmulu(os.path.join(path, i), newpath)

        else:
            fp = open(os.path.join(path, i), 'r')
            fp1 = open(os.path.join(newpath, i), 'w')  # 如果是文件则在新目录下创建
            for j in fp:
                fp1.write(j)  # 向新文件中写入数据
            fp.close()
            fp1.close()
            os.remove(os.path.join(path, i))  # 删除原文件
    print "remove over"

    os.rmdir(os.path.join(path))  # 删除原目录


aa = unicode(r"C:\Users\li\Desktop\副本", "utf-8")  # 处理中文目录问题
#copmulu(aa, r"C:\Users\li\Desktop\new")

shutil.move(aa, r"C:\Users\li\Desktop\new")

print file_list
for one in file_list:
    stu_id = one.split("-")[0].strip()
    stu_name = one.split("-")[1].strip()
    stu_city = one.split("-")[2].strip()
    print u"开始处理", stu_id, stu_name, stu_city

# for root, dirs, files in os.walk(original_path):
# #             print(root) #当前目录路径
# #             print(dirs) #当前路径下所有子目录
# #             print(files) #当前路径下所有非目录子文件
