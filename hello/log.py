#!/usr/bin/env python
# coding:utf-8
# 2019.03.15
import re
import sys
import os
import subprocess
import codecs
import linecache
import platform

pythonver = platform.python_version()
if pythonver.startswith('2'):
    reload(sys)
    sys.setdefaultencoding('utf-8')


def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    if pythonver.startswith('3'):
        stdos = [str(line, encoding='utf-8').strip("\n") for line in stdo]
    else:
        stdos = [line.strip("\n") for line in stdo]
    return stdos


if len(sys.argv) == 6:
    filepath = sys.argv[1]
    filematch = sys.argv[2]
    kbp = filepath
    code = sys.argv[4]
    lines = sys.argv[5]
    curkeyword = sys.argv[3]
    curkeyword = curkeyword[1:-1] if curkeyword.startswith("'") and curkeyword.endswith("'") else curkeyword
else:
    print(
            "||%s||FM-PLUGIN-EXECUTE-FAILED||Usage:%s [FullLogfilePath] [fileMatch default is default] [keyword1,keyword2,keyword3] [code default is utf-8, 'utf-8\gb2312\gbk'] [lines]" % (
        sys.argv[0], sys.argv[0]))
    sys.exit()

dir = os.path.dirname(filepath)
# logdir = os.environ['HOME']
# posFiles = logdir + '/poskey.log'
posFiles = './poskey.log'
if filematch.startswith("default"):
    if dir == '':
        print("||%s||PM-LINUX-LOG-01-07||0" % (kbp + "-" + curkeyword))
        sys.exit()
    elif not os.path.isdir(dir):
        print("||%s||PM-LINUX-LOG-01-07||0" % (kbp + "-" + curkeyword))
        sys.exit()
    checkedlog = filepath
else:
    if filematch.startswith("'") and filematch.endswith("'"):
        filename = eval(filematch)
    else:
        filename = filematch

    if len(re.findall("`", filename)) == 2:
        try:
            if filename.startswith("`") and filename.endswith("`"):
                filename = outputs(filename.strip('`'))[0]
            elif not filename.startswith("`") and filename.endswith("`"):
                filezuhe = outputs(filename.split('`')[1])[0]
                filename = filename.split('`')[0] + filezuhe
            elif filename.startswith("`") and not filename.endswith("`"):
                filezuhe = outputs(filename.split('`')[1])[0]
                filename = filezuhe + filename.split('`')[2]
            else:
                filezuhe = outputs(filename.split('`')[1])[0]
                filename = filename.split('`')[0] + filezuhe + filename.split('`')[2]
        except:
            filename = filename
    fullfile = dir + '/' + filename
    reg = "^" + filename + "$"
    try:
        comp = re.compile(reg, re.I)
    except Exception as e:
        print("||%s||FM-PLUGIN-EXECUTE-FAILED||Error:%s." % (sys.argv[0] + fullfile, e))
        sys.exit(0)
    filelist = []

    try:
        for file in os.listdir(dir):
            if comp.search(file):
                filelist.append(file)

    except Exception as e:
        print ("||%s||FM-PLUGIN-EXECUTE-FAILED||Error:%s." % (sys.argv[0] + '-' + fullfile, e))
        sys.exit(0)
    if len(filelist) == 0:
        print("||%s||PM-LINUX-LOG-01-07||0" % (kbp + "-" + curkeyword))
        sys.exit(0)
    s = sorted([(x, os.path.getmtime(os.path.join(dir, x))) for x in filelist], key=lambda i: i[1])
    checkedlog = dir + '/' + s[-1][0]
    # kbp=checkedlog

# if filematch.startswith("default"):
#    posFiles = './'+filepath.split('/')[-1] + curkeyword + '.log'
# else:
#    posFiles = '/ultraagent/bin/'+filename + curkeyword + '.log'
# print(posFiles)
if not os.path.exists(checkedlog):
    print("||%s||PM-LINUX-LOG-01-07||0" % (kbp + "-" + curkeyword))
    sys.exit()
else:
    # checkedlog = fullfile
    if not os.access(checkedlog, os.R_OK):
        print("||%s||PM-LINUX-LOG-01-07||0" % (kbp + "-" + curkeyword))
        sys.exit()
    else:
        pass


def getatt(dir, logname):
    size = os.path.getsize((os.path.join(dir, logname)))


def readOnly(filename):
    try:
        return open(filename, 'r')
    except Exception as e:
        print("||%s||PM-LINUX-LOG-01-07||0" % ((kbp + "-" + curkeyword)))
        exit(0)


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


def xieOnly(filename):
    return open(filename, 'w')


def getStartPosLog(posFiles):
    txt = readsOnly(posFiles)
    result = {}
    for i in txt:
        filename, pos = ':'.join(i.split(':')[0:-1]), i.split(':')[-1]
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
    f = xieOnly(posFiles)
    for k in posResult.keys():
        v = str(posResult[k]).strip()
        f.writelines('%s:%s\n' % (k, v))
    f.close()
    pass


def rematch(txt, regular):
    resultList = []
    nums = []
    regular1 = regular
    for num, t in enumerate(txt.split('\n')):
        try:
            pattern = re.compile(regular1)
        except Exception as e:
            print('||%s||PM-LINUX-LOG-01-07||%s' % ((kbp + "-" + curkeyword), e))
            sys.exit()
        result = (pattern.findall(t))
        resultList.extend(result)
        if result:
            nums.append(num)
    try:
        if nums:
            if int(lines):
                return len(resultList), ','.join(
                    txt.split('\n')[max(nums) - int(lines):max(nums) + int(lines) + 1]).replace("\r", "")
            else:
                return len(resultList), ''
        else:
            return len(resultList), ''
    except Exception as e:
        return 0, ''


def norematch(orgtext, regular):
    resultList = []
    nums = []
    regular1 = regular
    # print regular1
    for num, t in enumerate(orgtext.split('\n')):
        try:
            pattern = re.compile(regular1)
        except Exception as e:
            print('||%s||PM-LINUX-LOG-01-07||%s' % ((kbp + "-" + curkeyword), e))
            sys.exit()
        if t.startswith('MEIYOU '):
            pass
        else:
            result = (pattern.findall(t))
            resultList.extend(result)
            if result:
                nums.append(num)
    try:
        if nums:
            if int(lines):
                return len(nums), ','.join(
                    orgtext.split('\n')[max(nums) - int(lines):max(nums) + int(lines) + 1]).replace('MEIYOU ',
                                                                                                    '').replace("\r",
                                                                                                                "")
            else:
                return len(resultList), ''
        else:
            return len(resultList), ''
    except Exception as e:
        return 0, ''


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
    regular1 = regular.replace('^', '|')
    pattern = re.compile("^(?!.*" + regular1 + ").*")
    for t in txt.split('\n'):
        result = (pattern.findall(t))
        if result:
            resultList.append(t)
        else:
            resultList.append('MEIYOU ' + t)
    return '\n'.join(resultList)


def getText(f, startpos, endpos):
    try:
        filename = codecs.open(f, 'r', code, errors='ignore')
    except LookupError as e:
        print ("||%s||PM-LINUX-LOG-01-07||%s" % ((kbp + "-" + curkeyword), e))
        sys.exit(2)
    filename.seek(startpos, 0)
    textLength = getDistinct(startpos, endpos)
    try:
        text = filename.read(textLength)
    except UnicodeDecodeError:
        print ("||%s||PM-LINUX-LOG-01-07||0" % (kbp + "-" + curkeyword))
        sys.exit(0)
    filename.close()
    return text.strip()


def ValidNot(i):
    if i in ['$\&^', '$^\&', '\&$^', '\&^$', '^$\&', '^\&$', '$\&', '\&$', '^$', '^\&']:
        return False
    else:
        return True


def main(file, keyword):
    filekey = file + '|' + keyword
    global posFiles
    if not os.path.isfile(posFiles):
        try:
            os.mknod(posFiles)
        except Exception as e:
            sys.exit()
    else:
        pass
    posResult = getStartPosLog(posFiles)
    posResult_bak = posResult
    endpos = getEndPost(file)

    if endpos == 0:
        print("||%s||PM-LINUX-LOG-01-07||0" % (kbp + "-" + curkeyword))
        sys.exit()
    else:
        try:
            startpos = int(posResult[filekey])
        except:
            startpos = endpos
        posResult_bak[filekey] = endpos

    # print startpos,endpos
    keylist = []
    text = getText(file, startpos, endpos)
    for i in keyword.split(","):
        if len(i) != 0:
            if pythonver.startswith('2'):
                try:
                    i = i.decode("utf-8")
                except:
                    i = i
            if not ValidNot(i):
                print("||%s||PM-LINUX-LOG-01-07||0" % (kbp + "-" + curkeyword))
                continue
            else:
                if '\$' in i:
                    num = 0
                    jconts = []
                    for j in i.split('\$'):
                        jnum, jcont = rematch(text, j)
                        num = num + jnum
                        jconts.append(jcont)
                    anum = '||' + kbp + '-' + i + '||PM-LINUX-LOG-01-07||' + str(num) + '||' + jconts[-1].strip('\n')
                    keylist.append(anum)
                elif '\&' in i:
                    lengthj = len(i.split('\&'))
                    for j in range(lengthj):
                        text = getmatchtext(text, i.split('\&')[j])
                        if j == lengthj - 1:
                            num, cont = rematch(text, i.split('\&')[j])
                            anum = '||' + kbp + '-' + i + '||PM-LINUX-LOG-01-07||' + str(num) + '||' + cont.strip('\n')
                            keylist.append(anum)
                elif '^' in i:
                    if text:
                        lengthj = len(i.split('^'))
                        for j in range(1, lengthj):
                            text = getnocontain(text, i.split('^')[j])
                            if text:
                                if j == lengthj - 1:
                                    if i.split('^')[0]:
                                        num, cont = norematch(text, i.split('^')[0])
                                        anum = '||' + kbp + '-' + i + '||PM-LINUX-LOG-01-07||' + str(
                                            num) + '||' + cont.strip('\n')
                                        keylist.append(anum)
                                    else:
                                        maxnums = []
                                        for num, t in enumerate(text.split('\n')):
                                            if not t.startswith('MEIYOU'):
                                                maxnums.append(num)
                                        anum = '||' + kbp + '-' + i + '||PM-LINUX-LOG-01-07||' + str(
                                            len([i for i in text.split('\n') if
                                                 not i.startswith('MEIYOU ')])) + '||' + ','.join(text.split('\n')[
                                                                                                  max(maxnums) - int(
                                                                                                      lines):max(
                                                                                                      maxnums) + int(
                                                                                                      lines) + 1]).replace(
                                            "\r", "").strip('MEIYOU ')
                                        keylist.append(anum)
                            else:
                                anum = '||' + kbp + '-' + i + '||PM-LINUX-LOG-01-07||' + str(0) + '||'
                                keylist.append(anum)
                    else:
                        anum = '||' + kbp + '-' + i + '||PM-LINUX-LOG-01-07||' + str(0) + '||'
                        keylist.append(anum)
                else:
                    matchCount, cont = rematch(text, i)
                    a = '||' + kbp + '-' + i + '||PM-LINUX-LOG-01-07||' + str(matchCount) + '||' + cont
                    keylist.append(a)

    print((keylist, "keylist"))
    print('\n'.join(keylist), 123)
    print('\n'.join(keylist).encode("utf-8"))
    print('\n'.join(keylist))
    updatePosLog(posResult_bak, posFiles)


if __name__ == "__main__":
    keyword = sys.argv[3]
    keyword = keyword[1:-1] if keyword.startswith("'") and keyword.endswith("'") else keyword
    main(checkedlog, keyword)
