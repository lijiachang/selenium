# coding=utf-8

import winrm

win2008 = winrm.Session("http://122.14.214.236:5985/wsman", auth=("administrator", "uWFvkltUym"))

info = win2008.run_cmd("dir")
print(dir(winrm.Session))
print(info.std_out.decode())
print(info.std_err)