# coding:utf-8

from requests import Session
from time import time

start_time = time()
# 获取cookie 教程http://pandownload.com/faq/cookie.html

# 数据
log_path = f"./sign_log_{int(start_time)}.txt"  # 日志记录
like_url = 'https://tieba.baidu.com/mo/q/newmoindex?'
sign_url = 'http://tieba.baidu.com/sign/add'
tbs = '4fb45fea4498360d1547435295'
head = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'PSTM=1592312119; BAIDUID=3971EB494DA29FDF6EA2A9BCE3A4ED83:FG=1; BIDUPSID=00B7794521B7B2C939BCBA01A63D0050; BDUSS=tDeXF3Tzdhd0o0bmZPSUVxNWowZm5HY0RaYzZJQVktOU9KVGpEd0hRLWh5eFpmRVFBQUFBJCQAAAAAAAAAAAEAAAA9Ny4rc3VubnnKq9LiOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKE-716hPu9eM2; PANWEB=1; SCRC=5411f726f45f1c2a2da7b7c48bd2ce9a; STOKEN=5ce33c895d5ca45cf61421b5df631cc08b68fab80c55cbe8aa0404481dfc2a30; BDUSS_BFESS=tDeXF3Tzdhd0o0bmZPSUVxNWowZm5HY0RaYzZJQVktOU9KVGpEd0hRLWh5eFpmRVFBQUFBJCQAAAAAAAAAAAEAAAA9Ny4rc3VubnnKq9LiOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKE-716hPu9eM2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDCLND=%2FT%2FwYzpGibgqv8pgVYr1irSqwiXveX6MeCbprLywDz8%3D; H_PS_PSSID=7514_32606_1435_32573_32532_31254_32045_32115_32692_32583; __51cke__=; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1598062728,1598680093,1598769953,1598770050; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1598770050; __tins__19988117=%7B%22sid%22%3A%201598769954476%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201598771850303%7D; __51laig__=2; PANPSC=12551764619077206886%3Ajz2MdbBpuFxEvOPUgG7avzuv496EomYG5aWgeycxypr1G%2FM%2FwafI7M67BL4HeBCFEzh0OPEF2WlHW0I9s5N4Nmq6skESXUy0oayFpxjiJIfwnVz51Wwfo72A8Uov%2BABb4Q75Q2NJoS4zHA%2BRirEa8TGuaZCjAuzWYqZdy9zZ13nFd%2BczPBNYtzaPJvsmh0iKjFY%2Fj%2FLBUWg%3D',
    'Host': 'tieba.baidu.com',
    'Referer': 'http://tieba.baidu.com/i/i/forum',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/71.0.3578.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'}
s = Session()

# 获取关注的贴吧
bars = []
dic = s.get(like_url, headers=head).json()['data']['like_forum']
for bar_info in dic:
    bars.append(bar_info['forum_name'])

# 签到
already_signed_code = 1101
success_code = 0
need_verify_code = 2150040
already_signed = 0
succees = 0
failed_bar = []
logs = []  # 日志记录
n = 0

while n < len(bars):
    bar = bars[n]
    data = {
        'ie': 'utf-8',
        'kw': bar,
        'tbs': tbs
    }
    try:
        r = s.post(sign_url, data=data, headers=head)
    except Exception as e:
        print(f'未能签到{bar}, 由于{e}。')
        failed_bar.append(bar)
        continue
    dic = r.json()
    msg = dic['no']
    if msg == already_signed_code:
        already_signed += 1; r = '已经签到过了!'
    elif msg == need_verify_code:
        n -= 1; r = '需要验证码，即将重试!'
    elif msg == success_code:
        r = f"签到成功!你是第{dic['data']['uinfo']['user_sign_rank']}个签到的吧友,共签到{dic['data']['uinfo']['total_sign_num']}天。"
    else:
        r = '未知错误!' + dic['error']
    print(f"{bar}：{r}")
    succees += 1
    logs.append(dic)  # 日志记录
    n += 1
end_time = time()
t = end_time - start_time
l = len(bars)
failed = "\n失败列表：" + '\n'.join(failed_bar) if len(failed_bar) else ''
print(f'''共{l}个吧，其中: {succees}个吧签到成功，{len(failed_bar)}个吧签到失败，{already_signed}个吧已经签到。{failed}
此次运行用时{t}s。''')
with open(log_path, 'w') as f:  # 日志记录
    for log in logs:  # 日志记录
        f.write(str(log) + '\n')  # 日志记录