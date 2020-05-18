#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select APPLS_IN_DB2 from sysibmadm.SNAPDB";`
APPLS_IN_CONS=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-03-02||'$APPLS_IN_CONS
