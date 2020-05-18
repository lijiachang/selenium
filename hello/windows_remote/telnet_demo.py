# coding: utf-8

import telnetlib
import time
import logging

"""
使用telnet 模块，远程Windows机器 FTP命令下载介质，解压，替换，运行agent
By 李家昌，最后修改于 2018.04.25
"""
logger = logging.getLogger()  # 生成logging对象
hdlr = logging.FileHandler("telnet.log")  # 日志名和生成位置
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")  # 生成日志内容的格式
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


class Telnet(object):
    def __init__(self, ip, username, password, install_path):
        self._ip = ip
        self._username = username
        self._password = password
        self._install_path = install_path
        self._telnet = None
        self._connect()

    # 建立连接
    def _connect(self):
        if self._telnet is None:
            self._telnet = telnetlib.Telnet(self._ip)
        self._telnet.read_until("login:")
        self._telnet.write(self._username + "\r\n")
        self._telnet.read_until("password:")
        self._telnet.write(self._password + "\r\n")
        logger.info(self._telnet.read_until("C:\Documents and Settings\Administrator>"))
        logger.info("Telnet %s is connected !" % ip)
        print("Telnet %s is connected !" % ip)

    # 创建agent目录
    def mkdir(self):
        self._telnet.write("md {0}\r\n".format(self._install_path))
        self._telnet.write("cd {0}\r\n".format(self._install_path))
        logger.info(self._telnet.read_until("C:\ultrapower\UltraAgent>"))

    # 登录FTP下载介质
    def ftp_download(self):
        self._telnet.write("ftp\r\n")
        self._telnet.write("open 192.168.26.117\r\n")
        self._telnet.write("Anonymous\r\n")
        self._telnet.write("Anonymous\r\n")
        self._telnet.write("dir\r\n")
        self._telnet.write("get UltraAgent_win.zip\r\n")
        self._telnet.write("bye\r\n")
        tmp = self._telnet.read_until("Goodbye.")
        print(tmp.decode('GB2312'))

    # 解压agent介质
    def start_rar(self):
        self._telnet.write("start winrar x -y UltraAgent_win.zip\r\n")
        time.sleep(3)  # 等待三秒 解压完成
        tmp = self._telnet.read_until(">")
        print(tmp.decode('GB2312'))

    # 替换agent配置文件
    def replace_cfg(self):
        self._telnet.write("cd config\r\n")
        self._telnet.write("""write_cfg.bat C:\ultrapower\UltraAgent\config\cfg.json "192.168.95.113:58433" "'192.168.95.112:58433','192.168.95.113:58433'"\r\n""")
        tmp = self._telnet.read_until(">")
        print(tmp.decode('GB2312'))
        tmp = self._telnet.read_until(">")
        print(tmp.decode('GB2312'))

    # 运行agent程序
    def run_agent(self):
        self._telnet.write("cd ../bin\r\n")
        self._telnet.write("ultraagent -c ../config/cfg.json\r\n")
        tmp = self._telnet.read_until("bin>")
        print(tmp.decode('GB2312'))
        tmp = self._telnet.read_until("bin>")
        print(tmp.decode('GB2312'))






# ip.info 配置文件读取
f = open("ip.info")
info = f.read()
agent_info = info.split("Please input Agent IPAddress User Password：")[1].split("Please input transfer IP ：")[0].strip()
transfer_info = info.split("Please input transfer IP ：")[1].split("Please input install_path:")[0].strip()
transfer_ips = transfer_info.split("\n")
install_path = info.split("Please input install_path:")[1].strip()
f.close()

for line in agent_info.split("\n"):
    ip = line.split("/")[0]
    username = line.split("/")[1]
    password = line.split("/")[2]
    print("########### %s ###########" % ip)
    telnet = Telnet("192.168.180.56","administrator","cpzl_135",install_path)
    telnet.mkdir()
    telnet.ftp_download()
    telnet.start_rar()
    telnet.replace_cfg()
    telnet.run_agent()

    # tn = telnetlib.Telnet("192.168.180.56")
    # tn.read_until("login:")
    # tn.write(username + "\r\n")
    # tn.read_until("password:")
    # tn.write(password + "\r\n")
    # tmp = tn.read_until("C:\Documents and Settings\Administrator>")
    # logger.info(tmp)
    # logger.info("Telnet %s is connected !" % ip)
    # #  创建agent目录
    # tn.write("md {0}\r\n".format(install_path))
    # tn.write("cd {0}\r\n".format(install_path))
    # tn.write("dir\r\n")
    # tmp = tn.read_until(">")
    # print(tmp.decode('GB2312'))
    # # 登录FTP，下载agent介质
    # tn.write("ftp\r\n")
    # tn.write("open 192.168.26.117\r\n")
    # tn.write("Anonymous\r\n")
    # tn.write("Anonymous\r\n")
    # tn.write("dir\r\n")
    # tn.write("get UltraAgent_win.zip\r\n")
    # tn.write("bye\r\n")
    # tmp = tn.read_until(">")
    # print(tmp.decode('GB2312'))
    # # 解压agent介质
    # tn.write("start winrar x -y UltraAgent_win.zip\r\n")
    # time.sleep(3)  # 等待三秒 解压完成
    # tmp = tn.read_until(">")
    # print(tmp.decode('GB2312'))
    # # 替换配置文件 cfg.json
    # tn.write("cd config\r\n")
    # tn.write("""write_cfg.bat C:\ultrapower\UltraAgent\config\cfg.json "192.168.95.113:58433" "'192.168.95.112:58433','192.168.95.113:58433'"\r\n""")
    # tmp = tn.read_until(">")
    # print(tmp.decode('GB2312'))
    # # 运行agent程序
    # tn.write("cd ../bin\r\n")
    # tn.write("ultraagent -c ../config/cfg.json\r\n")
    # tmp = tn.read_until(">")
    # print(tmp.decode('GB2312'))
    # while True:
    #     tmp = tn.read_until(">", 1)
    #     print(tmp.decode('GB2312', 'ignore'))
