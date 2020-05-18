#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select LOCAL_CONS from sysibmadm.snapdbm";`
LocConnectsToDBM=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-04-03||'$LocConnectsToDBM
