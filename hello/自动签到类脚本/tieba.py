# coding:utf-8

from requests import Session
import time

start_time = time.time()
# 获取cookie 教程http://pandownload.com/faq/cookie.html
# 添加crontab 每天3点执行  
#00 03 * * * python3 /opt/tieba/tieba.py           


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
    'Cookie': 'PSTM=1610543582; BIDUPSID=17111B8D0C5A7464D4ECD710115202A8; BDUSS=GJ-elhITEJZZ1pkaFFqbWJwUHR5bXp2d1JiVDBsZjljRXpwVEY1TnNIeEZieWRnRVFBQUFBJCQAAAAAAAAAAAEAAAA9Ny4rc3VubnnKq9LiOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEXi~19F4v9fS; BDUSS_BFESS=GJ-elhITEJZZ1pkaFFqbWJwUHR5bXp2d1JiVDBsZjljRXpwVEY1TnNIeEZieWRnRVFBQUFBJCQAAAAAAAAAAAEAAAA9Ny4rc3VubnnKq9LiOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEXi~19F4v9fS; bdshare_firstime=1610763656012; rpln_guide=1; BAIDUID=810C4126106CB42F23CEA078788593CA:FG=1; __yjs_duid=1_11cae456603cd65c805dd4aabca14b6f1619102427467; MCITY=-131%3A; STOKEN=d119a1c772db5894b7d35e984008bb7fec88574a3f2644a356102c0f887f2e9c; BAIDU_WISE_UID=wapp_1630215121969_983; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=1; H_PS_PSSID=34436_34497_31254_33848_34092_34107_34507_26350_34428_34319_22160; BA_HECTOR=202k040l84a00h2hvm1gise9u0q; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1629811987,1629812007,1630215121,1630419719; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1630419719; 724449085_FRSVideoUploadTip=1; USER_JUMP=-1; video_bubble724449085=1',
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
    time.sleep(2)
end_time = time()
t = end_time - start_time
l = len(bars)
failed = "\n失败列表：" + '\n'.join(failed_bar) if len(failed_bar) else ''
print(f'''共{l}个吧，其中: {succees}个吧签到成功，{len(failed_bar)}个吧签到失败，{already_signed}个吧已经签到。{failed}
此次运行用时{t}s。''')
with open(log_path, 'w') as f:  # 日志记录
    for log in logs:  # 日志记录
        f.write(str(log) + '\n')  # 日志记录