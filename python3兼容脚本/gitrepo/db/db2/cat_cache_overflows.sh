#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select CAT_CACHE_OVERFLOWS from sysibmadm.SNAPDB";`
CAT_CACHE_OVERFLOWS=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-07-07||'$CAT_CACHE_OVERFLOWS
