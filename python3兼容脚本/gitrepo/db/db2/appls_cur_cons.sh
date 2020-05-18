#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select APPLS_CUR_CONS from sysibmadm.SNAPDB";`
APPLS_CUR_CONS=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-03-01||'$APPLS_CUR_CONS
