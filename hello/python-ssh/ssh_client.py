# coding:utf-8

import paramiko
import logging

"""
By 李家昌，最后修改于 2018.03.26
"""
logger = logging.getLogger()  # 生成logging对象
hdlr = logging.FileHandler("auto.log")  # 日志名和生成位置
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")  # 生成日志内容的格式
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


class SSHConnection(object):
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._transport = None
        self._sftp = None
        self._client = None
        self._connect()

    # 建立连接
    def _connect(self):
        transport = paramiko.Transport(self._host, self._port)
        transport.connect(username=self._username, password=self._password)
        self._transport = transport

    # 执行命令
    def exec_command(self, command, get_stout=True):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        stdin, stdout, stderr = self._client.exec_command(command)

        data = stdout.read()
        err = stderr.read()
        if get_stout and len(data) > 0:
            print(data.strip())
            return data
        if len(err) > 0:
            print(err.strip())
            return err

    # 下载
    def get(self, remote_path, local_path):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.get(remote_path, local_path)

    # 上传
    def put(self, local_path, remote_path):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.put(local_path, remote_path)

    # 关闭连接
    def close(self):
        if self._transport:
            self._transport.close()
        if self._client:
            self._client.close()


if __name__ == "__main__":

    # ip.info 配置文件读取
    f = open("ip.info")
    info = f.read()
    agent_info = info.split("Please input Agent IPAddress User Password：")[1].split("Please input transfer IP ：")[0].strip()
    transfer_info = info.split("Please input transfer IP ：")[1].split("Please input install_path:")[0].strip()
    transfer_ips = transfer_info.split("\n")
    install_path = info.split("Please input install_path:")[1].strip()
    f.close()

    for line in agent_info.split("\n"):
        host = line.split("/")[0]
        port = 22
        username = line.split("/")[1]
        password = line.split("/")[2]
        print("########### %s ###########" % host)
        conn = SSHConnection(host, port, username, password)
        logger.info("%s connected !" % host)
        conn.exec_command("cat /etc/redhat-release")
        conn.exec_command("mkdir -p %s" % install_path)
        conn.put("./UltraAgent.tar.gz", "%sUltraAgent.tar.gz" % install_path)
        logger.info("UltraAgent.tar.gz文件传输成功！")
        conn.exec_command(
            "tar -zxvf {0}UltraAgent.tar.gz -C {0}".format(install_path), get_stout=False)
        logger.info("UltraAgent.tar.gz解压成功！")
        conn.exec_command("cp -f {0}sedfile/cfg.json {0}config/".format(install_path))
        for index in range(len(transfer_ips)):
            if index == 0:
                conn.exec_command("sed -i -e '/\"addrs\"\: \[/a\            \"{0}\"' {1}config/cfg.json".format(transfer_ips[index].strip(), install_path))
            else:
                conn.exec_command("sed -i -e '/\"addrs\"\: \[/a\            \"{0}\",' {1}config/cfg.json".format(transfer_ips[index].strip(), install_path))
        logger.info("UltraAgent/config/cfg.json 配置文件已修改！")
        # conn.exec_command("sed -i 's/$1/{0}/g' {1}setagent.sh".format(transfer_info,install_path))
        ##conn.exec_command(
        ##    "{0}python2.7/bin/python2.7 {0}ultrapy/sigmam/middleware/zookeeper/get_zookeeper.py 192.168.95.114 52181".format(install_path))

        #conn.exec_command("{0}setagent.sh".format(install_path))
        conn.exec_command("{0}bin/control start".format(install_path))

        logger.info("主机 %s 执行完毕" % host)
        conn.close()

