import os
import re
from concurrent.futures import ThreadPoolExecutor, wait

import requests

finishedNum = 0
allNum = 0
fileList = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}


def download(downloadLink, name):
    global finishedNum
    global allNum
    for _ in range(10):
        try:
            req = requests.get(downloadLink, headers=headers, timeout=15).content
            with open(f"{name}", "wb") as f:
                f.write(req)
                f.flush()
            finishedNum += 1
            print(f"{name}下载成功, 总进度{round(finishedNum / allNum * 100, 2)}% ({finishedNum}/{allNum})")
            break
        except:
            if _ == 9:
                print(f"{name}下载失败")
            else:
                print(f"{name}正在进行第{_}次重试")


def merge_file(path, name):
    global fileList
    # linux: cat index1.ts index2.ts >>3.ts
    cmd = "copy /b "
    for i in fileList:
        if i != fileList[-1]:
            i = os.path.join(path, i)
            cmd += f"{i} + "
        else:
            i = os.path.join(path, i)
            cmd += f'{i} "{name}"'
    # os.chdir(path)
    with open('combine.cmd', 'w') as f:
        f.write(cmd)
    os.system("combine.cmd")
    os.system(r'del /Q {}\index*.ts'.format(path))
    os.system('del /Q *.cmd')


def downloader(url, name, threadNum):
    global allNum
    global fileList
    global finishedNum
    print("读取文件信息中...")
    downloadPath = 'Download'
    if not os.path.exists(downloadPath):
        os.mkdir(downloadPath)
    # 查看是否存在
    if os.path.exists(f"{downloadPath}/{name}"):
        print(f"视频文件已经存在，如需重新下载请先删除之前的视频文件")
        return
    content = requests.get(url, headers=headers).text.split('\n')
    if "#EXTM3U" not in content[0]:
        # raise BaseException(f"非M3U8链接")
        print(f">>>>>>>>>>>非M3U8链接<<<<<<<<")
        return
    # .m3u8 跳转
    for video in content:
        if ".m3u8" in video:
            if video[0] == '/':
                url = url.split('//')[0] + "//" + url.split('//')[1].split('/')[0] + video
            elif video[:4] == 'http':
                url = video
            else:
                url = url.replace(url.split('/')[-1], video)
            print(url)
            content = requests.get(url, headers=headers).text.split('\n')
    urls = []
    for index, video in enumerate(content):
        if '#EXTINF' in video:
            if content[index + 1][0] == '/':
                downloadLink = url.split('//')[0] + "//" + url.split('//')[1].split('/')[0] + content[index + 1]
            elif content[index + 1][:4] == 'http':
                downloadLink = content[index + 1]
            else:
                downloadLink = url.replace(url.split('/')[-1], content[index + 1])
            urls.append(downloadLink)
    allNum = len(urls)
    pool = ThreadPoolExecutor(max_workers=threadNum)
    futures = []
    for index, downloadLink in enumerate(urls):
        fileList.append(os.path.basename(downloadLink))
        futures.append(pool.submit(download, downloadLink, f"{downloadPath}/{os.path.basename(downloadLink)}"))
    wait(futures)
    print(f"运行完成")
    merge_file(downloadPath, name)
    print(f"合并完成")
    print(f"{name}文件下载成功")
    finishedNum = 0
    allNum = 0
    fileList = []


def get_video_pages(videos_url):
    rq = requests.get(videos_url, headers=headers)
    # print(rq.content)
    match = re.findall(r'href="/video/view/(\w+)"', str(rq.content))
    urls = set(match)
    urls = ['https://jiuse021.com/video/view/' + url for url in urls]
    return urls


def get_video_url(page_url):
    rq = requests.get(page_url, headers=headers)
    text = rq.content.decode('utf8')
    match = re.findall(r'https://cdn.jiuse.cloud/hls/\d+/index.m3u8', text)
    if match:
        m3u8_url = match[0]
    else:
        raise ValueError("未找到视频url...")
    title_str = re.findall("<title>([\s\S]*?)</title>", text, re.IGNORECASE)

    if title_str:
        m3u8_title = title_str[0].strip().split('-')[0].strip()
    else:
        raise ValueError("未找到视频title...")
    return m3u8_url, m3u8_title


if __name__ == '__main__':
    threadNum = 50
    start_page = int(input("从第几页开始爬:"))
    pages = ['https://jiuse021.com/video/category/most-favorite/' + str(x) for x in range(start_page, 5000)]

    for page in pages:
        print(f'开始{page}')
        videoUrls = get_video_pages(page)
        for url in videoUrls:
            m3u8_url, title = get_video_url(url)
            print(f'正在下载{page}页面的:\n{title}-{m3u8_url}')
            name = title + ".ts"
            print(name)
            downloader(m3u8_url, name, threadNum)
