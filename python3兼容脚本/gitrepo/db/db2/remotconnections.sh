#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select REM_CONS_IN from sysibmadm.snapdbm";`
RemConnectsToDBM=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-04-05||'$RemConnectsToDBM
