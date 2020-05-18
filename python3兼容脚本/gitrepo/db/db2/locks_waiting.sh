#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select LOCKS_WAITING from sysibmadm.SNAPDB";`
LOCKS_WAITING=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-03-03||'$LOCKS_WAITING
