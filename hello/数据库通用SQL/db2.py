#!/usr/bin/env python
# -*- coding:utf-8 -*-

#########################
# excute python2.7.13
# sudo pip install ibm_db
#########################
import ibm_db
# DATABASE：要连接的数据库名
# HOSTNAME：要连接的主机名，一般为主机IP地址
# PORT：数据库的监听端口
# PROTOCOL：网络协议
# UID：数据库用户名
# PWD：数据库用户密码

print (ibm_db.columns.__doc__)