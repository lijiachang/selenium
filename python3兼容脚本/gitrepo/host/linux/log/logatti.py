#!/usr/bin/env python
# coding:utf-8
import os
import sys
import re



if len(sys.argv) != 2:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||You should check the counts of the paramters." % sys.argv[0])
    sys.exit(0)

# Hip = outputs("ip add list|grep global|sed -n 1p|awk -F' ' '{print $2}'|awk -F'/' '{print $1}'")


filepath = sys.argv[1]
#####根据给定的正则文件名获取最新的文件
dir = os.path.dirname(filepath)
# logdir = os.path.dirname(sys.argv[0])
logdir = os.environ['HOME']
if dir == '':
    #print("||%s||FM-PLUGIN-EXECUTE-FAILED||Please insert the full path of the file." % sys.argv[0])
    print("||%s||PM-Dir-Status||1" % sys.argv[1])
elif not os.path.exists(dir):
    #print("||%s||FM-PLUGIN-EXECUTE-FAILED||Path %s not exists." % (sys.argv[0],dir))
    print("||%s||PM-Dir-Status||1" % (sys.argv[1]))
    sys.exit(0)

posFiles = logdir + '/pos.log'

timeFiles = logdir + '/time.log'

filename = os.path.split(filepath)[-1]

# reg = os.path.splitext(filename)[0]
reg = "^" + filename + "$"

try:
    comp = re.compile(reg, re.I)
except Exception as e:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Error:%s." % (sys.argv[0], e))
    sys.exit(0)

filelist = []
try:
    for file in os.listdir(dir):
        file1 = os.path.splitext(file)[0]
        if comp.search(file):
            filelist.append(file)

except Exception as e:
    sys.exit(0)

if len(filelist) == 0:
    #print("||%s||FM-PLUGIN-EXECUTE-FAILED||no file find" % sys.argv[0])
    print("||%s||PM-LINUX-LOG-01-07||1" % sys.argv[0])
    sys.exit(0)

s = sorted([(x, os.path.getmtime(os.path.join(dir, x))) for x in filelist], key=lambda i: i[1])
checkedlog = dir + '/' + s[-1][0]

logcount = len(filelist)
geshu = '||' + checkedlog + '||PM-LINUX-LOG-01-05||' + str(logcount)


# def getatt(dir, logname):
#     size = os.path.getsize((os.path.join(dir, logname)))
#     return size
def getatt(logname):
    size = os.path.getsize(logname)
    return size


def readOnly(filename):
    return open(filename, 'r')


def readsOnly(filename):
    content = open(filename, 'r')
    filelines = content.readlines()
    lines = []
    for li in filelines:
        if li.split():
            lines.append(li)
    content.close()
    return lines


def readWrite(filename):
    return open(filename, 'r+')


def writeOnly(filename):
    return open(filename, 'w')
    # pass


def getStartPosLog(posFiles):
    txt = readsOnly(posFiles)
    result = {}
    for i in txt:
        filename, pos = i.split(':')
        if filename != '':
            result[filename] = pos
    return result


def getEndPost(f):
    filename = readOnly(f)
    try:
        nowpos = filename.tell()
        filename.seek(0, 2)
        endpos = filename.tell()
        filename.seek(nowpos, 0)
    except:
        endpos = 0
    filename.close()
    return endpos
    # pass


def getStartTime(f):
    txt = readsOnly(timeFiles)
    result = {}
    for i in txt:
        filename, time = i.split(':')
        if filename != '':
            result[filename] = time
    return result


def getEndTime(dir,f):
    #f = os.path.join(dir, f)
    time = os.path.getmtime(f)
    return int(time)


def getDistinct(startpos, endpos):
    return endpos - startpos


def updatePosLog(posResult, posFiles):
    f = writeOnly(posFiles)
    for k in posResult.keys():
        v = posResult[k]
        f.writelines('%s:%s\n' % (k, v))
    f.close()
    pass


def main(file):
    global posFiles, timeFiles
    if not os.path.isfile(posFiles):
        try:
            # open(posFiles,'w')
            os.mknod(posFiles)

        except Exception as e:
            print("||%s||FM-PLUGIN-EXECUTE-FAILED||Error:%s." % (sys.argv[0], e))
            sys.exit(0)
    else:
        pass
    if not os.path.isfile(timeFiles):
        try:
            # open(timeFiles,'w')
            os.mknod(timeFiles)

        except Exception as e:
            print("||%s||FM-PLUGIN-EXECUTE-FAILED||Error:%s." % (sys.argv[0], e))
            sys.exit(0)

    else:
        pass
    posResult = getStartPosLog(posFiles)
    posResult_bak = getStartPosLog(posFiles)
    endpos = getEndPost(file)

    timeResult = getStartTime(timeFiles)
    timeResult_bak = getStartTime(timeFiles)
    endtime = getEndTime(dir,file)

    if endpos == 0:
        print("||%s||FM-PLUGIN-EXECUTE-FAILED||file %s is empty ,pass.." % (sys.argv[0], file))
        sys.exit(0)
    else:
        try:
            startpos = int(posResult[file])
        except:
            startpos = endpos
            # 处理切割后，偏移量归位
        posResult_bak[file] = endpos

    if endtime == 0:
        print("||%s||FM-PLUGIN-EXECUTE-FAILED||file %s is empty ,pass.." % (sys.argv[0], file))
        sys.exit(0)
    else:
        try:
            starttime = int(timeResult[file])
        except:
            starttime = endtime
            # 处理切割后，偏移量归位
        timeResult_bak[file] = endtime

    incsize = getDistinct(startpos, endpos)

    zeng = '||' + checkedlog + '||PM-LINUX-LOG-01-06||' + str(incsize)
    inctime = getDistinct(starttime, endtime)

    if incsize == 0:
        sizeupdate = 1
    else:
        sizeupdate = 0
    sizeu = '||' + checkedlog + '||PM-LINUX-LOG-01-04||' + str(sizeupdate)
    if inctime == 0:
        timeupdate = 1
    else:
        timeupdate = 0
    timeu = '||' + checkedlog + '||PM-LINUX-LOG-01-03||' + str(timeupdate)
    updatePosLog(posResult_bak, posFiles)
    updatePosLog(timeResult_bak, timeFiles)
    sizes = getatt(checkedlog)
    zsize = '||' + checkedlog + '||PM-LINUX-LOG-01-02||' + str(sizes)

    filestatus = '||' + checkedlog + '||PM-LINUX-LOG-01-07||' + '0'
    dirstatus = '||' + checkedlog + '||PM-Dir-Status||' + '0'

    print (geshu + '\n' + zeng + '\n' + zsize + '\n' + timeu + '\n' + sizeu + '\n' + filestatus + '\n' + dirstatus)


    ##print (geshu + '\n' + zeng + '\n' + zsize + '\n' + timeu + '\n' + sizeu)


if __name__ == "__main__":
    main(checkedlog)

