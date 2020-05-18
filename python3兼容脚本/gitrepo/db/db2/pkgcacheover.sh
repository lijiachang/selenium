#!/bin/bash

database=$1
a=`db2 connect to $database;db2 "select PKG_CACHE_NUM_OVERFLOWS from sysibmadm.SNAPDB";`
PkgCacheOverflows=`echo "$a"|awk 'NR==11{print}'|sed s/[[:space:]]//g`
echo '""||""||APM-DB2-07-05||'$PkgCacheOverflows
