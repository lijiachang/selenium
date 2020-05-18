#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select DEADLOCKS from sysibmadm.SNAPDB";`
NumDeadlocks=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-05-01||'$NumDeadlocks
