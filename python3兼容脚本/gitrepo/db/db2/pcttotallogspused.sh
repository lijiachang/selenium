#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select TOTAL_LOG_USED *1. / TOTAL_LOG_AVAILABLE * 100. from sysibmadm.SNAPDB";`
PctTotalLogSpUsed=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-09-03||'$PctTotalLogSpUsed
