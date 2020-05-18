#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select LOCAL_CONS_IN_EXEC from sysibmadm.snapdbm";`
LOCAL_CONS_IN_EXEC=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-04-04||'$LOCAL_CONS_IN_EXEC
