#!/usr/bin/env python
import subprocess
import sys


def outputs(command):
    ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdo = ps.stdout.readlines()
    stdos = [line.decode('utf-8').strip("\n") for line in stdo]
    return stdos


try:
    file_max = outputs('cat /proc/sys/fs/file-max')
    file_handle = outputs('cat /proc/sys/fs/file-nr')
    pid_max = outputs('cat /proc/sys/kernel/pid_max')
except Exception as e:
    print("||%s||FM-PLUGIN-EXECUTE-FAILED||Error:%s." % (sys.argv[0], e))
    sys.exit(0)

res_file_max = '""||""||kernel_file_max||' + file_max[0]
res_file_handle_allo = '""||""||kernel_file_handle_allo||' + file_handle[0].split('\t')[0]
res_file_handle_allo_noused = '""||""||kernel_file_handle_allo_noused||' + file_handle[0].split('\t')[1]
res_pid_max = '""||""||kernel_pid_max||' + pid_max[0]
print(res_file_max + '\n' + res_file_handle_allo + '\n' + res_file_handle_allo_noused + '\n' + res_pid_max)
