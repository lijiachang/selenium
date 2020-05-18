# coding=utf-8

"""
socket 服务端 、客户端


"""

import socket

"""
AF_INET 基于网络ip的通讯 ； AF_UNIX 基于本地文件的通讯
**在AF_INET下，以元组（host,port）的形式表示地址。
SOCK_STREAM基于tcp/ip   ； SOCK_DGRAM基于udp
"""
# 服务端
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
s.bind(("127.0.0.1", 8848))  # 绑定ip和端口
s.listen(8)  # 同时允许多少个请求
while True:
    connection, address = s.accept()  # 得到接受到的请求 （tupl）
    buf = connection.recv(1024)  # 抓取的字节数，后面的不要
    connection.send(buf)  # 接受到后再抛出，做测试。。

s.close()

# 客户端
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8848))
s.sendall(bytes("Hi!"))
s.close()
