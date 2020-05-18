# coding:utf-8


file1 = open("info.txt", mode="r", )
file2 = open("res.txt", "w+")

line = file1.readline()
while line:

    info = line[24:].split(".")
    index0 = int(line[24:].split(".")[0]) + 1

    for i in info[1:index0]:
        file2.write(chr(int(i)))

    info2 = info[index0:]
    # print "\n"
    #     # print info2
    file2.write("-")
    index2 = int(info2[0]) + 1
    for i in info2[1:index2]:
        file2.write(chr(int(i)))
    # print "\n"
    file2.write("-")
    info3 = info2[index2].split("=")[0].strip()
    file2.write(info3)

    file2.write("=")
    info4 = info2[index2].split(":")[-1].strip()
    file2.write(info4)
    file2.write("\n")
    line = file1.readline()

file1.close()
file2.close()
