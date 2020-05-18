# coding:utf-8

import paramiko
import logging

"""
用途：目标主机使用root用户，创建agent用户，并设置用户密码
By 李家昌，最后修改于 2018.03.22
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
    agent_info = info.split("Please input Agent IPAddress User Password：")[1].strip()
    f.close()

    for line in agent_info.split("\n"):
        host = line.split()[0]
        port = line.split()[1]
        username = line.split()[2]
        password = line.split()[3]
        print("########### %s ###########" % host)
        conn = SSHConnection(host, port, username, password)

        conn.exec_command("cat /etc/redhat-release")
        conn.exec_command("groupadd agent")
        conn.exec_command("mkdir -p /opt/ultrapower/UltraAgent")
        conn.exec_command("useradd -d /opt/ultrapower/UltraAgent -g agent -m agent")
        conn.exec_command("chown -R agent:agent /opt/ultrapower/UltraAgent")
        conn.exec_command("echo 'sigmam' | passwd --stdin agent")

        conn.close()

