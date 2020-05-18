#!/usr/bin/env python
# coding:utf-8

import re
import sys, os
import subprocess


#######0---True,1------False
#######\$---或,\&----与,^----非
def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    stdos = [line.strip("\n") for line in stdo]
    return stdos

<<<<<<< .mine

if len(sys.argv) != 4:
    print(
        "||%s||FM-PLUGIN-EXECUTE-FAILED||Usage:%s [FullLogfilePath] [keyword1,keyword2,keyword3] [mode 0-readfromend,1-readfromstart]" % (
            sys.argv[0], sys.argv[0]))
||||||| .r56534
if len(sys.argv)!=3:
    print ("||%s||FM-PLUGIN-EXECUTE-FAILED||Usage:%s [FullLogfilePath] [keyword1,keyword2,keyword3]" % (sys.argv[0], sys.argv[0]))
=======
if len(sys.argv)!=4:
    print ("||%s||FM-PLUGIN-EXECUTE-FAILED||Usage:%s [FullLogfilePath] [keyword1,keyword2,keyword3] [mode 0-readfromend,1-readfromstart]" % (sys.argv[0], sys.argv[0]))
>>>>>>> .r57319
    sys.exit()

<<<<<<< .mine
filepath = sys.argv[1]
mode = int(sys.argv[3])
dir = os.path.dirname(filepath)
logdir = os.environ['HOME']
# logdir=os.path.dirname(sys.argv[0])
if dir == '':
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Usage:%s [full file path]" % (sys.argv[0], sys.argv[0]))
||||||| .r56534

filepath=sys.argv[1]
dir=os.path.dirname(filepath)
#logdir = os.environ['HOME']
logdir=os.path.dirname(sys.argv[0])
if dir=='':
    print ("||%s||FM-PLUGIN-EXECUTE-FAILED||Usage:%s [full file path]" % (sys.argv[0], sys.argv[0]))
=======

filepath=sys.argv[1]
mode=int(sys.argv[3])
dir=os.path.dirname(filepath)
logdir = os.environ['HOME']
#logdir=os.path.dirname(sys.argv[0])
if dir=='':
    print ("||%s||FM-PLUGIN-EXECUTE-FAILED||Usage:%s [full file path]" % (sys.argv[0], sys.argv[0]))
>>>>>>> .r57319
    sys.exit()
posFiles = logdir + '/poskey.log'
filename = os.path.split(filepath)[-1]
if not os.path.exists(sys.argv[1]):
    print("||%s||PM-LINUX-LOG-01-01||1" % sys.argv[1])
    sys.exit()
else:
    checkedlog = sys.argv[1]
    if not os.access(checkedlog, os.R_OK):
        print("||%s||PM-LINUX-LOG-01-01||2" % checkedlog)
        sys.exit()
    else:
        pass


def getatt(dir, logname):
    size = os.path.getsize((os.path.join(dir, logname)))


def readOnly(filename):
<<<<<<< .mine
    return open(filename, 'r')
||||||| .r56534
    return open(filename, 'r',encoding='gbk')
=======
    try:
        return open(filename, 'r',encoding='gbk')
    except:
        return open(filename, 'r')
>>>>>>> .r57319


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
    txt = readsOnly(f)
    result = {}
    for i in txt:
        filename, time = i.split(':')
        if filename != '':
            result[filename] = time
    return result


def getEndTime(f):
    f = os.path.join(dir, f)
    time = os.path.getmtime(f)
    return int(time)


def getDistinct(startpos, endpos):
    return endpos - startpos


def updatePosLog(posResult, posFiles):
    f = writeOnly(posFiles)
    for k in posResult.keys():
        v = str(posResult[k])
        f.writelines('%s:%s\n' % (k, v))
    f.close()
    pass


def rematch(txt, regular):
    resultList = []
    regular1 = regular
    # print regular1
    for t in txt.split('\n'):
        try:
            pattern = re.compile(regular1)
        except Exception as e:
            print('||%s||FM-PLUGIN-EXECUTE-FAILED||%s' % (sys.argv[0], e))
            sys.exit()
        result = (pattern.findall(t))
        resultList.extend(result)
    try:
        return len(resultList)
    except Exception as e:
        return 0


def getmatchtext(txt, regular):
    resultList = []
    regular1 = regular
    pattern = re.compile(regular1)
    for t in txt.split('\n'):
        #    regular1=regular
        #    pattern = re.compile(regular1)
        result = (pattern.findall(t))
        if result:
            resultList.append(t)
    return '\n'.join(resultList)


def getnocontain(txt, regular):
    resultList = []
    regular1 = regular
    pattern = re.compile("^(?!.*" + regular1 + ").*")
    for t in txt.split('\n'):
        result = (pattern.findall(t))
        if result:
            resultList.append(t)
    return '\n'.join(resultList)


def getText(f, startpos, endpos):
    filename = readOnly(f)
    filename.seek(startpos, 0)
    textLength = getDistinct(startpos, endpos)
    text = filename.read(textLength)
    filename.close()
    return text.strip()


def ValidNot(i):
<<<<<<< .mine
    if i in ['$\&^', '$^\&', '\&$^', '\&^$', '^$\&', '^\&$', '$\&', '\&$', '^$', '^\&']:
||||||| .r56534
    if i in ['$&^','$^&','&$^','&^$','^$&','^&$','$&','&$','^$','^&']:
=======
    if i in ['$\&^','$^\&','\&$^','\&^$','^$\&','^\&$','$\&','\&$','^$','^\&']:
>>>>>>> .r57319
        return False
    else:
        return True


# def handlehuo(rega,text):

def main(file, keyword):
    global posFiles
    if not os.path.isfile(posFiles):
        try:
            os.mknod(posFiles)
        except Exception as e:
            print(e)
            sys.exit()
    else:
        pass
    posResult = getStartPosLog(posFiles)
    posResult_bak = getStartPosLog(posFiles)
    endpos = getEndPost(file)

    if endpos == 0:
        print("||%s||PM-LINUX-LOG-01-01||4" % checkedlog)

        sys.exit()
    else:
        try:
            startpos = int(posResult[file])
        except:
<<<<<<< .mine
            if mode == 0:
                startpos = endpos
            else:
                startpos = 0
||||||| .r56534
            startpos = 0
        if startpos > endpos:
            startpos = 0
=======
            if mode==0:
                startpos = endpos
            else:
                startpos = 0
>>>>>>> .r57319
        posResult_bak[file] = endpos
        # 处理切割后，偏移量归位
    # print startpos,endpos
    text = getText(file, startpos, endpos)
    # keylist=[]
    for i in keyword.split(","):
        keylist = []
        if not ValidNot(i):
            print("||%s||FM-PLUGIN-EXECUTE-FAILED||Keyword-Not-Valid-%s" % (checkedlog, i))
            continue
        else:
            if '\$' in i:
                num = 0
                for j in i.split('\$'):
                    num = num + rematch(text, j)
                anum = '||' + checkedlog + '||PM-LINUX-LOG-01-07||key=' + i + ';value=' + str(num)
                keylist.append(anum)
            elif '\&' in i:
                lengthj = len(i.split('\&'))
                for j in range(lengthj):
                    text = getmatchtext(text, i.split('\&')[j])
                    if j == lengthj - 1:
                        num = rematch(text, i.split('\&')[j])
                        anum = '||' + checkedlog + '||PM-LINUX-LOG-01-07||key=' + i + ';value=' + str(num)
                        keylist.append(anum)
            elif '^' in i:
                if text:
                    lengthj = len(i.split('^'))
                    for j in range(1, lengthj):
                        text = getnocontain(text, i.split('^')[j])
                        if text:
                            if j == lengthj - 1:
                                if i.split('^')[0]:
                                    num = rematch(text, i.split('^')[0])
                                    anum = '||' + checkedlog + '||PM-LINUX-LOG-01-07||key=' + i + ';value=' + str(num)
                                    keylist.append(anum)
                                else:
                                    anum = '||' + checkedlog + '||PM-LINUX-LOG-01-07||key=' + i + ';value=' + str(
                                        len(text.split('\n')))
                                    keylist.append(anum)
                        else:
                            anum = '||' + checkedlog + '||PM-LINUX-LOG-01-07||key=' + i + ';value=' + str(0)
                            keylist.append(anum)
                else:
                    anum = '||' + checkedlog + '||PM-LINUX-LOG-01-07||key=' + i + ';value=' + str(0)
                    keylist.append(anum)


            else:
                matchCount = rematch(text, i)
                a = '||' + checkedlog + '||PM-LINUX-LOG-01-07||key=' + i + ';value=' + str(matchCount)
                keylist.append(a)
        print('\n'.join(keylist))
    updatePosLog(posResult_bak, posFiles)


if __name__ == "__main__":
    keyword = sys.argv[2]
    keyword = keyword[1:-1] if keyword.startswith("'") and keyword.endswith("'") else keyword
    main(checkedlog, keyword)
