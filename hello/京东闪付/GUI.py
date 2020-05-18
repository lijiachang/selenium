# coding:utf-8

import Tkinter as tk
import tkMessageBox
import httplib  # python3.0 : import http.client
#import requests
from requests import get
import time
import threading
from os import remove
from base64 import b64decode

img = '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3/8Ygdv/NInK/3vD4/93vt3/NICy/xl6yv8ehd3/T6Pk/4bJ6/9wtdP/ZafF/zSO0f8bgtr/Wqrb/4nQ7v+K0O3/Ya/m/yCG3f8Yf9b/RZLH/4nN6v+Fzu3/gs7t/3q2z8QxRk8VOFJcAAEBAQAAAAAAfbzVAFuImkuDxuLyiNDu/4nQ7v+J0O7/iM7r/3Cxzv84gbH/GXzO/yaK3v9ns+r/j9Lx/2234f8fhdr/Mo/Y/4XI5/9wuOn/LY7f/xmA2P8id7n/Vpu+/3/J6P+Fzu3/fMHd/0mOtf8desb/G4Td/0Ca4v97wu3/jNDu/0Kd3/8agtr/Wqvb/43Q7/9frub/I4je/xl+0v8ufbT/crPR/4vQ7v+Fz+3/g87t/4bH4/NeiZpPisrkAAAAAAAZJisAAAAABm6nvpqJz+z/ic/u/4rQ7v+K0O7/itDu/4rR7/9+wd3/P4i3/xl90f8ee8j/ZKjP/2y24P8fhdr/MpDZ/3y/3/83h8L/F3jJ/y97sv9nqsn/g83r/4TO7f+Gzuz/iNDu/4XK5v9PlLv/HHvI/xh+1P81hL7/gcTh/0Od3/8agtr/WqnZ/1ek1v8dg9r/GnrK/zmCsf9zudb/jNHv/4zQ7v+Iz+7/gs7t/4nP7P90qcChAAAACB4sMgBbhpgAUXeGK32+2N+I0O7/ic/t/4rQ7v+J0O7/i9Du/4rQ7v+K0e//fLzc/0WJuP9Zlrv/icTh/2+34v8fhdr/M5Da/4jI6P92sdH/VZO5/3262f+N0e//h8/t/4fP7P+Iz+3/ic/t/4vR7/+Hyeb/UZS8/zyEsf9xs8//i8/q/0Od3/8agtr/XKva/2Kmxv8teq//UJK3/4PG4f+H0O7/idDu/4nQ7v+Hz+3/hs/t/4rQ7v+CwdvkVXuLMmWTpgCQ1fIAcqe+XYfM6fyHz+7/ic/t/4nP7v+K0O7/itDu/4rQ7v+Fy+n/SZ/e/y+O3f87leH/Qprj/zaS3/8chNz/I4jd/z6X4f8+l+L/M5Lg/0ed3v+Gyur/itDu/4jP7f+Iz+3/iM/u/4fM7f9SpeT/TqDf/1+p3/9vuOr/c7rp/zuX4P8bg9v/UKPf/3K66P9ortr/cLbl/3G56f+Ey+z/hs/t/4jP7f+Hz+3/hc7t/4nQ7v+Kzer+davBaZbb+QCW3PsAgr3XgInO7P+Iz+7/iM/t/4jP7f+L0O7/itDu/4vQ7v+Hzev/PJbY/xmB2f8heLz/JXSw/yV1sf8ndbH/JXWx/yR0sP8jeLv/GoLa/zKO1f+Bx+f/itDu/4nQ7f+Hz+3/hc7s/2iz4P8ehNv/GoPc/xuC2f8aftL/G37S/xyC2f8chNz/HIHW/xx/1P8cgtf/HILZ/yOG2P9vveT/hs/t/4bO7f+K0O7/itDt/4rQ7v+Kz+z/hcTeiJbd/ACL1PIAh8jjionP7P+K0O7/idDu/4nQ7v+K0O7/itDu/4vQ7v+Izuz/P5nZ/x2D2f9hqdP/gsHb/4HA2/+AwNv/f8Db/4LB2/9qsNf/H4Xb/zeT2P+Dyun/itDu/4vQ7v+Jz+3/iM/t/2iqy/8lerv/GoPb/yeByf9KibD/SYmu/yuFy/8bg9v/NYS7/z+Erf85ga7/M3us/zB7rv9xudr/iNDu/4bP7f+Hz+3/hs7t/4XO7P+K0O3/js/rkZDX9QCL0/EAicrlfYnP7f+K0O7/iM/u/4rQ7v+L0O7/itDu/4nQ7v+Hz+3/P5rc/x2E2/9Vp+P/cLrr/2+56/9uuev/brnr/2+66/9brOb/Hobd/zeT2v+Eyur/itDu/4vQ7v+K0O7/i9Du/43Q7P9mp8f/I3zC/yKI3f9uuen/jtHt/z6a3/8Ygdr/WKrg/4nP6/+IzOj/hcjl/4DF4v+Hzev/itDu/4rQ7v+Hz+3/hs/t/4jP7f+Kz+3/jM3piY7S7wCN0OwAjs7qVIzQ7fqL0O7/idDu/4nQ7v+K0O7/i9Du/4nQ7v+Gzev/OpPV/xd6zv8Yecr/GHjI/xh4yP8YeMj/GHjI/xh4yP8Yecr/F3vP/y6Jz/9/x+j/itDu/43R7v+M0O7/jtLu/5HT7/+N0Oz/V5zC/x1/z/8zkuD/e7/k/z6Huf8qdq3/T5S//4vO6v+O0u//jdLv/4zS7/+N0u7/jNHu/4rQ7v+J0O7/iM/t/4vQ7v+L0O39js7qYY3Q7ACS0OsAk9HrII/Q7deM0O7/itDu/4nQ7v+K0O7/jNDu/4vN7v+Jyej/Wpm//0+NtP9blbf/YJm5/2CYuf9emLj/X5i5/2CYuf9dlrf/UI20/1WTuv+FxeX/jc3u/4/R7v+N0e7/gMTq/3W66v95v+v/crfh/zOM0f8ag9z/TKHh/3Cz2/9vsdr/dLfh/3q/6v97wOv/eL7r/3K66v90u+n/iMzs/43R7v+K0O7/iM/t/4rQ7v+P0O3fkdDrJ5DQ6wCR0OsAV8n6AI7Q7IaK0O3/ic/u/4vQ7v+L0e7/gcfp/0CZ4P81lOL/NpTh/0CZ4v9InuX/SJ7m/0ie5f9InuT/SJ7k/0ie5f9InuX/QZni/zeU4f81lOL/O5bf/3/F6P+N0Oz/RZrX/xqA2P8cgdb/HIHW/xp+0v8agdj/HITc/x+F2v8df9P/HH/S/xyA1f8cgNX/HIHW/xuB2P8ihNb/c7vj/47S7v+Hz+3/iNDt/4zQ7f+Q0OyTmdDmApLQ6wCR0OsAjtDrAI7Q6zaKz+3qiM/t/4rQ7v+M0e//e8Di/yd9vv8Zcrr/G3O5/x1ytv8ec7X/HnO1/x15wv8agtv/GoDW/x50uf8ec7X/HXO3/xtzuf8acrr/IHi8/3W63f+Mz+v/UJW+/zR7rP87ga7/PoSw/0aHrf8sf77/G4Td/ySCzv9Mi7L/S4uv/0GFr/8/g6//O4Gu/zV9rP82fq7/dbjZ/4vR7/+Hz+7/itDu/43Q7e6Q0Os9j9DrAJDQ6gCT0esAj8/rAJDP6giLz+yuitDt/4vQ7v+L0O7/h8vo/26uy/9rq8j/ba3K/3Gxzv90tND/drTQ/06c0f8ag9z/J4bR/2ipyP92tdH/c7HN/26tyv9sq8j/a6zJ/4XI5f+N0e7/iczo/4jK5v+IzOn/ic7q/47R7P9dpM3/HILW/x6E2/9bqN7/j9Ht/4vP6/+Lzur/iszo/4bK5v+HyeX/i8/s/4nQ7v+Hz+3/iM/t/4/Q7LGT0OoJkdDrAJPR6wAAAAAAls/pAIvP6wCNz+tai9Dt+ojP7v+Hz+3/itDu/43S8P+M0vD/i9Lw/43S8P+O0/D/jdHu/1Wbxf8jcq7/PIa5/4fJ5v+P0/D/jtPw/4zS8P+M0vD/itLw/43R7/+N0e7/jdHu/43R7v+K0O7/i9Du/43S7/95vd3/LH68/y14rv9Ul7z/is3q/4zR7v+N0e7/jtHu/43R7v+N0e7/jdHu/4rQ7v+Hz+3/idDt+ZDQ7FmO0OwArtzrAAAAAAAAAAAAkNDrAIrP6QCKz+kZic/s0IXO7f+Gz+3/i9Du/4vQ7v+J0O7/i9Du/4vQ7v+M0O7/jNDu/4bI5f99vtn/gcLe/4zQ7f+N0e7/i9Du/4vQ7v+M0O7/idDu/4vQ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'
PAGE10 = r"https://pa.jd.com/prize/center/h5/draw?entranceKey=b183f8bdcc5077fe87d813847047e95b"
PAGE14 = r"https://pa.jd.com/prize/center/h5/draw?entranceKey=8581c41185dbd6e9e8c13a2c744d4636"
PAGE20 = r"https://pa.jd.com/prize/center/h5/draw?entranceKey=f513f407cdb3a7b675f2ac13b00b56a2"


# Cookies 处理
def update_cookie_list():
    try:
        global cookie_list_dict
        cookie_list_dict = list()
        for one_cookie in cookie_list:
            cookie_tmp = {}
            for line in one_cookie.split(';'):
                name, value = line.strip().split('=', 1)
                cookie_tmp[name] = value
            cookie_list_dict.append(cookie_tmp)
    except:
        tkMessageBox.showwarning(title="提示", message="Cookie格式有误！")


def get_webtime(host):
    conn = httplib.HTTPConnection(host)
    conn.request("GET", "/")
    r = conn.getresponse()
    ts = r.getheader('date')  # 获取http头date部分
    # 将GMT时间转换成北京时间
    ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    ttime = time.localtime(time.mktime(ltime) + 8 * 60 * 60)
    tm = "%02u:%02u:%02u" % (ttime.tm_hour, ttime.tm_min, ttime.tm_sec)
    return tm


#  点击添加按钮
def add_cookie_click():
    if entry.get() == "":
        tkMessageBox.showwarning(title="提示", message="请输入Cookie再添加！")
    else:
        cookie_list.append(entry.get().strip())
    print(cookie_list)
    var1.set(tuple(cookie_list))
    update_cookie_list()
    entry_text.set("")
    print(cookie_list_dict)


def add_localfile_cookies():
    try:
        with open('cookie.info', 'r') as f:
            read_lines = f.readlines()
            print(read_lines)
            for one_line in read_lines:
                cookie_list.append(one_line.strip())
        # print(cookie_list)
    except Exception:
        print("Not found localfile:cookie.info")
    update_cookie_list()  # 本地文件cookies更新到界面中
    var1.set(tuple(cookie_list))


root = tk.Tk()  # 生成root主窗口
var1 = tk.StringVar()
cookie_list = list()  # 原始cookie 列表
cookie_list_dict = list()  # 处理过后cookie 列表
add_localfile_cookies()  # 读取本地cookies文件

tmp = open("tmp.ico", "wb+")
tmp.write(b64decode(img))
tmp.close()
root.iconbitmap("tmp.ico")
remove("tmp.ico")
# root.iconbitmap(r"./t.ico")  # 窗口图标
root.geometry('500x400+600+400')  # 设置默认窗口的大小宽x高+偏移量
#root.resizable(False, False)  # 固定窗口大小
root.title("京东闪付5元 V1.8  作者QQ944581577")

frame_top = tk.Frame(root)
frame_top.pack()
frame_left = tk.Frame(root)
frame_left.pack(side="left")
frame_right = tk.Frame(root)
frame_right.pack(side="right")
frame_bottom = tk.Frame(root)
frame_bottom.pack(side="bottom")

lable123 = tk.Label(frame_top, text="添加Cookie:", font=(15))
lable123.pack(side="left")
entry_text = tk.StringVar()
entry = tk.Entry(frame_top, width=35, text=entry_text)
entry.pack(side="left")
button1 = tk.Button(frame_top, text="添加", command=add_cookie_click)
button1.pack(side=tk.LEFT)


def test_click():
    print(cookie_list)
    init_check()
    text.see(tk.END)  # 一直显示最新的一行
    text.update()


def del_listbox():
    del cookie_list[listbox.curselection()[0]]
    var1.set(tuple(cookie_list))
    update_cookie_list()
    print(cookie_list_dict)


# Cookie列表：
label_cookie_list = tk.Label(frame_left, text="Cookie列表：", font=(5))
label_cookie_list.pack()
frame_left_l = tk.Frame(frame_left)
frame_left_l.pack()
listbox = tk.Listbox(frame_left_l, listvariable=var1, bg="#FFFAFA")
listbox.pack(side="left", fill=tk.BOTH, expand=1)
# bar = tk.Scrollbar(frame_left_l, command=listbox.yview)
# bar.pack(side="right",fill=tk.Y)
# listbox.config(yscrollcommand=bar.set)
button_listbox_del = tk.Button(frame_left, text="删除选中", bg="#EE2C2C", command=del_listbox)
button_listbox_del.pack()

label_log = tk.Label(frame_right, text="日志：", font=(5))
label_log.pack()
text = tk.Text(frame_right, height=15, width=30, bg="#7A7A7A")  # 日志输出
#  键盘输入不会被插入到文本框:
text.bind("<KeyPress>", lambda e: "break")
text.pack()

# 京东和本地 时间对比
time_local_text = tk.StringVar()
label_local_time = tk.Label(frame_bottom, textvariable=time_local_text, font=("Arial Black", 10), fg="red").pack()
time_jd_text = tk.StringVar()
label_jd_time = tk.Label(frame_bottom, textvariable=time_jd_text, font=("Arial Black", 10), fg="red").pack()

label_jd_time2 = tk.Label(frame_bottom, text="提示：本地时间调成京东时间！软件免费使用！", wraplength=150, justify='left',
                          font=("Arial Black", 9), fg="black").pack()


def update_time():
    time_local_text.set("本地时间：" + time.strftime('%H.%M.%S', time.localtime(time.time())))
    time_jd_text.set("京东时间：" + get_webtime('www.jd.com'))


#####  京东时间 ######
# def time_compare():
#     text.insert("end", u"京东时间" + get_webtime('www.jd.com') + "\n")
#     text.insert("end", u"本机时间" + time.strftime('%H:%M:%S', time.localtime(time.time())) + "\n")
# time_compare()

button2 = tk.Button(root, text="检查所有cookie", bg="#9ACD32", command=test_click)  # 测试按钮 test
button2.pack(side=tk.LEFT)


def update_data(PAGE, cookie):
    html = get(PAGE, cookies=cookie)
    return html.text
    # soup = BeautifulSoup(html.text, "html.parser")
    # return soup.text


def init_check():
    print(cookie_list_dict)
    for one_cookie in cookie_list_dict:
        data_info = update_data(PAGE20, one_cookie)
        print(data_info)
        if "RULE_ERROR__00118" in data_info or "RULE_ERROR__00005" in data_info:
            text.insert("end", "Cookie检查：OK\n")
        elif u"登录后才可以领奖" in data_info:
            text.insert("end", "Cookie无效或过期，请检查！\n")
        elif u"请求参数不正确" in data_info or u"调用营销系统失败" in data_info:
            text.insert("end", "Cookie检查：OK\n")
        else:
            text.insert("end", "code:%s\n" % data_info)
        time.sleep(0.8)
    text.see(tk.END)  # 一直显示最新的一行
    text.update()

def judge_result(page, one_cookie):
    while True:
        result = update_data(page, one_cookie)
        print(result)
        # if '"state":0' in result:  # 解决 {"subRuleData":"请求参数不正确，请与研发人员联调好后，在继续调用","state":0}
        #     time.sleep(1)
        #     continue
        if u"今日已领取" in result or "prizeDesc" in result:
            text.insert("end", "【{0}:00】领取成功！\n".format(time.strftime('%H', time.localtime(time.time()))))
            break
        if u"登录后才可以领奖" in result:
            text.insert("end", "Cookie 已失效，请重新提取！\n")
            break
        else:
            time.sleep(0.8)
        text.see(tk.END)  # 一直显示最新的一行
        text.update()


def update_page():
    now = time.strftime('%H.%M', time.localtime(time.time()))
    now2 = time.strftime('%H.%M.%S', time.localtime(time.time()))
    # update_time()
    print(now2)
    if now == "10.00":
        threads = []
        for one_cookie in cookie_list_dict:
            t = threading.Thread(target=judge_result, args=(PAGE10, one_cookie,))  # 注意args后面有（）里面还有逗号,
            threads.append(t)
        for thread in threads:
            thread.start()
        time.sleep(62)
    if now == "14.00":
        threads = []
        for one_cookie in cookie_list_dict:
            t = threading.Thread(target=judge_result, args=(PAGE14, one_cookie,))  # 注意args后面有（）里面还有逗号,
            threads.append(t)
        for thread in threads:
            thread.start()
        time.sleep(62)
    if now == "20.00":
        threads = []
        for one_cookie in cookie_list_dict:
            t = threading.Thread(target=judge_result, args=(PAGE20, one_cookie,))  # 注意args后面有（）里面还有逗号,
            threads.append(t)
        for thread in threads:
            thread.start()
        time.sleep(62)

    global timer
    timer = threading.Timer(0.5, update_page)
    timer.start()

    update_time()  # 更新时间放到后面，前面会出问题


timer = threading.Timer(0.5, update_page)
timer.start()


# 确认退出的同时，写入cookie到本地
def close_window():
    exit_result = tkMessageBox.askokcancel(title="确认退出？", message="确认要关闭吗？")
    if exit_result:
        # if cookie_list:  # 如果有cookie列表，就保存到本地
        f = open('cookie.info', 'w')
        for one_cookie in cookie_list:
            #print(one_cookie)
            f.write(one_cookie + "\n")
        f.close()
        timer.cancel()  # 停止 Threading.Timer 定时器
        root.destroy()
    else:
        return


root.protocol("WM_DELETE_WINDOW", close_window)

root.mainloop()
