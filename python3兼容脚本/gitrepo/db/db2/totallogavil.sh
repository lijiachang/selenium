#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select TOTAL_LOG_AVAILABLE from sysibmadm.SNAPDB";`
TotalLogSpAvail=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-09-02||'$TotalLogSpAvail
